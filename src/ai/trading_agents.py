# -*- coding: utf-8 -*-
"""
AI Trading Agents and Autonomous Systems for NeoZork Interactive ML Trading Strategy Development.

This module provides intelligent trading agents with autonomous decision-making capabilities.
"""

import asyncio
import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Trading agent types."""
    MOMENTUM_AGENT = "momentum_agent"
    MEAN_REVERSION_AGENT = "mean_reversion_agent"
    ARBITRAGE_AGENT = "arbitrage_agent"
    MARKET_MAKING_AGENT = "market_making_agent"
    ML_AGENT = "ml_agent"
    REINFORCEMENT_AGENT = "reinforcement_agent"
    ENSEMBLE_AGENT = "ensemble_agent"
    ADAPTIVE_AGENT = "adaptive_agent"

class AgentState(Enum):
    """Agent states."""
    IDLE = "idle"
    ANALYZING = "analyzing"
    TRADING = "trading"
    LEARNING = "learning"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class DecisionType(Enum):
    """Decision types."""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    WAIT = "wait"
    EMERGENCY_EXIT = "emergency_exit"

@dataclass
class AgentConfig:
    """Agent configuration."""
    agent_type: AgentType
    name: str
    risk_tolerance: float = 0.5
    max_position_size: float = 0.1
    learning_rate: float = 0.01
    memory_size: int = 1000
    decision_threshold: float = 0.6
    confidence_threshold: float = 0.7
    max_trades_per_day: int = 100
    cooldown_period: int = 60  # seconds

@dataclass
class MarketObservation:
    """Market observation data."""
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
    technical_indicators: Dict[str, float] = field(default_factory=dict)

@dataclass
class TradingDecision:
    """Trading decision."""
    agent_id: str
    timestamp: datetime
    symbol: str
    decision: DecisionType
    confidence: float
    reasoning: str
    expected_return: float
    risk_score: float
    position_size: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

@dataclass
class AgentMemory:
    """Agent memory for learning."""
    observations: List[MarketObservation] = field(default_factory=list)
    decisions: List[TradingDecision] = field(default_factory=list)
    outcomes: List[Dict[str, Any]] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)

class TradingAgent:
    """Base trading agent class."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.state = AgentState.IDLE
        self.memory = AgentMemory()
        self.performance_history = []
        self.current_positions = {}
        self.last_decision_time = None
        self.total_trades = 0
        self.successful_trades = 0
        self.total_pnl = 0.0
        
    async def analyze_market(self, observation: MarketObservation) -> Dict[str, Any]:
        """Analyze market conditions."""
        try:
            self.state = AgentState.ANALYZING
            
            # Store observation in memory
            self.memory.observations.append(observation)
            if len(self.memory.observations) > self.config.memory_size:
                self.memory.observations.pop(0)
            
            # Perform analysis based on agent type
            analysis = await self._perform_analysis(observation)
            
            self.state = AgentState.IDLE
            return analysis
            
        except Exception as e:
            logger.error(f"Agent {self.config.name} failed to analyze market: {e}")
            self.state = AgentState.ERROR
            return {
                'status': 'error',
                'message': f'Analysis failed: {str(e)}'
            }
    
    async def make_decision(self, observation: MarketObservation) -> TradingDecision:
        """Make trading decision."""
        try:
            # Check cooldown period
            if (self.last_decision_time and 
                (datetime.now() - self.last_decision_time).seconds < self.config.cooldown_period):
                return TradingDecision(
                    agent_id=self.config.name,
                    timestamp=datetime.now(),
                    symbol=observation.symbol,
                    decision=DecisionType.WAIT,
                    confidence=0.0,
                    reasoning="Cooldown period active",
                    expected_return=0.0,
                    risk_score=0.0,
                    position_size=0.0
                )
            
            # Check daily trade limit
            if self.total_trades >= self.config.max_trades_per_day:
                return TradingDecision(
                    agent_id=self.config.name,
                    timestamp=datetime.now(),
                    symbol=observation.symbol,
                    decision=DecisionType.WAIT,
                    confidence=0.0,
                    reasoning="Daily trade limit reached",
                    expected_return=0.0,
                    risk_score=0.0,
                    position_size=0.0
                )
            
            self.state = AgentState.TRADING
            
            # Make decision based on agent type
            decision = await self._make_decision_logic(observation)
            
            # Store decision in memory
            self.memory.decisions.append(decision)
            if len(self.memory.decisions) > self.config.memory_size:
                self.memory.decisions.pop(0)
            
            self.last_decision_time = datetime.now()
            self.state = AgentState.IDLE
            
            return decision
            
        except Exception as e:
            logger.error(f"Agent {self.config.name} failed to make decision: {e}")
            self.state = AgentState.ERROR
            return TradingDecision(
                agent_id=self.config.name,
                timestamp=datetime.now(),
                symbol=observation.symbol,
                decision=DecisionType.HOLD,
                confidence=0.0,
                reasoning=f"Decision failed: {str(e)}",
                expected_return=0.0,
                risk_score=1.0,
                position_size=0.0
            )
    
    async def learn_from_outcome(self, decision: TradingDecision, outcome: Dict[str, Any]):
        """Learn from trading outcome."""
        try:
            self.state = AgentState.LEARNING
            
            # Store outcome
            self.memory.outcomes.append({
                'decision': decision,
                'outcome': outcome,
                'timestamp': datetime.now()
            })
            
            # Update performance metrics
            self._update_performance_metrics(decision, outcome)
            
            # Perform learning based on agent type
            await self._learn_from_outcome_logic(decision, outcome)
            
            self.state = AgentState.IDLE
            
        except Exception as e:
            logger.error(f"Agent {self.config.name} failed to learn: {e}")
            self.state = AgentState.ERROR
    
    async def _perform_analysis(self, observation: MarketObservation) -> Dict[str, Any]:
        """Perform market analysis (to be implemented by subclasses)."""
        return {
            'status': 'success',
            'analysis': 'Base analysis',
            'confidence': 0.5
        }
    
    async def _make_decision_logic(self, observation: MarketObservation) -> TradingDecision:
        """Make trading decision logic (to be implemented by subclasses)."""
        return TradingDecision(
            agent_id=self.config.name,
            timestamp=datetime.now(),
            symbol=observation.symbol,
            decision=DecisionType.HOLD,
            confidence=0.5,
            reasoning="Base decision logic",
            expected_return=0.0,
            risk_score=0.5,
            position_size=0.0
        )
    
    async def _learn_from_outcome_logic(self, decision: TradingDecision, outcome: Dict[str, Any]):
        """Learn from outcome logic (to be implemented by subclasses)."""
        pass
    
    def _update_performance_metrics(self, decision: TradingDecision, outcome: Dict[str, Any]):
        """Update performance metrics."""
        self.total_trades += 1
        
        if outcome.get('success', False):
            self.successful_trades += 1
        
        pnl = outcome.get('pnl', 0.0)
        self.total_pnl += pnl
        
        # Calculate win rate
        win_rate = self.successful_trades / self.total_trades if self.total_trades > 0 else 0.0
        
        self.memory.performance_metrics = {
            'total_trades': self.total_trades,
            'successful_trades': self.successful_trades,
            'win_rate': win_rate,
            'total_pnl': self.total_pnl,
            'avg_pnl_per_trade': self.total_pnl / self.total_trades if self.total_trades > 0 else 0.0
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            'agent_id': self.config.name,
            'agent_type': self.config.agent_type.value,
            'state': self.state.value,
            'total_trades': self.total_trades,
            'successful_trades': self.successful_trades,
            'win_rate': self.memory.performance_metrics.get('win_rate', 0.0),
            'total_pnl': self.total_pnl,
            'current_positions': len(self.current_positions),
            'memory_size': len(self.memory.observations),
            'last_decision_time': self.last_decision_time.isoformat() if self.last_decision_time else None
        }

