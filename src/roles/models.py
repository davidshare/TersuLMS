from sqlalchemy import (
    Column, Integer, String, ForeignKey, Table
)

from ..config.database import Base

class UserPermissions(Base):
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