# Продакшен и деплой AutoML Gluon моделей

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему продакшен критически важен

**Почему 87% ML-моделей никогда не попадают в продакшен?** Потому что их создатели не понимают, что обучение модели - это только 20% работы. Остальные 80% - это подготовка к продакшену, мониторинг и поддержка.

### Катастрофические последствия плохого продакшена
- **Microsoft Tay**: AI-чатбот стал расистом за 24 часа в продакшене
- **Amazon HR**: AI-система дискриминировала женщин при найме
- **Uber самоуправляемые авто**: Смерть пешехода из-за неправильной работы модели
- **Facebook алгоритм**: Распространение фейковых новостей из-за плохой валидации

### Преимущества правильного продакшена
- **Масштабируемость**: Модель работает с любым объемом данных
- **Надежность**: 99.9% uptime, автоматическое восстановление
- **Мониторинг**: Постоянный контроль качества предсказаний
- **Бизнес-ценность**: Реальная польза для компании и пользователей

## Введение в продакшен

<img src="images/optimized/production_architecture.png" alt="Продакшен архитектура" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 1: Архитектура продакшен системы AutoML Gluon*

**Почему продакшен в ML кардинально отличается от обычной разработки?** Потому что ML-модели - это не просто код, а живые системы, которые учатся и изменяются. Это как разница между заводом и садом - завод работает по плану, а сад требует постоянного ухода.

**Уникальные особенности ML продакшена:**
- **Данные меняются**: Модель может "забыть" то, что знала
- **Концептуальный дрифт**: Реальность изменяется быстрее модели
- **Зависимость от данных**: Нет данных = нет предсказаний
- **Черный ящик**: Сложно понять, почему модель приняла решение

Продакшен деплой ML-моделей - это критически важный этап, который требует тщательного планирования, мониторинга и поддержки. В этом разделе рассмотрим все аспекты деплоя AutoML Gluon моделей в продакшен.

## Подготовка модели к продакшену

<img src="images/optimized/performance_comparison.png" alt="Оптимизация моделей" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 2: Оптимизация моделей для продакшена*

**Почему важна оптимизация моделей для продакшена?** Потому что продакшен предъявляет совершенно другие требования к производительности, памяти и скорости.

### 🚀 Ключевые аспекты оптимизации

**Почему модель, которая отлично работает в Jupyter, может провалиться в продакшене?** Потому что продакшен предъявляет совершенно другие требования:

- **Производительность**: Скорость предсказаний критически важна
- **Память**: Ограниченные ресурсы сервера
- **Размер модели**: Должна помещаться в контейнер
- **Стабильность**: Работа на разных серверах и окружениях
- **Масштабируемость**: Обработка больших объемов запросов
- **Надежность**: Отказоустойчивость и восстановление

### Оптимизация модели

**Проблемы неоптимизированных моделей в продакшене:**
- **Медленные предсказания**: 5 секунд вместо 50мс - пользователи уйдут
- **Высокое потребление памяти**: Сервер падает под нагрузкой
- **Большой размер модели**: Не помещается в контейнер
- **Нестабильность**: Модель работает нестабильно на разных серверах

**Методы оптимизации моделей:**
- **Квантизация**: Уменьшение точности весов (float32 → float16)
- **Прунинг**: Удаление неважных нейронов
- **Дистилляция**: Обучение маленькой модели на большой
- **Оптимизация архитектуры**: Выбор более эффективных алгоритмов

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

# Создание оптимизированной модели для продакшена
def create_production_model(train_data, target_col):
    """Создание модели, оптимизированной для продакшена"""
    
    predictor = TabularPredictor(
        label=target_col,
        problem_type='auto',
        eval_metric='auto',
        path='./production_models'  # Отдельная папка для продакшен моделей
    )
    
    # Обучение с оптимизацией для деплоя
    predictor.fit(
        train_data,
        presets='optimize_for_deployment',  # Специальные настройки для продакшена
        time_limit=3600,  # 1 час - ограничение времени обучения
        num_bag_folds=3,   # Меньше фолдов для скорости
        num_bag_sets=1,
        ag_args_fit={
            'num_cpus': 4,        # Ограничение CPU для стабильности
            'num_gpus': 0,        # Отключение GPU для совместимости
            'memory_limit': 8     # Ограничение памяти в GB
        }
    )
    
    return predictor
```

**🔧 Детальное описание параметров оптимизации моделей для продакшена:**

**Функция create_production_model:**
- **Назначение**: Создание модели, оптимизированной для продакшен деплоя
- **Параметры**:
  - **`train_data`**: Данные для обучения
    - **Тип**: DataFrame
    - **Описание**: Таблица с обучающими данными
    - **Требования**: Должна содержать целевую переменную
  - **`target_col`**: Название целевой переменной
    - **Тип**: str
    - **Описание**: Название столбца с целевой переменной
- **Возвращаемое значение**: TabularPredictor - оптимизированная модель

**Параметры TabularPredictor:**
- **`label`**: Название целевой переменной
  - **Тип**: str
  - **Описание**: Столбец с целевой переменной для предсказания
- **`problem_type`**: Тип задачи машинного обучения
  - **Тип**: str
  - **Значения**: 'auto', 'binary', 'multiclass', 'regression'
  - **По умолчанию**: 'auto'
  - **Описание**: AutoGluon автоматически определяет тип задачи
- **`eval_metric`**: Метрика для оценки качества
  - **Тип**: str
  - **Значения**: 'auto', 'accuracy', 'f1', 'roc_auc', 'rmse', 'mae'
  - **По умолчанию**: 'auto'
  - **Описание**: Автоматический выбор метрики по типу задачи
- **`path`**: Путь для сохранения модели
  - **Тип**: str
  - **Описание**: Директория для сохранения файлов модели
  - **Рекомендации**: Используйте отдельную папку для продакшен моделей

**Параметры predictor.fit():**
- **`presets`**: Предустановленные настройки
  - **Тип**: str
  - **Значения**: 'optimize_for_deployment', 'best_quality', 'high_quality', 'good_quality', 'medium_quality', 'optimize_for_size'
  - **Описание**: 'optimize_for_deployment' оптимизирует модель для продакшена
- **`time_limit`**: Ограничение времени обучения
  - **Тип**: int
  - **Диапазон значений**: `[60, 86400]` (1 минута - 24 часа)
  - **По умолчанию**: 3600 (1 час)
  - **Рекомендации**: Для продакшена используйте 1-2 часа
- **`num_bag_folds`**: Количество фолдов для валидации
  - **Тип**: int
  - **Диапазон значений**: `[2, 10]` (рекомендуется 3-5)
  - **По умолчанию**: 8
  - **Рекомендации**: Для продакшена используйте 3-5 фолдов
- **`num_bag_sets`**: Количество наборов фолдов
  - **Тип**: int
  - **Диапазон значений**: `[1, 5]` (рекомендуется 1-2)
  - **По умолчанию**: 1
  - **Рекомендации**: Для продакшена используйте 1 набор

**Параметры ag_args_fit:**
- **`num_cpus`**: Количество CPU для обучения
  - **Тип**: int
  - **Диапазон значений**: `[1, 32]` (рекомендуется 2-8)
  - **По умолчанию**: 4
  - **Рекомендации**: Для продакшена используйте 2-4 CPU
- **`num_gpus`**: Количество GPU для обучения
  - **Тип**: int
  - **Диапазон значений**: `[0, 8]` (рекомендуется 0-2)
  - **По умолчанию**: 0
  - **Рекомендации**: Для продакшена отключите GPU для совместимости
- **`memory_limit`**: Ограничение памяти в GB
  - **Тип**: int
  - **Диапазон значений**: `[1, 64]` (рекомендуется 4-16)
  - **По умолчанию**: 8
  - **Рекомендации**: Для продакшена используйте 4-8 GB

**Почему важны ограничения ресурсов?** Потому что продакшен серверы имеют ограниченные ресурсы, и модель должна работать в этих рамках.

### Сжатие модели

```python
def compress_model(predictor, model_name):
    """Сжатие модели для продакшена"""
    
    # Сохранение сжатой модели
    predictor.save(
        model_name,
        save_space=True,
        compress=True,
        save_info=True
    )
    
    # Получение размера модели
    import os
    model_size = os.path.getsize(f"{model_name}/predictor.pkl") / (1024 * 1024)  # MB
    print(f"Model size: {model_size:.2f} MB")
    
    return model_size
