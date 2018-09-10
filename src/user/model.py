from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, PasswordType

from common.database import Base


class User(Base):
    __tablename__ = 'littera_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(length=32), unique=True, nullable=False)
    email = Column(EmailType, unique=True, nullable=False)
    phone = Column(String(length=11), unique=True, nullable=False)
    password = Column(PasswordType(schemes=['pbkdf2_sha256']), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<User(username={self.username}, email={self.email})>'
