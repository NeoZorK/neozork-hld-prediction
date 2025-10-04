# Руководство по изучению учебника

**Автор:** NeoZorK (Shcherbyna Rostyslav)  
**Дата:** 2025  
**Местоположение:** Ukraine, Zaporizhzhya  
**Версия:** 1.0  

## Почему руководство по изучению критически важно

**Почему 90% людей бросают изучение ML, не имея четкого плана?** Потому что они пытаются изучить все сразу, не понимая, с чего начать и как двигаться дальше. Это как попытка построить дом без чертежей.

### Проблемы без руководства по изучению
- **Перегрузка информацией**: Пытаются изучить все сразу
- **Неправильная последовательность**: Изучают сложное до простого
- **Отсутствие практики**: Только теория без применения
- **Потеря мотивации**: Не видят прогресса

### Преимущества правильного руководства
- **Поэтапное изучение**: От простого к сложному
- **Практическая направленность**: Теория сразу применяется
- **Измеримый прогресс**: Видят результаты на каждом этапе
- **Мотивация**: Постоянное чувство достижения

## Введение

**Почему руководство по изучению - это карта к успеху?** Потому что оно показывает оптимальный путь изучения, учитывая ваш уровень подготовки и цели.

Это руководство поможет вам максимально эффективно изучить учебник AutoML Gluon в зависимости от вашего уровня подготовки и целей.

## Для новичков (0-6 месяцев опыта)

**Почему новичкам нужен особый подход?** Потому что они еще не понимают основ ML и могут легко запутаться в сложных концепциях. Нужен пошаговый подход с быстрыми результатами.

### 🗺️ Путь обучения для новичков

```mermaid
graph TD
    A[Начало изучения] --> B{Выбор пути}
    B -->|Быстрый старт| C[1-2 недели]
    B -->|Полное изучение| D[1-2 месяца]
    
    C --> C1[День 1-2: Основы]
    C --> C2[День 3-4: Понимание]
    C --> C3[День 5-7: Валидация]
    C --> C4[День 8-10: Продакшен]
    C --> C5[День 11-14: Углубление]
    
    D --> D1[Неделя 1: Основы]
    D --> D2[Неделя 2: Оценка и валидация]
    D --> D3[Неделя 3: Продакшен]
    D --> D4[Неделя 4: Продвинутые темы]
    
    C1 --> E[Первый пример]
    C2 --> F[Создание модели]
    C3 --> G[Валидация модели]
    C4 --> H[Деплой в продакшен]
    C5 --> I[Система с переобучением]
    
    D1 --> J[3-5 простых моделей]
    D2 --> K[Полная валидация]
    D3 --> L[Продакшен система]
    D4 --> M[Реальная задача]
    
    E --> N[Успех!]
    F --> N
    G --> N
    H --> N
    I --> N
    J --> N
    K --> N
    L --> N
    M --> N
```

### 🚀 Быстрый старт (1-2 недели)

**Почему быстрый старт критически важен для новичков?** Потому что они должны увидеть результаты как можно быстрее, чтобы не потерять мотивацию.

**Цель:** Запустить первый пример как можно быстрее

#### День 1-2: Основы

**Время:** 2-3 часа в день  
**Фокус:** Установка и первый запуск

1. **Раздел 1** - Введение и установка
   - **Параметры установки:**
     - `pip install autogluon.tabular[all]` - полная установка
     - `pip install autogluon.tabular` - минимальная установка
     - `conda install -c conda-forge autogluon` - через conda
   - **Системные требования:**
     - Python 3.8+
     - RAM: минимум 4GB, рекомендуется 8GB+
     - CPU: 2+ ядра
     - Диск: 2GB свободного места

2. **Раздел 2** - Базовое использование
   - **Ключевые параметры TabularPredictor:**
     - `label`: Целевая переменная (обязательно)
     - `problem_type`: 'binary', 'multiclass', 'regression'
     - `eval_metric`: 'accuracy', 'f1', 'roc_auc', 'log_loss'
     - `path`: Путь для сохранения модели
     - `verbosity`: Уровень вывода (0-4)

3. **Практика:** Установите AutoML Gluon и запустите первый пример
   ```python
   # Минимальный пример с параметрами
   from autogluon.tabular import TabularPredictor
   import pandas as pd
   
   # Параметры для быстрого старта
   predictor = TabularPredictor(
       label='target',
       problem_type='binary',
       eval_metric='accuracy',
       path='quickstart_model',
       verbosity=2
   )
   ```

#### День 3-4: Понимание

**Время:** 2-3 часа в день  
**Фокус:** Понимание параметров и создание модели

4. **Раздел 3** - Продвинутая конфигурация
   - **Параметры обучения:**
     - `time_limit`: Лимит времени (секунды)
     - `presets`: 'best_quality', 'high_quality', 'medium_quality'
     - `num_trials`: Количество попыток hyperparameter tuning
     - `holdout_frac`: Доля данных для holdout валидации

5. **Раздел 4** - Метрики и оценка качества
   - **Доступные метрики:**
     - Классификация: 'accuracy', 'f1', 'roc_auc', 'log_loss'
     - Регрессия: 'rmse', 'mae', 'r2', 'pearsonr'
   - **Параметры оценки:**
     - `silent=True/False`: Тихий режим
     - `auxiliary_metrics=True/False`: Дополнительные метрики

6. **Практика:** Создайте свою первую модель
   ```python
   # Расширенный пример с параметрами
   predictor.fit(
       data,
       time_limit=300,              # 5 минут
       presets='medium_quality',    # Среднее качество
       num_trials=10,               # 10 попыток
       holdout_frac=0.2,            # 20% для валидации
       verbosity=2
   )
   ```

#### День 5-7: Валидация

**Время:** 2-3 часа в день  
**Фокус:** Валидация и оценка качества

7. **Раздел 5** - Валидация моделей
   - **Параметры валидации:**
     - `num_bag_folds`: Количество фолдов для бэггинга
     - `num_stack_levels`: Уровни стекинга
     - `auto_stack`: Автоматический стекинг
     - `refit_full`: Переобучение на всех данных

8. **Раздел 8** - Лучшие практики
   - **Параметры качества:**
     - `feature_prune`: Отбор признаков
     - `excluded_model_types`: Исключенные типы моделей
     - `included_model_types`: Включенные типы моделей

9. **Практика:** Проведите валидацию своей модели
   ```python
   # Валидация с параметрами
   predictor.fit(
       data,
       time_limit=600,              # 10 минут
       presets='high_quality',      # Высокое качество
       num_bag_folds=5,             # 5-fold бэггинг
       num_stack_levels=1,          # 1 уровень стекинга
       auto_stack=True,             # Автоматический стекинг
       refit_full=True,             # Переобучение
       feature_prune=True           # Отбор признаков
   )
   ```

#### День 8-10: Продакшен

**Время:** 3-4 часа в день  
**Фокус:** Деплой в продакшен

10. **Раздел 6** - Продакшен и деплой
    - **Параметры продакшена:**
      - `presets='optimize_for_deployment'`: Оптимизация для деплоя
      - `save_space=True`: Экономия места
      - `keep_only_best=True`: Только лучшая модель

