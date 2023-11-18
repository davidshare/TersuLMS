from fastapi import HTTPException
from .service import RoleService
from ..exceptions import AlreadyExistsException, DatabaseOperationException

class RoleController:
    """Controller class for handling permissions."""
    @staticmethod
    def create_permission(permission_name: str):
        """Handles creating permissions"""
        try:
            return RoleService.create_permission(permission_name)
        except AlreadyExistsException as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def get_permissions():
        """Handles getting all permissions"""
        try:
            return RoleService.get_permissions()
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
