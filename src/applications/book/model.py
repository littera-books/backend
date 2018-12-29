from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from common.database import Base


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    order = Column(Integer, unique=False, nullable=False, default=1)
    name = Column(String, unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    subscription_id = Column(Integer, ForeignKey('subscription.id'))
    subscription = relationship('Subscription', back_populates='book')
