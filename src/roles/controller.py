from fastapi import HTTPException
from .service import RoleService
from ..exceptions import (
    AlreadyExistsException, DatabaseOperationException, NotFoundException
)

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
        
    @staticmethod
    def get_permission_by_name(permission_name: str):
        """Handles getting a permission by name"""
        try:
            return RoleService.get_permission_by_name(permission_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def get_permission_by_id(permission_id: int):
        """Handles getting a permission by id"""
        try:
            return RoleService.get_permission_by_id(permission_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
    
    @staticmethod
    def update_permission_by_id(permission_id: int, permission_name: str):
        """Handles updating a permission by id"""
        try:
            return RoleService.update_permission_by_id(permission_id, permission_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e            
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        
    @staticmethod
    def update_permission_by_name(old_permission_name: str, new_permission_name: str):
        """Handles updating a permission by name"""
        try:
            return RoleService.update_permission_by_name(old_permission_name, new_permission_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e            
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
    
    @staticmethod
    def delete_permission_by_id(permission_id: int):
        """Handles deleting a permission by id"""
        try:
            return RoleService.delete_permission_by_id(permission_id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e            
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e

    @staticmethod
    def delete_permission_by_name(permission_name: str):
        """Handles deleting a permission by name"""
        try:
            return RoleService.delete_permission_by_name(permission_name)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e)) from e            
        except DatabaseOperationException as e:
            print(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error") from e
        

        """
        TODO: check all controllers and ensure the use of correct HTTP status codes
        TODO: check all controllers and ensure consistency in format and error handling
        TODO: check all controllers and ensure the use of correct commenting format
        """