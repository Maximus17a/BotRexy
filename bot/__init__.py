from discord.ext import commands
import discord

# Configurar intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

# Inicializar el bot con intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Exportar el objeto bot
__all__ = ["bot"]
