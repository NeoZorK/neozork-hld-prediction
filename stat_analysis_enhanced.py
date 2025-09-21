#!/usr/bin/env python3
"""
📊 Enhanced Statistical Analysis Tool for Financial Data 🚀

This enhanced version provides improved data transformation capabilities specifically
designed to handle high skewness and kurtosis in financial data. It includes advanced
transformation methods and better algorithms for distribution normalization.

Key Improvements:
- Enhanced transformation methods for high skewness data
- Robust Box-Cox with multiple optimization strategies
- Financial-specific transformations (log returns, percentage changes)
- Quantile-based transformations for outlier-resistant normalization
- Adaptive transformations that optimize for both skewness and kurtosis
- Better handling of extreme values and outliers

Usage:
    # Single file processing with enhanced transformations:
    python stat_analysis_enhanced.py -f <filename> [--descriptive] [--distribution] [--transform] [--enhanced]
    
    # Batch processing with enhanced transformations:
    python stat_analysis_enhanced.py --batch-fixed [--descriptive] [--distribution] [--transform] [--enhanced]
    
    # Enhanced transformation only:
    python stat_analysis_enhanced.py -f <filename> --enhanced-transform

Options:
    --descriptive    Perform descriptive statistics analysis
    --distribution   Perform distribution analysis (normality tests, skewness, kurtosis)
    --transform      Perform standard data transformation analysis
    --enhanced       Use enhanced transformation methods (recommended for high skewness)
    --enhanced-transform  Use only enhanced transformations
    --auto          Automatically answer 'y' to all questions (non-interactive mode)
    --output        Output directory for saving results and transformed data
    --verbose       Enable verbose logging output
"""

__version__ = "2.0.0"

import argparse
import sys
import os
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
import pandas as pd

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.statistics.file_operations import StatisticsFileOperations
from src.statistics.descriptive_stats import DescriptiveStatistics
from src.statistics.distribution_analysis import DistributionAnalysis
from src.statistics.data_transformation import DataTransformation
from src.statistics.enhanced_data_transformation import EnhancedDataTransformation
from src.statistics.cli_interface import StatisticsCLI
from src.statistics.reporting import StatisticsReporter
from src.statistics.color_utils import ColorUtils


