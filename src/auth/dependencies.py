from fastapi import HTTPException

def password_length_validator(password: str):
    """
    Validate the length of a password.

    Ensures that the given password is not shorter than 8 characters and not longer than 20 characters.
    Raises an HTTPException with status code 400 if the validation fails.

    Parameters:
    password (str): The password to validate.

    Raises:
    HTTPException: If the password length is not within the required range.
    """
    if password and not (8 <= len(password) <= 20):
        raise HTTPException(
            status_code=400, detail="Password must be between 8 and 20 characters")