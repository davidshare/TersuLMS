from fastapi import HTTPException

from .schemas import LessonCreate
from ..exceptions import AlreadyExistsException, DatabaseOperationException
from .service import LessonService

class LessonController:
    """Lesson controller class"""

    @staticmethod
    def create_lesson(lesson_data: LessonCreate):
        """Handles creating lessons"""
        try:
            return LessonService.create_lesson(lesson_data)
        except AlreadyExistsException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e