from fastapi import HTTPException

from .schemas import LessonCreate
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
    def delete_lesson(lesson_id: int):
        """Handles deleting lesson by id"""
        try:
            return LessonService.delete_lesson(lesson_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
