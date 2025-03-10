from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def role_required(required_role):
    """Middleware to check if user has required role"""
    def decorator(fn):
        def wrapper(*args, **kwargs):
            user = get_jwt_identity()  # Extract user info
            if user["role"] != required_role:
                return jsonify({"error": "Access denied"}), 403  # Forbidden
            return fn(*args, **kwargs)
        return wrapper
    return decorator