class EnhancedStatisticalAnalyzer:
    """Enhanced statistical analyzer with improved transformation capabilities."""
    
    def __init__(self, auto_mode: bool = False, output_directory: Optional[str] = None, 
                 analysis_options: Dict[str, Any] = None):
        """Initialize the enhanced statistical analyzer."""
        self.file_ops = StatisticsFileOperations()
        self.descriptive_stats = DescriptiveStatistics()
        self.distribution_analysis = DistributionAnalysis()
        self.data_transformation = DataTransformation()
        self.enhanced_transformation = EnhancedDataTransformation()
        self.cli = StatisticsCLI()
        self.reporter = StatisticsReporter()
        self.auto_mode = auto_mode
        self.output_directory = output_directory
        self.analysis_options = analysis_options or {}
        
        # Supported data directories
        self.supported_dirs = self.file_ops.get_supported_directories()
    
    def _get_user_input(self, prompt: str) -> str:
        """Get user input with automatic mode support."""
        if self.auto_mode:
            print(f"{prompt} y")
            return "y"
        else:
            return input(prompt).lower().strip()
    
    def analyze_file_enhanced(self, filename: str, analysis_options: Dict[str, bool]) -> Dict[str, Any]:
        """
        Analyze a single file with enhanced transformation capabilities.
        
        Args:
            filename: Name of the file to analyze
            analysis_options: Dictionary of analysis options
            
        Returns:
            Dictionary with analysis results
        """
        # Validate file
        file_info = self.file_ops.validate_file_path(filename)
        
        if file_info is None:
            raise ValueError(f"Invalid file '{filename}'. Please choose a file from supported directories.")
        
        return self._analyze_file_with_info_enhanced(file_info, analysis_options)
    
    def _analyze_file_with_info_enhanced(self, file_info: Dict[str, Any], 
                                       analysis_options: Dict[str, bool]) -> Dict[str, Any]:
        """Analyze a file using enhanced transformation methods."""
        # Load data first to get accurate metadata
        data = self.file_ops.load_data(file_info["file_path"], file_info["format"])
        
        if data is None or data.empty:
            raise ValueError("Could not load data or data is empty")
        
        # Update file_info with actual data dimensions
        file_info['rows_count'] = len(data)
        file_info['columns_count'] = len(data.columns)
        file_info['filename'] = os.path.basename(file_info['file_path'])
        
        # Display analysis start with accurate metadata
        self.reporter.display_analysis_start(file_info, analysis_options)
        
        # Get numeric columns
        numeric_columns = self._get_numeric_columns(data)
        
        if not numeric_columns:
            raise ValueError("No numeric columns found for analysis")
        
        # Perform analysis
        analysis_results = {}
        
        # Check if we need to run descriptive analysis
        need_descriptive = (analysis_options.get('descriptive', False) or 
                           analysis_options.get('basic', False) or 
                           analysis_options.get('distribution_chars', False) or 
                           analysis_options.get('variability', False) or 
                           analysis_options.get('missing', False))
        
        if need_descriptive:
            print("\n📊 Performing descriptive statistics analysis...")
            analysis_results['descriptive'] = self.descriptive_stats.analyze_data(data, numeric_columns)
        
        # Check if we need to run distribution analysis
        need_distribution = (analysis_options.get('distribution', False) or 
                           analysis_options.get('norm', False) or 
                           analysis_options.get('skewness', False) or 
                           analysis_options.get('kurtosis', False))
        
        if need_distribution:
            print("\n📈 Performing distribution analysis...")
            analysis_results['distribution'] = self.distribution_analysis.analyze_distributions(data, numeric_columns)
        
        # Check if we need to run transformation analysis
        need_transform = (analysis_options.get('transform', False) or 
                         analysis_options.get('enhanced', False) or
                         analysis_options.get('enhanced_transform', False) or
                         analysis_options.get('transformation_results', False) or 
                         analysis_options.get('transformation_comparison', False))
        
        if need_transform:
            print("\n🔄 Performing enhanced data transformation analysis...")
            
            # Get transformation recommendations
            if 'distribution' in analysis_results:
                recommendations = analysis_results['distribution'].get('distribution_recommendations', {})
                
                # Use enhanced recommendations if enhanced mode is enabled
                if analysis_options.get('enhanced', False) or analysis_options.get('enhanced_transform', False):
                    print("🎯 Using enhanced transformation recommendations...")
                    enhanced_recommendations = self.enhanced_transformation.get_enhanced_transformation_recommendations(data, numeric_columns)
                    transformations = enhanced_recommendations
                else:
                    transformations = self._prepare_transformations(recommendations, data)
                
                if transformations:
                    print("\n🎯 Selecting optimal enhanced transformations for each column...")
                    
                    if analysis_options.get('enhanced', False) or analysis_options.get('enhanced_transform', False):
                        # Use enhanced transformation methods
                        optimal_transformations = self._select_enhanced_transformations(data, transformations, numeric_columns)
                        analysis_results['transformation'] = self.enhanced_transformation.transform_data_enhanced(
                            data, optimal_transformations, numeric_columns
                        )
                    else:
                        # Use standard transformation methods
                        optimal_transformations = self._select_optimal_transformations(data, transformations, numeric_columns)
                        single_transformations = {col: [transform] for col, transform in optimal_transformations.items()}
                        analysis_results['transformation'] = self.data_transformation.transform_data(
                            data, single_transformations, numeric_columns
                        )
                    
                    # Add comparison results
                    analysis_results['transformation']['comparison'] = self.data_transformation.compare_transformations(
                        data, analysis_results['transformation']
                    )
                else:
                    analysis_results['transformation'] = {
                        'transformed_data': data,
                        'transformation_details': {},
                        'comparison': {}
                    }
        
        return {
            'file_info': file_info,
            'analysis_results': analysis_results,
            'numeric_columns': numeric_columns
        }
    
    def _select_enhanced_transformations(self, data: pd.DataFrame, transformations: Dict[str, List[str]], 
                                       numeric_columns: List[str]) -> Dict[str, str]:
        """Select the best enhanced transformation for each column."""
        optimal_transformations = {}
        
        for col in numeric_columns:
            if col not in transformations or not transformations[col]:
                continue
            
            col_data = data[col].dropna()
            if len(col_data) == 0:
                continue
            
            print(f"\n🔍 Testing enhanced transformations for column: {col}")
            print("-" * 60)
            
            best_transformation = None
            best_score = -float('inf')
            transformation_scores = {}
            
            # Test each transformation method
            for transform_type in transformations[col]:
                try:
                    # Apply enhanced transformation
                    transformed_col, details = self.enhanced_transformation._apply_enhanced_transformation(
                        col_data, transform_type, col
                    )
                    
                    if transformed_col is None or len(transformed_col) == 0:
                        print(f"  {transform_type}: Failed - No data returned")
                        continue
                    
                    # Check if transformation was successful
                    if not details.get('success', True):
                        print(f"  {transform_type}: Failed - {details.get('error', 'Unknown error')}")
                        continue
                    
                    # Use improvement score from enhanced transformation
                    score = details.get('improvement_score', 0.0)
                    transformation_scores[transform_type] = score
                    
                    print(f"  {transform_type}: Score = {score:.3f}")
                    
                    if score > best_score:
                        best_score = score
                        best_transformation = transform_type
                        
                except Exception as e:
                    print(f"  {transform_type}: Failed - {str(e)}")
                    continue
            
            if best_transformation:
                optimal_transformations[col] = best_transformation
                print(f"  ✅ Best: {best_transformation} (Score: {best_score:.3f})")
            else:
                print(f"  ❌ No suitable transformation found for {col}")
        
        return optimal_transformations
    
    def _prepare_transformations(self, recommendations: Dict[str, Any], data: pd.DataFrame = None) -> Dict[str, List[str]]:
        """Prepare transformation dictionary from recommendations."""
        transformations = {}
        
        for col, rec in recommendations.items():
            if rec.get('primary_recommendation') != "No transformation needed":
                recommended_transformations = rec.get('recommended_transformations', [])
                if recommended_transformations:
                    transformations[col] = recommended_transformations
            else:
                transformations[col] = ['log', 'sqrt', 'box_cox', 'yeo_johnson']
        
        return transformations
    
    def _select_optimal_transformations(self, data: pd.DataFrame, transformations: Dict[str, List[str]], 
                                      numeric_columns: List[str]) -> Dict[str, str]:
        """Select the best transformation for each column (standard method)."""
        optimal_transformations = {}
        
        for col in numeric_columns:
            if col not in transformations or not transformations[col]:
                continue
            
            col_data = data[col].dropna()
            if len(col_data) == 0:
                continue
            
            print(f"\n🔍 Testing transformations for column: {col}")
            print("-" * 50)
            
            best_transformation = None
            best_score = -float('inf')
            
            # Test each transformation method
            for transform_type in transformations[col]:
                try:
                    # Apply transformation
                    transformed_col, details = self.data_transformation._apply_transformation(
                        col_data, transform_type, col
                    )
                    
                    if transformed_col is None or len(transformed_col) == 0:
                        print(f"  {transform_type}: Failed - No data returned")
                        continue
                    
                    # Check if transformation was successful
                    if not details.get('success', True):
                        print(f"  {transform_type}: Failed - {details.get('error', 'Unknown error')}")
                        continue
                    
                    # Calculate comprehensive score
                    score = self._calculate_transformation_score(col_data, transformed_col, transform_type)
                    
                    print(f"  {transform_type}: Score = {score:.3f}")
                    
                    if score > best_score:
                        best_score = score
                        best_transformation = transform_type
                        
                except Exception as e:
                    print(f"  {transform_type}: Failed - {str(e)}")
                    continue
            
            if best_transformation:
                optimal_transformations[col] = best_transformation
                print(f"  ✅ Best: {best_transformation} (Score: {best_score:.3f})")
            else:
                print(f"  ❌ No suitable transformation found for {col}")
        
        return optimal_transformations
    
    def _calculate_transformation_score(self, original_data: pd.Series, transformed_data: pd.Series, 
                                      transform_type: str) -> float:
        """Calculate comprehensive score for transformation quality."""
        from scipy import stats
        import numpy as np
        
        try:
            # Calculate original statistics
            orig_skew = abs(stats.skew(original_data))
            orig_kurt = abs(stats.kurtosis(original_data))
            
            # Calculate transformed statistics
            trans_skew = abs(stats.skew(transformed_data))
            trans_kurt = abs(stats.kurtosis(transformed_data))
            
            # Test normality of transformed data
            if len(transformed_data) > 3:
                if len(transformed_data) <= 5000:
                    shapiro_stat, shapiro_p = stats.shapiro(transformed_data)
                    dagostino_stat, dagostino_p = stats.normaltest(transformed_data)
                    is_normal = shapiro_p > 0.05 and dagostino_p > 0.05
                else:
                    dagostino_stat, dagostino_p = stats.normaltest(transformed_data)
                    is_normal = dagostino_p > 0.05
            else:
                is_normal = False
            
            # Calculate improvement scores
            skew_improvement = max(0, (orig_skew - trans_skew) / max(orig_skew, 0.001))
            kurt_improvement = max(0, (orig_kurt - trans_kurt) / max(orig_kurt, 0.001))
            
            # Normalize skewness and kurtosis to 0-1 scale
            skew_score = max(0, 1 - min(trans_skew / 2.0, 1))
            kurt_score = max(0, 1 - min(trans_kurt / 3.0, 1))
            
            # Normality bonus
            normality_bonus = 0.3 if is_normal else 0
            
            # Calculate final score
            score = (
                0.3 * skew_improvement +
                0.2 * kurt_improvement +
                0.3 * skew_score +
                0.2 * kurt_score +
                normality_bonus
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            return 0.0
    
    def _get_numeric_columns(self, data) -> List[str]:
        """Get list of numeric columns from DataFrame."""
        import pandas as pd
        import numpy as np
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Filter out columns that are all NaN or have no variance
        valid_numeric_cols = []
        for col in numeric_cols:
            if not data[col].isna().all() and data[col].nunique() > 1:
                valid_numeric_cols.append(col)
        
        return valid_numeric_cols
    
    def run_enhanced_analysis(self, config: Dict[str, Any]) -> None:
        """Run enhanced statistical analysis."""
        try:
            # Set auto mode
            self.auto_mode = config['processing_options']['auto']
            
            # Set output directory
            if config['output_directory']:
                self.output_directory = config['output_directory']
            
            # Get analysis options
            analysis_options = config['analysis_options']
            
            # Determine processing mode
            file_processing = config['file_processing']
            
            if file_processing['mode'] == 'single_file':
                # Single file processing
                results = self.analyze_file_enhanced(file_processing['filename'], analysis_options)
                
                # Generate and display report
                report = self.reporter.generate_comprehensive_report(
                    results['file_info'], 
                    results['analysis_results'],
                    self.output_directory,
                    self.auto_mode,
                    self.analysis_options
                )
                
                print("\n" + report)
                
                # Handle data transformation
                if (analysis_options.get('transform', False) or 
                    analysis_options.get('enhanced', False) or
                    analysis_options.get('enhanced_transform', False)) and 'transformation' in results['analysis_results']:
                    self._handle_enhanced_data_transformation(results)
            
            print("\n🎉 Enhanced statistical analysis completed successfully!")
            
        except Exception as e:
            print(f"\nError during enhanced statistical analysis: {str(e)}")
            sys.exit(1)
    
    def _handle_enhanced_data_transformation(self, results: Dict[str, Any]):
        """Handle enhanced data transformation user interaction."""
        transformation_results = results['analysis_results'].get('transformation', {})
        transformation_details = transformation_results.get('transformation_details', {})
        
        if not transformation_details:
            return
        
        # Check if any transformations were successful
        has_successful_transformations = any(
            any(details.get('success', False) for details in col_details.values())
            for col_details in transformation_details.values()
        )
        
        if not has_successful_transformations:
            return
        
        # In auto mode, automatically transform and save
        if self.auto_mode:
            print("\n🔄 Auto mode: Applying enhanced transformations...")
            print("\n" + self._get_enhanced_transformation_summary(transformation_results))
            print("\n💾 Auto mode: Saving transformed data...")
            self._save_enhanced_transformed_data_with_metadata(results)
        else:
            # Ask if user wants to transform data
            while True:
                transform = self._get_user_input("\n🔄 Do you want to apply enhanced transformations? (y/n): ")
                if transform in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            if transform == 'y':
                # Display transformation summary
                print("\n" + self._get_enhanced_transformation_summary(transformation_results))
                
                # Ask if user wants to save transformed data
                while True:
                    save = self._get_user_input("\n💾 Do you want to save transformed data? (y/n): ")
                    if save in ['y', 'n']:
                        break
                    print("Please enter 'y' or 'n'")
                
                if save == 'y':
                    self._save_enhanced_transformed_data_with_metadata(results)
    
    def _get_enhanced_transformation_summary(self, transformation_results: Dict[str, Any]) -> str:
        """Get enhanced transformation summary."""
        summary = "================================================================================\n"
        summary += "ENHANCED DATA TRANSFORMATION SUMMARY\n"
        summary += "================================================================================\n"
        
        transformation_details = transformation_results.get('transformation_details', {})
        
        for col, col_transformations in transformation_details.items():
            summary += f"Column: {col}\n"
            summary += "-" * 40 + "\n"
            
            for transform_type, details in col_transformations.items():
                if details.get('success', False):
                    summary += f"  {transform_type}:\n"
                    summary += f"    Original Mean: {details.get('original_mean', 'N/A'):.4f}\n"
                    summary += f"    Transformed Mean: {details.get('transformed_mean', 'N/A'):.4f}\n"
                    summary += f"    Original Skewness: {details.get('original_skewness', 'N/A'):.4f}\n"
                    summary += f"    Transformed Skewness: {details.get('transformed_skewness', 'N/A'):.4f}\n"
                    summary += f"    Skewness Improvement: {details.get('skewness_improvement', 'N/A'):.4f}\n"
                    summary += f"    Improvement Score: {details.get('improvement_score', 'N/A'):.4f}\n"
                    if 'lambda' in details:
                        summary += f"    Lambda: {details['lambda']:.4f}\n"
                    summary += "\n"
        
        return summary
    
    def _save_enhanced_transformed_data_with_metadata(self, results: Dict[str, Any]):
        """Save enhanced transformed data with metadata."""
        try:
            file_info = results['file_info']
            transformation_results = results['analysis_results'].get('transformation', {})
            transformed_data = transformation_results.get('transformed_data')
            
            if transformed_data is None:
                print("No transformed data to save.")
                return
            
            # Create save path structure
            source = file_info.get("source", "unknown")
            format_type = file_info["format"]
            symbol = file_info.get("symbol", "unknown")
            indicator = file_info.get("indicator", "unknown")
            timeframe = file_info.get("timeframe", "unknown")
            
            save_path = f"data/fixed/transformed_by_stat_enhanced/{source}/{format_type}/{symbol}/{indicator}/{timeframe}/"
            
            # Create directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)
            
            # Generate filename
            filename = f"{symbol}_{timeframe}_{indicator}_enhanced_transformed.{format_type}"
            full_path = os.path.join(save_path, filename)
            
            # Save data
            self.file_ops.save_data(transformed_data, full_path, format_type)
            
            # Create and save transformation metadata
            metadata = self._create_enhanced_transformation_metadata(results, full_path)
            metadata_path = os.path.join(save_path, f"{symbol}_{timeframe}_{indicator}_enhanced_transformation_metadata.json")
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            print(f"\n✅ Enhanced transformed data saved to: {full_path}")
            print(f"✅ Enhanced transformation metadata saved to: {metadata_path}")
            
        except Exception as e:
            print(f"\n❌ Error saving enhanced transformed data: {str(e)}")
    
    def _create_enhanced_transformation_metadata(self, results: Dict[str, Any], transformed_file_path: str) -> Dict[str, Any]:
        """Create enhanced transformation metadata dictionary."""
        file_info = results['file_info']
        transformation_results = results['analysis_results'].get('transformation', {})
        transformation_details = transformation_results.get('transformation_details', {})
        
        metadata = {
            "transformation_info": {
                "original_file": file_info.get("file_path", "unknown"),
                "transformed_file": transformed_file_path,
                "timestamp": results.get("timestamp", "unknown"),
                "source": file_info.get("source", "unknown"),
                "symbol": file_info.get("symbol", "unknown"),
                "indicator": file_info.get("indicator", "unknown"),
                "timeframe": file_info.get("timeframe", "unknown"),
                "format": file_info.get("format", "unknown"),
                "enhanced_version": "2.0.0"
            },
            "enhanced_transformations_applied": {},
            "original_statistics": {},
            "transformed_statistics": {},
            "improvement_metrics": {}
        }
        
        # Add transformation details for each column
        for col, col_transformations in transformation_details.items():
            metadata["enhanced_transformations_applied"][col] = {}
            for transform_type, details in col_transformations.items():
                if details.get('success', False):
                    metadata["enhanced_transformations_applied"][col][transform_type] = {
                        "lambda": details.get('lambda'),
                        "parameters": details.get('parameters', {}),
                        "success": details.get('success', False),
                        "improvement_score": details.get('improvement_score', 0.0),
                        "skewness_improvement": details.get('skewness_improvement', 0.0),
                        "kurtosis_improvement": details.get('kurtosis_improvement', 0.0),
                        "method": details.get('method', 'unknown'),
                        "reason": details.get('reason', '')
                    }
        
        # Add original statistics
        if 'descriptive' in results['analysis_results']:
            desc_results = results['analysis_results']['descriptive']
            if 'basic_stats' in desc_results:
                metadata["original_statistics"]["basic"] = desc_results['basic_stats']
            if 'distribution_stats' in desc_results:
                metadata["original_statistics"]["distribution"] = desc_results['distribution_stats']
        
        return metadata


def create_enhanced_cli() -> argparse.ArgumentParser:
    """Create enhanced CLI parser."""
    parser = argparse.ArgumentParser(
        description="Enhanced Statistical Analysis Tool for Financial Data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Enhanced analysis with improved transformations:
  python stat_analysis_enhanced.py -f binance_BTCUSDT_D1.parquet --descriptive --distribution --enhanced --auto
  
  # Only enhanced transformations:
  python stat_analysis_enhanced.py -f binance_BTCUSDT_D1.parquet --enhanced-transform --auto
  
  # Batch processing with enhanced transformations:
  python stat_analysis_enhanced.py --batch-fixed --descriptive --distribution --enhanced --auto
        """
    )
    
    # File processing options
    file_group = parser.add_argument_group('File Processing Options')
    file_group.add_argument(
        "-f", "--file",
        type=str,
        help="📁 Single file to analyze (filename only, must be in supported directories)"
    )
    
    file_group.add_argument(
        "--path",
        type=str,
        help="📂 Custom file or directory path to analyze"
    )
    
    # Batch processing options
    batch_group = parser.add_argument_group('Batch Processing Options')
    batch_group.add_argument(
        "--batch-raw-parquet",
        action="store_true",
        help="📊 Process all files in data/raw_parquet/"
    )
    
    batch_group.add_argument(
        "--batch-fixed",
        action="store_true",
        help="📊 Process all files in data/fixed/ (recommended)"
    )
    
    batch_group.add_argument(
        "--batch-all",
        action="store_true",
        help="📊 Process all supported directories"
    )
    
    # Analysis options
    analysis_group = parser.add_argument_group('Analysis Options')
    analysis_group.add_argument(
        "--descriptive",
        action="store_true",
        help="📊 Perform descriptive statistics analysis"
    )
    
    analysis_group.add_argument(
        "--distribution",
        action="store_true",
        help="📈 Perform distribution analysis (normality tests, skewness, kurtosis)"
    )
    
    analysis_group.add_argument(
        "--transform",
        action="store_true",
        help="🔄 Perform standard data transformation analysis"
    )
    
    analysis_group.add_argument(
        "--enhanced",
        action="store_true",
        help="🚀 Use enhanced transformation methods (recommended for high skewness data)"
    )
    
    analysis_group.add_argument(
        "--enhanced-transform",
        action="store_true",
        help="🚀 Use only enhanced transformations (skip standard transformations)"
    )
    
    # Processing options
    processing_group = parser.add_argument_group('Processing Options')
    processing_group.add_argument(
        "--auto",
        action="store_true",
        help="🤖 Automatically answer 'y' to all questions (non-interactive mode)"
    )
    
    processing_group.add_argument(
        "--output",
        type=str,
        help="📁 Output directory for saving results and transformed data"
    )
    
    processing_group.add_argument(
        "--verbose",
        action="store_true",
        help="📝 Enable verbose logging output"
    )
    
    processing_group.add_argument(
        "--version",
        action="version",
        version=f"Enhanced Statistical Analysis Tool v{__version__}"
    )
    
    return parser


def main():
    """Main entry point for enhanced statistical analysis."""
    parser = create_enhanced_cli()
    args = parser.parse_args()
    
    # Validate arguments
    if not any([args.file, args.path, args.batch_raw_parquet, args.batch_fixed, args.batch_all]):
        parser.error("Please specify a file, path, or batch processing option")
    
    if not any([args.descriptive, args.distribution, args.transform, args.enhanced, args.enhanced_transform]):
        parser.error("Please specify at least one analysis option")
    
    # Create configuration
    config = {
        'file_processing': {
            'mode': 'single_file',
            'filename': args.file,
            'directory': args.path
        },
        'analysis_options': {
            'descriptive': args.descriptive,
            'distribution': args.distribution,
            'transform': args.transform,
            'enhanced': args.enhanced,
            'enhanced_transform': args.enhanced_transform
        },
        'processing_options': {
            'auto': args.auto
        },
        'output_directory': args.output
    }
    
    # Determine processing mode
    if args.batch_raw_parquet:
        config['file_processing']['mode'] = 'batch'
        config['file_processing']['directory'] = 'data/raw_parquet/'
    elif args.batch_fixed:
        config['file_processing']['mode'] = 'batch'
        config['file_processing']['directory'] = 'data/fixed/'
    elif args.batch_all:
        config['file_processing']['mode'] = 'batch_all'
    elif args.path:
        config['file_processing']['mode'] = 'custom_path'
    
    # Start timing
    start_time = time.time()
    
    # Create the enhanced analyzer
    analyzer = EnhancedStatisticalAnalyzer(
        auto_mode=config['processing_options']['auto'],
        output_directory=config['output_directory'],
        analysis_options=config['analysis_options']
    )
    
    # Run enhanced analysis
    analyzer.run_enhanced_analysis(config)
    
    # Calculate and display processing time
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"\n⏱️  Enhanced processing completed in {processing_time:.2f} seconds")
    print(f"{ColorUtils.green('🎉 Enhanced statistical analysis finished successfully!')}")


if __name__ == "__main__":
    main()