class MomentumAgent(TradingAgent):
    """Momentum-based trading agent."""
    
    async def _perform_analysis(self, observation: MarketObservation) -> Dict[str, Any]:
        """Analyze momentum indicators."""
        try:
            # Calculate momentum indicators
            rsi = observation.technical_indicators.get('rsi', 50)
            macd = observation.technical_indicators.get('macd', 0)
            bollinger_position = observation.technical_indicators.get('bollinger_position', 0.5)
            
            # Determine momentum strength
            momentum_score = 0.0
            if rsi > 70:
                momentum_score += 0.3  # Strong upward momentum
            elif rsi < 30:
                momentum_score -= 0.3  # Strong downward momentum
            
            if macd > 0:
                momentum_score += 0.2
            else:
                momentum_score -= 0.2
            
            if bollinger_position > 0.8:
                momentum_score += 0.2  # Near upper band
            elif bollinger_position < 0.2:
                momentum_score -= 0.2  # Near lower band
            
            return {
                'status': 'success',
                'momentum_score': momentum_score,
                'rsi': rsi,
                'macd': macd,
                'bollinger_position': bollinger_position,
                'confidence': min(1.0, abs(momentum_score))
            }
            
        except Exception as e:
            logger.error(f"Momentum analysis failed: {e}")
            return {
                'status': 'error',
                'message': f'Momentum analysis failed: {str(e)}'
            }
    
    async def _make_decision_logic(self, observation: MarketObservation) -> TradingDecision:
        """Make momentum-based decision."""
        try:
            analysis = await self._perform_analysis(observation)
            momentum_score = analysis.get('momentum_score', 0.0)
            confidence = analysis.get('confidence', 0.0)
            
            # Make decision based on momentum
            if momentum_score > self.config.decision_threshold:
                decision = DecisionType.BUY
                reasoning = f"Strong upward momentum (score: {momentum_score:.2f})"
                expected_return = momentum_score * 0.02  # 2% max expected return
            elif momentum_score < -self.config.decision_threshold:
                decision = DecisionType.SELL
                reasoning = f"Strong downward momentum (score: {momentum_score:.2f})"
                expected_return = abs(momentum_score) * 0.02
            else:
                decision = DecisionType.HOLD
                reasoning = f"Weak momentum (score: {momentum_score:.2f})"
                expected_return = 0.0
            
            # Calculate position size based on confidence and risk tolerance
            position_size = min(
                self.config.max_position_size,
                confidence * self.config.risk_tolerance * 0.1
            )
            
            # Calculate risk score
            risk_score = 1.0 - confidence
            
            return TradingDecision(
                agent_id=self.config.name,
                timestamp=datetime.now(),
                symbol=observation.symbol,
                decision=decision,
                confidence=confidence,
                reasoning=reasoning,
                expected_return=expected_return,
                risk_score=risk_score,
                position_size=position_size,
                stop_loss=observation.price * (0.98 if decision == DecisionType.BUY else 1.02),
                take_profit=observation.price * (1.05 if decision == DecisionType.BUY else 0.95)
            )
            
        except Exception as e:
            logger.error(f"Momentum decision failed: {e}")
            return TradingDecision(
                agent_id=self.config.name,
                timestamp=datetime.now(),
                symbol=observation.symbol,
                decision=DecisionType.HOLD,
                confidence=0.0,
                reasoning=f"Decision failed: {str(e)}",
                expected_return=0.0,
                risk_score=1.0,
                position_size=0.0
            )

