from discord.ext import commands
import discord
from bot.cogs.game_roles import GameRoles

# Configurar intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

# Inicializar el bot con intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Cargar cogs
bot.add_cog(GameRoles(bot))

# Exportar el objeto bot
__all__ = ["bot"]

# Sincronizar comandos
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot listo como {bot.user}")
