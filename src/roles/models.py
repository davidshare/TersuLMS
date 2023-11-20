from sqlalchemy import (
    Column, Integer, String, ForeignKey, Table
)
from sqlalchemy.orm import relationship

from src.model_mixins import TimestampMixin

from ..config.database import Base


class UserRole(Base, TimestampMixin):
    """Model for user roles."""
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    role_name = Column(String(50), unique=True)
    users = relationship("UserAuth", back_populates="user_role")


class UserPermissions(Base, TimestampMixin):
    """Model for user permissions."""
    __tablename__ = 'user_permissions'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    permission_name = Column(String(100), unique=True, nullable=False)


granted_permissions = Table(
    'granted_permissions',
    Base.metadata,
    Column('role_id', ForeignKey('user_roles.id'), primary_key=True),
    Column('permissions_id', ForeignKey(
        'user_permissions.id'), primary_key=True)
)
