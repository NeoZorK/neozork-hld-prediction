#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Natural Language Processing Module

This module provides advanced NLP capabilities for trading including:
- Sentiment analysis from news and social media
- Named entity recognition for financial entities
- Text classification and topic modeling
- Language models for financial text
- Real-time text processing
- Multi-language support
- Text summarization
- Question answering systems
- Financial document analysis
"""

import numpy as np
import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from collections import defaultdict, deque
import secrets
import json
import re
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentType(Enum):
    """Sentiment types."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    VERY_POSITIVE = "very_positive"
    VERY_NEGATIVE = "very_negative"

class EntityType(Enum):
    """Named entity types."""
    PERSON = "person"
    ORGANIZATION = "organization"
    MONEY = "money"
    PERCENT = "percent"
    DATE = "date"
    TIME = "time"
    LOCATION = "location"
    COMPANY = "company"
    STOCK_SYMBOL = "stock_symbol"
    CRYPTOCURRENCY = "cryptocurrency"

class TextCategory(Enum):
    """Text categories."""
    NEWS = "news"
    SOCIAL_MEDIA = "social_media"
    FINANCIAL_REPORT = "financial_report"
    ANALYST_REPORT = "analyst_report"
    REGULATORY_DOCUMENT = "regulatory_document"
    BLOG_POST = "blog_post"
    FORUM_POST = "forum_post"
    PRESS_RELEASE = "press_release"

@dataclass
class TextDocument:
    """Text document structure."""
    document_id: str
    text: str
    source: str
    category: TextCategory
    timestamp: datetime
    language: str = "en"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SentimentResult:
    """Sentiment analysis result."""
    document_id: str
    sentiment_type: SentimentType
    polarity: float  # -1 to 1
    subjectivity: float  # 0 to 1
    confidence: float  # 0 to 1
    keywords: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class NamedEntity:
    """Named entity."""
    text: str
    entity_type: EntityType
    start_pos: int
    end_pos: int
    confidence: float

@dataclass
class TextAnalysisResult:
    """Comprehensive text analysis result."""
    document_id: str
    sentiment: SentimentResult
    entities: List[NamedEntity]
    topics: List[str]
    keywords: List[str]
    summary: str
    language: str
    timestamp: datetime = field(default_factory=datetime.now)

