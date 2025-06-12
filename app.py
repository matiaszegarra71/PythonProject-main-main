import os
import time
import logging
from flask import render_template
from app import create_app, db
from app.models.user import User
from app.models.note import Note
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_db(app, max_retries=30, delay=2):
    """Esperar a que la base de datos esté disponible"""
    for attempt in range(max_retries):
        try:
            with app.app_context():
                # Intentar conectar a la base de datos
                db.session.execute(text("SELECT 1"))
                logger.info("✅ Conexión a la base de datos establecida")
                return True
        except OperationalError as e:
            logger.warning(f"⏳ Intento {attempt + 1}/{max_retries}: Esperando base de datos... ({str(e)[:100]})")
            time.sleep(delay)
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            time.sleep(delay)

    logger.error("❌ No se pudo conectar a la base de datos después de varios intentos")
    return False

def create_tables_safely(app):
    """Crear tablas de forma segura"""
    try:
        with app.app_context():
            db.create_all()
            logger.info("✅ Tablas de base de datos creadas/verificadas")
            return True
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        return False

# Crear la aplicación
app = create_app(os.getenv('FLASK_ENV', 'default'))

@app.route('/')
def index():
    """Landing page principal"""
    try:
        # Obtener estadísticas reales de la base de datos
        with app.app_context():
            total_users = User.query.count()
            total_notes = Note.query.count()

        return render_template('index.html',
                             total_users=total_users,
                             total_notes=total_notes)
    except Exception as e:
        logger.warning(f"No se pudieron obtener estadísticas: {e}")
        return render_template('index.html',
                             total_users=0,
                             total_notes=0)

@app.route('/api-info')
def api_info():
    """Información detallada de la API"""
    return {
        'message': 'TennisManager API v3.0 - Con autenticación JWT',
        'version': '3.0.0',
        'status': 'running',
        'description': 'API REST para gestión de canchas de tenis con autenticación JWT y roles',
        'company': 'TennisManager SaaS',
        'authentication': {
            'type': 'JWT Bearer Token',
            'header': 'Authorization: Bearer <token>',
            'expires_in': '1 hour',
            'roles': ['admin', 'manager', 'client']
        },
        'endpoints': {
            'public': {
                'landing': '/',
                'health': '/health',
                'api_info': '/api-info'
            },
            'auth': {
                'login': 'POST /api/auth/login',
                'register': 'POST /api/auth/register',
                'validate': 'GET /api/auth/validate (requires token)',
                'profile': 'GET /api/auth/profile (requires token)',
                'change_password': 'PUT /api/auth/change-password (requires token)',
                'list_users': 'GET /api/auth/users (admin only)'
            },
            'users': {
                'list': 'GET /api/users (manager+ required)',
                'get': 'GET /api/users/<id> (own profile or manager+)',
                'create': 'POST /api/users (admin only)',
                'update': 'PUT /api/users/<id> (own profile or admin)',
                'delete': 'DELETE /api/users/<id> (admin only)',
                'with_notes': 'GET /api/users/<id>/notes (own notes or manager+)'
            },
            'notes': {
                'list': 'GET /api/notes (own notes or manager+ for all)',
                'get': 'GET /api/notes/<id> (own notes or manager+)',
                'create': 'POST /api/notes (authenticated)',
                'update': 'PUT /api/notes/<id> (own notes or manager+)',
                'delete': 'DELETE /api/notes/<id> (own notes or manager+)',
                'search': 'GET /api/notes/search (own notes or manager+)',
                'by_user': 'GET /api/notes?user_id=<id> (own notes or manager+)'
            }
        },
        'role_permissions': {
            'admin': 'Full access to all endpoints',
            'manager': 'Can manage users and all notes',
            'client': 'Can only access own profile and notes'
        },
        'features': [
            'JWT Authentication with roles',
            'Password hashing with bcrypt',
            'Role-based access control',
            'Token validation and refresh',
            'Secure user management',
            'API REST completa',
            'Validaciones robustas',
            'Arquitectura MVC',
            'Clean Code (DRY, KISS)',
            'Dockerizado con MySQL',
            'Health checks automáticos',
            'Logging estructurado'
        ],
        'tech_stack': {
            'backend': 'Flask 3.0',
            'database': 'MySQL 8.0',
            'orm': 'SQLAlchemy 2.0',
            'auth': 'JWT + bcrypt',
            'containerization': 'Docker + Docker Compose',
            'frontend': 'Bootstrap 5 + Vanilla JS'
        },
        'test_users': {
            'admin': {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
            'manager': {'username': 'manager1', 'password': 'manager123', 'role': 'manager'},
            'client': {'username': 'eidan', 'password': 'eidan123', 'role': 'client'}
        }
    }

@app.route('/health')
def health_check():
    """Endpoint de health check mejorado"""
    try:
        # Verificar conexión a la base de datos
        with app.app_context():
            db.session.execute(text("SELECT 1"))

            # Obtener estadísticas básicas
            users_count = User.query.count()
            notes_count = Note.query.count()

            # Estadísticas por rol
            admin_count = User.query.filter_by(role='admin').count()
            manager_count = User.query.filter_by(role='manager').count()
            client_count = User.query.filter_by(role='client').count()

        return {
            'status': 'healthy',
            'message': 'TennisManager API v3.0 funcionando correctamente',
            'database': 'connected',
            'version': '3.0.0',
            'company': 'TennisManager SaaS',
            'authentication': 'JWT enabled',
            'stats': {
                'users': users_count,
                'notes': notes_count,
                'roles': {
                    'admin': admin_count,
                    'manager': manager_count,
                    'client': client_count
                },
                'uptime': '99.9%'
            },
            'endpoints': {
                'landing': 'http://localhost:5001/',
                'api_info': 'http://localhost:5001/api-info',
                'auth_login': 'http://localhost:5001/api/auth/login',
                'users': 'http://localhost:5001/api/users',
                'notes': 'http://localhost:5001/api/notes'
            }
        }, 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            'status': 'unhealthy',
            'message': 'Error en la conexión a la base de datos',
            'company': 'TennisManager SaaS',
            'version': '3.0.0',
            'error': str(e)
        }, 503

