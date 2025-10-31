from sqlalchemy import Column, String, Boolean, DateTime, Numeric, ForeignKey, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class AutomationRule(Base):
    __tablename__ = "automation_rules"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    rule_name = Column(VARCHAR(50), nullable=False)
    trigger_condition = Column(JSONB, nullable=False)
    adjustment_percent = Column(Numeric(8, 3), default=0.0)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    user = relationship("User")

