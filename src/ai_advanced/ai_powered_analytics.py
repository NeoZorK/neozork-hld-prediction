"""
AI-Powered Analytics System
Intelligent insights, pattern recognition, predictive modeling
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid
import json
from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsightType(Enum):
    """Insight type enumeration"""
    PATTERN_RECOGNITION = "pattern_recognition"
    ANOMALY_DETECTION = "anomaly_detection"
    PREDICTIVE_ANALYSIS = "predictive_analysis"
    CORRELATION_ANALYSIS = "correlation_analysis"
    TREND_ANALYSIS = "trend_analysis"
    MARKET_REGIME = "market_regime"
    RISK_ASSESSMENT = "risk_assessment"
    OPPORTUNITY_IDENTIFICATION = "opportunity_identification"

class PatternType(Enum):
    """Pattern type enumeration"""
    TECHNICAL_PATTERN = "technical_pattern"
    PRICE_PATTERN = "price_pattern"
    VOLUME_PATTERN = "volume_pattern"
    VOLATILITY_PATTERN = "volatility_pattern"
    SEASONAL_PATTERN = "seasonal_pattern"
    CYCLICAL_PATTERN = "cyclical_pattern"
    CORRELATION_PATTERN = "correlation_pattern"
    ANOMALY_PATTERN = "anomaly_pattern"

class ConfidenceLevel(Enum):
    """Confidence level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class Insight:
    """AI-generated insight"""
    insight_id: str
    insight_type: InsightType
    pattern_type: Optional[PatternType]
    title: str
    description: str
    confidence: ConfidenceLevel
    confidence_score: float
    data_points: List[Dict[str, Any]]
    indicators: List[str]
    recommendations: List[str]
    risk_level: str
    impact_score: float
    timeframe: str
    created_at: datetime
    expires_at: Optional[datetime]

@dataclass
class Pattern:
    """Detected pattern"""
    pattern_id: str
    pattern_type: PatternType
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    strength: float
    confidence: float
    data_points: List[Dict[str, Any]]
    indicators: List[str]
    metadata: Dict[str, Any]

@dataclass
class PredictiveModel:
    """Predictive model"""
    model_id: str
    model_type: str
    target_variable: str
    features: List[str]
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    created_at: datetime
    last_updated: datetime
    predictions: List[Dict[str, Any]]

