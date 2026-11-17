"""
Dataset Generation Script for Student Performance Prediction
Department of Computer Science & Engineering (AIML), JSS University, Noida

NOTE: This script generates a reproducible, synthetic academic demonstration dataset.
It simulates realistic student performance distributions across attendance, examination marks,
assignment scores, participation, and previous semester scores.
This dataset is explicitly designated as synthetic demonstration data for academic and laboratory purposes.
"""

import os
import numpy as np
import pandas as pd

def generate_academic_dataset(num_samples=1200, random_seed=42):
    np.random.seed(random_seed)

    # 1. Base academic aptitude / engagement latent factor (normal distribution)
    latent_factor = np.random.normal(loc=0.0, scale=1.0, size=num_samples)

    # 2. Correlated feature generation based on latent engagement
    # Attendance Percentage (40% to 99%)
    attendance = 75.0 + (12.0 * latent_factor) + np.random.normal(0, 5.0, num_samples)
    attendance = np.clip(attendance, 35.0, 99.0)

    # Internal Exam Marks (out of 30)
    internal = 20.0 + (5.0 * latent_factor) + np.random.normal(0, 3.0, num_samples)
    internal = np.clip(internal, 5.0, 30.0)

    # Assignment Score (out of 25)
    assignment = 18.0 + (4.0 * latent_factor) + np.random.normal(0, 2.5, num_samples)
    assignment = np.clip(assignment, 4.0, 25.0)

    # Classroom Participation Score (out of 20)
    participation = 14.0 + (3.5 * latent_factor) + np.random.normal(0, 2.0, num_samples)
    participation = np.clip(participation, 3.0, 20.0)

    # Previous Semester Marks Percentage (40% to 98%)
    prev_sem = 72.0 + (10.0 * latent_factor) + np.random.normal(0, 6.0, num_samples)
    prev_sem = np.clip(prev_sem, 40.0, 98.0)

    # 3. Formulate Composite Academic Health Index (0.0 to 1.0)
    # Weights: Attendance (0.35), Internals (0.25), Assignments (0.15), Participation (0.10), Prev Sem (0.15)
    composite_index = (
        0.35 * (attendance / 100.0) +
        0.25 * (internal / 30.0) +
        0.15 * (assignment / 25.0) +
        0.10 * (participation / 20.0) +
        0.15 * (prev_sem / 100.0)
    )

    # Add realistic variance/noise
    noise = np.random.normal(0, 0.03, num_samples)
    final_score = np.clip(composite_index + noise, 0.0, 1.0)

    # 4. Derive Ground Truth Risk Category
    # - Low Risk: Composite >= 0.72 (on track, strong standing)
    # - Medium Risk: 0.55 <= Composite < 0.72 (borderline, early warning needed)
    # - High Risk: Composite < 0.55 (severe danger of failure/detention)
    risk_category = []
    for score in final_score:
        if score < 0.55:
            risk_category.append('High')
        elif score < 0.72:
            risk_category.append('Medium')
        else:
            risk_category.append('Low')

    df = pd.DataFrame({
        'attendance_pct': np.round(attendance, 1),
        'internal_marks': np.round(internal, 1),
        'assignment_score': np.round(assignment, 1),
        'participation_score': np.round(participation, 1),
        'prev_sem_marks': np.round(prev_sem, 1),
        'risk_category': risk_category
    })

    return df

if __name__ == '__main__':
    output_dir = os.path.join(os.path.dirname(__file__))
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'student_academic_data.csv')

    df = generate_academic_dataset()
    df.to_csv(csv_path, index=False)

    print(f"[SUCCESS] Synthetic dataset generated at: {csv_path}")
    print(f"Dataset Shape: {df.shape}")
    print("\nClass Distribution:")
    print(df['risk_category'].value_counts(normalize=True).round(3))
    print("\nSummary Statistics:")
    print(df.describe().round(2))
