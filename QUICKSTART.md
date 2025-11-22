# 🚀 Guía de Inicio Rápido - BotRexy

Esta guía te ayudará a tener BotRexy funcionando en menos de 30 minutos.

## ⚡ Pasos Rápidos

### 1. Crear Bot en Discord (5 minutos)

1. Ve a https://discord.com/developers/applications
2. Clic en **"New Application"** → Dale un nombre → **"Create"**
3. Ve a **"Bot"** → **"Add Bot"** → Copia el **Token**
4. Activa los **3 Intents** (Presence, Server Members, Message Content)
5. Ve a **"OAuth2"** → Copia **Client ID** y **Client Secret**

### 2. Crear Base de Datos en Supabase (5 minutos)

1. Ve a https://supabase.com → **"New Project"**
2. Configura nombre y contraseña → **"Create"**
3. Ve a **Settings** → **API** → Copia **URL** y **anon key**
4. Ve a **SQL Editor** → Pega el contenido de `database_schema.sql` → **Run**

### 3. Desplegar en Render (10 minutos)

1. Ve a https://render.com → **"New +"** → **"Web Service"**
2. Conecta tu repositorio GitHub **BotRexy**
3. Configura:
   - **Name**: `botrexy`
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `python run.py`
   - **Plan**: Free
4. Agrega las **Variables de Entorno**:

```
DISCORD_TOKEN=tu_token_aqui
DISCORD_CLIENT_ID=tu_client_id
DISCORD_CLIENT_SECRET=tu_client_secret
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=tu_supabase_key
SECRET_KEY=genera_una_clave_random
REDIRECT_URI=https://botrexy.onrender.com/callback
PORT=5000
```

5. Clic en **"Create Web Service"** → Espera 5-10 minutos

### 4. Configuración Final (5 minutos)

1. **Actualizar Discord**:
   - Ve a Discord Developer Portal → Tu App → OAuth2
   - Agrega redirect: `https://botrexy.onrender.com/callback`

2. **Invitar Bot**:
   - OAuth2 → URL Generator
   - Scopes: `bot`, `applications.commands`
   - Permisos: `Administrator`
   - Copia URL → Abre en navegador → Selecciona servidor

3. **Probar**:
   - En Discord: `/nivel`
   - En web: `https://botrexy.onrender.com`

## ✅ Verificación

Si todo funciona:
- ✅ Bot aparece en línea en Discord
- ✅ Comando `/nivel` responde
- ✅ Puedes acceder al panel web
- ✅ Puedes iniciar sesión con Discord

## 🆘 Problemas Comunes

### Bot no se conecta
→ Verifica `DISCORD_TOKEN` y que los Intents estén activados

### Error de base de datos
→ Verifica que ejecutaste `database_schema.sql` en Supabase

### OAuth2 no funciona
→ Verifica que `REDIRECT_URI` coincida en Render y Discord

### Servicio se duerme
→ Es normal en plan gratuito, se despierta al recibir requests

## 📚 Siguiente Paso

Lee la [Guía de Despliegue Completa](DEPLOYMENT_GUIDE.md) para más detalles.

## 🎯 Comandos Básicos para Probar

```
/nivel              - Ver tu nivel
/ranking            - Ver ranking del servidor
/setwelcome #canal  - Configurar bienvenida (Admin)
/automod            - Ver configuración (Admin)
```

## 🌐 URLs Importantes

- **Panel Web**: https://tu-servicio.onrender.com
- **Discord Developer**: https://discord.com/developers/applications
- **Supabase Dashboard**: https://app.supabase.com
- **Render Dashboard**: https://dashboard.render.com

---

**¿Listo? ¡Empieza ahora!** 🎉

Si tienes problemas, consulta [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) o abre un issue en GitHub.
