from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from common.database import Base


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    months = Column(Integer, unique=True, nullable=False, default=0)
    price = Column(Integer, unique=False, nullable=False, default=0)
    description = Column(String(length=100), unique=False, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Product(months={self.months})>'
