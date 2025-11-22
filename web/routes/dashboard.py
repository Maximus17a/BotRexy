from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from bot.utils.database import db
from bot import bot
import logging
import discord

logger = logging.getLogger(__name__)

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def login_required(f):
    """Decorador para requerir login"""
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/')
@login_required
def dashboard():
    """Dashboard principal"""
    user = session.get('user')
    guilds = session.get('guilds', [])
    
    return render_template('dashboard.html', user=user, guilds=guilds)

@bp.route('/server/<guild_id>')
@login_required
def server_config(guild_id):
    """Configuración de servidor específico"""
    user = session.get('user')
    guilds = session.get('guilds', [])
    
    # Verificar que el usuario tenga acceso a este servidor
    guild = next((g for g in guilds if g['id'] == guild_id), None)
    
    if not guild:
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('server_config.html', user=user, guild=guild)

@bp.route('/api/server/<guild_id>/config', methods=['GET'])
@login_required
def get_server_config(guild_id):
    """Obtener configuración del servidor"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Obtener configuraciones
        guild_config = db.get_guild_config(int(guild_id))
        automod_config = db.get_automod_config(int(guild_id))
        welcome_config = db.get_welcome_config(int(guild_id))
        
        return jsonify({
            'guild': guild_config,
            'automod': automod_config,
            'welcome': welcome_config
        })
    except Exception as e:
        logger.error(f"Error getting server config: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/server/<guild_id>/config', methods=['POST'])
@login_required
def update_server_config(guild_id):
    """Actualizar configuración del servidor"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.json
        
        # Actualizar configuración según el tipo
        config_type = data.get('type')
        
        if config_type == 'guild':
            db.update_guild_config(int(guild_id), **data.get('config', {}))
        elif config_type == 'automod':
            db.update_automod_config(int(guild_id), **data.get('config', {}))
        elif config_type == 'welcome':
            db.update_welcome_config(int(guild_id), **data.get('config', {}))
        else:
            return jsonify({'error': 'Invalid config type'}), 400
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error updating server config: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/server/<guild_id>/leaderboard', methods=['GET'])
@login_required
def get_leaderboard(guild_id):
    """Obtener leaderboard del servidor"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        limit = request.args.get('limit', 10, type=int)
        leaderboard = db.get_leaderboard(int(guild_id), limit)
        
        return jsonify(leaderboard)
    except Exception as e:
        logger.error(f"Error getting leaderboard: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/server/<guild_id>/modlogs', methods=['GET'])
@login_required
def get_modlogs(guild_id):
    """Obtener logs de moderación"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        limit = request.args.get('limit', 50, type=int)
        logs = db.get_moderation_logs(int(guild_id), limit)
        
        return jsonify(logs)
    except Exception as e:
        logger.error(f"Error getting modlogs: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/server/<guild_id>/leaderboard')
@login_required
def leaderboard(guild_id):
    """Tabla de clasificación del servidor"""
    user = session.get('user')
    guilds = session.get('guilds', [])
    
    # Verificar acceso
    guild_data = next((g for g in guilds if g['id'] == guild_id), None)
    if not guild_data:
        return redirect(url_for('dashboard.dashboard'))
    
    # Obtener datos del leaderboard
    leaderboard_data = db.get_leaderboard(int(guild_id), limit=100)
    
    # Enriquecer datos con nombres de usuario
    enriched_data = []
    guild = bot.get_guild(int(guild_id))
    
    for entry in leaderboard_data:
        user_name = "Usuario Desconocido"
        avatar_url = None
        
        if guild:
            member = guild.get_member(int(entry['user_id']))
            if member:
                user_name = member.name
                avatar_url = member.display_avatar.url
            else:
                # Intentar obtener usuario globalmente si no está en el servidor
                try:
                    discord_user = bot.get_user(int(entry['user_id']))
                    if discord_user:
                        user_name = discord_user.name
                        avatar_url = discord_user.display_avatar.url
                except:
                    pass
        
        entry['username'] = user_name
        entry['avatar_url'] = avatar_url
        enriched_data.append(entry)
    
    return render_template('leaderboard.html', user=user, guild=guild_data, leaderboard=enriched_data)

@bp.route('/server/<guild_id>/logs')
@login_required
def logs(guild_id):
    """Logs de moderación del servidor"""
    user = session.get('user')
    guilds = session.get('guilds', [])
    
    # Verificar acceso
    guild_data = next((g for g in guilds if g['id'] == guild_id), None)
    if not guild_data:
        return redirect(url_for('dashboard.dashboard'))
    
    # Obtener logs
    logs_data = db.get_moderation_logs(int(guild_id), limit=50)
    
    # Enriquecer datos
    enriched_logs = []
    guild = bot.get_guild(int(guild_id))
    
    for log in logs_data:
        moderator_name = "Desconocido"
        user_name = "Desconocido"
        
        if guild:
            # Resolver moderador
            mod = guild.get_member(int(log['moderator_id']))
            if mod:
                moderator_name = mod.name
            
            # Resolver usuario afectado
            target = guild.get_member(int(log['user_id']))
            if target:
                user_name = target.name
        
        log['moderator_name'] = moderator_name
        log['user_name'] = user_name
        enriched_logs.append(log)
    
    return render_template('logs.html', user=user, guild=guild_data, logs=enriched_logs)