11. **Раздел 12** - Простой пример продакшена
    - **API параметры:**
      - `HOST`: Хост сервера
      - `PORT`: Порт сервера
      - `DEBUG`: Режим отладки
      - `MAX_BATCH_SIZE`: Максимальный размер батча

12. **Практика:** Задеплойте модель в продакшен
    ```python
    # Продакшен конфигурация
    predictor.fit(
        data,
        presets='optimize_for_deployment',
        save_space=True,
        keep_only_best=True,
        time_limit=1200
    )
    ```

#### День 11-14: Углубление

**Время:** 2-3 часа в день  
**Фокус:** Переобучение и продвинутые техники

13. **Раздел 7** - Переобучение моделей
    - **Параметры переобучения:**
      - `retrain_frequency`: Частота переобучения
      - `drift_detection_window`: Окно обнаружения дрифта
      - `performance_threshold`: Порог производительности

14. **Раздел 9** - Примеры использования
    - **Специализированные параметры:**
      - Для временных рядов: `time_limit` увеличен
      - Для больших данных: `num_cpus`, `memory_limit`
      - Для GPU: `num_gpus`

15. **Практика:** Создайте систему с переобучением
    ```python
    # Система переобучения
    class RetrainingSystem:
        def __init__(self, retrain_frequency=1000):
            self.retrain_frequency = retrain_frequency
            self.performance_threshold = 0.8
        
        def should_retrain(self, performance):
            return performance < self.performance_threshold
    ```

### 📚 Полное изучение (1-2 месяца)

**Цель:** Полное понимание AutoML Gluon

### 📊 Метрики прогресса обучения

```mermaid
graph LR
    A[Уровень 0<br/>Новичок] --> B[Уровень 1<br/>Основы]
    B --> C[Уровень 2<br/>Практика]
    C --> D[Уровень 3<br/>Продакшен]
    D --> E[Уровень 4<br/>Эксперт]
    
    A1[0% понимания<br/>0 моделей<br/>0 проектов] --> A
    B1[20% понимания<br/>1-3 модели<br/>1 простой проект] --> B
    C1[50% понимания<br/>5-10 моделей<br/>2-3 проекта] --> C
    D1[80% понимания<br/>10+ моделей<br/>Продакшен система] --> D
    E1[100% понимания<br/>Сложные системы<br/>Супер-система] --> E
    
    style A fill:#ffcccc
    style B fill:#ffffcc
    style C fill:#ccffcc
    style D fill:#ccccff
    style E fill:#ffccff
```

#### Неделя 1: Основы
1. **Раздел 1** - Введение и установка
2. **Раздел 2** - Базовое использование
3. **Раздел 3** - Продвинутая конфигурация
4. **Практика:** Создайте 3-5 простых моделей

#### Неделя 2: Оценка и валидация
5. **Раздел 4** - Метрики и оценка качества
6. **Раздел 5** - Валидация моделей
7. **Раздел 8** - Лучшие практики
8. **Практика:** Проведите полную валидацию

#### Неделя 3: Продакшен
9. **Раздел 6** - Продакшен и деплой
10. **Раздел 7** - Переобучение моделей
11. **Раздел 12** - Простой пример продакшена
12. **Практика:** Создайте продакшен систему

#### Неделя 4: Продвинутые темы
13. **Раздел 9** - Примеры использования
14. **Раздел 10** - Troubleshooting
15. **Раздел 13** - Сложный пример продакшена
16. **Практика:** Решите реальную задачу

## Для продвинутых пользователей (6+ месяцев опыта)

### 🎯 Путь для продвинутых пользователей

```mermaid
graph TD
    A[Продвинутый пользователь] --> B{Выбор стратегии}
    B -->|Быстрый деплой| C[Фокус на продакшене<br/>1 неделя]
    B -->|Глубокое изучение| D[Углубленное изучение<br/>2-3 недели]
    
    C --> C1[День 1-2: Архитектура]
    C --> C2[День 3-4: Валидация]
    C --> C3[День 5-7: Деплой]
    
    D --> D1[Неделя 1: Теория и основы]
    D --> D2[Неделя 2: Специализированные индикаторы]
    D --> D3[Неделя 3: Супер-система]
    
    C1 --> E1[Архитектура системы]
    C2 --> E2[Комплексная валидация]
    C3 --> E3[Продакшен система]
    
    D1 --> F1[Продвинутые техники]
    D2 --> F2[Модели для индикаторов]
    D3 --> F3[Супер-система]
    
    E1 --> G[Успех!]
    E2 --> G
    E3 --> G
    F1 --> G
    F2 --> G
    F3 --> G
```

### 🎯 Фокус на продакшене (1 неделя)

**Цель:** Создать робастную продакшен систему

#### День 1-2: Архитектура
1. **Раздел 6** - Продакшен и деплой
2. **Раздел 12** - Простой пример продакшена
3. **Раздел 13** - Сложный пример продакшена
4. **Практика:** Спроектируйте архитектуру системы

#### День 3-4: Валидация
5. **Раздел 5** - Валидация моделей
6. **Раздел 8** - Лучшие практики
7. **Практика:** Проведите комплексную валидацию

#### День 5-7: Деплой
8. **Раздел 7** - Переобучение моделей
9. **Раздел 9** - Примеры использования
10. **Практика:** Задеплойте систему в продакшен

### 🔬 Углубленное изучение (2-3 недели)

**Цель:** Стать экспертом в AutoML Gluon

#### Неделя 1: Теория и основы
1. **Раздел 14** - Теория и основы AutoML
2. **Раздел 15** - Интерпретируемость и объяснимость
3. **Раздел 16** - Продвинутые темы
4. **Практика:** Реализуйте продвинутые техники

#### Неделя 2: Специализированные индикаторы
5. **Раздел 19** - WAVE2 Индикатор
6. **Раздел 20** - SCHR Levels
7. **Раздел 21** - SCHR SHORT3
8. **Практика:** Создайте модели для каждого индикатора

#### Неделя 3: Супер-система
9. **Раздел 22** - Супер-система
10. **Раздел 17** - Этика и ответственный AI
11. **Раздел 18** - Кейс-стади
12. **Практика:** Создайте супер-систему

## Для экспертов (2+ года опыта)

### 🚀 Максимальная эффективность (3-5 дней)

**Цель:** Быстро освоить новые техники

#### День 1: Обзор
1. **Раздел 1** - Введение и установка (быстро)
2. **Раздел 14** - Теория и основы AutoML
3. **Раздел 16** - Продвинутые темы
4. **Практика:** Оцените новые возможности

#### День 2: Специализированные техники
5. **Раздел 19** - WAVE2 Индикатор
6. **Раздел 20** - SCHR Levels
7. **Раздел 21** - SCHR SHORT3
8. **Практика:** Протестируйте новые индикаторы

#### День 3: Супер-система
9. **Раздел 22** - Супер-система
10. **Раздел 18** - Кейс-стади (выборочно)
11. **Практика:** Создайте прототип супер-системы

#### День 4-5: Деплой и оптимизация
12. **Раздел 6** - Продакшен и деплой
13. **Раздел 7** - Переобучение моделей
14. **Практика:** Задеплойте и оптимизируйте систему

## Специализированные пути изучения

### 🎯 Карта специализированных путей

