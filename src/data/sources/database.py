"""
Database Data Source Implementation

This module provides database-based data source functionality.
"""

import pandas as pd
from typing import Dict, Any, Optional
import sqlite3

from .base import BaseDataSource
from ...core.exceptions import DataError, ValidationError


class SQLiteDataSource(BaseDataSource):
    """SQLite database data source implementation."""
    
    def __init__(self, db_path: str, table: str, config: Dict[str, Any]):
        """
        Initialize SQLite data source.
        
        Args:
            db_path: Path to SQLite database file
            table: Table name to query
            config: Configuration dictionary
        """
        super().__init__(f"sqlite_{table}", config)
        self.db_path = db_path
        self.table = table
    
    def fetch_data(self, query: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Fetch data from SQLite database.
        
        Args:
            query: SQL query (optional, defaults to SELECT * FROM table)
            **kwargs: Additional parameters
            
        Returns:
            DataFrame containing query results
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            if query is None:
                query = f"SELECT * FROM {self.table}"
            
            data = pd.read_sql_query(query, conn, **kwargs)
            conn.close()
            
            if data.empty:
                raise DataError("Query returned no data")
            
            return data
            
        except Exception as e:
            raise DataError(f"Database query failed: {e}")
    
    def is_available(self) -> bool:
        """Check if database is available."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.close()
            return True
        except Exception:
            return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get database metadata."""
        return {
            "type": "sqlite",
            "db_path": self.db_path,
            "table": self.table,
            "available": self.is_available()
        }


__all__ = ["SQLiteDataSource"]
