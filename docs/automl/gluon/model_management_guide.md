# 📦 Руководство по управлению моделями AutoGluon

## 🎯 Обзор

AutoGluon создает множество файлов моделей при обучении. Это руководство поможет вам эффективно управлять этими файлами.

## 📁 Структура файлов моделей

### Основные файлы (НЕ удалять):
```
models/autogluon/
├── predictor.pkl          # Главный объект предсказателя
├── learner.pkl            # Объект обучения
├── metadata.json          # Метаданные модели
├── version.txt            # Версия AutoGluon
└── models/                # Папка с обученными моделями
    ├── WeightedEnsemble_L2_FULL/    # Лучшая модель
    ├── RandomForest_r*_BAG_L1/      # RandomForest модели
    ├── ExtraTrees_r*_BAG_L1/        # ExtraTrees модели
    ├── CatBoost_r*_BAG_L1/          # CatBoost модели
    ├── LightGBM_r*_BAG_L1/          # LightGBM модели
    ├── NeuralNetTorch_r*_BAG_L1/    # Neural Network модели
    └── XGBoost_r*_BAG_L1/           # XGBoost модели
```

## 🚀 Быстрые действия

### 1. Архивирование старых моделей
```bash
# Использовать скрипт управления
python examples/automl/gluon/model_management.py

# Или вручную
mkdir -p models/autogluon/archived_models
mv models/autogluon/models/* models/autogluon/archived_models/
```

### 2. Очистка кэша
```bash
# Удалить кэшированные данные
rm -rf models/autogluon/utils/
```

### 3. Полная очистка для переобучения
```bash
# Удалить все модели
rm -rf models/autogluon/
```

## 📊 Анализ размера моделей

### Типичные размеры:
- **Полная модель**: 50-200 MB
- **Только лучшая модель**: 5-20 MB
- **Архив**: 100-500 MB

### Проверка размера:
```python
import os

def get_folder_size(folder_path):
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    return total_size / (1024 * 1024)  # MB

size_mb = get_folder_size("models/autogluon/")
print(f"Размер модели: {size_mb:.2f} MB")
```

## 🔄 Стратегии управления

### Стратегия 1: Минимальная (рекомендуется)
- Оставить только `WeightedEnsemble_L2_FULL`
- Архивировать остальные модели
- Размер: ~10-20 MB

### Стратегия 2: Полная
- Сохранить все модели
- Использовать для анализа
- Размер: ~100-200 MB

### Стратегия 3: Архивная
- Архивировать все модели
- Оставить только метаданные
- Размер: ~1-5 MB

## 🛠️ Автоматизация

### Скрипт управления моделями:
```python
from examples.automl.gluon.model_management import AutoGluonModelManager

manager = AutoGluonModelManager()

# Архивировать старые модели
manager.archive_old_models(keep_best=True)

# Очистить кэш
manager.clean_utils_cache()

# Получить размер
size_mb = manager.get_model_size()
```

### Планировщик задач (cron):
```bash
# Еженедельная очистка кэша
0 2 * * 0 cd /path/to/project && python examples/automl/gluon/model_management.py

# Ежемесячное архивирование
0 3 1 * * cd /path/to/project && python examples/automl/gluon/model_management.py
```

## ⚠️ Важные предупреждения

### НЕ удаляйте:
- `predictor.pkl` - основной файл модели
- `learner.pkl` - объект обучения
- `metadata.json` - конфигурация модели
- `WeightedEnsemble_L2_FULL/` - лучшая модель

### Можно удалить:
- `utils/` - кэшированные данные
- Старые модели в `models/`
- Архивные папки

## 🔍 Диагностика проблем

### Модель не загружается:
```python
# Проверить наличие основных файлов
import os
required_files = ['predictor.pkl', 'learner.pkl', 'metadata.json']
for file in required_files:
    if not os.path.exists(f"models/autogluon/{file}"):
        print(f"❌ Отсутствует: {file}")
```

### Большой размер модели:
```bash
# Найти самые большие файлы
find models/autogluon/ -name "*.pkl" -exec ls -lh {} \; | sort -k5 -hr | head -10
```

### Ошибки загрузки:
```python
# Проверить версию AutoGluon
with open("models/autogluon/version.txt", "r") as f:
    version = f.read().strip()
print(f"Версия AutoGluon: {version}")
```

## 📈 Мониторинг

### Отслеживание размера:
```python
import time
import json
from datetime import datetime

def log_model_size():
    size_mb = get_folder_size("models/autogluon/")
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "size_mb": size_mb
    }
    
    with open("logs/model_size.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

### Алерты при превышении лимита:
```python
MAX_SIZE_MB = 500  # Максимальный размер модели

if size_mb > MAX_SIZE_MB:
    print(f"⚠️ Размер модели превышен: {size_mb:.2f} MB > {MAX_SIZE_MB} MB")
    print("Рекомендуется архивирование старых моделей")
```

## 🎯 Рекомендации

1. **Регулярно архивируйте** старые модели
2. **Мониторьте размер** модели
3. **Очищайте кэш** после обучения
4. **Используйте автоматизацию** для управления
5. **Документируйте** изменения в моделях

## 📚 Дополнительные ресурсы

- [AutoGluon Documentation](https://auto.gluon.ai/)
- [Model Management Best Practices](https://docs.auto.gluon.ai/stable/tutorials/tabular/tabular-prediction.html)
- [Production Deployment Guide](https://docs.auto.gluon.ai/stable/tutorials/tabular/tabular-prediction.html#saving-and-loading-models)
