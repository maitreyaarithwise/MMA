from sqlalchemy import Column, String, Integer, DateTime, Text, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Platform(Base):
    __tablename__ = "platforms"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False, unique=True)
    base_url = Column(VARCHAR(100), nullable=False)
    rate_limit_per_min = Column(Integer)
    account_id_encrypted = Column(String)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    markets = relationship("Market", back_populates="platform")
