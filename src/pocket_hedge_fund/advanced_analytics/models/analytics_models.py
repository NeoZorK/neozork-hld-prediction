"""
Analytics Data Models

This module defines Pydantic models for analytics data structures.
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal
from enum import Enum
import uuid

from pydantic import BaseModel, Field, validator


class DataFrequency(str, Enum):
    """Data frequency enumeration."""
    TICK = "tick"
    MINUTE = "minute"
    HOUR = "hour"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class MarketRegime(str, Enum):
    """Market regime enumeration."""
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"
    TRENDING = "trending"
    MEAN_REVERTING = "mean_reverting"


class PredictionType(str, Enum):
    """Prediction type enumeration."""
    PRICE = "price"
    VOLATILITY = "volatility"
    DIRECTION = "direction"
    VOLUME = "volume"
    SENTIMENT = "sentiment"
    RISK = "risk"


class ModelType(str, Enum):
    """ML model type enumeration."""
    LINEAR_REGRESSION = "linear_regression"
    RANDOM_FOREST = "random_forest"
    XGBOOST = "xgboost"
    LSTM = "lstm"
    TRANSFORMER = "transformer"
    SVM = "svm"
    NEURAL_NETWORK = "neural_network"


class TimeSeriesData(BaseModel):
    """Time series data model."""
    timestamp: datetime
    value: Decimal
    metadata: Optional[Dict[str, Any]] = None


class MarketData(BaseModel):
    """Market data model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str
    timestamp: datetime
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: Decimal
    adjusted_close: Optional[Decimal] = None
    frequency: DataFrequency = DataFrequency.DAILY
    source: str = "market_data"
    metadata: Optional[Dict[str, Any]] = None

    @validator('high_price')
    def validate_high_price(cls, v, values):
        if 'low_price' in values and v < values['low_price']:
            raise ValueError('High price must be >= low price')
        return v

    @validator('close_price')
    def validate_close_price(cls, v, values):
        if 'low_price' in values and v < values['low_price']:
            raise ValueError('Close price must be >= low price')
        if 'high_price' in values and v > values['high_price']:
            raise ValueError('Close price must be <= high price')
        return v


class PredictionResult(BaseModel):
    """ML model prediction result."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    model_id: str
    symbol: str
    prediction_type: PredictionType
    predicted_value: Decimal
    confidence: Decimal = Field(ge=0, le=1)
    timestamp: datetime
    prediction_horizon: int  # in minutes/hours/days
    features_used: List[str]
    model_version: str
    metadata: Optional[Dict[str, Any]] = None

    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        return v


class AnalyticsInsight(BaseModel):
    """Analytics insight model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    insight_type: str
    title: str
    description: str
    confidence: Decimal = Field(ge=0, le=1)
    impact: str  # high, medium, low
    timeframe: str
    symbols: List[str]
    generated_at: datetime
    expires_at: Optional[datetime] = None
    source_data: List[str]
    recommendations: List[str] = []
    metadata: Optional[Dict[str, Any]] = None


class ModelPerformance(BaseModel):
    """Model performance metrics."""
    model_id: str
    model_type: ModelType
    symbol: str
    training_period: Dict[str, datetime]
    test_period: Dict[str, datetime]
    metrics: Dict[str, float]
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    metadata: Optional[Dict[str, Any]] = None


class FeatureImportance(BaseModel):
    """Feature importance analysis."""
    model_id: str
    feature_name: str
    importance_score: Decimal
    rank: int
    category: str  # technical, fundamental, sentiment, etc.
    description: Optional[str] = None
    created_at: datetime


class CorrelationMatrix(BaseModel):
    """Correlation matrix data."""
    symbols: List[str]
    correlations: Dict[str, Dict[str, float]]
    calculated_at: datetime
    period: str
    frequency: DataFrequency


class VolatilityMetrics(BaseModel):
    """Volatility metrics model."""
    symbol: str
    historical_volatility: Decimal
    implied_volatility: Optional[Decimal] = None
    garch_volatility: Optional[Decimal] = None
    realized_volatility: Decimal
    volatility_percentile: Decimal
    calculated_at: datetime
    period: str


class TrendAnalysis(BaseModel):
    """Trend analysis model."""
    symbol: str
    trend_direction: str  # up, down, sideways
    trend_strength: Decimal = Field(ge=0, le=1)
    trend_duration: int  # in periods
    support_level: Optional[Decimal] = None
    resistance_level: Optional[Decimal] = None
    break_probability: Decimal = Field(ge=0, le=1)
    analyzed_at: datetime
    timeframe: str


class MarketRegimeAnalysis(BaseModel):
    """Market regime analysis model."""
    current_regime: MarketRegime
    regime_probability: Dict[MarketRegime, Decimal]
    regime_duration: int  # in days
    transition_probability: Dict[MarketRegime, Decimal]
    analyzed_at: datetime
    symbols: List[str]
    confidence: Decimal = Field(ge=0, le=1)
