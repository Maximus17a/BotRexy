from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import requests
import logging
from bot import bot
import discord
from bot.utils.database import db

logger = logging.getLogger(__name__)

verification_bp = Blueprint('verification', __name__)

@verification_bp.route('/guilds/<guild_id>/verification')
def verification_config(guild_id):
    """Página de configuración de verificación"""
    try:
        # Verificar sesión
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        
        user_info = session['user']
        
        # Corrección: El access_token está DENTRO del diccionario 'user'
        token = user_info.get('access_token')
        
        if not token:
            # Si no hay token, forzar re-login
            return redirect(url_for('auth.login'))

        # Obtener información del servidor desde Discord API
        headers = {'Authorization': f"Bearer {token}"}
        
        # Verificar que el usuario es administrador del servidor
        response = requests.get('https://discord.com/api/users/@me/guilds', headers=headers)
        
        if response.status_code == 401:
            # Token expirado o inválido
            return redirect(url_for('auth.login'))
            
        user_guilds = response.json()
        guild_data = next((g for g in user_guilds if g['id'] == guild_id), None)
        
        if not guild_data or not (int(guild_data['permissions']) & 0x8):  # Administrator permission
            return "No tienes permisos de administrador en este servidor", 403
        
        # Obtener canales y roles del servidor usando el bot
        guild = bot.get_guild(int(guild_id))
        channels = []
        roles = []
        
        if guild:
            channels = [
                {'id': str(c.id), 'name': c.name} 
                for c in guild.channels 
                if isinstance(c, discord.TextChannel)
            ]
            roles = [
                {'id': str(r.id), 'name': r.name} 
                for r in guild.roles 
                if not r.managed and r.name != "@everyone"
            ]
        
        # Obtener configuración actual
        verification_config = db.get_verification_config(int(guild_id))
        guild_config = db.get_guild_config(int(guild_id))
        
        return render_template(
            'verification_config.html',
            guild=guild_data,
            channels=channels,
            roles=roles,
            config=guild_config if guild_config else {},
            verification_config=verification_config
        )
    
    except Exception as e:
        logger.error(f"Error in verification config: {e}", exc_info=True)
        # Si ocurre un error de sesión, intentar redirigir al login
        return redirect(url_for('auth.login'))


@verification_bp.route('/guilds/<guild_id>/game-roles')
def game_roles_config(guild_id):
    """Página de configuración de roles de juegos"""
    try:
        # Verificar sesión
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        
        user_info = session['user']
        token = user_info.get('access_token')
        
        if not token:
            return redirect(url_for('auth.login'))
        
        # Obtener información del servidor desde Discord API
        headers = {'Authorization': f"Bearer {token}"}
        
        # Verificar que el usuario es administrador del servidor
        response = requests.get('https://discord.com/api/users/@me/guilds', headers=headers)
        
        if response.status_code == 401:
            return redirect(url_for('auth.login'))

        user_guilds = response.json()
        guild = next((g for g in user_guilds if g['id'] == guild_id), None)
        
        if not guild or not (int(guild['permissions']) & 0x8):  # Administrator permission
            return "No tienes permisos de administrador en este servidor", 403
        
        # Obtener canales y roles del servidor
        channels = []
        roles = []
        
        # Obtener configuración actual
        game_roles_config = {}
        
        return render_template(
            'game_roles_config.html',
            guild=guild,
            channels=channels,
            roles=roles,
            game_roles_config=game_roles_config
        )
    
    except Exception as e:
        logger.error(f"Error in game roles config: {e}")
        return redirect(url_for('auth.login'))


# API endpoints
@verification_bp.route('/api/guilds/<guild_id>/verification', methods=['POST'])
def update_verification(guild_id):
    """Actualizar configuración de verificación"""
    try:
        if 'user' not in session:
            return jsonify({'success': False, 'error': 'No autorizado'}), 401
        
        data = request.json
        
        # Separar el campo 'verification_enabled' porque va en la tabla 'guilds', no en 'verification_config'
        verification_enabled = data.pop('verification_enabled', None)
        
        # 1. Actualizar configuración específica de verificación (tabla verification_config)
        if data:
            db.update_verification_config(int(guild_id), **data)
        
        # 2. Actualizar estado habilitado/deshabilitado (tabla guilds)
        if verification_enabled is not None:
            db.update_guild_config(int(guild_id), verification_enabled=bool(verification_enabled))
        
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Error updating verification: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@verification_bp.route('/api/guilds/<guild_id>/game-roles', methods=['POST'])
def add_game_role(guild_id):
    """Agregar rol de juego"""
    try:
        if 'user' not in session:
            return jsonify({'success': False, 'error': 'No autorizado'}), 401
        
        data = request.json
        
        # Aquí se actualizaría la base de datos
        # db.update_game_roles_config(guild_id, ...)
        
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Error adding game role: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@verification_bp.route('/api/guilds/<guild_id>/game-roles/<game_name>', methods=['DELETE'])
def remove_game_role(guild_id, game_name):
    """Remover rol de juego"""
    try:
        if 'user' not in session:
            return jsonify({'success': False, 'error': 'No autorizado'}), 401
        
        # Aquí se actualizaría la base de datos
        
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Error removing game role: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@verification_bp.route('/api/guilds/<guild_id>/game-roles/create-panel', methods=['POST'])
def create_game_roles_panel(guild_id):
    """Crear panel de roles de juegos en Discord"""
    try:
        if 'user' not in session:
            return jsonify({'success': False, 'error': 'No autorizado'}), 401
        
        data = request.json
        
        # Aquí se enviaría un comando al bot para crear el panel
        
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Error creating game roles panel: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500