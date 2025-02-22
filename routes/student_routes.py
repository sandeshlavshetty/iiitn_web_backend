from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

student_bp = Blueprint("student", __name__)

@student_bp.route("/", methods=["GET"])
@jwt_required()
def get_students():
    return jsonify({"message": "student routes working!"})
