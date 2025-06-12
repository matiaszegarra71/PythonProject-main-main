"""
🐛 Ejemplo de Debugging en AuthController
Mostrando cómo debuggear el login de TennisManager
"""

from flask import Blueprint, request, jsonify
from app.models.user import User
from app.services.user_service import UserService
from app.utils.response_helper import success_response, error_response
import ipdb

auth_debug_bp = Blueprint('auth_debug', __name__)

@auth_debug_bp.route('/api/auth/login-debug', methods=['POST'])
def login_debug():
    """
    Ejemplo de login con debugging
    Similar a tu auth_controller.py pero con breakpoints
    """
    try:
        # 1. Obtener datos del request
        data = request.get_json()

        # 🐛 BREAKPOINT: Inspeccionar datos recibidos
        ipdb.set_trace()  # ⬅️ Aquí puedes ver qué datos llegaron

        # Validar datos requeridos
        if not data or not data.get('username') or not data.get('password'):
            return error_response('Username y password son requeridos', 400)

        username = data.get('username')
        password = data.get('password')

        # 2. Buscar usuario por username o email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        # 🐛 BREAKPOINT: Verificar si se encontró el usuario
        ipdb.set_trace()  # ⬅️ Aquí puedes ver si user es None o tiene datos

        # Verificar si el usuario existe
        if not user:
            return error_response('Credenciales inválidas', 401, 'INVALID_CREDENTIALS')

        # 3. Verificar contraseña
        password_valid = user.check_password(password)

        # 🐛 BREAKPOINT: Verificar validación de contraseña
        ipdb.set_trace()  # ⬅️ Aquí puedes ver si la contraseña es válida

        if not password_valid:
            return error_response('Credenciales inválidas', 401, 'INVALID_CREDENTIALS')

        # 4. Verificar si el usuario está activo
        if not user.is_active:
            return error_response('Usuario inactivo', 401, 'USER_INACTIVE')

        # 5. Generar token JWT
        token = user.generate_token()

        # 🐛 BREAKPOINT: Verificar token generado
        ipdb.set_trace()  # ⬅️ Aquí puedes ver el token JWT

        # 6. Actualizar último login
        user.update_last_login()

        # 7. Preparar respuesta
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.value,
            'is_active': user.is_active,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }

        response_data = {
            'token': token,
            'user': user_data
        }

        # 🐛 BREAKPOINT: Verificar respuesta final
        ipdb.set_trace()  # ⬅️ Aquí puedes ver la respuesta completa

        return success_response('Login exitoso', response_data)

    except Exception as e:
        # 🐛 BREAKPOINT: Debugging en excepciones
        ipdb.set_trace()  # ⬅️ Aquí puedes inspeccionar el error

        return error_response(f'Error interno del servidor: {str(e)}', 500)

# Ejemplo de debugging condicional
@auth_debug_bp.route('/api/auth/validate-debug', methods=['GET'])
def validate_debug():
    """Ejemplo de validación con debugging condicional"""
    from app.utils.auth_decorators import token_required

    # Solo debuggear si hay un header específico
    debug_mode = request.headers.get('X-Debug-Mode') == 'true'

    if debug_mode:
        ipdb.set_trace()  # ⬅️ Solo debuggea si X-Debug-Mode: true

    # Tu lógica de validación aquí...
    return success_response('Token válido', {'debug_mode': debug_mode})

# Ejemplo de debugging con logging
@auth_debug_bp.route('/api/auth/register-debug', methods=['POST'])
def register_debug():
    """Ejemplo de registro con debugging y logging"""
    import logging

    # Configurar logging para debugging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    try:
        data = request.get_json()
        logger.debug(f"Datos recibidos: {data}")

        # Debugging solo para usuarios específicos
        if data and data.get('username') == 'debug_user':
            ipdb.set_trace()  # ⬅️ Solo debuggea para 'debug_user'

        # Tu lógica de registro aquí...
        return success_response('Usuario registrado', data)

    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        ipdb.post_mortem()  # ⬅️ Debugging post-mortem
        return error_response('Error en registro', 500)
