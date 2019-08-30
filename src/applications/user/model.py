from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, PasswordType

from common.database import Base
from applications.message.model import Message


class User(Base):
    __tablename__ = 'littera_user'
    __mapper_args__ = {
        'confirm_deleted_rows': False,
    }
    id = Column(Integer, primary_key=True)
    first_name = Column(String(length=20), unique=False, nullable=True)
    last_name = Column(String(length=20), unique=False, nullable=True)
    address = Column(String, unique=False, nullable=True)
    extra_address = Column(String, unique=False, nullable=True)
    email = Column(EmailType, unique=True, nullable=False)
    phone = Column(String(length=20), unique=True, nullable=True)
    password = Column(PasswordType(schemes=['pbkdf2_sha256']), unique=False, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    log = Column(Boolean, default=False)
    admin = relationship(Message, back_populates='user')
    survey_result = relationship('SurveyResult', back_populates='user', cascade='all, delete-orphan')
    subscription = relationship('Subscription', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User(email={self.email})>'

    def to_dict(self):
        """
        sanic-jwt 에 user 정보를 dict 형태로 전달하는 메서드
        """
        return {
            'user_id': self.id
        }
