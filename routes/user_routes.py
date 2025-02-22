from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/", methods=["GET"])
# @jwt_required()  #middleware
def get_users():
    return jsonify({"message": "User routes working!"})
