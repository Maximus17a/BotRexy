import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.database import db
import logging

logger = logging.getLogger(__name__)

# Emojis y colores para cada juego
GAME_EMOJIS = {
    'Rexys': '🎮',
    'Lolsito': '🎯',
    'Pokemon': '⚡',
    'Valorant': '🔫',
    'Fortnite': '🏗️',
    'Marvel Rivals': '⚔️',
    'Battlefield': '💣',
    'Palia': '🌿',
    'League of Legends': '🏆'
}

GAME_COLORS = {
    'Rexys': discord.ButtonStyle.green,
    'Lolsito': discord.ButtonStyle.blurple,
    'Pokemon': discord.ButtonStyle.red,
    'Valorant': discord.ButtonStyle.red,
    'Fortnite': discord.ButtonStyle.blurple,
    'Marvel Rivals': discord.ButtonStyle.red,
    'Battlefield': discord.ButtonStyle.green,
    'Palia': discord.ButtonStyle.blurple,
    'League of Legends': discord.ButtonStyle.blurple
}

class GameRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setupgameroles", description="Configurar panel de roles de juegos (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_game_roles(self, interaction: discord.Interaction, canal: discord.TextChannel):
        """Configurar panel de roles de juegos"""
        try:
            await interaction.response.defer(ephemeral=True)
            
            # Obtener configuración de roles de juegos
            game_roles_config = db.get_game_roles_config(interaction.guild.id)
            
            if not game_roles_config or not game_roles_config.get('roles'):
                await interaction.followup.send(
                    "❌ Primero debes configurar los roles de juegos con `/addgamerole`",
                    ephemeral=True
                )
                return
            
            # Crear embed principal
            embed = discord.Embed(
                title="🎮 Selección de Roles",
                description="Haz clic en los botones de abajo para obtener o remover roles de juegos y actividades.",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="¿Cómo funciona?",
                value="• Haz clic en un botón para agregar el rol\n• Si ya tienes el rol, haz clic nuevamente para quitarlo",
                inline=False
            )
            
            # Obtener roles configurados
            roles_data = game_roles_config.get('roles', {})
            
            if roles_data:
                roles_list = []
                for game_name, role_id in roles_data.items():
                    role = interaction.guild.get_role(int(role_id))
                    if role:
                        emoji = GAME_EMOJIS.get(game_name, '🎮')
                        roles_list.append(f"{emoji} {role.mention} - {game_name}")
                
                if roles_list:
                    embed.add_field(
                        name="Roles Disponibles:",
                        value="\n".join(roles_list),
                        inline=False
                    )
            
            embed.set_footer(text="Botones permanentes • Funcionan 24/7")
            
            # Crear vista con botones
            view = GameRolesView(roles_data)
            
            # Enviar mensaje
            message = await canal.send(embed=embed, view=view)
            
            # Guardar ID del mensaje
            db.update_game_roles_config(
                interaction.guild.id,
                channel_id=str(canal.id),
                message_id=str(message.id)
            )
            
            await interaction.followup.send(
                f"✅ Panel de roles de juegos creado en {canal.mention}",
                ephemeral=True
            )
        
        except Exception as e:
            logger.error(f"Error setting up game roles: {e}")
            await interaction.followup.send("❌ Error al configurar panel de roles.", ephemeral=True)
    
    @app_commands.command(name="addgamerole", description="Agregar un rol de juego (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_game_role(
        self,
        interaction: discord.Interaction,
        juego: str,
        rol: discord.Role
    ):
        """Agregar un rol de juego a la configuración"""
        try:
            # Obtener configuración actual
            game_roles_config = db.get_game_roles_config(interaction.guild.id)
            
            if not game_roles_config:
                game_roles_config = {'roles': {}}
            
            roles_data = game_roles_config.get('roles', {})
            roles_data[juego] = str(rol.id)
            
            db.update_game_roles_config(
                interaction.guild.id,
                roles=roles_data
            )
            
            emoji = GAME_EMOJIS.get(juego, '🎮')
            await interaction.response.send_message(
                f"✅ Rol de juego agregado: {emoji} **{juego}** → {rol.mention}",
                ephemeral=True
            )
        
        except Exception as e:
            logger.error(f"Error adding game role: {e}")
            await interaction.response.send_message("❌ Error al agregar rol de juego.", ephemeral=True)
    
    @add_game_role.autocomplete('juego')
    async def game_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        """Autocompletar nombres de juegos"""
        games = list(GAME_EMOJIS.keys())
        return [
            app_commands.Choice(name=f"{GAME_EMOJIS[game]} {game}", value=game)
            for game in games
            if current.lower() in game.lower()
        ][:25]
    
    @app_commands.command(name="removegamerole", description="Remover un rol de juego (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_game_role(self, interaction: discord.Interaction, juego: str):
        """Remover un rol de juego de la configuración"""
        try:
            game_roles_config = db.get_game_roles_config(interaction.guild.id)
            
            if not game_roles_config or not game_roles_config.get('roles'):
                await interaction.response.send_message(
                    "❌ No hay roles de juegos configurados.",
                    ephemeral=True
                )
                return
            
            roles_data = game_roles_config.get('roles', {})
            
            if juego not in roles_data:
                await interaction.response.send_message(
                    f"❌ El juego **{juego}** no está configurado.",
                    ephemeral=True
                )
                return
            
            del roles_data[juego]
            
            db.update_game_roles_config(
                interaction.guild.id,
                roles=roles_data
            )
            
            await interaction.response.send_message(
                f"✅ Rol de juego **{juego}** removido de la configuración.",
                ephemeral=True
            )
        
        except Exception as e:
            logger.error(f"Error removing game role: {e}")
            await interaction.response.send_message("❌ Error al remover rol de juego.", ephemeral=True)
    
    @app_commands.command(name="listgameroles", description="Ver roles de juegos configurados (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def list_game_roles(self, interaction: discord.Interaction):
        """Listar roles de juegos configurados"""
        try:
            game_roles_config = db.get_game_roles_config(interaction.guild.id)
            
            if not game_roles_config or not game_roles_config.get('roles'):
                await interaction.response.send_message(
                    "❌ No hay roles de juegos configurados.",
                    ephemeral=True
                )
                return
            
            embed = discord.Embed(
                title="🎮 Roles de Juegos Configurados",
                color=discord.Color.blue()
            )
            
            roles_data = game_roles_config.get('roles', {})
            
            for game_name, role_id in roles_data.items():
                role = interaction.guild.get_role(int(role_id))
                emoji = GAME_EMOJIS.get(game_name, '🎮')
                
                if role:
                    embed.add_field(
                        name=f"{emoji} {game_name}",
                        value=role.mention,
                        inline=True
                    )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except Exception as e:
            logger.error(f"Error listing game roles: {e}")
            await interaction.response.send_message("❌ Error al listar roles de juegos.", ephemeral=True)


class GameRolesView(discord.ui.View):
    def __init__(self, roles_data: dict):
        super().__init__(timeout=None)
        self.roles_data = roles_data
        
        # Crear botones dinámicamente
        for game_name, role_id in roles_data.items():
            emoji = GAME_EMOJIS.get(game_name, '🎮')
            style = GAME_COLORS.get(game_name, discord.ButtonStyle.gray)
            
            button = discord.ui.Button(
                label=game_name,
                emoji=emoji,
                style=style,
                custom_id=f"game_role_{role_id}"
            )
            button.callback = self.create_callback(role_id, game_name)
            self.add_item(button)
    
    def create_callback(self, role_id: str, game_name: str):
        """Crear callback para cada botón"""
        async def button_callback(interaction: discord.Interaction):
            try:
                role = interaction.guild.get_role(int(role_id))
                
                if not role:
                    await interaction.response.send_message(
                        "❌ Error: Rol no encontrado.",
                        ephemeral=True
                    )
                    return
                
                # Verificar si el usuario ya tiene el rol
                if role in interaction.user.roles:
                    # Remover rol
                    await interaction.user.remove_roles(role, reason="Rol de juego removido")
                    emoji = GAME_EMOJIS.get(game_name, '🎮')
                    await interaction.response.send_message(
                        f"{emoji} Se te ha removido el rol de **{game_name}**",
                        ephemeral=True
                    )
                else:
                    # Agregar rol
                    await interaction.user.add_roles(role, reason="Rol de juego agregado")
                    emoji = GAME_EMOJIS.get(game_name, '🎮')
                    await interaction.response.send_message(
                        f"{emoji} ¡Ahora tienes el rol de **{game_name}**!",
                        ephemeral=True
                    )
            
            except Exception as e:
                logger.error(f"Error in game role button: {e}")
                await interaction.response.send_message(
                    "❌ Error al cambiar rol. Por favor contacta a un administrador.",
                    ephemeral=True
                )
        
        return button_callback


async def setup(bot):
    await bot.add_cog(GameRoles(bot))
