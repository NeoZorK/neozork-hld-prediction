#!/usr/bin/env python3
"""
Standalone ML API for Pocket Hedge Fund.

This is a standalone FastAPI application that demonstrates
the ML and automated trading functionality.
"""

import asyncio
import logging
import sys
import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add src to path
sys.path.append('src')

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Custom JSON encoder to handle NaN values
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            if np.isnan(obj):
                return None
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

# Import our ML modules
from pocket_hedge_fund.ml.price_predictor import PricePredictor
from pocket_hedge_fund.trading.automated_trader import AutomatedTrader, TradingStrategy
from pocket_hedge_fund.data.data_manager import DataManager
from pocket_hedge_fund.analysis.indicator_integration_simple import IndicatorIntegration
from pocket_hedge_fund.portfolio.portfolio_manager import PortfolioManager
from pocket_hedge_fund.backtesting.backtest_engine import BacktestEngine, BacktestConfig, BacktestMode

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Pocket Hedge Fund ML API",
    description="Standalone ML and Automated Trading API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
data_manager = DataManager()
price_predictors = {}
automated_traders = {}
portfolio_managers = {}

# Pydantic models
class TrainModelRequest(BaseModel):
    symbols: List[str]
    model_type: str = "ensemble"
    lookback_days: int = 365
    target_column: str = "future_return_1"

class PredictRequest(BaseModel):
    symbol: str
    model_name: Optional[str] = None

class CreateTraderRequest(BaseModel):
    fund_id: str
    strategy: str = "combined"
    symbols: List[str]
    initial_capital: float = 100000.0

class TradingParamsRequest(BaseModel):
    fund_id: str
    min_confidence: Optional[float] = None
    min_signal_strength: Optional[float] = None
    max_position_size: Optional[float] = None
    stop_loss_pct: Optional[float] = None
    take_profit_pct: Optional[float] = None
    max_daily_trades: Optional[int] = None
    cooldown_minutes: Optional[int] = None

class RunCycleRequest(BaseModel):
    fund_id: str
    symbols: List[str]

class BacktestRequest(BaseModel):
    symbols: List[str]
    strategy: str = "combined"
    model_type: str = "ensemble"
    start_date: str  # ISO format
    end_date: str    # ISO format
    initial_capital: float = 100000.0
    commission: float = 0.001
    slippage: float = 0.0005
    mode: str = "walk_forward"
    train_window_days: int = 252
    test_window_days: int = 63
    retrain_frequency_days: int = 21

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Pocket Hedge Fund ML API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ml-api",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/ml/train-models")
async def train_ml_models(request: TrainModelRequest):
    """Train machine learning models for price prediction."""
    try:
        logger.info(f"Training ML models for symbols: {request.symbols}")
        
        training_results = {}
        
        for symbol in request.symbols:
            try:
                # Create or get predictor
                if symbol not in price_predictors:
                    predictor = PricePredictor(model_type=request.model_type)
                    price_predictors[symbol] = predictor
                else:
                    predictor = price_predictors[symbol]
                
                # Get data for training
                if symbol.startswith('data/'):
                    data = await data_manager.get_local_data(symbol)
                else:
                    data = await data_manager.get_yahoo_data(symbol, period=f"{request.lookback_days}d")
                
                if data.empty:
                    training_results[symbol] = {
                        'status': 'error',
                        'message': f'No data available for {symbol}'
                    }
                    continue
                
                # Train models
                result = await predictor.train_models(data, request.target_column)
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

@app.post("/api/v1/ml/predict")
async def make_prediction(request: PredictRequest):
    """Make price prediction using trained ML models."""
    try:
        logger.info(f"Making prediction for {request.symbol}")
        
        # Get predictor
        if request.symbol not in price_predictors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No trained models found for {request.symbol}"
            )
        
        predictor = price_predictors[request.symbol]
        
        # Get latest data
        if request.symbol.startswith('data/'):
            data = await data_manager.get_local_data(request.symbol)
        else:
            data = await data_manager.get_yahoo_data(request.symbol, period="30d")
        
        if data.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data available for {request.symbol}"
            )
        
        # Make prediction
        prediction_result = await predictor.predict(data, request.model_name)
        
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

