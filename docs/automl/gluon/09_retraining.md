# Переобучение моделей AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему переобучение критически важно

**Почему 90% ML-моделей теряют точность через 6 месяцев в продакшене?** Потому что мир меняется, а модели остаются статичными. Переобучение - это процесс "обновления знаний" модели, как врач, который изучает новые методы лечения.

### Катастрофические последствия устаревших моделей
- **Netflix рекомендации**: Модель 2010 года не понимала сериалы 2020 года
- **Google Translate**: Устаревшие модели давали неточные переводы новых сленгов
- **Банковские системы**: Модели не распознавали новые виды мошенничества
- **Медицинские диагнозы**: Устаревшие модели пропускали новые симптомы болезней

### Преимущества правильного переобучения
- **Актуальность**: Модель всегда работает с актуальными данными
- **Адаптивность**: Автоматически подстраивается под изменения
- **Конкурентоспособность**: Остается эффективной в динамичной среде
- **Доверие пользователей**: Результаты остаются точными и полезными

## Введение в переобучение

<img src="images/optimized/retraining_workflow.png" alt="Процесс переобучения" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 1: Процесс переобучения моделей AutoML Gluon*

**Почему переобучение - это не просто "обновить модель"?** Это процесс адаптации модели к изменяющемуся миру. Представьте врача, который не изучает новые методы лечения - он станет неэффективным.

**Почему модели "стареют" в продакшене?**
- **Концептуальный дрифт**: Реальность меняется быстрее модели
- **Данные дрифт**: Новые типы данных, которых не было при обучении
- **Пользовательские предпочтения**: Люди меняют поведение и вкусы
- **Технологические изменения**: Новые устройства, платформы, интерфейсы

Переобучение (retraining) - это критически важный процесс для поддержания актуальности ML-моделей в продакшене. В этом разделе рассмотрим все аспекты автоматизированного переобучения моделей.

## Стратегии переобучения

<img src="images/optimized/walk_forward_analysis.png" alt="Стратегии переобучения" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 2: Различные стратегии переобучения моделей*

**Почему важны разные стратегии переобучения?** Потому что разные типы данных и задач требуют разных подходов:

- **Периодическое переобучение**: Регулярные обновления по расписанию
- **Дрифт-триггерное переобучение**: Обновление при обнаружении изменений
- **Инкрементальное переобучение**: Постепенное обновление с новыми данными
- **Полное переобучение**: Полная перестройка модели с нуля
- **Адаптивное переобучение**: Автоматическая адаптация к изменениям
- **Гибридные стратегии**: Комбинация различных подходов

### 1. Периодическое переобучение

**Почему периодическое переобучение - самый простой и надежный подход?** Потому что оно работает по расписанию, как будильник, который напоминает обновить знания. Это как регулярные курсы повышения квалификации для врачей.

**Преимущества периодического переобучения:**
- **Простота**: Легко настроить и поддерживать
- **Надежность**: Регулярные обновления предотвращают деградацию
- **Планируемость**: Можно заранее подготовить ресурсы
- **Контроль качества**: Время на тестирование перед внедрением

**Выбор интервала переобучения:**
- **Ежедневно**: Для быстро меняющихся данных (финансы, новости)
- **Еженедельно**: Для большинства бизнес-задач
- **Ежемесячно**: Для стабильных доменов (медицина, образование)
- **По требованию**: При значительных изменениях в данных

