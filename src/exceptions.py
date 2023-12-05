class ApplicationException(Exception):
    """Base class for application-specific exceptions."""

    def __init__(self, message: str = "An error occurred in the application."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class AlreadyExistsException(ApplicationException):
    """Raised when a resource already exists."""

    def __init__(self, message: str = "The resource already exists."):
        super().__init__(message)


class NotFoundException(ApplicationException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found."):
        super().__init__(message)


class DatabaseOperationException(ApplicationException):
    """Raised for general database operation failures."""

    def __init__(self, message: str = "Database operation failed."):
        super().__init__(message)


class AuthenticationException(ApplicationException):
    """Exception raised for authentication-related errors."""

    def __init__(self, message: str = "Authentication failed."):
        super().__init__(message)


class TokenExpiredError(ApplicationException):
    """Raised when a token has expired."""

    def __init__(self, message: str = "Authentication failed."):
        super().__init__(message)


class InvalidTokenError(ApplicationException):
    """Raised when a token is invalid."""

    def __init__(self, message: str = "Authentication failed."):
        super().__init__(message)

class UniqueConstraintViolationException(ApplicationException):
    """Raised when a unique constraint is violated."""

    def __init__(self, message: str = "Unique constraint violated."):
        super().__init__(message)

class DuplicateQuestionException(ApplicationException):
    """Raised when a duplicate question is found in a quiz."""

    def __init__(self, message: str = "Duplicate question found in quiz."):
        super().__init__(message)

class NotNullViolationException(ApplicationException):
    """Raised when a not null constraint is violated."""

    def __init__(self, message: str = "Not null constraint violated."):
        super().__init__(message)