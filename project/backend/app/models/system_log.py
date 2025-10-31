from sqlalchemy import Column, String, DateTime, CheckConstraint, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from ..core.database import Base

class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(VARCHAR(30), CheckConstraint("level IN ('info','warn','error')"), nullable=False)
    message = Column(VARCHAR(255), nullable=False)
    context = Column(JSONB)
    timestamp = Column(DateTime(timezone=False), server_default=func.now())
