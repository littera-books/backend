from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType

from common.database import Base
from applications.message.model import Message


class Admin(Base):
    __tablename__ = 'littera_admin'
    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), unique=True, nullable=False)
    password = Column(PasswordType(schemes=['pbkdf2_sha256']), unique=False, nullable=False)
    is_admin = Column(Boolean, default=True)
    user = relationship(Message, back_populates='admin')

    def __repr__(self):
        return f'<Admin(username={self.username}>'

    def to_dict(self):
        """
        sanic-jwt 에 user 정보를 dict 형태로 전달하는 메서드
        """
        return {
            'user_id': self.id,
            'username': self.username,
            'is_admin': self.is_admin,
        }
