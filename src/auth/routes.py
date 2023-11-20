from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from .controller import AuthController
from .schemas import (
    UserAuthCreate, UserAuthResponse,
    UserAuthLogin, TokenResponse,
)

router = APIRouter()
hashing_router = APIRouter()
user_roles_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/user/", status_code=status.HTTP_201_CREATED, response_model=UserAuthResponse)
def create_user(user_data: UserAuthCreate):
    """API endpoint to create a new user."""
    return AuthController.create(user_data)


@router.post("/users/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def login(user_data: UserAuthLogin):
    """API endpoint to authenticate a user and generate a JWT token."""
    return AuthController.login(user_data)


@router.post("/token/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def refresh_token(token: str = Depends(oauth2_scheme)):
    """API endpoint to refresh a JWT token."""
    return AuthController.refresh_token(token)
