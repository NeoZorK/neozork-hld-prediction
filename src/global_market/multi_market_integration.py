"""
Multi-Market Integration System
Global exchanges, multiple asset classes, cross-market arbitrage
"""

import asyncio
import aiohttp
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssetClass(Enum):
    """Asset class enumeration"""
    CRYPTOCURRENCY = "cryptocurrency"
    FOREX = "forex"
    STOCKS = "stocks"
    COMMODITIES = "commodities"
    BONDS = "bonds"
    INDICES = "indices"
    DERIVATIVES = "derivatives"

class MarketType(Enum):
    """Market type enumeration"""
    SPOT = "spot"
    FUTURES = "futures"
    OPTIONS = "options"
    MARGIN = "margin"
    PERPETUAL = "perpetual"

@dataclass
class MarketData:
    """Market data structure"""
    symbol: str
    exchange: str
    asset_class: AssetClass
    market_type: MarketType
    price: float
    volume: float
    timestamp: datetime
    bid: float
    ask: float
    spread: float
    high_24h: float
    low_24h: float
    change_24h: float
    change_percent_24h: float

@dataclass
class ArbitrageOpportunity:
    """Arbitrage opportunity structure"""
    symbol: str
    buy_exchange: str
    sell_exchange: str
    buy_price: float
    sell_price: float
    spread: float
    spread_percent: float
    volume_available: float
    estimated_profit: float
    timestamp: datetime
    confidence: float

class ExchangeConnector:
    """Base class for exchange connectors"""
    
    def __init__(self, name: str, api_key: Optional[str] = None, secret: Optional[str] = None):
        self.name = name
        self.api_key = api_key
        self.secret = secret
        self.session = None
        self.rate_limits = {}
        self.last_request_time = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_ticker(self, symbol: str) -> Optional[MarketData]:
        """Get ticker data for a symbol"""
        raise NotImplementedError
        
    async def get_orderbook(self, symbol: str) -> Optional[Dict]:
        """Get order book data"""
        raise NotImplementedError
        
    async def get_trades(self, symbol: str, limit: int = 100) -> List[Dict]:
        """Get recent trades"""
        raise NotImplementedError

class BinanceConnector(ExchangeConnector):
    """Binance exchange connector"""
    
    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        super().__init__("binance", api_key, secret)
        self.base_url = "https://api.binance.com"
        
    async def get_ticker(self, symbol: str) -> Optional[MarketData]:
        """Get ticker data from Binance"""
        try:
            url = f"{self.base_url}/api/v3/ticker/24hr"
            params = {"symbol": symbol}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return MarketData(
                        symbol=data["symbol"],
                        exchange="binance",
                        asset_class=AssetClass.CRYPTOCURRENCY,
                        market_type=MarketType.SPOT,
                        price=float(data["lastPrice"]),
                        volume=float(data["volume"]),
                        timestamp=datetime.now(),
                        bid=float(data["bidPrice"]),
                        ask=float(data["askPrice"]),
                        spread=float(data["askPrice"]) - float(data["bidPrice"]),
                        high_24h=float(data["highPrice"]),
                        low_24h=float(data["lowPrice"]),
                        change_24h=float(data["priceChange"]),
                        change_percent_24h=float(data["priceChangePercent"])
                    )
        except Exception as e:
            logger.error(f"Error getting ticker from Binance: {e}")
            return None

class CoinbaseConnector(ExchangeConnector):
    """Coinbase exchange connector"""
    
    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        super().__init__("coinbase", api_key, secret)
        self.base_url = "https://api.exchange.coinbase.com"
        
    async def get_ticker(self, symbol: str) -> Optional[MarketData]:
        """Get ticker data from Coinbase"""
        try:
            url = f"{self.base_url}/products/{symbol}/ticker"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return MarketData(
                        symbol=symbol,
                        exchange="coinbase",
                        asset_class=AssetClass.CRYPTOCURRENCY,
                        market_type=MarketType.SPOT,
                        price=float(data["price"]),
                        volume=float(data["volume"]),
                        timestamp=datetime.now(),
                        bid=float(data["bid"]),
                        ask=float(data["ask"]),
                        spread=float(data["ask"]) - float(data["bid"]),
                        high_24h=0.0,  # Coinbase doesn't provide 24h data in ticker
                        low_24h=0.0,
                        change_24h=0.0,
                        change_percent_24h=0.0
                    )
        except Exception as e:
            logger.error(f"Error getting ticker from Coinbase: {e}")
            return None

