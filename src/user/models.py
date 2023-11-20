from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from ..config.database import Base

class User(Base):
    """Model for user profile."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('user_auth.id'))
    username = Column(String(20))
    fullname = Column(String(200))
    gender = Column(String(10))
    birthdate = Column(DateTime)
    role_id = Column(Integer, ForeignKey('user_roles.id'))
    profile_picture = Column(String(255))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_auth = relationship("UserAuth", back_populates="users")
    user_role = relationship("UserRole", back_populates="users")
