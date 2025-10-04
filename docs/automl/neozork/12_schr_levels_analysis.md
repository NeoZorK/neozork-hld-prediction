# 12. Анализ SCHR Levels - Создание высокоточной ML-модели

**Цель:** Максимально использовать индикатор SCHR Levels для создания робастной и прибыльной ML-модели с точностью более 95%.

## Что такое SCHR Levels?

**Теория:** SCHR Levels представляет собой революционный подход к анализу уровней поддержки и сопротивления, основанный на алгоритмическом анализе рыночного давления и предсказании будущих ценовых уровней. Это не просто статичные уровни, а динамическая система, которая адаптируется к изменениям рыночных условий.

### Определение и принцип работы

**Теория:** SCHR Levels основан на принципе анализа рыночного давления и его влияния на ценовые уровни. Это позволяет не только определять текущие уровни поддержки и сопротивления, но и предсказывать будущие максимумы и минимумы с высокой точностью.

**SCHR Levels** - это продвинутый индикатор уровней поддержки и сопротивления, который использует алгоритмический анализ для определения ключевых ценовых уровней. В отличие от простых уровней, SCHR Levels учитывает давление на уровни и предсказывает будущие максимумы и минимумы.

**Почему SCHR Levels превосходит традиционные уровни:**
- **Алгоритмический анализ:** Использует сложные алгоритмы для анализа уровней
- **Учет давления:** Анализирует давление на уровни для предсказания пробоев
- **Предсказание будущего:** Предсказывает будущие максимумы и минимумы
- **Адаптивность:** Адаптируется к изменениям рыночных условий

**Плюсы:**
- Высокая точность предсказаний
- Учет рыночного давления
- Предсказание будущих уровней
- Адаптивность к изменениям

**Минусы:**
- Сложность настройки параметров
- Высокие требования к вычислительным ресурсам
- Необходимость глубокого понимания теории

### Ключевые особенности SCHR Levels

**Теория:** Ключевые особенности SCHR Levels определяют его уникальные возможности для анализа рыночных уровней. Каждый параметр имеет теоретическое обоснование и практическое применение для различных рыночных условий.

**Почему эти особенности критичны:**
- **Анализ давления:** Критически важно для предсказания пробоев уровней
- **Сила уровней:** Определяет надежность уровней поддержки и сопротивления
- **Горизонт предсказания:** Влияет на точность предсказаний
- **Фактор волатильности:** Учитывает волатильность рынка
- **Вес тренда:** Балансирует влияние тренда на уровни

**Практическая реализация:** Класс `SCHRLevelsAnalyzer` представляет собой основу для анализа SCHR Levels с настраиваемыми параметрами. Каждый параметр имеет специфическое назначение и влияет на точность анализа уровней.

**Детальное объяснение параметров:**
- **pressure_threshold (0.7):** Минимальное значение давления, при котором уровень считается значимым. Более высокие значения дают более консервативные сигналы, но могут пропустить слабые, но важные уровни.
- **level_strength (0.8):** Минимальная сила уровня для его валидации. Определяет, насколько сильным должен быть уровень, чтобы считаться надежным.
- **prediction_horizon (20):** Количество периодов вперед для предсказания. Большие значения дают более долгосрочные прогнозы, но с меньшей точностью.
- **volatility_factor (1.5):** Множитель волатильности для адаптации к рыночным условиям. Высокие значения лучше подходят для волатильных рынков.
- **trend_weight (0.6):** Вес трендового компонента в анализе. Балансирует влияние тренда и уровней на финальное решение.

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class SCHRLevelsAnalyzer:
    """
    Анализатор SCHR Levels для определения уровней поддержки и сопротивления.
    
    Этот класс реализует алгоритмический анализ рыночного давления для создания
    высокоточных предсказаний уровней поддержки и сопротивления.
    """
    
    def __init__(self, 
                 pressure_threshold: float = 0.7,
                 level_strength: float = 0.8,
                 prediction_horizon: int = 20,
                 volatility_factor: float = 1.5,
                 trend_weight: float = 0.6):
        """
        Инициализация анализатора SCHR Levels.
        
        Args:
            pressure_threshold: Минимальное давление для валидации уровня (0.0-1.0)
            level_strength: Минимальная сила уровня (0.0-1.0)
            prediction_horizon: Горизонт предсказания в периодах
            volatility_factor: Фактор адаптации к волатильности
            trend_weight: Вес трендового компонента (0.0-1.0)
        """
        self.parameters = {
            'pressure_threshold': pressure_threshold,
            'level_strength': level_strength,
            'prediction_horizon': prediction_horizon,
            'volatility_factor': volatility_factor,
            'trend_weight': trend_weight
        }
        
        # Валидация параметров
        self._validate_parameters()
        
        # История расчетов для анализа
        self.calculation_history = []
        
    def _validate_parameters(self):
        """Валидация входных параметров"""
        if not 0.0 <= self.parameters['pressure_threshold'] <= 1.0:
            raise ValueError("pressure_threshold должен быть между 0.0 и 1.0")
        if not 0.0 <= self.parameters['level_strength'] <= 1.0:
            raise ValueError("level_strength должен быть между 0.0 и 1.0")
        if self.parameters['prediction_horizon'] <= 0:
            raise ValueError("prediction_horizon должен быть положительным")
        if self.parameters['volatility_factor'] <= 0:
            raise ValueError("volatility_factor должен быть положительным")
        if not 0.0 <= self.parameters['trend_weight'] <= 1.0:
            raise ValueError("trend_weight должен быть между 0.0 и 1.0")
    
    def analyze_levels(self, data: pd.DataFrame) -> Dict:
        """
        Основной метод анализа SCHR Levels.
        
        Args:
            data: DataFrame с OHLCV данными и SCHR колонками
            
        Returns:
            Dict с результатами анализа уровней
        """
        try:
            # Проверка наличия необходимых колонок
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                raise ValueError(f"Отсутствуют колонки: {missing_columns}")
            
            # Расчет уровней
            levels = self._calculate_levels(data)
            
            # Анализ давления
            pressure_analysis = self._analyze_pressure(data, levels)
            
            # Предсказание будущих уровней
            predictions = self._predict_future_levels(data, levels)
            
            # Сохранение результатов
            result = {
                'levels': levels,
                'pressure_analysis': pressure_analysis,
                'predictions': predictions,
                'parameters': self.parameters.copy(),
                'timestamp': pd.Timestamp.now()
            }
            
            self.calculation_history.append(result)
            return result
            
        except Exception as e:
            print(f"Ошибка в анализе SCHR Levels: {e}")
            return None
    
    def _calculate_levels(self, data: pd.DataFrame) -> Dict:
        """Расчет базовых уровней поддержки и сопротивления"""
        # Простой расчет уровней на основе максимумов и минимумов
        high_levels = data['High'].rolling(window=20).max()
        low_levels = data['Low'].rolling(window=20).min()
        
        return {
            'resistance': high_levels,
            'support': low_levels,
            'mid_level': (high_levels + low_levels) / 2
        }
    
    def _analyze_pressure(self, data: pd.DataFrame, levels: Dict) -> Dict:
        """Анализ давления на уровни"""
        # Расчет давления на основе объема и волатильности
        volume_pressure = data['Volume'] / data['Volume'].rolling(20).mean()
        volatility = data['Close'].rolling(20).std()
        
        pressure = volume_pressure * volatility * self.parameters['volatility_factor']
        
        return {
            'pressure': pressure,
            'pressure_direction': np.where(pressure > self.parameters['pressure_threshold'], 1, -1),
            'pressure_strength': np.clip(pressure, 0, 1)
        }
    
    def _predict_future_levels(self, data: pd.DataFrame, levels: Dict) -> Dict:
        """Предсказание будущих уровней"""
        horizon = self.parameters['prediction_horizon']
        
        # Простое предсказание на основе тренда
        trend = data['Close'].diff(20) / data['Close'].shift(20)
        trend_factor = 1 + trend * self.parameters['trend_weight']
        
        future_resistance = levels['resistance'] * trend_factor
        future_support = levels['support'] * trend_factor
        
        return {
            'future_resistance': future_resistance,
            'future_support': future_support,
            'trend_factor': trend_factor
        }
    
    def get_performance_metrics(self) -> Dict:
        """Получение метрик производительности анализатора"""
        if not self.calculation_history:
            return {"error": "Нет данных для анализа"}
        
        # Простые метрики на основе истории расчетов
        total_calculations = len(self.calculation_history)
        avg_pressure = np.mean([calc['pressure_analysis']['pressure'].mean() 
                               for calc in self.calculation_history])
        
        return {
            'total_calculations': total_calculations,
            'average_pressure': avg_pressure,
            'parameters': self.parameters
        }
```

### Структура данных SCHR Levels

**Теория:** Структура данных SCHR Levels представляет собой комплексную систему признаков, которая обеспечивает полный анализ рыночных уровней и давления. Каждый компонент имеет специфическое назначение и вносит вклад в общую точность предсказаний.

**Почему структура данных критична:**
- **Полнота анализа:** Обеспечивает всесторонний анализ рыночных уровней
- **Точность предсказаний:** Каждый компонент повышает точность предсказаний
- **Анализ давления:** Критически важно для предсказания пробоев
- **Интеграция с ML:** Оптимизирована для машинного обучения

**Практическая реализация:** Структура данных SCHR Levels представляет собой стандартизированный формат для хранения и обработки всех компонентов анализа уровней. Эта структура оптимизирована для машинного обучения и обеспечивает максимальную эффективность обработки.

**Детальное объяснение структуры данных:**
- **Основные уровни:** Содержат предсказанные и текущие уровни поддержки и сопротивления
- **Давление на уровни:** Количественные метрики рыночного давления и его направления
- **Дополнительные компоненты:** Вероятностные и уверенностные метрики для принятия решений

**Почему эта структура критична:**
- **Стандартизация:** Обеспечивает единообразную обработку данных
- **Эффективность:** Оптимизирована для быстрой обработки
- **Полнота:** Содержит все необходимые компоненты для анализа
- **Совместимость:** Совместима с различными ML-фреймворками

```python
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

class SCHRLevelType(Enum):
    """Типы уровней SCHR"""
    SUPPORT = "support"
    RESISTANCE = "resistance"
    PREDICTED_HIGH = "predicted_high"
    PREDICTED_LOW = "predicted_low"

class PressureDirection(Enum):
    """Направления давления"""
    UP = 1
    DOWN = -1
    NEUTRAL = 0

@dataclass
class SCHRLevelData:
    """Структура данных для одного уровня SCHR"""
    level_value: float
    level_type: SCHRLevelType
    pressure: float
    pressure_direction: PressureDirection
    confidence: float
    breakout_probability: float
    bounce_probability: float
    timestamp: pd.Timestamp

