from flask import Blueprint, request, jsonify, current_app
import os
from utils.file_helper import save_file
from flask_jwt_extended import jwt_required

media_bp = Blueprint("media", __name__)

@media_bp.route("/", methods=["GET"])
@jwt_required()
def get_medias():
    return jsonify({"message": "media routes working!"})


@media_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    file_path = save_file(file)
    
    if not file_path:
        return jsonify({"error": "Invalid file type"}), 400

    return jsonify({"message": "File uploaded successfully", "file_path": file_path})