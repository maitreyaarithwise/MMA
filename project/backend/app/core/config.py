import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://postgres:password@localhost/MMA",
        env="DATABASE_URL",
        description="Database connection URL"
    )
    DB_HOST: str = Field(default="localhost", env="DB_HOST")
    DB_PORT: int = Field(default=5432, env="DB_PORT")
    DB_NAME: str = Field(default="MMA", env="DB_NAME")
    DB_USER: str = Field(default="postres", env="DB_USER")
    DB_PASSWORD: str = Field(default="password", env="DB_PASSWORD")
    
    # Pinnacle API Configuration
    PINNACLE_API_KEY: str = Field(
        default="DEMOKEY",
        env="PINNACLE_API_KEY",
        description="Pinnacle API key"
    )
    PINNACLE_HOST: str = Field(
        default="DEMOHOST",
        env="PINNACLE_HOST",
        description="Pinnacle API host"
    )
    PINNACLE_BASE_URL: str = Field(
        default="DEMOURL",
        env="PINNACLE_BASE_URL",
        description="Pinnacle API base URL"
    )
    
    # Kalshi API Configuration
    KALSHI_API_KEY: Optional[str] = Field(default=None, env="KALSHI_API_KEY")
    KALSHI_BASE_URL: str = Field(
        default="https://trading-api.kalshi.com",
        env="KALSHI_BASE_URL",
        description="Kalshi API base URL"
    )
    
    # Application Settings
    APP_NAME: str = Field(
        default="Market Making Trading Dashboard API",
        env="APP_NAME"
    )
    VERSION: str = Field(default="1.0.0", env="VERSION")
    DEBUG: bool = Field(default=False, env="DEBUG", description="Enable debug mode")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8111, env="PORT")
    WORKERS: int = Field(default=1, env="WORKERS")
    
    # Security Settings
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY",
        description="Secret key for JWT tokens"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # CORS Settings
    CORS_ORIGINS: list = Field(
        default=["http://localhost:5173", "http://localhost:8111"],
        env="CORS_ORIGINS"
    )
    
    # Cache Settings
    REDIS_URL: Optional[str] = Field(default=None, env="REDIS_URL")
    CACHE_TTL: int = Field(default=300, env="CACHE_TTL")  # 5 minutes
    
    # Trading Settings
    MAX_POSITION_SIZE: float = Field(default=1000.0, env="MAX_POSITION_SIZE")
    MIN_QUOTE_SIZE: float = Field(default=10.0, env="MIN_QUOTE_SIZE")
    MAX_SPREAD_WIDTH: float = Field(default=5.0, env="MAX_SPREAD_WIDTH")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    def get_database_url(self) -> str:
        """Get database URL, either from DATABASE_URL or constructed from components"""
        if self.DATABASE_URL != "postgresql://user:password@localhost/MMA":
            return self.DATABASE_URL
        
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() == "development"

# Create settings instance
settings = Settings()