```python
import schedule
import time
from datetime import datetime, timedelta
import pandas as pd
from autogluon.tabular import TabularPredictor
import logging

class PeriodicRetraining:
    """Периодическое переобучение моделей"""
    
    def __init__(self, model_path: str, retraining_interval: int = 7):
        self.model_path = model_path
        self.retraining_interval = retraining_interval  # дни
        self.logger = logging.getLogger(__name__)
    
    def schedule_retraining(self):
        """Планирование переобучения"""
        # Еженедельное переобучение - основной механизм
        schedule.every().week.do(self.retrain_model)
        
        # Ежедневная проверка необходимости переобучения - мониторинг
        schedule.every().day.do(self.check_retraining_need)
        
        # Запуск планировщика - бесконечный цикл
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Проверка каждый час
    
    def retrain_model(self):
        """Переобучение модели - основной процесс обновления"""
        try:
            self.logger.info("Starting model retraining...")
            # Логирование начала процесса для мониторинга
            
            # Загрузка новых данных
            new_data = self.load_new_data()
            
            # Создание новой модели
            predictor = TabularPredictor(
                label='target',
                path=f"{self.model_path}_new"
            )
            
            # Обучение на новых данных
            predictor.fit(new_data, time_limit=3600)
            
            # Валидация новой модели
            if self.validate_new_model(predictor):
                # Замена старой модели
                self.deploy_new_model(predictor)
                self.logger.info("Model retraining completed successfully")
            else:
                self.logger.warning("New model validation failed, keeping old model")
                
        except Exception as e:
            self.logger.error(f"Model retraining failed: {e}")
    
    def check_retraining_need(self):
        """Проверка необходимости переобучения"""
        # Проверка качества текущей модели
        current_performance = self.evaluate_current_model()
        
        # Проверка дрейфа данных
        data_drift = self.check_data_drift()
        
        # Проверка времени последнего переобучения
        last_retraining = self.get_last_retraining_time()
        days_since_retraining = (datetime.now() - last_retraining).days
        
        # Критерии для переобучения
        if (current_performance < 0.8 or 
            data_drift > 0.1 or 
            days_since_retraining >= self.retraining_interval):
            self.logger.info("Retraining needed based on criteria")
            self.retrain_model()
```

### 2. Адаптивное переобучение

<img src="images/optimized/monte_carlo_analysis.png" alt="Адаптивное переобучение" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 3: Адаптивное переобучение и детекция дрейфа данных*

**Почему важно адаптивное переобучение?** Потому что оно реагирует на изменения в реальном времени:

- **Детекция дрейфа**: Автоматическое обнаружение изменений в данных
- **Триггеры переобучения**: Условия для запуска процесса переобучения
- **Мониторинг производительности**: Отслеживание качества модели
- **Статистические тесты**: Проверка значимости изменений
- **Адаптивные пороги**: Динамическая настройка чувствительности
- **Интеграция с мониторингом**: Связь с системами наблюдения

```python
class AdaptiveRetraining:
    """Адаптивное переобучение на основе производительности"""
    
    def __init__(self, model_path: str, performance_threshold: float = 0.8):
        self.model_path = model_path
        self.performance_threshold = performance_threshold
        self.performance_history = []
        self.logger = logging.getLogger(__name__)
    
    def monitor_performance(self, predictions: list, actuals: list):
        """Мониторинг производительности модели"""
        # Расчет текущей производительности
        current_performance = self.calculate_performance(predictions, actuals)
        
        # Добавление в историю
        self.performance_history.append({
            'timestamp': datetime.now(),
            'performance': current_performance
        })
        
        # Проверка тренда производительности
        if self.detect_performance_degradation():
            self.logger.warning("Performance degradation detected")
            self.trigger_retraining()
    
    def detect_performance_degradation(self) -> bool:
        """Обнаружение деградации производительности"""
        if len(self.performance_history) < 10:
            return False
        
        # Анализ тренда за последние 10 измерений
        recent_performance = [p['performance'] for p in self.performance_history[-10:]]
        
        # Проверка снижения производительности
        if (recent_performance[-1] < self.performance_threshold and
            recent_performance[-1] < recent_performance[0]):
            return True
        
        return False
    
    def trigger_retraining(self):
        """Запуск переобучения"""
        self.logger.info("Triggering adaptive retraining...")
        
        # Загрузка данных для переобучения
        retraining_data = self.load_retraining_data()
        
        # Создание и обучение новой модели
        predictor = TabularPredictor(
            label='target',
            path=f"{self.model_path}_adaptive"
        )
        
        predictor.fit(retraining_data, time_limit=3600)
        
        # Валидация и деплой
        if self.validate_new_model(predictor):
            self.deploy_new_model(predictor)
            self.performance_history = []  # Сброс истории
```

### 3. Инкрементальное переобучение

