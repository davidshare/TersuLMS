from sqlalchemy.exc import IntegrityError, SQLAlchemyError

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
            db.rollback()
            raise AlreadyExistsException(
                f"The slug {course_data.slug} already exists.") from e
        except SQLAlchemyError as e:
            print(e)
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
            print(e)
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
                raise NotFoundException(f"Course with id {course_id} does not exist.")
            return course
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e
