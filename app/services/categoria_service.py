from app.models.Categoria import Categoria
from app.services.base_service import BaseService

class CategoriaService(BaseService):
    def __init__(self):
        super().__init__(Categoria)
