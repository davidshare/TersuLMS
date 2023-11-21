from fastapi import APIRouter, status

from .controller import LessonController
from .schemas import LessonCreate, LessonResponse, LessonUpdate

router = APIRouter()

@router.post("/", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def create_lesson(lesson_data: LessonCreate):
    """Handles creating lessons"""
    return LessonController.create_lesson(lesson_data)

@router.get("/id/{lesson_id}", response_model=LessonResponse)
def get_lesson_by_id(lesson_id: int):
    """Handles getting lesson by id"""
    return LessonController.get_lesson_by_id(lesson_id)

@router.put("/id/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: int, lesson_data: LessonUpdate):
    """Handles updating lesson by id"""
    return LessonController.update_lesson(lesson_id, lesson_data)

@router.delete("/id/{lesson_id}")
def delete_lesson(lesson_id: int):
    """Handles deleting lesson by id"""
    return LessonController.delete_lesson(lesson_id)
