from fastapi import HTTPException
from .service import CourseCategoryService
from ..exceptions import (
    AlreadyExistsException, DatabaseOperationException, NotFoundException
)

class CourseCategoryController:
    """Controller class for handling course categories."""
    @staticmethod
    def create_course_category(name: str, description: str):
        """Handles creating course categories"""
        try:
            return CourseCategoryService.create_course_category(name, description)
        except AlreadyExistsException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_course_categories():
        """Handles getting all course categories"""
        try:
            return CourseCategoryService.get_course_categories()
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_course_category_by_id(category_id: int):
        """Handles getting a course category by id"""
        try:
            return CourseCategoryService.get_course_category_by_id(category_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def update_course_category(category_id: int, name: str, description: str):
        """Updates a course category using the provided data."""
        try:
            updated_category = CourseCategoryService.update_course_category(
                category_id, name, description)
            return updated_category
        except Exception as e:
            # Handle exceptions (like NotFound, AlreadyExists, etc.)
            print(f"Error updating course category: {e}")
            raise e

    @staticmethod
    def delete_course_category(category_id: int):
        """Handles deleting a course category by id"""
        try:
            return CourseCategoryService.delete_course_category(category_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
