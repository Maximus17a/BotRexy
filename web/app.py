from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect  # Importar CSRF
import sys
import os
import logging

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from bot.utils.database import db

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(config)  # Cargar configuración desde objeto
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH  # Aplicar límite de tamaño
CORS(app)

# Inicializar protección CSRF
csrf = CSRFProtect(app)

# Importar rutas
from web.routes import auth, dashboard, legal
from web.routes.welcome_config import bp as welcome_bp
from web.routes.game_roles import bp as game_roles_bp
from web.routes.verification_routes import verification_bp

# Registrar blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(welcome_bp)
app.register_blueprint(game_roles_bp)
app.register_blueprint(legal.bp)
app.register_blueprint(verification_bp)

@app.route('/')
def index():
    """Página principal"""
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/invite')
def invite():
    """Redirigir a invitación del bot"""
    invite_url = f"https://discord.com/api/oauth2/authorize?client_id={config.DISCORD_CLIENT_ID}&permissions=8&scope=bot%20applications.commands"
    return redirect(invite_url)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return render_template('500.html'), 500

# Manejar errores de tamaño de archivo
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'Archivo demasiado grande (Max 5MB)'}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.WEB_PORT, debug=False)