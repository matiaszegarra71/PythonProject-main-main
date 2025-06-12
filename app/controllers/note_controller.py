from flask import Blueprint, request, g
from app.services.note_service import NoteService
from app.services.user_service import UserService
from app.controllers.base_controller import BaseController
from app.utils.auth_decorators import token_required, manager_required

note_bp = Blueprint('notes', __name__)
note_service = NoteService()
user_service = UserService()

class NoteController(BaseController):
    """Controlador para operaciones de Note"""

    def __init__(self):
        super().__init__(note_service)

    @staticmethod
    @note_bp.route('', methods=['GET'])
    @token_required
    def get_all():
        """Obtener todas las notas (managers/admins ven todas, clients solo las suyas)"""
        try:
            current_user = g.current_user
            user_id = request.args.get('user_id', type=int)

            # Si no es manager/admin, solo puede ver sus propias notas
            if not current_user.has_permission('manager'):
                user_id = current_user.id

            if user_id:
                # Verificar permisos para ver notas de otro usuario
                if user_id != current_user.id and not current_user.has_permission('manager'):
                    return NoteController.error_response(
                        'No tienes permisos para ver las notas de otro usuario', 403
                    )
                notes = NoteService.get_by_user_id(user_id)
                message = f'Se encontraron {len(notes)} notas del usuario {user_id}'
            else:
                notes = NoteService.get_all()
                message = f'Se encontraron {len(notes)} notas'

            return NoteController.success_response(
                data=[note.to_dict() for note in notes],
                message=message
            )
        except Exception as e:
            return NoteController.error_response(f'Error al obtener notas: {str(e)}', 500)

    @staticmethod
    @note_bp.route('/<int:note_id>', methods=['GET'])
    @token_required
    def get_by_id(note_id):
        """Obtener nota por ID (usuarios solo pueden ver sus propias notas)"""
        try:
            current_user = g.current_user
            note = NoteService.get_by_id(note_id)

            if not note:
                return NoteController.error_response('Nota no encontrada', 404)

            # Verificar permisos: usuarios solo pueden ver sus propias notas
            if note.user_id != current_user.id and not current_user.has_permission('manager'):
                return NoteController.error_response(
                    'No tienes permisos para ver esta nota', 403
                )

            return NoteController.success_response(
                data=note.to_dict(),
                message='Nota encontrada'
            )
        except Exception as e:
            return NoteController.error_response(f'Error al obtener nota: {str(e)}', 500)

    @staticmethod
    @note_bp.route('/search', methods=['GET'])
    @token_required
    def search():
        """Buscar notas por título y usuario"""
        try:
            current_user = g.current_user
            user_id = request.args.get('user_id', type=int)
            title = request.args.get('title', '')

            # Si no es manager/admin, solo puede buscar en sus propias notas
            if not current_user.has_permission('manager'):
                user_id = current_user.id

            if not user_id:
                return NoteController.error_response('user_id es requerido', 400)

            # Verificar permisos para buscar notas de otro usuario
            if user_id != current_user.id and not current_user.has_permission('manager'):
                return NoteController.error_response(
                    'No tienes permisos para buscar en las notas de otro usuario', 403
                )

            notes = NoteService.search_by_title_and_user(user_id, title)

            return NoteController.success_response(
                data=[note.to_dict() for note in notes],
                message=f'Se encontraron {len(notes)} notas que coinciden con "{title}"'
            )
        except Exception as e:
            return NoteController.error_response(f'Error en búsqueda: {str(e)}', 500)

    @staticmethod
    @note_bp.route('', methods=['POST'])
    @token_required
    def create():
        """Crear nueva nota"""
        try:
            current_user = g.current_user
            data = request.get_json()

            if not data:
                return NoteController.error_response('Datos JSON requeridos', 400)

            # Validar campos requeridos
            required_fields = ['title', 'content']
            missing_fields = [field for field in required_fields if not data.get(field)]

            if missing_fields:
                return NoteController.error_response(
                    f'Campos requeridos: {", ".join(missing_fields)}', 400
                )

            # Si se especifica user_id, verificar permisos
            user_id = data.get('user_id')
            if user_id:
                # Solo managers/admins pueden crear notas para otros usuarios
                if user_id != current_user.id and not current_user.has_permission('manager'):
                    return NoteController.error_response(
                        'No tienes permisos para crear notas para otro usuario', 403
                    )
            else:
                # Si no se especifica user_id, usar el del usuario actual
                data['user_id'] = current_user.id

            note = NoteService.create(data)
            return NoteController.success_response(
                data=note.to_dict(),
                message=f'Nota "{note.title}" creada exitosamente',
                status_code=201
            )
        except ValueError as e:
            return NoteController.error_response(str(e), 400)
        except Exception as e:
            return NoteController.error_response(f'Error al crear nota: {str(e)}', 500)

    @staticmethod
    @note_bp.route('/<int:note_id>', methods=['PUT'])
    @token_required
    def update(note_id):
        """Actualizar nota (usuarios solo pueden actualizar sus propias notas)"""
        try:
            current_user = g.current_user
            data = request.get_json()

            if not data:
                return NoteController.error_response('Datos JSON requeridos', 400)

            # Verificar que la nota existe y permisos
            note = NoteService.get_by_id(note_id)
            if not note:
                return NoteController.error_response('Nota no encontrada', 404)

            # Verificar permisos: usuarios solo pueden actualizar sus propias notas
            if note.user_id != current_user.id and not current_user.has_permission('manager'):
                return NoteController.error_response(
                    'No tienes permisos para actualizar esta nota', 403
                )

            # No permitir cambiar el user_id a usuarios normales
            if 'user_id' in data and not current_user.has_permission('manager'):
                return NoteController.error_response(
                    'No puedes cambiar el propietario de la nota', 403
                )

            note = NoteService.update(note_id, data)
            return NoteController.success_response(
                data=note.to_dict(),
                message=f'Nota "{note.title}" actualizada exitosamente'
            )
        except ValueError as e:
            return NoteController.error_response(str(e), 400)
        except Exception as e:
            return NoteController.error_response(f'Error al actualizar nota: {str(e)}', 500)

    @staticmethod
    @note_bp.route('/<int:note_id>', methods=['DELETE'])
    @token_required
    def delete(note_id):
        """Eliminar nota (usuarios solo pueden eliminar sus propias notas)"""
        try:
            current_user = g.current_user

            # Verificar que la nota existe y permisos
            note = NoteService.get_by_id(note_id)
            if not note:
                return NoteController.error_response('Nota no encontrada', 404)

            # Verificar permisos: usuarios solo pueden eliminar sus propias notas
            if note.user_id != current_user.id and not current_user.has_permission('manager'):
                return NoteController.error_response(
                    'No tienes permisos para eliminar esta nota', 403
                )

            success = NoteService.delete(note_id)
            if not success:
                return NoteController.error_response('Error al eliminar nota', 500)

            return NoteController.success_response(
                message='Nota eliminada exitosamente'
            )
        except Exception as e:
            return NoteController.error_response(f'Error al eliminar nota: {str(e)}', 500)

