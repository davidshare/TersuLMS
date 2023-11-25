from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from src.config.database import get_db
from src.exceptions import DatabaseOperationException, NotFoundException
from src.lesson.models import Lesson
from src.lesson_content.models import (
    ArticleContent, QuizContent, QuizOption, QuizQuestion, VideoContent
)
from src.lesson_content.schemas import ArticleContentCreate, QuestionResponse, QuizContentCreate, QuizContentResponse, QuizOptionResponse, VideoContentCreate


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
        try:
            db = next(get_db())

            lesson = db.query(Lesson).filter(Lesson.id == quiz_content_data.lesson_id).first()
            if not lesson:
                raise NotFoundException(f"Lesson with id {quiz_content_data.lesson_id} not found")

            # Create QuizContent instance
            quiz_content = QuizContent(lesson_id=quiz_content_data.lesson_id, content_type=quiz_content_data.content_type)
            db.add(quiz_content)
            db.flush()

            for question_data in quiz_content_data.quiz_questions:
                quiz_question = QuizQuestion(question_text=question_data.question_text, quiz_content=quiz_content)
                db.add(quiz_question)
                db.flush()
                
                for option_data in question_data.options:
                    quiz_option = QuizOption(option_text=option_data.option_text, is_correct=option_data.is_correct, question_id=quiz_question.id)
                    db.add(quiz_option)

            db.commit()

            quiz_content = db.query(QuizContent).options(joinedload(QuizContent.quiz_questions).joinedload(QuizQuestion.options)).filter_by(id=quiz_content.id).first()

            # Construct the response
            quiz_questions_response = [
                QuestionResponse(
                    id=question.id,
                    question_text=question.question_text,
                    options=[
                        QuizOptionResponse(
                            id=option.id,
                            option_text=option.option_text,
                            is_correct=option.is_correct
                        ) for option in question.options
                    ]
                ) for question in quiz_content.quiz_questions
            ]

            quiz_content_response = QuizContentResponse(
                id=quiz_content.id,
                lesson_id=quiz_content.lesson_id,
                content_type=quiz_content.content_type,
                quiz_questions=quiz_questions_response
            )

            return quiz_content_response

        except SQLAlchemyError as e:
            db.rollback()
            raise DatabaseOperationException(str(e)) from e
