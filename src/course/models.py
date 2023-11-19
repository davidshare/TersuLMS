from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime,
    ForeignKey, Text 
)

from ..config.database import Base


class Course(Base):
    """Course Model"""
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    course_category_id = Column(Integer, ForeignKey('course_category.id'))
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    tags = Column(String(255), nullable=True)
    course_level = Column(String(50), nullable=True)
    course_language = Column(String(50), nullable=True)
    course_duration = Column(String(50), nullable=True)
    course_thumbnail = Column(String(255), nullable=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    published = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
