#!/usr/bin/env python3
"""
Natural Language Processing Module
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any, Optional
import uuid
import re


class TextCategory(Enum):
    """Text category enumeration"""
    NEWS = "news"
    SOCIAL_MEDIA = "social_media"
    FINANCIAL_REPORT = "financial_report"
    RESEARCH = "research"


class SentimentType(Enum):
    """Sentiment type enumeration"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class EntityType(Enum):
    """Entity type enumeration"""
    COMPANY = "company"
    PERSON = "person"
    CURRENCY = "currency"
    LOCATION = "location"


@dataclass
class SentimentAnalysis:
    """Sentiment analysis result"""
    sentiment_type: SentimentType
    polarity: float
    subjectivity: float


@dataclass
class Entity:
    """Named entity"""
    text: str
    entity_type: EntityType
    confidence: float


@dataclass
class DocumentAnalysis:
    """Document analysis result"""
    document_id: str
    sentiment: SentimentAnalysis
    entities: List[Entity]
    topics: List[str]
    keywords: List[str]
    language: str


class NLPAnalyticsManager:
    """NLP analytics manager"""
    
    def __init__(self):
        self.models = {}
        self.analysis_results = {}
        self.config = {
            'default_language': 'en',
            'confidence_threshold': 0.6,
            'max_keywords': 10
        }
    
    def process_document(self, text: str, source: str, category: TextCategory, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a document with NLP"""
        try:
            document_id = str(uuid.uuid4())
            
            # Simple sentiment analysis (mock)
            positive_words = ['strong', 'good', 'profit', 'growth', 'optimism', 'surge', 'beat']
            negative_words = ['loss', 'decline', 'fall', 'weak', 'concern', 'drop']
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            if positive_count > negative_count:
                sentiment_type = SentimentType.POSITIVE
                polarity = 0.3 + (positive_count - negative_count) * 0.1
            elif negative_count > positive_count:
                sentiment_type = SentimentType.NEGATIVE
                polarity = -0.3 - (negative_count - positive_count) * 0.1
            else:
                sentiment_type = SentimentType.NEUTRAL
                polarity = 0.0
            
            sentiment = SentimentAnalysis(
                sentiment_type=sentiment_type,
                polarity=polarity,
                subjectivity=0.6
            )
            
            # Simple entity extraction (mock)
            entities = []
            
            # Look for company names (simple pattern matching)
            company_patterns = [r'\b[A-Z][a-z]+ Inc\b', r'\b[A-Z][a-z]+ Corp\b', r'\bApple\b', r'\bMicrosoft\b']
            for pattern in company_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    entities.append(Entity(
                        text=match,
                        entity_type=EntityType.COMPANY,
                        confidence=0.9
                    ))
            
            # Look for currencies
            currency_patterns = [r'\bUSD\b', r'\bEUR\b', r'\bGBP\b', r'\$']
            for pattern in currency_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    entities.append(Entity(
                        text=match,
                        entity_type=EntityType.CURRENCY,
                        confidence=0.8
                    ))
            
            # Simple keyword extraction
            words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
            word_freq = {}
            for word in words:
                if word not in ['this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'said']:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            keywords = [word for word, freq in keywords]
            
            # Simple topic modeling (mock)
            topics = []
            if any(word in text_lower for word in ['earnings', 'revenue', 'profit']):
                topics.append('earnings')
            if any(word in text_lower for word in ['stock', 'price', 'trading']):
                topics.append('trading')
            if any(word in text_lower for word in ['growth', 'expansion']):
                topics.append('growth')
            
            analysis_result = DocumentAnalysis(
                document_id=document_id,
                sentiment=sentiment,
                entities=entities,
                topics=topics,
                keywords=keywords,
                language='en'
            )
            
            self.analysis_results[document_id] = {
                'text': text,
                'source': source,
                'category': category.value,
                'metadata': metadata or {},
                'analysis': analysis_result
            }
            
            return {
                'status': 'success',
                'document_id': document_id,
                'analysis_result': analysis_result
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_sentiment_summary(self) -> Dict[str, Any]:
        """Get sentiment summary"""
        try:
            if not self.analysis_results:
                return {
                    'status': 'success',
                    'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0},
                    'average_polarity': 0.0,
                    'overall_sentiment': 'neutral'
                }
            
            sentiments = [result['analysis'].sentiment for result in self.analysis_results.values()]
            
            sentiment_counts = {
                'positive': sum(1 for s in sentiments if s.sentiment_type == SentimentType.POSITIVE),
                'negative': sum(1 for s in sentiments if s.sentiment_type == SentimentType.NEGATIVE),
                'neutral': sum(1 for s in sentiments if s.sentiment_type == SentimentType.NEUTRAL)
            }
            
            avg_polarity = sum(s.polarity for s in sentiments) / len(sentiments)
            
            overall_sentiment = 'positive' if avg_polarity > 0.1 else 'negative' if avg_polarity < -0.1 else 'neutral'
            
            return {
                'status': 'success',
                'sentiment_distribution': sentiment_counts,
                'average_polarity': avg_polarity,
                'overall_sentiment': overall_sentiment
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_entity_analysis(self, entity_type: EntityType = None) -> Dict[str, Any]:
        """Get entity analysis"""
        try:
            all_entities = []
            for result in self.analysis_results.values():
                entities = result['analysis'].entities
                if entity_type:
                    entities = [e for e in entities if e.entity_type == entity_type]
                all_entities.extend(entities)
            
            entity_freq = {}
            for entity in all_entities:
                entity_freq[entity.text] = entity_freq.get(entity.text, 0) + 1
            
            most_frequent = sorted(entity_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                'status': 'success',
                'total_entities': len(all_entities),
                'unique_entities': len(entity_freq),
                'most_frequent_entities': [entity for entity, freq in most_frequent]
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_nlp_summary(self) -> Dict[str, Any]:
        """Get NLP summary"""
        categories = list(set([result['category'] for result in self.analysis_results.values()]))
        languages = list(set([result['analysis'].language for result in self.analysis_results.values()]))
        
        return {
            'total_documents': len(self.analysis_results),
            'analysis_results': len(self.analysis_results),
            'document_categories': categories,
            'languages': languages
        }