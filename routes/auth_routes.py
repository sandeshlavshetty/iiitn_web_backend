from flask import Blueprint, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def get_auths():
    return jsonify({"message": "auth routes working!"})
