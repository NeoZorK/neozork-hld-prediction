"""
ML API for Pocket Hedge Fund.

This module provides REST API endpoints for machine learning
and automated trading functionality.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, validator

from ..database import DatabaseManager, DatabaseUtils
from ..auth.middleware import get_current_user, require_fund_manager
from ..ml.price_predictor import PricePredictor
from ..trading.automated_trader import AutomatedTrader, TradingStrategy

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Create router
router = APIRouter(prefix="/ml", tags=["Machine Learning & Automated Trading"])

class MLAPI:
    """ML API class for dependency injection."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.router = router
        self.price_predictors = {}  # Cache predictors by symbol
        self.automated_traders = {}  # Cache traders by fund_id

# Pydantic models

class TrainModelRequest(BaseModel):
    symbols: List[str]
    model_type: str = "ensemble"  # ensemble, tree_based, linear
    lookback_days: int = 365
    target_column: str = "future_return_1"

class PredictRequest(BaseModel):
    symbol: str
    model_name: Optional[str] = None  # If None, use ensemble

class AutomatedTraderRequest(BaseModel):
    fund_id: str
    strategy: str = "combined"  # ml_only, technical_only, combined, conservative, aggressive
    symbols: List[str]

class TradingParamsRequest(BaseModel):
    fund_id: str
    min_confidence: Optional[float] = None
    min_signal_strength: Optional[float] = None
    max_position_size: Optional[float] = None
    stop_loss_pct: Optional[float] = None
    take_profit_pct: Optional[float] = None
    max_daily_trades: Optional[int] = None
    cooldown_minutes: Optional[int] = None

# API Endpoints

@router.post("/train-models", response_model=Dict[str, Any])
async def train_ml_models(
    train_request: TrainModelRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Train machine learning models for price prediction."""
    try:
        logger.info(f"Training ML models for symbols: {train_request.symbols}")
        
        training_results = {}
        
        for symbol in train_request.symbols:
            try:
                # Create or get predictor
                if symbol not in MLAPI(None).price_predictors:
                    predictor = PricePredictor(model_type=train_request.model_type)
                    MLAPI(None).price_predictors[symbol] = predictor
                else:
                    predictor = MLAPI(None).price_predictors[symbol]
                
                # Get data for training
                from ..data.data_manager import DataManager
                data_manager = DataManager()
                
                if symbol.startswith('data/'):
                    data = await data_manager.get_local_data(symbol)
                else:
                    data = await data_manager.get_yahoo_data(symbol, period=f"{train_request.lookback_days}d")
                
                if data.empty:
                    training_results[symbol] = {
                        'status': 'error',
                        'message': f'No data available for {symbol}'
                    }
                    continue
                
                # Train models
                result = await predictor.train_models(data, train_request.target_column)
                training_results[symbol] = result
                
                logger.info(f"Training completed for {symbol}")
                
            except Exception as e:
                logger.error(f"Error training models for {symbol}: {e}")
                training_results[symbol] = {
                    'status': 'error',
                    'message': str(e)
                }
        
        return {
            'status': 'success',
            'message': 'ML model training completed',
            'training_results': training_results,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in train_ml_models: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to train ML models: {str(e)}"
        )

@router.post("/predict", response_model=Dict[str, Any])
async def make_prediction(
    predict_request: PredictRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Make price prediction using trained ML models."""
    try:
        logger.info(f"Making prediction for {predict_request.symbol}")
        
        # Get predictor
        if predict_request.symbol not in MLAPI(None).price_predictors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No trained models found for {predict_request.symbol}"
            )
        
        predictor = MLAPI(None).price_predictors[predict_request.symbol]
        
        # Get latest data
        from ..data.data_manager import DataManager
        data_manager = DataManager()
        
        if predict_request.symbol.startswith('data/'):
            data = await data_manager.get_local_data(predict_request.symbol)
        else:
            data = await data_manager.get_yahoo_data(predict_request.symbol, period="30d")
        
        if data.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data available for {predict_request.symbol}"
            )
        
        # Make prediction
        prediction_result = await predictor.predict(data, predict_request.model_name)
        
        return {
            'status': 'success',
            'prediction_result': prediction_result,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to make prediction: {str(e)}"
        )

