import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.database import db
from bot.utils.image_gen import image_generator
import logging

logger = logging.getLogger(__name__)

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Enviar mensaje de bienvenida cuando un usuario se une"""
        try:
            # Verificar si el sistema de bienvenida está habilitado
            guild_config = db.get_guild_config(member.guild.id)
            if not guild_config or not guild_config.get('welcome_enabled', False):
                return
            
            # Obtener configuración de bienvenida
            welcome_config = db.get_welcome_config(member.guild.id)
            if not welcome_config:
                return
            
            # Obtener canal de bienvenida
            channel_id = welcome_config.get('channel_id')
            if not channel_id:
                return
            
            channel = member.guild.get_channel(int(channel_id))
            if not channel:
                return
            
            # Preparar mensaje
            message_template = welcome_config.get('message', '¡Bienvenido {user} a {server}!')
            message_text = message_template.format(
                user=member.mention,
                server=member.guild.name,
                members=member.guild.member_count
            )
            
            # Generar imagen si está habilitada
            if welcome_config.get('image_enabled', True):
                try:
                    avatar_url = member.display_avatar.url
                    bg_color = welcome_config.get('image_background', '#7289da')
                    text_color = welcome_config.get('image_text_color', '#ffffff')
                    background_image_url = welcome_config.get('background_image_url')
                    
                    # Convertir ruta relativa a absoluta si es necesario
                    if background_image_url and background_image_url.startswith('/'):
                        # Necesitamos la URL completa para la descarga
                        background_image_url = None  # Por ahora usar None, se puede configurar URL base
                    
                    # Definir el embed antes de usarlo
                    embed = discord.Embed(
                        title="¡Bienvenido!",
                        description=message_text,
                        color=discord.Color.blue()
                    )
                    embed.set_thumbnail(url=member.display_avatar.url)
                    embed.set_footer(text=f"Miembros totales: {member.guild.member_count}")

                    # Verificar si la generación de la imagen devuelve datos válidos
                    try:
                        image_bytes = image_generator.generate(
                            user_name=member.display_name,
                            user_avatar_url=avatar_url,
                            server_name=member.guild.name,
                            bg_color=bg_color,
                            text_color=text_color,
                            background_image_url=background_image_url,
                            font_size=24,
                            padding=20
                        )

                        if image_bytes:
                            file = discord.File(image_bytes, filename='welcome.png')
                            embed.set_image(url='attachment://welcome.png')
                            await channel.send(embed=embed, file=file)
                        else:
                            logger.warning("La generación de la imagen devolvió None. Enviando solo texto.")
                            await channel.send(embed=embed)
                    except Exception as e:
                        logger.error(f"Error generando la imagen de bienvenida: {e}")
                        await channel.send(embed=embed)
                except Exception as e:
                    logger.error(f"Error generating welcome image: {e}")
                    await channel.send(message_text)
            else:
                # Enviar solo texto
                await channel.send(message_text)
        
        except Exception as e:
            logger.error(f"Error in welcome message: {e}")
    
    @app_commands.command(name="setwelcome", description="Configurar canal de bienvenida (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_welcome(self, interaction: discord.Interaction, canal: discord.TextChannel):
        """Configurar canal de bienvenida"""
        try:
            db.update_welcome_config(interaction.guild.id, channel_id=str(canal.id))
            db.update_guild_config(interaction.guild.id, welcome_enabled=True)
            await interaction.response.send_message(f"✅ Canal de bienvenida configurado en {canal.mention}", ephemeral=True)
        except Exception as e:
            logger.error(f"Error setting welcome channel: {e}")
            await interaction.response.send_message("❌ Error al configurar canal de bienvenida.", ephemeral=True)
    
    @app_commands.command(name="welcomemsg", description="Configurar mensaje de bienvenida (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def welcome_message(self, interaction: discord.Interaction, mensaje: str):
        """Configurar mensaje de bienvenida"""
        try:
            db.update_welcome_config(interaction.guild.id, message=mensaje)
            
            embed = discord.Embed(
                title="✅ Mensaje de bienvenida actualizado",
                description="Variables disponibles:\n`{user}` - Mención del usuario\n`{server}` - Nombre del servidor\n`{members}` - Cantidad de miembros",
                color=discord.Color.green()
            )
            embed.add_field(name="Mensaje configurado", value=mensaje, inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error setting welcome message: {e}")
            await interaction.response.send_message("❌ Error al configurar mensaje de bienvenida.", ephemeral=True)
    
    @app_commands.command(name="testwelcome", description="Probar mensaje de bienvenida")
    @app_commands.checks.has_permissions(administrator=True)
    async def test_welcome(self, interaction: discord.Interaction):
        """Probar mensaje de bienvenida"""
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Simular evento de bienvenida
            await self.on_member_join(interaction.user)
            await interaction.followup.send("✅ Mensaje de bienvenida enviado!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error testing welcome: {e}")
            await interaction.followup.send("❌ Error al probar mensaje de bienvenida.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
