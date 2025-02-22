from flask import Blueprint, jsonify

student_bp = Blueprint("student", __name__)

@student_bp.route("/", methods=["GET"])
def get_students():
    return jsonify({"message": "student routes working!"})
