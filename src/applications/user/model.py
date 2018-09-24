from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, PasswordType

from common.database import Base
from applications.message.model import Message


class User(Base):
    __tablename__ = 'littera_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), unique=True, nullable=False)
    email = Column(EmailType, unique=True, nullable=False)
    phone = Column(String(length=11), unique=True, nullable=False)
    password = Column(PasswordType(schemes=['pbkdf2_sha256']), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    admin = relationship(Message, back_populates='user')

    def __repr__(self):
        return f'<User(username={self.username}, email={self.email})>'

    def to_dict(self):
        """
        sanic-jwt 에 user 정보를 dict 형태로 전달하는 메서드
        """
        return {
            'user_id': self.id,
            'username': self.username,
            'email': self.email
        }
