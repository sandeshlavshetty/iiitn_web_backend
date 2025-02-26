from flask import Blueprint
from .auth_routes import auth_bp
from .user_routes import user_bp
from .media_routes import media_bp
from .card_routes import card_bp
from .faculty_routes import faculty_bp
from .student_routes import student_bp
from .social_media_routes import social_media_bp
from .department_route import department_bp
from .alumni_routes import alumni_bp

def register_routes(app):
    app.register_blueprint(media_bp, url_prefix="/media")
    app.register_blueprint(social_media_bp, url_prefix="/social_media")
    app.register_blueprint(department_bp, url_prefix="/department")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(card_bp, url_prefix="/card")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(alumni_bp, url_prefix="/alumni")
