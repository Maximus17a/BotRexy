import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.database import db
import logging
import datetime

logger = logging.getLogger(__name__)

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def _create_verification_embed(self, guild, role_id, custom_intro=None):
        """Helper para crear el embed con el diseño exacto de las reglas"""
        
        # 1. Obtener el rol para mostrarlo
        role_mention = "@Verificado"
        if role_id:
            role = guild.get_role(int(role_id))
            if role:
                role_mention = role.mention

        # 2. Texto de introducción (desde DB o por defecto)
        description = custom_intro or "¡Bienvenido/a a nuestro servidor! Para acceder a todos los canales, por favor lee las reglas y acepta al final."

        # 3. Crear Embed
        embed = discord.Embed(
            title="📜 Reglas del Servidor",
            description=description,
            color=discord.Color.from_str("#2b2d31") # Color oscuro estilo Discord
        )

        # 4. Normas de Conducta (Texto formateado exactamente como la imagen)
        normas_text = (
            "**1. Respeto Mutuo**\n"
            "- Trata a todos con respeto. No se tolerará acoso, discriminación o lenguaje de odio.\n\n"
            "**2. Contenido Apropiado**\n"
            "- Mantén el contenido apropiado. El contenido NSFW está prohibido.\n\n"
            "**3. No Spam**\n"
            "- Evita el spam, flood o autopromoción no solicitada.\n\n"
            "**4. Uso de Canales**\n"
            "- Utiliza los canales para su propósito designado.\n\n"
            "**5. Privacidad**\n"
            "- No compartas información personal sin consentimiento.\n\n"
            "**6. Sigue las Indicaciones del Staff**\n"
            "- Las decisiones del equipo de moderación son finales."
        )

        embed.add_field(name="📋 Normas de Conducta", value=normas_text, inline=False)
        
        # 5. Campo Importante
        embed.add_field(
            name="⚠️ Importante", 
            value="Al hacer clic en el botón de abajo, aceptas cumplir con estas reglas. El incumplimiento puede resultar en sanciones.", 
            inline=False
        )

        # 6. Campo de Rol
        embed.add_field(name="Rol que recibirás:", value=role_mention, inline=False)

        # 7. Footer con fecha
        today = datetime.date.today().strftime("%d/%m/%Y")
        embed.set_footer(text=f"Última actualización: {today}")

        return embed

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Enviar mensaje de verificación cuando un usuario se une"""
        try:
            guild_config = db.get_guild_config(member.guild.id)
            if not guild_config or not guild_config.get('verification_enabled', False):
                return
            
            verification_config = db.get_verification_config(member.guild.id)
            if not verification_config:
                return
            
            channel_id = verification_config.get('channel_id')
            if not channel_id:
                return
            
            channel = member.guild.get_channel(int(channel_id))
            if not channel:
                return
            
            # Usar el generador de embed personalizado
            embed = self._create_verification_embed(
                member.guild, 
                verification_config.get('verified_role_id'),
                verification_config.get('message')
            )
            
            # Crear botón verde específico
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
        """Configurar sistema de verificación y enviar panel"""
        try:
            # Actualizar configuración
            db.update_verification_config(
                interaction.guild.id,
                channel_id=str(canal.id),
                verified_role_id=str(rol_verificado.id)
            )
            
            db.update_guild_config(interaction.guild.id, verification_enabled=True)
            
            # Generar el embed visualmente idéntico a la imagen
            embed_panel = self._create_verification_embed(
                interaction.guild, 
                rol_verificado.id,
                custom_intro="¡Bienvenido/a a nuestro servidor! Para acceder a todos los canales, por favor lee las reglas y acepta al final."
            )

            # Botón verde "Acepto las reglas"
            # Nota: Pasamos member_id=0 o None para que sea un botón público (persistent) 
            # pero VerificationView actualmente requiere member_id.
            # Para un panel público, modificaremos VerificationView abajo para aceptar cualquier usuario.
            view = VerificationView(None, str(rol_verificado.id))
            
            await canal.send(embed=embed_panel, view=view)
            
            await interaction.response.send_message(
                f"✅ Sistema de verificación configurado y panel enviado a {canal.mention}", 
                ephemeral=True
            )
        
        except Exception as e:
            logger.error(f"Error setting up verification: {e}")
            await interaction.response.send_message("❌ Error al configurar verificación.", ephemeral=True)

    # ... (Mantener comandos verify, toggleverification igual que antes) ...
    @app_commands.command(name="verify", description="Verificar manualmente a un usuario (Admin)")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def manual_verify(self, interaction: discord.Interaction, usuario: discord.Member):
        """Verificar manualmente a un usuario"""
        try:
            verification_config = db.get_verification_config(interaction.guild.id)
            if not verification_config or not verification_config.get('verified_role_id'):
                await interaction.response.send_message("❌ Sistema de verificación no configurado.", ephemeral=True)
                return
            role = interaction.guild.get_role(int(verification_config['verified_role_id']))
            if not role:
                await interaction.response.send_message("❌ Rol de verificación no encontrado.", ephemeral=True)
                return
            await usuario.add_roles(role, reason=f"Verificado manualmente por {interaction.user}")
            await interaction.response.send_message(f"✅ {usuario.mention} ha sido verificado manualmente.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error in manual verification: {e}")
            await interaction.response.send_message("❌ Error al verificar usuario.", ephemeral=True)
    
    @app_commands.command(name="toggleverification", description="Activar/desactivar verificación (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def toggle_verification(self, interaction: discord.Interaction):
        """Activar/desactivar sistema de verificación"""
        try:
            guild_config = db.get_guild_config(interaction.guild.id)
            current = guild_config.get('verification_enabled', False)
            db.update_guild_config(interaction.guild.id, verification_enabled=not current)
            status = "desactivado" if current else "activado"
            await interaction.response.send_message(f"✅ Sistema de verificación {status}.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error toggling verification: {e}")
            await interaction.response.send_message("❌ Error al cambiar estado de verificación.", ephemeral=True)


class VerificationView(discord.ui.View):
    def __init__(self, member_id: int | None, verified_role_id: str):
        super().__init__(timeout=None)
        self.member_id = member_id
        self.verified_role_id = verified_role_id
    
    # Cambiado estilo a verde (success) y etiqueta a "Acepto las reglas"
    @discord.ui.button(label="Acepto las reglas", style=discord.ButtonStyle.success, emoji="✅", custom_id="verify_button_rules")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botón de verificación"""
        try:
            # Si self.member_id es None, es un panel público, cualquiera puede hacer clic.
            # Si tiene un ID, es un mensaje de bienvenida personal.
            if self.member_id and interaction.user.id != self.member_id:
                await interaction.response.send_message(
                    "❌ Este botón de verificación no es para ti.",
                    ephemeral=True
                )
                return
            
            role = interaction.guild.get_role(int(self.verified_role_id))
            
            if not role:
                await interaction.response.send_message("❌ Error: Rol de verificación no encontrado.", ephemeral=True)
                return
            
            if role in interaction.user.roles:
                await interaction.response.send_message("✅ Ya has aceptado las reglas.", ephemeral=True)
                return
            
            await interaction.user.add_roles(role, reason="Verificación completada (Aceptó reglas)")
            
            await interaction.response.send_message(
                f"✅ ¡Gracias {interaction.user.mention}! Has aceptado las reglas y has sido verificado.",
                ephemeral=True
            )
            
        except Exception as e:
            logger.error(f"Error in verification button: {e}")
            await interaction.response.send_message("❌ Error al verificar.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Verification(bot))