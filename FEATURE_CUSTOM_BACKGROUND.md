# Nueva Funcionalidad: Imagen de Fondo Personalizada en Mensajes de Bienvenida

## Fecha: 21 de Noviembre, 2025
## Versión: 2.1.0

## Descripción

Se ha implementado la funcionalidad para que los administradores de servidor puedan subir una imagen personalizada como fondo para los mensajes de bienvenida. Anteriormente, solo era posible seleccionar un color sólido de fondo. Ahora, la imagen del usuario aparecerá sobre el fondo personalizado, proporcionando una experiencia más rica y personalizada.

## Cambios Realizados

### 1. Base de Datos (`bot/utils/database.py`)
- ✅ Agregado campo `background_image_url` en la tabla `welcome_config`
- ✅ Actualizado `create_welcome_config()` para incluir el nuevo campo
- ✅ El campo permite valores NULL (usa color de fondo si no hay imagen)

### 2. Backend - Rutas Web (`web/routes/welcome_config.py`)
- ✅ **Nuevo endpoint**: `POST /api/<guild_id>/upload-background`
  - Acepta archivos de imagen (PNG, JPG, JPEG, GIF, WebP)
  - Genera nombre único con UUID para evitar colisiones
  - Guarda la imagen en `web/static/images/backgrounds/`
  - Actualiza la URL en la base de datos
  
- ✅ **Nuevo endpoint**: `POST /api/<guild_id>/remove-background`
  - Elimina la imagen física del servidor
  - Limpia el campo en la base de datos
  
- ✅ Actualizado endpoint `POST /api/<guild_id>/preview`
  - Ahora incluye soporte para imagen de fondo personalizada
  - Convierte rutas relativas a URLs absolutas

### 3. Generador de Imágenes (`bot/utils/image_gen.py`)
- ✅ Actualizada función `generate()` para aceptar parámetro `background_image_url`
- ✅ Nueva función `_download_background()`:
  - Descarga imagen desde URL
  - Convierte a RGB si es necesario
  - Redimensiona a 800x300px usando interpolación LANCZOS
  - Fallback automático a color sólido si falla la descarga

### 4. Interfaz Web (`web/templates/welcome_config.html`)
- ✅ **Nuevo campo**: Input de tipo `file` para subir imagen
  - Acepta formatos: PNG, JPG, JPEG, GIF, WebP
  - Preview de la imagen actual subida
  - Botón para eliminar imagen de fondo
  
- ✅ **Actualizado**: Campo de color de fondo ahora es "alternativo"
  - Se usa cuando no hay imagen personalizada
  
- ✅ **JavaScript actualizado**:
  - `loadConfig()`: Carga y muestra imagen de fondo actual
  - `welcomeForm.submit`: Sube imagen antes de guardar configuración
  - `previewBtn.click`: Incluye imagen de fondo en la vista previa
  - `removeBackgroundBtn.click`: Elimina imagen de fondo

### 5. Cog de Discord (`bot/cogs/welcome.py`)
- ✅ Actualizado evento `on_member_join` para pasar `background_image_url` al generador

### 6. Esquema de Base de Datos
- ✅ Actualizado `database_schema.sql` con nuevo campo
- ✅ Creado script de migración en `migrations/add_background_image_url.sql`

### 7. Estructura de Archivos
- ✅ Creado directorio `web/static/images/backgrounds/`
- ✅ Agregado `.gitignore` para excluir imágenes subidas del control de versiones
- ✅ Agregado `.gitkeep` para mantener el directorio en el repositorio
- ✅ Actualizado `web/static/images/README.md` con documentación

## Cómo Usar

### Para Administradores de Servidor

1. **Accede al panel de bienvenida**:
   - Ve al Dashboard
   - Selecciona tu servidor
   - Haz clic en "Configurar Bienvenida"

2. **Subir imagen de fondo**:
   - En la sección "Imagen de Bienvenida"
   - Marca "Incluir imagen personalizada"
   - Haz clic en "Imagen de Fondo"
   - Selecciona tu imagen (PNG, JPG, GIF, WebP)
   - La imagen se subirá automáticamente al guardar

3. **Vista previa**:
   - Haz clic en "Vista Previa" para ver cómo quedará
   - La imagen mostrará al usuario en el centro sobre tu fondo personalizado

4. **Eliminar imagen**:
   - Si ya tienes una imagen subida, verás un botón "Eliminar"
   - Haz clic para remover la imagen y volver al color de fondo

### Formatos Soportados

- **PNG** (recomendado para transparencias)
- **JPG/JPEG** (mejor compresión)
- **GIF** (soporta animaciones simples)
- **WebP** (formato moderno con buena compresión)

### Consideraciones Técnicas

- **Tamaño recomendado**: 800x300px (se redimensionará automáticamente)
- **Almacenamiento**: Las imágenes se guardan en el servidor web
- **Rendimiento**: Las imágenes se cachean para acceso rápido
- **Límite de tamaño**: Sin límite definido (se recomienda < 5MB)

## Migración de Base de Datos

Si ya tienes una base de datos existente, ejecuta el siguiente SQL en Supabase:

```sql
ALTER TABLE welcome_config ADD COLUMN background_image_url TEXT;
```

O ejecuta el script completo en `migrations/add_background_image_url.sql`

## Ejemplo Visual

**Antes**: Fondo de color sólido (#7289da)
```
┌─────────────────────────────┐
│       Fondo azul sólido     │
│          ┌─────┐            │
│          │ 👤  │            │
│          └─────┘            │
│      ¡Bienvenido John!      │
└─────────────────────────────┘
```

**Ahora**: Imagen personalizada de fondo
```
┌─────────────────────────────┐
│  🌄 Imagen personalizada 🌄 │
│          ┌─────┐            │
│          │ 👤  │            │
│          └─────┘            │
│      ¡Bienvenido John!      │
└─────────────────────────────┘
```

## Testing

Para probar la nueva funcionalidad:

1. Sube una imagen de prueba
2. Usa el comando `/testwelcome` en Discord
3. Verifica que la imagen de fondo aparezca correctamente
4. Prueba eliminando la imagen y verifica el fallback al color

## Notas de Desarrollo

- El generador de imágenes usa Pillow (PIL) para procesamiento
- Las imágenes se descargan con `requests` con timeout de 10 segundos
- Se usa interpolación LANCZOS para mejor calidad al redimensionar
- Los archivos se nombran con UUID para evitar colisiones
- El sistema tiene fallback automático si la descarga de imagen falla

## Próximas Mejoras

- [ ] Límite de tamaño de archivo configurable
- [ ] Compresión automática de imágenes grandes
- [ ] Galería de fondos predeterminados
- [ ] Editor de imágenes integrado (recortar, filtros, etc.)
- [ ] Soporte para GIFs animados en Discord

## Soporte

Para problemas o preguntas sobre esta funcionalidad:
- Revisa los logs en `logger` para errores
- Verifica que el directorio `web/static/images/backgrounds/` tenga permisos de escritura
- Asegúrate de que Pillow esté instalado: `pip install Pillow`