class PatternRecognitionEngine:
    """Pattern recognition engine"""
    
    def __init__(self):
        self.patterns = {}
        self.pattern_templates = {}
        self.recognition_algorithms = {}
        
    async def detect_technical_patterns(self, data: pd.DataFrame) -> List[Pattern]:
        """Detect technical patterns in price data"""
        patterns = []
        
        # Simulate technical pattern detection
        if len(data) > 20:
            # Head and Shoulders pattern
            if self._detect_head_shoulders(data):
                pattern = Pattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.TECHNICAL_PATTERN,
                    name="Head and Shoulders",
                    description="Reversal pattern indicating potential trend change",
                    start_time=data.index[-20],
                    end_time=data.index[-1],
                    strength=0.75,
                    confidence=0.8,
                    data_points=[{"timestamp": data.index[-1], "price": data['close'].iloc[-1]}],
                    indicators=["RSI", "MACD", "Volume"],
                    metadata={"pattern_type": "reversal", "direction": "bearish"}
                )
                patterns.append(pattern)
            
            # Double Top pattern
            if self._detect_double_top(data):
                pattern = Pattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.TECHNICAL_PATTERN,
                    name="Double Top",
                    description="Bearish reversal pattern",
                    start_time=data.index[-15],
                    end_time=data.index[-1],
                    strength=0.7,
                    confidence=0.75,
                    data_points=[{"timestamp": data.index[-1], "price": data['close'].iloc[-1]}],
                    indicators=["RSI", "Volume"],
                    metadata={"pattern_type": "reversal", "direction": "bearish"}
                )
                patterns.append(pattern)
            
            # Ascending Triangle pattern
            if self._detect_ascending_triangle(data):
                pattern = Pattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.TECHNICAL_PATTERN,
                    name="Ascending Triangle",
                    description="Bullish continuation pattern",
                    start_time=data.index[-12],
                    end_time=data.index[-1],
                    strength=0.65,
                    confidence=0.7,
                    data_points=[{"timestamp": data.index[-1], "price": data['close'].iloc[-1]}],
                    indicators=["Volume", "Support/Resistance"],
                    metadata={"pattern_type": "continuation", "direction": "bullish"}
                )
                patterns.append(pattern)
        
        return patterns
    
    def _detect_head_shoulders(self, data: pd.DataFrame) -> bool:
        """Detect head and shoulders pattern"""
        if len(data) < 20:
            return False
        
        # Simplified detection logic
        prices = data['close'].values
        recent_prices = prices[-20:]
        
        # Look for three peaks with middle peak higher
        peaks = []
        for i in range(1, len(recent_prices) - 1):
            if recent_prices[i] > recent_prices[i-1] and recent_prices[i] > recent_prices[i+1]:
                peaks.append((i, recent_prices[i]))
        
        if len(peaks) >= 3:
            # Check if middle peak is highest
            middle_peak = peaks[len(peaks)//2]
            return middle_peak[1] > peaks[0][1] and middle_peak[1] > peaks[-1][1]
        
        return False
    
    def _detect_double_top(self, data: pd.DataFrame) -> bool:
        """Detect double top pattern"""
        if len(data) < 15:
            return False
        
        prices = data['close'].values
        recent_prices = prices[-15:]
        
        # Find two similar peaks
        max_price = np.max(recent_prices)
        peaks = []
        for i, price in enumerate(recent_prices):
            if price > max_price * 0.95:
                peaks.append(i)
        
        return len(peaks) >= 2
    
    def _detect_ascending_triangle(self, data: pd.DataFrame) -> bool:
        """Detect ascending triangle pattern"""
        if len(data) < 12:
            return False
        
        prices = data['close'].values
        recent_prices = prices[-12:]
        
        # Check for ascending support line
        support_line = np.polyfit(range(len(recent_prices)), recent_prices, 1)[0]
        return support_line > 0
    
    async def detect_volume_patterns(self, data: pd.DataFrame) -> List[Pattern]:
        """Detect volume patterns"""
        patterns = []
        
        if 'volume' in data.columns and len(data) > 10:
            volume_data = data['volume']
            
            # Volume spike pattern
            if self._detect_volume_spike(volume_data):
                pattern = Pattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.VOLUME_PATTERN,
                    name="Volume Spike",
                    description="Unusual volume increase indicating potential price movement",
                    start_time=data.index[-5],
                    end_time=data.index[-1],
                    strength=0.8,
                    confidence=0.85,
                    data_points=[{"timestamp": data.index[-1], "volume": volume_data.iloc[-1]}],
                    indicators=["Volume", "Price"],
                    metadata={"pattern_type": "volume_spike", "magnitude": "high"}
                )
                patterns.append(pattern)
            
            # Volume divergence pattern
            if self._detect_volume_divergence(data):
                pattern = Pattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.VOLUME_PATTERN,
                    name="Volume Divergence",
                    description="Volume and price moving in opposite directions",
                    start_time=data.index[-10],
                    end_time=data.index[-1],
                    strength=0.7,
                    confidence=0.75,
                    data_points=[{"timestamp": data.index[-1], "volume": volume_data.iloc[-1], "price": data['close'].iloc[-1]}],
                    indicators=["Volume", "Price", "RSI"],
                    metadata={"pattern_type": "divergence", "direction": "bearish"}
                )
                patterns.append(pattern)
        
        return patterns
    
    def _detect_volume_spike(self, volume_data: pd.Series) -> bool:
        """Detect volume spike"""
        if len(volume_data) < 5:
            return False
        
        recent_volume = volume_data.iloc[-1]
        avg_volume = volume_data.iloc[-10:-1].mean()
        
        return recent_volume > avg_volume * 2.0
    
    def _detect_volume_divergence(self, data: pd.DataFrame) -> bool:
        """Detect volume divergence"""
        if len(data) < 10:
            return False
        
        price_trend = np.polyfit(range(len(data)), data['close'], 1)[0]
        volume_trend = np.polyfit(range(len(data)), data['volume'], 1)[0]
        
        # Price going up, volume going down (bearish divergence)
        return price_trend > 0 and volume_trend < 0
    
    async def detect_volatility_patterns(self, data: pd.DataFrame) -> List[Pattern]:
        """Detect volatility patterns"""
        patterns = []
        
        if len(data) > 20:
            # Calculate rolling volatility
            returns = data['close'].pct_change().dropna()
            volatility = returns.rolling(window=20).std()
            
            # Volatility expansion pattern
            if self._detect_volatility_expansion(volatility):
                pattern = Pattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.VOLATILITY_PATTERN,
                    name="Volatility Expansion",
                    description="Increasing volatility indicating potential breakout",
                    start_time=data.index[-15],
                    end_time=data.index[-1],
                    strength=0.75,
                    confidence=0.8,
                    data_points=[{"timestamp": data.index[-1], "volatility": volatility.iloc[-1]}],
                    indicators=["ATR", "Bollinger Bands", "VIX"],
                    metadata={"pattern_type": "expansion", "direction": "breakout"}
                )
                patterns.append(pattern)
            
            # Volatility contraction pattern
            if self._detect_volatility_contraction(volatility):
                pattern = Pattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.VOLATILITY_PATTERN,
                    name="Volatility Contraction",
                    description="Decreasing volatility indicating potential consolidation",
                    start_time=data.index[-15],
                    end_time=data.index[-1],
                    strength=0.7,
                    confidence=0.75,
                    data_points=[{"timestamp": data.index[-1], "volatility": volatility.iloc[-1]}],
                    indicators=["ATR", "Bollinger Bands"],
                    metadata={"pattern_type": "contraction", "direction": "consolidation"}
                )
                patterns.append(pattern)
        
        return patterns
    
    def _detect_volatility_expansion(self, volatility: pd.Series) -> bool:
        """Detect volatility expansion"""
        if len(volatility) < 10:
            return False
        
        recent_vol = volatility.iloc[-1]
        avg_vol = volatility.iloc[-10:-1].mean()
        
        return recent_vol > avg_vol * 1.5
    
    def _detect_volatility_contraction(self, volatility: pd.Series) -> bool:
        """Detect volatility contraction"""
        if len(volatility) < 10:
            return False
        
        recent_vol = volatility.iloc[-1]
        avg_vol = volatility.iloc[-10:-1].mean()
        
        return recent_vol < avg_vol * 0.7

