from fastapi import APIRouter
from .auth.routes import router as auth_router, hashing_router, user_roles_router
from .roles.routes import router as roles_router

global_router = APIRouter()

global_router.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

global_router.include_router(
    hashing_router, prefix="/api/v1/auth", tags=["hashing-algorithms"])

global_router.include_router(
    user_roles_router, prefix="/api/v1/auth", tags=["user-roles"])

global_router.include_router(
    roles_router, prefix="/api/v1/roles", tags=["roles"])
