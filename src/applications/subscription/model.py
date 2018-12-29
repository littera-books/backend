from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from common.database import Base


class Subscription(Base):
    __tablename__ = 'subscription'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    user_id = Column(Integer, ForeignKey('littera_user.id'))
    first_name = Column(String(length=20), unique=False, nullable=True)
    last_name = Column(String(length=20), unique=False, nullable=True)
    address = Column(String, unique=False, nullable=True)
    extra_address = Column(String, unique=False, nullable=True)
    phone = Column(String(length=20), unique=False, nullable=True)
    created_at = Column(DateTime(timezone=True), primary_key=True, server_default=func.now())
    product = relationship('Product', back_populates='subscription')
    user = relationship('User', back_populates='subscription')
    book = relationship('Book', back_populates='subscription', cascade='all, delete-orphan')
