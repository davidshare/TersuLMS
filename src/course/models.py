from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean,
    ForeignKey, Text, Float 
)
from ..model_mixins import TimestampMixin
from ..config.database import Base


class Course(Base, TimestampMixin):
    """Course Model"""
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    course_category_id = Column(Integer, ForeignKey('course_category.id'))
    title = Column(String(50), nullable=False)
    slug = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    course_level = Column(String(50), nullable=False)
    course_language = Column(String(50), nullable=False)
    course_duration = Column(Integer, nullable=True)
    course_thumbnail = Column(String(255), nullable=True)
    author_id = Column(Integer, ForeignKey('user_auth.id'))
    published = Column(Boolean, default=False)
    published_at = Column(DateTime, default=datetime.utcnow)

    sections = relationship("Section", back_populates="course", cascade="all, delete-orphan")