```

**🔧 Детальное описание параметров сжатия модели:**

**Функция compress_model:**
- **Назначение**: Сжатие модели для уменьшения размера файлов
- **Параметры**:
  - **`predictor`**: Обученная модель
    - **Тип**: TabularPredictor
    - **Описание**: Обученная модель AutoGluon
  - **`model_name`**: Имя для сохранения модели
    - **Тип**: str
    - **Описание**: Путь и имя для сохранения сжатой модели
- **Возвращаемое значение**: float - размер модели в MB

**Параметры predictor.save():**
- **`model_name`**: Имя модели
  - **Тип**: str
  - **Описание**: Путь для сохранения модели
  - **Рекомендации**: Используйте описательные имена с версиями
- **`save_space`**: Оптимизация размера
  - **Тип**: bool
  - **По умолчанию**: True
  - **Описание**: Удаляет временные файлы для экономии места
  - **Влияние**: Уменьшает размер модели на 20-30%
- **`compress`**: Сжатие файлов
  - **Тип**: bool
  - **По умолчанию**: True
  - **Описание**: Использует gzip сжатие для файлов модели
  - **Влияние**: Уменьшает размер модели на 40-60%
- **`save_info`**: Сохранение информации о модели
  - **Тип**: bool
  - **По умолчанию**: True
  - **Описание**: Сохраняет метаданные о модели
  - **Использование**: Нужно для загрузки и отладки модели

**Методы сжатия:**
- **Удаление временных файлов**: Очистка промежуточных результатов
- **Gzip сжатие**: Сжатие файлов модели
- **Оптимизация весов**: Удаление неиспользуемых параметров
- **Квантизация**: Уменьшение точности весов (float32 → float16)

### Валидация модели

```python
def validate_production_model(predictor, test_data, performance_thresholds):
    """Валидация модели для продакшена"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Проверка пороговых значений
    validation_results = {}
    for metric, threshold in performance_thresholds.items():
        if metric in performance:
            validation_results[metric] = performance[metric] >= threshold
        else:
            validation_results[metric] = False
    
    # Проверка стабильности предсказаний
    if hasattr(predictor, 'predict_proba'):
        probabilities = predictor.predict_proba(test_data)
        prob_std = probabilities.std().mean()
        validation_results['stability'] = prob_std < 0.1  # Стабильность вероятностей
    
    return validation_results, performance
```

**🔧 Детальное описание параметров валидации модели для продакшена:**

**Функция validate_production_model:**
- **Назначение**: Валидация модели перед деплоем в продакшен
- **Параметры**:
  - **`predictor`**: Обученная модель
    - **Тип**: TabularPredictor
    - **Описание**: Модель для валидации
  - **`test_data`**: Тестовые данные
    - **Тип**: DataFrame
    - **Описание**: Данные для тестирования модели
    - **Требования**: Должны содержать целевую переменную
  - **`performance_thresholds`**: Пороговые значения метрик
    - **Тип**: dict
    - **Описание**: Словарь с минимальными значениями метрик
    - **Пример**: {'accuracy': 0.85, 'f1': 0.80, 'roc_auc': 0.90}
- **Возвращаемое значение**: tuple - (validation_results, performance)
  - **`validation_results`**: dict - результаты валидации
  - **`performance`**: dict - метрики производительности

**Структура validation_results:**
- **`metric_name`**: bool - результат проверки метрики
  - **True**: Метрика превышает пороговое значение
  - **False**: Метрика ниже порогового значения
- **`stability`**: bool - стабильность предсказаний
  - **True**: Стандартное отклонение вероятностей < 0.1
  - **False**: Высокая нестабильность предсказаний

**Структура performance:**
- **Метрики классификации**: accuracy, precision, recall, f1, roc_auc
- **Метрики регрессии**: rmse, mae, r2, mape
- **Кастомные метрики**: Любые метрики, определенные при обучении

**Проверки валидации:**
- **Пороговые значения**: Сравнение метрик с минимальными требованиями
- **Стабильность**: Анализ разброса вероятностей предсказаний
- **Производительность**: Оценка скорости предсказаний
- **Память**: Проверка использования памяти
- **Совместимость**: Тестирование на разных платформах

## API сервер для продакшена

### FastAPI сервер

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import logging
from typing import Dict, List, Any
import asyncio
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(title="AutoML Gluon Production API", version="1.0.0")

# Глобальная переменная для модели
model = None

class PredictionRequest(BaseModel):
    """Схема запроса для предсказания"""
    data: List[Dict[str, Any]]
    
class PredictionResponse(BaseModel):
    """Схема ответа с предсказаниями"""
    predictions: List[Any]
    probabilities: List[Dict[str, float]] = None
    model_info: Dict[str, Any]
    timestamp: str

class HealthResponse(BaseModel):
    """Схема ответа для health check"""
    status: str
    model_loaded: bool
    model_info: Dict[str, Any] = None

**🔧 Детальное описание параметров FastAPI сервера:**

**FastAPI приложение:**
- **`title`**: Название API
  - **Тип**: str
  - **Описание**: Отображается в документации Swagger
  - **Рекомендации**: Используйте описательное название
- **`version`**: Версия API
  - **Тип**: str
  - **Описание**: Версия API для отслеживания изменений
  - **Рекомендации**: Используйте семантическое версионирование (1.0.0)

**Класс PredictionRequest:**
- **`data`**: Данные для предсказания
  - **Тип**: List[Dict[str, Any]]
  - **Описание**: Список записей для предсказания
  - **Структура**: Каждая запись - словарь с признаками
  - **Пример**: [{"feature1": 1.0, "feature2": 2.0}, {"feature1": 3.0, "feature2": 4.0}]

**Класс PredictionResponse:**
- **`predictions`**: Предсказания модели
  - **Тип**: List[Any]
  - **Описание**: Список предсказаний для каждой записи
- **`probabilities`**: Вероятности предсказаний
  - **Тип**: List[Dict[str, float]] = None
  - **Описание**: Вероятности для каждого класса (только для классификации)
  - **Структура**: [{"class1": 0.8, "class2": 0.2}, ...]
- **`model_info`**: Информация о модели
  - **Тип**: Dict[str, Any]
  - **Описание**: Метаданные о модели
- **`timestamp`**: Время предсказания
  - **Тип**: str
  - **Описание**: ISO формат времени предсказания

**Класс HealthResponse:**
- **`status`**: Статус API
  - **Тип**: str
  - **Значения**: "healthy", "unhealthy"
  - **Описание**: Общий статус API
- **`model_loaded`**: Статус загрузки модели
  - **Тип**: bool
  - **Описание**: Загружена ли модель
- **`model_info`**: Информация о модели
  - **Тип**: Dict[str, Any] = None
  - **Описание**: Метаданные о модели (только если модель загружена)

@app.on_event("startup")
async def load_model():
    """Загрузка модели при запуске сервера"""
    global model
    try:
        model = TabularPredictor.load('./production_models')
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        model = None

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if model is None:
        return HealthResponse(
            status="unhealthy",
            model_loaded=False
        )
    
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        model_info={
            "model_path": model.path,
            "problem_type": model.problem_type,
            "eval_metric": model.eval_metric
        }
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Endpoint для предсказаний"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Преобразование данных в DataFrame
        df = pd.DataFrame(request.data)
        
        # Предсказания
        predictions = model.predict(df)
        
        # Вероятности (если доступны)
        probabilities = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(df)
            probabilities = proba.to_dict('records')
        
        # Информация о модели
        model_info = {
            "model_path": model.path,
            "problem_type": model.problem_type,
            "eval_metric": model.eval_metric,
            "num_features": len(df.columns)
        }
        
        return PredictionResponse(
            predictions=predictions.tolist(),
            probabilities=probabilities,
            model_info=model_info,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
async def model_info():
    """Информация о модели"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_path": model.path,
        "problem_type": model.problem_type,
        "eval_metric": model.eval_metric,
        "feature_importance": model.feature_importance().to_dict()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Flask сервер