```mermaid
graph TD
    A[Выбор специализации] --> B{Тип специалиста}
    
    B -->|Аналитик данных| C[📊 Аналитик данных]
    B -->|ML-инженер| D[🤖 ML-инженер]
    B -->|Трейдер| E[💰 Трейдер]
    B -->|Бизнес-аналитик| F[🏢 Бизнес-аналитик]
    
    C --> C1[Фокус: Понимание данных и метрик]
    C --> C2[Разделы: 1,2,4,5,15,8]
    C --> C3[Результат: Эксперт по анализу]
    
    D --> D1[Фокус: Продакшен и деплой]
    D --> D2[Разделы: 1,2,6,7,12,13,22]
    D --> D3[Результат: ML-системы в продакшене]
    
    E --> E1[Фокус: Торговые системы]
    E --> E2[Разделы: 1,2,19,20,21,22,18]
    E --> E3[Результат: Торговая супер-система]
    
    F --> F1[Фокус: Бизнес-применения]
    F --> F2[Разделы: 1,2,4,18,17,8]
    F --> F3[Результат: Бизнес-решения на AI]
    
    style C fill:#e1f5fe
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fff3e0
```

### 📊 Для аналитиков данных

**Фокус:** Понимание данных и метрик  
**Время:** 2-3 недели  
**Ключевые навыки:** Анализ данных, интерпретация результатов, выбор метрик

#### Параметры для аналитиков данных

1. **Раздел 1** - Введение и установка
   - **Параметры установки:**
     - `pip install autogluon.tabular[all]` - полная установка с визуализацией
     - `pip install matplotlib seaborn plotly` - дополнительные библиотеки визуализации
   - **Системные требования:**
     - RAM: 8GB+ (для больших датасетов)
     - Диск: 5GB+ (для данных и моделей)

2. **Раздел 2** - Базовое использование
   - **Ключевые параметры для анализа:**
     ```python
     predictor = TabularPredictor(
         label='target',
         problem_type='binary',
         eval_metric='roc_auc',        # ROC-AUC для анализа
         path='analysis_model',
         verbosity=3,                  # Подробный вывод
         presets='best_quality'        # Лучшее качество для анализа
     )
     ```

3. **Раздел 4** - Метрики и оценка качества
   - **Параметры метрик для анализа:**
     - `eval_metric`: 'roc_auc', 'f1', 'precision', 'recall'
     - `auxiliary_metrics=True`: Дополнительные метрики
     - `silent=False`: Подробный вывод метрик
   - **Анализ производительности:**
     ```python
     # Детальная оценка с параметрами
     performance = predictor.evaluate(
         test_data,
         silent=False,
         auxiliary_metrics=True,
         detailed_report=True
     )
     ```

4. **Раздел 5** - Валидация моделей
   - **Параметры валидации для анализа:**
     - `num_bag_folds=10`: Больше фолдов для стабильности
     - `holdout_frac=0.3`: Больше данных для валидации
     - `auto_stack=True`: Автоматический стекинг
   - **Кросс-валидация:**
     ```python
     predictor.fit(
         data,
         num_bag_folds=10,             # 10-fold CV
         holdout_frac=0.3,             # 30% для holdout
         auto_stack=True,              # Стекинг
         refit_full=True               # Переобучение
     )
     ```

5. **Раздел 15** - Интерпретируемость и объяснимость
   - **Параметры интерпретации:**
     - `feature_importance=True`: Важность признаков
     - `permutation_importance=True`: Перестановочная важность
     - `shap_values=True`: SHAP значения
   - **Анализ важности:**
     ```python
     # Важность признаков
     importance = predictor.feature_importance(data)
     
     # SHAP значения
     explainer = predictor.get_explainer()
     shap_values = explainer.shap_values(data)
     ```

6. **Раздел 8** - Лучшие практики
   - **Параметры качества для анализа:**
     - `feature_prune=True`: Отбор признаков
     - `excluded_model_types=['KNN']`: Исключение медленных моделей
     - `included_model_types=['RF', 'GBM', 'XGB']`: Включение интерпретируемых моделей

### 🤖 Для ML-инженеров

**Фокус:** Продакшен и деплой  
**Время:** 2-3 недели  
**Ключевые навыки:** Деплой, мониторинг, масштабирование, DevOps

#### Параметры для ML-инженеров

1. **Раздел 1** - Введение и установка
   - **Параметры установки для продакшена:**
     - `pip install autogluon.tabular[all]` - полная установка
     - `pip install gunicorn uwsgi` - WSGI серверы
     - `pip install docker kubernetes` - контейнеризация
   - **Системные требования:**
     - RAM: 16GB+ (для продакшена)
     - CPU: 8+ ядер
     - Диск: 20GB+ (для моделей и логов)

2. **Раздел 2** - Базовое использование
   - **Параметры для продакшена:**
     ```python
     predictor = TabularPredictor(
         label='target',
         problem_type='binary',
         eval_metric='accuracy',
         path='production_model',
         verbosity=1,                  # Минимальный вывод в продакшене
         presets='optimize_for_deployment'  # Оптимизация для деплоя
     )
     ```

3. **Раздел 6** - Продакшен и деплой
   - **Параметры оптимизации:**
     - `presets='optimize_for_deployment'`: Оптимизация для деплоя
     - `save_space=True`: Экономия места
     - `keep_only_best=True`: Только лучшая модель
     - `refit_full=False`: Отключение переобучения
   - **Конфигурация для продакшена:**
     ```python
     predictor.fit(
         data,
         presets='optimize_for_deployment',
         save_space=True,
         keep_only_best=True,
         refit_full=False,
         time_limit=3600,              # 1 час максимум
         num_trials=50,                # Больше попыток
         hyperparameter_tune_kwargs={
             'scheduler': 'local',
             'searcher': 'bayes',
             'num_trials': 50
         }
     )
     ```

4. **Раздел 7** - Переобучение моделей
   - **Параметры переобучения:**
     - `retrain_frequency=1000`: Частота переобучения
     - `drift_detection_window=200`: Окно обнаружения дрифта
     - `performance_threshold=0.8`: Порог производительности
     - `adaptation_rate=0.1`: Скорость адаптации
   - **Система переобучения:**
     ```python
     class ProductionRetrainingSystem:
         def __init__(self):
             self.retrain_frequency = 1000
             self.drift_threshold = 0.1
             self.performance_threshold = 0.8
             self.adaptation_rate = 0.1
         
         def should_retrain(self, performance, drift_score):
             return (performance < self.performance_threshold or 
                     drift_score > self.drift_threshold)
     ```

5. **Раздел 12** - Простой пример продакшена
   - **API параметры:**
     - `HOST='0.0.0.0'`: Привязка ко всем интерфейсам
     - `PORT=5000`: Порт сервера
     - `DEBUG=False`: Отключение debug в продакшене
     - `MAX_BATCH_SIZE=1000`: Максимальный размер батча
     - `REQUEST_TIMEOUT=30`: Таймаут запроса
   - **Конфигурация API:**
     ```python
     class ProductionConfig:
         HOST = '0.0.0.0'
         PORT = 5000
         DEBUG = False
         MAX_BATCH_SIZE = 1000
         REQUEST_TIMEOUT = 30
         API_KEY = os.getenv('API_KEY')
         RATE_LIMIT = 100
         ENABLE_METRICS = True
     ```

