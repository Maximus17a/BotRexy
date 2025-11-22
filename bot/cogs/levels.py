import discord
from discord.ext import commands
from discord import app_commands
import time
import config
from bot.utils.database import db
import logging

logger = logging.getLogger(__name__)

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_cooldowns = {}  # {user_id: timestamp}
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Otorgar XP por mensajes"""
        # Ignorar bots y mensajes sin servidor
        if message.author.bot or not message.guild:
            return
        
        # Verificar si el sistema de niveles está habilitado
        guild_config = await db.get_guild_config(message.guild.id)
        if not guild_config or not guild_config.get('levels_enabled', True):
            return
        
        # Verificar cooldown
        user_id = message.author.id
        current_time = time.time()
        
        if user_id in self.xp_cooldowns:
            if current_time - self.xp_cooldowns[user_id] < config.XP_COOLDOWN:
                return
        
        # Actualizar cooldown
        self.xp_cooldowns[user_id] = current_time
        
        # Agregar XP
        result = await db.add_xp(message.guild.id, user_id, config.XP_PER_MESSAGE)
        
        if result and result['leveled_up']:
            # Notificar subida de nivel
            embed = discord.Embed(
                title="🎉 ¡Subida de Nivel!",
                description=f"{message.author.mention} ha alcanzado el **Nivel {result['new_level']}**!",
                color=discord.Color.gold()
            )
            await message.channel.send(embed=embed)
    
    @app_commands.command(name="nivel", description="Ver tu nivel y experiencia")
    async def level(self, interaction: discord.Interaction, usuario: discord.Member = None):
        """Ver nivel de un usuario"""
        target = usuario or interaction.user
        
        user_data = await db.get_user_level(interaction.guild.id, target.id)
        
        if not user_data:
            await interaction.response.send_message("No se encontraron datos para este usuario.", ephemeral=True)
            return
        
        level = user_data['level']
        xp = user_data['xp']
        messages = user_data['messages']
        
        # Calcular XP para siguiente nivel
        xp_needed = db.xp_for_level(level + 1)
        xp_progress = xp - db.xp_for_level(level)
        xp_for_next = xp_needed - db.xp_for_level(level)
        
        # Crear barra de progreso
        progress_bar_length = 20
        progress = int((xp_progress / xp_for_next) * progress_bar_length)
        progress_bar = "█" * progress + "░" * (progress_bar_length - progress)
        
        embed = discord.Embed(
            title=f"📊 Nivel de {target.display_name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Nivel", value=f"**{level}**", inline=True)
        embed.add_field(name="XP", value=f"{xp_progress}/{xp_for_next}", inline=True)
        embed.add_field(name="Mensajes", value=f"{messages}", inline=True)
        embed.add_field(name="Progreso", value=f"`{progress_bar}` {int((xp_progress/xp_for_next)*100)}%", inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ranking", description="Ver la tabla de clasificación del servidor")
    async def leaderboard(self, interaction: discord.Interaction):
        """Mostrar tabla de clasificación"""
        leaderboard = await db.get_leaderboard(interaction.guild.id, 10)
        
        if not leaderboard:
            await interaction.response.send_message("No hay datos de clasificación aún.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=f"🏆 Ranking de {interaction.guild.name}",
            description="Top 10 usuarios por nivel",
            color=discord.Color.gold()
        )
        
        for idx, user_data in enumerate(leaderboard, 1):
            user_id = int(user_data['user_id'])
            user = interaction.guild.get_member(user_id)
            
            if user:
                name = user.display_name
            else:
                name = f"Usuario {user_id}"
            
            level = user_data['level']
            xp = user_data['xp']
            
            medal = ""
            if idx == 1:
                medal = "🥇"
            elif idx == 2:
                medal = "🥈"
            elif idx == 3:
                medal = "🥉"
            
            embed.add_field(
                name=f"{medal} #{idx} - {name}",
                value=f"Nivel {level} | {xp} XP",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="resetxp", description="Resetear XP de un usuario (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset_xp(self, interaction: discord.Interaction, usuario: discord.Member):
        """Resetear XP de un usuario"""
        try:
            await db.create_user(interaction.guild.id, usuario.id)
            await interaction.response.send_message(f"✅ XP de {usuario.mention} ha sido reseteado.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error resetting XP: {e}")
            await interaction.response.send_message("❌ Error al resetear XP.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Levels(bot))
