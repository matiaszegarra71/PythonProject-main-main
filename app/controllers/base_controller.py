from flask import jsonify, request

class BaseController:
    """Controlador base con métodos comunes (DRY principle)"""

    def __init__(self, service):
        self.service = service

    @staticmethod
    def success_response(data=None, message="Success", status_code=200):
        """Respuesta exitosa estándar"""
        response = {
            'success': True,
            'message': message
        }
        if data is not None:
            response['data'] = data
        return jsonify(response), status_code

    @staticmethod
    def error_response(message="Error", status_code=400, errors=None):
        """Respuesta de error estándar"""
        response = {
            'success': False,
            'message': message
        }
        if errors:
            response['errors'] = errors
        return jsonify(response), status_code

    def get_json_data(self):
        """Obtener datos JSON de la request"""
        if not request.is_json:
            return None, "Content-Type debe ser application/json"

        data = request.get_json()
        if not data:
            return None, "Body JSON requerido"

        return data, None

    def validate_id(self, id_param):
        """Validar que el ID sea un entero válido"""
        try:
            return int(id_param), None
        except (ValueError, TypeError):
            return None, "ID debe ser un número entero válido"
