from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from app.db import Base

class Subject(Base):
    __tablename__ = 'subjects'

    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_id = Column(Integer, ForeignKey('departments.dept_id', ondelete='RESTRICT'), nullable=False)
    subject_code = Column(String(20), unique=True, nullable=False)
    subject_name = Column(String(100), nullable=False)

    # Relationships
    department = relationship('Department', back_populates='subjects')
    teaching_assignments = relationship('TeachingAssignment', back_populates='subject')
    academic_records = relationship('AcademicRecord', back_populates='subject')


class TeachingAssignment(Base):
    __tablename__ = 'teaching_assignments'

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    faculty_id = Column(Integer, ForeignKey('faculty.faculty_id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id', ondelete='RESTRICT'), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.class_id', ondelete='RESTRICT'), nullable=False)

    __table_args__ = (
        UniqueConstraint('faculty_id', 'subject_id', 'class_id', name='uq_teaching_assignment'),
    )

    # Relationships
    faculty = relationship('Faculty', back_populates='teaching_assignments')
    subject = relationship('Subject', back_populates='teaching_assignments')
    academic_class = relationship('Class', back_populates='teaching_assignments')


class AssessmentCycle(Base):
    __tablename__ = 'assessment_cycles'

    cycle_id = Column(Integer, primary_key=True, autoincrement=True)
    cycle_name = Column(String(50), nullable=False)  # e.g., 'IA-1', 'IA-2'
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    # Relationships
    records = relationship('AcademicRecord', back_populates='cycle')
    predictions = relationship('Prediction', back_populates='cycle')


class AcademicRecord(Base):
    __tablename__ = 'academic_records'

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='RESTRICT'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id', ondelete='RESTRICT'), nullable=False)
    cycle_id = Column(Integer, ForeignKey('assessment_cycles.cycle_id', ondelete='RESTRICT'), nullable=False)
    entered_by = Column(Integer, ForeignKey('faculty.faculty_id', ondelete='RESTRICT'), nullable=False)

    attendance_pct = Column(Float, nullable=False)
    internal_marks = Column(Float, nullable=False)
    assignment_score = Column(Float, nullable=False)
    participation_score = Column(Float, nullable=False)
    prev_sem_marks = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'cycle_id', name='uq_student_subject_cycle'),
        CheckConstraint('attendance_pct >= 0 AND attendance_pct <= 100', name='chk_attendance_pct'),
        CheckConstraint('internal_marks >= 0', name='chk_internal_marks'),
        CheckConstraint('assignment_score >= 0', name='chk_assignment_score'),
        CheckConstraint('participation_score >= 0', name='chk_participation_score'),
        CheckConstraint('prev_sem_marks >= 0 AND prev_sem_marks <= 100', name='chk_prev_sem_marks'),
    )

    # Relationships
    student = relationship('Student', back_populates='academic_records')
    subject = relationship('Subject', back_populates='academic_records')
    cycle = relationship('AssessmentCycle', back_populates='records')
    evaluator = relationship('Faculty', back_populates='records_entered')

    def to_feature_dict(self):
        return {
            'attendance_pct': self.attendance_pct,
            'internal_marks': self.internal_marks,
            'assignment_score': self.assignment_score,
            'participation_score': self.participation_score,
            'prev_sem_marks': self.prev_sem_marks
        }
