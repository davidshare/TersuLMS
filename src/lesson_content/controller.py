from fastapi import HTTPException
from src.exceptions import DatabaseOperationException, NotFoundException
from src.lesson_content.schemas import ArticleContentCreate, QuizContentCreate, VideoContentCreate
from src.lesson_content.service import LessonContentService


class LessonContentController:
    """Lesson Content Controller Class"""

    @staticmethod
    def create_article_content(lesson_content_data: ArticleContentCreate):
        """Handles creating lesson content"""
        try:
            return LessonContentService.create_article_content(lesson_content_data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def create_video_content(video_content_data: VideoContentCreate):
        """Handles creating lesson content"""
        try:
            return LessonContentService.create_video_content(video_content_data)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def create_quiz_content(quiz_content_data: QuizContentCreate):
        """Handles creating lesson content"""
        try:
            return LessonContentService.create_quiz_content(quiz_content_data)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
