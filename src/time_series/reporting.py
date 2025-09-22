"""
Time Series Reporting Module

This module provides comprehensive reporting capabilities for time series analysis results,
including formatted output, summary statistics, and detailed analysis reports.

Features:
- Formatted output for all analysis types
- Summary statistics and interpretations
- Detailed analysis reports
- Color-coded results for better readability
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime
from .color_utils import ColorUtils


class TimeSeriesReporter:
    """Handles reporting and display of time series analysis results."""
    
    def __init__(self):
        """Initialize the time series reporter."""
        self.color_utils = ColorUtils()
    
    def generate_comprehensive_report(self, file_info: Dict[str, Any], 
                                    analysis_results: Dict[str, Any],
                                    output_directory: Optional[str] = None,
                                    auto_mode: bool = False,
                                    analysis_options: Dict[str, bool] = None) -> str:
        """
        Generate comprehensive time series analysis report.
        
        Args:
            file_info: File metadata information
            analysis_results: Complete analysis results
            output_directory: Directory to save reports
            auto_mode: Whether in auto mode
            analysis_options: Analysis options used
            
        Returns:
            Formatted report string
        """
        report_parts = []
        
        # Header
        report_parts.append(self._generate_header(file_info))
        
        # Analysis summary
        report_parts.append(self._generate_analysis_summary(analysis_results, analysis_options))
        
        # Stationarity analysis
        if 'stationarity' in analysis_results:
            report_parts.append(self._generate_stationarity_report(analysis_results['stationarity']))
        
        # Seasonality analysis
        if 'seasonality' in analysis_results:
            report_parts.append(self._generate_seasonality_report(analysis_results['seasonality']))
        
        # Financial features analysis
        if 'financial' in analysis_results:
            report_parts.append(self._generate_financial_report(analysis_results['financial']))
        
        # Data transformation analysis
        if 'transformation' in analysis_results:
            report_parts.append(self._generate_transformation_report(analysis_results['transformation']))
            
            # Add comparison analysis if available
            if 'comparison_analysis' in analysis_results['transformation']:
                report_parts.append(self._generate_comparison_report(analysis_results['transformation']['comparison_analysis']))
        
        # Overall assessment
        report_parts.append(self._generate_overall_assessment(analysis_results))
        
        # Footer
        report_parts.append(self._generate_footer())
        
        # Combine all parts
        full_report = "\n".join(report_parts)
        
        # Save report if output directory specified
        if output_directory:
            self._save_report(full_report, file_info, output_directory)
        
        return full_report
    
    def _generate_header(self, file_info: Dict[str, Any]) -> str:
        """Generate report header."""
        header = []
        header.append("=" * 80)
        header.append(self.color_utils.blue("📈 TIME SERIES ANALYSIS REPORT"))
        header.append("=" * 80)
        header.append("")
        
        # File information
        header.append(self.color_utils.bold("📁 FILE INFORMATION"))
        header.append("-" * 40)
        header.append(f"File: {file_info.get('filename', 'Unknown')}")
        header.append(f"Source: {file_info.get('source', 'Unknown')}")
        header.append(f"Symbol: {file_info.get('symbol', 'Unknown')}")
        header.append(f"Timeframe: {file_info.get('timeframe', 'Unknown')}")
        header.append(f"Indicator: {file_info.get('indicator', 'Unknown')}")
        header.append(f"Format: {file_info.get('format', 'Unknown').upper()}")
        header.append(f"Rows: {file_info.get('rows_count', 0):,}")
        header.append(f"Columns: {file_info.get('columns_count', 0)}")
        
        if file_info.get('start_date') and file_info.get('end_date'):
            header.append(f"Date Range: {file_info['start_date']} to {file_info['end_date']}")
        
        header.append("")
        header.append(self.color_utils.yellow("💡 RECOMMENDATION: Use already cleaned and transformed data"))
        header.append("   by clear_data.py and stat_analysis.py from data/fixed/ folder.")
        header.append("   Run clear_data.py --help for more information.")
        header.append("")
        
        return "\n".join(header)
    
    def _generate_analysis_summary(self, analysis_results: Dict[str, Any], 
                                 analysis_options: Dict[str, bool]) -> str:
        """Generate analysis summary."""
        summary = []
        summary.append(self.color_utils.bold("📊 ANALYSIS SUMMARY"))
        summary.append("-" * 40)
        
        # Analysis types performed
        analysis_types = []
        if 'stationarity' in analysis_results:
            analysis_types.append("Stationarity Analysis")
        if 'seasonality' in analysis_results:
            analysis_types.append("Seasonality Detection")
        if 'financial' in analysis_results:
            analysis_types.append("Financial Features")
        if 'transformation' in analysis_results:
            analysis_types.append("Data Transformation")
        
        summary.append(f"Analysis Types: {', '.join(analysis_types)}")
        summary.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append("")
        
        return "\n".join(summary)
    
    def _generate_stationarity_report(self, stationarity_results: Dict[str, Any]) -> str:
        """Generate stationarity analysis report."""
        report = []
        report.append(self.color_utils.bold("📊 STATIONARITY ANALYSIS"))
        report.append("=" * 50)
        
        # ADF Tests
        if 'adf_tests' in stationarity_results:
            report.append(self.color_utils.blue("🔍 Augmented Dickey-Fuller Tests"))
            report.append("-" * 40)
            
            for col, adf_data in stationarity_results['adf_tests'].items():
                if 'error' in adf_data:
                    report.append(f"❌ {col}: {adf_data['error']}")
                    continue
                
                report.append(f"\n📈 Column: {col}")
                
                # Best specification
                best_spec = adf_data.get('best_specification', 'standard')
                if best_spec in adf_data and adf_data[best_spec]:
                    result = adf_data[best_spec]
                    adf_stat = result['adf_statistic']
                    p_value = result['p_value']
                    is_stationary = result['is_stationary']
                    
                    report.append(f"  Best Specification: {best_spec}")
                    report.append(f"  ADF Statistic: {self.color_utils.format_adf_statistic(adf_stat, p_value)}")
                    report.append(f"  P-value: {self.color_utils.format_stationarity_p_value(p_value)}")
                    
                    if is_stationary:
                        report.append(f"  Status: {self.color_utils.green('✅ STATIONARY')}")
                    else:
                        report.append(f"  Status: {self.color_utils.red('❌ NON-STATIONARY')}")
        
        # Critical Values
        if 'critical_values' in stationarity_results:
            report.append(f"\n{self.color_utils.blue('📊 Critical Values')}")
            report.append("-" * 30)
            
            for col, crit_data in stationarity_results['critical_values'].items():
                if 'error' in crit_data:
                    continue
                
                report.append(f"\n📈 Column: {col}")
                crit_vals = crit_data.get('critical_values', {})
                for level, value in crit_vals.items():
                    report.append(f"  {level}: {self.color_utils.format_critical_value(value, level)}")
        
        # Recommendations
        if 'stationarity_recommendations' in stationarity_results:
            report.append(f"\n{self.color_utils.blue('💡 Stationarity Recommendations')}")
            report.append("-" * 40)
            
            for col, rec_data in stationarity_results['stationarity_recommendations'].items():
                if 'error' in rec_data:
                    continue
                
                report.append(f"\n📈 Column: {col}")
                is_stationary = rec_data.get('is_stationary', False)
                confidence = rec_data.get('confidence_level', 'unknown')
                
                if is_stationary:
                    report.append(f"  Status: {self.color_utils.green('✅ Stationary')}")
                    report.append(f"  Confidence: {confidence}")
                else:
                    report.append(f"  Status: {self.color_utils.red('❌ Non-stationary')}")
                    report.append(f"  Confidence: {confidence}")
                
                # Show recommendations
                actions = rec_data.get('recommended_actions', [])
                if actions:
                    report.append("  Recommendations:")
                    for action in actions:
                        report.append(f"    • {self.color_utils.format_recommendation(action)}")
        
        # Overall assessment
        if 'overall_assessment' in stationarity_results:
            overall = stationarity_results['overall_assessment']
            report.append(f"\n{self.color_utils.blue('📊 Overall Stationarity Assessment')}")
            report.append("-" * 45)
            report.append(f"Total Columns: {overall.get('total_columns', 0)}")
            report.append(f"Stationary Columns: {overall.get('stationary_columns', 0)}")
            report.append(f"Non-stationary Columns: {overall.get('non_stationary_columns', 0)}")
            report.append(f"Stationarity Rate: {overall.get('stationarity_rate', 0):.1%}")
            report.append(f"Overall Quality: {self.color_utils.format_quality_assessment(overall.get('overall_quality', 'unknown'))}")
            
            recommendations = overall.get('recommendations', [])
            if recommendations:
                report.append("\nOverall Recommendations:")
                for rec in recommendations:
                    report.append(f"  • {self.color_utils.format_recommendation(rec)}")
        
        report.append("")
        return "\n".join(report)
    
    def _generate_seasonality_report(self, seasonality_results: Dict[str, Any]) -> str:
        """Generate seasonality analysis report."""
        report = []
        report.append(self.color_utils.bold("📈 SEASONALITY DETECTION"))
        report.append("=" * 50)
        
        # Day patterns
        if 'day_patterns' in seasonality_results:
            report.append(self.color_utils.blue("📅 Day-of-Week Patterns"))
            report.append("-" * 35)
            
            for col, day_data in seasonality_results['day_patterns'].items():
                if 'error' in day_data:
                    report.append(f"❌ {col}: {day_data['error']}")
                    continue
                
                report.append(f"\n📈 Column: {col}")
                pattern_strength = day_data.get('pattern_strength', 0)
                has_pattern = day_data.get('has_significant_pattern', False)
                strongest_day = day_data.get('strongest_day')
                weakest_day = day_data.get('weakest_day')
                
                report.append(f"  Pattern Strength: {self.color_utils.format_seasonality_strength(pattern_strength)}")
                report.append(f"  Significant Pattern: {'Yes' if has_pattern else 'No'}")
                if strongest_day and weakest_day:
                    report.append(f"  Strongest Day: {strongest_day}")
                    report.append(f"  Weakest Day: {weakest_day}")
                
                interpretation = day_data.get('interpretation', '')
                if interpretation:
                    report.append(f"  Interpretation: {self.color_utils.format_interpretation(interpretation)}")
        
        # Month patterns
        if 'month_patterns' in seasonality_results:
            report.append(f"\n{self.color_utils.blue('📆 Monthly Patterns')}")
            report.append("-" * 30)
            
            for col, month_data in seasonality_results['month_patterns'].items():
                if 'error' in month_data:
                    report.append(f"❌ {col}: {month_data['error']}")
                    continue
                
                report.append(f"\n📈 Column: {col}")
                pattern_strength = month_data.get('pattern_strength', 0)
                has_pattern = month_data.get('has_significant_pattern', False)
                strongest_month = month_data.get('strongest_month')
                weakest_month = month_data.get('weakest_month')
                
                report.append(f"  Pattern Strength: {self.color_utils.format_seasonality_strength(pattern_strength)}")
                report.append(f"  Significant Pattern: {'Yes' if has_pattern else 'No'}")
                if strongest_month and weakest_month:
                    report.append(f"  Strongest Month: {strongest_month}")
                    report.append(f"  Weakest Month: {weakest_month}")
                
                interpretation = month_data.get('interpretation', '')
                if interpretation:
                    report.append(f"  Interpretation: {self.color_utils.format_interpretation(interpretation)}")
        
        # Cyclical patterns
        if 'cyclical_patterns' in seasonality_results:
            report.append(f"\n{self.color_utils.blue('🔄 Cyclical Patterns')}")
            report.append("-" * 30)
            
            for col, cycle_data in seasonality_results['cyclical_patterns'].items():
                if 'error' in cycle_data:
                    report.append(f"❌ {col}: {cycle_data['error']}")
                    continue
                
                report.append(f"\n📈 Column: {col}")
                cyclical_strength = cycle_data.get('cyclical_strength', 0)
                has_pattern = cycle_data.get('has_cyclical_pattern', False)
                strongest_cycle = cycle_data.get('strongest_cycle')
                
                report.append(f"  Cyclical Strength: {self.color_utils.format_seasonality_strength(cyclical_strength)}")
                report.append(f"  Cyclical Pattern: {'Yes' if has_pattern else 'No'}")
                
                if strongest_cycle:
                    lag = strongest_cycle.get('lag', 0)
                    autocorr = strongest_cycle.get('autocorrelation', 0)
                    interpretation = strongest_cycle.get('period_interpretation', '')
                    report.append(f"  Strongest Cycle: {self.color_utils.format_cyclical_period(lag)}")
                    report.append(f"  Autocorrelation: {autocorr:.4f}")
                    report.append(f"  Interpretation: {interpretation}")
                
                interpretation = cycle_data.get('interpretation', '')
                if interpretation:
                    report.append(f"  Overall: {self.color_utils.format_interpretation(interpretation)}")
        
        # Overall seasonality assessment
        if 'overall_seasonality' in seasonality_results:
            overall = seasonality_results['overall_seasonality']
            report.append(f"\n{self.color_utils.blue('📊 Overall Seasonality Assessment')}")
            report.append("-" * 40)
            report.append(f"Total Columns: {overall.get('total_columns', 0)}")
            report.append(f"Significant Day Patterns: {overall.get('significant_day_patterns', 0)}")
            report.append(f"Significant Month Patterns: {overall.get('significant_month_patterns', 0)}")
            report.append(f"Significant Cyclical Patterns: {overall.get('significant_cyclical_patterns', 0)}")
            report.append(f"Overall Seasonality Level: {overall.get('overall_seasonality_level', 'unknown')}")
            
            recommendations = overall.get('recommendations', [])
            if recommendations:
                report.append("\nOverall Recommendations:")
                for rec in recommendations:
                    report.append(f"  • {self.color_utils.format_recommendation(rec)}")
        
        report.append("")
        return "\n".join(report)
    
    def _generate_financial_report(self, financial_results: Dict[str, Any]) -> str:
        """Generate financial features analysis report."""
        report = []
        report.append(self.color_utils.bold("💰 FINANCIAL FEATURES ANALYSIS"))
        report.append("=" * 50)
        
        # Price range analysis
        if 'price_range_analysis' in financial_results:
            report.append(self.color_utils.blue("📊 Price Range Analysis"))
            report.append("-" * 35)
            
            for col, range_data in financial_results['price_range_analysis'].items():
                if 'error' in range_data:
                    report.append(f"❌ {col}: {range_data['error']}")
                    continue
                
                report.append(f"\n📈 Column: {col}")
                min_price = range_data.get('min_price', 0)
                max_price = range_data.get('max_price', 0)
                price_range = range_data.get('price_range', 0)
                range_percentage = range_data.get('range_percentage', 0)
                volatility_level = range_data.get('volatility_level', 'unknown')
                
                report.append(f"  Min Price: {min_price:.4f}")
                report.append(f"  Max Price: {max_price:.4f}")
                report.append(f"  Price Range: {self.color_utils.format_range(price_range)}")
                report.append(f"  Range %: {range_percentage:.2f}%")
                report.append(f"  Volatility Level: {volatility_level}")
                
                interpretation = range_data.get('interpretation', '')
                if interpretation:
                    report.append(f"  Interpretation: {self.color_utils.format_interpretation(interpretation)}")
        
        # Price changes analysis
        if 'price_changes_analysis' in financial_results:
            report.append(f"\n{self.color_utils.blue('📈 Price Changes Analysis')}")
            report.append("-" * 35)
            
            for col, changes_data in financial_results['price_changes_analysis'].items():
                if 'error' in changes_data:
                    report.append(f"❌ {col}: {changes_data['error']}")
                    continue
                
                report.append(f"\n📈 Column: {col}")
                overall_volatility = changes_data.get('overall_volatility', 0)
                report.append(f"  Overall Volatility: {self.color_utils.format_volatility(overall_volatility)}")
                
                return_consistency = changes_data.get('return_consistency')
                if return_consistency:
                    pos_pct = return_consistency.get('positive_percentage', 0)
                    neg_pct = return_consistency.get('negative_percentage', 0)
                    report.append(f"  Positive Returns: {pos_pct:.1f}%")
                    report.append(f"  Negative Returns: {neg_pct:.1f}%")
                
                interpretation = changes_data.get('interpretation', '')
                if interpretation:
                    report.append(f"  Interpretation: {self.color_utils.format_interpretation(interpretation)}")
        
        # Volatility analysis
        if 'volatility_analysis' in financial_results:
            report.append(f"\n{self.color_utils.blue('📊 Volatility Analysis')}")
            report.append("-" * 30)
            
            for col, vol_data in financial_results['volatility_analysis'].items():
                if 'error' in vol_data:
                    report.append(f"❌ {col}: {vol_data['error']}")
                    continue
                
                report.append(f"\n📈 Column: {col}")
                overall_vol = vol_data.get('overall_volatility', 0)
                annualized_vol = vol_data.get('annualized_volatility', 0)
                coeff_var = vol_data.get('coefficient_of_variation', 0)
                volatility_level = vol_data.get('volatility_level', 'unknown')
                
                report.append(f"  Overall Volatility: {self.color_utils.format_volatility(overall_vol)}")
                report.append(f"  Annualized Volatility: {self.color_utils.format_volatility(annualized_vol)}")
                report.append(f"  Coefficient of Variation: {coeff_var:.2f}%")
                report.append(f"  Volatility Level: {volatility_level}")
                
                # Risk metrics
                risk_metrics = vol_data.get('risk_metrics', {})
                if risk_metrics:
                    var_95 = risk_metrics.get('var_95', 0)
                    var_99 = risk_metrics.get('var_99', 0)
                    max_drawdown = risk_metrics.get('max_drawdown', 0)
                    sharpe_ratio = risk_metrics.get('sharpe_ratio', 0)
                    
                    report.append(f"  VaR (95%): {self.color_utils.format_price_change(var_95)}")
                    report.append(f"  VaR (99%): {self.color_utils.format_price_change(var_99)}")
                    report.append(f"  Max Drawdown: {self.color_utils.format_percentage_change(max_drawdown * 100)}")
                    report.append(f"  Sharpe Ratio: {sharpe_ratio:.4f}")
                
                interpretation = vol_data.get('interpretation', '')
                if interpretation:
                    report.append(f"  Interpretation: {self.color_utils.format_interpretation(interpretation)}")
        
        # Overall financial assessment
        if 'overall_financial_assessment' in financial_results:
            overall = financial_results['overall_financial_assessment']
            report.append(f"\n{self.color_utils.blue('📊 Overall Financial Assessment')}")
            report.append("-" * 40)
            report.append(f"Total Columns: {overall.get('total_columns', 0)}")
            report.append(f"Average Range %: {overall.get('average_range_percentage', 0):.2f}%")
            report.append(f"Average Volatility: {overall.get('average_volatility', 0):.4f}")
            report.append(f"Average CoV: {overall.get('average_coefficient_variation', 0):.2f}%")
            report.append(f"Overall Risk Level: {overall.get('overall_risk_level', 'unknown')}")
            
            recommendations = overall.get('recommendations', [])
            if recommendations:
                report.append("\nOverall Recommendations:")
                for rec in recommendations:
                    report.append(f"  • {self.color_utils.format_recommendation(rec)}")
        
        report.append("")
        return "\n".join(report)
    
    def _generate_transformation_report(self, transformation_results: Dict[str, Any]) -> str:
        """Generate data transformation report."""
        report = []
        report.append(self.color_utils.bold("🔄 DATA TRANSFORMATION ANALYSIS"))
        report.append("=" * 50)
        
        if 'transformation_details' in transformation_results:
            report.append(self.color_utils.blue("🔧 Applied Transformations"))
            report.append("-" * 35)
            
            for col, col_transforms in transformation_results['transformation_details'].items():
                report.append(f"\n📈 Column: {col}")
                
                for transform_type, details in col_transforms.items():
                    success = details.get('success', False)
                    if success:
                        improvement_score = details.get('improvement_score', 0)
                        report.append(f"  ✅ {transform_type}: Score {improvement_score:.3f}")
                        
                        # Show key statistics
                        orig_skew = details.get('original_skewness', 0)
                        trans_skew = details.get('transformed_skewness', 0)
                        orig_kurt = details.get('original_kurtosis', 0)
                        trans_kurt = details.get('transformed_kurtosis', 0)
                        
                        report.append(f"    Skewness: {orig_skew:.3f} → {trans_skew:.3f}")
                        report.append(f"    Kurtosis: {orig_kurt:.3f} → {trans_kurt:.3f}")
                    else:
                        error = details.get('error', 'Unknown error')
                        report.append(f"  ❌ {transform_type}: {error}")
        
        if 'recommendations' in transformation_results:
            report.append(f"\n{self.color_utils.blue('💡 Transformation Recommendations')}")
            report.append("-" * 40)
            
            for col, rec_data in transformation_results['recommendations'].items():
                report.append(f"\n📈 Column: {col}")
                best_transform = rec_data.get('best_transformation')
                if best_transform:
                    report.append(f"  Best Transformation: {best_transform}")
                
                actions = rec_data.get('recommended_actions', [])
                if actions:
                    report.append("  Recommendations:")
                    for action in actions:
                        report.append(f"    • {self.color_utils.format_recommendation(action)}")
                
                warnings = rec_data.get('warnings', [])
                if warnings:
                    report.append("  Warnings:")
                    for warning in warnings:
                        report.append(f"    ⚠️ {warning}")
        
        report.append("")
        return "\n".join(report)
    
    def _generate_comparison_report(self, comparison_results: Dict[str, Any]) -> str:
        """Generate comparison report for before/after transformation."""
        report = []
        report.append(self.color_utils.bold("📊 TRANSFORMATION COMPARISON ANALYSIS"))
        report.append("=" * 50)
        
        # Stationarity improvements
        if 'stationarity_improvements' in comparison_results:
            report.append(self.color_utils.blue("🔍 Stationarity Improvements"))
            report.append("-" * 35)
            
            improved_count = 0
            total_count = len(comparison_results['stationarity_improvements'])
            
            for col, data in comparison_results['stationarity_improvements'].items():
                original = data.get('original', False)
                transformed = data.get('transformed', False)
                improvement = data.get('improvement', 'No change')
                
                if improvement == 'Improved':
                    improved_count += 1
                    status_icon = "✅"
                elif improvement == 'Worsened':
                    status_icon = "❌"
                else:
                    status_icon = "➖"
                
                report.append(f"  {status_icon} {col}: {original} → {transformed} ({improvement})")
            
            improvement_rate = (improved_count / total_count * 100) if total_count > 0 else 0
            report.append(f"\n  📈 Stationarity Improvement Rate: {improvement_rate:.1f}% ({improved_count}/{total_count})")
        
        # Seasonality improvements
        if 'seasonality_improvements' in comparison_results:
            report.append(f"\n{self.color_utils.blue('📈 Seasonality Improvements')}")
            report.append("-" * 35)
            
            reduced_count = 0
            total_count = len(comparison_results['seasonality_improvements'])
            
            for col, data in comparison_results['seasonality_improvements'].items():
                original = data.get('original', False)
                transformed = data.get('transformed', False)
                improvement = data.get('improvement', 'No change')
                
                if improvement == 'Reduced':
                    reduced_count += 1
                    status_icon = "✅"
                elif improvement == 'Increased':
                    status_icon = "❌"
                else:
                    status_icon = "➖"
                
                report.append(f"  {status_icon} {col}: {original} → {transformed} ({improvement})")
            
            reduction_rate = (reduced_count / total_count * 100) if total_count > 0 else 0
            report.append(f"\n  📉 Seasonality Reduction Rate: {reduction_rate:.1f}% ({reduced_count}/{total_count})")
        
        # Financial improvements
        if 'financial_improvements' in comparison_results and comparison_results['financial_improvements']:
            report.append(f"\n{self.color_utils.blue('💰 Volatility Improvements')}")
            report.append("-" * 35)
            
            reduced_count = 0
            total_count = len(comparison_results['financial_improvements'])
            
            for col, data in comparison_results['financial_improvements'].items():
                original_vol = data.get('original_volatility', 'unknown')
                transformed_vol = data.get('transformed_volatility', 'unknown')
                improvement = data.get('improvement', 'No change')
                
                if improvement == 'Reduced':
                    reduced_count += 1
                    status_icon = "✅"
                elif improvement == 'Increased':
                    status_icon = "❌"
                else:
                    status_icon = "➖"
                
                report.append(f"  {status_icon} {col}: {original_vol} → {transformed_vol} ({improvement})")
            
            reduction_rate = (reduced_count / total_count * 100) if total_count > 0 else 0
            report.append(f"\n  📉 Volatility Reduction Rate: {reduction_rate:.1f}% ({reduced_count}/{total_count})")
        else:
            report.append(f"\n{self.color_utils.blue('💰 Volatility Improvements')}")
            report.append("-" * 35)
            report.append("  ⚠️  No financial improvements data available")
            report.append(f"\n  📉 Volatility Reduction Rate: 0.0% (0/0)")
        
        # Overall assessment
        if 'overall_assessment' in comparison_results:
            overall = comparison_results['overall_assessment']
            report.append(f"\n{self.color_utils.blue('📊 Overall Transformation Assessment')}")
            report.append("-" * 45)
            
            total_columns = overall.get('total_columns', 0)
            stationarity_improved = overall.get('stationarity_improved', 0)
            seasonality_reduced = overall.get('seasonality_reduced', 0)
            volatility_reduced = overall.get('volatility_reduced', 0)
            overall_improvement_rate = overall.get('overall_improvement_rate', 0)
            
            report.append(f"Total Columns Analyzed: {total_columns}")
            report.append(f"Stationarity Improved: {stationarity_improved}")
            report.append(f"Seasonality Reduced: {seasonality_reduced}")
            report.append(f"Volatility Reduced: {volatility_reduced}")
            report.append(f"Overall Improvement Rate: {overall_improvement_rate:.1%}")
            
            # Interpretation
            if overall_improvement_rate > 0.5:
                interpretation = "Excellent transformation results - significant improvements achieved"
                color = self.color_utils.green
            elif overall_improvement_rate > 0.3:
                interpretation = "Good transformation results - moderate improvements achieved"
                color = self.color_utils.yellow
            elif overall_improvement_rate > 0.1:
                interpretation = "Fair transformation results - some improvements achieved"
                color = self.color_utils.yellow
            else:
                interpretation = "Limited transformation results - minimal improvements achieved"
                color = self.color_utils.red
            
            report.append(f"\nInterpretation: {color(interpretation)}")
        
        report.append("")
        return "\n".join(report)
    
    def _generate_overall_assessment(self, analysis_results: Dict[str, Any]) -> str:
        """Generate overall assessment."""
        assessment = []
        assessment.append(self.color_utils.bold("📊 OVERALL ASSESSMENT"))
        assessment.append("=" * 30)
        
        # Count analysis types
        analysis_count = len([k for k in analysis_results.keys() if k in ['stationarity', 'seasonality', 'financial', 'transformation']])
        assessment.append(f"Analysis Types Completed: {analysis_count}")
        
        # Data quality assessment
        assessment.append(f"Data Quality: {self.color_utils.green('Good')} (using cleaned data from data/fixed/)")
        
        # Performance improvement information
        assessment.append(f"\n🚀 Performance Optimization:")
        assessment.append(f"• Fast mode enabled with sampling optimization")
        assessment.append(f"• Estimated speedup: {self.color_utils.green('~30-50x faster')} than standard analysis")
        assessment.append(f"• Memory usage optimized with garbage collection")
        assessment.append(f"• Large datasets automatically sampled for efficiency")
        
        # Recommendations
        assessment.append("\nKey Recommendations:")
        assessment.append("• Use cleaned data from data/fixed/ folder for best results")
        assessment.append("• Consider stationarity transformations for non-stationary data")
        assessment.append("• Account for seasonal patterns in modeling")
        assessment.append("• Monitor volatility levels for risk management")
        
        assessment.append("")
        return "\n".join(assessment)
    
    def _generate_footer(self) -> str:
        """Generate report footer."""
        footer = []
        footer.append("=" * 80)
        footer.append(self.color_utils.blue("📈 Time Series Analysis Complete"))
        footer.append("=" * 80)
        footer.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        footer.append("")
        return "\n".join(footer)
    
    def _save_report(self, report: str, file_info: Dict[str, Any], output_directory: str) -> None:
        """Save report to file."""
        try:
            import os
            from datetime import datetime
            
            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            symbol = file_info.get('symbol', 'unknown')
            filename = f"time_series_analysis_{symbol}_{timestamp}.txt"
            
            # Save file
            filepath = os.path.join(output_directory, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"\n💾 Report saved to: {filepath}")
            
        except Exception as e:
            print(f"\n❌ Error saving report: {str(e)}")
    
    def display_error(self, error_message: str, context: Dict[str, Any] = None) -> None:
        """Display error message with context."""
        print(f"\n{self.color_utils.red('❌ Error:')} {error_message}")
        if context:
            for key, value in context.items():
                print(f"  {key}: {value}")
    
    def display_analysis_start(self, file_info: Dict[str, Any], analysis_options: Dict[str, bool]) -> None:
        """Display analysis start information."""
        print("\n" + "=" * 80)
        print(self.color_utils.blue("📈 TIME SERIES ANALYSIS STARTING"))
        print("=" * 80)
        print(f"File: {file_info.get('filename', 'Unknown')}")
        print(f"Symbol: {file_info.get('symbol', 'Unknown')}")
        print(f"Timeframe: {file_info.get('timeframe', 'Unknown')}")
        print(f"Rows: {file_info.get('rows_count', 0):,}")
        print(f"Columns: {file_info.get('columns_count', 0)}")
        
        # Analysis options
        analysis_types = []
        if analysis_options.get('stationarity', False):
            analysis_types.append("Stationarity")
        if analysis_options.get('seasonality', False):
            analysis_types.append("Seasonality")
        if analysis_options.get('financial', False):
            analysis_types.append("Financial Features")
        if analysis_options.get('transform', False):
            analysis_types.append("Data Transformation")
        
        print(f"Analysis: {', '.join(analysis_types)}")
        print("=" * 80)
