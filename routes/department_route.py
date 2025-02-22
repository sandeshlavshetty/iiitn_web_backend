from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database.models import db
from sqlalchemy.exc import IntegrityError
from database.models import Department, db


department_bp = Blueprint("department", __name__)

# Department Routes
@department_bp.route("/", methods=["GET"])
def get_departments():
    departments = Department.query.all()
    return jsonify([{ "d_id": d.d_id, "dept_name": d.dept_name, "branch_name": d.branch_name } for d in departments])

@department_bp.route("/", methods=["POST"])
def create_department():
    data = request.json
    new_department = Department(dept_name=data["dept_name"], branch_name=data["branch_name"])
    db.session.add(new_department)
    db.session.commit()
    return jsonify({"message": "Department created successfully"}), 201

@department_bp.route("/departments/<int:d_id>", methods=["PUT"])
def update_department(d_id):
    data = request.json
    department = Department.query.get(d_id)
    if not department:
        return jsonify({"message": "Department not found"}), 404
    
    department.dept_name = data.get("dept_name", department.dept_name)
    department.branch_name = data.get("branch_name", department.branch_name)
    db.session.commit()
    
    return jsonify({"message": "Department updated successfully"}), 200

@department_bp.route("/departments/<int:d_id>", methods=["DELETE"])
def delete_department(d_id):
    department = Department.query.get(d_id)
    if not department:
        return jsonify({"message": "Department not found"}), 404

    db.session.delete(department)
    db.session.commit()
    return jsonify({"message": "Department deleted successfully"}), 200