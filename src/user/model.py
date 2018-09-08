import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy_utils import EmailType, PasswordType

from common.database import Base, engine


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(
        EmailType,
        unique=True,
        nullable=False,
    )
    password = Column(
        PasswordType(schemes=[
            'pbkdf2_sha512',
        ]),
        unique=False,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.now(timezone.utc).astimezone())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User(email={self.email})>'


Base.metadata.create_all(bind=engine)  # Base에 연결된 모든 테이블 매핑
