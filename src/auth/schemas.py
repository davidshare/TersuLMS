from pydantic import BaseModel, EmailStr

class UserLoginCreate(BaseModel):
    """
    A Pydantic model representing user login data for creating a new user.

    Attributes:
        email (EmailStr): The email address of the user. Must be a valid email format.
        password (str): The password for the user.
    """
    email: EmailStr
    password: str

class HashingAlgorithmCreate(BaseModel):
    """
    A Pydantic model representing a hashing algorithm.

    Attributes:
        algorithm_name (str): The name of the hashing algorithm.
    """
    algorithm_name: str
