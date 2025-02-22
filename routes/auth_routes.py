from flask import Blueprint, jsonify
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database.models import Person
from database import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def get_auths():
    return jsonify({"message": "auth routes working!"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = Person.query.filter_by(email_pri=email).first()
    
    if user and check_password_hash(user.password, password):
        # Generate JWT token
        access_token = create_access_token(identity={"email": user.email_pri, "role": user.role})
        return jsonify({"access_token": access_token}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()  # Protect this route
def protected():
    user = get_jwt_identity()
    return jsonify({"message": f"Welcome, {user['email']}!"}), 200

