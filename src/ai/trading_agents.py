#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Trading Agents Module

This module provides AI trading agents for autonomous trading decisions.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import uuid


class AgentType(Enum):
    """Agent type enumeration"""
    MOMENTUM_AGENT = "momentum_agent"
    ML_AGENT = "ml_agent"
    ENSEMBLE_AGENT = "ensemble_agent"
    SENTIMENT_AGENT = "sentiment_agent"
    ARBITRAGE_AGENT = "arbitrage_agent"


class DecisionType(Enum):
    """Trading decision types"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class AgentState(Enum):
    """Agent state enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    LEARNING = "learning"
    ERROR = "error"


@dataclass
class AgentConfig:
    """Configuration for trading agents"""
    agent_type: AgentType
    name: str
    risk_tolerance: float = 0.5
    max_position_size: float = 0.1
    decision_threshold: float = 0.6
    learning_rate: float = 0.01
    lookback_period: int = 20
    update_frequency: int = 1


@dataclass
class MarketObservation:
    """Market data observation"""
    timestamp: datetime
    symbol: str
    price: float
    volume: float
    bid: float
    ask: float
    spread: float
    volatility: float
    trend: str
    sentiment: float
    technical_indicators: Dict[str, float]


@dataclass
class TradingDecision:
    """Trading decision from an agent"""
    agent_id: str
    timestamp: datetime
    decision: DecisionType
    confidence: float
    reasoning: str
    position_size: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