```python
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import logging
from datetime import datetime
import traceback

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание Flask приложения
app = Flask(__name__)

# Глобальная переменная для модели
model = None

def load_model():
    """Загрузка модели"""
    global model
    try:
        model = TabularPredictor.load('./production_models')
        logger.info("Model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if model is None:
        return jsonify({
            "status": "unhealthy",
            "model_loaded": False
        }), 503
    
    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "model_info": {
            "model_path": model.path,
            "problem_type": model.problem_type,
            "eval_metric": model.eval_metric
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint для предсказаний"""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 503
    
    try:
        # Получение данных
        data = request.get_json()
        
        if 'data' not in data:
            return jsonify({"error": "No data provided"}), 400
        
        # Преобразование в DataFrame
        df = pd.DataFrame(data['data'])
        
        # Предсказания
        predictions = model.predict(df)
        
        # Вероятности (если доступны)
        probabilities = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(df)
            probabilities = proba.to_dict('records')
        
        return jsonify({
            "predictions": predictions.tolist(),
            "probabilities": probabilities,
            "model_info": {
                "model_path": model.path,
                "problem_type": model.problem_type,
                "eval_metric": model.eval_metric
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/model/info', methods=['GET'])
def model_info():
    """Информация о модели"""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 503
    
    return jsonify({
        "model_path": model.path,
        "problem_type": model.problem_type,
        "eval_metric": model.eval_metric,
        "feature_importance": model.feature_importance().to_dict()
    })

if __name__ == "__main__":
    if load_model():
        app.run(host="0.0.0.0", port=8000, debug=False)
    else:
        logger.error("Failed to start server - model not loaded")
```

## Docker контейнеризация

<img src="images/optimized/simple_production_flow.png" alt="Контейнеризация и деплой" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 3: Контейнеризация и стратегии деплоя ML-моделей*

**Почему важна контейнеризация для ML-моделей?** Потому что она обеспечивает консистентность и изоляцию:

- **Консистентность**: Одинаковая среда на всех серверах
- **Изоляция**: Модель не влияет на другие приложения
- **Портативность**: Легко переносить между серверами
- **Масштабируемость**: Простое горизонтальное масштабирование
- **Версионирование**: Контроль версий моделей и зависимостей
- **Безопасность**: Изолированная среда выполнения

### Dockerfile для продакшена

```dockerfile
# Dockerfile для продакшена
FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание пользователя для безопасности
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["python", "app.py"]
```

**🔧 Детальное описание параметров Docker контейнеризации:**

**Dockerfile инструкции:**
- **`FROM python:3.9-slim`**: Базовый образ
  - **Описание**: Использует Python 3.9 на базе Debian slim
  - **Размер**: ~150MB (компактный образ)
  - **Преимущества**: Быстрая загрузка, минимальная поверхность атаки
