
from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required

card_bp = Blueprint("card", __name__)

@card_bp.route("/", methods=["GET"])
# @jwt_required()
def get_cards():
    return jsonify({"message": "card routes working!"})


from database import db
from database.models import Card
from database.db_operations import add_card, get_card_by_id, update_card, delete_card, get_media

# ✅ Fetch Cards in Table Format
@card_bp.route('/cards', methods=['GET'])    #end_c
def get_cards_table():
    cards = Card.query.all()
    cards_list = [{
        "c_id": card.c_id,
        "c_category": card.c_category,
        "c_sub_category": card.c_sub_category,
        "title": card.title,
        "caption": card.caption,
        "content": card.content,
        "date": card.date.strftime('%Y-%m-%d') if card.date else None,
        "location": card.location,
        "media_img_id": card.media_img_id,
        "media_vid_id": card.media_vid_id,
        "media_doc_id": card.media_doc_id,
        "updated_by": card.updated_by,
        "updated_time": card.updated_time.strftime('%Y-%m-%d %H:%M:%S') if card.updated_time else None,
        "added_by": card.added_by,
        "added_time": card.added_time.strftime('%Y-%m-%d %H:%M:%S') if card.added_time else None,
        "visibility": card.visibility  # ✅ Added visibility
    } for card in cards]
    
    return jsonify(cards_list), 200

@card_bp.route('/cards', methods=['POST'])  #end_c
def create_card():
    data = request.get_json()
    # Default to True if visibility is not provided
    data["visibility"] = data.get("visibility", True)
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




@card_bp.route('/cards/category/<string:category>', methods=['GET'])
def get_cards_by_category(category):
    cards = Card.query.filter_by(c_category=category).all()
    media_types = ["image", "video", "doc"]

    if not cards:
        return jsonify({"message": "No cards found for this category"}), 404

    cards_list = []
    for card in cards:
        media_img = get_media(media_types[0], card.media_img_id)
        media_vid = get_media(media_types[1], card.media_vid_id)
        media_doc = get_media(media_types[2], card.media_doc_id)

        cards_list.append({
            "c_id": card.c_id,
            "c_category": card.c_category,
            "c_sub_category": card.c_sub_category,
            "title": card.title,
            "caption": card.caption,
            "content": card.content,
            "date": card.date.strftime('%Y-%m-%d') if card.date else None,
            "location": card.location,
            "media_img_path": media_img.image_path if media_img else None,
            "media_vid_path": media_vid.video_path if media_vid else None,
            "media_doc_path": media_doc.doc_path if media_doc else None,
            "updated_by": card.updated_by,
            "updated_time": card.updated_time.strftime('%Y-%m-%d %H:%M:%S') if card.updated_time else None,
            "added_by": card.added_by,
            "added_time": card.added_time.strftime('%Y-%m-%d %H:%M:%S') if card.added_time else None,
            "visibility": card.visibility  # ✅ Added visibility
        })

    return jsonify(cards_list), 200


# # ✅ Fetch Cards by Category
# @card_bp.route('/cards/category/<string:category>', methods=['GET'])
# def get_cards_by_category(category):
#     cards = Card.query.filter_by(c_category=category).all()
#     if not cards:
#         return jsonify({"message": "No cards found for this category"}), 404
    
    
    
#     cards_list = [{
#         "c_id": card.c_id,
#         "c_category": card.c_category,
#         "c_sub_category": card.c_sub_category,
#         "title": card.title,
#         "caption": card.caption,
#         "content": card.content,
#         "date": card.date.strftime('%Y-%m-%d') if card.date else None,
#         "location": card.location,
#         "media_img_id": card.media_img_id,
#         "media_vid_id": card.media_vid_id,
#         "media_doc_id": card.media_doc_id,
#         "updated_by": card.updated_by,
#         "updated_time": card.updated_time.strftime('%Y-%m-%d %H:%M:%S') if card.updated_time else None,
#         "added_by": card.added_by,
#         "added_time": card.added_time.strftime('%Y-%m-%d %H:%M:%S') if card.added_time else None
#     } for card in cards]
    
#     return jsonify(cards_list), 200


# ✅ Fetch Cards by Sub-Category
@card_bp.route('/cards/sub_category/<string:sub_category>', methods=['GET'])
def get_cards_by_sub_category(sub_category):
    cards = Card.query.filter_by(c_sub_category=sub_category).all()
    if not cards:
        return jsonify({"message": "No cards found for this sub-category"}), 404
    
    cards_list = [{
        "c_id": card.c_id,
        "c_category": card.c_category,
        "c_sub_category": card.c_sub_category,
        "title": card.title,
        "caption": card.caption,
        "content": card.content,
        "date": card.date.strftime('%Y-%m-%d') if card.date else None,
        "location": card.location,
        "media_img_id": card.media_img_id,
        "media_vid_id": card.media_vid_id,
        "media_doc_id": card.media_doc_id,
        "updated_by": card.updated_by,
        "updated_time": card.updated_time.strftime('%Y-%m-%d %H:%M:%S') if card.updated_time else None,
        "added_by": card.added_by,
        "added_time": card.added_time.strftime('%Y-%m-%d %H:%M:%S') if card.added_time else None
    } for card in cards]
    
    return jsonify(cards_list), 200
