from fastapi import HTTPException
from .schemas import CourseCreate, CourseUpdate
from ..exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException
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
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def get_course_by_slug(slug: str):
        """Handles getting courses by slug"""
        try:
            return CourseService.get_course_by_slug(slug)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def get_course_by_id(course_id: int):
        """Handles getting courses by id"""
        try:
            return CourseService.get_course_by_id(course_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def get_courses():
        """Handles getting all courses"""
        try:
            return CourseService.get_courses()
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def update_course_by_id(course_id: int, course_data: CourseUpdate):
        """Handles updating a course by id"""
        try:
            return CourseService.update_course_by_id(course_id, course_data)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def delete_course_by_id(course_id: int):
        """Handles deleting a course by id"""
        try:
            return CourseService.delete_course_by_id(course_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

