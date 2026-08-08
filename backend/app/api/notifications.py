"""Notifications API endpoints"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import NotificationService

notifications = Blueprint("notifications", __name__)


@notifications.route("/list", methods=["GET"])
@jwt_required()
def get_notifications():
    """Get user notifications"""
    try:
        user_id = int(get_jwt_identity())
        
        # Get all notifications
        all_notifications = NotificationService.get_user_notifications(user_id)
        
        result = [
            {
                "id": n.id,
                "message": n.message,
                "read_status": n.read_status,
                "created_at": n.created_at.isoformat(),
                "petition_id": n.petition_id
            }
            for n in all_notifications
        ]
        
        return jsonify({"notifications": result}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notifications.route("/unread", methods=["GET"])
@jwt_required()
def get_unread_notifications():
    """Get unread notifications"""
    try:
        user_id = int(get_jwt_identity())
        
        unread = NotificationService.get_user_notifications(user_id, unread_only=True)
        
        result = [
            {
                "id": n.id,
                "message": n.message,
                "created_at": n.created_at.isoformat(),
                "petition_id": n.petition_id
            }
            for n in unread
        ]
        
        return jsonify({"notifications": result, "count": len(result)}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notifications.route("/<int:notification_id>/read", methods=["PUT"])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        notification = NotificationService.mark_as_read(notification_id)
        
        if not notification:
            return jsonify({"error": "Notification not found"}), 404
        
        return jsonify({"message": "Notification marked as read"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notifications.route("/mark-all-read", methods=["PUT"])
@jwt_required()
def mark_all_read():
    """Mark all notifications as read"""
    try:
        user_id = int(get_jwt_identity())
        NotificationService.mark_all_as_read(user_id)
        
        return jsonify({"message": "All notifications marked as read"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
