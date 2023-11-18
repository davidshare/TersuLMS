from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from .security import validate_password_length


class UserAuthCreate(BaseModel):
    """
    A Pydantic model representing user login data for creating a new user.

    Attributes:
        email (EmailStr): The email address of the user. Must be a valid email format.
        password (str): The password for the user.
        hash_algorithm_id (int): The ID of the hashing algorithm to use for hashing the password.
    """
    email: EmailStr
    password: str
    hash_algorithm_id: Optional[int] = None

    @validator('password')
    @classmethod
    def password_validator(cls, v):
        """ Validates the length of the password """
        validate_password_length(v)
        return v


class UserAuthLogin(BaseModel):
    """
    A Pydantic model representing user login data for creating a new user.

    Attributes:
        email (EmailStr): The email address of the user. Must be a valid email format.
        password (str): The password for the user.
    """
    email: EmailStr
    password: str


class UserAuthResponse(BaseModel):
    """
    A Pydantic model representing user login data for creating a new user.

    Attributes:
        id (int): The ID of the user.
        email (EmailStr): The email address of the user. Must be a valid email format.
    """
    id: int
    email: str


class HashingAlgorithmCreate(BaseModel):
    """
    A Pydantic model representing a hashing algorithm.

    Attributes:
        algorithm_name (str): The name of the hashing algorithm.
    """
    algorithm_name: str


class TokenResponse(BaseModel):
    """
    A Pydantic model representing a token response.
    
    Attributes:
        access_token (str): The access token.
        token_type (str): The type of token.
    """

    access_token: str
    token_type: str

class UserRoleCreate(BaseModel):
    """
    A Pydantic model representing a user role.

    Attributes:
        role_name (str): The name of the role.
    """
    role_name: str

class UserRoleResponse(UserRoleCreate):
    """
    A Pydantic model representing a user role.

    Attributes:
        id (int): The ID of the role.
    """
    id: int

class RoleUpdate(BaseModel):
    """
    A Pydantic model representing a user role.

    Attributes:
        new_role_name (str): The name of the role.
    """
    new_role_name: str


