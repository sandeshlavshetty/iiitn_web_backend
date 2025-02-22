from flask import Blueprint
from .auth_routes import auth_bp
from .user_routes import user_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
