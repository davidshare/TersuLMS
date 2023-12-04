from fastapi import HTTPException

from .schemas import ArticleContentUpdate, FileContentUpdate, LessonCreate, QuizContentUpdate
from ..exceptions import (
    AlreadyExistsException, DatabaseOperationException,
    NotFoundException, UniqueConstraintViolationException
)
from .service import LessonService


class LessonController:
    """Lesson controller class"""

    @staticmethod
    def create_lesson(lesson_data: LessonCreate):
        """Handles creating lessons"""
        try:
            return LessonService.create_lesson(lesson_data)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except UniqueConstraintViolationException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except AlreadyExistsException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_lesson_by_id(lesson_id: int):
        """Handles getting lesson by id"""
        try:
            return LessonService.get_lesson_by_id(lesson_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def update_lesson(lesson_id: int, lesson_data: LessonCreate):
        """Handles updating lesson by id"""
        try:
            return LessonService.update_lesson(lesson_id, lesson_data)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except UniqueConstraintViolationException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except AlreadyExistsException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def update_file_content(file_content_id: int, file_content: FileContentUpdate):
        """
        Handles updating file content

        Args:
            file_content_id (int): File content id
            file_content (FileContent): File content data

        Returns:
            Filecontent: Filecontent object
        """
        try:
            return LessonService.update_file_content(file_content_id, file_content)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def update_article_content(article_content_id: int, article_content: ArticleContentUpdate):
        """
        Handles updating article content

        Args:
            article_content_id (int): Article content id
            article_content (ArticleContent): Article content data

        Returns:
            ArticleContent: ArticleContent object
        """
        try:
            return LessonService.update_article_content(article_content_id, article_content)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def update_quiz_content(quiz_content_id: int, quiz_content: QuizContentUpdate):
        """
        Handles updating quiz content

        Args:
            quiz_content_id (int): Quiz content id
            quiz_content (QuizContent): Quiz content data

        Returns:
            QuizContent: QuizContent object
        """
        try:
            return LessonService.update_quiz_content(quiz_content_id, quiz_content)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def delete_lesson(lesson_id: int):
        """Handles deleting lesson by id"""
        try:
            return LessonService.delete_lesson(lesson_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
