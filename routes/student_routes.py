from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database.models import db,  Person
from sqlalchemy.exc import IntegrityError


student_bp = Blueprint("student", __name__)

@student_bp.route("/", methods=["GET"])
@jwt_required()
def student_routes_root():
    return jsonify({"message": "student routes working!"})



# # 🆕 Create a Student
# @student_bp.route("/student", methods=["POST"])
# def add_student():
#     data = request.json

#     if not all(k in data for k in ("S_id", "P_id", "Join_year", "D_id")):
#         return jsonify({"error": "Missing required fields"}), 400

#     student = Student(
#         S_id=data["S_id"],
#         P_id=data["P_id"],
#         Join_year=data["Join_year"],
#         media_img_id=data.get("media_img_id"),  # Optional
#         D_id=data["D_id"]
#     )

#     try:
#         db.session.add(student)
#         db.session.commit()
#         return jsonify({"message": "Student added successfully", "student": student.to_dict()}), 201
#     except IntegrityError:
#         db.session.rollback()
#         return jsonify({"error": "Student with this ID or P_id already exists"}), 400

# # 📥 Get All Students
# @student_bp.route("/student", methods=["GET"])
# def get_students():
#     students = Student.query.all()
#     return jsonify([student.to_dict() for student in students]), 200

# # 📥 Get Student by S_id
# @student_bp.route("/student/<string:S_id>", methods=["GET"])
# def get_student(S_id):
#     student = Student.query.get(S_id)
#     if not student:
#         return jsonify({"error": "Student not found"}), 404
#     return jsonify(student.to_dict()), 200

# # ✏️ Update Student
# @student_bp.route("/student/<string:S_id>", methods=["PUT"])
# def update_student(S_id):
#     student = Student.query.get(S_id)
#     if not student:
#         return jsonify({"error": "Student not found"}), 404

#     data = request.json
#     student.P_id = data.get("P_id", student.P_id)
#     student.Join_year = data.get("Join_year", student.Join_year)
#     student.media_img_id = data.get("media_img_id", student.media_img_id)
#     student.D_id = data.get("D_id", student.D_id)

#     db.session.commit()
#     return jsonify({"message": "Student updated successfully", "student": student.to_dict()}), 200

# # ❌ Delete Student
# @student_bp.route("/student/<string:S_id>", methods=["DELETE"])
# def delete_student(S_id):
#     student = Student.query.get(S_id)
#     if not student:
#         return jsonify({"error": "Student not found"}), 404

#     db.session.delete(student)
#     db.session.commit()
#     return jsonify({"message": "Student deleted successfully"}), 200