@router.get("/model-info/{symbol}", response_model=Dict[str, Any])
async def get_model_info(
    symbol: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get information about trained ML models for a symbol."""
    try:
        logger.info(f"Getting model info for {symbol}")
        
        if symbol not in MLAPI(None).price_predictors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No trained models found for {symbol}"
            )
        
        predictor = MLAPI(None).price_predictors[symbol]
        model_info = predictor.get_model_info()
        
        return {
            'status': 'success',
            'symbol': symbol,
            'model_info': model_info,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model info: {str(e)}"
        )

@router.post("/automated-trader/create", response_model=Dict[str, Any])
async def create_automated_trader(
    trader_request: AutomatedTraderRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Create an automated trading system."""
    try:
        logger.info(f"Creating automated trader for fund {trader_request.fund_id}")
        
        # Validate strategy
        try:
            strategy = TradingStrategy(trader_request.strategy)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid strategy: {trader_request.strategy}"
            )
        
        # Create automated trader
        trader = AutomatedTrader(trader_request.fund_id, strategy)
        MLAPI(None).automated_traders[trader_request.fund_id] = trader
        
        # Initialize trader
        init_result = await trader.initialize()
        
        return {
            'status': 'success',
            'message': 'Automated trader created successfully',
            'fund_id': trader_request.fund_id,
            'strategy': trader_request.strategy,
            'symbols': trader_request.symbols,
            'init_result': init_result,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating automated trader: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create automated trader: {str(e)}"
        )

@router.post("/automated-trader/train", response_model=Dict[str, Any])
async def train_automated_trader(
    fund_id: str,
    symbols: List[str],
    lookback_days: int = 365,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Train ML models for automated trader."""
    try:
        logger.info(f"Training automated trader for fund {fund_id}")
        
        if fund_id not in MLAPI(None).automated_traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Automated trader not found for fund {fund_id}"
            )
        
        trader = MLAPI(None).automated_traders[fund_id]
        training_result = await trader.train_models(symbols, lookback_days)
        
        return {
            'status': 'success',
            'training_result': training_result,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error training automated trader: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to train automated trader: {str(e)}"
        )

@router.post("/automated-trader/start", response_model=Dict[str, Any])
async def start_automated_trading(
    fund_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Start automated trading."""
    try:
        logger.info(f"Starting automated trading for fund {fund_id}")
        
        if fund_id not in MLAPI(None).automated_traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Automated trader not found for fund {fund_id}"
            )
        
        trader = MLAPI(None).automated_traders[fund_id]
        trader.start_trading()
        
        return {
            'status': 'success',
            'message': f'Automated trading started for fund {fund_id}',
            'fund_id': fund_id,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting automated trading: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start automated trading: {str(e)}"
        )

@router.post("/automated-trader/stop", response_model=Dict[str, Any])
async def stop_automated_trading(
    fund_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Stop automated trading."""
    try:
        logger.info(f"Stopping automated trading for fund {fund_id}")
        
        if fund_id not in MLAPI(None).automated_traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Automated trader not found for fund {fund_id}"
            )
        
        trader = MLAPI(None).automated_traders[fund_id]
        trader.stop_trading()
        
        return {
            'status': 'success',
            'message': f'Automated trading stopped for fund {fund_id}',
            'fund_id': fund_id,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error stopping automated trading: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stop automated trading: {str(e)}"
        )

@router.post("/automated-trader/run-cycle", response_model=Dict[str, Any])
async def run_trading_cycle(
    fund_id: str,
    symbols: List[str],
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Run a trading cycle for specified symbols."""
    try:
        logger.info(f"Running trading cycle for fund {fund_id}")
        
        if fund_id not in MLAPI(None).automated_traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Automated trader not found for fund {fund_id}"
            )
        
        trader = MLAPI(None).automated_traders[fund_id]
        cycle_result = await trader.run_trading_cycle(symbols)
        
        return {
            'status': 'success',
            'cycle_result': cycle_result,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running trading cycle: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run trading cycle: {str(e)}"
        )

@router.get("/automated-trader/performance/{fund_id}", response_model=Dict[str, Any])
async def get_trader_performance(
    fund_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get performance summary of automated trader."""
    try:
        logger.info(f"Getting trader performance for fund {fund_id}")
        
        if fund_id not in MLAPI(None).automated_traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Automated trader not found for fund {fund_id}"
            )
        
        trader = MLAPI(None).automated_traders[fund_id]
        performance = trader.get_performance_summary()
        
        return {
            'status': 'success',
            'performance': performance,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trader performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get trader performance: {str(e)}"
        )

@router.post("/automated-trader/update-params", response_model=Dict[str, Any])
async def update_trading_params(
    params_request: TradingParamsRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Update trading parameters for automated trader."""
    try:
        logger.info(f"Updating trading params for fund {params_request.fund_id}")
        
        if params_request.fund_id not in MLAPI(None).automated_traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Automated trader not found for fund {params_request.fund_id}"
            )
        
        trader = MLAPI(None).automated_traders[params_request.fund_id]
        
        # Prepare new parameters
        new_params = {}
        for key, value in params_request.dict().items():
            if key != 'fund_id' and value is not None:
                new_params[key] = value
        
        result = trader.update_trading_params(new_params)
        
        return {
            'status': 'success',
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating trading params: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update trading params: {str(e)}"
        )

@router.get("/health", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Health check endpoint for ML API."""
    return {"status": "healthy", "service": "ml-api"}