6. **Раздел 13** - Сложный пример продакшена
   - **Параметры масштабирования:**
     - `num_workers=4`: Количество воркеров
     - `max_connections=1000`: Максимальные соединения
     - `memory_limit='2GB'`: Лимит памяти
     - `cpu_limit=2`: Лимит CPU
   - **Docker конфигурация:**
     ```dockerfile
     FROM python:3.9-slim
     WORKDIR /app
     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt
     COPY . .
     EXPOSE 5000
     CMD ["gunicorn", "--bind", "0.0.0.0:5000", 
          "--workers", "4", "--timeout", "30", "app:app"]
     ```

7. **Раздел 22** - Супер-система
   - **Параметры супер-системы:**
     - `ensemble_methods=['adaptive', 'context', 'temporal']`
     - `weight_update_frequency=100`
     - `confidence_threshold=0.7`
     - `min_models_agreement=2`
   - **Конфигурация супер-системы:**
     ```python
     super_system_config = {
         'ensemble_methods': ['adaptive', 'context', 'temporal'],
         'weight_update_frequency': 100,
         'confidence_threshold': 0.7,
         'min_models_agreement': 2,
         'performance_window': 500,
         'context_sensitivity': 0.8
     }
     ```

### 💰 Для трейдеров

**Фокус:** Торговые системы  
**Время:** 3-4 недели  
**Ключевые навыки:** Торговые индикаторы, риск-менеджмент, автоматизация торговли

#### Параметры для трейдеров

1. **Раздел 1** - Введение и установка
   - **Параметры установки для торговли:**
     - `pip install autogluon.tabular[all]` - полная установка
     - `pip install yfinance ccxt` - данные с бирж
     - `pip install ta-lib` - технические индикаторы
   - **Системные требования:**
     - RAM: 16GB+ (для обработки больших объемов данных)
     - CPU: 8+ ядер (для быстрых вычислений)
     - Диск: 50GB+ (для исторических данных)

2. **Раздел 2** - Базовое использование
   - **Параметры для торговых систем:**
     ```python
     predictor = TabularPredictor(
         label='target',
         problem_type='binary',        # Покупка/продажа
         eval_metric='f1',            # F1 для торговли
         path='trading_model',
         verbosity=2,
         presets='best_quality'       # Лучшее качество критично
     )
     ```

3. **Раздел 19** - WAVE2 Индикатор
   - **Параметры WAVE2:**
     - `min_wave_length=5`: Минимальная длина волны
     - `max_wave_length=50`: Максимальная длина волны
     - `amplitude_threshold=0.02`: Порог амплитуды (2%)
     - `frequency_threshold=0.1`: Порог частоты
     - `phase_threshold=0.3`: Порог фазы
   - **Конфигурация WAVE2:**
     ```python
     wave2_config = {
         'min_wave_length': 5,
         'max_wave_length': 50,
         'amplitude_threshold': 0.02,
         'frequency_threshold': 0.1,
         'phase_threshold': 0.3,
         'signal_threshold': 0.6,
         'risk_reward_ratio': 2.0
     }
     ```

4. **Раздел 20** - SCHR Levels
   - **Параметры SCHR Levels:**
     - `lookback_period=50`: Период анализа уровней
     - `min_touches=3`: Минимальные касания
     - `tolerance=0.001`: Допуск (0.1%)
     - `pressure_threshold=0.7`: Порог давления
     - `breakout_threshold=0.8`: Порог пробоя
   - **Конфигурация SCHR Levels:**
     ```python
     schr_config = {
         'lookback_period': 50,
         'min_touches': 3,
         'tolerance': 0.001,
         'pressure_threshold': 0.7,
         'breakout_threshold': 0.8,
         'volume_weight': 0.3,
         'volume_confirmation': True
     }
     ```

5. **Раздел 21** - SCHR SHORT3
   - **Параметры SCHR SHORT3:**
     - `short_period=3`: Краткосрочный период
     - `volatility_window=10`: Окно волатильности
     - `momentum_threshold=0.5`: Порог момента
     - `volatility_threshold=0.02`: Порог волатильности (2%)
     - `signal_strength=0.6`: Сила сигнала
   - **Конфигурация SCHR SHORT3:**
     ```python
     short3_config = {
         'short_period': 3,
         'volatility_window': 10,
         'momentum_threshold': 0.5,
         'volatility_threshold': 0.02,
         'signal_strength': 0.6,
         'pattern_types': ['candlestick', 'price_action'],
         'min_pattern_strength': 0.7
     }
     ```

6. **Раздел 22** - Супер-система
   - **Параметры супер-системы для торговли:**
     - `ensemble_methods=['adaptive', 'context', 'temporal']`
     - `weight_update_frequency=50`: Частое обновление весов
     - `confidence_threshold=0.8`: Высокий порог уверенности
     - `min_models_agreement=2`: Минимум 2 согласных модели
   - **Торговая конфигурация:**
     ```python
     trading_system_config = {
         'ensemble_methods': ['adaptive', 'context', 'temporal'],
         'weight_update_frequency': 50,
         'confidence_threshold': 0.8,
         'min_models_agreement': 2,
         'risk_management': {
             'max_position_size': 0.1,      # 10% капитала
             'stop_loss_threshold': 0.02,   # 2% стоп-лосс
             'take_profit_threshold': 0.04, # 4% тейк-профит
             'max_drawdown': 0.05          # 5% максимальная просадка
         },
         'trading_hours': {
             'start': '09:00',
             'end': '17:00',
             'timezone': 'UTC'
         }
     }
     ```

7. **Раздел 18** - Кейс-стади (криптотрейдинг)
   - **Параметры для криптотрейдинга:**
     - `timeframe='1h'`: Таймфрейм (1 час)
     - `lookback_days=365`: Год исторических данных
     - `volatility_adjustment=True`: Корректировка по волатильности
     - `market_hours_24_7=True`: Круглосуточная торговля
   - **Крипто конфигурация:**
     ```python
     crypto_config = {
         'timeframe': '1h',
         'lookback_days': 365,
         'volatility_adjustment': True,
         'market_hours_24_7': True,
         'exchanges': ['binance', 'coinbase', 'kraken'],
         'pairs': ['BTC/USDT', 'ETH/USDT', 'ADA/USDT'],
         'risk_management': {
             'max_position_size': 0.05,     # 5% для крипто
             'stop_loss_threshold': 0.03,   # 3% стоп-лосс
             'take_profit_threshold': 0.06, # 6% тейк-профит
             'max_drawdown': 0.03          # 3% максимальная просадка
         }
     }
     ```

### 🏢 Для бизнес-аналитиков

**Фокус:** Бизнес-применения  
**Время:** 2-3 недели  
**Ключевые навыки:** Бизнес-метрики, интерпретация результатов, ROI, этика AI

#### Параметры для бизнес-аналитиков

1. **Раздел 1** - Введение и установка
   - **Параметры установки для бизнеса:**
     - `pip install autogluon.tabular[all]` - полная установка
     - `pip install plotly dash` - интерактивные дашборды
     - `pip install jupyter voila` - презентации
   - **Системные требования:**
     - RAM: 8GB+ (для анализа больших датасетов)
     - CPU: 4+ ядра
     - Диск: 10GB+ (для данных и отчетов)

