from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .models import Course
from .schemas import CourseCreate
from ..exceptions import AlreadyExistsException, DatabaseOperationException
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