class MLAgent(TradingAgent):
    """ML-based trading agent."""
    
    def __init__(self, config: AgentConfig, ml_model=None):
        super().__init__(config)
        self.ml_model = ml_model
        self.feature_history = []
        
    async def _perform_analysis(self, observation: MarketObservation) -> Dict[str, Any]:
        """Perform ML-based analysis."""
        try:
            # Extract features for ML model
            features = self._extract_features(observation)
            self.feature_history.append(features)
            
            if len(self.feature_history) > 100:
                self.feature_history.pop(0)
            
            # Make prediction if model is available
            if self.ml_model and len(self.feature_history) >= 10:
                # Use recent features for prediction
                recent_features = np.array(self.feature_history[-10:])
                prediction = self.ml_model.predict(recent_features.reshape(1, -1))[0]
                
                return {
                    'status': 'success',
                    'ml_prediction': prediction,
                    'features': features,
                    'confidence': min(1.0, abs(prediction))
                }
            else:
                # Fallback to simple analysis
                return {
                    'status': 'success',
                    'ml_prediction': 0.0,
                    'features': features,
                    'confidence': 0.3
                }
            
        except Exception as e:
            logger.error(f"ML analysis failed: {e}")
            return {
                'status': 'error',
                'message': f'ML analysis failed: {str(e)}'
            }
    
    def _extract_features(self, observation: MarketObservation) -> List[float]:
        """Extract features from observation."""
        features = [
            observation.price,
            observation.volume,
            observation.spread,
            observation.volatility,
            observation.sentiment,
            observation.technical_indicators.get('rsi', 50),
            observation.technical_indicators.get('macd', 0),
            observation.technical_indicators.get('bollinger_position', 0.5),
            observation.technical_indicators.get('sma_20', observation.price),
            observation.technical_indicators.get('ema_12', observation.price)
        ]
        return features
    
    async def _make_decision_logic(self, observation: MarketObservation) -> TradingDecision:
        """Make ML-based decision."""
        try:
            analysis = await self._perform_analysis(observation)
            prediction = analysis.get('ml_prediction', 0.0)
            confidence = analysis.get('confidence', 0.0)
            
            # Make decision based on ML prediction
            if prediction > self.config.decision_threshold:
                decision = DecisionType.BUY
                reasoning = f"ML model predicts upward movement (prediction: {prediction:.3f})"
                expected_return = prediction * 0.03
            elif prediction < -self.config.decision_threshold:
                decision = DecisionType.SELL
                reasoning = f"ML model predicts downward movement (prediction: {prediction:.3f})"
                expected_return = abs(prediction) * 0.03
            else:
                decision = DecisionType.HOLD
                reasoning = f"ML model predicts neutral movement (prediction: {prediction:.3f})"
                expected_return = 0.0
            
            # Calculate position size
            position_size = min(
                self.config.max_position_size,
                confidence * self.config.risk_tolerance * 0.15
            )
            
            risk_score = 1.0 - confidence
            
            return TradingDecision(
                agent_id=self.config.name,
                timestamp=datetime.now(),
                symbol=observation.symbol,
                decision=decision,
                confidence=confidence,
                reasoning=reasoning,
                expected_return=expected_return,
                risk_score=risk_score,
                position_size=position_size,
                stop_loss=observation.price * (0.97 if decision == DecisionType.BUY else 1.03),
                take_profit=observation.price * (1.08 if decision == DecisionType.BUY else 0.92)
            )
            
        except Exception as e:
            logger.error(f"ML decision failed: {e}")
            return TradingDecision(
                agent_id=self.config.name,
                timestamp=datetime.now(),
                symbol=observation.symbol,
                decision=DecisionType.HOLD,
                confidence=0.0,
                reasoning=f"ML decision failed: {str(e)}",
                expected_return=0.0,
                risk_score=1.0,
                position_size=0.0
            )

