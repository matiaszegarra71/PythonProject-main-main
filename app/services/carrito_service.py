from app.models.Carrito import Carrito
from app.services.base_service import BaseService

class CarritoService(BaseService):
    def __init__(self):
        super().__init__(Carrito)
