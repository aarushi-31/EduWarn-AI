"""
Model Prediction & Factor Explainability Engine
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import os
import sys
import argparse
import joblib
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml.preprocessing import FEATURE_NAMES, validate_and_clean_features

_cached_pipeline = None

def get_model_pipeline(model_path=None):
    global _cached_pipeline
    if _cached_pipeline is not None:
        return _cached_pipeline

    if model_path is None:
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'models', 'best_student_model.joblib'))

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model artifact not found at: {model_path}. Please run ml/train_model.py first.")

    _cached_pipeline = joblib.load(model_path)
    return _cached_pipeline

def calculate_contributing_factors(cleaned_features, risk_category):
    """
    Computes explainability factors (FR5) detailing which academic features
    contributed most heavily to the predicted risk level.
    """
    factors = []

    # 1. Attendance Analysis (Target: >= 75%)
    att = cleaned_features['attendance_pct']
    if att < 60.0:
        att_contrib = 0.40
        factors.append({
            'feature_name': 'Attendance Percentage',
            'contribution': att_contrib,
            'status': 'Critical',
            'detail': f'Attendance is severely low at {att:.1f}% (university mandate is 75%).'
        })
    elif att < 75.0:
        att_contrib = 0.25
        factors.append({
            'feature_name': 'Attendance Percentage',
            'contribution': att_contrib,
            'status': 'Warning',
            'detail': f'Attendance is borderline at {att:.1f}% (below 75% threshold).'
        })
    else:
        factors.append({
            'feature_name': 'Attendance Percentage',
            'contribution': -0.20,
            'status': 'Good',
            'detail': f'Satisfactory attendance standing at {att:.1f}%.'
        })

    # 2. Internal Marks Analysis (Target: >= 18 / 30)
    int_marks = cleaned_features['internal_marks']
    if int_marks < 12.0:
        factors.append({
            'feature_name': 'Internal Examination Marks',
            'contribution': 0.30,
            'status': 'Critical',
            'detail': f'Internal examination score is critically low ({int_marks:.1f}/30).'
        })
    elif int_marks < 18.0:
        factors.append({
            'feature_name': 'Internal Examination Marks',
            'contribution': 0.15,
            'status': 'Warning',
            'detail': f'Internal score is average ({int_marks:.1f}/30).'
        })
    else:
        factors.append({
            'feature_name': 'Internal Examination Marks',
            'contribution': -0.15,
            'status': 'Good',
            'detail': f'Strong internal test score ({int_marks:.1f}/30).'
        })

    # 3. Assignment Performance (Target: >= 17 / 25)
    assn = cleaned_features['assignment_score']
    if assn < 12.0:
        factors.append({
            'feature_name': 'Assignment Submissions',
            'contribution': 0.15,
            'status': 'Warning',
            'detail': f'Assignment score ({assn:.1f}/25) indicates missed or low-scoring submissions.'
        })
    else:
        factors.append({
            'feature_name': 'Assignment Submissions',
            'contribution': -0.10,
            'status': 'Good',
            'detail': f'Consistent assignment completion ({assn:.1f}/25).'
        })

    # 4. Classroom Participation (Target: >= 13 / 20)
    part = cleaned_features['participation_score']
    if part < 10.0:
        factors.append({
            'feature_name': 'Class Participation',
            'contribution': 0.10,
            'status': 'Warning',
            'detail': f'Low engagement observed in practical/lecture sessions ({part:.1f}/20).'
        })

    # 5. Previous Semester Standing (Target: >= 60%)
    prev = cleaned_features['prev_sem_marks']
    if prev < 55.0:
        factors.append({
            'feature_name': 'Prior Academic Record',
            'contribution': 0.15,
            'status': 'Warning',
            'detail': f'Historical examination marks ({prev:.1f}%) reflect past foundational gaps.'
        })

    # Sort factors by contribution descending (highest risk contributors first)
    factors.sort(key=lambda x: x['contribution'], reverse=True)
    return factors

def generate_personalized_suggestions(cleaned_features, risk_category):
    """
    Generates actionable, evidence-based academic improvement recommendations (FR7).
    """
    suggestions = []

    if cleaned_features['attendance_pct'] < 75.0:
        shortfall_classes = int(np.ceil((75.0 - cleaned_features['attendance_pct']) * 0.6))
        suggestions.append(
            f"Prioritize attending the next {shortfall_classes} consecutive lectures/labs without absence to bring attendance above the 75% eligibility mark."
        )

    if cleaned_features['internal_marks'] < 18.0:
        suggestions.append(
            "Schedule a remedial doubts session with the subject faculty and review previous year question banks for the upcoming cycle."
        )

    if cleaned_features['assignment_score'] < 16.0:
        suggestions.append(
            "Ensure on-time submission for all upcoming module assignments; seek peer study group assistance on practical exercises."
        )

    if cleaned_features['participation_score'] < 12.0:
        suggestions.append(
            "Actively participate in lab programming problem-solving and oral viva questions during practical hours."
        )

    if risk_category == 'High':
        suggestions.insert(0, "URGENT INTERVENTION: Report to your Academic Mentor / Faculty Advisor for personalized academic counseling.")
    elif risk_category == 'Low' and not suggestions:
        suggestions.append("Maintain current study routine and consider taking up advanced technical mini-projects or certifications.")

    return suggestions

def predict_student_risk(record_dict, model_path=None):
    """
    Core inference function:
    Takes raw record dict, validates features, runs ML prediction, calculates explainability factors and suggestions.
    """
    cleaned, errors = validate_and_clean_features(record_dict)
    pipeline = get_model_pipeline(model_path)

    # Format dataframe for scikit-learn pipeline
    df_input = pd.DataFrame([cleaned])[FEATURE_NAMES]

    # Predict risk category
    predicted_class = pipeline.predict(df_input)[0]

    # Calculate risk score (continuous 0.0 to 1.0)
    # If classifier supports predict_proba, compute weighted risk probability
    if hasattr(pipeline.named_steps['classifier'], 'predict_proba'):
        classes = list(pipeline.named_steps['classifier'].classes_)
        probas = pipeline.predict_proba(df_input)[0]
        prob_dict = dict(zip(classes, probas))
        # Risk score = 1.0 * P(High) + 0.5 * P(Medium) + 0.0 * P(Low)
        risk_score = float(prob_dict.get('High', 0.0) * 1.0 + prob_dict.get('Medium', 0.0) * 0.5)
    else:
        # Fallback heuristic mapping
        mapping = {'Low': 0.15, 'Medium': 0.55, 'High': 0.90}
        risk_score = mapping.get(predicted_class, 0.5)

    factors = calculate_contributing_factors(cleaned, predicted_class)
    suggestions = generate_personalized_suggestions(cleaned, predicted_class)

    return {
        'risk_category': predicted_class,
        'risk_score': round(risk_score, 4),
        'cleaned_features': cleaned,
        'factors': factors,
        'suggestions': suggestions,
        'validation_errors': errors
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Predict Student Risk Category")
    parser.add_argument('--attendance', type=float, default=52.0, help="Attendance % (0-100)")
    parser.add_argument('--internal', type=float, default=11.5, help="Internal marks (0-30)")
    parser.add_argument('--assignment', type=float, default=9.0, help="Assignment score (0-25)")
    parser.add_argument('--participation', type=float, default=7.0, help="Participation (0-20)")
    parser.add_argument('--prev_sem', type=float, default=48.0, help="Previous semester % (0-100)")

    args = parser.parse_args()
    sample = {
        'attendance_pct': args.attendance,
        'internal_marks': args.internal,
        'assignment_score': args.assignment,
        'participation_score': args.participation,
        'prev_sem_marks': args.prev_sem
    }

    print("\nRunning Student Risk Inference on Sample:")
    print(sample)
    try:
        res = predict_student_risk(sample)
        print("\n" + "="*50)
        print(f"PREDICTED RISK CATEGORY: {res['risk_category'].upper()}")
        print(f"CONTINUOUS RISK SCORE  : {res['risk_score']} (0.0 to 1.0)")
        print("="*50)
        print("KEY CONTRIBUTING FACTORS (Explainability):")
        for f in res['factors']:
            print(f" - [{f['status']}] {f['feature_name']}: {f['detail']}")
        print("\nACTIONABLE SUGGESTIONS:")
        for s in res['suggestions']:
            print(f" • {s}")
        print("="*50 + "\n")
    except Exception as err:
        print(f"Error during prediction: {err}")