class KrakenConnector(ExchangeConnector):
    """Kraken exchange connector"""
    
    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        super().__init__("kraken", api_key, secret)
        self.base_url = "https://api.kraken.com"
        
    async def get_ticker(self, symbol: str) -> Optional[MarketData]:
        """Get ticker data from Kraken"""
        try:
            url = f"{self.base_url}/0/public/Ticker"
            params = {"pair": symbol}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if "result" in data and symbol in data["result"]:
                        ticker_data = data["result"][symbol]
                        return MarketData(
                            symbol=symbol,
                            exchange="kraken",
                            asset_class=AssetClass.CRYPTOCURRENCY,
                            market_type=MarketType.SPOT,
                            price=float(ticker_data["c"][0]),
                            volume=float(ticker_data["v"][1]),
                            timestamp=datetime.now(),
                            bid=float(ticker_data["b"][0]),
                            ask=float(ticker_data["a"][0]),
                            spread=float(ticker_data["a"][0]) - float(ticker_data["b"][0]),
                            high_24h=float(ticker_data["h"][1]),
                            low_24h=float(ticker_data["l"][1]),
                            change_24h=float(ticker_data["c"][0]) - float(ticker_data["o"]),
                            change_percent_24h=((float(ticker_data["c"][0]) - float(ticker_data["o"])) / float(ticker_data["o"])) * 100
                        )
        except Exception as e:
            logger.error(f"Error getting ticker from Kraken: {e}")
            return None

