"""
Data API for Pocket Hedge Fund.

This module provides REST API endpoints for data management and analysis.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, validator

from ..database import DatabaseManager, DatabaseUtils
from ..auth.middleware import get_current_user, require_fund_manager
from ..data.data_manager import DataManager
from ..analysis.indicator_integration_simple import IndicatorIntegration

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Create router
router = APIRouter(prefix="/data", tags=["Data Management"])

class DataAPI:
    """Data API class for dependency injection."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.router = router
        self.data_manager = DataManager()
        self.indicator_integration = IndicatorIntegration()

# Pydantic models

class DataRequest(BaseModel):
    symbols: List[str]
    source: str = "yahoo"  # yahoo, binance, local
    period: str = "1y"
    interval: str = "1d"

class IndicatorRequest(BaseModel):
    symbol: str
    indicators: Optional[List[str]] = None  # If None, calculate all

class TradingSignalRequest(BaseModel):
    symbol: str
    current_price: float

# API Endpoints

@router.post("/market-data", response_model=Dict[str, Any])
async def get_market_data(
    data_request: DataRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get market data for specified symbols."""
    try:
        # Mock authentication for demonstration
        logger.info(f"Fetching market data for symbols: {data_request.symbols}")
        
        results = {}
        
        for symbol in data_request.symbols:
            try:
                if data_request.source == "yahoo":
                    data = await DataManager().get_yahoo_data(
                        symbol, data_request.period, data_request.interval
                    )
                elif data_request.source == "binance":
                    data = await DataManager().get_binance_data(
                        symbol, data_request.interval
                    )
                elif data_request.source == "local":
                    data = await DataManager().get_local_data(symbol)
                else:
                    raise ValueError(f"Unsupported data source: {data_request.source}")
                
                # Convert to dict for JSON response
                results[symbol] = {
                    'data': data.to_dict('records') if not data.empty else [],
                    'columns': list(data.columns),
                    'shape': data.shape,
                    'last_updated': datetime.now().isoformat()
                }
                
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
                results[symbol] = {
                    'error': str(e),
                    'data': [],
                    'columns': [],
                    'shape': (0, 0)
                }
        
        return {
            'status': 'success',
            'source': data_request.source,
            'symbols': data_request.symbols,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in get_market_data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch market data: {str(e)}"
        )

@router.post("/indicators", response_model=Dict[str, Any])
async def calculate_indicators(
    indicator_request: IndicatorRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Calculate technical indicators for a symbol."""
    try:
        logger.info(f"Calculating indicators for {indicator_request.symbol}")
        
        # Get market data first
        data_manager = DataManager()
        try:
            data = await data_manager.get_yahoo_data(indicator_request.symbol)
        except:
            # Try local data if yahoo fails
            data = await data_manager.get_local_data(indicator_request.symbol)
        
        if data.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for symbol {indicator_request.symbol}"
            )
        
        # Calculate indicators
        indicator_integration = IndicatorIntegration()
        indicators = await indicator_integration.calculate_indicators(
            data, indicator_request.symbol
        )
        
        # Get indicator summary
        summary = indicator_integration.get_indicator_summary(indicator_request.symbol)
        
        return {
            'status': 'success',
            'symbol': indicator_request.symbol,
            'indicators_calculated': len(indicators),
            'indicator_summary': summary,
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

@router.post("/trading-signals", response_model=Dict[str, Any])
async def get_trading_signals(
    signal_request: TradingSignalRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get trading signals for a symbol."""
    try:
        logger.info(f"Generating trading signals for {signal_request.symbol}")
        
        # Get market data and calculate indicators
        data_manager = DataManager()
        try:
            data = await data_manager.get_yahoo_data(signal_request.symbol)
        except:
            # Try local data if yahoo fails
            data = await data_manager.get_local_data(signal_request.symbol)
        
        if data.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for symbol {signal_request.symbol}"
            )
        
        # Calculate indicators
        indicator_integration = IndicatorIntegration()
        await indicator_integration.calculate_indicators(data, signal_request.symbol)
        
        # Generate trading signals
        signals = indicator_integration.get_trading_signals(signal_request.symbol)
        
        # Add current price to signals
        signals['current_price'] = signal_request.current_price
        signals['price_change'] = (
            signal_request.current_price - data['close'].iloc[-1]
        ) / data['close'].iloc[-1] if not data.empty else 0
        
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

@router.get("/available-symbols", response_model=Dict[str, Any])
async def get_available_symbols(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    source: str = "yahoo"
) -> Dict[str, Any]:
    """Get list of available symbols from data source."""
    try:
        logger.info(f"Getting available symbols from {source}")
        
        data_manager = DataManager()
        symbols = await data_manager.get_available_symbols(source)
        
        return {
            'status': 'success',
            'source': source,
            'symbols': symbols,
            'count': len(symbols),
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting available symbols: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get available symbols: {str(e)}"
        )

@router.get("/data-sources", response_model=Dict[str, Any])
async def get_data_sources(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get information about available data sources."""
    try:
        data_sources = {
            'yahoo': {
                'name': 'Yahoo Finance',
                'description': 'Free financial data for stocks, ETFs, currencies, and cryptocurrencies',
                'supported_assets': ['stocks', 'etfs', 'currencies', 'crypto'],
                'update_frequency': 'real-time',
                'cost': 'free'
            },
            'binance': {
                'name': 'Binance API',
                'description': 'Cryptocurrency market data from Binance exchange',
                'supported_assets': ['cryptocurrencies'],
                'update_frequency': 'real-time',
                'cost': 'free (with rate limits)'
            },
            'local': {
                'name': 'Local Data Files',
                'description': 'Data from local CSV and Parquet files',
                'supported_assets': ['any'],
                'update_frequency': 'manual',
                'cost': 'free'
            }
        }
        
        return {
            'status': 'success',
            'data_sources': data_sources,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting data sources: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get data sources: {str(e)}"
        )

@router.get("/cache-info", response_model=Dict[str, Any])
async def get_cache_info(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get information about data cache."""
    try:
        data_manager = DataManager()
        cache_info = data_manager.get_cache_info()
        
        return {
            'status': 'success',
            'cache_info': cache_info,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting cache info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cache info: {str(e)}"
        )

@router.post("/clear-cache", response_model=Dict[str, Any])
async def clear_cache(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Clear data cache."""
    try:
        data_manager = DataManager()
        data_manager.clear_cache()
        
        return {
            'status': 'success',
            'message': 'Data cache cleared successfully',
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}"
        )

@router.get("/health", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Health check endpoint for data API."""
    return {"status": "healthy", "service": "data-api"}
