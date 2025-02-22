from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

media_bp = Blueprint("media", __name__)

@media_bp.route("/", methods=["GET"])
@jwt_required()
def get_medias():
    return jsonify({"message": "media routes working!"})