```python
class IncrementalRetraining:
    """Инкрементальное переобучение с сохранением знаний"""
    
    def __init__(self, model_path: str, batch_size: int = 1000):
        self.model_path = model_path
        self.batch_size = batch_size
        self.logger = logging.getLogger(__name__)
    
    def incremental_update(self, new_data: pd.DataFrame):
        """Инкрементальное обновление модели"""
        try:
            # Загрузка текущей модели
            current_predictor = TabularPredictor.load(self.model_path)
            
            # Объединение старых и новых данных
            combined_data = self.combine_data(current_predictor, new_data)
            
            # Обучение на объединенных данных
            updated_predictor = TabularPredictor(
                label='target',
                path=f"{self.model_path}_updated"
            )
            
            updated_predictor.fit(combined_data, time_limit=3600)
            
            # Валидация обновленной модели
            if self.validate_updated_model(updated_predictor):
                self.deploy_updated_model(updated_predictor)
                self.logger.info("Incremental update completed")
            else:
                self.logger.warning("Updated model validation failed")
                
        except Exception as e:
            self.logger.error(f"Incremental update failed: {e}")
    
    def combine_data(self, current_predictor, new_data: pd.DataFrame) -> pd.DataFrame:
        """Объединение старых и новых данных"""
        # Получение старых данных из модели (если доступно)
        old_data = self.extract_old_data(current_predictor)
        
        # Объединение данных
        if old_data is not None:
            combined_data = pd.concat([old_data, new_data], ignore_index=True)
        else:
            combined_data = new_data
        
        return combined_data
```

## Автоматизация переобучения

<img src="images/optimized/advanced_production_flow.png" alt="Автоматизация переобучения" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 4: Система автоматизированного переобучения моделей*

**Почему важна автоматизация переобучения?** Потому что ручное переобучение неэффективно и подвержено ошибкам:

- **Автоматические триггеры**: Запуск переобучения по условиям
- **Пайплайны CI/CD**: Интеграция с процессами разработки
- **A/B тестирование**: Сравнение старых и новых моделей
- **Откат изменений**: Возможность быстрого возврата к предыдущей версии
- **Мониторинг процесса**: Отслеживание статуса переобучения
- **Уведомления**: Алерты о статусе и результатах

### Система автоматического переобучения

```python
import asyncio
import aiohttp
from typing import Dict, List, Any
import json
from datetime import datetime, timedelta

class AutomatedRetrainingSystem:
    """Система автоматического переобучения"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.retraining_queue = asyncio.Queue()
        self.is_retraining = False
    
    async def start_monitoring(self):
        """Запуск мониторинга системы"""
        tasks = [
            self.monitor_data_quality(),
            self.monitor_model_performance(),
            self.monitor_data_drift(),
            self.process_retraining_queue()
        ]
        
        await asyncio.gather(*tasks)
    
    async def monitor_data_quality(self):
        """Мониторинг качества данных"""
        while True:
            try:
                # Проверка качества новых данных
                data_quality = await self.check_data_quality()
                
                if data_quality['score'] < self.config['data_quality_threshold']:
                    self.logger.warning(f"Data quality issue: {data_quality}")
                    await self.trigger_retraining('data_quality')
                
                await asyncio.sleep(3600)  # Проверка каждый час
                
            except Exception as e:
                self.logger.error(f"Data quality monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def monitor_model_performance(self):
        """Мониторинг производительности модели"""
        while True:
            try:
                # Получение метрик производительности
                performance = await self.get_model_performance()
                
                if performance['accuracy'] < self.config['performance_threshold']:
                    self.logger.warning(f"Performance degradation: {performance}")
                    await self.trigger_retraining('performance')
                
                await asyncio.sleep(1800)  # Проверка каждые 30 минут
                
            except Exception as e:
                self.logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def monitor_data_drift(self):
        """Мониторинг дрейфа данных"""
        while True:
            try:
                # Проверка дрейфа данных
                drift_score = await self.check_data_drift()
                
                if drift_score > self.config['drift_threshold']:
                    self.logger.warning(f"Data drift detected: {drift_score}")
                    await self.trigger_retraining('data_drift')
                
                await asyncio.sleep(7200)  # Проверка каждые 2 часа
                
            except Exception as e:
                self.logger.error(f"Data drift monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def trigger_retraining(self, reason: str):
        """Запуск переобучения"""
        if self.is_retraining:
            self.logger.info("Retraining already in progress")
            return
        
        retraining_request = {
            'timestamp': datetime.now().isoformat(),
            'reason': reason,
            'priority': self.get_retraining_priority(reason)
        }
        
        await self.retraining_queue.put(retraining_request)
        self.logger.info(f"Retraining queued: {retraining_request}")
    
    async def process_retraining_queue(self):
        """Обработка очереди переобучения"""
        while True:
            try:
                # Получение запроса на переобучение
                request = await self.retraining_queue.get()
                
                # Выполнение переобучения
                await self.execute_retraining(request)
                
                self.retraining_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Retraining processing error: {e}")
                await asyncio.sleep(300)
    
    async def execute_retraining(self, request: Dict[str, Any]):
        """Выполнение переобучения"""
        self.is_retraining = True
        
        try:
            self.logger.info(f"Starting retraining: {request}")
            
            # Загрузка данных
            data = await self.load_retraining_data()
            
            # Создание новой модели
            predictor = TabularPredictor(
                label='target',
                path=f"./models/retrained_{request['timestamp']}"
            )
            
            # Обучение
            predictor.fit(data, time_limit=3600)
            
            # Валидация
            if await self.validate_new_model(predictor):
                # Деплой новой модели
                await self.deploy_new_model(predictor)
                self.logger.info("Retraining completed successfully")
            else:
                self.logger.warning("New model validation failed")
            
        except Exception as e:
            self.logger.error(f"Retraining execution failed: {e}")
        finally:
            self.is_retraining = False
```

