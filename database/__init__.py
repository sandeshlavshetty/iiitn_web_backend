from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # This should exist

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()