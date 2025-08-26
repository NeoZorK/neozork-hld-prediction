#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script for Time Series Analysis functionality.

This script demonstrates the comprehensive time series analysis capabilities
of the NeoZork HLD Prediction system.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.eda.time_series_analysis import TimeSeriesAnalyzer, analyze_time_series


def main():
    """Run time series analysis demo."""
    print("🚀 NEOZORK HLD PREDICTION - TIME SERIES ANALYSIS DEMO")
    print("=" * 60)
    
    # Load sample data
    print("\n📁 Loading sample data...")
    try:
        data_path = Path("data/sample_ohlcv_1000.csv")
        if not data_path.exists():
            print(f"❌ Data file not found: {data_path}")
            print("Please ensure the data file exists.")
            return
            
        data = pd.read_csv(data_path)
        print(f"✅ Data loaded successfully!")
        print(f"   Shape: {data.shape[0]} rows × {data.shape[1]} columns")
        print(f"   Columns: {list(data.columns)}")
        
        # Show data preview
        print(f"\n📋 Data Preview:")
        print(data.head())
        print(f"\nData types:\n{data.dtypes}")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Initialize analyzer
    print(f"\n🔍 Initializing Time Series Analyzer...")
    analyzer = TimeSeriesAnalyzer(data)
    
    # Run comprehensive analysis
    print(f"\n📈 Starting comprehensive time series analysis...")
    print("   This will include:")
    print("   • Stationarity testing (ADF, KPSS)")
    print("   • Trend analysis (linear, moving averages)")
    print("   • Seasonality detection (decomposition, FFT)")
    print("   • Volatility analysis (clustering, persistence)")
    print("   • Autocorrelation analysis (ACF, PACF)")
    print("   • Forecasting (naive, seasonal, ARIMA)")
    print("   • Summary and recommendations")
    
    try:
        # Run analysis on Close price
        results = analyzer.comprehensive_analysis('Close')
        
        # Display summary
        if 'summary' in results:
            summary = results['summary']
            
            print(f"\n📋 ANALYSIS SUMMARY:")
            print("-" * 40)
            
            if 'key_findings' in summary and summary['key_findings']:
                print(f"🔍 Key Findings:")
                for i, finding in enumerate(summary['key_findings'], 1):
                    print(f"   {i}. {finding}")
            
            if 'recommendations' in summary and summary['recommendations']:
                print(f"\n💡 Recommendations:")
                for i, rec in enumerate(summary['recommendations'], 1):
                    print(f"   {i}. {rec}")
            
            if not summary.get('key_findings') and not summary.get('recommendations'):
                print("   No significant patterns detected in the data.")
        
        # Show detailed results
        print(f"\n📊 DETAILED RESULTS:")
        print("-" * 40)
        
        analyses = results.get('analyses', {})
        
        # Stationarity results
        if 'stationarity' in analyses and 'error' not in analyses['stationarity']:
            stationarity = analyses['stationarity']
            print(f"\n📈 Stationarity Analysis:")
            if 'tests' in stationarity:
                tests = stationarity['tests']
                if 'adf' in tests and 'error' not in tests['adf']:
                    adf = tests['adf']
                    print(f"   ADF Test: p-value={adf.get('p_value', 'N/A'):.4f}, "
                          f"Stationary={adf.get('is_stationary', 'N/A')}")
                if 'kpss' in tests and 'error' not in tests['kpss']:
                    kpss = tests['kpss']
                    print(f"   KPSS Test: p-value={kpss.get('p_value', 'N/A'):.4f}, "
                          f"Stationary={kpss.get('is_stationary', 'N/A')}")
        
        # Trend results
        if 'trends' in analyses and 'error' not in analyses['trends']:
            trends = analyses['trends']
            print(f"\n📈 Trend Analysis:")
            if 'trend_analysis' in trends:
                trend_analysis = trends['trend_analysis']
                if 'linear' in trend_analysis:
                    linear = trend_analysis['linear']
                    print(f"   Linear Trend: {linear.get('trend_direction', 'N/A')}, "
                          f"R²={linear.get('r_squared', 'N/A'):.4f}")
        
        # Seasonality results
        if 'seasonality' in analyses and 'error' not in analyses['seasonality']:
            seasonality = analyses['seasonality']
            print(f"\n🔄 Seasonality Analysis:")
            print(f"   Detected Period: {seasonality.get('detected_period', 'N/A')}")
            if 'seasonality_analysis' in seasonality:
                seasonality_analysis = seasonality['seasonality_analysis']
                if 'decomposition' in seasonality_analysis and 'error' not in seasonality_analysis['decomposition']:
                    decomp = seasonality_analysis['decomposition']
                    print(f"   Seasonal Strength: {decomp.get('seasonal_strength', 'N/A'):.4f}")
                    print(f"   Has Seasonality: {decomp.get('has_seasonality', 'N/A')}")
        
        # Volatility results
        if 'volatility' in analyses and 'error' not in analyses['volatility']:
            volatility = analyses['volatility']
            print(f"\n📊 Volatility Analysis:")
            if 'volatility_analysis' in volatility:
                vol_analysis = volatility['volatility_analysis']
                print(f"   Mean Volatility: {vol_analysis.get('mean_volatility', 'N/A'):.4f}")
                print(f"   Volatility Clustering: {vol_analysis.get('has_clustering', 'N/A')}")
        
        # Autocorrelation results
        if 'autocorrelation' in analyses and 'error' not in analyses['autocorrelation']:
            autocorr = analyses['autocorrelation']
            print(f"\n🔗 Autocorrelation Analysis:")
            if 'autocorrelation_analysis' in autocorr:
                acf_analysis = autocorr['autocorrelation_analysis']
                print(f"   Max ACF Lag: {acf_analysis.get('max_acf_lag', 'N/A')}")
                print(f"   Max PACF Lag: {acf_analysis.get('max_pacf_lag', 'N/A')}")
        
        # Show file locations
        print(f"\n💾 Results saved to:")
        print(f"   Results file: {results.get('results_file', 'N/A')}")
        print(f"   Plots directory: results/plots/time_series/")
        
        # Test individual analyses
        print(f"\n🧪 Testing individual analyses...")
        
        # Test stationarity analysis
        print("   📊 Testing stationarity analysis...")
        stationarity_result = analyzer.analyze_stationarity('Close')
        print(f"      ✅ Stationarity analysis completed")
        
        # Test trend analysis
        print("   📈 Testing trend analysis...")
        trend_result = analyzer.analyze_trends('Close')
        print(f"      ✅ Trend analysis completed")
        
        # Test seasonality analysis
        print("   🔄 Testing seasonality analysis...")
        seasonality_result = analyzer.analyze_seasonality('Close')
        print(f"      ✅ Seasonality analysis completed")
        
        # Test volatility analysis
        print("   📊 Testing volatility analysis...")
        volatility_result = analyzer.analyze_volatility('Close')
        print(f"      ✅ Volatility analysis completed")
        
        # Test autocorrelation analysis
        print("   🔗 Testing autocorrelation analysis...")
        autocorr_result = analyzer.analyze_autocorrelation('Close')
        print(f"      ✅ Autocorrelation analysis completed")
        
        # Test forecasting
        print("   🔮 Testing forecasting...")
        forecast_result = analyzer.forecast_series('Close', periods=10)
        print(f"      ✅ Forecasting completed")
        
        print(f"\n✅ All analyses completed successfully!")
        
        # Export results
        print(f"\n📤 Exporting results...")
        export_path = analyzer.export_results()
        print(f"   Results exported to: {export_path}")
        
        print(f"\n🎉 Time Series Analysis Demo completed successfully!")
        print(f"   Check the generated plots and results files for detailed analysis.")
        
    except Exception as e:
        print(f"❌ Error in time series analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
