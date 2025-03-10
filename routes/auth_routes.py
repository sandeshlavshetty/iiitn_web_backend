from flask import Blueprint, jsonify, session
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies,get_jwt
)

from database.models import Person
from database import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def get_auths():
    return jsonify({"message": "Auth routes working!"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    print("Received Data:", data)  # Debugging step
    email = data.get("email")
    password = data.get("password")

    user = Person.query.filter_by(email_pri=email).first()
    
    if user and check_password_hash(user.password, password):
        # Generate JWT tokens
        access_token = create_access_token(identity=user.email_pri, additional_claims={"role": user.role})
        refresh_token = create_refresh_token(identity=user.email_pri, additional_claims={"role": user.role})

        # Store user info in Flask session
        session["user"] = {
            "email": user.email_pri,
            "role": user.role,
            "name": user.name
        }

        # Set refresh token as HTTP-only cookie
        response = jsonify({"access_token": access_token, "user": session["user"]})
        set_access_cookies(response, access_token)  # Securely store access token in cookies
        set_refresh_cookies(response, refresh_token)  # Store refresh token securely
        return response, 200

    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_email = get_jwt_identity()
    claims = get_jwt()
    return jsonify({
        "message": f"Welcome, {user_email}!",
        "role": claims["role"]
    }), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using a valid refresh token"""
    user = get_jwt_identity()
    new_access_token = create_access_token(identity=user)

    response = jsonify({"access_token": new_access_token})
    set_access_cookies(response, new_access_token)  # Ensure access token is set in cookies
    return response, 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Logout user by clearing JWT cookies and session"""
    response = jsonify({"message": "Logged out successfully"})
    unset_jwt_cookies(response)  # Properly remove JWT cookies
    session.clear()  # Clear session
    return response, 200