# -*- coding: utf-8 -*-
"""
Alternative Data Sources and Sentiment Analysis for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive alternative data collection and sentiment analysis capabilities.
"""

import asyncio
import aiohttp
import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import time
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataSource(Enum):
    """Alternative data sources."""
    NEWS = "news"
    SOCIAL_MEDIA = "social_media"
    REDDIT = "reddit"
    TWITTER = "twitter"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    GITHUB = "github"
    ON_CHAIN = "on_chain"
    GOOGLE_TRENDS = "google_trends"
    ECONOMIC_INDICATORS = "economic_indicators"
    WEATHER = "weather"
    SATELLITE_DATA = "satellite_data"
    WEB_SCRAPING = "web_scraping"
    API_DATA = "api_data"

class SentimentType(Enum):
    """Sentiment types."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    VERY_POSITIVE = "very_positive"
    VERY_NEGATIVE = "very_negative"

class DataFrequency(Enum):
    """Data frequency."""
    REAL_TIME = "real_time"
    MINUTE = "minute"
    HOUR = "hour"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

@dataclass
class DataSourceConfig:
    """Data source configuration."""
    source: DataSource
    frequency: DataFrequency
    symbols: List[str]
    keywords: List[str] = field(default_factory=list)
    api_keys: Dict[str, str] = field(default_factory=dict)
    rate_limits: Dict[str, int] = field(default_factory=dict)
    filters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SentimentData:
    """Sentiment data structure."""
    timestamp: datetime
    source: DataSource
    symbol: str
    text: str
    sentiment_score: float
    sentiment_type: SentimentType
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AlternativeDataPoint:
    """Alternative data point."""
    timestamp: datetime
    source: DataSource
    symbol: str
    data_type: str
    value: Union[float, str, Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)

class SentimentAnalyzer:
    """Advanced sentiment analysis system."""
    
    def __init__(self):
        self.sentiment_models = {}
        self.sentiment_history = []
        self.keyword_sentiments = {}
        
    def analyze_text_sentiment(self, text: str, symbol: str = None) -> SentimentData:
        """Analyze sentiment of text."""
        try:
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Calculate sentiment score
            sentiment_score = self._calculate_sentiment_score(cleaned_text)
            
            # Determine sentiment type
            sentiment_type = self._determine_sentiment_type(sentiment_score)
            
            # Calculate confidence
            confidence = self._calculate_confidence(cleaned_text, sentiment_score)
            
            # Extract metadata
            metadata = self._extract_metadata(cleaned_text, symbol)
            
            sentiment_data = SentimentData(
                timestamp=datetime.now(),
                source=DataSource.SOCIAL_MEDIA,  # Default source
                symbol=symbol or "UNKNOWN",
                text=cleaned_text,
                sentiment_score=sentiment_score,
                sentiment_type=sentiment_type,
                confidence=confidence,
                metadata=metadata
            )
            
            # Store in history
            self.sentiment_history.append(sentiment_data)
            if len(self.sentiment_history) > 10000:
                self.sentiment_history.pop(0)
            
            return sentiment_data
            
        except Exception as e:
            logger.error(f"Failed to analyze sentiment: {e}")
            return SentimentData(
                timestamp=datetime.now(),
                source=DataSource.SOCIAL_MEDIA,
                symbol=symbol or "UNKNOWN",
                text=text,
                sentiment_score=0.0,
                sentiment_type=SentimentType.NEUTRAL,
                confidence=0.0
            )
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text."""
        try:
            # Remove URLs
            text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
            
            # Remove special characters but keep basic punctuation
            text = re.sub(r'[^\w\s.,!?]', '', text)
            
            # Remove extra whitespace
            text = ' '.join(text.split())
            
            # Convert to lowercase
            text = text.lower()
            
            return text
            
        except Exception as e:
            logger.error(f"Failed to clean text: {e}")
            return text
    
    def _calculate_sentiment_score(self, text: str) -> float:
        """Calculate sentiment score using rule-based approach."""
        try:
            # Define sentiment words
            positive_words = [
                'bullish', 'moon', 'pump', 'buy', 'long', 'profit', 'gain', 'rise', 'up',
                'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love',
                'hodl', 'diamond', 'hands', 'rocket', 'lambo', 'green', 'candle'
            ]
            
            negative_words = [
                'bearish', 'dump', 'sell', 'short', 'loss', 'crash', 'down', 'fall',
                'bad', 'terrible', 'awful', 'hate', 'fear', 'panic', 'red', 'candle',
                'rekt', 'bag', 'holder', 'fud', 'scam', 'rug', 'pull'
            ]
            
            # Count sentiment words
            words = text.split()
            positive_count = sum(1 for word in words if word in positive_words)
            negative_count = sum(1 for word in words if word in negative_words)
            
            # Calculate score
            total_sentiment_words = positive_count + negative_count
            if total_sentiment_words == 0:
                return 0.0
            
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
            
            # Normalize to [-1, 1] range
            sentiment_score = max(-1.0, min(1.0, sentiment_score))
            
            return sentiment_score
            
        except Exception as e:
            logger.error(f"Failed to calculate sentiment score: {e}")
            return 0.0
    
    def _determine_sentiment_type(self, sentiment_score: float) -> SentimentType:
        """Determine sentiment type from score."""
        if sentiment_score >= 0.6:
            return SentimentType.VERY_POSITIVE
        elif sentiment_score >= 0.2:
            return SentimentType.POSITIVE
        elif sentiment_score <= -0.6:
            return SentimentType.VERY_NEGATIVE
        elif sentiment_score <= -0.2:
            return SentimentType.NEGATIVE
        else:
            return SentimentType.NEUTRAL
    
    def _calculate_confidence(self, text: str, sentiment_score: float) -> float:
        """Calculate confidence in sentiment analysis."""
        try:
            # Base confidence on text length and sentiment strength
            text_length = len(text.split())
            sentiment_strength = abs(sentiment_score)
            
            # Longer texts with stronger sentiment = higher confidence
            length_factor = min(1.0, text_length / 20)  # Normalize to 20 words
            strength_factor = sentiment_strength
            
            confidence = (length_factor + strength_factor) / 2
            confidence = max(0.1, min(1.0, confidence))
            
            return confidence
            
        except Exception as e:
            logger.error(f"Failed to calculate confidence: {e}")
            return 0.5
    
    def _extract_metadata(self, text: str, symbol: str) -> Dict[str, Any]:
        """Extract metadata from text."""
        try:
            metadata = {
                'text_length': len(text),
                'word_count': len(text.split()),
                'has_emoji': bool(re.search(r'[^\w\s.,!?]', text)),
                'has_hashtag': '#' in text,
                'has_mention': '@' in text,
                'symbol_mentioned': symbol.lower() in text.lower() if symbol else False
            }
            
            # Extract potential price mentions
            price_pattern = r'\$?(\d+(?:\.\d{2})?)'
            price_matches = re.findall(price_pattern, text)
            if price_matches:
                metadata['price_mentions'] = [float(p) for p in price_matches]
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to extract metadata: {e}")
            return {}
    
    def get_sentiment_summary(self, symbol: str = None, hours: int = 24) -> Dict[str, Any]:
        """Get sentiment summary for a symbol."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter sentiment data
            if symbol:
                filtered_data = [
                    data for data in self.sentiment_history
                    if data.symbol == symbol and data.timestamp >= cutoff_time
                ]
            else:
                filtered_data = [
                    data for data in self.sentiment_history
                    if data.timestamp >= cutoff_time
                ]
            
            if not filtered_data:
                return {
                    'total_sentiments': 0,
                    'average_sentiment': 0.0,
                    'sentiment_distribution': {},
                    'confidence': 0.0
                }
            
            # Calculate summary statistics
            sentiment_scores = [data.sentiment_score for data in filtered_data]
            average_sentiment = np.mean(sentiment_scores)
            
            # Sentiment distribution
            sentiment_distribution = {}
            for sentiment_type in SentimentType:
                count = sum(1 for data in filtered_data if data.sentiment_type == sentiment_type)
                sentiment_distribution[sentiment_type.value] = count
            
            # Average confidence
            confidences = [data.confidence for data in filtered_data]
            average_confidence = np.mean(confidences)
            
            return {
                'total_sentiments': len(filtered_data),
                'average_sentiment': average_sentiment,
                'sentiment_distribution': sentiment_distribution,
                'confidence': average_confidence,
                'time_range_hours': hours
            }
            
        except Exception as e:
            logger.error(f"Failed to get sentiment summary: {e}")
            return {}

class AlternativeDataCollector:
    """Alternative data collection system."""
    
    def __init__(self):
        self.data_sources = {}
        self.collected_data = []
        self.sentiment_analyzer = SentimentAnalyzer()
        
    async def initialize(self) -> Dict[str, Any]:
        """Initialize data collector."""
        try:
            # Initialize data sources
            for source in DataSource:
                self.data_sources[source] = {
                    'enabled': False,
                    'last_collection': None,
                    'collection_count': 0,
                    'error_count': 0
                }
            
            logger.info("Alternative data collector initialized")
            
            return {
                'status': 'success',
                'data_sources': len(self.data_sources),
                'message': 'Alternative data collector initialized successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to initialize data collector: {e}")
            return {
                'status': 'error',
                'message': f'Failed to initialize data collector: {str(e)}'
            }
    
    async def collect_news_data(self, config: DataSourceConfig) -> Dict[str, Any]:
        """Collect news data."""
        try:
            # Simulate news data collection
            news_data = []
            
            for symbol in config.symbols:
                # Simulate news articles
                articles = [
                    {
                        'title': f'{symbol} Price Surges 10% on Positive Market Sentiment',
                        'content': f'{symbol} has seen significant price movement today with positive market sentiment driving the rally.',
                        'source': 'CryptoNews',
                        'timestamp': datetime.now(),
                        'url': f'https://example.com/news/{symbol.lower()}-surge'
                    },
                    {
                        'title': f'Analysts Predict {symbol} Will Continue Bullish Trend',
                        'content': f'Market analysts are optimistic about {symbol} future prospects based on recent developments.',
                        'source': 'MarketWatch',
                        'timestamp': datetime.now() - timedelta(hours=2),
                        'url': f'https://example.com/analysis/{symbol.lower()}-bullish'
                    }
                ]
                
                for article in articles:
                    # Analyze sentiment
                    sentiment_data = self.sentiment_analyzer.analyze_text_sentiment(
                        f"{article['title']} {article['content']}", symbol
                    )
                    
                    # Create data point
                    data_point = AlternativeDataPoint(
                        timestamp=article['timestamp'],
                        source=DataSource.NEWS,
                        symbol=symbol,
                        data_type='news_article',
                        value={
                            'title': article['title'],
                            'content': article['content'],
                            'source': article['source'],
                            'url': article['url'],
                            'sentiment': sentiment_data
                        },
                        metadata={
                            'word_count': len(article['content'].split()),
                            'has_sentiment': True
                        }
                    )
                    
                    news_data.append(data_point)
            
            # Store collected data
            self.collected_data.extend(news_data)
            
            # Update source status
            self.data_sources[DataSource.NEWS]['last_collection'] = datetime.now()
            self.data_sources[DataSource.NEWS]['collection_count'] += len(news_data)
            
            logger.info(f"Collected {len(news_data)} news articles")
            
            return {
                'status': 'success',
                'source': DataSource.NEWS.value,
                'data_points': len(news_data),
                'symbols': config.symbols,
                'message': f'Collected {len(news_data)} news articles'
            }
            
        except Exception as e:
            logger.error(f"Failed to collect news data: {e}")
            self.data_sources[DataSource.NEWS]['error_count'] += 1
            return {
                'status': 'error',
                'message': f'Failed to collect news data: {str(e)}'
            }
    
    async def collect_social_media_data(self, config: DataSourceConfig) -> Dict[str, Any]:
        """Collect social media data."""
        try:
            social_data = []
            
            for symbol in config.symbols:
                # Simulate social media posts
                posts = [
                    {
                        'text': f'Just bought more {symbol}! 🚀 To the moon! #crypto #bullish',
                        'platform': 'Twitter',
                        'author': 'CryptoTrader123',
                        'timestamp': datetime.now(),
                        'likes': 150,
                        'retweets': 25
                    },
                    {
                        'text': f'{symbol} looking bearish today. Might be time to sell. #bearish #crypto',
                        'platform': 'Reddit',
                        'author': 'BearMarketGuy',
                        'timestamp': datetime.now() - timedelta(hours=1),
                        'likes': 45,
                        'retweets': 8
                    },
                    {
                        'text': f'HODL {symbol}! Diamond hands! 💎🙌',
                        'platform': 'Telegram',
                        'author': 'DiamondHands',
                        'timestamp': datetime.now() - timedelta(minutes=30),
                        'likes': 200,
                        'retweets': 50
                    }
                ]
                
                for post in posts:
                    # Analyze sentiment
                    sentiment_data = self.sentiment_analyzer.analyze_text_sentiment(
                        post['text'], symbol
                    )
                    
                    # Create data point
                    data_point = AlternativeDataPoint(
                        timestamp=post['timestamp'],
                        source=DataSource.SOCIAL_MEDIA,
                        symbol=symbol,
                        data_type='social_post',
                        value={
                            'text': post['text'],
                            'platform': post['platform'],
                            'author': post['author'],
                            'engagement': {
                                'likes': post['likes'],
                                'retweets': post['retweets']
                            },
                            'sentiment': sentiment_data
                        },
                        metadata={
                            'has_emoji': '🚀' in post['text'] or '💎' in post['text'],
                            'has_hashtag': '#' in post['text'],
                            'engagement_score': post['likes'] + post['retweets'] * 2
                        }
                    )
                    
                    social_data.append(data_point)
            
            # Store collected data
            self.collected_data.extend(social_data)
            
            # Update source status
            self.data_sources[DataSource.SOCIAL_MEDIA]['last_collection'] = datetime.now()
            self.data_sources[DataSource.SOCIAL_MEDIA]['collection_count'] += len(social_data)
            
            logger.info(f"Collected {len(social_data)} social media posts")
            
            return {
                'status': 'success',
                'source': DataSource.SOCIAL_MEDIA.value,
                'data_points': len(social_data),
                'symbols': config.symbols,
                'message': f'Collected {len(social_data)} social media posts'
            }
            
        except Exception as e:
            logger.error(f"Failed to collect social media data: {e}")
            self.data_sources[DataSource.SOCIAL_MEDIA]['error_count'] += 1
            return {
                'status': 'error',
                'message': f'Failed to collect social media data: {str(e)}'
            }
    
    async def collect_on_chain_data(self, config: DataSourceConfig) -> Dict[str, Any]:
        """Collect on-chain data."""
        try:
            on_chain_data = []
            
            for symbol in config.symbols:
                # Simulate on-chain metrics
                metrics = {
                    'active_addresses': np.random.randint(10000, 100000),
                    'transaction_count': np.random.randint(50000, 500000),
                    'transaction_volume': np.random.uniform(1000000, 10000000),
                    'network_hash_rate': np.random.uniform(100, 1000),
                    'mining_difficulty': np.random.uniform(10, 100),
                    'whale_transactions': np.random.randint(10, 100),
                    'exchange_inflows': np.random.uniform(100000, 1000000),
                    'exchange_outflows': np.random.uniform(100000, 1000000)
                }
                
                # Create data point
                data_point = AlternativeDataPoint(
                    timestamp=datetime.now(),
                    source=DataSource.ON_CHAIN,
                    symbol=symbol,
                    data_type='on_chain_metrics',
                    value=metrics,
                    metadata={
                        'data_freshness': 'real_time',
                        'network_status': 'healthy'
                    }
                )
                
                on_chain_data.append(data_point)
            
            # Store collected data
            self.collected_data.extend(on_chain_data)
            
            # Update source status
            self.data_sources[DataSource.ON_CHAIN]['last_collection'] = datetime.now()
            self.data_sources[DataSource.ON_CHAIN]['collection_count'] += len(on_chain_data)
            
            logger.info(f"Collected {len(on_chain_data)} on-chain data points")
            
            return {
                'status': 'success',
                'source': DataSource.ON_CHAIN.value,
                'data_points': len(on_chain_data),
                'symbols': config.symbols,
                'message': f'Collected {len(on_chain_data)} on-chain data points'
            }
            
        except Exception as e:
            logger.error(f"Failed to collect on-chain data: {e}")
            self.data_sources[DataSource.ON_CHAIN]['error_count'] += 1
            return {
                'status': 'error',
                'message': f'Failed to collect on-chain data: {str(e)}'
            }
    
    async def collect_google_trends_data(self, config: DataSourceConfig) -> Dict[str, Any]:
        """Collect Google Trends data."""
        try:
            trends_data = []
            
            for symbol in config.symbols:
                # Simulate Google Trends data
                trends_metrics = {
                    'search_volume': np.random.randint(50, 100),
                    'related_queries': [
                        f'{symbol} price',
                        f'{symbol} news',
                        f'{symbol} prediction',
                        f'buy {symbol}',
                        f'{symbol} analysis'
                    ],
                    'rising_queries': [
                        f'{symbol} pump',
                        f'{symbol} moon',
                        f'{symbol} bullish'
                    ],
                    'geographic_data': {
                        'US': np.random.randint(20, 80),
                        'UK': np.random.randint(10, 50),
                        'Germany': np.random.randint(5, 30),
                        'Japan': np.random.randint(15, 60)
                    }
                }
                
                # Create data point
                data_point = AlternativeDataPoint(
                    timestamp=datetime.now(),
                    source=DataSource.GOOGLE_TRENDS,
                    symbol=symbol,
                    data_type='search_trends',
                    value=trends_metrics,
                    metadata={
                        'trend_direction': 'rising' if trends_metrics['search_volume'] > 75 else 'stable',
                        'interest_level': 'high' if trends_metrics['search_volume'] > 80 else 'medium'
                    }
                )
                
                trends_data.append(data_point)
            
            # Store collected data
            self.collected_data.extend(trends_data)
            
            # Update source status
            self.data_sources[DataSource.GOOGLE_TRENDS]['last_collection'] = datetime.now()
            self.data_sources[DataSource.GOOGLE_TRENDS]['collection_count'] += len(trends_data)
            
            logger.info(f"Collected {len(trends_data)} Google Trends data points")
            
            return {
                'status': 'success',
                'source': DataSource.GOOGLE_TRENDS.value,
                'data_points': len(trends_data),
                'symbols': config.symbols,
                'message': f'Collected {len(trends_data)} Google Trends data points'
            }
            
        except Exception as e:
            logger.error(f"Failed to collect Google Trends data: {e}")
            self.data_sources[DataSource.GOOGLE_TRENDS]['error_count'] += 1
            return {
                'status': 'error',
                'message': f'Failed to collect Google Trends data: {str(e)}'
            }
    
    async def collect_all_data(self, configs: List[DataSourceConfig]) -> Dict[str, Any]:
        """Collect data from all configured sources."""
        try:
            results = {}
            
            for config in configs:
                if config.source == DataSource.NEWS:
                    result = await self.collect_news_data(config)
                elif config.source == DataSource.SOCIAL_MEDIA:
                    result = await self.collect_social_media_data(config)
                elif config.source == DataSource.ON_CHAIN:
                    result = await self.collect_on_chain_data(config)
                elif config.source == DataSource.GOOGLE_TRENDS:
                    result = await self.collect_google_trends_data(config)
                else:
                    result = {
                        'status': 'error',
                        'message': f'Data source {config.source.value} not implemented'
                    }
                
                results[config.source.value] = result
            
            # Calculate summary
            total_data_points = sum(
                result.get('data_points', 0) for result in results.values()
                if result.get('status') == 'success'
            )
            
            successful_sources = sum(
                1 for result in results.values()
                if result.get('status') == 'success'
            )
            
            return {
                'status': 'success',
                'results': results,
                'total_data_points': total_data_points,
                'successful_sources': successful_sources,
                'total_sources': len(configs),
                'message': f'Collected {total_data_points} data points from {successful_sources}/{len(configs)} sources'
            }
            
        except Exception as e:
            logger.error(f"Failed to collect all data: {e}")
            return {
                'status': 'error',
                'message': f'Failed to collect all data: {str(e)}'
            }
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of collected data."""
        try:
            # Group data by source
            data_by_source = {}
            for data_point in self.collected_data:
                source = data_point.source.value
                if source not in data_by_source:
                    data_by_source[source] = []
                data_by_source[source].append(data_point)
            
            # Calculate statistics
            summary = {
                'total_data_points': len(self.collected_data),
                'data_by_source': {},
                'time_range': {},
                'sentiment_summary': {}
            }
            
            for source, data_points in data_by_source.items():
                if data_points:
                    timestamps = [dp.timestamp for dp in data_points]
                    summary['data_by_source'][source] = {
                        'count': len(data_points),
                        'latest': max(timestamps).isoformat(),
                        'oldest': min(timestamps).isoformat()
                    }
            
            # Overall time range
            if self.collected_data:
                all_timestamps = [dp.timestamp for dp in self.collected_data]
                summary['time_range'] = {
                    'start': min(all_timestamps).isoformat(),
                    'end': max(all_timestamps).isoformat(),
                    'duration_hours': (max(all_timestamps) - min(all_timestamps)).total_seconds() / 3600
                }
            
            # Sentiment summary
            sentiment_data = [dp for dp in self.collected_data if hasattr(dp.value, 'sentiment')]
            if sentiment_data:
                sentiment_scores = [dp.value.sentiment.sentiment_score for dp in sentiment_data]
                summary['sentiment_summary'] = {
                    'total_sentiments': len(sentiment_data),
                    'average_sentiment': np.mean(sentiment_scores),
                    'sentiment_std': np.std(sentiment_scores)
                }
            
            return {
                'status': 'success',
                'summary': summary,
                'message': f'Retrieved summary for {len(self.collected_data)} data points'
            }
            
        except Exception as e:
            logger.error(f"Failed to get data summary: {e}")
            return {
                'status': 'error',
                'message': f'Failed to get data summary: {str(e)}'
            }

