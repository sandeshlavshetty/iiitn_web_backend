from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from database.models import Person
from database import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = Person.query.filter_by(email_pri=data.get("email")).first()
    
    if user and check_password_hash(user.password, data.get("password")):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401
