from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.course.models import Course
from src.course_section.models import Section
from src.exceptions import (
    AlreadyExistsException, DatabaseOperationException,
    NotFoundException, UniqueConstraintViolationException
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
            lesson_dict = lesson_data.model_dump(
                exclude={'file_content', 'quiz_content', 'article_content'})
            filtered_lesson_data = {
                key: value for key, value in lesson_dict.items() if value is not None}
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

            question = db.query(QuizContent).filter(QuizContent.lesson_id ==
                                                    quiz_content.lesson_id, QuizContent.id == quiz_content_id).first()
            if not question:
                raise NotFoundException(
                    "The question you are trying to update does not exist")

            if quiz_content.question is not None:
                question.question = quiz_content.question

            if quiz_content.answer is not None:
                question.answer = quiz_content.answer

            if quiz_content.option_1 is not None:
                question.option_1 = quiz_content.option_1

            if quiz_content.option_2 is not None:
                question.option_2 = quiz_content.option_2

            if quiz_content.option_3 is not None:
                question.option_3 = quiz_content.option_3

            if quiz_content.option_4 is not None:
                question.option_4 = quiz_content.option_4

            db.commit()
            db.refresh(question)
            return question
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

# TODO: Ensure that ordering is reorganized after deleting a lesson
