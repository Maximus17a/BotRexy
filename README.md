# 🤖 BotRexy - Bot de Discord Completo

Bot de Discord con automoderación, sistema de niveles, bienvenidas personalizables y panel web de administración.

## ✨ Características

- **🛡️ Automoderación**: Anti-spam, filtro de palabras, límite de menciones y emojis
- **🏆 Sistema de Niveles**: XP automático por mensajes y tabla de clasificación
- **👋 Bienvenidas Personalizadas**: Mensajes e imágenes de bienvenida configurables
- **🔐 Sistema de Verificación**: Verificación automática con rol para nuevos miembros
- **🎮 Roles de Juegos**: Panel interactivo con botones para seleccionar roles de juegos
- **🌐 Panel Web**: Interfaz web para configurar el bot sin comandos
- **📊 Base de Datos**: Supabase para almacenamiento persistente
- **📝 Logs de Moderación**: Registro completo de acciones de moderación
- **⚡ Comandos Slash**: Comandos modernos de Discord

## 🚀 Despliegue en Render

### Requisitos Previos

1. **Cuenta de Discord Developer**
   - Ve a [Discord Developer Portal](https://discord.com/developers/applications)
   - Crea una nueva aplicación
   - En la sección "Bot", crea un bot y copia el token
   - En "OAuth2", agrega la URL de redirección: `https://tu-app.onrender.com/callback`
   - Copia el Client ID y Client Secret

2. **Cuenta de Supabase**
   - Ve a [Supabase](https://supabase.com)
   - Crea un nuevo proyecto
   - Ve a Settings > API y copia la URL y la clave anon/public
   - Ve a SQL Editor y ejecuta el contenido de `database_schema.sql`

3. **Cuenta de Render**
   - Ve a [Render](https://render.com)
   - Crea una cuenta gratuita

### Pasos de Despliegue

#### 1. Preparar el Repositorio

```bash
# Clonar o hacer push a tu repositorio de GitHub
git add .
git commit -m "Initial commit"
git push origin main
```

#### 2. Crear Web Service en Render

1. En Render Dashboard, haz clic en "New +" y selecciona "Web Service"
2. Conecta tu repositorio de GitHub
3. Configura el servicio:
   - **Name**: `botrexy` (o el nombre que prefieras)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`
   - **Plan**: Free

#### 3. Configurar Variables de Entorno

En la sección "Environment" de tu servicio en Render, agrega:

```
DISCORD_TOKEN=tu_token_del_bot
DISCORD_CLIENT_ID=tu_client_id
DISCORD_CLIENT_SECRET=tu_client_secret
SECRET_KEY=genera_una_clave_secreta_aleatoria
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_clave_anon_de_supabase
REDIRECT_URI=https://tu-app.onrender.com/callback
PORT=5000
```

**Nota**: Reemplaza `tu-app` con el nombre real de tu aplicación en Render.

#### 4. Desplegar

1. Haz clic en "Create Web Service"
2. Render automáticamente construirá y desplegará tu aplicación
3. Espera a que el despliegue termine (puede tomar unos minutos)

#### 5. Invitar el Bot a tu Servidor

1. Ve a Discord Developer Portal
2. En tu aplicación, ve a OAuth2 > URL Generator
3. Selecciona los scopes: `bot` y `applications.commands`
4. Selecciona los permisos necesarios (o marca "Administrator" para todos)
5. Copia la URL generada y ábrela en tu navegador
6. Selecciona tu servidor y autoriza el bot

### 🔧 Configuración Post-Despliegue

1. **Actualizar Redirect URI en Discord**
   - Ve a Discord Developer Portal
   - En OAuth2, agrega: `https://tu-app.onrender.com/callback`

2. **Verificar Base de Datos**
   - Asegúrate de haber ejecutado `database_schema.sql` en Supabase

3. **Probar el Bot**
   - Usa `/nivel` en tu servidor para verificar que funciona
   - Accede a `https://tu-app.onrender.com` para ver el panel web

## 📋 Comandos Disponibles

### Comandos de Usuario
- `/nivel [usuario]` - Ver nivel y experiencia
- `/ranking` - Ver tabla de clasificación del servidor

### Comandos de Moderación
- `/kick <usuario> [razón]` - Expulsar usuario
- `/ban <usuario> [razón]` - Banear usuario
- `/unban <user_id>` - Desbanear usuario
- `/timeout <usuario> <minutos> [razón]` - Silenciar usuario
- `/untimeout <usuario>` - Quitar silencio
- `/warn <usuario> <razón>` - Advertir usuario
- `/clear <cantidad>` - Eliminar mensajes
- `/modlogs [límite]` - Ver logs de moderación

### Comandos de Configuración (Admin)
- `/setwelcome <canal>` - Configurar canal de bienvenida
- `/welcomemsg <mensaje>` - Configurar mensaje de bienvenida
- `/testwelcome` - Probar mensaje de bienvenida
- `/automod` - Ver configuración de automoderación
- `/togglespam` - Activar/desactivar anti-spam
- `/toggleinvites` - Activar/desactivar anti-invitaciones
- `/togglelinks` - Activar/desactivar anti-enlaces
- `/resetxp <usuario>` - Resetear XP de un usuario

### Comandos de Verificación (Admin)
- `/setupverification <canal> <rol>` - Configurar sistema de verificación
- `/verify <usuario>` - Verificar manualmente a un usuario
- `/toggleverification` - Activar/desactivar verificación

### Comandos de Roles de Juegos (Admin)
- `/setupgameroles <canal>` - Crear panel de roles de juegos
- `/addgamerole <juego> <rol>` - Agregar rol de juego
- `/removegamerole <juego>` - Remover rol de juego
- `/listgameroles` - Ver roles configurados

## 🌐 Panel Web

Accede al panel web en `https://tu-app.onrender.com`

### Funcionalidades del Panel:
- **Dashboard**: Ver todos tus servidores
- **Configuración General**: Activar/desactivar sistemas
- **Configuración de Bienvenida**: Personalizar mensajes e imágenes
- **Sistema de Verificación**: Configurar canal y rol de verificación
- **Roles de Juegos**: Crear panel interactivo con botones para roles
- **Automoderación**: Configurar reglas de moderación
- **Vista Previa**: Ver cómo se verán las imágenes de bienvenida

## 🗄️ Estructura del Proyecto

```
BotRexy/
├── bot/                    # Código del bot de Discord
│   ├── cogs/              # Módulos de comandos
│   │   ├── automod.py     # Automoderación
│   │   ├── levels.py      # Sistema de niveles
│   │   ├── moderation.py  # Comandos de moderación
│   │   └── welcome.py     # Sistema de bienvenida
│   ├── utils/             # Utilidades
│   │   ├── database.py    # Conexión a Supabase
│   │   └── image_gen.py   # Generación de imágenes
│   └── main.py            # Punto de entrada del bot
├── web/                   # Panel web Flask
│   ├── routes/            # Rutas de la aplicación
│   │   ├── auth.py        # Autenticación OAuth2
│   │   ├── dashboard.py   # Dashboard principal
│   │   ├── legal.py       # Páginas legales
│   │   └── welcome_config.py  # Configuración de bienvenida
│   ├── static/            # Archivos estáticos
│   │   ├── css/
│   │   └── js/
│   ├── templates/         # Plantillas HTML
│   └── app.py             # Aplicación Flask
├── config.py              # Configuración general
├── run.py                 # Script principal
├── requirements.txt       # Dependencias
├── Procfile              # Configuración de Render
├── render.yaml           # Configuración de Render
└── database_schema.sql   # Schema de base de datos

```

## 🔐 Variables de Entorno

Copia `.env.example` a `.env` y completa los valores:

```bash
cp .env.example .env
```

Variables requeridas:
- `DISCORD_TOKEN`: Token del bot de Discord
- `DISCORD_CLIENT_ID`: Client ID de la aplicación
- `DISCORD_CLIENT_SECRET`: Client Secret de la aplicación
- `SUPABASE_URL`: URL de tu proyecto Supabase
- `SUPABASE_KEY`: Clave anon/public de Supabase
- `SECRET_KEY`: Clave secreta para Flask (genera una aleatoria)
- `REDIRECT_URI`: URL de callback OAuth2

## 🛠️ Desarrollo Local

### Requisitos
- Python 3.11+
- Cuenta de Discord Developer
- Proyecto de Supabase

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/BotRexy.git
cd BotRexy

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tus valores

# Ejecutar
python run.py
```

El bot y el servidor web se ejecutarán simultáneamente:
- Bot: Conectado a Discord
- Web: http://localhost:5000

## 📊 Base de Datos

### Tablas

- **guilds**: Configuración de servidores
- **users**: Datos de usuarios y niveles
- **welcome_config**: Configuración de bienvenida
- **automod_config**: Configuración de automoderación
- **verification_config**: Configuración de verificación
- **game_roles_config**: Configuración de roles de juegos
- **moderation_logs**: Logs de moderación

### Inicializar Base de Datos

1. Ve a tu proyecto en Supabase
2. Abre el SQL Editor
3. Copia y ejecuta el contenido de `database_schema.sql`

## 🐛 Solución de Problemas

### El bot no se conecta
- Verifica que `DISCORD_TOKEN` sea correcto
- Asegúrate de que el bot esté habilitado en Discord Developer Portal
- Revisa los logs en Render

### Error de base de datos
- Verifica que `SUPABASE_URL` y `SUPABASE_KEY` sean correctos
- Asegúrate de haber ejecutado `database_schema.sql`
- Verifica que las tablas existan en Supabase

### OAuth2 no funciona
- Verifica que `REDIRECT_URI` coincida con la configurada en Discord
- Asegúrate de que `DISCORD_CLIENT_ID` y `DISCORD_CLIENT_SECRET` sean correctos
- Verifica que la URL de redirección esté agregada en Discord Developer Portal

### El bot no responde a comandos
- Espera unos minutos después del despliegue para que los comandos se sincronicen
- Verifica que el bot tenga los permisos necesarios en tu servidor
- Usa `/` para ver los comandos disponibles

## 📝 Notas Importantes

- **Plan Gratuito de Render**: El servicio puede dormir después de 15 minutos de inactividad. Se despertará automáticamente cuando reciba una solicitud.
- **Límites de Supabase**: El plan gratuito tiene límites de almacenamiento y requests. Monitorea tu uso.
- **Comandos Slash**: Pueden tardar hasta 1 hora en sincronizarse globalmente después del primer despliegue.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Soporte

Si tienes problemas o preguntas:
- Abre un issue en GitHub
- Consulta la documentación de [Discord.py](https://discordpy.readthedocs.io/)
- Revisa la documentación de [Supabase](https://supabase.com/docs)
- Consulta la documentación de [Render](https://render.com/docs)

## 🌟 Créditos

Desarrollado con ❤️ usando:
- [Discord.py](https://github.com/Rapptz/discord.py)
- [Flask](https://flask.palletsprojects.com/)
- [Supabase](https://supabase.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Render](https://render.com/)

---

**¡Disfruta usando BotRexy!** 🎉
