from fastapi import HTTPException
from src.exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException
from .service import HashingAlgorithmService


class HashingAlgorithmController:
    """Controller class to handle hashing algorithm-related requests."""

    @staticmethod
    def create_hashing_algorithm(algorithm_name: str):
        """Handles hashing algorithm creation request."""
        try:
            return HashingAlgorithmService.create_hashing_algorithm(algorithm_name)
        except AlreadyExistsException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_all_hashing_algorithms():
        """Handles hashing algorithm creation request."""
        try:
            return HashingAlgorithmService.get_all_hashing_algorithms()
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_hashing_algorithm_by_id(algorithm_id: int):
        try:
            return HashingAlgorithmService.get_hashing_algorithm_by_id(algorithm_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def get_hashing_algorithm_by_name(algorithm_name: str):
        try:
            return HashingAlgorithmService.get_hashing_algorithm_by_name(algorithm_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def update_hashing_algorithm(algorithm_id: int, algorithm_name: str):
        try:
            return HashingAlgorithmService.update_hashing_algorithm(algorithm_id, algorithm_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def delete_hashing_algorithm(algorithm_id: int):
        try:
            return HashingAlgorithmService.delete_hashing_algorithm(algorithm_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
