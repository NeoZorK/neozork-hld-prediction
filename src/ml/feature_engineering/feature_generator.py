# -*- coding: utf-8 -*-
# src/ml/feature_engineering/feature_generator.py

"""
Main feature generator for NeoZorK HLD Prediction.

This module orchestrates the generation of all types of features:
- Proprietary PHLD and Wave features
- Technical indicator features
- Statistical features
- Temporal features
- Cross-timeframe features
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass
import time

from .base_feature_generator import BaseFeatureGenerator, FeatureConfig
from .proprietary_features import ProprietaryFeatureGenerator, ProprietaryFeatureConfig
from .technical_features import TechnicalFeatureGenerator, TechnicalFeatureConfig
from .statistical_features import StatisticalFeatureGenerator, StatisticalFeatureConfig
from .temporal_features import TemporalFeatureGenerator, TemporalFeatureConfig
from .cross_timeframe_features import CrossTimeframeFeatureGenerator, CrossTimeframeFeatureConfig
from .feature_selector import FeatureSelector, FeatureSelectionConfig
from .logger import logger


@dataclass
class MasterFeatureConfig:
    """Master configuration for all feature generators."""
    
    # Enable/disable different feature types
    enable_proprietary: bool = True
    enable_technical: bool = True
    enable_statistical: bool = True
    enable_temporal: bool = True
    enable_cross_timeframe: bool = True
    
    # Feature selection settings
    max_features: int = 200
    min_importance: float = 0.3
    correlation_threshold: float = 0.95
    
    # Performance settings
    parallel_processing: bool = False
    memory_limit_gb: float = 8.0
    
    # Individual generator configs
    proprietary_config: ProprietaryFeatureConfig = None
    technical_config: TechnicalFeatureConfig = None
    statistical_config: StatisticalFeatureConfig = None
    temporal_config: TemporalFeatureConfig = None
    cross_timeframe_config: CrossTimeframeFeatureConfig = None
    
    def __post_init__(self):
        """Set default values if not provided."""
        # Add FeatureConfig attributes for validation
        self.short_periods = [5, 10, 14]
        self.medium_periods = [20, 50, 100]
        self.long_periods = [200, 500]
        self.price_types = ['open', 'high', 'low', 'close']
        self.volatility_periods = [14, 20, 50]
        self.volume_periods = [14, 20, 50]
        self.custom_params = {}
        
        if self.proprietary_config is None:
            self.proprietary_config = ProprietaryFeatureConfig()
        if self.technical_config is None:
            self.technical_config = TechnicalFeatureConfig()
        if self.statistical_config is None:
            self.statistical_config = StatisticalFeatureConfig()
        if self.temporal_config is None:
            self.temporal_config = TemporalFeatureConfig()
        if self.cross_timeframe_config is None:
            self.cross_timeframe_config = CrossTimeframeFeatureConfig()


class FeatureGenerator(BaseFeatureGenerator):
    """
    Main feature generator that orchestrates all feature generation.
    
    This class coordinates the generation of features from all sources
    and provides a unified interface for the ML system.
    """
    
    def __init__(self, config: MasterFeatureConfig = None):
        """
        Initialize the main feature generator.
        
        Args:
            config: Master configuration for all feature generators
        """
        super().__init__(config or MasterFeatureConfig())
        self.master_config = self.config
        
        # Initialize individual generators
        self.generators = {}
        self._initialize_generators()
        
        # Feature selector
        selector_config = FeatureSelectionConfig(
            max_features=self.master_config.max_features,
            min_importance=self.master_config.min_importance,
            correlation_threshold=self.master_config.correlation_threshold
        )
        self.feature_selector = FeatureSelector(selector_config)
        
        # Feature tracking
        self.feature_categories = {}
        self.feature_importance = {}
        self.feature_correlations = {}
        
    def _initialize_generators(self):
        """Initialize individual feature generators based on configuration."""
        try:
            if self.master_config.enable_proprietary:
                self.generators['proprietary'] = ProprietaryFeatureGenerator(
                    self.master_config.proprietary_config
                )
                logger.print_info("Initialized proprietary feature generator")
                
            if self.master_config.enable_technical:
                self.generators['technical'] = TechnicalFeatureGenerator(
                    self.master_config.technical_config
                )
                logger.print_info("Initialized technical feature generator")
                
            if self.master_config.enable_statistical:
                self.generators['statistical'] = StatisticalFeatureGenerator(
                    self.master_config.statistical_config
                )
                logger.print_info("Initialized statistical feature generator")
                
            if self.master_config.enable_temporal:
                self.generators['temporal'] = TemporalFeatureGenerator(
                    self.master_config.temporal_config
                )
                logger.print_info("Initialized temporal feature generator")
                
            if self.master_config.enable_cross_timeframe:
                self.generators['cross_timeframe'] = CrossTimeframeFeatureGenerator(
                    self.master_config.cross_timeframe_config
                )
                logger.print_info("Initialized cross-timeframe feature generator")
                
        except Exception as e:
            logger.print_error(f"Error initializing feature generators: {e}")
            
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate all features from the input DataFrame.
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            DataFrame with original data plus all generated features
        """
        if not self.validate_data(df):
            return df
            
        start_time = time.time()
        logger.print_info("Starting comprehensive feature generation...")
        
        df_features = df.copy()
        total_features_generated = 0
        
        # Generate features from each generator
        for generator_name, generator in self.generators.items():
            try:
                logger.print_info(f"Generating {generator_name} features...")
                generator_start_time = time.time()
                
                df_features = generator.generate_features(df_features)
                
                # Track features by category
                self.feature_categories[generator_name] = generator.get_feature_names()
                total_features_generated += generator.get_feature_count()
                
                generator_time = time.time() - generator_start_time
                logger.print_info(f"Generated {generator.get_feature_count()} {generator_name} features in {generator_time:.2f}s")
                
            except Exception as e:
                logger.print_error(f"Error generating {generator_name} features: {e}")
                continue
                
        # Feature selection and optimization
        if total_features_generated > 0:
            logger.print_info("Performing feature selection and optimization...")
            df_features = self._optimize_features(df_features)
            
        total_time = time.time() - start_time
        logger.print_success(f"Feature generation completed in {total_time:.2f}s")
        logger.print_info(f"Total features generated: {total_features_generated}")
        logger.print_info(f"Final features after selection: {len(self.get_feature_names())}")
        
        return df_features
    
    def _optimize_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimize features through selection and importance analysis."""
        try:
            # Get all feature columns (excluding original OHLCV)
            original_columns = ['Open', 'High', 'Low', 'Close']
            if 'Volume' in df.columns:
                original_columns.append('Volume')
                
            feature_columns = [col for col in df.columns if col not in original_columns]
            
            if not feature_columns:
                logger.print_warning("No features to optimize")
                return df
                
            # Prepare feature matrix
            X = df[feature_columns].fillna(0)
            
            # Calculate feature importance (using correlation with price changes as proxy)
            price_changes = df['Close'].pct_change(fill_method=None).fillna(0)
            feature_importance = {}
            
            for col in feature_columns:
                try:
                    # Calculate correlation with price changes
                    correlation = abs(X[col].corr(price_changes))
                    feature_importance[col] = correlation if not np.isnan(correlation) else 0.0
                except Exception:
                    feature_importance[col] = 0.0
                    
            # Store feature importance
            self.feature_importance = feature_importance
            
            # Select best features
            selected_features = self.feature_selector.select_features(
                X, feature_importance, self.master_config.max_features
            )
            
            # Keep only selected features plus original data
            columns_to_keep = original_columns + selected_features
            df_optimized = df[columns_to_keep].copy()
            
            # Update feature tracking
            self.feature_names = selected_features
            self.features_generated = len(selected_features)
            
            logger.print_info(f"Feature optimization: {len(feature_columns)} -> {len(selected_features)} features")
            
            return df_optimized
            
        except Exception as e:
            logger.print_error(f"Error optimizing features: {e}")
            return df
    
    def get_feature_names(self) -> List[str]:
        """Get list of all generated feature names after optimization."""
        return self.feature_names
    
    def get_feature_categories(self) -> Dict[str, List[str]]:
        """Get features organized by category."""
        return self.feature_categories.copy()
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores."""
        return self.feature_importance.copy()
    
    def get_feature_summary(self) -> Dict[str, Any]:
        """Get comprehensive feature summary."""
        summary = {
            'total_features': self.features_generated,
            'categories': self.feature_categories,
            'importance': self.feature_importance,
            'generators_used': list(self.generators.keys()),
            'config': {
                'max_features': self.master_config.max_features,
                'min_importance': self.master_config.min_importance,
                'correlation_threshold': self.master_config.correlation_threshold
            }
        }
        
        # Add category counts
        for category, features in self.feature_categories.items():
            summary[f'{category}_count'] = len(features)
            
        return summary
    
    def export_feature_report(self, output_path: str = None) -> str:
        """
        Export comprehensive feature report.
        
        Args:
            output_path: Path to save the report (optional)
            
        Returns:
            Path to the saved report
        """
        try:
            if output_path is None:
                output_path = f"logs/feature_report_{int(time.time())}.txt"
                
            # Ensure directory exists
            import os
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("NEOZORk HLD PREDICTION - FEATURE GENERATION REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                # Summary
                summary = self.get_feature_summary()
                f.write(f"Total Features Generated: {summary['total_features']}\n")
                f.write(f"Generators Used: {', '.join(summary['generators_used'])}\n\n")
                
                # Configuration
                f.write("Configuration:\n")
                f.write(f"  Max Features: {summary['config']['max_features']}\n")
                f.write(f"  Min Importance: {summary['config']['min_importance']}\n")
                f.write(f"  Correlation Threshold: {summary['config']['correlation_threshold']}\n\n")
                
                # Category breakdown
                f.write("Feature Categories:\n")
                for category, features in summary['categories'].items():
                    f.write(f"  {category.capitalize()}: {len(features)} features\n")
                f.write("\n")
                
                # Feature importance (top 20)
                f.write("Top 20 Features by Importance:\n")
                sorted_features = sorted(
                    summary['importance'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:20]
                
                for i, (feature, importance) in enumerate(sorted_features, 1):
                    f.write(f"  {i:2d}. {feature:<40} {importance:.4f}\n")
                f.write("\n")
                
                # Detailed feature list by category
                for category, features in summary['categories'].items():
                    if features:
                        f.write(f"{category.capitalize()} Features:\n")
                        for feature in sorted(features):
                            importance = summary['importance'].get(feature, 0.0)
                            f.write(f"  {feature:<50} {importance:.4f}\n")
                        f.write("\n")
                        
            logger.print_success(f"Feature report exported to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.print_error(f"Error exporting feature report: {e}")
            return ""
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage information for features."""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'percent': process.memory_percent()
            }
        except ImportError:
            return {'error': 'psutil not available'}
    
    def cleanup(self):
        """Clean up resources and reset state."""
        try:
            # Reset all generators
            for generator in self.generators.values():
                if hasattr(generator, 'reset_feature_count'):
                    generator.reset_feature_count()
                    
            # Reset main generator
            self.reset_feature_count()
            self.feature_categories.clear()
            self.feature_importance.clear()
            self.feature_correlations.clear()
            
            logger.print_info("Feature generator cleanup completed")
            
        except Exception as e:
            logger.print_error(f"Error during cleanup: {e}")
    
    def __str__(self) -> str:
        """String representation of the feature generator."""
        return f"FeatureGenerator(features={self.features_generated}, generators={len(self.generators)})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"FeatureGenerator(config={self.master_config}, "
                f"features_generated={self.features_generated}, "
                f"generators={list(self.generators.keys())})")
