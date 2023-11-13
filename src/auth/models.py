from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, DateTime
from sqlalchemy.orm import relationship

from ..config.database import Base


class HashingAlgorithm(Base):
    __tablename__ = 'hashing_algorithms'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    algorithm_name = Column(String(10))


class UserLoginData(Base):
    __tablename__ = 'user_login'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    login_name = Column(String(20))
    password_hash = Column(String(250))
    password_salt = Column(String(100))
    hash_algorithm_id = Column(Integer, ForeignKey('hashing_algorithms.id'))
    email = Column(String(100))
    confirmation_token = Column(String(100))
    token_generation_time = Column(Date)
    is_active = Column(Boolean, default=False)
    password_recovery_token = Column(String(100))
    recovery_token_time = Column(Date)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    hashing_algorithms = relationship("HashingAlgorithms")
