from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from src.exceptions import NotFoundException, AlreadyExistsException, DatabaseOperationException, AuthenticationException, TokenExpiredError, InvalidTokenError
from .service import AuthService
from .schemas import UserAuthCreate, HashingAlgorithmCreate, UserAuthLogin, UserRoleCreate
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
    def create_hashing_algorithm(algorithm_name: HashingAlgorithmCreate):
        """Handles hashing algorithm creation request."""
        try:
            return AuthService.create_hashing_algorithm(algorithm_name)
        except AlreadyExistsException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

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

    @staticmethod
    def get_all_hashing_algorithms():
        try:
            return AuthService.get_all_hashing_algorithms()
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_hashing_algorithm_by_id(algorithm_id: int):
        try:
            return AuthService.get_hashing_algorithm_by_id(algorithm_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_hashing_algorithm_by_name(algorithm_name: str):
        try:
            return AuthService.get_hashing_algorithm_by_name(algorithm_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def update_hashing_algorithm(algorithm_id: int, algorithm_name: str):
        try:
            return AuthService.update_hashing_algorithm(algorithm_id, algorithm_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def delete_hashing_algorithm(algorithm_id: int):
        try:
            return AuthService.delete_hashing_algorithm(algorithm_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def create_role(role_name: UserRoleCreate):
        try:
            return AuthService.create_role(role_name)
        except AlreadyExistsException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_all_roles():
        """Handles getting all roles"""
        try:
            return AuthService.get_all_roles()
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_role_by_name(role_name: UserRoleCreate):
        """Handles getting roles by name"""
        try:
            return AuthService.get_role_by_name(role_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_role_by_id(role_id: int):
        """Handles getting roles by ID"""
        try:
            return AuthService.get_role_by_id(role_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def update_role_by_id(role_id: int, new_role_name: UserRoleCreate):
        """Handles updating roles"""
        try:
            return AuthService.update_role_by_id(role_id, new_role_name.role_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def update_role_by_name(old_role_name: str, new_role_name: str):
        """Handles updating roles"""
        try:
            return AuthService.update_role_by_name(old_role_name, new_role_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def delete_role_by_id(role_id: int):
        """Handles deleting roles"""
        try:
            return AuthService.delete_role_by_id(role_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def delete_role_by_name(role_name: str):
        """Handles deleting roles"""
        try:
            return AuthService.delete_role_by_name(role_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
