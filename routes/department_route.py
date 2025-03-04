from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database.models import db
from sqlalchemy.exc import IntegrityError
from database.models import Department, db, Branch


department_bp = Blueprint("department", __name__)

@department_bp.route("/departments/", methods=["POST"])
def create_department():
    data = request.json
    dept_name = data.get("dept_name")

    if not dept_name:
        return jsonify({"error": "Department name is required"}), 400

    existing_department = Department.query.filter_by(dept_name=dept_name).first()
    if existing_department:
        return jsonify({"error": "Department already exists"}), 400

    new_department = Department(dept_name=dept_name)
    db.session.add(new_department)
    db.session.commit()

    return jsonify(new_department.to_dict()), 201


@department_bp.route("/departments/", methods=["GET"])
def get_departments():
    departments = Department.query.all()
    return jsonify([dept.to_dict() for dept in departments])


@department_bp.route("/departments/<int:d_id>", methods=["GET"])
def get_department(d_id):
    department = Department.query.get_or_404(d_id)
    return jsonify(department.to_dict())


@department_bp.route("/departments/<int:d_id>", methods=["PUT"])
def update_department(d_id):
    department = Department.query.get_or_404(d_id)
    data = request.json
    new_dept_name = data.get("dept_name")

    if not new_dept_name:
        return jsonify({"error": "Department name is required"}), 400

    department.dept_name = new_dept_name
    db.session.commit()

    return jsonify(department.to_dict())


@department_bp.route("/departments/<int:d_id>", methods=["DELETE"])
def delete_department(d_id):
    department = Department.query.get_or_404(d_id)
    db.session.delete(department)
    db.session.commit()

    return jsonify({"message": "Department deleted successfully"}), 200


@department_bp.route("/branches/", methods=["POST"])
def add_branch():
    data = request.json
    branch_name = data.get("branch_name")
    d_id = data.get("d_id")

    if not branch_name or not d_id:
        return jsonify({"error": "Branch name and department ID are required"}), 400

    department = Department.query.get(d_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404

    existing_branch = Branch.query.filter_by(branch_name=branch_name, d_id=d_id).first()
    if existing_branch:
        return jsonify({"error": "Branch already exists in this department"}), 400

    new_branch = Branch(branch_name=branch_name, d_id=d_id)
    db.session.add(new_branch)
    db.session.commit()

    return jsonify(new_branch.to_dict()), 201


@department_bp.route("/branches/", methods=["GET"])
def get_branches():
    branches = Branch.query.all()
    return jsonify([branch.to_dict() for branch in branches])


@department_bp.route("/branches/<int:b_id>", methods=["GET"])
def get_branch(b_id):
    branch = Branch.query.get_or_404(b_id)
    return jsonify(branch.to_dict())


@department_bp.route("/branches/<int:b_id>", methods=["DELETE"])
def delete_branch(b_id):
    branch = Branch.query.get_or_404(b_id)
    db.session.delete(branch)
    db.session.commit()

    return jsonify({"message": "Branch deleted successfully"}), 200

