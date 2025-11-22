import discord
from discord.ext import commands
from discord import app_commands
import re
from collections import defaultdict
import time
import config
from bot.utils.database import db
import logging

logger = logging.getLogger(__name__)

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_tracker = defaultdict(list)  # {user_id: [timestamps]}
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Verificar mensajes para automoderación"""
        # Ignorar bots y mensajes sin servidor
        if message.author.bot or not message.guild:
            return
        
        # Ignorar administradores
        if message.author.guild_permissions.administrator:
            return
        
        # Verificar si automod está habilitado
        guild_config = await db.get_guild_config(message.guild.id)
        if not guild_config or not guild_config.get('automod_enabled', True):
            return
        
        # Obtener configuración de automod
        automod_config = await db.get_automod_config(message.guild.id)
        if not automod_config:
            return
        
        # Verificar anti-spam
        if automod_config.get('anti_spam', True):
            if await self.check_spam(message):
                return
        
        # Verificar menciones excesivas
        max_mentions = automod_config.get('max_mentions', config.MAX_MENTIONS)
        if len(message.mentions) > max_mentions:
            await self.delete_and_warn(message, f"Demasiadas menciones (máximo {max_mentions})")
            return
        
        # Verificar emojis excesivos
        max_emojis = automod_config.get('max_emojis', config.MAX_EMOJIS)
        emoji_count = len(re.findall(r'<a?:\w+:\d+>', message.content))
        if emoji_count > max_emojis:
            await self.delete_and_warn(message, f"Demasiados emojis (máximo {max_emojis})")
            return
        
        # Verificar invitaciones de Discord
        if automod_config.get('anti_invites', True):
            if re.search(r'discord\.gg/|discordapp\.com/invite/', message.content, re.IGNORECASE):
                await self.delete_and_warn(message, "Invitaciones de Discord no permitidas")
                return
        
        # Verificar enlaces
        if automod_config.get('anti_links', False):
            if re.search(r'https?://|www\.', message.content, re.IGNORECASE):
                await self.delete_and_warn(message, "Enlaces no permitidos")
                return
        
        # Verificar palabras prohibidas
        bad_words = automod_config.get('bad_words', [])
        if bad_words:
            content_lower = message.content.lower()
            for word in bad_words:
                if word.lower() in content_lower:
                    await self.delete_and_warn(message, "Lenguaje inapropiado")
                    return
    
    async def check_spam(self, message):
        """Verificar si un mensaje es spam"""
        user_id = message.author.id
        current_time = time.time()
        
        # Agregar timestamp actual
        self.spam_tracker[user_id].append(current_time)
        
        # Limpiar timestamps antiguos
        self.spam_tracker[user_id] = [
            ts for ts in self.spam_tracker[user_id]
            if current_time - ts < config.SPAM_INTERVAL
        ]
        
        # Verificar si excede el umbral
        if len(self.spam_tracker[user_id]) > config.SPAM_THRESHOLD:
            await self.timeout_user(message, "Spam detectado")
            self.spam_tracker[user_id].clear()
            return True
        
        return False
    
    async def delete_and_warn(self, message, reason):
        """Eliminar mensaje y advertir al usuario"""
        try:
            await message.delete()
            
            embed = discord.Embed(
                title="⚠️ Mensaje eliminado",
                description=f"{message.author.mention}, tu mensaje fue eliminado.\n**Razón:** {reason}",
                color=discord.Color.orange()
            )
            
            warning_msg = await message.channel.send(embed=embed)
            
            # Eliminar advertencia después de 5 segundos
            await warning_msg.delete(delay=5)
            
            # Registrar en logs
            await db.log_moderation(
                message.guild.id,
                message.author.id,
                self.bot.user.id,
                'message_delete',
                reason
            )
        except Exception as e:
            logger.error(f"Error deleting message: {e}")
    
    async def timeout_user(self, message, reason):
        """Aplicar timeout a un usuario"""
        try:
            await message.author.timeout(discord.utils.utcnow() + discord.timedelta(minutes=5), reason=reason)
            
            embed = discord.Embed(
                title="🔇 Usuario silenciado",
                description=f"{message.author.mention} ha sido silenciado por 5 minutos.\n**Razón:** {reason}",
                color=discord.Color.red()
            )
            
            await message.channel.send(embed=embed)
            
            # Registrar en logs
            await db.log_moderation(
                message.guild.id,
                message.author.id,
                self.bot.user.id,
                'timeout',
                reason
            )
        except Exception as e:
            logger.error(f"Error timing out user: {e}")
    
    @app_commands.command(name="automod", description="Configurar automoderación (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def automod_config(self, interaction: discord.Interaction):
        """Mostrar configuración de automoderación"""
        automod_config = await db.get_automod_config(interaction.guild.id)
        
        if not automod_config:
            await interaction.response.send_message("❌ Error al obtener configuración.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="⚙️ Configuración de Automoderación",
            description="Estado actual de las funciones de automoderación",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Anti-Spam",
            value="✅ Activado" if automod_config.get('anti_spam') else "❌ Desactivado",
            inline=True
        )
        embed.add_field(
            name="Anti-Invitaciones",
            value="✅ Activado" if automod_config.get('anti_invites') else "❌ Desactivado",
            inline=True
        )
        embed.add_field(
            name="Anti-Enlaces",
            value="✅ Activado" if automod_config.get('anti_links') else "❌ Desactivado",
            inline=True
        )
        embed.add_field(
            name="Máximo de Menciones",
            value=str(automod_config.get('max_mentions', config.MAX_MENTIONS)),
            inline=True
        )
        embed.add_field(
            name="Máximo de Emojis",
            value=str(automod_config.get('max_emojis', config.MAX_EMOJIS)),
            inline=True
        )
        embed.add_field(
            name="Palabras Prohibidas",
            value=str(len(automod_config.get('bad_words', []))),
            inline=True
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="togglespam", description="Activar/desactivar anti-spam (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def toggle_spam(self, interaction: discord.Interaction):
        """Activar/desactivar anti-spam"""
        automod_config = await db.get_automod_config(interaction.guild.id)
        current = automod_config.get('anti_spam', True)
        
        await db.update_automod_config(interaction.guild.id, anti_spam=not current)
        
        status = "desactivado" if current else "activado"
        await interaction.response.send_message(f"✅ Anti-spam {status}.", ephemeral=True)
    
    @app_commands.command(name="toggleinvites", description="Activar/desactivar anti-invitaciones (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def toggle_invites(self, interaction: discord.Interaction):
        """Activar/desactivar anti-invitaciones"""
        automod_config = await db.get_automod_config(interaction.guild.id)
        current = automod_config.get('anti_invites', True)
        
        await db.update_automod_config(interaction.guild.id, anti_invites=not current)
        
        status = "desactivado" if current else "activado"
        await interaction.response.send_message(f"✅ Anti-invitaciones {status}.", ephemeral=True)
    
    @app_commands.command(name="togglelinks", description="Activar/desactivar anti-enlaces (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def toggle_links(self, interaction: discord.Interaction):
        """Activar/desactivar anti-enlaces"""
        automod_config = await db.get_automod_config(interaction.guild.id)
        current = automod_config.get('anti_links', False)
        
        await db.update_automod_config(interaction.guild.id, anti_links=not current)
        
        status = "desactivado" if current else "activado"
        await interaction.response.send_message(f"✅ Anti-enlaces {status}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