@app.get("/api/v1/ml/model-info/{symbol}")
async def get_model_info(symbol: str):
    """Get information about trained ML models for a symbol."""
    try:
        logger.info(f"Getting model info for {symbol}")
        
        if symbol not in price_predictors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No trained models found for {symbol}"
            )
        
        predictor = price_predictors[symbol]
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

@app.post("/api/v1/trading/create-trader")
async def create_automated_trader(request: CreateTraderRequest):
    """Create an automated trading system."""
    try:
        logger.info(f"Creating automated trader for fund {request.fund_id}")
        
        # Validate strategy
        try:
            strategy = TradingStrategy(request.strategy)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid strategy: {request.strategy}"
            )
        
        # Create portfolio manager
        if request.fund_id not in portfolio_managers:
            portfolio_manager = PortfolioManager(request.fund_id, request.initial_capital)
            portfolio_managers[request.fund_id] = portfolio_manager
        
        # Create automated trader
        trader = AutomatedTrader(request.fund_id, strategy)
        automated_traders[request.fund_id] = trader
        
        # Initialize trader
        init_result = await trader.initialize()
        
        return {
            'status': 'success',
            'message': 'Automated trader created successfully',
            'fund_id': request.fund_id,
            'strategy': request.strategy,
            'symbols': request.symbols,
            'initial_capital': request.initial_capital,
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

@app.post("/api/v1/trading/start/{fund_id}")
async def start_automated_trading(fund_id: str):
    """Start automated trading."""
    try:
        logger.info(f"Starting automated trading for fund {fund_id}")
        
        if fund_id not in automated_traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Automated trader not found for fund {fund_id}"
            )
        
        trader = automated_traders[fund_id]
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

@app.post("/api/v1/trading/stop/{fund_id}")
async def stop_automated_trading(fund_id: str):
    """Stop automated trading."""
    try:
        logger.info(f"Stopping automated trading for fund {fund_id}")
        
        if fund_id not in automated_traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Automated trader not found for fund {fund_id}"
            )
        
        trader = automated_traders[fund_id]
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

@app.post("/api/v1/trading/run-cycle")
async def run_trading_cycle(request: RunCycleRequest):
    """Run a trading cycle for specified symbols."""
    try:
        logger.info(f"Running trading cycle for fund {request.fund_id}")
        
        if request.fund_id not in automated_traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Automated trader not found for fund {request.fund_id}"
            )
        
        trader = automated_traders[request.fund_id]
        cycle_result = await trader.run_trading_cycle(request.symbols)
        
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

@app.get("/api/v1/trading/performance/{fund_id}")
async def get_trader_performance(fund_id: str):
    """Get performance summary of automated trader."""
    try:
        logger.info(f"Getting trader performance for fund {fund_id}")
        
        if fund_id not in automated_traders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Automated trader not found for fund {fund_id}"
            )
        
        trader = automated_traders[fund_id]
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

@app.post("/api/v1/data/indicators")
async def calculate_indicators(request: Dict[str, str]):
    """Calculate technical indicators for a symbol."""
    try:
        symbol = request.get('symbol', '')
        logger.info(f"Calculating indicators for {symbol}")
        
        # Get data
        if symbol.startswith('data/'):
            data = await data_manager.get_local_data(symbol)
        else:
            data = await data_manager.get_yahoo_data(symbol, period="30d")
        
        if data.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data available for {symbol}"
            )
        
        # Calculate indicators
        indicator_integration = IndicatorIntegration()
        indicators = await indicator_integration.calculate_indicators(data, symbol)
        
        return {
            'status': 'success',
            'symbol': symbol,
            'indicators': indicators,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating indicators: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate indicators: {str(e)}"
        )

