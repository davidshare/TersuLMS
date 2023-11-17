from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError

from ..exceptions import AuthenticationException

from ..config.settings import settings

pwd_context = CryptContext(
    schemes=[settings.HASH_ALGORITHM], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt algorithm.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a hashed password.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The hashed password for comparison.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_length(password: str):
    """
    Validate the length of a password.

    Ensures that the given password is not shorter than 8 characters and not longer than 20 characters.
    Raises an HTTPException with status code 400 if the validation fails.

    Parameters:
    password (str): The password to validate.

    Raises:
    HTTPException: If the password length is not within the required range.
    """
    if not (8 <= len(password) <= 20):
        raise ValueError("Password must be between 8 and 20 characters")
    return password


def create_token(data: Union[str, Any], token_type: str, expires_delta: int = None) -> str:
    """
    Creates a JWT token (access or refresh) for a given subject.

    Args:
        subject (Union[str, Any]): The subject of the token (usually user identifier).
        token_type (str): Type of the token ('access' or 'refresh').
        expires_delta (int, optional): Custom expiration time for the token. Defaults to None.

    Returns:
        str: A JWT encoded token string.
    """
    if token_type == 'access':
        secret_key = settings.JWT_SECRET_KEY
        default_expiry = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    elif token_type == 'refresh':
        secret_key = settings.JWT_REFRESH_TOKEN_SECRET_KEY
        default_expiry = settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
    else:
        raise ValueError("Invalid token type specified")

    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=default_expiry)

    to_encode = {"exp": expires_delta, "id": data["id"]}
    encoded_jwt = jwt.encode(to_encode, secret_key, settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str, secret_key: str, algorithms: list):
    """
    Decodes a JWT token.

    Args:
        token (str): The JWT token to decode.
        secret_key (str): The secret key used to encode the token.
        algorithms (list): The list of algorithms to use for decoding.

    Raises:
        Exception: If the token is expired or invalid.

    Returns:
        dict: The decoded token payload.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms, options={
                            "verify_exp": False})
        return payload
    except JWTError as e:
        raise AuthenticationException("Token is invalid from here") from e


def is_token_expired(token: str, secret_key: str) -> bool:
    """
    Checks if the JWT token is expired.

    Args:
        token (str): JWT token to be validated.
        secret_key (str): Secret key used for decoding the token.

    Returns:
        bool: True if token is expired, False otherwise.
    """
    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])
        return False
    except ExpiredSignatureError:
        return True
    except JWTError:
        return False
