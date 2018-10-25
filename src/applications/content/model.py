from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

from common.database import Base


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    image_url = Column(String, unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Image (name={self.name})>'
