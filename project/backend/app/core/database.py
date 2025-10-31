"""
Database configuration and connection management
"""
import os
import logging
from typing import Generator, Optional
from contextlib import contextmanager
from sqlalchemy import create_engine, text, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from dotenv import load_dotenv

from .config import settings

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Database URL configuration
DATABASE_URL = settings.get_database_url()

# Engine configuration with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    echo_pool=settings.DEBUG,  # Log pool events in debug mode
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Connection event listeners for monitoring
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set database-specific pragmas for SQLite (if used)"""
    if "sqlite" in DATABASE_URL:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    """Log when a connection is checked out from the pool"""
    logger.debug("Connection checked out from pool")

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    """Log when a connection is checked in to the pool"""
    logger.debug("Connection checked in to pool")

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    This is the main function to use in FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Use this for non-FastAPI contexts.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def test_connection() -> bool:
    """
    Test database connection.
    Returns True if connection is successful, False otherwise.
    """
    try:
        with engine.connect() as connection:
            # Execute a simple query to test connection
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            logger.info("Database connection test successful")
            return True
    except OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error testing database connection: {e}")
        return False

def get_connection_info() -> dict:
    """
    Get database connection information.
    Returns a dictionary with connection details (excluding sensitive data).
    """
    return {
        "database_url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else "hidden",
        "pool_size": engine.pool.size(),
        "checked_out_connections": engine.pool.checkedout(),
        "overflow_connections": engine.pool.overflow(),
        "pool_status": engine.pool.status()
    }

def create_tables():
    """
    Create all tables defined in the models.
    This is typically called during application startup.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def drop_tables():
    """
    Drop all tables.
    WARNING: This will delete all data!
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped")
    except SQLAlchemyError as e:
        logger.error(f"Error dropping database tables: {e}")
        raise

def get_engine() -> Engine:
    """
    Get the database engine.
    Useful for advanced database operations.
    """
    return engine

def close_connections():
    """
    Close all database connections.
    Call this during application shutdown.
    """
    try:
        engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")

# Health check function
def health_check() -> dict:
    """
    Perform a comprehensive database health check.
    Returns a dictionary with health status and metrics.
    """
    try:
        # Test basic connection
        connection_ok = test_connection()
        
        # Get connection pool info
        pool_info = get_connection_info()
        
        # Test a simple query
        query_ok = False
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM information_schema.tables"))
                query_ok = True
        except Exception as e:
            logger.error(f"Query test failed: {e}")
        
        return {
            "status": "healthy" if connection_ok and query_ok else "unhealthy",
            "connection": connection_ok,
            "query": query_ok,
            "pool_info": pool_info,
            "database_url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else "hidden"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# Initialize database on module import (optional)
if settings.DEBUG:
    logger.info("Database module initialized")
    logger.info(f"Database URL: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else 'hidden'}")
