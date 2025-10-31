#!/usr/bin/env python3
"""
Database initialization script
Run this to create all tables in the database
"""
import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.database import (
    create_tables, 
    test_connection, 
    health_check, 
    get_connection_info,
    close_connections
)
from app.core.config import settings

# Import all models to ensure they are registered with SQLAlchemy
from app.models import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database with all tables"""
    print("Starting database initialization...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug mode: {settings.DEBUG}")
    
    # Test database connection first
    print("\nTesting database connection...")
    if not test_connection():
        print("ERROR: Database connection failed!")
        print("Please check your database configuration and ensure the database is running.")
        return False
    
    print("SUCCESS: Database connection successful!")
    
    # Show connection info
    conn_info = get_connection_info()
    print(f"\nConnection Info:")
    print(f"   Database: {conn_info['database_url']}")
    print(f"   Pool size: {conn_info['pool_size']}")
    print(f"   Checked out connections: {conn_info['checked_out_connections']}")
    
    # Create tables
    print("\nCreating database tables...")
    try:
        create_tables()
        print("SUCCESS: Database tables created successfully!")
        
        # Perform health check
        print("\nPerforming health check...")
        health_status = health_check()
        if health_status['status'] == 'healthy':
            print("SUCCESS: Database health check passed!")
        else:
            print("WARNING: Database health check failed!")
            print(f"   Status: {health_status}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Error creating database tables: {e}")
        logger.error(f"Database initialization failed: {e}")
        return False

def main():
    """Main function with proper error handling"""
    try:
        success = init_database()
        if success:
            print("\nDatabase initialization completed successfully!")
            sys.exit(0)
        else:
            print("\nDatabase initialization failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nDatabase initialization cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        logger.error(f"Unexpected error during initialization: {e}")
        sys.exit(1)
    finally:
        # Clean up connections
        close_connections()

if __name__ == "__main__":
    main()
