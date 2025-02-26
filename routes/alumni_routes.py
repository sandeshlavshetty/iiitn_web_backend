from flask import Blueprint, request, jsonify
from database import db
from database.models import Alumni, Student, Person

alumni_bp = Blueprint('alumni', __name__)

# Create a new alumni record
@alumni_bp.route('/alumni', methods=['POST'])
def create_alumni():
    data = request.get_json()
    s_id = data.get('s_id')
    curr_org = data.get('curr_org')
    brief = data.get('brief')

    student = Student.query.get(s_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    alumni = Alumni(s_id=s_id, curr_org=curr_org, brief=brief)
    db.session.add(alumni)
    db.session.commit()

    return jsonify({"message": "Alumni record created successfully"}), 201

# Get all alumni records
@alumni_bp.route('/alumni', methods=['GET'])
def get_all_alumni():
    alumni_list = Alumni.query.all()
    return jsonify([{"s_id": a.s_id, "curr_org": a.curr_org, "brief": a.brief} for a in alumni_list])

# Get a single alumni record by student ID
@alumni_bp.route('/alumni/<s_id>', methods=['GET'])
def get_alumni(s_id):
    alumni = Alumni.query.get(s_id)
    if not alumni:
        return jsonify({"error": "Alumni record not found"}), 404

    return jsonify({"s_id": alumni.s_id, "curr_org": alumni.curr_org, "brief": alumni.brief})

# Update an alumni record
@alumni_bp.route('/alumni/<s_id>', methods=['PUT'])
def update_alumni(s_id):
    alumni = Alumni.query.get(s_id)
    if not alumni:
        return jsonify({"error": "Alumni record not found"}), 404

    data = request.get_json()
    alumni.curr_org = data.get('curr_org', alumni.curr_org)
    alumni.brief = data.get('brief', alumni.brief)
    
    db.session.commit()
    return jsonify({"message": "Alumni record updated successfully"})

# Delete an alumni record
@alumni_bp.route('/alumni/<s_id>', methods=['DELETE'])
def delete_alumni(s_id):
    alumni = Alumni.query.get(s_id)
    if not alumni:
        return jsonify({"error": "Alumni record not found"}), 404

    db.session.delete(alumni)
    db.session.commit()
    return jsonify({"message": "Alumni record deleted successfully"})

# Register the blueprint in your Flask app (app.py)
# app.register_blueprint(alumni_bp, url_prefix='/api')

@alumni_bp.route('/alumni/details/<s_id>', methods=['GET'])
def get_alumni_details(s_id):
    alumni = Alumni.query.join(Student).join(Person).filter(Alumni.s_id == s_id).first()

    if not alumni:
        return jsonify({"error": "Alumni record not found"}), 404

    student = alumni.student
    person = student.person

    response = {
        "s_id": alumni.s_id,
        "curr_org": alumni.curr_org,
        "brief": alumni.brief,
        "name": person.name,
        "email_pri": person.email_pri,
        "email_sec": person.email_sec,
        "phone_no": person.phone_no,
        "alt_phone_no": person.alt_phone_no,
        "curr_address": person.curr_address,
        "perm_address": person.perm_address,
        "join_year": student.join_year,
    }

    return jsonify(response)
