from fastapi import APIRouter, status

from src.lesson_content.controller import LessonContentController
from src.lesson_content.schemas import (
    ArticleContentCreate, ArticleContentResponse, QuizContentCreate,
    QuizContentResponse, VideoContentCreate, VideoContentResponse
)

router = APIRouter()

@router.post("/video/", status_code=status.HTTP_201_CREATED, response_model=VideoContentResponse)
def create_lesson_content(video_content_data: VideoContentCreate):
    """Handles creating lesson content"""
    return LessonContentController.create_video_content(video_content_data)


@router.post("/article/", status_code=status.HTTP_201_CREATED, response_model=ArticleContentResponse)
def create_article_content(article_content_data: ArticleContentCreate):
    """Handles creating lesson content"""
    return LessonContentController.create_article_content(article_content_data)


@router.post("/quiz/", status_code=status.HTTP_201_CREATED, response_model=QuizContentResponse)
def create_quiz_content(quiz_content_data: QuizContentCreate):
    """Handles creating lesson content"""
    return LessonContentController.create_quiz_content(quiz_content_data)
