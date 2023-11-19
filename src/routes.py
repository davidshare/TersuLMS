from fastapi import APIRouter
from .auth.routes import router as auth_router, hashing_router, user_roles_router
from .roles.routes import router as roles_router
from .course_category.routes import router as course_category_router
from .course.routes import router as course_router

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