class EnsembleAgent(TradingAgent):
    """Ensemble trading agent that combines multiple strategies."""
    
    def __init__(self, config: AgentConfig, sub_agents: List[TradingAgent]):
        super().__init__(config)
        self.sub_agents = sub_agents
        self.agent_weights = {agent.config.name: 1.0 / len(sub_agents) for agent in sub_agents}
        
    async def _make_decision_logic(self, observation: MarketObservation) -> TradingDecision:
        """Make ensemble decision."""
        try:
            decisions = []
            confidences = []
            
            # Get decisions from all sub-agents
            for agent in self.sub_agents:
                try:
                    decision = await agent.make_decision(observation)
                    decisions.append(decision)
                    confidences.append(decision.confidence)
                except Exception as e:
                    logger.warning(f"Sub-agent {agent.config.name} failed: {e}")
                    continue
            
            if not decisions:
                return TradingDecision(
                    agent_id=self.config.name,
                    timestamp=datetime.now(),
                    symbol=observation.symbol,
                    decision=DecisionType.HOLD,
                    confidence=0.0,
                    reasoning="No sub-agents available",
                    expected_return=0.0,
                    risk_score=1.0,
                    position_size=0.0
                )
            
            # Weight decisions by agent performance
            weighted_decisions = {}
            total_weight = 0.0
            
            for i, decision in enumerate(decisions):
                agent_name = decision.agent_id
                weight = self.agent_weights.get(agent_name, 0.1) * decision.confidence
                
                decision_type = decision.decision.value
                if decision_type not in weighted_decisions:
                    weighted_decisions[decision_type] = 0.0
                
                weighted_decisions[decision_type] += weight
                total_weight += weight
            
            # Normalize weights
            if total_weight > 0:
                for decision_type in weighted_decisions:
                    weighted_decisions[decision_type] /= total_weight
            
            # Find the decision with highest weight
            best_decision_type = max(weighted_decisions.keys(), key=lambda x: weighted_decisions[x])
            ensemble_confidence = weighted_decisions[best_decision_type]
            
            # Calculate ensemble metrics
            avg_expected_return = np.mean([d.expected_return for d in decisions])
            avg_risk_score = np.mean([d.risk_score for d in decisions])
            avg_position_size = np.mean([d.position_size for d in decisions])
            
            # Create ensemble decision
            ensemble_decision = DecisionType(best_decision_type)
            reasoning = f"Ensemble decision: {best_decision_type} (confidence: {ensemble_confidence:.3f})"
            
            return TradingDecision(
                agent_id=self.config.name,
                timestamp=datetime.now(),
                symbol=observation.symbol,
                decision=ensemble_decision,
                confidence=ensemble_confidence,
                reasoning=reasoning,
                expected_return=avg_expected_return,
                risk_score=avg_risk_score,
                position_size=avg_position_size
            )
            
        except Exception as e:
            logger.error(f"Ensemble decision failed: {e}")
            return TradingDecision(
                agent_id=self.config.name,
                timestamp=datetime.now(),
                symbol=observation.symbol,
                decision=DecisionType.HOLD,
                confidence=0.0,
                reasoning=f"Ensemble decision failed: {str(e)}",
                expected_return=0.0,
                risk_score=1.0,
                position_size=0.0
            )

