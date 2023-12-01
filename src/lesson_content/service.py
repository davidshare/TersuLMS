from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from src.config.database import get_db
from src.exceptions import (
    AlreadyExistsException, DatabaseOperationException, NotFoundException,
)
from src.lesson.models import Lesson
from src.lesson_content.models import (
    ArticleContent, QuizContent, QuizOption, QuizQuestions, VideoContent
)
from src.lesson_content.schemas import (
    ArticleContentCreate, QuizContentCreate, QuizQuestionCreate, VideoContentCreate
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
    def create_quiz_question(quiz_question_data: QuizQuestionCreate):
        """Handles creating quiz questions"""
        try:
            db = next(get_db())
            print(f"**********************{quiz_question_data}")

            quiz = db.query(QuizContent).filter(
                QuizContent.id == quiz_question_data.quiz_id).first()
            if not quiz:
                raise NotFoundException(
                    f"Quiz with id {quiz_question_data.quiz_id} not found")
            
            existing_question = db.query(QuizQuestions).filter(
                    QuizQuestions.lesson_id == quiz_question_data.lesson_id,
                    QuizQuestions.question == quiz_question_data.question
                ).first()

            if existing_question:
                raise AlreadyExistsException(f"Question '{quiz_question_data.question}' already exists for lesson with id {quiz_question_data.lesson_id}")

            question = QuizQuestions(
                **quiz_question_data.model_dump())
            db.add(question)
            db.flush()

            for option_data in quiz_question_data.options:
                        option = QuizOption(
                            question_id=question.id, 
                            text=option_data.text, 
                            is_correct=option_data.is_correct
                        )
                        db.add(option)

            db.commit()
            quiz_question = db.query(QuizQuestions).options(
                joinedload(QuizQuestions.options)
            ).filter_by(id=question.id).first()
            return quiz_question
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

            quiz_content = db.query(QuizContent).filter(QuizContent.lesson_id == quiz_content_data.lesson_id).first()
            if not quiz_content:
                # Create quiz content
                quiz_content = QuizContent(
                    lesson_id=quiz_content_data.lesson_id, 
                    attempts_allowed=quiz_content_data.attempts_allowed, 
                    published=quiz_content_data.published
                )
                db.add(quiz_content)
                db.flush()
            
            quiz_content_data.quiz_questions = [
                question.model_copy(update={'lesson_id': quiz_content_data.lesson_id, 'quiz_id': quiz_content.id})
                for question in quiz_content_data.quiz_questions
            ]

            # Add unique questions with options to the quiz
            for question_data in quiz_content_data.quiz_questions:
                LessonContentService.create_quiz_question(question_data)
            db.commit()
            quiz_content = db.query(QuizContent).options(
                joinedload(QuizContent.quiz_questions)
            ).filter_by(id=quiz_content.id).first()
            return quiz_content
        except SQLAlchemyError as e:
            print(e)
            db.rollback()
            raise DatabaseOperationException(str(e)) from e