- **`RUN apt-get update && apt-get install -y`**: Установка системных зависимостей
  - **`gcc`**: Компилятор C для сборки Python пакетов
  - **`g++`**: Компилятор C++ для сборки Python пакетов
  - **`&& rm -rf /var/lib/apt/lists/*`**: Очистка кэша apt для уменьшения размера
- **`WORKDIR /app`**: Рабочая директория
  - **Описание**: Устанавливает /app как рабочую директорию
  - **Преимущества**: Изолирует файлы приложения
- **`COPY requirements.txt .`**: Копирование файла зависимостей
  - **Описание**: Копирует requirements.txt в контейнер
  - **Преимущества**: Кэширование слоев Docker
- **`RUN pip install --no-cache-dir -r requirements.txt`**: Установка Python зависимостей
  - **`--no-cache-dir`**: Отключает кэш pip для уменьшения размера
  - **Преимущества**: Уменьшает размер образа на 50-100MB
- **`COPY . .`**: Копирование кода приложения
  - **Описание**: Копирует весь код приложения в контейнер
  - **Рекомендации**: Используйте .dockerignore для исключения ненужных файлов
- **`RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app`**: Создание пользователя
  - **`-m`**: Создает домашнюю директорию
  - **`-u 1000`**: Устанавливает UID 1000
  - **`chown -R`**: Изменяет владельца всех файлов
  - **Безопасность**: Запуск не от root пользователя
- **`USER appuser`**: Переключение на пользователя
  - **Описание**: Переключается на созданного пользователя
  - **Безопасность**: Ограничивает права доступа
- **`EXPOSE 8000`**: Открытие порта
  - **Описание**: Документирует, что приложение использует порт 8000
  - **Примечание**: Не открывает порт автоматически
- **`CMD ["python", "app.py"]`**: Команда запуска
  - **Описание**: Запускает приложение при старте контейнера
  - **Формат**: JSON массив для избежания shell интерпретации

### Docker Compose для продакшена

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  autogluon-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/models
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - autogluon-api
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

**🔧 Детальное описание параметров Docker Compose:**

**Версия Docker Compose:**
- **`version: '3.8'`**: Версия формата файла
  - **Описание**: Использует формат Docker Compose версии 3.8
  - **Преимущества**: Поддержка новых функций и улучшенная совместимость

**Сервис autogluon-api:**
- **`build: .`**: Сборка образа
  - **Описание**: Собирает образ из Dockerfile в текущей директории
  - **Альтернативы**: Можно использовать `image: имя_образа` для готового образа
- **`ports`**: Проброс портов
  - **`"8000:8000"`**: Пробрасывает порт 8000 контейнера на порт 8000 хоста
  - **Формат**: "хост:контейнер"
- **`environment`**: Переменные окружения
  - **`MODEL_PATH=/app/models`**: Путь к моделям в контейнере
  - **`LOG_LEVEL=INFO`**: Уровень логирования
- **`volumes`**: Монтирование томов
  - **`./models:/app/models`**: Монтирует локальную папку models в контейнер
  - **`./logs:/app/logs`**: Монтирует локальную папку logs в контейнер
- **`restart: unless-stopped`**: Политика перезапуска
  - **Описание**: Перезапускает контейнер при сбое, кроме ручной остановки
  - **Альтернативы**: always, on-failure, no
- **`healthcheck`**: Проверка здоровья
  - **`test`**: Команда для проверки здоровья
  - **`interval: 30s`**: Интервал проверки
  - **`timeout: 10s`**: Таймаут команды
  - **`retries: 3`**: Количество попыток
  - **`start_period: 40s`**: Время ожидания перед первой проверкой

**Сервис nginx:**
- **`image: nginx:alpine`**: Готовый образ Nginx
  - **Описание**: Использует Alpine Linux версию Nginx
  - **Размер**: ~15MB (компактный образ)
- **`ports`**: Проброс портов
  - **`"80:80"`**: HTTP порт
  - **`"443:443"`**: HTTPS порт
- **`volumes`**: Монтирование конфигурации
  - **`./nginx.conf:/etc/nginx/nginx.conf`**: Конфигурация Nginx
  - **`./ssl:/etc/nginx/ssl`**: SSL сертификаты
- **`depends_on`**: Зависимости
  - **`autogluon-api`**: Nginx запускается после API сервиса

**Сервис redis:**
- **`image: redis:alpine`**: Готовый образ Redis
  - **Описание**: Использует Alpine Linux версию Redis
  - **Размер**: ~7MB (компактный образ)
- **`volumes`**: Постоянное хранение
  - **`redis_data:/data`**: Именованный том для данных Redis

**Тома:**
- **`redis_data`**: Именованный том
  - **Описание**: Создает постоянный том для данных Redis
  - **Преимущества**: Данные сохраняются при перезапуске контейнеров

## Kubernetes деплой

### Deployment манифест

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: autogluon-api
  labels:
    app: autogluon-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: autogluon-api
  template:
    metadata:
      labels:
        app: autogluon-api
    spec:
      containers:
      - name: autogluon-api
        image: autogluon-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: MODEL_PATH
          value: "/app/models"
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: model-storage
          mountPath: /app/models
        - name: log-storage
          mountPath: /app/logs
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
      - name: log-storage
        persistentVolumeClaim:
          claimName: log-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: autogluon-api-service
spec:
  selector:
    app: autogluon-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: log-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

**🔧 Детальное описание параметров Kubernetes деплоя:**

**Deployment манифест:**
- **`apiVersion: apps/v1`**: Версия API
  - **Описание**: Использует стабильную версию API для Deployment
- **`kind: Deployment`**: Тип ресурса
  - **Описание**: Создает Deployment для управления подами
- **`metadata.name`**: Имя Deployment
  - **Описание**: Уникальное имя для идентификации
- **`spec.replicas: 3`**: Количество реплик
  - **Описание**: Создает 3 копии приложения
  - **Преимущества**: Высокая доступность и нагрузочная способность
- **`spec.selector.matchLabels`**: Селектор подов
  - **Описание**: Выбирает поды с соответствующими метками
- **`spec.template`**: Шаблон пода
  - **Описание**: Определяет конфигурацию подов

**Контейнер:**
- **`name: autogluon-api`**: Имя контейнера
  - **Описание**: Уникальное имя контейнера в поде
- **`image: autogluon-api:latest`**: Образ контейнера
  - **Описание**: Docker образ для запуска
  - **Рекомендации**: Используйте конкретные теги версий вместо latest
- **`ports.containerPort: 8000`**: Порт контейнера
  - **Описание**: Порт, который слушает приложение