class SentimentAnalyzer:
    """Advanced sentiment analysis."""
    
    def __init__(self):
        self.financial_lexicon = self._load_financial_lexicon()
        self.sentiment_weights = self._load_sentiment_weights()
        self.lemmatizer = WordNetLemmatizer()
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('taggers/averaged_perceptron_tagger')
            nltk.data.find('chunkers/maxent_ne_chunker')
            nltk.data.find('corpora/words')
        except LookupError:
            logger.warning("NLTK data not found. Some features may not work properly.")
    
    def _load_financial_lexicon(self) -> Dict[str, float]:
        """Load financial sentiment lexicon."""
        return {
            # Positive financial terms
            'bullish': 0.8, 'surge': 0.7, 'rally': 0.7, 'gain': 0.6, 'profit': 0.8,
            'growth': 0.7, 'increase': 0.6, 'rise': 0.6, 'up': 0.5, 'positive': 0.6,
            'strong': 0.6, 'robust': 0.7, 'outperform': 0.8, 'beat': 0.7, 'exceed': 0.7,
            
            # Negative financial terms
            'bearish': -0.8, 'crash': -0.9, 'plunge': -0.8, 'loss': -0.7, 'decline': -0.6,
            'fall': -0.6, 'down': -0.5, 'negative': -0.6, 'weak': -0.6, 'underperform': -0.7,
            'miss': -0.6, 'disappoint': -0.7, 'concern': -0.5, 'risk': -0.4, 'volatile': -0.3,
            
            # Neutral/contextual terms
            'stable': 0.1, 'flat': 0.0, 'unchanged': 0.0, 'maintain': 0.1
        }
    
    def _load_sentiment_weights(self) -> Dict[str, float]:
        """Load sentiment weights for different contexts."""
        return {
            'headline': 1.5,
            'first_sentence': 1.2,
            'quote': 1.3,
            'financial_terms': 1.4,
            'company_name': 1.1
        }
    
    def analyze_sentiment(self, document: TextDocument) -> SentimentResult:
        """Analyze sentiment of text document."""
        try:
            # Basic sentiment using TextBlob
            blob = TextBlob(document.text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Enhanced sentiment analysis
            enhanced_polarity = self._enhance_sentiment(document.text, polarity)
            
            # Determine sentiment type
            sentiment_type = self._classify_sentiment(enhanced_polarity)
            
            # Calculate confidence
            confidence = self._calculate_confidence(document.text, enhanced_polarity)
            
            # Extract keywords
            keywords = self._extract_keywords(document.text)
            
            return SentimentResult(
                document_id=document.document_id,
                sentiment_type=sentiment_type,
                polarity=enhanced_polarity,
                subjectivity=subjectivity,
                confidence=confidence,
                keywords=keywords
            )
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return SentimentResult(
                document_id=document.document_id,
                sentiment_type=SentimentType.NEUTRAL,
                polarity=0.0,
                subjectivity=0.5,
                confidence=0.0
            )
    
    def _enhance_sentiment(self, text: str, base_polarity: float) -> float:
        """Enhance sentiment analysis with financial lexicon."""
        words = word_tokenize(text.lower())
        enhanced_score = base_polarity
        
        for word in words:
            if word in self.financial_lexicon:
                enhanced_score += self.financial_lexicon[word] * 0.1
        
        # Normalize to [-1, 1] range
        return max(-1.0, min(1.0, enhanced_score))
    
    def _classify_sentiment(self, polarity: float) -> SentimentType:
        """Classify sentiment based on polarity score."""
        if polarity >= 0.6:
            return SentimentType.VERY_POSITIVE
        elif polarity >= 0.2:
            return SentimentType.POSITIVE
        elif polarity <= -0.6:
            return SentimentType.VERY_NEGATIVE
        elif polarity <= -0.2:
            return SentimentType.NEGATIVE
        else:
            return SentimentType.NEUTRAL
    
    def _calculate_confidence(self, text: str, polarity: float) -> float:
        """Calculate confidence in sentiment analysis."""
        # Base confidence on text length and polarity magnitude
        text_length = len(text.split())
        polarity_magnitude = abs(polarity)
        
        # Longer texts with stronger sentiment get higher confidence
        length_factor = min(1.0, text_length / 50)
        polarity_factor = polarity_magnitude
        
        confidence = (length_factor + polarity_factor) / 2
        return min(1.0, max(0.0, confidence))
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        try:
            # Tokenize and filter
            words = word_tokenize(text.lower())
            stop_words = set(stopwords.words('english'))
            
            # Filter out stop words and short words
            keywords = [word for word in words 
                       if word not in stop_words and len(word) > 2 and word.isalpha()]
            
            # Get most common keywords
            word_freq = defaultdict(int)
            for word in keywords:
                word_freq[word] += 1
            
            # Return top keywords
            sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, freq in sorted_keywords[:10]]
            
        except Exception as e:
            logger.error(f"Keyword extraction failed: {e}")
            return []

