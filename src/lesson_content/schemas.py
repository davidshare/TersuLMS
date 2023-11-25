from typing import Optional, List
from pydantic import BaseModel

class QuizOptionCreate(BaseModel):
    """Create model for quiz options."""
    option_text: str
    is_correct: bool

class QuizQuestionCreate(BaseModel):
    """Create model for quiz questions."""
    question_text: str
    options: List[QuizOptionCreate]

class QuizOptionResponse(QuizOptionCreate):
    """Response model for quiz options."""
    id: int

class QuestionBase(BaseModel):
    """Base model for quiz questions."""
    id: int
    question_text: str
    options: List[QuizOptionResponse]

class QuestionResponse(QuestionBase):
    """Response model for quiz questions."""
    pass


class LessonContentBase(BaseModel):
    """Base model for lesson content."""
    lesson_id: int
    content_type: str
    
class VideoContentCreate(LessonContentBase):
    """Create model for video content."""
    video_url: str
    video_duration: int
    description: str

class ArticleContentCreate(LessonContentBase):
    """Create model for article content."""
    article_text: str

class QuizContentCreate(LessonContentBase):
    """Create model for quiz content."""
    quiz_questions: List[QuizQuestionCreate]

class VideoContentResponse(VideoContentCreate):
    """Response model for video content."""
    id: int

class ArticleContentResponse(ArticleContentCreate):
    """Response model for article content."""
    id: int

class QuizContentResponse(QuizContentCreate):
    """Response model for quiz content."""
    id: int
    lesson_id: int
    content_type: str
    quiz_questions: List[QuestionResponse]


class LessonContentUpdate(BaseModel):
    """Update model for lesson content."""
    video_url: Optional[str] = None
    video_duration: Optional[int] = None
    description: Optional[str] = None
    article_text: Optional[str] = None
    quiz_questions: Optional[List[QuestionBase]] = None

class LessonContentResponse(BaseModel):
    """Response model for lesson content."""
    id: int
    lesson_id: int
    content_type: str
    video_url: Optional[str] = None
    video_duration: Optional[int] = None
    description: Optional[str] = None
    article_text: Optional[str] = None
    quiz_questions: Optional[List[QuestionBase]] = None
