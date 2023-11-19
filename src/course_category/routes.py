from fastapi import APIRouter, status
from .controller import CourseCategoryController
from .schemas import (
    CourseCategoryCreate, CourseCategoryResponse, CourseCategoryUpdate
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=CourseCategoryResponse)
def create_course_category(course_category: CourseCategoryCreate):
    """API endpoint to create a new course category."""
    return CourseCategoryController.create_course_category(course_category.name, course_category.description)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CourseCategoryResponse])
def get_course_categories():
    """API endpoint to get all course categories."""
    return CourseCategoryController.get_course_categories()


@router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=CourseCategoryResponse)
def get_course_category_by_id(category_id: int):
    """API endpoint to get a course category by id."""
    return CourseCategoryController.get_course_category_by_id(category_id)

@router.put("/{category_id}", status_code=status.HTTP_200_OK, response_model=CourseCategoryResponse)
def update_course_category(category_id: int, course_category: CourseCategoryUpdate):
    """API endpoint to update a course category by id."""
    return CourseCategoryController.update_course_category(category_id, course_category.name, course_category.description)


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_course_category(category_id: int):
    """API endpoint to delete a course category by id."""
    return CourseCategoryController.delete_course_category(category_id)
