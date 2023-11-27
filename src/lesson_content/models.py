from sqlalchemy import Column, Integer, ForeignKey, Text, UniqueConstraint, String, Boolean
from sqlalchemy.orm import relationship

from ..config.database import Base
from ..model_mixins import TimestampMixin


class VideoContent(Base, TimestampMixin):
    """VideoContent Model"""
    __tablename__ = 'video_content'
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    url = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'video_content',
    }


class ArticleContent(Base, TimestampMixin):
    """ArticleContent Model"""
    __tablename__ = 'article_content'
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    text = Column(Text, nullable=False, unique=True)
    __mapper_args__ = {
        'polymorphic_identity': 'article_content',
    }


class QuizContent(Base, TimestampMixin):
    """QuizContent Model"""
    __tablename__ = 'quiz_content'
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    attempts_allowed = Column(Integer, nullable=False)
    published = Column(Boolean, default=False)

    quiz_questions = relationship('QuizQuestions', back_populates='quiz_content')

    __mapper_args__ = {
        'polymorphic_identity': 'quiz_content',
    }


class QuizQuestions(Base):
    """QuizQuestion Model"""
    __tablename__ = 'quiz_questions'
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quiz_content.id'))
    question = Column(Text, nullable=False)

    quiz_content = relationship('QuizContent', back_populates='quiz_questions')
    options = relationship('QuizOption', back_populates='quiz_question')


class QuizOption(Base, TimestampMixin):
    """QuizOption Model"""
    __tablename__ = 'quiz_option'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('quiz_questions.id'))
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)
    quiz_question = relationship('QuizQuestions', back_populates='options')

    __table_args__ = (
        UniqueConstraint('question_id', 'text', name='_question_option_text_uc'),
    )
