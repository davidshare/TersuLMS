import traceback
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.course.models import Course
from src.course_section.models import Section
from src.exceptions import (
    AlreadyExistsException, DatabaseOperationException,
    NotFoundException, NotNullViolationException, UniqueConstraintViolationException
)
from src.lesson.models import ArticleContent, FileContent, Lesson, QuizContent
from src.lesson.schemas import ArticleContentUpdate, LessonCreate
from ..config.database import get_db
from ..logger import logger


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
            
            LessonService.check_lesson_exits(lesson_data.section_id, lesson_data.title)
            
            max_order = db.query(func.max(Lesson.ordering)).filter(
                Lesson.section_id == lesson_data.section_id).scalar()
            new_order = 1 if max_order is None else max_order + 1

            created_lesson = LessonService.create_lesson_object(lesson_data, new_order)
            db.add(created_lesson)
            db.flush()

            if lesson_data.content_type in ["video", "pdf"]:
                LessonService.create_file_content(db,
                                                  created_lesson.id, lesson_data.file_content)
            elif lesson_data.content_type == "article":
                LessonService.create_article_content(
                    db, created_lesson.id, lesson_data.article_content)
            elif lesson_data.content_type == "quiz":
                LessonService.create_quiz_content(db,
                                                  created_lesson.id, lesson_data.quiz_content)
            db.commit()
            db.refresh(created_lesson)
            return created_lesson
        except Exception as e:
            logger.error(e)
            db.rollback()
            LessonService.handle_create_lesson_exceptions(e)

    @staticmethod
    def create_file_content(db, lesson_id: int, file_content: FileContent):
        """
        Handles creating file content

        Args:
            file_content (FileContent): File content data

        Returns:
            FileContent: FileContent object
        """
        file_content = FileContent(url=file_content.url, lesson_id=lesson_id)
        db.add(file_content)

    @staticmethod
    def create_article_content(db, lesson_id: int, article_content: ArticleContent):
        """
        Handles creating article content

        Args:
            article_content (ArticleContent): Article content data

        Returns:
            ArticleContent: ArticleContent object
        """
        article_content = ArticleContent(
            content=article_content.content, lesson_id=lesson_id)
        db.add(article_content)

    @staticmethod
    def create_quiz_content(db, lesson_id: int, quiz_content: QuizContent):
        """
        Handles creating quiz content

        Args:
            quiz_content (QuizContent): Quiz content data

        Returns:
            QuizContent: QuizContent object
        """
        try:
            created_quiz_contents = []
            for question_data in quiz_content.questions:
                question = QuizContent(
                    lesson_id=lesson_id, **question_data.model_dump())
                db.add(question)
                created_quiz_contents.append(quiz_content)
            return created_quiz_contents
        except SQLAlchemyError as e:
            logger.error(e)
            db.rollback()
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def create_question(lesson_id: int, question_data: QuizContent):
        """
        Handles creating a quiz question

        Args:
            lesson_id (int): Lesson id
            question_data (QuizContent): Quiz question data

        Returns:
            QuizContent: QuizContent object
        """
        try:
            db = next(get_db())

            question = LessonService.create_quiz_content(
                db, lesson_id, question_data)
            db.commit()
            db.refresh(question)
            return question
        except SQLAlchemyError as e:
            logger.error(e)
            db.rollback()
            raise DatabaseOperationException(str(e)) from e

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
    def check_lesson_exits(section_id, title):
        """
        Checks if a lesson exists in the section
        
        Args:
            section_id (int): Section id
            title (str): Lesson title
            
            Raises:
                AlreadyExistsException: If the lesson already exists
        """
        db = next(get_db())
        lesson = db.query(Lesson).filter(
            Lesson.section_id == section_id, Lesson.title == title).first()
        if lesson:
            raise AlreadyExistsException(
                f"The lesson with title {title} already exists in the section.")

    @staticmethod
    def check_quiz_exists(lesson_id: int, question: str):
        """
        Checks if a quiz exists in the lesson
        
        Args:
            lesson_id (int): Lesson id
            question (str): question
            
            Raises:
                AlreadyExistsException: If the question already exists
        """
        db = next(get_db())
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            raise NotFoundException(
                f"The quiz with id {lesson_id} you are trying to add a question to does not exist.")

        existing_questions = db.query(QuizContent).filter(
            QuizContent.question == question).first()
        if existing_questions:
            raise AlreadyExistsException(
                f"The question {question} already exists in the quiz.")

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
        traceback.print_exc()
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
    def create_lesson_object(lesson_data: LessonCreate, ordering):
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
        return Lesson(ordering=ordering, **filtered_lesson_data)

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
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e
        
    @staticmethod
    def get_lessons_by_course_id(course_id: int):
        """Handles getting lessons by course id"""
        try:
            db = next(get_db())
            course = db.query(Course).filter(Course.id == course_id).first()
            if not course:
                raise NotFoundException(f"The course with id {course_id} does not exist.")
            
            lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
            return lessons
        except SQLAlchemyError as e:
            logger.error(e)
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
            logger.error(e)
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
            logger.error(e)
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
            logger.error(e)
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
            logger.error(e)
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
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def delete_lesson(lesson_id: int):
        """
        Handles deleting lessons
        
        Args:
            lesson_id (int): Lesson id
        
        Returns:
            dict: Response message
        """
        try:
            db = next(get_db())
            found_lesson = db.query(Lesson).filter(
                Lesson.id == lesson_id).first()
            if not found_lesson:
                raise NotFoundException(
                    f"Lesson with id {lesson_id} not found.")
            if found_lesson.content_type in ["video", "pdf"]:
                LessonService.delete_file_content(found_lesson.id)
            elif found_lesson.content_type == "article":
                LessonService.delete_article_content(found_lesson.id)
            elif found_lesson.content_type == "quiz":
                LessonService.delete_quiz_content(found_lesson.id)
            db.delete(found_lesson)
            db.commit()
            return {"message": "Lesson deleted successfully."}
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def delete_file_content(lesson_id: int):
        """
        Handles deleting file content
        
        Args:
            lesson_id (int): File lesson id

        Returns:
            dict: Response message
        """
        try:
            db = next(get_db())
            file = db.query(FileContent).filter(
                FileContent.lesson_id == lesson_id).first()
            if not file:
                raise NotFoundException(
                    f"File content with lesson_id {lesson_id} not found.")
            db.delete(file)
            db.commit()
            return {"message": "File content deleted successfully."}
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def delete_article_content(lesson_id: int):
        """
        Handles deleting article content
        
        Args:
            lesson_id (int): Article lesson id

        Returns:
            dict: Response message
        """
        try:
            db = next(get_db())
            article = db.query(ArticleContent).filter(
                ArticleContent.lesson_id == lesson_id).first()
            if not article:
                raise NotFoundException(
                    f"Article content with lesson_id {lesson_id} not found.")
            db.delete(article)
            db.commit()
            return {"message": "Article content deleted successfully."}
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def delete_quiz_content(lesson_id: int):
        """
        Handles deleting quiz content
        
        Args:
            lesson_id (int): Quiz lesson id

        Returns:
            dict: Response message
        """
        try:
            db = next(get_db())
            question = db.query(QuizContent).filter(
                QuizContent.lesson_id == lesson_id).first()
            if not question:
                raise NotFoundException(
                    f"Quiz content with lesson_id {lesson_id} not found.")
            db.delete(question)
            db.commit()
            return {"message": "Quiz content deleted successfully."}
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseOperationException(str(e)) from e

# TODO: Ensure that ordering is reorganized after deleting a lesson
