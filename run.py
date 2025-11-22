import asyncio
import threading
import logging
import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

def run_web():
    """Ejecutar servidor web Flask"""
    logger.info("Starting web server...")
    from web.app import app
    app.run(host='0.0.0.0', port=config.WEB_PORT, debug=False, use_reloader=False)

def run_bot():
    """Ejecutar bot de Discord"""
    logger.info("Starting Discord bot...")
    from bot.main import main
    asyncio.run(main())

if __name__ == "__main__":
    # Verificar variables de entorno críticas
    if not config.DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN no está configurado. Por favor configura las variables de entorno.")
        sys.exit(1)
    
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        logger.error("SUPABASE_URL o SUPABASE_KEY no están configurados. Por favor configura las variables de entorno.")
        sys.exit(1)
    
    # Importar base de datos para evitar deadlocks en imports
    # Se hace aquí para asegurar que las variables de entorno estén verificadas
    from bot.utils.database import db

    logger.info("Starting BotRexy...")
    logger.info(f"Web server will run on port {config.WEB_PORT}")
    
    # Iniciar servidor web en un thread separado
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    
    # Ejecutar bot en el thread principal
    try:
        run_bot()
    except KeyboardInterrupt:
        logger.info("Shutting down BotRexy...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
