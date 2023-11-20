from fastapi import APIRouter
from .controller import HashingAlgorithmController
from .schema import HashingAlgorithmCreate

router = APIRouter()

@router.post("/hashing-algorithms/")
def create_hashing_algorithm(algorithm_name: HashingAlgorithmCreate):
    """API endpoint to create a new hashing algorithm."""
    return HashingAlgorithmController.create_hashing_algorithm(algorithm_name)


@router.get("/hashing-algorithms/")
def get_all_hashing_algorithms():
    """Get all hashing algorithms."""
    return HashingAlgorithmController.get_all_hashing_algorithms()


@router.get("/hashing-algorithms/{algorithm_id}")
def get_hashing_algorithm_by_id(algorithm_id: int):
    """Get a hashing algorithm by its ID."""
    return HashingAlgorithmController.get_hashing_algorithm_by_id(algorithm_id)


@router.get("/hashing-algorithms/name/{algorithm_name}")
def get_hashing_algorithm_by_name(algorithm_name: str):
    """Get a hashing algorithm by its name."""
    return HashingAlgorithmController.get_hashing_algorithm_by_name(algorithm_name)


@router.put("/hashing-algorithms/{algorithm_id}")
def update_hashing_algorithm(algorithm_id: int, algorithm_name: HashingAlgorithmCreate):
    """API endpoint to update a hashing algorithm."""
    return HashingAlgorithmController.update_hashing_algorithm(algorithm_id, algorithm_name.algorithm_name)


@router.delete("/hashing-algorithms/{algorithm_id}")
def delete_hashing_algorithm(algorithm_id: int):
    """API endpoint to delete a hashing algorithm."""
    return HashingAlgorithmController.delete_hashing_algorithm(algorithm_id)