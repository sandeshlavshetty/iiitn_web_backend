
from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required

card_bp = Blueprint("card", __name__)

@card_bp.route("/", methods=["GET"])
# @jwt_required()
def get_cards():
    return jsonify({"message": "card routes working!"})


from database import db
from database.models import Card
from database.db_operations import add_card, get_card_by_id, update_card, delete_card



@card_bp.route('/cards', methods=['POST'])
def create_card():
    data = request.get_json()
    card = add_card(db.session, data)
    return jsonify({"message": "Card created", "card": card.c_id}), 201

@card_bp.route('/cards/<int:c_id>', methods=['GET'])
def get_card(c_id):
    card = get_card_by_id(db.session, c_id)
    return jsonify(card) if card else (jsonify({"message": "Card not found"}), 404)

@card_bp.route('/cards/<int:c_id>', methods=['PUT'])
def edit_card(c_id):
    data = request.get_json()
    card = update_card(db.session, c_id, data)
    return jsonify({"message": "Card updated"}) if card else (jsonify({"message": "Card not found"}), 404)

@card_bp.route('/cards/<int:c_id>', methods=['DELETE'])
def remove_card(c_id):
    card = delete_card(db.session, c_id)
    return jsonify({"message": "Card deleted"}) if card else (jsonify({"message": "Card not found"}), 404)
