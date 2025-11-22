# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2025-11-21

### Añadido

#### Bot de Discord
- Sistema completo de automoderación con anti-spam, anti-invitaciones y filtro de palabras
- Sistema de niveles y experiencia con XP automático por mensajes
- Sistema de bienvenida con imágenes personalizables generadas dinámicamente
- Comandos de moderación: kick, ban, unban, timeout, untimeout, warn, clear
- Comandos de usuario: nivel, ranking
- Comandos de configuración: setwelcome, welcomemsg, testwelcome, automod, toggles
- Logs completos de moderación almacenados en base de datos
- Manejo de errores robusto con logging

#### Panel Web
- Autenticación OAuth2 con Discord
- Dashboard principal con lista de servidores del usuario
- Página de configuración general de servidor
- Editor visual de configuración de bienvenida con vista previa
- Configuración de automoderación desde la web
- Páginas legales: Política de Privacidad y Términos de Servicio
- Diseño responsive con Bootstrap 5
- Páginas de error personalizadas (404, 500)

#### Base de Datos
- Integración completa con Supabase
- 5 tablas: guilds, users, welcome_config, automod_config, moderation_logs
- Triggers automáticos para actualizar timestamps
- Índices optimizados para consultas frecuentes
- Schema SQL completo y documentado

#### Infraestructura
- Configuración para despliegue en Render
- Procfile y render.yaml configurados
- Variables de entorno con .env.example
- Ejecución simultánea de bot y servidor web
- Manejo de hilos para múltiples servicios

#### Documentación
- README.md completo con instrucciones de instalación y uso
- DEPLOYMENT_GUIDE.md con guía paso a paso de despliegue
- ARCHITECTURE.md con documentación técnica de la arquitectura
- PROJECT_SUMMARY.md con resumen ejecutivo del proyecto
- Comentarios y docstrings en todo el código

#### Utilidades
- Generador de imágenes de bienvenida con PIL
- Clase Database completa para interactuar con Supabase
- Funciones JavaScript reutilizables para el panel web
- Estilos CSS personalizados con tema de Discord

### Seguridad
- Tokens y secretos manejados con variables de entorno
- Validación de permisos en todos los comandos
- Verificación de roles de administrador en panel web
- OAuth2 seguro con Discord
- Sanitización de inputs en automoderación

## [Unreleased]

### Planeado para Futuras Versiones
- Sistema de economía con monedas virtuales
- Comandos de música
- Sistema de tickets de soporte
- Roles automáticos por nivel
- Estadísticas avanzadas en el panel
- Sistema de reportes de usuarios
- Integración con APIs externas

---

[1.0.0]: https://github.com/Maximus17a/BotRexy/releases/tag/v1.0.0
