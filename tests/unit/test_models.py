"""
Unit Tests for Database Models and Relational Integrity (Exp 5, NFR5)
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import pytest
from app.models.user import User, Student, Faculty, Class, Department
from app.models.academic import Subject, TeachingAssignment, AssessmentCycle, AcademicRecord
from app.models.prediction import MLModel, Prediction, PredictionFactor, Suggestion, Notification

def test_user_student_relationship(session):
    """Verify 1:1 relationship between User and Student."""
    student = session.query(Student).filter_by(roll_no='TEST001').first()
    assert student is not None
    assert student.user is not None
    assert student.user.username == 'test_student1'
    assert student.academic_class.section == 'A'

def test_academic_record_features(session):
    """Verify AcademicRecord attributes and dictionary export."""
    rec = session.query(AcademicRecord).first()
    assert rec is not None
    assert rec.attendance_pct >= 0 and rec.attendance_pct <= 100
    features = rec.to_feature_dict()
    assert 'attendance_pct' in features
    assert 'internal_marks' in features
    assert 'assignment_score' in features

def test_ml_model_metadata(session):
    """Verify ML Model metadata entry exists."""
    model = session.query(MLModel).first()
    assert model is not None
    assert model.accuracy > 0.70
    assert model.f1_score > 0.70

def test_prediction_badge_classes(session):
    """Verify dynamic CSS badge styling for risk categories."""
    p_high = Prediction(student_id=1, cycle_id=1, model_id=1, risk_category='High', risk_score=0.9)
    p_med = Prediction(student_id=1, cycle_id=1, model_id=1, risk_category='Medium', risk_score=0.6)
    p_low = Prediction(student_id=1, cycle_id=1, model_id=1, risk_category='Low', risk_score=0.1)

    assert p_high.badge_class == 'danger'
    assert p_med.badge_class == 'warning'
    assert p_low.badge_class == 'success'
