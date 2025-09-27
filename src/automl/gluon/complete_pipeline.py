"""
Complete Trading Strategy Pipeline
Полный пайплайн торговой стратегии
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging
from pathlib import Path
import time
from datetime import datetime

# Local imports
from .gluon import GluonAutoML
from .models.gluon_evaluator import GluonEvaluator
from .data.multi_indicator_loader import MultiIndicatorLoader
from .data.data_cleaner import DataCleaner
from .features.updated_feature_engineer import UpdatedCustomFeatureEngineer
from .analysis.advanced_analysis import AdvancedTradingAnalyzer
from .config import GluonConfig, ExperimentConfig

logger = logging.getLogger(__name__)


class CompleteTradingPipeline:
    """
    Complete pipeline for creating robust and profitable trading models.
    Полный пайплайн для создания робастных и прибыльных торговых моделей.
    """
    
    def __init__(self, base_data_path: str = "data/cache/csv_converted/"):
        """
        Initialize Complete Trading Pipeline.
        
        Args:
            base_data_path: Base path to data directory
        """
        self.base_data_path = base_data_path
        self.multi_loader = MultiIndicatorLoader(base_data_path)
        self.data_cleaner = DataCleaner()
        self.feature_engineer = UpdatedCustomFeatureEngineer()
        self.analyzer = AdvancedTradingAnalyzer()
        
        # Initialize AutoGluon with optimal configuration
        self.gluon_config = GluonConfig(
            time_limit=7200,  # 2 hours
            presets=['best_quality'],
            excluded_model_types=["NN_TORCH", "NN_FASTAI"],
            num_bag_folds=5,
            # Disable dynamic stacking to avoid "Learner is already fit" error
            dynamic_stacking=False,
            num_stack_levels=1
        )
        
        # Initialize gluon as None - will be created fresh each time
        self.gluon = None
        
    def _create_fresh_gluon(self):
        """
        Create a fresh GluonAutoML instance.
        Создать новый экземпляр GluonAutoML.
        """
        logger.info("🔄 Creating fresh GluonAutoML instance...")
        
        # Clean up old instance if exists
        if self.gluon is not None:
            try:
                # Try to clean up any existing state
                if hasattr(self.gluon, 'trainer') and hasattr(self.gluon.trainer, 'predictor'):
                    del self.gluon.trainer.predictor
                if hasattr(self.gluon, 'trainer'):
                    del self.gluon.trainer
                del self.gluon
            except Exception as e:
                logger.warning(f"⚠️ Error cleaning up old gluon instance: {e}")
        
        # Create new instance
        self.gluon = GluonAutoML()
        logger.info("✅ Fresh GluonAutoML instance created")
        
    def _get_unique_model_path(self):
        """
        Get unique model path for this session.
        Получить уникальный путь модели для этой сессии.
        """
        import uuid
        session_id = str(uuid.uuid4())[:8]
        return f"models/autogluon_{session_id}"
        
    def _cleanup_old_models(self):
        """
        Clean up old model directories.
        Очистить старые директории моделей.
        """
        logger.info("🧹 Cleaning up old model directories...")
        
        import shutil
        import glob
        import os
        
        # Clean up all autogluon directories
        cleanup_patterns = [
            "models/autogluon*",
            "models/autogluon",
            "models/autogluon/ds_sub_fit*",
            "models/autogluon/ds_sub_fit",
            "models/autogluon/ds_sub_fit/sub_fit_ho*",
            "models/autogluon/ds_sub_fit/sub_fit_ho"
        ]
        
        for pattern in cleanup_patterns:
            model_dirs = glob.glob(pattern)
            for model_dir in model_dirs:
                try:
                    if os.path.exists(model_dir):
                        shutil.rmtree(model_dir)
                        logger.info(f"✅ Cleaned: {model_dir}")
                except Exception as e:
                    logger.warning(f"⚠️ Could not clean {model_dir}: {e}")
        
        # Additional cleanup for any remaining .pkl files
        pkl_files = glob.glob("models/**/*.pkl", recursive=True)
        for pkl_file in pkl_files:
            try:
                if os.path.exists(pkl_file):
                    os.remove(pkl_file)
                    logger.info(f"✅ Removed: {pkl_file}")
            except Exception as e:
                logger.warning(f"⚠️ Could not remove {pkl_file}: {e}")
        
        # Force cleanup using subprocess
        import subprocess
        try:
            # Use find command to locate and remove any remaining AutoGluon directories
            result = subprocess.run(['find', 'models', '-name', '*autogluon*', '-type', 'd'], 
                                 capture_output=True, text=True)
            if result.stdout:
                for dir_path in result.stdout.strip().split('\n'):
                    if dir_path and os.path.exists(dir_path):
                        shutil.rmtree(dir_path)
                        logger.info(f"✅ Force cleaned: {dir_path}")
        except Exception as e:
            logger.warning(f"⚠️ Force cleanup failed: {e}")
        
        logger.info("🧹 Model cleanup completed")
        
    def _train_with_isolated_process(self, train_data: pd.DataFrame, val_data: pd.DataFrame, 
                                   model_path: str) -> bool:
        """
        Train model using isolated subprocess to avoid "Learner is already fit" error.
        Обучить модель используя изолированный подпроцесс для избежания ошибки "Learner is already fit".
        """
        import subprocess
        import tempfile
        import pickle
        
        logger.info("🔄 Training with isolated subprocess...")
        
        try:
            # Create temporary files for data
            with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as train_file:
                train_path = train_file.name
                pickle.dump(train_data, train_file)
            
            with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as val_file:
                val_path = val_file.name
                pickle.dump(val_data, val_file)
            
            # Run isolated training
            cmd = [
                'python', 'src/automl/gluon/isolated_trainer.py',
                '--train-data', train_path,
                '--val-data', val_path,
                '--target-column', 'target',
                '--model-path', model_path
            ]
            
            logger.info(f"🚀 Running isolated training: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)  # 2 hour timeout
            
            # Clean up temporary files
            import os
            os.unlink(train_path)
            os.unlink(val_path)
            
            if result.returncode == 0:
                logger.info("✅ Isolated training completed successfully")
                return True
            else:
                logger.error(f"❌ Isolated training failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Isolated training timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Isolated training error: {e}")
            return False
        
    def run_complete_pipeline(self, symbols: List[str] = None, timeframes: List[str] = None, 
                            target_symbol: str = None, target_timeframe: str = None,
                            use_auto_scan: bool = True, interactive: bool = True) -> Dict[str, Any]:
        """
        Run complete trading strategy pipeline.
        Запустить полный пайплайн торговой стратегии.
        
        Args:
            symbols: List of trading symbols (ignored if use_auto_scan=True)
            timeframes: List of timeframes (ignored if use_auto_scan=True)
            target_symbol: Target symbol for final model (auto-detected if use_auto_scan=True)
            target_timeframe: Target timeframe for final model (auto-detected if use_auto_scan=True)
            use_auto_scan: Whether to use automatic scanning and selection
            interactive: Whether to use interactive selection
            
        Returns:
            Dictionary with complete pipeline results
        """
        logger.info("🚀 Starting Complete Trading Strategy Pipeline")
        
        if use_auto_scan:
            logger.info("🔍 Using automatic data scanning and selection")
            logger.info(f"Interactive mode: {interactive}")
        else:
            logger.info(f"Symbols: {symbols}")
            logger.info(f"Timeframes: {timeframes}")
            logger.info(f"Target: {target_symbol} {target_timeframe}")
        
        pipeline_start_time = time.time()
        results = {}
        
        try:
            # Step 1: Load and combine data
            logger.info("📊 Step 1: Loading and combining data...")
            combined_data = self._load_and_combine_data(
                symbols=symbols, 
                timeframes=timeframes,
                use_auto_scan=use_auto_scan,
                interactive=interactive
            )
            # Get actual loaded symbols and timeframes from data
            if use_auto_scan:
                actual_symbols = combined_data['symbol'].unique().tolist() if 'symbol' in combined_data.columns else []
                actual_timeframes = combined_data['timeframe'].unique().tolist() if 'timeframe' in combined_data.columns else []
                actual_indicators = combined_data['indicator'].unique().tolist() if 'indicator' in combined_data.columns else []
            else:
                actual_symbols = symbols
                actual_timeframes = timeframes
                actual_indicators = []
            
            results['data_loading'] = {
                'total_rows': len(combined_data),
                'total_columns': len(combined_data.columns),
                'symbols_loaded': actual_symbols,
                'timeframes_loaded': actual_timeframes,
                'indicators_loaded': actual_indicators,
                'auto_scan_used': use_auto_scan
            }
            
            # Step 2: Feature engineering
            logger.info("🔧 Step 2: Feature engineering...")
            data_with_features = self._create_all_features(combined_data, target_symbol, target_timeframe)
            results['feature_engineering'] = {
                'features_created': len([col for col in data_with_features.columns if 'probability' in col]),
                'total_features': len(data_with_features.columns),
                'data_shape': data_with_features.shape
            }
            
            # Step 2.5: Data cleaning
            logger.info("🧹 Step 2.5: Data cleaning...")
            cleaned_data, cleaning_report = self.data_cleaner.clean_data(data_with_features, "target")
            validation_report = self.data_cleaner.validate_data(cleaned_data, "target")
            results['data_cleaning'] = {
                'cleaning_report': cleaning_report,
                'validation_report': validation_report
            }
            
            # Step 3: Data preparation
            logger.info("📋 Step 3: Data preparation...")
            train_data, val_data, test_data = self._prepare_data(cleaned_data)
            results['data_preparation'] = {
                'train_size': len(train_data),
                'val_size': len(val_data),
                'test_size': len(test_data),
                'train_ratio': len(train_data) / len(data_with_features),
                'val_ratio': len(val_data) / len(data_with_features),
                'test_ratio': len(test_data) / len(data_with_features)
            }
            
            # Step 4: Model training
            logger.info("🤖 Step 4: Model training...")
            
            # Create fresh GluonAutoML instance
            self._create_fresh_gluon()
            
            # Get unique model path
            unique_model_path = self._get_unique_model_path()
            logger.info(f"📁 Using unique model path: {unique_model_path}")
            
            # Clean up old models
            self._cleanup_old_models()
            
            # Train with isolated process to avoid "Learner is already fit" error
            training_start = time.time()
            try:
                # Use isolated training process
                success = self._train_with_isolated_process(train_data, val_data, unique_model_path)
                training_time = time.time() - training_start
                
                if success:
                    logger.info(f"✅ Model training completed in {training_time:.2f} seconds")
                else:
                    raise Exception("Isolated training failed")
                    
            except Exception as e:
                logger.error(f"❌ Model training failed: {e}")
                training_time = time.time() - training_start
            results['model_training'] = {
                'training_time_seconds': training_time,
                'training_time_minutes': training_time / 60,
                'model_ready': True
            }
            
            # Step 5: Model evaluation
            logger.info("📈 Step 5: Model evaluation...")
            try:
                # Load the trained model from the isolated process
                from autogluon.tabular import TabularPredictor
                predictor = TabularPredictor.load(unique_model_path)
                
                # Create a temporary GluonAutoML instance for evaluation
                temp_gluon = GluonAutoML()
                temp_gluon.predictor = predictor
                temp_gluon.evaluator = GluonEvaluator(predictor)
                
                # Store the predictor in the main gluon instance for later use
                self.gluon = temp_gluon
                
                evaluation = temp_gluon.evaluate_models(test_data, "target")
                results['model_evaluation'] = evaluation
                logger.info("✅ Model evaluation completed successfully")
            except Exception as e:
                logger.error(f"❌ Model evaluation failed: {e}")
                results['model_evaluation'] = {'error': str(e)}
            
            # Step 6: Advanced analysis
            logger.info("🔍 Step 6: Advanced analysis...")
            analysis_results = self._run_advanced_analysis(test_data)
            results['advanced_analysis'] = analysis_results
            
            # Step 7: Model export
            logger.info("💾 Step 7: Model export...")
            export_path = self.gluon.export_models(f"models/complete_pipeline_{target_symbol}_{target_timeframe}")
            results['model_export'] = {
                'export_path': export_path,
                'export_successful': True
            }
            
            # Step 8: Performance report
            logger.info("📊 Step 8: Generating performance report...")
            performance_report = self._generate_performance_report(results)
            results['performance_report'] = performance_report
            
            # Final summary
            pipeline_time = time.time() - pipeline_start_time
            results['pipeline_summary'] = {
                'total_time_seconds': pipeline_time,
                'total_time_minutes': pipeline_time / 60,
                'pipeline_successful': True,
                'target_symbol': target_symbol,
                'target_timeframe': target_timeframe,
                'completion_time': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Complete pipeline finished successfully in {pipeline_time/60:.1f} minutes")
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {e}")
            results['pipeline_summary'] = {
                'pipeline_successful': False,
                'error': str(e),
                'completion_time': datetime.now().isoformat()
            }
        
        return results
    
    def _load_and_combine_data(self, symbols: List[str] = None, timeframes: List[str] = None, 
                              use_auto_scan: bool = True, interactive: bool = True) -> pd.DataFrame:
        """
        Load and combine data from multiple sources.
        Загрузить и объединить данные из множественных источников.
        
        Args:
            symbols: List of symbols (ignored if use_auto_scan=True)
            timeframes: List of timeframes (ignored if use_auto_scan=True)
            use_auto_scan: Whether to use automatic scanning and selection
            interactive: Whether to use interactive selection
            
        Returns:
            Combined dataframe
        """
        if use_auto_scan:
            logger.info("🔍 Using automatic data scanning and selection...")
            
            # Use auto-loading
            final_data = self.multi_loader.auto_load_data(interactive=interactive)
            
            if final_data.empty:
                raise ValueError("No data loaded successfully with auto-scan")
            
            logger.info(f"📊 Auto-loaded data: {len(final_data)} rows, {len(final_data.columns)} columns")
            return final_data
        
        else:
            # Original manual loading
            logger.info("📊 Using manual data loading...")
            
            if not symbols or not timeframes:
                raise ValueError("Symbols and timeframes must be provided when use_auto_scan=False")
            
            all_combined_data = []
            
            for symbol in symbols:
                for timeframe in timeframes:
                    try:
                        logger.info(f"📊 Loading {symbol} {timeframe}...")
                        
                        # Load all indicators for this symbol/timeframe
                        symbol_data = self.multi_loader.load_symbol_data(symbol, timeframe)
                        
                        # Combine indicators
                        combined_symbol_data = self.multi_loader.combine_indicators(symbol_data)
                        
                        if not combined_symbol_data.empty:
                            # Add metadata
                            combined_symbol_data['symbol'] = symbol
                            combined_symbol_data['timeframe'] = timeframe
                            
                            # Add timeframe weight
                            timeframe_weights = {'M1': 1, 'M5': 2, 'M15': 3, 'H1': 4, 'H4': 8, 'D1': 16, 'W1': 32, 'MN1': 64}
                            combined_symbol_data['timeframe_weight'] = timeframe_weights.get(timeframe, 1)
                            
                            all_combined_data.append(combined_symbol_data)
                            logger.info(f"✅ {symbol} {timeframe}: {len(combined_symbol_data)} rows")
                        else:
                            logger.warning(f"⚠️ No data for {symbol} {timeframe}")
                            
                    except Exception as e:
                        logger.error(f"❌ Failed to load {symbol} {timeframe}: {e}")
                        continue
            
            if not all_combined_data:
                raise ValueError("No data loaded successfully")
            
            # Combine all data
            logger.info("🔄 Combining all data...")
            final_data = pd.concat(all_combined_data, ignore_index=True)
            
            # Add technical indicators
            final_data = self.multi_loader.add_technical_indicators(final_data)
            
            logger.info(f"📊 Final combined data: {len(final_data)} rows, {len(final_data.columns)} columns")
            
            return final_data
    
    def _create_all_features(self, data: pd.DataFrame, target_symbol: str, target_timeframe: str) -> pd.DataFrame:
        """Create all custom features."""
        
        logger.info("🔧 Creating custom features...")
        
        # Filter for target symbol and timeframe if specified
        if target_symbol and target_timeframe:
            target_data = data[(data['symbol'] == target_symbol) & (data['timeframe'] == target_timeframe)]
            if not target_data.empty:
                logger.info(f"Using target data: {target_symbol} {target_timeframe} ({len(target_data)} rows)")
                data = target_data
            else:
                logger.warning(f"Target data not found, using all data")
        
        # Create target variable
        data = self.multi_loader.create_target_variable(data, method='price_direction')
        
        # Create custom features using the updated feature engineer
        # For now, we'll create features based on available columns
        data_with_features = data.copy()
        
        # Add SCHR features if CSVExport columns are available
        csv_export_columns = ['pressure', 'pressure_vector', 'predicted_low', 'predicted_high']
        if any(col in data.columns for col in csv_export_columns):
            logger.info("Creating SCHR features...")
            data_with_features = self.feature_engineer.create_schr_features(data_with_features)
        
        # Add WAVE2 features if WAVE2 columns are available
        wave2_columns = ['wave', 'fast_line', 'ma_line', 'direction', 'signal']
        if any(col in data.columns for col in wave2_columns):
            logger.info("Creating WAVE2 features...")
            data_with_features = self.feature_engineer.create_wave2_features(data_with_features)
        
        # Add SHORT3 features if SHORT3 columns are available
        short3_columns = ['short_trend', 'r_trend', 'global', 'direction', 'r_direction', 'signal', 'r_signal', 'g_direction', 'g_signal']
        if any(col in data.columns for col in short3_columns):
            logger.info("Creating SHORT3 features...")
            data_with_features = self.feature_engineer.create_short3_features(data_with_features)
        
        # Remove rows with NaN target
        initial_rows = len(data_with_features)
        data_with_features = data_with_features.dropna(subset=['target'])
        removed_rows = initial_rows - len(data_with_features)
        
        if removed_rows > 0:
            logger.info(f"Removed {removed_rows} rows with NaN target")
        
        logger.info(f"✅ Feature engineering completed: {len(data_with_features)} rows, {len(data_with_features.columns)} columns")
        
        return data_with_features
    
    def _prepare_data(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Prepare data for training with time series split."""
        
        logger.info("📋 Preparing data with time series split...")
        
        # Sort by time if possible
        if data.index.dtype == 'datetime64[ns]':
            data = data.sort_index()
        elif 'timestamp' in data.columns:
            data = data.sort_values('timestamp')
        
        # Time series split
        total_len = len(data)
        train_end = int(total_len * 0.6)
        val_end = int(total_len * 0.8)
        
        train_data = data.iloc[:train_end]
        val_data = data.iloc[train_end:val_end]
        test_data = data.iloc[val_end:]
        
        logger.info(f"Data split: Train={len(train_data)}, Val={len(val_data)}, Test={len(test_data)}")
        
        return train_data, val_data, test_data
    
    def _run_advanced_analysis(self, test_data: pd.DataFrame) -> Dict[str, Any]:
        """Run advanced analysis including backtesting, walk forward, and Monte Carlo."""
        
        logger.info("🔍 Running advanced analysis...")
        
        analysis_results = {}
        
        try:
            # Backtesting
            logger.info("📈 Running backtesting...")
            backtest_results = self.analyzer.comprehensive_backtesting(self.gluon, test_data)
            analysis_results['backtesting'] = backtest_results
            
            # Walk Forward Analysis
            logger.info("🚶 Running Walk Forward analysis...")
            wf_results = self.analyzer.walk_forward_analysis(self.gluon, test_data, 
                                                           window_size=500, step_size=50)
            analysis_results['walk_forward'] = wf_results
            
            # Monte Carlo Simulation
            logger.info("🎲 Running Monte Carlo simulation...")
            mc_results = self.analyzer.monte_carlo_simulation(self.gluon, test_data, 
                                                            n_simulations=500, sample_size=300)
            analysis_results['monte_carlo'] = mc_results
            
            # Performance Report
            performance_report = self.analyzer.create_performance_report(
                backtest_results, wf_results, mc_results
            )
            analysis_results['performance_report'] = performance_report
            
            logger.info("✅ Advanced analysis completed")
            
        except Exception as e:
            logger.error(f"❌ Advanced analysis failed: {e}")
            analysis_results['error'] = str(e)
        
        return analysis_results
    
    def _generate_performance_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive performance report."""
        
        report = f"""
