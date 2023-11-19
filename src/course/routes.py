from fastapi import APIRouter, status

from .controller import CourseController
from .schemas import CourseCreate, CourseResponse

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK, response_model=CourseResponse)
def create_course(course: CourseCreate):
    """API endpoint to create a new course."""
    return CourseController.create_course(course)