"""Notification service for sending alerts"""
from app.models import Notification
from app.extensions import db

class NotificationService:
    """Handle notifications for petition updates"""
    
    @staticmethod
    def create_notification(user_id, petition_id, message):
        """Create a new notification"""
        notification = Notification(
            user_id=user_id,
            petition_id=petition_id,
            message=message
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def get_user_notifications(user_id, unread_only=False):
        """Get notifications for a user"""
        query = Notification.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(read_status=False)
        
        return query.order_by(Notification.created_at.desc()).all()
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark notification as read"""
        notification = Notification.query.get(notification_id)
        if notification:
            notification.read_status = True
            db.session.commit()
        return notification
    
    @staticmethod
    def mark_all_as_read(user_id):
        """Mark all notifications as read for a user"""
        Notification.query.filter_by(
            user_id=user_id,
            read_status=False
        ).update({"read_status": True})
        db.session.commit()
    
    @staticmethod
    def notify_petition_submitted(user_id, petition_id, petition_title):
        """Send notification when petition is submitted"""
        message = f"Your petition '{petition_title}' has been submitted successfully. Petition ID: {petition_id}"
        return NotificationService.create_notification(user_id, petition_id, message)
    
    @staticmethod
    def notify_status_update(user_id, petition_id, new_status, comment=None):
        """Send notification when petition status changes"""
        message = f"Your petition status has been updated to: {new_status}"
        if comment:
            message += f". Comment: {comment}"
        return NotificationService.create_notification(user_id, petition_id, message)
    
    @staticmethod
    def notify_resolution(user_id, petition_id, resolution_comment):
        """Send notification when petition is resolved"""
        message = f"Your petition has been resolved. Resolution: {resolution_comment}"
        return NotificationService.create_notification(user_id, petition_id, message)
