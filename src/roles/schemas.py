from pydantic import BaseModel


class Permission(BaseModel):
    """
    A Pydantic model representing a permission.

    Attributes:
        permission_name (str): The name of the permission.
    """
    permission_name: str


class UserPermissionCreate(Permission):
    """
    A Pydantic model representing a user permission.

    Attributes:
        permission_name (str): The name of the permission.
    """
    pass


class UserPermissionResponse(Permission):
    """
    A Pydantic model representing a user permission.

    Attributes:
        id (int): The ID of the permission.
        permission_name (str): The name of the permission.
    """
    id: int

class UserPermissionUpdate(BaseModel):
    """
    A Pydantic model representing a user permission.

    Attributes:
        new_permission_name (str): The name of the permission.
    """
    new_permission_name: str
