from functools import wraps
from flask import request, jsonify, g
from app.models.user import User

def token_required(f):
    """Decorador para requerir token JWT válido"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Buscar token en headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer TOKEN
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Formato de token inválido. Use: Bearer <token>'
                }), 401

        if not token:
            return jsonify({
                'success': False,
                'message': 'Token de acceso requerido'
            }), 401

        try:
            current_user = User.verify_token(token)
            if current_user is None:
                return jsonify({
                    'success': False,
                    'message': 'Token inválido o expirado'
                }), 401

            g.current_user = current_user

        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error al verificar token',
                'error': str(e)
            }), 401

        return f(*args, **kwargs)

    return decorated

def role_required(required_role):
    """Decorador para requerir rol específico"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(g, 'current_user') or g.current_user is None:
                return jsonify({
                    'success': False,
                    'message': 'Usuario no autenticado'
                }), 401

            if not g.current_user.has_permission(required_role):
                return jsonify({
                    'success': False,
                    'message': f'Acceso denegado. Se requiere rol: {required_role} o superior',
                    'user_role': g.current_user.role
                }), 403

            return f(*args, **kwargs)

        return decorated
    return decorator

def admin_required(f):
    """Decorador para requerir rol de administrador"""
    return role_required('admin')(f)

def manager_required(f):
    """Decorador para requerir rol de manager o superior"""
    return role_required('manager')(f)

def client_required(f):
    """Decorador para requerir cualquier usuario autenticado"""
    return role_required('client')(f)

def optional_auth(f):
    """Decorador para autenticación opcional"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Buscar token en headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer TOKEN
                current_user = User.verify_token(token)
                g.current_user = current_user
            except (IndexError, Exception):
                g.current_user = None
        else:
            g.current_user = None

        return f(*args, **kwargs)

    return decorated
