"""Analytics API endpoints"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Petition, Department, User
from app.extensions import db
from sqlalchemy import func
from datetime import datetime, timedelta

analytics = Blueprint("analytics", __name__)


@analytics.route("/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard_stats():
    """Get overall dashboard statistics"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        # Build base query
        query = Petition.query
        
        # Filter by user for citizens
        if user.role == "citizen":
            query = query.filter_by(user_id=user_id)
        
        # Total petitions
        total_petitions = query.count()
        
        # Status breakdown
        status_counts = db.session.query(
            Petition.status,
            func.count(Petition.id)
        ).group_by(Petition.status)
        
        if user.role == "citizen":
            status_counts = status_counts.filter_by(user_id=user_id)
        
        status_breakdown = {status: count for status, count in status_counts.all()}
        
        # Priority breakdown
        priority_counts = db.session.query(
            Petition.priority,
            func.count(Petition.id)
        ).group_by(Petition.priority)
        
        if user.role == "citizen":
            priority_counts = priority_counts.filter_by(user_id=user_id)
        
        priority_breakdown = {priority: count for priority, count in priority_counts.all()}
        
        # Department breakdown
        dept_counts = db.session.query(
            Department.name,
            func.count(Petition.id)
        ).join(Petition).group_by(Department.name)
        
        if user.role == "citizen":
            dept_counts = dept_counts.filter(Petition.user_id == user_id)
        
        department_breakdown = {dept: count for dept, count in dept_counts.all()}
        
        # Average resolution time (for resolved petitions)
        resolved_petitions = query.filter(Petition.resolved_at.isnot(None)).all()
        avg_resolution_time = 0
        if resolved_petitions:
            total_time = sum([
                (p.resolved_at - p.created_at).total_seconds() / 86400  # Convert to days
                for p in resolved_petitions
            ])
            avg_resolution_time = round(total_time / len(resolved_petitions), 2)
        
        return jsonify({
            "total_petitions": total_petitions,
            "status_breakdown": status_breakdown,
            "priority_breakdown": priority_breakdown,
            "department_breakdown": department_breakdown,
            "avg_resolution_days": avg_resolution_time,
            "resolved_count": len(resolved_petitions)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics.route("/trends", methods=["GET"])
@jwt_required()
def get_trends():
    """Get petition trends over time"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        # Get petitions from last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        query = db.session.query(
            func.date(Petition.created_at).label('date'),
            func.count(Petition.id).label('count')
        ).filter(Petition.created_at >= thirty_days_ago)\
         .group_by(func.date(Petition.created_at))\
         .order_by(func.date(Petition.created_at))
        
        if user.role == "citizen":
            query = query.filter(Petition.user_id == user_id)
        
        results = query.all()
        
        trends = [
            {
                "date": str(date),
                "count": count
            }
            for date, count in results
        ]
        
        return jsonify({"trends": trends}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics.route("/priority-distribution", methods=["GET"])
@jwt_required()
def get_priority_distribution():
    """Get detailed priority distribution"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        query = db.session.query(
            Petition.priority,
            Petition.urgency_level,
            func.count(Petition.id)
        ).group_by(Petition.priority, Petition.urgency_level)
        
        if user.role == "citizen":
            query = query.filter(Petition.user_id == user_id)
        
        results = query.all()
        
        distribution = [
            {
                "priority": priority,
                "urgency": urgency,
                "count": count
            }
            for priority, urgency, count in results
        ]
        
        return jsonify({"distribution": distribution}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics.route("/sentiment-analysis", methods=["GET"])
@jwt_required()
def get_sentiment_analysis():
    """Get sentiment analysis statistics"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        query = Petition.query
        
        if user.role == "citizen":
            query = query.filter_by(user_id=user_id)
        
        petitions = query.all()
        
        # Calculate sentiment statistics
        if petitions:
            sentiments = [p.sentiment_score for p in petitions if p.sentiment_score is not None]
            
            if sentiments:
                avg_sentiment = sum(sentiments) / len(sentiments)
                positive_count = len([s for s in sentiments if s > 0.05])
                negative_count = len([s for s in sentiments if s < -0.05])
                neutral_count = len(sentiments) - positive_count - negative_count
            else:
                avg_sentiment = 0
                positive_count = negative_count = neutral_count = 0
        else:
            avg_sentiment = 0
            positive_count = negative_count = neutral_count = 0
        
        return jsonify({
            "average_sentiment": round(avg_sentiment, 3),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "total_analyzed": len(petitions)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
