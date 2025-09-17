"""
Database utilities for Pocket Hedge Fund.

This module provides utility functions for database operations,
data validation, and common database tasks.
"""

import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, date
from decimal import Decimal
import json

from sqlalchemy import text, func, and_, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .connection import DatabaseManager
from .models import (
    UserModel, FundModel, PortfolioModel, PerformanceModel,
    TransactionModel, StrategyModel, InvestmentModel, RiskModel
)

logger = logging.getLogger(__name__)


class DatabaseUtils:
    """
    Database utilities for common operations.
    
    Provides helper methods for data validation, queries, and operations.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize database utils.
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
    
    async def validate_user_exists(self, user_id: str) -> bool:
        """
        Validate if user exists.
        
        Args:
            user_id: User ID to validate
            
        Returns:
            True if user exists, False otherwise
        """
        try:
            async with self.db_manager.get_async_session() as session:
                result = await session.execute(
                    text("SELECT 1 FROM users WHERE id = :user_id"),
                    {"user_id": user_id}
                )
                return result.fetchone() is not None
        except Exception as e:
            logger.error(f"Error validating user existence: {e}")
            return False
    
    async def validate_fund_exists(self, fund_id: str) -> bool:
        """
        Validate if fund exists.
        
        Args:
            fund_id: Fund ID to validate
            
        Returns:
            True if fund exists, False otherwise
        """
        try:
            async with self.db_manager.get_async_session() as session:
                result = await session.execute(
                    text("SELECT 1 FROM funds WHERE id = :fund_id"),
                    {"fund_id": fund_id}
                )
                return result.fetchone() is not None
        except Exception as e:
            logger.error(f"Error validating fund existence: {e}")
            return False
    
    async def get_fund_summary(self, fund_id: str) -> Optional[Dict[str, Any]]:
        """
        Get fund summary information.
        
        Args:
            fund_id: Fund ID
            
        Returns:
            Dict containing fund summary or None
        """
        try:
            async with self.db_manager.get_async_session() as session:
                # Get fund basic info
                fund_result = await session.execute(
                    text("""
                        SELECT f.*, u.email as manager_email, u.first_name, u.last_name
                        FROM funds f
                        JOIN users u ON f.manager_id = u.id
                        WHERE f.id = :fund_id
                    """),
                    {"fund_id": fund_id}
                )
                fund = fund_result.fetchone()
                
                if not fund:
                    return None
                
                # Get portfolio summary
                portfolio_result = await session.execute(
                    text("""
                        SELECT 
                            COUNT(*) as total_positions,
                            SUM(market_value) as total_market_value,
                            SUM(unrealized_pnl) as total_unrealized_pnl
                        FROM portfolios
                        WHERE fund_id = :fund_id
                    """),
                    {"fund_id": fund_id}
                )
                portfolio = portfolio_result.fetchone()
                
                # Get latest performance
                performance_result = await session.execute(
                    text("""
                        SELECT *
                        FROM performances
                        WHERE fund_id = :fund_id
                        ORDER BY date DESC
                        LIMIT 1
                    """),
                    {"fund_id": fund_id}
                )
                performance = performance_result.fetchone()
                
                return {
                    'fund': dict(fund._mapping) if fund else None,
                    'portfolio': dict(portfolio._mapping) if portfolio else None,
                    'performance': dict(performance._mapping) if performance else None
                }
                
        except Exception as e:
            logger.error(f"Error getting fund summary: {e}")
            return None
    
    async def get_user_funds(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all funds for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of fund dictionaries
        """
        try:
            async with self.db_manager.get_async_session() as session:
                result = await session.execute(
                    text("""
                        SELECT f.*, 
                               COUNT(p.id) as position_count,
                               SUM(p.market_value) as total_value
                        FROM funds f
                        LEFT JOIN portfolios p ON f.id = p.fund_id
                        WHERE f.manager_id = :user_id
                        GROUP BY f.id
                        ORDER BY f.created_at DESC
                    """),
                    {"user_id": user_id}
                )
                
                funds = []
                for row in result:
                    funds.append(dict(row._mapping))
                
                return funds
                
        except Exception as e:
            logger.error(f"Error getting user funds: {e}")
            return []
    
    async def get_portfolio_positions(self, fund_id: str) -> List[Dict[str, Any]]:
        """
        Get portfolio positions for a fund.
        
        Args:
            fund_id: Fund ID
            
        Returns:
            List of position dictionaries
        """
        try:
            async with self.db_manager.get_async_session() as session:
                result = await session.execute(
                    text("""
                        SELECT *
                        FROM portfolios
                        WHERE fund_id = :fund_id
                        ORDER BY market_value DESC
                    """),
                    {"fund_id": fund_id}
                )
                
                positions = []
                for row in result:
                    positions.append(dict(row._mapping))
                
                return positions
                
        except Exception as e:
            logger.error(f"Error getting portfolio positions: {e}")
            return []
    
    async def get_performance_history(self, fund_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get performance history for a fund.
        
        Args:
            fund_id: Fund ID
            days: Number of days to retrieve
            
        Returns:
            List of performance dictionaries
        """
        try:
            async with self.db_manager.get_async_session() as session:
                result = await session.execute(
                    text("""
                        SELECT *
                        FROM performances
                        WHERE fund_id = :fund_id
                        ORDER BY date DESC
                        LIMIT :days
                    """),
                    {"fund_id": fund_id, "days": days}
                )
                
                performance = []
                for row in result:
                    performance.append(dict(row._mapping))
                
                return performance
                
        except Exception as e:
            logger.error(f"Error getting performance history: {e}")
            return []
    
    async def get_transaction_history(self, fund_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get transaction history for a fund.
        
        Args:
            fund_id: Fund ID
            limit: Maximum number of transactions to retrieve
            
        Returns:
            List of transaction dictionaries
        """
        try:
            async with self.db_manager.get_async_session() as session:
                result = await session.execute(
                    text("""
                        SELECT *
                        FROM transactions
                        WHERE fund_id = :fund_id
                        ORDER BY created_at DESC
                        LIMIT :limit
                    """),
                    {"fund_id": fund_id, "limit": limit}
                )
                
                transactions = []
                for row in result:
                    transactions.append(dict(row._mapping))
                
                return transactions
                
        except Exception as e:
            logger.error(f"Error getting transaction history: {e}")
            return []
    
    async def calculate_portfolio_metrics(self, fund_id: str) -> Dict[str, Any]:
        """
        Calculate portfolio metrics for a fund.
        
        Args:
            fund_id: Fund ID
            
        Returns:
            Dict containing portfolio metrics
        """
        try:
            async with self.db_manager.get_async_session() as session:
                # Get portfolio summary
                result = await session.execute(
                    text("""
                        SELECT 
                            COUNT(*) as total_positions,
                            SUM(market_value) as total_market_value,
                            SUM(unrealized_pnl) as total_unrealized_pnl,
                            AVG(position_size_pct) as avg_position_size,
                            MAX(position_size_pct) as max_position_size,
                            MIN(position_size_pct) as min_position_size
                        FROM portfolios
                        WHERE fund_id = :fund_id
                    """),
                    {"fund_id": fund_id}
                )
                
                portfolio_metrics = result.fetchone()
                
                if not portfolio_metrics:
                    return {}
                
                # Get fund cash balance
                fund_result = await session.execute(
                    text("""
                        SELECT current_capital
                        FROM funds
                        WHERE id = :fund_id
                    """),
                    {"fund_id": fund_id}
                )
                fund = fund_result.fetchone()
                
                total_capital = float(fund.current_capital) if fund else 0.0
                total_market_value = float(portfolio_metrics.total_market_value) if portfolio_metrics.total_market_value else 0.0
                cash_balance = total_capital - total_market_value
                
                return {
                    'total_positions': portfolio_metrics.total_positions or 0,
                    'total_market_value': total_market_value,
                    'cash_balance': cash_balance,
                    'total_capital': total_capital,
                    'total_unrealized_pnl': float(portfolio_metrics.total_unrealized_pnl) if portfolio_metrics.total_unrealized_pnl else 0.0,
                    'avg_position_size': float(portfolio_metrics.avg_position_size) if portfolio_metrics.avg_position_size else 0.0,
                    'max_position_size': float(portfolio_metrics.max_position_size) if portfolio_metrics.max_position_size else 0.0,
                    'min_position_size': float(portfolio_metrics.min_position_size) if portfolio_metrics.min_position_size else 0.0,
                    'cash_percentage': (cash_balance / total_capital * 100) if total_capital > 0 else 0.0
                }
                
        except Exception as e:
            logger.error(f"Error calculating portfolio metrics: {e}")
            return {}
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dict containing database statistics
        """
        try:
            async with self.db_manager.get_async_session() as session:
                stats = {}
                
                # Get table counts
                tables = [
                    'users', 'funds', 'portfolios', 'performances',
                    'transactions', 'strategies', 'investments', 'risks'
                ]
                
                for table in tables:
                    result = await session.execute(
                        text(f"SELECT COUNT(*) as count FROM {table}")
                    )
                    count = result.fetchone().count
                    stats[f'{table}_count'] = count
                
                # Get database size
                size_result = await session.execute(
                    text("""
                        SELECT pg_size_pretty(pg_database_size(current_database())) as size
                    """)
                )
                size = size_result.fetchone().size
                stats['database_size'] = size
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
    
    async def cleanup_old_data(self, days_to_keep: int = 365) -> Dict[str, Any]:
        """
        Cleanup old data from database.
        
        Args:
            days_to_keep: Number of days of data to keep
            
        Returns:
            Dict containing cleanup results
        """
        try:
            async with self.db_manager.get_async_session() as session:
                cleanup_date = datetime.now(datetime.UTC).date() - timedelta(days=days_to_keep)
                
                # Cleanup old performance data
                perf_result = await session.execute(
                    text("""
                        DELETE FROM performances
                        WHERE date < :cleanup_date
                    """),
                    {"cleanup_date": cleanup_date}
                )
                perf_deleted = perf_result.rowcount
                
                # Cleanup old risk data
                risk_result = await session.execute(
                    text("""
                        DELETE FROM risks
                        WHERE date < :cleanup_date
                    """),
                    {"cleanup_date": cleanup_date}
                )
                risk_deleted = risk_result.rowcount
                
                # Cleanup old transactions (keep more recent ones)
                trans_result = await session.execute(
                    text("""
                        DELETE FROM transactions
                        WHERE created_at < :cleanup_date
                        AND transaction_type IN ('fee', 'dividend')
                    """),
                    {"cleanup_date": cleanup_date}
                )
                trans_deleted = trans_result.rowcount
                
                await session.commit()
                
                return {
                    'status': 'success',
                    'message': 'Data cleanup completed',
                    'deleted_records': {
                        'performances': perf_deleted,
                        'risks': risk_deleted,
                        'transactions': trans_deleted
                    }
                }
                
        except Exception as e:
            logger.error(f"Error during data cleanup: {e}")
            return {
                'status': 'error',
                'message': f'Data cleanup failed: {str(e)}'
            }
    
    def validate_decimal(self, value: Any, precision: int = 20, scale: int = 2) -> Decimal:
        """
        Validate and convert value to Decimal.
        
        Args:
            value: Value to validate
            precision: Maximum precision
            scale: Maximum scale
            
        Returns:
            Validated Decimal value
        """
        try:
            if value is None:
                return Decimal('0.00')
            
            decimal_value = Decimal(str(value))
            
            # Check precision and scale
            if decimal_value.as_tuple().exponent < -scale:
                raise ValueError(f"Scale exceeds maximum of {scale}")
            
            # Round to specified scale
            return decimal_value.quantize(Decimal('0.' + '0' * scale))
            
        except Exception as e:
            logger.error(f"Error validating decimal: {e}")
            return Decimal('0.00')
    
    def validate_percentage(self, value: Any) -> Decimal:
        """
        Validate percentage value (0-1).
        
        Args:
            value: Value to validate
            
        Returns:
            Validated percentage as Decimal
        """
        try:
            decimal_value = self.validate_decimal(value, 5, 4)
            
            if not (0 <= decimal_value <= 1):
                raise ValueError("Percentage must be between 0 and 1")
            
            return decimal_value
            
        except Exception as e:
            logger.error(f"Error validating percentage: {e}")
            return Decimal('0.0000')
