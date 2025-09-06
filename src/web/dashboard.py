# -*- coding: utf-8 -*-
"""
Web Dashboard for NeoZork Interactive ML Trading Strategy Development.

This module provides a web interface for monitoring trading system performance.
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging
import threading
import queue
import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import our trading system components
from src.data.real_exchange_apis import ExchangeAPIManager, ExchangeType, APIKey
from src.ml.real_ml_models import RealMLModels, ModelType
from src.integration.real_trading_system import RealTradingSystem, TradingConfig, TradingMode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = 'neozork_trading_dashboard_secret_key'

# Global variables for trading system
trading_system = None
api_manager = None
ml_models = None
dashboard_data = {
    'portfolio': {},
    'signals': [],
    'performance': {},
    'models': {},
    'exchanges': {}
}

# Data update queue
data_queue = queue.Queue()

class DashboardManager:
    """Manager for dashboard data and updates."""
    
    def __init__(self):
        self.is_running = False
        self.update_thread = None
        self.last_update = datetime.now()
        
    def start(self):
        """Start dashboard data updates."""
        if not self.is_running:
            self.is_running = True
            self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
            self.update_thread.start()
            logger.info("Dashboard manager started")
    
    def stop(self):
        """Stop dashboard data updates."""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=5)
        logger.info("Dashboard manager stopped")
    
    def _update_loop(self):
        """Main update loop for dashboard data."""
        while self.is_running:
            try:
                self._update_dashboard_data()
                time.sleep(10)  # Update every 10 seconds
            except Exception as e:
                logger.error(f"Dashboard update error: {e}")
                time.sleep(30)  # Wait longer on error
    
    def _update_dashboard_data(self):
        """Update dashboard data from trading system."""
        global dashboard_data, trading_system, api_manager, ml_models
        
        try:
            # Update portfolio data
            if trading_system:
                portfolio_result = trading_system.get_portfolio_status()
                if portfolio_result['status'] == 'success':
                    dashboard_data['portfolio'] = portfolio_result['portfolio']
                    
                    # Update performance metrics
                    dashboard_data['performance'] = {
                        'total_return': portfolio_result['portfolio']['total_return_pct'],
                        'portfolio_value': portfolio_result['portfolio']['total_value'],
                        'cash': portfolio_result['portfolio']['cash'],
                        'positions_count': portfolio_result['portfolio']['positions_count'],
                        'unrealized_pnl': portfolio_result['portfolio']['unrealized_pnl'],
                        'last_update': datetime.now().isoformat()
                    }
            
            # Update exchange status
            if api_manager:
                status = api_manager.get_connection_status()
                dashboard_data['exchanges'] = status
            
            # Update model information
            if ml_models:
                model_info = ml_models.get_model_info()
                if model_info['status'] == 'success':
                    dashboard_data['models'] = model_info['models']
            
            # Update signals (keep last 50)
            if trading_system and hasattr(trading_system, 'signals_history'):
                recent_signals = trading_system.signals_history[-50:]
                dashboard_data['signals'] = [
                    {
                        'symbol': signal.symbol,
                        'signal_type': signal.signal_type.value,
                        'confidence': signal.confidence,
                        'price': signal.price,
                        'timestamp': signal.timestamp.isoformat(),
                        'model_name': signal.model_name
                    }
                    for signal in recent_signals
                ]
            
            self.last_update = datetime.now()
            
        except Exception as e:
            logger.error(f"Error updating dashboard data: {e}")

# Initialize dashboard manager
dashboard_manager = DashboardManager()

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html')

@app.route('/api/portfolio')
def api_portfolio():
    """Get portfolio data."""
    return jsonify(dashboard_data['portfolio'])

@app.route('/api/performance')
def api_performance():
    """Get performance data."""
    return jsonify(dashboard_data['performance'])

@app.route('/api/signals')
def api_signals():
    """Get trading signals."""
    return jsonify(dashboard_data['signals'])

@app.route('/api/models')
def api_models():
    """Get model information."""
    return jsonify(dashboard_data['models'])

@app.route('/api/exchanges')
def api_exchanges():
    """Get exchange status."""
    return jsonify(dashboard_data['exchanges'])

@app.route('/api/status')
def api_status():
    """Get overall system status."""
    return jsonify({
        'status': 'running',
        'last_update': dashboard_manager.last_update.isoformat(),
        'trading_system': trading_system is not None,
        'api_manager': api_manager is not None,
        'ml_models': ml_models is not None
    })

@app.route('/api/generate_signal', methods=['POST'])
def api_generate_signal():
    """Generate a new trading signal."""
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'BTCUSDT')
        
        if trading_system:
            result = trading_system.generate_signal(symbol)
            return jsonify(result)
        else:
            return jsonify({
                'status': 'error',
                'message': 'Trading system not initialized'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Signal generation failed: {str(e)}'
        })

@app.route('/api/train_model', methods=['POST'])
def api_train_model():
    """Train a new ML model."""
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'BTCUSDT')
        model_type = data.get('model_type', 'random_forest_regressor')
        
        if trading_system:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            # Map model type
            model_type_map = {
                'linear_regression': ModelType.LINEAR_REGRESSION,
                'random_forest_regressor': ModelType.RANDOM_FOREST_REGRESSOR,
                'gradient_boosting': ModelType.GRADIENT_BOOSTING
            }
            
            ml_model_type = model_type_map.get(model_type, ModelType.RANDOM_FOREST_REGRESSOR)
            
            result = trading_system.train_model(symbol, ml_model_type, start_date, end_date)
            return jsonify(result)
        else:
            return jsonify({
                'status': 'error',
                'message': 'Trading system not initialized'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Model training failed: {str(e)}'
        })

@app.route('/api/start_trading', methods=['POST'])
def api_start_trading():
    """Start trading system."""
    try:
        if trading_system:
            result = trading_system.start_trading()
            return jsonify(result)
        else:
            return jsonify({
                'status': 'error',
                'message': 'Trading system not initialized'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to start trading: {str(e)}'
        })

@app.route('/api/stop_trading', methods=['POST'])
def api_stop_trading():
    """Stop trading system."""
    try:
        if trading_system:
            result = trading_system.stop_trading()
            return jsonify(result)
        else:
            return jsonify({
                'status': 'error',
                'message': 'Trading system not initialized'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to stop trading: {str(e)}'
        })

def initialize_trading_system():
    """Initialize the trading system for dashboard."""
    global trading_system, api_manager, ml_models
    
    try:
        # Create API manager
        api_manager = ExchangeAPIManager()
        
        # Add exchanges with demo keys
        binance_key = APIKey(
            api_key="demo_binance_api_key",
            secret_key="demo_binance_secret_key",
            sandbox=True
        )
        
        bybit_key = APIKey(
            api_key="demo_bybit_api_key",
            secret_key="demo_bybit_secret_key",
            sandbox=True
        )
        
        # Add exchanges
        api_manager.add_exchange(ExchangeType.BINANCE, binance_key)
        api_manager.add_exchange(ExchangeType.BYBIT, bybit_key)
        
        # Create ML models
        ml_models = RealMLModels()
        
        # Create trading system
        config = TradingConfig(
            symbol="BTCUSDT",
            model_name="dashboard_model",
            trading_mode=TradingMode.PAPER,
            position_size=0.1,
            stop_loss_pct=0.05,
            take_profit_pct=0.1,
            max_positions=3,
            min_confidence=0.6
        )
        
        trading_system = RealTradingSystem(config)
        
        # Initialize trading system
        api_keys = {
            ExchangeType.BINANCE: binance_key,
            ExchangeType.BYBIT: bybit_key
        }
        
        init_result = trading_system.initialize(api_keys)
        
        if init_result['status'] == 'success':
            logger.info("Trading system initialized successfully for dashboard")
            
            # Train initial model
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            train_result = trading_system.train_model(
                "BTCUSDT", ModelType.RANDOM_FOREST_REGRESSOR, start_date, end_date
            )
            
            if train_result['status'] == 'success':
                logger.info(f"Initial model trained: {train_result['model_name']}")
            else:
                logger.warning(f"Initial model training failed: {train_result['message']}")
        else:
            logger.error(f"Trading system initialization failed: {init_result['message']}")
            
    except Exception as e:
        logger.error(f"Failed to initialize trading system: {e}")

def create_templates():
    """Create HTML templates for the dashboard."""
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Create dashboard.html
    dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeoZork Trading Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .dashboard-grid {
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
        .positive { color: #28a745; }
        .negative { color: #dc3545; }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .status-online { background-color: #28a745; }
        .status-offline { background-color: #dc3545; }
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        .btn:hover { background: #5a6fd8; }
        .btn-danger { background: #dc3545; }
        .btn-danger:hover { background: #c82333; }
        .btn-success { background: #28a745; }
        .btn-success:hover { background: #218838; }
        .signals-table {
            width: 100%;
            border-collapse: collapse;
        }
        .signals-table th, .signals-table td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .signals-table th {
            background-color: #f8f9fa;
        }
        .signal-buy { color: #28a745; font-weight: bold; }
        .signal-sell { color: #dc3545; font-weight: bold; }
        .signal-hold { color: #6c757d; font-weight: bold; }
        .last-update {
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 NeoZork Trading Dashboard</h1>
        <p>Real-time ML Trading Strategy Monitoring</p>
    </div>

    <div class="dashboard-grid">
        <!-- Portfolio Overview -->
        <div class="card">
            <h3>📊 Portfolio Overview</h3>
            <div class="metric">
                <span>Total Value:</span>
                <span class="metric-value" id="total-value">$0.00</span>
            </div>
            <div class="metric">
                <span>Cash:</span>
                <span class="metric-value" id="cash">$0.00</span>
            </div>
            <div class="metric">
                <span>Positions:</span>
                <span class="metric-value" id="positions">0</span>
            </div>
            <div class="metric">
                <span>Total Return:</span>
                <span class="metric-value" id="total-return">0.00%</span>
            </div>
            <div class="metric">
                <span>Unrealized P&L:</span>
                <span class="metric-value" id="unrealized-pnl">$0.00</span>
            </div>
        </div>

        <!-- System Status -->
        <div class="card">
            <h3>🔧 System Status</h3>
            <div class="metric">
                <span>Trading System:</span>
                <span><span class="status-indicator" id="trading-status"></span><span id="trading-text">Unknown</span></span>
            </div>
            <div class="metric">
                <span>API Manager:</span>
                <span><span class="status-indicator" id="api-status"></span><span id="api-text">Unknown</span></span>
            </div>
            <div class="metric">
                <span>ML Models:</span>
                <span><span class="status-indicator" id="ml-status"></span><span id="ml-text">Unknown</span></span>
            </div>
            <div class="metric">
                <span>Last Update:</span>
                <span class="metric-value" id="last-update">Never</span>
            </div>
        </div>

        <!-- Exchange Status -->
        <div class="card">
            <h3>🌐 Exchange Status</h3>
            <div id="exchange-status">
                <div class="metric">
                    <span>Loading...</span>
                </div>
            </div>
        </div>

        <!-- Model Information -->
        <div class="card">
            <h3>🤖 ML Models</h3>
            <div id="model-info">
                <div class="metric">
                    <span>Loading...</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Controls -->
    <div class="card">
        <h3>🎮 Trading Controls</h3>
        <button class="btn btn-success" onclick="startTrading()">Start Trading</button>
        <button class="btn btn-danger" onclick="stopTrading()">Stop Trading</button>
        <button class="btn" onclick="generateSignal()">Generate Signal</button>
        <button class="btn" onclick="trainModel()">Train Model</button>
    </div>

    <!-- Recent Signals -->
    <div class="card">
        <h3>📈 Recent Signals</h3>
        <table class="signals-table">
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Symbol</th>
                    <th>Signal</th>
                    <th>Price</th>
                    <th>Confidence</th>
                    <th>Model</th>
                </tr>
            </thead>
            <tbody id="signals-table-body">
                <tr>
                    <td colspan="6">No signals yet</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="last-update">
        <p>Last updated: <span id="last-update-time">Never</span></p>
    </div>

    <script>
        // Update dashboard data
        function updateDashboard() {
            // Update portfolio
            fetch('/api/portfolio')
                .then(response => response.json())
                .then(data => {
                    if (data.total_value) {
                        document.getElementById('total-value').textContent = '$' + data.total_value.toFixed(2);
                        document.getElementById('cash').textContent = '$' + data.cash.toFixed(2);
                        document.getElementById('positions').textContent = data.positions_count;
                        document.getElementById('total-return').textContent = data.total_return_pct.toFixed(2) + '%';
                        document.getElementById('unrealized-pnl').textContent = '$' + data.unrealized_pnl.toFixed(2);
                        
                        // Color code return
                        const returnElement = document.getElementById('total-return');
                        if (data.total_return_pct > 0) {
                            returnElement.className = 'metric-value positive';
                        } else if (data.total_return_pct < 0) {
                            returnElement.className = 'metric-value negative';
                        }
                    }
                });

            // Update system status
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('trading-status').className = 'status-indicator ' + (data.trading_system ? 'status-online' : 'status-offline');
                    document.getElementById('trading-text').textContent = data.trading_system ? 'Online' : 'Offline';
                    document.getElementById('api-status').className = 'status-indicator ' + (data.api_manager ? 'status-online' : 'status-offline');
                    document.getElementById('api-text').textContent = data.api_manager ? 'Online' : 'Offline';
                    document.getElementById('ml-status').className = 'status-indicator ' + (data.ml_models ? 'status-online' : 'status-offline');
                    document.getElementById('ml-text').textContent = data.ml_models ? 'Online' : 'Offline';
                    document.getElementById('last-update').textContent = new Date(data.last_update).toLocaleTimeString();
                    document.getElementById('last-update-time').textContent = new Date(data.last_update).toLocaleString();
                });

            // Update exchange status
            fetch('/api/exchanges')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('exchange-status');
                    container.innerHTML = '';
                    for (const [exchange, status] of Object.entries(data)) {
                        const div = document.createElement('div');
                        div.className = 'metric';
                        div.innerHTML = `
                            <span>${exchange.toUpperCase()}:</span>
                            <span><span class="status-indicator ${status.connected ? 'status-online' : 'status-offline'}"></span>${status.connected ? 'Connected' : 'Disconnected'}</span>
                        `;
                        container.appendChild(div);
                    }
                });

            // Update model info
            fetch('/api/models')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('model-info');
                    container.innerHTML = '';
                    if (data.models) {
                        for (const [modelName, modelInfo] of Object.entries(data.models)) {
                            const div = document.createElement('div');
                            div.className = 'metric';
                            div.innerHTML = `
                                <span>${modelName}:</span>
                                <span class="metric-value">${modelInfo.model_type}</span>
                            `;
                            container.appendChild(div);
                        }
                    } else {
                        container.innerHTML = '<div class="metric"><span>No models trained</span></div>';
                    }
                });

            // Update signals
            fetch('/api/signals')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.getElementById('signals-table-body');
                    if (data.length > 0) {
                        tbody.innerHTML = '';
                        data.slice(-10).reverse().forEach(signal => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${new Date(signal.timestamp).toLocaleTimeString()}</td>
                                <td>${signal.symbol}</td>
                                <td class="signal-${signal.signal_type}">${signal.signal_type.toUpperCase()}</td>
                                <td>$${signal.price.toFixed(4)}</td>
                                <td>${(signal.confidence * 100).toFixed(1)}%</td>
                                <td>${signal.model_name}</td>
                            `;
                            tbody.appendChild(row);
                        });
                    }
                });
        }

        // Control functions
        function startTrading() {
            fetch('/api/start_trading', {method: 'POST'})
                .then(response => response.json())
                .then(data => alert(data.message));
        }

        function stopTrading() {
            fetch('/api/stop_trading', {method: 'POST'})
                .then(response => response.json())
                .then(data => alert(data.message));
        }

        function generateSignal() {
            fetch('/api/generate_signal', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({symbol: 'BTCUSDT'})
            })
            .then(response => response.json())
            .then(data => alert(data.message));
        }

        function trainModel() {
            fetch('/api/train_model', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({symbol: 'BTCUSDT', model_type: 'random_forest_regressor'})
            })
            .then(response => response.json())
            .then(data => alert(data.message));
        }

        // Update dashboard every 5 seconds
        setInterval(updateDashboard, 5000);
        
        // Initial update
        updateDashboard();
    </script>
</body>
</html>'''
    
    with open(templates_dir / 'dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    logger.info("Dashboard templates created")

def run_dashboard(host='127.0.0.1', port=5000, debug=False):
    """Run the dashboard web server."""
    try:
        # Create templates
        create_templates()
        
        # Initialize trading system
        initialize_trading_system()
        
        # Start dashboard manager
        dashboard_manager.start()
        
        logger.info(f"Starting NeoZork Trading Dashboard on http://{host}:{port}")
        
        # Run Flask app
        app.run(host=host, port=port, debug=debug, use_reloader=False)
        
    except KeyboardInterrupt:
        logger.info("Dashboard stopped by user")
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
    finally:
        dashboard_manager.stop()

if __name__ == "__main__":
    run_dashboard(debug=True)
