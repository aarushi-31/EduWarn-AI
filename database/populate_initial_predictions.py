import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import get_session
from app.models.user import Student
from app.models.academic import AssessmentCycle
from app.services.prediction_service import generate_student_prediction

def populate_all():
    session = get_session()
    students = session.query(Student).all()
    cycles = session.query(AssessmentCycle).order_by(AssessmentCycle.cycle_id.asc()).all()

    print(f"[INFO] Populating initial ML predictions for {len(students)} students across {len(cycles)} cycles...")
    count = 0
    for cycle in cycles:
        for student in students:
            try:
                pred = generate_student_prediction(student.student_id, cycle.cycle_id)
                count += 1
            except Exception as e:
                print(f"[ERROR] Student {student.roll_no} in cycle {cycle.cycle_name}: {e}")

    print(f"[SUCCESS] Successfully generated and stored {count} predictions with factors and suggestions!")

if __name__ == '__main__':
    populate_all()
