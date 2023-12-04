from sqlalchemy import (
    Column, Integer, String, Boolean,
    ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship

from ..config.database import Base
from ..model_mixins import TimestampMixin


class Lesson(Base, TimestampMixin):
    """
    Model for lessons

    Attributes:
        id (int): Primary key
        course_id (int): Foreign key to course
        section_id (int): Foreign key to section
        title (str): Lesson title
        description (str): Lesson description
        thumbnail_url (str): URL to lesson thumbnail
        content_type (str): Type of content (article, video, quiz)
        access_type (str): Type of access (free, paid)
        quiz_attempts_allowed (int): Number of attempts allowed for quiz
        ordering (int): Order of lesson in section
        duration (int): Duration of lesson in seconds
        published (bool): Whether lesson is published
    """
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    section_id = Column(Integer, ForeignKey('section.id'), nullable=False)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String(255), nullable=True)
    content_type = Column(String(50), nullable=False)
    access_type = Column(String(50), nullable=False)
    quiz_attempts_allowed = Column(Integer, nullable=False)
    ordering = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    published = Column(Boolean, default=False)

    section = relationship("Section", back_populates="lessons")
    article_content = relationship("ArticleContent", back_populates="lesson")
    file_content = relationship("FileContent", back_populates="lesson")
    quiz_content = relationship("QuizContent", back_populates="lesson")

    __table_args__ = (
        UniqueConstraint('section_id', 'course_id', 'title', name='unique_section_lesson'),
        UniqueConstraint('section_id', 'course_id', 'ordering', name='_course_section_ordering_uc'),
    )

class FileContent(Base, TimestampMixin):
    """
    Model for File content

    Attributes:
        id (int): Primary key
        lesson_id (int): Foreign key to lesson
        url (str): URL to file
    """
    __tablename__ = 'file_content'
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    url = Column(String(255), nullable=False, unique=True)

    lesson = relationship("Lesson", back_populates="file_content")

class ArticleContent(Base, TimestampMixin):
    """
    Model for article content

    Attributes:
        id (int): Primary key
        lesson_id (int): Foreign key to lesson
        text (str): Article text
    """
    __tablename__ = 'article_content'
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    content = Column(Text, nullable=False, unique=True)

    lesson = relationship("Lesson", back_populates="article_content")
    

class QuizContent(Base, TimestampMixin):
    """
    Model for quiz content

    Attributes:
        id (int): Primary key
        lesson_id (int): Foreign key to lesson
        quiz_id (int): Foreign key to quiz
        question (str): Quiz question
        option_1 (str): Quiz option 1
        option_2 (str): Quiz option 2
        option_3 (str): Quiz option 3
        option_4 (str): Quiz option 4
    """
    __tablename__ = 'quiz_content'
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    question = Column(Text, nullable=False)
    option_1 = Column(Text, nullable=False)
    option_2 = Column(Text, nullable=False)
    option_3 = Column(Text, nullable=True)
    option_4 = Column(Text, nullable=True)
    answer = Column(Text, nullable=False)

    lesson = relationship("Lesson", back_populates="quiz_content")

    __table_args__ = (
        UniqueConstraint('lesson_id', 'question', name='unique_lesson_question'),
    )