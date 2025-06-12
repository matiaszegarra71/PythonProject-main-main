from app.models.Emprendimiento import Emprendimiento
from app.services.base_service import BaseService

class EmprendimientoService(BaseService):
    def __init__(self):
        super().__init__(Emprendimiento)
