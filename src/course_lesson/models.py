from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

from ..config.database import Base

class Lesson(Base):
    """CourseVideo Model"""
    __tablename__ = 'course_video'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    section_id = Column(Integer, ForeignKey('section.id'))
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    video_url = Column(String(255), nullable=True)
    duration = Column(Integer(50), nullable=True)
    published = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
