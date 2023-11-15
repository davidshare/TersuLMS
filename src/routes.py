from fastapi import APIRouter
from .auth.routes import router as auth_router

global_router = APIRouter()

global_router.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])