from operator import le
from fastapi import APIRouter

from src import lesson

from .hashing_algorithms.routes import router as hashing_router
from .course_section.routes import router as course_section_router
from .auth.routes import router as auth_router, user_roles_router
from .roles.routes import router as roles_router
from .course_category.routes import router as course_category_router
from .course.routes import router as course_router
from .lesson.routes import router as lesson_router
from .lesson_content.routes import router as lesson_content_router

global_router = APIRouter()

global_router.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

global_router.include_router(
    hashing_router, prefix="/api/v1/auth", tags=["hashing-algorithms"])

global_router.include_router(
    user_roles_router, prefix="/api/v1/auth", tags=["user-roles"])

global_router.include_router(
    roles_router, prefix="/api/v1/roles", tags=["roles"])

global_router.include_router(
    course_category_router, prefix="/api/v1/categories", tags=["categories"])


global_router.include_router(
    course_router, prefix="/api/v1/courses", tags=["courses"])

global_router.include_router(
    course_section_router, prefix="/api/v1/sections", tags=["sections"])

global_router.include_router(
    lesson_router, prefix="/api/v1/lessons", tags=["lessons"])

global_router.include_router(
    lesson_content_router, prefix="/api/v1/lesson-content", tags=["lesson-content"])

"""
TODO: check all routes and ensure the use of correct HTTP status codes
TODO: check all routes and ensure the use of correct response methods
"""
