from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src import lesson
from src.course.models import Course
from src.course_section.models import Section
from src.exceptions import (
    AlreadyExistsException, DatabaseOperationException,
    NotFoundException, NotNullViolationException, UniqueConstraintViolationException
)
from src.lesson.models import ArticleContent, FileContent, Lesson, QuizContent
from src.lesson.schemas import ArticleContentUpdate, LessonCreate
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
            LessonService.validate_section(
                lesson_data.course_id, lesson_data.section_id)
            LessonService.check_existing_lesson(
                lesson_data.course_id, lesson_data.section_id, lesson_data.ordering)
            created_lesson = LessonService.create_lesson_object(lesson_data)
            db.add(created_lesson)
            db.flush()

            if lesson_data.content_type in ["video", "pdf"]:
                LessonService.create_file_content(
                    created_lesson.id, lesson_data.file_content)
            elif lesson_data.content_type == "article":
                LessonService.create_article_content(
                    created_lesson.id, lesson_data.article_content)
            elif lesson_data.content_type == "quiz":
                LessonService.create_quiz_content(
                    created_lesson.id, lesson_data.quiz_content)

            db.commit()
            db.refresh(lesson)
            return lesson
        except Exception as e:
            db.rollback()
            LessonService.handle_create_lesson_exceptions(e)

    @staticmethod
    def create_file_content(lesson_id: int, file_content: FileContent):
        """
        Handles creating file content

        Args:
            file_content (FileContent): File content data

        Returns:
            FileContent: FileContent object
        """
        db = next(get_db())
        file_content = FileContent(url=file_content.url, lesson_id=lesson_id)
        db.add(file_content)

    @staticmethod
    def create_article_content(lesson_id: int, article_content: ArticleContent):
        """
        Handles creating article content

        Args:
            article_content (ArticleContent): Article content data

        Returns:
            ArticleContent: ArticleContent object
        """
        db = next(get_db())
        article_content = ArticleContent(
            content=article_content.content, lesson_id=lesson_id)
        db.add(article_content)

    @staticmethod
    def create_quiz_content(lesson_id: int, quiz_content: QuizContent):
        """
        Handles creating quiz content

        Args:
            quiz_content (QuizContent): Quiz content data

        Returns:
            QuizContent: QuizContent object
        """
        db = next(get_db())
        for question_data in quiz_content.questions:
            quiz_content = QuizContent(
                lesson_id=lesson_id, **question_data.model_dump())
            db.add(quiz_content)

    @staticmethod
    def validate_section(course_id, section_id):
        """
        Validates that the section belongs to the course
        
        Args:
            course_id (int): Course id
            section_id (int): Section id
            
            Raises:
                NotFoundException: If the section does not exist
        """
        db = next(get_db())
        section = db.query(Section).filter(
            Section.course_id == course_id, Section.id == section_id).first()
        if not section:
            raise NotFoundException(
                f"Section with id {section_id} that belongs to the course with id {course_id} not found.")

    @staticmethod
    def check_existing_lesson(course_id: int, section_id: int,  ordering: int):
        """
        Checks if a lesson already exists in the section with the given ordering
        
        Args:
            section_id (int): Section id
            course_id (int): Course id
            ordering (int): Lesson ordering
            
            Raises:
                AlreadyExistsException: If the lesson already exists
        """
        db = next(get_db())
        found_lesson = db.query(Lesson).filter(Lesson.course_id == course_id,
                                               Lesson.section_id == section_id, Lesson.ordering == ordering).first()
        if found_lesson:
            raise AlreadyExistsException(
                f"Lesson with ordering {ordering} already exists in section with id {section_id} that belongs to the course with id {course_id}")

    @staticmethod
    def handle_create_lesson_exceptions(exception):
        """
        Handles exceptions that occur when creating a lesson

        Args:
            exception (Exception): Exception object

        Raises:
            DatabaseOperationException: If a database error occurs
            AlreadyExistsException: If the lesson already exists
            UniqueConstraintViolationException: If a unique constraint is violated
            NotNullViolationException: If a required field is missing or null
        """
        if isinstance(exception, IntegrityError):
            print(exception)
            if "foreign key constraint" in str(exception.orig).lower():
                raise DatabaseOperationException(
                    "Invalid section or course ID") from exception
            elif "_course_section_ordering_uc" in str(exception.orig).lower():
                raise UniqueConstraintViolationException(
                    "Duplicate ordering in the same section.") from exception
            elif "file_content_url_key" in str(exception.orig).lower():
                raise AlreadyExistsException(
                    "The file already exists.") from exception
            elif "not-null constraint" in str(exception.orig).lower():
                raise NotNullViolationException(
                    "A required field is missing or null.") from exception
            elif "unique_section_lesson" in str(exception.orig).lower():
                raise AlreadyExistsException(
                    "A lesson with the title already exists.") from exception
            else:
                raise DatabaseOperationException(
                    f"A database error occurred.{exception}") from exception
        elif isinstance(exception, SQLAlchemyError):
            raise DatabaseOperationException(
                "A database error occurred.") from exception
        else:
            raise exception

    @staticmethod
    def create_lesson_object(lesson_data: LessonCreate):
        """
        Creates a lesson object
        
        Args:
            lesson_data (LessonCreate): Lesson data
            
        Returns:
            Lesson: Lesson object
        """
        lesson_dict = lesson_data.model_dump(
            exclude={'file_content', 'quiz_content', 'article_content'})
        if lesson_data.content_type != "quiz":
            lesson_dict['quiz_attempts_allowed'] = 0
        filtered_lesson_data = {
            key: value for key, value in lesson_dict.items() if value is not None}
        return Lesson(**filtered_lesson_data)

    @staticmethod
    def get_lesson_by_id(lesson_id: int):
        """Handles getting lesson by id"""
        try:
            db = next(get_db())
            found_lesson = db.query(Lesson).filter(
                Lesson.id == lesson_id).first()
            if not found_lesson:
                raise NotFoundException(
                    f"Lesson with id {lesson_id} not found.")
            return found_lesson
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
                if key == 'quiz_attempts_allowed' and lesson.content_type != "quiz":
                    continue
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
    def update_file_content(file_content_id: int, file_content: FileContent):
        """
        Handles updating file content

        Args:
            file_content_id (int): File content id
            file_content (FileContent): File content data

        Returns:
            Filecontent: Filecontent object
        """
        try:
            db = next(get_db())

            file = db.query(FileContent).filter(FileContent.lesson_id ==
                                                file_content.lesson_id, FileContent.id == file_content_id).first()
            if not file:
                raise NotFoundException(
                    "The file you are trying to update does not exist")

            if file_content.url is not None:
                file.url = file_content.url

            db.commit()
            db.refresh(file)
            return file
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def update_article_content(article_content_id: int, article_content: ArticleContentUpdate):
        """
        Handles updating article content

        Args:
            article_content_id (int): Article content id
            article_content (ArticleContent): Article content data

        Returns:
            ArticleContent: ArticleContent object
        """
        try:
            db = next(get_db())

            article = db.query(ArticleContent).filter(ArticleContent.lesson_id ==
                                                      article_content.lesson_id, ArticleContent.id == article_content_id).first()
            if not article:
                raise NotFoundException(
                    "The article you are trying to update does not exist")

            if article_content.content is not None:
                article.content = article_content.content

            db.commit()
            db.refresh(article)
            return article
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def update_quiz_content(quiz_content_id: int, quiz_content: QuizContent):
        """
        Handles updating quiz content

        Args:
            quiz_content_id (int): Quiz content id
            quiz_content (QuizContent): Quiz content data

        Returns:
            QuizContent: QuizContent object
        """
        try:
            db = next(get_db())
            question = db.query(QuizContent).filter_by(
                id=quiz_content_id, lesson_id=quiz_content.lesson_id).first()
            if not question:
                raise NotFoundException(
                    "The question you are trying to update does not exist")

            for attr in ['question', 'answer', 'option_1', 'option_2', 'option_3', 'option_4']:
                if getattr(quiz_content, attr) is not None:
                    setattr(question, attr, getattr(quiz_content, attr))

            db.commit()
            db.refresh(question)
            return question
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

# TODO: Ensure that ordering is reorganized after deleting a lesson
