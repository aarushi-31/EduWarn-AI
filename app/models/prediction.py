from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from app.db import Base

class MLModel(Base):
    __tablename__ = 'ml_models'

    model_id = Column(Integer, primary_key=True, autoincrement=True)
    algorithm = Column(String(80), nullable=False)
    version = Column(String(20), nullable=False)
    accuracy = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    trained_on = Column(DateTime, default=datetime.utcnow)

    # Relationships
    predictions = relationship('Prediction', back_populates='model_used')


class Prediction(Base):
    __tablename__ = 'predictions'

    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='RESTRICT'), nullable=False)
    cycle_id = Column(Integer, ForeignKey('assessment_cycles.cycle_id', ondelete='RESTRICT'), nullable=False)
    model_id = Column(Integer, ForeignKey('ml_models.model_id', ondelete='RESTRICT'), nullable=False)
    risk_category = Column(String(20), nullable=False)  # 'Low', 'Medium', 'High'
    risk_score = Column(Float, nullable=False)          # Normalized 0.0 to 1.0 (higher = higher risk)
    predicted_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('student_id', 'cycle_id', 'model_id', name='uq_student_cycle_model'),
        CheckConstraint("risk_category IN ('Low', 'Medium', 'High')", name='chk_risk_category')
    )

    # Relationships
    student = relationship('Student', back_populates='predictions')
    cycle = relationship('AssessmentCycle', back_populates='predictions')
    model_used = relationship('MLModel', back_populates='predictions')
    factors = relationship('PredictionFactor', back_populates='prediction', cascade='all, delete-orphan')
    suggestions = relationship('Suggestion', back_populates='prediction', cascade='all, delete-orphan')
    notifications = relationship('Notification', back_populates='prediction', cascade='all, delete-orphan')

    @property
    def badge_class(self):
        if self.risk_category == 'High':
            return 'danger'
        elif self.risk_category == 'Medium':
            return 'warning'
        return 'success'


class PredictionFactor(Base):
    __tablename__ = 'prediction_factors'

    factor_id = Column(Integer, primary_key=True, autoincrement=True)
    prediction_id = Column(Integer, ForeignKey('predictions.prediction_id', ondelete='CASCADE'), nullable=False)
    feature_name = Column(String(80), nullable=False)
    contribution = Column(Float, nullable=False)  # Relative weight of this feature toward risk

    # Relationships
    prediction = relationship('Prediction', back_populates='factors')


class Suggestion(Base):
    __tablename__ = 'suggestions'

    suggestion_id = Column(Integer, primary_key=True, autoincrement=True)
    prediction_id = Column(Integer, ForeignKey('predictions.prediction_id', ondelete='CASCADE'), nullable=False)
    suggestion_text = Column(Text, nullable=False)

    # Relationships
    prediction = relationship('Prediction', back_populates='suggestions')


class Notification(Base):
    __tablename__ = 'notifications'

    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    prediction_id = Column(Integer, ForeignKey('predictions.prediction_id', ondelete='CASCADE'), nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('is_read IN (0, 1)', name='chk_notification_is_read'),
    )

    # Relationships
    recipient = relationship('User', back_populates='notifications')
    prediction = relationship('Prediction', back_populates='notifications')
