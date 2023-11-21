from fastapi import APIRouter, status

from .controller import LessonController
from .schemas import LessonCreate, LessonResponse

router = APIRouter()

@router.post("/", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def create_lesson(lesson_data: LessonCreate):
    """Handles creating lessons"""
    return LessonController.create_lesson(lesson_data)