# 🚀 COMPLETE TRADING STRATEGY PIPELINE REPORT
# Отчет полного пайплайна торговой стратегии

## 📊 Pipeline Summary / Сводка пайплайна

**Execution Time:** {results.get('pipeline_summary', {}).get('total_time_minutes', 0):.1f} minutes
**Status:** {'✅ SUCCESS' if results.get('pipeline_summary', {}).get('pipeline_successful', False) else '❌ FAILED'}
**Target:** {results.get('pipeline_summary', {}).get('target_symbol', 'N/A')} {results.get('pipeline_summary', {}).get('target_timeframe', 'N/A')}

## 📈 Data Processing / Обработка данных

**Data Loading:**
- Total Rows: {results.get('data_loading', {}).get('total_rows', 0):,}
- Total Columns: {results.get('data_loading', {}).get('total_columns', 0)}
- Symbols: {', '.join(results.get('data_loading', {}).get('symbols_loaded', []))}
- Timeframes: {', '.join(results.get('data_loading', {}).get('timeframes_loaded', []))}

**Feature Engineering:**
- Custom Features Created: {results.get('feature_engineering', {}).get('features_created', 0)}
- Total Features: {results.get('feature_engineering', {}).get('total_features', 0)}
- Final Data Shape: {results.get('feature_engineering', {}).get('data_shape', 'N/A')}