class SCHRLevelsDataStructure:
    """
    Класс для работы со структурой данных SCHR Levels.
    
    Обеспечивает стандартизированную работу с данными уровней,
    включая валидацию, преобразования и экспорт.
    """
    
    def __init__(self):
        """Инициализация структуры данных"""
        self.schr_columns = {
            # Основные уровни
            'predicted_high': 'Предсказанный максимум',
            'predicted_low': 'Предсказанный минимум',
            'support_level': 'Уровень поддержки',
            'resistance_level': 'Уровень сопротивления',
            
            # Давление на уровни
            'pressure': 'Давление на уровень',
            'pressure_vector': 'Вектор давления',
            'pressure_strength': 'Сила давления',
            'pressure_direction': 'Направление давления',
            
            # Дополнительные компоненты
            'level_confidence': 'Уверенность в уровне',
            'level_breakout_probability': 'Вероятность пробоя уровня',
            'level_bounce_probability': 'Вероятность отскока от уровня',
            
            # Метаданные
            'timestamp': 'Временная метка',
            'asset': 'Актив',
            'timeframe': 'Таймфрейм'
        }
        
        # Валидация колонок
        self.required_columns = list(self.schr_columns.keys())
        
    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, bool]:
        """
        Валидация DataFrame на соответствие структуре SCHR Levels.
        
        Args:
            df: DataFrame для валидации
            
        Returns:
            Dict с результатами валидации
        """
        validation_results = {}
        
        # Проверка наличия обязательных колонок
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        validation_results['has_required_columns'] = len(missing_columns) == 0
        validation_results['missing_columns'] = missing_columns
        
        # Проверка типов данных
        numeric_columns = [col for col in self.schr_columns.keys() 
                          if col not in ['timestamp', 'asset', 'timeframe']]
        type_validation = all(pd.api.types.is_numeric_dtype(df[col]) for col in numeric_columns 
                             if col in df.columns)
        validation_results['correct_data_types'] = type_validation
        
        # Проверка на пропущенные значения
        null_counts = df.isnull().sum()
        validation_results['has_nulls'] = null_counts.sum() > 0
        validation_results['null_counts'] = null_counts.to_dict()
        
        # Проверка диапазонов значений
        range_validation = self._validate_value_ranges(df)
        validation_results['valid_ranges'] = range_validation
        
        return validation_results
    
    def _validate_value_ranges(self, df: pd.DataFrame) -> bool:
        """Валидация диапазонов значений"""
        try:
            # Проверка вероятностей (должны быть 0-1)
            prob_columns = ['level_confidence', 'level_breakout_probability', 'level_bounce_probability']
            for col in prob_columns:
                if col in df.columns:
                    if not ((df[col] >= 0) & (df[col] <= 1)).all():
                        return False
            
            # Проверка давления (должно быть положительным)
            pressure_columns = ['pressure', 'pressure_strength']
            for col in pressure_columns:
                if col in df.columns:
                    if not (df[col] >= 0).all():
                        return False
            
            # Проверка направления давления (-1, 0, 1)
            if 'pressure_direction' in df.columns:
                if not df['pressure_direction'].isin([-1, 0, 1]).all():
                    return False
            
            return True
        except Exception:
            return False
    
    def create_sample_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """
        Создание образца данных для тестирования.
        
        Args:
            n_samples: Количество образцов
            
        Returns:
            DataFrame с образцом данных SCHR Levels
        """
        np.random.seed(42)
        
        # Создание базовых данных
        data = {
            'timestamp': pd.date_range('2023-01-01', periods=n_samples, freq='1H'),
            'asset': 'GBPUSD',
            'timeframe': 'H1',
            
            # Основные уровни (симулируем реалистичные значения)
            'predicted_high': np.random.uniform(1.25, 1.35, n_samples),
            'predicted_low': np.random.uniform(1.20, 1.30, n_samples),
            'support_level': np.random.uniform(1.21, 1.29, n_samples),
            'resistance_level': np.random.uniform(1.26, 1.34, n_samples),
            
            # Давление на уровни
            'pressure': np.random.uniform(0.1, 2.0, n_samples),
            'pressure_vector': np.random.uniform(-1.0, 1.0, n_samples),
            'pressure_strength': np.random.uniform(0.0, 1.0, n_samples),
            'pressure_direction': np.random.choice([-1, 0, 1], n_samples),
            
            # Дополнительные компоненты
            'level_confidence': np.random.uniform(0.0, 1.0, n_samples),
            'level_breakout_probability': np.random.uniform(0.0, 1.0, n_samples),
            'level_bounce_probability': np.random.uniform(0.0, 1.0, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Обеспечиваем логическую согласованность
        df['predicted_high'] = np.maximum(df['predicted_high'], df['resistance_level'])
        df['predicted_low'] = np.minimum(df['predicted_low'], df['support_level'])
        
        return df
    
    def export_to_parquet(self, df: pd.DataFrame, filepath: str) -> bool:
        """
        Экспорт данных в Parquet формат.
        
        Args:
            df: DataFrame для экспорта
            filepath: Путь к файлу
            
        Returns:
            True если экспорт успешен
        """
        try:
            # Валидация перед экспортом
            validation = self.validate_dataframe(df)
            if not validation['has_required_columns']:
                print(f"Ошибка: отсутствуют колонки {validation['missing_columns']}")
                return False
            
            # Экспорт
            df.to_parquet(filepath, index=False)
            print(f"Данные успешно экспортированы в {filepath}")
            return True
            
        except Exception as e:
            print(f"Ошибка при экспорте: {e}")
            return False
    
    def load_from_parquet(self, filepath: str) -> Optional[pd.DataFrame]:
        """
        Загрузка данных из Parquet файла.
        
        Args:
            filepath: Путь к файлу
            
        Returns:
            DataFrame с данными или None при ошибке
        """
        try:
            df = pd.read_parquet(filepath)
            
            # Валидация загруженных данных
            validation = self.validate_dataframe(df)
            if not validation['has_required_columns']:
                print(f"Предупреждение: отсутствуют колонки {validation['missing_columns']}")
            
            print(f"Данные успешно загружены из {filepath}")
            print(f"Размер данных: {df.shape}")
            
            return df
            
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            return None
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict:
        """
        Получение сводки по данным.
        
        Args:
            df: DataFrame для анализа
            
        Returns:
            Dict с сводкой данных
        """
        summary = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'null_counts': df.isnull().sum().to_dict(),
            'numeric_summary': df.describe().to_dict() if len(df) > 0 else {}
        }
        
        return summary

# Пример использования
if __name__ == "__main__":
    # Создание структуры данных
    schr_structure = SCHRLevelsDataStructure()
    
    # Создание образца данных
    sample_data = schr_structure.create_sample_data(100)
    
    # Валидация данных
    validation_results = schr_structure.validate_dataframe(sample_data)
    print("Результаты валидации:", validation_results)
    
    # Получение сводки
    summary = schr_structure.get_data_summary(sample_data)
    print("Сводка данных:", summary)
```

## Анализ SCHR Levels по таймфреймам

**Теория:** Анализ SCHR Levels по различным таймфреймам является критически важным для создания робастной торговой системы. Каждый таймфрейм имеет свои особенности и требует специфических параметров для достижения максимальной эффективности.

**Почему мультитаймфреймовый анализ критичен:**
- **Различные рыночные циклы:** Каждый таймфрейм отражает разные рыночные циклы
- **Оптимизация параметров:** Разные параметры для разных временных горизонтов
- **Снижение рисков:** Диверсификация по таймфреймам снижает общие риски
- **Повышение точности:** Комбинирование сигналов с разных таймфреймов

### M1 (1 минута) - Микро-уровни

**Теория:** M1 таймфрейм предназначен для анализа микро-уровней и требует максимально быстрой реакции на изменения рыночного давления. Параметры SCHR Levels для M1 оптимизированы для выявления краткосрочных возможностей.

**Почему M1 анализ важен:**
- **Высокая частота сигналов:** Обеспечивает множество торговых возможностей
- **Быстрая реакция:** Позволяет быстро реагировать на изменения давления
- **Микро-уровни:** Выявляет краткосрочные уровни поддержки и сопротивления
- **Скальпинг:** Подходит для скальпинговых стратегий

**Плюсы:**
- Высокая частота торговых возможностей
- Быстрая реакция на изменения
- Выявление микро-уровней
- Подходит для скальпинга

**Минусы:**
- Высокие требования к точности
- Большое количество ложных сигналов
- Высокие транзакционные издержки
- Психологическое напряжение

**Практическая реализация:** Класс `SCHRLevelsM1Analysis` специально оптимизирован для работы с 1-минутными данными, где скорость реакции и точность детекции микро-уровней критически важны. Параметры настроены для максимальной чувствительности к краткосрочным изменениям.

**Детальное объяснение M1 анализа:**
- **Микро-уровни:** Обнаруживает очень близкие к текущей цене уровни (в пределах 0.1%)
- **Быстрые пробои:** Детектирует пробои, которые происходят в течение 1-5 минут
- **Микро-давление:** Анализирует давление на очень коротких временных интервалах
- **Скальпинг уровни:** Специальные уровни для скальпинговых стратегий

**Почему M1 анализ критичен:**
- **Высокая частота сигналов:** Обеспечивает множество торговых возможностей
- **Быстрая реакция:** Позволяет быстро реагировать на изменения рынка
- **Микро-анализ:** Выявляет детали, недоступные на больших таймфреймах
- **Скальпинг:** Подходит для высокочастотных торговых стратегий

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy import stats
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class SCHRLevelsM1Analysis:
    """
    Анализ SCHR Levels на 1-минутном таймфрейме.
    
    Специализированный класс для анализа микро-уровней и быстрых изменений
    рыночного давления на самом коротком таймфрейме.
    """
    
    def __init__(self, 
                 pressure_threshold: float = 0.5,
                 level_strength: float = 0.6,
                 prediction_horizon: int = 5,
                 volatility_factor: float = 2.0,
                 micro_threshold: float = 0.001):
        """
        Инициализация анализатора M1.
        
        Args:
            pressure_threshold: Порог давления для M1 (более чувствительный)
            level_strength: Минимальная сила уровня для M1
            prediction_horizon: Горизонт предсказания (короткий для M1)
            volatility_factor: Фактор волатильности (высокий для M1)
            micro_threshold: Порог для детекции микро-уровней (0.1%)
        """
        self.timeframe = 'M1'
        self.optimal_params = {
            'pressure_threshold': pressure_threshold,
            'level_strength': level_strength,
            'prediction_horizon': prediction_horizon,
            'volatility_factor': volatility_factor,
            'micro_threshold': micro_threshold
        }
        
        # Инициализация компонентов
        self.scaler = StandardScaler()
        self.feature_history = []
        
        # Валидация параметров
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Валидация параметров для M1"""
        if not 0.0 <= self.optimal_params['pressure_threshold'] <= 1.0:
            raise ValueError("pressure_threshold должен быть между 0.0 и 1.0")
        if not 0.0 <= self.optimal_params['level_strength'] <= 1.0:
            raise ValueError("level_strength должен быть между 0.0 и 1.0")
        if self.optimal_params['prediction_horizon'] <= 0:
            raise ValueError("prediction_horizon должен быть положительным")
        if self.optimal_params['micro_threshold'] <= 0:
            raise ValueError("micro_threshold должен быть положительным")
    
    def analyze_m1_features(self, data: pd.DataFrame) -> Dict:
        """
        Комплексный анализ признаков для M1 таймфрейма.
        
        Args:
            data: DataFrame с OHLCV данными и SCHR колонками
            
        Returns:
            Dict с результатами анализа M1 признаков
        """
        try:
            # Проверка данных
            if len(data) < 10:
                raise ValueError("Недостаточно данных для анализа M1")
            
            features = {}
            
            # 1. Микро-уровни
            features['micro_levels'] = self._detect_micro_levels(data)
            
            # 2. Быстрые пробои
            features['quick_breakouts'] = self._detect_quick_breakouts(data)
            
            # 3. Микро-давление
            features['micro_pressure'] = self._analyze_micro_pressure(data)
            
            # 4. Скальпинг уровни
            features['scalping_levels'] = self._detect_scalping_levels(data)
            
            # 5. Временные паттерны
            features['temporal_patterns'] = self._analyze_temporal_patterns(data)
            
            # 6. Волатильность анализ
            features['volatility_analysis'] = self._analyze_volatility(data)
            
            # Сохранение истории
            self.feature_history.append({
                'timestamp': pd.Timestamp.now(),
                'features': features,
                'data_length': len(data)
            })
            
            return features
            
        except Exception as e:
            print(f"Ошибка в анализе M1 признаков: {e}")
            return {}
    
    def _detect_micro_levels(self, data: pd.DataFrame) -> Dict:
        """
        Детекция микро-уровней для M1.
        
        Микро-уровни - это уровни, которые находятся очень близко к текущей цене
        и могут быть использованы для скальпинговых стратегий.
        """
        # Анализ близости к уровням
        distance_to_high = (data['predicted_high'] - data['Close']) / data['Close']
        distance_to_low = (data['Close'] - data['predicted_low']) / data['Close']
        distance_to_support = (data['Close'] - data['support_level']) / data['Close']
        distance_to_resistance = (data['resistance_level'] - data['Close']) / data['Close']
        
        # Микро-уровни (близко к предсказанным уровням)
        micro_threshold = self.optimal_params['micro_threshold']
        micro_high = distance_to_high < micro_threshold
        micro_low = distance_to_low < micro_threshold
        micro_support = distance_to_support < micro_threshold
        micro_resistance = distance_to_resistance < micro_threshold
        
        # Сила микро-уровней
        micro_strength = np.where(
            micro_high | micro_low | micro_support | micro_resistance,
            np.maximum(
                np.maximum(1 - distance_to_high, 1 - distance_to_low),
                np.maximum(1 - distance_to_support, 1 - distance_to_resistance)
            ),
            0
        )
        
        return {
            'micro_high': micro_high,
            'micro_low': micro_low,
            'micro_support': micro_support,
            'micro_resistance': micro_resistance,
            'distance_to_high': distance_to_high,
            'distance_to_low': distance_to_low,
            'distance_to_support': distance_to_support,
            'distance_to_resistance': distance_to_resistance,
            'micro_strength': micro_strength,
            'micro_count': np.sum(micro_high | micro_low | micro_support | micro_resistance)
        }
    
    def _detect_quick_breakouts(self, data: pd.DataFrame) -> Dict:
        """
        Детекция быстрых пробоев для M1.
        
        Быстрые пробои - это пробои уровней, которые происходят в течение
        короткого времени (1-5 минут) и могут быть использованы для быстрых сделок.
        """
        # Расчет пробоев
        breakout_high = data['Close'] > data['predicted_high']
        breakout_low = data['Close'] < data['predicted_low']
        breakout_support = data['Close'] < data['support_level']
        breakout_resistance = data['Close'] > data['resistance_level']
        
        # Быстрые пробои (в течение 5 периодов)
        quick_window = min(5, len(data))
        quick_breakout_high = breakout_high.rolling(window=quick_window).sum() > 0
        quick_breakout_low = breakout_low.rolling(window=quick_window).sum() > 0
        
        # Сила пробоев
        breakout_strength_high = np.where(
            breakout_high,
            (data['Close'] - data['predicted_high']) / data['predicted_high'],
            0
        )
        breakout_strength_low = np.where(
            breakout_low,
            (data['predicted_low'] - data['Close']) / data['predicted_low'],
            0
        )
        
        # Частота пробоев
        breakout_frequency = (breakout_high | breakout_low).rolling(window=20).sum() / 20
        
        return {
            'breakout_high': breakout_high,
            'breakout_low': breakout_low,
            'breakout_support': breakout_support,
            'breakout_resistance': breakout_resistance,
            'quick_breakout_high': quick_breakout_high,
            'quick_breakout_low': quick_breakout_low,
            'breakout_strength_high': breakout_strength_high,
            'breakout_strength_low': breakout_strength_low,
            'breakout_frequency': breakout_frequency
        }
    
    def _analyze_micro_pressure(self, data: pd.DataFrame) -> Dict:
        """
        Анализ микро-давления для M1.
        
        Микро-давление - это давление на уровни в очень коротких временных интервалах,
        которое может указывать на скорые изменения направления цены.
        """
        # Базовое давление
        base_pressure = data['pressure'] if 'pressure' in data.columns else np.ones(len(data))
        
        # Микро-давление (изменения за 1-3 периода)
        micro_pressure_1 = base_pressure.diff(1).abs()
        micro_pressure_3 = base_pressure.diff(3).abs()
        
        # Направление микро-давления
        pressure_direction = np.sign(base_pressure.diff(1))
        
        # Ускорение давления
        pressure_acceleration = base_pressure.diff(1).diff(1)
        
        # Волатильность давления
        pressure_volatility = base_pressure.rolling(window=5).std()
        
        # Пороги для M1
        pressure_threshold = self.optimal_params['pressure_threshold']
        high_pressure = base_pressure > pressure_threshold
        extreme_pressure = base_pressure > pressure_threshold * 1.5
        
        return {
            'base_pressure': base_pressure,
            'micro_pressure_1': micro_pressure_1,
            'micro_pressure_3': micro_pressure_3,
            'pressure_direction': pressure_direction,
            'pressure_acceleration': pressure_acceleration,
            'pressure_volatility': pressure_volatility,
            'high_pressure': high_pressure,
            'extreme_pressure': extreme_pressure,
            'pressure_trend': base_pressure.rolling(window=5).mean()
        }
    
    def _detect_scalping_levels(self, data: pd.DataFrame) -> Dict:
        """
        Детекция скальпинг уровней для M1.
        
        Скальпинг уровни - это специальные уровни, которые подходят для
        высокочастотных торговых стратегий с быстрым входом и выходом.
        """
        # Базовые уровни
        high_levels = data['predicted_high']
        low_levels = data['predicted_low']
        support_levels = data['support_level']
        resistance_levels = data['resistance_level']
        
        # Скальпинг диапазон (узкий диапазон для скальпинга)
        scalping_range = (high_levels - low_levels) / data['Close']
        narrow_range = scalping_range < 0.002  # 0.2% для скальпинга
        
        # Скальпинг уровни (уровни в узком диапазоне)
        scalping_high = high_levels[narrow_range]
        scalping_low = low_levels[narrow_range]
        
        # Сила скальпинг уровней
        scalping_strength = np.where(
            narrow_range,
            scalping_range * 1000,  # Нормализация для скальпинга
            0
        )
        
        # Частота касаний скальпинг уровней
        touch_frequency = (data['Close'] <= high_levels * 1.001) & (data['Close'] >= low_levels * 0.999)
        touch_frequency = touch_frequency.rolling(window=10).sum() / 10
        
        return {
            'scalping_range': scalping_range,
            'narrow_range': narrow_range,
            'scalping_high': scalping_high,
            'scalping_low': scalping_low,
            'scalping_strength': scalping_strength,
            'touch_frequency': touch_frequency,
            'scalping_opportunities': narrow_range.sum()
        }
    
    def _analyze_temporal_patterns(self, data: pd.DataFrame) -> Dict:
        """
        Анализ временных паттернов для M1.
        
        Временные паттерны - это повторяющиеся паттерны в поведении уровней
        в зависимости от времени дня, дня недели и других временных факторов.
        """
        # Временные компоненты
        timestamps = pd.to_datetime(data.index) if hasattr(data.index, 'to_datetime') else data.index
        hour = timestamps.hour if hasattr(timestamps, 'hour') else np.zeros(len(data))
        minute = timestamps.minute if hasattr(timestamps, 'minute') else np.zeros(len(data))
        day_of_week = timestamps.dayofweek if hasattr(timestamps, 'dayofweek') else np.zeros(len(data))
        
        # Паттерны по часам
        hourly_patterns = {}
        for h in range(24):
            hour_mask = hour == h
            if hour_mask.sum() > 0:
                hourly_patterns[f'hour_{h}'] = {
                    'count': hour_mask.sum(),
                    'avg_pressure': data['pressure'][hour_mask].mean() if 'pressure' in data.columns else 0,
                    'avg_volatility': data['Close'][hour_mask].std() if len(data[hour_mask]) > 1 else 0
                }
        
        # Паттерны по дням недели
        daily_patterns = {}
        for d in range(7):
            day_mask = day_of_week == d
            if day_mask.sum() > 0:
                daily_patterns[f'day_{d}'] = {
                    'count': day_mask.sum(),
                    'avg_pressure': data['pressure'][day_mask].mean() if 'pressure' in data.columns else 0,
                    'avg_volatility': data['Close'][day_mask].std() if len(data[day_mask]) > 1 else 0
                }
        
        return {
            'hourly_patterns': hourly_patterns,
            'daily_patterns': daily_patterns,
            'current_hour': hour,
            'current_minute': minute,
            'current_day': day_of_week
        }
    
    def _analyze_volatility(self, data: pd.DataFrame) -> Dict:
        """
        Анализ волатильности для M1.
        
        Волатильность критически важна для M1 анализа, так как она определяет
        эффективность скальпинговых стратегий и риск быстрых движений.
        """
        # Базовые метрики волатильности
        returns = data['Close'].pct_change()
        volatility_1min = returns.rolling(window=5).std()
        volatility_5min = returns.rolling(window=25).std()
        volatility_15min = returns.rolling(window=75).std()
        
        # Относительная волатильность
        relative_volatility = volatility_1min / volatility_15min
        
        # Волатильность уровней
        level_volatility = (data['predicted_high'] - data['predicted_low']).rolling(window=10).std()
        
        # Волатильность давления
        pressure_volatility = data['pressure'].rolling(window=10).std() if 'pressure' in data.columns else np.zeros(len(data))
        
        # Классификация волатильности
        low_vol = volatility_1min < volatility_1min.quantile(0.33)
        medium_vol = (volatility_1min >= volatility_1min.quantile(0.33)) & (volatility_1min < volatility_1min.quantile(0.67))
        high_vol = volatility_1min >= volatility_1min.quantile(0.67)
        
        return {
            'volatility_1min': volatility_1min,
            'volatility_5min': volatility_5min,
            'volatility_15min': volatility_15min,
            'relative_volatility': relative_volatility,
            'level_volatility': level_volatility,
            'pressure_volatility': pressure_volatility,
            'low_volatility': low_vol,
            'medium_volatility': medium_vol,
            'high_volatility': high_vol,
            'volatility_trend': volatility_1min.rolling(window=20).mean()
        }
    
    def get_m1_summary(self, features: Dict) -> Dict:
        """
        Получение сводки по M1 анализу.
        
        Args:
            features: Результаты анализа M1 признаков
            
        Returns:
            Dict с сводкой M1 анализа
        """
        summary = {
            'timeframe': self.timeframe,
            'parameters': self.optimal_params,
            'analysis_timestamp': pd.Timestamp.now(),
            'feature_count': len(features)
        }
        
        # Сводка по микро-уровням
        if 'micro_levels' in features:
            micro = features['micro_levels']
            summary['micro_levels'] = {
                'total_micro_levels': micro.get('micro_count', 0),
                'avg_distance_to_high': micro.get('distance_to_high', pd.Series()).mean(),
                'avg_distance_to_low': micro.get('distance_to_low', pd.Series()).mean()
            }
        
        # Сводка по пробоям
        if 'quick_breakouts' in features:
            breakouts = features['quick_breakouts']
            summary['breakouts'] = {
                'total_breakouts': breakouts.get('breakout_high', pd.Series()).sum() + breakouts.get('breakout_low', pd.Series()).sum(),
                'avg_breakout_frequency': breakouts.get('breakout_frequency', pd.Series()).mean()
            }
        
        return summary

# Пример использования
if __name__ == "__main__":
    # Создание анализатора M1
    m1_analyzer = SCHRLevelsM1Analysis()
    
    # Создание тестовых данных
    dates = pd.date_range('2023-01-01', periods=100, freq='1min')
    test_data = pd.DataFrame({
        'Open': np.random.uniform(1.25, 1.35, 100),
        'High': np.random.uniform(1.26, 1.36, 100),
        'Low': np.random.uniform(1.24, 1.34, 100),
        'Close': np.random.uniform(1.25, 1.35, 100),
        'Volume': np.random.uniform(1000, 10000, 100),
        'predicted_high': np.random.uniform(1.26, 1.36, 100),
        'predicted_low': np.random.uniform(1.24, 1.34, 100),
        'support_level': np.random.uniform(1.24, 1.34, 100),
        'resistance_level': np.random.uniform(1.26, 1.36, 100),
        'pressure': np.random.uniform(0.1, 2.0, 100)
    }, index=dates)
    
    # Анализ M1 признаков
    features = m1_analyzer.analyze_m1_features(test_data)
    
    # Получение сводки
    summary = m1_analyzer.get_m1_summary(features)
    print("Сводка M1 анализа:", summary)
```

### M5 (5 минут) - Краткосрочные уровни

**Теория:** M5 таймфрейм представляет собой оптимальный баланс между частотой сигналов и их качеством для анализа краткосрочных уровней. Это наиболее популярный таймфрейм для краткосрочной торговли на основе уровней.

**Почему M5 анализ важен:**
- **Оптимальный баланс:** Хорошее соотношение частоты и качества сигналов
- **Снижение шума:** Меньше рыночного шума по сравнению с M1
- **Краткосрочные уровни:** Выявляет краткосрочные уровни поддержки и сопротивления
- **Стабильность:** Более стабильные сигналы

**Плюсы:**
- Оптимальный баланс частоты и качества
- Меньше рыночного шума
- Стабильные сигналы
- Подходит для большинства стратегий

**Минусы:**
- Меньше торговых возможностей чем M1
- Требует больше времени для анализа
- Потенциальные задержки в сигналах

**Практическая реализация:** Класс `SCHRLevelsM5Analysis` оптимизирован для 5-минутного таймфрейма, который представляет собой идеальный баланс между частотой сигналов и их качеством. M5 обеспечивает достаточно данных для анализа, но не перегружен рыночным шумом.

**Детальное объяснение M5 анализа:**
- **Краткосрочные уровни:** Обнаруживает уровни, действующие в течение 5-30 минут
- **Быстрые отскоки:** Детектирует отскоки от уровней в течение короткого времени
- **Краткосрочное давление:** Анализирует давление на промежуточных временных интервалах
- **Среднесрочные паттерны:** Выявляет паттерны, которые не видны на M1, но важны для краткосрочной торговли

**Почему M5 анализ важен:**
- **Оптимальный баланс:** Лучшее соотношение частоты и качества сигналов
- **Снижение шума:** Меньше рыночного шума по сравнению с M1
- **Практичность:** Подходит для большинства торговых стратегий
- **Стабильность:** Более стабильные и надежные сигналы

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

class SCHRLevelsM5Analysis:
    """
    Анализ SCHR Levels на 5-минутном таймфрейме.
    
    Специализированный класс для анализа краткосрочных уровней и паттернов
    на 5-минутном таймфрейме, обеспечивающий оптимальный баланс между
    частотой сигналов и их качеством.
    """
    
    def __init__(self, 
                 pressure_threshold: float = 0.6,
                 level_strength: float = 0.7,
                 prediction_horizon: int = 10,
                 volatility_factor: float = 1.8,
                 bounce_threshold: float = 0.002):
        """
        Инициализация анализатора M5.
        
        Args:
            pressure_threshold: Порог давления для M5 (средний)
            level_strength: Минимальная сила уровня для M5
            prediction_horizon: Горизонт предсказания (средний для M5)
            volatility_factor: Фактор волатильности (средний для M5)
            bounce_threshold: Порог для детекции отскоков (0.2%)
        """
        self.timeframe = 'M5'
        self.optimal_params = {
            'pressure_threshold': pressure_threshold,
            'level_strength': level_strength,
            'prediction_horizon': prediction_horizon,
            'volatility_factor': volatility_factor,
            'bounce_threshold': bounce_threshold
        }
        
        # Инициализация компонентов
        self.scaler = StandardScaler()
        self.feature_history = []
        self.level_clusters = None
        
        # Валидация параметров
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Валидация параметров для M5"""
        if not 0.0 <= self.optimal_params['pressure_threshold'] <= 1.0:
            raise ValueError("pressure_threshold должен быть между 0.0 и 1.0")
        if not 0.0 <= self.optimal_params['level_strength'] <= 1.0:
            raise ValueError("level_strength должен быть между 0.0 и 1.0")
        if self.optimal_params['prediction_horizon'] <= 0:
            raise ValueError("prediction_horizon должен быть положительным")
        if self.optimal_params['bounce_threshold'] <= 0:
            raise ValueError("bounce_threshold должен быть положительным")
    
    def analyze_m5_features(self, data: pd.DataFrame) -> Dict:
        """
        Комплексный анализ признаков для M5 таймфрейма.
        
        Args:
            data: DataFrame с OHLCV данными и SCHR колонками
            
        Returns:
            Dict с результатами анализа M5 признаков
        """
        try:
            # Проверка данных
            if len(data) < 20:
                raise ValueError("Недостаточно данных для анализа M5")
            
            features = {}
            
            # 1. Краткосрочные уровни
            features['short_levels'] = self._detect_short_levels(data)
            
            # 2. Быстрые отскоки
            features['quick_bounces'] = self._detect_quick_bounces(data)
            
            # 3. Краткосрочное давление
            features['short_pressure'] = self._analyze_short_pressure(data)
            
            # 4. Среднесрочные паттерны
            features['medium_patterns'] = self._detect_medium_patterns(data)
            
            # 5. Кластеризация уровней
            features['level_clusters'] = self._cluster_levels(data)
            
            # 6. Трендовый анализ
            features['trend_analysis'] = self._analyze_trends(data)
            
            # Сохранение истории
            self.feature_history.append({
                'timestamp': pd.Timestamp.now(),
                'features': features,
                'data_length': len(data)
            })
            
            return features
            
        except Exception as e:
            print(f"Ошибка в анализе M5 признаков: {e}")
            return {}
    
    def _detect_short_levels(self, data: pd.DataFrame) -> Dict:
        """
        Детекция краткосрочных уровней для M5.
        
        Краткосрочные уровни - это уровни поддержки и сопротивления,
        которые действуют в течение 5-30 минут и подходят для краткосрочной торговли.
        """
        # Базовые уровни
        high_levels = data['predicted_high']
        low_levels = data['predicted_low']
        support_levels = data['support_level']
        resistance_levels = data['resistance_level']
        
        # Расстояния до уровней
        distance_to_high = (high_levels - data['Close']) / data['Close']
        distance_to_low = (data['Close'] - low_levels) / data['Close']
        distance_to_support = (data['Close'] - support_levels) / data['Close']
        distance_to_resistance = (resistance_levels - data['Close']) / data['Close']
        
        # Краткосрочные уровни (близко к цене)
        short_threshold = 0.005  # 0.5% для M5
        short_high = distance_to_high < short_threshold
        short_low = distance_to_low < short_threshold
        short_support = distance_to_support < short_threshold
        short_resistance = distance_to_resistance < short_threshold
        
        # Сила краткосрочных уровней
        short_strength = np.where(
            short_high | short_low | short_support | short_resistance,
            np.maximum(
                np.maximum(1 - distance_to_high, 1 - distance_to_low),
                np.maximum(1 - distance_to_support, 1 - distance_to_resistance)
            ),
            0
        )
        
        # Стабильность уровней (как долго уровень держится)
        level_stability = self._calculate_level_stability(data)
        
        return {
            'short_high': short_high,
            'short_low': short_low,
            'short_support': short_support,
            'short_resistance': short_resistance,
            'distance_to_high': distance_to_high,
            'distance_to_low': distance_to_low,
            'distance_to_support': distance_to_support,
            'distance_to_resistance': distance_to_resistance,
            'short_strength': short_strength,
            'level_stability': level_stability,
            'short_level_count': np.sum(short_high | short_low | short_support | short_resistance)
        }
    
    def _detect_quick_bounces(self, data: pd.DataFrame) -> Dict:
        """
        Детекция быстрых отскоков для M5.
        
        Быстрые отскоки - это отскоки от уровней, которые происходят
        в течение 5-15 минут и могут быть использованы для быстрых сделок.
        """
        # Базовые уровни
        high_levels = data['predicted_high']
        low_levels = data['predicted_low']
        support_levels = data['support_level']
        resistance_levels = data['resistance_level']
        
        # Детекция касаний уровней
        touch_high = (data['Close'] <= high_levels * 1.001) & (data['Close'] >= high_levels * 0.999)
        touch_low = (data['Close'] >= low_levels * 0.999) & (data['Close'] <= low_levels * 1.001)
        touch_support = (data['Close'] <= support_levels * 1.001) & (data['Close'] >= support_levels * 0.999)
        touch_resistance = (data['Close'] >= resistance_levels * 0.999) & (data['Close'] <= resistance_levels * 1.001)
        
        # Быстрые отскоки (в течение 3 периодов)
        bounce_window = min(3, len(data))
        quick_bounce_high = touch_high.rolling(window=bounce_window).sum() > 0
        quick_bounce_low = touch_low.rolling(window=bounce_window).sum() > 0
        quick_bounce_support = touch_support.rolling(window=bounce_window).sum() > 0
        quick_bounce_resistance = touch_resistance.rolling(window=bounce_window).sum() > 0
        
        # Сила отскоков
        bounce_strength_high = np.where(
            touch_high,
            (high_levels - data['Close']) / high_levels,
            0
        )
        bounce_strength_low = np.where(
            touch_low,
            (data['Close'] - low_levels) / low_levels,
            0
        )
        
        # Частота отскоков
        bounce_frequency = (touch_high | touch_low | touch_support | touch_resistance).rolling(window=20).sum() / 20
        
        # Успешность отскоков (приводит ли к развороту)
        bounce_success = self._calculate_bounce_success(data, touch_high, touch_low)
        
        return {
            'touch_high': touch_high,
            'touch_low': touch_low,
            'touch_support': touch_support,
            'touch_resistance': touch_resistance,
            'quick_bounce_high': quick_bounce_high,
            'quick_bounce_low': quick_bounce_low,
            'quick_bounce_support': quick_bounce_support,
            'quick_bounce_resistance': quick_bounce_resistance,
            'bounce_strength_high': bounce_strength_high,
            'bounce_strength_low': bounce_strength_low,
            'bounce_frequency': bounce_frequency,
            'bounce_success': bounce_success
        }
    
    def _analyze_short_pressure(self, data: pd.DataFrame) -> Dict:
        """
        Анализ краткосрочного давления для M5.
        
        Краткосрочное давление - это давление на уровни в промежуточных
        временных интервалах, которое может указывать на направление движения.
        """
        # Базовое давление
        base_pressure = data['pressure'] if 'pressure' in data.columns else np.ones(len(data))
        
        # Краткосрочное давление (изменения за 5-15 периодов)
        short_pressure_5 = base_pressure.rolling(window=5).mean()
        short_pressure_15 = base_pressure.rolling(window=15).mean()
        
        # Изменение давления
        pressure_change_5 = base_pressure.diff(5)
        pressure_change_15 = base_pressure.diff(15)
        
        # Направление давления
        pressure_direction = np.sign(pressure_change_5)
        
        # Ускорение давления
        pressure_acceleration = pressure_change_5.diff(5)
        
        # Волатильность давления
        pressure_volatility = base_pressure.rolling(window=10).std()
        
        # Пороги для M5
        pressure_threshold = self.optimal_params['pressure_threshold']
        high_pressure = base_pressure > pressure_threshold
        extreme_pressure = base_pressure > pressure_threshold * 1.3
        
        # Тренд давления
        pressure_trend = base_pressure.rolling(window=20).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        
        return {
            'base_pressure': base_pressure,
            'short_pressure_5': short_pressure_5,
            'short_pressure_15': short_pressure_15,
            'pressure_change_5': pressure_change_5,
            'pressure_change_15': pressure_change_15,
            'pressure_direction': pressure_direction,
            'pressure_acceleration': pressure_acceleration,
            'pressure_volatility': pressure_volatility,
            'high_pressure': high_pressure,
            'extreme_pressure': extreme_pressure,
            'pressure_trend': pressure_trend
        }
    
    def _detect_medium_patterns(self, data: pd.DataFrame) -> Dict:
        """
        Детекция среднесрочных паттернов для M5.
        
        Среднесрочные паттерны - это паттерны, которые формируются
        в течение 15-60 минут и могут указывать на более значимые движения.
        """
        # Базовые данные
        high = data['High']
        low = data['Low']
        close = data['Close']
        volume = data['Volume'] if 'Volume' in data.columns else np.ones(len(data))
        
        # Паттерн "Двойная вершина/дно"
        double_top = self._detect_double_top_bottom(high, low, close)
        
        # Паттерн "Треугольник"
        triangle = self._detect_triangle_pattern(high, low, close)
        
        # Паттерн "Флаг/Вымпел"
        flag_pennant = self._detect_flag_pennant(high, low, close, volume)
        
        # Паттерн "Клин"
        wedge = self._detect_wedge_pattern(high, low, close)
        
        # Общая сила паттернов
        pattern_strength = np.maximum(
            np.maximum(double_top['strength'], triangle['strength']),
            np.maximum(flag_pennant['strength'], wedge['strength'])
        )
        
        return {
            'double_top': double_top,
            'triangle': triangle,
            'flag_pennant': flag_pennant,
            'wedge': wedge,
            'pattern_strength': pattern_strength,
            'total_patterns': np.sum(pattern_strength > 0.5)
        }
    
    def _cluster_levels(self, data: pd.DataFrame) -> Dict:
        """
        Кластеризация уровней для M5.
        
        Кластеризация уровней помогает выявить группы похожих уровней
        и определить наиболее значимые области поддержки и сопротивления.
        """
        # Подготовка данных для кластеризации
        levels_data = np.column_stack([
            data['predicted_high'].values,
            data['predicted_low'].values,
            data['support_level'].values,
            data['resistance_level'].values
        ])
        
        # Удаление NaN значений
        valid_mask = ~np.isnan(levels_data).any(axis=1)
        levels_data_clean = levels_data[valid_mask]
        
        if len(levels_data_clean) < 10:
            return {'clusters': None, 'cluster_labels': None, 'cluster_centers': None}
        
        # Кластеризация K-means
        n_clusters = min(5, len(levels_data_clean) // 10)
        if n_clusters < 2:
            n_clusters = 2
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(levels_data_clean)
        
        # Создание полных меток (включая NaN)
        full_labels = np.full(len(data), -1)
        full_labels[valid_mask] = cluster_labels
        
        # Анализ кластеров
        cluster_analysis = {}
        for i in range(n_clusters):
            cluster_mask = cluster_labels == i
            if cluster_mask.sum() > 0:
                cluster_data = levels_data_clean[cluster_mask]
                cluster_analysis[f'cluster_{i}'] = {
                    'size': cluster_mask.sum(),
                    'center': kmeans.cluster_centers_[i],
                    'avg_level': np.mean(cluster_data),
                    'level_std': np.std(cluster_data)
                }
        
        self.level_clusters = kmeans
        
        return {
            'clusters': kmeans,
            'cluster_labels': full_labels,
            'cluster_centers': kmeans.cluster_centers_,
            'cluster_analysis': cluster_analysis,
            'n_clusters': n_clusters
        }
    
    def _analyze_trends(self, data: pd.DataFrame) -> Dict:
        """
        Анализ трендов для M5.
        
        Анализ трендов помогает определить общее направление движения
        и его силу на 5-минутном таймфрейме.
        """
        # Базовые данные
        close = data['Close']
        high = data['High']
        low = data['Low']
        
        # Простые скользящие средние
        sma_5 = close.rolling(window=5).mean()
        sma_10 = close.rolling(window=10).mean()
        sma_20 = close.rolling(window=20).mean()
        
        # Экспоненциальные скользящие средние
        ema_5 = close.ewm(span=5).mean()
        ema_10 = close.ewm(span=10).mean()
        ema_20 = close.ewm(span=20).mean()
        
        # Направление тренда
        trend_direction = np.where(
            close > sma_20, 1,  # Восходящий
            np.where(close < sma_20, -1, 0)  # Нисходящий, боковой
        )
        
        # Сила тренда
        trend_strength = abs(close - sma_20) / sma_20
        
        # Ускорение тренда
        trend_acceleration = sma_5.diff(5)
        
        # Конвергенция/дивергенция скользящих средних
        macd = ema_5 - ema_20
        macd_signal = macd.ewm(span=3).mean()
        macd_histogram = macd - macd_signal
        
        # RSI для определения перекупленности/перепроданности
        rsi = self._calculate_rsi(close, 14)
        
        return {
            'sma_5': sma_5,
            'sma_10': sma_10,
            'sma_20': sma_20,
            'ema_5': ema_5,
            'ema_10': ema_10,
            'ema_20': ema_20,
            'trend_direction': trend_direction,
            'trend_strength': trend_strength,
            'trend_acceleration': trend_acceleration,
            'macd': macd,
            'macd_signal': macd_signal,
            'macd_histogram': macd_histogram,
            'rsi': rsi
        }
    
    def _calculate_level_stability(self, data: pd.DataFrame) -> pd.Series:
        """Расчет стабильности уровней"""
        # Простой расчет стабильности на основе изменчивости уровней
        level_changes = data['predicted_high'].diff().abs() + data['predicted_low'].diff().abs()
        stability = 1 / (1 + level_changes.rolling(window=10).mean())
        return stability.fillna(0)
    
    def _calculate_bounce_success(self, data: pd.DataFrame, touch_high: pd.Series, touch_low: pd.Series) -> pd.Series:
        """Расчет успешности отскоков"""
        # Простой расчет: отскок успешен, если после касания цена движется в противоположном направлении
        future_returns = data['Close'].shift(-5) / data['Close'] - 1
        bounce_success = np.where(
            touch_high,
            future_returns < -0.001,  # Цена падает после касания максимума
            np.where(touch_low, future_returns > 0.001, False)  # Цена растет после касания минимума
        )
        return pd.Series(bounce_success, index=data.index)
    
    def _detect_double_top_bottom(self, high: pd.Series, low: pd.Series, close: pd.Series) -> Dict:
        """Детекция паттерна двойная вершина/дно"""
        # Упрощенная детекция двойной вершины
        peaks = high.rolling(window=5, center=True).max() == high
        valleys = low.rolling(window=5, center=True).min() == low
        
        return {
            'double_top': peaks,
            'double_bottom': valleys,
            'strength': np.where(peaks | valleys, 0.5, 0)
        }
    
    def _detect_triangle_pattern(self, high: pd.Series, low: pd.Series, close: pd.Series) -> Dict:
        """Детекция треугольных паттернов"""
        # Упрощенная детекция треугольника
        high_trend = high.rolling(window=10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        low_trend = low.rolling(window=10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        
        triangle = (high_trend < 0) & (low_trend > 0)  # Сходящийся треугольник
        
        return {
            'triangle': triangle,
            'strength': np.where(triangle, 0.6, 0)
        }
    
    def _detect_flag_pennant(self, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> Dict:
        """Детекция паттернов флаг/вымпел"""
        # Упрощенная детекция флага
        price_range = high - low
        avg_range = price_range.rolling(window=10).mean()
        flag = price_range < avg_range * 0.5  # Узкий диапазон
        
        return {
            'flag': flag,
            'strength': np.where(flag, 0.4, 0)
        }
    
    def _detect_wedge_pattern(self, high: pd.Series, low: pd.Series, close: pd.Series) -> Dict:
        """Детекция клиновых паттернов"""
        # Упрощенная детекция клина
        high_trend = high.rolling(window=10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        low_trend = low.rolling(window=10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        
        wedge = (high_trend < 0) & (low_trend < 0)  # Нисходящий клин
        
        return {
            'wedge': wedge,
            'strength': np.where(wedge, 0.5, 0)
        }
    
    def _calculate_rsi(self, close: pd.Series, period: int = 14) -> pd.Series:
        """Расчет RSI"""
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50)
    
    def get_m5_summary(self, features: Dict) -> Dict:
        """
        Получение сводки по M5 анализу.
        
        Args:
            features: Результаты анализа M5 признаков
            
        Returns:
            Dict с сводкой M5 анализа
        """
        summary = {
            'timeframe': self.timeframe,
            'parameters': self.optimal_params,
            'analysis_timestamp': pd.Timestamp.now(),
            'feature_count': len(features)
        }
        
        # Сводка по краткосрочным уровням
        if 'short_levels' in features:
            short = features['short_levels']
            summary['short_levels'] = {
                'total_short_levels': short.get('short_level_count', 0),
                'avg_stability': short.get('level_stability', pd.Series()).mean()
            }
        
        # Сводка по отскокам
        if 'quick_bounces' in features:
            bounces = features['quick_bounces']
            summary['bounces'] = {
                'total_bounces': bounces.get('bounce_frequency', pd.Series()).sum(),
                'bounce_success_rate': bounces.get('bounce_success', pd.Series()).mean()
            }
        
        # Сводка по паттернам
        if 'medium_patterns' in features:
            patterns = features['medium_patterns']
            summary['patterns'] = {
                'total_patterns': patterns.get('total_patterns', 0),
                'avg_strength': patterns.get('pattern_strength', pd.Series()).mean()
            }
        
        return summary

# Пример использования
if __name__ == "__main__":
    # Создание анализатора M5
    m5_analyzer = SCHRLevelsM5Analysis()
    
    # Создание тестовых данных
    dates = pd.date_range('2023-01-01', periods=200, freq='5min')
    test_data = pd.DataFrame({
        'Open': np.random.uniform(1.25, 1.35, 200),
        'High': np.random.uniform(1.26, 1.36, 200),
        'Low': np.random.uniform(1.24, 1.34, 200),
        'Close': np.random.uniform(1.25, 1.35, 200),
        'Volume': np.random.uniform(1000, 10000, 200),
        'predicted_high': np.random.uniform(1.26, 1.36, 200),
        'predicted_low': np.random.uniform(1.24, 1.34, 200),
        'support_level': np.random.uniform(1.24, 1.34, 200),
        'resistance_level': np.random.uniform(1.26, 1.36, 200),
        'pressure': np.random.uniform(0.1, 2.0, 200)
    }, index=dates)
    
    # Анализ M5 признаков
    features = m5_analyzer.analyze_m5_features(test_data)
    
    # Получение сводки
    summary = m5_analyzer.get_m5_summary(features)
    print("Сводка M5 анализа:", summary)
```

### H1 (1 час) - Среднесрочные уровни

**Теория:** H1 таймфрейм предназначен для анализа среднесрочных уровней и анализа основных трендов. Это критически важный таймфрейм для понимания общей рыночной динамики и принятия стратегических решений.

**Почему H1 анализ важен:**
- **Анализ трендов:** Обеспечивает анализ основных рыночных трендов
- **Среднесрочные уровни:** Выявляет среднесрочные уровни поддержки и сопротивления
- **Стратегические решения:** Подходит для принятия стратегических торговых решений
- **Стабильность:** Наиболее стабильные и надежные сигналы

**Плюсы:**
- Анализ основных трендов
- Стабильные сигналы
- Подходит для стратегических решений
- Минимальное влияние шума

**Минусы:**
- Меньше торговых возможностей
- Медленная реакция на изменения
- Требует больше времени для анализа
- Потенциальные упущенные возможности

**Практическая реализация:** Класс `SCHRLevelsH1Analysis` оптимизирован для часового таймфрейма, который является критически важным для понимания общей рыночной динамики и принятия стратегических торговых решений. H1 обеспечивает стабильные сигналы с минимальным влиянием рыночного шума.

**Детальное объяснение H1 анализа:**
- **Среднесрочные уровни:** Обнаруживает уровни, действующие в течение 1-4 часов
- **Трендовые пробои:** Детектирует пробои, которые могут изменить общий тренд
- **Среднесрочное давление:** Анализирует давление на более длительных временных интервалах
- **Стратегические решения:** Подходит для принятия стратегических торговых решений

**Почему H1 анализ критичен:**
- **Стратегическая важность:** Обеспечивает понимание общей рыночной динамики
- **Стабильность сигналов:** Наиболее стабильные и надежные сигналы
- **Минимальный шум:** Минимальное влияние рыночного шума
- **Трендовый анализ:** Лучший таймфрейм для анализа трендов

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import warnings
warnings.filterwarnings('ignore')

class SCHRLevelsH1Analysis:
    """
    Анализ SCHR Levels на часовом таймфрейме.
    
    Специализированный класс для анализа среднесрочных уровней и трендов
    на часовом таймфрейме, обеспечивающий стратегическое понимание
    рыночной динамики и принятие долгосрочных торговых решений.
    """
    
    def __init__(self, 
                 pressure_threshold: float = 0.7,
                 level_strength: float = 0.8,
                 prediction_horizon: int = 20,
                 volatility_factor: float = 1.5,
                 trend_threshold: float = 0.01):
        """
        Инициализация анализатора H1.
        
        Args:
            pressure_threshold: Порог давления для H1 (стандартный)
            level_strength: Минимальная сила уровня для H1
            prediction_horizon: Горизонт предсказания (стандартный для H1)
            volatility_factor: Фактор волатильности (стандартный для H1)
            trend_threshold: Порог для определения тренда (1%)
        """
        self.timeframe = 'H1'
        self.optimal_params = {
            'pressure_threshold': pressure_threshold,
            'level_strength': level_strength,
            'prediction_horizon': prediction_horizon,
            'volatility_factor': volatility_factor,
            'trend_threshold': trend_threshold
        }
        
        # Инициализация компонентов
        self.scaler = StandardScaler()
        self.feature_history = []
        self.trend_models = {}
        
        # Валидация параметров
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Валидация параметров для H1"""
        if not 0.0 <= self.optimal_params['pressure_threshold'] <= 1.0:
            raise ValueError("pressure_threshold должен быть между 0.0 и 1.0")
        if not 0.0 <= self.optimal_params['level_strength'] <= 1.0:
            raise ValueError("level_strength должен быть между 0.0 и 1.0")
        if self.optimal_params['prediction_horizon'] <= 0:
            raise ValueError("prediction_horizon должен быть положительным")
        if self.optimal_params['trend_threshold'] <= 0:
            raise ValueError("trend_threshold должен быть положительным")
    
    def analyze_h1_features(self, data: pd.DataFrame) -> Dict:
        """
        Комплексный анализ признаков для H1 таймфрейма.
        
        Args:
            data: DataFrame с OHLCV данными и SCHR колонками
            
        Returns:
            Dict с результатами анализа H1 признаков
        """
        try:
            # Проверка данных
            if len(data) < 50:
                raise ValueError("Недостаточно данных для анализа H1")
            
            features = {}
            
            # 1. Среднесрочные уровни
            features['medium_levels'] = self._detect_medium_levels(data)
            
            # 2. Трендовые пробои
            features['trend_breakouts'] = self._detect_trend_breakouts(data)
            
            # 3. Среднесрочное давление
            features['medium_pressure'] = self._analyze_medium_pressure(data)
            
            # 4. Трендовый анализ
            features['trend_analysis'] = self._analyze_trends(data)
            
            # 5. Аномалии и выбросы
            features['anomalies'] = self._detect_anomalies(data)
            
            # 6. Сезонность и циклы
            features['seasonality'] = self._analyze_seasonality(data)
            
            # 7. Корреляционный анализ
            features['correlations'] = self._analyze_correlations(data)
            
            # Сохранение истории
            self.feature_history.append({
                'timestamp': pd.Timestamp.now(),
                'features': features,
                'data_length': len(data)
            })
            
            return features
            
        except Exception as e:
            print(f"Ошибка в анализе H1 признаков: {e}")
            return {}
    
    def _detect_medium_levels(self, data: pd.DataFrame) -> Dict:
        """
        Детекция среднесрочных уровней для H1.
        
        Среднесрочные уровни - это уровни поддержки и сопротивления,
        которые действуют в течение 1-4 часов и подходят для среднесрочной торговли.
        """
        # Базовые уровни
        high_levels = data['predicted_high']
        low_levels = data['predicted_low']
        support_levels = data['support_level']
        resistance_levels = data['resistance_level']
        
        # Расстояния до уровней
        distance_to_high = (high_levels - data['Close']) / data['Close']
        distance_to_low = (data['Close'] - low_levels) / data['Close']
        distance_to_support = (data['Close'] - support_levels) / data['Close']
        distance_to_resistance = (resistance_levels - data['Close']) / data['Close']
        
        # Среднесрочные уровни (близко к цене)
        medium_threshold = 0.01  # 1% для H1
        medium_high = distance_to_high < medium_threshold
        medium_low = distance_to_low < medium_threshold
        medium_support = distance_to_support < medium_threshold
        medium_resistance = distance_to_resistance < medium_threshold
        
        # Сила среднесрочных уровней
        medium_strength = np.where(
            medium_high | medium_low | medium_support | medium_resistance,
            np.maximum(
                np.maximum(1 - distance_to_high, 1 - distance_to_low),
                np.maximum(1 - distance_to_support, 1 - distance_to_resistance)
            ),
            0
        )
        
        # Длительность уровней (как долго уровень держится)
        level_duration = self._calculate_level_duration(data)
        
        # Стабильность уровней
        level_stability = self._calculate_level_stability(data)
        
        # Значимость уровней (на основе объема и волатильности)
        level_significance = self._calculate_level_significance(data)
        
        return {
            'medium_high': medium_high,
            'medium_low': medium_low,
            'medium_support': medium_support,
            'medium_resistance': medium_resistance,
            'distance_to_high': distance_to_high,
            'distance_to_low': distance_to_low,
            'distance_to_support': distance_to_support,
            'distance_to_resistance': distance_to_resistance,
            'medium_strength': medium_strength,
            'level_duration': level_duration,
            'level_stability': level_stability,
            'level_significance': level_significance,
            'medium_level_count': np.sum(medium_high | medium_low | medium_support | medium_resistance)
        }
    
    def _detect_trend_breakouts(self, data: pd.DataFrame) -> Dict:
        """
        Детекция трендовых пробоев для H1.
        
        Трендовые пробои - это пробои уровней, которые могут изменить
        общий тренд и привести к значительным движениям цены.
        """
        # Базовые уровни
        high_levels = data['predicted_high']
        low_levels = data['predicted_low']
        support_levels = data['support_level']
        resistance_levels = data['resistance_level']
        
        # Детекция пробоев
        breakout_high = data['Close'] > high_levels
        breakout_low = data['Close'] < low_levels
        breakout_support = data['Close'] < support_levels
        breakout_resistance = data['Close'] > resistance_levels
        
        # Трендовые пробои (с подтверждением)
        trend_confirmation_window = 4  # 4 часа для подтверждения
        trend_breakout_high = breakout_high.rolling(window=trend_confirmation_window).sum() >= 2
        trend_breakout_low = breakout_low.rolling(window=trend_confirmation_window).sum() >= 2
        
        # Сила трендовых пробоев
        breakout_strength_high = np.where(
            trend_breakout_high,
            (data['Close'] - high_levels) / high_levels,
            0
        )
        breakout_strength_low = np.where(
            trend_breakout_low,
            (low_levels - data['Close']) / low_levels,
            0
        )
        
        # Объем при пробоях
        volume_confirmation = self._analyze_volume_at_breakouts(data, breakout_high, breakout_low)
        
        # Волатильность при пробоях
        volatility_confirmation = self._analyze_volatility_at_breakouts(data, breakout_high, breakout_low)
        
        # Частота трендовых пробоев
        trend_breakout_frequency = (trend_breakout_high | trend_breakout_low).rolling(window=24).sum() / 24
        
        return {
            'breakout_high': breakout_high,
            'breakout_low': breakout_low,
            'breakout_support': breakout_support,
            'breakout_resistance': breakout_resistance,
            'trend_breakout_high': trend_breakout_high,
            'trend_breakout_low': trend_breakout_low,
            'breakout_strength_high': breakout_strength_high,
            'breakout_strength_low': breakout_strength_low,
            'volume_confirmation': volume_confirmation,
            'volatility_confirmation': volatility_confirmation,
            'trend_breakout_frequency': trend_breakout_frequency
        }
    
    def _analyze_medium_pressure(self, data: pd.DataFrame) -> Dict:
        """
        Анализ среднесрочного давления для H1.
        
        Среднесрочное давление - это давление на уровни в более длительных
        временных интервалах, которое может указывать на направление тренда.
        """
        # Базовое давление
        base_pressure = data['pressure'] if 'pressure' in data.columns else np.ones(len(data))
        
        # Среднесрочное давление (изменения за 4-12 часов)
        medium_pressure_4 = base_pressure.rolling(window=4).mean()
        medium_pressure_12 = base_pressure.rolling(window=12).mean()
        medium_pressure_24 = base_pressure.rolling(window=24).mean()
        
        # Изменение давления
        pressure_change_4 = base_pressure.diff(4)
        pressure_change_12 = base_pressure.diff(12)
        pressure_change_24 = base_pressure.diff(24)
        
        # Направление давления
        pressure_direction = np.sign(pressure_change_4)
        
        # Ускорение давления
        pressure_acceleration = pressure_change_4.diff(4)
        
        # Волатильность давления
        pressure_volatility = base_pressure.rolling(window=12).std()
        
        # Пороги для H1
        pressure_threshold = self.optimal_params['pressure_threshold']
        high_pressure = base_pressure > pressure_threshold
        extreme_pressure = base_pressure > pressure_threshold * 1.2
        
        # Тренд давления
        pressure_trend = base_pressure.rolling(window=24).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        
        # Циклические паттерны давления
        pressure_cycles = self._detect_pressure_cycles(base_pressure)
        
        return {
            'base_pressure': base_pressure,
            'medium_pressure_4': medium_pressure_4,
            'medium_pressure_12': medium_pressure_12,
            'medium_pressure_24': medium_pressure_24,
            'pressure_change_4': pressure_change_4,
            'pressure_change_12': pressure_change_12,
            'pressure_change_24': pressure_change_24,
            'pressure_direction': pressure_direction,
            'pressure_acceleration': pressure_acceleration,
            'pressure_volatility': pressure_volatility,
            'high_pressure': high_pressure,
            'extreme_pressure': extreme_pressure,
            'pressure_trend': pressure_trend,
            'pressure_cycles': pressure_cycles
        }
    
    def _analyze_trends(self, data: pd.DataFrame) -> Dict:
        """
        Анализ трендов для H1.
        
        Анализ трендов помогает определить общее направление движения
        и его силу на часовом таймфрейме.
        """
        # Базовые данные
        close = data['Close']
        high = data['High']
        low = data['Low']
        volume = data['Volume'] if 'Volume' in data.columns else np.ones(len(data))
        
        # Простые скользящие средние
        sma_12 = close.rolling(window=12).mean()
        sma_24 = close.rolling(window=24).mean()
        sma_48 = close.rolling(window=48).mean()
        
        # Экспоненциальные скользящие средние
        ema_12 = close.ewm(span=12).mean()
        ema_24 = close.ewm(span=24).mean()
        ema_48 = close.ewm(span=48).mean()
        
        # Направление тренда
        trend_direction = np.where(
            close > sma_24, 1,  # Восходящий
            np.where(close < sma_24, -1, 0)  # Нисходящий, боковой
        )
        
        # Сила тренда
        trend_strength = abs(close - sma_24) / sma_24
        
        # Ускорение тренда
        trend_acceleration = sma_12.diff(4)
        
        # MACD
        macd = ema_12 - ema_24
        macd_signal = macd.ewm(span=9).mean()
        macd_histogram = macd - macd_signal
        
        # RSI
        rsi = self._calculate_rsi(close, 14)
        
        # Bollinger Bands
        bb_middle = sma_24
        bb_std = close.rolling(window=24).std()
        bb_upper = bb_middle + (bb_std * 2)
        bb_lower = bb_middle - (bb_std * 2)
        
        # ADX (Average Directional Index)
        adx = self._calculate_adx(high, low, close, 14)
        
        # Stochastic Oscillator
        stoch_k, stoch_d = self._calculate_stochastic(high, low, close, 14, 3)
        
        return {
            'sma_12': sma_12,
            'sma_24': sma_24,
            'sma_48': sma_48,
            'ema_12': ema_12,
            'ema_24': ema_24,
            'ema_48': ema_48,
            'trend_direction': trend_direction,
            'trend_strength': trend_strength,
            'trend_acceleration': trend_acceleration,
            'macd': macd,
            'macd_signal': macd_signal,
            'macd_histogram': macd_histogram,
            'rsi': rsi,
            'bb_upper': bb_upper,
            'bb_middle': bb_middle,
            'bb_lower': bb_lower,
            'adx': adx,
            'stoch_k': stoch_k,
            'stoch_d': stoch_d
        }
    
    def _detect_anomalies(self, data: pd.DataFrame) -> Dict:
        """
        Детекция аномалий и выбросов для H1.
        
        Аномалии могут указывать на необычные рыночные условия
        или потенциальные возможности для торговли.
        """
        # Подготовка данных для детекции аномалий
        features = np.column_stack([
            data['Close'].values,
            data['High'].values,
            data['Low'].values,
            data['Volume'].values if 'Volume' in data.columns else np.ones(len(data)),
            data['pressure'].values if 'pressure' in data.columns else np.ones(len(data))
        ])
        
        # Удаление NaN значений
        valid_mask = ~np.isnan(features).any(axis=1)
        features_clean = features[valid_mask]
        
        if len(features_clean) < 10:
            return {'anomalies': None, 'anomaly_scores': None}
        
        # Isolation Forest для детекции аномалий
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomaly_labels = iso_forest.fit_predict(features_clean)
        anomaly_scores = iso_forest.decision_function(features_clean)
        
        # Создание полных меток
        full_labels = np.full(len(data), 1)  # 1 = нормальный
        full_scores = np.full(len(data), 0.0)
        full_labels[valid_mask] = anomaly_labels
        full_scores[valid_mask] = anomaly_scores
        
        # Аномалии (метка -1)
        anomalies = full_labels == -1
        
        return {
            'anomalies': anomalies,
            'anomaly_scores': full_scores,
            'anomaly_count': np.sum(anomalies)
        }
    
    def _analyze_seasonality(self, data: pd.DataFrame) -> Dict:
        """
        Анализ сезонности и циклов для H1.
        
        Сезонность может влиять на поведение уровней и давления
        в зависимости от времени дня, дня недели и других факторов.
        """
        # Временные компоненты
        timestamps = pd.to_datetime(data.index) if hasattr(data.index, 'to_datetime') else data.index
        hour = timestamps.hour if hasattr(timestamps, 'hour') else np.zeros(len(data))
        day_of_week = timestamps.dayofweek if hasattr(timestamps, 'dayofweek') else np.zeros(len(data))
        day_of_month = timestamps.day if hasattr(timestamps, 'day') else np.zeros(len(data))
        
        # Анализ по часам
        hourly_analysis = {}
        for h in range(24):
            hour_mask = hour == h
            if hour_mask.sum() > 0:
                hourly_analysis[f'hour_{h}'] = {
                    'count': hour_mask.sum(),
                    'avg_pressure': data['pressure'][hour_mask].mean() if 'pressure' in data.columns else 0,
                    'avg_volatility': data['Close'][hour_mask].std() if len(data[hour_mask]) > 1 else 0,
                    'avg_volume': data['Volume'][hour_mask].mean() if 'Volume' in data.columns else 0
                }
        
        # Анализ по дням недели
        daily_analysis = {}
        for d in range(7):
            day_mask = day_of_week == d
            if day_mask.sum() > 0:
                daily_analysis[f'day_{d}'] = {
                    'count': day_mask.sum(),
                    'avg_pressure': data['pressure'][day_mask].mean() if 'pressure' in data.columns else 0,
                    'avg_volatility': data['Close'][day_mask].std() if len(data[day_mask]) > 1 else 0,
                    'avg_volume': data['Volume'][day_mask].mean() if 'Volume' in data.columns else 0
                }
        
        # Циклические паттерны
        cycles = self._detect_cyclical_patterns(data)
        
        return {
            'hourly_analysis': hourly_analysis,
            'daily_analysis': daily_analysis,
            'cycles': cycles,
            'current_hour': hour,
            'current_day': day_of_week,
            'current_day_of_month': day_of_month
        }
    
    def _analyze_correlations(self, data: pd.DataFrame) -> Dict:
        """
        Анализ корреляций между различными признаками для H1.
        
        Корреляционный анализ помогает понять взаимосвязи между
        различными компонентами SCHR Levels.
        """
        # Подготовка данных для корреляционного анализа
        numeric_columns = ['Close', 'High', 'Low', 'Volume', 'pressure', 
                          'predicted_high', 'predicted_low', 'support_level', 'resistance_level']
        
        # Фильтрация существующих колонок
        available_columns = [col for col in numeric_columns if col in data.columns]
        correlation_data = data[available_columns]
        
        # Расчет корреляций
        correlations = correlation_data.corr()
        
        # Наиболее коррелированные пары
        corr_pairs = []
        for i in range(len(correlations.columns)):
            for j in range(i+1, len(correlations.columns)):
                corr_value = correlations.iloc[i, j]
                if not np.isnan(corr_value):
                    corr_pairs.append({
                        'feature1': correlations.columns[i],
                        'feature2': correlations.columns[j],
                        'correlation': corr_value,
                        'abs_correlation': abs(corr_value)
                    })
        
        # Сортировка по абсолютной корреляции
        corr_pairs.sort(key=lambda x: x['abs_correlation'], reverse=True)
        
        return {
            'correlation_matrix': correlations,
            'top_correlations': corr_pairs[:10],  # Топ-10 корреляций
            'high_correlations': [pair for pair in corr_pairs if pair['abs_correlation'] > 0.7]
        }
    
    def _calculate_level_duration(self, data: pd.DataFrame) -> pd.Series:
        """Расчет длительности уровней"""
        # Простой расчет длительности на основе стабильности уровней
        level_changes = data['predicted_high'].diff().abs() + data['predicted_low'].diff().abs()
        duration = level_changes.rolling(window=12).apply(lambda x: len(x) - np.sum(x > 0.001))
        return duration.fillna(0)
    
    def _calculate_level_stability(self, data: pd.DataFrame) -> pd.Series:
        """Расчет стабильности уровней"""
        level_changes = data['predicted_high'].diff().abs() + data['predicted_low'].diff().abs()
        stability = 1 / (1 + level_changes.rolling(window=12).mean())
        return stability.fillna(0)
    
    def _calculate_level_significance(self, data: pd.DataFrame) -> pd.Series:
        """Расчет значимости уровней"""
        # Комбинация объема и волатильности
        volume_factor = data['Volume'] / data['Volume'].rolling(24).mean() if 'Volume' in data.columns else np.ones(len(data))
        volatility_factor = data['Close'].rolling(12).std() / data['Close'].rolling(24).std()
        significance = volume_factor * volatility_factor
        return significance.fillna(1)
    
    def _analyze_volume_at_breakouts(self, data: pd.DataFrame, breakout_high: pd.Series, breakout_low: pd.Series) -> Dict:
        """Анализ объема при пробоях"""
        if 'Volume' not in data.columns:
            return {'volume_confirmation': np.zeros(len(data))}
        
        # Средний объем
        avg_volume = data['Volume'].rolling(24).mean()
        
        # Объем при пробоях
        volume_at_breakout_high = np.where(breakout_high, data['Volume'] / avg_volume, 1)
        volume_at_breakout_low = np.where(breakout_low, data['Volume'] / avg_volume, 1)
        
        # Подтверждение пробоя объемом
        volume_confirmation = (volume_at_breakout_high > 1.2) | (volume_at_breakout_low > 1.2)
        
        return {
            'volume_confirmation': volume_confirmation,
            'volume_ratio_high': volume_at_breakout_high,
            'volume_ratio_low': volume_at_breakout_low
        }
    
    def _analyze_volatility_at_breakouts(self, data: pd.DataFrame, breakout_high: pd.Series, breakout_low: pd.Series) -> Dict:
        """Анализ волатильности при пробоях"""
        # Волатильность
        volatility = data['Close'].rolling(12).std()
        avg_volatility = volatility.rolling(24).mean()
        
        # Волатильность при пробоях
        vol_at_breakout_high = np.where(breakout_high, volatility / avg_volatility, 1)
        vol_at_breakout_low = np.where(breakout_low, volatility / avg_volatility, 1)
        
        # Подтверждение пробоя волатильностью
        volatility_confirmation = (vol_at_breakout_high > 1.1) | (vol_at_breakout_low > 1.1)
        
        return {
            'volatility_confirmation': volatility_confirmation,
            'volatility_ratio_high': vol_at_breakout_high,
            'volatility_ratio_low': vol_at_breakout_low
        }
    
    def _detect_pressure_cycles(self, pressure: pd.Series) -> Dict:
        """Детекция циклических паттернов давления"""
        # Простой анализ циклов с помощью автокорреляции
        autocorr = pressure.autocorr(lag=12)
        
        # Детекция циклов
        cycles = pressure.rolling(window=24).apply(lambda x: len(np.where(np.diff(np.sign(x.diff())))[0]))
        
        return {
            'autocorrelation': autocorr,
            'cycle_count': cycles,
            'has_cycles': abs(autocorr) > 0.3 if not np.isnan(autocorr) else False
        }
    
    def _detect_cyclical_patterns(self, data: pd.DataFrame) -> Dict:
        """Детекция циклических паттернов"""
        # Анализ циклов в цене
        price_cycles = data['Close'].rolling(window=24).apply(lambda x: len(np.where(np.diff(np.sign(x.diff())))[0]))
        
        # Анализ циклов в объеме
        volume_cycles = data['Volume'].rolling(window=24).apply(lambda x: len(np.where(np.diff(np.sign(x.diff())))[0])) if 'Volume' in data.columns else pd.Series(0, index=data.index)
        
        return {
            'price_cycles': price_cycles,
            'volume_cycles': volume_cycles,
            'cycle_strength': (price_cycles + volume_cycles) / 2
        }
    
    def _calculate_rsi(self, close: pd.Series, period: int = 14) -> pd.Series:
        """Расчет RSI"""
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50)
    
    def _calculate_adx(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Расчет ADX"""
        # True Range
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Directional Movement
        dm_plus = np.where((high.diff() > low.diff().abs()) & (high.diff() > 0), high.diff(), 0)
        dm_minus = np.where((low.diff().abs() > high.diff()) & (low.diff() < 0), low.diff().abs(), 0)
        
        # Smoothed values
        atr = tr.rolling(window=period).mean()
        di_plus = 100 * pd.Series(dm_plus).rolling(window=period).mean() / atr
        di_minus = 100 * pd.Series(dm_minus).rolling(window=period).mean() / atr
        
        # ADX
        dx = 100 * abs(di_plus - di_minus) / (di_plus + di_minus)
        adx = dx.rolling(window=period).mean()
        
        return adx.fillna(25)
    
    def _calculate_stochastic(self, high: pd.Series, low: pd.Series, close: pd.Series, k_period: int = 14, d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
        """Расчет Stochastic Oscillator"""
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        
        k_percent = 100 * (close - lowest_low) / (highest_high - lowest_low)
        d_percent = k_percent.rolling(window=d_period).mean()
        
        return k_percent.fillna(50), d_percent.fillna(50)
    
    def get_h1_summary(self, features: Dict) -> Dict:
        """
        Получение сводки по H1 анализу.
        
        Args:
            features: Результаты анализа H1 признаков
            
        Returns:
            Dict с сводкой H1 анализа
        """
        summary = {
            'timeframe': self.timeframe,
            'parameters': self.optimal_params,
            'analysis_timestamp': pd.Timestamp.now(),
            'feature_count': len(features)
        }
        
        # Сводка по среднесрочным уровням
        if 'medium_levels' in features:
            medium = features['medium_levels']
            summary['medium_levels'] = {
                'total_medium_levels': medium.get('medium_level_count', 0),
                'avg_duration': medium.get('level_duration', pd.Series()).mean(),
                'avg_stability': medium.get('level_stability', pd.Series()).mean(),
                'avg_significance': medium.get('level_significance', pd.Series()).mean()
            }
        
        # Сводка по трендовым пробоям
        if 'trend_breakouts' in features:
            breakouts = features['trend_breakouts']
            summary['trend_breakouts'] = {
                'total_trend_breakouts': breakouts.get('trend_breakout_frequency', pd.Series()).sum(),
                'volume_confirmation_rate': breakouts.get('volume_confirmation', pd.Series()).mean(),
                'volatility_confirmation_rate': breakouts.get('volatility_confirmation', pd.Series()).mean()
            }
        
        # Сводка по аномалиям
        if 'anomalies' in features:
            anomalies = features['anomalies']
            summary['anomalies'] = {
                'total_anomalies': anomalies.get('anomaly_count', 0),
                'anomaly_rate': anomalies.get('anomaly_count', 0) / len(features.get('medium_levels', {}).get('medium_high', pd.Series()))
            }
        
        return summary

# Пример использования
if __name__ == "__main__":
    # Создание анализатора H1
    h1_analyzer = SCHRLevelsH1Analysis()
    
    # Создание тестовых данных
    dates = pd.date_range('2023-01-01', periods=500, freq='1H')
    test_data = pd.DataFrame({
        'Open': np.random.uniform(1.25, 1.35, 500),
        'High': np.random.uniform(1.26, 1.36, 500),
        'Low': np.random.uniform(1.24, 1.34, 500),
        'Close': np.random.uniform(1.25, 1.35, 500),
        'Volume': np.random.uniform(1000, 10000, 500),
        'predicted_high': np.random.uniform(1.26, 1.36, 500),
        'predicted_low': np.random.uniform(1.24, 1.34, 500),
        'support_level': np.random.uniform(1.24, 1.34, 500),
        'resistance_level': np.random.uniform(1.26, 1.36, 500),
        'pressure': np.random.uniform(0.1, 2.0, 500)
    }, index=dates)
    
    # Анализ H1 признаков
    features = h1_analyzer.analyze_h1_features(test_data)
    
    # Получение сводки
    summary = h1_analyzer.get_h1_summary(features)
    print("Сводка H1 анализа:", summary)
```

## Создание признаков для ML

**Теория:** Создание признаков для машинного обучения на основе SCHR Levels является критически важным этапом для достижения высокой точности предсказаний. Качественные признаки определяют успех ML-модели.

**Почему создание признаков критично:**
- **Качество данных:** Качественные признаки определяют качество модели
- **Точность предсказаний:** Хорошие признаки повышают точность предсказаний
- **Робастность:** Правильные признаки обеспечивают робастность модели
- **Интерпретируемость:** Понятные признаки облегчают интерпретацию результатов

### 1. Базовые признаки SCHR Levels

**Теория:** Базовые признаки SCHR Levels представляют собой фундаментальные компоненты для анализа рыночных уровней. Они обеспечивают основу для более сложных признаков и являются основой для ML-модели.

**Почему базовые признаки важны:**
- **Фундаментальная основа:** Обеспечивают базовую информацию о рыночных уровнях
- **Простота интерпретации:** Легко понимаются и интерпретируются
- **Стабильность:** Обеспечивают стабильную основу для анализа
- **Эффективность:** Минимальные вычислительные требования

**Практическая реализация:** Класс `SCHRLevelsFeatureEngineer` представляет собой комплексную систему создания признаков для машинного обучения на основе SCHR Levels. Этот класс обеспечивает создание всех необходимых признаков для достижения высокой точности ML-моделей.

**Детальное объяснение создания признаков:**
- **Базовые признаки:** Фундаментальные компоненты SCHR Levels для анализа уровней
- **Признаки давления:** Количественные метрики рыночного давления и его динамики
- **Временные признаки:** Анализ временных аспектов и паттернов
- **Статистические признаки:** Статистические метрики для улучшения качества модели

**Почему создание признаков критично:**
- **Качество данных:** Качественные признаки определяют качество ML-модели
- **Точность предсказаний:** Хорошие признаки значительно повышают точность
- **Робастность:** Правильные признаки обеспечивают устойчивость модели
- **Интерпретируемость:** Понятные признаки облегчают интерпретацию результатов

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class SCHRLevelsFeatureEngineer:
    """
    Создание признаков на основе SCHR Levels для машинного обучения.
    
    Комплексная система создания признаков, которая преобразует сырые данные
    SCHR Levels в качественные признаки для ML-моделей, обеспечивая высокую
    точность предсказаний и робастность системы.
    """
    
    def __init__(self, 
                 lag_periods: List[int] = [1, 2, 3, 5, 10, 20],
                 rolling_windows: List[int] = [5, 10, 20, 50],
                 feature_selection_k: int = 50,
                 scaler_type: str = 'standard'):
        """
        Инициализация инженера признаков.
        
        Args:
            lag_periods: Периоды для создания лаговых признаков
            rolling_windows: Окна для скользящих статистик
            feature_selection_k: Количество лучших признаков для отбора
            scaler_type: Тип нормализации ('standard', 'minmax', 'robust')
        """
        self.lag_periods = lag_periods
        self.rolling_windows = rolling_windows
        self.feature_selection_k = feature_selection_k
        
        # Инициализация скейлеров
        if scaler_type == 'standard':
            self.scaler = StandardScaler()
        elif scaler_type == 'minmax':
            self.scaler = MinMaxScaler()
        elif scaler_type == 'robust':
            self.scaler = RobustScaler()
        else:
            raise ValueError("scaler_type должен быть 'standard', 'minmax' или 'robust'")
        
        # Инициализация селекторов признаков
        self.feature_selector = SelectKBest(score_func=f_classif, k=feature_selection_k)
        self.mutual_info_selector = SelectKBest(score_func=mutual_info_classif, k=feature_selection_k)
        
        # История созданных признаков
        self.feature_history = []
        self.feature_importance = {}
        
    def create_basic_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание базовых признаков SCHR Levels.
        
        Базовые признаки представляют собой фундаментальные компоненты
        для анализа уровней поддержки и сопротивления.
        
        Args:
            data: DataFrame с OHLCV данными и SCHR колонками
            
        Returns:
            DataFrame с базовыми признаками
        """
        features = pd.DataFrame(index=data.index)
        
        # 1. Основные уровни
        features['predicted_high'] = data['predicted_high']
        features['predicted_low'] = data['predicted_low']
        features['support_level'] = data['support_level']
        features['resistance_level'] = data['resistance_level']
        
        # 2. Расстояния до уровней (нормализованные)
        features['distance_to_high'] = (data['predicted_high'] - data['Close']) / data['Close']
        features['distance_to_low'] = (data['Close'] - data['predicted_low']) / data['Close']
        features['distance_to_support'] = (data['Close'] - data['support_level']) / data['Close']
        features['distance_to_resistance'] = (data['resistance_level'] - data['Close']) / data['Close']
        
        # 3. Диапазон уровней
        features['level_range'] = (data['predicted_high'] - data['predicted_low']) / data['Close']
        features['support_resistance_range'] = (data['resistance_level'] - data['support_level']) / data['Close']
        
        # 4. Позиция относительно уровней
        level_range = data['predicted_high'] - data['predicted_low']
        features['position_in_range'] = np.where(
            level_range > 0,
            (data['Close'] - data['predicted_low']) / level_range,
            0.5
        )
        
        # 5. Относительные уровни
        features['high_low_ratio'] = data['predicted_high'] / data['predicted_low']
        features['support_resistance_ratio'] = data['resistance_level'] / data['support_level']
        
        # 6. Близость к уровням
        features['closest_level_distance'] = np.minimum(
            features['distance_to_high'],
            features['distance_to_low']
        )
        features['closest_level_type'] = np.where(
            features['distance_to_high'] < features['distance_to_low'], 1, -1
        )
        
        return features
    
    def create_pressure_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание признаков давления на основе SCHR Levels.
        
        Признаки давления анализируют рыночное давление и его влияние
        на уровни поддержки и сопротивления.
        
        Args:
            data: DataFrame с OHLCV данными и SCHR колонками
            
        Returns:
            DataFrame с признаками давления
        """
        features = pd.DataFrame(index=data.index)
        
        # 1. Основные признаки давления
        features['pressure'] = data['pressure']
        features['pressure_vector'] = data['pressure_vector']
        features['pressure_strength'] = data['pressure_strength']
        features['pressure_direction'] = data['pressure_direction']
        
        # 2. Нормализованное давление
        features['pressure_normalized'] = data['pressure'] / data['Close']
        features['pressure_vector_normalized'] = data['pressure_vector'] / data['Close']
        
        # 3. Изменения давления
        features['pressure_change'] = data['pressure'].diff()
        features['pressure_vector_change'] = data['pressure_vector'].diff()
        features['pressure_strength_change'] = data['pressure_strength'].diff()
        
        # 4. Ускорение давления
        features['pressure_acceleration'] = data['pressure'].diff().diff()
        features['pressure_vector_acceleration'] = data['pressure_vector'].diff().diff()
        
        # 5. Волатильность давления
        for window in self.rolling_windows:
            features[f'pressure_volatility_{window}'] = data['pressure'].rolling(window).std()
            features[f'pressure_vector_volatility_{window}'] = data['pressure_vector'].rolling(window).std()
        
        # 6. Тренд давления
        for window in self.rolling_windows:
            features[f'pressure_trend_{window}'] = data['pressure'].rolling(window).apply(
                lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0
            )
        
        # 7. Экстремальные значения давления
        for window in self.rolling_windows:
            features[f'pressure_max_{window}'] = data['pressure'].rolling(window).max()
            features[f'pressure_min_{window}'] = data['pressure'].rolling(window).min()
            features[f'pressure_quantile_75_{window}'] = data['pressure'].rolling(window).quantile(0.75)
            features[f'pressure_quantile_25_{window}'] = data['pressure'].rolling(window).quantile(0.25)
        
        return features
    
    def create_temporal_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание временных признаков SCHR Levels.
        
        Временные признаки учитывают временные аспекты рыночной динамики,
        включая циклы, сезонность и временные паттерны.
        
        Args:
            data: DataFrame с OHLCV данными и SCHR колонками
            
        Returns:
            DataFrame с временными признаками
        """
        features = pd.DataFrame(index=data.index)
        
        # 1. Временные компоненты
        timestamps = pd.to_datetime(data.index) if hasattr(data.index, 'to_datetime') else data.index
        
        # Часы дня
        features['hour'] = timestamps.hour if hasattr(timestamps, 'hour') else 0
        features['hour_sin'] = np.sin(2 * np.pi * features['hour'] / 24)
        features['hour_cos'] = np.cos(2 * np.pi * features['hour'] / 24)
        
        # Дни недели
        features['day_of_week'] = timestamps.dayofweek if hasattr(timestamps, 'dayofweek') else 0
        features['day_sin'] = np.sin(2 * np.pi * features['day_of_week'] / 7)
        features['day_cos'] = np.cos(2 * np.pi * features['day_of_week'] / 7)
        
        # Дни месяца
        features['day_of_month'] = timestamps.day if hasattr(timestamps, 'day') else 1
        features['month'] = timestamps.month if hasattr(timestamps, 'month') else 1
        
        # 2. Лаговые признаки
        for lag in self.lag_periods:
            features[f'pressure_lag_{lag}'] = data['pressure'].shift(lag)
            features[f'close_lag_{lag}'] = data['Close'].shift(lag)
            features[f'volume_lag_{lag}'] = data['Volume'].shift(lag) if 'Volume' in data.columns else 0
        
        # 3. Скользящие статистики
        for window in self.rolling_windows:
            # Средние значения
            features[f'pressure_mean_{window}'] = data['pressure'].rolling(window).mean()
            features[f'close_mean_{window}'] = data['Close'].rolling(window).mean()
            
            # Стандартные отклонения
            features[f'pressure_std_{window}'] = data['pressure'].rolling(window).std()
            features[f'close_std_{window}'] = data['Close'].rolling(window).std()
            
            # Минимумы и максимумы
            features[f'pressure_min_{window}'] = data['pressure'].rolling(window).min()
            features[f'pressure_max_{window}'] = data['pressure'].rolling(window).max()
            features[f'close_min_{window}'] = data['Close'].rolling(window).min()
            features[f'close_max_{window}'] = data['Close'].rolling(window).max()
            
            # Квантили
            features[f'pressure_q25_{window}'] = data['pressure'].rolling(window).quantile(0.25)
            features[f'pressure_q75_{window}'] = data['pressure'].rolling(window).quantile(0.75)
        
        # 4. Временные паттерны
        features['is_weekend'] = features['day_of_week'].isin([5, 6]).astype(int)
        features['is_market_open'] = ((features['hour'] >= 9) & (features['hour'] <= 17)).astype(int)
        
        return features
    
    def create_interaction_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание признаков взаимодействия между различными компонентами.
        
        Признаки взаимодействия выявляют нелинейные зависимости между
        различными компонентами SCHR Levels.
        
        Args:
            data: DataFrame с OHLCV данными и SCHR колонками
            
        Returns:
            DataFrame с признаками взаимодействия
        """
        features = pd.DataFrame(index=data.index)
        
        # 1. Взаимодействие давления и уровней
        features['pressure_level_interaction'] = data['pressure'] * data['predicted_high'] / data['Close']
        features['pressure_support_interaction'] = data['pressure'] * data['support_level'] / data['Close']
        features['pressure_resistance_interaction'] = data['pressure'] * data['resistance_level'] / data['Close']
        
        # 2. Взаимодействие давления и волатильности
        volatility = data['Close'].rolling(20).std()
        features['pressure_volatility_interaction'] = data['pressure'] * volatility
        
        # 3. Взаимодействие уровней и объема
        if 'Volume' in data.columns:
            features['level_volume_interaction'] = (data['predicted_high'] - data['predicted_low']) * data['Volume']
            features['support_volume_interaction'] = data['support_level'] * data['Volume']
            features['resistance_volume_interaction'] = data['resistance_level'] * data['Volume']
        
        # 4. Полиномиальные признаки
        features['pressure_squared'] = data['pressure'] ** 2
        features['pressure_cubed'] = data['pressure'] ** 3
        features['level_range_squared'] = ((data['predicted_high'] - data['predicted_low']) / data['Close']) ** 2
        
        # 5. Логарифмические признаки
        features['log_pressure'] = np.log1p(data['pressure'])
        features['log_level_range'] = np.log1p((data['predicted_high'] - data['predicted_low']) / data['Close'])
        
        # 6. Признаки отношений
        features['pressure_volume_ratio'] = data['pressure'] / data['Volume'] if 'Volume' in data.columns else 0
        features['level_volatility_ratio'] = (data['predicted_high'] - data['predicted_low']) / volatility
        
        return features
    
    def create_statistical_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание статистических признаков SCHR Levels.
        
        Статистические признаки предоставляют дополнительную информацию
        о распределении и характеристиках данных.
        
        Args:
            data: DataFrame с OHLCV данными и SCHR колонками
            
        Returns:
            DataFrame со статистическими признаками
        """
        features = pd.DataFrame(index=data.index)
        
        # 1. Z-скоры
        for window in self.rolling_windows:
            rolling_mean = data['pressure'].rolling(window).mean()
            rolling_std = data['pressure'].rolling(window).std()
            features[f'pressure_zscore_{window}'] = (data['pressure'] - rolling_mean) / rolling_std
            
            rolling_mean_close = data['Close'].rolling(window).mean()
            rolling_std_close = data['Close'].rolling(window).std()
            features[f'close_zscore_{window}'] = (data['Close'] - rolling_mean_close) / rolling_std_close
        
        # 2. Процентили
        for window in self.rolling_windows:
            features[f'pressure_percentile_{window}'] = data['pressure'].rolling(window).rank(pct=True)
            features[f'close_percentile_{window}'] = data['Close'].rolling(window).rank(pct=True)
        
        # 3. Асимметрия и эксцесс
        for window in self.rolling_windows:
            features[f'pressure_skew_{window}'] = data['pressure'].rolling(window).skew()
            features[f'pressure_kurt_{window}'] = data['pressure'].rolling(window).kurt()
            features[f'close_skew_{window}'] = data['Close'].rolling(window).skew()
            features[f'close_kurt_{window}'] = data['Close'].rolling(window).kurt()
        
        # 4. Автокорреляция
        for lag in [1, 2, 3, 5, 10]:
            features[f'pressure_autocorr_{lag}'] = data['pressure'].rolling(20).apply(
                lambda x: x.autocorr(lag=lag) if len(x) > lag else 0
            )
        
        # 5. Энтропия (приблизительная)
        for window in self.rolling_windows:
            features[f'pressure_entropy_{window}'] = data['pressure'].rolling(window).apply(
                lambda x: self._calculate_entropy(x) if len(x) > 1 else 0
            )
        
        return features
    
    def create_all_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание всех признаков SCHR Levels.
        
        Объединяет все типы признаков в единый DataFrame для обучения ML-модели.
        
        Args:
            data: DataFrame с OHLCV данными и SCHR колонками
            
        Returns:
            DataFrame со всеми признаками
        """
        print("Создание базовых признаков...")
        basic_features = self.create_basic_features(data)
        
        print("Создание признаков давления...")
        pressure_features = self.create_pressure_features(data)
        
        print("Создание временных признаков...")
        temporal_features = self.create_temporal_features(data)
        
        print("Создание признаков взаимодействия...")
        interaction_features = self.create_interaction_features(data)
        
        print("Создание статистических признаков...")
        statistical_features = self.create_statistical_features(data)
        
        # Объединение всех признаков
        all_features = pd.concat([
            basic_features,
            pressure_features,
            temporal_features,
            interaction_features,
            statistical_features
        ], axis=1)
        
        # Удаление колонок с NaN значениями
        all_features = all_features.dropna()
        
        # Сохранение истории
        self.feature_history.append({
            'timestamp': pd.Timestamp.now(),
            'feature_count': len(all_features.columns),
            'data_shape': all_features.shape
        })
        
        print(f"Создано {len(all_features.columns)} признаков")
        return all_features
    
    def select_features(self, X: pd.DataFrame, y: pd.Series, method: str = 'f_classif') -> pd.DataFrame:
        """
        Отбор лучших признаков для ML-модели.
        
        Args:
            X: DataFrame с признаками
            y: Series с целевой переменной
            method: Метод отбора признаков ('f_classif', 'mutual_info')
            
        Returns:
            DataFrame с отобранными признаками
        """
        if method == 'f_classif':
            selector = self.feature_selector
        elif method == 'mutual_info':
            selector = self.mutual_info_selector
        else:
            raise ValueError("method должен быть 'f_classif' или 'mutual_info'")
        
        # Отбор признаков
        X_selected = selector.fit_transform(X, y)
        selected_features = X.columns[selector.get_support()]
        
        # Сохранение важности признаков
        self.feature_importance[method] = {
            'scores': selector.scores_,
            'selected_features': selected_features.tolist()
        }
        
        return pd.DataFrame(X_selected, columns=selected_features, index=X.index)
    
    def scale_features(self, X: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Нормализация признаков.
        
        Args:
            X: DataFrame с признаками
            fit: Обучать скейлер на данных
            
        Returns:
            DataFrame с нормализованными признаками
        """
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    
    def _calculate_entropy(self, series: pd.Series) -> float:
        """Расчет энтропии для серии"""
        try:
            # Дискретизация для расчета энтропии
            bins = pd.cut(series, bins=10, labels=False, include_lowest=True)
            value_counts = bins.value_counts()
            probabilities = value_counts / len(bins)
            entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
            return entropy
        except:
            return 0.0
    
    def get_feature_summary(self) -> Dict:
        """
        Получение сводки по созданным признакам.
        
        Returns:
            Dict с сводкой по признакам
        """
        summary = {
            'total_features_created': len(self.feature_history),
            'feature_importance': self.feature_importance,
            'scaler_type': type(self.scaler).__name__,
            'lag_periods': self.lag_periods,
            'rolling_windows': self.rolling_windows
        }
        
        return summary

# Пример использования
if __name__ == "__main__":
    # Создание инженера признаков
    feature_engineer = SCHRLevelsFeatureEngineer()
    
    # Создание тестовых данных
    dates = pd.date_range('2023-01-01', periods=1000, freq='1H')
    test_data = pd.DataFrame({
        'Open': np.random.uniform(1.25, 1.35, 1000),
        'High': np.random.uniform(1.26, 1.36, 1000),
        'Low': np.random.uniform(1.24, 1.34, 1000),
        'Close': np.random.uniform(1.25, 1.35, 1000),
        'Volume': np.random.uniform(1000, 10000, 1000),
        'predicted_high': np.random.uniform(1.26, 1.36, 1000),
        'predicted_low': np.random.uniform(1.24, 1.34, 1000),
        'support_level': np.random.uniform(1.24, 1.34, 1000),
        'resistance_level': np.random.uniform(1.26, 1.36, 1000),
        'pressure': np.random.uniform(0.1, 2.0, 1000),
        'pressure_vector': np.random.uniform(-1.0, 1.0, 1000),
        'pressure_strength': np.random.uniform(0.0, 1.0, 1000),
        'pressure_direction': np.random.choice([-1, 0, 1], 1000)
    }, index=dates)
    
    # Создание всех признаков
    features = feature_engineer.create_all_features(test_data)
    
    # Создание целевой переменной для демонстрации
    target = (test_data['Close'].shift(-1) > test_data['Close']).astype(int)
    target = target[features.index]
    
    # Отбор признаков
    selected_features = feature_engineer.select_features(features, target)
    
    # Нормализация признаков
    scaled_features = feature_engineer.scale_features(selected_features)
    
    print("Сводка по признакам:", feature_engineer.get_feature_summary())
    print(f"Исходное количество признаков: {len(features.columns)}")
    print(f"Отобранное количество признаков: {len(selected_features.columns)}")
    print(f"Форма нормализованных признаков: {scaled_features.shape}")
```

### 2. Продвинутые признаки

**Теория:** Продвинутые признаки SCHR Levels представляют собой сложные комбинации базовых признаков, которые выявляют скрытые паттерны и взаимосвязи в данных уровней. Они критически важны для достижения высокой точности ML-модели.

**Почему продвинутые признаки критичны:**
- **Выявление паттернов:** Обнаруживают скрытые паттерны в данных
- **Повышение точности:** Значительно повышают точность предсказаний
- **Робастность:** Обеспечивают устойчивость к рыночному шуму
- **Адаптивность:** Позволяют модели адаптироваться к изменениям рынка

**Плюсы:**
- Высокая точность предсказаний
- Выявление скрытых паттернов
- Повышение робастности
- Адаптивность к изменениям

**Минусы:**
- Сложность вычислений
- Потенциальное переобучение
- Сложность интерпретации
- Высокие требования к данным

**Практическая реализация:** Функция `create_advanced_schr_features` создает сложные признаки, которые выявляют скрытые паттерны и взаимосвязи в данных SCHR Levels. Эти признаки критически важны для достижения высокой точности ML-модели.

**Детальное объяснение продвинутых признаков:**
- **Пробитие уровней:** Детектирует моменты, когда цена пробивает ключевые уровни
- **Отскоки от уровней:** Выявляет отскоки от уровней поддержки и сопротивления
- **Сила уровней:** Количественно оценивает силу различных уровней
- **Конвергенция уровней:** Анализирует сближение различных типов уровней
- **Волатильность относительно уровней:** Сравнивает волатильность с силой уровней
- **Тренд относительно уровней:** Анализирует тренд относительно динамики уровней

**Почему продвинутые признаки критичны:**
- **Выявление паттернов:** Обнаруживают скрытые паттерны в данных
- **Повышение точности:** Значительно повышают точность предсказаний
- **Робастность:** Обеспечивают устойчивость к рыночному шуму
- **Адаптивность:** Позволяют модели адаптироваться к изменениям рынка

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy import stats
from scipy.signal import find_peaks
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def create_advanced_schr_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Создание продвинутых признаков SCHR Levels.
    
    Продвинутые признаки представляют собой сложные комбинации базовых
    признаков, которые выявляют скрытые паттерны и взаимосвязи в данных
    уровней для достижения высокой точности ML-модели.
    
    Args:
        data: DataFrame с OHLCV данными и SCHR колонками
        
    Returns:
        DataFrame с продвинутыми признаками
    """
    features = pd.DataFrame(index=data.index)
    
    # 1. Пробитие уровней
    print("Создание признаков пробития уровней...")
    features['breakout_high'] = (data['Close'] > data['predicted_high']).astype(int)
    features['breakout_low'] = (data['Close'] < data['predicted_low']).astype(int)
    features['breakout_support'] = (data['Close'] < data['support_level']).astype(int)
    features['breakout_resistance'] = (data['Close'] > data['resistance_level']).astype(int)
    
    # Сила пробитий
    features['breakout_strength_high'] = np.where(
        features['breakout_high'],
        (data['Close'] - data['predicted_high']) / data['predicted_high'],
        0
    )
    features['breakout_strength_low'] = np.where(
        features['breakout_low'],
        (data['predicted_low'] - data['Close']) / data['predicted_low'],
        0
    )
    
    # 2. Отскоки от уровней
    print("Создание признаков отскоков...")
    features['bounce_from_high'] = ((data['Close'] < data['predicted_high']) & 
                                  (data['Close'].shift(1) >= data['predicted_high'])).astype(int)
    features['bounce_from_low'] = ((data['Close'] > data['predicted_low']) & 
                                 (data['Close'].shift(1) <= data['predicted_low'])).astype(int)
    features['bounce_from_support'] = ((data['Close'] > data['support_level']) & 
                                     (data['Close'].shift(1) <= data['support_level'])).astype(int)
    features['bounce_from_resistance'] = ((data['Close'] < data['resistance_level']) & 
                                        (data['Close'].shift(1) >= data['resistance_level'])).astype(int)
    
    # Сила отскоков
    features['bounce_strength_high'] = np.where(
        features['bounce_from_high'],
        (data['predicted_high'] - data['Close']) / data['predicted_high'],
        0
    )
    features['bounce_strength_low'] = np.where(
        features['bounce_from_low'],
        (data['Close'] - data['predicted_low']) / data['predicted_low'],
        0
    )
    
    # 3. Сила уровней
    print("Создание признаков силы уровней...")
    features['level_strength'] = abs(data['predicted_high'] - data['predicted_low']) / data['Close']
    features['support_strength'] = abs(data['Close'] - data['support_level']) / data['Close']
    features['resistance_strength'] = abs(data['resistance_level'] - data['Close']) / data['Close']
    
    # Относительная сила уровней
    features['relative_level_strength'] = features['level_strength'] / data['Close'].rolling(20).std()
    features['relative_support_strength'] = features['support_strength'] / data['Close'].rolling(20).std()
    features['relative_resistance_strength'] = features['resistance_strength'] / data['Close'].rolling(20).std()
    
    # 4. Конвергенция уровней
    print("Создание признаков конвергенции...")
    features['level_convergence'] = abs(data['predicted_high'] - data['resistance_level']) / data['Close']
    features['support_convergence'] = abs(data['predicted_low'] - data['support_level']) / data['Close']
    
    # Степень конвергенции
    features['convergence_ratio'] = features['level_convergence'] / (features['level_strength'] + 1e-10)
    features['support_convergence_ratio'] = features['support_convergence'] / (features['support_strength'] + 1e-10)
    
    # 5. Волатильность относительно уровней
    print("Создание признаков волатильности...")
    volatility = data['Close'].rolling(20).std()
    features['volatility_vs_levels'] = volatility / (features['level_strength'] + 1e-10)
    features['volatility_vs_support'] = volatility / (features['support_strength'] + 1e-10)
    features['volatility_vs_resistance'] = volatility / (features['resistance_strength'] + 1e-10)
    
    # 6. Тренд относительно уровней
    print("Создание признаков тренда...")
    price_change_20 = data['Close'] - data['Close'].shift(20)
    high_change_20 = data['predicted_high'] - data['predicted_high'].shift(20)
    low_change_20 = data['predicted_low'] - data['predicted_low'].shift(20)
    
    features['trend_vs_high'] = np.where(
        abs(high_change_20) > 1e-10,
        price_change_20 / high_change_20,
        0
    )
    features['trend_vs_low'] = np.where(
        abs(low_change_20) > 1e-10,
        price_change_20 / low_change_20,
        0
    )
    
    # 7. Паттерны уровней
    print("Создание признаков паттернов...")
    features['level_pattern_triangle'] = _detect_triangle_pattern(data)
    features['level_pattern_wedge'] = _detect_wedge_pattern(data)
    features['level_pattern_channel'] = _detect_channel_pattern(data)
    
    # 8. Моментные признаки
    print("Создание моментных признаков...")
    features['momentum_levels'] = _calculate_level_momentum(data)
    features['momentum_pressure'] = _calculate_pressure_momentum(data)
    
    # 9. Фрактальные признаки
    print("Создание фрактальных признаков...")
    features['fractal_dimension'] = _calculate_fractal_dimension(data)
    features['hurst_exponent'] = _calculate_hurst_exponent(data)
    
    # 10. Волновые признаки
    print("Создание волновых признаков...")
    features['wave_pattern'] = _detect_wave_patterns(data)
    features['wave_amplitude'] = _calculate_wave_amplitude(data)
    features['wave_frequency'] = _calculate_wave_frequency(data)
    
    # 11. Корреляционные признаки
    print("Создание корреляционных признаков...")
    features['price_pressure_correlation'] = _calculate_price_pressure_correlation(data)
    features['level_volume_correlation'] = _calculate_level_volume_correlation(data)
    
    # 12. Энтропийные признаки
    print("Создание энтропийных признаков...")
    features['price_entropy'] = _calculate_price_entropy(data)
    features['pressure_entropy'] = _calculate_pressure_entropy(data)
    
    # 13. Сезонные признаки
    print("Создание сезонных признаков...")
    features['seasonal_level_pattern'] = _detect_seasonal_level_patterns(data)
    features['seasonal_pressure_pattern'] = _detect_seasonal_pressure_patterns(data)
    
    # 14. Аномалии уровней
    print("Создание признаков аномалий...")
    features['level_anomaly'] = _detect_level_anomalies(data)
    features['pressure_anomaly'] = _detect_pressure_anomalies(data)
    
    # 15. Комбинированные признаки
    print("Создание комбинированных признаков...")
    features['breakout_bounce_ratio'] = _calculate_breakout_bounce_ratio(features)
    features['level_pressure_interaction'] = _calculate_level_pressure_interaction(data)
    features['multi_timeframe_strength'] = _calculate_multi_timeframe_strength(data)
    
    print(f"Создано {len(features.columns)} продвинутых признаков")
    return features

def _detect_triangle_pattern(data: pd.DataFrame) -> pd.Series:
    """Детекция треугольных паттернов"""
    high = data['High']
    low = data['Low']
    
    # Простая детекция треугольника
    high_trend = high.rolling(window=10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0)
    low_trend = low.rolling(window=10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0)
    
    # Сходящийся треугольник
    triangle = (high_trend < 0) & (low_trend > 0)
    
    return triangle.astype(int)

def _detect_wedge_pattern(data: pd.DataFrame) -> pd.Series:
    """Детекция клиновых паттернов"""
    high = data['High']
    low = data['Low']
    
    high_trend = high.rolling(window=10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0)
    low_trend = low.rolling(window=10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0)
    
    # Нисходящий клин
    wedge = (high_trend < 0) & (low_trend < 0) & (abs(high_trend) > abs(low_trend))
    
    return wedge.astype(int)

def _detect_channel_pattern(data: pd.DataFrame) -> pd.Series:
    """Детекция канальных паттернов"""
    high = data['High']
    low = data['Low']
    
    # Простая детекция канала
    high_ma = high.rolling(window=20).mean()
    low_ma = low.rolling(window=20).mean()
    
    channel = (high - high_ma).abs() < (high_ma * 0.01) & (low - low_ma).abs() < (low_ma * 0.01)
    
    return channel.astype(int)

def _calculate_level_momentum(data: pd.DataFrame) -> pd.Series:
    """Расчет моментных признаков уровней"""
    level_range = data['predicted_high'] - data['predicted_low']
    momentum = level_range.diff(5)
    
    return momentum.fillna(0)

def _calculate_pressure_momentum(data: pd.DataFrame) -> pd.Series:
    """Расчет моментных признаков давления"""
    pressure = data['pressure']
    momentum = pressure.diff(5)
    
    return momentum.fillna(0)

def _calculate_fractal_dimension(data: pd.DataFrame) -> pd.Series:
    """Расчет фрактальной размерности"""
    close = data['Close']
    
    def fractal_dim(series):
        if len(series) < 10:
            return 1.0
        
        # Упрощенный расчет фрактальной размерности
        n = len(series)
        L = np.sum(np.abs(np.diff(series)))
        return np.log(n) / (np.log(n) + np.log(L / (series.max() - series.min() + 1e-10)))
    
    fractal_dim_series = close.rolling(window=20).apply(fractal_dim)
    return fractal_dim_series.fillna(1.0)

def _calculate_hurst_exponent(data: pd.DataFrame) -> pd.Series:
    """Расчет экспоненты Херста"""
    close = data['Close']
    
    def hurst(series):
        if len(series) < 10:
            return 0.5
        
        # Упрощенный расчет экспоненты Херста
        lags = range(2, min(20, len(series)))
        tau = [np.sqrt(np.std(np.subtract(series[lag:], series[:-lag]))) for lag in lags]
        poly = np.polyfit(np.log(lags), np.log(tau), 1)
        return poly[0] * 2.0
    
    hurst_series = close.rolling(window=50).apply(hurst)
    return hurst_series.fillna(0.5)

def _detect_wave_patterns(data: pd.DataFrame) -> pd.Series:
    """Детекция волновых паттернов"""
    close = data['Close']
    
    # Поиск пиков и впадин
    peaks, _ = find_peaks(close, distance=5)
    valleys, _ = find_peaks(-close, distance=5)
    
    # Создание серии с волновыми паттернами
    wave_pattern = pd.Series(0, index=close.index)
    
    # Отметка пиков
    for peak in peaks:
        if peak < len(wave_pattern):
            wave_pattern.iloc[peak] = 1
    
    # Отметка впадин
    for valley in valleys:
        if valley < len(wave_pattern):
            wave_pattern.iloc[valley] = -1
    
    return wave_pattern

def _calculate_wave_amplitude(data: pd.DataFrame) -> pd.Series:
    """Расчет амплитуды волн"""
    close = data['Close']
    
    # Скользящая амплитуда
    amplitude = close.rolling(window=10).max() - close.rolling(window=10).min()
    
    return amplitude.fillna(0)

def _calculate_wave_frequency(data: pd.DataFrame) -> pd.Series:
    """Расчет частоты волн"""
    close = data['Close']
    
    # Подсчет пересечений средней линии
    mean_line = close.rolling(window=20).mean()
    crossings = (close > mean_line).astype(int).diff().abs()
    frequency = crossings.rolling(window=20).sum()
    
    return frequency.fillna(0)

def _calculate_price_pressure_correlation(data: pd.DataFrame) -> pd.Series:
    """Расчет корреляции цены и давления"""
    close = data['Close']
    pressure = data['pressure']
    
    correlation = close.rolling(window=20).corr(pressure)
    
    return correlation.fillna(0)

def _calculate_level_volume_correlation(data: pd.DataFrame) -> pd.Series:
    """Расчет корреляции уровней и объема"""
    if 'Volume' not in data.columns:
        return pd.Series(0, index=data.index)
    
    level_range = data['predicted_high'] - data['predicted_low']
    volume = data['Volume']
    
    correlation = level_range.rolling(window=20).corr(volume)
    
    return correlation.fillna(0)

def _calculate_price_entropy(data: pd.DataFrame) -> pd.Series:
    """Расчет энтропии цены"""
    close = data['Close']
    
    def entropy(series):
        if len(series) < 5:
            return 0.0
        
        # Дискретизация
        bins = pd.cut(series, bins=5, labels=False, include_lowest=True)
        value_counts = bins.value_counts()
        probabilities = value_counts / len(bins)
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        return entropy
    
    entropy_series = close.rolling(window=20).apply(entropy)
    return entropy_series.fillna(0)

def _calculate_pressure_entropy(data: pd.DataFrame) -> pd.Series:
    """Расчет энтропии давления"""
    pressure = data['pressure']
    
    def entropy(series):
        if len(series) < 5:
            return 0.0
        
        bins = pd.cut(series, bins=5, labels=False, include_lowest=True)
        value_counts = bins.value_counts()
        probabilities = value_counts / len(bins)
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        return entropy
    
    entropy_series = pressure.rolling(window=20).apply(entropy)
    return entropy_series.fillna(0)

def _detect_seasonal_level_patterns(data: pd.DataFrame) -> pd.Series:
    """Детекция сезонных паттернов уровней"""
    timestamps = pd.to_datetime(data.index) if hasattr(data.index, 'to_datetime') else data.index
    hour = timestamps.hour if hasattr(timestamps, 'hour') else 0
    
    # Простая сезонность по часам
    seasonal_pattern = np.sin(2 * np.pi * hour / 24)
    
    return pd.Series(seasonal_pattern, index=data.index)

def _detect_seasonal_pressure_patterns(data: pd.DataFrame) -> pd.Series:
    """Детекция сезонных паттернов давления"""
    timestamps = pd.to_datetime(data.index) if hasattr(data.index, 'to_datetime') else data.index
    hour = timestamps.hour if hasattr(timestamps, 'hour') else 0
    
    # Сезонность давления
    pressure_seasonal = np.cos(2 * np.pi * hour / 24)
    
    return pd.Series(pressure_seasonal, index=data.index)

def _detect_level_anomalies(data: pd.DataFrame) -> pd.Series:
    """Детекция аномалий уровней"""
    level_range = data['predicted_high'] - data['predicted_low']
    
    # Z-score для детекции аномалий
    mean_range = level_range.rolling(window=50).mean()
    std_range = level_range.rolling(window=50).std()
    z_score = (level_range - mean_range) / (std_range + 1e-10)
    
    anomalies = (z_score.abs() > 2).astype(int)
    return anomalies.fillna(0)

def _detect_pressure_anomalies(data: pd.DataFrame) -> pd.Series:
    """Детекция аномалий давления"""
    pressure = data['pressure']
    
    # Z-score для детекции аномалий
    mean_pressure = pressure.rolling(window=50).mean()
    std_pressure = pressure.rolling(window=50).std()
    z_score = (pressure - mean_pressure) / (std_pressure + 1e-10)
    
    anomalies = (z_score.abs() > 2).astype(int)
    return anomalies.fillna(0)

def _calculate_breakout_bounce_ratio(features: pd.DataFrame) -> pd.Series:
    """Расчет соотношения пробоев и отскоков"""
    total_breakouts = features['breakout_high'] + features['breakout_low']
    total_bounces = features['bounce_from_high'] + features['bounce_from_low']
    
    ratio = np.where(
        total_bounces > 0,
        total_breakouts / total_bounces,
        0
    )
    
    return pd.Series(ratio, index=features.index)

def _calculate_level_pressure_interaction(data: pd.DataFrame) -> pd.Series:
    """Расчет взаимодействия уровней и давления"""
    level_range = data['predicted_high'] - data['predicted_low']
    pressure = data['pressure']
    
    interaction = level_range * pressure / data['Close']
    
    return interaction

def _calculate_multi_timeframe_strength(data: pd.DataFrame) -> pd.Series:
    """Расчет силы на нескольких таймфреймах"""
    close = data['Close']
    
    # Различные периоды для мультитаймфреймового анализа
    periods = [5, 10, 20, 50]
    strength_components = []
    
    for period in periods:
        sma = close.rolling(window=period).mean()
        strength = abs(close - sma) / sma
        strength_components.append(strength)
    
    # Комбинированная сила
    multi_strength = np.mean(strength_components, axis=0)
    
    return pd.Series(multi_strength, index=data.index)

# Пример использования
if __name__ == "__main__":
    # Создание тестовых данных
    dates = pd.date_range('2023-01-01', periods=1000, freq='1H')
    test_data = pd.DataFrame({
        'Open': np.random.uniform(1.25, 1.35, 1000),
        'High': np.random.uniform(1.26, 1.36, 1000),
        'Low': np.random.uniform(1.24, 1.34, 1000),
        'Close': np.random.uniform(1.25, 1.35, 1000),
        'Volume': np.random.uniform(1000, 10000, 1000),
        'predicted_high': np.random.uniform(1.26, 1.36, 1000),
        'predicted_low': np.random.uniform(1.24, 1.34, 1000),
        'support_level': np.random.uniform(1.24, 1.34, 1000),
        'resistance_level': np.random.uniform(1.26, 1.36, 1000),
        'pressure': np.random.uniform(0.1, 2.0, 1000)
    }, index=dates)
    
    # Создание продвинутых признаков
    advanced_features = create_advanced_schr_features(test_data)
    
    print(f"Создано {len(advanced_features.columns)} продвинутых признаков")
    print("Колонки:", list(advanced_features.columns))
```

### 3. Временные признаки

**Теория:** Временные признаки SCHR Levels учитывают временные аспекты рыночной динамики, включая циклы, сезонность и временные паттерны уровней. Они критически важны для понимания временной структуры рынка.

**Почему временные признаки важны:**
- **Временная структура:** Учитывают временные аспекты рыночных уровней
- **Циклические паттерны:** Выявляют повторяющиеся паттерны уровней
- **Сезонность:** Учитывают сезонные эффекты
- **Временные зависимости:** Анализируют зависимости во времени

**Плюсы:**
- Учет временной структуры
- Выявление циклов
- Учет сезонности
- Анализ временных зависимостей

**Минусы:**
- Сложность вычислений
- Потенциальная нестационарность
- Сложность интерпретации
- Высокие требования к данным

```python
def create_temporal_schr_features(data):
    """Создание временных признаков SCHR Levels"""
    features = pd.DataFrame(index=data.index)
    
    # 1. Время с последнего пробоя
    features['time_since_breakout'] = self._calculate_time_since_breakout(data)
    
    # 2. Частота пробоев
    features['breakout_frequency'] = self._calculate_breakout_frequency(data)
    
    # 3. Длительность нахождения в диапазоне
    features['time_in_range'] = self._calculate_time_in_range(data)
    
    # 4. Циклические паттерны уровней
    features['level_cyclical_pattern'] = self._detect_level_cyclical_pattern(data)
    
    return features
```

## Создание целевых переменных

**Теория:** Создание целевых переменных является критически важным этапом для обучения ML-модели на основе SCHR Levels. Правильно определенные целевые переменные определяют успех всей системы машинного обучения.

**Почему создание целевых переменных критично:**
- **Определение задачи:** Четко определяет задачу машинного обучения
- **Качество обучения:** Качественные целевые переменные улучшают обучение
- **Интерпретируемость:** Понятные целевые переменные облегчают интерпретацию
- **Практическая применимость:** Обеспечивают практическую применимость результатов

### 1. Пробитие уровней

**Теория:** Пробитие уровней является наиболее важной целевой переменной для торговых систем на основе SCHR Levels. Она определяет основную задачу - предсказание пробоев уровней поддержки и сопротивления.

**Почему пробитие уровней важно:**
- **Основная задача:** Основная задача торговых систем на основе уровней
- **Практическая применимость:** Непосредственно применимо в торговле
- **Простота интерпретации:** Легко понимается и интерпретируется
- **Универсальность:** Подходит для различных торговых стратегий

**Плюсы:**
- Простота понимания
- Прямая применимость
- Универсальность
- Легкость интерпретации

**Минусы:**
- Упрощение сложности рынка
- Игнорирование силы движения
- Потенциальная потеря информации

```python
def create_level_breakout_target(data, horizon=1):
    """Создание целевой переменной - пробитие уровней"""
    future_high = data['predicted_high'].shift(-horizon)
    future_low = data['predicted_low'].shift(-horizon)
    future_close = data['Close'].shift(-horizon)
    
    # Классификация пробоев
    breakout_high = (future_close > future_high).astype(int)
    breakout_low = (future_close < future_low).astype(int)
    
    # Комбинированная целевая переменная
    target = np.where(breakout_high, 2,  # Пробой вверх
                     np.where(breakout_low, 0, 1))  # Пробой вниз, без пробоя
    
    return target
```

### 2. Отскоки от уровней

**Теория:** Отскоки от уровней представляют собой важную целевую переменную для торговых систем на основе SCHR Levels. Они определяют способность уровней поддержки и сопротивления удерживать цену.

**Почему отскоки от уровней важны:**
- **Сила уровней:** Определяют силу уровней поддержки и сопротивления
- **Торговые возможности:** Предоставляют торговые возможности
- **Управление рисками:** Помогают в управлении рисками
- **Оптимизация стратегий:** Позволяют оптимизировать торговые стратегии

**Плюсы:**
- Определение силы уровней
- Торговые возможности
- Улучшение управления рисками
- Оптимизация стратегий

**Минусы:**
- Сложность определения
- Потенциальная нестабильность
- Сложность интерпретации
- Высокие требования к данным

```python
def create_level_bounce_target(data, horizon=1):
    """Создание целевой переменной - отскоки от уровней"""
    future_high = data['predicted_high'].shift(-horizon)
    future_low = data['predicted_low'].shift(-horizon)
    future_close = data['Close'].shift(-horizon)
    
    # Детекция отскоков
    bounce_from_high = ((future_close < future_high) & 
                       (data['Close'] >= data['predicted_high'])).astype(int)
    bounce_from_low = ((future_close > future_low) & 
                      (data['Close'] <= data['predicted_low'])).astype(int)
    
    # Комбинированная целевая переменная
    target = np.where(bounce_from_high, 2,  # Отскок от максимума
                     np.where(bounce_from_low, 0, 1))  # Отскок от минимума, без отскока
    
    return target
```

### 3. Направление давления

**Теория:** Направление давления является критически важной целевой переменной для SCHR Levels, так как оно определяет направление рыночного давления и его влияние на ценовые уровни.

**Почему направление давления важно:**
- **Предсказание пробоев:** Помогает предсказывать пробои уровней
- **Анализ рыночного давления:** Анализирует рыночное давление
- **Управление рисками:** Помогает в управлении рисками
- **Оптимизация стратегий:** Позволяет оптимизировать торговые стратегии

**Плюсы:**
- Предсказание пробоев
- Анализ рыночного давления
- Улучшение управления рисками
- Оптимизация стратегий

**Минусы:**
- Сложность измерения
- Потенциальная нестабильность
- Сложность интерпретации
- Высокие требования к данным

```python
def create_pressure_direction_target(data, horizon=1):
    """Создание целевой переменной - направление давления"""
    future_pressure = data['pressure'].shift(-horizon)
    current_pressure = data['pressure']
    
    # Изменение давления
    pressure_change = future_pressure - current_pressure
    
    # Классификация направления
    target = pd.cut(
        pressure_change,
        bins=[-np.inf, -0.1, 0.1, np.inf],
        labels=[0, 1, 2],  # 0=down, 1=stable, 2=up
        include_lowest=True
    )
    
    return target.astype(int)
```

## ML-модели для SCHR Levels

**Теория:** ML-модели для SCHR Levels представляют собой комплексную систему машинного обучения, которая использует различные алгоритмы для анализа данных SCHR Levels и генерации торговых сигналов. Это критически важно для создания высокоточных торговых систем.

**Почему ML-модели критичны:**
- **Высокая точность:** Обеспечивают высокую точность предсказаний
- **Адаптивность:** Могут адаптироваться к изменениям рынка
- **Автоматизация:** Автоматизируют процесс анализа и принятия решений
- **Масштабируемость:** Могут обрабатывать большие объемы данных

### 1. Классификатор пробоев

**Теория:** Классификатор пробоев является основной задачей для торговых систем на основе SCHR Levels, где модель должна предсказать пробои уровней поддержки и сопротивления. Это критически важно для принятия торговых решений.

**Почему классификатор пробоев важен:**
- **Основная задача:** Основная задача торговых систем на основе уровней
- **Практическая применимость:** Непосредственно применимо в торговле
- **Простота интерпретации:** Легко интерпретируется
- **Универсальность:** Подходит для различных стратегий

**Плюсы:**
- Прямая применимость
- Простота интерпретации
- Универсальность
- Высокая точность

**Минусы:**
- Упрощение сложности
- Потенциальная потеря информации
- Ограниченная гибкость

```python
class SCHRLevelsClassifier:
    """Классификатор на основе SCHR Levels"""
    
    def __init__(self):
        self.models = {
            'xgboost': XGBClassifier(),
            'lightgbm': LGBMClassifier(),
            'catboost': CatBoostClassifier(),
            'random_forest': RandomForestClassifier(),
            'neural_network': MLPClassifier()
        }
        self.ensemble = VotingClassifier(
            estimators=list(self.models.items()),
            voting='soft'
        )
    
    def train(self, X, y):
        """Обучение модели"""
        # Разделение на train/validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Обучение ансамбля
        self.ensemble.fit(X_train, y_train)
        
        # Валидация
        val_score = self.ensemble.score(X_val, y_val)
        print(f"Validation accuracy: {val_score:.4f}")
        
        return self.ensemble
    
    def predict(self, X):
        """Предсказание"""
        return self.ensemble.predict(X)
    
    def predict_proba(self, X):
        """Предсказание вероятностей"""
        return self.ensemble.predict_proba(X)
```

### 2. Регрессор для прогнозирования уровней

**Теория:** Регрессор для прогнозирования уровней представляет собой более сложную задачу, где модель должна предсказать конкретные значения уровней поддержки и сопротивления. Это критически важно для точного управления позициями.

**Почему регрессор важен:**
- **Точность прогнозов:** Обеспечивает более точные прогнозы уровней
- **Управление позициями:** Помогает в точном управлении позициями
- **Оптимизация стратегий:** Позволяет оптимизировать торговые стратегии
- **Управление рисками:** Помогает в управлении рисками

**Плюсы:**
- Более точные прогнозы
- Лучшее управление позициями
- Оптимизация стратегий
- Улучшение управления рисками

**Минусы:**
- Сложность обучения
- Потенциальная нестабильность
- Сложность интерпретации
- Высокие требования к данным

```python
class SCHRLevelsRegressor:
    """Регрессор для прогнозирования уровней"""
    
    def __init__(self):
        self.models = {
            'xgboost': XGBRegressor(),
            'lightgbm': LGBMRegressor(),
            'catboost': CatBoostRegressor(),
            'neural_network': MLPRegressor()
        }
        self.ensemble = VotingRegressor(
            estimators=list(self.models.items())
        )
    
    def train(self, X, y):
        """Обучение регрессора"""
        self.ensemble.fit(X, y)
        return self.ensemble
    
    def predict(self, X):
        """Предсказание уровней"""
        return self.ensemble.predict(X)
```

### 3. Deep Learning модель

**Теория:** Deep Learning модели представляют собой наиболее сложные и мощные алгоритмы машинного обучения, которые могут выявлять сложные нелинейные зависимости в данных SCHR Levels. Это критически важно для достижения максимальной точности.

**Почему Deep Learning модели важны:**
- **Сложные зависимости:** Могут выявлять сложные нелинейные зависимости
- **Высокая точность:** Обеспечивают максимальную точность предсказаний
- **Адаптивность:** Могут адаптироваться к сложным рыночным условиям
- **Масштабируемость:** Могут обрабатывать большие объемы данных

**Плюсы:**
- Высокая точность
- Выявление сложных зависимостей
- Адаптивность к сложным условиям
- Масштабируемость

**Минусы:**
- Сложность обучения
- Высокие требования к данным
- Потенциальное переобучение
- Сложность интерпретации

```python
class SCHRLevelsDeepModel:
    """Deep Learning модель для SCHR Levels"""
    
    def __init__(self, input_dim, output_dim):
        self.model = self._build_model(input_dim, output_dim)
        self.scaler = StandardScaler()
    
    def _build_model(self, input_dim, output_dim):
        """Построение нейронной сети"""
        model = Sequential([
            Dense(512, activation='relu', input_dim=input_dim),
            Dropout(0.3),
            Dense(256, activation='relu'),
            Dropout(0.3),
            Dense(128, activation='relu'),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(output_dim, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, X, y):
        """Обучение модели"""
        # Нормализация данных
        X_scaled = self.scaler.fit_transform(X)
        
        # One-hot encoding для y
        y_encoded = to_categorical(y)
        
        # Обучение
        history = self.model.fit(
            X_scaled, y_encoded,
            epochs=100,
            batch_size=32,
            validation_split=0.2,
            callbacks=[EarlyStopping(patience=10)]
        )
        
        return history
```

## Бэктестинг SCHR Levels модели

**Теория:** Бэктестинг SCHR Levels модели является критически важным этапом для валидации эффективности торговой стратегии на основе уровней. Это позволяет оценить производительность модели на исторических данных перед реальным использованием.

**Почему бэктестинг критичен:**
- **Валидация стратегии:** Позволяет проверить эффективность стратегии
- **Оценка рисков:** Помогает оценить потенциальные риски
- **Оптимизация параметров:** Позволяет оптимизировать параметры стратегии
- **Уверенность:** Повышает уверенность в стратегии

### 1. Стратегия бэктестинга

**Теория:** Стратегия бэктестинга определяет методологию тестирования SCHR Levels модели на исторических данных. Правильная стратегия критически важна для получения достоверных результатов.

**Почему стратегия бэктестинга важна:**
- **Достоверность результатов:** Обеспечивает достоверность результатов
- **Избежание переобучения:** Помогает избежать переобучения
- **Реалистичность:** Обеспечивает реалистичность тестирования
- **Валидация:** Позволяет валидировать стратегию

**Плюсы:**
- Достоверность результатов
- Избежание переобучения
- Реалистичность тестирования
- Валидация стратегии

**Минусы:**
- Сложность настройки
- Потенциальные проблемы с данными
- Время на тестирование

```python
class SCHRLevelsBacktester:
    """Бэктестер для SCHR Levels модели"""
    
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.results = {}
    
    def backtest(self, start_date, end_date):
        """Бэктестинг стратегии"""
        # Фильтрация данных по датам
        mask = (self.data.index >= start_date) & (self.data.index <= end_date)
        test_data = self.data[mask]
        
        # Предсказания модели
        predictions = self.model.predict(test_data)
        
        # Расчет доходности
        returns = self._calculate_returns(test_data, predictions)
        
        # Метрики производительности
        metrics = self._calculate_metrics(returns)
        
        return {
            'returns': returns,
            'metrics': metrics,
            'predictions': predictions
        }
    
    def _calculate_returns(self, data, predictions):
        """Расчет доходности"""
        returns = []
        position = 0
        
        for i, (date, row) in enumerate(data.iterrows()):
            if i == 0:
                continue
            
            # Сигнал модели
            signal = predictions[i]
            
            # Логика торговли на основе уровней
            if signal == 2 and position <= 0:  # Пробой вверх
                position = 1
            elif signal == 0 and position >= 0:  # Пробой вниз
                position = -1
            elif signal == 1:  # Без пробоя
                position = 0
            
            # Расчет доходности
            if position != 0:
                current_return = (row['Close'] - data.iloc[i-1]['Close']) / data.iloc[i-1]['Close']
                returns.append(current_return * position)
            else:
                returns.append(0)
        
        return returns
```

### 2. Метрики производительности

**Теория:** Метрики производительности являются критически важными для оценки эффективности SCHR Levels модели. Они обеспечивают количественную оценку различных аспектов производительности торговой стратегии на основе уровней.

**Почему метрики производительности важны:**
- **Количественная оценка:** Обеспечивают количественную оценку производительности
- **Сравнение стратегий:** Позволяют сравнивать различные стратегии
- **Оптимизация:** Помогают в оптимизации параметров
- **Управление рисками:** Критически важны для управления рисками

**Плюсы:**
- Количественная оценка
- Возможность сравнения
- Помощь в оптимизации
- Критически важно для управления рисками

**Минусы:**
- Сложность интерпретации
- Потенциальные проблемы с данными
- Необходимость понимания метрик

```python
def calculate_schr_performance_metrics(returns):
    """Расчет метрик производительности для SCHR Levels"""
    returns = np.array(returns)
    
    # Базовая статистика
    total_return = np.sum(returns)
    annualized_return = total_return * 252
    
    # Волатильность
    volatility = np.std(returns) * np.sqrt(252)
    
    # Sharpe Ratio
    risk_free_rate = 0.02
    sharpe_ratio = (annualized_return - risk_free_rate) / volatility
    
    # Максимальная просадка
    cumulative_returns = np.cumsum(returns)
    running_max = np.maximum.accumulate(cumulative_returns)
    drawdown = cumulative_returns - running_max
    max_drawdown = np.min(drawdown)
    
    # Win Rate
    win_rate = np.sum(returns > 0) / len(returns)
    
    # Profit Factor
    gross_profit = np.sum(returns[returns > 0])
    gross_loss = abs(np.sum(returns[returns < 0]))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf
    
    # Специфичные метрики для уровней
    level_hit_rate = self._calculate_level_hit_rate(returns)
    breakout_accuracy = self._calculate_breakout_accuracy(returns)
    
    return {
        'total_return': total_return,
        'annualized_return': annualized_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'level_hit_rate': level_hit_rate,
        'breakout_accuracy': breakout_accuracy
    }
```

## Оптимизация параметров SCHR Levels

**Теория:** Оптимизация параметров SCHR Levels является критически важным этапом для достижения максимальной эффективности торговой стратегии на основе уровней. Правильно оптимизированные параметры могут значительно повысить производительность системы.

**Почему оптимизация параметров критична:**
- **Максимизация производительности:** Позволяет достичь максимальной производительности
- **Адаптация к рынку:** Помогает адаптироваться к различным рыночным условиям
- **Снижение рисков:** Может снизить риски стратегии
- **Повышение прибыльности:** Может значительно повысить прибыльность

### 1. Генетический алгоритм

**Теория:** Генетический алгоритм представляет собой эволюционный метод оптимизации, который имитирует процесс естественного отбора для поиска оптимальных параметров SCHR Levels. Это особенно эффективно для сложных многомерных задач оптимизации.

**Почему генетический алгоритм важен:**
- **Глобальная оптимизация:** Может найти глобальный оптимум
- **Робастность:** Устойчив к локальным минимумам
- **Гибкость:** Может работать с различными типами параметров
- **Эффективность:** Эффективен для сложных задач

**Плюсы:**
- Глобальная оптимизация
- Робастность
- Гибкость
- Эффективность

**Минусы:**
- Сложность настройки
- Время выполнения
- Потенциальная нестабильность

```python
class SCHRLevelsOptimizer:
    """Оптимизатор параметров SCHR Levels"""
    
    def __init__(self, data):
        self.data = data
        self.best_params = None
        self.best_score = -np.inf
    
    def optimize_genetic(self, n_generations=50, population_size=100):
        """Оптимизация с помощью генетического алгоритма"""
        # Инициализация популяции
        population = self._initialize_population(population_size)
        
        for generation in range(n_generations):
            # Оценка популяции
            scores = self._evaluate_population(population)
            
            # Отбор лучших особей
            elite = self._select_elite(population, scores, top_k=10)
            
            # Скрещивание и мутация
            new_population = self._crossover_and_mutate(elite, population_size)
            
            # Обновление популяции
            population = new_population
            
            # Сохранение лучшего результата
            best_idx = np.argmax(scores)
            if scores[best_idx] > self.best_score:
                self.best_score = scores[best_idx]
                self.best_params = population[best_idx]
            
            print(f"Generation {generation}: Best score = {self.best_score:.4f}")
        
        return self.best_params, self.best_score
    
    def _initialize_population(self, size):
        """Инициализация популяции"""
        population = []
        
        for _ in range(size):
            params = {
                'pressure_threshold': np.random.uniform(0.3, 0.9),
                'level_strength': np.random.uniform(0.5, 0.95),
                'prediction_horizon': np.random.randint(5, 50),
                'volatility_factor': np.random.uniform(1.0, 3.0),
                'trend_weight': np.random.uniform(0.3, 0.8)
            }
            population.append(params)
        
        return population
```

### 2. Bayesian Optimization

**Теория:** Bayesian Optimization представляет собой интеллектуальный метод оптимизации, который использует байесовскую статистику для эффективного поиска оптимальных параметров SCHR Levels. Это особенно эффективно для дорогих в вычислении функций.

**Почему Bayesian Optimization важен:**
- **Эффективность:** Очень эффективен для дорогих функций
- **Интеллектуальный поиск:** Использует информацию о предыдущих оценках
- **Быстрая сходимость:** Быстро сходится к оптимуму
- **Учет неопределенности:** Учитывает неопределенность в оценках

**Плюсы:**
- Высокая эффективность
- Интеллектуальный поиск
- Быстрая сходимость
- Учет неопределенности

**Минусы:**
- Сложность реализации
- Требования к данным
- Потенциальные проблемы с масштабированием

```python
from skopt import gp_minimize
from skopt.space import Real, Integer

class SCHRLevelsBayesianOptimizer:
    """Bayesian оптимизация параметров SCHR Levels"""
    
    def __init__(self, data):
        self.data = data
        self.space = [
            Real(0.3, 0.9, name='pressure_threshold'),
            Real(0.5, 0.95, name='level_strength'),
            Integer(5, 50, name='prediction_horizon'),
            Real(1.0, 3.0, name='volatility_factor'),
            Real(0.3, 0.8, name='trend_weight')
        ]
    
    def optimize(self, n_calls=100):
        """Bayesian оптимизация"""
        result = gp_minimize(
            func=self._objective_function,
            dimensions=self.space,
            n_calls=n_calls,
            random_state=42
        )
        
        return result.x, -result.fun
    
    def _objective_function(self, params):
        """Целевая функция для оптимизации"""
        pressure_threshold, level_strength, prediction_horizon, volatility_factor, trend_weight = params
        
        # Расчет SCHR Levels с данными параметрами
        schr_data = self._calculate_schr_levels(pressure_threshold, level_strength, 
                                               prediction_horizon, volatility_factor, trend_weight)
        
        # Расчет производительности
        performance = self._calculate_performance(schr_data)
        
        # Возвращаем отрицательное значение для минимизации
        return -performance
```

## Продакшн деплой SCHR Levels модели

**Теория:** Продакшн деплой SCHR Levels модели является финальным этапом создания торговой системы на основе уровней, который обеспечивает развертывание модели в реальной торговой среде. Это критически важно для практического применения системы.

**Почему продакшн деплой критичен:**
- **Практическое применение:** Обеспечивает практическое применение системы
- **Автоматизация:** Автоматизирует торговые процессы
- **Масштабируемость:** Позволяет масштабировать систему
- **Мониторинг:** Обеспечивает мониторинг производительности

### 1. API для SCHR Levels модели

**Теория:** API для SCHR Levels модели обеспечивает программный интерфейс для взаимодействия с моделью, что критически важно для интеграции с торговыми системами и автоматизации процессов.

**Почему API важен:**
- **Интеграция:** Обеспечивает интеграцию с торговыми системами
- **Автоматизация:** Позволяет автоматизировать процессы
- **Масштабируемость:** Обеспечивает масштабируемость системы
- **Гибкость:** Обеспечивает гибкость в использовании

**Плюсы:**
- Интеграция с системами
- Автоматизация процессов
- Масштабируемость
- Гибкость использования

**Минусы:**
- Сложность разработки
- Требования к безопасности
- Необходимость мониторинга

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI(title="SCHR Levels ML Model API")

class SCHRPredictionRequest(BaseModel):
    predicted_high: float
    predicted_low: float
    pressure: float
    pressure_vector: float
    additional_features: dict = {}

class SCHRPredictionResponse(BaseModel):
    prediction: int
    probability: float
    confidence: str
    level_strength: float

@app.post("/predict", response_model=SCHRPredictionResponse)
async def predict(request: SCHRPredictionRequest):
    """Предсказание на основе SCHR Levels"""
    try:
        # Загрузка модели
        model = joblib.load('models/schr_levels_model.pkl')
        
        # Подготовка данных
        features = np.array([
            request.predicted_high,
            request.predicted_low,
            request.pressure,
            request.pressure_vector
        ])
        
        # Предсказание
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0].max()
        
        # Определение уверенности
        if probability > 0.8:
            confidence = "high"
        elif probability > 0.6:
            confidence = "medium"
        else:
            confidence = "low"
        
        # Расчет силы уровня
        level_strength = abs(request.predicted_high - request.predicted_low) / request.predicted_high
        
        return SCHRPredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            confidence=confidence,
            level_strength=float(level_strength)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2. Docker контейнер