@app.post("/api/v1/data/trading-signals")
async def get_trading_signals(symbol: str):
    """Generate trading signals for a symbol."""
    try:
        logger.info(f"Generating trading signals for {symbol}")
        
        # Get data
        if symbol.startswith('data/'):
            data = await data_manager.get_local_data(symbol)
        else:
            data = await data_manager.get_yahoo_data(symbol, period="30d")
        
        if data.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data available for {symbol}"
            )
        
        # Calculate indicators and generate signals
        indicator_integration = IndicatorIntegration()
        await indicator_integration.calculate_indicators(data, symbol)
        signals = indicator_integration.get_trading_signals(symbol)
        
        return {
            'status': 'success',
            'signals': signals,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating trading signals: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate trading signals: {str(e)}"
        )

@app.get("/api/v1/portfolio/summary/{fund_id}")
async def get_portfolio_summary(fund_id: str):
    """Get portfolio summary for a fund."""
    try:
        logger.info(f"Getting portfolio summary for fund {fund_id}")
        
        if fund_id not in portfolio_managers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Portfolio manager not found for fund {fund_id}"
            )
        
        portfolio_manager = portfolio_managers[fund_id]
        summary = portfolio_manager.get_portfolio_summary()
        
        return {
            'status': 'success',
            'portfolio_summary': summary,
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting portfolio summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get portfolio summary: {str(e)}"
        )

@app.get("/api/v1/status")
async def get_system_status():
    """Get system status."""
    return {
        'status': 'running',
        'ml_models': len(price_predictors),
        'automated_traders': len(automated_traders),
        'portfolio_managers': len(portfolio_managers),
        'timestamp': datetime.now().isoformat()
    }

@app.post("/api/v1/backtest/run")
async def run_backtest(request: BacktestRequest):
    """Run comprehensive backtest."""
    try:
        logger.info(f"Starting backtest for symbols: {request.symbols}")
        
        # Parse dates
        start_date = datetime.fromisoformat(request.start_date.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(request.end_date.replace('Z', '+00:00'))
        
        # Validate strategy
        try:
            strategy = TradingStrategy(request.strategy)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid strategy: {request.strategy}"
            )
        
        # Validate mode
        try:
            mode = BacktestMode(request.mode)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid mode: {request.mode}"
            )
        
        # Create backtest config
        config = BacktestConfig(
            start_date=start_date,
            end_date=end_date,
            initial_capital=request.initial_capital,
            commission=request.commission,
            slippage=request.slippage,
            mode=mode,
            train_window_days=request.train_window_days,
            test_window_days=request.test_window_days,
            retrain_frequency_days=request.retrain_frequency_days
        )
        
        # Create and run backtest engine
        engine = BacktestEngine(config)
        result = await engine.run_backtest(request.symbols, strategy, request.model_type)
        
        # Convert result to dict for JSON serialization
        result_dict = {
            'total_return': result.total_return,
            'annualized_return': result.annualized_return,
            'volatility': result.volatility,
            'sharpe_ratio': result.sharpe_ratio,
            'max_drawdown': result.max_drawdown,
            'win_rate': result.win_rate,
            'total_trades': result.total_trades,
            'winning_trades': result.winning_trades,
            'losing_trades': result.losing_trades,
            'avg_win': result.avg_win,
            'avg_loss': result.avg_loss,
            'profit_factor': result.profit_factor,
            'calmar_ratio': result.calmar_ratio,
            'sortino_ratio': result.sortino_ratio,
            'trades': result.trades,
            'equity_curve': result.equity_curve.to_dict('records') if not result.equity_curve.empty else [],
            'performance_metrics': result.performance_metrics
        }
        
        return {
            'status': 'success',
            'backtest_result': result_dict,
            'config': {
                'symbols': request.symbols,
                'strategy': request.strategy,
                'model_type': request.model_type,
                'start_date': request.start_date,
                'end_date': request.end_date,
                'initial_capital': request.initial_capital,
                'mode': request.mode
            },
            'timestamp': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run backtest: {str(e)}"
        )

@app.get("/api/v1/backtest/strategies")
async def get_available_strategies():
    """Get available trading strategies."""
    return {
        'strategies': [strategy.value for strategy in TradingStrategy],
        'modes': [mode.value for mode in BacktestMode],
        'model_types': ['ensemble', 'tree_based', 'linear'],
        'timestamp': datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    # Run the application
    uvicorn.run(
        "ml_api_standalone:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
