from flask import Blueprint, request, jsonify
from database.db_operations import add_social_media, get_social_media, delete_social_media

social_media_bp = Blueprint("social_media", __name__)

@social_media_bp.route("/", methods=["GET"])
def fetch_social_media():
    sm_entry = get_social_media()
    if not sm_entry:
        return jsonify({"error": "No social media links found"}), 404
#
    return jsonify({
        "sm_id": sm_entry.sm_id,
        "insta": sm_entry.insta,
        "twitter": sm_entry.twitter,
        "linkedin": sm_entry.linkedin,
        "youtube": sm_entry.youtube
    })

@social_media_bp.route("/", methods=["POST"])
def update_social_media():
    data = request.json
    insta = data.get("insta", "")
    twitter = data.get("twitter", "")
    linkedin = data.get("linkedin", "")
    youtube = data.get("youtube", "")

    sm_entry = add_social_media(insta, twitter, linkedin, youtube)
    
    return jsonify({
        "message": "Social media links updated",
        "sm_id": sm_entry.sm_id
    })

@social_media_bp.route("/", methods=["DELETE"])
def remove_social_media():
    if delete_social_media():
        return jsonify({"message": "Social media links deleted"})
    return jsonify({"error": "No social media links found"}), 404

