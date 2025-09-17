"""
Trading module for Pocket Hedge Fund.

This module provides automated trading functionality using ML predictions
and technical analysis.
"""

from .automated_trader import AutomatedTrader, TradingStrategy, TradingSignal

__all__ = ["AutomatedTrader", "TradingStrategy", "TradingSignal"]