**Data Preparation:**
- Train Size: {results.get('data_preparation', {}).get('train_size', 0):,}
- Validation Size: {results.get('data_preparation', {}).get('val_size', 0):,}
- Test Size: {results.get('data_preparation', {}).get('test_size', 0):,}

## 🤖 Model Performance / Производительность модели

**Training:**
- Training Time: {results.get('model_training', {}).get('training_time_minutes', 0):.1f} minutes
- Model Status: {'✅ Ready' if results.get('model_training', {}).get('model_ready', False) else '❌ Failed'}

**Evaluation:**
{self._format_evaluation_results(results.get('model_evaluation', {}))}

## 🔍 Advanced Analysis / Продвинутый анализ

{self._format_advanced_analysis_results(results.get('advanced_analysis', {}))}

## 💾 Model Export / Экспорт модели

**Export Path:** {results.get('model_export', {}).get('export_path', 'N/A')}
**Export Status:** {'✅ Success' if results.get('model_export', {}).get('export_successful', False) else '❌ Failed'}

## 🎯 Recommendations / Рекомендации

1. **Model Quality:** {'✅ High' if self._is_high_quality_model(results) else '⚠️ Needs Improvement'}
2. **Production Ready:** {'✅ Yes' if self._is_production_ready(results) else '❌ No'}
3. **Next Steps:** {self._get_next_steps(results)}

