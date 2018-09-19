from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from common.database import Base


class Message(Base):
    __tablename__ = 'message'
    user_id = Column(Integer, ForeignKey('littera_user.id'), primary_key=True)
    admin_id = Column(Integer, ForeignKey('littera_admin.id'), primary_key=True)
    body = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship('User', back_populates='admin')
    admin = relationship('Admin', back_populates='user')

    def __repr__(self):
        return f'<Message(created_at={self.created_at}>'
