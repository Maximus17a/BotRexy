from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, send_file
from bot.utils.database import db
from bot.utils.image_gen import image_generator
import logging
import io

logger = logging.getLogger(__name__)

bp = Blueprint('welcome', __name__, url_prefix='/welcome')

def login_required(f):
    """Decorador para requerir login"""
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/<guild_id>')
@login_required
def welcome_editor(guild_id):
    """Editor de configuración de bienvenida"""
    user = session.get('user')
    guilds = session.get('guilds', [])
    
    # Verificar que el usuario tenga acceso a este servidor
    guild = next((g for g in guilds if g['id'] == guild_id), None)
    
    if not guild:
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('welcome_config.html', user=user, guild=guild)

@bp.route('/api/<guild_id>/config', methods=['GET'])
@login_required
def get_welcome_config(guild_id):
    """Obtener configuración de bienvenida"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        config = db.get_welcome_config(int(guild_id))
        
        return jsonify(config)
    except Exception as e:
        logger.error(f"Error getting welcome config: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/config', methods=['POST'])
@login_required
def update_welcome_config(guild_id):
    """Actualizar configuración de bienvenida"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.json
        
        # Actualizar configuración
        db.update_welcome_config(int(guild_id), **data)
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error updating welcome config: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/preview', methods=['POST'])
@login_required
def preview_welcome(guild_id):
    """Previsualizar imagen de bienvenida"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        guild = next((g for g in guilds if g['id'] == guild_id), None)
        
        if not guild:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.json
        user = session.get('user')
        
        # Generar imagen de preview
        avatar_url = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
        
        image_bytes = image_generator.generate(
            user_name=data.get('user_name', user['username']),
            user_avatar_url=avatar_url,
            server_name=guild['name'],
            bg_color=data.get('bg_color', '#7289da'),
            text_color=data.get('text_color', '#ffffff')
        )
        
        if not image_bytes:
            return jsonify({'error': 'Failed to generate image'}), 500
        
        return send_file(image_bytes, mimetype='image/png')
    except Exception as e:
        logger.error(f"Error previewing welcome: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/channels', methods=['GET'])
@login_required
def get_channels(guild_id):
    """Obtener canales del servidor (simulado, requiere bot activo)"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # En producción, esto debería obtener los canales del bot
        # Por ahora retornamos un placeholder
        return jsonify([
            {'id': '0', 'name': 'Selecciona un canal', 'type': 0}
        ])
    except Exception as e:
        logger.error(f"Error getting channels: {e}")
        return jsonify({'error': 'Internal server error'}), 500
