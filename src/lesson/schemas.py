from typing import List, Optional
from pydantic import BaseModel

from src.model_mixins import TimestampMixin


class FileContentCreate(BaseModel, TimestampMixin):
    """
    Schema for file content base
    
    Attributes:
        lesson_id (int): Foreign key to lesson
        url (str): URL to file
    """
    lesson_id: Optional[int] = None
    url: str


class FileContentUpdate(BaseModel, TimestampMixin):
    """
    Schema for file content base
    
    Attributes:
        lesson_id (int): Foreign key to lesson
        url (str): URL to file
    """
    lesson_id: Optional[int]
    url: Optional[str]


class FileContentResponse(BaseModel, TimestampMixin):
    """
    Schema for file content response
    
    Attributes:
        id (int): Primary key
        lesson_id (int): Foreign key to lesson
        url (str): URL to file
    """
    id: int
    lesson_id: int
    url: str


class ArticleContentCreate(BaseModel, TimestampMixin):
    """
    Schema for article content base
    
    Attributes:
        lesson_id (int): Foreign key to lesson
        content (str): Article content
    """
    lesson_id: Optional[int] = None
    content: str


class ArticleContentUpdate(BaseModel, TimestampMixin):
    """
    Schema for article content base
    
    Attributes:
        lesson_id (int): Foreign key to lesson
        content (str): Article content
    """
    lesson_id: Optional[int]
    content: Optional[str]


class ArticleContentResponse(BaseModel, TimestampMixin):
    """
    Schema for article content response
    
    Attributes:
        id (int): Primary key
        lesson_id (int): Foreign key to lesson
        content (str): Article content
    """
    id: int
    lesson_id: int
    content: str


class QuizQuestionCreate(BaseModel):
    """
    Schema for a single quiz question
    """
    question: str
    option_1: str
    option_2: str
    option_3: Optional[str] = None
    option_4: Optional[str] = None
    answer: str

class QuizContentCreate(BaseModel):
    """
    Schema for quiz content with multiple questions
    """
    lesson_id: Optional[int] = None
    questions: List[QuizQuestionCreate]


class QuizContentUpdate(BaseModel, TimestampMixin):
    """
    Schema for quiz content base
    
    Attributes:
        lesson_id (int): Foreign key to lesson
        content (str): Quiz content
    """
    lesson_id: Optional[int] = None
    question: Optional[str] = None
    option_1: Optional[str] = None
    option_2: Optional[str] = None
    option_3: Optional[str] = None
    option_4: Optional[str] = None
    answer: Optional[str] = None


class QuizContentResponse(BaseModel, TimestampMixin):
    """
    Schema for quiz content response
    
    Attributes:
        id (int): Primary key
        lesson_id (int): Foreign key to lesson
        content (str): Quiz content
    """
    id: int
    lesson_id: int
    question: str
    option_1: str
    option_2: str
    option_3: Optional[str] = None
    option_4: Optional[str] = None
    answer: str


class LessonCreate(BaseModel, TimestampMixin):
    """
    Schema for lesson base
    
    Attributes:
        course_id (int): Foreign key to course
        section_id (int): Foreign key to section
        title (str): Lesson title
        description (str): Lesson description
        thumbnail_url (str): URL to lesson thumbnail
        content_type (str): Type of content (article, video, quiz, pdf)
        access_type (str): Type of access (free, paid)
        quiz_attempts_allowed (int): Number of attempts allowed for quiz
        ordering (int): Order of lesson in section
        duration (int): Duration of lesson in seconds
        published (bool): Whether lesson is published
            
    """
    course_id: int
    section_id: int
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    content_type: str
    access_type: str
    quiz_attempts_allowed: Optional[int]
    ordering: int
    duration: int
    published: bool
    file_content: Optional[FileContentCreate] = None
    article_content: Optional[ArticleContentCreate] = None
    quiz_content: Optional[QuizContentCreate] = None


class LessonUpdate(BaseModel, TimestampMixin):
    """
    Schema for lesson base
    
    Attributes:
        course_id (int): Foreign key to course
        section_id (int): Foreign key to section
        title (str): Lesson title
        description (str): Lesson description
        thumbnail_url (str): URL to lesson thumbnail
        content_type (str): Type of content (article, video, quiz, pdf)
        access_type (str): Type of access (free, paid)
        quiz_attempts_allowed (int): Number of attempts allowed for quiz
        ordering (int): Order of lesson in section
        duration (int): Duration of lesson in seconds
        published (bool): Whether lesson is published
            
    """
    course_id: Optional[int]
    section_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    thumbnail_url: Optional[str]
    content_type: Optional[str]
    access_type: Optional[str]
    quiz_attempts_allowed: Optional[int]
    ordering: Optional[int]
    duration: Optional[int]
    published: Optional[bool]


class LessonResponse(BaseModel, TimestampMixin):
    """
    Schema for lesson response
    
    Attributes:
        id (int): Primary key
        course_id (int): Foreign key to course
        section_id (int): Foreign key to section
        title (str): Lesson title
        description (str): Lesson description
        thumbnail_url (str): URL to lesson thumbnail
        content_type (str): Type of content (article, video, quiz, pdf)
        access_type (str): Type of access (free, paid)
        quiz_attempts_allowed (int): Number of attempts allowed for quiz
        ordering (int): Order of lesson in section
        duration (int): Duration of lesson in seconds
        published (bool): Whether lesson is published
            
    """
    id: int
    course_id: int
    section_id: int
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    content_type: str
    access_type: str
    quiz_attempts_allowed: Optional[int]
    ordering: int
    duration: int
    published: bool
