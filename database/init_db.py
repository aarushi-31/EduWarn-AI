import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import Base, get_engine, get_session
from app.models import (
    User, Department, Class, Faculty, Student,
    Subject, TeachingAssignment, AssessmentCycle, AcademicRecord,
    MLModel, Prediction, PredictionFactor, Suggestion, Notification
)

def init_database(reset=False):
    engine = get_engine()
    if reset:
        print("[INFO] Dropping existing database tables...")
        Base.metadata.drop_all(bind=engine)
    print("[INFO] Creating database schema conforming to Experiment 5 (14 tables)...")
    Base.metadata.create_all(bind=engine)
    print("[SUCCESS] All 14 relational tables created successfully!")

def check_status():
    session = get_session()
    tables = [
        ('users', User),
        ('departments', Department),
        ('classes', Class),
        ('faculty', Faculty),
        ('students', Student),
        ('subjects', Subject),
        ('teaching_assignments', TeachingAssignment),
        ('assessment_cycles', AssessmentCycle),
        ('academic_records', AcademicRecord),
        ('ml_models', MLModel),
        ('predictions', Prediction),
        ('prediction_factors', PredictionFactor),
        ('suggestions', Suggestion),
        ('notifications', Notification)
    ]
    print("\n" + "="*50)
    print("DATABASE SCHEMA & TABLE STATUS")
    print("="*50)
    total_rows = 0
    for table_name, model in tables:
        try:
            count = session.query(model).count()
            total_rows += count
            print(f" - {table_name:<25}: {count:>4} rows")
        except Exception as e:
            print(f" - {table_name:<25}: ERROR ({e})")
    print("="*50)
    print(f"Total Tables: {len(tables)} | Total Rows: {total_rows}\n")

if __name__ == '__main__':
    if '--reset' in sys.argv:
        init_database(reset=True)
    elif '--status' in sys.argv:
        check_status()
    else:
        init_database()
        check_status()
