"""Database Manager - Database connection and query management system"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import json
import asyncpg
import aioredis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text, select, insert, update, delete
import pandas as pd

logger = logging.getLogger(__name__)


class DatabaseType(Enum):
    """Database type enumeration."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    REDIS = "redis"
    MONGODB = "mongodb"


class QueryType(Enum):
    """Query type enumeration."""
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"


class ConnectionStatus(Enum):
    """Connection status enumeration."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass
class DatabaseConfig:
    """Database configuration data class."""
    db_type: DatabaseType
    host: str
    port: int
    database: str
    username: str
    password: str
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600
    echo: bool = False
    ssl_mode: str = "prefer"


@dataclass
class QueryResult:
    """Query result data class."""
    query_id: str
    query_type: QueryType
    execution_time: float
    rows_affected: int
    data: List[Dict[str, Any]]
    error: Optional[str] = None
    executed_at: datetime = None


@dataclass
class ConnectionInfo:
    """Database connection information."""
    connection_id: str
    db_type: DatabaseType
    status: ConnectionStatus
    created_at: datetime
    last_used: datetime
    query_count: int = 0
    error_count: int = 0


# SQLAlchemy Base
Base = declarative_base()


class DatabaseManager:
    """Database connection and query management system."""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = None
        self.session_factory = None
        self.redis_pool = None
        self.connections: Dict[str, ConnectionInfo] = {}
        self.query_cache: Dict[str, Any] = {}
        self.connection_pools: Dict[str, Any] = {}
        
        # Initialize database components
        self._initialize_database_components()
        
    def _initialize_database_components(self):
        """Initialize database components."""
        try:
            if self.config.db_type == DatabaseType.POSTGRESQL:
                self._initialize_postgresql()
            elif self.config.db_type == DatabaseType.REDIS:
                self._initialize_redis()
            elif self.config.db_type == DatabaseType.SQLITE:
                self._initialize_sqlite()
            else:
                logger.warning(f"Database type {self.config.db_type.value} not fully supported yet")
                
        except Exception as e:
            logger.error(f"Failed to initialize database components: {e}")
    
    def _initialize_postgresql(self):
        """Initialize PostgreSQL connection."""
        try:
            # Create async engine
            database_url = f"postgresql+asyncpg://{self.config.username}:{self.config.password}@{self.config.host}:{self.config.port}/{self.config.database}"
            
            self.engine = create_async_engine(
                database_url,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                echo=self.config.echo
            )
            
            # Create session factory
            self.session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            logger.info("Initialized PostgreSQL connection")
            
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL: {e}")
    
    def _initialize_redis(self):
        """Initialize Redis connection."""
        try:
            # Redis will be initialized when needed
            logger.info("Redis connection will be initialized on first use")
            
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
    
    def _initialize_sqlite(self):
        """Initialize SQLite connection."""
        try:
            # Create async engine for SQLite
            database_url = f"sqlite+aiosqlite:///{self.config.database}"
            
            self.engine = create_async_engine(
                database_url,
                echo=self.config.echo,
                pool_pre_ping=True
            )
            
            # Create session factory
            self.session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            logger.info("Initialized SQLite connection")
            
        except Exception as e:
            logger.error(f"Failed to initialize SQLite: {e}")
    
    async def connect(self) -> Dict[str, Any]:
        """Establish database connection."""
        try:
            if self.config.db_type == DatabaseType.POSTGRESQL:
                return await self._connect_postgresql()
            elif self.config.db_type == DatabaseType.REDIS:
                return await self._connect_redis()
            elif self.config.db_type == DatabaseType.SQLITE:
                return await self._connect_sqlite()
            else:
                return {'error': f'Unsupported database type: {self.config.db_type.value}'}
                
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return {'error': str(e)}
    
    async def _connect_postgresql(self) -> Dict[str, Any]:
        """Connect to PostgreSQL database."""
        try:
            # Test connection
            async with self.engine.begin() as conn:
                result = await conn.execute(text("SELECT 1"))
                result.fetchone()
            
            # Create connection info
            connection_id = str(uuid.uuid4())
            connection_info = ConnectionInfo(
                connection_id=connection_id,
                db_type=self.config.db_type,
                status=ConnectionStatus.CONNECTED,
                created_at=datetime.now(),
                last_used=datetime.now()
            )
            
            self.connections[connection_id] = connection_info
            
            logger.info("Connected to PostgreSQL database")
            return {
                'status': 'success',
                'connection_id': connection_id,
                'db_type': self.config.db_type.value,
                'host': self.config.host,
                'database': self.config.database
            }
            
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            return {'error': str(e)}
    
    async def _connect_redis(self) -> Dict[str, Any]:
        """Connect to Redis database."""
        try:
            # Create Redis connection pool
            self.redis_pool = aioredis.ConnectionPool.from_url(
                f"redis://{self.config.host}:{self.config.port}/{self.config.database}",
                max_connections=self.config.pool_size
            )
            
            # Test connection
            redis = aioredis.Redis(connection_pool=self.redis_pool)
            await redis.ping()
            
            # Create connection info
            connection_id = str(uuid.uuid4())
            connection_info = ConnectionInfo(
                connection_id=connection_id,
                db_type=self.config.db_type,
                status=ConnectionStatus.CONNECTED,
                created_at=datetime.now(),
                last_used=datetime.now()
            )
            
            self.connections[connection_id] = connection_info
            
            logger.info("Connected to Redis database")
            return {
                'status': 'success',
                'connection_id': connection_id,
                'db_type': self.config.db_type.value,
                'host': self.config.host,
                'database': self.config.database
            }
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return {'error': str(e)}
    
    async def _connect_sqlite(self) -> Dict[str, Any]:
        """Connect to SQLite database."""
        try:
            # Test connection
            async with self.engine.begin() as conn:
                result = await conn.execute(text("SELECT 1"))
                result.fetchone()
            
            # Create connection info
            connection_id = str(uuid.uuid4())
            connection_info = ConnectionInfo(
                connection_id=connection_id,
                db_type=self.config.db_type,
                status=ConnectionStatus.CONNECTED,
                created_at=datetime.now(),
                last_used=datetime.now()
            )
            
            self.connections[connection_id] = connection_info
            
            logger.info("Connected to SQLite database")
            return {
                'status': 'success',
                'connection_id': connection_id,
                'db_type': self.config.db_type.value,
                'database': self.config.database
            }
            
        except Exception as e:
            logger.error(f"Failed to connect to SQLite: {e}")
            return {'error': str(e)}
    
    async def execute_query(self, query: str, params: Dict[str, Any] = None, 
                          query_type: QueryType = QueryType.SELECT) -> Dict[str, Any]:
        """Execute database query."""
        try:
            start_time = datetime.now()
            query_id = str(uuid.uuid4())
            
            if self.config.db_type == DatabaseType.POSTGRESQL:
                result = await self._execute_postgresql_query(query, params, query_type)
            elif self.config.db_type == DatabaseType.REDIS:
                result = await self._execute_redis_query(query, params, query_type)
            elif self.config.db_type == DatabaseType.SQLITE:
                result = await self._execute_sqlite_query(query, params, query_type)
            else:
                return {'error': f'Unsupported database type: {self.config.db_type.value}'}
            
            if 'error' in result:
                return result
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Create query result
            query_result = QueryResult(
                query_id=query_id,
                query_type=query_type,
                execution_time=execution_time,
                rows_affected=result.get('rows_affected', 0),
                data=result.get('data', []),
                executed_at=datetime.now()
            )
            
            # Update connection info
            for connection_info in self.connections.values():
                if connection_info.status == ConnectionStatus.CONNECTED:
                    connection_info.last_used = datetime.now()
                    connection_info.query_count += 1
                    break
            
            logger.info(f"Executed {query_type.value} query in {execution_time:.3f}s")
            return {
                'status': 'success',
                'query_result': query_result.__dict__,
                'execution_time': execution_time
            }
            
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            return {'error': str(e)}
    
    async def _execute_postgresql_query(self, query: str, params: Dict[str, Any], 
                                      query_type: QueryType) -> Dict[str, Any]:
        """Execute PostgreSQL query."""
        try:
            async with self.session_factory() as session:
                if query_type == QueryType.SELECT:
                    result = await session.execute(text(query), params or {})
                    rows = result.fetchall()
                    data = [dict(row._mapping) for row in rows]
                    return {'data': data, 'rows_affected': len(data)}
                
                elif query_type == QueryType.INSERT:
                    result = await session.execute(text(query), params or {})
                    await session.commit()
                    return {'rows_affected': result.rowcount, 'data': []}
                
                elif query_type == QueryType.UPDATE:
                    result = await session.execute(text(query), params or {})
                    await session.commit()
                    return {'rows_affected': result.rowcount, 'data': []}
                
                elif query_type == QueryType.DELETE:
                    result = await session.execute(text(query), params or {})
                    await session.commit()
                    return {'rows_affected': result.rowcount, 'data': []}
                
                else:
                    result = await session.execute(text(query), params or {})
                    await session.commit()
                    return {'rows_affected': result.rowcount, 'data': []}
                    
        except Exception as e:
            return {'error': str(e)}
    
    async def _execute_redis_query(self, query: str, params: Dict[str, Any], 
                                 query_type: QueryType) -> Dict[str, Any]:
        """Execute Redis query."""
        try:
            redis = aioredis.Redis(connection_pool=self.redis_pool)
            
            # Parse Redis command
            parts = query.strip().split()
            command = parts[0].upper()
            args = parts[1:] if len(parts) > 1 else []
            
            # Execute Redis command
            if command == "GET":
                result = await redis.get(args[0])
                return {'data': [{'value': result.decode() if result else None}], 'rows_affected': 1}
            
            elif command == "SET":
                await redis.set(args[0], args[1])
                return {'rows_affected': 1, 'data': []}
            
            elif command == "HGET":
                result = await redis.hget(args[0], args[1])
                return {'data': [{'value': result.decode() if result else None}], 'rows_affected': 1}
            
            elif command == "HSET":
                result = await redis.hset(args[0], args[1], args[2])
                return {'rows_affected': result, 'data': []}
            
            elif command == "DEL":
                result = await redis.delete(args[0])
                return {'rows_affected': result, 'data': []}
            
            else:
                return {'error': f'Unsupported Redis command: {command}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    async def _execute_sqlite_query(self, query: str, params: Dict[str, Any], 
                                  query_type: QueryType) -> Dict[str, Any]:
        """Execute SQLite query."""
        try:
            async with self.session_factory() as session:
                if query_type == QueryType.SELECT:
                    result = await session.execute(text(query), params or {})
                    rows = result.fetchall()
                    data = [dict(row._mapping) for row in rows]
                    return {'data': data, 'rows_affected': len(data)}
                
                else:
                    result = await session.execute(text(query), params or {})
                    await session.commit()
                    return {'rows_affected': result.rowcount, 'data': []}
                    
        except Exception as e:
            return {'error': str(e)}
    
    async def execute_batch_queries(self, queries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute multiple queries in batch."""
        try:
            results = []
            total_execution_time = 0
            
            for query_info in queries:
                query = query_info['query']
                params = query_info.get('params', {})
                query_type = QueryType(query_info.get('type', 'select'))
                
                result = await self.execute_query(query, params, query_type)
                if 'error' in result:
                    return {'error': f'Batch query failed: {result["error"]}'}
                
                results.append(result)
                total_execution_time += result['execution_time']
            
            logger.info(f"Executed {len(queries)} batch queries in {total_execution_time:.3f}s")
            return {
                'status': 'success',
                'results': results,
                'total_queries': len(queries),
                'total_execution_time': total_execution_time
            }
            
        except Exception as e:
            logger.error(f"Failed to execute batch queries: {e}")
            return {'error': str(e)}
    
    async def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get table information."""
        try:
            if self.config.db_type == DatabaseType.POSTGRESQL:
                query = """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = :table_name
                ORDER BY ordinal_position
                """
            elif self.config.db_type == DatabaseType.SQLITE:
                query = f"PRAGMA table_info({table_name})"
            else:
                return {'error': f'Table info not supported for {self.config.db_type.value}'}
            
            result = await self.execute_query(query, {'table_name': table_name})
            if 'error' in result:
                return result
            
            return {
                'status': 'success',
                'table_name': table_name,
                'columns': result['query_result']['data']
            }
            
        except Exception as e:
            logger.error(f"Failed to get table info: {e}")
            return {'error': str(e)}
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            stats = {
                'db_type': self.config.db_type.value,
                'host': self.config.host,
                'database': self.config.database,
                'active_connections': len([c for c in self.connections.values() 
                                         if c.status == ConnectionStatus.CONNECTED]),
                'total_connections': len(self.connections),
                'total_queries': sum(c.query_count for c in self.connections.values()),
                'total_errors': sum(c.error_count for c in self.connections.values())
            }
            
            # Get database-specific stats
            if self.config.db_type == DatabaseType.POSTGRESQL:
                db_stats = await self._get_postgresql_stats()
                stats.update(db_stats)
            elif self.config.db_type == DatabaseType.REDIS:
                db_stats = await self._get_redis_stats()
                stats.update(db_stats)
            
            return {
                'status': 'success',
                'stats': stats
            }
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {'error': str(e)}
    
    async def _get_postgresql_stats(self) -> Dict[str, Any]:
        """Get PostgreSQL specific statistics."""
        try:
            # Get database size
            size_query = "SELECT pg_size_pretty(pg_database_size(current_database())) as size"
            size_result = await self.execute_query(size_query)
            
            # Get table count
            table_query = """
            SELECT COUNT(*) as table_count
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """
            table_result = await self.execute_query(table_query)
            
            return {
                'database_size': size_result['query_result']['data'][0]['size'] if size_result['query_result']['data'] else 'Unknown',
                'table_count': table_result['query_result']['data'][0]['table_count'] if table_result['query_result']['data'] else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to get PostgreSQL stats: {e}")
            return {}
    
    async def _get_redis_stats(self) -> Dict[str, Any]:
        """Get Redis specific statistics."""
        try:
            redis = aioredis.Redis(connection_pool=self.redis_pool)
            info = await redis.info()
            
            return {
                'redis_version': info.get('redis_version', 'Unknown'),
                'used_memory': info.get('used_memory_human', 'Unknown'),
                'connected_clients': info.get('connected_clients', 0),
                'total_commands_processed': info.get('total_commands_processed', 0)
            }
            
        except Exception as e:
            logger.error(f"Failed to get Redis stats: {e}")
            return {}
    
    async def disconnect(self) -> Dict[str, Any]:
        """Disconnect from database."""
        try:
            # Close SQLAlchemy engine
            if self.engine:
                await self.engine.dispose()
            
            # Close Redis pool
            if self.redis_pool:
                await self.redis_pool.disconnect()
            
            # Update connection status
            for connection_info in self.connections.values():
                connection_info.status = ConnectionStatus.DISCONNECTED
            
            logger.info("Disconnected from database")
            return {
                'status': 'success',
                'message': 'Disconnected from database'
            }
            
        except Exception as e:
            logger.error(f"Failed to disconnect from database: {e}")
            return {'error': str(e)}
    
    def get_database_summary(self) -> Dict[str, Any]:
        """Get database manager summary."""
        active_connections = len([c for c in self.connections.values() 
                                if c.status == ConnectionStatus.CONNECTED])
        total_queries = sum(c.query_count for c in self.connections.values())
        total_errors = sum(c.error_count for c in self.connections.values())
        
        return {
            'db_type': self.config.db_type.value,
            'host': self.config.host,
            'database': self.config.database,
            'active_connections': active_connections,
            'total_connections': len(self.connections),
            'total_queries': total_queries,
            'total_errors': total_errors,
            'cache_size': len(self.query_cache)
        }
