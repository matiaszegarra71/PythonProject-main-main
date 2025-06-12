from app.models.usuario import Usuario
from app.services.base_service import BaseService

class UsuarioService(BaseService):
    def __init__(self):
        super().__init__(Usuario)