## Валидация переобученных моделей

### Система валидации

```python
class RetrainingValidator:
    """Валидатор переобученных моделей"""
    
    def __init__(self, validation_config: Dict[str, Any]):
        self.config = validation_config
        self.logger = logging.getLogger(__name__)
    
    async def validate_new_model(self, new_predictor, old_predictor=None) -> bool:
        """Валидация новой модели"""
        try:
            # Загрузка тестовых данных
            test_data = await self.load_test_data()
            
            # Предсказания новой модели
            new_predictions = new_predictor.predict(test_data)
            new_performance = new_predictor.evaluate(test_data)
            
            # Сравнение с старой моделью (если доступна)
            if old_predictor is not None:
                old_predictions = old_predictor.predict(test_data)
                old_performance = old_predictor.evaluate(test_data)
                
                # Проверка улучшения производительности
                if not self.check_performance_improvement(new_performance, old_performance):
                    self.logger.warning("New model doesn't improve performance")
                    return False
            
            # Проверка минимальных требований
            if not self.check_minimum_requirements(new_performance):
                self.logger.warning("New model doesn't meet minimum requirements")
                return False
            
            # Проверка стабильности
            if not self.check_model_stability(new_predictor, test_data):
                self.logger.warning("New model is not stable")
                return False
            
            # Проверка совместимости
            if not self.check_compatibility(new_predictor):
                self.logger.warning("New model is not compatible")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Model validation failed: {e}")
            return False
    
    def check_performance_improvement(self, new_perf: Dict, old_perf: Dict) -> bool:
        """Проверка улучшения производительности"""
        improvement_threshold = self.config.get('improvement_threshold', 0.02)
        
        for metric in self.config['performance_metrics']:
            if metric in new_perf and metric in old_perf:
                improvement = new_perf[metric] - old_perf[metric]
                if improvement < improvement_threshold:
                    return False
        
        return True
    
    def check_minimum_requirements(self, performance: Dict) -> bool:
        """Проверка минимальных требований"""
        for metric, threshold in self.config['minimum_requirements'].items():
            if metric in performance and performance[metric] < threshold:
                return False
        
        return True
    
    def check_model_stability(self, predictor, test_data: pd.DataFrame) -> bool:
        """Проверка стабильности модели"""
        # Множественные предсказания на одних и тех же данных
        predictions = []
        for _ in range(5):
            pred = predictor.predict(test_data)
            predictions.append(pred)
        
        # Проверка согласованности
        consistency = self.calculate_prediction_consistency(predictions)
        return consistency > self.config.get('stability_threshold', 0.95)
    
    def check_compatibility(self, predictor) -> bool:
        """Проверка совместимости модели"""
        # Проверка версии AutoGluon
        if hasattr(predictor, 'version'):
            if predictor.version != self.config.get('required_version'):
                return False
        
        # Проверка формата модели
        if not self.check_model_format(predictor):
            return False
        
        return True
```

## Мониторинг переобучения

<img src="images/optimized/production_architecture.png" alt="Мониторинг переобучения" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 5: Система мониторинга процесса переобучения*

