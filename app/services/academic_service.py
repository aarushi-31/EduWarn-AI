"""
Academic Data and Reporting Service
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import io
import csv
from datetime import datetime
from app.db import get_session
from app.models.user import Student, Faculty, Class, Department, User
from app.models.academic import Subject, TeachingAssignment, AssessmentCycle, AcademicRecord
from app.models.prediction import Prediction, MLModel, PredictionFactor, Suggestion
from ml.preprocessing import validate_and_clean_features
from app.services.prediction_service import generate_student_prediction

def get_faculty_assignments(faculty_id):
    """Returns list of teaching assignments for a faculty member."""
    session = get_session()
    return session.query(TeachingAssignment).filter_by(faculty_id=faculty_id).all()

def get_faculty_classes(faculty_id):
    """Returns distinct classes assigned to a faculty member."""
    session = get_session()
    assignments = session.query(TeachingAssignment).filter_by(faculty_id=faculty_id).all()
    class_ids = list(set([a.class_id for a in assignments]))
    return session.query(Class).filter(Class.class_id.in_(class_ids)).all() if class_ids else []

def get_faculty_students(faculty_id, class_id=None, cycle_id=None, risk_filter=None):
    """
    Retrieves students belonging to a faculty's assigned classes with their latest academic
    record and ML risk prediction. Supports filtering by class, cycle, and risk category.
    """
    session = get_session()
    allowed_classes = get_faculty_classes(faculty_id)
    allowed_class_ids = [c.class_id for c in allowed_classes]

    if not allowed_class_ids:
        return []

    target_class_ids = [class_id] if class_id and class_id in allowed_class_ids else allowed_class_ids

    # Query students in target classes
    students = session.query(Student).filter(Student.class_id.in_(target_class_ids)).order_by(Student.roll_no).all()

    # Determine target assessment cycle (default to latest if not specified)
    if not cycle_id:
        latest_cycle = session.query(AssessmentCycle).order_by(AssessmentCycle.cycle_id.desc()).first()
        cycle_id = latest_cycle.cycle_id if latest_cycle else None

    results = []
    for s in students:
        # Fetch academic record for cycle
        rec = session.query(AcademicRecord).filter_by(student_id=s.student_id, cycle_id=cycle_id).first() if cycle_id else None

        # Fetch latest prediction for this student in cycle
        pred = session.query(Prediction).filter_by(student_id=s.student_id, cycle_id=cycle_id).first() if cycle_id else None

        if risk_filter and risk_filter != 'All':
            if not pred or pred.risk_category != risk_filter:
                continue

        results.append({
            'student': s,
            'class': s.academic_class,
            'record': rec,
            'prediction': pred
        })

    return results

def save_or_update_record(student_id, subject_id, cycle_id, faculty_id, raw_data):
    """
    Validates and persists an academic record for a student, then triggers ML prediction.
    """
    session = get_session()
    cleaned, errors = validate_and_clean_features(raw_data)
    if errors:
        raise ValueError("; ".join(errors))

    record = session.query(AcademicRecord).filter_by(
        student_id=student_id, subject_id=subject_id, cycle_id=cycle_id
    ).first()

    if record:
        record.attendance_pct = cleaned['attendance_pct']
        record.internal_marks = cleaned['internal_marks']
        record.assignment_score = cleaned['assignment_score']
        record.participation_score = cleaned['participation_score']
        record.prev_sem_marks = cleaned['prev_sem_marks']
        record.entered_by = faculty_id
    else:
        record = AcademicRecord(
            student_id=student_id,
            subject_id=subject_id,
            cycle_id=cycle_id,
            entered_by=faculty_id,
            attendance_pct=cleaned['attendance_pct'],
            internal_marks=cleaned['internal_marks'],
            assignment_score=cleaned['assignment_score'],
            participation_score=cleaned['participation_score'],
            prev_sem_marks=cleaned['prev_sem_marks']
        )
        session.add(record)

    session.commit()

    # Automatically trigger prediction for this student in this cycle
    pred = generate_student_prediction(student_id, cycle_id)
    return record, pred

def process_bulk_csv_upload(file_stream, faculty_id, subject_id, cycle_id):
    """
    Parses a CSV file with student academic metrics, validates records,
    persists records to DB, and executes ML prediction pipeline.
    Expected CSV columns: roll_no, attendance_pct, internal_marks, assignment_score, participation_score, prev_sem_marks
    """
    session = get_session()
    reader = csv.DictReader(io.StringIO(file_stream.read().decode('utf-8-sig')))

    processed_count = 0
    predictions_count = 0
    errors = []

    for row_idx, row in enumerate(reader, start=1):
        roll_no = row.get('roll_no', '').strip()
        if not roll_no:
            errors.append(f"Row {row_idx}: Missing 'roll_no'")
            continue

        student = session.query(Student).filter_by(roll_no=roll_no).first()
        if not student:
            errors.append(f"Row {row_idx}: Student with Roll No '{roll_no}' not found in database.")
            continue

        try:
            _, pred = save_or_update_record(
                student_id=student.student_id,
                subject_id=subject_id,
                cycle_id=cycle_id,
                faculty_id=faculty_id,
                raw_data=row
            )
            processed_count += 1
            if pred:
                predictions_count += 1
        except Exception as err:
            errors.append(f"Row {row_idx} ({roll_no}): {str(err)}")

    return {
        'processed': processed_count,
        'predictions': predictions_count,
        'errors': errors
    }

def get_student_academic_profile(student_id):
    """
    Retrieves complete academic dossier for a student:
    profile, classes, all historical records, latest predictions, factors, suggestions.
    """
    session = get_session()
    student = session.query(Student).filter_by(student_id=student_id).first()
    if not student:
        return None

    # Historical records ordered by cycle
    records = session.query(AcademicRecord).filter_by(student_id=student_id).join(AssessmentCycle).order_by(AssessmentCycle.cycle_id.asc()).all()

    # Predictions ordered by cycle
    predictions = session.query(Prediction).filter_by(student_id=student_id).join(AssessmentCycle).order_by(AssessmentCycle.cycle_id.asc()).all()

    latest_prediction = predictions[-1] if predictions else None

    return {
        'student': student,
        'records': records,
        'predictions': predictions,
        'latest_prediction': latest_prediction
    }

def get_department_aggregates(dept_id=None):
    """
    Calculates department-wide and class-level summary statistics for HOD dashboard (FR8).
    """
    session = get_session()
    dept = session.query(Department).first() if not dept_id else session.query(Department).filter_by(dept_id=dept_id).first()
    if not dept:
        return {}

    total_students = session.query(Student).count()
    total_faculty = session.query(Faculty).count()
    total_classes = session.query(Class).count()

    # Get latest cycle
    latest_cycle = session.query(AssessmentCycle).order_by(AssessmentCycle.cycle_id.desc()).first()

    # Risk distributions in latest cycle
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0
    unpredicted_count = 0

    if latest_cycle:
        high_risk_count = session.query(Prediction).filter_by(cycle_id=latest_cycle.cycle_id, risk_category='High').count()
        medium_risk_count = session.query(Prediction).filter_by(cycle_id=latest_cycle.cycle_id, risk_category='Medium').count()
        low_risk_count = session.query(Prediction).filter_by(cycle_id=latest_cycle.cycle_id, risk_category='Low').count()
        total_predicted = high_risk_count + medium_risk_count + low_risk_count
        unpredicted_count = max(0, total_students - total_predicted)

    # Class-wise statistics
    class_stats = []
    classes = session.query(Class).all()
    for c in classes:
        c_students = session.query(Student).filter_by(class_id=c.class_id).all()
        s_ids = [s.student_id for s in c_students]

        c_high = session.query(Prediction).filter(
            Prediction.cycle_id == (latest_cycle.cycle_id if latest_cycle else 0),
            Prediction.student_id.in_(s_ids),
            Prediction.risk_category == 'High'
        ).count() if s_ids and latest_cycle else 0

        c_med = session.query(Prediction).filter(
            Prediction.cycle_id == (latest_cycle.cycle_id if latest_cycle else 0),
            Prediction.student_id.in_(s_ids),
            Prediction.risk_category == 'Medium'
        ).count() if s_ids and latest_cycle else 0

        c_low = session.query(Prediction).filter(
            Prediction.cycle_id == (latest_cycle.cycle_id if latest_cycle else 0),
            Prediction.student_id.in_(s_ids),
            Prediction.risk_category == 'Low'
        ).count() if s_ids and latest_cycle else 0

        class_stats.append({
            'class': c,
            'total_students': len(c_students),
            'high_risk': c_high,
            'medium_risk': c_med,
            'low_risk': c_low
        })

    return {
        'department': dept,
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_classes': total_classes,
        'latest_cycle': latest_cycle,
        'risk_distribution': {
            'High': high_risk_count,
            'Medium': medium_risk_count,
            'Low': low_risk_count,
            'Unpredicted': unpredicted_count
        },
        'class_stats': class_stats
    }
