-- BotRexy Database Schema for Supabase
-- Ejecutar este script en el SQL Editor de Supabase

-- Tabla de configuración de servidores
CREATE TABLE IF NOT EXISTS guilds (
    id BIGSERIAL PRIMARY KEY,
    guild_id TEXT UNIQUE NOT NULL,
    prefix TEXT DEFAULT '!',    automod_enabled BOOLEAN DEFAULT false,
    levels_enabled BOOLEAN DEFAULT true,
    welcome_enabled BOOLEAN DEFAULT false,
    verification_enabled BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de usuarios y niveles
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    guild_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0,
    messages INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(guild_id, user_id)
);

-- Tabla de configuración de bienvenida
CREATE TABLE IF NOT EXISTS welcome_config (
    id BIGSERIAL PRIMARY KEY,
    guild_id TEXT UNIQUE NOT NULL,
    channel_id TEXT,
    message TEXT DEFAULT '¡Bienvenido {user} a {server}!',
    image_enabled BOOLEAN DEFAULT TRUE,
    image_background TEXT DEFAULT '#7289da',
    image_text_color TEXT DEFAULT '#ffffff',
    background_image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de configuración de automoderación
CREATE TABLE IF NOT EXISTS automod_config (
    id BIGSERIAL PRIMARY KEY,
    guild_id TEXT UNIQUE NOT NULL,
    anti_spam BOOLEAN DEFAULT TRUE,
    anti_links BOOLEAN DEFAULT FALSE,
    anti_invites BOOLEAN DEFAULT TRUE,
    bad_words JSONB DEFAULT '[]'::jsonb,
    max_mentions INTEGER DEFAULT 5,
    max_emojis INTEGER DEFAULT 10,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de logs de moderación
CREATE TABLE IF NOT EXISTS moderation_logs (
    id BIGSERIAL PRIMARY KEY,
    guild_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    moderator_id TEXT NOT NULL,
    action TEXT NOT NULL,
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_users_guild_id ON users(guild_id);
CREATE INDEX IF NOT EXISTS idx_users_level ON users(guild_id, level DESC, xp DESC);
CREATE INDEX IF NOT EXISTS idx_moderation_logs_guild_id ON moderation_logs(guild_id);
CREATE INDEX IF NOT EXISTS idx_moderation_logs_created_at ON moderation_logs(created_at DESC);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para actualizar updated_at
CREATE TRIGGER update_guilds_updated_at BEFORE UPDATE ON guilds
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_welcome_config_updated_at BEFORE UPDATE ON welcome_config
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_automod_config_updated_at BEFORE UPDATE ON automod_config
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Tabla de configuración de verificación
CREATE TABLE IF NOT EXISTS verification_config (
    id BIGSERIAL PRIMARY KEY,
    guild_id TEXT UNIQUE NOT NULL,
    channel_id TEXT,
    verified_role_id TEXT,
    message TEXT DEFAULT '¡Bienvenido! Por favor verifica que eres humano.',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de configuración de roles de juegos
CREATE TABLE IF NOT EXISTS game_roles_config (
    id BIGSERIAL PRIMARY KEY,
    guild_id TEXT UNIQUE NOT NULL,
    channel_id TEXT,
    message_id TEXT,
    roles JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Triggers para actualizar updated_at
CREATE TRIGGER update_verification_config_updated_at BEFORE UPDATE ON verification_config
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_game_roles_config_updated_at BEFORE UPDATE ON game_roles_config
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comentarios para documentación
COMMENT ON TABLE guilds IS 'Configuración general de cada servidor de Discord';
COMMENT ON TABLE users IS 'Datos de usuarios, niveles y experiencia por servidor';
COMMENT ON TABLE welcome_config IS 'Configuración de mensajes de bienvenida por servidor';
COMMENT ON TABLE automod_config IS 'Configuración de automoderación por servidor';
COMMENT ON TABLE moderation_logs IS 'Registro de acciones de moderación';
COMMENT ON TABLE verification_config IS 'Configuración del sistema de verificación por servidor';
COMMENT ON TABLE game_roles_config IS 'Configuración de roles de juegos por servidor';
