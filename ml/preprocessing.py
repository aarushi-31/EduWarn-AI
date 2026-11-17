"""
Preprocessing and Feature Validation Module
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

FEATURE_NAMES = [
    'attendance_pct',
    'internal_marks',
    'assignment_score',
    'participation_score',
    'prev_sem_marks'
]

# Physical academic limits
FEATURE_BOUNDS = {
    'attendance_pct': (0.0, 100.0),
    'internal_marks': (0.0, 30.0),
    'assignment_score': (0.0, 25.0),
    'participation_score': (0.0, 20.0),
    'prev_sem_marks': (0.0, 100.0)
}

# Baseline median defaults for imputation
FEATURE_DEFAULTS = {
    'attendance_pct': 75.0,
    'internal_marks': 20.0,
    'assignment_score': 18.0,
    'participation_score': 14.0,
    'prev_sem_marks': 70.0
}

def validate_and_clean_features(record):
    """
    Validates and cleans a dictionary or Series containing academic features.
    Clips values to realistic academic boundaries and imputes missing fields.
    """
    cleaned = {}
    errors = []

    for feature in FEATURE_NAMES:
        raw_val = record.get(feature) if isinstance(record, dict) else getattr(record, feature, None)

        if raw_val is None or (isinstance(raw_val, str) and raw_val.strip() == ''):
            cleaned[feature] = FEATURE_DEFAULTS[feature]
            continue

        try:
            val = float(raw_val)
        except (ValueError, TypeError):
            errors.append(f"Invalid non-numeric value for {feature}: '{raw_val}'")
            continue

        min_b, max_b = FEATURE_BOUNDS[feature]
        if val < min_b or val > max_b:
            errors.append(f"Feature '{feature}' value {val} out of permitted range [{min_b}, {max_b}]")
            val = max(min_b, min(val, max_b))  # clip

        cleaned[feature] = float(val)

    if errors:
        return cleaned, errors
    return cleaned, None

def create_preprocessing_pipeline():
    """
    Returns a ColumnTransformer configured to standardize numeric academic features.
    """
    transformer = ColumnTransformer(
        transformers=[
            ('num_scaler', StandardScaler(), FEATURE_NAMES)
        ],
        remainder='drop'
    )
    return transformer

def get_feature_vector(cleaned_dict):
    """
    Converts a validated feature dictionary into a 2D numpy array [1, num_features]
    ordered by FEATURE_NAMES.
    """
    values = [cleaned_dict[feat] for feat in FEATURE_NAMES]
    return np.array([values], dtype=np.float32)
