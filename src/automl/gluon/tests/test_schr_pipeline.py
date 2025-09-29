#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест SCHR Levels AutoML Pipeline
Проверяем работу пайплайна на реальных данных
"""

import sys
import logging
from pathlib import Path
import os

# Disable CUDA for MacBook M1
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["AUTOGLUON_USE_GPU"] = "false"
os.environ["AUTOGLUON_USE_GPU_TORCH"] = "false"
os.environ["AUTOGLUON_USE_GPU_FASTAI"] = "false"

# Добавляем текущую директорию в путь
sys.path.append(str(Path(__file__).parent))

# Импортируем класс напрямую из файла
import importlib.util
spec = importlib.util.spec_from_file_location("schr_levels_gluon", "../../../schr-levels-gluon.py")
schr_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schr_module)
SCHRLevelsAutoMLPipeline = schr_module.SCHRLevelsAutoMLPipeline

# Настройка логирования для теста
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_data_loading():
    """Тест загрузки данных"""
    print("🔍 Тестируем загрузку данных...")
    
    pipeline = SCHRLevelsAutoMLPipeline()
    
    try:
        # Загружаем данные BTCUSD MN1
        data = pipeline.load_schr_data("BTCUSD", "MN1")
        print(f"✅ Данные загружены: {len(data)} записей, {len(data.columns)} колонок")
        print(f"📊 Колонки: {list(data.columns)}")
        print(f"📅 Период: {data.index.min()} - {data.index.max()}")
        return data
    except Exception as e:
        print(f"❌ Ошибка загрузки данных: {e}")
        return None

def test_target_creation(data):
    """Тест создания целевых переменных"""
    print("\n🎯 Тестируем создание целевых переменных...")
    
    pipeline = SCHRLevelsAutoMLPipeline()
    
    try:
        data_with_targets = pipeline.create_target_variables(data)
        print(f"✅ Целевые переменные созданы: {len(data_with_targets)} записей")
        
        # Проверяем наличие целевых переменных
        target_cols = [col for col in data_with_targets.columns if col.startswith('target_')]
        print(f"📊 Целевые переменные: {target_cols}")
        
        for col in target_cols:
            print(f"   {col}: {data_with_targets[col].value_counts().to_dict()}")
        
        return data_with_targets
    except Exception as e:
        print(f"❌ Ошибка создания целевых переменных: {e}")
        return None

def test_feature_creation(data):
    """Тест создания признаков"""
    print("\n🔧 Тестируем создание признаков...")
    
    pipeline = SCHRLevelsAutoMLPipeline()
    
    try:
        features_data = pipeline.create_features(data)
        print(f"✅ Признаки созданы: {len(features_data)} записей, {len(features_data.columns)} признаков")
        
        # Показываем новые признаки
        new_features = [col for col in features_data.columns if col not in data.columns]
        print(f"📊 Новые признаки ({len(new_features)}): {new_features[:10]}...")
        
        return features_data
    except Exception as e:
        print(f"❌ Ошибка создания признаков: {e}")
        return None

def test_single_model_training(data, task="pressure_vector_sign"):
    """Тест обучения одной модели"""
    print(f"\n🤖 Тестируем обучение модели для задачи: {task}")
    
    pipeline = SCHRLevelsAutoMLPipeline()
    
    try:
        # Быстрое обучение для теста
        original_time_limit = pipeline.task_configs[task]['time_limit']
        pipeline.task_configs[task]['time_limit'] = 300  # 5 минут для теста
        
        results = pipeline.train_model(data, task, test_size=0.3)
        
        print(f"✅ Модель обучена успешно!")
        print(f"📊 Метрики: {results['metrics']}")
        
        # Восстанавливаем оригинальный time_limit
        pipeline.task_configs[task]['time_limit'] = original_time_limit
        
        return results
    except Exception as e:
        print(f"❌ Ошибка обучения модели: {e}")
        return None

def test_prediction(data, task="pressure_vector_sign"):
    """Тест предсказания"""
    print(f"\n🔮 Тестируем предсказания для задачи: {task}")
    
    pipeline = SCHRLevelsAutoMLPipeline()
    
    try:
        # Сначала обучаем модель
        results = pipeline.train_model(data, task, test_size=0.3)
        
        if results:
            # Тестируем предсказание на последней записи
            test_data = data.tail(1)
            predictions = pipeline.predict(test_data, task)
            
            print(f"✅ Предсказания получены!")
            print(f"🔮 Предсказание: {predictions.iloc[0]}")
            
            return predictions
    except Exception as e:
        print(f"❌ Ошибка предсказания: {e}")
        return None

def main():
    """Основная функция тестирования"""
    print("🚀 Запускаем тест SCHR Levels AutoML Pipeline")
    print("="*60)
    
    # Тест 1: Загрузка данных
    data = test_data_loading()
    if data is None:
        print("❌ Не удалось загрузить данные. Тест прерван.")
        return
    
    # Тест 2: Создание целевых переменных
    data_with_targets = test_target_creation(data)
    if data_with_targets is None:
        print("❌ Не удалось создать целевые переменные. Тест прерван.")
        return
    
    # Тест 3: Создание признаков
    final_data = test_feature_creation(data_with_targets)
    if final_data is None:
        print("❌ Не удалось создать признаки. Тест прерван.")
        return
    
    # Тест 4: Обучение модели
    model_results = test_single_model_training(final_data, "pressure_vector_sign")
    if model_results is None:
        print("❌ Не удалось обучить модель. Тест прерван.")
        return
    
    # Тест 5: Предсказания
    predictions = test_prediction(final_data, "pressure_vector_sign")
    if predictions is None:
        print("❌ Не удалось получить предсказания. Тест прерван.")
        return
    
    print("\n" + "="*60)
    print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
    print("✅ Пайплайн готов к использованию")
    print("="*60)

if __name__ == "__main__":
    main()
