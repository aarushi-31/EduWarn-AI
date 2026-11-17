import sys
import os
from datetime import datetime, date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import Base, get_engine, get_session
from app.models import (
    User, Department, Class, Faculty, Student,
    Subject, TeachingAssignment, AssessmentCycle, AcademicRecord,
    MLModel, Prediction, PredictionFactor, Suggestion, Notification
)

def seed_database():
    engine = get_engine()
    session = get_session()

    print("[INFO] Recreating database schema for fresh seeding...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("[INFO] 1. Creating Admin / HOD Account...")
    admin_user = User(
        username='admin_hod',
        email='hod.aiml@jssuni.edu.in',
        role='admin'
    )
    admin_user.set_password('AdminPassword123!')
    session.add(admin_user)
    session.flush()

    print("[INFO] 2. Creating Faculty Accounts...")
    f1_user = User(username='faculty_neha', email='neha.gupta@jssuni.edu.in', role='faculty')
    f1_user.set_password('FacultyPassword123!')
    session.add(f1_user)

    f2_user = User(username='faculty_amit', email='amit.verma@jssuni.edu.in', role='faculty')
    f2_user.set_password('FacultyPassword123!')
    session.add(f2_user)
    session.flush()

    # Department
    dept = Department(dept_name='Computer Science & Engineering (AIML)')
    session.add(dept)
    session.flush()

    faculty1 = Faculty(user_id=f1_user.user_id, dept_id=dept.dept_id, name='Prof. Neha Gupta')
    faculty2 = Faculty(user_id=f2_user.user_id, dept_id=dept.dept_id, name='Dr. Amit Verma')
    session.add_all([faculty1, faculty2])
    session.flush()

    dept.hod_id = faculty2.faculty_id

    print("[INFO] 3. Creating Academic Classes & Subjects...")
    class_5a = Class(dept_id=dept.dept_id, section='A', semester=5, academic_year='2026-2027')
    class_5b = Class(dept_id=dept.dept_id, section='B', semester=5, academic_year='2026-2027')
    session.add_all([class_5a, class_5b])
    session.flush()

    sub_se = Subject(dept_id=dept.dept_id, subject_code='KCS-501', subject_name='Software Engineering')
    sub_ml = Subject(dept_id=dept.dept_id, subject_code='KCS-502', subject_name='Machine Learning Techniques')
    sub_daa = Subject(dept_id=dept.dept_id, subject_code='KCS-503', subject_name='Design and Analysis of Algorithms')
    session.add_all([sub_se, sub_ml, sub_daa])
    session.flush()

    # Teaching Assignments
    t1 = TeachingAssignment(faculty_id=faculty1.faculty_id, subject_id=sub_se.subject_id, class_id=class_5a.class_id)
    t2 = TeachingAssignment(faculty_id=faculty1.faculty_id, subject_id=sub_se.subject_id, class_id=class_5b.class_id)
    t3 = TeachingAssignment(faculty_id=faculty2.faculty_id, subject_id=sub_ml.subject_id, class_id=class_5a.class_id)
    session.add_all([t1, t2, t3])
    session.flush()

    print("[INFO] 4. Creating Assessment Cycles...")
    cycle_ia1 = AssessmentCycle(cycle_name='IA-1', start_date=date(2026, 9, 1), end_date=date(2026, 9, 15))
    cycle_ia2 = AssessmentCycle(cycle_name='IA-2', start_date=date(2026, 11, 1), end_date=date(2026, 11, 15))
    session.add_all([cycle_ia1, cycle_ia2])
    session.flush()

    print("[INFO] 5. Creating Student Cohort & Academic Records...")
    cohort = [
        # High Risk Profiles (Low Attendance, Weak Internals)
        ('22AIML001', 'Rohit Sharma', 'student_rohit', class_5a, (52.0, 11.5, 9.0, 7.0, 48.0), (48.0, 9.0, 8.0, 6.0, 48.0)),
        ('22AIML002', 'Aakash Mishra', 'student_aakash', class_5a, (58.0, 13.0, 10.0, 8.0, 52.0), (54.0, 12.0, 9.0, 7.5, 52.0)),
        ('22AIML003', 'Simran Kaur', 'student_simran', class_5b, (61.0, 14.0, 11.0, 9.0, 50.0), (59.0, 12.5, 10.0, 8.0, 50.0)),
        ('22AIML004', 'Tanmay Joshi', 'student_tanmay', class_5b, (55.0, 10.0, 8.0, 6.0, 46.0), (50.0, 9.5, 7.5, 6.0, 46.0)),

        # Medium Risk Profiles (Borderline attendance 68-76%, average marks)
        ('22AIML005', 'Priya Singh', 'student_priya', class_5a, (71.0, 19.5, 16.0, 13.0, 64.0), (67.0, 17.0, 14.5, 12.0, 64.0)),
        ('22AIML006', 'Vikram Malhotra', 'student_vikram', class_5a, (73.0, 20.0, 15.0, 12.0, 62.0), (74.0, 21.0, 16.0, 13.0, 62.0)),
        ('22AIML007', 'Kavita Das', 'student_kavita', class_5b, (70.0, 18.0, 14.0, 11.0, 59.0), (72.0, 19.0, 15.0, 12.0, 59.0)),
        ('22AIML008', 'Rohan Gupta', 'student_rohan', class_5b, (74.0, 21.5, 17.0, 13.0, 65.0), (69.0, 18.0, 15.0, 11.5, 65.0)),
        ('22AIML009', 'Sneha Roy', 'student_sneha', class_5a, (72.0, 19.0, 16.5, 12.5, 63.0), (70.0, 18.5, 15.0, 12.0, 63.0)),

        # Low Risk Profiles (High attendance >85%, strong marks)
        ('22AIML010', 'Aarav Patel', 'student_aarav', class_5a, (92.0, 28.5, 24.0, 19.0, 86.0), (94.0, 29.0, 24.5, 19.5, 86.0)),
        ('22AIML011', 'Ananya Verma', 'student_ananya', class_5a, (88.0, 26.0, 22.0, 18.0, 81.0), (90.0, 27.5, 23.0, 18.5, 81.0)),
        ('22AIML012', 'Devendra Yadav', 'student_devendra', class_5a, (85.0, 25.0, 21.0, 17.0, 78.0), (86.0, 26.0, 22.0, 17.5, 78.0)),
        ('22AIML013', 'Meera Iyer', 'student_meera', class_5b, (95.0, 29.5, 25.0, 20.0, 91.0), (96.0, 30.0, 25.0, 20.0, 91.0)),
        ('22AIML014', 'Nikhil Saxena', 'student_nikhil', class_5b, (89.0, 27.0, 23.0, 17.5, 83.0), (91.0, 28.0, 23.5, 18.0, 83.0)),
        ('22AIML015', 'Ritika Sen', 'student_ritika', class_5b, (87.0, 26.5, 22.5, 18.0, 80.0), (88.0, 27.0, 23.0, 18.0, 80.0)),
        ('22AIML016', 'Siddharth Jain', 'student_siddharth', class_5a, (83.0, 24.0, 20.0, 16.0, 75.0), (84.0, 25.0, 21.0, 16.5, 75.0)),
        ('22AIML017', 'Pooja Hegde', 'student_pooja', class_5b, (91.0, 28.0, 23.5, 18.5, 85.0), (93.0, 28.5, 24.0, 19.0, 85.0)),
        ('22AIML018', 'Kunal Kapoor', 'student_kunal', class_5a, (80.0, 23.0, 19.0, 15.0, 72.0), (82.0, 24.0, 20.0, 15.5, 72.0)),
        ('22AIML019', 'Ishaan Trivedi', 'student_ishaan', class_5b, (79.0, 22.0, 18.5, 14.5, 70.0), (80.0, 23.0, 19.0, 15.0, 70.0)),
        ('22AIML020', 'Tara Bhatt', 'student_tara', class_5a, (86.0, 25.5, 21.5, 17.0, 79.0), (87.0, 26.0, 22.0, 17.5, 79.0))
    ]

    for roll, name, username, target_class, ia1_scores, ia2_scores in cohort:
        u = User(username=username, email=f"{username}@jssuni.edu.in", role='student')
        u.set_password('StudentPassword123!')
        session.add(u)
        session.flush()

        s = Student(user_id=u.user_id, class_id=target_class.class_id, roll_no=roll, name=name)
        session.add(s)
        session.flush()

        # IA-1 record for Software Engineering
        rec_ia1 = AcademicRecord(
            student_id=s.student_id,
            subject_id=sub_se.subject_id,
            cycle_id=cycle_ia1.cycle_id,
            entered_by=faculty1.faculty_id,
            attendance_pct=ia1_scores[0],
            internal_marks=ia1_scores[1],
            assignment_score=ia1_scores[2],
            participation_score=ia1_scores[3],
            prev_sem_marks=ia1_scores[4]
        )
        # IA-2 record for Software Engineering
        rec_ia2 = AcademicRecord(
            student_id=s.student_id,
            subject_id=sub_se.subject_id,
            cycle_id=cycle_ia2.cycle_id,
            entered_by=faculty1.faculty_id,
            attendance_pct=ia2_scores[0],
            internal_marks=ia2_scores[1],
            assignment_score=ia2_scores[2],
            participation_score=ia2_scores[3],
            prev_sem_marks=ia2_scores[4]
        )
        session.add_all([rec_ia1, rec_ia2])

    session.commit()
    print(f"[SUCCESS] Seeded {len(cohort)} students, 2 faculty, 1 admin, 2 classes, 3 subjects, and 40 academic records!")

if __name__ == '__main__':
    seed_database()
