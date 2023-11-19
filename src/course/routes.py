from fastapi import APIRouter, status

from .controller import CourseController
from .schemas import CourseCreate, CourseResponse

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK, response_model=CourseResponse)
def create_course(course: CourseCreate):
    """API endpoint to create a new course."""
    return CourseController.create_course(course)

@router.get("/slug/{slug}", status_code=status.HTTP_200_OK, response_model=CourseResponse)
def get_course_by_slug(slug: str):
    """API endpoint to get a course by slug."""
    return CourseController.get_course_by_slug(slug)

@router.get("/id/{course_id}", status_code=status.HTTP_200_OK, response_model=CourseResponse)
def get_course_by_id(course_id: int):
    """API endpoint to get a course by id."""
    return CourseController.get_course_by_id(course_id)