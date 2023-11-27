from fastapi import APIRouter, status

from src.auth.schemas import RoleUpdate, UserRoleCreate, UserRoleResponse
from .controller import RoleController

from .schemas import (
    UserPermissionCreate, UserPermissionResponse, UserPermissionUpdate
)

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK, response_model=UserRoleResponse)
def create_user_role(role_name: UserRoleCreate):
    """API endpoint to create a new user role."""
    return RoleController.create_role(role_name)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserRoleResponse])
def get_all_user_roles():
    """API endpoint to get all user roles."""
    return RoleController.get_all_roles()


@router.get("/users/roles/id/{role_id}", status_code=status.HTTP_200_OK, response_model=UserRoleResponse)
def get_user_role_by_id(role_id: int):
    """API endpoint to get a user role by ID."""
    return RoleController.get_role_by_id(role_id)


@router.get("/users/roles/name/{role_name}", status_code=status.HTTP_200_OK, response_model=UserRoleResponse)
def get_user_role_by_name(role_name: str):
    """API endpoint to get a user role by name or id."""
    return RoleController.get_role_by_name(role_name)


@router.put("/users/roles/id/{role_id}", status_code=status.HTTP_200_OK, response_model=UserRoleCreate)
def update_user_role_by_id(role_id: int, role_name: UserRoleCreate):
    """API endpoint to update a user role."""
    return RoleController.update_role_by_id(role_id, role_name)


@router.put("/users/roles/name/{old_role_name}", status_code=status.HTTP_200_OK, response_model=UserRoleCreate)
def update_user_role_by_name(old_role_name: str, role_update: RoleUpdate):
    """API endpoint to update a user role."""
    return RoleController.update_role_by_name(old_role_name, role_update.new_role_name)


@router.delete("/users/roles/id/{role_id}", status_code=status.HTTP_200_OK)
def delete_user_role_by_id(role_id: int):
    """API endpoint to delete a user role."""
    return RoleController.delete_role_by_id(role_id)


@router.delete("/users/roles/name/{role_name}", status_code=status.HTTP_200_OK)
def delete_user_role_by_name(role_name: str):
    """API endpoint to delete a user role."""
    return RoleController.delete_role_by_name(role_name)

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


@router.put("/permissions/id/{permission_id}", status_code=status.HTTP_200_OK, response_model=UserPermissionResponse)
def update_permission_by_id(permission_id: int, permission: UserPermissionCreate):
    """API endpoint to update a user permission by id."""
    return RoleController.update_permission_by_id(permission_id, permission.permission_name)


@router.put("/permissions/name/{old_permission_name}", status_code=status.HTTP_200_OK, response_model=UserPermissionResponse)
def update_permission_by_name(old_permission_name: str, permission_update: UserPermissionUpdate):
    """API endpoint to update a user permission by name."""
    return RoleController.update_permission_by_name(old_permission_name, permission_update.new_permission_name)

@router.delete("/permissions/id/{permission_id}", status_code=status.HTTP_200_OK)
def delete_permission_by_id(permission_id: int):
    """API endpoint to delete a user permission by id."""
    return RoleController.delete_permission_by_id(permission_id)

@router.delete("/permissions/name/{permission_name}", status_code=status.HTTP_200_OK)
def delete_permission_by_name(permission_name: str):
    """API endpoint to delete a user permission by name."""
    return RoleController.delete_permission_by_name(permission_name)