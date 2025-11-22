import discord
from discord.ext import commands
import asyncio
import logging
import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BotRexy(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = False
        
        super().__init__(
            command_prefix=config.BOT_PREFIX,
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self):
        """Cargar cogs al iniciar"""
        cogs = [
            'bot.cogs.moderation',
            'bot.cogs.levels',
            'bot.cogs.welcome',
            'bot.cogs.automod',
            'bot.cogs.game_roles',
            'bot.cogs.verification'
            
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}: {e}")
        
        # Sincronizar comandos slash
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Evento cuando el bot está listo"""
        logger.info(f'Bot conectado como {self.user} (ID: {self.user.id})')
        logger.info(f'Conectado a {len(self.guilds)} servidor(es)')
        
        # Establecer presencia
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servidores | /help"
            )
        )
    
    async def on_guild_join(self, guild):
        """Evento cuando el bot se une a un servidor"""
        logger.info(f'Bot añadido al servidor: {guild.name} (ID: {guild.id})')
        
        # Actualizar presencia
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servidores | /help"
            )
        )
    
    async def on_guild_remove(self, guild):
        """Evento cuando el bot es removido de un servidor"""
        logger.info(f'Bot removido del servidor: {guild.name} (ID: {guild.id})')
        
        # Actualizar presencia
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servidores | /help"
            )
        )

# Instancia global del bot
bot = BotRexy()

async def main():
    """Función principal"""
    if not config.DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN no está configurado en las variables de entorno")
        return
    
    # Usar la instancia global
    global bot
    
    try:
        await bot.start(config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error al ejecutar el bot: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
