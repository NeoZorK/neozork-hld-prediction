#!/usr/bin/env python3
"""
Test ML functionality for Pocket Hedge Fund.

This script tests the machine learning and automated trading functionality.
"""

import asyncio
import sys
import os
sys.path.append('../../src')

from pocket_hedge_fund.ml.price_predictor import PricePredictor
from pocket_hedge_fund.trading.automated_trader import AutomatedTrader, TradingStrategy
from pocket_hedge_fund.data.data_manager import DataManager

async def test_ml_functionality():
    """Test ML functionality."""
    print("🚀 Testing ML Functionality for Pocket Hedge Fund")
    print("=" * 60)
    
    try:
        # Test 1: Data Manager
        print("\n1. Testing Data Manager...")
        data_manager = DataManager()
        
        # Load local data
        data = await data_manager.get_local_data("../../data/mn1.csv")
        print(f"   ✅ Loaded {len(data)} records from local data")
        
        # Test 2: Price Predictor
        print("\n2. Testing Price Predictor...")
        predictor = PricePredictor(model_type="ensemble")
        
        # Prepare features
        features_df = await predictor.prepare_features(data)
        print(f"   ✅ Prepared {len(predictor.feature_columns)} features")
        
        # Train models
        training_result = await predictor.train_models(data)
        print(f"   ✅ Training completed: {training_result['status']}")
        
        # Make prediction
        prediction_result = await predictor.predict(data)
        print(f"   ✅ Prediction completed: {prediction_result['status']}")
        
        if prediction_result['status'] == 'success':
            predictions = prediction_result['predictions']
            for model_name, pred in predictions.items():
                if 'prediction' in pred:
                    print(f"      {model_name}: {pred['prediction']:.4f} (confidence: {pred['confidence']:.2f})")
        
        # Test 3: Automated Trader
        print("\n3. Testing Automated Trader...")
        trader = AutomatedTrader("test-fund-001", TradingStrategy.COMBINED)
        
        # Initialize trader
        init_result = await trader.initialize()
        print(f"   ✅ Trader initialized: {init_result['status']}")
        
        # Train models for trader
        training_result = await trader.train_models(["../../data/mn1.csv"], 30)
        print(f"   ✅ Trader training completed: {training_result['status']}")
        
        # Generate trading signals
        signal_result = await trader.generate_trading_signals("../../data/mn1.csv", 110.0)
        print(f"   ✅ Trading signals generated: {signal_result['status']}")
        
        if signal_result['status'] == 'success':
            signals = signal_result['signals']
            print(f"      Combined Signal: {signals['combined_signal'].value}")
            print(f"      Confidence: {signals['confidence']:.2f}")
            print(f"      Reasoning: {', '.join(signals['reasoning'])}")
        
        # Test 4: Performance Summary
        print("\n4. Testing Performance Summary...")
        performance = trader.get_performance_summary()
        print(f"   ✅ Performance summary generated")
        print(f"      Strategy: {performance['strategy']}")
        print(f"      Is Active: {performance['is_active']}")
        print(f"      Trading Enabled: {performance['trading_enabled']}")
        
        print("\n🎉 All ML functionality tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error testing ML functionality: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ml_functionality())