# Example usage and testing
async def test_alternative_data_sources():
    """Test alternative data sources and sentiment analysis."""
    print("🧪 Testing Alternative Data Sources and Sentiment Analysis...")
    
    # Create data collector
    data_collector = AlternativeDataCollector()
    
    # Initialize
    init_result = await data_collector.initialize()
    if init_result['status'] == 'success':
        print(f"  • Data collector initialized: ✅")
        print(f"    - Data sources: {init_result['data_sources']}")
    else:
        print(f"  • Data collector initialization: ❌ {init_result['message']}")
        return None
    
    # Test sentiment analysis
    print("  • Testing sentiment analysis...")
    
    test_texts = [
        "Bitcoin is going to the moon! 🚀 HODL!",
        "Market crash incoming, sell everything!",
        "BTC price is stable today, no major movements.",
        "Ethereum is looking very bullish, diamond hands! 💎🙌",
        "This is a scam, rug pull incoming!"
    ]
    
    for i, text in enumerate(test_texts):
        sentiment_data = data_collector.sentiment_analyzer.analyze_text_sentiment(text, "BTC")
        print(f"    ✅ Text {i+1}: {sentiment_data.sentiment_type.value} (score: {sentiment_data.sentiment_score:.3f}, confidence: {sentiment_data.confidence:.3f})")
    
    # Test data collection
    print("  • Testing data collection...")
    
    # Create data source configurations
    configs = [
        DataSourceConfig(
            source=DataSource.NEWS,
            frequency=DataFrequency.HOUR,
            symbols=['BTC', 'ETH', 'ADA'],
            keywords=['crypto', 'bitcoin', 'ethereum']
        ),
        DataSourceConfig(
            source=DataSource.SOCIAL_MEDIA,
            frequency=DataFrequency.MINUTE,
            symbols=['BTC', 'ETH'],
            keywords=['#crypto', '#bitcoin', '#ethereum']
        ),
        DataSourceConfig(
            source=DataSource.ON_CHAIN,
            frequency=DataFrequency.HOUR,
            symbols=['BTC', 'ETH'],
            keywords=[]
        ),
        DataSourceConfig(
            source=DataSource.GOOGLE_TRENDS,
            frequency=DataFrequency.DAILY,
            symbols=['BTC', 'ETH', 'ADA'],
            keywords=['bitcoin', 'ethereum', 'cardano']
        )
    ]
    
    # Collect data from all sources
    collection_result = await data_collector.collect_all_data(configs)
    
    if collection_result['status'] == 'success':
        print(f"  • Data collection: ✅")
        print(f"    - Total data points: {collection_result['total_data_points']}")
        print(f"    - Successful sources: {collection_result['successful_sources']}/{collection_result['total_sources']}")
        
        # Show results for each source
        for source, result in collection_result['results'].items():
            if result['status'] == 'success':
                print(f"      ✅ {source}: {result['data_points']} data points")
            else:
                print(f"      ❌ {source}: {result['message']}")
    else:
        print(f"  • Data collection: ❌ {collection_result['message']}")
    
    # Test sentiment summary
    print("  • Testing sentiment summary...")
    
    sentiment_summary = data_collector.sentiment_analyzer.get_sentiment_summary("BTC", hours=24)
    if sentiment_summary['total_sentiments'] > 0:
        print(f"    ✅ BTC sentiment summary:")
        print(f"        - Total sentiments: {sentiment_summary['total_sentiments']}")
        print(f"        - Average sentiment: {sentiment_summary['average_sentiment']:.3f}")
        print(f"        - Confidence: {sentiment_summary['confidence']:.3f}")
        print(f"        - Distribution: {sentiment_summary['sentiment_distribution']}")
    else:
        print(f"    ⚠️ No sentiment data available for BTC")
    
    # Test data summary
    print("  • Testing data summary...")
    
    summary_result = data_collector.get_data_summary()
    if summary_result['status'] == 'success':
        print(f"    ✅ Data summary:")
        summary = summary_result['summary']
        print(f"        - Total data points: {summary['total_data_points']}")
        print(f"        - Data sources: {len(summary['data_by_source'])}")
        
        for source, stats in summary['data_by_source'].items():
            print(f"        - {source}: {stats['count']} points")
        
        if summary['sentiment_summary']:
            sent_summary = summary['sentiment_summary']
            print(f"        - Sentiment: {sent_summary['total_sentiments']} sentiments, avg: {sent_summary['average_sentiment']:.3f}")
    else:
        print(f"    ❌ Data summary: {summary_result['message']}")
    
    print("✅ Alternative Data Sources and Sentiment Analysis test completed!")
    
    return data_collector

if __name__ == "__main__":
    asyncio.run(test_alternative_data_sources())