class MultiMarketManager:
    """Multi-market integration manager"""
    
    def __init__(self):
        self.exchanges = {}
        self.market_data = {}
        self.arbitrage_opportunities = []
        self.supported_assets = {
            AssetClass.CRYPTOCURRENCY: ["BTC", "ETH", "BNB", "ADA", "SOL", "DOT", "MATIC", "AVAX"],
            AssetClass.FOREX: ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"],
            AssetClass.STOCKS: ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"],
            AssetClass.COMMODITIES: ["GOLD", "SILVER", "OIL", "GAS"],
            AssetClass.INDICES: ["SPX", "NDX", "DJI", "VIX"]
        }
        
    async def add_exchange(self, connector: ExchangeConnector):
        """Add an exchange connector"""
        self.exchanges[connector.name] = connector
        logger.info(f"Added exchange: {connector.name}")
        
    async def get_market_data(self, symbol: str, exchanges: List[str] = None) -> Dict[str, MarketData]:
        """Get market data from multiple exchanges"""
        if exchanges is None:
            exchanges = list(self.exchanges.keys())
            
        market_data = {}
        tasks = []
        
        for exchange_name in exchanges:
            if exchange_name in self.exchanges:
                connector = self.exchanges[exchange_name]
                task = connector.get_ticker(symbol)
                tasks.append((exchange_name, task))
        
        # Execute all requests concurrently
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        for i, result in enumerate(results):
            exchange_name = tasks[i][0]
            if isinstance(result, MarketData):
                market_data[exchange_name] = result
            elif isinstance(result, Exception):
                logger.error(f"Error getting data from {exchange_name}: {result}")
                
        return market_data
    
    async def detect_arbitrage_opportunities(self, symbol: str, min_spread_percent: float = 0.5) -> List[ArbitrageOpportunity]:
        """Detect arbitrage opportunities across exchanges"""
        market_data = await self.get_market_data(symbol)
        
        if len(market_data) < 2:
            return []
            
        opportunities = []
        exchanges = list(market_data.keys())
        
        # Compare all pairs of exchanges
        for i in range(len(exchanges)):
            for j in range(i + 1, len(exchanges)):
                exchange1 = exchanges[i]
                exchange2 = exchanges[j]
                
                data1 = market_data[exchange1]
                data2 = market_data[exchange2]
                
                # Check both directions
                spread1 = data2.ask - data1.bid
                spread2 = data1.ask - data2.bid
                
                spread_percent1 = (spread1 / data1.bid) * 100
                spread_percent2 = (spread2 / data2.bid) * 100
                
                # Check if spread is above minimum threshold
                if spread_percent1 > min_spread_percent:
                    volume_available = min(data1.volume, data2.volume)
                    estimated_profit = spread1 * volume_available
                    
                    opportunity = ArbitrageOpportunity(
                        symbol=symbol,
                        buy_exchange=exchange1,
                        sell_exchange=exchange2,
                        buy_price=data1.bid,
                        sell_price=data2.ask,
                        spread=spread1,
                        spread_percent=spread_percent1,
                        volume_available=volume_available,
                        estimated_profit=estimated_profit,
                        timestamp=datetime.now(),
                        confidence=min(spread_percent1 / 2, 1.0)  # Confidence based on spread
                    )
                    opportunities.append(opportunity)
                
                if spread_percent2 > min_spread_percent:
                    volume_available = min(data1.volume, data2.volume)
                    estimated_profit = spread2 * volume_available
                    
                    opportunity = ArbitrageOpportunity(
                        symbol=symbol,
                        buy_exchange=exchange2,
                        sell_exchange=exchange1,
                        buy_price=data2.bid,
                        sell_price=data1.ask,
                        spread=spread2,
                        spread_percent=spread_percent2,
                        volume_available=volume_available,
                        estimated_profit=estimated_profit,
                        timestamp=datetime.now(),
                        confidence=min(spread_percent2 / 2, 1.0)
                    )
                    opportunities.append(opportunity)
        
        # Sort by estimated profit
        opportunities.sort(key=lambda x: x.estimated_profit, reverse=True)
        return opportunities
    
    async def get_cross_market_analysis(self, symbols: List[str]) -> Dict[str, Any]:
        """Get cross-market analysis for multiple symbols"""
        analysis = {
            "timestamp": datetime.now(),
            "symbols": symbols,
            "market_data": {},
            "arbitrage_opportunities": {},
            "correlations": {},
            "volatility_analysis": {},
            "liquidity_analysis": {}
        }
        
        # Get market data for all symbols
        for symbol in symbols:
            market_data = await self.get_market_data(symbol)
            analysis["market_data"][symbol] = market_data
            
            # Detect arbitrage opportunities
            opportunities = await self.detect_arbitrage_opportunities(symbol)
            analysis["arbitrage_opportunities"][symbol] = opportunities
            
            # Calculate volatility
            if market_data:
                prices = [data.price for data in market_data.values()]
                if len(prices) > 1:
                    volatility = np.std(prices) / np.mean(prices) * 100
                    analysis["volatility_analysis"][symbol] = {
                        "volatility_percent": volatility,
                        "price_range": max(prices) - min(prices),
                        "price_std": np.std(prices)
                    }
                
                # Calculate liquidity
                total_volume = sum(data.volume for data in market_data.values())
                analysis["liquidity_analysis"][symbol] = {
                    "total_volume": total_volume,
                    "avg_volume": total_volume / len(market_data),
                    "volume_std": np.std([data.volume for data in market_data.values()])
                }
        
        # Calculate correlations between symbols
        if len(symbols) > 1:
            price_matrix = []
            for symbol in symbols:
                if symbol in analysis["market_data"] and analysis["market_data"][symbol]:
                    prices = [data.price for data in analysis["market_data"][symbol].values()]
                    if prices:
                        price_matrix.append(prices)
            
            if len(price_matrix) > 1:
                correlation_matrix = np.corrcoef(price_matrix)
                for i, symbol1 in enumerate(symbols):
                    for j, symbol2 in enumerate(symbols):
                        if i != j:
                            analysis["correlations"][f"{symbol1}_{symbol2}"] = correlation_matrix[i][j]
        
        return analysis
    
    async def get_portfolio_exposure(self, portfolio: Dict[str, float]) -> Dict[str, Any]:
        """Calculate portfolio exposure across markets"""
        exposure = {
            "timestamp": datetime.now(),
            "total_value": 0,
            "asset_class_exposure": {},
            "exchange_exposure": {},
            "geographic_exposure": {},
            "risk_metrics": {}
        }
        
        for symbol, quantity in portfolio.items():
            market_data = await self.get_market_data(symbol)
            
            for exchange, data in market_data.items():
                position_value = quantity * data.price
                exposure["total_value"] += position_value
                
                # Asset class exposure
                asset_class = data.asset_class.value
                if asset_class not in exposure["asset_class_exposure"]:
                    exposure["asset_class_exposure"][asset_class] = 0
                exposure["asset_class_exposure"][asset_class] += position_value
                
                # Exchange exposure
                if exchange not in exposure["exchange_exposure"]:
                    exposure["exchange_exposure"][exchange] = 0
                exposure["exchange_exposure"][exchange] += position_value
        
        # Calculate percentages
        if exposure["total_value"] > 0:
            for asset_class in exposure["asset_class_exposure"]:
                exposure["asset_class_exposure"][asset_class] = (
                    exposure["asset_class_exposure"][asset_class] / exposure["total_value"] * 100
                )
            
            for exchange in exposure["exchange_exposure"]:
                exposure["exchange_exposure"][exchange] = (
                    exposure["exchange_exposure"][exchange] / exposure["total_value"] * 100
                )
        
        return exposure
    
    def get_summary(self) -> Dict[str, Any]:
        """Get system summary"""
        return {
            "total_exchanges": len(self.exchanges),
            "supported_assets": {asset.value: len(symbols) for asset, symbols in self.supported_assets.items()},
            "total_arbitrage_opportunities": len(self.arbitrage_opportunities),
            "active_connections": len([ex for ex in self.exchanges.values() if ex.session]),
            "last_update": datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of MultiMarketManager"""
    manager = MultiMarketManager()
    
    # Add exchanges
    async with BinanceConnector() as binance:
        async with CoinbaseConnector() as coinbase:
            async with KrakenConnector() as kraken:
                await manager.add_exchange(binance)
                await manager.add_exchange(coinbase)
                await manager.add_exchange(kraken)
                
                # Get market data for BTC
                print("Getting market data for BTC...")
                btc_data = await manager.get_market_data("BTCUSDT")
                for exchange, data in btc_data.items():
                    print(f"{exchange}: ${data.price:.2f} (Volume: {data.volume:.2f})")
                
                # Detect arbitrage opportunities
                print("\nDetecting arbitrage opportunities...")
                opportunities = await manager.detect_arbitrage_opportunities("BTCUSDT")
                for opp in opportunities[:3]:  # Show top 3
                    print(f"Arbitrage: Buy {opp.buy_exchange} @ ${opp.buy_price:.2f}, "
                          f"Sell {opp.sell_exchange} @ ${opp.sell_price:.2f}, "
                          f"Spread: {opp.spread_percent:.2f}%, Profit: ${opp.estimated_profit:.2f}")
                
                # Cross-market analysis
                print("\nCross-market analysis...")
                analysis = await manager.get_cross_market_analysis(["BTCUSDT", "ETHUSDT"])
                print(f"Analysis completed for {len(analysis['symbols'])} symbols")
                
                # Portfolio exposure
                print("\nPortfolio exposure analysis...")
                portfolio = {"BTCUSDT": 0.1, "ETHUSDT": 1.0}
                exposure = await manager.get_portfolio_exposure(portfolio)
                print(f"Total portfolio value: ${exposure['total_value']:.2f}")
                
                # System summary
                print("\nSystem summary:")
                summary = manager.get_summary()
                print(f"Total exchanges: {summary['total_exchanges']}")
                print(f"Supported assets: {summary['supported_assets']}")

if __name__ == "__main__":
    asyncio.run(main())