class BaseAgent:
    """Base class for all trading agents"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.agent_id = str(uuid.uuid4())
        self.state = AgentState.ACTIVE
        self.total_trades = 0
        self.successful_trades = 0
        self.total_pnl = 0.0
        self.last_decision = None
        self.performance_history = []
    
    async def process_observation(self, observation: MarketObservation) -> TradingDecision:
        """Process market observation and make decision"""
        raise NotImplementedError("Subclasses must implement process_observation")
    
    def update_performance(self, pnl: float, success: bool):
        """Update agent performance metrics"""
        self.total_trades += 1
        self.total_pnl += pnl
        if success:
            self.successful_trades += 1
        
        self.performance_history.append({
            'timestamp': datetime.now(),
            'pnl': pnl,
            'success': success,
            'total_pnl': self.total_pnl,
            'win_rate': self.successful_trades / self.total_trades if self.total_trades > 0 else 0
        })
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            'agent_id': self.agent_id,
            'name': self.config.name,
            'type': self.config.agent_type.value,
            'state': self.state.value,
            'total_trades': self.total_trades,
            'win_rate': self.successful_trades / self.total_trades if self.total_trades > 0 else 0,
            'total_pnl': self.total_pnl,
            'last_decision': self.last_decision.decision.value if self.last_decision else None
        }


class MomentumAgent(BaseAgent):
    """Momentum-based trading agent"""
    
    async def process_observation(self, observation: MarketObservation) -> TradingDecision:
        """Process observation using momentum strategy"""
        # Simple momentum logic
        rsi = observation.technical_indicators.get('rsi', 50)
        macd = observation.technical_indicators.get('macd', 0)
        
        confidence = 0.5
        decision = DecisionType.HOLD
        reasoning = "Neutral momentum"
        
        if rsi < 30 and macd > 0:
            decision = DecisionType.BUY
            confidence = min(0.9, 0.5 + (30 - rsi) / 30)
            reasoning = "Oversold with positive MACD"
        elif rsi > 70 and macd < 0:
            decision = DecisionType.SELL
            confidence = min(0.9, 0.5 + (rsi - 70) / 30)
            reasoning = "Overbought with negative MACD"
        
        trading_decision = TradingDecision(
            agent_id=self.agent_id,
            timestamp=datetime.now(),
            decision=decision,
            confidence=confidence,
            reasoning=reasoning,
            position_size=min(self.config.max_position_size, confidence * 0.1)
        )
        
        self.last_decision = trading_decision
        return trading_decision


class MLAgent(BaseAgent):
    """Machine learning-based trading agent"""
    
    def __init__(self, config: AgentConfig, model=None):
        super().__init__(config)
        self.model = model
    
    async def process_observation(self, observation: MarketObservation) -> TradingDecision:
        """Process observation using ML model"""
        # Mock ML decision logic
        import random
        
        # Simulate model prediction
        if self.model:
            prediction = random.uniform(-1, 1)  # Mock prediction
        else:
            prediction = random.uniform(-0.5, 0.5)  # Less confident without model
        
        if prediction > self.config.decision_threshold:
            decision = DecisionType.BUY
            confidence = min(0.9, abs(prediction))
            reasoning = f"ML model prediction: {prediction:.3f} (buy signal)"
        elif prediction < -self.config.decision_threshold:
            decision = DecisionType.SELL
            confidence = min(0.9, abs(prediction))
            reasoning = f"ML model prediction: {prediction:.3f} (sell signal)"
        else:
            decision = DecisionType.HOLD
            confidence = 0.5
            reasoning = f"ML model prediction: {prediction:.3f} (neutral)"
        
        trading_decision = TradingDecision(
            agent_id=self.agent_id,
            timestamp=datetime.now(),
            decision=decision,
            confidence=confidence,
            reasoning=reasoning,
            position_size=min(self.config.max_position_size, confidence * 0.1)
        )
        
        self.last_decision = trading_decision
        return trading_decision


class EnsembleAgent(BaseAgent):
    """Ensemble agent that combines multiple agents"""
    
    def __init__(self, config: AgentConfig, sub_agents: List[BaseAgent]):
        super().__init__(config)
        self.sub_agents = sub_agents
    
    async def process_observation(self, observation: MarketObservation) -> TradingDecision:
        """Process observation using ensemble of agents"""
        # Get decisions from all sub-agents
        decisions = []
        for agent in self.sub_agents:
            decision = await agent.process_observation(observation)
            decisions.append(decision)
        
        # Combine decisions (simple voting)
        buy_votes = sum(1 for d in decisions if d.decision == DecisionType.BUY)
        sell_votes = sum(1 for d in decisions if d.decision == DecisionType.SELL)
        hold_votes = sum(1 for d in decisions if d.decision == DecisionType.HOLD)
        
        # Calculate weighted confidence
        total_confidence = sum(d.confidence for d in decisions)
        avg_confidence = total_confidence / len(decisions) if decisions else 0.5
        
        if buy_votes > sell_votes and buy_votes > hold_votes:
            final_decision = DecisionType.BUY
            reasoning = f"Ensemble vote: {buy_votes} buy, {sell_votes} sell, {hold_votes} hold"
        elif sell_votes > buy_votes and sell_votes > hold_votes:
            final_decision = DecisionType.SELL
            reasoning = f"Ensemble vote: {buy_votes} buy, {sell_votes} sell, {hold_votes} hold"
        else:
            final_decision = DecisionType.HOLD
            reasoning = f"Ensemble vote: {buy_votes} buy, {sell_votes} sell, {hold_votes} hold"
        
        trading_decision = TradingDecision(
            agent_id=self.agent_id,
            timestamp=datetime.now(),
            decision=final_decision,
            confidence=avg_confidence,
            reasoning=reasoning,
            position_size=min(self.config.max_position_size, avg_confidence * 0.1)
        )
        
        self.last_decision = trading_decision
        return trading_decision


class AgentManager:
    """Manager for all trading agents"""
    
    def __init__(self):
        self.agents = {}
        self.config = {
            'max_agents': 10,
            'update_frequency': 1,
            'performance_tracking': True
        }
        self.market_data_history = []
    
    def add_agent(self, agent: BaseAgent) -> Dict[str, Any]:
        """Add an agent to the manager"""
        try:
            if len(self.agents) >= self.config['max_agents']:
                return {
                    'status': 'error',
                    'message': f"Maximum number of agents ({self.config['max_agents']}) reached"
                }
            
            self.agents[agent.agent_id] = agent
            return {
                'status': 'success',
                'agent_id': agent.agent_id,
                'message': f"Agent {agent.config.name} added successfully"
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def remove_agent(self, agent_id: str) -> Dict[str, Any]:
        """Remove an agent from the manager"""
        try:
            if agent_id in self.agents:
                agent = self.agents.pop(agent_id)
                return {
                    'status': 'success',
                    'message': f"Agent {agent.config.name} removed successfully"
                }
            else:
                return {
                    'status': 'error',
                    'message': f"Agent {agent_id} not found"
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    async def process_market_data(self, observation: MarketObservation) -> Dict[str, Any]:
        """Process market data with all agents"""
        try:
            self.market_data_history.append(observation)
            
            # Process with all agents concurrently
            tasks = []
            for agent in self.agents.values():
                if agent.state == AgentState.ACTIVE:
                    tasks.append(agent.process_observation(observation))
            
            if not tasks:
                return {
                    'status': 'warning',
                    'message': 'No active agents to process market data',
                    'total_agents': 0,
                    'results': {}
                }
            
            # Wait for all agents to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Organize results
            agent_results = {}
            for i, (agent_id, agent) in enumerate(self.agents.items()):
                if agent.state == AgentState.ACTIVE:
                    if i < len(results) and not isinstance(results[i], Exception):
                        agent_results[agent.config.name] = {
                            'agent_id': agent_id,
                            'decision': results[i],
                            'status': 'success'
                        }
                    else:
                        agent_results[agent.config.name] = {
                            'agent_id': agent_id,
                            'status': 'error',
                            'message': str(results[i]) if i < len(results) else 'Unknown error'
                        }
            
            return {
                'status': 'success',
                'total_agents': len([a for a in self.agents.values() if a.state == AgentState.ACTIVE]),
                'results': agent_results,
                'timestamp': observation.timestamp,
                'symbol': observation.symbol
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_agent_performance(self) -> Dict[str, Any]:
        """Get performance metrics for all agents"""
        try:
            performance = {}
            for agent_id, agent in self.agents.items():
                performance[agent.config.name] = {
                    'agent_id': agent_id,
                    'agent_type': agent.config.agent_type.value,
                    'state': agent.state.value,
                    'total_trades': agent.total_trades,
                    'successful_trades': agent.successful_trades,
                    'win_rate': agent.successful_trades / agent.total_trades if agent.total_trades > 0 else 0,
                    'total_pnl': agent.total_pnl,
                    'performance_history_length': len(agent.performance_history)
                }
            
            return {
                'status': 'success',
                'performance': performance,
                'total_agents': len(self.agents),
                'active_agents': len([a for a in self.agents.values() if a.state == AgentState.ACTIVE])
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_market_data_history(self) -> List[MarketObservation]:
        """Get historical market data"""
        return self.market_data_history
    
    def clear_history(self):
        """Clear market data history"""
        self.market_data_history.clear()