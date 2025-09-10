# -*- coding: utf-8 -*-
"""
Order Management System for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive order management capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import warnings

class OrderStatus(Enum):
    """Order status enumeration."""
    PENDING = "PENDING"
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

class OrderType(Enum):
    """Order type enumeration."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"

class OrderSide(Enum):
    """Order side enumeration."""
    BUY = "BUY"
    SELL = "SELL"

class OrderManagementSystem:
    """
    Order Management System for trading operations.
    
    Features:
    - Order Creation and Management
    - Order Routing
    - Risk Management
    - Position Management
    - Portfolio Tracking
    - Performance Monitoring
    """
    
    def __init__(self):
        """Initialize the Order Management System."""
        self.orders = {}
        self.positions = {}
        self.portfolios = {}
        self.risk_limits = {}
        self.order_history = []
        self.performance_metrics = {}
    
    def create_order(self, symbol: str, side: str, order_type: str, 
                    quantity: float, price: float = None, 
                    stop_price: float = None, time_in_force: str = "GTC",
                    exchange: str = "binance") -> Dict[str, Any]:
        """
        Create a new order.
        
        Args:
            symbol: Trading symbol
            side: Order side (BUY, SELL)
            order_type: Order type (MARKET, LIMIT, STOP, etc.)
            quantity: Order quantity
            price: Order price (for LIMIT orders)
            stop_price: Stop price (for STOP orders)
            time_in_force: Time in force (GTC, IOC, FOK)
            exchange: Target exchange
            
        Returns:
            Order creation result
        """
        try:
            # Generate order ID
            order_id = f"order_{int(time.time() * 1000)}"
            
            # Validate order parameters
            validation_result = self._validate_order(symbol, side, order_type, quantity, price, stop_price)
            if validation_result["status"] != "success":
                return validation_result
            
            # Create order
            order = {
                "order_id": order_id,
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity,
                "price": price,
                "stop_price": stop_price,
                "time_in_force": time_in_force,
                "exchange": exchange,
                "status": OrderStatus.NEW.value,
                "created_time": time.time(),
                "updated_time": time.time(),
                "filled_quantity": 0.0,
                "remaining_quantity": quantity,
                "average_price": 0.0,
                "commission": 0.0,
                "commission_asset": "USDT"
            }
            
            # Store order
            self.orders[order_id] = order
            
            # Add to order history
            self.order_history.append(order.copy())
            
            result = {
                "status": "success",
                "order_id": order_id,
                "order": order,
                "message": "Order created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create order: {str(e)}"}
    
    def modify_order(self, order_id: str, quantity: float = None, 
                    price: float = None, stop_price: float = None) -> Dict[str, Any]:
        """
        Modify an existing order.
        
        Args:
            order_id: Order ID to modify
            quantity: New quantity
            price: New price
            stop_price: New stop price
            
        Returns:
            Order modification result
        """
        try:
            if order_id not in self.orders:
                return {"status": "error", "message": f"Order {order_id} not found"}
            
            order = self.orders[order_id]
            
            # Check if order can be modified
            if order["status"] not in [OrderStatus.NEW.value, OrderStatus.PENDING.value]:
                return {"status": "error", "message": f"Order {order_id} cannot be modified"}
            
            # Update order parameters
            if quantity is not None:
                order["quantity"] = quantity
                order["remaining_quantity"] = quantity - order["filled_quantity"]
            
            if price is not None:
                order["price"] = price
            
            if stop_price is not None:
                order["stop_price"] = stop_price
            
            order["updated_time"] = time.time()
            
            result = {
                "status": "success",
                "order_id": order_id,
                "order": order,
                "message": "Order modified successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to modify order: {str(e)}"}
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel an order.
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            Order cancellation result
        """
        try:
            if order_id not in self.orders:
                return {"status": "error", "message": f"Order {order_id} not found"}
            
            order = self.orders[order_id]
            
            # Check if order can be canceled
            if order["status"] in [OrderStatus.FILLED.value, OrderStatus.CANCELED.value, OrderStatus.REJECTED.value]:
                return {"status": "error", "message": f"Order {order_id} cannot be canceled"}
            
            # Update order status
            order["status"] = OrderStatus.CANCELED.value
            order["updated_time"] = time.time()
            
            result = {
                "status": "success",
                "order_id": order_id,
                "order": order,
                "message": "Order canceled successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to cancel order: {str(e)}"}
    
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """
        Get order status.
        
        Args:
            order_id: Order ID
            
        Returns:
            Order status
        """
        try:
            if order_id not in self.orders:
                return {"status": "error", "message": f"Order {order_id} not found"}
            
            order = self.orders[order_id]
            
            result = {
                "status": "success",
                "order": order
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get order status: {str(e)}"}
    
    def get_open_orders(self, symbol: str = None, exchange: str = None) -> Dict[str, Any]:
        """
        Get open orders.
        
        Args:
            symbol: Filter by symbol
            exchange: Filter by exchange
            
        Returns:
            Open orders
        """
        try:
            open_orders = []
            
            for order_id, order in self.orders.items():
                if order["status"] in [OrderStatus.NEW.value, OrderStatus.PENDING.value, OrderStatus.PARTIALLY_FILLED.value]:
                    if symbol is None or order["symbol"] == symbol:
                        if exchange is None or order["exchange"] == exchange:
                            open_orders.append(order)
            
            result = {
                "status": "success",
                "open_orders": open_orders,
                "n_orders": len(open_orders)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get open orders: {str(e)}"}
    
    def get_order_history(self, symbol: str = None, exchange: str = None, 
                         limit: int = 100) -> Dict[str, Any]:
        """
        Get order history.
        
        Args:
            symbol: Filter by symbol
            exchange: Filter by exchange
            limit: Maximum number of orders to return
            
        Returns:
            Order history
        """
        try:
            filtered_orders = []
            
            for order in self.order_history:
                if symbol is None or order["symbol"] == symbol:
                    if exchange is None or order["exchange"] == exchange:
                        filtered_orders.append(order)
            
            # Sort by creation time (newest first)
            filtered_orders.sort(key=lambda x: x["created_time"], reverse=True)
            
            # Limit results
            filtered_orders = filtered_orders[:limit]
            
            result = {
                "status": "success",
                "orders": filtered_orders,
                "n_orders": len(filtered_orders)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get order history: {str(e)}"}
    
    def update_position(self, symbol: str, side: str, quantity: float, 
                       price: float, exchange: str = "binance") -> Dict[str, Any]:
        """
        Update position after order fill.
        
        Args:
            symbol: Trading symbol
            side: Order side (BUY, SELL)
            quantity: Filled quantity
            price: Fill price
            exchange: Exchange name
            
        Returns:
            Position update result
        """
        try:
            position_key = f"{exchange}_{symbol}"
            
            if position_key not in self.positions:
                # Create new position
                self.positions[position_key] = {
                    "symbol": symbol,
                    "exchange": exchange,
                    "quantity": 0.0,
                    "average_price": 0.0,
                    "unrealized_pnl": 0.0,
                    "realized_pnl": 0.0,
                    "total_cost": 0.0,
                    "last_update": time.time()
                }
            
            position = self.positions[position_key]
            
            # Update position
            if side == OrderSide.BUY.value:
                # Add to position
                new_quantity = position["quantity"] + quantity
                new_cost = position["total_cost"] + (quantity * price)
                position["average_price"] = new_cost / new_quantity if new_quantity > 0 else 0
                position["quantity"] = new_quantity
                position["total_cost"] = new_cost
            else:
                # Reduce position
                position["quantity"] -= quantity
                position["total_cost"] -= (quantity * position["average_price"])
                
                # Calculate realized P&L
                realized_pnl = quantity * (price - position["average_price"])
                position["realized_pnl"] += realized_pnl
            
            position["last_update"] = time.time()
            
            result = {
                "status": "success",
                "position": position,
                "message": "Position updated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to update position: {str(e)}"}
    
    def get_positions(self, exchange: str = None) -> Dict[str, Any]:
        """
        Get current positions.
        
        Args:
            exchange: Filter by exchange
            
        Returns:
            Current positions
        """
        try:
            filtered_positions = []
            
            for position_key, position in self.positions.items():
                if exchange is None or position["exchange"] == exchange:
                    if position["quantity"] != 0:  # Only non-zero positions
                        filtered_positions.append(position)
            
            result = {
                "status": "success",
                "positions": filtered_positions,
                "n_positions": len(filtered_positions)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get positions: {str(e)}"}
    
    def calculate_portfolio_value(self, exchange: str = None) -> Dict[str, Any]:
        """
        Calculate portfolio value.
        
        Args:
            exchange: Filter by exchange
            
        Returns:
            Portfolio value
        """
        try:
            total_value = 0.0
            total_cost = 0.0
            total_pnl = 0.0
            
            for position_key, position in self.positions.items():
                if exchange is None or position["exchange"] == exchange:
                    if position["quantity"] != 0:
                        # Simulate current price
                        current_price = position["average_price"] * np.random.uniform(0.9, 1.1)
                        position_value = position["quantity"] * current_price
                        position_cost = position["total_cost"]
                        position_pnl = position_value - position_cost
                        
                        total_value += position_value
                        total_cost += position_cost
                        total_pnl += position_pnl
            
            portfolio = {
                "total_value": total_value,
                "total_cost": total_cost,
                "total_pnl": total_pnl,
                "return_percentage": (total_pnl / total_cost * 100) if total_cost > 0 else 0,
                "exchange": exchange,
                "timestamp": time.time()
            }
            
            result = {
                "status": "success",
                "portfolio": portfolio
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to calculate portfolio value: {str(e)}"}
    
    def set_risk_limits(self, risk_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set risk management limits.
        
        Args:
            risk_config: Risk configuration
            
        Returns:
            Risk limits result
        """
        try:
            # Validate risk configuration
            required_fields = ["max_position_size", "max_daily_loss", "max_drawdown"]
            for field in required_fields:
                if field not in risk_config:
                    return {"status": "error", "message": f"Missing required field: {field}"}
            
            # Set risk limits
            self.risk_limits = {
                "max_position_size": risk_config["max_position_size"],
                "max_daily_loss": risk_config["max_daily_loss"],
                "max_drawdown": risk_config["max_drawdown"],
                "max_orders_per_minute": risk_config.get("max_orders_per_minute", 10),
                "max_orders_per_day": risk_config.get("max_orders_per_day", 100),
                "stop_loss_percentage": risk_config.get("stop_loss_percentage", 0.05),
                "take_profit_percentage": risk_config.get("take_profit_percentage", 0.10),
                "update_time": time.time()
            }
            
            result = {
                "status": "success",
                "risk_limits": self.risk_limits,
                "message": "Risk limits set successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to set risk limits: {str(e)}"}
    
    def check_risk_limits(self, order_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if order violates risk limits.
        
        Args:
            order_config: Order configuration
            
        Returns:
            Risk check result
        """
        try:
            if not self.risk_limits:
                return {"status": "error", "message": "No risk limits set"}
            
            # Check position size
            order_quantity = order_config.get("quantity", 0)
            if order_quantity > self.risk_limits["max_position_size"]:
                return {
                    "status": "violation",
                    "violation_type": "position_size",
                    "limit": self.risk_limits["max_position_size"],
                    "value": order_quantity,
                    "message": "Order quantity exceeds maximum position size"
                }
            
            # Check daily loss (simplified)
            # In real implementation, this would check actual P&L
            
            # Check drawdown (simplified)
            # In real implementation, this would check actual drawdown
            
            result = {
                "status": "success",
                "risk_check": "passed",
                "message": "Order passes risk limits"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to check risk limits: {str(e)}"}
    
    def get_performance_metrics(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Get performance metrics.
        
        Args:
            start_date: Start date for metrics
            end_date: End date for metrics
            
        Returns:
            Performance metrics
        """
        try:
            # Filter orders by date range
            filtered_orders = self.order_history
            
            if start_date:
                start_timestamp = pd.to_datetime(start_date).timestamp()
                filtered_orders = [o for o in filtered_orders if o["created_time"] >= start_timestamp]
            
            if end_date:
                end_timestamp = pd.to_datetime(end_date).timestamp()
                filtered_orders = [o for o in filtered_orders if o["created_time"] <= end_timestamp]
            
            # Calculate metrics
            total_orders = len(filtered_orders)
            filled_orders = len([o for o in filtered_orders if o["status"] == OrderStatus.FILLED.value])
            canceled_orders = len([o for o in filtered_orders if o["status"] == OrderStatus.CANCELED.value])
            
            # Calculate total volume
            total_volume = sum(o["quantity"] * (o["price"] or 0) for o in filtered_orders if o["status"] == OrderStatus.FILLED.value)
            
            # Calculate average fill time (simplified)
            fill_times = []
            for order in filtered_orders:
                if order["status"] == OrderStatus.FILLED.value:
                    fill_time = order["updated_time"] - order["created_time"]
                    fill_times.append(fill_time)
            
            avg_fill_time = np.mean(fill_times) if fill_times else 0
            
            metrics = {
                "total_orders": total_orders,
                "filled_orders": filled_orders,
                "canceled_orders": canceled_orders,
                "fill_rate": (filled_orders / total_orders * 100) if total_orders > 0 else 0,
                "cancel_rate": (canceled_orders / total_orders * 100) if total_orders > 0 else 0,
                "total_volume": total_volume,
                "average_fill_time": avg_fill_time,
                "start_date": start_date,
                "end_date": end_date,
                "timestamp": time.time()
            }
            
            self.performance_metrics = metrics
            
            result = {
                "status": "success",
                "metrics": metrics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get performance metrics: {str(e)}"}
    
    def _validate_order(self, symbol: str, side: str, order_type: str, 
                       quantity: float, price: float, stop_price: float) -> Dict[str, Any]:
        """Validate order parameters."""
        try:
            # Check required fields
            if not symbol:
                return {"status": "error", "message": "Symbol is required"}
            
            if not side or side not in [OrderSide.BUY.value, OrderSide.SELL.value]:
                return {"status": "error", "message": "Invalid side"}
            
            if not order_type or order_type not in [ot.value for ot in OrderType]:
                return {"status": "error", "message": "Invalid order type"}
            
            if quantity <= 0:
                return {"status": "error", "message": "Quantity must be positive"}
            
            # Check price requirements
            if order_type in [OrderType.LIMIT.value, OrderType.STOP_LIMIT.value]:
                if price is None or price <= 0:
                    return {"status": "error", "message": "Price is required for LIMIT orders"}
            
            if order_type in [OrderType.STOP.value, OrderType.STOP_LIMIT.value]:
                if stop_price is None or stop_price <= 0:
                    return {"status": "error", "message": "Stop price is required for STOP orders"}
            
            return {"status": "success"}
            
        except Exception as e:
            return {"status": "error", "message": f"Validation failed: {str(e)}"}
