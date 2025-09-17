#!/usr/bin/env python3
"""
ML Dashboard for Pocket Hedge Fund.

This is a web-based dashboard for monitoring and managing
the ML trading system.
"""

import asyncio
import logging
import sys
import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Add src to path
sys.path.append('..')

from fastapi import FastAPI, HTTPException, status, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import aiohttp
import pandas as pd

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
    title="Pocket Hedge Fund ML Dashboard",
    description="Web Dashboard for ML Trading System",
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
backtest_results = {}

# Dashboard HTML
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pocket Hedge Fund ML Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .card h3 {
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .metric-value {
            font-weight: bold;
            color: #667eea;
        }
        .status {
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
        }
        .status.running {
            background: #d4edda;
            color: #155724;
        }
        .status.stopped {
            background: #f8d7da;
            color: #721c24;
        }
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        .btn:hover {
            background: #5a6fd8;
        }
        .btn.danger {
            background: #dc3545;
        }
        .btn.danger:hover {
            background: #c82333;
        }
        .form-group {
            margin: 10px 0;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .chart-container {
            position: relative;
            height: 300px;
            margin: 20px 0;
        }
        .log {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 10px;
            height: 200px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Pocket Hedge Fund ML Dashboard</h1>
            <p>Advanced AI-Powered Trading System</p>
        </div>

        <div class="grid">
            <!-- System Status -->
            <div class="card">
                <h3>📊 System Status</h3>
                <div class="metric">
                    <span>API Status:</span>
                    <span class="metric-value" id="api-status">Loading...</span>
                </div>
                <div class="metric">
                    <span>ML Models:</span>
                    <span class="metric-value" id="ml-models">0</span>
                </div>
                <div class="metric">
                    <span>Active Traders:</span>
                    <span class="metric-value" id="active-traders">0</span>
                </div>
                <div class="metric">
                    <span>Portfolios:</span>
                    <span class="metric-value" id="portfolios">0</span>
                </div>
                <button class="btn" onclick="refreshStatus()">🔄 Refresh</button>
            </div>

            <!-- ML Model Management -->
            <div class="card">
                <h3>🧠 ML Model Management</h3>
                <div class="form-group">
                    <label>Symbol:</label>
                    <input type="text" id="train-symbol" value="data/mn1.csv" placeholder="Enter symbol">
                </div>
                <div class="form-group">
                    <label>Model Type:</label>
                    <select id="model-type">
                        <option value="ensemble">Ensemble</option>
                        <option value="tree_based">Tree Based</option>
                        <option value="linear">Linear</option>
                    </select>
                </div>
                <button class="btn" onclick="trainModel()">🚀 Train Model</button>
                <button class="btn" onclick="predictPrice()">🔮 Predict Price</button>
            </div>

            <!-- Trading System -->
            <div class="card">
                <h3>⚡ Trading System</h3>
                <div class="form-group">
                    <label>Fund ID:</label>
                    <input type="text" id="fund-id" value="test-fund-001" placeholder="Enter fund ID">
                </div>
                <div class="form-group">
                    <label>Strategy:</label>
                    <select id="trading-strategy">
                        <option value="combined">Combined</option>
                        <option value="ml_only">ML Only</option>
                        <option value="technical_only">Technical Only</option>
                        <option value="conservative">Conservative</option>
                        <option value="aggressive">Aggressive</option>
                    </select>
                </div>
                <button class="btn" onclick="createTrader()">➕ Create Trader</button>
                <button class="btn" onclick="startTrading()">▶️ Start Trading</button>
                <button class="btn danger" onclick="stopTrading()">⏹️ Stop Trading</button>
            </div>

            <!-- Backtesting -->
            <div class="card">
                <h3>📈 Backtesting</h3>
                <div class="form-group">
                    <label>Symbols:</label>
                    <input type="text" id="backtest-symbols" value="data/mn1.csv" placeholder="Comma-separated symbols">
                </div>
                <div class="form-group">
                    <label>Strategy:</label>
                    <select id="backtest-strategy">
                        <option value="combined">Combined</option>
                        <option value="ml_only">ML Only</option>
                        <option value="technical_only">Technical Only</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Start Date:</label>
                    <input type="date" id="start-date" value="2023-01-01">
                </div>
                <div class="form-group">
                    <label>End Date:</label>
                    <input type="date" id="end-date" value="2023-12-31">
                </div>
                <button class="btn" onclick="runBacktest()">🏃 Run Backtest</button>
            </div>

            <!-- Performance Metrics -->
            <div class="card">
                <h3>📊 Performance Metrics</h3>
                <div class="metric">
                    <span>Total Return:</span>
                    <span class="metric-value" id="total-return">0%</span>
                </div>
                <div class="metric">
                    <span>Sharpe Ratio:</span>
                    <span class="metric-value" id="sharpe-ratio">0.00</span>
                </div>
                <div class="metric">
                    <span>Max Drawdown:</span>
                    <span class="metric-value" id="max-drawdown">0%</span>
                </div>
                <div class="metric">
                    <span>Win Rate:</span>
                    <span class="metric-value" id="win-rate">0%</span>
                </div>
                <button class="btn" onclick="refreshMetrics()">🔄 Refresh Metrics</button>
            </div>

            <!-- Real-time Logs -->
            <div class="card">
                <h3>📝 Real-time Logs</h3>
                <div class="log" id="logs">
                    <div>System initialized...</div>
                </div>
                <button class="btn" onclick="clearLogs()">🗑️ Clear Logs</button>
            </div>
        </div>

        <!-- Charts -->
        <div class="card">
            <h3>📈 Performance Chart</h3>
            <div class="chart-container">
                <canvas id="performanceChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        let performanceChart;
        let logs = [];

        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            initializeChart();
            refreshStatus();
            setInterval(refreshStatus, 5000); // Refresh every 5 seconds
        });

        function initializeChart() {
            const ctx = document.getElementById('performanceChart').getContext('2d');
            performanceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Portfolio Value',
                        data: [],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: false
                        }
                    }
                }
            });
        }

        function addLog(message) {
            const timestamp = new Date().toLocaleTimeString();
            logs.push(`[${timestamp}] ${message}`);
            if (logs.length > 100) logs.shift(); // Keep only last 100 logs
            
            const logElement = document.getElementById('logs');
            logElement.innerHTML = logs.map(log => `<div>${log}</div>`).join('');
            logElement.scrollTop = logElement.scrollHeight;
        }

        function clearLogs() {
            logs = [];
            document.getElementById('logs').innerHTML = '<div>Logs cleared...</div>';
        }

        async function refreshStatus() {
            try {
                const response = await axios.get('/api/v1/status');
                const data = response.data;
                
                document.getElementById('api-status').textContent = data.status;
                document.getElementById('ml-models').textContent = data.ml_models;
                document.getElementById('active-traders').textContent = data.automated_traders;
                document.getElementById('portfolios').textContent = data.portfolio_managers;
                
                addLog('Status refreshed');
            } catch (error) {
                addLog(`Error refreshing status: ${error.message}`);
            }
        }

        async function trainModel() {
            const symbol = document.getElementById('train-symbol').value;
            const modelType = document.getElementById('model-type').value;
            
            addLog(`Training ${modelType} model for ${symbol}...`);
            
            try {
                const response = await axios.post('/api/v1/ml/train-models', {
                    symbols: [symbol],
                    model_type: modelType,
                    lookback_days: 365
                });
                
                addLog(`Model training completed: ${response.data.status}`);
            } catch (error) {
                addLog(`Error training model: ${error.message}`);
            }
        }

        async function predictPrice() {
            const symbol = document.getElementById('train-symbol').value;
            
            addLog(`Making prediction for ${symbol}...`);
            
            try {
                const response = await axios.post('/api/v1/ml/predict', {
                    symbol: symbol
                });
                
                addLog(`Prediction completed: ${response.data.status}`);
            } catch (error) {
                addLog(`Error making prediction: ${error.message}`);
            }
        }

        async function createTrader() {
            const fundId = document.getElementById('fund-id').value;
            const strategy = document.getElementById('trading-strategy').value;
            
            addLog(`Creating trader for fund ${fundId} with ${strategy} strategy...`);
            
            try {
                const response = await axios.post('/api/v1/trading/create-trader', {
                    fund_id: fundId,
                    strategy: strategy,
                    symbols: ['data/mn1.csv'],
                    initial_capital: 100000.0
                });
                
                addLog(`Trader created: ${response.data.status}`);
            } catch (error) {
                addLog(`Error creating trader: ${error.message}`);
            }
        }

        async function startTrading() {
            const fundId = document.getElementById('fund-id').value;
            
            addLog(`Starting trading for fund ${fundId}...`);
            
            try {
                const response = await axios.post(`/api/v1/trading/start/${fundId}`);
                addLog(`Trading started: ${response.data.status}`);
            } catch (error) {
                addLog(`Error starting trading: ${error.message}`);
            }
        }

        async function stopTrading() {
            const fundId = document.getElementById('fund-id').value;
            
            addLog(`Stopping trading for fund ${fundId}...`);
            
            try {
                const response = await axios.post(`/api/v1/trading/stop/${fundId}`);
                addLog(`Trading stopped: ${response.data.status}`);
            } catch (error) {
                addLog(`Error stopping trading: ${error.message}`);
            }
        }

        async function runBacktest() {
            const symbols = document.getElementById('backtest-symbols').value.split(',');
            const strategy = document.getElementById('backtest-strategy').value;
            const startDate = document.getElementById('start-date').value;
            const endDate = document.getElementById('end-date').value;
            
            addLog(`Running backtest for ${symbols.join(', ')}...`);
            
            try {
                const response = await axios.post('/api/v1/backtest/run', {
                    symbols: symbols,
                    strategy: strategy,
                    model_type: 'ensemble',
                    start_date: startDate + 'T00:00:00Z',
                    end_date: endDate + 'T23:59:59Z',
                    initial_capital: 100000.0,
                    mode: 'walk_forward'
                });
                
                const result = response.data.backtest_result;
                addLog(`Backtest completed: ${(result.total_return * 100).toFixed(2)}% return`);
                
                // Update performance metrics
                document.getElementById('total-return').textContent = `${(result.total_return * 100).toFixed(2)}%`;
                document.getElementById('sharpe-ratio').textContent = result.sharpe_ratio.toFixed(2);
                document.getElementById('max-drawdown').textContent = `${(result.max_drawdown * 100).toFixed(2)}%`;
                document.getElementById('win-rate').textContent = `${(result.win_rate * 100).toFixed(2)}%`;
                
                // Update chart
                updateChart(result.equity_curve);
                
            } catch (error) {
                addLog(`Error running backtest: ${error.message}`);
            }
        }

        function updateChart(equityCurve) {
            if (!equityCurve || equityCurve.length === 0) return;
            
            const labels = equityCurve.map(point => new Date(point.timestamp).toLocaleDateString());
            const data = equityCurve.map(point => point.capital);
            
            performanceChart.data.labels = labels;
            performanceChart.data.datasets[0].data = data;
            performanceChart.update();
        }

        async function refreshMetrics() {
            addLog('Refreshing performance metrics...');
            // This would typically fetch from a specific fund
            // For now, we'll just log the action
        }
    </script>