---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def _format_evaluation_results(self, evaluation: Dict[str, Any]) -> str:
        """Format evaluation results for report."""
        if not evaluation:
            return "No evaluation results available"
        
        formatted = "**Model Metrics:**\n"
        for metric, value in evaluation.items():
            if isinstance(value, (int, float)):
                formatted += f"- {metric}: {value:.4f}\n"
        
        return formatted
    
    def _format_advanced_analysis_results(self, analysis: Dict[str, Any]) -> str:
        """Format advanced analysis results for report."""
        if not analysis:
            return "No advanced analysis results available"
        
        formatted = ""
        
        if 'backtesting' in analysis:
            bt = analysis['backtesting']
            formatted += f"**Backtesting:**\n"
            formatted += f"- Total Return: {bt.get('total_return', 0):.2%}\n"
            formatted += f"- Sharpe Ratio: {bt.get('sharpe_ratio', 0):.3f}\n"
            formatted += f"- Max Drawdown: {bt.get('max_drawdown', 0):.2%}\n"
        
        if 'walk_forward' in analysis:
            wf = analysis['walk_forward']
            formatted += f"**Walk Forward:**\n"
            formatted += f"- Stability Score: {wf.get('stability_score', 0):.3f}\n"
            formatted += f"- Mean Accuracy: {wf.get('mean_accuracy', 0):.3f}\n"
        
        if 'monte_carlo' in analysis:
            mc = analysis['monte_carlo']
            formatted += f"**Monte Carlo:**\n"
            formatted += f"- Robustness Score: {mc.get('robustness_score', 0):.3f}\n"
            formatted += f"- Mean Accuracy: {mc.get('mean_accuracy', 0):.3f}\n"
        
        return formatted
    
    def _is_high_quality_model(self, results: Dict[str, Any]) -> bool:
        """Check if model is high quality."""
        evaluation = results.get('model_evaluation', {})
        accuracy = evaluation.get('accuracy', 0)
        return accuracy > 0.6
    
    def _is_production_ready(self, results: Dict[str, Any]) -> bool:
        """Check if model is production ready."""
        return (results.get('pipeline_summary', {}).get('pipeline_successful', False) and
                results.get('model_export', {}).get('export_successful', False))
    
    def _get_next_steps(self, results: Dict[str, Any]) -> str:
        """Get next steps recommendations."""
        if results.get('pipeline_summary', {}).get('pipeline_successful', False):
            return "Deploy model to production, set up monitoring, and schedule retraining"
        else:
            return "Fix pipeline issues, check data quality, and retry"
