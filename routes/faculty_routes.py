from flask import Blueprint, jsonify

faculty_bp = Blueprint("faculty", __name__)

@faculty_bp.route("/", methods=["GET"])
def get_facultys():
    return jsonify({"message": "faculty routes working!"})
