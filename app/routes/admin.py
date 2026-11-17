"""
Administrator / HOD Portal Routes Controller
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import get_session
from app.models.user import Faculty, Department, Class, Student
from app.models.academic import AssessmentCycle
from app.models.prediction import MLModel, Prediction
from app.services.auth_service import login_required, role_required
from app.services.academic_service import get_department_aggregates

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
@role_required('admin')
def require_admin():
    pass

@admin_bp.route('/dashboard')
def dashboard():
    aggregates = get_department_aggregates()
    db = get_session()
    faculty_list = db.query(Faculty).all()
    active_model = db.query(MLModel).order_by(MLModel.model_id.desc()).first()
    cycles = db.query(AssessmentCycle).all()

    return render_template(
        'admin/dashboard.html',
        aggregates=aggregates,
        faculty_list=faculty_list,
        active_model=active_model,
        cycles=cycles
    )

@admin_bp.route('/reports')
def reports():
    aggregates = get_department_aggregates()
    db = get_session()
    cycles = db.query(AssessmentCycle).all()
    selected_cycle_id = request.args.get('cycle_id', type=int) or (cycles[-1].cycle_id if cycles else None)

    # Detailed report data
    predictions = db.query(Prediction).filter_by(cycle_id=selected_cycle_id).join(Student).order_by(Student.roll_no).all() if selected_cycle_id else []

    return render_template(
        'admin/reports.html',
        aggregates=aggregates,
        cycles=cycles,
        selected_cycle_id=selected_cycle_id,
        predictions=predictions
    )
