from flask import Blueprint
from app.services.categoria_service import CategoriaService
from app.controllers.base_controller import BaseController

categoria_bp = Blueprint('categorias', __name__)
categoria_service = CategoriaService()

class CategoriaController(BaseController):
    def __init__(self):
        super().__init__(categoria_service)

    @staticmethod
    @categoria_bp.route('', methods=['GET'])
    def get_all():
        try:
            categorias = CategoriaService.get_all()
            return CategoriaController.success_response(
                data=[c.to_dict() for c in categorias],
                message=f'Se encontraron {len(categorias)} categorías'
            )
        except Exception as e:
            return CategoriaController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @categoria_bp.route('/<int:categoria_id>', methods=['GET'])
    def get_by_id(categoria_id):
        try:
            categoria = CategoriaService.get_by_id(categoria_id)
            if not categoria:
                return CategoriaController.error_response('Categoría no encontrada', 404)
            return CategoriaController.success_response(
                data=categoria.to_dict(),
                message='Categoría encontrada'
            )
        except Exception as e:
            return CategoriaController.error_response(f'Error: {str(e)}', 500)

categoria_controller = CategoriaController()
