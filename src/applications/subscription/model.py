from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from common.database import Base


class Subscription(Base):
    __tablename__ = 'subscription'
    product_id = Column(Integer, ForeignKey('product.id'))
    user_id = Column(Integer, ForeignKey('littera_user.id'))
    created_at = Column(DateTime(timezone=True), primary_key=True, server_default=func.now())
    product = relationship('Product', back_populates='subscription')
    user = relationship('User', back_populates='subscription')
