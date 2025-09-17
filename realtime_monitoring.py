#!/usr/bin/env python3
"""
Real-time Monitoring System for Pocket Hedge Fund.

This module provides real-time monitoring, alerting, and WebSocket
communication for the ML trading system.
"""

import asyncio
import logging
import sys
import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import uuid

# Add src to path
sys.path.append('src')

from fastapi import FastAPI, HTTPException, status, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import pandas as pd

# Import our ML modules
from pocket_hedge_fund.ml.price_predictor import PricePredictor
from pocket_hedge_fund.trading.automated_trader import AutomatedTrader, TradingStrategy
from pocket_hedge_fund.data.data_manager import DataManager
from pocket_hedge_fund.analysis.indicator_integration_simple import IndicatorIntegration
from pocket_hedge_fund.portfolio.portfolio_manager import PortfolioManager
from pocket_hedge_fund.backtesting.backtest_engine import BacktestEngine, BacktestConfig, BacktestMode
from pocket_hedge_fund.analytics.performance_analyzer import PerformanceAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Data classes for monitoring
@dataclass
class SystemAlert:
    """System alert data structure."""
    id: str
    type: str  # 'error', 'warning', 'info', 'success'
    title: str
    message: str
    timestamp: datetime
    source: str
    severity: int  # 1-5 (1=low, 5=critical)
    resolved: bool = False

@dataclass
class PerformanceUpdate:
    """Performance update data structure."""
    timestamp: datetime
    fund_id: str
    total_return: float
    daily_return: float
    portfolio_value: float
    active_positions: int
    sharpe_ratio: float
    max_drawdown: float

@dataclass
class TradingSignal:
    """Trading signal data structure."""
    timestamp: datetime
    symbol: str
    signal_type: str  # 'buy', 'sell', 'hold'
    confidence: float
    price: float
    quantity: float
    strategy: str

@dataclass
class SystemStatus:
    """System status data structure."""
    timestamp: datetime
    api_status: str
    ml_models: int
    active_traders: int
    portfolios: int
    total_trades: int
    system_load: float
    memory_usage: float
    cpu_usage: float

