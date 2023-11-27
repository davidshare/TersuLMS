from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from src.config.database import get_db
from src.exceptions import (
    DatabaseOperationException, NotFoundException,
)
from src.lesson.models import Lesson
from src.lesson_content.models import (
    ArticleContent, QuizContent, QuizOption, QuizQuestions, VideoContent
)
from src.lesson_content.schemas import (
    ArticleContentCreate, QuizContentCreate, VideoContentCreate
)


class LessonContentService:
    """Service class for handling lesson content"""

    @staticmethod
    def create_video_content(video_content_data: VideoContentCreate):
        """Handles creating lesson content"""
        try:
            db = next(get_db())

            lesson = db.query(Lesson).filter(
                Lesson.id == video_content_data.lesson_id).first()
            if not lesson:
                raise NotFoundException(
                    f"Lesson with id {video_content_data.lesson_id} not found")

            video_content = VideoContent(**video_content_data.model_dump())
            db.add(video_content)
            db.commit()
            db.refresh(video_content)
            return video_content
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def create_article_content(article_content_data: ArticleContentCreate):
        """Handles creating lesson content"""
        try:
            db = next(get_db())

            lesson = db.query(Lesson).filter(
                Lesson.id == article_content_data.lesson_id).first()
            if not lesson:
                raise NotFoundException(
                    f"Lesson with id {article_content_data.lesson_id} not found")

            article_content = ArticleContent(
                **article_content_data.model_dump())
            db.add(article_content)
            db.commit()
            db.refresh(article_content)
            return article_content
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def create_quiz_content(quiz_content_data: QuizContentCreate):
        """
        Handles creating quiz content with unique questions and their options.
        :param quiz_content_data: QuizContentCreate, data for creating the quiz content, including questions and options.
        :return: QuizContent, the created quiz content.
        """
        try:
            db = next(get_db())
            # Check if the associated lesson exists
            lesson = db.query(Lesson).filter(Lesson.id == quiz_content_data.lesson_id).first()
            if not lesson:
                raise NotFoundException(f"Lesson with id {quiz_content_data.lesson_id} not found")

            # Create quiz content
            quiz_content = QuizContent(
                lesson_id=quiz_content_data.lesson_id, 
                attempts_allowed=quiz_content_data.attempts_allowed, 
                published=quiz_content_data.published
            )
            db.add(quiz_content)
            db.flush()

            # Add unique questions with options to the quiz
            for question_data in quiz_content_data.quiz_questions:
                # Correcting the filter condition to match the model attributes
                existing_question = db.query(QuizQuestions).filter(
                    QuizQuestions.quiz_id == quiz_content.id,
                    QuizQuestions.question == question_data.question
                ).first()

                if existing_question is None:
                    # Question doesn't exist, so add it
                    question = QuizQuestions(quiz_id=quiz_content.id, question=question_data.question)
                    db.add(question)
                    db.flush()

                    # Add options for the question
                    for option_data in question_data.options:
                        option = QuizOption(
                            question_id=question.id, 
                            text=option_data.text, 
                            is_correct=option_data.is_correct
                        )
                        db.add(option)
            db.commit()
            quiz_content = db.query(QuizContent).options(
                joinedload(QuizContent.quiz_questions)
            ).filter_by(id=quiz_content.id).first()
            return quiz_content
        except SQLAlchemyError as e:
            print(e)
            db.rollback()
            raise DatabaseOperationException(str(e)) from e
