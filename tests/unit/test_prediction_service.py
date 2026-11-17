"""
Unit Tests for ML Prediction Service, Explainability & Alerts (FR4, FR5, FR7, NFR4)
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import time
import pytest
from ml.predict import predict_student_risk, calculate_contributing_factors, generate_personalized_suggestions
from app.services.prediction_service import generate_student_prediction
from app.models.prediction import Prediction, Notification

def test_prediction_classification_high_risk():
    """Verify low attendance and low internal marks yield High Risk classification."""
    weak_student = {
        'attendance_pct': 45.0,
        'internal_marks': 8.0,
        'assignment_score': 7.0,
        'participation_score': 5.0,
        'prev_sem_marks': 42.0
    }
    result = predict_student_risk(weak_student)
    assert result['risk_category'] == 'High'
    assert result['risk_score'] > 0.65
    assert len(result['factors']) > 0
    assert len(result['suggestions']) > 0

def test_prediction_classification_low_risk():
    """Verify strong metrics yield Low Risk classification."""
    strong_student = {
        'attendance_pct': 94.0,
        'internal_marks': 29.0,
        'assignment_score': 24.0,
        'participation_score': 19.0,
        'prev_sem_marks': 90.0
    }
    result = predict_student_risk(strong_student)
    assert result['risk_category'] == 'Low'
    assert result['risk_score'] < 0.40

def test_contributing_factors_explainability():
    """Verify explainability engine highlights attendance as critical when below 60%."""
    sample = {
        'attendance_pct': 50.0,
        'internal_marks': 15.0,
        'assignment_score': 15.0,
        'participation_score': 12.0,
        'prev_sem_marks': 65.0
    }
    factors = calculate_contributing_factors(sample, 'High')
    att_factor = next(f for f in factors if f['feature_name'] == 'Attendance Percentage')
    assert att_factor['status'] == 'Critical'
    assert att_factor['contribution'] > 0.30

def test_prediction_latency_performance():
    """Verify model inference latency is under 100 milliseconds (NFR4)."""
    sample = {
        'attendance_pct': 75.0,
        'internal_marks': 20.0,
        'assignment_score': 18.0,
        'participation_score': 14.0,
        'prev_sem_marks': 70.0
    }
    start = time.time()
    for _ in range(10):
        predict_student_risk(sample)
    duration = (time.time() - start) / 10.0
    assert duration < 0.10  # less than 100ms per inference

def test_end_to_end_prediction_generation(session):
    """Verify end-to-end service persistence in database."""
    pred = generate_student_prediction(student_id=1, cycle_id=1)
    assert pred is not None
    assert pred.risk_category in ('Low', 'Medium', 'High')
    assert len(pred.factors) > 0
    assert len(pred.suggestions) > 0
