"""
Student Portal Routes Controller
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import get_session
from app.models.user import Student, User
from app.services.auth_service import login_required, role_required
from app.services.academic_service import get_student_academic_profile
from app.services.notification_service import get_user_notifications, mark_notification_as_read, mark_all_as_read

student_bp = Blueprint('student', __name__)

@student_bp.before_request
@login_required
@role_required('student')
def require_student():
    pass

@student_bp.route('/dashboard')
def dashboard():
    student_id = session.get('student_id')
    user_id = session.get('user_id')

    if not student_id:
        db = get_session()
        st = db.query(Student).filter_by(user_id=user_id).first()
        if st:
            student_id = st.student_id
            session['student_id'] = st.student_id
        else:
            flash("No student profile linked to this account.", "danger")
            return redirect(url_for('auth.login'))

    profile = get_student_academic_profile(student_id)
    notifications = get_user_notifications(user_id=user_id, limit=5)

    return render_template(
        'student/dashboard.html',
        profile=profile,
        notifications=notifications
    )

@student_bp.route('/notifications')
def notifications():
    user_id = session.get('user_id')
    all_notifs = get_user_notifications(user_id=user_id, limit=50)
    return render_template('student/notifications.html', notifications=all_notifs)

@student_bp.route('/notifications/read/<int:notification_id>')
def mark_read(notification_id):
    user_id = session.get('user_id')
    mark_notification_as_read(notification_id, user_id)
    return redirect(url_for('student.notifications'))

@student_bp.route('/notifications/read-all')
def read_all():
    user_id = session.get('user_id')
    mark_all_as_read(user_id)
    flash("All notifications marked as read.", "info")
    return redirect(url_for('student.notifications'))