- **`env`**: Переменные окружения
  - **`MODEL_PATH`**: Путь к моделям в контейнере
  - **`LOG_LEVEL`**: Уровень логирования

**Ресурсы:**
- **`resources.requests`**: Минимальные ресурсы
  - **`memory: "1Gi"`**: Минимум 1GB RAM
  - **`cpu: "500m"`**: Минимум 0.5 CPU
- **`resources.limits`**: Максимальные ресурсы
  - **`memory: "2Gi"`**: Максимум 2GB RAM
  - **`cpu: "1000m"`**: Максимум 1 CPU

**Проверки здоровья:**
- **`livenessProbe`**: Проверка жизнеспособности
  - **`httpGet`**: HTTP запрос для проверки
  - **`path: /health`**: Путь для проверки
  - **`port: 8000`**: Порт для проверки
  - **`initialDelaySeconds: 30`**: Задержка перед первой проверкой
  - **`periodSeconds: 10`**: Интервал проверки
- **`readinessProbe`**: Проверка готовности
  - **Описание**: Проверяет, готов ли контейнер принимать трафик
  - **`initialDelaySeconds: 5`**: Быстрая проверка готовности

**Тома:**
- **`volumeMounts`**: Монтирование томов в контейнер
  - **`model-storage`**: Том для моделей
  - **`log-storage`**: Том для логов
- **`volumes`**: Определение томов
  - **`persistentVolumeClaim`**: Использование PVC для постоянного хранения

**Service:**
- **`kind: Service`**: Тип ресурса
  - **Описание**: Создает сервис для доступа к подам
- **`spec.selector`**: Селектор подов
  - **Описание**: Выбирает поды для балансировки нагрузки
- **`spec.ports`**: Проброс портов
  - **`port: 80`**: Внешний порт
  - **`targetPort: 8000`**: Порт контейнера
- **`type: LoadBalancer`**: Тип сервиса
  - **Описание**: Создает внешний LoadBalancer

**PersistentVolumeClaim:**
- **`kind: PersistentVolumeClaim`**: Тип ресурса
  - **Описание**: Запрос на постоянное хранилище
- **`spec.accessModes`**: Режимы доступа
  - **`ReadWriteOnce`**: Чтение/запись одним узлом
- **`spec.resources.requests.storage`**: Размер хранилища
  - **`10Gi`**: 10GB для моделей
  - **`5Gi`**: 5GB для логов

## Мониторинг и логирование

<img src="images/optimized/advanced_production_flow.png" alt="Мониторинг и логирование" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 4: Система мониторинга и логирования в продакшене*

**Почему критически важен мониторинг ML-моделей?** Потому что модели могут деградировать со временем:

- **Детекция дрейфа**: Изменение распределения входных данных
- **Мониторинг производительности**: Отслеживание скорости и точности
- **Алертинг**: Уведомления о проблемах в реальном времени
- **Логирование**: Детальная информация для отладки
- **Метрики бизнеса**: Связь технических метрик с бизнес-результатами
- **Автоматическое восстановление**: Реагирование на проблемы без вмешательства человека

### Система мониторинга

```python
import logging
import time
from datetime import datetime
import psutil
import requests
from typing import Dict, Any

class ProductionMonitor:
    """Мониторинг продакшен системы"""
    
    def __init__(self, log_file='production.log'):
        self.log_file = log_file
        self.setup_logging()
        self.metrics = {}
    
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_prediction(self, input_data: Dict, prediction: Any, 
                      processing_time: float, model_info: Dict):
        """Логирование предсказания"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'input_data': input_data,
            'prediction': prediction,
            'processing_time': processing_time,
            'model_info': model_info
        }
        self.logger.info(f"Prediction: {log_entry}")
    
    def log_error(self, error: Exception, context: Dict):
        """Логирование ошибок"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error': str(error),
            'context': context,
            'traceback': traceback.format_exc()
        }
        self.logger.error(f"Error: {error_entry}")
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Получение системных метрик"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'timestamp': datetime.now().isoformat()
        }
    
    def check_model_health(self, model) -> Dict[str, Any]:
        """Проверка здоровья модели"""
        try:
            # Тестовое предсказание
            test_data = pd.DataFrame({'feature1': [1.0], 'feature2': [2.0]})
            start_time = time.time()
            prediction = model.predict(test_data)
            processing_time = time.time() - start_time
            
            return {
                'status': 'healthy',
                'processing_time': processing_time,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
```

**🔧 Детальное описание параметров системы мониторинга:**

**Класс ProductionMonitor:**
- **Назначение**: Мониторинг продакшен системы AutoML Gluon
- **Параметры конструктора**:
  - **`log_file`**: Путь к файлу логов
    - **Тип**: str
    - **По умолчанию**: 'production.log'
    - **Описание**: Файл для записи логов мониторинга

**Метод setup_logging():**
- **Назначение**: Настройка системы логирования
- **Параметры logging.basicConfig():**
  - **`level=logging.INFO`**: Уровень логирования
    - **Тип**: int
    - **Значения**: DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
    - **Описание**: Логирует сообщения уровня INFO и выше
  - **`format`**: Формат логов
    - **Тип**: str
    - **Описание**: Шаблон для форматирования логов
    - **Компоненты**: время, имя логгера, уровень, сообщение
  - **`handlers`**: Обработчики логов
    - **`FileHandler`**: Запись в файл
    - **`StreamHandler`**: Вывод в консоль

**Метод log_prediction():**
- **Назначение**: Логирование предсказаний модели
- **Параметры**:
  - **`input_data`**: Входные данные
    - **Тип**: Dict
    - **Описание**: Данные, поданные на вход модели
  - **`prediction`**: Предсказание модели
    - **Тип**: Any
    - **Описание**: Результат предсказания
  - **`processing_time`**: Время обработки
    - **Тип**: float
    - **Описание**: Время выполнения предсказания в секундах
  - **`model_info`**: Информация о модели
    - **Тип**: Dict
    - **Описание**: Метаданные о модели

**Метод log_error():**
- **Назначение**: Логирование ошибок системы
- **Параметры**:
  - **`error`**: Исключение
    - **Тип**: Exception
    - **Описание**: Ошибка, которая произошла
  - **`context`**: Контекст ошибки
    - **Тип**: Dict
    - **Описание**: Дополнительная информация об ошибке

