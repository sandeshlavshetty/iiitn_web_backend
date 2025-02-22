from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required


faculty_bp = Blueprint("faculty", __name__)

@faculty_bp.route("/", methods=["GET"])
@jwt_required()
def get_facultys():
    return jsonify({"message": "faculty routes working!"})
