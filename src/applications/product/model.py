from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from common.database import Base


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    months = Column(Integer, unique=True, nullable=False, default=0)
    price = Column(Integer, unique=False, nullable=False, default=0)
    description = Column(String(length=100), unique=False, nullable=True)
    is_visible = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    promotion = relationship('Promotion', uselist=False, back_populates='product')
    subscription = relationship('Subscription', back_populates='product', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Product(months={self.months})>'


class Promotion(Base):
    __tablename__ = 'promotion'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    code = Column(String(length=20), unique=True, nullable=False)
    product = relationship('Product', back_populates='promotion')
