"""Petitions API endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Petition, PetitionStatus, User, Department
from app.services import PetitionProcessor, NotificationService
from datetime import datetime
import os
from werkzeug.utils import secure_filename

petitions = Blueprint("petitions", __name__)

# Initialize petition processor
processor = PetitionProcessor()

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@petitions.route("/submit", methods=["POST"])
@jwt_required()
def submit_petition():
    """Submit a new petition with AI processing"""
    try:
        user_id = int(get_jwt_identity())
        
        # Get form data
        title = request.form.get("title")
        description = request.form.get("description")
        
        if not title or not description:
            return jsonify({"error": "Title and description are required"}), 400
        
        # Process petition through AI/NLP pipeline
        ai_analysis = processor.process_petition(title, description)
        
        # Get department ID
        department_id = processor.get_department_id(ai_analysis["classification"]["category"], db.session)
        
        # Generate unique petition ID
        petition_id = processor.generate_petition_id()
        
        # Handle file upload if present
        attachment_path = None
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create uploads directory if it doesn't exist
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filepath = os.path.join(UPLOAD_FOLDER, f"{petition_id}_{filename}")
                file.save(filepath)
                attachment_path = filepath
        
        # Create petition record
        petition = Petition(
            petition_id=petition_id,
            user_id=user_id,
            title=title,
            description=description,
            category=ai_analysis["classification"]["category"],
            department_id=department_id,
            priority=ai_analysis["priority"]["level"],
            sentiment_score=ai_analysis["sentiment"]["compound"],
            urgency_level=ai_analysis["urgency"]["level"],
            status="submitted",
            attachment_path=attachment_path
        )
        
        db.session.add(petition)
        db.session.commit()
        
        # Create initial status entry
        status_entry = PetitionStatus(
            petition_id=petition.id,
            status="submitted",
            comment="Petition submitted and processed by AI",
            updated_by=user_id
        )
        db.session.add(status_entry)
        db.session.commit()
        
        # Send notification
        NotificationService.notify_petition_submitted(user_id, petition.id, title)
        
        return jsonify({
            "message": "Petition submitted successfully",
            "petition_id": petition_id,
            "ai_analysis": {
                "category": ai_analysis["classification"]["category"],
                "confidence": ai_analysis["classification"]["confidence"],
                "priority": ai_analysis["priority"]["level"],
                "urgency": ai_analysis["urgency"]["level"],
                "sentiment": ai_analysis["sentiment"]["polarity"],
                "keywords": ai_analysis["keywords"]
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@petitions.route("/list", methods=["GET"])
@jwt_required()
def list_petitions():
    """List petitions with filters"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        # Build query
        query = Petition.query
        
        # Filter by user for citizens
        if user.role == "citizen":
            query = query.filter_by(user_id=user_id)
        
        # Apply filters
        status_filter = request.args.get("status")
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        priority_filter = request.args.get("priority")
        if priority_filter:
            query = query.filter_by(priority=priority_filter)
        
        department_filter = request.args.get("department")
        if department_filter:
            dept = Department.query.filter_by(name=department_filter).first()
            if dept:
                query = query.filter_by(department_id=dept.id)
        
        # Order by created date
        petitions_list = query.order_by(Petition.created_at.desc()).all()
        
        # Format response
        result = []
        for p in petitions_list:
            result.append({
                "id": p.id,
                "petition_id": p.petition_id,
                "title": p.title,
                "description": p.description[:200] + "..." if len(p.description) > 200 else p.description,
                "category": p.category,
                "department": p.department.name if p.department else None,
                "priority": p.priority,
                "urgency_level": p.urgency_level,
                "status": p.status,
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat()
            })
        
        return jsonify({"petitions": result, "count": len(result)}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@petitions.route("/<int:petition_id>", methods=["GET"])
@jwt_required()
def get_petition(petition_id):
    """Get detailed petition information"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        petition = Petition.query.get(petition_id)
        if not petition:
            return jsonify({"error": "Petition not found"}), 404
        
        # Check access rights
        if user.role == "citizen" and petition.user_id != user_id:
            return jsonify({"error": "Unauthorized access"}), 403
        
        # Get status history
        status_history = PetitionStatus.query.filter_by(petition_id=petition.id)\
            .order_by(PetitionStatus.timestamp.desc()).all()
        
        return jsonify({
            "petition": {
                "id": petition.id,
                "petition_id": petition.petition_id,
                "title": petition.title,
                "description": petition.description,
                "category": petition.category,
                "department": petition.department.name if petition.department else None,
                "priority": petition.priority,
                "urgency_level": petition.urgency_level,
                "sentiment_score": petition.sentiment_score,
                "status": petition.status,
                "created_at": petition.created_at.isoformat(),
                "updated_at": petition.updated_at.isoformat(),
                "resolved_at": petition.resolved_at.isoformat() if petition.resolved_at else None,
                "resolution_comment": petition.resolution_comment,
                "attachment_path": petition.attachment_path,
                "user": {
                    "name": petition.user.name,
                    "email": petition.user.email
                }
            },
            "status_history": [
                {
                    "status": s.status,
                    "comment": s.comment,
                    "timestamp": s.timestamp.isoformat(),
                    "updated_by": s.updater.name if s.updater else "System"
                }
                for s in status_history
            ]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@petitions.route("/<int:petition_id>/status", methods=["PUT"])
@jwt_required()
def update_status(petition_id):
    """Update petition status (officers/admin only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        # Check if user is officer or admin
        if user.role not in ["officer", "admin"]:
            return jsonify({"error": "Unauthorized. Only officers can update status"}), 403
        
        petition = Petition.query.get(petition_id)
        if not petition:
            return jsonify({"error": "Petition not found"}), 404
        
        data = request.json
        new_status = data.get("status")
        comment = data.get("comment", "")
        
        if not new_status:
            return jsonify({"error": "Status is required"}), 400
        
        # Update petition status
        petition.status = new_status
        petition.updated_at = datetime.utcnow()
        
        # If resolved, set resolved_at and resolution_comment
        if new_status == "resolved":
            petition.resolved_at = datetime.utcnow()
            petition.resolution_comment = comment
        
        # Create status history entry
        status_entry = PetitionStatus(
            petition_id=petition.id,
            status=new_status,
            comment=comment,
            updated_by=user_id
        )
        db.session.add(status_entry)
        db.session.commit()
        
        # Send notification to user
        if new_status == "resolved":
            NotificationService.notify_resolution(petition.user_id, petition.id, comment)
        else:
            NotificationService.notify_status_update(petition.user_id, petition.id, new_status, comment)
        
        return jsonify({
            "message": "Status updated successfully",
            "petition_id": petition.petition_id,
            "new_status": new_status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@petitions.route("/track/<petition_id_str>", methods=["GET"])
def track_petition(petition_id_str):
    """Track petition by petition ID (public endpoint)"""
    try:
        petition = Petition.query.filter_by(petition_id=petition_id_str).first()
        if not petition:
            return jsonify({"error": "Petition not found"}), 404
        
        # Get status history
        status_history = PetitionStatus.query.filter_by(petition_id=petition.id)\
            .order_by(PetitionStatus.timestamp.asc()).all()
        
        return jsonify({
            "petition_id": petition.petition_id,
            "title": petition.title,
            "category": petition.category,
            "department": petition.department.name if petition.department else None,
            "priority": petition.priority,
            "status": petition.status,
            "created_at": petition.created_at.isoformat(),
            "status_timeline": [
                {
                    "status": s.status,
                    "comment": s.comment,
                    "timestamp": s.timestamp.isoformat()
                }
                for s in status_history
            ]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
