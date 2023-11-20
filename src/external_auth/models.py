from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..config.database import Base
from ..model_mixins import TimestampMixin
    
class ExternalProvider(Base, TimestampMixin):
    """Model for external providers."""
    __tablename__ = 'external_providers'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    provider_name = Column(String(50))
    web_service_endpoint = Column(String(200))

class ExternalUserAuth(Base, TimestampMixin):
    """Model for external user authentication."""
    __tablename__ = 'external_user_auth'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('user_auth.id'))
    provider_id = Column(Integer, ForeignKey('external_providers.id'))
    provider_token = Column(String(100))
    external_provider = relationship("ExternalProvider")

