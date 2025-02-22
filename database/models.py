from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = "person"
    p_id = db.Column(db.Integer, primary_key=True)
    email_pri = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