**Метод get_system_metrics():**
- **Назначение**: Получение системных метрик
- **Возвращаемое значение**: Dict[str, Any] - системные метрики
- **Метрики**:
  - **`cpu_percent`**: Загрузка CPU
    - **Тип**: float
    - **Диапазон**: 0.0-100.0
    - **Описание**: Процент использования CPU
  - **`memory_percent`**: Использование памяти
    - **Тип**: float
    - **Диапазон**: 0.0-100.0
    - **Описание**: Процент использования RAM
  - **`disk_percent`**: Использование диска
    - **Тип**: float
    - **Диапазон**: 0.0-100.0
    - **Описание**: Процент использования диска
  - **`timestamp`**: Время измерения
    - **Тип**: str
    - **Описание**: ISO формат времени

**Метод check_model_health():**
- **Назначение**: Проверка здоровья модели
- **Параметры**:
  - **`model`**: Модель для проверки
    - **Тип**: TabularPredictor
    - **Описание**: Модель AutoGluon для тестирования
- **Возвращаемое значение**: Dict[str, Any] - статус здоровья
- **Структура результата**:
  - **`status`**: Статус модели
    - **Тип**: str
    - **Значения**: 'healthy', 'unhealthy'
  - **`processing_time`**: Время обработки тестового запроса
    - **Тип**: float
    - **Описание**: Время выполнения тестового предсказания
  - **`error`**: Описание ошибки (если есть)
    - **Тип**: str
    - **Описание**: Текст ошибки при неудачной проверке

### Алерты и уведомления

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