**Теория:** Docker контейнеризация обеспечивает изоляцию, портабельность и масштабируемость SCHR Levels модели в продакшн среде. Это критически важно для обеспечения стабильности и простоты развертывания.

**Почему Docker контейнер важен:**
- **Изоляция:** Обеспечивает изоляцию модели
- **Портабельность:** Позволяет легко переносить модель
- **Масштабируемость:** Упрощает масштабирование
- **Управление:** Упрощает управление зависимостями

**Плюсы:**
- Изоляция модели
- Портабельность
- Масштабируемость
- Упрощение управления

**Минусы:**
- Дополнительная сложность
- Потенциальные проблемы с производительностью
- Необходимость управления контейнерами

```dockerfile
# Dockerfile для SCHR Levels модели
FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование модели и кода
COPY models/ ./models/
COPY src/ ./src/
COPY main.py .

# Экспорт порта
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Мониторинг производительности

**Теория:** Мониторинг производительности SCHR Levels модели является критически важным для обеспечения стабильности и эффективности торговой системы в продакшн среде. Это позволяет быстро выявлять и устранять проблемы.

**Почему мониторинг производительности важен:**
- **Стабильность:** Обеспечивает стабильность системы
- **Быстрое выявление проблем:** Позволяет быстро выявлять проблемы
- **Оптимизация:** Помогает в оптимизации производительности
- **Управление рисками:** Критически важно для управления рисками

**Плюсы:**
- Обеспечение стабильности
- Быстрое выявление проблем
- Помощь в оптимизации
- Критически важно для управления рисками

**Минусы:**
- Сложность настройки
- Необходимость постоянного внимания
- Потенциальные ложные срабатывания

```python
class SCHRLevelsMonitor:
    """Мониторинг SCHR Levels модели"""
    
    def __init__(self):
        self.performance_history = []
        self.alert_thresholds = {
            'accuracy': 0.7,
            'level_hit_rate': 0.6,
            'breakout_accuracy': 0.8,
            'latency': 1.0
        }
    
    def monitor_prediction(self, prediction, actual, latency, level_data):
        """Мониторинг предсказания"""
        # Расчет точности
        accuracy = 1 if prediction == actual else 0
        
        # Расчет метрик уровней
        level_hit_rate = self._calculate_level_hit_rate(level_data)
        breakout_accuracy = self._calculate_breakout_accuracy(level_data)
        
        # Сохранение метрик
        self.performance_history.append({
            'timestamp': datetime.now(),
            'accuracy': accuracy,
            'level_hit_rate': level_hit_rate,
            'breakout_accuracy': breakout_accuracy,
            'latency': latency,
            'prediction': prediction,
            'actual': actual
        })
        
        # Проверка алертов
        self._check_alerts()
    
    def _check_alerts(self):
        """Проверка алертов"""
        if len(self.performance_history) < 10:
            return
        
        recent_performance = self.performance_history[-10:]
        
        # Проверка точности
        avg_accuracy = np.mean([p['accuracy'] for p in recent_performance])
        if avg_accuracy < self.alert_thresholds['accuracy']:
            self._send_alert("Low accuracy detected")
        
        # Проверка точности уровней
        avg_level_hit_rate = np.mean([p['level_hit_rate'] for p in recent_performance])
        if avg_level_hit_rate < self.alert_thresholds['level_hit_rate']:
            self._send_alert("Low level hit rate detected")
        
        # Проверка точности пробоев
        avg_breakout_accuracy = np.mean([p['breakout_accuracy'] for p in recent_performance])
        if avg_breakout_accuracy < self.alert_thresholds['breakout_accuracy']:
            self._send_alert("Low breakout accuracy detected")
