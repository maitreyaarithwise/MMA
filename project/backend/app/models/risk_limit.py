from sqlalchemy import Column, String, Boolean, DateTime, Numeric, ForeignKey, CheckConstraint, UniqueConstraint, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class RiskLimit(Base):
    __tablename__ = "risk_limits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    market_id = Column(VARCHAR(50))
    limit_type = Column(VARCHAR(30), CheckConstraint("limit_type IN ('position','stop_loss','quote_size')"))
    limit_value = Column(Numeric(15, 5), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    platform = relationship("Platform")
    
    # Unique constraint
    __table_args__ = (UniqueConstraint('user_id', 'platform_id', 'market_id', 'limit_type'),)