2. **Раздел 2** - Базовое использование
   - **Параметры для бизнес-анализа:**
     ```python
     predictor = TabularPredictor(
         label='target',
         problem_type='binary',
         eval_metric='roc_auc',        # ROC-AUC для бизнеса
         path='business_model',
         verbosity=2,
         presets='high_quality'        # Высокое качество
     )
     ```

3. **Раздел 4** - Метрики и оценка качества
   - **Бизнес-метрики:**
     - `eval_metric='roc_auc'`: ROC-AUC для классификации
     - `eval_metric='rmse'`: RMSE для регрессии
     - `auxiliary_metrics=True`: Дополнительные метрики
   - **Анализ ROI:**
     ```python
     # Бизнес-метрики
     business_metrics = {
         'roi': 0.15,                  # 15% ROI
         'cost_per_prediction': 0.01,  # $0.01 за предсказание
         'accuracy_threshold': 0.85,   # 85% точность
         'false_positive_cost': 10.0,  # $10 за ложный положительный
         'false_negative_cost': 50.0   # $50 за ложный отрицательный
     }
     ```

4. **Раздел 18** - Кейс-стади
   - **Параметры для кейс-стади:**
     - `time_limit=1800`: 30 минут на обучение
     - `presets='best_quality'`: Лучшее качество
     - `holdout_frac=0.2`: 20% для валидации
     - `feature_prune=True`: Отбор признаков
   - **Конфигурация кейс-стади:**
     ```python
     case_study_config = {
         'time_limit': 1800,
         'presets': 'best_quality',
         'holdout_frac': 0.2,
         'feature_prune': True,
         'business_context': {
             'industry': 'finance',
             'use_case': 'credit_scoring',
             'stakeholders': ['risk_team', 'business_team'],
             'compliance_required': True
         }
     }
     ```

5. **Раздел 17** - Этика и ответственный AI
   - **Параметры этики:**
     - `fairness_metrics=True`: Метрики справедливости
     - `bias_detection=True`: Обнаружение смещений
     - `explainability=True`: Объяснимость решений
     - `privacy_preserving=True`: Сохранение приватности
   - **Этическая конфигурация:**
     ```python
     ethics_config = {
         'fairness_metrics': True,
         'bias_detection': True,
         'explainability': True,
         'privacy_preserving': True,
         'protected_attributes': ['age', 'gender', 'race'],
         'fairness_threshold': 0.8,
         'bias_threshold': 0.1
     }
     ```

6. **Раздел 8** - Лучшие практики
   - **Параметры качества для бизнеса:**
     - `feature_prune=True`: Отбор признаков
     - `excluded_model_types=['KNN']`: Исключение медленных моделей
     - `included_model_types=['RF', 'GBM', 'XGB']`: Интерпретируемые модели
     - `refit_full=True`: Переобучение на всех данных
   - **Бизнес-конфигурация:**
     ```python
     business_config = {
         'feature_prune': True,
         'excluded_model_types': ['KNN', 'NN_TORCH'],
         'included_model_types': ['RF', 'GBM', 'XGB', 'CAT'],
         'refit_full': True,
         'business_requirements': {
             'max_inference_time': 0.1,    # 100ms максимум
             'min_accuracy': 0.85,         # 85% минимум
             'max_model_size': 100,        # 100MB максимум
             'interpretability_required': True
         }
     }
     ```

## Практические рекомендации

### 📝 Ведение заметок

1. **Создайте файл заметок** для каждого раздела
2. **Записывайте код** который вы пробуете
3. **Фиксируйте ошибки** и их решения
4. **Отмечайте важные моменты** для будущего использования

### 🧪 Практические упражнения

### 🔄 Блок-схема практических упражнений

```mermaid
graph TD
    A[Начало практики] --> B[Упражнение 1: Первая модель<br/>30 минут]
    B --> C{Модель работает?}
    C -->|Да| D[Упражнение 2: Валидация<br/>1 час]
    C -->|Нет| E[Исправление ошибок<br/>15 минут]
    E --> B
    
    D --> F{Валидация прошла?}
    F -->|Да| G[Упражнение 3: Продакшен<br/>2 часа]
    F -->|Нет| H[Анализ проблем<br/>30 минут]
    H --> D
    
    G --> I{API работает?}
    I -->|Да| J[Успех!<br/>Готов к реальным задачам]
    I -->|Нет| K[Отладка продакшена<br/>1 час]
    K --> G
    
    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style D fill:#e8f5e8
    style G fill:#fff3e0
    style J fill:#e0f2f1
```

#### Упражнение 1: Первая модель (30 минут)

**Цель:** Создать первую модель AutoML Gluon с пониманием всех параметров

```python
# Создайте простую модель на датасете Iris
from autogluon.tabular import TabularPredictor
import pandas as pd
from sklearn.datasets import load_iris

# Загрузка данных
iris = load_iris()
data = pd.DataFrame(iris.data, columns=iris.feature_names)
data['target'] = iris.target

# Создание модели с детальными параметрами
predictor = TabularPredictor(
    label='target',                    # Целевая переменная (обязательный параметр)
    problem_type='multiclass',         # Тип задачи: 'binary', 'multiclass', 'regression'
    eval_metric='accuracy',            # Метрика оценки: 'accuracy', 'f1', 'roc_auc', 'log_loss'
    path='iris_model',                 # Путь для сохранения модели
    verbosity=2,                       # Уровень вывода: 0-4 (0=тихо, 4=подробно)
    presets='medium_quality_faster_inference'  # Предустановки качества
)

# Обучение модели с параметрами
predictor.fit(
    data,                              # Обучающие данные
    time_limit=60,                     # Лимит времени обучения (секунды)
    presets='medium_quality',          # Качество моделей: 'best_quality', 'high_quality', 'medium_quality', 'optimize_for_deployment'
    num_trials=10,                     # Количество попыток для hyperparameter tuning
    hyperparameter_tune_kwargs={       # Параметры настройки гиперпараметров
        'scheduler': 'local',          # Планировщик: 'local', 'ray'
        'searcher': 'auto',            # Поисковик: 'auto', 'random', 'bayes'
        'num_trials': 10,              # Количество попыток
        'search_space': 'default'      # Пространство поиска
    },
    holdout_frac=0.2,                  # Доля данных для holdout валидации
    num_bag_folds=0,                   # Количество фолдов для бэггинга (0=отключить)
    num_stack_levels=0,                # Количество уровней стекинга (0=отключить)
    auto_stack=True,                   # Автоматический стекинг
    num_gpus=0,                        # Количество GPU для обучения
    num_cpus=None,                     # Количество CPU (None=автоопределение)
    memory_limit=None,                 # Лимит памяти (None=без ограничений)
    feature_prune=True,                # Отбор признаков
    excluded_model_types=[],           # Исключенные типы моделей
    included_model_types=[],           # Включенные типы моделей ([]=все)
    refit_full=True,                   # Переобучение на всех данных
    set_best_to_refit_full=True,       # Установка лучшей модели как refit_full
    save_space=True,                   # Экономия места на диске
    save_bag_folds=True,               # Сохранение бэггинг фолдов
    keep_only_best=True,               # Сохранение только лучшей модели
    num_bag_sets=1,                    # Количество наборов бэггинга
    num_stack_levels=0,                # Количество уровней стекинга
    num_bag_folds=0,                   # Количество фолдов бэггинга
    ag_args_fit={                      # Дополнительные аргументы для fit
        'num_gpus': 0,
        'num_cpus': None,
        'time_limit': 60
    },
    ag_args_ensemble={                 # Аргументы для ансамбля
        'num_gpus': 0,
        'num_cpus': None
    }
)

# Оценка модели
predictions = predictor.predict(data)
print(f"Точность: {predictor.evaluate(data)}")

# Дополнительная информация о модели
print(f"Лучшая модель: {predictor.get_model_best()}")
print(f"Доступные модели: {predictor.get_model_names()}")
print(f"Важность признаков: {predictor.feature_importance(data)}")
```