class AgentManager:
    """Manager for multiple trading agents."""
    
    def __init__(self):
        self.agents = {}
        self.agent_performance = {}
        self.market_data = {}
        
    def add_agent(self, agent: TradingAgent) -> Dict[str, Any]:
        """Add an agent to the manager."""
        try:
            self.agents[agent.config.name] = agent
            self.agent_performance[agent.config.name] = {
                'total_trades': 0,
                'successful_trades': 0,
                'total_pnl': 0.0,
                'win_rate': 0.0
            }
            
            logger.info(f"Agent {agent.config.name} added to manager")
            
            return {
                'status': 'success',
                'agent_name': agent.config.name,
                'agent_type': agent.config.agent_type.value,
                'message': f'Agent {agent.config.name} added successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to add agent: {e}")
            return {
                'status': 'error',
                'message': f'Failed to add agent: {str(e)}'
            }
    
    async def process_market_data(self, observation: MarketObservation) -> Dict[str, Any]:
        """Process market data with all agents."""
        try:
            results = {}
            
            # Process with each agent
            for agent_name, agent in self.agents.items():
                try:
                    # Analyze market
                    analysis = await agent.analyze_market(observation)
                    
                    # Make decision
                    decision = await agent.make_decision(observation)
                    
                    results[agent_name] = {
                        'analysis': analysis,
                        'decision': decision,
                        'agent_status': agent.get_agent_status()
                    }
                    
                except Exception as e:
                    logger.error(f"Agent {agent_name} failed to process market data: {e}")
                    results[agent_name] = {
                        'error': str(e),
                        'agent_status': agent.get_agent_status()
                    }
            
            return {
                'status': 'success',
                'timestamp': observation.timestamp.isoformat(),
                'symbol': observation.symbol,
                'results': results,
                'total_agents': len(self.agents),
                'message': f'Processed market data with {len(self.agents)} agents'
            }
            
        except Exception as e:
            logger.error(f"Failed to process market data: {e}")
            return {
                'status': 'error',
                'message': f'Failed to process market data: {str(e)}'
            }
    
    def get_agent_performance(self) -> Dict[str, Any]:
        """Get performance of all agents."""
        try:
            performance = {}
            
            for agent_name, agent in self.agents.items():
                status = agent.get_agent_status()
                performance[agent_name] = {
                    'agent_type': status['agent_type'],
                    'state': status['state'],
                    'total_trades': status['total_trades'],
                    'successful_trades': status['successful_trades'],
                    'win_rate': status['win_rate'],
                    'total_pnl': status['total_pnl'],
                    'current_positions': status['current_positions']
                }
            
            return {
                'status': 'success',
                'performance': performance,
                'total_agents': len(self.agents),
                'message': f'Retrieved performance for {len(self.agents)} agents'
            }
            
        except Exception as e:
            logger.error(f"Failed to get agent performance: {e}")
            return {
                'status': 'error',
                'message': f'Failed to get agent performance: {str(e)}'
            }

# Example usage and testing
async def test_trading_agents():
    """Test trading agents system."""
    print("🧪 Testing AI Trading Agents System...")
    
    # Create agent manager
    agent_manager = AgentManager()
    
    # Create different types of agents
    momentum_config = AgentConfig(
        agent_type=AgentType.MOMENTUM_AGENT,
        name="MomentumAgent_1",
        risk_tolerance=0.6,
        max_position_size=0.15,
        decision_threshold=0.5
    )
    momentum_agent = MomentumAgent(momentum_config)
    
    ml_config = AgentConfig(
        agent_type=AgentType.ML_AGENT,
        name="MLAgent_1",
        risk_tolerance=0.4,
        max_position_size=0.1,
        decision_threshold=0.6
    )
    ml_agent = MLAgent(ml_config)
    
    ensemble_config = AgentConfig(
        agent_type=AgentType.ENSEMBLE_AGENT,
        name="EnsembleAgent_1",
        risk_tolerance=0.5,
        max_position_size=0.12,
        decision_threshold=0.55
    )
    ensemble_agent = EnsembleAgent(ensemble_config, [momentum_agent, ml_agent])
    
    # Add agents to manager
    agents = [momentum_agent, ml_agent, ensemble_agent]
    for agent in agents:
        result = agent_manager.add_agent(agent)
        print(f"  • Added {agent.config.name}: {'✅' if result['status'] == 'success' else '❌'}")
    
    print(f"  • Total agents: {len(agent_manager.agents)}")
    
    # Test market data processing
    print("  • Testing market data processing...")
    
    # Create sample market observations
    observations = []
    for i in range(5):
        observation = MarketObservation(
            timestamp=datetime.now(),
            symbol="BTCUSDT",
            price=50000 + random.uniform(-1000, 1000),
            volume=random.uniform(1000, 10000),
            bid=50000 + random.uniform(-1000, 1000),
            ask=50000 + random.uniform(-1000, 1000),
            spread=random.uniform(10, 50),
            volatility=random.uniform(0.01, 0.05),
            trend=random.choice(["up", "down", "sideways"]),
            sentiment=random.uniform(-1, 1),
            technical_indicators={
                'rsi': random.uniform(20, 80),
                'macd': random.uniform(-100, 100),
                'bollinger_position': random.uniform(0, 1),
                'sma_20': 50000 + random.uniform(-500, 500),
                'ema_12': 50000 + random.uniform(-500, 500)
            }
        )
        observations.append(observation)
    
    # Process market data with agents
    for i, observation in enumerate(observations):
        result = await agent_manager.process_market_data(observation)
        
        if result['status'] == 'success':
            print(f"    ✅ Observation {i+1}: Processed with {result['total_agents']} agents")
            
            # Show decisions
            for agent_name, agent_result in result['results'].items():
                if 'decision' in agent_result:
                    decision = agent_result['decision']
                    print(f"      {agent_name}: {decision.decision.value} (confidence: {decision.confidence:.3f})")
        else:
            print(f"    ❌ Observation {i+1}: {result['message']}")
    
    # Test agent performance
    performance = agent_manager.get_agent_performance()
    if performance['status'] == 'success':
        print(f"  • Agent performance: ✅")
        for agent_name, perf in performance['performance'].items():
            print(f"    {agent_name}:")
            print(f"      - Type: {perf['agent_type']}")
            print(f"      - State: {perf['state']}")
            print(f"      - Trades: {perf['total_trades']}")
            print(f"      - Win Rate: {perf['win_rate']:.1%}")
            print(f"      - PnL: ${perf['total_pnl']:.2f}")
    
    # Test individual agent status
    print("  • Testing individual agent status...")
    for agent in agents:
        status = agent.get_agent_status()
        print(f"    ✅ {status['agent_id']}: {status['state']}, {status['total_trades']} trades")
    
    print("✅ AI Trading Agents System test completed!")
    
    return agent_manager

if __name__ == "__main__":
    asyncio.run(test_trading_agents())
