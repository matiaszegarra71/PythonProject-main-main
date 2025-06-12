from flask import Blueprint
from app.services.producto_service import ProductoService
from app.controllers.base_controller import BaseController

producto_bp = Blueprint('productos', __name__)
producto_service = ProductoService()

class ProductoController(BaseController):
    def __init__(self):
        super().__init__(producto_service)

    @staticmethod
    @producto_bp.route('', methods=['GET'])
    def get_all():
        try:
            productos = ProductoService.get_all()
            return ProductoController.success_response(
                data=[p.to_dict() for p in productos],
                message=f'Se encontraron {len(productos)} productos'
            )
        except Exception as e:
            return ProductoController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @producto_bp.route('/<int:producto_id>', methods=['GET'])
    def get_by_id(producto_id):
        try:
            producto = ProductoService.get_by_id(producto_id)
            if not producto:
                return ProductoController.error_response('Producto no encontrado', 404)
            return ProductoController.success_response(
                data=producto.to_dict(),
                message='Producto encontrado'
            )
        except Exception as e:
            return ProductoController.error_response(f'Error: {str(e)}', 500)

producto_controller = ProductoController()
