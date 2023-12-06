from re import A
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from src import course_section

from src.course.models import Course

from ..logger import logger
from ..exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException
from ..config.database import get_db
from .models import Section


class SectionService:
    """Service class for managing course sections."""

    @staticmethod
    def create_section(section_data):
        """Creates a new course section."""
        try:
            db = next(get_db())
            course = db.query(Course).filter(
                Course.id == section_data.course_id).first()
            if not course:
                raise NotFoundException(
                    f"Course with id {section_data.course_id} not found")

            course_sections = db.query(Section).filter(
                Section.course_id == section_data.course_id, Section.title == section_data.title).first()
            if course_sections:
                raise AlreadyExistsException(
                    f"Section with title {section_data.title} already exists for course with id {section_data.course_id}")

            max_order = db.query(func.max(Section.ordering)).filter(
                Section.course_id == section_data.course_id).scalar()
            new_order = 1 if max_order is None else max_order + 1
            section = Section(ordering=new_order, **section_data.dict())
            db.add(section)
            db.commit()
            db.refresh(section)
            return section
        except SQLAlchemyError as e:
            logger.error(e)
            db.rollback()
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def update_section(section_id, update_data):
        """Updates an existing course section."""
        try:
            db = next(get_db())
            section = db.query(Section).filter(
                Section.id == section_id).first()
            if not section:
                raise NotFoundException(
                    f"Section with id {section_id} not found")

            for key, value in update_data.dict(exclude_unset=True).items():
                if hasattr(section, key):
                    setattr(section, key, value)

            db.commit()
            db.refresh(section)
            return section
        except SQLAlchemyError as e:
            logger.error(e)
            db.rollback()
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_section(section_id):
        """Retrieves a specific course section by ID."""
        try:
            db = next(get_db())
            section = db.query(Section).filter(
                Section.id == section_id).first()
            if not section:
                raise NotFoundException(
                    f"Section with id {section_id} not found")
            return section
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_section_by_course_id(section_id, course_id):
        """Retrieves a specific course section by ID."""
        try:
            db = next(get_db())
            section = db.query(Section).filter(
                Section.id == section_id, Section.course_id == course_id).first()
            if not section:
                raise NotFoundException(
                    f"Section with id {section_id} for course with id {course_id} does not exist.")
            return section
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_sections(course_id):
        """Retrieves all course sections."""
        try:
            db = next(get_db())
            sections = db.query(Section).filter(
                Section.course_id == course_id).all()
            return sections
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def delete_section(section_id):
        """Deletes a specific course section."""
        try:
            db = next(get_db())
            section = db.query(Section).filter(
                Section.id == section_id).first()
            if not section:
                raise NotFoundException(
                    f"Section with id {section_id} not found")

            db.delete(section)
            db.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            db.rollback()
            raise DatabaseOperationException(str(e)) from e


# TODO: Handle ordering of sections during update or deletion