@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404"""
    return {
        'success': False,
        'message': 'Endpoint no encontrado',
        'error': 'Not Found',
        'available_endpoints': {
            'public': {
                'landing': '/',
                'health': '/health',
                'api_info': '/api-info'
            },
            'auth': {
                'login': '/api/auth/login',
                'register': '/api/auth/register',
                'validate': '/api/auth/validate'
            },
            'protected': {
                'users': '/api/users',
                'notes': '/api/notes'
            }
        }
    }, 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500"""
    return {
        'success': False,
        'message': 'Error interno del servidor',
        'error': 'Internal Server Error',
        'company': 'TennisManager SaaS',
        'version': '3.0.0'
    }, 500

if __name__ == '__main__':
    logger.info("🚀 Iniciando TennisManager API v3.0 con autenticación JWT...")

    # Esperar a que la base de datos esté disponible
    if wait_for_db(app):
        # Crear tablas
        if create_tables_safely(app):
            logger.info("🎉 TennisManager API v3.0 lista para recibir peticiones")
            logger.info("🌐 Landing page: http://localhost:5001/")
            logger.info("💚 Health check: http://localhost:5001/health")
            logger.info("📊 API info: http://localhost:5001/api-info")
            logger.info("🔐 Auth login: http://localhost:5001/api/auth/login")
            logger.info("🔑 Usuarios de prueba: admin/admin123, manager1/manager123, eidan/eidan123")
            app.run(host='0.0.0.0', port=5000, debug=True)
        else:
            logger.error("❌ Error al inicializar las tablas")
            exit(1)
    else:
        logger.error("❌ No se pudo conectar a la base de datos")
        exit(1)
