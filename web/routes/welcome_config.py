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

# Configuración de subida de imágenes (usar la de app.config si estuviera disponible, o hardcoded segura)
UPLOAD_FOLDER = 'web/static/images/backgrounds'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('welcome', __name__, url_prefix='/welcome')

# ... (login_required y welcome_editor sin cambios) ...

@bp.route('/<guild_id>')
@login_required
def welcome_editor(guild_id):
    """Editor de configuración de bienvenida"""
    user = session.get('user')
    guilds = session.get('guilds', [])
    guild = next((g for g in guilds if g['id'] == guild_id), None)
    if not guild:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('welcome_config.html', user=user, guild=guild)

@bp.route('/api/<guild_id>/config', methods=['GET'])
@login_required
def get_welcome_config(guild_id):
    # ... (Sin cambios en GET) ...
    try:
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        config = db.get_welcome_config(int(guild_id))
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
        # Solo permitir campos específicos, ignorar background_image_url (se maneja via upload)
        allowed_fields = {
            'channel_id', 'message', 'image_enabled', 
            'image_background', 'image_text_color'
        }
        
        safe_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        # Separar welcome_enabled que va en otra tabla
        welcome_enabled = data.get('welcome_enabled')
        
        # Actualizar configuración segura
        db.update_welcome_config(int(guild_id), **safe_data)
        
        # Actualizar welcome_enabled en guilds
        if welcome_enabled is not None:
            db.update_guild_config(int(guild_id), welcome_enabled=bool(welcome_enabled))
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error updating welcome config: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/upload-background', methods=['POST'])
@login_required
def upload_background(guild_id):
    """Subir imagen de fondo personalizada (Con protección de tamaño en config)"""
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
            # Generar nombre único seguro
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{guild_id}_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Guardar archivo
            file.save(filepath)
            
            # Generar URL relativa (segura)
            image_url = f"/static/images/backgrounds/{filename}"
            
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

# ... (El resto de funciones remove_background, preview_welcome, get_channels sin cambios mayores, 
# pero preview_welcome se beneficia de que update_welcome_config ya no deja inyectar URLs externas) ...