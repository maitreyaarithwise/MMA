from sqlalchemy import Column, String, DateTime, Text, CheckConstraint, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(50), nullable=False, unique=True)
    first_name = Column(VARCHAR(50), nullable=False)
    last_name = Column(VARCHAR(50), nullable=False)
    phone_number = Column(VARCHAR(30), nullable=False, unique=True)
    email = Column(VARCHAR(50), unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(VARCHAR(30), CheckConstraint("role IN ('admin','trader')"), default='trader')
    kalshi_api_key_encrypted = Column(String)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    last_login = Column(DateTime(timezone=False))
