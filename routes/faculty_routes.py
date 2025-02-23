from flask import Blueprint, jsonify, request
from database.models import FacultyStaff, db

# from flask_jwt_extended import jwt_required


# faculty_bp = Blueprint(" ", __name__)

# @faculty_bp.route("/", methods=["GET"])
# # @jwt_required()
# def get_facultys():
#     return jsonify({"message": "faculty routes working!"})



# # Faculty & Staff Routes
# @faculty_bp.route("/faculty_staff", methods=["GET"])  #endp checked
# def get_faculty_staff():
#     faculty_staff = FacultyStaff.query.all()
#     return jsonify([{ "f_id": f.f_id, "p_id": f.p_id, "join_year": f.join_year, "positions": f.positions, "f_or_s": f.f_or_s } for f in faculty_staff])

# @faculty_bp.route("/faculty_staff", methods=["POST"])     #endp checked
# def create_faculty_staff():
#     data = request.json
#     new_faculty_staff = FacultyStaff(
#         p_id=data["p_id"],
#         join_year=data["join_year"],
#         media_img_id=data.get("media_img_id"),
#         d_id=data["d_id"],
#         positions=data["positions"],
#         f_or_s=data["f_or_s"]
#     )
#     db.session.add(new_faculty_staff)
#     db.session.commit()
#     return jsonify({"message": "Faculty/Staff created successfully"}), 20


# @faculty_bp.route("/faculty_staff/<int:f_id>", methods=["PUT"])
# def update_faculty_staff(f_id):
#     data = request.json
#     faculty_staff = FacultyStaff.query.get(f_id)
#     if not faculty_staff:
#         return jsonify({"message": "Faculty/Staff not found"}), 404
    
#     faculty_staff.p_id = data.get("p_id", faculty_staff.p_id)
#     faculty_staff.join_year = data.get("join_year", faculty_staff.join_year)
#     faculty_staff.media_img_id = data.get("media_img_id", faculty_staff.media_img_id)
#     faculty_staff.d_id = data.get("d_id", faculty_staff.d_id)
#     faculty_staff.positions = data.get("positions", faculty_staff.positions)
#     faculty_staff.f_or_s = data.get("f_or_s", faculty_staff.f_or_s)
    
#     db.session.commit()
#     return jsonify({"message": "Faculty/Staff updated successfully"}), 200

# @faculty_bp.route("/faculty_staff/<int:f_id>", methods=["DELETE"])
# def delete_faculty_staff(f_id):
#     faculty_staff = FacultyStaff.query.get(f_id)
#     if not faculty_staff:
#         return jsonify({"message": "Faculty/Staff not found"}), 404

#     db.session.delete(faculty_staff)
#     db.session.commit()
#     return jsonify({"message": "Faculty/Staff deleted successfully"}), 200



from flask import Blueprint, jsonify, request
from database.models import FacultyStaff, db

faculty_bp = Blueprint("faculty", __name__)

@faculty_bp.route("/", methods=["GET"])
def get_facultys():
    return jsonify({"message": "Faculty routes working!"})

@faculty_bp.route("/faculty_staff", methods=["GET"])  
def get_faculty_staff():
    faculty_staff = FacultyStaff.query.all()
    return jsonify([f.to_dict() for f in faculty_staff])

@faculty_bp.route("/faculty_staff/<int:f_id>", methods=["GET"])  
def get_faculty_by_id(f_id):
    faculty_staff = FacultyStaff.query.get(f_id)
    if not faculty_staff:
        return jsonify({"message": "Faculty/Staff not found"}), 404
    return jsonify(faculty_staff.to_dict()), 200

@faculty_bp.route("/faculty_staff", methods=["POST"])     
def create_faculty_staff():
    data = request.json
    new_faculty_staff = FacultyStaff(
        p_id=data["p_id"],
        join_year=data["join_year"],
        media_img_id=data.get("media_img_id"),
        d_id=data["d_id"],
        positions=data["positions"],
        f_or_s=data["f_or_s"],
        education=data.get("education"),
        experience=data.get("experience"),
        teaching=data.get("teaching"),
        research=data.get("research"),
        pub_id=data.get("pub_id")
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
    faculty_staff.d_id = data.get("d_id", faculty_staff.d_id)
    faculty_staff.positions = data.get("positions", faculty_staff.positions)
    faculty_staff.f_or_s = data.get("f_or_s", faculty_staff.f_or_s)
    faculty_staff.education = data.get("education", faculty_staff.education)
    faculty_staff.experience = data.get("experience", faculty_staff.experience)
    faculty_staff.teaching = data.get("teaching", faculty_staff.teaching)
    faculty_staff.research = data.get("research", faculty_staff.research)
    faculty_staff.pub_id = data.get("pub_id", faculty_staff.pub_id)

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
