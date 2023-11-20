from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, DateTime
from sqlalchemy.orm import relationship

from src.model_mixins import TimestampMixin
from ..config.database import Base

class RefreshToken(Base):
    """Model for refresh tokens."""
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('user_auth.id'))
    user = relationship("UserAuth", back_populates="refresh_tokens")
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)


class UserAuth(Base, TimestampMixin):
    """Model for user authentication."""
    __tablename__ = 'user_auth'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True)
    password = Column(String(250))
    hash_algorithm_id = Column(Integer, ForeignKey('hashing_algorithms.id'))
    is_active = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
    password_recovery_token = Column(String(100))
    recovery_token_time = Column(Date)
    user_role_id = Column(Integer, ForeignKey('user_roles.id'))
    hashing_algorithm = relationship("HashingAlgorithm")
    user_role = relationship("UserRole")
    refresh_tokens = relationship(
        "RefreshToken", order_by=RefreshToken.id, back_populates="user")

class EmailVerification(Base):
    """Model for email verification."""
    __tablename__ = 'email_verification'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('user_auth.id'))
    confirmation_token = Column(String(100))
    token_generation_time = Column(Date)
    is_active = Column(Boolean, default=False)
    is_used = Column(Boolean, default=False)
    expired_at = Column(DateTime, nullable=False,
                        default=lambda: datetime.utcnow() + timedelta(minutes=15))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_auth = relationship("UserAuth")
