from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, CheckConstraint, VARCHAR
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class QuoteActionLog(Base):
    __tablename__ = "quote_actions_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    market_id = Column(VARCHAR(50), nullable=False)
    action_type = Column(VARCHAR(30), CheckConstraint("action_type IN ('CREATE','UPDATE','DELETE')"))
    quote_id = Column(VARCHAR(50))
    payload = Column(JSONB)
    response_status = Column(VARCHAR(50))
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    platform = relationship("Platform")