**Почему критически важен мониторинг переобучения?** Потому что процесс переобучения может пойти не так:

- **Мониторинг производительности**: Отслеживание качества новой модели
- **Сравнение моделей**: A/B тестирование старой и новой версий
- **Детекция проблем**: Раннее обнаружение ухудшения качества
- **Метрики дрейфа**: Отслеживание изменений в данных
- **Ресурсное потребление**: Мониторинг использования CPU, памяти, GPU
- **Временные метрики**: Отслеживание времени обучения и инференса

### Система мониторинга

```python
class RetrainingMonitor:
    """Мониторинг процесса переобучения"""
    
    def __init__(self, monitoring_config: Dict[str, Any]):
        self.config = monitoring_config
        self.logger = logging.getLogger(__name__)
        self.metrics = {}
    
    def start_monitoring(self, retraining_process):
        """Запуск мониторинга"""
        # Мониторинг ресурсов
        self.monitor_resources()
        
        # Мониторинг прогресса
        self.monitor_progress(retraining_process)
        
        # Мониторинг качества
        self.monitor_quality(retraining_process)
    
    def monitor_resources(self):
        """Мониторинг системных ресурсов"""
        import psutil
        
        while True:
            try:
                # CPU использование
                cpu_percent = psutil.cpu_percent()
                
                # Память
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                
                # Диск
                disk = psutil.disk_usage('/')
                disk_percent = disk.percent
                
                # Логирование метрик
                self.logger.info(f"Resources - CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%")
                
                # Проверка лимитов
                if cpu_percent > 90:
                    self.logger.warning("High CPU usage detected")
                
                if memory_percent > 90:
                    self.logger.warning("High memory usage detected")
                
                if disk_percent > 90:
                    self.logger.warning("High disk usage detected")
                
                time.sleep(60)  # Проверка каждую минуту
                
            except Exception as e:
                self.logger.error(f"Resource monitoring error: {e}")
                time.sleep(300)
    
    def monitor_progress(self, retraining_process):
        """Мониторинг прогресса переобучения"""
        start_time = datetime.now()
        
        while retraining_process.is_alive():
            elapsed_time = datetime.now() - start_time
            
            # Проверка времени выполнения
            if elapsed_time.total_seconds() > self.config.get('max_retraining_time', 7200):
                self.logger.error("Retraining timeout exceeded")
                retraining_process.terminate()
                break
            
            # Логирование прогресса
            self.logger.info(f"Retraining progress: {elapsed_time}")
            
            time.sleep(300)  # Проверка каждые 5 минут
    
    def monitor_quality(self, retraining_process):
        """Мониторинг качества переобучения"""
        # Мониторинг метрик качества
        quality_metrics = {
            'accuracy': [],
            'precision': [],
            'recall': [],
            'f1_score': []
        }
        
        while retraining_process.is_alive():
            try:
                # Получение текущих метрик
                current_metrics = self.get_current_metrics()
                
                # Добавление в историю
                for metric, value in current_metrics.items():
                    if metric in quality_metrics:
                        quality_metrics[metric].append(value)
                
                # Анализ тренда
                self.analyze_quality_trend(quality_metrics)
                
                time.sleep(600)  # Проверка каждые 10 минут
                
            except Exception as e:
                self.logger.error(f"Quality monitoring error: {e}")
                time.sleep(300)
```

## Откат моделей

### Система отката

```python
class ModelRollback:
    """Система отката моделей"""
    
    def __init__(self, rollback_config: Dict[str, Any]):
        self.config = rollback_config
        self.logger = logging.getLogger(__name__)
        self.model_versions = []
    
    def create_backup(self, model_path: str):
        """Создание резервной копии модели"""
        backup_path = f"{model_path}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Копирование модели
            import shutil
            shutil.copytree(model_path, backup_path)
            
            # Сохранение информации о версии
            version_info = {
                'timestamp': datetime.now().isoformat(),
                'path': backup_path,
                'original_path': model_path
            }
            
            self.model_versions.append(version_info)
            
            self.logger.info(f"Model backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Backup creation failed: {e}")
            return None
    
    def rollback_model(self, target_version: str = None):
        """Откат к предыдущей версии модели"""
        try:
            if target_version is None:
                # Откат к последней версии
                if len(self.model_versions) < 2:
                    self.logger.warning("No previous version available for rollback")
                    return False
                
                target_version = self.model_versions[-2]['path']
            else:
                # Откат к указанной версии
                target_version = self.find_version_path(target_version)
                if target_version is None:
                    self.logger.error(f"Version {target_version} not found")
                    return False
            
            # Восстановление модели
            current_path = self.config['current_model_path']
            backup_path = self.config['backup_model_path']
            
            # Создание резервной копии текущей модели
            self.create_backup(current_path)
            
            # Восстановление из резервной копии
            import shutil
            shutil.copytree(target_version, current_path, dirs_exist_ok=True)
            
            self.logger.info(f"Model rolled back to: {target_version}")
            return True
            
        except Exception as e:
            self.logger.error(f"Model rollback failed: {e}")
            return False
    
    def find_version_path(self, version_id: str) -> str:
        """Поиск пути к версии модели"""
        for version in self.model_versions:
            if version_id in version['path']:
                return version['path']
        return None
```

