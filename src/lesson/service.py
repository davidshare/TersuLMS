from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.course.models import Course
from src.course_section.models import Section
from src.exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException, UniqueConstraintViolationException
from src.lesson.models import ArticleContent, FileContent, Lesson, QuizContent
from src.lesson.schemas import LessonCreate, QuizContentCreate
from ..config.database import get_db


class LessonService:
    """Service class for handling lessons"""

    @staticmethod
    def create_lesson(lesson_data: LessonCreate):
        """Handles creating lessons

        Args:
            lesson_data (LessonCreate): Lesson data

        Returns:
            Lesson: Lesson object
        """
        try:
            db = next(get_db())
            section = db.query(Section).filter(
                Course.id == lesson_data.course_id, Section.id == lesson_data.section_id).first()
            if not section:
                raise NotFoundException(
                    f"Section with id {lesson_data.section_id} that belongs to the course with id {lesson_data.course_id} not not found.")

            lesson = db.query(Lesson).filter(Lesson.section_id == lesson_data.section_id, Lesson.course_id ==
                                        lesson_data.course_id, Lesson.ordering == lesson_data.ordering).first()
            if lesson:
                raise AlreadyExistsException(
                    f"Lesson with ordering {lesson_data.ordering} already exists in section with id {lesson_data.section_id}.")
            lesson_dict = lesson_data.model_dump(exclude={'file_content', 'quiz_content', 'article_content'})
            filtered_lesson_data = {key: value for key, value in lesson_dict.items() if value is not None}
            lesson = Lesson(**filtered_lesson_data)
            db.add(lesson)
            db.flush()

            if lesson_data.content_type == "video" or lesson_data.content_type == "pdf":
                file_content = FileContent(
                    url=lesson_data.file_content.url, lesson_id=lesson.id)
                db.add(file_content)

            elif lesson_data.content_type == "article":
                article_content = ArticleContent(
                    content=lesson_data.article_content.content, lesson_id=lesson.id)
                db.add(article_content)
            
            elif lesson_data.content_type == "quiz":
                for question_data in lesson_data.quiz_content.questions:
                    quiz_content = QuizContent(
                        lesson_id=lesson.id, **question_data.model_dump())
                    db.add(quiz_content)
            
            db.commit()
            db.refresh(lesson)
            return lesson

        except IntegrityError as e:
            db.rollback()
            error_message = str(e.orig).lower()
            if "foreign key constraint" in error_message:
                raise DatabaseOperationException(
                    "Invalid section or course ID") from e
            elif "_course_section_ordering_uc" in error_message:
                raise UniqueConstraintViolationException(
                    "Duplicate ordering in the same section.") from e
            elif "file_content_url_key" in error_message:
                print(e)
                raise AlreadyExistsException(
                    f"The file {lesson_data.file_content.url} already exists.") from e
            else:
                print(e)
                raise AlreadyExistsException(
                    f"The lesson {lesson_data.title} already exists.") from e
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

    @staticmethod
    def create_file_content(lesson_id: int, url: str):
        """
        Handles creating file content for lessons
        
        Args:
            lesson_id (int): Lesson ID
            url (str): URL to file
        
        Returns:
            Lesson: Lesson object
        """
        try:
            db = next(get_db())
            lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
            if not lesson:
                raise NotFoundException(
                    f"Lesson with id {lesson_id} not found.")

            file_content = FileContent(url=url, lesson_id=lesson_id)
            db.add(file_content)
            db.commit()
            db.refresh(file_content)
            return lesson
        except IntegrityError as e:
            db.rollback()
            raise AlreadyExistsException(
                f"File content for lesson with id {lesson_id} already exists.") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def create_article_content(lesson_id: int, content: str):
        """
        Handles creating article content for lessons
        
        Args:
            lesson_id (int): Lesson ID
            content (str): Article content
        
        Returns:
            Lesson: Lesson object
        """
        try:
            db = next(get_db())
            lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
            if not lesson:
                raise NotFoundException(
                    f"Lesson with id {lesson_id} not found.")

            article_content = ArticleContent(
                content=content, lesson_id=lesson_id)
            db.add(article_content)
            db.commit()
            db.refresh(article_content)
            return lesson
        except IntegrityError as e:
            db.rollback()
            raise AlreadyExistsException(
                f"Article content for lesson with id {lesson_id} already exists.") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def create_quiz_content(quiz_content_data: QuizContentCreate):
        """
        Handles creating quiz content for lessons

        Args:
            quiz_content_data (QuizContentCreate): Quiz content data

        Returns:
            quiz_content: Quiz content object
        """
        try:
            db = next(get_db())
            lesson = db.query(Lesson).filter(
                Lesson.id == quiz_content_data.lesson_id).first()
            if not lesson:
                raise NotFoundException(
                    f"Lesson with id {quiz_content_data.lesson_id} not found.")

            created_quiz_contents = []
            for question_data in quiz_content_data.questions:
                quiz_content = QuizContent(
                    lesson_id=quiz_content_data.lesson_id, **question_data.dict())
                db.add(quiz_content)
                db.flush()
                created_quiz_contents.append(quiz_content)

            db.commit()
            return created_quiz_contents
        except IntegrityError as e:
            db.rollback()
            raise AlreadyExistsException(
                f"Quiz content for lesson with id {quiz_content_data.lesson_id} already exists.") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

# TODO: Ensure that ordering is reorganized after deleting a lesson
