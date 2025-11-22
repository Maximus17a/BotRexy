-- Migración: Agregar campo background_image_url a welcome_config
-- Fecha: 2025-11-21
-- Descripción: Permite a los usuarios subir una imagen de fondo personalizada para los mensajes de bienvenida

-- Agregar columna si no existe
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'welcome_config' 
        AND column_name = 'background_image_url'
    ) THEN
        ALTER TABLE welcome_config ADD COLUMN background_image_url TEXT;
        RAISE NOTICE 'Columna background_image_url agregada exitosamente';
    ELSE
        RAISE NOTICE 'La columna background_image_url ya existe';
    END IF;
END $$;
