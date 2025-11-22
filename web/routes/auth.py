from flask import Blueprint, redirect, request, session, url_for, jsonify
import requests
import config
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__)

@bp.route('/login')
def login():
    """Iniciar proceso de login con Discord OAuth2"""
    oauth_url = (
        f"{config.DISCORD_API_BASE}/oauth2/authorize"
        f"?client_id={config.DISCORD_CLIENT_ID}"
        f"&redirect_uri={config.REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={'+'.join(config.OAUTH2_SCOPES)}"
    )
    return redirect(oauth_url)

@bp.route('/callback')
def callback():
    """Callback de OAuth2"""
    code = request.args.get('code')
    
    if not code:
        return redirect(url_for('index'))
    
    # Intercambiar código por token
    data = {
        'client_id': config.DISCORD_CLIENT_ID,
        'client_secret': config.DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': config.REDIRECT_URI
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        # Obtener access token
        response = requests.post(f"{config.DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        
        access_token = token_data['access_token']
        
        # Obtener información del usuario
        headers = {
            'Authorization': f"Bearer {access_token}"
        }
        
        user_response = requests.get(f"{config.DISCORD_API_BASE}/users/@me", headers=headers)
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Obtener guilds del usuario
        guilds_response = requests.get(f"{config.DISCORD_API_BASE}/users/@me/guilds", headers=headers)
        guilds_response.raise_for_status()
        guilds_data = guilds_response.json()
        
        # Filtrar guilds donde el usuario es administrador
        admin_guilds = [
            guild for guild in guilds_data
            if (int(guild['permissions']) & 0x8) == 0x8  # Administrator permission
        ]
        
        # Guardar en sesión
        session['user'] = {
            'id': user_data['id'],
            'username': user_data['username'],
            'discriminator': user_data.get('discriminator', '0'),
            'avatar': user_data['avatar'],
            'access_token': access_token
        }
        
        session['guilds'] = admin_guilds
        
        logger.info(f"User logged in: {user_data['username']} ({user_data['id']})")
        
        return redirect(url_for('dashboard.dashboard'))
    
    except Exception as e:
        logger.error(f"Error in OAuth callback: {e}")
        return redirect(url_for('index'))

@bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('index'))

@bp.route('/api/user')
def api_user():
    """API endpoint para obtener información del usuario"""
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify(user)
