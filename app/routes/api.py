"""
Internal JSON API Controller
Provides data endpoints for dynamic Chart.js rendering and AJAX UI updates.
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

from flask import Blueprint, jsonify, session
from app.db import get_session
from app.models.prediction import Prediction, MLModel
from app.models.academic import AssessmentCycle, AcademicRecord
from app.models.user import Student
from app.services.auth_service import login_required
from app.services.notification_service import get_unread_count
from app.services.academic_service import get_department_aggregates

api_bp = Blueprint('api', __name__)

@api_bp.route('/notifications/unread-count')
@login_required
def unread_notifications_count():
    user_id = session.get('user_id')
    count = get_unread_count(user_id) if user_id else 0
    return jsonify({'unread_count': count})

@api_bp.route('/charts/department-risk')
@login_required
def department_risk_chart():
    aggregates = get_department_aggregates()
    dist = aggregates.get('risk_distribution', {'High': 0, 'Medium': 0, 'Low': 0})
    return jsonify({
        'labels': ['High Risk', 'Medium Risk', 'Low Risk'],
        'data': [dist.get('High', 0), dist.get('Medium', 0), dist.get('Low', 0)],
        'colors': ['#dc3545', '#ffc107', '#198754']
    })

@api_bp.route('/charts/student-metrics/<int:student_id>')
@login_required
def student_metrics_chart(student_id):
    db = get_session()
    records = db.query(AcademicRecord).filter_by(student_id=student_id).join(AssessmentCycle).order_by(AssessmentCycle.cycle_id.asc()).all()

    cycles = [r.cycle.cycle_name for r in records]
    attendance = [r.attendance_pct for r in records]
    internals = [r.internal_marks for r in records]
    assignments = [r.assignment_score for r in records]

    return jsonify({
        'cycles': cycles,
        'attendance': attendance,
        'internals': internals,
        'assignments': assignments
    })
