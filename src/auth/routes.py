from fastapi import APIRouter, Depends
from .controller import AuthController
from .schemas import UserLoginCreate, HashingAlgorithmCreate
from .dependencies import password_length_validator

router = APIRouter()


@router.post("/user/")
def create_user(user_data: UserLoginCreate = Depends(password_length_validator)):
    """API endpoint to create a new user."""
    return AuthController.create(user_data)


@router.post("/hashing-algorithms/")
def create_hashing_algorithm(algorithm_name: HashingAlgorithmCreate):
    """API endpoint to create a new hashing algorithm."""
    return AuthController.create_hashing_algorithm(algorithm_name)


@router.get("/hashing-algorithms/")
def get_all_hashing_algorithms():
    """Get all hashing algorithms."""
    return AuthController.get_all_hashing_algorithms()


@router.get("/hashing-algorithms/{algorithm_id}")
def get_hashing_algorithm_by_id(algorithm_id: int):
    """Get a hashing algorithm by its ID."""
    return AuthController.get_hashing_algorithm_by_id(algorithm_id)


@router.get("/hashing-algorithms/name/{algorithm_name}")
def get_hashing_algorithm_by_name(algorithm_name: str):
    """Get a hashing algorithm by its name."""
    return AuthController.get_hashing_algorithm_by_name(algorithm_name)


@router.put("/hashing-algorithms/{algorithm_id}")
def update_hashing_algorithm(algorithm_id: int, algorithm_name: HashingAlgorithmCreate):
    """API endpoint to update a hashing algorithm."""
    return AuthController.update_hashing_algorithm(algorithm_id, algorithm_name.algorithm_name)


@router.delete("/hashing-algorithms/{algorithm_id}")
def delete_hashing_algorithm(algorithm_id: int):
    """API endpoint to delete a hashing algorithm."""
    return AuthController.delete_hashing_algorithm(algorithm_id)
