"""Departments API endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Department, Petition, User

departments = Blueprint("departments", __name__)


@departments.route("/list", methods=["GET"])
def list_departments():
    """List all departments (public endpoint)"""
    try:
        depts = Department.query.all()
        
        result = [
            {
                "id": d.id,
                "name": d.name,
                "description": d.description,
                "email": d.email
            }
            for d in depts
        ]
        
        return jsonify({"departments": result}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@departments.route("/<int:dept_id>/petitions", methods=["GET"])
@jwt_required()
def get_department_petitions(dept_id):
    """Get all petitions for a specific department"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        # Only officers and admins can view department petitions
        if user.role not in ["officer", "admin"]:
            return jsonify({"error": "Unauthorized"}), 403
        
        department = Department.query.get(dept_id)
        if not department:
            return jsonify({"error": "Department not found"}), 404
        
        # Get petitions for this department
        petitions = Petition.query.filter_by(department_id=dept_id)\
            .order_by(Petition.created_at.desc()).all()
        
        result = [
            {
                "id": p.id,
                "petition_id": p.petition_id,
                "title": p.title,
                "priority": p.priority,
                "urgency_level": p.urgency_level,
                "status": p.status,
                "created_at": p.created_at.isoformat(),
                "user": {
                    "name": p.user.name,
                    "email": p.user.email
                }
            }
            for p in petitions
        ]
        
        return jsonify({
            "department": department.name,
            "petitions": result,
            "count": len(result)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@departments.route("/create", methods=["POST"])
@jwt_required()
def create_department():
    """Create a new department (admin only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return jsonify({"error": "Unauthorized. Admin access required"}), 403
        
        data = request.json
        name = data.get("name")
        description = data.get("description", "")
        email = data.get("email", "")
        
        if not name:
            return jsonify({"error": "Department name is required"}), 400
        
        # Check if department already exists
        existing = Department.query.filter_by(name=name).first()
        if existing:
            return jsonify({"error": "Department already exists"}), 400
        
        department = Department(
            name=name,
            description=description,
            email=email
        )
        
        db.session.add(department)
        db.session.commit()
        
        return jsonify({
            "message": "Department created successfully",
            "department": {
                "id": department.id,
                "name": department.name
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
