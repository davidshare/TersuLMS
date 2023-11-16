class AlreadyExistsException(Exception):
    """Raised when a resource with the given already exists."""

    def __init__(self, message="The resource already exists."):
        self.message = message
        super().__init__(self.message)


class NotFoundException(Exception):
    """Raised when a requested resource is not found."""

    def __init__(self, message="Resource not found."):
        self.message = message
        super().__init__(self.message)


class DatabaseOperationException(Exception):
    """Raised for general database operation failures."""

    def __init__(self, message="Database operation failed."):
        self.message = message
        super().__init__(self.message)
