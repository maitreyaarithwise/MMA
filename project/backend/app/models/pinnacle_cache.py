from sqlalchemy import Column, String, Numeric, DateTime, UniqueConstraint, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..core.database import Base

class PinnacleCache(Base):
    __tablename__ = "pinnacle_cache"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(VARCHAR(50), nullable=False)
    market_name = Column(VARCHAR(50), nullable=False)
    team_name = Column(VARCHAR(50))
    odds = Column(Numeric(15, 5))
    spread_width = Column(Numeric(15, 5))
    last_updated = Column(DateTime(timezone=False), server_default=func.now())
    
    # Unique constraint
    __table_args__ = (UniqueConstraint('event_id', 'market_name', 'team_name'),)

