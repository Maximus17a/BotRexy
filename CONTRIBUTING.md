# Guía de Contribución

¡Gracias por tu interés en contribuir a BotRexy! Este documento proporciona pautas para contribuir al proyecto.

## Código de Conducta

Al participar en este proyecto, te comprometes a mantener un ambiente respetuoso y colaborativo.

## ¿Cómo Contribuir?

### Reportar Bugs

Si encuentras un bug, por favor abre un issue en GitHub con:

- **Título descriptivo**: Resume el problema en pocas palabras
- **Descripción detallada**: Explica qué esperabas que sucediera y qué sucedió realmente
- **Pasos para reproducir**: Lista los pasos exactos para reproducir el problema
- **Entorno**: Versión de Python, sistema operativo, etc.
- **Logs**: Si es posible, incluye logs relevantes

### Sugerir Mejoras

Para sugerir nuevas características o mejoras:

1. Abre un issue con la etiqueta "enhancement"
2. Describe claramente la funcionalidad propuesta
3. Explica por qué sería útil para el proyecto
4. Si es posible, proporciona ejemplos de uso

### Pull Requests

#### Proceso

1. **Fork** el repositorio
2. **Crea una rama** para tu feature:
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```
3. **Realiza tus cambios** siguiendo las guías de estilo
4. **Commit** tus cambios con mensajes descriptivos:
   ```bash
   git commit -m "Add: descripción breve del cambio"
   ```
5. **Push** a tu fork:
   ```bash
   git push origin feature/nombre-descriptivo
   ```
6. **Abre un Pull Request** en GitHub

#### Guías para Pull Requests

- Un PR debe resolver un solo problema o agregar una sola característica
- Actualiza la documentación si es necesario
- Asegúrate de que el código funcione correctamente
- Sigue las convenciones de código del proyecto
- Escribe mensajes de commit claros y descriptivos

### Convenciones de Código

#### Python

- Sigue [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Usa 4 espacios para indentación (no tabs)
- Longitud máxima de línea: 100 caracteres
- Usa docstrings para funciones y clases
- Nombra variables y funciones en `snake_case`
- Nombra clases en `PascalCase`

Ejemplo:
```python
async def get_user_level(self, guild_id: int, user_id: int):
    """
    Obtener nivel y XP de un usuario.
    
    Args:
        guild_id: ID del servidor de Discord
        user_id: ID del usuario
    
    Returns:
        dict: Datos del usuario con nivel y XP
    """
    # Implementación
```

#### JavaScript

- Usa ES6+ cuando sea posible
- Usa 4 espacios para indentación
- Usa `const` y `let`, evita `var`
- Usa arrow functions cuando sea apropiado
- Usa camelCase para variables y funciones

#### HTML/CSS

- Indentación de 4 espacios
- Usa clases de Bootstrap cuando sea posible
- Mantén el CSS organizado y comentado
- Usa nombres de clase descriptivos

### Estructura de Commits

Usa prefijos en los mensajes de commit:

- `Add:` - Nueva característica
- `Fix:` - Corrección de bug
- `Update:` - Actualización de código existente
- `Remove:` - Eliminación de código
- `Refactor:` - Refactorización sin cambio de funcionalidad
- `Docs:` - Cambios en documentación
- `Style:` - Cambios de formato (espacios, punto y coma, etc.)
- `Test:` - Agregar o modificar tests

Ejemplos:
```
Add: sistema de economía con monedas virtuales
Fix: error en cálculo de XP para niveles altos
Update: mejorar rendimiento de queries a base de datos
Docs: agregar ejemplos de uso en README
```

## Áreas de Contribución

### Código

- Nuevas características
- Corrección de bugs
- Optimización de rendimiento
- Refactorización

### Documentación

- Mejorar README
- Agregar ejemplos
- Traducir documentación
- Corregir errores tipográficos

### Diseño

- Mejorar UI del panel web
- Diseñar nuevas páginas
- Optimizar para móviles

### Testing

- Escribir tests unitarios
- Probar en diferentes entornos
- Reportar bugs

## Desarrollo Local

### Configuración del Entorno

```bash
# Clonar tu fork
git clone https://github.com/TU_USUARIO/BotRexy.git
cd BotRexy

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales

# Ejecutar
python run.py
```

### Testing

Antes de enviar un PR, asegúrate de:

1. Probar todos los comandos del bot
2. Verificar que el panel web funcione correctamente
3. Comprobar que no haya errores en los logs
4. Probar en diferentes navegadores (para cambios web)

## Preguntas

Si tienes preguntas sobre cómo contribuir, puedes:

- Abrir un issue con la etiqueta "question"
- Contactar a los mantenedores del proyecto

## Licencia

Al contribuir a BotRexy, aceptas que tus contribuciones se licenciarán bajo la Licencia MIT.

---

¡Gracias por contribuir a BotRexy! 🎉
