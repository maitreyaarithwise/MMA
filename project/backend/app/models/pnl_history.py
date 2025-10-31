from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, UniqueConstraint, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class PnlHistory(Base):
    __tablename__ = "pnl_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    market_id = Column(VARCHAR(50))
    realized_pnl = Column(Numeric(15, 5), default=0)
    unrealized_pnl = Column(Numeric(15, 5), default=0)
    total_pnl = Column(Numeric(15, 5))  # This would be calculated in the application layer
    recorded_at = Column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    platform = relationship("Platform")
    
    # Unique constraint
    __table_args__ = (UniqueConstraint('user_id', 'platform_id', 'market_id', 'recorded_at'),)

