"""
Statistics Reporting Module

This module provides comprehensive reporting capabilities for statistical analysis results.
It includes detailed report generation, summary statistics, and formatted output.

Features:
- Detailed analysis reports
- Summary statistics
- Formatted output for different analysis types
- Progress tracking and status updates
- Error reporting and warnings
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import os
import json
import logging
from .color_utils import ColorUtils


class StatisticsReporter:
    """Handles reporting and output formatting for statistical analysis."""
    
    def __init__(self):
        """Initialize the statistics reporter."""
        self.logger = logging.getLogger(__name__)
    
    def generate_comprehensive_report(self, file_info: Dict[str, Any], 
                                    analysis_results: Dict[str, Any],
                                    output_directory: Optional[str] = None) -> str:
        """
        Generate a comprehensive analysis report.
        
        Args:
            file_info: File metadata information
            analysis_results: Results from statistical analysis
            output_directory: Directory to save report files
            
        Returns:
            Formatted comprehensive report string
        """
        report_sections = []
        
        # Header
        report_sections.append(self._generate_header(file_info))
        
        # File information
        report_sections.append(self._generate_file_info_section(file_info))
        
        # Descriptive statistics
        if 'descriptive' in analysis_results:
            report_sections.append(self._generate_analysis_description("descriptive"))
            report_sections.append(self._generate_descriptive_section(analysis_results['descriptive']))
        
        # Distribution analysis
        if 'distribution' in analysis_results:
            report_sections.append(self._generate_analysis_description("distribution"))
            report_sections.append(self._generate_distribution_section(analysis_results['distribution']))
        
        # Data transformation
        if 'transformation' in analysis_results:
            report_sections.append(self._generate_analysis_description("transformation"))
            report_sections.append(self._generate_transformation_section(analysis_results['transformation']))
        
        # Summary and recommendations
        report_sections.append(self._generate_summary_section(analysis_results))
        
        # Statistical glossary
        report_sections.append(self._generate_statistical_glossary())
        
        # Combine all sections
        full_report = "\n\n".join(report_sections)
        
        # Save report if output directory is specified
        if output_directory:
            self._save_report(full_report, file_info, output_directory)
        
        return full_report
    
    def _generate_header(self, file_info: Dict[str, Any]) -> str:
        """Generate report header."""
        header = []
        header.append("=" * 100)
        header.append("📊 COMPREHENSIVE STATISTICAL ANALYSIS REPORT")
        header.append("=" * 100)
        header.append(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        header.append(f"📁 File: {file_info.get('filename', 'Unknown')}")
        header.append(f"📂 Source: {file_info.get('source', 'Unknown')}")
        header.append(f"📊 Symbol: {file_info.get('symbol', 'Unknown')}")
        header.append(f"⏰ Timeframe: {file_info.get('timeframe', 'Unknown')}")
        if file_info.get('indicator'):
            header.append(f"📈 Indicator: {file_info.get('indicator', 'Unknown')}")
        header.append("=" * 100)
        
        return "\n".join(header)
    
    def _generate_analysis_description(self, analysis_type: str) -> str:
        """Generate description for analysis type."""
        descriptions = {
            "descriptive": {
                "title": "📊 DESCRIPTIVE STATISTICS - OVERVIEW",
                "description": [
                    "Descriptive statistics provide a summary of the main characteristics of your dataset.",
                    "This analysis helps you understand the basic properties of your data without making",
                    "inferences about the larger population.",
                    "",
                    "What it includes:",
                    "• Basic statistics (mean, median, standard deviation, min, max)",
                    "• Distribution characteristics (skewness, kurtosis)",
                    "• Variability measures (variance, coefficient of variation, IQR, range)",
                    "• Missing data analysis",
                    "",
                    "How to use:",
                    "• Use this to get a quick overview of your data quality and distribution",
                    "• Identify potential data issues (missing values, extreme values)",
                    "• Understand the central tendency and spread of your data",
                    "• Determine if data transformation might be needed"
                ]
            },
            "distribution": {
                "title": "📈 DISTRIBUTION ANALYSIS - OVERVIEW",
                "description": [
                    "Distribution analysis examines how your data is distributed and whether it follows",
                    "a normal (Gaussian) distribution. This is crucial for many statistical methods.",
                    "",
                    "What it includes:",
                    "• Normality tests (Shapiro-Wilk, D'Agostino-Pearson)",
                    "• Skewness analysis (measure of asymmetry)",
                    "• Kurtosis analysis (measure of tail heaviness)",
                    "• Transformation recommendations",
                    "",
                    "Why it matters:",
                    "• Many statistical tests assume normal distribution",
                    "• Helps determine if data transformation is needed",
                    "• Identifies outliers and extreme values",
                    "• Guides model selection and parameter estimation",
                    "",
                    "How to interpret:",
                    "• Green = Good/Normal distribution",
                    "• Yellow = Moderate deviation, consider transformation",
                    "• Red = Strong deviation, transformation recommended"
                ]
            },
            "transformation": {
                "title": "🔄 DATA TRANSFORMATION ANALYSIS - OVERVIEW",
                "description": [
                    "Data transformation applies mathematical functions to make your data more suitable",
                    "for statistical analysis, especially when data doesn't follow a normal distribution.",
                    "",
                    "What it includes:",
                    "• Applies recommended transformations (log, Box-Cox, etc.)",
                    "• Compares original vs transformed data",
                    "• Measures improvement in distribution characteristics",
                    "• Provides transformation details and parameters",
                    "",
                    "Common transformations:",
                    "• Log transformation: Reduces right skewness, stabilizes variance",
                    "• Box-Cox transformation: Automatically finds optimal transformation",
                    "• Square root: Mild transformation for count data",
                    "• Square: For left-skewed data",
                    "",
                    "Benefits:",
                    "• Makes data more normally distributed",
                    "• Improves model performance",
                    "• Reduces impact of outliers",
                    "• Enables use of parametric statistical tests"
                ]
            }
        }
        
        if analysis_type not in descriptions:
            return ""
        
        desc = descriptions[analysis_type]
        section = []
        section.append("=" * 100)
        section.append(desc["title"])
        section.append("=" * 100)
        section.extend(desc["description"])
        section.append("=" * 100)
        
        return "\n".join(section)
    
    def _generate_statistical_glossary(self) -> str:
        """Generate glossary of statistical terms."""
        glossary = []
        glossary.append("📚 STATISTICAL TERMS GLOSSARY")
        glossary.append("=" * 100)
        
        terms = {
            "Skewness": {
                "definition": "Measures the asymmetry of data distribution around the mean",
                "interpretation": [
                    "• 0 = Perfectly symmetric (normal distribution)",
                    "• Positive = Right tail is longer (right-skewed)",
                    "• Negative = Left tail is longer (left-skewed)",
                    "• |skewness| < 0.5 = Approximately symmetric",
                    "• |skewness| 0.5-1.0 = Moderately skewed",
                    "• |skewness| > 1.0 = Highly skewed"
                ]
            },
            "Kurtosis": {
                "definition": "Measures the 'tailedness' or heaviness of the distribution tails",
                "interpretation": [
                    "• 0 = Normal distribution (mesokurtic)",
                    "• Positive = Heavy tails, more extreme values (leptokurtic)",
                    "• Negative = Light tails, fewer extreme values (platykurtic)",
                    "• |kurtosis| < 0.5 = Approximately normal",
                    "• |kurtosis| 0.5-1.0 = Slightly different from normal",
                    "• |kurtosis| > 1.0 = Significantly different from normal"
                ]
            },
            "Highly skewed (right-tailed)": {
                "definition": "Data has a long right tail with most values clustered on the left",
                "characteristics": [
                    "• Mean > Median > Mode",
                    "• Many small values, few very large values",
                    "• Common in income, house prices, response times",
                    "• May indicate log-normal distribution"
                ]
            },
            "Approximately normal (mesokurtic)": {
                "definition": "Data follows a bell-shaped curve with moderate tail thickness",
                "characteristics": [
                    "• Symmetric around the mean",
                    "• 68% of data within 1 standard deviation",
                    "• 95% of data within 2 standard deviations",
                    "• Ideal for most statistical tests"
                ]
            },
            "Heavy-tailed (leptokurtic)": {
                "definition": "Distribution has fatter tails than normal, more extreme values",
                "characteristics": [
                    "• More outliers than normal distribution",
                    "• Higher probability of extreme values",
                    "• Common in financial returns, stock prices",
                    "• May indicate risk or volatility"
                ]
            },
            "Moderately skewed (right-tailed)": {
                "definition": "Data shows moderate right skewness, not severe but noticeable",
                "characteristics": [
                    "• Somewhat asymmetric",
                    "• May benefit from transformation",
                    "• Still usable for many analyses",
                    "• Consider log transformation"
                ]
            },
            "Light-tailed (platykurtic)": {
                "definition": "Distribution has thinner tails than normal, fewer extreme values",
                "characteristics": [
                    "• Fewer outliers than expected",
                    "• Data more concentrated around mean",
                    "• May indicate data quality issues",
                    "• Consider investigating data collection"
                ]
            },
            "Variance": {
                "definition": "Average of squared differences from the mean",
                "interpretation": [
                    "• Measures data spread around the mean",
                    "• Higher variance = more spread out data",
                    "• Lower variance = more clustered data",
                    "• Square root of variance = standard deviation"
                ]
            },
            "Coefficient of Variation": {
                "definition": "Standard deviation divided by mean, expressed as percentage",
                "interpretation": [
                    "• < 15% = Low variability (consistent data)",
                    "• 15-35% = Moderate variability",
                    "• > 35% = High variability (inconsistent data)",
                    "• Useful for comparing variability across different scales"
                ]
            },
            "High variability": {
                "definition": "Data shows large spread or inconsistency",
                "implications": [
                    "• Data points are widely scattered",
                    "• May indicate measurement errors",
                    "• Could suggest multiple populations",
                    "• Consider data cleaning or stratification"
                ]
            },
            "IQR (Interquartile Range)": {
                "definition": "Difference between 75th and 25th percentiles",
                "interpretation": [
                    "• Measures middle 50% of data spread",
                    "• Less sensitive to outliers than range",
                    "• Used to identify outliers (1.5 × IQR rule)",
                    "• Robust measure of variability"
                ]
            },
            "Range": {
                "definition": "Difference between maximum and minimum values",
                "interpretation": [
                    "• Shows total spread of data",
                    "• Sensitive to outliers",
                    "• Simple but limited measure",
                    "• Good for initial data exploration"
                ]
            },
            "Shapiro-Wilk Test": {
                "definition": "Statistical test for normality, especially good for small samples",
                "interpretation": [
                    "• p > 0.05 = Data appears normal",
                    "• p ≤ 0.05 = Data does not appear normal",
                    "• Most powerful for n < 50",
                    "• Sensitive to outliers"
                ]
            },
            "D'Agostino-Pearson Test": {
                "definition": "Combines skewness and kurtosis to test normality",
                "interpretation": [
                    "• p > 0.05 = Data appears normal",
                    "• p ≤ 0.05 = Data does not appear normal",
                    "• Good for larger samples",
                    "• Tests both skewness and kurtosis together"
                ]
            },
            "Z-Score": {
                "definition": "Number of standard deviations a value is from the mean",
                "interpretation": [
                    "• |Z| < 2 = Normal range",
                    "• |Z| 2-3 = Unusual but not extreme",
                    "• |Z| > 3 = Extreme outlier",
                    "• Z = (value - mean) / standard deviation"
                ]
            },
            "Severity": {
                "definition": "Level of deviation from normal distribution",
                "levels": [
                    "• Low = Minor deviation, no action needed",
                    "• Moderate = Noticeable deviation, consider transformation",
                    "• Severe = Strong deviation, transformation recommended",
                    "• Critical = Extreme deviation, immediate action needed"
                ]
            },
            "Log Transformation": {
                "definition": "Applies natural logarithm to data values",
                "use_cases": [
                    "• Reduces right skewness",
                    "• Stabilizes variance",
                    "• Good for multiplicative relationships",
                    "• Cannot handle zero or negative values"
                ]
            },
            "Box-Cox Transformation": {
                "definition": "Power transformation that finds optimal lambda parameter",
                "benefits": [
                    "• Automatically finds best transformation",
                    "• Handles zero and negative values (with shift)",
                    "• Most versatile transformation",
                    "• Can handle various distribution shapes"
                ]
            },
            "Square Root Transformation": {
                "definition": "Applies square root function to data values",
                "use_cases": [
                    "• Mild transformation for count data",
                    "• Reduces right skewness moderately",
                    "• Good for Poisson-like distributions",
                    "• Cannot handle negative values"
                ]
            },
            "Square Transformation": {
                "definition": "Squares data values",
                "use_cases": [
                    "• For left-skewed data",
                    "• Increases right skewness",
                    "• Rarely used in practice",
                    "• May indicate data quality issues"
                ]
            }
        }
        
        for term, info in terms.items():
            glossary.append(f"\n{ColorUtils.bold(term)}:")
            glossary.append(f"  {info['definition']}")
            if 'interpretation' in info:
                glossary.append("  Interpretation:")
                glossary.extend([f"    {item}" for item in info['interpretation']])
            if 'characteristics' in info:
                glossary.append("  Characteristics:")
                glossary.extend([f"    {item}" for item in info['characteristics']])
            if 'implications' in info:
                glossary.append("  Implications:")
                glossary.extend([f"    {item}" for item in info['implications']])
            if 'levels' in info:
                glossary.append("  Levels:")
                glossary.extend([f"    {item}" for item in info['levels']])
            if 'use_cases' in info:
                glossary.append("  Use Cases:")
                glossary.extend([f"    {item}" for item in info['use_cases']])
            if 'benefits' in info:
                glossary.append("  Benefits:")
                glossary.extend([f"    {item}" for item in info['benefits']])
        
        glossary.append("\n" + "=" * 100)
        return "\n".join(glossary)
    
    def _generate_file_info_section(self, file_info: Dict[str, Any]) -> str:
        """Generate file information section."""
        section = []
        section.append("📁 FILE INFORMATION")
        section.append("-" * 50)
        
        # Basic file info
        section.append(f"File Path: {file_info.get('file_path', 'Unknown')}")
        section.append(f"File Size: {file_info.get('file_size', 0):,} bytes")
        section.append(f"Format: {file_info.get('format', 'Unknown').upper()}")
        section.append(f"Rows: {file_info.get('rows_count', 0):,}")
        section.append(f"Columns: {file_info.get('columns_count', 0)}")
        
        # Date range
        if file_info.get('start_date') and file_info.get('end_date'):
            section.append(f"Date Range: {file_info.get('start_date')} to {file_info.get('end_date')}")
        
        # Data types
        if 'data_types' in file_info:
            section.append("\nData Types:")
            for col, dtype in file_info['data_types'].items():
                section.append(f"  {col}: {dtype}")
        
        return "\n".join(section)
    
    def _generate_descriptive_section(self, descriptive_results: Dict[str, Any]) -> str:
        """Generate descriptive statistics section."""
        section = []
        section.append("📊 DESCRIPTIVE STATISTICS")
        section.append("-" * 50)
        
        # Overview
        overview = descriptive_results.get('overview', {})
        section.append(f"Total Rows: {overview.get('total_rows', 0):,}")
        section.append(f"Total Columns: {overview.get('total_columns', 0)}")
        section.append(f"Numeric Columns: {overview.get('numeric_columns_count', 0)}")
        section.append(f"Memory Usage: {overview.get('memory_usage_mb', 0):.2f} MB")
        section.append("")
        
        # Basic statistics
        basic_stats = descriptive_results.get('basic_stats', {})
        if basic_stats:
            section.append("BASIC STATISTICS")
            section.append("-" * 30)
            for col, stats in basic_stats.items():
                section.append(f"Column: {col}")
                section.append(f"  Count: {stats.get('count', 0):,}")
                section.append(f"  Mean: {stats.get('mean', 0):.4f}")
                section.append(f"  Median: {stats.get('median', 0):.4f}")
                section.append(f"  Std Dev: {ColorUtils.format_basic_stat_value(stats.get('std', 0), 'std')}")
                section.append(f"  Min: {stats.get('min', 0):.4f}")
                section.append(f"  Max: {stats.get('max', 0):.4f}")
                section.append("")
        
        # Distribution statistics
        dist_stats = descriptive_results.get('distribution_stats', {})
        if dist_stats:
            section.append("DISTRIBUTION CHARACTERISTICS")
            section.append("-" * 30)
            for col, stats in dist_stats.items():
                section.append(f"Column: {col}")
                skewness = stats.get('skewness', 0)
                kurtosis = stats.get('kurtosis', 0)
                section.append(f"  Skewness: {ColorUtils.format_skewness(skewness)}")
                section.append(f"  Kurtosis: {ColorUtils.format_kurtosis(kurtosis)}")
                section.append("")
        
        # Variability statistics
        var_stats = descriptive_results.get('variability_stats', {})
        if var_stats:
            section.append("VARIABILITY ANALYSIS")
            section.append("-" * 30)
            for col, stats in var_stats.items():
                section.append(f"Column: {col}")
                section.append(f"  Variance: {ColorUtils.format_variance(stats.get('variance', 0))}")
                cv = stats.get('coefficient_of_variation', 0)
                cv_interpretation = stats.get('cv_interpretation', 'N/A')
                section.append(f"  Coefficient of Variation: {ColorUtils.format_coefficient_variation(cv)} - {cv_interpretation}")
                section.append(f"  IQR: {ColorUtils.format_iqr(stats.get('iqr', 0))}")
                section.append(f"  Range: {ColorUtils.format_range(stats.get('range', 0))}")
                section.append("")
        
        # Missing data analysis
        missing_data = descriptive_results.get('missing_data', {})
        if missing_data:
            section.append("MISSING DATA ANALYSIS")
            section.append("-" * 30)
            for col, stats in missing_data.items():
                section.append(f"Column: {col}")
                section.append(f"  Valid Data Points: {stats.get('valid_data_points', 0):,}")
                section.append(f"  Missing Data Points: {stats.get('missing_data_points', 0):,}")
                missing_pct = stats.get('missing_percentage', 0)
                section.append(f"  Missing Percentage: {ColorUtils.format_missing_data(missing_pct)}")
                section.append("")
        
        return "\n".join(section)
    
    def _generate_distribution_section(self, distribution_results: Dict[str, Any]) -> str:
        """Generate distribution analysis section."""
        section = []
        section.append("📈 DISTRIBUTION ANALYSIS")
        section.append("-" * 50)
        
        # Normality tests
        normality_tests = distribution_results.get('normality_tests', {})
        if normality_tests:
            section.append("NORMALITY TESTS")
            section.append("-" * 30)
            for col, tests in normality_tests.items():
                section.append(f"Column: {col}")
                overall_interp = tests.get('overall_interpretation', 'N/A')
                section.append(f"  Overall: {ColorUtils.format_overall_interpretation(overall_interp)}")
                
                # Shapiro-Wilk
                sw = tests.get('shapiro_wilk', {})
                if not np.isnan(sw.get('p_value', np.nan)):
                    p_value = sw.get('p_value', 0)
                    interpretation = sw.get('interpretation', 'N/A')
                    section.append(f"  Shapiro-Wilk: p={ColorUtils.format_normality_p_value(p_value)} - {ColorUtils.format_interpretation(interpretation)}")
                
                # D'Agostino-Pearson
                dp = tests.get('dagostino_pearson', {})
                if not np.isnan(dp.get('p_value', np.nan)):
                    p_value = dp.get('p_value', 0)
                    interpretation = dp.get('interpretation', 'N/A')
                    section.append(f"  D'Agostino-Pearson: p={ColorUtils.format_normality_p_value(p_value)} - {ColorUtils.format_interpretation(interpretation)}")
                
                section.append("")
        
        # Skewness analysis
        skewness_analysis = distribution_results.get('skewness_analysis', {})
        if skewness_analysis:
            section.append("SKEWNESS ANALYSIS")
            section.append("-" * 30)
            for col, analysis in skewness_analysis.items():
                section.append(f"Column: {col}")
                section.append(f"  Skewness: {analysis.get('skewness', 0):.4f}")
                section.append(f"  Z-Score: {analysis.get('skewness_z_score', 0):.4f}")
                interpretation = analysis.get('interpretation', 'N/A')
                section.append(f"  Interpretation: {ColorUtils.format_interpretation(interpretation)}")
                severity = analysis.get('severity', 'N/A')
                section.append(f"  Severity: {ColorUtils.format_severity(severity)}")
                recommendation = analysis.get('recommendation', 'N/A')
                section.append(f"  Recommendation: {ColorUtils.format_transformation_recommendation(recommendation)}")
                section.append("")
        
        # Kurtosis analysis
        kurtosis_analysis = distribution_results.get('kurtosis_analysis', {})
        if kurtosis_analysis:
            section.append("KURTOSIS ANALYSIS")
            section.append("-" * 30)
            for col, analysis in kurtosis_analysis.items():
                section.append(f"Column: {col}")
                section.append(f"  Kurtosis: {analysis.get('kurtosis', 0):.4f}")
                section.append(f"  Z-Score: {analysis.get('kurtosis_z_score', 0):.4f}")
                interpretation = analysis.get('interpretation', 'N/A')
                section.append(f"  Interpretation: {ColorUtils.format_interpretation(interpretation)}")
                severity = analysis.get('severity', 'N/A')
                section.append(f"  Severity: {ColorUtils.format_severity(severity)}")
                recommendation = analysis.get('recommendation', 'N/A')
                section.append(f"  Recommendation: {ColorUtils.format_transformation_recommendation(recommendation)}")
                section.append("")
        
        # Transformation recommendations
        recommendations = distribution_results.get('distribution_recommendations', {})
        if recommendations:
            section.append("TRANSFORMATION RECOMMENDATIONS")
            section.append("-" * 30)
            for col, rec in recommendations.items():
                section.append(f"Column: {col}")
                primary_rec = rec.get('primary_recommendation', 'N/A')
                section.append(f"  Primary Recommendation: {ColorUtils.format_transformation_recommendation(primary_rec)}")
                section.append(f"  Reasoning: {rec.get('reasoning', 'N/A')}")
                if rec.get('recommended_transformations'):
                    all_recs = ', '.join(rec.get('recommended_transformations', []))
                    section.append(f"  All Recommendations: {ColorUtils.format_transformation_recommendation(all_recs)}")
                section.append("")
        
        return "\n".join(section)
    
    def _generate_transformation_section(self, transformation_results: Dict[str, Any]) -> str:
        """Generate data transformation section."""
        section = []
        section.append("🔄 DATA TRANSFORMATION ANALYSIS")
        section.append("-" * 50)
        
        # Transformation details
        transformation_details = transformation_results.get('transformation_details', {})
        if transformation_details:
            section.append("TRANSFORMATION RESULTS")
            section.append("-" * 30)
            for col, details in transformation_details.items():
                section.append(f"Column: {col}")
                for transformation, trans_details in details.items():
                    if not trans_details.get('success', False):
                        section.append(f"  {transformation}: {ColorUtils.red('FAILED')} - {trans_details.get('error', 'Unknown error')}")
                        continue
                    
                    section.append(f"  {transformation}:")
                    section.append(f"    Original Mean: {trans_details.get('original_mean', 0):.4f}")
                    section.append(f"    Transformed Mean: {trans_details.get('transformed_mean', 0):.4f}")
                    section.append(f"    Original Skewness: {trans_details.get('original_skewness', 0):.4f}")
                    section.append(f"    Transformed Skewness: {trans_details.get('transformed_skewness', 0):.4f}")
                    
                    if 'lambda' in trans_details:
                        section.append(f"    Lambda: {trans_details['lambda']:.4f}")
                    
                    if 'shift_constant' in trans_details and trans_details['shift_constant'] > 0:
                        section.append(f"    Shift Constant: {trans_details['shift_constant']:.4f}")
                    
                    if 'note' in trans_details:
                        section.append(f"    Note: {trans_details['note']}")
                
                section.append("")
        
        # Comparison results
        comparison = transformation_results.get('comparison', {})
        if comparison:
            section.append("TRANSFORMATION COMPARISON")
            section.append("-" * 30)
            for col, col_comparison in comparison.items():
                section.append(f"Column: {col}")
                for transformation, comp_stats in col_comparison.items():
                    section.append(f"  {transformation}:")
                    
                    orig_stats = comp_stats.get('original_stats', {})
                    trans_stats = comp_stats.get('transformed_stats', {})
                    improvement = comp_stats.get('improvement', {})
                    
                    section.append(f"    Original - Mean: {orig_stats.get('mean', 0):.4f}, Skewness: {orig_stats.get('skewness', 0):.4f}")
                    section.append(f"    Transformed - Mean: {trans_stats.get('mean', 0):.4f}, Skewness: {trans_stats.get('skewness', 0):.4f}")
                    section.append(f"    Skewness Improvement: {improvement.get('skewness_improvement', 0):.4f}")
                    section.append(f"    Kurtosis Improvement: {improvement.get('kurtosis_improvement', 0):.4f}")
                
                section.append("")
        
        return "\n".join(section)
    
    def _generate_summary_section(self, analysis_results: Dict[str, Any]) -> str:
        """Generate summary and recommendations section."""
        section = []
        section.append("📋 SUMMARY AND RECOMMENDATIONS")
        section.append("-" * 50)
        
        # Data quality assessment
        section.append("DATA QUALITY ASSESSMENT")
        section.append("-" * 30)
        
        # Check for missing data
        if 'descriptive' in analysis_results:
            missing_data = analysis_results['descriptive'].get('missing_data', {})
            total_missing = sum(stats.get('missing_percentage', 0) for stats in missing_data.values())
            avg_missing = total_missing / len(missing_data) if missing_data else 0
            
            if avg_missing < 5:
                section.append(f"✅ Missing Data: {ColorUtils.green('Excellent (< 5%)')}")
            elif avg_missing < 15:
                section.append(f"⚠️  Missing Data: {ColorUtils.yellow('Good (5-15%)')}")
            else:
                section.append(f"❌ Missing Data: {ColorUtils.red('Poor (> 15%)')}")
        
        # Check for normality
        if 'distribution' in analysis_results:
            normality_tests = analysis_results['distribution'].get('normality_tests', {})
            normal_count = 0
            total_columns = len(normality_tests)
            
            for tests in normality_tests.values():
                if 'normal' in tests.get('overall_interpretation', '').lower():
                    normal_count += 1
            
            if total_columns > 0:
                normal_ratio = normal_count / total_columns
                if normal_ratio >= 0.75:
                    section.append(f"✅ Normality: {ColorUtils.green('Most columns are approximately normal')}")
                elif normal_ratio >= 0.5:
                    section.append(f"⚠️  Normality: {ColorUtils.yellow('Mixed results - some columns need transformation')}")
                else:
                    section.append(f"❌ Normality: {ColorUtils.red('Most columns are not normal - transformation recommended')}")
        
        # Transformation recommendations
        if 'distribution' in analysis_results:
            recommendations = analysis_results['distribution'].get('distribution_recommendations', {})
            if recommendations:
                section.append("\nTRANSFORMATION RECOMMENDATIONS")
                section.append("-" * 30)
                for col, rec in recommendations.items():
                    if rec.get('primary_recommendation') != "No transformation needed":
                        primary_rec = rec.get('primary_recommendation', 'N/A')
                        section.append(f"• {col}: {ColorUtils.format_transformation_recommendation(primary_rec)}")
        
        # General recommendations
        section.append("\nGENERAL RECOMMENDATIONS")
        section.append("-" * 30)
        section.append("• Use cleaned data from data/fixed/ folder for best results")
        section.append("• Consider data transformation for non-normal distributions")
        section.append("• Monitor data quality regularly")
        section.append("• Validate statistical assumptions before modeling")
        
        return "\n".join(section)
    
    def _save_report(self, report: str, file_info: Dict[str, Any], output_directory: str):
        """
        Save report to file.
        
        Args:
            report: Report content to save
            file_info: File metadata information
            output_directory: Directory to save report
        """
        try:
            # Create filename
            filename = file_info.get('filename', 'unknown')
            base_name = os.path.splitext(filename)[0]
            report_filename = f"{base_name}_statistical_analysis_report.txt"
            report_path = os.path.join(output_directory, report_filename)
            
            # Save report
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.logger.info(f"Report saved to: {report_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")
    
    def display_progress(self, current: int, total: int, operation: str):
        """
        Display progress information.
        
        Args:
            current: Current progress
            total: Total items
            operation: Operation description
        """
        if total > 0:
            percentage = (current / total) * 100
            bar_length = 40
            filled_length = int(bar_length * current // total)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            print(f"\r{operation}: |{bar}| {percentage:.1f}% ({current}/{total})", end='', flush=True)
            
            if current == total:
                print()  # New line when complete
    
    def display_analysis_start(self, file_info: Dict[str, Any], analysis_options: Dict[str, bool]):
        """
        Display analysis start information.
        
        Args:
            file_info: File metadata information
            analysis_options: Analysis options selected
        """
        print("\n" + "=" * 80)
        print(ColorUtils.blue("🚀 STARTING STATISTICAL ANALYSIS"))
        print("=" * 80)
        print(f"📁 File: {file_info.get('filename', 'Unknown')}")
        print(f"📂 Source: {file_info.get('source', 'Unknown')}")
        print(f"📊 Symbol: {file_info.get('symbol', 'Unknown')}")
        print(f"⏰ Timeframe: {file_info.get('timeframe', 'Unknown')}")
        print(f"📈 Rows: {file_info.get('rows_count', 0):,}")
        print(f"📊 Columns: {file_info.get('columns_count', 0)}")
        
        print("\n📊 Analysis Options:")
        if analysis_options.get('descriptive', False):
            print(f"  {ColorUtils.green('✅ Descriptive Statistics')}")
        if analysis_options.get('distribution', False):
            print(f"  {ColorUtils.green('✅ Distribution Analysis')}")
        if analysis_options.get('transform', False):
            print(f"  {ColorUtils.green('✅ Data Transformation')}")
        
        print("=" * 80)
    
    def display_analysis_complete(self, file_info: Dict[str, Any], processing_time: float):
        """
        Display analysis completion information.
        
        Args:
            file_info: File metadata information
            processing_time: Time taken for analysis
        """
        print("\n" + "=" * 80)
        print(ColorUtils.green("✅ ANALYSIS COMPLETED SUCCESSFULLY"))
        print("=" * 80)
        print(f"📁 File: {file_info.get('filename', 'Unknown')}")
        print(f"⏱️  Processing Time: {processing_time:.2f} seconds")
        print("=" * 80)
    
    def display_error(self, error_message: str, file_info: Optional[Dict[str, Any]] = None):
        """
        Display error information.
        
        Args:
            error_message: Error message to display
            file_info: Optional file metadata information
        """
        print("\n" + "=" * 80)
        print(ColorUtils.red("❌ ANALYSIS ERROR"))
        print("=" * 80)
        if file_info:
            print(f"📁 File: {file_info.get('filename', 'Unknown')}")
        print(f"💥 Error: {ColorUtils.red(error_message)}")
        print("=" * 80)
    
    def display_warning(self, warning_message: str):
        """
        Display warning information.
        
        Args:
            warning_message: Warning message to display
        """
        print(f"\n⚠️  WARNING: {ColorUtils.yellow(warning_message)}")
    
    def display_info(self, info_message: str):
        """
        Display information message.
        
        Args:
            info_message: Information message to display
        """
        print(f"\nℹ️  INFO: {ColorUtils.blue(info_message)}")
