# TennisManager SaaS v2.0

Plataforma SaaS completa para la gestión de canchas de tenis con API REST desarrollada con Flask 3.0, siguiendo arquitectura MVC y principios de clean code (DRY, KISS).

## 🎾 Sobre TennisManager

**TennisManager** es una solución SaaS integral diseñada para revolucionar la gestión de clubes de tenis. Combina una potente API REST con una interfaz web moderna para ofrecer:

- **Gestión de Canchas**: Reservas inteligentes y control de disponibilidad
- **Administración de Usuarios**: Miembros, instructores y visitantes
- **Sistema de Pagos**: Procesamiento seguro y facturación automática
- **Analytics Avanzados**: Reportes de ocupación e ingresos
- **App Móvil**: Reservas desde cualquier lugar
- **API Completa**: Integración con sistemas existentes

## 🚀 Características Técnicas

- **Flask 3.0**: Última versión estable con mejoras de rendimiento
- **Landing Page Moderna**: Interfaz web atractiva con Bootstrap 5
- **Arquitectura MVC**: Separación clara entre Modelos, Vistas (Controllers) y Servicios
- **Clean Code**: Implementación de principios DRY y KISS
- **Dockerizado**: Aplicación completamente containerizada con health checks
- **Base de datos MySQL 8.0**: Persistencia de datos robusta con UTF8MB4
- **API REST**: Endpoints completos para CRUD de Users y Notes
- **Health Checks**: Monitoreo de salud de servicios
- **Logging**: Sistema de logs estructurado
- **Error Handling**: Manejo robusto de errores

## 📋 Requisitos

- Docker
- Docker Compose (v2.0+)

## 🛠️ Instalación y Ejecución

### Con Docker Compose (Recomendado)

```bash
# Clonar el repositorio
git clone <repo-url>
cd tennismanager-saas

# Ejecutar con logs visibles
make up-logs

# O ejecutar en segundo plano
make up-build
```

La aplicación estará disponible en:
- **🏠 Landing Page**: `http://localhost:5001/`
- **💚 Health Check**: `http://localhost:5001/health`
- **📊 API Info**: `http://localhost:5001/api-info`

### Comandos Útiles

```bash
# Ver ayuda de comandos disponibles
make help

# Ver logs en tiempo real
make logs

# Ver estado de servicios
make health

# Inicializar datos de ejemplo
make init-db

# Probar la API
make test-health
make test-users
make test-notes

# Limpiar y reconstruir
make rebuild
```

### Desarrollo Local

1. Instalar dependencias:
```bash
make dev-install
```

2. Configurar variables de entorno:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/flask_notes_db
```

3. Ejecutar la aplicación:
```bash
make dev-run
```

## 🌐 Interfaz Web

### Landing Page
La landing page de TennisManager incluye:

- **Hero Section**: Presentación atractiva del producto
- **Características**: 6 funcionalidades principales destacadas
- **Estadísticas**: Métricas de uso y confiabilidad
- **API Demo**: Ejemplos de código en vivo
- **Call to Action**: Formularios de contacto y prueba gratuita
- **Footer Completo**: Enlaces y información de contacto

### Diseño Responsivo
- **Mobile First**: Optimizado para dispositivos móviles
- **Bootstrap 5**: Framework CSS moderno
- **Animaciones**: Efectos suaves y profesionales
- **Tipografía**: Google Fonts (Poppins)
- **Iconos**: Font Awesome 6

## 📚 API Endpoints

### Información General
- `GET /` - Landing page principal
- `GET /health` - Health check con estadísticas
- `GET /api-info` - Información detallada de la API

### Users

- `GET /api/users` - Obtener todos los usuarios
- `GET /api/users/<id>` - Obtener usuario por ID
- `GET /api/users/<id>/notes` - Obtener usuario con sus notas
- `POST /api/users` - Crear nuevo usuario
- `PUT /api/users/<id>` - Actualizar usuario
- `DELETE /api/users/<id>` - Eliminar usuario

### Notes

- `GET /api/notes` - Obtener todas las notas
- `GET /api/notes?user_id=<id>` - Obtener notas de un usuario
- `GET /api/notes/<id>` - Obtener nota por ID
- `GET /api/notes/search?user_id=<id>&title=<query>` - Buscar notas por título
- `POST /api/notes` - Crear nueva nota
- `PUT /api/notes/<id>` - Actualizar nota
- `DELETE /api/notes/<id>` - Eliminar nota

## 📝 Ejemplos de Uso

### Acceder a la Landing Page
```bash
# Abrir en el navegador
open http://localhost:5001/
```

### Health Check Completo
```bash
curl http://localhost:5001/health | jq
```

### Información de la API
```bash
curl http://localhost:5001/api-info | jq
```

### Crear Usuario (Club Member)
```bash
curl -X POST http://localhost:5001/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_miembro",
    "email": "miembro@tennisclub.com"
  }'
```

### Crear Nota (Reserva de Cancha)
```bash
curl -X POST http://localhost:5001/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Reserva Cancha 1",
    "content": "Reserva para partido dobles - Sábado 16:00",
    "user_id": 1
  }'
