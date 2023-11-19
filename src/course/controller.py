from fastapi import HTTPException
from .schemas import CourseCreate
from ..exceptions import AlreadyExistsException, DatabaseOperationException
from .service import CourseService


class CourseController:
    """Course controller class"""

    @staticmethod
    def create_course(course_data: CourseCreate):
        """Handles creating courses"""
        try:
            return CourseService.create_course(course_data)
        except AlreadyExistsException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

