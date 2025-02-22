from flask import Blueprint, jsonify

media_bp = Blueprint("media", __name__)

@media_bp.route("/", methods=["GET"])
def get_medias():
    return jsonify({"message": "media routes working!"})