note_controller = NoteController()

@note_bp.route('/', methods=['GET'])
def get_all_notes():
    """GET /api/notes - Obtener todas las notas"""
    user_id = request.args.get('user_id')

    if user_id:
        # Filtrar por usuario
        user_id, error = note_controller.validate_id(user_id)
        if error:
            return note_controller.error_response(error)

        notes = note_controller.service.get_notes_by_user(user_id)
    else:
        # Obtener todas las notas
        notes = note_controller.service.get_all()

    notes_data = [note.to_dict() for note in notes]
    return note_controller.success_response(
        data=notes_data,
        message=f"Se encontraron {len(notes_data)} notas"
    )

@note_bp.route('/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """GET /api/notes/<id> - Obtener nota por ID"""
    note = note_controller.service.get_by_id(note_id)
    if not note:
        return note_controller.error_response("Nota no encontrada", 404)

    return note_controller.success_response(
        data=note.to_dict(),
        message="Nota encontrada"
    )

@note_bp.route('/search', methods=['GET'])
def search_notes():
    """GET /api/notes/search?user_id=<id>&title=<query> - Buscar notas por título"""
    user_id = request.args.get('user_id')
    title_query = request.args.get('title')

    if not user_id:
        return note_controller.error_response("user_id es requerido")

    if not title_query:
        return note_controller.error_response("title es requerido para la búsqueda")

    user_id, error = note_controller.validate_id(user_id)
    if error:
        return note_controller.error_response(error)

    notes = note_controller.service.search_notes_by_title(user_id, title_query)
    notes_data = [note.to_dict() for note in notes]

    return note_controller.success_response(
        data=notes_data,
        message=f"Se encontraron {len(notes_data)} notas con '{title_query}'"
    )

@note_bp.route('/', methods=['POST'])
def create_note():
    """POST /api/notes - Crear nueva nota"""
    data, error = note_controller.get_json_data()
    if error:
        return note_controller.error_response(error)

    # Validar datos
    validation_errors = note_controller.service.validate_note_data(data)
    if validation_errors:
        return note_controller.error_response(
            "Datos inválidos",
            errors=validation_errors
        )

    # Verificar que el usuario existe
    user = user_service.get_by_id(data['user_id'])
    if not user:
        return note_controller.error_response("Usuario no encontrado", 404)

    # Crear nota
    note, error = note_controller.service.create(data)
    if error:
        return note_controller.error_response(f"Error al crear nota: {error}")

    return note_controller.success_response(
        data=note.to_dict(),
        message="Nota creada exitosamente",
        status_code=201
    )

@note_bp.route('/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """PUT /api/notes/<id> - Actualizar nota"""
    data, error = note_controller.get_json_data()
    if error:
        return note_controller.error_response(error)

    # Validar datos
    validation_errors = note_controller.service.validate_note_data(data, is_update=True)
    if validation_errors:
        return note_controller.error_response(
            "Datos inválidos",
            errors=validation_errors
        )

    # Si se está actualizando el user_id, verificar que existe
    if 'user_id' in data:
        user = user_service.get_by_id(data['user_id'])
        if not user:
            return note_controller.error_response("Usuario no encontrado", 404)

    # Actualizar nota
    note, error = note_controller.service.update(note_id, data)
    if error:
        return note_controller.error_response(f"Error al actualizar nota: {error}")

    return note_controller.success_response(
        data=note.to_dict(),
        message="Nota actualizada exitosamente"
    )

@note_bp.route('/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """DELETE /api/notes/<id> - Eliminar nota"""
    success, error = note_controller.service.delete(note_id)
    if not success:
        status_code = 404 if "no encontrado" in error.lower() else 400
        return note_controller.error_response(f"Error al eliminar nota: {error}", status_code)

    return note_controller.success_response(
        message="Nota eliminada exitosamente"
    )
