from flask import Blueprint
from app.services.carrito_service import CarritoService
from app.controllers.base_controller import BaseController

carrito_bp = Blueprint('carritos', __name__)
carrito_service = CarritoService()

class CarritoController(BaseController):
    def __init__(self):
        super().__init__(carrito_service)

    @staticmethod
    @carrito_bp.route('', methods=['GET'])
    def get_all():
        try:
            carritos = CarritoService.get_all()
            return CarritoController.success_response(
                data=[c.to_dict() for c in carritos],
                message=f'Se encontraron {len(carritos)} carritos'
            )
        except Exception as e:
            return CarritoController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @carrito_bp.route('/<int:carrito_id>', methods=['GET'])
    def get_by_id(carrito_id):
        try:
            carrito = CarritoService.get_by_id(carrito_id)
            if not carrito:
                return CarritoController.error_response('Carrito no encontrado', 404)
            return CarritoController.success_response(
                data=carrito.to_dict(),
                message='Carrito encontrado'
            )
        except Exception as e:
            return CarritoController.error_response(f'Error: {str(e)}', 500)

carrito_controller = CarritoController()