```

## 🏗️ Arquitectura

```
├── app/
│   ├── __init__.py          # Factory pattern de Flask
│   ├── templates/           # Templates HTML
│   │   ├── base.html        # Template base
│   │   └── index.html       # Landing page
│   ├── models/              # Modelos de datos (M)
│   │   ├── user.py
│   │   └── note.py
│   ├── services/            # Lógica de negocio
│   │   ├── base_service.py  # Servicio base (DRY)
│   │   ├── user_service.py
│   │   └── note_service.py
│   └── controllers/         # Controladores/Vistas (C)
│       ├── base_controller.py
│       ├── user_controller.py
│       └── note_controller.py
├── config.py               # Configuración
├── app.py                 # Punto de entrada + Landing page
├── init.sql               # Inicialización de MySQL
├── requirements.txt       # Dependencias
├── Dockerfile            # Imagen Docker
├── docker-compose.yml    # Orquestación
└── Makefile             # Comandos útiles
```

## 🎨 Características de la Landing Page

### Diseño Visual
- **Colores**: Paleta verde profesional (#2E8B57, #228B22, #32CD32)
- **Gradientes**: Efectos modernos y atractivos
- **Cards**: Diseño con hover effects y sombras
- **Responsive**: Adaptable a todos los dispositivos

### Funcionalidades JavaScript
- **Smooth Scrolling**: Navegación suave entre secciones
- **Animaciones**: Contadores animados en estadísticas
- **Intersection Observer**: Animaciones al hacer scroll
- **Bootstrap Components**: Navbar responsive y modales

### Secciones Principales
1. **Hero**: Presentación principal con CTAs
2. **Features**: 6 características clave del producto
3. **Stats**: Estadísticas de uso y confiabilidad
4. **API Demo**: Ejemplos de código en vivo
5. **CTA**: Call to action para conversión
6. **Contact**: Información de contacto

## 🔧 Mejoras v2.0

### Nuevas Características
- **Landing Page Completa**: Interfaz web profesional
- **Branding TennisManager**: Identidad visual coherente
- **Flask 3.0**: Actualización a la última versión
- **SQLAlchemy 2.0**: Soporte para la nueva sintaxis
- **Health Checks**: Monitoreo automático de servicios
- **Wait Strategy**: Espera inteligente para la base de datos
- **Logging**: Sistema de logs mejorado
- **Error Handling**: Manejo robusto de errores HTTP
- **Security**: Usuario no-root en contenedores
- **UTF8MB4**: Soporte completo para emojis y caracteres especiales

### Principios Implementados

#### DRY (Don't Repeat Yourself)
- `BaseService`: Operaciones CRUD comunes
- `BaseController`: Métodos de respuesta estándar
- Templates reutilizables con Jinja2

#### KISS (Keep It Simple, Stupid)
- Estructura clara y simple
- Separación de responsabilidades
- Código legible y mantenible

#### Clean Code
- Nombres descriptivos
- Funciones pequeñas y específicas
- Comentarios útiles
- Manejo consistente de errores
- Logging estructurado

## 🗄️ Modelo de Datos

### User (Club Member)
```json
{
  "id": 1,
  "username": "eidan",
  "email": "eidan@tennismanager.com",
  "created_at": "2025-01-27T10:00:00",
  "updated_at": "2025-01-27T10:00:00",
  "notes_count": 3
}
```

### Note (Reserva/Actividad)
```json
{
  "id": 1,
  "title": "Reserva Cancha Central",
  "content": "Cancha reservada para torneo del sábado 15:00-17:00",
  "created_at": "2025-01-27T10:00:00",
  "updated_at": "2025-01-27T10:00:00",
  "user_id": 1,
  "user": {
    "id": 1,
    "username": "eidan"
  }
}
```

## 🔍 Respuestas de la API

### Health Check Completo
```json
{
  "status": "healthy",
  "message": "TennisManager API funcionando correctamente",
  "database": "connected",
  "version": "2.0.0",
  "company": "TennisManager SaaS",
  "stats": {
    "users": 5,
    "notes": 8,
    "uptime": "99.9%"
  },
  "endpoints": {
    "landing": "http://localhost:5001/",
    "api_info": "http://localhost:5001/api-info",
    "users": "http://localhost:5001/api/users",
    "notes": "http://localhost:5001/api/notes"
  }
}
```

## 🚀 Próximas Mejoras

- [ ] Autenticación JWT para usuarios
- [ ] Dashboard de administración
- [ ] Sistema de reservas real
- [ ] Integración de pagos (Stripe)
- [ ] Notificaciones push
- [ ] App móvil nativa
- [ ] Tests unitarios y de integración
- [ ] Documentación OpenAPI/Swagger
- [ ] Métricas con Prometheus
- [ ] Cache con Redis

## 🐛 Troubleshooting

### Puerto 5000 ocupado
Si tienes problemas con el puerto 5000 (común en macOS con AirPlay), la aplicación usa el puerto 5001 por defecto.

### Problemas de conexión a MySQL
La aplicación incluye un sistema de espera automática para MySQL. Si persisten los problemas:

```bash
# Ver logs detallados
make logs-db

# Reconstruir completamente
make rebuild
```

### Landing page no carga
Verifica que los templates estén en la carpeta correcta:
```bash
ls -la app/templates/
```

## 🎾 Demo en Vivo

Una vez ejecutada la aplicación, puedes:

1. **Visitar la landing page**: `http://localhost:5001/`
2. **Probar la API**: Usar los botones "Probar API" en la página
3. **Ver estadísticas**: Health check con datos reales
4. **Explorar endpoints**: Información completa en `/api-info`

## 👨‍💻 Desarrollado por

**Eidan** - 2025

Especialista en desarrollo de aplicaciones SaaS para la industria deportiva.

---

**Versión**: 2.0.0
**Flask**: 3.0.0
**Python**: 3.11
**MySQL**: 8.0
**Frontend**: Bootstrap 5 + Vanilla JS
