from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from database.db_operations import add_person, get_person, get_all_persons, update_person, delete_person


user_bp = Blueprint("user", __name__)

# @user_bp.route("/", methods=["GET"])
# # @jwt_required()  #middleware
# def get_users():
#     return jsonify({"message": "User routes working!"})

@user_bp.route("/", methods=["GET"])
def fetch_all_persons():
    persons = get_all_persons()
    return jsonify([
        {
            "p_id": p.p_id,
            "email_pri": p.email_pri,
            "email_sec": p.email_sec,
            "name": p.name,
            "phone_no": p.phone_no,
            "alt_phone_no": p.alt_phone_no,
            "curr_address": p.curr_address,
            "perm_address": p.perm_address,
            "role": p.role,
            "sm_id": p.sm_id
        } for p in persons
    ])

@user_bp.route("/<int:p_id>", methods=["GET"])
def fetch_person(p_id):
    p = get_person(p_id)
    if not p:
        return jsonify({"error": "Person not found"}), 404

    return jsonify({
        "p_id": p.p_id,
        "email_pri": p.email_pri,
        "email_sec": p.email_sec,
        "name": p.name,
        "phone_no": p.phone_no,
        "alt_phone_no": p.alt_phone_no,
        "curr_address": p.curr_address,
        "perm_address": p.perm_address,
        "role": p.role,
        "sm_id": p.sm_id
    })

@user_bp.route("/", methods=["POST"])
def create_person():
    data = request.json
    required_fields = ["email_pri", "name", "phone_no", "password", "role"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    person = add_person(
        email_pri=data["email_pri"],
        email_sec=data.get("email_sec"),
        name=data["name"],
        phone_no=data["phone_no"],
        alt_phone_no=data.get("alt_phone_no"),
        curr_address=data.get("curr_address"),
        perm_address=data.get("perm_address"),
        password=data["password"],
        role=data["role"],
        sm_id=data.get("sm_id")
    )

    return jsonify({"message": "Person added", "p_id": person.p_id})

@user_bp.route("/<int:p_id>", methods=["PUT"])
def modify_person(p_id):
    data = request.json
    person = update_person(p_id, **data)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    return jsonify({"message": "Person updated", "p_id": person.p_id})

@user_bp.route("/<int:p_id>", methods=["DELETE"])
def remove_person(p_id):
    if delete_person(p_id):
        return jsonify({"message": "Person deleted"})
    return jsonify({"error": "Person not found"}), 404
