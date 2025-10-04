"""
CLI Commands for SCHR Levels AutoML

Individual command implementations for different operations.
"""

import os
import sys
import webbrowser
from typing import Any, Dict
from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """Base class for CLI commands"""
    
    @abstractmethod
    def execute(self, args) -> int:
        """Execute the command"""
        pass


class TrainCommand(BaseCommand):
    """Train ML models command"""
    
    def execute(self, args) -> int:
        """Execute training command"""
        try:
            from ...analysis.pipeline import SCHRLevelsAutoMLPipeline
            
            print("🚀 Starting SCHR Levels Model Training...")
            
            # Initialize pipeline
            pipeline = SCHRLevelsAutoMLPipeline(data_path=args.data_path)
            
            # Load data
            print(f"📊 Loading data for {args.symbol} {args.timeframe}...")
            data = pipeline.load_schr_data(args.symbol, args.timeframe)
            data = pipeline.create_target_variables(data)
            data = pipeline.create_features(data)
            
            print(f"✅ Loaded {len(data)} records with {len(data.columns)} features")
            
            # Determine tasks
            tasks = args.tasks if 'all' not in args.tasks else [
                'pressure_vector_sign', 'price_direction_1period', 'level_breakout'
            ]
            
            # Train models
            results = {}
            for task in tasks:
                print(f"\n🤖 Training model for {task}...")
                
                # Configure training
                config = {
                    'time_limit': args.time_limit,
                    'presets': args.presets,
                    'excluded_model_types': args.exclude_models or [],
                    'use_gpu': args.gpu,
                    'num_gpus': 1 if args.gpu else 0
                }
                
                result = pipeline.train_model(data, task, **config)
                if result:
                    results[task] = result
                    print(f"✅ {task}: {result['metrics']['accuracy']:.2%} accuracy")
                else:
                    print(f"❌ Failed to train {task}")
            
            # Save results
            if args.output_dir:
                os.makedirs(args.output_dir, exist_ok=True)
                pipeline.save_results(results, args.output_dir)
                print(f"💾 Results saved to {args.output_dir}")
            
            # Launch web interface if requested
            if args.web:
                self._launch_web_interface(args, results)
            
            print("🎉 Training completed successfully!")
            return 0
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return 1
    
    def _launch_web_interface(self, args, results):
        """Launch web interface for training results"""
        from ...web.dashboard import SCHRWebDashboard
        
        dashboard = SCHRWebDashboard(port=args.port, host=args.host)
        dashboard.show_training_results(results)
        
        if args.browser:
            webbrowser.open(f"http://{args.host}:{args.port}")


class PredictCommand(BaseCommand):
    """Make predictions command"""
    
    def execute(self, args) -> int:
        """Execute prediction command"""
        try:
            from ...analysis.pipeline import SCHRLevelsAutoMLPipeline
            
            print("🔮 Starting SCHR Levels Predictions...")
            
            # Initialize pipeline
            pipeline = SCHRLevelsAutoMLPipeline(data_path=args.data_path)
            
            # Load data
            data = pipeline.load_schr_data(args.symbol, args.timeframe)
            data = pipeline.create_target_variables(data)
            data = pipeline.create_features(data)
            
            # Make predictions
            tasks = args.tasks if 'all' not in args.tasks else [
                'pressure_vector_sign', 'price_direction_1period', 'level_breakout'
            ]
            
            predictions = {}
            for task in tasks:
                print(f"\n🔮 Making predictions for {task}...")
                
                try:
                    pred_result = pipeline.predict_for_trading(data.tail(10), task)
                    predictions[task] = pred_result
                    
                    print(f"✅ {task} predictions:")
                    print(f"   Predictions: {pred_result['predictions'].values}")
                    if pred_result['probabilities'] is not None:
                        print(f"   Probabilities: {pred_result['probabilities'].values}")
                        
                except Exception as e:
                    print(f"❌ Failed to predict {task}: {e}")
            
            # Save predictions if requested
            if args.save_predictions:
                import pandas as pd
                pred_df = pd.DataFrame(predictions)
                pred_df.to_csv(f"{args.output_dir}/predictions_{args.symbol}_{args.timeframe}.csv")
                print(f"💾 Predictions saved to {args.output_dir}")
            
            # Launch web interface if requested
            if args.web:
                self._launch_web_interface(args, predictions)
            
            print("🎉 Predictions completed successfully!")
            return 0
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            return 1
    
    def _launch_web_interface(self, args, predictions):
        """Launch web interface for predictions"""
        from ...web.dashboard import SCHRWebDashboard
        
        dashboard = SCHRWebDashboard(port=args.port, host=args.host)
        dashboard.show_predictions(predictions)
        
        if args.browser:
            webbrowser.open(f"http://{args.host}:{args.port}")


