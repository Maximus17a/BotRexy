from discord.ext import commands

# Inicializar el bot
bot = commands.Bot(command_prefix="!")

# Exportar el objeto bot
__all__ = ["bot"]
