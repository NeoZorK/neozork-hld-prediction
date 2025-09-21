#!/usr/bin/env python3
"""
📊 Statistical Analysis Tool for Financial Data 🚀

This script provides comprehensive statistical analysis for financial time series data
from multiple sources and formats. It supports parquet, JSON, and CSV formats
from various data sources including Binance, Polygon, yfinance, and cleaned data.

Usage:
    # Single file processing:
    python stat_analysis.py -f <filename> [--descriptive] [--distribution] [--transform]
    
    # Batch processing by directory:
    python stat_analysis.py --batch-raw-parquet [--descriptive] [--distribution] [--transform]
    python stat_analysis.py --batch-csv-converted [--descriptive] [--distribution] [--transform]
    python stat_analysis.py --batch-indicators-parquet [--descriptive] [--distribution] [--transform]
    python stat_analysis.py --batch-indicators-json [--descriptive] [--distribution] [--transform]
    python stat_analysis.py --batch-indicators-csv [--descriptive] [--distribution] [--transform]
    python stat_analysis.py --batch-fixed [--descriptive] [--distribution] [--transform]
    python stat_analysis.py --batch-all [--descriptive] [--distribution] [--transform]
    
    # Custom path processing:
    python stat_analysis.py --path <path> [--descriptive] [--distribution] [--transform]

The filename must be from one of the supported data directories:
- data/cache/csv_converted/
- data/raw_parquet/
- data/indicators/parquet/
- data/indicators/json/
- data/indicators/csv/
- data/fixed/ (cleaned data - recommended)

Options:
    --descriptive    Perform descriptive statistics analysis
    --distribution   Perform distribution analysis (normality tests, skewness, kurtosis)
    --transform      Perform data transformation analysis and recommendations
    --auto          Automatically answer 'y' to all questions (non-interactive mode)
    --recursive     Recursively search subdirectories when using --path
    --output        Output directory for saving results and transformed data
    --verbose       Enable verbose logging output
    --version       Show version information

Note: It is recommended to use already cleaned data from data/fixed/ folder.
You can run clear_data.py --help for more information about data cleaning.
"""

__version__ = "1.0.0"

import argparse
import sys
import os
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.statistics.file_operations import StatisticsFileOperations
from src.statistics.descriptive_stats import DescriptiveStatistics
from src.statistics.distribution_analysis import DistributionAnalysis
from src.statistics.data_transformation import DataTransformation
from src.statistics.cli_interface import StatisticsCLI
from src.statistics.reporting import StatisticsReporter
from src.statistics.color_utils import ColorUtils


