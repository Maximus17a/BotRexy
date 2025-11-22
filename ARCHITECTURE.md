# Arquitectura del Bot de Discord - BotRexy

## Descripción General

BotRexy es un bot de Discord completo con panel web de administración, que incluye automoderación, sistema de niveles, bienvenidas personalizables y más.

## Componentes Principales

### 1. Bot de Discord (Python)
- **Framework**: discord.py
- **Funcionalidades**:
  - Automoderación (anti-spam, palabras prohibidas, enlaces)
  - Sistema de niveles y experiencia
  - Sistema de bienvenida con imágenes personalizables
  - Comandos de administración
  - Logs de moderación

### 2. Panel Web (Flask)
- **Framework**: Flask + Bootstrap 5
- **Funcionalidades**:
  - Dashboard de servidores
  - Configuración de bienvenida (texto, canal, imagen)
  - Editor de imagen de bienvenida
  - Configuración de automoderación
  - Gestión de niveles
  - Páginas legales (Privacidad, Términos)

### 3. Base de Datos (Supabase)
- **Tablas**:
  - `guilds`: Configuración de servidores
  - `users`: Datos de usuarios y niveles
  - `moderation_logs`: Registro de acciones de moderación
  - `welcome_config`: Configuración de bienvenida
  - `automod_config`: Configuración de automoderación

### 4. Autenticación
- OAuth2 de Discord para el panel web
- Sesiones seguras con Flask-Session

## Estructura de Archivos

```
BotRexy/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada del bot
│   ├── cogs/
│   │   ├── __init__.py
│   │   ├── moderation.py    # Comandos de moderación
│   │   ├── levels.py        # Sistema de niveles
│   │   ├── welcome.py       # Sistema de bienvenida
│   │   └── automod.py       # Automoderación
│   └── utils/
│       ├── __init__.py
│       ├── database.py      # Conexión a Supabase
│       └── image_gen.py     # Generación de imágenes
├── web/
│   ├── __init__.py
│   ├── app.py               # Aplicación Flask
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Autenticación OAuth2
│   │   ├── dashboard.py     # Dashboard principal
│   │   ├── welcome.py       # Configuración de bienvenida
│   │   └── legal.py         # Páginas legales
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── welcome_config.html
│   │   ├── privacy.html
│   │   └── terms.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── config.py                # Configuración general
├── requirements.txt         # Dependencias
├── Procfile                 # Para Render
├── render.yaml              # Configuración de Render
└── README.md
```

## Flujo de Datos

1. **Usuario se une al servidor** → Bot detecta evento → Consulta configuración en Supabase → Genera imagen de bienvenida → Envía mensaje
2. **Usuario envía mensaje** → Bot verifica automoderación → Otorga XP → Actualiza nivel en base de datos
3. **Admin accede al panel** → OAuth2 Discord → Verifica permisos → Muestra dashboard → Permite configuración → Guarda en Supabase

## Despliegue en Render

- **Tipo**: Web Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python run.py` (ejecuta bot + web en paralelo)
- **Variables de entorno**:
  - `DISCORD_TOKEN`
  - `DISCORD_CLIENT_ID`
  - `DISCORD_CLIENT_SECRET`
  - `SUPABASE_URL`
  - `SUPABASE_KEY`
  - `SECRET_KEY`
  - `REDIRECT_URI`

## Seguridad

- Tokens y secretos en variables de entorno
- Validación de permisos en panel web
- Rate limiting en endpoints
- Sanitización de inputs
- HTTPS obligatorio
