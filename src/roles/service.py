from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..exceptions import AlreadyExistsException, DatabaseOperationException
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