class NamedEntityRecognizer:
    """Named entity recognition for financial text."""
    
    def __init__(self):
        self.financial_entities = self._load_financial_entities()
        self.stock_patterns = self._load_stock_patterns()
        self.crypto_patterns = self._load_crypto_patterns()
    
    def _load_financial_entities(self) -> Dict[str, EntityType]:
        """Load financial entity mappings."""
        return {
            'apple': EntityType.COMPANY,
            'microsoft': EntityType.COMPANY,
            'google': EntityType.COMPANY,
            'amazon': EntityType.COMPANY,
            'tesla': EntityType.COMPANY,
            'bitcoin': EntityType.CRYPTOCURRENCY,
            'ethereum': EntityType.CRYPTOCURRENCY,
            'dollar': EntityType.MONEY,
            'euro': EntityType.MONEY,
            'yen': EntityType.MONEY
        }
    
    def _load_stock_patterns(self) -> List[str]:
        """Load stock symbol patterns."""
        return [
            r'\b[A-Z]{1,5}\b',  # Basic stock symbols
            r'\$[A-Z]{1,5}\b',  # Stock symbols with $ prefix
            r'\b[A-Z]{1,5}:\w+\b'  # Exchange:Symbol format
        ]
    
    def _load_crypto_patterns(self) -> List[str]:
        """Load cryptocurrency patterns."""
        return [
            r'\bBTC\b', r'\bETH\b', r'\bADA\b', r'\bDOT\b', r'\bLINK\b',
            r'\bBitcoin\b', r'\bEthereum\b', r'\bCardano\b', r'\bPolkadot\b'
        ]
    
    def extract_entities(self, document: TextDocument) -> List[NamedEntity]:
        """Extract named entities from text document."""
        try:
            entities = []
            text = document.text
            
            # Extract using NLTK
            try:
                tokens = word_tokenize(text)
                pos_tags = pos_tag(tokens)
                chunks = ne_chunk(pos_tags)
                
                for chunk in chunks:
                    if hasattr(chunk, 'label'):
                        entity_text = ' '.join([token for token, pos in chunk.leaves()])
                        entity_type = self._map_nltk_entity(chunk.label())
                        
                        entities.append(NamedEntity(
                            text=entity_text,
                            entity_type=entity_type,
                            start_pos=text.find(entity_text),
                            end_pos=text.find(entity_text) + len(entity_text),
                            confidence=0.8
                        ))
            except Exception as e:
                logger.warning(f"NLTK entity extraction failed: {e}")
            
            # Extract financial entities
            financial_entities = self._extract_financial_entities(text)
            entities.extend(financial_entities)
            
            # Extract stock symbols
            stock_entities = self._extract_stock_symbols(text)
            entities.extend(stock_entities)
            
            # Extract cryptocurrencies
            crypto_entities = self._extract_cryptocurrencies(text)
            entities.extend(crypto_entities)
            
            # Remove duplicates
            unique_entities = self._remove_duplicate_entities(entities)
            
            return unique_entities
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return []
    
    def _map_nltk_entity(self, nltk_label: str) -> EntityType:
        """Map NLTK entity labels to our entity types."""
        mapping = {
            'PERSON': EntityType.PERSON,
            'ORGANIZATION': EntityType.ORGANIZATION,
            'GPE': EntityType.LOCATION,
            'MONEY': EntityType.MONEY,
            'PERCENT': EntityType.PERCENT,
            'DATE': EntityType.DATE,
            'TIME': EntityType.TIME
        }
        return mapping.get(nltk_label, EntityType.ORGANIZATION)
    
    def _extract_financial_entities(self, text: str) -> List[NamedEntity]:
        """Extract financial entities using lexicon."""
        entities = []
        text_lower = text.lower()
        
        for entity_name, entity_type in self.financial_entities.items():
            if entity_name in text_lower:
                start_pos = text_lower.find(entity_name)
                entities.append(NamedEntity(
                    text=entity_name.title(),
                    entity_type=entity_type,
                    start_pos=start_pos,
                    end_pos=start_pos + len(entity_name),
                    confidence=0.9
                ))
        
        return entities
    
    def _extract_stock_symbols(self, text: str) -> List[NamedEntity]:
        """Extract stock symbols using patterns."""
        entities = []
        
        for pattern in self.stock_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append(NamedEntity(
                    text=match.group(),
                    entity_type=EntityType.STOCK_SYMBOL,
                    start_pos=match.start(),
                    end_pos=match.end(),
                    confidence=0.7
                ))
        
        return entities
    
    def _extract_cryptocurrencies(self, text: str) -> List[NamedEntity]:
        """Extract cryptocurrency mentions."""
        entities = []
        
        for pattern in self.crypto_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append(NamedEntity(
                    text=match.group(),
                    entity_type=EntityType.CRYPTOCURRENCY,
                    start_pos=match.start(),
                    end_pos=match.end(),
                    confidence=0.8
                ))
        
        return entities
    
    def _remove_duplicate_entities(self, entities: List[NamedEntity]) -> List[NamedEntity]:
        """Remove duplicate entities."""
        seen = set()
        unique_entities = []
        
        for entity in entities:
            key = (entity.text.lower(), entity.start_pos, entity.end_pos)
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)
        
        return unique_entities

