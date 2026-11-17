"""
Unit Tests for Data Preprocessing and Feature Validation (FR3)
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import pytest
from ml.preprocessing import validate_and_clean_features, get_feature_vector, FEATURE_NAMES

def test_clean_and_scale_valid_features():
    """Verify clean numeric values within permitted bounds pass without errors."""
    sample = {
        'attendance_pct': 82.5,
        'internal_marks': 22.0,
        'assignment_score': 19.0,
        'participation_score': 15.0,
        'prev_sem_marks': 75.0
    }
    cleaned, errors = validate_and_clean_features(sample)
    assert errors is None
    assert cleaned['attendance_pct'] == 82.5
    assert cleaned['internal_marks'] == 22.0

def test_handle_missing_values():
    """Verify missing values are safely imputed using sensible default baselines."""
    sample = {
        'attendance_pct': None,
        'internal_marks': '',
        'assignment_score': 15.0,
        'participation_score': 10.0,
        'prev_sem_marks': 65.0
    }
    cleaned, errors = validate_and_clean_features(sample)
    assert cleaned['attendance_pct'] == 75.0  # default
    assert cleaned['internal_marks'] == 20.0  # default
    assert cleaned['assignment_score'] == 15.0

def test_clip_out_of_bound_values():
    """Verify out-of-range values are flagged with warnings and clipped to legal thresholds."""
    sample = {
        'attendance_pct': 120.0,  # exceeds 100
        'internal_marks': -5.0,   # below 0
        'assignment_score': 15.0,
        'participation_score': 10.0,
        'prev_sem_marks': 65.0
    }
    cleaned, errors = validate_and_clean_features(sample)
    assert errors is not None
    assert len(errors) == 2
    assert cleaned['attendance_pct'] == 100.0
    assert cleaned['internal_marks'] == 0.0

def test_get_feature_vector():
    """Verify feature dictionary converts to standard 2D numpy matrix [1, 5]."""
    sample = {
        'attendance_pct': 80.0,
        'internal_marks': 20.0,
        'assignment_score': 18.0,
        'participation_score': 14.0,
        'prev_sem_marks': 70.0
    }
    vec = get_feature_vector(sample)
    assert vec.shape == (1, 5)
    assert vec[0][0] == 80.0
