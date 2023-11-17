from fastapi import HTTPException


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
    def validate_password_length(password: str):
        if not (8 <= len(password) <= 20):
            raise ValueError("Password must be between 8 and 20 characters")
        return password
