from flask import Blueprint
from app.services.emprendimiento_service import EmprendimientoService
from app.controllers.base_controller import BaseController

emprendimiento_bp = Blueprint('emprendimientos', __name__)
emprendimiento_service = EmprendimientoService()

class EmprendimientoController(BaseController):
    def __init__(self):
        super().__init__(emprendimiento_service)

    @staticmethod
    @emprendimiento_bp.route('', methods=['GET'])
    def get_all():
        try:
            emprendimientos = EmprendimientoService.get_all()
            return EmprendimientoController.success_response(
                data=[e.to_dict() for e in emprendimientos],
                message=f'Se encontraron {len(emprendimientos)} emprendimientos'
            )
        except Exception as e:
            return EmprendimientoController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @emprendimiento_bp.route('/<int:emprendimiento_id>', methods=['GET'])
    def get_by_id(emprendimiento_id):
        try:
            emprendimiento = EmprendimientoService.get_by_id(emprendimiento_id)
            if not emprendimiento:
                return EmprendimientoController.error_response('Emprendimiento no encontrado', 404)
            return EmprendimientoController.success_response(
                data=emprendimiento.to_dict(),
                message='Emprendimiento encontrado'
            )
        except Exception as e:
            return EmprendimientoController.error_response(f'Error: {str(e)}', 500)

emprendimiento_controller = EmprendimientoController()
