"""
Financial Analysis Reporting Module

This module provides comprehensive reporting functionality for financial analysis results,
including detailed reports, summaries, and data transformation recommendations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
from .color_utils import ColorUtils


class FinanceReporter:
    """Comprehensive reporting for financial analysis results."""
    
    def __init__(self):
        """Initialize the finance reporter."""
        self.logger = logging.getLogger(__name__)
    
    def generate_comprehensive_report(self, analysis_results: Dict[str, Any],
                                    file_metadata: Dict[str, Any],
                                    analysis_types: List[str]) -> str:
        """
        Generate a comprehensive financial analysis report.
        
        Args:
            analysis_results: Dictionary with all analysis results
            file_metadata: File metadata information
            analysis_types: List of analysis types performed
            
        Returns:
            Comprehensive report string
        """
        try:
            report_parts = []
            
            # Header
            report_parts.append(self._generate_header(file_metadata, analysis_types))
            
            # Executive Summary
            report_parts.append(self._generate_executive_summary(analysis_results))
            
            # Data Quality Assessment
            if 'ohlcv_analysis' in analysis_results:
                report_parts.append(self._generate_data_quality_section(analysis_results['ohlcv_analysis']))
            
            # OHLCV Analysis Report
            if 'ohlcv_analysis' in analysis_results and 'ohlcv' in analysis_types:
                report_parts.append(self._generate_ohlcv_report(analysis_results['ohlcv_analysis']))
            
            # Volatility Analysis Report
            if 'volatility_analysis' in analysis_results and 'volatility' in analysis_types:
                report_parts.append(self._generate_volatility_report(analysis_results['volatility_analysis']))
            
            # Returns Analysis Report
            if 'returns_analysis' in analysis_results and 'returns' in analysis_types:
                report_parts.append(self._generate_returns_report(analysis_results['returns_analysis']))
            
            # Drawdown Analysis Report
            if 'drawdown_analysis' in analysis_results and 'drawdown' in analysis_types:
                report_parts.append(self._generate_drawdown_report(analysis_results['drawdown_analysis']))
            
            # Recommendations
            report_parts.append(self._generate_recommendations_section(analysis_results))
            
            # Footer
            report_parts.append(self._generate_footer())
            
            return "\n\n".join(report_parts)
        
        except Exception as e:
            self.logger.error(f"Error generating comprehensive report: {str(e)}")
            return f"Error generating report: {str(e)}"
    
    def _generate_header(self, file_metadata: Dict[str, Any], 
                        analysis_types: List[str]) -> str:
        """Generate report header."""
        header_parts = []
        
        header_parts.append("=" * 80)
        header_parts.append("📊 COMPREHENSIVE FINANCIAL ANALYSIS REPORT")
        header_parts.append("=" * 80)
        header_parts.append(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        header_parts.append(f"📁 File: {file_metadata.get('file_path', 'Unknown')}")
        header_parts.append(f"📊 Symbol: {file_metadata.get('symbol', 'Unknown')}")
        header_parts.append(f"⏰ Timeframe: {file_metadata.get('timeframe', 'Unknown')}")
        header_parts.append(f"📈 Source: {file_metadata.get('source', 'Unknown')}")
        header_parts.append(f"📊 Analysis Types: {', '.join(analysis_types)}")
        header_parts.append("=" * 80)
        
        return "\n".join(header_parts)
    
    def _generate_executive_summary(self, analysis_results: Dict[str, Any]) -> str:
        """Generate executive summary."""
        summary_parts = []
        
        summary_parts.append("📋 EXECUTIVE SUMMARY")
        summary_parts.append("-" * 40)
        
        # Overall assessment
        summary_parts.append("🎯 Overall Assessment:")
        
        # Data quality summary
        if 'ohlcv_analysis' in analysis_results:
            ohlcv = analysis_results['ohlcv_analysis']
            if 'data_quality_assessment' in ohlcv:
                dq = ohlcv['data_quality_assessment']
                completeness = dq.get('completeness_score', 0)
                summary_parts.append(f"  • Data Quality: {completeness:.1f}% completeness")
        
        # Key findings
        summary_parts.append("\n🔍 Key Findings:")
        
        # OHLCV findings
        if 'ohlcv_analysis' in analysis_results:
            ohlcv = analysis_results['ohlcv_analysis']
            if 'price_validation' in ohlcv and 'ohlc_validation' in ohlcv['price_validation']:
                ohlc = ohlcv['price_validation']['ohlc_validation']
                valid_pct = (ohlc.get('valid_rows', 0) / ohlc.get('total_rows', 1)) * 100
                summary_parts.append(f"  • Price Validation: {valid_pct:.1f}% valid OHLC relationships")
        
        # Volatility findings
        if 'volatility_analysis' in analysis_results:
            vol = analysis_results['volatility_analysis']
            if 'rolling_volatility' in vol and 'volatility_windows' in vol['rolling_volatility']:
                vw = vol['rolling_volatility']['volatility_windows']
                if vw:
                    # Get current volatility from first available column
                    first_col = list(vw.keys())[0]
                    if 'window_20' in vw[first_col]:
                        current_vol = vw[first_col]['window_20'].get('current_volatility', 0)
                        summary_parts.append(f"  • Current Volatility: {current_vol:.4f}")
        
        # Returns findings
        if 'returns_analysis' in analysis_results:
            ret = analysis_results['returns_analysis']
            if 'cumulative_returns' in ret and 'cumulative_simple_returns' in ret['cumulative_returns']:
                csr = ret['cumulative_returns']['cumulative_simple_returns']
                if csr:
                    first_col = list(csr.keys())[0]
                    total_return = csr[first_col].get('total_return', 0)
                    summary_parts.append(f"  • Total Return: {total_return:.1%}")
        
        # Drawdown findings
        if 'drawdown_analysis' in analysis_results:
            dd = analysis_results['drawdown_analysis']
            if 'maximum_drawdown' in dd and 'maximum_drawdowns' in dd['maximum_drawdown']:
                mdd = dd['maximum_drawdown']['maximum_drawdowns']
                if mdd:
                    first_col = list(mdd.keys())[0]
                    max_dd = mdd[first_col].get('maximum_drawdown_percentage', 0)
                    summary_parts.append(f"  • Maximum Drawdown: {max_dd:.1f}%")
        
        return "\n".join(summary_parts)
    
    def _generate_data_quality_section(self, ohlcv_results: Dict[str, Any]) -> str:
        """Generate data quality assessment section."""
        quality_parts = []
        
        quality_parts.append("📊 DATA QUALITY ASSESSMENT")
        quality_parts.append("-" * 40)
        
        if 'data_quality_assessment' in ohlcv_results:
            dq = ohlcv_results['data_quality_assessment']
            
            # Completeness score
            completeness = dq.get('completeness_score', 0)
            quality_parts.append(f"📈 Data Completeness: {completeness:.1f}%")
            
            # Quality issues
            if 'quality_issues' in dq and dq['quality_issues']:
                quality_parts.append("\n⚠️  Quality Issues:")
                for issue in dq['quality_issues']:
                    quality_parts.append(f"  • {issue}")
            
            # Recommendations
            if 'recommendations' in dq and dq['recommendations']:
                quality_parts.append("\n💡 Recommendations:")
                for rec in dq['recommendations']:
                    quality_parts.append(f"  • {rec}")
        
        return "\n".join(quality_parts)
    
    def _generate_ohlcv_report(self, ohlcv_results: Dict[str, Any]) -> str:
        """Generate OHLCV analysis report."""
        ohlcv_parts = []
        
        ohlcv_parts.append("📊 OHLCV DATA ANALYSIS")
        ohlcv_parts.append("-" * 40)
        
        # Price validation
        if 'price_validation' in ohlcv_results:
            pv = ohlcv_results['price_validation']
            
            if 'ohlc_validation' in pv:
                ohlc = pv['ohlc_validation']
                valid_pct = (ohlc.get('valid_rows', 0) / ohlc.get('total_rows', 1)) * 100
                ohlcv_parts.append(f"✅ OHLC Validation: {valid_pct:.1f}% valid rows")
                
                if 'error_summary' in ohlc and ohlc['error_summary']:
                    ohlcv_parts.append("\n❌ Validation Errors:")
                    for error, count in ohlc['error_summary'].items():
                        ohlcv_parts.append(f"  • {error}: {count} occurrences")
            
            if 'price_gaps' in pv:
                gaps = pv['price_gaps']
                total_gaps = gaps.get('total_gaps', 0)
                significant_gaps = gaps.get('significant_gaps', 0)
                ohlcv_parts.append(f"\n📈 Price Gaps: {total_gaps} total, {significant_gaps} significant")
        
        # Volume analysis
        if 'volume_analysis' in ohlcv_results:
            va = ohlcv_results['volume_analysis']
            
            if 'volume_patterns' in va:
                vp = va['volume_patterns']
                zero_vol_pct = vp.get('zero_volume_percentage', 0)
                ohlcv_parts.append(f"\n📊 Volume Analysis: {zero_vol_pct:.1f}% zero volumes")
                
                if 'volume_statistics' in vp:
                    vs = vp['volume_statistics']
                    mean_vol = vs.get('mean_volume', 0)
                    ohlcv_parts.append(f"  • Average Volume: {mean_vol:,.0f}")
        
        # Price-volume relationships
        if 'price_volume_relationships' in ohlcv_results:
            pvr = ohlcv_results['price_volume_relationships']
            
            if 'correlation_analysis' in pvr:
                corr = pvr['correlation_analysis']
                price_vol_corr = corr.get('price_volume_correlation', 0)
                ohlcv_parts.append(f"\n🔗 Price-Volume Correlation: {price_vol_corr:.3f}")
        
        return "\n".join(ohlcv_parts)
    
    def _generate_volatility_report(self, volatility_results: Dict[str, Any]) -> str:
        """Generate volatility analysis report."""
        vol_parts = []
        
        vol_parts.append("📈 VOLATILITY ANALYSIS")
        vol_parts.append("-" * 40)
        
        # Rolling volatility
        if 'rolling_volatility' in volatility_results:
            rv = volatility_results['rolling_volatility']
            
            if 'volatility_windows' in rv:
                vw = rv['volatility_windows']
                vol_parts.append("📊 Rolling Volatility Analysis:")
                
                for col, windows in vw.items():
                    vol_parts.append(f"\n  {col}:")
                    for window, data in windows.items():
                        current_vol = data.get('current_volatility', 0)
                        annualized_vol = data.get('annualized_volatility', 0)
                        vol_parts.append(f"    • {window}: {current_vol:.4f} (Annualized: {annualized_vol:.1%})")
        
        # GARCH models
        if 'garch_models' in volatility_results:
            gm = volatility_results['garch_models']
            
            if 'garch_models' in gm:
                garch_models = gm['garch_models']
                vol_parts.append("\n🔬 GARCH Model Analysis:")
                
                for col, models in garch_models.items():
                    vol_parts.append(f"\n  {col}:")
                    for model_type, result in models.items():
                        if result.get('success', False):
                            aic = result.get('fit_statistics', {}).get('aic', 0)
                            vol_parts.append(f"    • {model_type}: AIC = {aic:.2f}")
                        else:
                            vol_parts.append(f"    • {model_type}: Failed")
        
        # Volatility clustering
        if 'volatility_clustering' in volatility_results:
            vc = volatility_results['volatility_clustering']
            
            if 'clustering_analysis' in vc:
                ca = vc['clustering_analysis']
                vol_parts.append("\n🔍 Volatility Clustering:")
                
                for col, analysis in ca.items():
                    if 'clustering_analysis' in analysis:
                        clustering = analysis['clustering_analysis']
                        strength = clustering.get('clustering_strength', 'unknown')
                        vol_parts.append(f"  • {col}: {strength} clustering")
        
        return "\n".join(vol_parts)
    
    def _generate_returns_report(self, returns_results: Dict[str, Any]) -> str:
        """Generate returns analysis report."""
        ret_parts = []
        
        ret_parts.append("💰 RETURNS ANALYSIS")
        ret_parts.append("-" * 40)
        
        # Simple returns
        if 'simple_returns' in returns_results:
            sr = returns_results['simple_returns']
            
            if 'returns_analysis' in sr:
                ra = sr['returns_analysis']
                ret_parts.append("📊 Simple Returns Analysis:")
                
                for col, analysis in ra.items():
                    win_rate = analysis.get('win_rate', 0)
                    avg_positive = analysis.get('average_positive_return', 0)
                    avg_negative = analysis.get('average_negative_return', 0)
                    ret_parts.append(f"\n  {col}:")
                    ret_parts.append(f"    • Win Rate: {win_rate:.1f}%")
                    ret_parts.append(f"    • Avg Positive Return: {avg_positive:.2%}")
                    ret_parts.append(f"    • Avg Negative Return: {avg_negative:.2%}")
        
        # Cumulative returns
        if 'cumulative_returns' in returns_results:
            cr = returns_results['cumulative_returns']
            
            if 'cumulative_simple_returns' in cr:
                csr = cr['cumulative_simple_returns']
                ret_parts.append("\n📈 Cumulative Returns:")
                
                for col, analysis in csr.items():
                    total_return = analysis.get('total_return', 0)
                    max_return = analysis.get('max_return', 0)
                    ret_parts.append(f"  • {col}: {total_return:.1%} (Max: {max_return:.1%})")
        
        # Risk metrics
        if 'returns_risk_metrics' in returns_results:
            rm = returns_results['returns_risk_metrics']
            
            if 'risk_metrics' in rm:
                risk_metrics = rm['risk_metrics']
                ret_parts.append("\n⚠️  Risk Metrics:")
                
                for col, metrics in risk_metrics.items():
                    sharpe = metrics.get('sharpe_ratio', 0)
                    volatility = metrics.get('volatility', 0)
                    ret_parts.append(f"  • {col}: Sharpe = {sharpe:.2f}, Volatility = {volatility:.2%}")
        
        return "\n".join(ret_parts)
    
    def _generate_drawdown_report(self, drawdown_results: Dict[str, Any]) -> str:
        """Generate drawdown analysis report."""
        dd_parts = []
        
        dd_parts.append("📉 DRAWDOWN ANALYSIS")
        dd_parts.append("-" * 40)
        
        # Maximum drawdown
        if 'maximum_drawdown' in drawdown_results:
            md = drawdown_results['maximum_drawdown']
            
            if 'maximum_drawdowns' in md:
                mdd = md['maximum_drawdowns']
                dd_parts.append("📊 Maximum Drawdown Analysis:")
                
                for col, analysis in mdd.items():
                    max_dd = analysis.get('maximum_drawdown_percentage', 0)
                    current_dd = analysis.get('current_drawdown_percentage', 0)
                    dd_parts.append(f"\n  {col}:")
                    dd_parts.append(f"    • Maximum Drawdown: {max_dd:.1f}%")
                    dd_parts.append(f"    • Current Drawdown: {current_dd:.1f}%")
        
        # Drawdown duration
        if 'drawdown_duration' in drawdown_results:
            dd_dur = drawdown_results['drawdown_duration']
            
            if 'duration_statistics' in dd_dur:
                ds = dd_dur['duration_statistics']
                dd_parts.append("\n⏱️  Drawdown Duration:")
                
                for col, stats in ds.items():
                    avg_duration = stats.get('average_duration', 0)
                    max_duration = stats.get('max_duration', 0)
                    time_in_dd = stats.get('percentage_time_in_drawdown', 0)
                    dd_parts.append(f"  • {col}: Avg = {avg_duration:.0f} days, Max = {max_duration} days")
                    dd_parts.append(f"    Time in Drawdown: {time_in_dd:.1f}%")
        
        # Recovery analysis
        if 'recovery_analysis' in drawdown_results:
            ra = drawdown_results['recovery_analysis']
            
            if 'recovery_statistics' in ra:
                rs = ra['recovery_statistics']
                dd_parts.append("\n🔄 Recovery Analysis:")
                
                for col, stats in rs.items():
                    avg_recovery = stats.get('average_recovery_time', 0)
                    success_rate = stats.get('recovery_success_rate', 0)
                    dd_parts.append(f"  • {col}: Avg Recovery = {avg_recovery:.0f} days, Success Rate = {success_rate:.1%}")
        
        return "\n".join(dd_parts)
    
    def _generate_recommendations_section(self, analysis_results: Dict[str, Any]) -> str:
        """Generate recommendations section."""
        rec_parts = []
        
        rec_parts.append("💡 RECOMMENDATIONS")
        rec_parts.append("-" * 40)
        
        # Collect recommendations from all analyses
        all_recommendations = []
        
        # OHLCV recommendations
        if 'ohlcv_analysis' in analysis_results:
            ohlcv = analysis_results['ohlcv_analysis']
            if 'recommendations' in ohlcv:
                all_recommendations.extend(ohlcv['recommendations'].get('data_cleaning', []))
                all_recommendations.extend(ohlcv['recommendations'].get('analysis_improvements', []))
                all_recommendations.extend(ohlcv['recommendations'].get('risk_considerations', []))
        
        # Volatility recommendations
        if 'volatility_analysis' in analysis_results:
            vol = analysis_results['volatility_analysis']
            if 'recommendations' in vol:
                all_recommendations.extend(vol['recommendations'].get('risk_management', []))
                all_recommendations.extend(vol['recommendations'].get('trading_strategies', []))
        
        # Returns recommendations
        if 'returns_analysis' in analysis_results:
            ret = analysis_results['returns_analysis']
            if 'recommendations' in ret:
                all_recommendations.extend(ret['recommendations'].get('return_optimization', []))
                all_recommendations.extend(ret['recommendations'].get('risk_management', []))
        
        # Drawdown recommendations
        if 'drawdown_analysis' in analysis_results:
            dd = analysis_results['drawdown_analysis']
            if 'recommendations' in dd:
                all_recommendations.extend(dd['recommendations'].get('risk_management', []))
                all_recommendations.extend(dd['recommendations'].get('position_sizing', []))
        
        # Display recommendations
        if all_recommendations:
            for i, rec in enumerate(all_recommendations, 1):
                rec_parts.append(f"{i}. {rec}")
        else:
            rec_parts.append("No specific recommendations generated.")
        
        return "\n".join(rec_parts)
    
    def _generate_footer(self) -> str:
        """Generate report footer."""
        footer_parts = []
        
        footer_parts.append("=" * 80)
        footer_parts.append("📊 Financial Analysis Report Complete")
        footer_parts.append(f"Generated by Neozork Financial Analysis Tool")
        footer_parts.append(f"Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        footer_parts.append("=" * 80)
        
        return "\n".join(footer_parts)
    
    def generate_summary_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a summary report."""
        summary_parts = []
        
        summary_parts.append("📊 FINANCIAL ANALYSIS SUMMARY")
        summary_parts.append("=" * 50)
        
        # OHLCV summary
        if 'ohlcv_analysis' in analysis_results:
            ohlcv = analysis_results['ohlcv_analysis']
            if 'data_quality_assessment' in ohlcv:
                dq = ohlcv['data_quality_assessment']
                completeness = dq.get('completeness_score', 0)
                summary_parts.append(f"📈 Data Quality: {completeness:.1f}%")
        
        # Volatility summary
        if 'volatility_analysis' in analysis_results:
            vol = analysis_results['volatility_analysis']
            if 'rolling_volatility' in vol and 'volatility_windows' in vol['rolling_volatility']:
                vw = vol['rolling_volatility']['volatility_windows']
                if vw:
                    first_col = list(vw.keys())[0]
                    if 'window_20' in vw[first_col]:
                        current_vol = vw[first_col]['window_20'].get('current_volatility', 0)
                        summary_parts.append(f"📊 Current Volatility: {current_vol:.4f}")
        
        # Returns summary
        if 'returns_analysis' in analysis_results:
            ret = analysis_results['returns_analysis']
            if 'cumulative_returns' in ret and 'cumulative_simple_returns' in ret['cumulative_returns']:
                csr = ret['cumulative_returns']['cumulative_simple_returns']
                if csr:
                    first_col = list(csr.keys())[0]
                    total_return = csr[first_col].get('total_return', 0)
                    summary_parts.append(f"💰 Total Return: {total_return:.1%}")
        
        # Drawdown summary
        if 'drawdown_analysis' in analysis_results:
            dd = analysis_results['drawdown_analysis']
            if 'maximum_drawdown' in dd and 'maximum_drawdowns' in dd['maximum_drawdown']:
                mdd = dd['maximum_drawdown']['maximum_drawdowns']
                if mdd:
                    first_col = list(mdd.keys())[0]
                    max_dd = mdd[first_col].get('maximum_drawdown_percentage', 0)
                    summary_parts.append(f"📉 Max Drawdown: {max_dd:.1f}%")
        
        return "\n".join(summary_parts)
    
    def generate_transformation_recommendations(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data transformation recommendations."""
        recommendations = {
            'data_cleaning': [],
            'data_transformation': [],
            'feature_engineering': [],
            'quality_improvements': []
        }
        
        try:
            # OHLCV recommendations
            if 'ohlcv_analysis' in analysis_results:
                ohlcv = analysis_results['ohlcv_analysis']
                
                # Data quality recommendations
                if 'data_quality_assessment' in ohlcv:
                    dq = ohlcv['data_quality_assessment']
                    completeness = dq.get('completeness_score', 100)
                    
                    if completeness < 90:
                        recommendations['data_cleaning'].append("Address missing data to improve completeness")
                    
                    if 'quality_issues' in dq and dq['quality_issues']:
                        for issue in dq['quality_issues']:
                            recommendations['data_cleaning'].append(f"Fix: {issue}")
                
                # Price validation recommendations
                if 'price_validation' in ohlcv:
                    pv = ohlcv['price_validation']
                    if 'ohlc_validation' in pv:
                        ohlc = pv['ohlc_validation']
                        valid_pct = (ohlc.get('valid_rows', 0) / ohlc.get('total_rows', 1)) * 100
                        
                        if valid_pct < 95:
                            recommendations['data_cleaning'].append("Review and fix OHLC price relationships")
                
                # Volume recommendations
                if 'volume_analysis' in ohlcv:
                    va = ohlcv['volume_analysis']
                    if 'volume_patterns' in va:
                        vp = va['volume_patterns']
                        zero_vol_pct = vp.get('zero_volume_percentage', 0)
                        
                        if zero_vol_pct > 10:
                            recommendations['data_cleaning'].append("Investigate and handle zero volume periods")
            
            # Volatility recommendations
            if 'volatility_analysis' in analysis_results:
                vol = analysis_results['volatility_analysis']
                
                if 'rolling_volatility' in vol:
                    recommendations['feature_engineering'].append("Consider adding volatility-based features")
                    recommendations['data_transformation'].append("Apply volatility normalization if needed")
            
            # Returns recommendations
            if 'returns_analysis' in analysis_results:
                ret = analysis_results['returns_analysis']
                
                if 'returns_distribution' in ret:
                    recommendations['data_transformation'].append("Consider log returns for better statistical properties")
                    recommendations['feature_engineering'].append("Add returns-based technical indicators")
            
            # Drawdown recommendations
            if 'drawdown_analysis' in analysis_results:
                dd = analysis_results['drawdown_analysis']
                
                if 'maximum_drawdown' in dd:
                    recommendations['quality_improvements'].append("Monitor drawdown patterns for data quality")
                    recommendations['feature_engineering'].append("Add drawdown-based risk features")
        
        except Exception as e:
            self.logger.error(f"Error generating transformation recommendations: {str(e)}")
            recommendations['error'] = str(e)
        
        return recommendations
    
    def save_report(self, report: str, output_path: str) -> bool:
        """Save report to file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            return True
        except Exception as e:
            self.logger.error(f"Error saving report: {str(e)}")
            return False
