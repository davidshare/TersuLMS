from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, DateTime, Table
from sqlalchemy.orm import relationship

from ..config.database import Base

granted_permissions = Table(
    'granted_permissions',
    Base.metadata,
    Column('role_id', ForeignKey('user_roles.id'), primary_key=True),
    Column('permissions_id', ForeignKey('user_permissions.id'), primary_key=True)
)


class HashingAlgorithm(Base):
    __tablename__ = 'hashing_algorithms'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    algorithm_name = Column(String(10))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    

class ExternalProvider(Base):
    __tablename__ = 'external_providers'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    provider_name = Column(String(50))
    web_service_endpoint = Column(String(200))


class UserAuth(Base):
    __tablename__ = 'user_login'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    password = Column(String(250))
    hash_algorithm_id = Column(Integer, ForeignKey('hashing_algorithms.id'))
    email = Column(String(100), unique=True)
    is_active = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
    password_recovery_token = Column(String(100))
    recovery_token_time = Column(Date)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    hashing_algorithm = relationship(HashingAlgorithm)

class ExternalUserAuth(Base):
    __tablename__ = 'external_user_login'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('user_login.id'))
    provider_id = Column(Integer, ForeignKey('external_providers.id'))
    provider_token = Column(String(100))
    external_provider = relationship("ExternalProvider")

class EmailVerification(Base):
    __tablename__ = 'email_verification'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('user_login.id'))
    confirmation_token = Column(String(100))
    token_generation_time = Column(Date)
    is_active = Column(Boolean, default=False)
    is_used = Column(Boolean, default=False)
    expired_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(minutes=15))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_login = relationship("UserAuth")

class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    description = Column(String(255))

class UserPermissions(Base):
    __tablename__ = 'user_permissions'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    description = Column(String(255))
