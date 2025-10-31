from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, CheckConstraint, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(VARCHAR(30), CheckConstraint("type IN ('fill','timeout','error','system')"))
    message = Column(VARCHAR(255), nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    user = relationship("User")

