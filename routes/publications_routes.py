from flask import Blueprint, request, jsonify
from database import db
from database.models import Publication
from sqlalchemy.exc import SQLAlchemyError

publication_bp = Blueprint("publication",__name__)

@publication_bp.route("/", methods=["POST"])
def create_publication():
    try:
        data = request.json
        new_pub = Publication(
            title=data["title"],
            content=data["content"],
            link=data.get("link"),  # Optional
            status=data["status"],
            type=data["type"],
            branch=data["branch"]   # New Attribute
        )

        db.session.add(new_pub)
        db.session.commit()
        return jsonify({"message": "Publication created successfully!", "id": new_pub.pub_id}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Read All Publications
@publication_bp.route("/", methods=["GET"])
def get_publications():
    publications = Publication.query.all()
    result = [{
        "pub_id": pub.pub_id,
        "title": pub.title,
        "content": pub.content,
        "link": pub.link,
        "status": pub.status,
        "type": pub.type
    } for pub in publications]
    
    return jsonify(result), 200

# Read Single Publication by ID
@publication_bp.route("/<int:pub_id>", methods=["GET"])
def get_publication(pub_id):
    pub = Publication.query.get(pub_id)
    if not pub:
        return jsonify({"error": "Publication not found"}), 404

    result = {
        "pub_id": pub.pub_id,
        "title": pub.title,
        "content": pub.content,
        "link": pub.link,
        "status": pub.status,
        "type": pub.type
    }
    return jsonify(result), 200

# Update Publication
@publication_bp.route("/<int:pub_id>", methods=["PUT"])
def update_publication(pub_id):
    pub = Publication.query.get(pub_id)
    if not pub:
        return jsonify({"error": "Publication not found"}), 404

    data = request.json
    pub.title = data.get("title", pub.title)
    pub.content = data.get("content", pub.content)
    pub.link = data.get("link", pub.link)
    pub.status = data.get("status", pub.status)
    pub.type = data.get("type", pub.type)

    try:
        db.session.commit()
        return jsonify({"message": "Publication updated successfully!"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete Publication
@publication_bp.route("/<int:pub_id>", methods=["DELETE"])
def delete_publication(pub_id):
    pub = Publication.query.get(pub_id)
    if not pub:
        return jsonify({"error": "Publication not found"}), 404

    try:
        db.session.delete(pub)
        db.session.commit()
        return jsonify({"message": "Publication deleted successfully!"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500