</body>
</html>
"""

# API Endpoints

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the ML Dashboard."""
    return DASHBOARD_HTML

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

@app.post("/api/v1/ml/train-models")
async def train_ml_models(request: Dict[str, Any]):
    """Train machine learning models."""
    try:
        symbols = request.get('symbols', [])
        model_type = request.get('model_type', 'ensemble')
        
        logger.info(f"Training ML models for symbols: {symbols}")
        
        training_results = {}
        
        for symbol in symbols:
            try:
                # Create or get predictor
                if symbol not in price_predictors:
                    predictor = PricePredictor(model_type=model_type)
                    price_predictors[symbol] = predictor
                else:
                    predictor = price_predictors[symbol]
                
                # Get data for training
                if symbol.startswith('data/'):
                    data = await data_manager.get_local_data(f"../../{symbol}")
                else:
                    data = await data_manager.get_yahoo_data(symbol, period="365d")
                
                if data.empty:
                    training_results[symbol] = {
                        'status': 'error',
                        'message': f'No data available for {symbol}'
                    }
                    continue
                
                # Train models
                result = await predictor.train_models(data)
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
async def make_prediction(request: Dict[str, Any]):
    """Make price prediction."""
    try:
        symbol = request.get('symbol', '')
        model_name = request.get('model_name')
        
        logger.info(f"Making prediction for {symbol}")
        
        # Get predictor
        if symbol not in price_predictors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No trained models found for {symbol}"
            )
        
        predictor = price_predictors[symbol]
        
        # Get latest data
        if symbol.startswith('data/'):
            data = await data_manager.get_local_data(f"../../{symbol}")
        else:
            data = await data_manager.get_yahoo_data(symbol, period="30d")
        
        if data.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data available for {symbol}"
            )
        
        # Make prediction
        prediction_result = await predictor.predict(data, model_name)
        
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

