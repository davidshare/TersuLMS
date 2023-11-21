from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.course.models import Course
from src.course_section.models import Section
from src.exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException, UniqueConstraintViolationException
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
            error_message = str(e.orig).lower()
            if "foreign key constraint" in error_message:
                raise DatabaseOperationException(
                    "Invalid section or course ID") from e
            elif "_course_section_ordering_uc" in error_message:
                raise UniqueConstraintViolationException(
                    "Duplicate ordering in the same section.") from e
            else:
                raise AlreadyExistsException(
                    f"The lesson {lesson.title} already exists.") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_lesson_by_id(lesson_id: int):
        """Handles getting lesson by id"""
        try:
            db = next(get_db())
            lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
            if not lesson:
                raise NotFoundException(
                    f"Lesson with id {lesson_id} not found.")
            return lesson
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def update_lesson(lesson_id: int, lesson_data: LessonCreate):
        """Handles updating lessons"""
        try:
            db = next(get_db())
            lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
            if not lesson:
                raise NotFoundException(
                    f"Lesson with id {lesson_id} not found.")
            
            for key, value in lesson_data.model_dump(exclude_unset=True).items():
                if hasattr(lesson, key):
                    setattr(lesson, key, value)

            db.commit()
            db.refresh(lesson)
            return lesson
        except IntegrityError as e:
            print(e)
            db.rollback()
            error_message = str(e.orig).lower()
            if "foreign key constraint" in error_message:
                raise DatabaseOperationException(
                    "Invalid section or course ID") from e
            elif "_course_section_ordering_uc" in error_message:
                raise UniqueConstraintViolationException(
                    "Duplicate ordering in the same section.") from e
            else:
                raise AlreadyExistsException(
                    f"The lesson {lesson.title} already exists.") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def delete_lesson(lesson_id: int):
        """Handles deleting lessons"""
        try:
            db = next(get_db())
            lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
            if not lesson:
                raise NotFoundException(
                    f"Lesson with id {lesson_id} not found.")
            db.delete(lesson)
            db.commit()
            return {"message": "Lesson deleted successfully."}
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e


#TODO: Ensure that ordering is reorganized after deleting a lesson