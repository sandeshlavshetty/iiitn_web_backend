from flask import Blueprint, jsonify
# from flask_jwt_extended import jwt_required

card_bp = Blueprint("card", __name__)

@card_bp.route("/", methods=["GET"])
# @jwt_required()
def get_cards():
    return jsonify({"message": "card routes working!"})
