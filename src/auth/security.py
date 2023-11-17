from passlib.context import CryptContext
from ..config.settings import settings

pwd_context = CryptContext(schemes=[settings.HASH_ALGORITHM], deprecated="auto")

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
