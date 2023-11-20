from pydantic import BaseModel

class HashingAlgorithmCreate(BaseModel):
    """
    A Pydantic model representing a hashing algorithm.

    Attributes:
        algorithm_name (str): The name of the hashing algorithm.
    """
    algorithm_name: str