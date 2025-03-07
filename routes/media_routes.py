from flask import Blueprint, request, jsonify, current_app
import os
from utils.file_helper import save_file,delete_file,update_file
from database.db_operations import add_media, get_media, delete_media_type, create_media,get_all_media,get_media_by_id,update_media,delete_media,get_media_path

# from flask_jwt_extended import jwt_required
from database.models import Media  # Ensure Media model is imported
from config import Config
media_bp = Blueprint("media", __name__)

@media_bp.route("/", methods=["GET"])
# @jwt_required()
def get_medias():
    return jsonify({"message": "media routes working!"})


# img,video,doc routes

@media_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files or "media_type" not in request.form:
        return jsonify({"error": "File and media_type are required"}), 400
    print("supabase upload route is called")
    file = request.files["file"]
    

    file_path = save_file(file)  # Store locally
   
    if not file_path:
        return jsonify({"error": "Invalid file type"}), 400

    # print(f"File name :- {file.filename}")
    media_entry = add_media(file.filename, file_path)
    if not media_entry:
        return jsonify({"error": "Invalid media type"}), 400

    file_name = file.filename
    file_ext = file_name.split('.')[-1].lower()
    if file_ext in ["jpg", "jpeg", "png", "gif", "webp"]:
        media_type ="image"
    elif file_ext in ["mp4", "mov", "avi", "mkv"]:
        media_type = "video"
    else:
        media_type = "doc"
    
    return jsonify({
        "message": "File uploaded successfully",
        "media_id": media_entry.media_img_id if media_type == "image" else
                    media_entry.media_vid_id if media_type == "video" else
                    media_entry.media_doc_id,
        "file_path": file_path
    })


@media_bp.route("/<int:media_id>", methods=["GET"])
def get_media_details(media_id):
    media = get_media(media_id)
    if not media:
        return jsonify({"error": "Media not found"}), 404
    else :
        file_name = media.filename
        file_ext = file_name.split('.')[-1].lower()
        if file_ext in ["jpg", "jpeg", "png", "gif", "webp"]:
           media_type ="image"
        elif file_ext in ["mp4", "mov", "avi", "mkv"]:
           media_type = "video"
        else:
            media_type = "doc"
           
        return jsonify({
            "media_id": media.media_img_id if media_type == "image" else
                     media.media_vid_id if media_type == "video" else
                     media.media_doc_id,
            "file_name": media.image_file_name if media_type == "image" else
                     media.video_file_name if media_type == "video" else
                     media.doc_file_name,
            "file_path": os.path.join(Config.SUPABASE_STORAGE_URL,media.image_path) if media_type == "image" else
                        os.path.join(Config.SUPABASE_STORAGE_URL,media.video_path) if media_type == "video" else
                        os.path.join(Config.SUPABASE_STORAGE_URL,media.doc_path)
            })

@media_bp.route("/<int:media_id>", methods=["DELETE"])
def delete_media_file(media_id):
    result = delete_media_type(media_id)
    if result:
        return jsonify({"message": "Media deleted successfully"})
    
    return jsonify({"error": "Media not found"}), 404


@media_bp.route("/<path:media_path>", methods=["GET"])
def give_image_url(media_path):
    if media_path :
        print(f"public url :- {os.path.join(Config.SUPABASE_STORAGE_URL,media_path)}")
        return jsonify({"url": os.path.join(Config.SUPABASE_STORAGE_URL,media_path)})
    
    return None

# Medai table routes



@media_bp.route('/media', methods=['POST'])
def create_new_media():
    data = request.get_json()
    new_media = create_media(data)
    return jsonify({'message': 'Media added successfully', 'm_id': new_media.m_id}), 201

@media_bp.route('/media', methods=['GET'])
def fetch_all_media():
    media_list = get_all_media()
    return jsonify([{
        'm_id': media.m_id,
        'm_category': media.m_category,
        'm_sub_category': media.m_sub_category,
        'title': media.title,
        'updated_by': media.updated_by,
        'updated_time': media.updated_time,
        'added_by': media.added_by,
        'added_time': media.added_time,
        'media_img_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_img_id)),
        'media_vid_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_vid_id)),
        'media_doc_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_doc_id)),
        "preference": media.preference,
        "expiry_date" : media.expiry_date,
        'date' : media.date
    } for media in media_list]), 200

@media_bp.route('/media/<int:m_id>', methods=['GET'])
def fetch_media_by_id(m_id):
    media = get_media_by_id(m_id)
    if not media:
        return jsonify({'error': 'Media not found'}), 404
    return jsonify({
        'm_id': media.m_id,
        'm_category': media.m_category,
        'm_sub_category': media.m_sub_category,
        'title': media.title,
        'updated_by': media.updated_by,
        'updated_time': media.updated_time,
        'added_by': media.added_by,
        'added_time': media.added_time,
        'media_img_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_img_id)),
        'media_vid_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_vid_id)),
        'media_doc_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_doc_id)),
        "preference": media.preference,
        "expiry_date" : media.expiry_date
        "date" : media.date
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
        'm_id': media.m_id, 
        'm_category': media.m_category, 
        'title': media.title,
        'updated_by': media.updated_by,
        'updated_time': media.updated_time,
        'added_by': media.added_by,
        'added_time': media.added_time,
        'media_img_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_img_id)),
        'media_vid_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_vid_id)),
        'media_doc_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_doc_id)),
        "preference": media.preference,
        "expiry_date" : media.expiry_date,
        "date":media.date
    } for media in media_list]), 200

@media_bp.route('/media/sub_category/<string:sub_category>', methods=['GET'])
def get_media_by_sub_category(sub_category):
    media_list = Media.query.filter_by(m_sub_category=sub_category).all()
    if not media_list:
        return jsonify({"message": "No media found for this sub-category"}), 404
    return jsonify([{ 
        'm_id': media.m_id, 
        'm_sub_category': media.m_sub_category, 
        'title': media.title,
        'updated_by': media.updated_by,
        'updated_time': media.updated_time,
        'added_by': media.added_by,
        'added_time': media.added_time,
        'media_img_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_img_id)),
        'media_vid_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_vid_id)),
        'media_doc_id': os.path.join(Config.SUPABASE_STORAGE_URL,get_media_path(media.media_doc_id)),
        "preference": media.preference,
        "expiry_date" : media.expiry_date,
        "date":media.date
    } for media in media_list]), 200
