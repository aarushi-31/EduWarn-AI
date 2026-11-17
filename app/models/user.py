from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(String(20), nullable=False)  # 'student', 'faculty', 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("role IN ('student', 'faculty', 'admin')", name='chk_user_role'),
    )

    # Relationships
    student_profile = relationship('Student', back_populates='user', uselist=False, cascade='all, delete-orphan')
    faculty_profile = relationship('Faculty', back_populates='user', uselist=False, cascade='all, delete-orphan')
    notifications = relationship('Notification', back_populates='recipient', cascade='all, delete-orphan', order_by="desc(Notification.created_at)")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Department(Base):
    __tablename__ = 'departments'

    dept_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name = Column(String(100), nullable=False)
    hod_id = Column(Integer, ForeignKey('faculty.faculty_id', ondelete='SET NULL'), nullable=True)

    # Relationships
    classes = relationship('Class', back_populates='department')
    faculty_members = relationship('Faculty', back_populates='department', foreign_keys='Faculty.dept_id')
    subjects = relationship('Subject', back_populates='department')


class Class(Base):
    __tablename__ = 'classes'

    class_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_id = Column(Integer, ForeignKey('departments.dept_id', ondelete='RESTRICT'), nullable=False)
    section = Column(String(10), nullable=False)
    semester = Column(Integer, nullable=False)
    academic_year = Column(String(20), nullable=False)

    __table_args__ = (
        CheckConstraint('semester BETWEEN 1 AND 8', name='chk_class_semester'),
    )

    # Relationships
    department = relationship('Department', back_populates='classes')
    students = relationship('Student', back_populates='academic_class')
    teaching_assignments = relationship('TeachingAssignment', back_populates='academic_class')

    @property
    def display_name(self):
        return f"Sem {self.semester} - Section {self.section} ({self.academic_year})"


class Faculty(Base):
    __tablename__ = 'faculty'

    faculty_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), unique=True, nullable=False)
    dept_id = Column(Integer, ForeignKey('departments.dept_id', ondelete='RESTRICT'), nullable=False)
    name = Column(String(100), nullable=False)

    # Relationships
    user = relationship('User', back_populates='faculty_profile')
    department = relationship('Department', back_populates='faculty_members', foreign_keys=[dept_id])
    teaching_assignments = relationship('TeachingAssignment', back_populates='faculty')
    records_entered = relationship('AcademicRecord', back_populates='evaluator')


class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), unique=True, nullable=False)
    class_id = Column(Integer, ForeignKey('classes.class_id', ondelete='RESTRICT'), nullable=False)
    roll_no = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)

    # Relationships
    user = relationship('User', back_populates='student_profile')
    academic_class = relationship('Class', back_populates='students')
    academic_records = relationship('AcademicRecord', back_populates='student')
    predictions = relationship('Prediction', back_populates='student', order_by="desc(Prediction.predicted_at)")