class AlertSystem:
    """Система алертов для продакшена"""
    
    def __init__(self, smtp_server, smtp_port, email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
    def send_email_alert(self, subject: str, message: str, recipients: list):
        """Отправка email алерта"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email alert sent to {recipients}")
        except Exception as e:
            print(f"Failed to send email alert: {e}")
    
    def send_slack_alert(self, webhook_url: str, message: str):
        """Отправка Slack алерта"""
        try:
            payload = {
                "text": message,
                "username": "AutoML Gluon Monitor",
                "icon_emoji": ":robot_face:"
            }
            
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            
            print("Slack alert sent successfully")
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")
    
    def check_performance_thresholds(self, metrics: Dict[str, float], 
                                   thresholds: Dict[str, float]):
        """Проверка пороговых значений производительности"""
        alerts = []
        
        for metric, threshold in thresholds.items():
            if metric in metrics and metrics[metric] < threshold:
                alerts.append(f"{metric} is below threshold: {metrics[metric]} < {threshold}")
        
        return alerts
```

**🔧 Детальное описание параметров системы алертов:**

**Класс AlertSystem:**
- **Назначение**: Система уведомлений для продакшен мониторинга
- **Параметры конструктора**:
  - **`smtp_server`**: SMTP сервер
    - **Тип**: str
    - **Описание**: Адрес SMTP сервера для отправки email
    - **Примеры**: 'smtp.gmail.com', 'smtp.yandex.ru'
  - **`smtp_port`**: Порт SMTP сервера
    - **Тип**: int
    - **По умолчанию**: 587 (TLS), 465 (SSL)
    - **Описание**: Порт для подключения к SMTP серверу
  - **`email`**: Email отправителя
    - **Тип**: str
    - **Описание**: Email адрес для отправки уведомлений
  - **`password`**: Пароль email
    - **Тип**: str
    - **Описание**: Пароль для аутентификации на SMTP сервере

**Метод send_email_alert():**
- **Назначение**: Отправка email уведомлений
- **Параметры**:
  - **`subject`**: Тема письма
    - **Тип**: str
    - **Описание**: Заголовок email уведомления
    - **Примеры**: "Model Performance Alert", "System Health Warning"
  - **`message`**: Текст сообщения
    - **Тип**: str
    - **Описание**: Содержимое email уведомления
  - **`recipients`**: Список получателей
    - **Тип**: list
    - **Описание**: Список email адресов получателей
    - **Пример**: ['admin@company.com', 'devops@company.com']

**Метод send_slack_alert():**
- **Назначение**: Отправка уведомлений в Slack
- **Параметры**:
  - **`webhook_url`**: URL webhook
    - **Тип**: str
    - **Описание**: URL Slack webhook для отправки сообщений
    - **Формат**: https://hooks.slack.com/services/...
  - **`message`**: Текст сообщения
    - **Тип**: str
    - **Описание**: Содержимое Slack уведомления
- **Структура payload**:
  - **`text`**: Текст сообщения
  - **`username`**: Имя отправителя
  - **`icon_emoji`**: Иконка отправителя

**Метод check_performance_thresholds():**
- **Назначение**: Проверка пороговых значений метрик
- **Параметры**:
  - **`metrics`**: Текущие метрики
    - **Тип**: Dict[str, float]
    - **Описание**: Словарь с текущими значениями метрик
    - **Пример**: {'accuracy': 0.85, 'response_time': 0.5}
  - **`thresholds`**: Пороговые значения
    - **Тип**: Dict[str, float]
    - **Описание**: Словарь с минимальными значениями метрик
    - **Пример**: {'accuracy': 0.90, 'response_time': 1.0}
- **Возвращаемое значение**: list - список алертов
- **Логика проверки**:
  - Сравнивает текущие метрики с пороговыми значениями
  - Создает алерт, если метрика ниже порога
  - Возвращает список строк с описанием проблем

## Масштабирование

<img src="images/optimized/production_comparison.png" alt="Масштабирование ML-систем" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 5: Стратегии масштабирования ML-систем*

**Почему важно правильное масштабирование ML-систем?** Потому что ML-модели имеют уникальные требования к ресурсам:

- **Горизонтальное масштабирование**: Добавление новых серверов для обработки нагрузки
- **Вертикальное масштабирование**: Увеличение ресурсов существующих серверов
- **Автоматическое масштабирование**: Динамическое изменение ресурсов по нагрузке
- **Балансировка нагрузки**: Равномерное распределение запросов между серверами
- **Кэширование**: Сохранение результатов для ускорения ответов
- **Асинхронная обработка**: Неблокирующая обработка запросов

### Горизонтальное масштабирование

```python
# Настройка для горизонтального масштабирования
import asyncio
from concurrent.futures import ThreadPoolExecutor
import queue
import threading

class ScalablePredictionService:
    """Масштабируемый сервис предсказаний"""
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.request_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
    async def process_prediction(self, data: Dict) -> Dict:
        """Асинхронная обработка предсказания"""
        loop = asyncio.get_event_loop()
        
        # Выполнение предсказания в отдельном потоке
        result = await loop.run_in_executor(
            self.executor, 
            self._predict_sync, 
            data
        )
        
        return result
    
    def _predict_sync(self, data: Dict) -> Dict:
        """Синхронное предсказание"""
        # Ваша логика предсказания
        pass
    
    def batch_predict(self, batch_data: List[Dict]) -> List[Dict]:
        """Пакетная обработка предсказаний"""
        results = []
        
        # Разделение на батчи
        batch_size = 100
        for i in range(0, len(batch_data), batch_size):
            batch = batch_data[i:i+batch_size]
            
            # Параллельная обработка батча
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self._predict_sync, data) for data in batch]
                batch_results = [future.result() for future in futures]
                results.extend(batch_results)
        
        return results
```

**🔧 Детальное описание параметров масштабирования:**

**Класс ScalablePredictionService:**
- **Назначение**: Масштабируемый сервис для обработки предсказаний
- **Параметры конструктора**:
  - **`max_workers`**: Максимальное количество потоков
    - **Тип**: int
    - **По умолчанию**: 4
    - **Диапазон значений**: `[1, 32]` (рекомендуется 2-16)
    - **Описание**: Количество параллельных потоков для обработки
    - **Рекомендации**: Используйте количество CPU ядер × 2

**Метод process_prediction():**
- **Назначение**: Асинхронная обработка предсказания
- **Параметры**:
  - **`data`**: Данные для предсказания
    - **Тип**: Dict
    - **Описание**: Входные данные для модели
- **Возвращаемое значение**: Dict - результат предсказания
- **Особенности**:
  - **Асинхронность**: Не блокирует основной поток
  - **Параллельность**: Использует отдельный поток для вычислений
  - **Масштабируемость**: Поддерживает множественные запросы

**Метод _predict_sync():**
- **Назначение**: Синхронное выполнение предсказания
- **Параметры**:
  - **`data`**: Данные для предсказания
    - **Тип**: Dict
    - **Описание**: Входные данные для модели
- **Возвращаемое значение**: Dict - результат предсказания
- **Особенности**:
  - **Синхронность**: Блокирующее выполнение
  - **Потокобезопасность**: Может выполняться в разных потоках
  - **Производительность**: Оптимизирован для быстрого выполнения

**Метод batch_predict():**
- **Назначение**: Пакетная обработка множественных предсказаний
- **Параметры**:
  - **`batch_data`**: Список данных для предсказания
    - **Тип**: List[Dict]
    - **Описание**: Список входных данных
- **Возвращаемое значение**: List[Dict] - список результатов
- **Параметры обработки**:
  - **`batch_size`**: Размер батча
    - **Тип**: int
    - **По умолчанию**: 100
    - **Диапазон значений**: `[10, 1000]` (рекомендуется 50-200)
    - **Описание**: Количество запросов в одном батче
- **Особенности**:
  - **Пакетная обработка**: Группирует запросы для эффективности
  - **Параллельность**: Обрабатывает батчи параллельно
  - **Память**: Контролирует использование памяти через размер батча

### Кэширование

```python
import redis
import json
import hashlib
from typing import Any, Optional

class PredictionCache:
    """Кэш для предсказаний"""
    
    def __init__(self, redis_host='localhost', redis_port=6379, ttl=3600):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.ttl = ttl
    
    def _generate_cache_key(self, data: Dict) -> str:
        """Генерация ключа кэша"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get_prediction(self, data: Dict) -> Optional[Dict]:
        """Получение предсказания из кэша"""
        cache_key = self._generate_cache_key(data)
        cached_result = self.redis_client.get(cache_key)
        
        if cached_result:
            return json.loads(cached_result)
        
        return None
    
    def set_prediction(self, data: Dict, prediction: Dict):
        """Сохранение предсказания в кэш"""
        cache_key = self._generate_cache_key(data)
        self.redis_client.setex(
            cache_key, 
            self.ttl, 
            json.dumps(prediction)
        )
    
    def invalidate_cache(self, pattern: str = "*"):
        """Очистка кэша"""
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)
```

**🔧 Детальное описание параметров кэширования:**

**Класс PredictionCache:**
- **Назначение**: Кэширование предсказаний для ускорения ответов
- **Параметры конструктора**:
  - **`redis_host`**: Хост Redis сервера
    - **Тип**: str
    - **По умолчанию**: 'localhost'
    - **Описание**: Адрес Redis сервера для кэширования
  - **`redis_port`**: Порт Redis сервера
    - **Тип**: int
    - **По умолчанию**: 6379
    - **Описание**: Порт для подключения к Redis
  - **`ttl`**: Время жизни кэша
    - **Тип**: int
    - **По умолчанию**: 3600 (1 час)
    - **Диапазон значений**: `[60, 86400]` (1 минута - 24 часа)
    - **Описание**: Время в секундах, через которое кэш истекает

**Метод _generate_cache_key():**
- **Назначение**: Генерация уникального ключа для кэша
- **Параметры**:
  - **`data`**: Данные для предсказания
    - **Тип**: Dict
    - **Описание**: Входные данные для генерации ключа
- **Возвращаемое значение**: str - MD5 хеш ключа
- **Алгоритм**:
  - Сериализует данные в JSON с сортировкой ключей
  - Создает MD5 хеш от строки данных
  - Возвращает 32-символьный хеш

**Метод get_prediction():**
- **Назначение**: Получение предсказания из кэша
- **Параметры**:
  - **`data`**: Данные для поиска
    - **Тип**: Dict
    - **Описание**: Входные данные для поиска в кэше
- **Возвращаемое значение**: Optional[Dict] - результат из кэша или None
- **Логика работы**:
  - Генерирует ключ кэша из данных
  - Ищет значение в Redis
  - Десериализует JSON в словарь
  - Возвращает None, если ключ не найден

**Метод set_prediction():**
- **Назначение**: Сохранение предсказания в кэш
- **Параметры**:
  - **`data`**: Входные данные
    - **Тип**: Dict
    - **Описание**: Данные для генерации ключа
  - **`prediction`**: Результат предсказания
    - **Тип**: Dict
    - **Описание**: Предсказание для сохранения
- **Особенности**:
  - Использует `setex` для установки TTL
  - Сериализует предсказание в JSON
  - Автоматически истекает через TTL

**Метод invalidate_cache():**
- **Назначение**: Очистка кэша
- **Параметры**:
  - **`pattern`**: Паттерн для поиска ключей
    - **Тип**: str
    - **По умолчанию**: "*" (все ключи)
    - **Описание**: Паттерн для поиска ключей в Redis
    - **Примеры**: "*", "prediction:*", "model_v1:*"
- **Особенности**:
  - Использует `keys()` для поиска ключей
  - Удаляет все найденные ключи
  - Поддерживает wildcard паттерны

## Безопасность

### Аутентификация и авторизация

```python
from functools import wraps
import jwt
from datetime import datetime, timedelta
import secrets