#### Упражнение 2: Валидация (1 час)

**Цель:** Провести полную валидацию модели с пониманием всех параметров валидации

```python
# Проведите полную валидацию модели
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Разделение данных с параметрами
train_data, test_data = train_test_split(
    data, 
    test_size=0.2,                      # Доля тестовых данных (20%)
    random_state=42,                    # Случайное состояние для воспроизводимости
    stratify=data['target']             # Стратификация по целевой переменной
)

# Создание модели с параметрами валидации
predictor = TabularPredictor(
    label='target',
    problem_type='multiclass',
    eval_metric='accuracy',
    path='iris_validation_model',
    verbosity=2
)

# Обучение с параметрами валидации
predictor.fit(
    train_data,
    time_limit=120,                     # Увеличенное время для лучшего качества
    presets='high_quality',             # Высокое качество для валидации
    holdout_frac=0.2,                   # 20% данных для holdout валидации
    num_bag_folds=5,                    # 5-fold бэггинг для стабильности
    num_stack_levels=1,                 # 1 уровень стекинга
    auto_stack=True,                    # Автоматический стекинг
    num_trials=20,                      # Больше попыток для hyperparameter tuning
    hyperparameter_tune_kwargs={
        'scheduler': 'local',
        'searcher': 'bayes',            # Байесовский поиск для лучших результатов
        'num_trials': 20,
        'search_space': 'default'
    },
    feature_prune=True,                 # Отбор признаков
    refit_full=True,                    # Переобучение на всех данных
    set_best_to_refit_full=True
)

# Валидация на тестовых данных
test_predictions = predictor.predict(test_data)
test_accuracy = predictor.evaluate(test_data, silent=True)

# Детальная оценка производительности
print(f"Точность на тесте: {test_accuracy}")

# Кросс-валидация на обучающих данных
cv_scores = []
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in skf.split(train_data.drop('target', axis=1), train_data['target']):
    cv_train = train_data.iloc[train_idx]
    cv_val = train_data.iloc[val_idx]
    
    # Обучение на фолде
    cv_predictor = TabularPredictor(
        label='target',
        problem_type='multiclass',
        eval_metric='accuracy',
        path=f'cv_model_{len(cv_scores)}',
        verbosity=0
    )
    cv_predictor.fit(cv_train, time_limit=60, presets='medium_quality')
    
    # Оценка на валидационном фолде
    cv_pred = cv_predictor.predict(cv_val)
    cv_acc = cv_predictor.evaluate(cv_val, silent=True)
    cv_scores.append(cv_acc)

print(f"Средняя точность CV: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores)*2:.4f})")

# Детальный отчет о классификации
print("\nОтчет о классификации:")
print(classification_report(test_data['target'], test_predictions))

# Матрица ошибок
print("\nМатрица ошибок:")
print(confusion_matrix(test_data['target'], test_predictions))

# Анализ важности признаков
feature_importance = predictor.feature_importance(test_data)
print(f"\nВажность признаков:")
print(feature_importance)

# Анализ производительности по классам
class_names = iris.target_names
for i, class_name in enumerate(class_names):
    class_mask = test_data['target'] == i
    if np.sum(class_mask) > 0:
        class_accuracy = np.mean(test_predictions[class_mask] == test_data['target'][class_mask])
        print(f"Точность для класса {class_name}: {class_accuracy:.4f}")

# Анализ уверенности предсказаний
pred_proba = predictor.predict_proba(test_data)
confidence = np.max(pred_proba, axis=1)
print(f"\nСредняя уверенность предсказаний: {np.mean(confidence):.4f}")
print(f"Минимальная уверенность: {np.min(confidence):.4f}")
print(f"Максимальная уверенность: {np.max(confidence):.4f}")

# Анализ ошибок
errors = test_predictions != test_data['target']
if np.sum(errors) > 0:
    print(f"\nАнализ ошибок ({np.sum(errors)} из {len(test_data)}):")
    error_indices = np.where(errors)[0]
    for idx in error_indices[:5]:  # Показываем первые 5 ошибок
        true_class = class_names[test_data['target'].iloc[idx]]
        pred_class = class_names[test_predictions[idx]]
        confidence_error = confidence[idx]
        print(f"  Индекс {idx}: Истина={true_class}, Предсказание={pred_class}, Уверенность={confidence_error:.4f}")
```

#### Упражнение 3: Продакшен (2 часа)

**Цель:** Создать полноценную продакшен API с пониманием всех параметров деплоя

