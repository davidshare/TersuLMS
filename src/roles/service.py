from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.auth.schemas import UserRoleCreate
from ..exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException
from .models import UserPermissions, UserRole
from ..config.database import SessionLocal, get_db

class RoleService:
    """Service class for handling permissions."""

    @staticmethod
    def create_role(role_name: UserRoleCreate):
        """Creates a new role."""
        try:
            with SessionLocal() as db:
                role = UserRole(role_name=role_name.role_name)
                db.add(role)
                db.commit()
                db.refresh(role)
                return role
        except IntegrityError as exc:
            raise AlreadyExistsException(
                f"Role {role_name} already exists.") from exc
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_all_roles():
        """Returns all roles."""
        try:
            with SessionLocal() as db:
                roles = db.query(UserRole).all()
                return [{"id": role.id, "role_name": role.role_name} for role in roles]
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e))from e

    @staticmethod
    def get_role_by_name(role_name: UserRoleCreate):
        """Returns a role based on its name."""
        try:
            with SessionLocal() as db:
                role = db.query(UserRole).filter(
                    UserRole.role_name == role_name).first()
                if not role:
                    raise NotFoundException("Role not found")
                return role
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_role_by_id(role_id: int):
        """Returns a role based on its ID."""
        try:
            with SessionLocal() as db:
                role = db.query(UserRole).filter(
                    UserRole.id == role_id).first()
                if not role:
                    raise NotFoundException("Role not found")
                return role
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def update_role_by_id(role_id: int, new_role_name: str):
        """Updates a role's name."""
        try:
            with SessionLocal() as db:
                role = db.query(UserRole).filter(
                    UserRole.id == role_id).first()
                if role:
                    role.role_name = new_role_name
                    db.commit()
                    return {"id": role.id, "role_name": role.role_name}
                else:
                    raise NotFoundException("Role not found")
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def update_role_by_name(old_role_name: str, new_role_name: str):
        """Updates a role's name."""
        try:
            with SessionLocal() as db:
                role = db.query(UserRole).filter(
                    UserRole.role_name == old_role_name).first()
                if role:
                    role.role_name = new_role_name
                    db.commit()
                    return {"id": role.id, "role_name": role.role_name}
                else:
                    raise NotFoundException("Role not found")
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def delete_role_by_id(role_id: int):
        """Deletes a role."""
        try:
            with SessionLocal() as db:
                role = db.query(UserRole).filter(
                    UserRole.id == role_id).first()
                if role:
                    db.delete(role)
                    db.commit()
                    return True
                else:
                    raise NotFoundException("Role not found")
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def delete_role_by_name(role_name: str):
        """Deletes a role."""
        try:
            with SessionLocal() as db:
                role = db.query(UserRole).filter(
                    UserRole.role_name == role_name).first()
                if role:
                    db.delete(role)
                    db.commit()
                    return True
                else:
                    raise NotFoundException("Role not found")
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

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