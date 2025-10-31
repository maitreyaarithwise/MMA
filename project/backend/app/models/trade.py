from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, CheckConstraint, UniqueConstraint, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    market_id = Column(VARCHAR(50), nullable=False)
    quote_id = Column(VARCHAR(50))
    side = Column(VARCHAR(30), CheckConstraint("side IN ('buy','sell')"), nullable=False)
    price = Column(Numeric(15, 5), nullable=False)
    size = Column(Integer, nullable=False)
    counterparty = Column(VARCHAR(100))
    timestamp = Column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    platform = relationship("Platform")
    
    # Unique constraint
    __table_args__ = (UniqueConstraint('platform_id', 'market_id', 'quote_id'),)

