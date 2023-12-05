from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..logger import logger

from .models import Course
from .schemas import CourseCreate
from ..exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException
from ..config.database import get_db


class CourseService:
    """Service class for handling courses."""

    @staticmethod
    def create_course(course_data: CourseCreate):
        """
        Handles creating courses
        """
        try:
            db = next(get_db())
            course = Course(**course_data.model_dump())
            db.add(course)
            db.commit()
            db.refresh(course)
            return course
        except IntegrityError as e:
            logger.error(e)
            db.rollback()
            raise AlreadyExistsException(
                f"The slug {course_data.slug} already exists.") from e
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_course_by_slug(slug: str):
        """
        Handles getting courses by slug
        """
        try:
            db = next(get_db())
            course = db.query(Course).filter(Course.slug == slug).first()
            if not course:
                raise NotFoundException(
                    f"Course with slug {slug} does not exist.")
            return course
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_course_by_id(course_id: int):
        """
        Handles getting courses by id
        """
        try:
            db = next(get_db())
            course = db.query(Course).filter(Course.id == course_id).first()
            if not course:
                raise NotFoundException(
                    f"Course with id {course_id} does not exist.")
            return course
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_courses():
        """
        Handles getting all courses
        """
        try:
            db = next(get_db())
            courses = db.query(Course).all()
            return courses
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def update_course_by_id(course_id: int, course_data):
        """Updates a course based on the given data."""
        try:
            db = next(get_db())
            course = db.query(Course).filter(Course.id == course_id).first()
            if not course:
                raise NotFoundException(f"Course with id {course_id} not found")

            # Iterate through the dictionary and update only if the value is not None
            for key, value in course_data.dict(exclude_unset=True).items():
                if hasattr(course, key) and key != 'slug' and value is not None:
                    setattr(course, key, value)

            db.commit()
            db.refresh(course)
            return course
        except IntegrityError as e:
            logger.error(e)
            db.rollback()
            raise AlreadyExistsException(f"Conflict in updating course {course_id}.") from e
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e
        
    @staticmethod
    def delete_course_by_id(course_id: int):
        """Deletes a course by id."""
        try:
            db = next(get_db())
            course = db.query(Course).filter(Course.id == course_id).first()
            if not course:
                raise NotFoundException(f"Course with id {course_id} not found")

            db.delete(course)
            db.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e
