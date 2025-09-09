"""
Database Connection Manager for Pocket Hedge Fund

This module provides database connection management, connection pooling,
and database operations for the Pocket Hedge Fund system.
"""

import asyncio
import logging
import os
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager
import asyncpg
from asyncpg import Pool, Connection
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration class."""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', '5432'))
        self.database = os.getenv('DB_NAME', 'neozork_fund')
        self.username = os.getenv('DB_USER', 'neozork_user')
        self.password = os.getenv('DB_PASSWORD', 'neozork_password')
        self.pool_size = int(os.getenv('DB_POOL_SIZE', '10'))
        self.max_overflow = int(os.getenv('DB_MAX_OVERFLOW', '20'))
        self.pool_timeout = int(os.getenv('DB_POOL_TIMEOUT', '30'))
        self.pool_recycle = int(os.getenv('DB_POOL_RECYCLE', '3600'))
        
    @property
    def sync_url(self) -> str:
        """Get synchronous database URL."""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    @property
    def async_url(self) -> str:
        """Get asynchronous database URL."""
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class DatabaseManager:
    """
    Database connection manager with connection pooling and async support.
    
    This class provides:
    - Connection pooling for better performance
    - Async and sync database operations
    - Automatic connection management
    - Error handling and retry logic
    - Transaction management
    """
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self._pool: Optional[Pool] = None
        self._sync_engine = None
        self._async_engine = None
        self._async_session_factory = None
        self._sync_session_factory = None
        self._initialized = False
        
    async def initialize(self):
        """Initialize database connections and pools."""
        try:
            logger.info("Initializing database connections...")
            
            # Initialize async connection pool
            self._pool = await asyncpg.create_pool(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                min_size=5,
                max_size=self.config.pool_size,
                command_timeout=self.config.pool_timeout
            )
            
            # Initialize SQLAlchemy engines
            self._sync_engine = create_engine(
                self.config.sync_url,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                echo=False
            )
            
            self._async_engine = create_async_engine(
                self.config.async_url,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                echo=False
            )
            
            # Initialize session factories
            self._sync_session_factory = sessionmaker(
                bind=self._sync_engine,
                autocommit=False,
                autoflush=False
            )
            
            self._async_session_factory = async_sessionmaker(
                bind=self._async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False
            )
            
            # Test connections
            await self._test_connections()
            
            self._initialized = True
            logger.info("Database connections initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connections: {e}")
            raise
    
    async def _test_connections(self):
        """Test database connections."""
        try:
            # Test async connection
            async with self._pool.acquire() as conn:
                result = await conn.fetchval("SELECT 1")
                assert result == 1
            
            # Test sync connection
            with self._sync_engine.connect() as conn:
                result = conn.execute(text("SELECT 1")).scalar()
                assert result == 1
                
            logger.info("Database connection tests passed")
            
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise
    
    @asynccontextmanager
    async def get_connection(self):
        """Get async database connection from pool."""
        if not self._initialized:
            await self.initialize()
        
        conn = None
        try:
            conn = await self._pool.acquire()
            yield conn
        finally:
            if conn:
                await self._pool.release(conn)
    
    @asynccontextmanager
    async def get_session(self):
        """Get async SQLAlchemy session."""
        if not self._initialized:
            await self.initialize()
        
        async with self._async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    @asynccontextmanager
    def get_sync_session(self):
        """Get sync SQLAlchemy session."""
        if not self._initialized:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        session = self._sync_session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute async query and return results."""
        async with self.get_connection() as conn:
            try:
                if params:
                    rows = await conn.fetch(query, *params.values())
                else:
                    rows = await conn.fetch(query)
                
                return [dict(row) for row in rows]
            except Exception as e:
                logger.error(f"Query execution failed: {e}")
                raise
    
    async def execute_query_named(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute async query with named parameters and return results."""
        async with self.get_connection() as conn:
            try:
                if params:
                    rows = await conn.fetch(query, **params)
                else:
                    rows = await conn.fetch(query)
                
                return [dict(row) for row in rows]
            except Exception as e:
                logger.error(f"Query execution failed: {e}")
                raise
    
    async def execute_command(self, command: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Execute async command and return result."""
        async with self.get_connection() as conn:
            try:
                if params:
                    result = await conn.execute(command, *params.values())
                else:
                    result = await conn.execute(command)
                
                return result
            except Exception as e:
                logger.error(f"Command execution failed: {e}")
                raise
    
    def execute_sync_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute sync query and return results."""
        try:
            with psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password
            ) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    
                    rows = cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Sync query execution failed: {e}")
            raise
    
    async def create_tables(self):
        """Create database tables from schema."""
        try:
            schema_path = os.path.join(
                os.path.dirname(__file__), 
                'schema.sql'
            )
            
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            async with self.get_connection() as conn:
                await conn.execute(schema_sql)
            
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    async def drop_tables(self):
        """Drop all database tables."""
        try:
            tables = [
                'audit_log', 'api_keys', 'risk_metrics', 'performance_snapshots',
                'transactions', 'fund_strategies', 'trading_strategies',
                'portfolio_positions', 'investors', 'funds', 'users'
            ]
            
            async with self.get_connection() as conn:
                for table in tables:
                    await conn.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            
            logger.info("Database tables dropped successfully")
            
        except Exception as e:
            logger.error(f"Failed to drop tables: {e}")
            raise
    
    async def reset_database(self):
        """Reset database by dropping and recreating tables."""
        try:
            logger.info("Resetting database...")
            await self.drop_tables()
            await self.create_tables()
            logger.info("Database reset completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to reset database: {e}")
            raise
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            stats = {}
            
            # Get table sizes
            size_query = """
                SELECT 
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
            """
            
            stats['table_sizes'] = await self.execute_query(size_query)
            
            # Get connection info
            conn_query = """
                SELECT 
                    count(*) as total_connections,
                    count(*) FILTER (WHERE state = 'active') as active_connections,
                    count(*) FILTER (WHERE state = 'idle') as idle_connections
                FROM pg_stat_activity 
                WHERE datname = current_database();
            """
            
            conn_stats = await self.execute_query(conn_query)
            stats['connections'] = conn_stats[0] if conn_stats else {}
            
            # Get database size
            db_size_query = "SELECT pg_size_pretty(pg_database_size(current_database())) as database_size;"
            db_size = await self.execute_query(db_size_query)
            stats['database_size'] = db_size[0]['database_size'] if db_size else 'Unknown'
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {}
    
    async def close(self):
        """Close all database connections."""
        try:
            if self._pool:
                await self._pool.close()
            
            if self._async_engine:
                await self._async_engine.dispose()
            
            if self._sync_engine:
                self._sync_engine.dispose()
            
            self._initialized = False
            logger.info("Database connections closed")
            
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")


# Global database manager instance
db_manager = DatabaseManager()


async def get_db_manager() -> DatabaseManager:
    """Get global database manager instance."""
    if not db_manager._initialized:
        await db_manager.initialize()
    return db_manager


async def init_database():
    """Initialize database with tables and sample data."""
    manager = await get_db_manager()
    await manager.create_tables()
    logger.info("Database initialized successfully")


async def close_database():
    """Close database connections."""
    await db_manager.close()
    logger.info("Database connections closed")