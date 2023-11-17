from fastapi import HTTPException
from .service import AuthService
from .schemas import UserLoginCreate, HashingAlgorithmCreate
from .security import hash_password
from src.exceptions import NotFoundException, AlreadyExistsException, DatabaseOperationException


class AuthController:
    """Controller class to handle authentication-related requests."""

    @staticmethod
    def create(user_data: UserLoginCreate):
        try:
            user_data.password = hash_password(user_data.password)
            return AuthService.create(user_data)
        except AlreadyExistsException as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def create_hashing_algorithm(algorithm_name: HashingAlgorithmCreate):
        try:
            return AuthService.create_hashing_algorithm(algorithm_name)
        except AlreadyExistsException as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

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
