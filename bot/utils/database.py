from supabase import create_client, Client
import config
import logging

logger = logging.getLogger(__name__)

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'client'):
            try:
                # Crear cliente sin opciones adicionales para evitar problemas de compatibilidad
                self.client: Client = create_client(
                    supabase_url=config.SUPABASE_URL,
                    supabase_key=config.SUPABASE_KEY
                )
            except Exception as e:
                logger.error(f"Error initializing Supabase client: {e}")
                raise
    
    # Guild Management
    def get_guild_config(self, guild_id: int):
        """Obtener configuración de un servidor"""
        try:
            response = self.client.table('guilds').select('*').eq('guild_id', str(guild_id)).execute()
            if response.data:
                return response.data[0]
            else:
                # Crear configuración por defecto
                return self.create_guild_config(guild_id)
        except Exception as e:
            logger.error(f"Error getting guild config: {e}")
            return None
    
    def create_guild_config(self, guild_id: int):
        """Crear configuración por defecto para un servidor"""
        try:
            data = {
                'guild_id': str(guild_id),
                'prefix': config.BOT_PREFIX,
                'automod_enabled': True,
                'levels_enabled': True,
                'welcome_enabled': False
            }
            response = self.client.table('guilds').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating guild config: {e}")
            return None
    
    def update_guild_config(self, guild_id: int, **kwargs):
        """Actualizar configuración de un servidor"""
        try:
            response = self.client.table('guilds').update(kwargs).eq('guild_id', str(guild_id)).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating guild config: {e}")
            return None
    
    # User Levels
    def get_user_level(self, guild_id: int, user_id: int):
        """Obtener nivel y XP de un usuario"""
        try:
            response = self.client.table('users').select('*').eq('guild_id', str(guild_id)).eq('user_id', str(user_id)).execute()
            if response.data:
                return response.data[0]
            else:
                return self.create_user(guild_id, user_id)
        except Exception as e:
            logger.error(f"Error getting user level: {e}")
            return None
    
    def create_user(self, guild_id: int, user_id: int):
        """Crear registro de usuario"""
        try:
            data = {
                'guild_id': str(guild_id),
                'user_id': str(user_id),
                'xp': 0,
                'level': 0,
                'messages': 0
            }
            response = self.client.table('users').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    def add_xp(self, guild_id: int, user_id: int, xp: int):
        """Agregar XP a un usuario"""
        try:
            user = self.get_user_level(guild_id, user_id)
            if not user:
                return None
            
            new_xp = user['xp'] + xp
            new_level = user['level']
            new_messages = user['messages'] + 1
            
            # Calcular nuevo nivel
            xp_needed = self.xp_for_level(new_level + 1)
            leveled_up = False
            
            while new_xp >= xp_needed:
                new_level += 1
                leveled_up = True
                xp_needed = self.xp_for_level(new_level + 1)
            
            response = self.client.table('users').update({
                'xp': new_xp,
                'level': new_level,
                'messages': new_messages
            }).eq('guild_id', str(guild_id)).eq('user_id', str(user_id)).execute()
            
            return {'leveled_up': leveled_up, 'new_level': new_level, 'data': response.data[0] if response.data else None}
        except Exception as e:
            logger.error(f"Error adding XP: {e}")
            return None
    
    def xp_for_level(self, level: int) -> int:
        """Calcular XP necesaria para un nivel"""
        return config.LEVEL_MULTIPLIER * (level ** 2)
    
    def get_leaderboard(self, guild_id: int, limit: int = 10):
        """Obtener tabla de clasificación"""
        try:
            response = self.client.table('users').select('*').eq('guild_id', str(guild_id)).order('level', desc=True).order('xp', desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []
    
    # Welcome Configuration
    def get_welcome_config(self, guild_id: int):
        """Obtener configuración de bienvenida"""
        try:
            response = self.client.table('welcome_config').select('*').eq('guild_id', str(guild_id)).execute()
            if response.data:
                return response.data[0]
            else:
                return self.create_welcome_config(guild_id)
        except Exception as e:
            logger.error(f"Error getting welcome config: {e}")
            return None
    
    def create_welcome_config(self, guild_id: int):
        """Crear configuración de bienvenida por defecto"""
        try:
            data = {
                'guild_id': str(guild_id),
                'channel_id': None,
                'message': '¡Bienvenido {user} a {server}!',
                'image_enabled': True,
                'image_background': '#7289da',
                'image_text_color': '#ffffff',
                'background_image_url': None
            }
            response = self.client.table('welcome_config').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating welcome config: {e}")
            return None
    
    def update_welcome_config(self, guild_id: int, **kwargs):
        """Actualizar configuración de bienvenida"""
        try:
            response = self.client.table('welcome_config').update(kwargs).eq('guild_id', str(guild_id)).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating welcome config: {e}")
            return None
    
    # Automod Configuration
    def get_automod_config(self, guild_id: int):
        """Obtener configuración de automoderación"""
        try:
            response = self.client.table('automod_config').select('*').eq('guild_id', str(guild_id)).execute()
            if response.data:
                return response.data[0]
            else:
                return self.create_automod_config(guild_id)
        except Exception as e:
            logger.error(f"Error getting automod config: {e}")
            return None
    
    def create_automod_config(self, guild_id: int):
        """Crear configuración de automoderación por defecto"""
        try:
            data = {
                'guild_id': str(guild_id),
                'anti_spam': True,
                'anti_links': False,
                'anti_invites': True,
                'bad_words': [],
                'max_mentions': config.MAX_MENTIONS,
                'max_emojis': config.MAX_EMOJIS
            }
            response = self.client.table('automod_config').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating automod config: {e}")
            return None
    
    def update_automod_config(self, guild_id: int, **kwargs):
        """Actualizar configuración de automoderación"""
        try:
            response = self.client.table('automod_config').update(kwargs).eq('guild_id', str(guild_id)).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating automod config: {e}")
            return None
    
    # Moderation Logs
    def log_moderation(self, guild_id: int, user_id: int, moderator_id: int, action: str, reason: str = None):
        """Registrar acción de moderación"""
        try:
            data = {
                'guild_id': str(guild_id),
                'user_id': str(user_id),
                'moderator_id': str(moderator_id),
                'action': action,
                'reason': reason
            }
            response = self.client.table('moderation_logs').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error logging moderation: {e}")
            return None
    
    def get_moderation_logs(self, guild_id: int, limit: int = 50):
        """Obtener logs de moderación"""
        try:
            response = self.client.table('moderation_logs').select('*').eq('guild_id', str(guild_id)).order('created_at', desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error getting moderation logs: {e}")
            return []

    # Verification Configuration
    def get_verification_config(self, guild_id: int):
        """Obtener configuración de verificación"""
        try:
            response = self.client.table('verification_config').select('*').eq('guild_id', str(guild_id)).execute()
            if response.data:
                return response.data[0]
            else:
                return self.create_verification_config(guild_id)
        except Exception as e:
            logger.error(f"Error getting verification config: {e}")
            return None
    
    def create_verification_config(self, guild_id: int):
        """Crear configuración de verificación por defecto"""
        try:
            data = {
                'guild_id': str(guild_id),
                'channel_id': None,
                'verified_role_id': None,
                # Actualizado para coincidir con la imagen
                'message': '¡Bienvenido/a a nuestro servidor! Para acceder a todos los canales, por favor lee las reglas y acepta al final.'
            }
            response = self.client.table('verification_config').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating verification config: {e}")
            return None
    
    def update_verification_config(self, guild_id: int, **kwargs):
        """Actualizar configuración de verificación"""
        try:
            response = self.client.table('verification_config').update(kwargs).eq('guild_id', str(guild_id)).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating verification config: {e}")
            return None
    
    # Game Roles Configuration
    def get_game_roles_config(self, guild_id: int):
        """Obtener configuración de roles de juegos"""
        try:
            response = self.client.table('game_roles_config').select('*').eq('guild_id', str(guild_id)).execute()
            if response.data:
                return response.data[0]
            else:
                return self.create_game_roles_config(guild_id)
        except Exception as e:
            logger.error(f"Error getting game roles config: {e}")
            return None
    
    def create_game_roles_config(self, guild_id: int):
        """Crear configuración de roles de juegos por defecto"""
        try:
            data = {
                'guild_id': str(guild_id),
                'channel_id': None,
                'message_id': None,
                'roles': {}
            }
            response = self.client.table('game_roles_config').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating game roles config: {e}")
            return None
    
    def update_game_roles_config(self, guild_id: int, **kwargs):
        """Actualizar configuración de roles de juegos"""
        try:
            response = self.client.table('game_roles_config').update(kwargs).eq('guild_id', str(guild_id)).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating game roles config: {e}")
            return None

    def get_roles_config(self, guild_id: int):
        """Obtener configuración de roles de juegos para un servidor"""
        try:
            response = self.client.table('game_roles_config').select('*').eq('guild_id', str(guild_id)).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error obteniendo configuración de roles: {e}")
            return None

    def update_roles_config(self, guild_id: int, roles: dict):
        """Actualizar configuración de roles de juegos para un servidor"""
        try:
            response = self.client.table('game_roles_config').update({"roles": roles}).eq('guild_id', str(guild_id)).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error actualizando configuración de roles: {e}")
            return None

# Instancia global
db = Database()