```python
# Создайте простую API для модели
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import logging
import os
import time
from datetime import datetime
import json
from functools import wraps
import traceback

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Включение CORS для фронтенда

# Конфигурация приложения
class Config:
    # Параметры модели
    MODEL_PATH = os.getenv('MODEL_PATH', 'iris_validation_model')
    MODEL_TYPE = os.getenv('MODEL_TYPE', 'TabularPredictor')
    
    # Параметры API
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Параметры производительности
    MAX_BATCH_SIZE = int(os.getenv('MAX_BATCH_SIZE', 1000))
    MAX_REQUEST_SIZE = int(os.getenv('MAX_REQUEST_SIZE', 1024 * 1024))  # 1MB
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))  # 30 секунд
    
    # Параметры мониторинга
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'True').lower() == 'true'
    METRICS_INTERVAL = int(os.getenv('METRICS_INTERVAL', 60))  # 60 секунд
    
    # Параметры безопасности
    API_KEY = os.getenv('API_KEY', None)
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', 100))  # запросов в минуту
    
    # Параметры валидации
    REQUIRED_FEATURES = ['sepal length (cm)', 'sepal width (cm)', 
                        'petal length (cm)', 'petal width (cm)']
    FEATURE_RANGES = {
        'sepal length (cm)': (4.0, 8.0),
        'sepal width (cm)': (2.0, 4.5),
        'petal length (cm)': (1.0, 7.0),
        'petal width (cm)': (0.1, 2.5)
    }

app.config.from_object(Config)

# Глобальные переменные для мониторинга
request_count = 0
error_count = 0
total_prediction_time = 0
start_time = time.time()

# Загрузка модели с обработкой ошибок
try:
    predictor = TabularPredictor.load(Config.MODEL_PATH)
    logger.info(f"Модель загружена из {Config.MODEL_PATH}")
    logger.info(f"Доступные модели: {predictor.get_model_names()}")
    logger.info(f"Лучшая модель: {predictor.get_model_best()}")
except Exception as e:
    logger.error(f"Ошибка загрузки модели: {e}")
    predictor = None

# Декораторы для обработки ошибок и мониторинга
def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global error_count
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_count += 1
            logger.error(f"Ошибка в {f.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
    return decorated_function

def monitor_performance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global request_count, total_prediction_time
        start_time = time.time()
        request_count += 1
        
        result = f(*args, **kwargs)
        
        prediction_time = time.time() - start_time
        total_prediction_time += prediction_time
        
        logger.info(f"Запрос {request_count}: время выполнения {prediction_time:.4f}с")
        return result
    return decorated_function

def validate_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if Config.API_KEY:
            api_key = request.headers.get('X-API-Key')
            if not api_key or api_key != Config.API_KEY:
                return jsonify({'error': 'Invalid API Key'}), 401
        return f(*args, **kwargs)
    return decorated_function

def validate_input_data(data):
    """Валидация входных данных"""
    if not isinstance(data, (list, dict)):
        raise ValueError("Данные должны быть списком или словарем")
    
    if isinstance(data, dict):
        data = [data]
    
    if len(data) > Config.MAX_BATCH_SIZE:
        raise ValueError(f"Превышен максимальный размер батча: {len(data)} > {Config.MAX_BATCH_SIZE}")
    
    validated_data = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Элемент {i} должен быть словарем")
        
        # Проверка обязательных признаков
        for feature in Config.REQUIRED_FEATURES:
            if feature not in item:
                raise ValueError(f"Отсутствует обязательный признак: {feature}")
        
        # Проверка типов и диапазонов значений
        validated_item = {}
        for feature, value in item.items():
            if feature in Config.REQUIRED_FEATURES:
                try:
                    float_value = float(value)
                    min_val, max_val = Config.FEATURE_RANGES[feature]
                    if not (min_val <= float_value <= max_val):
                        raise ValueError(f"Значение {feature}={float_value} вне диапазона [{min_val}, {max_val}]")
                    validated_item[feature] = float_value
                except (ValueError, TypeError):
                    raise ValueError(f"Некорректное значение для {feature}: {value}")
            else:
                validated_item[feature] = value
        
        validated_data.append(validated_item)
    
    return validated_data

@app.route('/health', methods=['GET'])
@handle_errors
def health_check():
    """Проверка здоровья API"""
    global request_count, error_count, total_prediction_time, start_time
    
    uptime = time.time() - start_time
    avg_prediction_time = total_prediction_time / max(request_count, 1)
    error_rate = error_count / max(request_count, 1)
    
    health_status = {
        'status': 'healthy' if predictor is not None else 'unhealthy',
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': uptime,
        'model_loaded': predictor is not None,
        'metrics': {
            'total_requests': request_count,
            'total_errors': error_count,
            'error_rate': error_rate,
            'average_prediction_time': avg_prediction_time
        }
    }
    
    status_code = 200 if predictor is not None else 503
    return jsonify(health_status), status_code

@app.route('/predict', methods=['POST'])
@handle_errors
@monitor_performance
@validate_api_key
def predict():
    """Основной endpoint для предсказаний"""
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 503
    
    # Валидация размера запроса
    content_length = request.content_length
    if content_length and content_length > Config.MAX_REQUEST_SIZE:
        return jsonify({'error': 'Request too large'}), 413
    
    # Получение и валидация данных
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        validated_data = validate_input_data(data)
    except ValueError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Data processing error: {str(e)}'}), 400
    
    # Преобразование в DataFrame
    df = pd.DataFrame(validated_data)
    
    # Предсказания
    try:
        predictions = predictor.predict(df)
        probabilities = predictor.predict_proba(df)
        
        # Формирование ответа
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            result = {
                'index': i,
                'prediction': int(pred),
                'prediction_class': ['setosa', 'versicolor', 'virginica'][int(pred)],
                'probabilities': {
                    'setosa': float(prob[0]),
                    'versicolor': float(prob[1]),
                    'virginica': float(prob[2])
                },
                'confidence': float(np.max(prob))
            }
            results.append(result)
        
        response = {
            'predictions': results,
            'metadata': {
                'model_name': predictor.get_model_best(),
                'timestamp': datetime.now().isoformat(),
                'total_predictions': len(results)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Ошибка предсказания: {str(e)}")
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/model_info', methods=['GET'])
@handle_errors
def model_info():
    """Информация о модели"""
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 503
    
    info = {
        'model_type': 'TabularPredictor',
        'best_model': predictor.get_model_best(),
        'available_models': predictor.get_model_names(),
        'feature_importance': predictor.feature_importance().to_dict() if hasattr(predictor, 'feature_importance') else None,
        'model_path': Config.MODEL_PATH,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(info)

@app.route('/metrics', methods=['GET'])
@handle_errors
def get_metrics():
    """Метрики производительности"""
    if not Config.ENABLE_METRICS:
        return jsonify({'error': 'Metrics disabled'}), 403
    
    global request_count, error_count, total_prediction_time, start_time
    
    uptime = time.time() - start_time
    avg_prediction_time = total_prediction_time / max(request_count, 1)
    error_rate = error_count / max(request_count, 1)
    requests_per_second = request_count / max(uptime, 1)
    
    metrics = {
        'uptime_seconds': uptime,
        'total_requests': request_count,
        'total_errors': error_count,
        'error_rate': error_rate,
        'average_prediction_time': avg_prediction_time,
        'requests_per_second': requests_per_second,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(metrics)

if __name__ == '__main__':
    logger.info(f"Запуск API сервера на {Config.HOST}:{Config.PORT}")
    logger.info(f"Debug режим: {Config.DEBUG}")
    logger.info(f"Модель: {Config.MODEL_PATH}")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
        threaded=True,  # Многопоточность
        use_reloader=False  # Отключение автоперезагрузки в продакшене
    )
```

### Дополнительные файлы для продакшена

#### requirements.txt
```txt
flask==2.3.3
flask-cors==4.0.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
autogluon.tabular==0.8.2
gunicorn==21.2.0
```

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "30", "app:app"]
```

#### docker-compose.yml
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MODEL_PATH=/app/models/iris_validation_model
      - DEBUG=False
      - API_KEY=your-secret-key
      - MAX_BATCH_SIZE=1000
      - RATE_LIMIT=100
    volumes:
      - ./models:/app/models
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 🔄 Итеративный подход

### 🔁 Цикл обучения

```mermaid
graph LR
    A[Читайте раздел<br/>10-15 мин] --> B[Пробуйте код<br/>20-30 мин]
    B --> C[Анализируйте результаты<br/>5-10 мин]
    C --> D[Делайте заметки<br/>5 мин]
    D --> E[Переходите к следующему разделу]
    E --> A
    
    B --> F{Код работает?}
    F -->|Нет| G[Исправьте ошибки<br/>10-15 мин]
    G --> B
    F -->|Да| C
    
    C --> H{Понятно?}
    H -->|Нет| I[Перечитайте раздел<br/>10 мин]
    I --> A
    H -->|Да| D
    
    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#e0f2f1
