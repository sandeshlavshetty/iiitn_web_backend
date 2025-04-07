from flask import Blueprint, jsonify, request
from database.models import FacultyStaff, db, Person, Branch, MediaImageCard , Department
from config import Config
import os

faculty_bp = Blueprint("faculty", __name__)
 
@faculty_bp.route("/", methods=["GET"])
def get_facultys():
    return jsonify({"message": "Faculty routes working!"})


@faculty_bp.route("/faculty_staff", methods=["GET"])
def get_faculty_staff():
    faculty_staff = (
        db.session.query(FacultyStaff, Person, Department, MediaImageCard)
        .join(Person, FacultyStaff.p_id == Person.p_id)
        .join(Department, FacultyStaff.d_id == Department.d_id)
        .outerjoin(MediaImageCard, FacultyStaff.media_img_id == MediaImageCard.media_img_id)  # Outer join to handle null images
        .all()
    )

    result = [
        {
            "f_id": faculty.f_id,
            "p_id": person.p_id,
            "name": person.name,
            "email": person.email_pri,
            "phone_no": person.phone_no,
            "join_year": faculty.join_year,
            "positions": faculty.positions,
            "f_or_s": faculty.f_or_s,
            "education": faculty.education,
            "experience": faculty.experience,
            "teaching": faculty.teaching,
            "research": faculty.research,
            "d_id": department.d_id,
            "dept_name": department.dept_name,
            "content": faculty.content,
            "preference": faculty.preference,
            "image_path": os.path.join(Config.MEDIA_BASE_URL,media.image_path) if media.image_path else None
        }
        for faculty, person, department, media in faculty_staff
    ]

    return jsonify(result)

@faculty_bp.route("/faculty_staff/<int:f_id>", methods=["GET"])
def get_faculty_by_id(f_id):
    faculty_staff = (
        db.session.query(FacultyStaff, Person, Department, MediaImageCard)
        .join(Person, FacultyStaff.p_id == Person.p_id)
        .join(Department, FacultyStaff.d_id == Department.d_id)
        .outerjoin(MediaImageCard, FacultyStaff.media_img_id == MediaImageCard.media_img_id)
        .filter(FacultyStaff.f_id == f_id)
        .first()
    )

    if not faculty_staff:
        return jsonify({"message": "Faculty/Staff not found"}), 404

    faculty, person, department, media = faculty_staff

    return jsonify({
        "f_id": faculty.f_id,
        "p_id": person.p_id,
        "name": person.name,
        "email": person.email_pri,
        "phone_no": person.phone_no,
        "join_year": faculty.join_year,
        "positions": faculty.positions,
        "f_or_s": faculty.f_or_s,
        "education": faculty.education,
        "experience": faculty.experience,
        "teaching": faculty.teaching,
        "research": faculty.research,
        "d_id": department.d_id,
    "dept_name": department.dept_name,
        "content": faculty.content,
        "preference": faculty.preference,
        "image_path": os.path.join(Config.MEDIA_BASE_URL,media.image_path) if media.image_path else None
    }), 200

@faculty_bp.route("/faculty_staff", methods=["POST"])
def create_faculty_staff():
    data = request.json
    new_faculty_staff = FacultyStaff(
        p_id=data["p_id"],
        join_year=data["join_year"],
        media_img_id=data.get("media_img_id"),
        d_id=data["d_id"],  # CHANGED from b_id to d_id
        positions=data["positions"],
        f_or_s=data["f_or_s"],
        education=data.get("education"),
        experience=data.get("experience"),
        teaching=data.get("teaching"),
        research=data.get("research"),
        content = data.get("content"),
        preference = data.get("preference")
    )

    db.session.add(new_faculty_staff)
    db.session.commit()
    return jsonify({"message": "Faculty/Staff created successfully"}), 201

@faculty_bp.route("/faculty_staff/<int:f_id>", methods=["PUT"])
def update_faculty_staff(f_id):
    data = request.json
    faculty_staff = FacultyStaff.query.get(f_id)

    if not faculty_staff:
        return jsonify({"message": "Faculty/Staff not found"}), 404

    faculty_staff.p_id = data.get("p_id", faculty_staff.p_id)
    faculty_staff.join_year = data.get("join_year", faculty_staff.join_year)
    faculty_staff.media_img_id = data.get("media_img_id", faculty_staff.media_img_id)
    faculty_staff.d_id = data.get("d_id", faculty_staff.d_id)  # CHANGED from b_id
    faculty_staff.positions = data.get("positions", faculty_staff.positions)
    faculty_staff.f_or_s = data.get("f_or_s", faculty_staff.f_or_s)
    faculty_staff.education = data.get("education", faculty_staff.education)
    faculty_staff.experience = data.get("experience", faculty_staff.experience)
    faculty_staff.teaching = data.get("teaching", faculty_staff.teaching)
    faculty_staff.research = data.get("research", faculty_staff.research)
    faculty_staff.preference = data.get("preference", faculty_staff.preference)

    db.session.commit()
    return jsonify({"message": "Faculty/Staff updated successfully"}), 200

@faculty_bp.route("/faculty_staff/<int:f_id>", methods=["DELETE"])
def delete_faculty_staff(f_id):
    faculty_staff = FacultyStaff.query.get(f_id)

    if not faculty_staff:
        return jsonify({"message": "Faculty/Staff not found"}), 404

    db.session.delete(faculty_staff)
    db.session.commit()
    return jsonify({"message": "Faculty/Staff deleted successfully"}), 200

@faculty_bp.route("/faculty_staff/<int:f_id>", methods=["PATCH"])
def patch_faculty_staff(f_id):
    data = request.json
    faculty_staff = FacultyStaff.query.get(f_id)

    if not faculty_staff:
        return jsonify({"message": "Faculty/Staff not found"}), 404

    # Update only the fields present in the request
    for key, value in data.items():
        if hasattr(faculty_staff, key):
            setattr(faculty_staff, key, value)

    db.session.commit()
    return jsonify({"message": "Faculty/Staff updated successfully"}), 200

@faculty_bp.route("/faculty_staff/default", methods=["PATCH"])
def create_default_faculty_staff():
    data = request.json

    # Create a new FacultyStaff entry with required fields and others set to None
    new_faculty_staff = FacultyStaff(
        p_id=data.get("p_id"),  # Required as it's unique and foreign key
        join_year=data.get("join_year", 2024),  # Default join year if not provided
        media_img_id=None,
        d_id=data.get("d_id"),  # CHANGED from b_id to d_id
        positions=data.get("positions", ""),  # Default to empty string
        f_or_s=data.get("f_or_s", "Faculty"),  # Defaulting to "Faculty"
        education=None,
        experience=None,
        teaching=None,
        research=None,
        content=None,
        preference=data.get("preference", 0)  # Default priority
    )

    db.session.add(new_faculty_staff)
    db.session.commit()

    return jsonify({
        "message": "Faculty/Staff created successfully",
        "faculty_staff": new_faculty_staff.to_dict()
    }), 201



