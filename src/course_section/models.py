from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from ..model_mixins import TimestampMixin
from ..config.database import Base

class Section(Base, TimestampMixin):
    """Model for course sections"""
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(255))
    ordering = Column(Integer, nullable=False)

    course = relationship("Course", back_populates="sections")
    lessons = relationship("Lesson", back_populates="section", cascade="all, delete-orphan")

    __table__args__ = (
        UniqueConstraint('course_id', 'ordering', name='_course_ordering_uc'),
        UniqueConstraint('course_id', 'title', name='_course_title_uc'),
    )