```

1. **Читайте раздел** (10-15 минут)
2. **Пробуйте код** (20-30 минут)
3. **Анализируйте результаты** (5-10 минут)
4. **Делайте заметки** (5 минут)
5. **Переходите к следующему разделу**

### 🎯 Постановка целей

### ⏰ Временная шкала целей обучения

```mermaid
gantt
    title Временная шкала целей обучения AutoML Gluon
    dateFormat X
    axisFormat %s
    
    section Краткосрочные (1-2 недели)
    Запуск первого примера    :done, short1, 0, 1
    Понимание основ          :done, short2, 1, 2
    Создание простой модели  :done, short3, 2, 3
    
    section Среднесрочные (1-2 месяца)
    Продакшен система        :active, medium1, 3, 5
    Продвинутые техники      :medium2, 5, 7
    Реальная задача          :medium3, 7, 9
    
    section Долгосрочные (3-6 месяцев)
    Эксперт в AutoML Gluon   :long1, 9, 12
    Супер-система            :long2, 12, 15
    Обмен знаниями           :long3, 15, 18
```

#### Краткосрочные цели (1-2 недели)
- Запустить первый пример
- Понять основные концепции
- Создать простую модель

#### Среднесрочные цели (1-2 месяца)
- Создать продакшен систему
- Понять продвинутые техники
- Решить реальную задачу

#### Долгосрочные цели (3-6 месяцев)
- Стать экспертом в AutoML Gluon
- Создать супер-систему
- Поделиться знаниями с другими

## Ресурсы для углубления

### 📚 Дополнительная литература
- "AutoML: Methods, Systems, Challenges" - Frank Hutter
- "Hands-On Machine Learning" - Aurélien Géron
- "The Elements of Statistical Learning" - Hastie, Tibshirani, Friedman

### 🌐 Онлайн ресурсы
- [AutoML Gluon Documentation](https://auto.gluon.ai/)
- [Amazon SageMaker](https://aws.amazon.com/sagemaker/)
- [Kaggle Learn](https://www.kaggle.com/learn)

### 👥 Сообщество
- [AutoML Gluon GitHub](https://github.com/autogluon/autogluon)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/autogluon)
- [Reddit r/MachineLearning](https://www.reddit.com/r/MachineLearning/)

## Заключение

### 🎯 Путь к успеху

```mermaid
graph TD
    A[Начало изучения] --> B[Выбор подходящего пути]
    B --> C[Следование практическим рекомендациям]
    C --> D[Постоянная практика]
    D --> E[Достижение целей]
    E --> F[Становление экспертом]
    F --> G[Создание супер-системы]
    G --> H[Успех! 🎉]
    
    B --> B1[Новичок: 1-2 месяца]
    B --> B2[Продвинутый: 2-3 недели]
    B --> B3[Эксперт: 3-5 дней]
    
    C --> C1[Итеративный подход]
    C --> C2[Практические упражнения]
    C --> C3[Ведение заметок]
    
    D --> D1[Создание моделей]
    D --> D2[Валидация результатов]
    D --> D3[Деплой в продакшен]
    
    style A fill:#e3f2fd
    style H fill:#e8f5e8
    style F fill:#fff3e0
    style G fill:#f3e5f5
```

## Справочная таблица параметров по уровням

### Параметры для разных уровней подготовки

| Параметр | Новичок | Продвинутый | Эксперт | Описание |
|----------|---------|-------------|---------|----------|
| **time_limit** | 60-300 | 600-1800 | 3600+ | Лимит времени обучения (сек) |
| **presets** | 'medium_quality' | 'high_quality' | 'best_quality' | Качество моделей |
| **num_trials** | 5-10 | 20-50 | 100+ | Количество попыток tuning |
| **holdout_frac** | 0.2 | 0.2-0.3 | 0.1-0.2 | Доля данных для валидации |
| **num_bag_folds** | 0-3 | 5-10 | 10+ | Количество фолдов бэггинга |
| **num_stack_levels** | 0-1 | 1-2 | 2+ | Уровни стекинга |
| **verbosity** | 2-3 | 1-2 | 0-1 | Уровень вывода |
| **feature_prune** | False | True | True | Отбор признаков |
| **refit_full** | False | True | True | Переобучение на всех данных |

### Параметры по специализациям

| Параметр | Аналитик | ML-инженер | Трейдер | Бизнес-аналитик |
|----------|----------|------------|---------|-----------------|
| **eval_metric** | 'roc_auc' | 'accuracy' | 'f1' | 'roc_auc' |
| **presets** | 'best_quality' | 'optimize_for_deployment' | 'best_quality' | 'high_quality' |
| **verbosity** | 3 | 1 | 2 | 2 |
| **auxiliary_metrics** | True | False | True | True |
| **feature_prune** | True | True | True | True |
| **excluded_model_types** | ['KNN'] | ['KNN', 'NN_TORCH'] | [] | ['KNN', 'NN_TORCH'] |
| **included_model_types** | ['RF', 'GBM', 'XGB'] | [] | [] | ['RF', 'GBM', 'XGB', 'CAT'] |

### Системные требования по уровням

| Компонент | Новичок | Продвинутый | Эксперт | Продакшен |
|-----------|---------|-------------|---------|-----------|
| **RAM** | 4-8GB | 8-16GB | 16-32GB | 32GB+ |
| **CPU** | 2-4 ядра | 4-8 ядер | 8-16 ядер | 16+ ядер |
| **Диск** | 2-5GB | 5-20GB | 20-50GB | 50GB+ |
| **GPU** | Не требуется | Опционально | Рекомендуется | Обязательно |

### Параметры производительности

| Параметр | Значение | Описание | Влияние |
|----------|----------|----------|---------|
| **time_limit** | 60-3600 | Лимит времени обучения | Качество vs скорость |
| **num_trials** | 5-100 | Количество попыток tuning | Качество vs время |
| **num_bag_folds** | 0-20 | Количество фолдов | Стабильность vs время |
| **num_stack_levels** | 0-3 | Уровни стекинга | Качество vs сложность |
| **holdout_frac** | 0.1-0.3 | Доля валидации | Надежность vs данные |

### Рекомендации по выбору параметров

#### Для быстрого прототипирования

```python
predictor = TabularPredictor(
    label='target',
    problem_type='binary',
    eval_metric='accuracy',
    presets='medium_quality',
    time_limit=300,
    num_trials=10,
    verbosity=2
)
```

#### Для продакшена

```python
predictor = TabularPredictor(
    label='target',
    problem_type='binary',
    eval_metric='accuracy',
    presets='optimize_for_deployment',
    time_limit=3600,
    num_trials=50,
    feature_prune=True,
    save_space=True,
    keep_only_best=True,
    verbosity=1
)
```

#### Для исследований

```python
predictor = TabularPredictor(
    label='target',
    problem_type='binary',
    eval_metric='roc_auc',
    presets='best_quality',
    time_limit=7200,
    num_trials=100,
    num_bag_folds=10,
    num_stack_levels=2,
    feature_prune=True,
    refit_full=True,
    verbosity=3
)
```

## Заключение

Этот учебник рассчитан на разные уровни подготовки. Выберите подходящий путь изучения и следуйте практическим рекомендациям. Помните: лучший способ изучить AutoML Gluon - это практика!

**Ключевые принципы успешного изучения:**
1. **Начните с простого** - используйте параметры по умолчанию
2. **Практикуйтесь постоянно** - создавайте модели каждый день
3. **Экспериментируйте с параметрами** - изучайте их влияние
4. **Документируйте результаты** - ведите записи экспериментов
5. **Применяйте на реальных задачах** - решайте практические проблемы
