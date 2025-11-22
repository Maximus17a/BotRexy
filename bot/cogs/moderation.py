import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.database import db
import logging

logger = logging.getLogger(__name__)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="kick", description="Expulsar a un usuario del servidor")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, usuario: discord.Member, razon: str = "No especificada"):
        """Expulsar a un usuario"""
        try:
            if usuario.top_role >= interaction.user.top_role:
                await interaction.response.send_message("❌ No puedes expulsar a este usuario.", ephemeral=True)
                return
            
            await usuario.kick(reason=razon)
            
            embed = discord.Embed(
                title="👢 Usuario Expulsado",
                description=f"{usuario.mention} ha sido expulsado del servidor.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
            embed.add_field(name="Razón", value=razon, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
            # Registrar en logs
            await db.log_moderation(
                interaction.guild.id,
                usuario.id,
                interaction.user.id,
                'kick',
                razon
            )
        except Exception as e:
            logger.error(f"Error kicking user: {e}")
            await interaction.response.send_message("❌ Error al expulsar al usuario.", ephemeral=True)
    
    @app_commands.command(name="ban", description="Banear a un usuario del servidor")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, usuario: discord.Member, razon: str = "No especificada"):
        """Banear a un usuario"""
        try:
            if usuario.top_role >= interaction.user.top_role:
                await interaction.response.send_message("❌ No puedes banear a este usuario.", ephemeral=True)
                return
            
            await usuario.ban(reason=razon)
            
            embed = discord.Embed(
                title="🔨 Usuario Baneado",
                description=f"{usuario.mention} ha sido baneado del servidor.",
                color=discord.Color.red()
            )
            embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
            embed.add_field(name="Razón", value=razon, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
            # Registrar en logs
            await db.log_moderation(
                interaction.guild.id,
                usuario.id,
                interaction.user.id,
                'ban',
                razon
            )
        except Exception as e:
            logger.error(f"Error banning user: {e}")
            await interaction.response.send_message("❌ Error al banear al usuario.", ephemeral=True)
    
    @app_commands.command(name="unban", description="Desbanear a un usuario")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        """Desbanear a un usuario"""
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user)
            
            embed = discord.Embed(
                title="✅ Usuario Desbaneado",
                description=f"{user.mention} ha sido desbaneado.",
                color=discord.Color.green()
            )
            embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
            # Registrar en logs
            await db.log_moderation(
                interaction.guild.id,
                user.id,
                interaction.user.id,
                'unban',
                None
            )
        except Exception as e:
            logger.error(f"Error unbanning user: {e}")
            await interaction.response.send_message("❌ Error al desbanear al usuario.", ephemeral=True)
    
    @app_commands.command(name="timeout", description="Silenciar a un usuario temporalmente")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, usuario: discord.Member, minutos: int, razon: str = "No especificada"):
        """Aplicar timeout a un usuario"""
        try:
            if usuario.top_role >= interaction.user.top_role:
                await interaction.response.send_message("❌ No puedes silenciar a este usuario.", ephemeral=True)
                return
            
            if minutos < 1 or minutos > 40320:  # 28 días máximo
                await interaction.response.send_message("❌ El tiempo debe estar entre 1 y 40320 minutos (28 días).", ephemeral=True)
                return
            
            await usuario.timeout(discord.utils.utcnow() + discord.timedelta(minutes=minutos), reason=razon)
            
            embed = discord.Embed(
                title="🔇 Usuario Silenciado",
                description=f"{usuario.mention} ha sido silenciado por {minutos} minutos.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
            embed.add_field(name="Razón", value=razon, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
            # Registrar en logs
            await db.log_moderation(
                interaction.guild.id,
                usuario.id,
                interaction.user.id,
                'timeout',
                f"{razon} ({minutos} minutos)"
            )
        except Exception as e:
            logger.error(f"Error timing out user: {e}")
            await interaction.response.send_message("❌ Error al silenciar al usuario.", ephemeral=True)
    
    @app_commands.command(name="untimeout", description="Quitar silencio a un usuario")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout(self, interaction: discord.Interaction, usuario: discord.Member):
        """Quitar timeout a un usuario"""
        try:
            await usuario.timeout(None)
            
            embed = discord.Embed(
                title="🔊 Silencio Removido",
                description=f"{usuario.mention} ya no está silenciado.",
                color=discord.Color.green()
            )
            embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
            # Registrar en logs
            await db.log_moderation(
                interaction.guild.id,
                usuario.id,
                interaction.user.id,
                'untimeout',
                None
            )
        except Exception as e:
            logger.error(f"Error removing timeout: {e}")
            await interaction.response.send_message("❌ Error al quitar silencio.", ephemeral=True)
    
    @app_commands.command(name="clear", description="Eliminar mensajes en un canal")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, cantidad: int):
        """Eliminar mensajes"""
        try:
            if cantidad < 1 or cantidad > 100:
                await interaction.response.send_message("❌ La cantidad debe estar entre 1 y 100.", ephemeral=True)
                return
            
            await interaction.response.defer(ephemeral=True)
            
            deleted = await interaction.channel.purge(limit=cantidad)
            
            await interaction.followup.send(f"✅ Se eliminaron {len(deleted)} mensajes.", ephemeral=True)
            
            # Registrar en logs
            await db.log_moderation(
                interaction.guild.id,
                interaction.user.id,
                interaction.user.id,
                'clear',
                f"{len(deleted)} mensajes en {interaction.channel.mention}"
            )
        except Exception as e:
            logger.error(f"Error clearing messages: {e}")
            await interaction.followup.send("❌ Error al eliminar mensajes.", ephemeral=True)
    
    @app_commands.command(name="warn", description="Advertir a un usuario")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, usuario: discord.Member, razon: str):
        """Advertir a un usuario"""
        try:
            embed = discord.Embed(
                title="⚠️ Advertencia",
                description=f"{usuario.mention} has recibido una advertencia.",
                color=discord.Color.yellow()
            )
            embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
            embed.add_field(name="Razón", value=razon, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
            # Intentar enviar DM al usuario
            try:
                dm_embed = discord.Embed(
                    title="⚠️ Has recibido una advertencia",
                    description=f"En el servidor **{interaction.guild.name}**",
                    color=discord.Color.yellow()
                )
                dm_embed.add_field(name="Razón", value=razon, inline=False)
                await usuario.send(embed=dm_embed)
            except:
                pass
            
            # Registrar en logs
            await db.log_moderation(
                interaction.guild.id,
                usuario.id,
                interaction.user.id,
                'warn',
                razon
            )
        except Exception as e:
            logger.error(f"Error warning user: {e}")
            await interaction.response.send_message("❌ Error al advertir al usuario.", ephemeral=True)
    
    @app_commands.command(name="modlogs", description="Ver logs de moderación")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def modlogs(self, interaction: discord.Interaction, limite: int = 10):
        """Ver logs de moderación"""
        try:
            if limite < 1 or limite > 50:
                await interaction.response.send_message("❌ El límite debe estar entre 1 y 50.", ephemeral=True)
                return
            
            logs = await db.get_moderation_logs(interaction.guild.id, limite)
            
            if not logs:
                await interaction.response.send_message("No hay logs de moderación.", ephemeral=True)
                return
            
            embed = discord.Embed(
                title="📋 Logs de Moderación",
                description=f"Últimas {len(logs)} acciones",
                color=discord.Color.blue()
            )
            
            for log in logs:
                user_id = log['user_id']
                mod_id = log['moderator_id']
                action = log['action']
                reason = log['reason'] or 'No especificada'
                timestamp = log['created_at']
                
                embed.add_field(
                    name=f"{action.upper()} - <@{user_id}>",
                    value=f"Moderador: <@{mod_id}>\nRazón: {reason}\nFecha: {timestamp}",
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error getting modlogs: {e}")
            await interaction.response.send_message("❌ Error al obtener logs.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
