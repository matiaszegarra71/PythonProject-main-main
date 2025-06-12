from flask import Blueprint, request, jsonify, g
from app.models.user import User
from app.services.user_service import UserService
from app.utils.auth_decorators import token_required, admin_required
from app.controllers.base_controller import BaseController
from app import db

auth_bp = Blueprint('auth', __name__)

class AuthController(BaseController):

    @staticmethod
    @auth_bp.route('/login', methods=['POST'])
    def login():
        """Endpoint de login que retorna JWT token"""
        try:
            data = request.get_json()

            if not data:
                return AuthController.error_response(
                    'Datos JSON requeridos', 400
                )

            # Validar campos requeridos
            required_fields = ['username', 'password']
            missing_fields = [field for field in required_fields if not data.get(field)]

            if missing_fields:
                return AuthController.error_response(
                    f'Campos requeridos: {", ".join(missing_fields)}', 400
                )

            # Validar que username no sea None antes de hacer strip()
            username_raw = data.get('username')
            password = data.get('password')

            if not username_raw:
                return AuthController.error_response(
                    'Username no puede estar vacío', 400
                )

            if not password:
                return AuthController.error_response(
                    'Password no puede estar vacío', 400
                )

            username = username_raw.strip()

            # Buscar usuario por username o email
            user = User.query.filter(
                (User.username == username) | (User.email == username)
            ).first()

            if not user:
                return AuthController.error_response(
                    'Credenciales inválidas', 401
                )

            if not user.is_active:
                return AuthController.error_response(
                    'Cuenta desactivada. Contacte al administrador', 401
                )

            if not user.check_password(password):
                return AuthController.error_response(
                    'Credenciales inválidas', 401
                )

            # Generar token JWT
            token = user.generate_token(expires_in=3600)  # 1 hora

            # Actualizar último login
            user.update_last_login()

            return AuthController.success_response(
                data={
                    'token': token,
                    'user': user.to_public_dict(),
                    'expires_in': 3600
                },
                message=f'Login exitoso. Bienvenido {user.username}!'
            )

        except Exception as e:
            return AuthController.error_response(
                f'Error en login: {str(e)}', 500
            )

    @staticmethod
    @auth_bp.route('/register', methods=['POST'])
    def register():
        """Endpoint de registro de nuevos usuarios"""
        try:
            data = request.get_json()

            if not data:
                return AuthController.error_response(
                    'Datos JSON requeridos', 400
                )

            # Validar campos requeridos
            required_fields = ['username', 'email', 'password']
            missing_fields = [field for field in required_fields if not data.get(field)]

            if missing_fields:
                return AuthController.error_response(
                    f'Campos requeridos: {", ".join(missing_fields)}', 400
                )

            username = data.get('username').strip()
            email = data.get('email').strip().lower()
            password = data.get('password')
            role = data.get('role', 'client')  # Por defecto client

            # Campos opcionales de información personal
            name = data.get('name', '').strip() if data.get('name') else None
            last_name = data.get('last_name', '').strip() if data.get('last_name') else None
            phone = data.get('phone', '').strip() if data.get('phone') else None
            address = data.get('address', '').strip() if data.get('address') else None
            gender = data.get('gender')

            # Validar rol
            valid_roles = ['admin', 'manager', 'client']
            if role not in valid_roles:
                return AuthController.error_response(
                    f'Rol inválido. Roles válidos: {", ".join(valid_roles)}', 400
                )

            # Validar género si se proporciona
            if gender and gender not in ['male', 'female', 'other', 'prefer_not_to_say']:
                return AuthController.error_response(
                    'Género inválido. Opciones válidas: male, female, other, prefer_not_to_say', 400
                )

            # Validar longitud de contraseña
            if len(password) < 6:
                return AuthController.error_response(
                    'La contraseña debe tener al menos 6 caracteres', 400
                )

            # Validar teléfono si se proporciona
            if phone and len(phone) < 7:
                return AuthController.error_response(
                    'El teléfono debe tener al menos 7 caracteres', 400
                )

            # Verificar si el usuario ya existe
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()

            if existing_user:
                if existing_user.username == username:
                    return AuthController.error_response(
                        'El nombre de usuario ya está en uso', 409
                    )
                else:
                    return AuthController.error_response(
                        'El email ya está registrado', 409
                    )

            # Crear nuevo usuario
            user = User(
                username=username,
                email=email,
                name=name,
                last_name=last_name,
                phone=phone,
                address=address,
                gender=gender,
                role=role
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            # Generar token para el nuevo usuario
            token = user.generate_token(expires_in=3600)

            return AuthController.success_response(
                data={
                    'token': token,
                    'user': user.to_public_dict(),
                    'expires_in': 3600
                },
                message=f'Usuario {username} registrado exitosamente',
                status_code=201
            )

        except Exception as e:
            db.session.rollback()
            return AuthController.error_response(
                f'Error en registro: {str(e)}', 500
            )

    @staticmethod
    @auth_bp.route('/validate', methods=['GET'])
    @token_required
    def validate_token():
        """Validar token JWT y retornar información del usuario"""
        try:
            user = g.current_user

            return AuthController.success_response(
                data={
                    'valid': True,
                    'user': user.to_public_dict(),
                    'permissions': {
                        'is_admin': user.has_role('admin'),
                        'is_manager': user.has_permission('manager'),
                        'is_client': user.has_permission('client')
                    }
                },
                message='Token válido'
            )

        except Exception as e:
            return AuthController.error_response(
                f'Error en validación: {str(e)}', 500
            )

    @staticmethod
    @auth_bp.route('/profile', methods=['GET'])
    @token_required
    def get_profile():
        """Obtener perfil del usuario autenticado"""
        try:
            user = g.current_user

            return AuthController.success_response(
                data=user.to_dict(),
                message='Perfil obtenido exitosamente'
            )

        except Exception as e:
            return AuthController.error_response(
                f'Error al obtener perfil: {str(e)}', 500
            )

    @staticmethod
    @auth_bp.route('/change-password', methods=['PUT'])
    @token_required
    def change_password():
        """Cambiar contraseña del usuario autenticado"""
        try:
            data = request.get_json()

            if not data:
                return AuthController.error_response(
                    'Datos JSON requeridos', 400
                )

            current_password = data.get('current_password')
            new_password = data.get('new_password')

            if not current_password or not new_password:
                return AuthController.error_response(
                    'current_password y new_password son requeridos', 400
                )

            user = g.current_user

            # Verificar contraseña actual
            if not user.check_password(current_password):
                return AuthController.error_response(
                    'Contraseña actual incorrecta', 401
                )

            # Validar nueva contraseña
            if len(new_password) < 6:
                return AuthController.error_response(
                    'La nueva contraseña debe tener al menos 6 caracteres', 400
                )

            # Cambiar contraseña
            user.set_password(new_password)
            db.session.commit()

            return AuthController.success_response(
                message='Contraseña cambiada exitosamente'
            )

        except Exception as e:
            db.session.rollback()
            return AuthController.error_response(
                f'Error al cambiar contraseña: {str(e)}', 500
            )

    @staticmethod
    @auth_bp.route('/users', methods=['GET'])
    @token_required
    @admin_required
    def list_all_users():
        """Listar todos los usuarios (solo admin)"""
        try:
            users = User.query.all()

            return AuthController.success_response(
                data=[user.to_dict() for user in users],
                message=f'Se encontraron {len(users)} usuarios'
            )

        except Exception as e:
            return AuthController.error_response(
                f'Error al listar usuarios: {str(e)}', 500
            )
