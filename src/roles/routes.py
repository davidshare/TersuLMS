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