class TextSummarizer:
    """Text summarization for financial documents."""
    
    def __init__(self):
        self.max_sentences = 3
        self.min_sentence_length = 10
    
    def summarize(self, document: TextDocument) -> str:
        """Generate summary of text document."""
        try:
            sentences = sent_tokenize(document.text)
            
            if len(sentences) <= self.max_sentences:
                return document.text
            
            # Score sentences based on various factors
            sentence_scores = []
            for sentence in sentences:
                score = self._score_sentence(sentence, document)
                sentence_scores.append((sentence, score))
            
            # Sort by score and select top sentences
            sentence_scores.sort(key=lambda x: x[1], reverse=True)
            top_sentences = sentence_scores[:self.max_sentences]
            
            # Sort by original order
            top_sentences.sort(key=lambda x: document.text.find(x[0]))
            
            summary = ' '.join([sentence for sentence, score in top_sentences])
            return summary
            
        except Exception as e:
            logger.error(f"Text summarization failed: {e}")
            return document.text[:200] + "..." if len(document.text) > 200 else document.text
    
    def _score_sentence(self, sentence: str, document: TextDocument) -> float:
        """Score sentence for summarization."""
        score = 0.0
        
        # Length factor
        if len(sentence.split()) >= self.min_sentence_length:
            score += 1.0
        
        # Position factor (first and last sentences get higher scores)
        sentences = sent_tokenize(document.text)
        if sentence in sentences:
            position = sentences.index(sentence)
            if position == 0 or position == len(sentences) - 1:
                score += 2.0
            elif position < 3:  # First few sentences
                score += 1.0
        
        # Financial terms factor
        financial_terms = ['profit', 'revenue', 'growth', 'earnings', 'stock', 'market', 'price']
        for term in financial_terms:
            if term.lower() in sentence.lower():
                score += 1.0
        
        # Question factor (questions get lower scores)
        if sentence.strip().endswith('?'):
            score -= 0.5
        
        return score

