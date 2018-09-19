from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from common.database import Base


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    subject = Column(String(length=10), unique=True, nullable=False)
    title = Column(String(length=255), unique=False, nullable=False)
    selection = relationship('Selection', back_populates='question')

    def __repr__(self):
        return f'<Question title={self.subject}>'


class Selection(Base):
    __tablename__ = 'selection'
    id = Column(Integer, primary_key=True)
    select = Column(String(length=255), unique=False, nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship('Question', back_populates='selection')
