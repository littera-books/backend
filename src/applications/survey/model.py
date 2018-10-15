from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from common.database import Base


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    subject = Column(String(length=50), unique=True, nullable=False)
    title = Column(String(length=255), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    selection = relationship('Selection', back_populates='question', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Question subject={self.subject}>'


class Selection(Base):
    __tablename__ = 'selection'
    id = Column(Integer, primary_key=True)
    select = Column(String(length=255), unique=False, nullable=False)
    is_accepted = Column(Boolean, unique=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship('Question', back_populates='selection')
    user = relationship('SurveyResult', back_populates='selection', cascade='all, delete-orphan')


class SurveyResult(Base):
    __tablename__ = 'survey_result'
    user_id = Column(Integer, ForeignKey('littera_user.id'), primary_key=True)
    selection_id = Column(Integer, ForeignKey('selection.id'), primary_key=True)
    user = relationship('User', back_populates='selection')
    selection = relationship('Selection', back_populates='user')


class ResignSurvey(Base):
    __tablename__ = 'resign_survey'
    id = Column(Integer, primary_key=True)
    content = Column(String, unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