class SecurityManager:
    """Менеджер безопасности"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.api_keys = {}
    
    def generate_api_key(self, user_id: str) -> str:
        """Генерация API ключа"""
        api_key = secrets.token_urlsafe(32)
        self.api_keys[api_key] = {
            'user_id': user_id,
            'created_at': datetime.now(),
            'permissions': ['predict', 'model_info']
        }
        return api_key
    
    def validate_api_key(self, api_key: str) -> bool:
        """Валидация API ключа"""
        return api_key in self.api_keys
    
    def get_user_permissions(self, api_key: str) -> list:
        """Получение разрешений пользователя"""
        if api_key in self.api_keys:
            return self.api_keys[api_key]['permissions']
        return []
    
    def require_auth(self, permissions: list = None):
        """Декоратор для проверки аутентификации"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Проверка API ключа
                api_key = request.headers.get('X-API-Key')
                if not api_key or not self.validate_api_key(api_key):
                    return jsonify({'error': 'Invalid API key'}), 401
                
                # Проверка разрешений
                if permissions:
                    user_permissions = self.get_user_permissions(api_key)
                    if not any(perm in user_permissions for perm in permissions):
                        return jsonify({'error': 'Insufficient permissions'}), 403
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
```

### Валидация входных данных

```python
from pydantic import BaseModel, validator
from typing import List, Dict, Any, Union
import numpy as np

class InputValidator:
    """Валидатор входных данных"""
    
    def __init__(self, feature_schema: Dict[str, Any]):
        self.feature_schema = feature_schema
    
    def validate_input(self, data: List[Dict[str, Any]]) -> bool:
        """Валидация входных данных"""
        try:
            for record in data:
                # Проверка наличия всех обязательных признаков
                for feature, schema in self.feature_schema.items():
                    if feature not in record:
                        raise ValueError(f"Missing required feature: {feature}")
                    
                    # Проверка типа данных
                    if not isinstance(record[feature], schema['type']):
                        raise ValueError(f"Invalid type for feature {feature}")
                    
                    # Проверка диапазона значений
                    if 'min' in schema and record[feature] < schema['min']:
                        raise ValueError(f"Value too small for feature {feature}")
                    
                    if 'max' in schema and record[feature] > schema['max']:
                        raise ValueError(f"Value too large for feature {feature}")
            
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False
    
    def sanitize_input(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Очистка входных данных"""
        sanitized_data = []
        
        for record in data:
            sanitized_record = {}
            for feature, value in record.items():
                # Очистка от потенциально опасных символов
                if isinstance(value, str):
                    sanitized_record[feature] = value.strip()
                else:
                    sanitized_record[feature] = value
            
            sanitized_data.append(sanitized_record)
        
        return sanitized_data
```

## Тестирование продакшен системы

### Нагрузочное тестирование

```python
import asyncio
import aiohttp
import time
from typing import List, Dict, Any
import statistics

class LoadTester:
    """Нагрузочное тестирование API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []
    
    async def single_request(self, session: aiohttp.ClientSession, 
                           data: Dict[str, Any]) -> Dict[str, Any]:
        """Одиночный запрос"""
        start_time = time.time()
        
        try:
            async with session.post(
                f"{self.base_url}/predict",
                json={"data": [data]}
            ) as response:
                result = await response.json()
                processing_time = time.time() - start_time
                
                return {
                    'status_code': response.status,
                    'processing_time': processing_time,
                    'success': response.status == 200,
                    'result': result
                }
        except Exception as e:
            return {
                'status_code': 0,
                'processing_time': time.time() - start_time,
                'success': False,
                'error': str(e)
            }
    
    async def load_test(self, concurrent_users: int, 
                       requests_per_user: int, 
                       test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Нагрузочное тестирование"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for user in range(concurrent_users):
                for request in range(requests_per_user):
                    data = test_data[request % len(test_data)]
                    task = self.single_request(session, data)
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks)
        
        # Анализ результатов
        successful_requests = [r for r in results if r['success']]
        failed_requests = [r for r in results if not r['success']]
        
        processing_times = [r['processing_time'] for r in successful_requests]
        
        return {
            'total_requests': len(results),
            'successful_requests': len(successful_requests),
            'failed_requests': len(failed_requests),
            'success_rate': len(successful_requests) / len(results),
            'avg_processing_time': statistics.mean(processing_times),
            'min_processing_time': min(processing_times),
            'max_processing_time': max(processing_times),
            'p95_processing_time': statistics.quantiles(processing_times, n=20)[18]
        }
```

## Лучшие практики продакшена

<img src="images/optimized/retraining_workflow.png" alt="Лучшие практики продакшена" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 6: Лучшие практики и рекомендации для продакшена ML-моделей*

**Почему важны лучшие практики продакшена?** Потому что они помогают избежать типичных ошибок и обеспечить надежность:

- **Планирование**: Тщательное планирование архитектуры и ресурсов
- **Тестирование**: Комплексное тестирование перед деплоем
- **Мониторинг**: Непрерывный мониторинг качества и производительности
- **Документация**: Подробная документация для команды
- **Безопасность**: Защита данных и моделей
- **Версионирование**: Контроль версий моделей и кода
- **Откат**: Возможность быстрого отката при проблемах

### 🎯 Ключевые принципы успешного продакшена

**Почему следуют лучшим практикам?** Потому что они проверены временем и помогают избежать проблем:

- **Принцип "Fail Fast"**: Быстрое обнаружение и исправление проблем
- **Принцип "Graceful Degradation"**: Плавное снижение функциональности при сбоях
- **Принцип "Observability"**: Полная видимость состояния системы
- **Принцип "Automation"**: Автоматизация рутинных процессов
- **Принцип "Security by Design"**: Безопасность с самого начала
- **Принцип "Continuous Improvement"**: Постоянное улучшение системы

## Следующие шаги

После освоения продакшен деплоя переходите к:
- [Переобучению моделей](./07_retraining.md)
- [Лучшим практикам](./08_best_practices.md)
- [Примерам использования](./09_examples.md)
