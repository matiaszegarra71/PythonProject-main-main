from flask import Blueprint, request, g
from app.services.user_service import UserService
from app.controllers.base_controller import BaseController
from app.utils.auth_decorators import token_required, admin_required, manager_required
from app.services.usuario_service import UsuarioService


user_bp = Blueprint('users', __name__)
user_service = UserService()

class UserController(BaseController):
    """Controlador para operaciones de User"""

    def __init__(self):
        super().__init__(user_service)

    @staticmethod
    @user_bp.route('', methods=['GET'])
    @token_required
    @manager_required
    def get_all():
        """Obtener todos los usuarios (requiere rol manager o admin)"""
        try:
            users = UserService.get_all()
            return UserController.success_response(
                data=[user.to_dict() for user in users],
                message=f'Se encontraron {len(users)} usuarios'
            )
        except Exception as e:
            return UserController.error_response(f'Error al obtener usuarios: {str(e)}', 500)

    @staticmethod
    @user_bp.route('/<int:user_id>', methods=['GET'])
    @token_required
    def get_by_id(user_id):
        """Obtener usuario por ID (usuarios pueden ver su propio perfil, managers/admins pueden ver cualquiera)"""
        try:
            current_user = g.current_user

            # Los usuarios solo pueden ver su propio perfil, managers/admins pueden ver cualquiera
            if not current_user.has_permission('manager') and current_user.id != user_id:
                return UserController.error_response(
                    'No tienes permisos para ver este usuario', 403
                )

            user = UserService.get_by_id(user_id)
            if not user:
                return UserController.error_response('Usuario no encontrado', 404)

            return UserController.success_response(
                data=user.to_dict(),
                message='Usuario encontrado'
            )
        except Exception as e:
            return UserController.error_response(f'Error al obtener usuario: {str(e)}', 500)

    @staticmethod
    @user_bp.route('/<int:user_id>/notes', methods=['GET'])
    @token_required
    def get_user_with_notes(user_id):
        """Obtener usuario con sus notas"""
        try:
            current_user = g.current_user

            # Los usuarios solo pueden ver sus propias notas, managers/admins pueden ver cualquiera
            if not current_user.has_permission('manager') and current_user.id != user_id:
                return UserController.error_response(
                    'No tienes permisos para ver las notas de este usuario', 403
                )

            user = UserService.get_user_with_notes(user_id)
            if not user:
                return UserController.error_response('Usuario no encontrado', 404)

            user_data = user.to_dict()
            user_data['notes'] = [note.to_dict() for note in user.notes]

            return UserController.success_response(
                data=user_data,
                message=f'Usuario encontrado con {len(user.notes)} notas'
            )
        except Exception as e:
            return UserController.error_response(f'Error al obtener usuario con notas: {str(e)}', 500)

    @staticmethod
    @user_bp.route('', methods=['POST'])
    @token_required
    @admin_required
    def create():
        """Crear nuevo usuario (solo admin)"""
        try:
            data = request.get_json()

            if not data:
                return UserController.error_response('Datos JSON requeridos', 400)

            # Validar campos requeridos
            required_fields = ['username', 'email', 'password']
            missing_fields = [field for field in required_fields if not data.get(field)]

            if missing_fields:
                return UserController.error_response(
                    f'Campos requeridos: {", ".join(missing_fields)}', 400
                )

            # Validar rol si se proporciona
            role = data.get('role', 'client')
            valid_roles = ['admin', 'manager', 'client']
            if role not in valid_roles:
                return UserController.error_response(
                    f'Rol inválido. Roles válidos: {", ".join(valid_roles)}', 400
                )

            user = UserService.create(data)
            return UserController.success_response(
                data=user.to_dict(),
                message=f'Usuario {user.username} creado exitosamente',
                status_code=201
            )
        except ValueError as e:
            return UserController.error_response(str(e), 400)
        except Exception as e:
            return UserController.error_response(f'Error al crear usuario: {str(e)}', 500)

    @staticmethod
    @user_bp.route('/<int:user_id>', methods=['PUT'])
    @token_required
    def update(user_id):
        """Actualizar usuario (usuarios pueden actualizar su propio perfil, admins pueden actualizar cualquiera)"""
        try:
            current_user = g.current_user

            # Los usuarios solo pueden actualizar su propio perfil, admins pueden actualizar cualquiera
            if not current_user.has_role('admin') and current_user.id != user_id:
                return UserController.error_response(
                    'No tienes permisos para actualizar este usuario', 403
                )

            data = request.get_json()

            if not data:
                return UserController.error_response('Datos JSON requeridos', 400)

            # Los usuarios normales no pueden cambiar su rol
            if 'role' in data and not current_user.has_role('admin'):
                return UserController.error_response(
                    'Solo los administradores pueden cambiar roles', 403
                )

            user = UserService.update(user_id, data)
            if not user:
                return UserController.error_response('Usuario no encontrado', 404)

            return UserController.success_response(
                data=user.to_dict(),
                message=f'Usuario {user.username} actualizado exitosamente'
            )
        except ValueError as e:
            return UserController.error_response(str(e), 400)
        except Exception as e:
            return UserController.error_response(f'Error al actualizar usuario: {str(e)}', 500)

    @staticmethod
    @user_bp.route('/<int:user_id>', methods=['DELETE'])
    @token_required
    @admin_required
    def delete(user_id):
        """Eliminar usuario (solo admin)"""
        try:
            current_user = g.current_user

            # No permitir que los admins se eliminen a sí mismos
            if current_user.id == user_id:
                return UserController.error_response(
                    'No puedes eliminar tu propia cuenta', 400
                )

            success = UserService.delete(user_id)
            if not success:
                return UserController.error_response('Usuario no encontrado', 404)

            return UserController.success_response(
                message='Usuario eliminado exitosamente'
            )
        except Exception as e:
            return UserController.error_response(f'Error al eliminar usuario: {str(e)}', 500)

user_controller = UserController()
