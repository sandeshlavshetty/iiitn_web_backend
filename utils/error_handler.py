

from flask import jsonify
from werkzeug.exceptions import HTTPException

class APIException(Exception):
    def __init__(self, message, code=400):
        super().__init__(message)
        self.message = message
        self.code = code

def register_error_handlers(app):
    @app.errorhandler(APIException)
    def handle_api_exception(e):
        return jsonify({
            "status": "error",
            "message": e.message
        }), e.code

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            "status": "error",
            "message": e.description,
            "code": e.code
        }), e.code

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        return jsonify({
            "status": "error",
            "message": "Internal Server Error",
            "detail": str(e)
        }), 500
