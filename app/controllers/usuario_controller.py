from flask import Blueprint, request, g
from app.services.usuario_service import UsuarioService
from app.controllers.base_controller import BaseController
from app.utils.auth_decorators import token_required, admin_required

usuario_bp = Blueprint('usuarios', __name__)
usuario_service = UsuarioService()

class UsuarioController(BaseController):
    """Controlador para operaciones de Usuario"""

    def __init__(self):
        super().__init__(usuario_service)

    @staticmethod
    @usuario_bp.route('', methods=['GET'])
    @token_required
    def get_all():
        """Obtener todos los usuarios"""
        try:
            usuarios = UsuarioService.get_all()
            return UsuarioController.success_response(
                data=[usuario.to_dict() for usuario in usuarios],
                message=f'Se encontraron {len(usuarios)} usuarios'
            )
        except Exception as e:
            return UsuarioController.error_response(f'Error al obtener usuarios: {str(e)}', 500)

    @staticmethod
    @usuario_bp.route('/<int:usuario_id>', methods=['GET'])
    @token_required
    def get_by_id(usuario_id):
        """Obtener usuario por ID"""
        try:
            usuario = UsuarioService.get_by_id(usuario_id)
            if not usuario:
                return UsuarioController.error_response('Usuario no encontrado', 404)

            return UsuarioController.success_response(
                data=usuario.to_dict(),
                message='Usuario encontrado'
            )
        except Exception as e:
            return UsuarioController.error_response(f'Error al obtener usuario: {str(e)}', 500)

    @staticmethod
    @usuario_bp.route('', methods=['POST'])
    def create():
        """Crear nuevo usuario"""
        try:
            data = request.get_json()

            if not data:
                return UsuarioController.error_response('Datos JSON requeridos', 400)

            # Validar campos requeridos
            required_fields = ['correoElectronico', 'contraseña']
            missing_fields = [field for field in required_fields if not data.get(field)]

            if missing_fields:
                return UsuarioController.error_response(
                    f'Campos requeridos: {", ".join(missing_fields)}', 400
                )

            usuario = UsuarioService.create(data)
            return UsuarioController.success_response(
                data=usuario.to_dict(),
                message=f'Usuario creado exitosamente',
                status_code=201
            )
        except ValueError as e:
            return UsuarioController.error_response(str(e), 400)
        except Exception as e:
            return UsuarioController.error_response(f'Error al crear usuario: {str(e)}', 500)

    @staticmethod
    @usuario_bp.route('/<int:usuario_id>', methods=['PUT'])
    @token_required
    def update(usuario_id):
        """Actualizar usuario"""
        try:
            data = request.get_json()

            if not data:
                return UsuarioController.error_response('Datos JSON requeridos', 400)

            usuario = UsuarioService.update(usuario_id, data)
            if not usuario:
                return UsuarioController.error_response('Usuario no encontrado', 404)

            return UsuarioController.success_response(
                data=usuario.to_dict(),
                message='Usuario actualizado exitosamente'
            )
        except ValueError as e:
            return UsuarioController.error_response(str(e), 400)
        except Exception as e:
            return UsuarioController.error_response(f'Error al actualizar usuario: {str(e)}', 500)

    @staticmethod
    @usuario_bp.route('/<int:usuario_id>', methods=['DELETE'])
    @token_required
    @admin_required
    def delete(usuario_id):
        """Eliminar usuario (solo admin)"""
        try:
            success = UsuarioService.delete(usuario_id)
            if not success:
                return UsuarioController.error_response('Usuario no encontrado', 404)

            return UsuarioController.success_response(
                message='Usuario eliminado exitosamente'
            )
        except Exception as e:
            return UsuarioController.error_response(f'Error al eliminar usuario: {str(e)}', 500)

usuario_controller = UsuarioController()