class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.subscriptions: Dict[WebSocket, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, subscriptions: List[str] = None):
        """Accept a WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.subscriptions[websocket] = set(subscriptions or [])
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.subscriptions:
            del self.subscriptions[websocket]
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: str, subscription_type: str = None):
        """Broadcast a message to all connected WebSockets."""
        if not self.active_connections:
            return
        
        disconnected = []
        for websocket in self.active_connections:
            try:
                # Check if client is subscribed to this type
                if subscription_type and websocket in self.subscriptions:
                    if subscription_type not in self.subscriptions[websocket]:
                        continue
                
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                disconnected.append(websocket)
        
        # Remove disconnected connections
        for websocket in disconnected:
            self.disconnect(websocket)

class AlertManager:
    """Manages system alerts and notifications."""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.alerts: List[SystemAlert] = []
        self.alert_thresholds = {
            'error': 5,
            'warning': 3,
            'info': 1
        }
    
    async def create_alert(self, alert_type: str, title: str, message: str, 
                          source: str, severity: int = 1):
        """Create and broadcast a new alert."""
        alert = SystemAlert(
            id=str(uuid.uuid4()),
            type=alert_type,
            title=title,
            message=message,
            timestamp=datetime.now(),
            source=source,
            severity=severity
        )
        
        self.alerts.append(alert)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
        
        # Broadcast alert
        alert_data = {
            'type': 'alert',
            'data': asdict(alert)
        }
        await self.connection_manager.broadcast(
            json.dumps(alert_data, default=str),
            'alerts'
        )
        
        logger.info(f"Alert created: {alert_type} - {title}")
    
    async def resolve_alert(self, alert_id: str):
        """Resolve an alert."""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                
                # Broadcast resolution
                resolution_data = {
                    'type': 'alert_resolved',
                    'data': {'id': alert_id}
                }
                await self.connection_manager.broadcast(
                    json.dumps(resolution_data),
                    'alerts'
                )
                break
    
    def get_active_alerts(self) -> List[SystemAlert]:
        """Get all active (unresolved) alerts."""
        return [alert for alert in self.alerts if not alert.resolved]

class PerformanceMonitor:
    """Monitors system performance and trading metrics."""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.performance_history: List[PerformanceUpdate] = []
        self.trading_signals: List[TradingSignal] = []
        self.system_status_history: List[SystemStatus] = []
    
    async def update_performance(self, fund_id: str, portfolio_manager: PortfolioManager):
        """Update and broadcast performance metrics."""
        try:
            # Get portfolio summary
            summary = await portfolio_manager.get_portfolio_summary()
            
            # Calculate performance metrics
            total_return = (summary['total_value'] - summary['initial_capital']) / summary['initial_capital']
            daily_return = 0.0  # Would need historical data to calculate
            
            performance_update = PerformanceUpdate(
                timestamp=datetime.now(),
                fund_id=fund_id,
                total_return=total_return,
                daily_return=daily_return,
                portfolio_value=summary['total_value'],
                active_positions=len(summary['positions']),
                sharpe_ratio=0.0,  # Would need historical data
                max_drawdown=0.0   # Would need historical data
            )
            
            self.performance_history.append(performance_update)
            
            # Keep only last 1000 updates
            if len(self.performance_history) > 1000:
                self.performance_history = self.performance_history[-1000:]
            
            # Broadcast performance update
            performance_data = {
                'type': 'performance_update',
                'data': asdict(performance_update)
            }
            await self.connection_manager.broadcast(
                json.dumps(performance_data, default=str),
                'performance'
            )
            
        except Exception as e:
            logger.error(f"Error updating performance: {e}")
    
    async def add_trading_signal(self, symbol: str, signal_type: str, 
                               confidence: float, price: float, 
                               quantity: float, strategy: str):
        """Add and broadcast a trading signal."""
        signal = TradingSignal(
            timestamp=datetime.now(),
            symbol=symbol,
            signal_type=signal_type,
            confidence=confidence,
            price=price,
            quantity=quantity,
            strategy=strategy
        )
        
        self.trading_signals.append(signal)
        
        # Keep only last 1000 signals
        if len(self.trading_signals) > 1000:
            self.trading_signals = self.trading_signals[-1000:]
        
        # Broadcast trading signal
        signal_data = {
            'type': 'trading_signal',
            'data': asdict(signal)
        }
        await self.connection_manager.broadcast(
            json.dumps(signal_data, default=str),
            'trading'
        )
    
    async def update_system_status(self, ml_models: int, active_traders: int, 
                                 portfolios: int, total_trades: int):
        """Update and broadcast system status."""
        status = SystemStatus(
            timestamp=datetime.now(),
            api_status='running',
            ml_models=ml_models,
            active_traders=active_traders,
            portfolios=portfolios,
            total_trades=total_trades,
            system_load=0.0,  # Would need system monitoring
            memory_usage=0.0,  # Would need system monitoring
            cpu_usage=0.0     # Would need system monitoring
        )
        
        self.system_status_history.append(status)
        
        # Keep only last 1000 status updates
        if len(self.system_status_history) > 1000:
            self.system_status_history = self.system_status_history[-1000:]
        
        # Broadcast system status
        status_data = {
            'type': 'system_status',
            'data': asdict(status)
        }
        await self.connection_manager.broadcast(
            json.dumps(status_data, default=str),
            'status'
        )

# Create FastAPI app
app = FastAPI(
    title="Pocket Hedge Fund Real-time Monitoring",
    description="Real-time monitoring and alerting system",
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
connection_manager = ConnectionManager()
alert_manager = AlertManager(connection_manager)
performance_monitor = PerformanceMonitor(connection_manager)

# Global system state
data_manager = DataManager()
price_predictors = {}
automated_traders = {}
portfolio_managers = {}

# Monitoring HTML
MONITORING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real-time Monitoring - Pocket Hedge Fund</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1400px;
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
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-connected { background-color: #28a745; }
        .status-disconnected { background-color: #dc3545; }
        .alert {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 4px solid;
        }
        .alert-error { background-color: #f8d7da; border-color: #dc3545; }
        .alert-warning { background-color: #fff3cd; border-color: #ffc107; }
        .alert-info { background-color: #d1ecf1; border-color: #17a2b8; }
        .alert-success { background-color: #d4edda; border-color: #28a745; }
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
        .subscription-controls {
            margin: 10px 0;
        }
        .subscription-controls label {
            margin-right: 15px;
        }
        .subscription-controls input[type="checkbox"] {
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔴 Real-time Monitoring - Pocket Hedge Fund</h1>
            <p>Live System Monitoring and Alerting</p>
            <div>
                <span class="status-indicator" id="connection-status"></span>
                <span id="connection-text">Connecting...</span>
            </div>
        </div>

        <div class="grid">
            <!-- Connection Status -->
            <div class="card">
                <h3>📡 Connection Status</h3>
                <div class="metric">
                    <span>WebSocket Status:</span>
                    <span class="metric-value" id="ws-status">Disconnected</span>
                </div>
                <div class="metric">
                    <span>Active Connections:</span>
                    <span class="metric-value" id="active-connections">0</span>
                </div>
                <div class="metric">
                    <span>Last Update:</span>
                    <span class="metric-value" id="last-update">Never</span>
                </div>
                <div class="subscription-controls">
                    <h4>Subscriptions:</h4>
                    <label><input type="checkbox" id="sub-alerts" checked> Alerts</label>
                    <label><input type="checkbox" id="sub-performance" checked> Performance</label>
                    <label><input type="checkbox" id="sub-trading" checked> Trading</label>
                    <label><input type="checkbox" id="sub-status" checked> Status</label>
                </div>
            </div>

            <!-- System Status -->
            <div class="card">
                <h3>📊 System Status</h3>
                <div class="metric">
                    <span>API Status:</span>
                    <span class="metric-value" id="api-status">Unknown</span>
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
                <div class="metric">
                    <span>Total Trades:</span>
                    <span class="metric-value" id="total-trades">0</span>
                </div>
            </div>

            <!-- Performance Metrics -->
            <div class="card">
                <h3>📈 Performance Metrics</h3>
                <div class="metric">
                    <span>Total Return:</span>
                    <span class="metric-value" id="total-return">0%</span>
                </div>
                <div class="metric">
                    <span>Daily Return:</span>
                    <span class="metric-value" id="daily-return">0%</span>
                </div>
                <div class="metric">
                    <span>Portfolio Value:</span>
                    <span class="metric-value" id="portfolio-value">$0</span>
                </div>
                <div class="metric">
                    <span>Active Positions:</span>
                    <span class="metric-value" id="active-positions">0</span>
                </div>
                <div class="metric">
                    <span>Sharpe Ratio:</span>
                    <span class="metric-value" id="sharpe-ratio">0.00</span>
                </div>
            </div>

            <!-- Active Alerts -->
            <div class="card">
                <h3>🚨 Active Alerts</h3>
                <div id="alerts-container">
                    <div class="alert alert-info">No active alerts</div>
                </div>
            </div>

            <!-- Trading Signals -->
            <div class="card">
                <h3>⚡ Trading Signals</h3>
                <div id="signals-container">
                    <div class="alert alert-info">No recent signals</div>
                </div>
            </div>

            <!-- Real-time Logs -->
            <div class="card">
                <h3>📝 Real-time Logs</h3>
                <div class="log" id="logs">
                    <div>System initialized...</div>
                </div>
            </div>
        </div>

        <!-- Performance Chart -->
        <div class="card">
            <h3>📈 Performance Chart</h3>
            <div class="chart-container">
                <canvas id="performanceChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        let ws;
        let performanceChart;
        let logs = [];
        let performanceData = [];

        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            initializeChart();
            connectWebSocket();
            setupSubscriptionControls();
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

        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            ws = new WebSocket(wsUrl);
            
            ws.onopen = function(event) {
                updateConnectionStatus(true);
                addLog('WebSocket connected');
                
                // Send subscription preferences
                sendSubscriptions();
            };
            
            ws.onmessage = function(event) {
                try {
                    const message = JSON.parse(event.data);
                    handleMessage(message);
                } catch (e) {
                    addLog(`Error parsing message: ${e.message}`);
                }
            };
            
            ws.onclose = function(event) {
                updateConnectionStatus(false);
                addLog('WebSocket disconnected');
                
                // Reconnect after 5 seconds
                setTimeout(connectWebSocket, 5000);
            };
            
            ws.onerror = function(error) {
                addLog(`WebSocket error: ${error}`);
            };
        }

        function updateConnectionStatus(connected) {
            const statusIndicator = document.getElementById('connection-status');
            const statusText = document.getElementById('connection-text');
            const wsStatus = document.getElementById('ws-status');
            
            if (connected) {
                statusIndicator.className = 'status-indicator status-connected';
                statusText.textContent = 'Connected';
                wsStatus.textContent = 'Connected';
            } else {
                statusIndicator.className = 'status-indicator status-disconnected';
                statusText.textContent = 'Disconnected';
                wsStatus.textContent = 'Disconnected';
            }
        }

        function handleMessage(message) {
            const timestamp = new Date().toLocaleTimeString();
            document.getElementById('last-update').textContent = timestamp;
            
            switch (message.type) {
                case 'alert':
                    handleAlert(message.data);
                    break;
                case 'alert_resolved':
                    handleAlertResolved(message.data.id);
                    break;
                case 'performance_update':
                    handlePerformanceUpdate(message.data);
                    break;
                case 'trading_signal':
                    handleTradingSignal(message.data);
                    break;
                case 'system_status':
                    handleSystemStatus(message.data);
                    break;
                default:
                    addLog(`Unknown message type: ${message.type}`);
            }
        }

        function handleAlert(alert) {
            const container = document.getElementById('alerts-container');
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${alert.type}`;
            alertDiv.innerHTML = `
                <strong>${alert.title}</strong><br>
                ${alert.message}<br>
                <small>${new Date(alert.timestamp).toLocaleString()}</small>
            `;
            alertDiv.id = `alert-${alert.id}`;
            
            // Add to top of container
            if (container.firstChild && container.firstChild.className.includes('alert-info')) {
                container.removeChild(container.firstChild);
            }
            container.insertBefore(alertDiv, container.firstChild);
            
            addLog(`Alert: ${alert.title} - ${alert.message}`);
        }

        function handleAlertResolved(alertId) {
            const alertElement = document.getElementById(`alert-${alertId}`);
            if (alertElement) {
                alertElement.remove();
            }
        }

        function handlePerformanceUpdate(data) {
            document.getElementById('total-return').textContent = `${(data.total_return * 100).toFixed(2)}%`;
            document.getElementById('daily-return').textContent = `${(data.daily_return * 100).toFixed(2)}%`;
            document.getElementById('portfolio-value').textContent = `$${data.portfolio_value.toLocaleString()}`;
            document.getElementById('active-positions').textContent = data.active_positions;
            document.getElementById('sharpe-ratio').textContent = data.sharpe_ratio.toFixed(2);
            
            // Update chart
            performanceData.push({
                timestamp: new Date(data.timestamp),
                value: data.portfolio_value
            });
            
            if (performanceData.length > 100) {
                performanceData = performanceData.slice(-100);
            }
            
            const labels = performanceData.map(d => d.timestamp.toLocaleTimeString());
            const values = performanceData.map(d => d.value);
            
            performanceChart.data.labels = labels;
            performanceChart.data.datasets[0].data = values;
            performanceChart.update();
        }

        function handleTradingSignal(data) {
            const container = document.getElementById('signals-container');
            const signalDiv = document.createElement('div');
            signalDiv.className = `alert alert-${data.signal_type === 'buy' ? 'success' : data.signal_type === 'sell' ? 'warning' : 'info'}`;
            signalDiv.innerHTML = `
                <strong>${data.signal_type.toUpperCase()}</strong> ${data.symbol}<br>
                Price: $${data.price.toFixed(2)} | Quantity: ${data.quantity}<br>
                Confidence: ${(data.confidence * 100).toFixed(1)}% | Strategy: ${data.strategy}<br>
                <small>${new Date(data.timestamp).toLocaleString()}</small>
            `;
            
            // Add to top of container
            if (container.firstChild && container.firstChild.className.includes('alert-info')) {
                container.removeChild(container.firstChild);
            }
            container.insertBefore(signalDiv, container.firstChild);
            
            addLog(`Trading Signal: ${data.signal_type.toUpperCase()} ${data.symbol} at $${data.price}`);
        }

        function handleSystemStatus(data) {
            document.getElementById('api-status').textContent = data.api_status;
            document.getElementById('ml-models').textContent = data.ml_models;
            document.getElementById('active-traders').textContent = data.active_traders;
            document.getElementById('portfolios').textContent = data.portfolios;
            document.getElementById('total-trades').textContent = data.total_trades;
        }

        function setupSubscriptionControls() {
            const checkboxes = document.querySelectorAll('.subscription-controls input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', sendSubscriptions);
            });
        }

        function sendSubscriptions() {
            if (!ws || ws.readyState !== WebSocket.OPEN) return;
            
            const subscriptions = [];
            if (document.getElementById('sub-alerts').checked) subscriptions.push('alerts');
            if (document.getElementById('sub-performance').checked) subscriptions.push('performance');
            if (document.getElementById('sub-trading').checked) subscriptions.push('trading');
            if (document.getElementById('sub-status').checked) subscriptions.push('status');
            
            ws.send(JSON.stringify({
                type: 'subscribe',
                subscriptions: subscriptions
            }));
        }

        function addLog(message) {
            const timestamp = new Date().toLocaleTimeString();
            logs.push(`[${timestamp}] ${message}`);
            if (logs.length > 100) logs.shift();
            
            const logElement = document.getElementById('logs');
            logElement.innerHTML = logs.map(log => `<div>${log}</div>`).join('');
            logElement.scrollTop = logElement.scrollHeight;
        }
    </script>
</body>
</html>
"""

