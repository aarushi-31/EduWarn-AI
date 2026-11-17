from app.db import Base, db_session
from app.models.user import User, Department, Class, Faculty, Student
from app.models.academic import Subject, TeachingAssignment, AssessmentCycle, AcademicRecord
from app.models.prediction import MLModel, Prediction, PredictionFactor, Suggestion, Notification

__all__ = [
    'Base',
    'db_session',
    'User',
    'Department',
    'Class',
    'Faculty',
    'Student',
    'Subject',
    'TeachingAssignment',
    'AssessmentCycle',
    'AcademicRecord',
    'MLModel',
    'Prediction',
    'PredictionFactor',
    'Suggestion',
    'Notification'
]
