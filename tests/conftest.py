"""
PyTest Configuration and Global Fixtures
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import os
import sys
import pytest
from datetime import datetime, date

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.db import Base, init_db_engine, get_session
from app.models import (
    User, Department, Class, Faculty, Student,
    Subject, TeachingAssignment, AssessmentCycle, AcademicRecord,
    MLModel, Prediction
)

@pytest.fixture(scope='session')
def app():
    test_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_instance.db'))
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{test_db_path}',
        'SECRET_KEY': 'test-secret-key-12345'
    })

    engine = init_db_engine(f'sqlite:///{test_db_path}')
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Seed baseline fixtures
    session = get_session()

    # Admin
    admin = User(username='test_admin', email='admin@test.edu', role='admin')
    admin.set_password('AdminPass123!')
    session.add(admin)

    # Department
    dept = Department(dept_name='CSE (AIML)')
    session.add(dept)
    session.flush()

    # Faculty
    fac_user = User(username='test_faculty', email='faculty@test.edu', role='faculty')
    fac_user.set_password('FacultyPass123!')
    session.add(fac_user)
    session.flush()

    faculty = Faculty(user_id=fac_user.user_id, dept_id=dept.dept_id, name='Dr. Test Faculty')
    session.add(faculty)
    session.flush()

    # Class & Subject
    cls = Class(dept_id=dept.dept_id, section='A', semester=5, academic_year='2026-27')
    session.add(cls)
    session.flush()

    sub = Subject(dept_id=dept.dept_id, subject_code='CS501', subject_name='Software Engineering')
    session.add(sub)
    session.flush()

    ta = TeachingAssignment(faculty_id=faculty.faculty_id, subject_id=sub.subject_id, class_id=cls.class_id)
    session.add(ta)

    # Students
    stu_user1 = User(username='test_student1', email='s1@test.edu', role='student')
    stu_user1.set_password('StudentPass123!')
    session.add(stu_user1)
    session.flush()

    stu1 = Student(user_id=stu_user1.user_id, class_id=cls.class_id, roll_no='TEST001', name='Test Student Alpha')
    session.add(stu1)

    stu_user2 = User(username='test_student2', email='s2@test.edu', role='student')
    stu_user2.set_password('StudentPass123!')
    session.add(stu_user2)
    session.flush()

    stu2 = Student(user_id=stu_user2.user_id, class_id=cls.class_id, roll_no='TEST002', name='Test Student Beta')
    session.add(stu2)

    # Cycles
    c1 = AssessmentCycle(cycle_name='IA-1', start_date=date(2026, 9, 1))
    c2 = AssessmentCycle(cycle_name='IA-2', start_date=date(2026, 11, 1))
    session.add_all([c1, c2])
    session.flush()

    # Academic Records
    rec1 = AcademicRecord(
        student_id=stu1.student_id,
        subject_id=sub.subject_id,
        cycle_id=c1.cycle_id,
        entered_by=faculty.faculty_id,
        attendance_pct=52.0,
        internal_marks=10.0,
        assignment_score=8.0,
        participation_score=7.0,
        prev_sem_marks=45.0
    )
    rec2 = AcademicRecord(
        student_id=stu2.student_id,
        subject_id=sub.subject_id,
        cycle_id=c1.cycle_id,
        entered_by=faculty.faculty_id,
        attendance_pct=92.0,
        internal_marks=28.0,
        assignment_score=24.0,
        participation_score=19.0,
        prev_sem_marks=88.0
    )
    session.add_all([rec1, rec2])

    # ML Model
    ml_mod = MLModel(algorithm="Logistic Regression", version="v1.0.0", accuracy=0.87, f1_score=0.86)
    session.add(ml_mod)

    session.commit()

    yield app

    # Teardown
    try:
        session.close()
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
    except Exception:
        pass

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def session():
    return get_session()