## Примеры использования

### Полный пример системы переобучения

```python
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from autogluon.tabular import TabularPredictor

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompleteRetrainingSystem:
    """Полная система переобучения"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.current_model = None
        self.retraining_history = []
    
    async def initialize(self):
        """Инициализация системы"""
        # Загрузка текущей модели
        self.current_model = TabularPredictor.load(self.config['model_path'])
        
        # Запуск мониторинга
        await self.start_monitoring()
    
    async def start_monitoring(self):
        """Запуск мониторинга"""
        tasks = [
            self.monitor_performance(),
            self.monitor_data_drift(),
            self.monitor_schedule()
        ]
        
        await asyncio.gather(*tasks)
    
    async def monitor_performance(self):
        """Мониторинг производительности"""
        while True:
            try:
                # Получение метрик производительности
                performance = await self.get_current_performance()
                
                # Проверка деградации
                if performance['accuracy'] < self.config['performance_threshold']:
                    self.logger.warning(f"Performance degradation detected: {performance}")
                    await self.trigger_retraining('performance_degradation')
                
                await asyncio.sleep(1800)  # Проверка каждые 30 минут
                
            except Exception as e:
                self.logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def monitor_data_drift(self):
        """Мониторинг дрейфа данных"""
        while True:
            try:
                # Проверка дрейфа данных
                drift_score = await self.check_data_drift()
                
                if drift_score > self.config['drift_threshold']:
                    self.logger.warning(f"Data drift detected: {drift_score}")
                    await self.trigger_retraining('data_drift')
                
                await asyncio.sleep(3600)  # Проверка каждый час
                
            except Exception as e:
                self.logger.error(f"Data drift monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def monitor_schedule(self):
        """Мониторинг расписания"""
        while True:
            try:
                # Проверка времени последнего переобучения
                last_retraining = self.get_last_retraining_time()
                days_since_retraining = (datetime.now() - last_retraining).days
                
                if days_since_retraining >= self.config['retraining_interval']:
                    self.logger.info("Scheduled retraining triggered")
                    await self.trigger_retraining('scheduled')
                
                await asyncio.sleep(3600)  # Проверка каждый час
                
            except Exception as e:
                self.logger.error(f"Schedule monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def trigger_retraining(self, reason: str):
        """Запуск переобучения"""
        self.logger.info(f"Triggering retraining: {reason}")
        
        try:
            # Создание резервной копии
            backup_path = self.create_model_backup()
            
            # Загрузка новых данных
            new_data = await self.load_new_data()
            
            # Создание новой модели
            new_predictor = TabularPredictor(
                label=self.config['target_column'],
                path=f"{self.config['model_path']}_new"
            )
            
            # Обучение
            new_predictor.fit(new_data, time_limit=3600)
            
            # Валидация
            if await self.validate_new_model(new_predictor):
                # Деплой новой модели
                await self.deploy_new_model(new_predictor)
                
                # Обновление истории
                self.retraining_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'reason': reason,
                    'backup_path': backup_path,
                    'status': 'success'
                })
                
                self.logger.info("Retraining completed successfully")
            else:
                # Откат к предыдущей версии
                self.rollback_model(backup_path)
                
                self.retraining_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'reason': reason,
                    'backup_path': backup_path,
                    'status': 'failed'
                })
                
                self.logger.warning("Retraining failed, rolled back to previous version")
                
        except Exception as e:
            self.logger.error(f"Retraining failed: {e}")
            
            # Откат в случае ошибки
            if 'backup_path' in locals():
                self.rollback_model(backup_path)
    
    async def validate_new_model(self, new_predictor) -> bool:
        """Валидация новой модели"""
        try:
            # Загрузка тестовых данных
            test_data = await self.load_test_data()
            
            # Предсказания новой модели
            new_predictions = new_predictor.predict(test_data)
            new_performance = new_predictor.evaluate(test_data)
            
            # Сравнение с текущей моделью
            current_predictions = self.current_model.predict(test_data)
            current_performance = self.current_model.evaluate(test_data)
            
            # Проверка улучшения
            improvement = new_performance['accuracy'] - current_performance['accuracy']
            
            if improvement < self.config.get('improvement_threshold', 0.01):
                self.logger.warning(f"Insufficient improvement: {improvement}")
                return False
            
            # Проверка минимальных требований
            if new_performance['accuracy'] < self.config.get('minimum_accuracy', 0.8):
                self.logger.warning(f"Accuracy below minimum: {new_performance['accuracy']}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Model validation failed: {e}")
            return False
    
    async def deploy_new_model(self, new_predictor):
        """Деплой новой модели"""
        try:
            # Остановка текущего сервиса
            await self.stop_current_service()
            
            # Замена модели
            import shutil
            shutil.copytree(new_predictor.path, self.config['model_path'], dirs_exist_ok=True)
            
            # Обновление текущей модели
            self.current_model = new_predictor
            
            # Запуск обновленного сервиса
            await self.start_updated_service()
            
            self.logger.info("New model deployed successfully")
            
        except Exception as e:
            self.logger.error(f"Model deployment failed: {e}")
            raise
    
    def create_model_backup(self) -> str:
        """Создание резервной копии модели"""
        backup_path = f"{self.config['model_path']}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        import shutil
        shutil.copytree(self.config['model_path'], backup_path)
        
        return backup_path
    
    def rollback_model(self, backup_path: str):
        """Откат к предыдущей версии"""
        import shutil
        shutil.copytree(backup_path, self.config['model_path'], dirs_exist_ok=True)
        
        # Обновление текущей модели
        self.current_model = TabularPredictor.load(self.config['model_path'])
        
        self.logger.info(f"Model rolled back to: {backup_path}")

# Конфигурация системы
config = {
    'model_path': './production_models',
    'target_column': 'target',
    'performance_threshold': 0.8,
    'drift_threshold': 0.1,
    'retraining_interval': 7,  # дни
    'improvement_threshold': 0.01,
    'minimum_accuracy': 0.8
}

# Запуск системы
async def main():
    system = CompleteRetrainingSystem(config)
    await system.initialize()

if __name__ == "__main__":
    asyncio.run(main())
```

