from flask import Blueprint, request, jsonify, current_app
import os
from utils.file_helper import save_file
from database.db_operations import add_media, get_media, delete_media , create_media,get_all_media,get_media_by_id,update_media,delete_media
# from flask_jwt_extended import jwt_required
from database.models import Media  # Ensure Media model is imported
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

    print(f"File name :- {file.filename}")
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


@media_bp.route('/media', methods=['POST'])
def create_new_media():
    data = request.get_json()
    new_media = create_media(data)
    return jsonify({'message': 'Media added successfully', 'm_id': new_media.M_id}), 201

@media_bp.route('/media', methods=['GET'])
def fetch_all_media():
    media_list = get_all_media()
    return jsonify([{
        'M_id': media.m_id,
        'M_category': media.m_category,
        'M_sub_category': media.m_sub_category,
        'Title': media.title,
        'Updated_by': media.updated_by,
        'Updated_time': media.updated_time,
        'Added_by': media.added_by,
        'Added_time': media.added_time,
        'media_img_id': media.media_img_id,
        'media_vid_id': media.media_vid_id,
        'media_doc_id': media.media_doc_id
    } for media in media_list]), 200

@media_bp.route('/media/<int:m_id>', methods=['GET'])
def fetch_media_by_id(m_id):
    media = get_media_by_id(m_id)
    if not media:
        return jsonify({'error': 'Media not found'}), 404
    return jsonify({
        'M_id': media.m_id,
        'M_category': media.m_category,
        'M_sub_category': media.m_sub_category,
        'Title': media.title,
        'Updated_by': media.updated_by,
        'Updated_time': media.updated_time,
        'Added_by': media.added_by,
        'Added_time': media.added_time,
        'media_img_id': media.media_img_id,
        'media_vid_id': media.media_vid_id,
        'media_doc_id': media.media_doc_id
    }), 200

@media_bp.route('/media/<int:m_id>', methods=['PUT'])
def modify_media(m_id):
    data = request.get_json()
    updated_media = update_media(m_id, data)
    if not updated_media:
        return jsonify({'error': 'Media not found'}), 404
    return jsonify({'message': 'Media updated successfully'}), 200

@media_bp.route('/media/<int:m_id>', methods=['DELETE'])
def remove_media(m_id):
    if not delete_media(m_id):
        return jsonify({'error': 'Media not found'}), 404
    return jsonify({'message': 'Media deleted successfully'}), 200



@media_bp.route('/media/category/<string:category>', methods=['GET'])
def get_media_by_category(category):
    media_list = Media.query.filter_by(m_category=category).all()
    if not media_list:
        return jsonify({"message": "No media found for this category"}), 404
    return jsonify([{ 
        'M_id': media.m_id, 
        'M_category': media.m_category, 
        'Title': media.title,
        'Updated_by': media.updated_by,
        'Updated_time': media.updated_time,
        'Added_by': media.added_by,
        'Added_time': media.added_time,
        'media_img_id': media.media_img_id,
        'media_vid_id': media.media_vid_id,
        'media_doc_id': media.media_doc_id
    } for media in media_list]), 200

@media_bp.route('/media/sub_category/<string:sub_category>', methods=['GET'])
def get_media_by_sub_category(sub_category):
    media_list = Media.query.filter_by(m_sub_category=sub_category).all()
    if not media_list:
        return jsonify({"message": "No media found for this sub-category"}), 404
    return jsonify([{ 
        'M_id': media.m_id, 
        'M_sub_category': media.m_sub_category, 
        'Title': media.title,
        'Updated_by': media.updated_by,
        'Updated_time': media.updated_time,
        'Added_by': media.added_by,
        'Added_time': media.added_time,
        'media_img_id': media.media_img_id,
        'media_vid_id': media.media_vid_id,
        'media_doc_id': media.media_doc_id
    } for media in media_list]), 200
