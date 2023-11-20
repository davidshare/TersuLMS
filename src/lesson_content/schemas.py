from pydantic import BaseModel
from typing import Optional, List

class LessonContentBase(BaseModel):
    """Base model for LessonContent objects"""
    lesson_id: int
    content_type: str

class VideoContentCreate(LessonContentBase):
    """VideoContentCreate model"""
    video_url: str
    video_duration: int

class VideoContentUpdate(BaseModel):
    """VideoContentUpdate model"""
    video_url: Optional[str] = None
    video_duration: Optional[int] = None

class VideoContentResponse(VideoContentCreate):
    """VideoContentResponse model"""
    id: int

class ArticleContentCreate(LessonContentBase):
    """ArticleContentCreate model"""
    article_text: str

class ArticleContentUpdate(BaseModel):
    """ArticleContentUpdate model"""
    article_text: Optional[str] = None

class ArticleContentResponse(ArticleContentCreate):
    """ArticleContentResponse model"""
    id: int

class QuestionBase(BaseModel):
    """Base model for Question objects"""
    question_text: str
    options: List[str]
    correct_option: int


class QuizContentCreate(LessonContentBase):
    """QuizContentCreate model"""
    quiz_questions: List[QuestionBase]

class QuizContentUpdate(BaseModel):
    """QuizContentUpdate model"""
    quiz_questions: Optional[List[QuestionBase]] = None

class QuizContentResponse(QuizContentCreate):
    """QuizContentResponse model"""
    id: int

class QuizOptionCreate(BaseModel):
    """QuizOptionCreate model"""
    text: str
    is_correct: bool

class QuizOptionUpdate(BaseModel):
    """QuizOptionUpdate model"""
    text: Optional[str] = None
    is_correct: Optional[bool] = None

class QuizOptionResponse(QuizOptionCreate):
    """QuizOptionResponse model"""
    id: int
    question_id: int

    class Config:
        orm_mode = True



