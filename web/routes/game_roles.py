from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from bot.utils.database import db
import logging
import discord
from bot import bot
import asyncio

logger = logging.getLogger(__name__)

bp = Blueprint('game_roles', __name__, url_prefix='/game-roles')

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
def game_roles_editor(guild_id):
    """Editor de configuración de roles de juegos"""
    user = session.get('user')
    guilds = session.get('guilds', [])
    
    # Verificar que el usuario tenga acceso a este servidor
    guild = next((g for g in guilds if g['id'] == guild_id), None)
    
    if not guild:
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('game_roles_config.html', user=user, guild=guild)

@bp.route('/api/<guild_id>/config', methods=['GET'])
@login_required
def get_game_roles_config(guild_id):
    """Obtener configuración de roles de juegos"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        config = db.get_game_roles_config(int(guild_id))
        
        return jsonify(config)
    except Exception as e:
        logger.error(f"Error getting game roles config: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/config', methods=['POST'])
@login_required
def update_game_roles_config(guild_id):
    """Actualizar configuración de roles de juegos"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.json
        
        # Actualizar configuración
        db.update_game_roles_config(int(guild_id), **data)
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error updating game roles config: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/add-role', methods=['POST'])
@login_required
def add_game_role(guild_id):
    """Agregar un rol de juego"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.json
        game_name = data.get('game_name')
        role_id = data.get('role_id')
        
        if not game_name or not role_id:
            return jsonify({'error': 'Missing parameters'}), 400
        
        # Obtener configuración actual
        config = db.get_game_roles_config(int(guild_id))
        roles = config.get('roles', {})
        
        # Agregar nuevo rol
        if isinstance(roles, dict):
            roles[game_name] = role_id
        else:
            roles = {game_name: role_id}
        
        # Actualizar
        db.update_game_roles_config(int(guild_id), roles=roles)
        
        return jsonify({'success': True, 'roles': roles})
    except Exception as e:
        logger.error(f"Error adding game role: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/remove-role', methods=['POST'])
@login_required
def remove_game_role(guild_id):
    """Eliminar un rol de juego"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.json
        game_name = data.get('game_name')
        
        if not game_name:
            return jsonify({'error': 'Missing game_name'}), 400
        
        # Obtener configuración actual
        config = db.get_game_roles_config(int(guild_id))
        roles = config.get('roles', {})
        
        # Eliminar rol
        if isinstance(roles, dict) and game_name in roles:
            del roles[game_name]
        
        # Actualizar
        db.update_game_roles_config(int(guild_id), roles=roles)
        
        return jsonify({'success': True, 'roles': roles})
    except Exception as e:
        logger.error(f"Error removing game role: {e}")
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
        discord_channels = bot.get_guild_channels(guild_id)
        channels = [
            {'id': str(channel.id), 'name': channel.name}
            for channel in discord_channels if channel.type == discord.ChannelType.text
        ]

        return jsonify(channels)
    except Exception as e:
        logger.error(f"Error getting channels: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/roles', methods=['GET'])
@login_required
def get_roles(guild_id):
    """Obtener roles del servidor desde Discord"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403

        # Obtener roles desde Discord
        discord_roles = bot.get_guild_roles(guild_id)
        roles = [
            {'id': str(role.id), 'name': role.name}
            for role in discord_roles if not role.managed
        ]

        return jsonify(roles)
    except Exception as e:
        logger.error(f"Error getting roles: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/api/<guild_id>/create-panel', methods=['POST'])
@login_required
async def create_panel(guild_id):
    """Crear panel de roles en Discord"""
    try:
        # Verificar acceso
        guilds = session.get('guilds', [])
        if not any(g['id'] == guild_id for g in guilds):
            return jsonify({'error': 'Unauthorized'}), 403

        # Obtener configuración actual
        config = db.get_game_roles_config(int(guild_id))
        if not config or not config.get('channel_id'):
            return jsonify({'error': 'No hay canal configurado'}), 400

        roles = config.get('roles', {})
        if not roles:
            return jsonify({'error': 'No hay roles configurados'}), 400

        # Crear embed
        embed = discord.Embed(
            title="Selección de Roles",
            description="Haz clic en los botones de abajo para obtener o remover roles de juegos y actividades.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="¿Cómo funciona?",
            value="- Haz clic en un botón para agregar el rol\n- Si ya tienes el rol, haz clic nuevamente para quitarlo",
            inline=False
        )

        for game_name, role_id in roles.items():
            embed.add_field(
                name=game_name,
                value=f"<@&{role_id}>",
                inline=True
            )

        # Crear botones
        view = discord.ui.View()
        for game_name, role_id in roles.items():
            view.add_item(
                discord.ui.Button(
                    label=game_name,
                    custom_id=f"role_{role_id}",
                    style=discord.ButtonStyle.primary
                )
            )

        # Enviar mensaje al canal
        channel = bot.get_channel(int(config['channel_id']))
        if not channel:
            return jsonify({'error': 'Canal no encontrado'}), 404

        message = await channel.send(embed=embed, view=view)

        # Actualizar message_id en la base de datos
        db.update_game_roles_config(int(guild_id), message_id=str(message.id))

        return jsonify({'success': True, 'message_id': message.id})
    except Exception as e:
        logger.error(f"Error creating panel: {e}")
        return jsonify({'error': 'Internal server error'}), 500