## Лучшие практики переобучения

<img src="images/optimized/robustness_analysis.png" alt="Лучшие практики переобучения" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 6: Лучшие практики и рекомендации для переобучения моделей*

**Почему важны лучшие практики переобучения?** Потому что неправильное переобучение может ухудшить качество модели:

- **Планирование**: Тщательное планирование стратегии переобучения
- **Тестирование**: Комплексное тестирование новых моделей
- **Валидация**: Проверка качества на независимых данных
- **Документация**: Подробная документация процесса
- **Версионирование**: Контроль версий моделей и данных
- **Откат**: Возможность быстрого возврата к предыдущей версии
- **Мониторинг**: Непрерывное отслеживание качества

### 🎯 Ключевые принципы успешного переобучения

**Почему следуют лучшим практикам?** Потому что они проверены опытом и помогают избежать проблем:

- **Принцип "Постепенности"**: Постепенное внедрение изменений
- **Принцип "Валидации"**: Обязательная проверка качества
- **Принцип "Отката"**: Возможность быстрого возврата
- **Принцип "Мониторинга"**: Непрерывное наблюдение за процессом
- **Принцип "Документации"**: Подробная фиксация всех изменений
- **Принцип "Тестирования"**: Комплексная проверка перед внедрением

## Следующие шаги

После освоения переобучения моделей переходите к:
- [Лучшим практикам](./08_best_practices.md)
- [Примерам использования](./09_examples.md)
- [Troubleshooting](./10_troubleshooting.md)
