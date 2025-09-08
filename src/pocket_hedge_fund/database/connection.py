"""
Database connection management for Pocket Hedge Fund.

This module provides database connectivity, connection pooling,
and session management for the Pocket Hedge Fund system.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
import asyncpg
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Database manager for Pocket Hedge Fund.
    
    Provides connection pooling, session management, and database utilities.
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            database_url: Database connection URL. If None, uses environment variables.
        """
        self.database_url = database_url or self._get_database_url()
        self.engine = None
        self.async_engine = None
        self.session_factory = None
        self.async_session_factory = None
        self._connection_pool = None
        
    def _get_database_url(self) -> str:
        """Get database URL from environment variables."""
        # Try PostgreSQL first
        if os.getenv("DATABASE_URL"):
            return os.getenv("DATABASE_URL")
        
        # Try individual components
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        database = os.getenv("DB_NAME", "pocket_hedge_fund")
        username = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "password")
        
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    async def initialize(self) -> Dict[str, Any]:
        """
        Initialize database connections and engines.
        
        Returns:
            Dict containing initialization results
        """
        try:
            logger.info("Initializing database connections...")
            
            # Create synchronous engine
            self.engine = create_engine(
                self.database_url,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            
            # Create asynchronous engine
            async_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://")
            self.async_engine = create_async_engine(
                async_url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            
            # Create session factories
            self.session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False
            )
            
            self.async_session_factory = sessionmaker(
                bind=self.async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False
            )
            
            # Test connections
            await self._test_connections()
            
            logger.info("Database connections initialized successfully")
            
            return {
                'status': 'success',
                'message': 'Database connections initialized successfully',
                'database_url': self.database_url.replace(self.database_url.split('@')[0].split('//')[1], '***'),
                'pool_size': 10,
                'max_overflow': 20
            }
            
        except Exception as e:
            logger.error(f"Failed to initialize database connections: {e}")
            return {
                'status': 'error',
                'message': f'Failed to initialize database: {str(e)}'
            }
    
    async def _test_connections(self):
        """Test database connections."""
        try:
            # Test synchronous connection
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                assert result.fetchone()[0] == 1
            
            # Test asynchronous connection
            async with self.async_engine.begin() as conn:
                result = await conn.execute(text("SELECT 1"))
                assert result.fetchone()[0] == 1
                
            logger.info("Database connection tests passed")
            
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise
    
    @asynccontextmanager
    async def get_async_session(self):
        """
        Get asynchronous database session.
        
        Yields:
            AsyncSession: Database session
        """
        if not self.async_session_factory:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        async with self.async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    def get_sync_session(self):
        """
        Get synchronous database session.
        
        Returns:
            Session: Database session
        """
        if not self.session_factory:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        return self.session_factory()
    
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a raw SQL query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Query result
        """
        async with self.get_async_session() as session:
            result = await session.execute(text(query), params or {})
            return result.fetchall()
    
    async def execute_scalar(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a scalar query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Scalar result
        """
        async with self.get_async_session() as session:
            result = await session.execute(text(query), params or {})
            return result.scalar()
    
    async def close(self):
        """Close database connections."""
        try:
            if self.async_engine:
                await self.async_engine.dispose()
            if self.engine:
                self.engine.dispose()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")
    
    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get database connection information.
        
        Returns:
            Dict containing connection info
        """
        return {
            'database_url': self.database_url.replace(
                self.database_url.split('@')[0].split('//')[1], '***'
            ),
            'pool_size': 10,
            'max_overflow': 20,
            'engine_initialized': self.engine is not None,
            'async_engine_initialized': self.async_engine is not None
        }


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


async def get_db_manager() -> DatabaseManager:
    """
    Get global database manager instance.
    
    Returns:
        DatabaseManager: Global database manager
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
        await _db_manager.initialize()
    return _db_manager


async def get_db_connection() -> DatabaseManager:
    """
    Get database connection.
    
    Returns:
        DatabaseManager: Database manager instance
    """
    return await get_db_manager()


async def close_db_connections():
    """Close all database connections."""
    global _db_manager
    if _db_manager:
        await _db_manager.close()
        _db_manager = None
