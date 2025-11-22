import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.database import db
import logging

logger = logging.getLogger(__name__)

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Enviar mensaje de verificación cuando un usuario se une"""
        try:
            # Verificar si el sistema de verificación está habilitado
            guild_config = await db.get_guild_config(member.guild.id)
            if not guild_config or not guild_config.get('verification_enabled', False):
                return
            
            # Obtener configuración de verificación
            verification_config = await db.get_verification_config(member.guild.id)
            if not verification_config:
                return
            
            # Obtener canal de verificación
            channel_id = verification_config.get('channel_id')
            if not channel_id:
                return
            
            channel = member.guild.get_channel(int(channel_id))
            if not channel:
                return
            
            # Crear embed de verificación
            embed = discord.Embed(
                title="🔐 Verificación Requerida",
                description=f"¡Bienvenido {member.mention}!\n\nPara acceder al servidor, por favor verifica que eres humano haciendo clic en el botón de abajo.",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(
                name="¿Por qué verificar?",
                value="La verificación nos ayuda a mantener el servidor seguro y libre de bots maliciosos.",
                inline=False
            )
            
            # Crear botón de verificación
            view = VerificationView(member.id, verification_config.get('verified_role_id'))
            
            await channel.send(embed=embed, view=view)
        
        except Exception as e:
            logger.error(f"Error in verification on_member_join: {e}")
    
    @app_commands.command(name="setupverification", description="Configurar sistema de verificación (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_verification(
        self, 
        interaction: discord.Interaction, 
        canal: discord.TextChannel,
        rol_verificado: discord.Role
    ):
        """Configurar sistema de verificación"""
        try:
            # Actualizar configuración
            await db.update_verification_config(
                interaction.guild.id,
                channel_id=str(canal.id),
                verified_role_id=str(rol_verificado.id)
            )
            
            await db.update_guild_config(interaction.guild.id, verification_enabled=True)
            
            embed = discord.Embed(
                title="✅ Sistema de Verificación Configurado",
                description="El sistema de verificación ha sido configurado correctamente.",
                color=discord.Color.green()
            )
            embed.add_field(name="Canal", value=canal.mention, inline=True)
            embed.add_field(name="Rol", value=rol_verificado.mention, inline=True)
            embed.add_field(
                name="Próximos pasos",
                value="Cuando un nuevo miembro se una, recibirá un mensaje de verificación en el canal configurado.",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except Exception as e:
            logger.error(f"Error setting up verification: {e}")
            await interaction.response.send_message("❌ Error al configurar verificación.", ephemeral=True)
    
    @app_commands.command(name="verify", description="Verificar manualmente a un usuario (Admin)")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def manual_verify(self, interaction: discord.Interaction, usuario: discord.Member):
        """Verificar manualmente a un usuario"""
        try:
            verification_config = await db.get_verification_config(interaction.guild.id)
            
            if not verification_config or not verification_config.get('verified_role_id'):
                await interaction.response.send_message("❌ Sistema de verificación no configurado.", ephemeral=True)
                return
            
            role = interaction.guild.get_role(int(verification_config['verified_role_id']))
            
            if not role:
                await interaction.response.send_message("❌ Rol de verificación no encontrado.", ephemeral=True)
                return
            
            await usuario.add_roles(role, reason=f"Verificado manualmente por {interaction.user}")
            
            await interaction.response.send_message(
                f"✅ {usuario.mention} ha sido verificado manualmente.",
                ephemeral=True
            )
        
        except Exception as e:
            logger.error(f"Error in manual verification: {e}")
            await interaction.response.send_message("❌ Error al verificar usuario.", ephemeral=True)
    
    @app_commands.command(name="toggleverification", description="Activar/desactivar verificación (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def toggle_verification(self, interaction: discord.Interaction):
        """Activar/desactivar sistema de verificación"""
        try:
            guild_config = await db.get_guild_config(interaction.guild.id)
            current = guild_config.get('verification_enabled', False)
            
            await db.update_guild_config(interaction.guild.id, verification_enabled=not current)
            
            status = "desactivado" if current else "activado"
            await interaction.response.send_message(f"✅ Sistema de verificación {status}.", ephemeral=True)
        
        except Exception as e:
            logger.error(f"Error toggling verification: {e}")
            await interaction.response.send_message("❌ Error al cambiar estado de verificación.", ephemeral=True)


class VerificationView(discord.ui.View):
    def __init__(self, member_id: int, verified_role_id: str):
        super().__init__(timeout=None)  # No timeout para que persista
        self.member_id = member_id
        self.verified_role_id = verified_role_id
    
    @discord.ui.button(label="✅ Verificarme", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botón de verificación"""
        try:
            # Verificar que sea el usuario correcto
            if interaction.user.id != self.member_id:
                await interaction.response.send_message(
                    "❌ Este botón de verificación no es para ti.",
                    ephemeral=True
                )
                return
            
            # Obtener el rol
            role = interaction.guild.get_role(int(self.verified_role_id))
            
            if not role:
                await interaction.response.send_message(
                    "❌ Error: Rol de verificación no encontrado.",
                    ephemeral=True
                )
                return
            
            # Verificar si ya tiene el rol
            if role in interaction.user.roles:
                await interaction.response.send_message(
                    "✅ Ya estás verificado.",
                    ephemeral=True
                )
                return
            
            # Agregar rol
            await interaction.user.add_roles(role, reason="Verificación completada")
            
            # Responder
            embed = discord.Embed(
                title="✅ Verificación Exitosa",
                description=f"¡Felicidades {interaction.user.mention}! Has sido verificado correctamente.\n\nAhora tienes acceso completo al servidor.",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # Log de moderación
            await db.log_moderation(
                interaction.guild.id,
                interaction.user.id,
                self.bot.user.id,
                'verification',
                'Usuario verificado automáticamente'
            )
        
        except Exception as e:
            logger.error(f"Error in verification button: {e}")
            await interaction.response.send_message(
                "❌ Error al verificar. Por favor contacta a un administrador.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Verification(bot))
