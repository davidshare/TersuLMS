from sqlalchemy import (
    Column, Integer, String, Boolean,
    ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship

from ..config.database import Base
from ..model_mixins import TimestampMixin


class Lesson(Base, TimestampMixin):
    """Model for course lessons"""
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    section_id = Column(Integer, ForeignKey('section.id'))
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    content_url = Column(String(255), nullable=True)
    thumbnail_url = Column(String(255), nullable=True)
    content_type = Column(String(50), nullable=False)
    access_type = Column(String(50), nullable=False)
    ordering = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    published = Column(Boolean, default=False)

    section = relationship("Section", back_populates="lessons")

    __table_args__ = (
        UniqueConstraint('section_id', 'course_id', 'title',
                        'description', name='unique_section_lesson'),
    )
