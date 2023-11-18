from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException
from .models import UserPermissions
from ..config.database import get_db

class RoleService:
    """Service class for handling permissions."""

    @staticmethod
    def create_permission(permission_name: str):
        """Handles creating permissions"""
        try:
            db = next(get_db())
            permission = UserPermissions(permission_name=permission_name)
            db.add(permission)
            db.commit()
            db.refresh(permission)
            # return {"id": permission.id, "permission_name": permission.permission_name}
            return permission
        except IntegrityError as e:
            db.rollback()
            raise AlreadyExistsException(
                f"The permission {permission_name} already exists.") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e
        
    @staticmethod
    def get_permissions():
        """Handles getting all permissions"""
        try:
            db = next(get_db())
            permissions = db.query(UserPermissions).all()
            return permissions
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e
        
    @staticmethod
    def get_permission_by_name(permission_name: str):
        """Handles getting a permission by name"""
        try:
            db = next(get_db())
            permission = db.query(UserPermissions).filter(
                UserPermissions.permission_name == permission_name).first()
            if not permission:
                raise NotFoundException(
                        f"The permission {permission_name} does not exist.")
            return permission
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e
        
    @staticmethod
    def get_permission_by_id(permission_id: int):
        """Handles getting a permission by id"""
        try:
            db = next(get_db())
            permission = db.query(UserPermissions).filter(
                UserPermissions.id == permission_id).first()
            if not permission:
                raise NotFoundException(
                        f"The permission with id {permission_id} does not exist.")
            return permission
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e
        
    @staticmethod
    def update_permission_by_id(permission_id: int, permission_name: str):
        """Handles updating a permission by id"""
        try:
            db = next(get_db())
            permission = db.query(UserPermissions).filter(
                UserPermissions.id == permission_id).first()
            if not permission:
                raise NotFoundException(
                        f"The permission with id {permission_id} does not exist.")
            permission.permission_name = permission_name
            db.commit()
            db.refresh(permission)
            return permission
        except IntegrityError as e:
            db.rollback()
            raise AlreadyExistsException(
                f"The permission {permission_name} already exists.") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e
    
    @staticmethod
    def update_permission_by_name(old_permission_name: str, new_permission_name: str):
        """Handles updating a permission by name"""
        try:
            db = next(get_db())
            permission = db.query(UserPermissions).filter(
                UserPermissions.permission_name == old_permission_name).first()
            if not permission:
                raise NotFoundException(
                        f"The permission {old_permission_name} does not exist.")
            permission.permission_name = new_permission_name
            db.commit()
            db.refresh(permission)
            return permission
        except IntegrityError as e:
            db.rollback()
            raise AlreadyExistsException(
                f"The permission {new_permission_name} already exists.") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e
    
    @staticmethod
    def delete_permission_by_id(permission_id: int):
        """Handles deleting a permission by id"""
        try:
            db = next(get_db())
            permission = db.query(UserPermissions).filter(
                UserPermissions.id == permission_id).first()
            if not permission:
                raise NotFoundException(
                        f"The permission with id {permission_id} does not exist.")
            db.delete(permission)
            db.commit()
            return permission
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e
    
    @staticmethod
    def delete_permission_by_name(permission_name: str):
        """Handles deleting a permission by name"""
        try:
            db = next(get_db())
            permission = db.query(UserPermissions).filter(
                UserPermissions.permission_name == permission_name).first()
            if not permission:
                raise NotFoundException(
                        f"The permission {permission_name} does not exist.")
            db.delete(permission)
            db.commit()
            return permission
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e