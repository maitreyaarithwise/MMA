from sqlalchemy import Column, String, Integer, DateTime, Numeric, Boolean, ForeignKey, UniqueConstraint, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class CounterpartyStats(Base):
    __tablename__ = "counterparty_stats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    counterparty_id = Column(VARCHAR(50), nullable=False)
    trades_count = Column(Integer, default=0)
    cumulative_pnl = Column(Numeric(15, 5), default=0)
    sharp_flag = Column(Boolean, default=False)
    last_updated = Column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    platform = relationship("Platform")
    
    # Unique constraint
    __table_args__ = (UniqueConstraint('platform_id', 'counterparty_id'),)

