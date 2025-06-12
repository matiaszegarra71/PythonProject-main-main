from app.models.note import Note
from app.services.base_service import BaseService
from app import db

class NoteService(BaseService):
    """Servicio para operaciones específicas de Note"""

    def __init__(self):
        super().__init__(Note)

    @staticmethod
    def get_all():
        """Obtener todas las notas"""
        return Note.query.all()

    @staticmethod
    def get_by_id(note_id):
        """Obtener nota por ID"""
        return Note.query.get(note_id)

    @staticmethod
    def get_by_user_id(user_id):
        """Obtener todas las notas de un usuario"""
        return Note.query.filter_by(user_id=user_id).all()

    @staticmethod
    def search_by_title_and_user(user_id, title_query):
        """Buscar notas por título y usuario"""
        return Note.query.filter(
            Note.user_id == user_id,
            Note.title.contains(title_query)
        ).all()

    @staticmethod
    def create(data):
        """Crear nueva nota con validaciones"""
        # Validar campos requeridos
        required_fields = ['title', 'content', 'user_id']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f'El campo {field} es requerido')

        title = data.get('title').strip()
        content = data.get('content').strip()
        user_id = data.get('user_id')

        # Validaciones
        if len(title) < 1:
            raise ValueError('El título no puede estar vacío')

        if len(content) < 1:
            raise ValueError('El contenido no puede estar vacío')

        # Crear nota
        note = Note(
            title=title,
            content=content,
            user_id=user_id
        )

        db.session.add(note)
        db.session.commit()

        return note

    @staticmethod
    def update(note_id, data):
        """Actualizar nota"""
        note = Note.query.get(note_id)
        if not note:
            return None

        # Campos que se pueden actualizar
        updatable_fields = ['title', 'content', 'user_id']

        for field in updatable_fields:
            if field in data:
                if field == 'title':
                    new_title = data[field].strip()
                    if len(new_title) < 1:
                        raise ValueError('El título no puede estar vacío')
                    note.title = new_title

                elif field == 'content':
                    new_content = data[field].strip()
                    if len(new_content) < 1:
                        raise ValueError('El contenido no puede estar vacío')
                    note.content = new_content

                elif field == 'user_id':
                    note.user_id = data[field]

        db.session.commit()
        return note

    @staticmethod
    def delete(note_id):
        """Eliminar nota"""
        try:
            note = Note.query.get(note_id)
            if not note:
                return False

            db.session.delete(note)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    def get_notes_by_user(self, user_id):
        """Obtener todas las notas de un usuario (método de instancia para compatibilidad)"""
        return self.model.query.filter_by(user_id=user_id).all()

    def get_notes_by_user_paginated(self, user_id, page=1, per_page=10):
        """Obtener notas de un usuario con paginación"""
        return self.model.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def search_notes_by_title(self, user_id, title_query):
        """Buscar notas por título (método de instancia para compatibilidad)"""
        return self.model.query.filter(
            self.model.user_id == user_id,
            self.model.title.contains(title_query)
        ).all()

    def validate_note_data(self, data, is_update=False):
        """Validar datos de la nota"""
        errors = []

        if not is_update or 'title' in data:
            if not data.get('title') or len(data['title'].strip()) < 1:
                errors.append("Título es requerido")

        if not is_update or 'user_id' in data:
            if not data.get('user_id'):
                errors.append("user_id es requerido")

        return errors
