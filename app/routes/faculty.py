"""
Faculty Portal Routes Controller
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, Response
from app.db import get_session
from app.models.user import Student, Class, Faculty
from app.models.academic import Subject, AssessmentCycle, TeachingAssignment
from app.services.auth_service import login_required, role_required
from app.services.academic_service import (
    get_faculty_classes, get_faculty_students, save_or_update_record,
    process_bulk_csv_upload, get_student_academic_profile
)
from app.services.prediction_service import batch_predict_class_cycle

faculty_bp = Blueprint('faculty', __name__)

@faculty_bp.before_request
@login_required
@role_required('faculty')
def require_faculty():
    pass

@faculty_bp.route('/dashboard')
def dashboard():
    faculty_id = session.get('faculty_id')
    db = get_session()

    classes = get_faculty_classes(faculty_id)
    cycles = db.query(AssessmentCycle).order_by(AssessmentCycle.cycle_id.asc()).all()

    # Query parameters for filtering
    selected_class_id = request.args.get('class_id', type=int)
    if not selected_class_id and classes:
        selected_class_id = classes[0].class_id

    selected_cycle_id = request.args.get('cycle_id', type=int)
    if not selected_cycle_id and cycles:
        selected_cycle_id = cycles[-1].cycle_id  # default to latest cycle

    risk_filter = request.args.get('risk', 'All')
    search_query = request.args.get('search', '').strip().lower()

    # Fetch students with records and predictions
    roster = get_faculty_students(
        faculty_id=faculty_id,
        class_id=selected_class_id,
        cycle_id=selected_cycle_id,
        risk_filter=risk_filter
    )

    if search_query:
        roster = [item for item in roster if search_query in item['student'].name.lower() or search_query in item['student'].roll_no.lower()]

    # Statistics for dashboard summary cards
    all_roster = get_faculty_students(faculty_id=faculty_id, class_id=selected_class_id, cycle_id=selected_cycle_id)
    counts = {
        'total': len(all_roster),
        'high': sum(1 for x in all_roster if x['prediction'] and x['prediction'].risk_category == 'High'),
        'medium': sum(1 for x in all_roster if x['prediction'] and x['prediction'].risk_category == 'Medium'),
        'low': sum(1 for x in all_roster if x['prediction'] and x['prediction'].risk_category == 'Low'),
    }
    counts['unpredicted'] = counts['total'] - (counts['high'] + counts['medium'] + counts['low'])

    return render_template(
        'faculty/dashboard.html',
        classes=classes,
        cycles=cycles,
        selected_class_id=selected_class_id,
        selected_cycle_id=selected_cycle_id,
        risk_filter=risk_filter,
        search_query=search_query,
        roster=roster,
        counts=counts
    )

@faculty_bp.route('/student/<int:student_id>')
def student_detail(student_id):
    profile = get_student_academic_profile(student_id)
    if not profile:
        flash("Student record not found.", "danger")
        return redirect(url_for('faculty.dashboard'))

    return render_template('faculty/student_detail.html', profile=profile)

@faculty_bp.route('/enter-record', methods=['GET', 'POST'])
def enter_record():
    faculty_id = session.get('faculty_id')
    db = get_session()

    classes = get_faculty_classes(faculty_id)
    cycles = db.query(AssessmentCycle).all()
    assignments = db.query(TeachingAssignment).filter_by(faculty_id=faculty_id).all()
    subjects = list(set([a.subject for a in assignments]))

    selected_class_id = request.args.get('class_id', type=int) or (classes[0].class_id if classes else None)
    students = db.query(Student).filter_by(class_id=selected_class_id).order_by(Student.roll_no).all() if selected_class_id else []

    if request.method == 'POST':
        student_id = request.form.get('student_id', type=int)
        subject_id = request.form.get('subject_id', type=int)
        cycle_id = request.form.get('cycle_id', type=int)

        raw_data = {
            'attendance_pct': request.form.get('attendance_pct'),
            'internal_marks': request.form.get('internal_marks'),
            'assignment_score': request.form.get('assignment_score'),
            'participation_score': request.form.get('participation_score'),
            'prev_sem_marks': request.form.get('prev_sem_marks')
        }

        try:
            record, pred = save_or_update_record(
                student_id=student_id,
                subject_id=subject_id,
                cycle_id=cycle_id,
                faculty_id=faculty_id,
                raw_data=raw_data
            )
            flash(f"Academic record successfully saved! ML Prediction: {pred.risk_category} Risk (Score: {pred.risk_score:.3f})", "success")
            return redirect(url_for('faculty.student_detail', student_id=student_id))
        except Exception as e:
            flash(f"Error saving record: {str(e)}", "danger")

    return render_template(
        'faculty/enter_record.html',
        classes=classes,
        cycles=cycles,
        subjects=subjects,
        students=students,
        selected_class_id=selected_class_id
    )

@faculty_bp.route('/upload-csv', methods=['GET', 'POST'])
def upload_csv():
    faculty_id = session.get('faculty_id')
    db = get_session()

    classes = get_faculty_classes(faculty_id)
    cycles = db.query(AssessmentCycle).all()
    assignments = db.query(TeachingAssignment).filter_by(faculty_id=faculty_id).all()
    subjects = list(set([a.subject for a in assignments]))

    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash("Please upload a CSV file.", "danger")
            return redirect(request.url)

        file = request.files['csv_file']
        if file.filename == '':
            flash("No selected file.", "danger")
            return redirect(request.url)

        subject_id = request.form.get('subject_id', type=int)
        cycle_id = request.form.get('cycle_id', type=int)

        if not subject_id or not cycle_id:
            flash("Subject and Assessment Cycle are required.", "danger")
            return redirect(request.url)

        res = process_bulk_csv_upload(
            file_stream=file.stream,
            faculty_id=faculty_id,
            subject_id=subject_id,
            cycle_id=cycle_id
        )

        if res['processed'] > 0:
            flash(f"Successfully processed {res['processed']} records and generated {res['predictions']} ML predictions!", "success")
        if res['errors']:
            flash(f"Encountered {len(res['errors'])} errors during upload. Check console/logs.", "warning")

        return redirect(url_for('faculty.dashboard', cycle_id=cycle_id))

    return render_template('faculty/upload_csv.html', classes=classes, cycles=cycles, subjects=subjects)

@faculty_bp.route('/download-csv-sample')
def download_csv_sample():
    csv_content = "roll_no,attendance_pct,internal_marks,assignment_score,participation_score,prev_sem_marks\n22AIML001,52.0,11.5,9.0,7.0,48.0\n22AIML005,71.0,19.5,16.0,13.0,64.0\n22AIML010,92.0,28.5,24.0,19.0,86.0\n"
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=sample_academic_upload.csv"}
    )

@faculty_bp.route('/batch-predict', methods=['POST'])
def batch_predict():
    class_id = request.form.get('class_id', type=int)
    cycle_id = request.form.get('cycle_id', type=int)

    if not class_id or not cycle_id:
        flash("Invalid class or assessment cycle.", "danger")
        return redirect(url_for('faculty.dashboard'))

    res = batch_predict_class_cycle(class_id=class_id, cycle_id=cycle_id)
    flash(f"Batch prediction complete: {res['success']} of {res['total']} students evaluated.", "info")
    return redirect(url_for('faculty.dashboard', class_id=class_id, cycle_id=cycle_id))
