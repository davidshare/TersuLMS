from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.course.models import Course
from src.course_section.models import Section
from src.exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException
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

            course_exists = db.query(Course).filter(
                Course.id == lesson.course_id).first()
            if not course_exists:
                raise NotFoundException(
                    f"Course with id {lesson.course_id} not found.")

            section_exists = db.query(Section).filter(
                Section.id == lesson.section_id).first()
            if not section_exists:
                raise NotFoundException(
                    f"Section with id {lesson.section_id} not found.")

            lesson = Lesson(**lesson.model_dump())
            db.add(lesson)
            db.commit()
            db.refresh(lesson)
            return lesson
        except IntegrityError as e:
            print(e)
            db.rollback()
            if "foreign key constraint" in str(e.orig).lower():
                print(f"ForeignKeyViolation: {e}")
                raise DatabaseOperationException(
                    "Invalid section or course ID") from e
            else:
                raise AlreadyExistsException(
                    f"The lesson {lesson.title} already exists for this section.") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e
