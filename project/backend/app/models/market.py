from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Market(Base):
    __tablename__ = "markets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform_id = Column(Integer, ForeignKey("platforms.id", ondelete="CASCADE"))
    market_id = Column(VARCHAR(50), nullable=False)
    sport = Column(VARCHAR(50), default='NFL')
    market_name = Column(VARCHAR(50))
    event_name = Column(VARCHAR(50))
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    platform = relationship("Platform", back_populates="markets")
    
    # Unique constraint
    __table_args__ = (UniqueConstraint('platform_id', 'market_id'),)

