from typing import Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..logger import logger
from .models import CourseCategory
from ..config.database import get_db
from ..exceptions import (
    AlreadyExistsException, DatabaseOperationException, NotFoundException
)


class CourseCategoryService:
    """Service class for handling course categories."""

    @staticmethod
    def create_course_category(name: str, description: str):
        """Handles creating course categories"""
        try:
            db = next(get_db())
            course_category = CourseCategory(
                name=name, description=description)
            db.add(course_category)
            db.commit()
            db.refresh(course_category)
            return course_category
        except IntegrityError as e:
            logger.error(e)
            db.rollback()
            raise AlreadyExistsException(
                f"The course category {name} already exists.") from e
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_course_categories():
        """Handles getting all course categories"""
        try:
            db = next(get_db())
            course_categories = db.query(CourseCategory).all()
            return course_categories
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_course_category_by_id(category_id: int):
        """Handles getting a course category by id"""
        try:
            db = next(get_db())
            course_category = db.query(CourseCategory).filter(
                CourseCategory.id == category_id).first()
            if not course_category:
                raise NotFoundException(
                    f"The course category with id {category_id} does not exist.")
            return course_category
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def update_course_category(category_id: int, name: Optional[str] = None, description: Optional[str] = None):
        """Handles updating a course category by id. Can update name, description, or both."""
        try:
            db = next(get_db())
            course_category = db.query(CourseCategory).filter(
                CourseCategory.id == category_id).first()
            if not course_category:
                raise NotFoundException(
                    f"The course category with id {category_id} does not exist.")

            if name is not None:
                course_category.name = name
            if description is not None:
                course_category.description = description

            db.commit()
            db.refresh(course_category)
            return course_category
        except IntegrityError as e:
            logger.error(e)
            db.rollback()
            raise AlreadyExistsException(
                f"A course category with the name {name} already exists.") from e
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def delete_course_category(category_id: int):
        """Handles deleting a course category by id"""
        try:
            db = next(get_db())
            course_category = db.query(CourseCategory).filter(
                CourseCategory.id == category_id).first()
            if not course_category:
                raise NotFoundException(
                    f"The course category with id {category_id} does not exist.")
            db.delete(course_category)
            db.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e
