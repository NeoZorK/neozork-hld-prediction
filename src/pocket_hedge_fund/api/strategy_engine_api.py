"""
NeoZork Pocket Hedge Fund - Strategy Engine API

This module provides RESTful API endpoints for strategy execution including:
- Strategy creation and management
- Strategy execution control
- Performance monitoring
- Backtesting
- Order management
- Risk management
- Real-time execution status
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Body, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import logging
import asyncio
import json

from ..strategy_engine.strategy_executor import (
    StrategyExecutor, StrategyStatus, OrderType, OrderSide, OrderStatus,
    SignalType, RiskLevel, TradingSignal, Order, StrategyExecution
)
from ..auth.jwt_manager import JWTManager
from ..config.database_manager import DatabaseManager
from ..config.config_manager import ConfigManager
from ..notifications.notification_manager import NotificationManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/v1/strategy-engine", tags=["strategy-engine"])

# Security
security = HTTPBearer()

# Global instances
strategy_executor = None
jwt_manager = None
notification_manager = None

async def get_strategy_executor() -> StrategyExecutor:
    """Get strategy executor instance"""
    global strategy_executor
    if not strategy_executor:
        db_manager = DatabaseManager()
        config_manager = ConfigManager()
        notification_mgr = NotificationManager(db_manager, config_manager)
        
        await db_manager.initialize()
        await config_manager.initialize()
        await notification_mgr.initialize()
        
        strategy_executor = StrategyExecutor(db_manager, config_manager, notification_mgr)
        await strategy_executor.initialize()
    
    return strategy_executor

async def get_jwt_manager() -> JWTManager:
    """Get JWT manager instance"""
    global jwt_manager
    if not jwt_manager:
        jwt_manager = JWTManager()
    
    return jwt_manager

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    jwt_mgr = await get_jwt_manager()
    
    try:
        payload = jwt_mgr.validate_token(credentials.credentials)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Pydantic models

class StrategyCreateRequest(BaseModel):
    """Request model for creating strategy"""
    strategy_type: str = Field(..., description="Strategy type (momentum, mean_reversion)")
    name: str = Field(..., description="Strategy name")
    description: str = Field(..., description="Strategy description")
    fund_id: str = Field(..., description="Fund ID to associate with strategy")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Strategy parameters")
    risk_parameters: Dict[str, Any] = Field(default_factory=dict, description="Risk parameters")
    execution_parameters: Dict[str, Any] = Field(default_factory=dict, description="Execution parameters")

class StrategyResponse(BaseModel):
    """Response model for strategy"""
    strategy_id: str
    strategy_type: str
    name: str
    description: str
    fund_id: str
    status: str
    parameters: Dict[str, Any]
    risk_parameters: Dict[str, Any]
    execution_parameters: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class StrategyExecutionResponse(BaseModel):
    """Response model for strategy execution"""
    execution_id: str
    strategy_id: str
    fund_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime]
    total_signals: int
    successful_signals: int
    failed_signals: int
    total_orders: int
    filled_orders: int
    cancelled_orders: int
    total_pnl: float
    total_commission: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    created_at: datetime
    updated_at: datetime

class StrategyPerformanceResponse(BaseModel):
    """Response model for strategy performance"""
    strategy_id: str
    name: str
    status: str
    start_time: datetime
    end_time: Optional[datetime]
    total_signals: int
    successful_signals: int
    failed_signals: int
    success_rate: float
    total_orders: int
    filled_orders: int
    cancelled_orders: int
    fill_rate: float
    total_pnl: float
    total_commission: float
    net_pnl: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    positions: int
    active_orders: int

class BacktestRequest(BaseModel):
    """Request model for backtesting"""
    strategy_id: str = Field(..., description="Strategy ID to backtest")
    start_date: datetime = Field(..., description="Backtest start date")
    end_date: datetime = Field(..., description="Backtest end date")
    initial_capital: float = Field(..., description="Initial capital for backtest")
    symbols: List[str] = Field(default_factory=list, description="Symbols to backtest")

class BacktestResponse(BaseModel):
    """Response model for backtest results"""
    strategy_id: str
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    total_trades: int
    winning_trades: int
    win_rate: float
    equity_curve: List[float]
    trades: List[Dict[str, Any]]

class OrderResponse(BaseModel):
    """Response model for order"""
    order_id: str
    strategy_id: str
    symbol: str
    order_type: str
    side: str
    quantity: float
    price: Optional[float]
    stop_price: Optional[float]
    status: str
    filled_quantity: float
    average_fill_price: Optional[float]
    commission: float
    created_at: datetime
    updated_at: datetime

class SignalResponse(BaseModel):
    """Response model for trading signal"""
    signal_id: str
    strategy_id: str
    symbol: str
    signal_type: str
    strength: float
    price: float
    quantity: float
    stop_loss: Optional[float]
    take_profit: Optional[float]
    confidence: float
    metadata: Dict[str, Any]
    created_at: datetime

class StrategyListResponse(BaseModel):
    """Response model for strategy list"""
    strategies: List[StrategyResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int

# API Endpoints

@router.post("/strategies", response_model=Dict[str, str])
async def create_strategy(
    request: StrategyCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new trading strategy"""
    try:
        # Check permissions
        if current_user.get("role") not in ["ADMIN", "MANAGER", "TRADER"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        # Validate strategy type
        if request.strategy_type not in ["momentum", "mean_reversion"]:
            raise HTTPException(status_code=400, detail="Invalid strategy type")
        
        # Create strategy
        executor = await get_strategy_executor()
        strategy_id = await executor.create_strategy(
            strategy_id=str(uuid4()),
            strategy_type=request.strategy_type,
            parameters=request.parameters,
            fund_id=request.fund_id
        )
        
        return {
            "status": "success",
            "message": "Strategy created successfully",
            "strategy_id": strategy_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create strategy: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/strategies", response_model=StrategyListResponse)
async def get_strategies(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    fund_id: Optional[str] = Query(None, description="Filter by fund ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: dict = Depends(get_current_user)
):
    """Get list of strategies with pagination and filtering"""
    try:
        executor = await get_strategy_executor()
        
        # Get strategies (in real implementation, this would query database)
        strategies = []
        for strategy_id, strategy in executor.strategies.items():
            execution = executor.executions.get(strategy_id)
            
            if fund_id and execution and execution.fund_id != fund_id:
                continue
            
            if status and strategy.status.value != status:
                continue
            
            strategies.append(StrategyResponse(
                strategy_id=strategy_id,
                strategy_type=type(strategy).__name__.lower().replace("strategy", ""),
                name=strategy.name,
                description=strategy.description,
                fund_id=execution.fund_id if execution else "",
                status=strategy.status.value,
                parameters=strategy.parameters,
                risk_parameters=strategy.risk_parameters,
                execution_parameters=strategy.execution_parameters,
                created_at=execution.created_at if execution else datetime.now(datetime.UTC),
                updated_at=execution.updated_at if execution else datetime.now(datetime.UTC)
            ))
        
        # Apply pagination
        total_count = len(strategies)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_strategies = strategies[start_idx:end_idx]
        
        total_pages = (total_count + page_size - 1) // page_size
        
        return StrategyListResponse(
            strategies=paginated_strategies,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get strategies: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/strategies/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(
    strategy_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get strategy by ID"""
    try:
        executor = await get_strategy_executor()
        
        if strategy_id not in executor.strategies:
            raise HTTPException(status_code=404, detail="Strategy not found")
        
        strategy = executor.strategies[strategy_id]
        execution = executor.executions.get(strategy_id)
        
        return StrategyResponse(
            strategy_id=strategy_id,
            strategy_type=type(strategy).__name__.lower().replace("strategy", ""),
            name=strategy.name,
            description=strategy.description,
            fund_id=execution.fund_id if execution else "",
            status=strategy.status.value,
            parameters=strategy.parameters,
            risk_parameters=strategy.risk_parameters,
            execution_parameters=strategy.execution_parameters,
            created_at=execution.created_at if execution else datetime.now(datetime.UTC),
            updated_at=execution.updated_at if execution else datetime.now(datetime.UTC)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get strategy: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/strategies/{strategy_id}/start", response_model=Dict[str, str])
async def start_strategy(
    strategy_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Start strategy execution"""
    try:
        # Check permissions
        if current_user.get("role") not in ["ADMIN", "MANAGER", "TRADER"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        executor = await get_strategy_executor()
        
        if strategy_id not in executor.strategies:
            raise HTTPException(status_code=404, detail="Strategy not found")
        
        success = await executor.start_strategy(strategy_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to start strategy")
        
        return {
            "status": "success",
            "message": "Strategy started successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start strategy: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/strategies/{strategy_id}/stop", response_model=Dict[str, str])
async def stop_strategy(
    strategy_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Stop strategy execution"""
    try:
        # Check permissions
        if current_user.get("role") not in ["ADMIN", "MANAGER", "TRADER"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        executor = await get_strategy_executor()
        
        if strategy_id not in executor.strategies:
            raise HTTPException(status_code=404, detail="Strategy not found")
        
        success = await executor.stop_strategy(strategy_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to stop strategy")
        
        return {
            "status": "success",
            "message": "Strategy stopped successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to stop strategy: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/strategies/{strategy_id}/performance", response_model=StrategyPerformanceResponse)
async def get_strategy_performance(
    strategy_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get strategy performance metrics"""
    try:
        executor = await get_strategy_executor()
        
        if strategy_id not in executor.strategies:
            raise HTTPException(status_code=404, detail="Strategy not found")
        
        performance = await executor.get_strategy_performance(strategy_id)
        
        if not performance:
            raise HTTPException(status_code=404, detail="Performance data not found")
        
        return StrategyPerformanceResponse(**performance)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get strategy performance: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/strategies/{strategy_id}/backtest", response_model=BacktestResponse)
async def backtest_strategy(
    strategy_id: str,
    request: BacktestRequest,
    current_user: dict = Depends(get_current_user)
):
    """Backtest a strategy"""
    try:
        # Check permissions
        if current_user.get("role") not in ["ADMIN", "MANAGER", "TRADER", "ANALYST"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        executor = await get_strategy_executor()
        
        if strategy_id not in executor.strategies:
            raise HTTPException(status_code=404, detail="Strategy not found")
        
        # Validate dates
        if request.end_date <= request.start_date:
            raise HTTPException(status_code=400, detail="End date must be after start date")
        
        if request.initial_capital <= 0:
            raise HTTPException(status_code=400, detail="Initial capital must be positive")
        
        # Run backtest
        backtest_results = await executor.backtest_strategy(
            strategy_id=strategy_id,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital
        )
        
        if not backtest_results:
            raise HTTPException(status_code=500, detail="Backtest failed")
        
        return BacktestResponse(
            strategy_id=strategy_id,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital,
            final_capital=backtest_results["final_capital"],
            total_return=backtest_results["total_return"],
            sharpe_ratio=backtest_results["sharpe_ratio"],
            max_drawdown=backtest_results["max_drawdown"],
            total_trades=backtest_results["total_trades"],
            winning_trades=backtest_results["winning_trades"],
            win_rate=backtest_results["winning_trades"] / backtest_results["total_trades"] if backtest_results["total_trades"] > 0 else 0,
            equity_curve=backtest_results["equity_curve"],
            trades=backtest_results["trades"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to backtest strategy: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/strategies/{strategy_id}/orders", response_model=List[OrderResponse])
async def get_strategy_orders(
    strategy_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    status: Optional[str] = Query(None, description="Filter by order status"),
    current_user: dict = Depends(get_current_user)
):
    """Get strategy orders"""
    try:
        executor = await get_strategy_executor()
        
        if strategy_id not in executor.strategies:
            raise HTTPException(status_code=404, detail="Strategy not found")
        
        # Get orders for strategy
        strategy_orders = []
        for order_id, order in executor.orders.items():
            if order.strategy_id == strategy_id:
                if status and order.status.value != status:
                    continue
                
                strategy_orders.append(OrderResponse(
                    order_id=order.order_id,
                    strategy_id=order.strategy_id,
                    symbol=order.symbol,
                    order_type=order.order_type.value,
                    side=order.side.value,
                    quantity=order.quantity,
                    price=order.price,
                    stop_price=order.stop_price,
                    status=order.status.value,
                    filled_quantity=order.filled_quantity,
                    average_fill_price=order.average_fill_price,
                    commission=order.commission,
                    created_at=order.created_at,
                    updated_at=order.updated_at
                ))
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_orders = strategy_orders[start_idx:end_idx]
        
        return paginated_orders
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get strategy orders: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/strategies/{strategy_id}/signals", response_model=List[SignalResponse])
async def get_strategy_signals(
    strategy_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    signal_type: Optional[str] = Query(None, description="Filter by signal type"),
    current_user: dict = Depends(get_current_user)
):
    """Get strategy signals"""
    try:
        executor = await get_strategy_executor()
        
        if strategy_id not in executor.strategies:
            raise HTTPException(status_code=404, detail="Strategy not found")
        
        strategy = executor.strategies[strategy_id]
        
        # Get signals for strategy
        strategy_signals = []
        for signal in strategy.signals:
            if signal_type and signal.signal_type.value != signal_type:
                continue
            
            strategy_signals.append(SignalResponse(
                signal_id=signal.signal_id,
                strategy_id=signal.strategy_id,
                symbol=signal.symbol,
                signal_type=signal.signal_type.value,
                strength=signal.strength,
                price=signal.price,
                quantity=signal.quantity,
                stop_loss=signal.stop_loss,
                take_profit=signal.take_profit,
                confidence=signal.confidence,
                metadata=signal.metadata,
                created_at=signal.created_at
            ))
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_signals = strategy_signals[start_idx:end_idx]
        
        return paginated_signals
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get strategy signals: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/executions", response_model=List[StrategyExecutionResponse])
async def get_strategy_executions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    fund_id: Optional[str] = Query(None, description="Filter by fund ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: dict = Depends(get_current_user)
):
    """Get strategy executions"""
    try:
        executor = await get_strategy_executor()
        
        # Get executions
        executions = []
        for execution in executor.executions.values():
            if fund_id and execution.fund_id != fund_id:
                continue
            
            if status and execution.status.value != status:
                continue
            
            executions.append(StrategyExecutionResponse(
                execution_id=execution.execution_id,
                strategy_id=execution.strategy_id,
                fund_id=execution.fund_id,
                status=execution.status.value,
                start_time=execution.start_time,
                end_time=execution.end_time,
                total_signals=execution.total_signals,
                successful_signals=execution.successful_signals,
                failed_signals=execution.failed_signals,
                total_orders=execution.total_orders,
                filled_orders=execution.filled_orders,
                cancelled_orders=execution.cancelled_orders,
                total_pnl=execution.total_pnl,
                total_commission=execution.total_commission,
                max_drawdown=execution.max_drawdown,
                sharpe_ratio=execution.sharpe_ratio,
                win_rate=execution.win_rate,
                created_at=execution.created_at,
                updated_at=execution.updated_at
            ))
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_executions = executions[start_idx:end_idx]
        
        return paginated_executions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get strategy executions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/statistics", response_model=Dict[str, Any])
async def get_strategy_statistics(
    fund_id: Optional[str] = Query(None, description="Filter by fund ID"),
    current_user: dict = Depends(get_current_user)
):
    """Get strategy engine statistics"""
    try:
        executor = await get_strategy_executor()
        
        # Calculate statistics
        total_strategies = len(executor.strategies)
        active_strategies = len([s for s in executor.strategies.values() if s.status == StrategyStatus.ACTIVE])
        total_orders = len(executor.orders)
        total_executions = len(executor.executions)
        
        # Calculate performance metrics
        total_pnl = sum(e.total_pnl for e in executor.executions.values())
        total_commission = sum(e.total_commission for e in executor.executions.values())
        net_pnl = total_pnl - total_commission
        
        statistics = {
            "total_strategies": total_strategies,
            "active_strategies": active_strategies,
            "paused_strategies": len([s for s in executor.strategies.values() if s.status == StrategyStatus.PAUSED]),
            "stopped_strategies": len([s for s in executor.strategies.values() if s.status == StrategyStatus.STOPPED]),
            "total_executions": total_executions,
            "total_orders": total_orders,
            "total_pnl": total_pnl,
            "total_commission": total_commission,
            "net_pnl": net_pnl,
            "strategies_by_type": {
                "momentum": len([s for s in executor.strategies.values() if type(s).__name__ == "MomentumStrategy"]),
                "mean_reversion": len([s for s in executor.strategies.values() if type(s).__name__ == "MeanReversionStrategy"])
            }
        }
        
        return statistics
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get strategy statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# WebSocket endpoint for real-time strategy updates
@router.websocket("/ws/{strategy_id}")
async def websocket_strategy_updates(websocket: WebSocket, strategy_id: str):
    """WebSocket endpoint for real-time strategy updates"""
    try:
        await websocket.accept()
        
        executor = await get_strategy_executor()
        
        if strategy_id not in executor.strategies:
            await websocket.close(code=1008, reason="Strategy not found")
            return
        
        strategy = executor.strategies[strategy_id]
        execution = executor.executions[strategy_id]
        
        # Send initial status
        await websocket.send_json({
            "type": "strategy_status",
            "data": {
                "strategy_id": strategy_id,
                "name": strategy.name,
                "status": strategy.status.value,
                "total_signals": execution.total_signals,
                "successful_signals": execution.successful_signals,
                "total_orders": execution.total_orders,
                "filled_orders": execution.filled_orders,
                "total_pnl": execution.total_pnl
            }
        })
        
        # Keep connection alive and send updates
        while True:
            try:
                # Check for updates
                current_execution = executor.executions[strategy_id]
                
                # Send performance update
                await websocket.send_json({
                    "type": "performance_update",
                    "data": {
                        "strategy_id": strategy_id,
                        "total_signals": current_execution.total_signals,
                        "successful_signals": current_execution.successful_signals,
                        "total_orders": current_execution.total_orders,
                        "filled_orders": current_execution.filled_orders,
                        "total_pnl": current_execution.total_pnl,
                        "timestamp": datetime.now(datetime.UTC).isoformat()
                    }
                })
                
                # Wait before next update
                await asyncio.sleep(5)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
        
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        await websocket.close()

# Import uuid4 for strategy ID generation
from uuid import uuid4
