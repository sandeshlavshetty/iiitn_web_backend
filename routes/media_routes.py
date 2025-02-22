from flask import Blueprint, request, jsonify, current_app
import os
from utils.file_helper import save_file
from database.db_operations import add_media, get_media, delete_media
# from flask_jwt_extended import jwt_required

media_bp = Blueprint("media", __name__)

@media_bp.route("/", methods=["GET"])
# @jwt_required()
def get_medias():
    return jsonify({"message": "media routes working!"})




@media_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files or "media_type" not in request.form:
        return jsonify({"error": "File and media_type are required"}), 400

    file = request.files["file"]
    media_type = request.form["media_type"]

    file_path = save_file(file)  # Store locally
    if not file_path:
        return jsonify({"error": "Invalid file type"}), 400

    media_entry = add_media(file.filename, file_path, media_type)
    if not media_entry:
        return jsonify({"error": "Invalid media type"}), 400

    return jsonify({
        "message": "File uploaded successfully",
        "media_id": media_entry.media_img_id if media_type == "image" else
                    media_entry.media_vid_id if media_type == "video" else
                    media_entry.media_doc_id,
        "file_path": file_path
    })

@media_bp.route("/<media_type>/<int:media_id>", methods=["GET"])
def get_media_details(media_type, media_id):
    media = get_media(media_type, media_id)
    if not media:
        return jsonify({"error": "Media not found"}), 404

    return jsonify({
        "media_id": media.media_img_id if media_type == "image" else
                    media.media_vid_id if media_type == "video" else
                    media.media_doc_id,
        "file_name": media.image_file_name if media_type == "image" else
                     media.video_file_name if media_type == "video" else
                     media.doc_file_name,
        "file_path": media.image_path if media_type == "image" else
                     media.video_path if media_type == "video" else
                     media.doc_path
    })

@media_bp.route("/<media_type>/<int:media_id>", methods=["DELETE"])
def delete_media_file(media_type, media_id):
    if delete_media(media_type, media_id):
        return jsonify({"message": "Media deleted successfully"})
    return jsonify({"error": "Media not found"}), 404