class AnomalyDetectionEngine:
    """Anomaly detection engine"""
    
    def __init__(self):
        self.anomaly_models = {}
        self.thresholds = {}
        
    async def detect_price_anomalies(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect price anomalies"""
        anomalies = []
        
        if len(data) > 20:
            prices = data['close'].values
            
            # Statistical anomaly detection
            mean_price = np.mean(prices)
            std_price = np.std(prices)
            
            for i, price in enumerate(prices):
                z_score = abs(price - mean_price) / std_price
                
                if z_score > 2.5:  # 2.5 standard deviations
                    anomaly = {
                        "anomaly_id": str(uuid.uuid4()),
                        "type": "price_anomaly",
                        "timestamp": data.index[i],
                        "value": price,
                        "z_score": z_score,
                        "severity": "high" if z_score > 3.0 else "medium",
                        "description": f"Price anomaly detected: {price:.2f} (Z-score: {z_score:.2f})"
                    }
                    anomalies.append(anomaly)
            
            # Volume anomaly detection
            if 'volume' in data.columns:
                volume_anomalies = await self._detect_volume_anomalies(data)
                anomalies.extend(volume_anomalies)
        
        return anomalies
    
    async def _detect_volume_anomalies(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect volume anomalies"""
        anomalies = []
        
        volumes = data['volume'].values
        mean_volume = np.mean(volumes)
        std_volume = np.std(volumes)
        
        for i, volume in enumerate(volumes):
            z_score = abs(volume - mean_volume) / std_volume
            
            if z_score > 2.0:
                anomaly = {
                    "anomaly_id": str(uuid.uuid4()),
                    "type": "volume_anomaly",
                    "timestamp": data.index[i],
                    "value": volume,
                    "z_score": z_score,
                    "severity": "high" if z_score > 3.0 else "medium",
                    "description": f"Volume anomaly detected: {volume:.0f} (Z-score: {z_score:.2f})"
                }
                anomalies.append(anomaly)
        
        return anomalies
    
    async def detect_temporal_anomalies(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect temporal anomalies"""
        anomalies = []
        
        if len(data) > 24:  # Need at least 24 hours of data
            # Detect unusual trading hours activity
            data['hour'] = data.index.hour
            hourly_volumes = data.groupby('hour')['volume'].mean()
            
            for hour, avg_volume in hourly_volumes.items():
                if hour < 6 or hour > 22:  # Unusual hours
                    current_volume = data[data['hour'] == hour]['volume'].iloc[-1] if len(data[data['hour'] == hour]) > 0 else 0
                    
                    if current_volume > avg_volume * 3:
                        anomaly = {
                            "anomaly_id": str(uuid.uuid4()),
                            "type": "temporal_anomaly",
                            "timestamp": data.index[-1],
                            "value": current_volume,
                            "hour": hour,
                            "severity": "medium",
                            "description": f"Unusual volume at hour {hour}: {current_volume:.0f}"
                        }
                        anomalies.append(anomaly)
        
        return anomalies

class PredictiveAnalyticsEngine:
    """Predictive analytics engine"""
    
    def __init__(self):
        self.models = {}
        self.predictions = {}
        
    async def create_predictive_model(self, data: pd.DataFrame, target_column: str, 
                                    features: List[str], model_type: str = "regression") -> str:
        """Create a predictive model"""
        model_id = str(uuid.uuid4())
        
        # Simulate model creation and training
        model = PredictiveModel(
            model_id=model_id,
            model_type=model_type,
            target_variable=target_column,
            features=features,
            accuracy=np.random.uniform(0.75, 0.95),
            precision=np.random.uniform(0.70, 0.90),
            recall=np.random.uniform(0.65, 0.85),
            f1_score=np.random.uniform(0.70, 0.88),
            created_at=datetime.now(),
            last_updated=datetime.now(),
            predictions=[]
        )
        
        self.models[model_id] = model
        
        logger.info(f"Created predictive model {model_id} for {target_column}")
        return model_id
    
    async def make_predictions(self, model_id: str, data: pd.DataFrame, 
                             horizon: int = 1) -> List[Dict[str, Any]]:
        """Make predictions using a model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        predictions = []
        
        # Simulate predictions
        for i in range(horizon):
            prediction = {
                "prediction_id": str(uuid.uuid4()),
                "model_id": model_id,
                "timestamp": datetime.now() + timedelta(hours=i),
                "predicted_value": np.random.normal(0.5, 0.1),
                "confidence_interval": {
                    "lower": np.random.normal(0.4, 0.05),
                    "upper": np.random.normal(0.6, 0.05)
                },
                "features_used": model.features,
                "model_accuracy": model.accuracy
            }
            predictions.append(prediction)
        
        model.predictions.extend(predictions)
        
        return predictions
    
    async def evaluate_model_performance(self, model_id: str, test_data: pd.DataFrame) -> Dict[str, float]:
        """Evaluate model performance"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        
        # Simulate performance evaluation
        performance = {
            "accuracy": model.accuracy + np.random.normal(0, 0.02),
            "precision": model.precision + np.random.normal(0, 0.02),
            "recall": model.recall + np.random.normal(0, 0.02),
            "f1_score": model.f1_score + np.random.normal(0, 0.02),
            "mae": np.random.uniform(0.01, 0.05),
            "rmse": np.random.uniform(0.02, 0.08),
            "r2_score": np.random.uniform(0.70, 0.90)
        }
        
        return performance

class AIPoweredAnalyticsManager:
    """AI-powered analytics manager"""
    
    def __init__(self):
        self.pattern_engine = PatternRecognitionEngine()
        self.anomaly_engine = AnomalyDetectionEngine()
        self.predictive_engine = PredictiveAnalyticsEngine()
        self.insights = {}
        self.analytics_history = []
        
    async def analyze_market_data(self, data: pd.DataFrame, symbol: str) -> List[Insight]:
        """Comprehensive market data analysis"""
        insights = []
        
        # Pattern recognition
        technical_patterns = await self.pattern_engine.detect_technical_patterns(data)
        volume_patterns = await self.pattern_engine.detect_volume_patterns(data)
        volatility_patterns = await self.pattern_engine.detect_volatility_patterns(data)
        
        # Anomaly detection
        price_anomalies = await self.anomaly_engine.detect_price_anomalies(data)
        temporal_anomalies = await self.anomaly_engine.detect_temporal_anomalies(data)
        
        # Generate insights from patterns
        for pattern in technical_patterns + volume_patterns + volatility_patterns:
            insight = await self._generate_insight_from_pattern(pattern, data, symbol)
            insights.append(insight)
        
        # Generate insights from anomalies
        for anomaly in price_anomalies + temporal_anomalies:
            insight = await self._generate_insight_from_anomaly(anomaly, data, symbol)
            insights.append(insight)
        
        # Store insights
        for insight in insights:
            self.insights[insight.insight_id] = insight
        
        logger.info(f"Generated {len(insights)} insights for {symbol}")
        return insights
    
    async def _generate_insight_from_pattern(self, pattern: Pattern, data: pd.DataFrame, symbol: str) -> Insight:
        """Generate insight from detected pattern"""
        confidence_score = pattern.confidence
        confidence_level = self._get_confidence_level(confidence_score)
        
        # Generate recommendations based on pattern
        recommendations = []
        if pattern.pattern_type == PatternType.TECHNICAL_PATTERN:
            if "bearish" in pattern.metadata.get("direction", ""):
                recommendations.append("Consider reducing position size")
                recommendations.append("Monitor for trend reversal confirmation")
            elif "bullish" in pattern.metadata.get("direction", ""):
                recommendations.append("Consider increasing position size")
                recommendations.append("Look for entry opportunities")
        
        insight = Insight(
            insight_id=str(uuid.uuid4()),
            insight_type=InsightType.PATTERN_RECOGNITION,
            pattern_type=pattern.pattern_type,
            title=f"{pattern.name} Detected in {symbol}",
            description=f"{pattern.description}. Pattern strength: {pattern.strength:.2f}",
            confidence=confidence_level,
            confidence_score=confidence_score,
            data_points=pattern.data_points,
            indicators=pattern.indicators,
            recommendations=recommendations,
            risk_level="medium" if confidence_score < 0.8 else "low",
            impact_score=pattern.strength,
            timeframe="short-term",
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=24)
        )
        
        return insight
    
    async def _generate_insight_from_anomaly(self, anomaly: Dict[str, Any], data: pd.DataFrame, symbol: str) -> Insight:
        """Generate insight from detected anomaly"""
        confidence_score = 0.8 if anomaly["severity"] == "high" else 0.6
        confidence_level = self._get_confidence_level(confidence_score)
        
        recommendations = []
        if anomaly["type"] == "price_anomaly":
            recommendations.append("Investigate potential market manipulation")
            recommendations.append("Monitor for follow-up price movements")
        elif anomaly["type"] == "volume_anomaly":
            recommendations.append("Check for news or events affecting the asset")
            recommendations.append("Monitor for potential breakout or breakdown")
        
        insight = Insight(
            insight_id=str(uuid.uuid4()),
            insight_type=InsightType.ANOMALY_DETECTION,
            pattern_type=PatternType.ANOMALY_PATTERN,
            title=f"{anomaly['type'].title()} Detected in {symbol}",
            description=anomaly["description"],
            confidence=confidence_level,
            confidence_score=confidence_score,
            data_points=[{"timestamp": anomaly["timestamp"], "value": anomaly["value"]}],
            indicators=["Statistical Analysis", "Z-Score"],
            recommendations=recommendations,
            risk_level=anomaly["severity"],
            impact_score=confidence_score,
            timeframe="immediate",
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=12)
        )
        
        return insight
    
    def _get_confidence_level(self, score: float) -> ConfidenceLevel:
        """Convert confidence score to confidence level"""
        if score >= 0.9:
            return ConfidenceLevel.VERY_HIGH
        elif score >= 0.8:
            return ConfidenceLevel.HIGH
        elif score >= 0.6:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    async def create_predictive_model(self, data: pd.DataFrame, target_column: str, 
                                    features: List[str], model_type: str = "regression") -> str:
        """Create a predictive model"""
        return await self.predictive_engine.create_predictive_model(data, target_column, features, model_type)
    
    async def make_predictions(self, model_id: str, data: pd.DataFrame, horizon: int = 1) -> List[Dict[str, Any]]:
        """Make predictions using a model"""
        return await self.predictive_engine.make_predictions(model_id, data, horizon)
    
    async def get_insights_summary(self) -> Dict[str, Any]:
        """Get insights summary"""
        insight_types = {}
        confidence_levels = {}
        risk_levels = {}
        
        for insight in self.insights.values():
            # Count by type
            insight_type = insight.insight_type.value
            insight_types[insight_type] = insight_types.get(insight_type, 0) + 1
            
            # Count by confidence level
            confidence = insight.confidence.value
            confidence_levels[confidence] = confidence_levels.get(confidence, 0) + 1
            
            # Count by risk level
            risk = insight.risk_level
            risk_levels[risk] = risk_levels.get(risk, 0) + 1
        
        return {
            "total_insights": len(self.insights),
            "insight_types": insight_types,
            "confidence_distribution": confidence_levels,
            "risk_distribution": risk_levels,
            "active_insights": len([i for i in self.insights.values() if i.expires_at is None or i.expires_at > datetime.now()]),
            "expired_insights": len([i for i in self.insights.values() if i.expires_at is not None and i.expires_at <= datetime.now()])
        }
    
    async def get_high_confidence_insights(self, min_confidence: float = 0.8) -> List[Insight]:
        """Get high confidence insights"""
        high_confidence_insights = []
        
        for insight in self.insights.values():
            if insight.confidence_score >= min_confidence:
                high_confidence_insights.append(insight)
        
        # Sort by confidence score descending
        high_confidence_insights.sort(key=lambda x: x.confidence_score, reverse=True)
        
        return high_confidence_insights
    
    async def get_insights_by_type(self, insight_type: InsightType) -> List[Insight]:
        """Get insights by type"""
        filtered_insights = []
        
        for insight in self.insights.values():
            if insight.insight_type == insight_type:
                filtered_insights.append(insight)
        
        return filtered_insights
    
    def get_summary(self) -> Dict[str, Any]:
        """Get system summary"""
        return {
            "total_insights": len(self.insights),
            "predictive_models": len(self.predictive_engine.models),
            "analytics_history_entries": len(self.analytics_history),
            "pattern_recognition_engine": "active",
            "anomaly_detection_engine": "active",
            "predictive_analytics_engine": "active",
            "last_update": datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of AIPoweredAnalyticsManager"""
    manager = AIPoweredAnalyticsManager()
    
    # Generate sample market data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='H')
    np.random.seed(42)
    
    data = pd.DataFrame({
        'open': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1),
        'high': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1) + np.random.uniform(0, 2, len(dates)),
        'low': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1) - np.random.uniform(0, 2, len(dates)),
        'close': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1),
        'volume': np.random.uniform(1000, 10000, len(dates))
    }, index=dates)
    
    # Analyze market data
    insights = await manager.analyze_market_data(data, "BTCUSDT")
    print(f"Generated {len(insights)} insights")
    
    # Create predictive model
    model_id = await manager.create_predictive_model(
        data, 
        target_column='close', 
        features=['open', 'high', 'low', 'volume'],
        model_type='regression'
    )
    print(f"Created predictive model: {model_id}")
    
    # Make predictions
    predictions = await manager.make_predictions(model_id, data, horizon=5)
    print(f"Generated {len(predictions)} predictions")
    
    # Get insights summary
    summary = await manager.get_insights_summary()
    print(f"Insights summary: {summary}")
    
    # Get high confidence insights
    high_conf_insights = await manager.get_high_confidence_insights(0.7)
    print(f"High confidence insights: {len(high_conf_insights)}")
    
    # System summary
    system_summary = manager.get_summary()
    print(f"System summary: {system_summary}")

if __name__ == "__main__":
    asyncio.run(main())
