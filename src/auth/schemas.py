from pydantic import BaseModel, EmailStr

class UserAuthCreate(BaseModel):
    """
    A Pydantic model representing user login data for creating a new user.

    Attributes:
        email (EmailStr): The email address of the user. Must be a valid email format.
        password (str): The password for the user.
    """
    email: EmailStr
    password: str

class UserAuthSave(BaseModel):
    """
    A Pydantic model representing user data for saving a new user.

    Attributes:
        email (EmailStr): The email address of the user. Must be a valid email format.
        password (str): The password for the user.
        hash_algorithm_id (int): The ID of the hashing algorithm to use for hashing the password.
    """
    email: EmailStr
    password: str
    hash_algorithm_id: int


class HashingAlgorithmCreate(BaseModel):
    """
    A Pydantic model representing a hashing algorithm.

    Attributes:
        algorithm_name (str): The name of the hashing algorithm.
    """
    algorithm_name: str