class StatisticalAnalyzer:
    """Main class for statistical analysis operations."""
    
    def __init__(self, auto_mode: bool = False, output_directory: Optional[str] = None, analysis_options: Dict[str, Any] = None):
        """Initialize the statistical analyzer.
        
        Args:
            auto_mode: If True, automatically answer 'y' to all questions
            output_directory: Directory to save results and transformed data
            analysis_options: Dictionary with analysis options
        """
        self.file_ops = StatisticsFileOperations()
        self.descriptive_stats = DescriptiveStatistics()
        self.distribution_analysis = DistributionAnalysis()
        self.data_transformation = DataTransformation()
        self.cli = StatisticsCLI()
        self.reporter = StatisticsReporter()
        self.auto_mode = auto_mode
        self.output_directory = output_directory
        self.analysis_options = analysis_options or {}
        
        # Supported data directories
        self.supported_dirs = self.file_ops.get_supported_directories()
    
    def _get_user_input(self, prompt: str) -> str:
        """
        Get user input with automatic mode support.
        
        Args:
            prompt: Input prompt to display
            
        Returns:
            User input or 'y' if in auto mode
        """
        if self.auto_mode:
            print(f"{prompt} y")
            return "y"
        else:
            return input(prompt).lower().strip()
    
    def analyze_file(self, filename: str, analysis_options: Dict[str, bool]) -> Dict[str, Any]:
        """
        Analyze a single file with specified options.
        
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
        
        # Display analysis start
        self.reporter.display_analysis_start(file_info, analysis_options)
        
        # Load data
        data = self.file_ops.load_data(file_info["file_path"], file_info["format"])
        
        if data is None or data.empty:
            raise ValueError("Could not load data or data is empty")
        
        # Get numeric columns
        numeric_columns = self._get_numeric_columns(data)
        
        if not numeric_columns:
            raise ValueError("No numeric columns found for analysis")
        
        # Perform analysis
        analysis_results = {}
        
        # Check if we need to run descriptive analysis (main flag or any descriptive detail flags)
        need_descriptive = (analysis_options.get('descriptive', False) or 
                           analysis_options.get('basic', False) or 
                           analysis_options.get('distribution_chars', False) or 
                           analysis_options.get('variability', False) or 
                           analysis_options.get('missing', False))
        
        if need_descriptive:
            print("\n📊 Performing descriptive statistics analysis...")
            analysis_results['descriptive'] = self.descriptive_stats.analyze_data(data, numeric_columns)
        
        # Check if we need to run distribution analysis (main flag or any distribution detail flags)
        need_distribution = (analysis_options.get('distribution', False) or 
                           analysis_options.get('norm', False) or 
                           analysis_options.get('skewness', False) or 
                           analysis_options.get('kurtosis', False))
        
        if need_distribution:
            print("\n📈 Performing distribution analysis...")
            analysis_results['distribution'] = self.distribution_analysis.analyze_distributions(data, numeric_columns)
        
        # Check if we need to run transformation analysis (main flag or any transformation detail flags)
        need_transform = (analysis_options.get('transform', False) or 
                         analysis_options.get('transformation_results', False) or 
                         analysis_options.get('transformation_comparison', False))
        
        if need_transform:
            print("\n🔄 Performing data transformation analysis...")
            # Get transformation recommendations
            if 'distribution' in analysis_results:
                recommendations = analysis_results['distribution'].get('distribution_recommendations', {})
                transformations = self._prepare_transformations(recommendations)
                
                if transformations:
                    analysis_results['transformation'] = self.data_transformation.transform_data(
                        data, transformations, numeric_columns
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
    
    def _prepare_transformations(self, recommendations: Dict[str, Any]) -> Dict[str, List[str]]:
        """Prepare transformation dictionary from recommendations."""
        transformations = {}
        
        for col, rec in recommendations.items():
            if rec.get('primary_recommendation') != "No transformation needed":
                # Get the first recommended transformation
                recommended_transformations = rec.get('recommended_transformations', [])
                if recommended_transformations:
                    transformations[col] = [recommended_transformations[0]]
        
        return transformations
    
    def run_batch_processing(self, directory: str, directory_name: str, analysis_options: Dict[str, bool], auto_mode: bool = False) -> None:
        """
        Run batch processing for all files in a directory.
        
        Args:
            directory: Directory path to process
            directory_name: Human-readable directory name for display
            analysis_options: Dictionary of analysis options
        """
        print(f"\n{'='*80}")
        print(f"BATCH PROCESSING: {directory_name}")
        print(f"Directory: {directory}")
        print(f"{'='*80}")
        
        files = self.file_ops.get_files_in_directory(directory)
        
        if not files:
            print(f"No supported files found in {directory}")
            return
        
        print(f"Found {len(files)} files to process:")
        for i, file in enumerate(files, 1):
            print(f"  {i}. {file}")
        
        if not self.auto_mode:
            while True:
                proceed = self._get_user_input(f"\nProcess all {len(files)} files? (y/n): ")
                if proceed in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            if proceed != 'y':
                print("Batch processing cancelled.")
                return
        
        # Process each file
        successful = 0
        failed = 0
        
        for i, filename in enumerate(files, 1):
            print(f"\n{'='*60}")
            print(f"PROCESSING FILE {i}/{len(files)}: {filename}")
            print(f"{'='*60}")
            
            try:
                results = self.analyze_file(filename, analysis_options)
                
                # Generate and display report
                report = self.reporter.generate_comprehensive_report(
                    results['file_info'], 
                    results['analysis_results'],
                    self.output_directory,
                    auto_mode,
                    self.analysis_options
                )
                
                print("\n" + report)
                
                # Ask about data transformation
                if analysis_options.get('transform', False) and 'transformation' in results['analysis_results']:
                    self._handle_data_transformation(results)
                
                successful += 1
                print(f"{ColorUtils.green('✅ Successfully processed:')} {filename}")
                
            except Exception as e:
                failed += 1
                self.reporter.display_error(str(e), {'filename': filename})
        
        # Summary
        print(f"\n{'='*80}")
        print(f"BATCH PROCESSING COMPLETE")
        print(f"{'='*80}")
        print(f"Total files: {len(files)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success rate: {(successful/len(files)*100):.1f}%")
    
    def _handle_data_transformation(self, results: Dict[str, Any]):
        """Handle data transformation user interaction."""
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
            print("\n🔄 Auto mode: Applying transformations...")
            print("\n" + self.data_transformation.get_transformation_summary(transformation_results))
            print("\n💾 Auto mode: Saving transformed data...")
            self._save_transformed_data_with_metadata(results)
            self._validate_transformations(results)
        else:
            # Ask if user wants to transform data
            while True:
                transform = self._get_user_input("\n🔄 Do you want to transform your data? (y/n): ")
                if transform in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            if transform == 'y':
                # Display transformation summary
                print("\n" + self.data_transformation.get_transformation_summary(transformation_results))
                
                # Ask if user wants to save transformed data
                while True:
                    save = self._get_user_input("\n💾 Do you want to save transformed data? (y/n): ")
                    if save in ['y', 'n']:
                        break
                    print("Please enter 'y' or 'n'")
                
                if save == 'y':
                    self._save_transformed_data_with_metadata(results)
                    self._validate_transformations(results)
    
    def _save_transformed_data_with_metadata(self, results: Dict[str, Any]):
        """Save transformed data with metadata to appropriate directory."""
        try:
            file_info = results['file_info']
            transformation_results = results['analysis_results'].get('transformation', {})
            transformed_data = transformation_results.get('transformed_data')
            
            if transformed_data is None:
                print("No transformed data to save.")
                return
            
            # Create save path structure: data/fixed/transformed_by_stat/<source>/<format>/<symbol>/<indicator>/<timeframe>/
            source = file_info.get("source", "unknown")
            format_type = file_info["format"]
            symbol = file_info.get("symbol", "unknown")
            indicator = file_info.get("indicator", "unknown")
            timeframe = file_info.get("timeframe", "unknown")
            
            save_path = f"data/fixed/transformed_by_stat/{source}/{format_type}/{symbol}/{indicator}/{timeframe}/"
            
            # Create directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)
            
            # Generate filename
            filename = f"{symbol}_{timeframe}_{indicator}_transformed.{format_type}"
            full_path = os.path.join(save_path, filename)
            
            # Save data
            self.file_ops.save_data(transformed_data, full_path, format_type)
            
            # Create and save transformation metadata
            metadata = self._create_transformation_metadata(results, full_path)
            metadata_path = os.path.join(save_path, f"{symbol}_{timeframe}_{indicator}_transformation_metadata.json")
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            print(f"\n✅ Transformed data saved to: {full_path}")
            print(f"✅ Transformation metadata saved to: {metadata_path}")
            
        except Exception as e:
            print(f"\n❌ Error saving transformed data: {str(e)}")
    
    def _create_transformation_metadata(self, results: Dict[str, Any], transformed_file_path: str) -> Dict[str, Any]:
        """Create transformation metadata dictionary."""
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
                "format": file_info.get("format", "unknown")
            },
            "transformations_applied": {},
            "original_statistics": {},
            "transformed_statistics": {}
        }
        
        # Add transformation details for each column
        for col, col_transformations in transformation_details.items():
            metadata["transformations_applied"][col] = {}
            for transform_type, details in col_transformations.items():
                if details.get('success', False):
                    metadata["transformations_applied"][col][transform_type] = {
                        "lambda": details.get('lambda'),
                        "parameters": details.get('parameters', {}),
                        "success": details.get('success', False),
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
    
    def _validate_transformations(self, results: Dict[str, Any]):
        """Validate if transformations helped solve the problems."""
        print("\n" + "="*80)
        print("🔍 POST-TRANSFORMATION VALIDATION")
        print("="*80)
        
        try:
            transformation_results = results['analysis_results'].get('transformation', {})
            transformed_data = transformation_results.get('transformed_data')
            transformation_details = transformation_results.get('transformation_details', {})
            
            if transformed_data is None:
                print("No transformed data available for validation.")
                return
            
            # Get original data for comparison
            file_info = results['file_info']
            original_data = self.file_ops.load_data(file_info["file_path"], file_info["format"])
            original_numeric_columns = self._get_numeric_columns(original_data)
            
            # Run distribution analysis on original data
            print("\n📊 Running distribution analysis on original data...")
            original_distribution = self.distribution_analysis.analyze_distributions(original_data, original_numeric_columns)
            
            print("\n📈 TRANSFORMATION EFFECTIVENESS ANALYSIS")
            print("-" * 50)
            
            # Compare each transformed column with its original
            for col in original_numeric_columns:
                if col not in transformation_details:
                    continue
                
                col_transformations = transformation_details[col]
                if not col_transformations:
                    continue
                
                print(f"\n🔍 Column: {col}")
                print("-" * 30)
                
                # Get original statistics
                orig_skew = original_distribution['skewness_analysis'][col]['skewness']
                orig_kurt = original_distribution['kurtosis_analysis'][col]['kurtosis']
                orig_normality = original_distribution['normality_tests'][col]['overall_interpretation']
                
                for transform_type, details in col_transformations.items():
                    if not details.get('success', False):
                        continue
                    
                    # Find the transformed column name
                    transformed_col_name = f"{col}_{transform_type}"
                    if transformed_col_name not in transformed_data.columns:
                        continue
                    
                    # Calculate statistics for transformed column
                    transformed_col = transformed_data[transformed_col_name].dropna()
                    
                    if len(transformed_col) == 0:
                        continue
                    
                    from scipy import stats
                    import numpy as np
                    
                    trans_skew = stats.skew(transformed_col)
                    trans_kurt = stats.kurtosis(transformed_col)
                    
                    # Test normality of transformed data
                    if len(transformed_col) > 3:
                        shapiro_stat, shapiro_p = stats.shapiro(transformed_col)
                        dagostino_stat, dagostino_p = stats.normaltest(transformed_col)
                        
                        # Determine normality interpretation
                        if shapiro_p > 0.05 and dagostino_p > 0.05:
                            trans_normality = "Data appears to be normally distributed"
                        else:
                            trans_normality = "Data does not appear to be normally distributed"
                    else:
                        trans_normality = "Insufficient data for normality test"
                    
                    print(f"  {transform_type}:")
                    
                    # Compare normality
                    orig_normal = 'normally distributed' in orig_normality.lower()
                    trans_normal = 'normally distributed' in trans_normality.lower()
                    
                    if not orig_normal and trans_normal:
                        print(f"    Normality: {ColorUtils.green('✅ IMPROVED - Now normally distributed')}")
                    elif orig_normal and trans_normal:
                        print(f"    Normality: {ColorUtils.green('✅ MAINTAINED - Still normally distributed')}")
                    elif not orig_normal and not trans_normal:
                        print(f"    Normality: {ColorUtils.yellow('⚠️  PARTIAL - Still not normally distributed')}")
                    else:
                        print(f"    Normality: {ColorUtils.red('❌ WORSENED - No longer normally distributed')}")
                    
                    # Compare skewness
                    orig_skewness_abs = abs(orig_skew)
                    trans_skewness_abs = abs(trans_skew)
                    
                    if trans_skewness_abs < orig_skewness_abs:
                        improvement = ((orig_skewness_abs - trans_skewness_abs) / orig_skewness_abs) * 100
                        print(f"    Skewness: {ColorUtils.green(f'✅ IMPROVED - Reduced by {improvement:.1f}%')} (orig: {orig_skew:.3f} → trans: {trans_skew:.3f})")
                    elif abs(trans_skewness_abs - orig_skewness_abs) < 0.001:
                        print(f"    Skewness: {ColorUtils.yellow('⚠️  NO CHANGE - Skewness unchanged')} (orig: {orig_skew:.3f} → trans: {trans_skew:.3f})")
                    else:
                        print(f"    Skewness: {ColorUtils.red('❌ WORSENED - Skewness increased')} (orig: {orig_skew:.3f} → trans: {trans_skew:.3f})")
                    
                    # Compare kurtosis
                    orig_kurtosis_abs = abs(orig_kurt)
                    trans_kurtosis_abs = abs(trans_kurt)
                    
                    if trans_kurtosis_abs < orig_kurtosis_abs:
                        improvement = ((orig_kurtosis_abs - trans_kurtosis_abs) / orig_kurtosis_abs) * 100
                        print(f"    Kurtosis: {ColorUtils.green(f'✅ IMPROVED - Reduced by {improvement:.1f}%')} (orig: {orig_kurt:.3f} → trans: {trans_kurt:.3f})")
                    elif abs(trans_kurtosis_abs - orig_kurtosis_abs) < 0.001:
                        print(f"    Kurtosis: {ColorUtils.yellow('⚠️  NO CHANGE - Kurtosis unchanged')} (orig: {orig_kurt:.3f} → trans: {trans_kurt:.3f})")
                    else:
                        print(f"    Kurtosis: {ColorUtils.red('❌ WORSENED - Kurtosis increased')} (orig: {orig_kurt:.3f} → trans: {trans_kurt:.3f})")
            
            print("\n" + "="*80)
            
        except Exception as e:
            print(f"\n❌ Error during transformation validation: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _save_transformed_data(self, results: Dict[str, Any]):
        """Save transformed data to appropriate directory."""
        try:
            file_info = results['file_info']
            transformation_results = results['analysis_results'].get('transformation', {})
            transformed_data = transformation_results.get('transformed_data')
            
            if transformed_data is None:
                print("No transformed data to save.")
                return
            
            # Create save path structure: data/fixed/transformed_by_stat/<source>/<format>/<symbol>/<indicator>/<timeframe>/
            source = file_info.get("source", "unknown")
            format_type = file_info["format"]
            symbol = file_info.get("symbol", "unknown")
            indicator = file_info.get("indicator", "unknown")
            timeframe = file_info.get("timeframe", "unknown")
            
            save_path = f"data/fixed/transformed_by_stat/{source}/{format_type}/{symbol}/{indicator}/{timeframe}/"
            
            # Create directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)
            
            # Generate filename
            filename = f"{symbol}_{timeframe}_{indicator}_transformed.{format_type}"
            full_path = os.path.join(save_path, filename)
            
            # Save data
            self.file_ops.save_data(transformed_data, full_path, format_type)
            
            print(f"\n✅ Transformed data saved to: {full_path}")
            
        except Exception as e:
            print(f"\n❌ Error saving transformed data: {str(e)}")
    
    def run(self, config: Dict[str, Any]) -> None:
        """
        Main execution method.
        
        Args:
            config: Configuration dictionary from CLI
        """
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
                results = self.analyze_file(file_processing['filename'], analysis_options)
                
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
                if analysis_options.get('transform', False) and 'transformation' in results['analysis_results']:
                    self._handle_data_transformation(results)
                
            elif file_processing['mode'] == 'batch':
                # Batch processing
                self.run_batch_processing(file_processing['directory'], 
                                       f"Directory: {file_processing['directory']}", 
                                       analysis_options,
                                       self.auto_mode)
                
            elif file_processing['mode'] == 'batch_all':
                # Process all directories
                directories = [
                    ("data/cache/csv_converted/", "CSV Converted Files"),
                    ("data/raw_parquet/", "Raw Parquet Files"),
                    ("data/indicators/parquet/", "Indicators Parquet Files"),
                    ("data/indicators/json/", "Indicators JSON Files"),
                    ("data/indicators/csv/", "Indicators CSV Files"),
                    ("data/fixed/", "Fixed Files")
                ]
                
                total_successful = 0
                total_failed = 0
                total_files = 0
                
                for directory, name in directories:
                    if os.path.exists(directory):
                        files = self.file_ops.get_files_in_directory(directory)
                        if files:
                            print(f"\n{'='*100}")
                            print(f"PROCESSING DIRECTORY: {name}")
                            print(f"{'='*100}")
                            
                            for filename in files:
                                total_files += 1
                                print(f"\n{'='*60}")
                                print(f"PROCESSING FILE: {filename}")
                                print(f"{'='*60}")
                                
                                try:
                                    results = self.analyze_file(filename, analysis_options)
                                    
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
                                    if analysis_options.get('transform', False) and 'transformation' in results['analysis_results']:
                                        self._handle_data_transformation(results)
                                    
                                    total_successful += 1
                                    print(f"{ColorUtils.green('✅ Successfully processed:')} {filename}")
                                    
                                except Exception as e:
                                    total_failed += 1
                                    self.reporter.display_error(str(e), {'filename': filename})
                
                # Overall summary
                print(f"\n{'='*100}")
                print(f"🌟 BATCH PROCESSING ALL DIRECTORIES COMPLETE 🌟")
                print(f"{'='*100}")
                print(f"📊 Total files processed: {total_files}")
                print(f"✅ Successful: {total_successful}")
                print(f"❌ Failed: {total_failed}")
                if total_files > 0:
                    print(f"📈 Overall success rate: {(total_successful/total_files*100):.1f}%")
                else:
                    print("⚠️  No files found to process.")
                    
            elif file_processing['mode'] == 'custom_path':
                # Custom path processing
                custom_path = file_processing['directory']
                path_validation = self.cli.validate_custom_path(custom_path)
                
                if not path_validation['valid']:
                    print(f"❌ Error: {path_validation['error']}")
                    return
                
                if path_validation['is_file']:
                    # Single file processing
                    print(f"\n📁 Processing single file: {custom_path}")
                    # Extract filename from path
                    filename = os.path.basename(custom_path)
                    # Check if file is in supported directories
                    file_info = self.file_ops.validate_file_path(filename)
                    if file_info is None:
                        # If not in supported directories, try to process directly
                        print(f"⚠️  File '{filename}' not found in supported directories, attempting direct processing...")
                        # Create a mock file_info for direct processing
                        file_info = {
                            "file_path": custom_path,
                            "format": custom_path.split('.')[-1].lower(),
                            "symbol": "Unknown",
                            "timeframe": "Unknown", 
                            "source": "Custom",
                            "indicator": None,
                            "folder_source": os.path.dirname(custom_path)
                        }
                    
                    results = self.analyze_file(filename, analysis_options)
                    
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
                    if analysis_options.get('transform', False) and 'transformation' in results['analysis_results']:
                        self._handle_data_transformation(results)
                        
                elif path_validation['is_directory']:
                    # Directory processing
                    print(f"\n📂 Starting batch processing for custom directory: {custom_path}")
                    self.run_batch_processing(custom_path, f"Custom Directory: {custom_path}", analysis_options, self.auto_mode)
            
            print("\n🎉 Statistical analysis completed successfully!")
            
        except Exception as e:
            print(f"\nError during statistical analysis: {str(e)}")
            sys.exit(1)


def main():
    """Main entry point."""
    cli = StatisticsCLI()
    
    # Parse arguments
    args = cli.parse_arguments()
    
    # Validate arguments
    config = cli.validate_arguments(args)
    
    # Display help examples if requested
    if hasattr(args, 'help_examples') and args.help_examples:
        cli.display_help_examples()
        return
    
    # Confirm analysis configuration
    if not cli.confirm_analysis(config, config['processing_options']['auto']):
        print(ColorUtils.red("❌ Analysis cancelled."))
        return
    
    # Start timing
    start_time = time.time()
    
    # Create the analyzer
    analyzer = StatisticalAnalyzer(
        auto_mode=config['processing_options']['auto'],
        output_directory=config['output_directory'],
        analysis_options=config['analysis_options']
    )
    
    # Run analysis
    analyzer.run(config)
    
    # Calculate and display processing time
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"\n⏱️  Processing completed in {processing_time:.2f} seconds")
    print(f"{ColorUtils.green('🎉 Statistical analysis finished successfully!')}")


if __name__ == "__main__":
    main()