@app.post("/api/v1/trading/create-trader")
async def create_automated_trader(request: Dict[str, Any]):
    """Create an automated trading system."""
    try:
        fund_id = request.get('fund_id', '')
        strategy = request.get('strategy', 'combined')
        symbols = request.get('symbols', [])
        initial_capital = request.get('initial_capital', 100000.0)
        
        logger.info(f"Creating automated trader for fund {fund_id}")
        
        # Validate strategy
        try:
            strategy_enum = TradingStrategy(strategy)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid strategy: {strategy}"
            )
        
        # Create portfolio manager
        if fund_id not in portfolio_managers:
            portfolio_manager = PortfolioManager(fund_id, initial_capital)
            portfolio_managers[fund_id] = portfolio_manager
        
        # Create automated trader
        trader = AutomatedTrader(fund_id, strategy_enum)
        automated_traders[fund_id] = trader
        
        # Initialize trader
        init_result = await trader.initialize()
        
        return {
            'status': 'success',
            'message': 'Automated trader created successfully',
            'fund_id': fund_id,
            'strategy': strategy,
            'symbols': symbols,
            'initial_capital': initial_capital,
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

@app.post("/api/v1/backtest/run")
async def run_backtest(request: Dict[str, Any]):
    """Run comprehensive backtest."""
    try:
        symbols = request.get('symbols', [])
        strategy = request.get('strategy', 'combined')
        model_type = request.get('model_type', 'ensemble')
        start_date = request.get('start_date', '')
        end_date = request.get('end_date', '')
        initial_capital = request.get('initial_capital', 100000.0)
        mode = request.get('mode', 'walk_forward')
        
        logger.info(f"Starting backtest for symbols: {symbols}")
        
        # Parse dates
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Validate strategy
        try:
            strategy_enum = TradingStrategy(strategy)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid strategy: {strategy}"
            )
        
        # Validate mode
        try:
            mode_enum = BacktestMode(mode)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid mode: {mode}"
            )
        
        # Create backtest config
        config = BacktestConfig(
            start_date=start_dt,
            end_date=end_dt,
            initial_capital=initial_capital,
            mode=mode_enum
        )
        
        # Create and run backtest engine
        engine = BacktestEngine(config)
        result = await engine.run_backtest(symbols, strategy_enum, model_type)
        
        # Store result
        backtest_results[f"{symbols}_{strategy}_{mode}"] = result
        
        # Convert result to dict for JSON serialization
        result_dict = {
            'total_return': float(result.total_return) if not np.isnan(result.total_return) else 0.0,
            'annualized_return': float(result.annualized_return) if not np.isnan(result.annualized_return) else 0.0,
            'volatility': float(result.volatility) if not np.isnan(result.volatility) else 0.0,
            'sharpe_ratio': float(result.sharpe_ratio) if not np.isnan(result.sharpe_ratio) else 0.0,
            'max_drawdown': float(result.max_drawdown) if not np.isnan(result.max_drawdown) else 0.0,
            'win_rate': float(result.win_rate) if not np.isnan(result.win_rate) else 0.0,
            'total_trades': int(result.total_trades),
            'winning_trades': int(result.winning_trades),
            'losing_trades': int(result.losing_trades),
            'avg_win': float(result.avg_win) if not np.isnan(result.avg_win) else 0.0,
            'avg_loss': float(result.avg_loss) if not np.isnan(result.avg_loss) else 0.0,
            'profit_factor': float(result.profit_factor) if not np.isnan(result.profit_factor) else 0.0,
            'calmar_ratio': float(result.calmar_ratio) if not np.isnan(result.calmar_ratio) else 0.0,
            'sortino_ratio': float(result.sortino_ratio) if not np.isnan(result.sortino_ratio) else 0.0,
            'trades': result.trades,
            'equity_curve': result.equity_curve.to_dict('records') if not result.equity_curve.empty else [],
            'performance_metrics': result.performance_metrics
        }
        
        return {
            'status': 'success',
            'backtest_result': result_dict,
            'config': {
                'symbols': symbols,
                'strategy': strategy,
                'model_type': model_type,
                'start_date': start_date,
                'end_date': end_date,
                'initial_capital': initial_capital,
                'mode': mode
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

if __name__ == "__main__":
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    # Run the application
    uvicorn.run(
        "ml_dashboard:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        log_level="info"
    )
