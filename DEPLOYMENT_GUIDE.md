# 📦 Guía de Despliegue Completa - BotRexy

Esta guía te llevará paso a paso a través del proceso completo de despliegue de BotRexy en Render.

## 📋 Tabla de Contenidos

1. [Configuración de Discord](#1-configuración-de-discord)
2. [Configuración de Supabase](#2-configuración-de-supabase)
3. [Preparación del Código](#3-preparación-del-código)
4. [Despliegue en Render](#4-despliegue-en-render)
5. [Configuración Final](#5-configuración-final)
6. [Verificación](#6-verificación)

---

## 1. Configuración de Discord

### 1.1 Crear Aplicación de Discord

1. Ve a [Discord Developer Portal](https://discord.com/developers/applications)
2. Haz clic en **"New Application"**
3. Dale un nombre a tu aplicación (ej: "BotRexy")
4. Acepta los términos y haz clic en **"Create"**

### 1.2 Configurar el Bot

1. En el menú lateral, ve a **"Bot"**
2. Haz clic en **"Add Bot"** y confirma
3. **Copia el Token** (guárdalo en un lugar seguro, lo necesitarás después)
4. Activa las siguientes **Privileged Gateway Intents**:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. Haz clic en **"Save Changes"**

### 1.3 Configurar OAuth2

1. En el menú lateral, ve a **"OAuth2"** > **"General"**
2. Copia el **Client ID** (guárdalo)
3. Copia el **Client Secret** (haz clic en "Reset Secret" si es necesario)
4. En **"Redirects"**, agrega temporalmente:
   ```
   http://localhost:5000/callback
   ```
   (Actualizaremos esto después del despliegue)

### 1.4 Generar URL de Invitación

1. Ve a **"OAuth2"** > **"URL Generator"**
2. Selecciona los siguientes **scopes**:
   - ✅ bot
   - ✅ applications.commands
3. Selecciona los siguientes **permisos**:
   - ✅ Administrator (o selecciona permisos específicos según necesites)
4. **Copia la URL generada** (la usarás después para invitar el bot)
https://discord.com/oauth2/authorize?client_id=1439403067488469143&permissions=8&integration_type=0&scope=bot+applications.commands

---

## 2. Configuración de Supabase

### 2.1 Crear Proyecto

1. Ve a [Supabase](https://supabase.com)
2. Haz clic en **"Start your project"** o **"New Project"**
3. Selecciona tu organización o crea una nueva
4. Configura tu proyecto:
   - **Name**: BotRexy (o el nombre que prefieras)
   - **Database Password**: Genera una contraseña segura (guárdala)
   - **Region**: Selecciona la región más cercana
5. Haz clic en **"Create new project"**
6. Espera a que el proyecto se inicialice (puede tomar 1-2 minutos)

### 2.2 Obtener Credenciales

1. Una vez creado el proyecto, ve a **"Settings"** (⚙️) > **"API"**
2. Copia los siguientes valores:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: Una clave larga que empieza con `eyJ...`

### 2.3 Crear Tablas

1. Ve a **"SQL Editor"** en el menú lateral
2. Haz clic en **"New query"**
3. Abre el archivo `database_schema.sql` de tu proyecto
4. Copia todo el contenido y pégalo en el editor SQL
5. Haz clic en **"Run"** (▶️)
6. Verifica que aparezca el mensaje de éxito

### 2.4 Verificar Tablas

1. Ve a **"Table Editor"** en el menú lateral
2. Deberías ver las siguientes tablas:
   - guilds
   - users
   - welcome_config
   - automod_config
   - moderation_logs

---

## 3. Preparación del Código

### 3.1 Subir a GitHub

Si aún no has subido el código a GitHub:

```bash
# Inicializar repositorio (si no está inicializado)
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit - BotRexy"

# Crear repositorio en GitHub y conectarlo
git remote add origin https://github.com/TU_USUARIO/BotRexy.git

# Subir código
git branch -M main
git push -u origin main
```

### 3.2 Verificar Archivos Esenciales

Asegúrate de que tu repositorio contenga:
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `run.py`
- ✅ `config.py`
- ✅ Carpetas `bot/` y `web/`

---

## 4. Despliegue en Render

### 4.1 Crear Cuenta en Render

1. Ve a [Render](https://render.com)
2. Haz clic en **"Get Started"**
3. Regístrate con GitHub (recomendado) o email

### 4.2 Crear Web Service

1. En el Dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub:
   - Si es la primera vez, autoriza a Render a acceder a GitHub
   - Busca y selecciona tu repositorio **BotRexy**
4. Haz clic en **"Connect"**

### 4.3 Configurar el Servicio

Completa los siguientes campos:

- **Name**: `botrexy` (o el nombre que prefieras, sin espacios)
- **Region**: Selecciona la región más cercana
- **Branch**: `main`
- **Root Directory**: (déjalo vacío)
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  python run.py
  ```
- **Plan**: Selecciona **"Free"**

### 4.4 Configurar Variables de Entorno

Desplázate hasta la sección **"Environment Variables"** y agrega las siguientes:

| Key | Value |
|-----|-------|
| `DISCORD_TOKEN` | El token del bot que copiaste de Discord |
| `DISCORD_CLIENT_ID` | El Client ID de Discord |
| `DISCORD_CLIENT_SECRET` | El Client Secret de Discord |
| `SUPABASE_URL` | La URL de tu proyecto Supabase |
| `SUPABASE_KEY` | La clave anon/public de Supabase |
| `SECRET_KEY` | Genera una clave aleatoria (ej: `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `REDIRECT_URI` | `https://botrexy.onrender.com/callback` (reemplaza `botrexy` con tu nombre de servicio) |
| `PORT` | `5000` |

**Importante**: Asegúrate de que `REDIRECT_URI` use el nombre exacto de tu servicio en Render.

### 4.5 Crear el Servicio

1. Revisa toda la configuración
2. Haz clic en **"Create Web Service"**
3. Render comenzará a construir y desplegar tu aplicación
4. Este proceso puede tomar 5-10 minutos

### 4.6 Esperar el Despliegue

Verás los logs en tiempo real. Espera a ver mensajes como:
```
Bot conectado como BotRexy#1234
Starting web server...
```

Una vez que veas **"Your service is live 🎉"**, tu aplicación está desplegada.

---

## 5. Configuración Final

### 5.1 Actualizar Redirect URI en Discord

1. Vuelve a [Discord Developer Portal](https://discord.com/developers/applications)
2. Selecciona tu aplicación
3. Ve a **"OAuth2"** > **"General"**
4. En **"Redirects"**, agrega:
   ```
   https://TU-SERVICIO.onrender.com/callback
   ```
   (Reemplaza `TU-SERVICIO` con el nombre de tu servicio en Render)
5. Haz clic en **"Save Changes"**

### 5.2 Invitar el Bot a tu Servidor

1. Usa la URL de invitación que generaste en el paso 1.4
2. O genera una nueva en **"OAuth2"** > **"URL Generator"**
3. Abre la URL en tu navegador
4. Selecciona el servidor donde quieres agregar el bot
5. Autoriza los permisos
6. Completa el captcha si aparece
7. ¡El bot ahora está en tu servidor!

---

## 6. Verificación

### 6.1 Verificar el Bot

En tu servidor de Discord:

1. El bot debería aparecer en la lista de miembros
2. Prueba el comando: `/nivel`
3. El bot debería responder con tu nivel actual

### 6.2 Verificar el Panel Web

1. Abre tu navegador y ve a: `https://TU-SERVICIO.onrender.com`
2. Deberías ver la página de inicio de BotRexy
3. Haz clic en **"Iniciar Sesión"**
4. Autoriza la aplicación con Discord
5. Deberías ser redirigido al Dashboard
6. Verifica que puedas ver tus servidores

### 6.3 Configurar Bienvenida (Opcional)

1. En el Dashboard, selecciona tu servidor
2. Haz clic en **"Configurar Bienvenida"**
3. Activa el sistema de bienvenida
4. Selecciona un canal
5. Personaliza el mensaje
6. Guarda los cambios
7. Prueba con `/testwelcome`

---

## 🎉 ¡Listo!

Tu bot está completamente desplegado y funcionando. Ahora puedes:

- Usar todos los comandos del bot en Discord
- Configurar el bot desde el panel web
- Personalizar la bienvenida
- Ver estadísticas y logs

---

## 🐛 Solución de Problemas Comunes

### El bot no se conecta

**Síntoma**: El bot no aparece en línea en Discord

**Soluciones**:
1. Verifica que `DISCORD_TOKEN` sea correcto en Render
2. Asegúrate de haber activado los Intents en Discord Developer Portal
3. Revisa los logs en Render para ver errores específicos

### Error de base de datos

**Síntoma**: Errores relacionados con Supabase en los logs

**Soluciones**:
1. Verifica que `SUPABASE_URL` y `SUPABASE_KEY` sean correctos
2. Asegúrate de haber ejecutado `database_schema.sql` en Supabase
3. Verifica que las tablas existan en el Table Editor de Supabase

### OAuth2 no funciona

**Síntoma**: Error al iniciar sesión en el panel web

**Soluciones**:
1. Verifica que `REDIRECT_URI` en Render coincida exactamente con la URL en Discord
2. Asegúrate de que `DISCORD_CLIENT_ID` y `DISCORD_CLIENT_SECRET` sean correctos
3. Verifica que la URL de redirección esté agregada en Discord Developer Portal

### El servicio se duerme

**Síntoma**: El bot deja de responder después de un tiempo

**Explicación**: El plan gratuito de Render duerme el servicio después de 15 minutos de inactividad.

**Soluciones**:
1. Actualiza a un plan de pago en Render
2. Usa un servicio de "ping" externo para mantener el servicio activo
3. Acepta que el servicio se dormirá y se despertará cuando reciba una solicitud

---

## 📞 Soporte Adicional

Si sigues teniendo problemas:

1. Revisa los logs en Render (pestaña "Logs")
2. Verifica la consola del navegador para errores del panel web (F12)
3. Consulta la documentación oficial:
   - [Discord.py](https://discordpy.readthedocs.io/)
   - [Supabase](https://supabase.com/docs)
   - [Render](https://render.com/docs)

---

**¡Feliz moderación!** 🚀
