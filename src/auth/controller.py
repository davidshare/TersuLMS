from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from src.exceptions import NotFoundException, AlreadyExistsException, DatabaseOperationException, AuthenticationException, TokenExpiredError, InvalidTokenError
from .service import AuthService
from .schemas import UserAuthCreate, UserAuthLogin, UserRoleCreate
from .security import hash_password


class AuthController:
    """Controller class to handle authentication-related requests."""

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    def create(user_data: UserAuthCreate):
        """Handles user creation request."""
        try:
            user_data.password = hash_password(user_data.password)
            return AuthService.create(user_data)
        except AlreadyExistsException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def login(user_data: UserAuthLogin):
        """Handles login request."""
        try:
            return AuthService.login(user_data)
        except AuthenticationException as e:
            raise HTTPException(status_code=401, detail=str(e)) from e
        except DatabaseOperationException as e:
            # Handle database operation errors
            raise HTTPException(
                status_code=500, detail="A server error occurred.") from e

    @staticmethod
    def refresh_token(refresh_token: str):
        """Handles refresh token request."""
        try:
            return AuthService.refresh_token(refresh_token)
        except AuthenticationException as e:
            raise HTTPException(status_code=401, detail=str(e)) from e
        except TokenExpiredError as e:
            raise HTTPException(status_code=401, detail="Token expired") from e
        except InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token") from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail=e) from e

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            user = AuthService.get_user_from_token(token)
            if user is None:
                raise HTTPException(
                    status_code=401, detail="Invalid authentication credentials")
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

