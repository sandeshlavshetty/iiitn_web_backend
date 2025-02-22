from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database.models import db
from sqlalchemy.exc import IntegrityError
from database.models import Student, db

student_bp = Blueprint("student", __name__)

@student_bp.route("/", methods=["GET"])
# @jwt_required()
def student_routes_root():
    return jsonify({"message": "student routes working!"})



@student_bp.route("/students", methods=["GET"])   # end_c
def get_students():
    students = Student.query.all()
    return jsonify([{ "s_id": s.s_id, "p_id": s.p_id, "join_year": s.join_year, "d_id": s.d_id } for s in students])

@student_bp.route("/students", methods=["POST"])
def create_student():
    data = request.json
    new_student = Student(
        s_id=data["s_id"],
        p_id=data["p_id"],
        join_year=data["join_year"],
        media_img_id=data.get("media_img_id"),
        d_id=data["d_id"]
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student created successfully"}), 201


@student_bp.route("/students/<string:s_id>", methods=["PUT"])
def update_student(s_id):
    data = request.json
    student = Student.query.get(s_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    
    student.p_id = data.get("p_id", student.p_id)
    student.join_year = data.get("join_year", student.join_year)
    student.media_img_id = data.get("media_img_id", student.media_img_id)
    student.d_id = data.get("d_id", student.d_id)
    
    db.session.commit()
    return jsonify({"message": "Student updated successfully"}), 200


@student_bp.route("/students/<string:s_id>", methods=["DELETE"])
def delete_student(s_id):
    student = Student.query.get(s_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"}), 200