# API Endpoints

@app.get("/", response_class=HTMLResponse)
async def monitoring_dashboard():
    """Serve the real-time monitoring dashboard."""
    return MONITORING_HTML

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    await connection_manager.connect(websocket)
    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get('type') == 'subscribe':
                    # Update subscriptions
                    subscriptions = message.get('subscriptions', [])
                    connection_manager.subscriptions[websocket] = set(subscriptions)
                    logger.info(f"Updated subscriptions: {subscriptions}")
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received: {data}")
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

@app.get("/api/v1/monitoring/status")
async def get_monitoring_status():
    """Get current monitoring system status."""
    return {
        'active_connections': len(connection_manager.active_connections),
        'active_alerts': len(alert_manager.get_active_alerts()),
        'performance_updates': len(performance_monitor.performance_history),
        'trading_signals': len(performance_monitor.trading_signals),
        'system_status_updates': len(performance_monitor.system_status_history),
        'timestamp': datetime.now().isoformat()
    }

@app.get("/api/v1/monitoring/alerts")
async def get_alerts():
    """Get all alerts."""
    return {
        'alerts': [asdict(alert) for alert in alert_manager.alerts],
        'active_alerts': [asdict(alert) for alert in alert_manager.get_active_alerts()],
        'timestamp': datetime.now().isoformat()
    }

