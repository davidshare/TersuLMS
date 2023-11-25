from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship

from ..config.database import Base
from ..model_mixins import TimestampMixin


class LessonContent(Base, TimestampMixin):
    """LessonContent Model"""
    __tablename__ = 'lesson_content'
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    content_type = Column(String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'lesson_content',
        'polymorphic_on': content_type
    }


class VideoContent(LessonContent, TimestampMixin):
    """VideoContent Model"""
    __tablename__ = 'video_content'
    id = Column(Integer, ForeignKey('lesson_content.id'), primary_key=True)
    video_url = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    video_duration = Column(Integer, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'video_content',
    }


class ArticleContent(LessonContent, TimestampMixin):
    """ArticleContent Model"""
    __tablename__ = 'article_content'
    id = Column(Integer, ForeignKey('lesson_content.id'), primary_key=True)
    article_text = Column(Text, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'article_content',
    }


class QuizContent(LessonContent, TimestampMixin):
    """QuizContent Model"""
    __tablename__ = 'quiz_content'
    id = Column(Integer, ForeignKey('lesson_content.id'), primary_key=True)

    quiz_questions = relationship(
        'QuizQuestion', back_populates='quiz_content')

    __mapper_args__ = {
        'polymorphic_identity': 'quiz',
    }


class QuizQuestion(Base):
    """QuizQuestion Model"""
    __tablename__ = 'quiz_question'

    id = Column(Integer, primary_key=True)
    quiz_content_id = Column(Integer, ForeignKey('quiz_content.id'))
    question_text = Column(Text, nullable=False)
    quiz_content = relationship('QuizContent', back_populates='quiz_questions')
    options = relationship("QuizOption", back_populates="quiz_question")


class QuizOption(Base, TimestampMixin):
    """QuizOption Model"""
    __tablename__ = 'quiz_option'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('quiz_question.id'))
    option_text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)
    quiz_question = relationship("QuizQuestion", back_populates="options")
