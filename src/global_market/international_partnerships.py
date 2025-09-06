"""
International Partnerships System
API integrations, data providers, liquidity providers
"""

import asyncio
import aiohttp
import json
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PartnershipType(Enum):
    """Partnership type enumeration"""
    EXCHANGE = "exchange"
    DATA_PROVIDER = "data_provider"
    LIQUIDITY_PROVIDER = "liquidity_provider"
    PAYMENT_PROCESSOR = "payment_processor"
    REGULATORY_SERVICE = "regulatory_service"
    TECHNOLOGY_PARTNER = "technology_partner"

class PartnershipStatus(Enum):
    """Partnership status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"

class DataProviderType(Enum):
    """Data provider type enumeration"""
    MARKET_DATA = "market_data"
    NEWS_FEED = "news_feed"
    SENTIMENT_DATA = "sentiment_data"
    ON_CHAIN_DATA = "on_chain_data"
    ECONOMIC_DATA = "economic_data"
    SOCIAL_MEDIA = "social_media"

@dataclass
class Partnership:
    """Partnership definition"""
    partnership_id: str
    name: str
    partnership_type: PartnershipType
    status: PartnershipStatus
    api_endpoint: str
    api_key: str
    api_secret: str
    rate_limits: Dict[str, int]
    supported_features: List[str]
    supported_markets: List[str]
    contact_info: Dict[str, str]
    contract_details: Dict[str, Any]
    created_at: datetime
    last_activity: datetime
    performance_metrics: Dict[str, float]

@dataclass
class DataProvider:
    """Data provider definition"""
    provider_id: str
    name: str
    provider_type: DataProviderType
    api_endpoint: str
    api_key: str
    data_schema: Dict[str, Any]
    update_frequency: int  # seconds
    data_quality_score: float
    latency_ms: float
    availability_percent: float
    cost_per_request: float
    supported_symbols: List[str]
    created_at: datetime

@dataclass
class LiquidityProvider:
    """Liquidity provider definition"""
    provider_id: str
    name: str
    api_endpoint: str
    api_key: str
    supported_assets: List[str]
    min_order_size: Dict[str, float]
    max_order_size: Dict[str, float]
    fee_structure: Dict[str, float]
    settlement_time: int  # minutes
    credit_limit: float
    current_usage: float
    performance_metrics: Dict[str, float]
    created_at: datetime

class APIManager:
    """API management for partnerships"""
    
    def __init__(self):
        self.partnerships = {}
        self.api_sessions = {}
        self.rate_limit_trackers = {}
        self.request_logs = {}
        
    async def register_partnership(self, partnership: Partnership) -> bool:
        """Register new partnership"""
        self.partnerships[partnership.partnership_id] = partnership
        self.rate_limit_trackers[partnership.partnership_id] = {
            "requests_per_minute": 0,
            "requests_per_hour": 0,
            "requests_per_day": 0,
            "last_reset_minute": datetime.now(),
            "last_reset_hour": datetime.now(),
            "last_reset_day": datetime.now()
        }
        self.request_logs[partnership.partnership_id] = []
        
        logger.info(f"Registered partnership: {partnership.name}")
        return True
    
    async def make_api_request(self, partnership_id: str, endpoint: str, 
                             method: str = "GET", data: Dict[str, Any] = None,
                             headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Make API request to partnership"""
        if partnership_id not in self.partnerships:
            return {"error": "Partnership not found"}
        
        partnership = self.partnerships[partnership_id]
        
        # Check rate limits
        if not await self._check_rate_limits(partnership_id):
            return {"error": "Rate limit exceeded"}
        
        # Prepare request
        url = f"{partnership.api_endpoint}{endpoint}"
        request_headers = {
            "Content-Type": "application/json",
            "User-Agent": "NeoZork-Trading-System/1.0"
        }
        
        if headers:
            request_headers.update(headers)
        
        # Add authentication
        if partnership.api_key:
            request_headers["X-API-Key"] = partnership.api_key
        
        # Add signature if secret is provided
        if partnership.api_secret and data:
            signature = self._generate_signature(partnership.api_secret, data)
            request_headers["X-Signature"] = signature
        
        # Make request
        start_time = datetime.now()
        try:
            async with aiohttp.ClientSession() as session:
                if method.upper() == "GET":
                    async with session.get(url, headers=request_headers) as response:
                        result = await response.json()
                elif method.upper() == "POST":
                    async with session.post(url, headers=request_headers, json=data) as response:
                        result = await response.json()
                elif method.upper() == "PUT":
                    async with session.put(url, headers=request_headers, json=data) as response:
                        result = await response.json()
                else:
                    return {"error": f"Unsupported method: {method}"}
                
                # Log request
                await self._log_request(partnership_id, endpoint, method, response.status, 
                                      datetime.now() - start_time)
                
                return {
                    "status": "success",
                    "status_code": response.status,
                    "data": result,
                    "response_time": (datetime.now() - start_time).total_seconds()
                }
                
        except Exception as e:
            logger.error(f"API request failed for {partnership_id}: {e}")
            return {
                "status": "error",
                "error": str(e),
                "response_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def _check_rate_limits(self, partnership_id: str) -> bool:
        """Check if request is within rate limits"""
        partnership = self.partnerships[partnership_id]
        tracker = self.rate_limit_trackers[partnership_id]
        now = datetime.now()
        
        # Reset counters if needed
        if (now - tracker["last_reset_minute"]).seconds >= 60:
            tracker["requests_per_minute"] = 0
            tracker["last_reset_minute"] = now
        
        if (now - tracker["last_reset_hour"]).seconds >= 3600:
            tracker["requests_per_hour"] = 0
            tracker["last_reset_hour"] = now
        
        if (now - tracker["last_reset_day"]).days >= 1:
            tracker["requests_per_day"] = 0
            tracker["last_reset_day"] = now
        
        # Check limits
        rate_limits = partnership.rate_limits
        
        if tracker["requests_per_minute"] >= rate_limits.get("per_minute", 1000):
            return False
        if tracker["requests_per_hour"] >= rate_limits.get("per_hour", 10000):
            return False
        if tracker["requests_per_day"] >= rate_limits.get("per_day", 100000):
            return False
        
        # Increment counters
        tracker["requests_per_minute"] += 1
        tracker["requests_per_hour"] += 1
        tracker["requests_per_day"] += 1
        
        return True
    
    def _generate_signature(self, secret: str, data: Dict[str, Any]) -> str:
        """Generate API signature"""
        message = json.dumps(data, sort_keys=True)
        signature = hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    async def _log_request(self, partnership_id: str, endpoint: str, method: str, 
                          status_code: int, response_time: timedelta):
        """Log API request"""
        log_entry = {
            "partnership_id": partnership_id,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_time_ms": response_time.total_seconds() * 1000,
            "timestamp": datetime.now()
        }
        
        self.request_logs[partnership_id].append(log_entry)
        
        # Keep only last 1000 requests
        if len(self.request_logs[partnership_id]) > 1000:
            self.request_logs[partnership_id] = self.request_logs[partnership_id][-1000:]

class DataProviderManager:
    """Data provider management"""
    
    def __init__(self):
        self.data_providers = {}
        self.data_cache = {}
        self.data_quality_scores = {}
        
    async def register_data_provider(self, provider: DataProvider) -> bool:
        """Register data provider"""
        self.data_providers[provider.provider_id] = provider
        self.data_cache[provider.provider_id] = {}
        self.data_quality_scores[provider.provider_id] = {
            "accuracy": 0.95,
            "completeness": 0.90,
            "timeliness": 0.85,
            "consistency": 0.92
        }
        
        logger.info(f"Registered data provider: {provider.name}")
        return True
    
    async def fetch_market_data(self, provider_id: str, symbols: List[str]) -> Dict[str, Any]:
        """Fetch market data from provider"""
        if provider_id not in self.data_providers:
            return {"error": "Data provider not found"}
        
        provider = self.data_providers[provider_id]
        
        # Check cache first
        cache_key = f"{provider_id}_{'_'.join(symbols)}"
        if cache_key in self.data_cache[provider_id]:
            cached_data = self.data_cache[provider_id][cache_key]
            if (datetime.now() - cached_data["timestamp"]).seconds < provider.update_frequency:
                return {
                    "status": "success",
                    "data": cached_data["data"],
                    "source": "cache",
                    "timestamp": cached_data["timestamp"]
                }
        
        # Fetch fresh data (simulated)
        market_data = {}
        for symbol in symbols:
            if symbol in provider.supported_symbols:
                market_data[symbol] = {
                    "price": 50000.0 + hash(symbol) % 10000,  # Simulated price
                    "volume": 1000000 + hash(symbol) % 500000,
                    "timestamp": datetime.now(),
                    "bid": 49950.0 + hash(symbol) % 100,
                    "ask": 50050.0 + hash(symbol) % 100
                }
        
        # Cache the data
        self.data_cache[provider_id][cache_key] = {
            "data": market_data,
            "timestamp": datetime.now()
        }
        
        return {
            "status": "success",
            "data": market_data,
            "source": "api",
            "timestamp": datetime.now()
        }
    
    async def fetch_news_data(self, provider_id: str, keywords: List[str], 
                            limit: int = 100) -> Dict[str, Any]:
        """Fetch news data from provider"""
        if provider_id not in self.data_providers:
            return {"error": "Data provider not found"}
        
        provider = self.data_providers[provider_id]
        
        # Simulate news data
        news_data = []
        for i in range(min(limit, 10)):
            news_item = {
                "id": f"news_{i}",
                "title": f"Market Update: {keywords[0] if keywords else 'General'}",
                "content": f"Latest market analysis and trends for {keywords[0] if keywords else 'cryptocurrency'}",
                "source": provider.name,
                "published_at": datetime.now() - timedelta(hours=i),
                "sentiment_score": 0.5 + (hash(str(i)) % 100) / 100 - 0.5,  # -0.5 to 0.5
                "keywords": keywords,
                "url": f"https://example.com/news/{i}"
            }
            news_data.append(news_item)
        
        return {
            "status": "success",
            "data": news_data,
            "total_count": len(news_data),
            "timestamp": datetime.now()
        }
    
    async def get_data_quality_report(self, provider_id: str) -> Dict[str, Any]:
        """Get data quality report for provider"""
        if provider_id not in self.data_providers:
            return {"error": "Data provider not found"}
        
        provider = self.data_providers[provider_id]
        quality_scores = self.data_quality_scores[provider_id]
        
        return {
            "provider_id": provider_id,
            "provider_name": provider.name,
            "quality_scores": quality_scores,
            "overall_score": sum(quality_scores.values()) / len(quality_scores),
            "data_availability": provider.availability_percent,
            "average_latency": provider.latency_ms,
            "cost_per_request": provider.cost_per_request,
            "supported_symbols_count": len(provider.supported_symbols),
            "report_timestamp": datetime.now()
        }

class LiquidityProviderManager:
    """Liquidity provider management"""
    
    def __init__(self):
        self.liquidity_providers = {}
        self.order_history = {}
        self.performance_metrics = {}
        
    async def register_liquidity_provider(self, provider: LiquidityProvider) -> bool:
        """Register liquidity provider"""
        self.liquidity_providers[provider.provider_id] = provider
        self.order_history[provider.provider_id] = []
        self.performance_metrics[provider.provider_id] = {
            "total_volume": 0.0,
            "successful_orders": 0,
            "failed_orders": 0,
            "average_fill_time": 0.0,
            "slippage": 0.0
        }
        
        logger.info(f"Registered liquidity provider: {provider.name}")
        return True
    
    async def place_order(self, provider_id: str, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Place order through liquidity provider"""
        if provider_id not in self.liquidity_providers:
            return {"error": "Liquidity provider not found"}
        
        provider = self.liquidity_providers[provider_id]
        
        # Validate order
        symbol = order_data.get("symbol")
        quantity = order_data.get("quantity")
        order_type = order_data.get("order_type", "market")
        
        if symbol not in provider.supported_assets:
            return {"error": f"Asset {symbol} not supported by provider"}
        
        if quantity < provider.min_order_size.get(symbol, 0):
            return {"error": f"Order size below minimum for {symbol}"}
        
        if quantity > provider.max_order_size.get(symbol, float('inf')):
            return {"error": f"Order size above maximum for {symbol}"}
        
        # Check credit limit
        if provider.current_usage + quantity > provider.credit_limit:
            return {"error": "Credit limit exceeded"}
        
        # Simulate order execution
        order_id = str(uuid.uuid4())
        fill_time = 0.5 + (hash(order_id) % 100) / 100  # 0.5-1.5 seconds
        
        order_result = {
            "order_id": order_id,
            "provider_id": provider_id,
            "symbol": symbol,
            "quantity": quantity,
            "order_type": order_type,
            "status": "filled",
            "fill_price": 50000.0 + (hash(order_id) % 1000),  # Simulated price
            "fill_time_seconds": fill_time,
            "fees": quantity * provider.fee_structure.get(symbol, 0.001),
            "timestamp": datetime.now()
        }
        
        # Update provider usage
        provider.current_usage += quantity
        
        # Log order
        self.order_history[provider.provider_id].append(order_result)
        
        # Update performance metrics
        metrics = self.performance_metrics[provider_id]
        metrics["total_volume"] += quantity
        metrics["successful_orders"] += 1
        metrics["average_fill_time"] = (metrics["average_fill_time"] + fill_time) / 2
        
        return {
            "status": "success",
            "order_result": order_result
        }
    
    async def get_liquidity_quote(self, provider_id: str, symbol: str, 
                                quantity: float) -> Dict[str, Any]:
        """Get liquidity quote from provider"""
        if provider_id not in self.liquidity_providers:
            return {"error": "Liquidity provider not found"}
        
        provider = self.liquidity_providers[provider_id]
        
        if symbol not in provider.supported_assets:
            return {"error": f"Asset {symbol} not supported"}
        
        # Simulate quote
        base_price = 50000.0 + (hash(symbol) % 10000)
        spread = 0.001  # 0.1% spread
        
        quote = {
            "provider_id": provider_id,
            "symbol": symbol,
            "quantity": quantity,
            "bid_price": base_price * (1 - spread/2),
            "ask_price": base_price * (1 + spread/2),
            "spread": spread,
            "fees": quantity * provider.fee_structure.get(symbol, 0.001),
            "valid_until": datetime.now() + timedelta(seconds=30),
            "timestamp": datetime.now()
        }
        
        return {
            "status": "success",
            "quote": quote
        }
    
    async def get_provider_performance(self, provider_id: str) -> Dict[str, Any]:
        """Get performance metrics for liquidity provider"""
        if provider_id not in self.liquidity_providers:
            return {"error": "Liquidity provider not found"}
        
        provider = self.liquidity_providers[provider_id]
        metrics = self.performance_metrics[provider_id]
        orders = self.order_history[provider_id]
        
        success_rate = 0.0
        if metrics["successful_orders"] + metrics["failed_orders"] > 0:
            success_rate = metrics["successful_orders"] / (metrics["successful_orders"] + metrics["failed_orders"])
        
        return {
            "provider_id": provider_id,
            "provider_name": provider.name,
            "performance_metrics": metrics,
            "success_rate": success_rate,
            "credit_utilization": provider.current_usage / provider.credit_limit * 100,
            "total_orders": len(orders),
            "recent_orders": orders[-10:] if orders else [],
            "report_timestamp": datetime.now()
        }

class InternationalPartnershipsManager:
    """Main international partnerships manager"""
    
    def __init__(self):
        self.api_manager = APIManager()
        self.data_provider_manager = DataProviderManager()
        self.liquidity_provider_manager = LiquidityProviderManager()
        self.partnership_analytics = {}
        
    async def initialize_partnerships(self):
        """Initialize default partnerships"""
        # Register exchange partnerships
        binance_partnership = Partnership(
            partnership_id="binance_partnership",
            name="Binance Exchange",
            partnership_type=PartnershipType.EXCHANGE,
            status=PartnershipStatus.ACTIVE,
            api_endpoint="https://api.binance.com",
            api_key="sample_api_key",
            api_secret="sample_api_secret",
            rate_limits={"per_minute": 1200, "per_hour": 10000, "per_day": 100000},
            supported_features=["spot_trading", "futures", "options"],
            supported_markets=["BTC", "ETH", "BNB", "ADA", "SOL"],
            contact_info={"email": "partnerships@binance.com", "phone": "+1-555-0123"},
            contract_details={"tier": "VIP", "discount": 0.1},
            created_at=datetime.now(),
            last_activity=datetime.now(),
            performance_metrics={"uptime": 99.9, "latency": 50.0}
        )
        
        # Register data providers
        market_data_provider = DataProvider(
            provider_id="market_data_provider",
            name="Market Data Solutions",
            provider_type=DataProviderType.MARKET_DATA,
            api_endpoint="https://api.marketdata.com",
            api_key="sample_data_key",
            data_schema={"price": "float", "volume": "int", "timestamp": "datetime"},
            update_frequency=1,
            data_quality_score=0.95,
            latency_ms=25.0,
            availability_percent=99.8,
            cost_per_request=0.001,
            supported_symbols=["BTC", "ETH", "BNB", "ADA", "SOL", "DOT", "MATIC"],
            created_at=datetime.now()
        )
        
        news_data_provider = DataProvider(
            provider_id="news_data_provider",
            name="Financial News Feed",
            provider_type=DataProviderType.NEWS_FEED,
            api_endpoint="https://api.newsfeed.com",
            api_key="sample_news_key",
            data_schema={"title": "string", "content": "string", "sentiment": "float"},
            update_frequency=60,
            data_quality_score=0.90,
            latency_ms=100.0,
            availability_percent=99.5,
            cost_per_request=0.005,
            supported_symbols=["BTC", "ETH", "BNB", "ADA", "SOL"],
            created_at=datetime.now()
        )
        
        # Register liquidity providers
        liquidity_provider = LiquidityProvider(
            provider_id="liquidity_provider_1",
            name="Global Liquidity Solutions",
            api_endpoint="https://api.liquidity.com",
            api_key="sample_liquidity_key",
            supported_assets=["BTC", "ETH", "BNB", "ADA", "SOL"],
            min_order_size={"BTC": 0.001, "ETH": 0.01, "BNB": 0.1, "ADA": 10.0, "SOL": 0.1},
            max_order_size={"BTC": 100.0, "ETH": 1000.0, "BNB": 10000.0, "ADA": 100000.0, "SOL": 10000.0},
            fee_structure={"BTC": 0.001, "ETH": 0.001, "BNB": 0.001, "ADA": 0.001, "SOL": 0.001},
            settlement_time=5,
            credit_limit=1000000.0,
            current_usage=0.0,
            performance_metrics={"fill_rate": 99.5, "slippage": 0.05},
            created_at=datetime.now()
        )
        
        # Register all partnerships
        await self.api_manager.register_partnership(binance_partnership)
        await self.data_provider_manager.register_data_provider(market_data_provider)
        await self.data_provider_manager.register_data_provider(news_data_provider)
        await self.liquidity_provider_manager.register_liquidity_provider(liquidity_provider)
        
        logger.info("Initialized international partnerships")
    
    async def get_partnership_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive partnership dashboard"""
        dashboard = {
            "timestamp": datetime.now(),
            "partnerships": {
                "total": len(self.api_manager.partnerships),
                "active": len([p for p in self.api_manager.partnerships.values() 
                             if p.status == PartnershipStatus.ACTIVE]),
                "by_type": {}
            },
            "data_providers": {
                "total": len(self.data_provider_manager.data_providers),
                "by_type": {}
            },
            "liquidity_providers": {
                "total": len(self.liquidity_provider_manager.liquidity_providers),
                "total_credit_limit": sum(p.credit_limit for p in self.liquidity_provider_manager.liquidity_providers.values()),
                "total_usage": sum(p.current_usage for p in self.liquidity_provider_manager.liquidity_providers.values())
            },
            "performance_summary": {
                "total_api_requests": sum(len(logs) for logs in self.api_manager.request_logs.values()),
                "average_response_time": 0.0,
                "success_rate": 0.0
            }
        }
        
        # Calculate partnership types
        for partnership in self.api_manager.partnerships.values():
            ptype = partnership.partnership_type.value
            if ptype not in dashboard["partnerships"]["by_type"]:
                dashboard["partnerships"]["by_type"][ptype] = 0
            dashboard["partnerships"]["by_type"][ptype] += 1
        
        # Calculate data provider types
        for provider in self.data_provider_manager.data_providers.values():
            ptype = provider.provider_type.value
            if ptype not in dashboard["data_providers"]["by_type"]:
                dashboard["data_providers"]["by_type"][ptype] = 0
            dashboard["data_providers"]["by_type"][ptype] += 1
        
        # Calculate performance metrics
        total_requests = 0
        total_response_time = 0.0
        successful_requests = 0
        
        for logs in self.api_manager.request_logs.values():
            for log in logs:
                total_requests += 1
                total_response_time += log["response_time_ms"]
                if log["status_code"] < 400:
                    successful_requests += 1
        
        if total_requests > 0:
            dashboard["performance_summary"]["average_response_time"] = total_response_time / total_requests
            dashboard["performance_summary"]["success_rate"] = successful_requests / total_requests
        
        return dashboard
    
    async def execute_trading_workflow(self, symbol: str, quantity: float) -> Dict[str, Any]:
        """Execute complete trading workflow using partnerships"""
        workflow_result = {
            "symbol": symbol,
            "quantity": quantity,
            "timestamp": datetime.now(),
            "steps": {}
        }
        
        # Step 1: Get market data
        market_data = await self.data_provider_manager.fetch_market_data("market_data_provider", [symbol])
        workflow_result["steps"]["market_data"] = market_data
        
        # Step 2: Get news sentiment
        news_data = await self.data_provider_manager.fetch_news_data("news_data_provider", [symbol], 5)
        workflow_result["steps"]["news_data"] = news_data
        
        # Step 3: Get liquidity quote
        quote = await self.liquidity_provider_manager.get_liquidity_quote("liquidity_provider_1", symbol, quantity)
        workflow_result["steps"]["liquidity_quote"] = quote
        
        # Step 4: Place order (if quote is acceptable)
        if quote.get("status") == "success":
            order_data = {
                "symbol": symbol,
                "quantity": quantity,
                "order_type": "market"
            }
            order_result = await self.liquidity_provider_manager.place_order("liquidity_provider_1", order_data)
            workflow_result["steps"]["order_execution"] = order_result
        
        return workflow_result
    
    def get_summary(self) -> Dict[str, Any]:
        """Get partnerships system summary"""
        return {
            "total_partnerships": len(self.api_manager.partnerships),
            "total_data_providers": len(self.data_provider_manager.data_providers),
            "total_liquidity_providers": len(self.liquidity_provider_manager.liquidity_providers),
            "total_api_requests": sum(len(logs) for logs in self.api_manager.request_logs.values()),
            "last_update": datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of InternationalPartnershipsManager"""
    manager = InternationalPartnershipsManager()
    
    # Initialize partnerships
    await manager.initialize_partnerships()
    
    # Get partnership dashboard
    dashboard = await manager.get_partnership_dashboard()
    print(f"Partnership Dashboard:")
    print(f"  Total Partnerships: {dashboard['partnerships']['total']}")
    print(f"  Active Partnerships: {dashboard['partnerships']['active']}")
    print(f"  Data Providers: {dashboard['data_providers']['total']}")
    print(f"  Liquidity Providers: {dashboard['liquidity_providers']['total']}")
    
    # Execute trading workflow
    workflow = await manager.execute_trading_workflow("BTC", 0.1)
    print(f"\nTrading Workflow for BTC:")
    print(f"  Market Data: {workflow['steps']['market_data']['status']}")
    print(f"  News Data: {workflow['steps']['news_data']['status']}")
    print(f"  Liquidity Quote: {workflow['steps']['liquidity_quote']['status']}")
    print(f"  Order Execution: {workflow['steps']['order_execution']['status']}")
    
    # Get provider performance
    performance = await manager.liquidity_provider_manager.get_provider_performance("liquidity_provider_1")
    print(f"\nLiquidity Provider Performance:")
    print(f"  Success Rate: {performance['success_rate']:.2%}")
    print(f"  Total Volume: {performance['performance_metrics']['total_volume']:.2f}")
    print(f"  Credit Utilization: {performance['credit_utilization']:.1f}%")
    
    # System summary
    summary = manager.get_summary()
    print(f"\nSystem Summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