```

## Следующие шаги

После анализа SCHR Levels переходите к:
- **[13_schr_short3_analysis.md](13_schr_short3_analysis.md)** - Анализ SCHR SHORT3
- **[14_advanced_practices.md](14_advanced_practices.md)** - Продвинутые практики

## Ключевые выводы

**Теория:** Ключевые выводы суммируют наиболее важные аспекты анализа SCHR Levels, которые критически важны для создания прибыльной и робастной торговой системы на основе уровней.

1. **SCHR Levels - мощный индикатор для анализа уровней поддержки и сопротивления**
   - **Теория:** SCHR Levels представляет собой революционный подход к анализу уровней поддержки и сопротивления
   - **Почему важно:** Обеспечивает высокую точность анализа уровней
   - **Плюсы:** Высокая точность, учет давления, предсказание будущего, адаптивность
   - **Минусы:** Сложность настройки, высокие требования к ресурсам

2. **Давление на уровни - ключевой фактор для предсказания пробоев**
   - **Теория:** Анализ давления на уровни критически важен для предсказания пробоев
   - **Почему важно:** Позволяет предсказывать пробои уровней с высокой точностью
   - **Плюсы:** Предсказание пробоев, анализ рыночного давления, улучшение управления рисками
   - **Минусы:** Сложность измерения, потенциальная нестабильность

3. **Мультитаймфреймовый анализ - разные параметры для разных таймфреймов**
   - **Теория:** Каждый таймфрейм требует специфических параметров для максимальной эффективности
   - **Почему важно:** Обеспечивает оптимальную производительность на всех временных горизонтах
   - **Плюсы:** Оптимизация производительности, снижение рисков, повышение точности
   - **Минусы:** Сложность настройки, необходимость понимания каждого таймфрейма

4. **Высокая точность - возможность достижения 95%+ точности**
   - **Теория:** Правильно настроенная SCHR Levels модель может достигать очень высокой точности
   - **Почему важно:** Высокая точность критична для прибыльной торговли
   - **Плюсы:** Высокая прибыльность, снижение рисков, уверенность в стратегии
   - **Минусы:** Высокие требования к настройке, потенциальное переобучение

5. **Продакшн готовность - полная интеграция с продакшн системами**
   - **Теория:** SCHR Levels модель может быть полностью интегрирована в продакшн системы
   - **Почему важно:** Обеспечивает практическое применение системы
   - **Плюсы:** Автоматизация, масштабируемость, мониторинг
   - **Минусы:** Сложность разработки, требования к безопасности

---

**Важно:** SCHR Levels требует тщательного анализа давления на уровни и адаптации параметров для каждого актива и таймфрейма.
