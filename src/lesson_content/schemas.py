from typing import List, Optional
from pydantic import BaseModel


class LessonContentBase(BaseModel):
    """
    Base schema for lesson content. This class serves as a foundation for defining
    various types of lesson content schemas.

    Attributes:
        lesson_id (int): The unique identifier of the associated lesson.

    This class inherits from BaseModel, which is a base class provided by Pydantic
    used for defining data validation, serialization, and model attributes.
    """
    lesson_id: int


class ArticleContentCreate(LessonContentBase):
    """
    Schema for creating article content.

    Attributes:
        text (str): The text of the article.

    This class inherits from LessonContentBase.
    """
    text: str


class ArticleContentResponse(ArticleContentCreate):
    """
    Schema for returning article content.

    This class inherits from ArticleContentCreate.
    """
    id: int


class VideoContentCreate(LessonContentBase):
    """
    Schema for creating video content.

    Attributes:
        url (str): The url of the video.
        description (str): The description of the video.
        duration (int): The duration of the video in seconds.

    This class inherits from LessonContentBase.
    """
    url: str
    description: str
    duration: int


class VideoContentResponse(VideoContentCreate):
    """
    Schema for returning video content.

    This class inherits from VideoContentCreate.
    """
    id: int


class QuizOptionBase(BaseModel):
    """
    Base schema for quiz options. This class serves as a foundation for defining
    various types of quiz option schemas.

    Attributes:
        text (str): The text of the quiz option.
        is_correct (bool): Whether the quiz option is correct or not.

    This class inherits from BaseModel.
    """
    question_id: Optional[int] = None
    text: str
    is_correct: bool


class QuizQuestionCreate(BaseModel):
    """
    Schema for creating quiz questions.

    Attributes:
        question_text (str): The text of the quiz question.
        options (List[QuizOptionBase]): The list of quiz options.

    This class inherits from BaseModel.
    """
    quiz_id: Optional[int] = None
    question: str
    options: List[QuizOptionBase]


class QuizContentCreate(LessonContentBase):
    """
    Schema for creating quiz content.

    Attributes:
        attempts_allowed (int): The number of attempts allowed for the quiz.
        published (bool): Whether the quiz is published or not.
        questions (List[QuizQuestionCreate]): The list of quiz questions.

    This class inherits from LessonContentBase.
    """
    quiz_questions: List[QuizQuestionCreate]
    attempts_allowed: int
    published: bool


class QuizContentResponse(QuizContentCreate):
    """
    Schema for returning quiz content.

    This class inherits from QuizContentCreate.
    """
    id: int
    
