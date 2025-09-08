"""Fund Manager - Core fund management functionality"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class FundType(Enum):
    """Fund type enumeration."""
    MINI = "mini"  # $1,000 - $10,000
    STANDARD = "standard"  # $10,000 - $100,000
    PREMIUM = "premium"  # $100,000 - $1,000,000
    INSTITUTIONAL = "institutional"  # $1,000,000+


@dataclass
class FundConfig:
    """Fund configuration data class."""
    fund_id: str
    name: str
    fund_type: FundType
    initial_capital: float
    management_fee: float
    performance_fee: float
    risk_level: float
    max_drawdown: float
    target_return: float
    strategies: List[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class FundMetrics:
    """Fund metrics data class."""
    total_value: float
    total_invested: float
    total_pnl: float
    total_return: float
    daily_return: float
    sharpe_ratio: float
    max_drawdown: float
    volatility: float
    win_rate: float
    profit_factor: float
    investor_count: int
    aum: float


class FundManager:
    """Core fund management functionality."""
    
    def __init__(self):
        self.funds: Dict[str, FundConfig] = {}
        self.fund_metrics: Dict[str, FundMetrics] = {}
        self.fund_history: Dict[str, List[Dict[str, Any]]] = {}
        self.investors: Dict[str, List[str]] = {}  # fund_id -> investor_ids
        self.fee_schedule = {
            FundType.MINI: {'management': 0.02, 'performance': 0.20},
            FundType.STANDARD: {'management': 0.015, 'performance': 0.15},
            FundType.PREMIUM: {'management': 0.01, 'performance': 0.10},
            FundType.INSTITUTIONAL: {'management': 0.005, 'performance': 0.05}
        }
        
    async def create_fund(self, name: str, fund_type: FundType, 
                         initial_capital: float, risk_level: float = 0.02,
                         target_return: float = 0.15) -> Dict[str, Any]:
        """Create a new fund."""
        try:
            fund_id = str(uuid.uuid4())
            
            # Get fee schedule for fund type
            fees = self.fee_schedule[fund_type]
            
            # Create fund configuration
            fund_config = FundConfig(
                fund_id=fund_id,
                name=name,
                fund_type=fund_type,
                initial_capital=initial_capital,
                management_fee=fees['management'],
                performance_fee=fees['performance'],
                risk_level=risk_level,
                max_drawdown=0.15,  # Default 15% max drawdown
                target_return=target_return,
                strategies=[],  # Will be populated later
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Initialize fund metrics
            fund_metrics = FundMetrics(
                total_value=initial_capital,
                total_invested=initial_capital,
                total_pnl=0.0,
                total_return=0.0,
                daily_return=0.0,
                sharpe_ratio=0.0,
                max_drawdown=0.0,
                volatility=0.0,
                win_rate=0.0,
                profit_factor=0.0,
                investor_count=0,
                aum=initial_capital
            )
            
            # Store fund data
            self.funds[fund_id] = fund_config
            self.fund_metrics[fund_id] = fund_metrics
            self.fund_history[fund_id] = []
            self.investors[fund_id] = []
            
            logger.info(f"Created fund: {name} ({fund_id}) with {initial_capital} capital")
            return {
                'status': 'success',
                'fund_id': fund_id,
                'fund_config': fund_config.__dict__,
                'fund_metrics': fund_metrics.__dict__
            }
            
        except Exception as e:
            logger.error(f"Failed to create fund: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def get_fund_info(self, fund_id: str) -> Dict[str, Any]:
        """Get comprehensive fund information."""
        try:
            if fund_id not in self.funds:
                return {'error': 'Fund not found'}
            
            fund_config = self.funds[fund_id]
            fund_metrics = self.fund_metrics.get(fund_id)
            fund_history = self.fund_history.get(fund_id, [])
            investor_count = len(self.investors.get(fund_id, []))
            
            fund_info = {
                'fund_config': fund_config.__dict__,
                'fund_metrics': fund_metrics.__dict__ if fund_metrics else {},
                'investor_count': investor_count,
                'recent_history': fund_history[-10:] if fund_history else [],  # Last 10 records
                'timestamp': datetime.now()
            }
            
            return fund_info
            
        except Exception as e:
            logger.error(f"Failed to get fund info: {e}")
            return {'error': str(e)}
    
    async def add_investor(self, fund_id: str, investor_id: str, 
                          investment_amount: float) -> Dict[str, Any]:
        """Add an investor to the fund."""
        try:
            if fund_id not in self.funds:
                return {'error': 'Fund not found'}
            
            if fund_id not in self.investors:
                self.investors[fund_id] = []
            
            # Add investor
            if investor_id not in self.investors[fund_id]:
                self.investors[fund_id].append(investor_id)
            
            # Update fund metrics
            if fund_id in self.fund_metrics:
                self.fund_metrics[fund_id].investor_count = len(self.investors[fund_id])
                self.fund_metrics[fund_id].aum += investment_amount
                self.fund_metrics[fund_id].total_invested += investment_amount
            
            logger.info(f"Added investor {investor_id} to fund {fund_id} with {investment_amount}")
            return {
                'status': 'success',
                'investor_id': investor_id,
                'investment_amount': investment_amount,
                'new_investor_count': len(self.investors[fund_id])
            }
            
        except Exception as e:
            logger.error(f"Failed to add investor: {e}")
            return {'error': str(e)}
    
    async def calculate_fees(self, fund_id: str, period_days: int = 30) -> Dict[str, Any]:
        """Calculate management and performance fees."""
        try:
            if fund_id not in self.funds:
                return {'error': 'Fund not found'}
            
            fund_config = self.funds[fund_id]
            fund_metrics = self.fund_metrics.get(fund_id)
            
            if not fund_metrics:
                return {'error': 'Fund metrics not available'}
            
            # Calculate management fee (annual, prorated)
            management_fee_rate = fund_config.management_fee
            management_fee = fund_metrics.aum * management_fee_rate * (period_days / 365)
            
            # Calculate performance fee (only if positive returns)
            performance_fee = 0.0
            if fund_metrics.total_return > 0:
                performance_fee_rate = fund_config.performance_fee
                performance_fee = fund_metrics.total_pnl * performance_fee_rate
            
            total_fees = management_fee + performance_fee
            
            fee_calculation = {
                'fund_id': fund_id,
                'period_days': period_days,
                'aum': fund_metrics.aum,
                'total_return': fund_metrics.total_return,
                'management_fee_rate': management_fee_rate,
                'management_fee': management_fee,
                'performance_fee_rate': fund_config.performance_fee,
                'performance_fee': performance_fee,
                'total_fees': total_fees,
                'timestamp': datetime.now()
            }
            
            return fee_calculation
            
        except Exception as e:
            logger.error(f"Failed to calculate fees: {e}")
            return {'error': str(e)}
    
    async def get_fund_list(self, fund_type: Optional[FundType] = None) -> Dict[str, Any]:
        """Get list of all funds, optionally filtered by type."""
        try:
            funds_list = []
            
            for fund_id, fund_config in self.funds.items():
                if fund_type is None or fund_config.fund_type == fund_type:
                    fund_metrics = self.fund_metrics.get(fund_id)
                    investor_count = len(self.investors.get(fund_id, []))
                    
                    fund_summary = {
                        'fund_id': fund_id,
                        'name': fund_config.name,
                        'fund_type': fund_config.fund_type.value,
                        'status': 'active',  # TODO: Implement status tracking
                        'aum': fund_metrics.aum if fund_metrics else 0,
                        'total_return': fund_metrics.total_return if fund_metrics else 0,
                        'investor_count': investor_count,
                        'created_at': fund_config.created_at,
                        'updated_at': fund_config.updated_at
                    }
                    funds_list.append(fund_summary)
            
            return {
                'funds': funds_list,
                'total_count': len(funds_list),
                'filter_type': fund_type.value if fund_type else None,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Failed to get fund list: {e}")
            return {'error': str(e)}
    
    def get_fund_summary(self) -> Dict[str, Any]:
        """Get summary of all funds."""
        summary = {
            'total_funds': len(self.funds),
            'funds_by_type': {},
            'total_aum': 0,
            'total_investors': 0,
            'funds': []
        }
        
        # Group by fund type
        for fund_config in self.funds.values():
            fund_type = fund_config.fund_type.value
            if fund_type not in summary['funds_by_type']:
                summary['funds_by_type'][fund_type] = 0
            summary['funds_by_type'][fund_type] += 1
        
        # Calculate totals
        for fund_id, fund_metrics in self.fund_metrics.items():
            summary['total_aum'] += fund_metrics.aum
            summary['total_investors'] += fund_metrics.investor_count
        
        return summary