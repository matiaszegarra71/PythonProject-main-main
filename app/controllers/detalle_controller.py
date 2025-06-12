from flask import Blueprint
from app.services.detalle_service import DetalleService
from app.controllers.base_controller import BaseController

detalle_bp = Blueprint('detalles', __name__)
detalle_service = DetalleService()

class DetalleController(BaseController):
    def __init__(self):
        super().__init__(detalle_service)

    @staticmethod
    @detalle_bp.route('', methods=['GET'])
    def get_all():
        try:
            detalles = DetalleService.get_all()
            return DetalleController.success_response(
                data=[d.to_dict() for d in detalles],
                message=f'Se encontraron {len(detalles)} detalles'
            )
        except Exception as e:
            return DetalleController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @detalle_bp.route('/<int:detalle_id>', methods=['GET'])
    def get_by_id(detalle_id):
        try:
            detalle = DetalleService.get_by_id(detalle_id)
            if not detalle:
                return DetalleController.error_response('Detalle no encontrado', 404)
            return DetalleController.success_response(
                data=detalle.to_dict(),
                message='Detalle encontrado'
            )
        except Exception as e:
            return DetalleController.error_response(f'Error: {str(e)}', 500)

detalle_controller = DetalleController()