@app.post("/api/v1/monitoring/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    """Resolve an alert."""
    await alert_manager.resolve_alert(alert_id)
    return {"status": "success", "message": f"Alert {alert_id} resolved"}

@app.get("/api/v1/monitoring/performance")
async def get_performance_history():
    """Get performance history."""
    return {
        'performance_history': [asdict(update) for update in performance_monitor.performance_history[-100:]],
        'timestamp': datetime.now().isoformat()
    }

@app.get("/api/v1/monitoring/signals")
async def get_trading_signals():
    """Get trading signals history."""
    return {
        'trading_signals': [asdict(signal) for signal in performance_monitor.trading_signals[-100:]],
        'timestamp': datetime.now().isoformat()
    }

# Background monitoring tasks
async def background_monitoring():
    """Background task for continuous monitoring."""
    while True:
        try:
            # Update system status
            await performance_monitor.update_system_status(
                ml_models=len(price_predictors),
                active_traders=len(automated_traders),
                portfolios=len(portfolio_managers),
                total_trades=0  # Would need to track this
            )
            
            # Update performance for each portfolio
            for fund_id, portfolio_manager in portfolio_managers.items():
                await performance_monitor.update_performance(fund_id, portfolio_manager)
            
            # Wait 5 seconds before next update
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"Error in background monitoring: {e}")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    """Start background monitoring tasks."""
    asyncio.create_task(background_monitoring())
    logger.info("Real-time monitoring system started")

if __name__ == "__main__":
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    # Run the application
    uvicorn.run(
        "realtime_monitoring:app",
        host="127.0.0.1",
        port=8002,
        reload=True,
        log_level="info"
    )