class BacktestCommand(BaseCommand):
    """Run backtesting command"""
    
    def execute(self, args) -> int:
        """Execute backtesting command"""
        try:
            from ...analysis.backtest import SCHRBacktester
            
            print("📈 Starting SCHR Levels Backtesting...")
            
            # Initialize backtester
            backtester = SCHRBacktester(
                data_path=args.data_path,
                initial_capital=args.initial_capital,
                commission=args.commission
            )
            
            # Run backtest
            results = backtester.run_backtest(
                symbol=args.symbol,
                timeframe=args.timeframe,
                start_date=args.start_date,
                end_date=args.end_date,
                strategy=args.strategy
            )
            
            # Display results
            print(f"\n📊 Backtest Results:")
            print(f"   Total Return: {results['total_return']:.2%}")
            print(f"   Sharpe Ratio: {results['sharpe_ratio']:.2f}")
            print(f"   Max Drawdown: {results['max_drawdown']:.2%}")
            print(f"   Win Rate: {results['win_rate']:.2%}")
            
            # Launch web interface if requested
            if args.web:
                self._launch_web_interface(args, results)
            
            print("🎉 Backtesting completed successfully!")
            return 0
            
        except Exception as e:
            print(f"❌ Backtesting failed: {e}")
            return 1
    
    def _launch_web_interface(self, args, results):
        """Launch web interface for backtest results"""
        from ...web.dashboard import SCHRWebDashboard
        
        dashboard = SCHRWebDashboard(port=args.port, host=args.host)
        dashboard.show_backtest_results(results)
        
        if args.browser:
            webbrowser.open(f"http://{args.host}:{args.port}")


class ValidateCommand(BaseCommand):
    """Run validation command"""
    
    def execute(self, args) -> int:
        """Execute validation command"""
        try:
            from ...analysis.pipeline import SCHRLevelsAutoMLPipeline
            
            print(f"🔍 Starting {args.type} validation...")
            
            # Initialize pipeline
            pipeline = SCHRLevelsAutoMLPipeline(data_path=args.data_path)
            
            # Load data
            data = pipeline.load_schr_data(args.symbol, args.timeframe)
            data = pipeline.create_target_variables(data)
            data = pipeline.create_features(data)
            
            # Run validation
            tasks = args.tasks if 'all' not in args.tasks else [
                'pressure_vector_sign', 'price_direction_1period', 'level_breakout'
            ]
            
            validation_results = {}
            for task in tasks:
                print(f"\n🔍 Validating {task}...")
                
                if args.type == 'walk-forward':
                    result = pipeline.walk_forward_validation(
                        data, task, n_splits=args.splits
                    )
                elif args.type == 'monte-carlo':
                    result = pipeline.monte_carlo_validation(
                        data, task, n_iterations=args.iterations
                    )
                else:
                    print(f"❌ Unknown validation type: {args.type}")
                    continue
                
                validation_results[task] = result
                print(f"✅ {task}: {result['mean_accuracy']:.2%} ± {result['std_accuracy']:.2%}")
            
            # Save results if requested
            if args.save_results:
                import pickle
                with open(f"{args.output_dir}/validation_results.pkl", 'wb') as f:
                    pickle.dump(validation_results, f)
                print(f"💾 Validation results saved to {args.output_dir}")
            
            # Launch web interface if requested
            if args.web:
                self._launch_web_interface(args, validation_results)
            
            print("🎉 Validation completed successfully!")
            return 0
            
        except Exception as e:
            print(f"❌ Validation failed: {e}")
            return 1
    
    def _launch_web_interface(self, args, results):
        """Launch web interface for validation results"""
        from ...web.dashboard import SCHRWebDashboard
        
        dashboard = SCHRWebDashboard(port=args.port, host=args.host)
        dashboard.show_validation_results(results, args.type)
        
        if args.browser:
            webbrowser.open(f"http://{args.host}:{args.port}")


class WebCommand(BaseCommand):
    """Launch web dashboard command"""
    
    def execute(self, args) -> int:
        """Execute web dashboard command"""
        try:
            from ...web.dashboard import SCHRWebDashboard
            
            print(f"🌐 Starting SCHR Levels Web Dashboard on {args.host}:{args.port}")
            
            # Initialize dashboard
            dashboard = SCHRWebDashboard(
                port=args.port,
                host=args.host,
                theme=args.theme,
                auto_refresh=args.auto_refresh
            )
            
            # Launch dashboard
            dashboard.launch()
            
            if args.browser:
                webbrowser.open(f"http://{args.host}:{args.port}")
            
            print("🎉 Web dashboard launched successfully!")
            return 0
            
        except Exception as e:
            print(f"❌ Web dashboard failed: {e}")
            return 1
