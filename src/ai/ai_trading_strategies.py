#!/usr/bin/env python3
"""
AI Trading Strategies Module
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
import uuid


class StrategyType(Enum):
    """Strategy type enumeration"""
    DEEP_Q_NETWORK = "deep_q_network"
    POLICY_GRADIENT = "policy_gradient"
    ACTOR_CRITIC = "actor_critic"
    MULTI_AGENT = "multi_agent"


class TradingState(Enum):
    """Trading state enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    LEARNING = "learning"


class MarketRegime(Enum):
    """Market regime enumeration"""
    HIGH_VOLATILITY = "high_volatility"
    LOW_VOLATILITY = "low_volatility"
    TRENDING = "trending"
    SIDEWAYS = "sideways"


class ActionType(Enum):
    """Action type enumeration"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class AITradingStrategyManager:
    """AI trading strategy manager"""
    
    def __init__(self):
        self.strategies = {}
        self.agents = {}
        self.performance_records = {}
        self.config = {
            'max_strategies': 50,
            'learning_rate': 0.001,
            'exploration_rate': 0.1
        }
    
    def create_strategy(self, strategy_type: StrategyType, name: str, description: str = "", parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new AI trading strategy"""
        try:
            strategy_id = str(uuid.uuid4())[:22]  # Shorter ID for display
            
            strategy_info = {
                'strategy_id': strategy_id,
                'type': strategy_type.value,
                'name': name,
                'description': description,
                    'parameters': parameters or {},
                'status': 'created'
                }
            
            self.strategies[strategy_id] = strategy_info
            
            return {
                'status': 'success',
                'strategy_id': strategy_id,
                'strategy_info': strategy_info
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def add_agent_to_system(self, agent_id: str, strategy_type: StrategyType, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Add an agent to the multi-agent system"""
        try:
            agent_info = {
                'agent_id': agent_id,
                'strategy_type': strategy_type.value,
                'parameters': parameters or {},
                'status': 'active',
                'performance': {'trades': 0, 'wins': 0, 'losses': 0}
            }
            
            self.agents[agent_id] = agent_info
            
            return {
                'status': 'success',
                'agent_id': agent_id,
                'agent_info': agent_info
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def detect_market_regime(self, market_data: pd.DataFrame) -> Dict[str, Any]:
        """Detect current market regime"""
        try:
            # Simple regime detection based on volatility
            if 'price' in market_data.columns:
                returns = market_data['price'].pct_change().dropna()
                volatility = returns.std()
                
                if volatility > 0.03:
                    regime = MarketRegime.HIGH_VOLATILITY
                    confidence = 0.8
                else:
                    regime = MarketRegime.LOW_VOLATILITY
                    confidence = 0.6
                
                return {
                    'status': 'success',
                    'regime': regime.value,
                    'confidence': confidence,
                    'volatility': volatility
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Price column not found in market data'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_strategy_summary(self) -> Dict[str, Any]:
        """Get summary of all strategies"""
        return {
            'total_strategies': len(self.strategies),
            'multi_agent_agents': len(self.agents),
            'performance_records': len(self.performance_records),
            'strategy_types': list(set([s['type'] for s in self.strategies.values()]))
        }