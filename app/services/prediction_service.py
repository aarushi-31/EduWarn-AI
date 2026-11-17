"""
Prediction Service
Coordinates ML inference, factor explainability, suggestion generation,
database persistence, and risk-change early warning alerts.
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

from datetime import datetime
from app.db import get_session
from app.models.user import Student, User, Faculty
from app.models.academic import AcademicRecord, AssessmentCycle, TeachingAssignment
from app.models.prediction import MLModel, Prediction, PredictionFactor, Suggestion
from ml.predict import predict_student_risk
from app.services.notification_service import create_notification

def get_or_register_active_model(session):
    """Retrieves the latest registered model from the database, or creates an initial entry."""
    active_model = session.query(MLModel).order_by(MLModel.model_id.desc()).first()
    if not active_model:
        active_model = MLModel(
            algorithm="Logistic Regression Pipeline",
            version="v1.0.0",
            accuracy=0.8708,
            f1_score=0.8600,
            trained_on=datetime.utcnow()
        )
        session.add(active_model)
        session.commit()
    return active_model

def generate_student_prediction(student_id, cycle_id, model_path=None):
    """
    Executes end-to-end prediction workflow for a single student in a specific assessment cycle.
    """
    session = get_session()

    student = session.query(Student).filter_by(student_id=student_id).first()
    if not student:
        raise ValueError(f"Student ID {student_id} not found.")

    cycle = session.query(AssessmentCycle).filter_by(cycle_id=cycle_id).first()
    if not cycle:
        raise ValueError(f"Assessment Cycle ID {cycle_id} not found.")

    # Find academic record for this student and cycle
    record = session.query(AcademicRecord).filter_by(student_id=student_id, cycle_id=cycle_id).first()
    if not record:
        raise ValueError(f"No academic record exists for student {student.name} ({student.roll_no}) in cycle {cycle.cycle_name}.")

    feature_dict = record.to_feature_dict()

    # Run ML prediction engine
    result = predict_student_risk(feature_dict, model_path=model_path)
    active_model = get_or_register_active_model(session)

    # Check for existing prediction for the same student, cycle, and model
    existing_pred = session.query(Prediction).filter_by(
        student_id=student_id, cycle_id=cycle_id, model_id=active_model.model_id
    ).first()

    # Look for previous historical cycle prediction to detect risk change (Elicited Requirement)
    prev_pred = session.query(Prediction).join(AssessmentCycle).filter(
        Prediction.student_id == student_id,
        Prediction.cycle_id != cycle_id
    ).order_by(Prediction.predicted_at.desc()).first()

    if existing_pred:
        # Update existing prediction record
        pred = existing_pred
        pred.risk_category = result['risk_category']
        pred.risk_score = result['risk_score']
        pred.predicted_at = datetime.utcnow()

        # Clear old factors and suggestions for fresh insertion
        for f in list(pred.factors):
            session.delete(f)
        for s in list(pred.suggestions):
            session.delete(s)
        session.flush()
    else:
        # Create new prediction record
        pred = Prediction(
            student_id=student_id,
            cycle_id=cycle_id,
            model_id=active_model.model_id,
            risk_category=result['risk_category'],
            risk_score=result['risk_score'],
            predicted_at=datetime.utcnow()
        )
        session.add(pred)
        session.flush()

    # Save Contributing Factors (FR5)
    for factor in result['factors']:
        pf = PredictionFactor(
            prediction_id=pred.prediction_id,
            feature_name=factor['feature_name'],
            contribution=factor['contribution']
        )
        session.add(pf)

    # Save Improvement Suggestions (FR7)
    for suggestion_text in result['suggestions']:
        sug = Suggestion(
            prediction_id=pred.prediction_id,
            suggestion_text=suggestion_text
        )
        session.add(sug)

    # Check for risk-category change and trigger Early Warning Alert
    if prev_pred and prev_pred.risk_category != pred.risk_category:
        direction = "escalated" if (
            (prev_pred.risk_category == 'Low' and pred.risk_category in ('Medium', 'High')) or
            (prev_pred.risk_category == 'Medium' and pred.risk_category == 'High')
        ) else "improved"

        alert_msg = (
            f"Early Warning Alert: Student {student.name} ({student.roll_no}) risk level has {direction} "
            f"from '{prev_pred.risk_category}' to '{pred.risk_category}' in {cycle.cycle_name}."
        )

        # Notify Student
        create_notification(user_id=student.user_id, message=alert_msg, prediction_id=pred.prediction_id)

        # Notify Faculty who teaches this student
        assignment = session.query(TeachingAssignment).filter_by(class_id=student.class_id).first()
        if assignment and assignment.faculty:
            create_notification(user_id=assignment.faculty.user_id, message=alert_msg, prediction_id=pred.prediction_id)

    session.commit()
    return pred

def batch_predict_class_cycle(class_id, cycle_id, model_path=None):
    """
    Runs batch predictions for all students in a class for a given assessment cycle.
    """
    session = get_session()
    students = session.query(Student).filter_by(class_id=class_id).all()

    success_count = 0
    errors = []

    for s in students:
        try:
            generate_student_prediction(s.student_id, cycle_id, model_path=model_path)
            success_count += 1
        except Exception as e:
            errors.append(f"{s.roll_no}: {str(e)}")

    return {
        'total': len(students),
        'success': success_count,
        'errors': errors
    }
