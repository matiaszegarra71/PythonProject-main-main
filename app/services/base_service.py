from app import db
from sqlalchemy.exc import IntegrityError

class BaseService:
    """Servicio base con operaciones CRUD comunes (DRY principle)"""

    def __init__(self, model):
        self.model = model

    def get_all(self):
        """Obtener todos los registros"""
        return self.model.query.all()

    def get_by_id(self, id):
        """Obtener registro por ID"""
        return self.model.query.get(id)

    def create(self, data):
        """Crear nuevo registro"""
        try:
            instance = self.model(**data)
            db.session.add(instance)
            db.session.commit()
            return instance, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    def update(self, id, data):
        """Actualizar registro existente"""
        try:
            instance = self.get_by_id(id)
            if not instance:
                return None, "Registro no encontrado"

            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)

            db.session.commit()
            return instance, None
        except IntegrityError as e:
            db.session.rollback()
            return None, str(e)
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    def delete(self, id):
        """Eliminar registro"""
        try:
            instance = self.get_by_id(id)
            if not instance:
                return False, "Registro no encontrado"

            db.session.delete(instance)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
