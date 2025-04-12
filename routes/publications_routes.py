from flask import Blueprint, request, jsonify
from database import db
from database.models import Publication
from sqlalchemy.exc import SQLAlchemyError

publication_bp = Blueprint("publication",__name__)

# Allowed ENUM values for validation
VALID_TYPES = {"publication", "project", "consultancy"}
VALID_BRANCHES = {"CSE", "ECE", "BS"}
VALID_STATUSES = {"ongoing", "completed", "proposed"}

# Create Publication Route
@publication_bp.route("/", methods=["POST"])
def create_publication():
    try:
        data = request.json

        # Validate ENUM type
        if data["type"] not in VALID_TYPES:
            return jsonify({"error": f"Invalid type: {data['type']}. Allowed: {list(VALID_TYPES)}"}), 400
        
        if data["branch_enum"] not in VALID_BRANCHES:
            return jsonify({"error": f"Invalid branch_enum: {data['branch_enum']}. Allowed: {list(VALID_BRANCHES)}"}), 400

        if not isinstance(data.get("pub_year"), int):
            return jsonify({"error": "Invalid or missing pub_year (must be integer)"}), 400
        
        if data["status"] not in VALID_STATUSES:
            return jsonify({"error": f"Invalid status: {data['status']}. Allowed: {list(VALID_STATUSES)}"}), 400
        
        new_pub = Publication(
            title=data["title"],
            content=data["content"],
            link=data.get("link"),  # Optional
            status=data["status"],
            type=data["type"],  # Storing as string directly
            branch_enum=data["branch_enum"],  # ENUM handling
            pub_year=data["pub_year"],
            lead_name=data.get("lead_name"),  # ✅ Optional
            published_in=data.get("published_in")  # ✅ Optional
        )

        db.session.add(new_pub)
        db.session.commit()
        return jsonify({"message": "Publication created successfully!", "id": new_pub.pub_id}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# Get All Publications Route
@publication_bp.route("/", methods=["GET"])
def get_publications():
    publications = Publication.query.all()
    result = [pub.to_dict() for pub in publications]
    return jsonify(result), 200




# Get Single Publication by ID
@publication_bp.route("/<int:pub_id>", methods=["GET"])
def get_publication(pub_id):
    pub = Publication.query.get(pub_id)
    if not pub:
        return jsonify({"error": "Publication not found"}), 404

    return jsonify(pub.to_dict()), 200

# Update Publication Route
@publication_bp.route("/<int:pub_id>", methods=["PATCH"])
def update_publication(pub_id):
    pub = Publication.query.get(pub_id)
    if not pub:
        return jsonify({"error": "Publication not found"}), 404

    data = request.json

    # Validate ENUM type if provided
    if "type" in data and data["type"] not in VALID_TYPES:
        return jsonify({"error": f"Invalid type: {data['type']}. Allowed: {list(VALID_TYPES)}"}), 400

    if "branch_enum" in data and data["branch_enum"] not in VALID_BRANCHES:
        return jsonify({"error": f"Invalid branch_enum: {data['branch_enum']}. Allowed: {list(VALID_BRANCHES)}"}), 400
    if "status" in data and data["status"] not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status: {data['status']}. Allowed: {list(VALID_STATUSES)}"}), 400

    pub.title = data.get("title", pub.title)
    pub.content = data.get("content", pub.content)
    pub.link = data.get("link", pub.link)
    pub.status = data.get("status", pub.status)
    pub.type = data.get("type", pub.type)  # Storing as string directly
    pub.branch_enum = data.get("branch_enum", pub.branch_enum)  # ENUM handling
    pub.pub_year = data.get("pub_year", pub.pub_year)
    pub.lead_name = data.get("lead_name", pub.lead_name)  # ✅ Optional
    pub.published_in = data.get("published_in", pub.published_in)  # ✅ Optional

    try:
        db.session.commit()
        return jsonify({"message": "Publication updated successfully!"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete Publication Route
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
