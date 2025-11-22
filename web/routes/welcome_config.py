from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, send_file
from bot.utils.database import db
from bot.utils.image_gen import image_generator
from bot import bot
import discord
import logging
import io
import os
from werkzeug.utils import secure_filename
import uuid

logger = logging.getLogger(__name__)

# Configuración de subida de imágenes
UPLOAD_FOLDER = 'web/static/images/backgrounds'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        
        # Obtener configuración de welcome_config
        config = db.get_welcome_config(int(guild_id))
        
        # Obtener el estado de welcome_enabled desde guilds
        guild_config = db.get_guild_config(int(guild_id))
        if guild_config:
            config['welcome_enabled'] = guild_config.get('welcome_enabled', False)
        else:
            config['welcome_enabled'] = False
        
        return jsonify(config)
    except Exception as e:
        logger.error(f"Error getting welcome config: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/config', methods=['POST'])
@login_required
def update_welcome_config(guild_id):
    """Actualizar configuración de bienvenida (SECURIZED)"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.json
        
        # SECURITY: Mass Assignment Protection
        # Solo permitir campos específicos
        allowed_fields = {
            'channel_id', 'message', 'image_enabled', 
            'image_background', 'image_text_color'
        }
        
        safe_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        # Separar welcome_enabled que va en otra tabla
        welcome_enabled = data.get('welcome_enabled')
        
        # Actualizar configuración segura
        db.update_welcome_config(int(guild_id), **safe_data)
        
        # Actualizar welcome_enabled en guilds si se proporcionó
        if welcome_enabled is not None:
            db.update_guild_config(int(guild_id), welcome_enabled=bool(welcome_enabled))
        
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
        
        # Obtener URL de imagen de fondo si existe
        background_image_url = data.get('background_image_url')
        if background_image_url and background_image_url.startswith('/'):
            # Convertir ruta relativa a absoluta
            background_image_url = request.host_url.rstrip('/') + background_image_url
        
        image_bytes = image_generator.generate(
            user_name=data.get('user_name', user['username']),
            user_avatar_url=avatar_url,
            server_name=guild['name'],
            bg_color=data.get('bg_color', '#7289da'),
            text_color=data.get('text_color', '#ffffff'),
            background_image_url=background_image_url
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
    """Obtener canales del servidor desde Discord"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403

        # Obtener canales desde Discord
        guild = bot.get_guild(int(guild_id))
        if not guild:
            return jsonify({'error': 'Guild not found'}), 404
            
        channels = [
            {'id': str(channel.id), 'name': channel.name, 'type': channel.type.value}
            for channel in guild.channels 
            if channel.type == discord.ChannelType.text or channel.type == discord.ChannelType.news
        ]

        return jsonify(channels)
    except Exception as e:
        logger.error(f"Error getting channels: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/upload-background', methods=['POST'])
@login_required
def upload_background(guild_id):
    """Subir imagen de fondo personalizada"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        if 'background_image' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['background_image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Generar nombre único
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{guild_id}_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Guardar archivo
            file.save(filepath)
            
            # Generar URL de la imagen
            image_url = f"/static/images/backgrounds/{filename}"
            
            # Actualizar configuración en base de datos
            db.update_welcome_config(int(guild_id), background_image_url=image_url)
            
            return jsonify({
                'success': True,
                'image_url': image_url
            })
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        logger.error(f"Error uploading background: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/remove-background', methods=['POST'])
@login_required
def remove_background(guild_id):
    """Eliminar imagen de fondo personalizada"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Obtener configuración actual
        config = db.get_welcome_config(int(guild_id))
        
        if config and config.get('background_image_url'):
            # Intentar eliminar archivo físico
            try:
                filename = config['background_image_url'].split('/')[-1]
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                logger.warning(f"Could not delete file: {e}")
        
        # Actualizar configuración en base de datos
        db.update_welcome_config(int(guild_id), background_image_url=None)
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Error removing background: {e}")
        return jsonify({'error': 'Internal server error'}), 500