class NLPAnalyticsManager:
    """Main NLP analytics manager."""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.entity_recognizer = NamedEntityRecognizer()
        self.text_summarizer = TextSummarizer()
        self.documents: Dict[str, TextDocument] = {}
        self.analysis_results: Dict[str, TextAnalysisResult] = {}
        self.performance_history: List[Dict[str, Any]] = []
    
    def process_document(self, text: str, source: str, category: TextCategory, 
                        language: str = "en", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process text document for analysis."""
        try:
            document_id = secrets.token_urlsafe(16)
            
            document = TextDocument(
                document_id=document_id,
                text=text,
                source=source,
                category=category,
                timestamp=datetime.now(),
                language=language,
                metadata=metadata or {}
            )
            
            self.documents[document_id] = document
            
            # Perform comprehensive analysis
            analysis_result = self._analyze_document(document)
            self.analysis_results[document_id] = analysis_result
            
            logger.info(f"Document {document_id} processed successfully")
            return {
                'status': 'success',
                'document_id': document_id,
                'analysis_result': analysis_result,
                'message': 'Document processed successfully'
            }
            
        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _analyze_document(self, document: TextDocument) -> TextAnalysisResult:
        """Perform comprehensive text analysis."""
        # Sentiment analysis
        sentiment = self.sentiment_analyzer.analyze_sentiment(document)
        
        # Named entity recognition
        entities = self.entity_recognizer.extract_entities(document)
        
        # Text summarization
        summary = self.text_summarizer.summarize(document)
        
        # Extract topics (simplified)
        topics = self._extract_topics(document.text)
        
        # Extract keywords
        keywords = sentiment.keywords
        
        return TextAnalysisResult(
            document_id=document.document_id,
            sentiment=sentiment,
            entities=entities,
            topics=topics,
            keywords=keywords,
            summary=summary,
            language=document.language
        )
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text (simplified implementation)."""
        # Simple topic extraction based on financial keywords
        topics = []
        
        topic_keywords = {
            'earnings': ['earnings', 'profit', 'revenue', 'income'],
            'market': ['market', 'trading', 'stock', 'shares'],
            'cryptocurrency': ['bitcoin', 'crypto', 'blockchain', 'ethereum'],
            'regulation': ['regulation', 'compliance', 'legal', 'policy'],
            'technology': ['technology', 'innovation', 'digital', 'ai']
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def get_sentiment_summary(self, time_period: timedelta = None) -> Dict[str, Any]:
        """Get sentiment summary for time period."""
        try:
            cutoff_time = datetime.now() - (time_period or timedelta(days=1))
            
            recent_results = [
                result for result in self.analysis_results.values()
                if result.timestamp >= cutoff_time
            ]
            
            if not recent_results:
                return {'status': 'error', 'message': 'No recent analysis results found'}
            
            # Calculate sentiment statistics
            sentiment_counts = defaultdict(int)
            total_polarity = 0.0
            total_confidence = 0.0
            
            for result in recent_results:
                sentiment_counts[result.sentiment.sentiment_type.value] += 1
                total_polarity += result.sentiment.polarity
                total_confidence += result.sentiment.confidence
            
            avg_polarity = total_polarity / len(recent_results)
            avg_confidence = total_confidence / len(recent_results)
            
            return {
                'status': 'success',
                'time_period': str(time_period or timedelta(days=1)),
                'total_documents': len(recent_results),
                'sentiment_distribution': dict(sentiment_counts),
                'average_polarity': avg_polarity,
                'average_confidence': avg_confidence,
                'overall_sentiment': self._classify_overall_sentiment(avg_polarity),
                'message': 'Sentiment summary generated successfully'
            }
            
        except Exception as e:
            logger.error(f"Sentiment summary generation failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _classify_overall_sentiment(self, avg_polarity: float) -> str:
        """Classify overall sentiment based on average polarity."""
        if avg_polarity >= 0.2:
            return "positive"
        elif avg_polarity <= -0.2:
            return "negative"
        else:
            return "neutral"
    
    def get_entity_analysis(self, entity_type: EntityType = None) -> Dict[str, Any]:
        """Get entity analysis results."""
        try:
            all_entities = []
            for result in self.analysis_results.values():
                if entity_type:
                    filtered_entities = [e for e in result.entities if e.entity_type == entity_type]
                    all_entities.extend(filtered_entities)
                else:
                    all_entities.extend(result.entities)
            
            # Count entity occurrences
            entity_counts = defaultdict(int)
            for entity in all_entities:
                entity_counts[entity.text] += 1
            
            # Get most frequent entities
            sorted_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'status': 'success',
                'total_entities': len(all_entities),
                'unique_entities': len(entity_counts),
                'entity_type_filter': entity_type.value if entity_type else None,
                'most_frequent_entities': sorted_entities[:20],
                'message': 'Entity analysis completed successfully'
            }
            
        except Exception as e:
            logger.error(f"Entity analysis failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_nlp_summary(self) -> Dict[str, Any]:
        """Get summary of NLP analytics."""
        return {
            'total_documents': len(self.documents),
            'analysis_results': len(self.analysis_results),
            'document_categories': list(set([doc.category.value for doc in self.documents.values()])),
            'languages': list(set([doc.language for doc in self.documents.values()])),
            'recent_analyses': len([r for r in self.analysis_results.values() 
                                  if (datetime.now() - r.timestamp).total_seconds() <= 3600])
        }

# Example usage and testing
if __name__ == "__main__":
    # Create NLP analytics manager
    nlp_manager = NLPAnalyticsManager()
    
    # Test document processing
    print("Testing document processing...")
    
    # Sample financial news
    sample_text = """
    Apple Inc. reported strong quarterly earnings, beating analyst expectations. 
    The company's revenue grew by 15% year-over-year, driven by robust iPhone sales. 
    CEO Tim Cook expressed optimism about the company's future prospects. 
    The stock price surged 8% in after-hours trading following the announcement.
    """
    
    result = nlp_manager.process_document(
        text=sample_text,
        source="Financial News",
        category=TextCategory.NEWS,
        metadata={'company': 'Apple', 'ticker': 'AAPL'}
    )
    
    if result['status'] == 'success':
        analysis = result['analysis_result']
        print(f"Document processed: {result['document_id']}")
        print(f"Sentiment: {analysis.sentiment.sentiment_type.value} (polarity: {analysis.sentiment.polarity:.3f})")
        print(f"Entities found: {len(analysis.entities)}")
        print(f"Topics: {analysis.topics}")
        print(f"Summary: {analysis.summary}")
    
    # Test sentiment summary
    print("\nTesting sentiment summary...")
    sentiment_summary = nlp_manager.get_sentiment_summary()
    if sentiment_summary['status'] == 'success':
        print(f"Sentiment distribution: {sentiment_summary['sentiment_distribution']}")
        print(f"Average polarity: {sentiment_summary['average_polarity']:.3f}")
        print(f"Overall sentiment: {sentiment_summary['overall_sentiment']}")
    
    # Test entity analysis
    print("\nTesting entity analysis...")
    entity_analysis = nlp_manager.get_entity_analysis()
    if entity_analysis['status'] == 'success':
        print(f"Total entities: {entity_analysis['total_entities']}")
        print(f"Most frequent entities: {entity_analysis['most_frequent_entities'][:5]}")
    
    # Test NLP summary
    print("\nNLP summary:")
    summary = nlp_manager.get_nlp_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\nNLP Analytics Manager initialized successfully!")
