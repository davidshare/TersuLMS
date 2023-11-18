from fastapi import APIRouter, status
from .controller import RoleController

from .schemas import (
    UserPermissionCreate, UserPermissionResponse
    )

router = APIRouter()

@router.post("/permissions/", status_code=status.HTTP_200_OK, response_model=UserPermissionResponse)
def create_user_permission(permission: UserPermissionCreate):
    """API endpoint to create a new user permission."""
    return RoleController.create_permission(permission.permission_name)

@router.get("/permissions/", status_code=status.HTTP_200_OK, response_model=list[UserPermissionResponse])
def get_user_permissions():
    """API endpoint to get all user permissions."""
    return RoleController.get_permissions()

@router.get("/permissions/name/{permission_name}", status_code=status.HTTP_200_OK, response_model=UserPermissionResponse)
def get_permission_by_name(permission_name: str):
    """API endpoint to get a user permission by name."""
    return RoleController.get_permission_by_name(permission_name)

@router.get("/permissions/id/{permission_id}", status_code=status.HTTP_200_OK, response_model=UserPermissionResponse)
def get_permission_by_id(permission_id: int):
    """API endpoint to get a user permission by id."""
    return RoleController.get_permission_by_id(permission_id)