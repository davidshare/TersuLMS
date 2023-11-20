from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.exceptions import AlreadyExistsException, DatabaseOperationException
from src.lesson.models import Lesson
from src.lesson.schemas import LessonCreate
from ..config.database import get_db


class LessonService:
    """Service class for handling lessons"""

    @staticmethod
    def create_lesson(lesson: LessonCreate):
        """Handles creating lessons"""
        try:
            db = next(get_db())
            lesson = Lesson(**lesson.model_dump())
            db.add(lesson)
            db.commit()
            db.refresh(lesson)
            return lesson
        except IntegrityError as e:
            db.rollback()
            raise AlreadyExistsException(
                f"The lesson {lesson.title} already exists.") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e
