"""
Distribution Analysis Module

This module provides comprehensive distribution analysis for financial data.
It includes normality tests, detailed skewness and kurtosis analysis,
and distribution transformation recommendations.

Features:
- Normality Tests: Shapiro-Wilk, D'Agostino-Pearson, Anderson-Darling, Kolmogorov-Smirnov
- Skewness & Kurtosis: Detailed analysis with interpretation
- Distribution Recommendations: Suggestions for data transformation
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from scipy import stats
from scipy.stats import shapiro, normaltest, anderson, kstest
import logging
from .color_utils import ColorUtils


class DistributionAnalysis:
    """Handles distribution analysis and normality testing."""
    
    def __init__(self):
        """Initialize the distribution analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def analyze_distributions(self, data: pd.DataFrame, numeric_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive distribution analysis.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns to analyze. If None, auto-detect.
            
        Returns:
            Dictionary containing all distribution analysis results
        """
        if numeric_columns is None:
            numeric_columns = self._get_numeric_columns(data)
        
        if not numeric_columns:
            self.logger.warning("No numeric columns found for distribution analysis")
            return {}
        
        results = {
            'normality_tests': self._perform_normality_tests(data, numeric_columns),
            'skewness_analysis': self._analyze_skewness(data, numeric_columns),
            'kurtosis_analysis': self._analyze_kurtosis(data, numeric_columns),
            'distribution_recommendations': self._generate_transformation_recommendations(data, numeric_columns)
        }
        
        return results
    
    def _get_numeric_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Get list of numeric columns from DataFrame.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of numeric column names
        """
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Filter out columns that are all NaN or have no variance
        valid_numeric_cols = []
        for col in numeric_cols:
            if not data[col].isna().all() and data[col].nunique() > 1:
                valid_numeric_cols.append(col)
        
        return valid_numeric_cols
    
    def _perform_normality_tests(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Perform various normality tests for each numeric column.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with normality test results for each column
        """
        normality_results = {}
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            
            if len(col_data) < 3:
                normality_results[col] = {
                    'shapiro_wilk': {'statistic': np.nan, 'p_value': np.nan, 'interpretation': 'Insufficient data'},
                    'dagostino_pearson': {'statistic': np.nan, 'p_value': np.nan, 'interpretation': 'Insufficient data'},
                    'anderson_darling': {'statistic': np.nan, 'critical_values': {}, 'interpretation': 'Insufficient data'},
                    'kolmogorov_smirnov': {'statistic': np.nan, 'p_value': np.nan, 'interpretation': 'Insufficient data'},
                    'overall_interpretation': 'Insufficient data for normality testing'
                }
                continue
            
            # Shapiro-Wilk test (best for small samples, n < 5000)
            shapiro_result = self._shapiro_wilk_test(col_data)
            
            # D'Agostino-Pearson test
            dagostino_result = self._dagostino_pearson_test(col_data)
            
            # Anderson-Darling test
            anderson_result = self._anderson_darling_test(col_data)
            
            # Kolmogorov-Smirnov test
            ks_result = self._kolmogorov_smirnov_test(col_data)
            
            # Overall interpretation
            overall_interpretation = self._interpret_overall_normality([
                shapiro_result, dagostino_result, anderson_result, ks_result
            ])
            
            normality_results[col] = {
                'shapiro_wilk': shapiro_result,
                'dagostino_pearson': dagostino_result,
                'anderson_darling': anderson_result,
                'kolmogorov_smirnov': ks_result,
                'overall_interpretation': overall_interpretation
            }
        
        return normality_results
    
    def _shapiro_wilk_test(self, data: np.ndarray) -> Dict[str, Any]:
        """
        Perform Shapiro-Wilk normality test.
        
        Args:
            data: Array of data to test
            
        Returns:
            Dictionary with test results and interpretation
        """
        try:
            if len(data) > 5000:
                # For large samples, use a subset
                data_sample = np.random.choice(data, 5000, replace=False)
            else:
                data_sample = data
            
            statistic, p_value = shapiro(data_sample)
            
            if p_value > 0.05:
                interpretation = "Data appears to be normally distributed (p > 0.05)"
            else:
                interpretation = "Data does not appear to be normally distributed (p ≤ 0.05)"
            
            return {
                'statistic': float(statistic),
                'p_value': float(p_value),
                'interpretation': interpretation,
                'sample_size': len(data_sample)
            }
        except Exception as e:
            return {
                'statistic': np.nan,
                'p_value': np.nan,
                'interpretation': f"Test failed: {str(e)}",
                'sample_size': len(data)
            }
    
    def _dagostino_pearson_test(self, data: np.ndarray) -> Dict[str, Any]:
        """
        Perform D'Agostino-Pearson normality test.
        
        Args:
            data: Array of data to test
            
        Returns:
            Dictionary with test results and interpretation
        """
        try:
            statistic, p_value = normaltest(data)
            
            if p_value > 0.05:
                interpretation = "Data appears to be normally distributed (p > 0.05)"
            else:
                interpretation = "Data does not appear to be normally distributed (p ≤ 0.05)"
            
            return {
                'statistic': float(statistic),
                'p_value': float(p_value),
                'interpretation': interpretation
            }
        except Exception as e:
            return {
                'statistic': np.nan,
                'p_value': np.nan,
                'interpretation': f"Test failed: {str(e)}"
            }
    
    def _anderson_darling_test(self, data: np.ndarray) -> Dict[str, Any]:
        """
        Perform Anderson-Darling normality test.
        
        Args:
            data: Array of data to test
            
        Returns:
            Dictionary with test results and interpretation
        """
        try:
            result = anderson(data, dist='norm')
            statistic = result.statistic
            critical_values = dict(zip(result.critical_values, result.significance_level))
            
            # Find the highest significance level where we can reject normality
            max_significance = 0
            for cv, sig in critical_values.items():
                if statistic > cv:
                    max_significance = sig
            
            if max_significance == 0:
                interpretation = "Data appears to be normally distributed (statistic < all critical values)"
            else:
                interpretation = f"Data does not appear to be normally distributed (rejected at {max_significance*100}% significance level)"
            
            return {
                'statistic': float(statistic),
                'critical_values': critical_values,
                'interpretation': interpretation
            }
        except Exception as e:
            return {
                'statistic': np.nan,
                'critical_values': {},
                'interpretation': f"Test failed: {str(e)}"
            }
    
    def _kolmogorov_smirnov_test(self, data: np.ndarray) -> Dict[str, Any]:
        """
        Perform Kolmogorov-Smirnov normality test.
        
        Args:
            data: Array of data to test
            
        Returns:
            Dictionary with test results and interpretation
        """
        try:
            # Standardize the data
            mean_val = np.mean(data)
            std_val = np.std(data, ddof=1)
            standardized_data = (data - mean_val) / std_val
            
            statistic, p_value = kstest(standardized_data, 'norm')
            
            if p_value > 0.05:
                interpretation = "Data appears to be normally distributed (p > 0.05)"
            else:
                interpretation = "Data does not appear to be normally distributed (p ≤ 0.05)"
            
            return {
                'statistic': float(statistic),
                'p_value': float(p_value),
                'interpretation': interpretation
            }
        except Exception as e:
            return {
                'statistic': np.nan,
                'p_value': np.nan,
                'interpretation': f"Test failed: {str(e)}"
            }
    
    def _interpret_overall_normality(self, test_results: List[Dict[str, Any]]) -> str:
        """
        Provide overall interpretation based on multiple normality tests.
        
        Args:
            test_results: List of test result dictionaries
            
        Returns:
            Overall interpretation string
        """
        # Count how many tests suggest normality
        normal_count = 0
        total_tests = 0
        
        for result in test_results:
            if 'p_value' in result and not np.isnan(result['p_value']):
                total_tests += 1
                if result['p_value'] > 0.05:
                    normal_count += 1
        
        if total_tests == 0:
            return "No valid normality tests could be performed"
        
        normal_ratio = normal_count / total_tests
        
        if normal_ratio >= 0.75:
            return f"Data appears to be normally distributed ({normal_count}/{total_tests} tests suggest normality)"
        elif normal_ratio >= 0.5:
            return f"Data shows mixed normality results ({normal_count}/{total_tests} tests suggest normality)"
        else:
            return f"Data does not appear to be normally distributed ({normal_count}/{total_tests} tests suggest normality)"
    
    def _analyze_skewness(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Perform detailed skewness analysis.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with skewness analysis for each column
        """
        skewness_results = {}
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            
            if len(col_data) < 3:
                skewness_results[col] = {
                    'skewness': np.nan,
                    'skewness_standard_error': np.nan,
                    'skewness_z_score': np.nan,
                    'interpretation': 'Insufficient data',
                    'severity': 'Unknown',
                    'recommendation': 'Need more data for analysis'
                }
                continue
            
            # Calculate skewness
            skewness = stats.skew(col_data)
            
            # Calculate standard error of skewness
            n = len(col_data)
            se_skewness = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
            
            # Calculate z-score for skewness
            z_skewness = skewness / se_skewness if se_skewness > 0 else 0
            
            # Interpret skewness
            interpretation, severity, recommendation = self._interpret_skewness(skewness, z_skewness)
            
            skewness_results[col] = {
                'skewness': float(skewness),
                'skewness_standard_error': float(se_skewness),
                'skewness_z_score': float(z_skewness),
                'interpretation': interpretation,
                'severity': severity,
                'recommendation': recommendation
            }
        
        return skewness_results
    
    def _interpret_skewness(self, skewness: float, z_score: float) -> Tuple[str, str, str]:
        """
        Interpret skewness values and provide recommendations.
        
        Args:
            skewness: Skewness value
            z_score: Z-score of skewness
            
        Returns:
            Tuple of (interpretation, severity, recommendation)
        """
        abs_skewness = abs(skewness)
        abs_z_score = abs(z_score)
        
        # Determine interpretation
        if abs_skewness < 0.5:
            interpretation = "Approximately symmetric"
        elif abs_skewness < 1.0:
            interpretation = "Moderately skewed"
        else:
            interpretation = "Highly skewed"
        
        if skewness > 0:
            interpretation += " (right-tailed)"
        elif skewness < 0:
            interpretation += " (left-tailed)"
        
        # Determine severity
        if abs_z_score < 2:
            severity = "Mild"
        elif abs_z_score < 3:
            severity = "Moderate"
        else:
            severity = "Severe"
        
        # Provide recommendation
        if abs_skewness < 0.5:
            recommendation = "No transformation needed - data is approximately symmetric"
        elif abs_skewness < 1.0:
            if skewness > 0:
                recommendation = "Consider log transformation or square root transformation"
            else:
                recommendation = "Consider square transformation or Box-Cox transformation"
        else:
            if skewness > 0:
                recommendation = "Strongly recommend log transformation or Box-Cox transformation"
            else:
                recommendation = "Strongly recommend Box-Cox transformation or Yeo-Johnson transformation"
        
        return interpretation, severity, recommendation
    
    def _analyze_kurtosis(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Perform detailed kurtosis analysis.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with kurtosis analysis for each column
        """
        kurtosis_results = {}
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            
            if len(col_data) < 4:
                kurtosis_results[col] = {
                    'kurtosis': np.nan,
                    'kurtosis_standard_error': np.nan,
                    'kurtosis_z_score': np.nan,
                    'interpretation': 'Insufficient data',
                    'severity': 'Unknown',
                    'recommendation': 'Need more data for analysis'
                }
                continue
            
            # Calculate kurtosis
            kurtosis = stats.kurtosis(col_data)
            
            # Calculate standard error of kurtosis
            n = len(col_data)
            se_kurtosis = np.sqrt(24 * n * (n - 1) / ((n - 3) * (n - 2) * (n + 3) * (n + 5)))
            
            # Calculate z-score for kurtosis
            z_kurtosis = kurtosis / se_kurtosis if se_kurtosis > 0 else 0
            
            # Interpret kurtosis
            interpretation, severity, recommendation = self._interpret_kurtosis(kurtosis, z_kurtosis)
            
            kurtosis_results[col] = {
                'kurtosis': float(kurtosis),
                'kurtosis_standard_error': float(se_kurtosis),
                'kurtosis_z_score': float(z_kurtosis),
                'interpretation': interpretation,
                'severity': severity,
                'recommendation': recommendation
            }
        
        return kurtosis_results
    
    def _interpret_kurtosis(self, kurtosis: float, z_score: float) -> Tuple[str, str, str]:
        """
        Interpret kurtosis values and provide recommendations.
        
        Args:
            kurtosis: Kurtosis value
            z_score: Z-score of kurtosis
            
        Returns:
            Tuple of (interpretation, severity, recommendation)
        """
        abs_kurtosis = abs(kurtosis)
        abs_z_score = abs(z_score)
        
        # Determine interpretation
        if abs_kurtosis < 0.5:
            interpretation = "Approximately normal (mesokurtic)"
        elif kurtosis > 0.5:
            interpretation = "Heavy-tailed (leptokurtic)"
        else:
            interpretation = "Light-tailed (platykurtic)"
        
        # Determine severity
        if abs_z_score < 2:
            severity = "Mild"
        elif abs_z_score < 3:
            severity = "Moderate"
        else:
            severity = "Severe"
        
        # Provide recommendation
        if abs_kurtosis < 0.5:
            recommendation = "No transformation needed - kurtosis is approximately normal"
        elif kurtosis > 0.5:
            recommendation = "Consider log transformation or Box-Cox transformation to reduce heavy tails"
        else:
            recommendation = "Consider square transformation or investigate data quality (light tails may indicate data issues)"
        
        return interpretation, severity, recommendation
    
    def _generate_transformation_recommendations(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Generate transformation recommendations based on distribution analysis.
        
        Args:
            data: DataFrame to analyze
            numeric_columns: List of numeric columns
            
        Returns:
            Dictionary with transformation recommendations for each column
        """
        recommendations = {}
        
        for col in numeric_columns:
            col_data = data[col].dropna()
            
            if len(col_data) < 3:
                recommendations[col] = {
                    'recommended_transformations': [],
                    'primary_recommendation': 'Insufficient data for recommendations',
                    'reasoning': 'Need at least 3 data points for analysis',
                    'transformation_priority': []
                }
                continue
            
            # Get skewness and kurtosis
            skewness = stats.skew(col_data)
            kurtosis = stats.kurtosis(col_data)
            
            # Generate recommendations based on distribution characteristics
            recommended_transformations = []
            reasoning_parts = []
            
            # Check for skewness
            if abs(skewness) > 1.0:
                if skewness > 0:
                    recommended_transformations.extend(['log', 'sqrt', 'box_cox'])
                    reasoning_parts.append(f"Strong positive skewness ({skewness:.3f})")
                else:
                    recommended_transformations.extend(['square', 'box_cox', 'yeo_johnson'])
                    reasoning_parts.append(f"Strong negative skewness ({skewness:.3f})")
            elif abs(skewness) > 0.5:
                if skewness > 0:
                    recommended_transformations.extend(['sqrt', 'log'])
                    reasoning_parts.append(f"Moderate positive skewness ({skewness:.3f})")
                else:
                    recommended_transformations.extend(['square', 'box_cox'])
                    reasoning_parts.append(f"Moderate negative skewness ({skewness:.3f})")
            
            # Check for kurtosis
            if kurtosis > 1.0:
                if 'log' not in recommended_transformations:
                    recommended_transformations.append('log')
                reasoning_parts.append(f"High kurtosis ({kurtosis:.3f}) - heavy tails")
            elif kurtosis < -1.0:
                reasoning_parts.append(f"Low kurtosis ({kurtosis:.3f}) - light tails (check data quality)")
            
            # Check for outliers (using IQR method)
            q75, q25 = np.percentile(col_data, [75, 25])
            iqr = q75 - q25
            lower_bound = q25 - 1.5 * iqr
            upper_bound = q75 + 1.5 * iqr
            outliers = np.sum((col_data < lower_bound) | (col_data > upper_bound))
            outlier_percentage = (outliers / len(col_data)) * 100
            
            if outlier_percentage > 5:
                if 'box_cox' not in recommended_transformations:
                    recommended_transformations.append('box_cox')
                reasoning_parts.append(f"High outlier percentage ({outlier_percentage:.1f}%)")
            
            # Determine primary recommendation
            if not recommended_transformations:
                primary_recommendation = "No transformation needed - data appears approximately normal"
            else:
                # Prioritize transformations
                if 'box_cox' in recommended_transformations:
                    primary_recommendation = "Box-Cox transformation (most versatile)"
                elif 'log' in recommended_transformations:
                    primary_recommendation = "Log transformation (good for positive skewness)"
                elif 'sqrt' in recommended_transformations:
                    primary_recommendation = "Square root transformation (mild positive skewness)"
                elif 'yeo_johnson' in recommended_transformations:
                    primary_recommendation = "Yeo-Johnson transformation (handles negative values)"
                else:
                    primary_recommendation = recommended_transformations[0]
            
            # Create transformation priority list
            transformation_priority = []
            if 'box_cox' in recommended_transformations:
                transformation_priority.append('box_cox')
            if 'yeo_johnson' in recommended_transformations:
                transformation_priority.append('yeo_johnson')
            if 'log' in recommended_transformations:
                transformation_priority.append('log')
            if 'sqrt' in recommended_transformations:
                transformation_priority.append('sqrt')
            if 'square' in recommended_transformations:
                transformation_priority.append('square')
            
            recommendations[col] = {
                'recommended_transformations': recommended_transformations,
                'primary_recommendation': primary_recommendation,
                'reasoning': '; '.join(reasoning_parts) if reasoning_parts else 'Data appears approximately normal',
                'transformation_priority': transformation_priority,
                'outlier_percentage': outlier_percentage
            }
        
        return recommendations
    
    def get_summary_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a summary report of distribution analysis.
        
        Args:
            results: Results from analyze_distributions method
            
        Returns:
            Formatted summary report string
        """
        report = []
        report.append("=" * 80)
        report.append("DISTRIBUTION ANALYSIS SUMMARY")
        report.append("=" * 80)
        
        # Normality tests
        normality_tests = results.get('normality_tests', {})
        if normality_tests:
            report.append("NORMALITY TESTS")
            report.append("-" * 40)
            for col, tests in normality_tests.items():
                report.append(f"Column: {col}")
                report.append(f"  Overall: {tests.get('overall_interpretation', 'N/A')}")
                
                # Shapiro-Wilk
                sw = tests.get('shapiro_wilk', {})
                if not np.isnan(sw.get('p_value', np.nan)):
                    report.append(f"  Shapiro-Wilk: p={sw.get('p_value', 0):.4f} - {sw.get('interpretation', 'N/A')}")
                
                # D'Agostino-Pearson
                dp = tests.get('dagostino_pearson', {})
                if not np.isnan(dp.get('p_value', np.nan)):
                    report.append(f"  D'Agostino-Pearson: p={dp.get('p_value', 0):.4f} - {dp.get('interpretation', 'N/A')}")
                
                report.append("")
        
        # Skewness analysis
        skewness_analysis = results.get('skewness_analysis', {})
        if skewness_analysis:
            report.append("SKEWNESS ANALYSIS")
            report.append("-" * 40)
            for col, analysis in skewness_analysis.items():
                report.append(f"Column: {col}")
                report.append(f"  Skewness: {analysis.get('skewness', 0):.4f}")
                report.append(f"  Interpretation: {analysis.get('interpretation', 'N/A')}")
                report.append(f"  Severity: {analysis.get('severity', 'N/A')}")
                report.append(f"  Recommendation: {analysis.get('recommendation', 'N/A')}")
                report.append("")
        
        # Kurtosis analysis
        kurtosis_analysis = results.get('kurtosis_analysis', {})
        if kurtosis_analysis:
            report.append("KURTOSIS ANALYSIS")
            report.append("-" * 40)
            for col, analysis in kurtosis_analysis.items():
                report.append(f"Column: {col}")
                report.append(f"  Kurtosis: {analysis.get('kurtosis', 0):.4f}")
                report.append(f"  Interpretation: {analysis.get('interpretation', 'N/A')}")
                report.append(f"  Severity: {analysis.get('severity', 'N/A')}")
                report.append(f"  Recommendation: {analysis.get('recommendation', 'N/A')}")
                report.append("")
        
        # Transformation recommendations
        recommendations = results.get('distribution_recommendations', {})
        if recommendations:
            report.append("TRANSFORMATION RECOMMENDATIONS")
            report.append("-" * 40)
            for col, rec in recommendations.items():
                report.append(f"Column: {col}")
                report.append(f"  Primary Recommendation: {rec.get('primary_recommendation', 'N/A')}")
                report.append(f"  Reasoning: {rec.get('reasoning', 'N/A')}")
                if rec.get('recommended_transformations'):
                    report.append(f"  All Recommendations: {', '.join(rec.get('recommended_transformations', []))}")
                report.append("")
        
        return "\n".join(report)
