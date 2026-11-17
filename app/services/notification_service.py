"""
Notification and Early Warning Alert Service
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

from datetime import datetime
from app.db import get_session
from app.models.prediction import Notification

def create_notification(user_id, message, prediction_id=None):
    """Creates a new notification record."""
    session = get_session()
    notif = Notification(
        user_id=user_id,
        prediction_id=prediction_id,
        message=message,
        is_read=False,
        created_at=datetime.utcnow()
    )
    session.add(notif)
    session.commit()
    return notif

def get_user_notifications(user_id, unread_only=False, limit=15):
    """Fetches user notifications ordered by timestamp descending."""
    session = get_session()
    query = session.query(Notification).filter_by(user_id=user_id)
    if unread_only:
        query = query.filter_by(is_read=False)
    return query.order_by(Notification.created_at.desc()).limit(limit).all()

def get_unread_count(user_id):
    """Returns total unread notifications count for badge display."""
    session = get_session()
    return session.query(Notification).filter_by(user_id=user_id, is_read=False).count()

def mark_notification_as_read(notification_id, user_id):
    """Marks a single notification as read if owned by user."""
    session = get_session()
    notif = session.query(Notification).filter_by(notification_id=notification_id, user_id=user_id).first()
    if notif:
        notif.is_read = True
        session.commit()
        return True
    return False

def mark_all_as_read(user_id):
    """Marks all notifications as read for a user."""
    session = get_session()
    session.query(Notification).filter_by(user_id=user_id, is_read=False).update({'is_read': True})
    session.commit()
