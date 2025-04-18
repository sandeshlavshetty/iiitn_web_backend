
from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required
from config import Config
import os

card_bp = Blueprint("card", __name__)

@card_bp.route("/", methods=["GET"])
# @jwt_required()
def get_cards():
    return jsonify({"message": "card routes working!"})


from database import db
from database.models import Card
from database.db_operations import add_card, get_card_by_id, update_card, delete_card, get_media, get_media_path

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
       "media_img_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_img_id, "image")) if card.media_img_id else None,
        "media_vid_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_vid_id, "video")) if card.media_vid_id else None,
        "media_doc_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_doc_id, "doc")) if card.media_doc_id else None,
        "updated_by": card.updated_by,
        "updated_time": card.updated_time.strftime('%Y-%m-%d %H:%M:%S') if card.updated_time else None,
        "added_by": card.added_by,
        "added_time": card.added_time.strftime('%Y-%m-%d %H:%M:%S') if card.added_time else None,
        "visibility": card.visibility,
        "preference": card.preference,
        "expiry_date" : card.expiry_date 
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
    media_types = ["image", "video", "doc"]

    if not card:
        return jsonify({"message": "Card not found"}), 404

    

    card_data = {
        "c_id": card.c_id,
        "c_category": card.c_category,
        "c_sub_category": card.c_sub_category,
        "title": card.title,
        "caption": card.caption,
        "content": card.content,
        "date": card.date.strftime('%Y-%m-%d') if card.date else None,
        "location": card.location,
       "media_img_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_img_id, "image")) if card.media_img_id else None,
        "media_vid_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_vid_id, "video")) if card.media_vid_id else None,
        "media_doc_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_doc_id, "doc")) if card.media_doc_id else None,
        "updated_by": card.updated_by,
        "updated_time": card.updated_time.strftime('%Y-%m-%d %H:%M:%S') if card.updated_time else None,
        "added_by": card.added_by,
        "added_time": card.added_time.strftime('%Y-%m-%d %H:%M:%S') if card.added_time else None,
        "visibility": card.visibility,
        "preference": card.preference,
        "expiry_date" : card.expiry_date 
    }
    return jsonify(card_data), 200


@card_bp.route('/cards/<int:c_id>', methods=['PATCH'])
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

    if not cards:
        return jsonify({"message": "No cards found for this category"}), 404

    cards_list = []
    for card in cards:
        cards_list.append({
            "c_id": card.c_id,
            "c_category": card.c_category,
            "c_sub_category": card.c_sub_category,
            "title": card.title,
            "caption": card.caption,
            "content": card.content,
            "date": card.date.strftime('%Y-%m-%d') if card.date else None,
            "location": card.location,
            "media_img_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_img_id, "image")) if card.media_img_id else None,
            "media_vid_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_vid_id, "video")) if card.media_vid_id else None,
            "media_doc_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_doc_id, "doc")) if card.media_doc_id else None,
            "updated_by": card.updated_by,
            "updated_time": card.updated_time.strftime('%Y-%m-%d %H:%M:%S') if card.updated_time else None,
            "added_by": card.added_by,
            "added_time": card.added_time.strftime('%Y-%m-%d %H:%M:%S') if card.added_time else None,
            "visibility": card.visibility,
            "preference": card.preference,
            "expiry_date": card.expiry_date.strftime('%Y-%m-%d') if card.expiry_date else None,  # format the expiry_date properly
        })

    return jsonify(cards_list), 200



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
        "media_img_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_img_id, "image")) if card.media_img_id else None,
        "media_vid_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_vid_id, "video")) if card.media_vid_id else None,
        "media_doc_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_doc_id, "doc")) if card.media_doc_id else None,
        "updated_by": card.updated_by,
        "updated_time": card.updated_time.strftime('%Y-%m-%d %H:%M:%S') if card.updated_time else None,
        "added_by": card.added_by,
        "added_time": card.added_time.strftime('%Y-%m-%d %H:%M:%S') if card.added_time else None,
         "visibility": card.visibility,
         "preference": card.preference,
        "expiry_date" : card.expiry_date 
    } for card in cards]
    
    return jsonify(cards_list), 200


@card_bp.route('/cards/<int:c_id>/visibility', methods=['PATCH'])
def toggle_card_visibility(c_id):
    """Toggle the visibility of a card identified by c_id."""
    data = request.get_json()
    new_visibility = data.get("visibility")

    if new_visibility not in [True, False]:
        return jsonify({"message": "Invalid visibility value. Use True or False."}), 400

    card = Card.query.get(c_id)
    
    if not card:
        return jsonify({"message": "Card not found"}), 404

    card.visibility = new_visibility
    db.session.commit()

    return jsonify({
        "message": "Card visibility updated",
        "c_id": card.c_id,
        "new_visibility": card.visibility
    }), 200


@card_bp.route('/cards/grouped/<string:category>', methods=['GET'])
def get_grouped_cards_by_category(category):
    """Group cards by sub-category under a given category."""
    cards = Card.query.filter_by(c_category=category).all()

    if not cards:
        return jsonify({"message": "No cards found for this category"}), 404

    grouped_cards = {}
    for card in cards:
        sub_category = card.c_sub_category
        if sub_category not in grouped_cards:
            grouped_cards[sub_category] = []
        
        grouped_cards[sub_category].append({
            "c_id": card.c_id,
            "title": card.title,
            "caption": card.caption,
            "content": card.content,
            "date": card.date.strftime('%Y-%m-%d') if card.date else None,
            "location": card.location,
           "media_img_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_img_id, "image")) if card.media_img_id else None,
        "media_vid_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_vid_id, "video")) if card.media_vid_id else None,
        "media_doc_id": os.path.join(Config.MEDIA_BASE_URL, get_media_path(card.media_doc_id, "doc")) if card.media_doc_id else None,
            "updated_by": card.updated_by,
            "updated_time": card.updated_time.strftime('%Y-%m-%d %H:%M:%S') if card.updated_time else None,
            "added_by": card.added_by,
            "added_time": card.added_time.strftime('%Y-%m-%d %H:%M:%S') if card.added_time else None,
            "visibility": card.visibility,
            "preference": card.preference,
            "expiry_date" : card.expiry_date 
        })

    return jsonify(grouped_cards), 200


@card_bp.route('/cards/categories', methods=['GET'])
def get_unique_categories_subcategories():
    """Fetch unique categories with their associated sub-categories."""
    cards = Card.query.with_entities(Card.c_category, Card.c_sub_category).distinct().all()

    category_dict = {}
    for category, sub_category in cards:
        if category not in category_dict:
            category_dict[category] = set()
        category_dict[category].add(sub_category)

    # Convert sets to lists for JSON serialization
    result = {category: list(sub_categories) for category, sub_categories in category_dict.items()}

    return jsonify(result), 200


@card_bp.route('/cards/unique-categories', methods=['GET'])
def get_unique_categories():
    """Fetch only unique categories."""
    categories = db.session.query(Card.c_category).distinct().all()
    unique_categories = [category[0] for category in categories]
    
    return jsonify({"categories": unique_categories}), 200


@card_bp.route('/cards/unique-sub-categories', methods=['GET'])
def get_unique_sub_categories():
    """Fetch only unique sub-categories."""
    sub_categories = db.session.query(Card.c_sub_category).distinct().all()
    unique_sub_categories = [sub_category[0] for sub_category in sub_categories]
    
    return jsonify({"sub_categories": unique_sub_categories}), 200