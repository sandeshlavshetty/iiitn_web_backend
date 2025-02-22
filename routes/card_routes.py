from flask import Blueprint, jsonify

card_bp = Blueprint("card", __name__)

@card_bp.route("/", methods=["GET"])
def get_cards():
    return jsonify({"message": "card routes working!"})
