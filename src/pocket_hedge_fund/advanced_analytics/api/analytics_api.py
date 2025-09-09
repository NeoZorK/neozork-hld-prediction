"""
Advanced Analytics API

REST API endpoints for advanced analytics functionality.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Depends, Query, Path, BackgroundTasks
from fastapi import status
from pydantic import BaseModel, Field, validator

from ..core.analytics_engine import AnalyticsEngine
from ..models.analytics_models import (
    MarketData, PredictionResult, AnalyticsInsight, 
    ModelPerformance, DataFrequency, PredictionType, ModelType
)
from ...auth.auth_manager import get_current_user
from ...database.connection import get_db_manager

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/analytics", tags=["advanced-analytics"])

# Global analytics engine instance
analytics_engine = None


async def get_analytics_engine() -> AnalyticsEngine:
    """Get analytics engine instance."""
    global analytics_engine
    if analytics_engine is None:
        db_manager = await get_db_manager()
        analytics_engine = AnalyticsEngine(db_manager)
        await analytics_engine.initialize()
    return analytics_engine


# Request/Response Models

class MarketDataRequest(BaseModel):
    """Request model for market data analysis."""
    symbol: str = Field(..., description="Asset symbol")
    start_date: datetime = Field(..., description="Start date for analysis")
    end_date: datetime = Field(..., description="End date for analysis")
    frequency: DataFrequency = Field(DataFrequency.DAILY, description="Data frequency")
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v


class PredictionRequest(BaseModel):
    """Request model for predictions."""
    symbol: str = Field(..., description="Asset symbol")
    prediction_type: PredictionType = Field(..., description="Type of prediction")
    horizon: int = Field(1, ge=1, le=30, description="Prediction horizon in periods")
    features: Optional[Dict[str, Any]] = Field(None, description="Custom features")


class InsightRequest(BaseModel):
    """Request model for insight generation."""
    symbol: str = Field(..., description="Asset symbol")
    analysis_period: int = Field(30, ge=1, le=365, description="Analysis period in days")
    include_predictions: bool = Field(True, description="Include model predictions")


class ModelTrainingRequest(BaseModel):
    """Request model for model training."""
    model_name: str = Field(..., description="Name of the model to train")
    symbol: str = Field(..., description="Asset symbol")
    training_period: int = Field(365, ge=30, le=1095, description="Training period in days")
    test_period: int = Field(30, ge=7, le=90, description="Test period in days")


class AnalyticsResponse(BaseModel):
    """Base response model for analytics."""
    success: bool = Field(True, description="Success status")
    message: str = Field("", description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    symbol: str
    prediction_type: str
    predicted_value: Decimal
    confidence: Decimal
    prediction_horizon: int
    features_used: List[str]
    timestamp: datetime


class InsightResponse(BaseModel):
    """Response model for insights."""
    symbol: str
    insights: List[Dict[str, Any]]
    total_insights: int
    generated_at: datetime


class ModelPerformanceResponse(BaseModel):
    """Response model for model performance."""
    model_id: str
    model_type: str
    symbol: str
    metrics: Dict[str, float]
    performance_grade: str
    recommendations: List[str]
    created_at: datetime


# API Endpoints

@router.get("/health", response_model=AnalyticsResponse)
async def health_check():
    """Health check endpoint for analytics service."""
    try:
        engine = await get_analytics_engine()
        return AnalyticsResponse(
            success=True,
            message="Analytics service is healthy",
            data={"status": "operational", "engine_initialized": True}
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analytics service health check failed: {str(e)}"
        )


@router.post("/market-data/process", response_model=AnalyticsResponse)
async def process_market_data(
    request: MarketDataRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Process and clean market data for analysis."""
    try:
        engine = await get_analytics_engine()
        
        # Process market data
        market_data = await engine.process_market_data(
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            frequency=request.frequency
        )
        
        return AnalyticsResponse(
            success=True,
            message=f"Processed {len(market_data)} market data records",
            data={
                "symbol": request.symbol,
                "records_count": len(market_data),
                "date_range": {
                    "start": request.start_date.isoformat(),
                    "end": request.end_date.isoformat()
                },
                "frequency": request.frequency.value
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to process market data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process market data: {str(e)}"
        )


@router.post("/predictions/generate", response_model=PredictionResponse)
async def generate_prediction(
    request: PredictionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Generate prediction using ML models."""
    try:
        engine = await get_analytics_engine()
        
        # Make prediction
        prediction = await engine.make_prediction(
            symbol=request.symbol,
            prediction_type=request.prediction_type,
            horizon=request.horizon,
            features=request.features
        )
        
        return PredictionResponse(
            symbol=prediction.symbol,
            prediction_type=prediction.prediction_type.value,
            predicted_value=prediction.predicted_value,
            confidence=prediction.confidence,
            prediction_horizon=prediction.prediction_horizon,
            features_used=prediction.features_used,
            timestamp=prediction.timestamp
        )
        
    except Exception as e:
        logger.error(f"Failed to generate prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate prediction: {str(e)}"
        )


@router.post("/insights/generate", response_model=InsightResponse)
async def generate_insights(
    request: InsightRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Generate actionable insights for a symbol."""
    try:
        engine = await get_analytics_engine()
        
        # Generate insights
        insights = await engine.generate_insights(
            symbol=request.symbol,
            market_data=None,  # Will be fetched internally
            predictions=None if not request.include_predictions else []
        )
        
        # Convert insights to dict format
        insights_data = []
        for insight in insights:
            insights_data.append({
                "id": insight.id,
                "type": insight.insight_type,
                "title": insight.title,
                "description": insight.description,
                "confidence": float(insight.confidence),
                "impact": insight.impact,
                "timeframe": insight.timeframe,
                "recommendations": insight.recommendations,
                "generated_at": insight.generated_at.isoformat()
            })
        
        return InsightResponse(
            symbol=request.symbol,
            insights=insights_data,
            total_insights=len(insights_data),
            generated_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Failed to generate insights: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate insights: {str(e)}"
        )


@router.post("/models/train", response_model=ModelPerformanceResponse)
async def train_model(
    request: ModelTrainingRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Train a new ML model."""
    try:
        engine = await get_analytics_engine()
        
        # Check if user has permission to train models
        if current_user.get('role') not in ['admin', 'data_scientist']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to train models"
            )
        
        # Add training task to background
        background_tasks.add_task(
            _train_model_background,
            request.model_name,
            request.symbol,
            request.training_period,
            request.test_period
        )
        
        return ModelPerformanceResponse(
            model_id=f"{request.model_name}_{request.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            model_type=request.model_name,
            symbol=request.symbol,
            metrics={"status": "training_started"},
            performance_grade="N/A",
            recommendations=["Model training has been started in background"],
            created_at=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start model training: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start model training: {str(e)}"
        )


@router.get("/models/{model_id}/performance", response_model=ModelPerformanceResponse)
async def get_model_performance(
    model_id: str = Path(..., description="Model ID"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get model performance metrics."""
    try:
        engine = await get_analytics_engine()
        
        # Get model performance
        performance = await engine.evaluate_model_performance(model_id, [])
        
        return ModelPerformanceResponse(
            model_id=performance.model_id,
            model_type=performance.model_type.value,
            symbol=performance.symbol,
            metrics=performance.metrics,
            performance_grade="B",  # Would be calculated based on metrics
            recommendations=["Monitor model performance regularly"],
            created_at=performance.created_at
        )
        
    except Exception as e:
        logger.error(f"Failed to get model performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model performance: {str(e)}"
        )


@router.get("/analysis/{symbol}/comprehensive", response_model=AnalyticsResponse)
async def get_comprehensive_analysis(
    symbol: str = Path(..., description="Asset symbol"),
    period: int = Query(30, ge=1, le=365, description="Analysis period in days"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get comprehensive analysis for a symbol."""
    try:
        engine = await get_analytics_engine()
        
        # Run comprehensive analysis
        analysis = await engine.run_comprehensive_analysis(symbol, period)
        
        return AnalyticsResponse(
            success=True,
            message=f"Comprehensive analysis completed for {symbol}",
            data={
                "symbol": analysis['symbol'],
                "analysis_period": period,
                "market_data_points": len(analysis['market_data']),
                "features_generated": len(analysis['features']),
                "predictions_count": len(analysis['predictions']),
                "insights_count": len(analysis['insights']),
                "analysis_timestamp": analysis['analysis_timestamp'].isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get comprehensive analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get comprehensive analysis: {str(e)}"
        )


@router.get("/features/{symbol}/generate", response_model=AnalyticsResponse)
async def generate_features(
    symbol: str = Path(..., description="Asset symbol"),
    period: int = Query(30, ge=1, le=365, description="Data period in days"),
    feature_types: str = Query("technical,statistical,momentum", description="Comma-separated feature types"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Generate features for a symbol."""
    try:
        engine = await get_analytics_engine()
        
        # Get market data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period)
        market_data = await engine.process_market_data(symbol, start_date, end_date)
        
        # Generate features
        feature_types_list = [ft.strip() for ft in feature_types.split(',')]
        features = await engine.generate_features(market_data, feature_types_list)
        
        return AnalyticsResponse(
            success=True,
            message=f"Generated {len(features)} feature groups for {symbol}",
            data={
                "symbol": symbol,
                "feature_groups": list(features.keys()),
                "feature_count": len(features),
                "feature_types": feature_types_list,
                "generated_at": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to generate features: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate features: {str(e)}"
        )


@router.get("/models/list", response_model=AnalyticsResponse)
async def list_models(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List all available models."""
    try:
        # This would typically query a database
        models = [
            {
                "model_id": "price_predictor_lstm",
                "model_type": "LSTM",
                "description": "Price prediction using LSTM",
                "status": "active",
                "accuracy": 0.75
            },
            {
                "model_id": "volatility_predictor_nn",
                "model_type": "Neural Network",
                "description": "Volatility prediction using neural networks",
                "status": "active",
                "accuracy": 0.82
            },
            {
                "model_id": "sentiment_analyzer_transformer",
                "model_type": "Transformer",
                "description": "Sentiment analysis using transformers",
                "status": "active",
                "accuracy": 0.78
            }
        ]
        
        return AnalyticsResponse(
            success=True,
            message=f"Retrieved {len(models)} models",
            data={
                "models": models,
                "total_count": len(models)
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list models: {str(e)}"
        )


# Background Tasks

async def _train_model_background(
    model_name: str,
    symbol: str,
    training_period: int,
    test_period: int
):
    """Background task for model training."""
    try:
        logger.info(f"Starting background training for {model_name} on {symbol}")
        
        # This would contain the actual training logic
        # For now, just simulate training
        await asyncio.sleep(10)  # Simulate training time
        
        logger.info(f"Background training completed for {model_name} on {symbol}")
        
    except Exception as e:
        logger.error(f"Background training failed for {model_name} on {symbol}: {e}")


# Error Handlers

@router.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )


@router.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception in analytics API: {exc}")
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error in analytics service"
    )
