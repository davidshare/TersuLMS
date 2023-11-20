from sqlalchemy import Column, Integer, String

from ..model_mixins import TimestampMixin
from ..config.database import Base

class HashingAlgorithm(Base, TimestampMixin):
    """Model for hashing algorithms."""
    __tablename__ = 'hashing_algorithms'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    algorithm_name = Column(String(10))