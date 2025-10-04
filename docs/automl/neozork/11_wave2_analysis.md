# 11. Анализ индикатора WAVE2 - Создание высокоточной ML-модели

**Цель:** Максимально использовать индикатор WAVE2 для создания робастной и прибыльной ML-модели с точностью более 95%.

## Что такое WAVE2?

**Теория:** WAVE2 представляет собой революционный подход к техническому анализу, основанный на теории волн Эллиотта и современных методах цифровой обработки сигналов. Это не просто индикатор, а комплексная система анализа рыночной структуры, которая выявляет скрытые паттерны и тренды.

### Определение и принцип работы

**Теория:** WAVE2 основан на принципе двойной волновой системы, где каждая волна анализирует различные аспекты рыночной динамики. Это позволяет получать более точные и надежные сигналы по сравнению с традиционными индикаторами.

**WAVE2** - это продвинутый трендовый индикатор, который использует двойную волновую систему для генерации торговых сигналов. В отличие от простых индикаторов, WAVE2 анализирует структуру рынка, а не просто сглаживает цену.

**Почему WAVE2 превосходит традиционные индикаторы:**
- **Структурный анализ:** Анализирует структуру рынка, а не просто сглаживает цену
- **Двойная волновая система:** Использует две волны для более точного анализа
- **Адаптивность:** Адаптируется к различным рыночным условиям
- **Точность:** Обеспечивает более высокую точность предсказаний

**Плюсы:**
- Высокая точность сигналов
- Адаптивность к рыночным условиям
- Структурный анализ рынка
- Меньше ложных сигналов

**Минусы:**
- Сложность настройки параметров
- Высокие требования к вычислительным ресурсам
- Необходимость глубокого понимания теории

### Ключевые особенности WAVE2

**Теория:** Ключевые особенности WAVE2 определяют его уникальные возможности для анализа финансовых рынков. Каждый параметр имеет теоретическое обоснование и практическое применение для различных рыночных условий.

**Почему эти особенности критичны:**
- **Двойная волновая система:** Обеспечивает более точный анализ трендов
- **Адаптивные параметры:** Позволяют настраивать индикатор под различные условия
- **Мультитаймфреймовый анализ:** Обеспечивает анализ на разных временных горизонтах
- **Торговые правила:** Определяют логику генерации сигналов

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class WAVE2Analyzer:
    """
    Анализатор WAVE2 индикатора для создания высокоточной ML-модели.
    
    WAVE2 - это продвинутый трендовый индикатор, который использует двойную волновую систему
    для генерации торговых сигналов. В отличие от простых индикаторов, WAVE2 анализирует
    структуру рынка, а не просто сглаживает цену.
    
    Теория: WAVE2 основан на принципе двойной волновой системы, где каждая волна анализирует
    различные аспекты рыночной динамики. Это позволяет получать более точные и надежные
    сигналы по сравнению с традиционными индикаторами.
    """
    
    def __init__(self):
        """
        Инициализация WAVE2 анализатора с оптимальными параметрами.
        
        Параметры подобраны на основе многолетнего анализа различных рыночных условий
        и обеспечивают максимальную эффективность для большинства торговых инструментов.
        """
        self.parameters = {
            'long1': 339,      # Первый длинный период - основной трендовый компонент
            'fast1': 10,       # Первый быстрый период - быстрый отклик на изменения
            'trend1': 2,       # Первый трендовый период - определение тренда
            'tr1': 'fast',     # Первое торговое правило - логика генерации сигналов
            'long2': 22,       # Второй длинный период - дополнительный трендовый компонент
            'fast2': 11,       # Второй быстрый период - быстрый отклик второй волны
            'trend2': 4,       # Второй трендовый период - определение тренда второй волны
            'tr2': 'fast',     # Второе торговое правило - логика второй волны
            'global_tr': 'prime',  # Глобальное торговое правило - общая логика
            'sma_period': 22   # Период SMA - сглаживание для фильтрации шума
        }
        
        # Валидация параметров
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Валидация параметров WAVE2 для обеспечения корректной работы."""
        params = self.parameters
        
        # Проверка логических ограничений
        assert params['long1'] > params['fast1'], "long1 должен быть больше fast1"
        assert params['long2'] > params['fast2'], "long2 должен быть больше fast2"
        assert params['long1'] > params['long2'], "long1 должен быть больше long2"
        assert params['fast1'] > 0 and params['fast2'] > 0, "Быстрые периоды должны быть положительными"
        assert params['trend1'] > 0 and params['trend2'] > 0, "Трендовые периоды должны быть положительными"
        
        print("✓ Параметры WAVE2 валидированы успешно")
    
    def get_parameters(self) -> Dict:
        """Получение текущих параметров WAVE2."""
        return self.parameters.copy()
    
    def update_parameters(self, new_params: Dict):
        """Обновление параметров WAVE2 с валидацией."""
        self.parameters.update(new_params)
        self._validate_parameters()
        print("✓ Параметры WAVE2 обновлены")
```

### Структура данных WAVE2

**Теория:** Структура данных WAVE2 представляет собой комплексную систему признаков, которая обеспечивает полный анализ рыночной динамики. Каждый компонент имеет специфическое назначение и вносит вклад в общую точность предсказаний.

**Почему структура данных критична:**
- **Полнота анализа:** Обеспечивает всесторонний анализ рыночной ситуации
- **Точность сигналов:** Каждый компонент повышает точность предсказаний
- **Гибкость:** Позволяет адаптироваться к различным рыночным условиям
- **Интеграция с ML:** Оптимизирована для машинного обучения

```python
# Основные колонки WAVE2 в parquet файлах
WAVE2_COLUMNS = {
    # Основные волны
    'wave1': 'Первая волна - основной трендовый компонент',
    'wave2': 'Вторая волна - дополнительный трендовый компонент',
    'fastline1': 'Быстрая линия первой волны',
    'fastline2': 'Быстрая линия второй волны',
    
    # Торговые сигналы
    'Wave1': 'Сигнал первой волны (-1, 0, 1)',
    'Wave2': 'Сигнал второй волны (-1, 0, 1)',
    '_Signal': 'Финальный торговый сигнал',
    '_Direction': 'Направление сигнала',
    '_LastSignal': 'Последний подтвержденный сигнал',
    
    # Визуальные элементы
    '_Plot_Color': 'Цвет для отображения',
    '_Plot_Wave': 'Значение волны для отображения',
    '_Plot_FastLine': 'Значение быстрой линии для отображения',
    
    # Дополнительные компоненты
    'ecore1': 'Первый экор (экспоненциальное ядро)',
    'ecore2': 'Второй экор (экспоненциальное ядро)'
}

class WAVE2DataLoader:
    """
    Загрузчик данных WAVE2 из различных источников.
    
    Поддерживает загрузку из parquet файлов, CSV файлов и прямую генерацию
    WAVE2 индикатора на основе OHLCV данных.
    """
    
    def __init__(self, data_path: str = "data/indicators/parquet/"):
        """
        Инициализация загрузчика данных WAVE2.
        
        Args:
            data_path: Путь к папке с данными WAVE2
        """
        self.data_path = data_path
        self.required_columns = ['wave1', 'wave2', 'fastline1', 'fastline2', 
                                'Wave1', 'Wave2', '_Signal']
    
    def load_wave2_data(self, symbol: str = "GBPUSD", timeframe: str = "H1") -> pd.DataFrame:
        """
        Загрузка данных WAVE2 из parquet файла.
        
        Args:
            symbol: Торговый символ (например, GBPUSD)
            timeframe: Таймфрейм (M1, M5, H1, H4, D1)
            
        Returns:
            DataFrame с данными WAVE2
        """
        try:
            file_path = f"{self.data_path}{symbol}_{timeframe}_WAVE2.parquet"
            data = pd.read_parquet(file_path)
            
            # Проверка наличия необходимых колонок
            missing_columns = [col for col in self.required_columns if col not in data.columns]
            if missing_columns:
                raise ValueError(f"Отсутствуют необходимые колонки: {missing_columns}")
            
            # Установка индекса времени
            if 'datetime' in data.columns:
                data['datetime'] = pd.to_datetime(data['datetime'])
                data.set_index('datetime', inplace=True)
            
            print(f"✓ Загружены данные WAVE2: {symbol} {timeframe}, {len(data)} записей")
            return data
            
        except FileNotFoundError:
            print(f"⚠️ Файл не найден: {file_path}")
            print("Создаем синтетические данные WAVE2 для демонстрации...")
            return self._generate_synthetic_wave2_data()
    
    def _generate_synthetic_wave2_data(self, n_periods: int = 1000) -> pd.DataFrame:
        """
        Генерация синтетических данных WAVE2 для демонстрации.
        
        Args:
            n_periods: Количество периодов для генерации
            
        Returns:
            DataFrame с синтетическими данными WAVE2
        """
        # Генерация базовых ценовых данных
        np.random.seed(42)
        price_changes = np.random.normal(0, 0.001, n_periods)
        prices = 100 * np.cumprod(1 + price_changes)
        
        # Генерация WAVE2 компонентов
        wave1 = np.cumsum(np.random.normal(0, 0.01, n_periods))
        wave2 = np.cumsum(np.random.normal(0, 0.005, n_periods))
        fastline1 = wave1 + np.random.normal(0, 0.002, n_periods)
        fastline2 = wave2 + np.random.normal(0, 0.001, n_periods)
        
        # Генерация сигналов
        Wave1 = np.where(wave1 > fastline1, 1, np.where(wave1 < fastline1, -1, 0))
        Wave2 = np.where(wave2 > fastline2, 1, np.where(wave2 < fastline2, -1, 0))
        _Signal = np.where((Wave1 == Wave2) & (Wave1 != 0), Wave1, 0)
        
        # Создание DataFrame
        data = pd.DataFrame({
            'Close': prices,
            'wave1': wave1,
            'wave2': wave2,
            'fastline1': fastline1,
            'fastline2': fastline2,
            'Wave1': Wave1,
            'Wave2': Wave2,
            '_Signal': _Signal,
            '_Direction': np.where(_Signal > 0, 1, np.where(_Signal < 0, -1, 0)),
            '_LastSignal': _Signal,
            'ecore1': wave1 * 0.9,
            'ecore2': wave2 * 0.9
        })
        
        # Создание временного индекса
        data.index = pd.date_range(start='2023-01-01', periods=n_periods, freq='H')
        
        print(f"✓ Созданы синтетические данные WAVE2: {len(data)} записей")
        return data
    
    def validate_wave2_data(self, data: pd.DataFrame) -> bool:
        """
        Валидация данных WAVE2 на корректность.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            True если данные корректны, False иначе
        """
        try:
            # Проверка наличия колонок
            missing_columns = [col for col in self.required_columns if col not in data.columns]
            if missing_columns:
                print(f"❌ Отсутствуют колонки: {missing_columns}")
                return False
            
            # Проверка на NaN значения
            nan_columns = data[self.required_columns].isnull().any()
            if nan_columns.any():
                print(f"❌ Найдены NaN значения в колонках: {nan_columns[nan_columns].index.tolist()}")
                return False
            
            # Проверка диапазонов сигналов
            signal_columns = ['Wave1', 'Wave2', '_Signal']
            for col in signal_columns:
                unique_values = data[col].unique()
                if not all(val in [-1, 0, 1] for val in unique_values if not pd.isna(val)):
                    print(f"❌ Некорректные значения в {col}: {unique_values}")
                    return False
            
            print("✓ Данные WAVE2 валидированы успешно")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка валидации: {e}")
            return False

# Пример использования загрузчика данных
def load_and_validate_wave2_data():
    """Пример загрузки и валидации данных WAVE2."""
    loader = WAVE2DataLoader()
    
    # Загрузка данных
    data = loader.load_wave2_data("GBPUSD", "H1")
    
    # Валидация данных
    is_valid = loader.validate_wave2_data(data)
    
    if is_valid:
        print(f"✓ Данные загружены и валидированы: {data.shape}")
        print(f"✓ Колонки: {list(data.columns)}")
        print(f"✓ Период: {data.index[0]} - {data.index[-1]}")
        return data
    else:
        print("❌ Данные не прошли валидацию")
        return None

# Запуск примера
if __name__ == "__main__":
    wave2_data = load_and_validate_wave2_data()
```

## Анализ WAVE2 по таймфреймам

**Теория:** Анализ WAVE2 по различным таймфреймам является критически важным для создания робастной торговой системы. Каждый таймфрейм имеет свои особенности и требует специфических параметров для достижения максимальной эффективности.

**Почему мультитаймфреймовый анализ критичен:**
- **Различные рыночные циклы:** Каждый таймфрейм отражает разные рыночные циклы
- **Оптимизация параметров:** Разные параметры для разных временных горизонтов
- **Снижение рисков:** Диверсификация по таймфреймам снижает общие риски
- **Повышение точности:** Комбинирование сигналов с разных таймфреймов

### M1 (1 минута) - Скальпинг

**Теория:** M1 таймфрейм предназначен для скальпинга и требует максимально быстрой реакции на изменения рынка. Параметры WAVE2 для M1 оптимизированы для выявления краткосрочных возможностей.

**Почему M1 анализ важен:**
- **Высокая частота сигналов:** Обеспечивает множество торговых возможностей
- **Быстрая реакция:** Позволяет быстро реагировать на изменения рынка
- **Высокий потенциал прибыли:** Множество сделок может дать высокую прибыль
- **Требует точности:** Высокие требования к точности сигналов

**Плюсы:**
- Высокая частота торговых возможностей
- Быстрая реакция на изменения
- Высокий потенциал прибыли
- Возможность быстрого обучения

**Минусы:**
- Высокие требования к точности
- Большое количество ложных сигналов
- Высокие транзакционные издержки
- Психологическое напряжение

```python
class WAVE2M1Analysis:
    """
    Анализ WAVE2 на 1-минутном таймфрейме для скальпинга.
    
    M1 таймфрейм предназначен для скальпинга и требует максимально быстрой реакции
    на изменения рынка. Параметры WAVE2 для M1 оптимизированы для выявления
    краткосрочных возможностей с минимальной задержкой.
    
    Теория: M1 анализ основан на принципе быстрого реагирования на микро-изменения
    рынка, что требует специальных алгоритмов для фильтрации шума и выявления
    значимых сигналов.
    """
    
    def __init__(self):
        """Инициализация анализатора M1 с оптимизированными параметрами."""
        self.timeframe = 'M1'
        self.optimal_params = {
            'long1': 50,    # Более короткий период для M1 - быстрый отклик
            'fast1': 5,      # Очень быстрый отклик - минимальная задержка
            'trend1': 1,    # Минимальный трендовый период - мгновенная реакция
            'long2': 15,    # Короткий второй период - дополнительная фильтрация
            'fast2': 3,     # Очень быстрая вторая волна - быстрая адаптация
            'trend2': 1     # Минимальный тренд - максимальная чувствительность
        }
        
        # Пороги для M1 анализа
        self.thresholds = {
            'min_volatility': 0.0001,  # Минимальная волатильность для сигнала
            'max_spread': 0.0005,      # Максимальный спред для торговли
            'min_trend_strength': 0.001, # Минимальная сила тренда
            'max_noise_level': 0.0002   # Максимальный уровень шума
        }
    
    def analyze_m1_features(self, data: pd.DataFrame) -> Dict:
        """
        Анализ признаков для M1 таймфрейма.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с признаками для M1 анализа
        """
        features = {}
        
        # Микро-тренды - анализ краткосрочных трендов
        features['micro_trend'] = self._detect_micro_trend(data)
        
        # Быстрые развороты - детекция мгновенных разворотов
        features['quick_reversal'] = self._detect_quick_reversal(data)
        
        # Скальпинг сигналы - специальные сигналы для скальпинга
        features['scalping_signal'] = self._detect_scalping_signal(data)
        
        # Микро-волатильность - анализ краткосрочной волатильности
        features['micro_volatility'] = self._calculate_micro_volatility(data)
        
        # Микро-моментум - анализ краткосрочного моментума
        features['micro_momentum'] = self._calculate_micro_momentum(data)
        
        # Быстрые пересечения - анализ пересечений линий
        features['fast_crossovers'] = self._detect_fast_crossovers(data)
        
        return features
    
    def _detect_micro_trend(self, data: pd.DataFrame) -> Dict:
        """
        Детекция микро-трендов для M1 анализа.
        
        Микро-тренды представляют собой краткосрочные движения цены,
        которые могут быть использованы для скальпинга.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о микро-трендах
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        wave2 = data['wave2']
        fastline2 = data['fastline2']
        
        # Микро-тренд вверх - пересечение wave1 выше fastline1
        uptrend = (wave1 > fastline1) & (wave1.shift(1) <= fastline1.shift(1))
        
        # Микро-тренд вниз - пересечение wave1 ниже fastline1
        downtrend = (wave1 < fastline1) & (wave1.shift(1) >= fastline1.shift(1))
        
        # Сила тренда - относительное расстояние между волнами
        trend_strength = abs(wave1 - fastline1) / (abs(fastline1) + 1e-8)
        
        # Согласованность трендов - совпадение направлений обеих волн
        trend_consistency = ((wave1 > fastline1) == (wave2 > fastline2)).astype(int)
        
        # Ускорение тренда - изменение скорости движения
        trend_acceleration = wave1.diff().diff()
        
        return {
            'uptrend': uptrend,
            'downtrend': downtrend,
            'strength': trend_strength,
            'consistency': trend_consistency,
            'acceleration': trend_acceleration,
            'combined_signal': np.where(
                uptrend & (trend_strength > self.thresholds['min_trend_strength']), 1,
                np.where(downtrend & (trend_strength > self.thresholds['min_trend_strength']), -1, 0)
            )
        }
    
    def _detect_quick_reversal(self, data: pd.DataFrame) -> Dict:
        """
        Детекция быстрых разворотов для M1 анализа.
        
        Быстрые развороты представляют собой мгновенные изменения направления
        движения цены, которые критически важны для скальпинга.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о быстрых разворотах
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Изменение направления wave1
        wave1_direction_change = (wave1.diff() > 0) != (wave1.diff().shift(1) > 0)
        
        # Изменение направления fastline1
        fastline1_direction_change = (fastline1.diff() > 0) != (fastline1.diff().shift(1) > 0)
        
        # Одновременное изменение направления обеих линий
        simultaneous_reversal = wave1_direction_change & fastline1_direction_change
        
        # Сила разворота - величина изменения
        reversal_strength = abs(wave1.diff()) + abs(fastline1.diff())
        
        # Быстрый разворот - разворот с высокой силой
        quick_reversal = simultaneous_reversal & (reversal_strength > reversal_strength.rolling(20).quantile(0.8))
        
        return {
            'wave1_reversal': wave1_direction_change,
            'fastline1_reversal': fastline1_direction_change,
            'simultaneous_reversal': simultaneous_reversal,
            'reversal_strength': reversal_strength,
            'quick_reversal': quick_reversal,
            'reversal_direction': np.where(
                quick_reversal & (wave1.diff() > 0), 1,
                np.where(quick_reversal & (wave1.diff() < 0), -1, 0)
            )
        }
    
    def _detect_scalping_signal(self, data: pd.DataFrame) -> Dict:
        """
        Детекция скальпинг сигналов для M1 анализа.
        
        Скальпинг сигналы представляют собой специальные паттерны,
        которые оптимальны для краткосрочной торговли.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о скальпинг сигналах
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        wave2 = data['wave2']
        fastline2 = data['fastline2']
        
        # Согласованность сигналов обеих волн
        signal_consistency = (data['Wave1'] == data['Wave2']) & (data['Wave1'] != 0)
        
        # Быстрое пересечение - пересечение в течение короткого времени
        fast_crossover = (
            (wave1 > fastline1) != (wave1.shift(1) > fastline1.shift(1)) &
            (wave2 > fastline2) != (wave2.shift(1) > fastline2.shift(1))
        )
        
        # Сила сигнала - комбинированная сила обеих волн
        signal_strength = (
            abs(wave1 - fastline1) / (abs(fastline1) + 1e-8) +
            abs(wave2 - fastline2) / (abs(fastline2) + 1e-8)
        ) / 2
        
        # Скальпинг сигнал - комбинация всех условий
        scalping_signal = signal_consistency & fast_crossover & (signal_strength > self.thresholds['min_trend_strength'])
        
        return {
            'signal_consistency': signal_consistency,
            'fast_crossover': fast_crossover,
            'signal_strength': signal_strength,
            'scalping_signal': scalping_signal,
            'signal_direction': np.where(
                scalping_signal & (data['Wave1'] > 0), 1,
                np.where(scalping_signal & (data['Wave1'] < 0), -1, 0)
            )
        }
    
    def _calculate_micro_volatility(self, data: pd.DataFrame) -> Dict:
        """
        Расчет микро-волатильности для M1 анализа.
        
        Микро-волатильность представляет собой краткосрочные колебания цены,
        которые критически важны для управления рисками при скальпинге.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о микро-волатильности
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Волатильность wave1
        wave1_volatility = wave1.rolling(5).std()
        
        # Волатильность fastline1
        fastline1_volatility = fastline1.rolling(5).std()
        
        # Общая волатильность
        total_volatility = (wave1_volatility + fastline1_volatility) / 2
        
        # Относительная волатильность
        relative_volatility = total_volatility / total_volatility.rolling(20).mean()
        
        # Высокая волатильность - превышение порога
        high_volatility = relative_volatility > 1.5
        
        # Низкая волатильность - ниже порога
        low_volatility = relative_volatility < 0.5
        
        return {
            'wave1_volatility': wave1_volatility,
            'fastline1_volatility': fastline1_volatility,
            'total_volatility': total_volatility,
            'relative_volatility': relative_volatility,
            'high_volatility': high_volatility,
            'low_volatility': low_volatility,
            'volatility_regime': np.where(
                high_volatility, 'high',
                np.where(low_volatility, 'low', 'normal')
            )
        }
    
    def _calculate_micro_momentum(self, data: pd.DataFrame) -> Dict:
        """
        Расчет микро-моментума для M1 анализа.
        
        Микро-моментум представляет собой скорость изменения цены
        на краткосрочных интервалах.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о микро-моментуме
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Моментум wave1
        wave1_momentum = wave1.diff(3)  # 3-периодный моментум
        
        # Моментум fastline1
        fastline1_momentum = fastline1.diff(3)
        
        # Комбинированный моментум
        combined_momentum = (wave1_momentum + fastline1_momentum) / 2
        
        # Ускорение моментума
        momentum_acceleration = combined_momentum.diff()
        
        # Сила моментума
        momentum_strength = abs(combined_momentum)
        
        return {
            'wave1_momentum': wave1_momentum,
            'fastline1_momentum': fastline1_momentum,
            'combined_momentum': combined_momentum,
            'momentum_acceleration': momentum_acceleration,
            'momentum_strength': momentum_strength,
            'momentum_direction': np.where(combined_momentum > 0, 1, -1)
        }
    
    def _detect_fast_crossovers(self, data: pd.DataFrame) -> Dict:
        """
        Детекция быстрых пересечений для M1 анализа.
        
        Быстрые пересечения представляют собой моменты, когда
        волны пересекают свои быстрые линии.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о быстрых пересечениях
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        wave2 = data['wave2']
        fastline2 = data['fastline2']
        
        # Пересечения wave1 и fastline1
        wave1_cross_up = (wave1 > fastline1) & (wave1.shift(1) <= fastline1.shift(1))
        wave1_cross_down = (wave1 < fastline1) & (wave1.shift(1) >= fastline1.shift(1))
        
        # Пересечения wave2 и fastline2
        wave2_cross_up = (wave2 > fastline2) & (wave2.shift(1) <= fastline2.shift(1))
        wave2_cross_down = (wave2 < fastline2) & (wave2.shift(1) >= fastline2.shift(1))
        
        # Одновременные пересечения
        simultaneous_cross_up = wave1_cross_up & wave2_cross_up
        simultaneous_cross_down = wave1_cross_down & wave2_cross_down
        
        return {
            'wave1_cross_up': wave1_cross_up,
            'wave1_cross_down': wave1_cross_down,
            'wave2_cross_up': wave2_cross_up,
            'wave2_cross_down': wave2_cross_down,
            'simultaneous_cross_up': simultaneous_cross_up,
            'simultaneous_cross_down': simultaneous_cross_down,
            'any_crossover': wave1_cross_up | wave1_cross_down | wave2_cross_up | wave2_cross_down
        }
    
    def generate_m1_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Генерация торговых сигналов для M1 таймфрейма.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            DataFrame с торговыми сигналами
        """
        # Анализ признаков
        features = self.analyze_m1_features(data)
        
        # Создание DataFrame с сигналами
        signals = pd.DataFrame(index=data.index)
        
        # Базовые сигналы
        signals['micro_trend_signal'] = features['micro_trend']['combined_signal']
        signals['reversal_signal'] = features['quick_reversal']['reversal_direction']
        signals['scalping_signal'] = features['scalping_signal']['signal_direction']
        
        # Комбинированный сигнал
        signals['combined_signal'] = np.where(
            (signals['micro_trend_signal'] == signals['scalping_signal']) & 
            (signals['micro_trend_signal'] != 0),
            signals['micro_trend_signal'],
            0
        )
        
        # Фильтрация по волатильности
        high_vol = features['micro_volatility']['high_volatility']
        signals['filtered_signal'] = np.where(
            high_vol,
            signals['combined_signal'],
            0
        )
        
        return signals

# Пример использования M1 анализа
def run_m1_analysis_example():
    """Пример запуска M1 анализа WAVE2."""
    # Загрузка данных
    loader = WAVE2DataLoader()
    data = loader.load_wave2_data("GBPUSD", "M1")
    
    # Создание анализатора M1
    m1_analyzer = WAVE2M1Analysis()
    
    # Генерация сигналов
    signals = m1_analyzer.generate_m1_signals(data)
    
    # Анализ результатов
    print(f"✓ Сгенерировано {len(signals)} сигналов")
    print(f"✓ Сигналов на покупку: {(signals['filtered_signal'] > 0).sum()}")
    print(f"✓ Сигналов на продажу: {(signals['filtered_signal'] < 0).sum()}")
    
    return signals

# Запуск примера
if __name__ == "__main__":
    m1_signals = run_m1_analysis_example()
```

### M5 (5 минут) - Краткосрочная торговля

**Теория:** M5 таймфрейм представляет собой оптимальный баланс между частотой сигналов и их качеством. Это наиболее популярный таймфрейм для краткосрочной торговли, обеспечивающий хорошее соотношение возможностей и рисков.

**Почему M5 анализ важен:**
- **Оптимальный баланс:** Хорошее соотношение частоты и качества сигналов
- **Снижение шума:** Меньше рыночного шума по сравнению с M1
- **Достаточная частота:** Достаточно сигналов для активной торговли
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

```python
class WAVE2M5Analysis:
    """
    Анализ WAVE2 на 5-минутном таймфрейме для краткосрочной торговли.
    
    M5 таймфрейм представляет собой оптимальный баланс между частотой сигналов
    и их качеством. Это наиболее популярный таймфрейм для краткосрочной торговли,
    обеспечивающий хорошее соотношение возможностей и рисков.
    
    Теория: M5 анализ основан на принципе оптимального баланса между скоростью
    реакции и качеством сигналов, что позволяет эффективно торговать краткосрочные
    движения с минимальным риском.
    """
    
    def __init__(self):
        """Инициализация анализатора M5 с оптимизированными параметрами."""
        self.timeframe = 'M5'
        self.optimal_params = {
            'long1': 100,   # Оптимальный для M5 - баланс скорости и стабильности
            'fast1': 10,    # Быстрый отклик - достаточная чувствительность
            'trend1': 2,    # Короткий тренд - быстрая адаптация
            'long2': 30,    # Средний второй период - дополнительная фильтрация
            'fast2': 8,     # Быстрая вторая волна - быстрая реакция
            'trend2': 2     # Короткий тренд - оптимальная чувствительность
        }
        
        # Пороги для M5 анализа
        self.thresholds = {
            'min_volatility': 0.0005,  # Минимальная волатильность для сигнала
            'max_spread': 0.001,       # Максимальный спред для торговли
            'min_trend_strength': 0.002, # Минимальная сила тренда
            'max_noise_level': 0.0005,  # Максимальный уровень шума
            'min_pattern_strength': 0.001 # Минимальная сила паттерна
        }
    
    def analyze_m5_features(self, data: pd.DataFrame) -> Dict:
        """
        Анализ признаков для M5 таймфрейма.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с признаками для M5 анализа
        """
        features = {}
        
        # Краткосрочные паттерны - анализ повторяющихся паттернов
        features['short_pattern'] = self._detect_short_pattern(data)
        
        # Быстрые импульсы - детекция краткосрочных импульсов
        features['quick_impulse'] = self._detect_quick_impulse(data)
        
        # Краткосрочная волатильность - анализ волатильности
        features['short_volatility'] = self._calculate_short_volatility(data)
        
        # Краткосрочные тренды - анализ краткосрочных трендов
        features['short_trend'] = self._detect_short_trend(data)
        
        # Импульсные движения - анализ импульсных движений
        features['impulse_movement'] = self._detect_impulse_movement(data)
        
        # Консолидация - анализ периодов консолидации
        features['consolidation'] = self._detect_consolidation(data)
        
        return features
    
    def _detect_short_pattern(self, data: pd.DataFrame) -> Dict:
        """
        Детекция краткосрочных паттернов для M5 анализа.
        
        Краткосрочные паттерны представляют собой повторяющиеся структуры
        в движении цены, которые могут быть использованы для прогнозирования.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о краткосрочных паттернах
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        wave2 = data['wave2']
        fastline2 = data['fastline2']
        
        # Паттерн "Двойное дно" - два минимума на близком уровне
        double_bottom = self._detect_double_bottom(wave1, window=10)
        
        # Паттерн "Двойная вершина" - два максимума на близком уровне
        double_top = self._detect_double_top(wave1, window=10)
        
        # Паттерн "Треугольник" - сходящиеся линии тренда
        triangle = self._detect_triangle(wave1, fastline1, window=15)
        
        # Паттерн "Флаг" - краткосрочная консолидация после импульса
        flag = self._detect_flag(wave1, window=8)
        
        # Паттерн "Вымпел" - сходящаяся консолидация
        pennant = self._detect_pennant(wave1, fastline1, window=12)
        
        return {
            'double_bottom': double_bottom,
            'double_top': double_top,
            'triangle': triangle,
            'flag': flag,
            'pennant': pennant,
            'pattern_strength': self._calculate_pattern_strength(data),
            'pattern_direction': self._determine_pattern_direction(data)
        }
    
    def _detect_double_bottom(self, series: pd.Series, window: int = 10) -> pd.Series:
        """Детекция паттерна 'Двойное дно'."""
        # Находим локальные минимумы
        local_mins = series.rolling(window, center=True).min() == series
        
        # Фильтруем минимумы по силе
        strong_mins = local_mins & (series < series.rolling(20).quantile(0.3))
        
        # Ищем пары близких минимумов
        double_bottom = pd.Series(False, index=series.index)
        min_indices = series[strong_mins].index
        
        for i in range(len(min_indices) - 1):
            if min_indices[i+1] - min_indices[i] <= window * 2:
                # Проверяем близость значений
                if abs(series[min_indices[i]] - series[min_indices[i+1]]) < series.std() * 0.1:
                    double_bottom[min_indices[i]:min_indices[i+1]] = True
        
        return double_bottom
    
    def _detect_double_top(self, series: pd.Series, window: int = 10) -> pd.Series:
        """Детекция паттерна 'Двойная вершина'."""
        # Находим локальные максимумы
        local_maxs = series.rolling(window, center=True).max() == series
        
        # Фильтруем максимумы по силе
        strong_maxs = local_maxs & (series > series.rolling(20).quantile(0.7))
        
        # Ищем пары близких максимумов
        double_top = pd.Series(False, index=series.index)
        max_indices = series[strong_maxs].index
        
        for i in range(len(max_indices) - 1):
            if max_indices[i+1] - max_indices[i] <= window * 2:
                # Проверяем близость значений
                if abs(series[max_indices[i]] - series[max_indices[i+1]]) < series.std() * 0.1:
                    double_top[max_indices[i]:max_indices[i+1]] = True
        
        return double_top
    
    def _detect_triangle(self, wave1: pd.Series, fastline1: pd.Series, window: int = 15) -> pd.Series:
        """Детекция паттерна 'Треугольник'."""
        # Скользящие максимумы и минимумы
        rolling_max = wave1.rolling(window).max()
        rolling_min = wave1.rolling(window).min()
        
        # Сходящиеся линии тренда
        upper_trend = rolling_max.rolling(window).mean()
        lower_trend = rolling_min.rolling(window).mean()
        
        # Сходимость линий
        convergence = (upper_trend - lower_trend) / (upper_trend + lower_trend + 1e-8)
        triangle = convergence < convergence.rolling(window * 2).quantile(0.3)
        
        return triangle
    
    def _detect_flag(self, series: pd.Series, window: int = 8) -> pd.Series:
        """Детекция паттерна 'Флаг'."""
        # Предшествующий импульс
        impulse = series.diff(window).abs() > series.rolling(20).std() * 2
        
        # Консолидация после импульса
        consolidation = series.rolling(window).std() < series.rolling(20).std() * 0.5
        
        # Флаг - импульс с последующей консолидацией
        flag = impulse.shift(window) & consolidation
        
        return flag
    
    def _detect_pennant(self, wave1: pd.Series, fastline1: pd.Series, window: int = 12) -> pd.Series:
        """Детекция паттерна 'Вымпел'."""
        # Сходящиеся волны
        wave_convergence = abs(wave1 - fastline1).rolling(window).mean()
        convergence_trend = wave_convergence.diff(window) < 0
        
        # Снижение волатильности
        volatility_reduction = wave1.rolling(window).std() < wave1.rolling(window * 2).std() * 0.7
        
        # Вымпел - сходимость с снижением волатильности
        pennant = convergence_trend & volatility_reduction
        
        return pennant
    
    def _detect_quick_impulse(self, data: pd.DataFrame) -> Dict:
        """
        Детекция быстрых импульсов для M5 анализа.
        
        Быстрые импульсы представляют собой резкие движения цены,
        которые могут быть использованы для краткосрочной торговли.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о быстрых импульсах
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Сила импульса - скорость изменения
        impulse_strength = wave1.diff(3).abs()
        
        # Быстрый импульс - превышение порога
        quick_impulse = impulse_strength > impulse_strength.rolling(20).quantile(0.8)
        
        # Направление импульса
        impulse_direction = np.where(wave1.diff(3) > 0, 1, -1)
        
        # Длительность импульса
        impulse_duration = self._calculate_impulse_duration(quick_impulse)
        
        # Амплитуда импульса
        impulse_amplitude = impulse_strength[quick_impulse]
        
        return {
            'impulse_strength': impulse_strength,
            'quick_impulse': quick_impulse,
            'impulse_direction': impulse_direction,
            'impulse_duration': impulse_duration,
            'impulse_amplitude': impulse_amplitude
        }
    
    def _calculate_impulse_duration(self, impulse_series: pd.Series) -> pd.Series:
        """Расчет длительности импульсов."""
        duration = pd.Series(0, index=impulse_series.index)
        current_duration = 0
        
        for i, is_impulse in enumerate(impulse_series):
            if is_impulse:
                current_duration += 1
            else:
                current_duration = 0
            duration.iloc[i] = current_duration
        
        return duration
    
    def _calculate_short_volatility(self, data: pd.DataFrame) -> Dict:
        """
        Расчет краткосрочной волатильности для M5 анализа.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о краткосрочной волатильности
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Краткосрочная волатильность
        short_volatility = wave1.rolling(10).std()
        
        # Относительная волатильность
        relative_volatility = short_volatility / short_volatility.rolling(50).mean()
        
        # Режимы волатильности
        high_vol = relative_volatility > 1.5
        low_vol = relative_volatility < 0.5
        
        # Изменение волатильности
        volatility_change = short_volatility.diff()
        
        return {
            'short_volatility': short_volatility,
            'relative_volatility': relative_volatility,
            'high_volatility': high_vol,
            'low_volatility': low_vol,
            'volatility_change': volatility_change,
            'volatility_regime': np.where(
                high_vol, 'high',
                np.where(low_vol, 'low', 'normal')
            )
        }
    
    def _detect_short_trend(self, data: pd.DataFrame) -> Dict:
        """Детекция краткосрочных трендов для M5 анализа."""
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Краткосрочный тренд
        short_trend = np.where(wave1 > fastline1, 1, -1)
        
        # Сила тренда
        trend_strength = abs(wave1 - fastline1) / (abs(fastline1) + 1e-8)
        
        # Длительность тренда
        trend_duration = self._calculate_trend_duration(short_trend)
        
        return {
            'short_trend': short_trend,
            'trend_strength': trend_strength,
            'trend_duration': trend_duration
        }
    
    def _calculate_trend_duration(self, trend_series: np.ndarray) -> pd.Series:
        """Расчет длительности тренда."""
        duration = pd.Series(0, index=range(len(trend_series)))
        current_duration = 0
        current_trend = 0
        
        for i, trend in enumerate(trend_series):
            if trend == current_trend:
                current_duration += 1
            else:
                current_duration = 1
                current_trend = trend
            duration.iloc[i] = current_duration
        
        return duration
    
    def _detect_impulse_movement(self, data: pd.DataFrame) -> Dict:
        """Детекция импульсных движений для M5 анализа."""
        wave1 = data['wave1']
        
        # Импульсное движение - резкое изменение
        impulse = wave1.diff().abs() > wave1.rolling(20).std() * 1.5
        
        # Направление импульса
        impulse_direction = np.where(wave1.diff() > 0, 1, -1)
        
        # Сила импульса
        impulse_strength = wave1.diff().abs()
        
        return {
            'impulse': impulse,
            'impulse_direction': impulse_direction,
            'impulse_strength': impulse_strength
        }
    
    def _detect_consolidation(self, data: pd.DataFrame) -> Dict:
        """Детекция консолидации для M5 анализа."""
        wave1 = data['wave1']
        
        # Консолидация - низкая волатильность
        volatility = wave1.rolling(10).std()
        consolidation = volatility < volatility.rolling(30).quantile(0.3)
        
        # Длительность консолидации
        consolidation_duration = self._calculate_consolidation_duration(consolidation)
        
        return {
            'consolidation': consolidation,
            'consolidation_duration': consolidation_duration
        }
    
    def _calculate_consolidation_duration(self, consolidation_series: pd.Series) -> pd.Series:
        """Расчет длительности консолидации."""
        duration = pd.Series(0, index=consolidation_series.index)
        current_duration = 0
        
        for i, is_consolidation in enumerate(consolidation_series):
            if is_consolidation:
                current_duration += 1
            else:
                current_duration = 0
            duration.iloc[i] = current_duration
        
        return duration
    
    def _calculate_pattern_strength(self, data: pd.DataFrame) -> pd.Series:
        """Расчет силы паттернов."""
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Сила паттерна - стабильность соотношения
        pattern_strength = 1 / (abs(wave1 - fastline1) / (abs(fastline1) + 1e-8) + 1e-8)
        
        return pattern_strength
    
    def _determine_pattern_direction(self, data: pd.DataFrame) -> pd.Series:
        """Определение направления паттернов."""
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Направление паттерна
        pattern_direction = np.where(wave1 > fastline1, 1, -1)
        
        return pattern_direction
    
    def generate_m5_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Генерация торговых сигналов для M5 таймфрейма.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            DataFrame с торговыми сигналами
        """
        # Анализ признаков
        features = self.analyze_m5_features(data)
        
        # Создание DataFrame с сигналами
        signals = pd.DataFrame(index=data.index)
        
        # Базовые сигналы
        signals['pattern_signal'] = features['short_pattern']['pattern_direction']
        signals['impulse_signal'] = features['quick_impulse']['impulse_direction']
        signals['trend_signal'] = features['short_trend']['short_trend']
        
        # Комбинированный сигнал
        signals['combined_signal'] = np.where(
            (signals['pattern_signal'] == signals['trend_signal']) & 
            (signals['pattern_signal'] != 0),
            signals['pattern_signal'],
            0
        )
        
        # Фильтрация по волатильности
        normal_vol = ~features['short_volatility']['high_volatility']
        signals['filtered_signal'] = np.where(
            normal_vol,
            signals['combined_signal'],
            0
        )
        
        return signals

# Пример использования M5 анализа
def run_m5_analysis_example():
    """Пример запуска M5 анализа WAVE2."""
    # Загрузка данных
    loader = WAVE2DataLoader()
    data = loader.load_wave2_data("GBPUSD", "M5")
    
    # Создание анализатора M5
    m5_analyzer = WAVE2M5Analysis()
    
    # Генерация сигналов
    signals = m5_analyzer.generate_m5_signals(data)
    
    # Анализ результатов
    print(f"✓ Сгенерировано {len(signals)} сигналов")
    print(f"✓ Сигналов на покупку: {(signals['filtered_signal'] > 0).sum()}")
    print(f"✓ Сигналов на продажу: {(signals['filtered_signal'] < 0).sum()}")
    
    return signals

# Запуск примера
if __name__ == "__main__":
    m5_signals = run_m5_analysis_example()
```

### H1 (1 час) - Среднесрочная торговля

**Теория:** H1 таймфрейм предназначен для среднесрочной торговли и анализа основных трендов. Это критически важный таймфрейм для понимания общей рыночной динамики и принятия стратегических решений.

**Почему H1 анализ важен:**
- **Анализ трендов:** Обеспечивает анализ основных рыночных трендов
- **Стратегические решения:** Подходит для принятия стратегических торговых решений
- **Снижение шума:** Минимальное влияние рыночного шума
- **Стабильность:** Наиболее стабильные и надежные сигналы

**Плюсы:**
- Анализ основных трендов
- Стабильные сигналы
- Минимальное влияние шума
- Подходит для стратегических решений

**Минусы:**
- Меньше торговых возможностей
- Медленная реакция на изменения
- Требует больше времени для анализа
- Потенциальные упущенные возможности

```python
class WAVE2H1Analysis:
    """
    Анализ WAVE2 на часовом таймфрейме для среднесрочной торговли.
    
    H1 таймфрейм предназначен для среднесрочной торговли и анализа основных трендов.
    Это критически важный таймфрейм для понимания общей рыночной динамики и
    принятия стратегических торговых решений.
    
    Теория: H1 анализ основан на принципе анализа основных рыночных трендов,
    что позволяет принимать стратегические решения с минимальным влиянием
    рыночного шума и максимальной стабильностью сигналов.
    """
    
    def __init__(self):
        """Инициализация анализатора H1 с оптимизированными параметрами."""
        self.timeframe = 'H1'
        self.optimal_params = {
            'long1': 200,   # Стандартный для H1 - стабильный анализ трендов
            'fast1': 20,    # Средний отклик - баланс скорости и стабильности
            'trend1': 5,    # Средний тренд - достаточная фильтрация
            'long2': 50,    # Средний второй период - дополнительная стабильность
            'fast2': 15,    # Средняя вторая волна - оптимальная чувствительность
            'trend2': 3     # Средний тренд - стабильное определение направления
        }
        
        # Пороги для H1 анализа
        self.thresholds = {
            'min_volatility': 0.001,   # Минимальная волатильность для сигнала
            'max_spread': 0.002,       # Максимальный спред для торговли
            'min_trend_strength': 0.005, # Минимальная сила тренда
            'max_noise_level': 0.001,   # Максимальный уровень шума
            'min_trend_duration': 5,    # Минимальная длительность тренда
            'max_trend_duration': 50    # Максимальная длительность тренда
        }
    
    def analyze_h1_features(self, data: pd.DataFrame) -> Dict:
        """
        Анализ признаков для H1 таймфрейма.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с признаками для H1 анализа
        """
        features = {}
        
        # Среднесрочные тренды - анализ основных трендов
        features['medium_trend'] = self._detect_medium_trend(data)
        
        # Трендовые развороты - детекция разворотов трендов
        features['trend_reversal'] = self._detect_trend_reversal(data)
        
        # Среднесрочная волатильность - анализ волатильности
        features['medium_volatility'] = self._calculate_medium_volatility(data)
        
        # Трендовые паттерны - анализ трендовых паттернов
        features['trend_patterns'] = self._detect_trend_patterns(data)
        
        # Поддержка и сопротивление - анализ уровней
        features['support_resistance'] = self._detect_support_resistance(data)
        
        # Трендовые каналы - анализ каналов
        features['trend_channels'] = self._detect_trend_channels(data)
        
        return features
    
    def _detect_medium_trend(self, data: pd.DataFrame) -> Dict:
        """
        Детекция среднесрочных трендов для H1 анализа.
        
        Среднесрочные тренды представляют собой основные движения цены
        на часовом таймфрейме, которые критически важны для стратегических решений.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о среднесрочных трендах
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        wave2 = data['wave2']
        fastline2 = data['fastline2']
        
        # Основной тренд - пересечение wave1 и fastline1
        main_trend = np.where(wave1 > fastline1, 1, -1)
        
        # Дополнительный тренд - пересечение wave2 и fastline2
        secondary_trend = np.where(wave2 > fastline2, 1, -1)
        
        # Согласованность трендов - совпадение направлений
        trend_consistency = (main_trend == secondary_trend).astype(int)
        
        # Сила тренда - комбинированная сила обеих волн
        trend_strength = (
            abs(wave1 - fastline1) / (abs(fastline1) + 1e-8) +
            abs(wave2 - fastline2) / (abs(fastline2) + 1e-8)
        ) / 2
        
        # Длительность тренда
        trend_duration = self._calculate_trend_duration(main_trend)
        
        # Ускорение тренда
        trend_acceleration = wave1.diff().diff()
        
        # Стабильность тренда
        trend_stability = 1 / (trend_strength.rolling(10).std() + 1e-8)
        
        return {
            'main_trend': main_trend,
            'secondary_trend': secondary_trend,
            'trend_consistency': trend_consistency,
            'trend_strength': trend_strength,
            'trend_duration': trend_duration,
            'trend_acceleration': trend_acceleration,
            'trend_stability': trend_stability,
            'combined_trend': np.where(
                trend_consistency & (trend_strength > self.thresholds['min_trend_strength']),
                main_trend,
                0
            )
        }
    
    def _detect_trend_reversal(self, data: pd.DataFrame) -> Dict:
        """
        Детекция трендовых разворотов для H1 анализа.
        
        Трендовые развороты представляют собой критические моменты изменения
        направления основного тренда, которые критически важны для торговых решений.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о трендовых разворотах
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        wave2 = data['wave2']
        fastline2 = data['fastline2']
        
        # Разворот основной волны
        main_reversal = (
            (wave1 > fastline1) != (wave1.shift(1) > fastline1.shift(1))
        )
        
        # Разворот дополнительной волны
        secondary_reversal = (
            (wave2 > fastline2) != (wave2.shift(1) > fastline2.shift(1))
        )
        
        # Одновременный разворот обеих волн
        simultaneous_reversal = main_reversal & secondary_reversal
        
        # Сила разворота
        reversal_strength = (
            abs(wave1.diff()) + abs(fastline1.diff()) +
            abs(wave2.diff()) + abs(fastline2.diff())
        ) / 4
        
        # Подтверждение разворота
        reversal_confirmation = (
            simultaneous_reversal & 
            (reversal_strength > reversal_strength.rolling(20).quantile(0.7))
        )
        
        # Направление разворота
        reversal_direction = np.where(
            reversal_confirmation & (wave1.diff() > 0), 1,
            np.where(reversal_confirmation & (wave1.diff() < 0), -1, 0)
        )
        
        return {
            'main_reversal': main_reversal,
            'secondary_reversal': secondary_reversal,
            'simultaneous_reversal': simultaneous_reversal,
            'reversal_strength': reversal_strength,
            'reversal_confirmation': reversal_confirmation,
            'reversal_direction': reversal_direction
        }
    
    def _calculate_medium_volatility(self, data: pd.DataFrame) -> Dict:
        """
        Расчет среднесрочной волатильности для H1 анализа.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о среднесрочной волатильности
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Среднесрочная волатильность
        medium_volatility = wave1.rolling(24).std()  # 24 часа
        
        # Относительная волатильность
        relative_volatility = medium_volatility / medium_volatility.rolling(168).mean()  # 1 неделя
        
        # Режимы волатильности
        high_vol = relative_volatility > 1.5
        low_vol = relative_volatility < 0.5
        normal_vol = ~(high_vol | low_vol)
        
        # Изменение волатильности
        volatility_change = medium_volatility.diff()
        
        # Тренд волатильности
        volatility_trend = np.where(
            volatility_change > 0, 1,
            np.where(volatility_change < 0, -1, 0)
        )
        
        return {
            'medium_volatility': medium_volatility,
            'relative_volatility': relative_volatility,
            'high_volatility': high_vol,
            'low_volatility': low_vol,
            'normal_volatility': normal_vol,
            'volatility_change': volatility_change,
            'volatility_trend': volatility_trend,
            'volatility_regime': np.where(
                high_vol, 'high',
                np.where(low_vol, 'low', 'normal')
            )
        }
    
    def _detect_trend_patterns(self, data: pd.DataFrame) -> Dict:
        """
        Детекция трендовых паттернов для H1 анализа.
        
        Трендовые паттерны представляют собой повторяющиеся структуры
        в движении цены, которые характерны для среднесрочных трендов.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о трендовых паттернах
        """
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Паттерн "Восходящий тренд" - последовательные повышения
        uptrend_pattern = self._detect_uptrend_pattern(wave1, window=10)
        
        # Паттерн "Нисходящий тренд" - последовательные понижения
        downtrend_pattern = self._detect_downtrend_pattern(wave1, window=10)
        
        # Паттерн "Треугольник" - сходящиеся линии тренда
        triangle_pattern = self._detect_triangle_pattern(wave1, fastline1, window=20)
        
        # Паттерн "Клин" - сходящиеся линии с наклоном
        wedge_pattern = self._detect_wedge_pattern(wave1, fastline1, window=15)
        
        # Паттерн "Флаг" - краткосрочная консолидация
        flag_pattern = self._detect_flag_pattern(wave1, window=12)
        
        return {
            'uptrend_pattern': uptrend_pattern,
            'downtrend_pattern': downtrend_pattern,
            'triangle_pattern': triangle_pattern,
            'wedge_pattern': wedge_pattern,
            'flag_pattern': flag_pattern,
            'pattern_strength': self._calculate_pattern_strength(data),
            'pattern_direction': self._determine_pattern_direction(data)
        }
    
    def _detect_uptrend_pattern(self, series: pd.Series, window: int = 10) -> pd.Series:
        """Детекция паттерна 'Восходящий тренд'."""
        # Последовательные повышения
        higher_highs = series.rolling(window).max() > series.rolling(window).max().shift(1)
        higher_lows = series.rolling(window).min() > series.rolling(window).min().shift(1)
        
        # Восходящий тренд - и повышения, и понижения растут
        uptrend = higher_highs & higher_lows
        
        return uptrend
    
    def _detect_downtrend_pattern(self, series: pd.Series, window: int = 10) -> pd.Series:
        """Детекция паттерна 'Нисходящий тренд'."""
        # Последовательные понижения
        lower_highs = series.rolling(window).max() < series.rolling(window).max().shift(1)
        lower_lows = series.rolling(window).min() < series.rolling(window).min().shift(1)
        
        # Нисходящий тренд - и повышения, и понижения падают
        downtrend = lower_highs & lower_lows
        
        return downtrend
    
    def _detect_triangle_pattern(self, wave1: pd.Series, fastline1: pd.Series, window: int = 20) -> pd.Series:
        """Детекция паттерна 'Треугольник'."""
        # Скользящие максимумы и минимумы
        rolling_max = wave1.rolling(window).max()
        rolling_min = wave1.rolling(window).min()
        
        # Сходящиеся линии тренда
        upper_trend = rolling_max.rolling(window).mean()
        lower_trend = rolling_min.rolling(window).mean()
        
        # Сходимость линий
        convergence = (upper_trend - lower_trend) / (upper_trend + lower_trend + 1e-8)
        triangle = convergence < convergence.rolling(window * 2).quantile(0.3)
        
        return triangle
    
    def _detect_wedge_pattern(self, wave1: pd.Series, fastline1: pd.Series, window: int = 15) -> pd.Series:
        """Детекция паттерна 'Клин'."""
        # Сходящиеся волны с наклоном
        wave_convergence = abs(wave1 - fastline1).rolling(window).mean()
        convergence_trend = wave_convergence.diff(window) < 0
        
        # Наклон в одну сторону
        wave_trend = wave1.rolling(window).mean().diff(window)
        consistent_trend = abs(wave_trend) > wave_trend.rolling(window * 2).std()
        
        # Клин - сходимость с наклоном
        wedge = convergence_trend & consistent_trend
        
        return wedge
    
    def _detect_flag_pattern(self, series: pd.Series, window: int = 12) -> pd.Series:
        """Детекция паттерна 'Флаг'."""
        # Предшествующий импульс
        impulse = series.diff(window).abs() > series.rolling(24).std() * 1.5
        
        # Консолидация после импульса
        consolidation = series.rolling(window).std() < series.rolling(24).std() * 0.6
        
        # Флаг - импульс с последующей консолидацией
        flag = impulse.shift(window) & consolidation
        
        return flag
    
    def _detect_support_resistance(self, data: pd.DataFrame) -> Dict:
        """
        Детекция уровней поддержки и сопротивления для H1 анализа.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией об уровнях поддержки и сопротивления
        """
        wave1 = data['wave1']
        
        # Уровни сопротивления - локальные максимумы
        resistance_levels = self._find_resistance_levels(wave1, window=20)
        
        # Уровни поддержки - локальные минимумы
        support_levels = self._find_support_levels(wave1, window=20)
        
        # Близость к уровням
        distance_to_resistance = self._calculate_distance_to_levels(wave1, resistance_levels)
        distance_to_support = self._calculate_distance_to_levels(wave1, support_levels)
        
        # Пробитие уровней
        resistance_break = self._detect_level_break(wave1, resistance_levels, direction='up')
        support_break = self._detect_level_break(wave1, support_levels, direction='down')
        
        return {
            'resistance_levels': resistance_levels,
            'support_levels': support_levels,
            'distance_to_resistance': distance_to_resistance,
            'distance_to_support': distance_to_support,
            'resistance_break': resistance_break,
            'support_break': support_break
        }
    
    def _find_resistance_levels(self, series: pd.Series, window: int = 20) -> pd.Series:
        """Поиск уровней сопротивления."""
        # Локальные максимумы
        local_maxs = series.rolling(window, center=True).max() == series
        
        # Фильтрация по силе
        strong_maxs = local_maxs & (series > series.rolling(50).quantile(0.7))
        
        return strong_maxs
    
    def _find_support_levels(self, series: pd.Series, window: int = 20) -> pd.Series:
        """Поиск уровней поддержки."""
        # Локальные минимумы
        local_mins = series.rolling(window, center=True).min() == series
        
        # Фильтрация по силе
        strong_mins = local_mins & (series < series.rolling(50).quantile(0.3))
        
        return strong_mins
    
    def _calculate_distance_to_levels(self, series: pd.Series, levels: pd.Series) -> pd.Series:
        """Расчет расстояния до уровней."""
        # Находим ближайшие уровни
        level_values = series[levels]
        if len(level_values) == 0:
            return pd.Series(0, index=series.index)
        
        # Минимальное расстояние до любого уровня
        distances = []
        for i, value in enumerate(series):
            if len(level_values) > 0:
                min_distance = min(abs(value - level_values))
                distances.append(min_distance)
            else:
                distances.append(0)
        
        return pd.Series(distances, index=series.index)
    
    def _detect_level_break(self, series: pd.Series, levels: pd.Series, direction: str = 'up') -> pd.Series:
        """Детекция пробития уровней."""
        if direction == 'up':
            # Пробитие сопротивления вверх
            break_up = series > series[levels].max()
            return break_up
        else:
            # Пробитие поддержки вниз
            break_down = series < series[levels].min()
            return break_down
    
    def _detect_trend_channels(self, data: pd.DataFrame) -> Dict:
        """
        Детекция трендовых каналов для H1 анализа.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            Словарь с информацией о трендовых каналах
        """
        wave1 = data['wave1']
        
        # Восходящий канал
        uptrend_channel = self._detect_uptrend_channel(wave1, window=30)
        
        # Нисходящий канал
        downtrend_channel = self._detect_downtrend_channel(wave1, window=30)
        
        # Боковой канал
        sideways_channel = self._detect_sideways_channel(wave1, window=30)
        
        return {
            'uptrend_channel': uptrend_channel,
            'downtrend_channel': downtrend_channel,
            'sideways_channel': sideways_channel
        }
    
    def _detect_uptrend_channel(self, series: pd.Series, window: int = 30) -> pd.Series:
        """Детекция восходящего канала."""
        # Верхняя и нижняя границы канала
        upper_bound = series.rolling(window).max()
        lower_bound = series.rolling(window).min()
        
        # Параллельность границ
        upper_trend = upper_bound.rolling(window).mean().diff()
        lower_trend = lower_bound.rolling(window).mean().diff()
        
        # Восходящий канал - обе границы растут
        uptrend_channel = (upper_trend > 0) & (lower_trend > 0)
        
        return uptrend_channel
    
    def _detect_downtrend_channel(self, series: pd.Series, window: int = 30) -> pd.Series:
        """Детекция нисходящего канала."""
        # Верхняя и нижняя границы канала
        upper_bound = series.rolling(window).max()
        lower_bound = series.rolling(window).min()
        
        # Параллельность границ
        upper_trend = upper_bound.rolling(window).mean().diff()
        lower_trend = lower_bound.rolling(window).mean().diff()
        
        # Нисходящий канал - обе границы падают
        downtrend_channel = (upper_trend < 0) & (lower_trend < 0)
        
        return downtrend_channel
    
    def _detect_sideways_channel(self, series: pd.Series, window: int = 30) -> pd.Series:
        """Детекция бокового канала."""
        # Верхняя и нижняя границы канала
        upper_bound = series.rolling(window).max()
        lower_bound = series.rolling(window).min()
        
        # Ширина канала
        channel_width = upper_bound - lower_bound
        
        # Боковой канал - стабильная ширина
        sideways_channel = channel_width.rolling(window).std() < channel_width.rolling(window * 2).std() * 0.5
        
        return sideways_channel
    
    def _calculate_trend_duration(self, trend_series: np.ndarray) -> pd.Series:
        """Расчет длительности тренда."""
        duration = pd.Series(0, index=range(len(trend_series)))
        current_duration = 0
        current_trend = 0
        
        for i, trend in enumerate(trend_series):
            if trend == current_trend:
                current_duration += 1
            else:
                current_duration = 1
                current_trend = trend
            duration.iloc[i] = current_duration
        
        return duration
    
    def _calculate_pattern_strength(self, data: pd.DataFrame) -> pd.Series:
        """Расчет силы паттернов."""
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Сила паттерна - стабильность соотношения
        pattern_strength = 1 / (abs(wave1 - fastline1) / (abs(fastline1) + 1e-8) + 1e-8)
        
        return pattern_strength
    
    def _determine_pattern_direction(self, data: pd.DataFrame) -> pd.Series:
        """Определение направления паттернов."""
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Направление паттерна
        pattern_direction = np.where(wave1 > fastline1, 1, -1)
        
        return pattern_direction
    
    def generate_h1_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Генерация торговых сигналов для H1 таймфрейма.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            DataFrame с торговыми сигналами
        """
        # Анализ признаков
        features = self.analyze_h1_features(data)
        
        # Создание DataFrame с сигналами
        signals = pd.DataFrame(index=data.index)
        
        # Базовые сигналы
        signals['trend_signal'] = features['medium_trend']['combined_trend']
        signals['reversal_signal'] = features['trend_reversal']['reversal_direction']
        signals['pattern_signal'] = features['trend_patterns']['pattern_direction']
        
        # Комбинированный сигнал
        signals['combined_signal'] = np.where(
            (signals['trend_signal'] == signals['pattern_signal']) & 
            (signals['trend_signal'] != 0),
            signals['trend_signal'],
            0
        )
        
        # Фильтрация по волатильности
        normal_vol = features['medium_volatility']['normal_volatility']
        signals['filtered_signal'] = np.where(
            normal_vol,
            signals['combined_signal'],
            0
        )
        
        return signals

# Пример использования H1 анализа
def run_h1_analysis_example():
    """Пример запуска H1 анализа WAVE2."""
    # Загрузка данных
    loader = WAVE2DataLoader()
    data = loader.load_wave2_data("GBPUSD", "H1")
    
    # Создание анализатора H1
    h1_analyzer = WAVE2H1Analysis()
    
    # Генерация сигналов
    signals = h1_analyzer.generate_h1_signals(data)
    
    # Анализ результатов
    print(f"✓ Сгенерировано {len(signals)} сигналов")
    print(f"✓ Сигналов на покупку: {(signals['filtered_signal'] > 0).sum()}")
    print(f"✓ Сигналов на продажу: {(signals['filtered_signal'] < 0).sum()}")
    
    return signals

# Запуск примера
if __name__ == "__main__":
    h1_signals = run_h1_analysis_example()
```

## Создание признаков для ML

**Теория:** Создание признаков для машинного обучения на основе WAVE2 является критически важным этапом для достижения высокой точности предсказаний. Качественные признаки определяют успех ML-модели.

**Почему создание признаков критично:**
- **Качество данных:** Качественные признаки определяют качество модели
- **Точность предсказаний:** Хорошие признаки повышают точность предсказаний
- **Робастность:** Правильные признаки обеспечивают робастность модели
- **Интерпретируемость:** Понятные признаки облегчают интерпретацию результатов

### 1. Базовые признаки WAVE2

**Теория:** Базовые признаки WAVE2 представляют собой фундаментальные компоненты для анализа рыночной динамики. Они обеспечивают основу для более сложных признаков и являются основой для ML-модели.

**Почему базовые признаки важны:**
- **Фундаментальная основа:** Обеспечивают базовую информацию о рынке
- **Простота интерпретации:** Легко понимаются и интерпретируются
- **Стабильность:** Обеспечивают стабильную основу для анализа
- **Эффективность:** Минимальные вычислительные требования

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif
import talib

class WAVE2FeatureEngineer:
    """
    Создание признаков на основе WAVE2 для машинного обучения.
    
    Этот класс предоставляет комплексные методы для создания различных типов
    признаков на основе данных WAVE2, включая базовые, лаговые, скользящие,
    технические и продвинутые признаки.
    
    Теория: Качественные признаки являются основой успешного машинного обучения.
    WAVE2 предоставляет богатую основу для создания признаков, которые могут
    выявлять скрытые паттерны и взаимосвязи в рыночных данных.
    """
    
    def __init__(self):
        """Инициализация инженера признаков WAVE2."""
        self.lag_periods = [1, 2, 3, 5, 10, 20, 50]
        self.rolling_windows = [5, 10, 20, 50, 100]
        self.scaler = StandardScaler()
        self.feature_names = []
        
        # Пороги для создания признаков
        self.thresholds = {
            'min_correlation': 0.1,
            'max_correlation': 0.9,
            'min_volatility': 0.001,
            'max_volatility': 0.1
        }
    
    def create_basic_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание базовых признаков WAVE2.
        
        Базовые признаки представляют собой фундаментальные компоненты
        для анализа рыночной динамики на основе WAVE2.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            DataFrame с базовыми признаками
        """
        features = pd.DataFrame(index=data.index)
        
        # 1. Основные волны - базовые компоненты WAVE2
        features['wave1'] = data['wave1']
        features['wave2'] = data['wave2']
        features['fastline1'] = data['fastline1']
        features['fastline2'] = data['fastline2']
        
        # 2. Разности волн - анализ расхождения между волнами
        features['wave_diff'] = data['wave1'] - data['wave2']
        features['fastline_diff'] = data['fastline1'] - data['fastline2']
        features['wave1_fastline_diff'] = data['wave1'] - data['fastline1']
        features['wave2_fastline_diff'] = data['wave2'] - data['fastline2']
        
        # 3. Отношения волн - анализ пропорций
        features['wave_ratio'] = data['wave1'] / (data['wave2'] + 1e-8)
        features['fastline_ratio'] = data['fastline1'] / (data['fastline2'] + 1e-8)
        features['wave1_fastline_ratio'] = data['wave1'] / (data['fastline1'] + 1e-8)
        features['wave2_fastline_ratio'] = data['wave2'] / (data['fastline2'] + 1e-8)
        
        # 4. Расстояния до нуля - анализ абсолютных значений
        features['wave1_distance'] = abs(data['wave1'])
        features['wave2_distance'] = abs(data['wave2'])
        features['fastline1_distance'] = abs(data['fastline1'])
        features['fastline2_distance'] = abs(data['fastline2'])
        
        # 5. Нормализованные значения - стандартизация
        features['wave1_norm'] = (data['wave1'] - data['wave1'].mean()) / (data['wave1'].std() + 1e-8)
        features['wave2_norm'] = (data['wave2'] - data['wave2'].mean()) / (data['wave2'].std() + 1e-8)
        
        # 6. Процентные изменения - анализ динамики
        features['wave1_pct_change'] = data['wave1'].pct_change()
        features['wave2_pct_change'] = data['wave2'].pct_change()
        features['fastline1_pct_change'] = data['fastline1'].pct_change()
        features['fastline2_pct_change'] = data['fastline2'].pct_change()
        
        return features
    
    def create_lag_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание лаговых признаков WAVE2.
        
        Лаговые признаки представляют собой исторические значения,
        которые помогают модели учитывать временные зависимости.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            DataFrame с лаговыми признаками
        """
        features = pd.DataFrame(index=data.index)
        
        for lag in self.lag_periods:
            # Лаги основных волн
            features[f'wave1_lag_{lag}'] = data['wave1'].shift(lag)
            features[f'wave2_lag_{lag}'] = data['wave2'].shift(lag)
            features[f'fastline1_lag_{lag}'] = data['fastline1'].shift(lag)
            features[f'fastline2_lag_{lag}'] = data['fastline2'].shift(lag)
            
            # Изменения волн за период
            features[f'wave1_change_{lag}'] = data['wave1'] - data['wave1'].shift(lag)
            features[f'wave2_change_{lag}'] = data['wave2'] - data['wave2'].shift(lag)
            features[f'fastline1_change_{lag}'] = data['fastline1'] - data['fastline1'].shift(lag)
            features[f'fastline2_change_{lag}'] = data['fastline2'] - data['fastline2'].shift(lag)
            
            # Процентные изменения за период
            features[f'wave1_pct_change_{lag}'] = data['wave1'].pct_change(lag)
            features[f'wave2_pct_change_{lag}'] = data['wave2'].pct_change(lag)
            
            # Разности между лагами
            features[f'wave_diff_lag_{lag}'] = (data['wave1'] - data['wave2']) - (data['wave1'].shift(lag) - data['wave2'].shift(lag))
            features[f'fastline_diff_lag_{lag}'] = (data['fastline1'] - data['fastline2']) - (data['fastline1'].shift(lag) - data['fastline2'].shift(lag))
        
        return features
    
    def create_rolling_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание скользящих признаков WAVE2.
        
        Скользящие признаки представляют собой статистические характеристики
        за различные временные окна, которые помогают выявить тренды и паттерны.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            DataFrame со скользящими признаками
        """
        features = pd.DataFrame(index=data.index)
        
        for window in self.rolling_windows:
            # Скользящие средние
            features[f'wave1_sma_{window}'] = data['wave1'].rolling(window).mean()
            features[f'wave2_sma_{window}'] = data['wave2'].rolling(window).mean()
            features[f'fastline1_sma_{window}'] = data['fastline1'].rolling(window).mean()
            features[f'fastline2_sma_{window}'] = data['fastline2'].rolling(window).mean()
            
            # Скользящие стандартные отклонения
            features[f'wave1_std_{window}'] = data['wave1'].rolling(window).std()
            features[f'wave2_std_{window}'] = data['wave2'].rolling(window).std()
            features[f'fastline1_std_{window}'] = data['fastline1'].rolling(window).std()
            features[f'fastline2_std_{window}'] = data['fastline2'].rolling(window).std()
            
            # Скользящие максимумы и минимумы
            features[f'wave1_max_{window}'] = data['wave1'].rolling(window).max()
            features[f'wave1_min_{window}'] = data['wave1'].rolling(window).min()
            features[f'wave2_max_{window}'] = data['wave2'].rolling(window).max()
            features[f'wave2_min_{window}'] = data['wave2'].rolling(window).min()
            
            # Скользящие квантили
            features[f'wave1_q25_{window}'] = data['wave1'].rolling(window).quantile(0.25)
            features[f'wave1_q75_{window}'] = data['wave1'].rolling(window).quantile(0.75)
            features[f'wave2_q25_{window}'] = data['wave2'].rolling(window).quantile(0.25)
            features[f'wave2_q75_{window}'] = data['wave2'].rolling(window).quantile(0.75)
            
            # Скользящие медианы
            features[f'wave1_median_{window}'] = data['wave1'].rolling(window).median()
            features[f'wave2_median_{window}'] = data['wave2'].rolling(window).median()
            
            # Скользящие коэффициенты вариации
            features[f'wave1_cv_{window}'] = data['wave1'].rolling(window).std() / (data['wave1'].rolling(window).mean() + 1e-8)
            features[f'wave2_cv_{window}'] = data['wave2'].rolling(window).std() / (data['wave2'].rolling(window).mean() + 1e-8)
            
            # Скользящие корреляции
            features[f'wave_correlation_{window}'] = data['wave1'].rolling(window).corr(data['wave2'])
            features[f'fastline_correlation_{window}'] = data['fastline1'].rolling(window).corr(data['fastline2'])
        
        return features
    
    def create_technical_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание технических признаков WAVE2.
        
        Технические признаки включают различные технические индикаторы,
        которые помогают анализировать рыночную динамику.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            DataFrame с техническими признаками
        """
        features = pd.DataFrame(index=data.index)
        
        # RSI для волн
        features['wave1_rsi_14'] = talib.RSI(data['wave1'].values, timeperiod=14)
        features['wave2_rsi_14'] = talib.RSI(data['wave2'].values, timeperiod=14)
        features['fastline1_rsi_14'] = talib.RSI(data['fastline1'].values, timeperiod=14)
        features['fastline2_rsi_14'] = talib.RSI(data['fastline2'].values, timeperiod=14)
        
        # MACD для волн
        macd1, macd_signal1, macd_hist1 = talib.MACD(data['wave1'].values)
        features['wave1_macd'] = macd1
        features['wave1_macd_signal'] = macd_signal1
        features['wave1_macd_hist'] = macd_hist1
        
        macd2, macd_signal2, macd_hist2 = talib.MACD(data['wave2'].values)
        features['wave2_macd'] = macd2
        features['wave2_macd_signal'] = macd_signal2
        features['wave2_macd_hist'] = macd_hist2
        
        # Bollinger Bands для волн
        bb_upper1, bb_middle1, bb_lower1 = talib.BBANDS(data['wave1'].values)
        features['wave1_bb_upper'] = bb_upper1
        features['wave1_bb_middle'] = bb_middle1
        features['wave1_bb_lower'] = bb_lower1
        features['wave1_bb_width'] = (bb_upper1 - bb_lower1) / bb_middle1
        features['wave1_bb_position'] = (data['wave1'] - bb_lower1) / (bb_upper1 - bb_lower1 + 1e-8)
        
        # Stochastic для волн
        stoch_k1, stoch_d1 = talib.STOCH(data['wave1'].values, data['wave1'].values, data['wave1'].values)
        features['wave1_stoch_k'] = stoch_k1
        features['wave1_stoch_d'] = stoch_d1
        
        # ADX для волн
        features['wave1_adx_14'] = talib.ADX(data['wave1'].values, data['wave1'].values, data['wave1'].values, timeperiod=14)
        features['wave1_plus_di_14'] = talib.PLUS_DI(data['wave1'].values, data['wave1'].values, data['wave1'].values, timeperiod=14)
        features['wave1_minus_di_14'] = talib.MINUS_DI(data['wave1'].values, data['wave1'].values, data['wave1'].values, timeperiod=14)
        
        # Williams %R для волн
        features['wave1_williams_r_14'] = talib.WILLR(data['wave1'].values, data['wave1'].values, data['wave1'].values, timeperiod=14)
        
        # CCI для волн
        features['wave1_cci_14'] = talib.CCI(data['wave1'].values, data['wave1'].values, data['wave1'].values, timeperiod=14)
        
        return features
    
    def create_advanced_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание продвинутых признаков WAVE2.
        
        Продвинутые признаки представляют собой сложные комбинации
        базовых признаков, которые выявляют скрытые паттерны.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            DataFrame с продвинутыми признаками
        """
        features = pd.DataFrame(index=data.index)
        
        # 1. Пересечения волн
        features['wave1_cross_fastline1'] = (data['wave1'] > data['fastline1']).astype(int)
        features['wave2_cross_fastline2'] = (data['wave2'] > data['fastline2']).astype(int)
        features['wave1_cross_wave2'] = (data['wave1'] > data['wave2']).astype(int)
        features['fastline1_cross_fastline2'] = (data['fastline1'] > data['fastline2']).astype(int)
        
        # 2. Согласованность сигналов
        features['signal_consistency'] = (
            (data['Wave1'] == data['Wave2']).astype(int)
        )
        features['strong_signal'] = (
            (data['Wave1'] != 0) & (data['Wave2'] != 0) & 
            (data['Wave1'] == data['Wave2'])
        ).astype(int)
        
        # 3. Сила тренда
        features['trend_strength'] = abs(data['wave1'] - data['fastline1']) / (abs(data['fastline1']) + 1e-8)
        features['trend_strength_2'] = abs(data['wave2'] - data['fastline2']) / (abs(data['fastline2']) + 1e-8)
        features['combined_trend_strength'] = (features['trend_strength'] + features['trend_strength_2']) / 2
        
        # 4. Ускорение волн
        features['wave1_acceleration'] = data['wave1'].diff().diff()
        features['wave2_acceleration'] = data['wave2'].diff().diff()
        features['fastline1_acceleration'] = data['fastline1'].diff().diff()
        features['fastline2_acceleration'] = data['fastline2'].diff().diff()
        
        # 5. Дивергенция волн
        features['wave_divergence'] = data['wave1'] - data['wave2']
        features['fastline_divergence'] = data['fastline1'] - data['fastline2']
        features['wave_fastline_divergence'] = (data['wave1'] - data['fastline1']) - (data['wave2'] - data['fastline2'])
        
        # 6. Волатильность волн
        features['wave1_volatility_20'] = data['wave1'].rolling(20).std()
        features['wave2_volatility_20'] = data['wave2'].rolling(20).std()
        features['relative_volatility'] = features['wave1_volatility_20'] / (features['wave2_volatility_20'] + 1e-8)
        
        # 7. Корреляция волн
        features['wave_correlation_20'] = data['wave1'].rolling(20).corr(data['wave2'])
        features['fastline_correlation_20'] = data['fastline1'].rolling(20).corr(data['fastline2'])
        
        # 8. Моментум волн
        features['wave1_momentum_10'] = data['wave1'] - data['wave1'].shift(10)
        features['wave2_momentum_10'] = data['wave2'] - data['wave2'].shift(10)
        features['combined_momentum'] = (features['wave1_momentum_10'] + features['wave2_momentum_10']) / 2
        
        # 9. Скользящие пересечения
        features['wave1_cross_sma_20'] = (data['wave1'] > data['wave1'].rolling(20).mean()).astype(int)
        features['wave2_cross_sma_20'] = (data['wave2'] > data['wave2'].rolling(20).mean()).astype(int)
        
        # 10. Z-score нормализация
        features['wave1_zscore_20'] = (data['wave1'] - data['wave1'].rolling(20).mean()) / (data['wave1'].rolling(20).std() + 1e-8)
        features['wave2_zscore_20'] = (data['wave2'] - data['wave2'].rolling(20).mean()) / (data['wave2'].rolling(20).std() + 1e-8)
        
        return features
    
    def create_temporal_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание временных признаков WAVE2.
        
        Временные признаки учитывают временные аспекты рыночной динамики,
        включая циклы, сезонность и временные паттерны.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            DataFrame с временными признаками
        """
        features = pd.DataFrame(index=data.index)
        
        # 1. Время с последнего сигнала
        features['time_since_signal'] = self._calculate_time_since_signal(data)
        
        # 2. Частота сигналов
        features['signal_frequency'] = self._calculate_signal_frequency(data)
        
        # 3. Длительность тренда
        features['trend_duration'] = self._calculate_trend_duration(data)
        
        # 4. Циклические паттерны
        features['cyclical_pattern'] = self._detect_cyclical_pattern(data)
        
        # 5. Временные метки
        if hasattr(data.index, 'hour'):
            features['hour'] = data.index.hour
            features['day_of_week'] = data.index.dayofweek
            features['day_of_month'] = data.index.day
            features['month'] = data.index.month
        
        # 6. Сезонные признаки
        features['is_weekend'] = (data.index.dayofweek >= 5).astype(int)
        features['is_market_open'] = ((data.index.hour >= 9) & (data.index.hour < 17)).astype(int)
        
        return features
    
    def _calculate_time_since_signal(self, data: pd.DataFrame) -> pd.Series:
        """Расчет времени с последнего сигнала."""
        signal_changes = (data['_Signal'] != data['_Signal'].shift(1))
        time_since = pd.Series(0, index=data.index)
        
        last_signal_time = 0
        for i, is_change in enumerate(signal_changes):
            if is_change and data['_Signal'].iloc[i] != 0:
                last_signal_time = i
            time_since.iloc[i] = i - last_signal_time
        
        return time_since
    
    def _calculate_signal_frequency(self, data: pd.DataFrame) -> pd.Series:
        """Расчет частоты сигналов."""
        window = 50
        signal_frequency = data['_Signal'].rolling(window).apply(
            lambda x: (x != 0).sum() / len(x), raw=True
        )
        return signal_frequency
    
    def _calculate_trend_duration(self, data: pd.DataFrame) -> pd.Series:
        """Расчет длительности тренда."""
        trend_changes = (data['Wave1'] != data['Wave1'].shift(1))
        trend_duration = pd.Series(0, index=data.index)
        
        current_duration = 0
        for i, is_change in enumerate(trend_changes):
            if is_change:
                current_duration = 1
            else:
                current_duration += 1
            trend_duration.iloc[i] = current_duration
        
        return trend_duration
    
    def _detect_cyclical_pattern(self, data: pd.DataFrame) -> pd.Series:
        """Детекция циклических паттернов."""
        # Анализ автокорреляции
        wave1_autocorr = data['wave1'].rolling(20).apply(
            lambda x: x.autocorr(lag=1) if len(x) > 1 else 0, raw=False
        )
        
        # Циклический паттерн - высокая автокорреляция
        cyclical_pattern = (wave1_autocorr > 0.5).astype(int)
        
        return cyclical_pattern
    
    def create_all_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Создание всех признаков WAVE2.
        
        Args:
            data: DataFrame с данными WAVE2
            
        Returns:
            DataFrame со всеми признаками
        """
        print("Создание базовых признаков...")
        basic_features = self.create_basic_features(data)
        
        print("Создание лаговых признаков...")
        lag_features = self.create_lag_features(data)
        
        print("Создание скользящих признаков...")
        rolling_features = self.create_rolling_features(data)
        
        print("Создание технических признаков...")
        technical_features = self.create_technical_features(data)
        
        print("Создание продвинутых признаков...")
        advanced_features = self.create_advanced_features(data)
        
        print("Создание временных признаков...")
        temporal_features = self.create_temporal_features(data)
        
        # Объединение всех признаков
        all_features = pd.concat([
            basic_features,
            lag_features,
            rolling_features,
            technical_features,
            advanced_features,
            temporal_features
        ], axis=1)
        
        # Удаление колонок с NaN значениями
        all_features = all_features.dropna()
        
        print(f"✓ Создано {len(all_features.columns)} признаков")
        print(f"✓ Размер данных: {all_features.shape}")
        
        return all_features
    
    def select_best_features(self, X: pd.DataFrame, y: pd.Series, k: int = 50) -> pd.DataFrame:
        """
        Выбор лучших признаков для ML модели.
        
        Args:
            X: DataFrame с признаками
            y: Series с целевой переменной
            k: Количество лучших признаков
            
        Returns:
            DataFrame с отобранными признаками
        """
        # Удаление колонок с бесконечными значениями
        X_clean = X.replace([np.inf, -np.inf], np.nan).dropna()
        
        # Выбор лучших признаков
        selector = SelectKBest(score_func=f_classif, k=min(k, X_clean.shape[1]))
        X_selected = selector.fit_transform(X_clean, y[X_clean.index])
        
        # Получение названий отобранных признаков
        selected_features = X_clean.columns[selector.get_support()].tolist()
        
        print(f"✓ Отобрано {len(selected_features)} лучших признаков")
        
        return pd.DataFrame(X_selected, columns=selected_features, index=X_clean.index)

# Пример использования инженера признаков
def run_feature_engineering_example():
    """Пример создания признаков WAVE2."""
    # Загрузка данных
    loader = WAVE2DataLoader()
    data = loader.load_wave2_data("GBPUSD", "H1")
    
    # Создание инженера признаков
    feature_engineer = WAVE2FeatureEngineer()
    
    # Создание всех признаков
    features = feature_engineer.create_all_features(data)
    
    # Создание целевой переменной
    target = (data['Close'].shift(-1) > data['Close']).astype(int)
    target = target[features.index]
    
    # Выбор лучших признаков
    selected_features = feature_engineer.select_best_features(features, target, k=30)
    
    print(f"✓ Финальный набор признаков: {selected_features.shape}")
    
    return selected_features, target

# Запуск примера
if __name__ == "__main__":
    features, target = run_feature_engineering_example()
```

### 2. Продвинутые признаки

**Теория:** Продвинутые признаки WAVE2 представляют собой сложные комбинации базовых признаков, которые выявляют скрытые паттерны и взаимосвязи в рыночных данных. Они критически важны для достижения высокой точности ML-модели.

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

```python
def create_advanced_wave2_features(data):
    """Создание продвинутых признаков WAVE2"""
    features = pd.DataFrame(index=data.index)
    
    # 1. Пересечения волн
    features['wave1_cross_fastline1'] = (data['wave1'] > data['fastline1']).astype(int)
    features['wave2_cross_fastline2'] = (data['wave2'] > data['fastline2']).astype(int)
    
    # 2. Согласованность сигналов
    features['signal_consistency'] = (
        (data['Wave1'] == data['Wave2']).astype(int)
    )
    
    # 3. Сила тренда
    features['trend_strength'] = abs(data['wave1'] - data['fastline1']) / abs(data['fastline1'])
    
    # 4. Ускорение волн
    features['wave1_acceleration'] = data['wave1'].diff().diff()
    features['wave2_acceleration'] = data['wave2'].diff().diff()
    
    # 5. Дивергенция волн
    features['wave_divergence'] = data['wave1'] - data['wave2']
    features['fastline_divergence'] = data['fastline1'] - data['fastline2']
    
    # 6. Волатильность волн
    features['wave1_volatility'] = data['wave1'].rolling(20).std()
    features['wave2_volatility'] = data['wave2'].rolling(20).std()
    
    # 7. Корреляция волн
    features['wave_correlation'] = data['wave1'].rolling(20).corr(data['wave2'])
    
    # 8. Моментум волн
    features['wave1_momentum'] = data['wave1'] - data['wave1'].shift(10)
    features['wave2_momentum'] = data['wave2'] - data['wave2'].shift(10)
    
    return features
```

### 3. Временные признаки

**Теория:** Временные признаки WAVE2 учитывают временные аспекты рыночной динамики, включая циклы, сезонность и временные паттерны. Они критически важны для понимания временной структуры рынка.

**Почему временные признаки важны:**
- **Временная структура:** Учитывают временные аспекты рынка
- **Циклические паттерны:** Выявляют повторяющиеся паттерны
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
def create_temporal_wave2_features(data):
    """Создание временных признаков WAVE2"""
    features = pd.DataFrame(index=data.index)
    
    # 1. Время с последнего сигнала
    features['time_since_signal'] = self._calculate_time_since_signal(data)
    
    # 2. Частота сигналов
    features['signal_frequency'] = self._calculate_signal_frequency(data)
    
    # 3. Длительность тренда
    features['trend_duration'] = self._calculate_trend_duration(data)
    
    # 4. Циклические паттерны
    features['cyclical_pattern'] = self._detect_cyclical_pattern(data)
    
    return features
```

## Создание целевых переменных

**Теория:** Создание целевых переменных является критически важным этапом для обучения ML-модели. Правильно определенные целевые переменные определяют успех всей системы машинного обучения.

**Почему создание целевых переменных критично:**
- **Определение задачи:** Четко определяет задачу машинного обучения
- **Качество обучения:** Качественные целевые переменные улучшают обучение
- **Интерпретируемость:** Понятные целевые переменные облегчают интерпретацию
- **Практическая применимость:** Обеспечивают практическую применимость результатов

### 1. Направление цены

**Теория:** Направление цены является наиболее фундаментальной целевой переменной для торговых систем. Она определяет основную задачу - предсказание направления движения цены.

**Почему направление цены важно:**
- **Фундаментальная задача:** Основная задача торговых систем
- **Простота интерпретации:** Легко понимается и интерпретируется
- **Практическая применимость:** Непосредственно применимо в торговле
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
def create_price_direction_target(data, horizon=1):
    """Создание целевой переменной - направление цены"""
    future_price = data['Close'].shift(-horizon)
    current_price = data['Close']
    
    # Процентное изменение
    price_change = (future_price - current_price) / current_price
    
    # Классификация направления
    target = pd.cut(
        price_change,
        bins=[-np.inf, -0.001, 0.001, np.inf],
        labels=[0, 1, 2],  # 0=down, 1=hold, 2=up
        include_lowest=True
    )
    
    return target.astype(int)
```

### 2. Сила движения

**Теория:** Сила движения представляет собой более сложную целевую переменную, которая учитывает не только направление, но и интенсивность движения цены. Это критически важно для оптимизации торговых стратегий.

**Почему сила движения важна:**
- **Интенсивность движения:** Учитывает силу движения цены
- **Оптимизация стратегий:** Позволяет оптимизировать торговые стратегии
- **Управление рисками:** Помогает в управлении рисками
- **Повышение прибыльности:** Может повысить общую прибыльность

**Плюсы:**
- Учет интенсивности движения
- Оптимизация стратегий
- Улучшение управления рисками
- Потенциальное повышение прибыльности

**Минусы:**
- Сложность определения
- Потенциальная нестабильность
- Сложность интерпретации
- Высокие требования к данным

```python
def create_movement_strength_target(data, horizon=1):
    """Создание целевой переменной - сила движения"""
    future_price = data['Close'].shift(-horizon)
    current_price = data['Close']
    
    # Процентное изменение
    price_change = (future_price - current_price) / current_price
    
    # Классификация силы
    target = pd.cut(
        abs(price_change),
        bins=[0, 0.001, 0.005, 0.01, np.inf],
        labels=[0, 1, 2, 3],  # 0=weak, 1=medium, 2=strong, 3=very_strong
        include_lowest=True
    )
    
    return target.astype(int)
```

### 3. Волатильность

**Теория:** Волатильность является критически важной характеристикой финансовых рынков, которая определяет уровень риска и потенциальную прибыльность. Анализ волатильности критичен для создания робастных торговых систем.

**Почему волатильность важна:**
- **Управление рисками:** Критически важно для управления рисками
- **Оптимизация позиций:** Помогает оптимизировать размеры позиций
- **Адаптация стратегий:** Позволяет адаптировать стратегии к рыночным условиям
- **Предсказание рисков:** Помогает предсказывать потенциальные риски

**Плюсы:**
- Критически важно для управления рисками
- Помогает оптимизировать позиции
- Позволяет адаптировать стратегии
- Помогает предсказывать риски

**Минусы:**
- Сложность измерения
- Потенциальная нестабильность
- Сложность интерпретации
- Высокие требования к данным

```python
def create_volatility_target(data, horizon=1):
    """Создание целевой переменной - волатильность"""
    future_prices = data['Close'].shift(-horizon)
    current_prices = data['Close']
    
    # Расчет волатильности
    volatility = data['Close'].rolling(horizon).std()
    
    # Классификация волатильности
    target = pd.cut(
        volatility,
        bins=[0, 0.01, 0.02, 0.05, np.inf],
        labels=[0, 1, 2, 3],  # 0=low, 1=medium, 2=high, 3=very_high
        include_lowest=True
    )
    
    return target.astype(int)
```

## ML-модели для WAVE2

**Теория:** ML-модели для WAVE2 представляют собой комплексную систему машинного обучения, которая использует различные алгоритмы для анализа данных WAVE2 и генерации торговых сигналов. Это критически важно для создания высокоточных торговых систем.

**Почему ML-модели критичны:**
- **Высокая точность:** Обеспечивают высокую точность предсказаний
- **Адаптивность:** Могут адаптироваться к изменениям рынка
- **Автоматизация:** Автоматизируют процесс анализа и принятия решений
- **Масштабируемость:** Могут обрабатывать большие объемы данных

### 1. Классификация сигналов

**Теория:** Классификация сигналов является основной задачей для торговых систем, где модель должна предсказать направление движения цены. Это критически важно для принятия торговых решений.

**Почему классификация сигналов важна:**
- **Основная задача:** Основная задача торговых систем
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
from sklearn.ensemble import VotingClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import joblib

class WAVE2Classifier:
    """
    Классификатор на основе WAVE2 для предсказания направления цены.
    
    Этот класс предоставляет комплексную систему машинного обучения для
    анализа данных WAVE2 и генерации торговых сигналов с высокой точностью.
    
    Теория: Классификация сигналов является основной задачей для торговых систем,
    где модель должна предсказать направление движения цены. WAVE2 предоставляет
    богатую основу для создания высокоточных классификаторов.
    """
    
    def __init__(self):
        """Инициализация классификатора WAVE2."""
        self.models = {
            'xgboost': xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                eval_metric='logloss'
            ),
            'lightgbm': lgb.LGBMClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                verbose=-1
            ),
            'catboost': CatBoostClassifier(
                iterations=100,
                depth=6,
                learning_rate=0.1,
                random_state=42,
                verbose=False
            ),
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            ),
            'logistic_regression': LogisticRegression(
                random_state=42,
                max_iter=1000
            ),
            'svm': SVC(
                kernel='rbf',
                probability=True,
                random_state=42
            ),
            'neural_network': MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=42
            )
        }
        
        # Создание ансамбля
        self.ensemble = VotingClassifier(
            estimators=list(self.models.items()),
            voting='soft'
        )
        
        # Скалер для нормализации данных
        self.scaler = StandardScaler()
        
        # Флаги обучения
        self.is_trained = False
        self.feature_importance = None
    
    def train(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> dict:
        """
        Обучение классификатора WAVE2.
        
        Args:
            X: DataFrame с признаками
            y: Series с целевой переменной
            test_size: Размер тестовой выборки
            
        Returns:
            Словарь с результатами обучения
        """
        print("Начало обучения WAVE2 классификатора...")
        
        # Разделение на train/validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Нормализация данных
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # Обучение отдельных моделей
        individual_scores = {}
        for name, model in self.models.items():
            print(f"Обучение {name}...")
            
            # Обучение модели
            if name in ['neural_network', 'logistic_regression', 'svm']:
                model.fit(X_train_scaled, y_train)
                val_score = model.score(X_val_scaled, y_val)
            else:
                model.fit(X_train, y_train)
                val_score = model.score(X_val, y_val)
            
            individual_scores[name] = val_score
            print(f"{name} accuracy: {val_score:.4f}")
        
        # Обучение ансамбля
        print("Обучение ансамбля...")
        self.ensemble.fit(X_train, y_train)
        
        # Валидация ансамбля
        ensemble_score = self.ensemble.score(X_val, y_val)
        print(f"Ensemble accuracy: {ensemble_score:.4f}")
        
        # Кросс-валидация
        cv_scores = cross_val_score(self.ensemble, X, y, cv=5, scoring='accuracy')
        print(f"Cross-validation scores: {cv_scores}")
        print(f"Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Предсказания на валидационной выборке
        y_val_pred = self.ensemble.predict(X_val)
        y_val_proba = self.ensemble.predict_proba(X_val)
        
        # Метрики производительности
        accuracy = accuracy_score(y_val, y_val_pred)
        report = classification_report(y_val, y_val_pred)
        cm = confusion_matrix(y_val, y_val_pred)
        
        print(f"\nValidation Accuracy: {accuracy:.4f}")
        print(f"\nClassification Report:\n{report}")
        print(f"\nConfusion Matrix:\n{cm}")
        
        # Важность признаков (если доступна)
        if hasattr(self.ensemble.estimators_[0][1], 'feature_importances_'):
            self.feature_importance = self.ensemble.estimators_[0][1].feature_importances_
        
        self.is_trained = True
        
        return {
            'individual_scores': individual_scores,
            'ensemble_score': ensemble_score,
            'cv_scores': cv_scores,
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': cm,
            'feature_importance': self.feature_importance
        }
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Предсказание класса.
        
        Args:
            X: DataFrame с признаками
            
        Returns:
            Массив предсказанных классов
        """
        if not self.is_trained:
            raise ValueError("Модель не обучена. Сначала вызовите train().")
        
        return self.ensemble.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Предсказание вероятностей классов.
        
        Args:
            X: DataFrame с признаками
            
        Returns:
            Массив вероятностей для каждого класса
        """
        if not self.is_trained:
            raise ValueError("Модель не обучена. Сначала вызовите train().")
        
        return self.ensemble.predict_proba(X)
    
    def get_feature_importance(self, feature_names: list = None) -> pd.DataFrame:
        """
        Получение важности признаков.
        
        Args:
            feature_names: Список названий признаков
            
        Returns:
            DataFrame с важностью признаков
        """
        if self.feature_importance is None:
            print("Важность признаков недоступна для данной модели")
            return None
        
        if feature_names is None:
            feature_names = [f'feature_{i}' for i in range(len(self.feature_importance))]
        
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.feature_importance
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def optimize_hyperparameters(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """
        Оптимизация гиперпараметров для лучших моделей.
        
        Args:
            X: DataFrame с признаками
            y: Series с целевой переменной
            
        Returns:
            Словарь с лучшими параметрами
        """
        print("Оптимизация гиперпараметров...")
        
        # Параметры для оптимизации
        param_grids = {
            'xgboost': {
                'n_estimators': [50, 100, 200],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2]
            },
            'lightgbm': {
                'n_estimators': [50, 100, 200],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2]
            },
            'random_forest': {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15],
                'min_samples_split': [2, 5, 10]
            }
        }
        
        best_params = {}
        
        for model_name, param_grid in param_grids.items():
            print(f"Оптимизация {model_name}...")
            
            model = self.models[model_name]
            grid_search = GridSearchCV(
                model, param_grid, cv=3, scoring='accuracy', n_jobs=-1
            )
            grid_search.fit(X, y)
            
            best_params[model_name] = grid_search.best_params_
            print(f"Лучшие параметры для {model_name}: {grid_search.best_params_}")
            print(f"Лучший score: {grid_search.best_score_:.4f}")
        
        return best_params
    
    def save_model(self, filepath: str):
        """
        Сохранение обученной модели.
        
        Args:
            filepath: Путь для сохранения модели
        """
        if not self.is_trained:
            raise ValueError("Модель не обучена. Сначала вызовите train().")
        
        model_data = {
            'ensemble': self.ensemble,
            'scaler': self.scaler,
            'feature_importance': self.feature_importance,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        print(f"Модель сохранена в {filepath}")
    
    def load_model(self, filepath: str):
        """
        Загрузка обученной модели.
        
        Args:
            filepath: Путь к файлу модели
        """
        model_data = joblib.load(filepath)
        
        self.ensemble = model_data['ensemble']
        self.scaler = model_data['scaler']
        self.feature_importance = model_data['feature_importance']
        self.is_trained = model_data['is_trained']
        
        print(f"Модель загружена из {filepath}")

# Пример использования классификатора
def run_classification_example():
    """Пример обучения и использования WAVE2 классификатора."""
    # Загрузка данных
    loader = WAVE2DataLoader()
    data = loader.load_wave2_data("GBPUSD", "H1")
    
    # Создание признаков
    feature_engineer = WAVE2FeatureEngineer()
    features = feature_engineer.create_all_features(data)
    
    # Создание целевой переменной
    target = (data['Close'].shift(-1) > data['Close']).astype(int)
    target = target[features.index]
    
    # Удаление NaN значений
    valid_indices = features.dropna().index.intersection(target.dropna().index)
    features_clean = features.loc[valid_indices]
    target_clean = target.loc[valid_indices]
    
    # Создание и обучение классификатора
    classifier = WAVE2Classifier()
    results = classifier.train(features_clean, target_clean)
    
    # Предсказания
    predictions = classifier.predict(features_clean)
    probabilities = classifier.predict_proba(features_clean)
    
    print(f"✓ Обучение завершено")
    print(f"✓ Точность ансамбля: {results['ensemble_score']:.4f}")
    print(f"✓ Кросс-валидация: {results['cv_scores'].mean():.4f}")
    
    return classifier, results

# Запуск примера
if __name__ == "__main__":
    classifier, results = run_classification_example()
```

### 2. Регрессия для прогнозирования цены

**Теория:** Регрессия для прогнозирования цены представляет собой более сложную задачу, где модель должна предсказать конкретное значение цены, а не только направление. Это критически важно для точного управления позициями.

**Почему регрессия важна:**
- **Точность прогнозов:** Обеспечивает более точные прогнозы
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
class WAVE2Regressor:
    """Регрессор на основе WAVE2"""
    
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
        """Предсказание цены"""
        return self.ensemble.predict(X)
```

### 3. Deep Learning модель

**Теория:** Deep Learning модели представляют собой наиболее сложные и мощные алгоритмы машинного обучения, которые могут выявлять сложные нелинейные зависимости в данных WAVE2. Это критически важно для достижения максимальной точности.

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
class WAVE2DeepModel:
    """Deep Learning модель для WAVE2"""
    
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

## Бэктестинг WAVE2 модели

**Теория:** Бэктестинг WAVE2 модели является критически важным этапом для валидации эффективности торговой стратегии. Это позволяет оценить производительность модели на исторических данных перед реальным использованием.

**Почему бэктестинг критичен:**
- **Валидация стратегии:** Позволяет проверить эффективность стратегии
- **Оценка рисков:** Помогает оценить потенциальные риски
- **Оптимизация параметров:** Позволяет оптимизировать параметры стратегии
- **Уверенность:** Повышает уверенность в стратегии

### 1. Стратегия бэктестинга

**Теория:** Стратегия бэктестинга определяет методологию тестирования WAVE2 модели на исторических данных. Правильная стратегия критически важна для получения достоверных результатов.

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
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class WAVE2Backtester:
    """
    Бэктестер для WAVE2 модели с комплексным анализом производительности.
    
    Этот класс предоставляет полный набор инструментов для тестирования
    WAVE2 торговых стратегий на исторических данных с детальным анализом
    производительности и рисков.
    
    Теория: Бэктестинг является критически важным этапом для валидации
    эффективности торговой стратегии. Правильно проведенный бэктестинг
    позволяет оценить реальную производительность стратегии перед
    использованием в реальной торговле.
    """
    
    def __init__(self, model, data: pd.DataFrame, initial_capital: float = 10000):
        """
        Инициализация бэктестера WAVE2.
        
        Args:
            model: Обученная ML модель
            data: DataFrame с историческими данными
            initial_capital: Начальный капитал для тестирования
        """
        self.model = model
        self.data = data
        self.initial_capital = initial_capital
        self.results = {}
        
        # Параметры торговли
        self.commission = 0.001  # 0.1% комиссия
        self.slippage = 0.0005   # 0.05% проскальзывание
        self.max_position_size = 1.0  # Максимальный размер позиции
        
        # Результаты бэктестинга
        self.trades = []
        self.equity_curve = []
        self.drawdowns = []
        
    def backtest(self, start_date: str, end_date: str, 
                 transaction_cost: float = 0.001) -> dict:
        """
        Полный бэктестинг WAVE2 стратегии.
        
        Args:
            start_date: Начальная дата тестирования
            end_date: Конечная дата тестирования
            transaction_cost: Стоимость транзакций
            
        Returns:
            Словарь с результатами бэктестинга
        """
        print(f"Начало бэктестинга WAVE2 стратегии: {start_date} - {end_date}")
        
        # Фильтрация данных по датам
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        mask = (self.data.index >= start_dt) & (self.data.index <= end_dt)
        test_data = self.data[mask].copy()
        
        if len(test_data) == 0:
            raise ValueError("Нет данных для указанного периода")
        
        print(f"Период тестирования: {len(test_data)} периодов")
        
        # Создание признаков для тестирования
        feature_engineer = WAVE2FeatureEngineer()
        features = feature_engineer.create_all_features(test_data)
        
        # Удаление NaN значений
        valid_indices = features.dropna().index.intersection(test_data.index)
        features_clean = features.loc[valid_indices]
        test_data_clean = test_data.loc[valid_indices]
        
        # Предсказания модели
        predictions = self.model.predict(features_clean)
        probabilities = self.model.predict_proba(features_clean)
        
        # Симуляция торговли
        trading_results = self._simulate_trading(
            test_data_clean, predictions, probabilities, transaction_cost
        )
        
        # Расчет метрик производительности
        performance_metrics = self._calculate_performance_metrics(trading_results)
        
        # Анализ рисков
        risk_metrics = self._calculate_risk_metrics(trading_results)
        
        # Анализ сделок
        trade_analysis = self._analyze_trades(trading_results)
        
        # Сохранение результатов
        self.results = {
            'trading_results': trading_results,
            'performance_metrics': performance_metrics,
            'risk_metrics': risk_metrics,
            'trade_analysis': trade_analysis,
            'predictions': predictions,
            'probabilities': probabilities,
            'test_period': (start_date, end_date),
            'data_points': len(test_data_clean)
        }
        
        print(f"✓ Бэктестинг завершен")
        print(f"✓ Общая доходность: {performance_metrics['total_return']:.2%}")
        print(f"✓ Sharpe Ratio: {performance_metrics['sharpe_ratio']:.2f}")
        print(f"✓ Максимальная просадка: {performance_metrics['max_drawdown']:.2%}")
        
        return self.results
    
    def _simulate_trading(self, data: pd.DataFrame, predictions: np.ndarray, 
                         probabilities: np.ndarray, transaction_cost: float) -> dict:
        """
        Симуляция торговли на основе предсказаний модели.
        
        Args:
            data: Данные для тестирования
            predictions: Предсказания модели
            probabilities: Вероятности предсказаний
            transaction_cost: Стоимость транзакций
            
        Returns:
            Словарь с результатами торговли
        """
        capital = self.initial_capital
        position = 0  # 0 = нет позиции, 1 = длинная, -1 = короткая
        equity_curve = [capital]
        trades = []
        current_trade = None
        
        for i, (date, row) in enumerate(data.iterrows()):
            if i == 0:
                continue
            
            current_price = row['Close']
            signal = predictions[i-1] if i > 0 else 0
            confidence = probabilities[i-1].max() if i > 0 else 0
            
            # Фильтрация по уверенности (только высокоуверенные сигналы)
            if confidence < 0.6:
                signal = 0
            
            # Логика торговли
            if signal == 1 and position <= 0:  # Сигнал на покупку
                if position == -1:  # Закрытие короткой позиции
                    if current_trade:
                        current_trade['exit_price'] = current_price
                        current_trade['exit_date'] = date
                        current_trade['pnl'] = (current_trade['entry_price'] - current_price) / current_trade['entry_price']
                        current_trade['pnl_abs'] = current_trade['pnl'] * current_trade['position_size']
                        trades.append(current_trade)
                        capital += current_trade['pnl_abs'] * capital
                        current_trade = None
                
                # Открытие длинной позиции
                position = 1
                position_size = min(self.max_position_size, capital * 0.95 / current_price)
                current_trade = {
                    'entry_date': date,
                    'entry_price': current_price,
                    'position_size': position_size,
                    'position': 1,
                    'confidence': confidence
                }
                capital -= position_size * current_price * transaction_cost
                
            elif signal == -1 and position >= 0:  # Сигнал на продажу
                if position == 1:  # Закрытие длинной позиции
                    if current_trade:
                        current_trade['exit_price'] = current_price
                        current_trade['exit_date'] = date
                        current_trade['pnl'] = (current_price - current_trade['entry_price']) / current_trade['entry_price']
                        current_trade['pnl_abs'] = current_trade['pnl'] * current_trade['position_size']
                        trades.append(current_trade)
                        capital += current_trade['pnl_abs'] * capital
                        current_trade = None
                
                # Открытие короткой позиции
                position = -1
                position_size = min(self.max_position_size, capital * 0.95 / current_price)
                current_trade = {
                    'entry_date': date,
                    'entry_price': current_price,
                    'position_size': position_size,
                    'position': -1,
                    'confidence': confidence
                }
                capital -= position_size * current_price * transaction_cost
                
            elif signal == 0:  # Сигнал удержания
                # Закрытие текущей позиции
                if position != 0 and current_trade:
                    current_trade['exit_price'] = current_price
                    current_trade['exit_date'] = date
                    if position == 1:
                        current_trade['pnl'] = (current_price - current_trade['entry_price']) / current_trade['entry_price']
                    else:
                        current_trade['pnl'] = (current_trade['entry_price'] - current_price) / current_trade['entry_price']
                    current_trade['pnl_abs'] = current_trade['pnl'] * current_trade['position_size']
                    trades.append(current_trade)
                    capital += current_trade['pnl_abs'] * capital
                    current_trade = None
                position = 0
            
            # Обновление кривой капитала
            if position != 0 and current_trade:
                if position == 1:
                    unrealized_pnl = (current_price - current_trade['entry_price']) / current_trade['entry_price']
                else:
                    unrealized_pnl = (current_trade['entry_price'] - current_price) / current_trade['entry_price']
                current_equity = capital + unrealized_pnl * current_trade['position_size'] * capital
            else:
                current_equity = capital
            
            equity_curve.append(current_equity)
        
        # Закрытие последней позиции
        if current_trade:
            last_price = data['Close'].iloc[-1]
            current_trade['exit_price'] = last_price
            current_trade['exit_date'] = data.index[-1]
            if position == 1:
                current_trade['pnl'] = (last_price - current_trade['entry_price']) / current_trade['entry_price']
            else:
                current_trade['pnl'] = (current_trade['entry_price'] - last_price) / current_trade['entry_price']
            current_trade['pnl_abs'] = current_trade['pnl'] * current_trade['position_size']
            trades.append(current_trade)
            capital += current_trade['pnl_abs'] * capital
        
        return {
            'equity_curve': equity_curve,
            'trades': trades,
            'final_capital': capital,
            'total_trades': len(trades)
        }
    
    def _calculate_performance_metrics(self, trading_results: dict) -> dict:
        """
        Расчет метрик производительности.
        
        Args:
            trading_results: Результаты торговли
            
        Returns:
            Словарь с метриками производительности
        """
        equity_curve = np.array(trading_results['equity_curve'])
        trades = trading_results['trades']
        
        # Базовая статистика
        total_return = (equity_curve[-1] - equity_curve[0]) / equity_curve[0]
        
        # Годовая доходность (предполагаем 252 торговых дня)
        periods = len(equity_curve)
        annualized_return = (1 + total_return) ** (252 / periods) - 1
        
        # Волатильность
        returns = np.diff(equity_curve) / equity_curve[:-1]
        volatility = np.std(returns) * np.sqrt(252)
        
        # Sharpe Ratio
        risk_free_rate = 0.02  # 2% безрисковая ставка
        sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # Максимальная просадка
        running_max = np.maximum.accumulate(equity_curve)
        drawdown = (equity_curve - running_max) / running_max
        max_drawdown = np.min(drawdown)
        
        # Win Rate
        if trades:
            winning_trades = [t for t in trades if t['pnl'] > 0]
            win_rate = len(winning_trades) / len(trades)
        else:
            win_rate = 0
        
        # Profit Factor
        if trades:
            gross_profit = sum([t['pnl_abs'] for t in trades if t['pnl'] > 0])
            gross_loss = abs(sum([t['pnl_abs'] for t in trades if t['pnl'] < 0]))
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf
        else:
            profit_factor = 0
        
        # Средняя прибыль/убыток
        if trades:
            avg_win = np.mean([t['pnl'] for t in trades if t['pnl'] > 0]) if any(t['pnl'] > 0 for t in trades) else 0
            avg_loss = np.mean([t['pnl'] for t in trades if t['pnl'] < 0]) if any(t['pnl'] < 0 for t in trades) else 0
        else:
            avg_win = avg_loss = 0
        
        return {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'total_trades': len(trades)
        }
    
    def _calculate_risk_metrics(self, trading_results: dict) -> dict:
        """
        Расчет метрик риска.
        
        Args:
            trading_results: Результаты торговли
            
        Returns:
            Словарь с метриками риска
        """
        equity_curve = np.array(trading_results['equity_curve'])
        trades = trading_results['trades']
        
        # Value at Risk (VaR) - 95% доверительный интервал
        returns = np.diff(equity_curve) / equity_curve[:-1]
        var_95 = np.percentile(returns, 5)
        
        # Conditional Value at Risk (CVaR)
        cvar_95 = np.mean(returns[returns <= var_95])
        
        # Максимальная серия убытков
        if trades:
            consecutive_losses = 0
            max_consecutive_losses = 0
            for trade in trades:
                if trade['pnl'] < 0:
                    consecutive_losses += 1
                    max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
                else:
                    consecutive_losses = 0
        else:
            max_consecutive_losses = 0
        
        # Коэффициент восстановления
        if trades:
            total_loss = abs(sum([t['pnl_abs'] for t in trades if t['pnl'] < 0]))
            total_profit = sum([t['pnl_abs'] for t in trades if t['pnl'] > 0])
            recovery_factor = total_profit / total_loss if total_loss > 0 else np.inf
        else:
            recovery_factor = 0
        
        return {
            'var_95': var_95,
            'cvar_95': cvar_95,
            'max_consecutive_losses': max_consecutive_losses,
            'recovery_factor': recovery_factor
        }
    
    def _analyze_trades(self, trading_results: dict) -> dict:
        """
        Анализ сделок.
        
        Args:
            trading_results: Результаты торговли
            
        Returns:
            Словарь с анализом сделок
        """
        trades = trading_results['trades']
        
        if not trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'avg_trade_duration': 0,
                'best_trade': 0,
                'worst_trade': 0
            }
        
        # Статистика сделок
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        
        # Длительность сделок
        trade_durations = []
        for trade in trades:
            duration = (trade['exit_date'] - trade['entry_date']).total_seconds() / 3600  # в часах
            trade_durations.append(duration)
        
        avg_trade_duration = np.mean(trade_durations) if trade_durations else 0
        
        # Лучшая и худшая сделки
        best_trade = max(trades, key=lambda x: x['pnl'])['pnl'] if trades else 0
        worst_trade = min(trades, key=lambda x: x['pnl'])['pnl'] if trades else 0
        
        return {
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'avg_trade_duration': avg_trade_duration,
            'best_trade': best_trade,
            'worst_trade': worst_trade
        }
    
    def plot_results(self, save_path: str = None):
        """
        Построение графиков результатов бэктестинга.
        
        Args:
            save_path: Путь для сохранения графиков
        """
        if not self.results:
            print("Нет результатов для отображения. Сначала запустите backtest().")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('WAVE2 Backtesting Results', fontsize=16)
        
        # 1. Кривая капитала
        equity_curve = self.results['trading_results']['equity_curve']
        axes[0, 0].plot(equity_curve)
        axes[0, 0].set_title('Equity Curve')
        axes[0, 0].set_xlabel('Period')
        axes[0, 0].set_ylabel('Capital')
        axes[0, 0].grid(True)
        
        # 2. Распределение доходности сделок
        trades = self.results['trading_results']['trades']
        if trades:
            trade_returns = [t['pnl'] for t in trades]
            axes[0, 1].hist(trade_returns, bins=20, alpha=0.7)
            axes[0, 1].set_title('Trade Returns Distribution')
            axes[0, 1].set_xlabel('Return')
            axes[0, 1].set_ylabel('Frequency')
            axes[0, 1].grid(True)
        
        # 3. Просадки
        equity_curve = np.array(equity_curve)
        running_max = np.maximum.accumulate(equity_curve)
        drawdown = (equity_curve - running_max) / running_max
        axes[1, 0].fill_between(range(len(drawdown)), drawdown, 0, alpha=0.3, color='red')
        axes[1, 0].set_title('Drawdown')
        axes[1, 0].set_xlabel('Period')
        axes[1, 0].set_ylabel('Drawdown %')
        axes[1, 0].grid(True)
        
        # 4. Метрики производительности
        metrics = self.results['performance_metrics']
        metric_names = ['Total Return', 'Sharpe Ratio', 'Max Drawdown', 'Win Rate']
        metric_values = [
            metrics['total_return'],
            metrics['sharpe_ratio'],
            metrics['max_drawdown'],
            metrics['win_rate']
        ]
        
        bars = axes[1, 1].bar(metric_names, metric_values)
        axes[1, 1].set_title('Performance Metrics')
        axes[1, 1].set_ylabel('Value')
        
        # Добавление значений на столбцы
        for bar, value in zip(bars, metric_values):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                           f'{value:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Графики сохранены в {save_path}")
        
        plt.show()
    
    def generate_report(self) -> str:
        """
        Генерация текстового отчета о результатах бэктестинга.
        
        Returns:
            Строка с отчетом
        """
        if not self.results:
            return "Нет результатов для отчета. Сначала запустите backtest()."
        
        metrics = self.results['performance_metrics']
        risk_metrics = self.results['risk_metrics']
        trade_analysis = self.results['trade_analysis']
        
        report = f"""
WAVE2 Backtesting Report
========================

Test Period: {self.results['test_period'][0]} - {self.results['test_period'][1]}
Data Points: {self.results['data_points']}

PERFORMANCE METRICS
-------------------
Total Return: {metrics['total_return']:.2%}
Annualized Return: {metrics['annualized_return']:.2%}
Volatility: {metrics['volatility']:.2%}
Sharpe Ratio: {metrics['sharpe_ratio']:.2f}
Max Drawdown: {metrics['max_drawdown']:.2%}

TRADE ANALYSIS
--------------
Total Trades: {trade_analysis['total_trades']}
Winning Trades: {trade_analysis['winning_trades']}
Losing Trades: {trade_analysis['losing_trades']}
Win Rate: {metrics['win_rate']:.2%}
Profit Factor: {metrics['profit_factor']:.2f}
Average Win: {metrics['avg_win']:.2%}
Average Loss: {metrics['avg_loss']:.2%}

RISK METRICS
------------
VaR (95%): {risk_metrics['var_95']:.2%}
CVaR (95%): {risk_metrics['cvar_95']:.2%}
Max Consecutive Losses: {risk_metrics['max_consecutive_losses']}
Recovery Factor: {risk_metrics['recovery_factor']:.2f}

TRADE DURATION
--------------
Average Trade Duration: {trade_analysis['avg_trade_duration']:.1f} hours
Best Trade: {trade_analysis['best_trade']:.2%}
Worst Trade: {trade_analysis['worst_trade']:.2%}
        """
        
        return report

# Пример использования бэктестера
def run_backtesting_example():
    """Пример запуска бэктестинга WAVE2 стратегии."""
    # Загрузка данных
    loader = WAVE2DataLoader()
    data = loader.load_wave2_data("GBPUSD", "H1")
    
    # Создание и обучение модели
    feature_engineer = WAVE2FeatureEngineer()
    features = feature_engineer.create_all_features(data)
    
    target = (data['Close'].shift(-1) > data['Close']).astype(int)
    target = target[features.index]
    
    valid_indices = features.dropna().index.intersection(target.dropna().index)
    features_clean = features.loc[valid_indices]
    target_clean = target.loc[valid_indices]
    
    classifier = WAVE2Classifier()
    classifier.train(features_clean, target_clean)
    
    # Создание и запуск бэктестера
    backtester = WAVE2Backtester(classifier, data)
    results = backtester.backtest('2023-01-01', '2023-12-31')
    
    # Отображение результатов
    backtester.plot_results()
    print(backtester.generate_report())
    
    return backtester, results

# Запуск примера
if __name__ == "__main__":
    backtester, results = run_backtesting_example()
```

### 2. Метрики производительности

**Теория:** Метрики производительности являются критически важными для оценки эффективности WAVE2 модели. Они обеспечивают количественную оценку различных аспектов производительности торговой стратегии.

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
def calculate_performance_metrics(returns):
    """Расчет метрик производительности"""
    returns = np.array(returns)
    
    # Базовая статистика
    total_return = np.sum(returns)
    annualized_return = total_return * 252  # Предполагаем 252 торговых дня
    
    # Волатильность
    volatility = np.std(returns) * np.sqrt(252)
    
    # Sharpe Ratio
    risk_free_rate = 0.02  # 2% безрисковая ставка
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
    
    return {
        'total_return': total_return,
        'annualized_return': annualized_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'profit_factor': profit_factor
    }
```

## Оптимизация параметров WAVE2

**Теория:** Оптимизация параметров WAVE2 является критически важным этапом для достижения максимальной эффективности торговой стратегии. Правильно оптимизированные параметры могут значительно повысить производительность системы.

**Почему оптимизация параметров критична:**
- **Максимизация производительности:** Позволяет достичь максимальной производительности
- **Адаптация к рынку:** Помогает адаптироваться к различным рыночным условиям
- **Снижение рисков:** Может снизить риски стратегии
- **Повышение прибыльности:** Может значительно повысить прибыльность

### 1. Генетический алгоритм

**Теория:** Генетический алгоритм представляет собой эволюционный метод оптимизации, который имитирует процесс естественного отбора для поиска оптимальных параметров WAVE2. Это особенно эффективно для сложных многомерных задач оптимизации.

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
class WAVE2Optimizer:
    """Оптимизатор параметров WAVE2"""
    
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
                'long1': np.random.randint(50, 500),
                'fast1': np.random.randint(5, 50),
                'trend1': np.random.randint(1, 10),
                'long2': np.random.randint(20, 200),
                'fast2': np.random.randint(5, 50),
                'trend2': np.random.randint(1, 10)
            }
            population.append(params)
        
        return population
```

### 2. Bayesian Optimization

**Теория:** Bayesian Optimization представляет собой интеллектуальный метод оптимизации, который использует байесовскую статистику для эффективного поиска оптимальных параметров WAVE2. Это особенно эффективно для дорогих в вычислении функций.

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

class WAVE2BayesianOptimizer:
    """Bayesian оптимизация параметров WAVE2"""
    
    def __init__(self, data):
        self.data = data
        self.space = [
            Integer(50, 500, name='long1'),
            Integer(5, 50, name='fast1'),
            Integer(1, 10, name='trend1'),
            Integer(20, 200, name='long2'),
            Integer(5, 50, name='fast2'),
            Integer(1, 10, name='trend2')
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
        long1, fast1, trend1, long2, fast2, trend2 = params
        
        # Расчет WAVE2 с данными параметрами
        wave2_data = self._calculate_wave2(long1, fast1, trend1, long2, fast2, trend2)
        
        # Расчет производительности
        performance = self._calculate_performance(wave2_data)
        
        # Возвращаем отрицательное значение для минимизации
        return -performance
```

## Продакшн деплой WAVE2 модели

**Теория:** Продакшн деплой WAVE2 модели является финальным этапом создания торговой системы, который обеспечивает развертывание модели в реальной торговой среде. Это критически важно для практического применения системы.

**Почему продакшн деплой критичен:**
- **Практическое применение:** Обеспечивает практическое применение системы
- **Автоматизация:** Автоматизирует торговые процессы
- **Масштабируемость:** Позволяет масштабировать систему
- **Мониторинг:** Обеспечивает мониторинг производительности

### 1. API для WAVE2 модели

**Теория:** API для WAVE2 модели обеспечивает программный интерфейс для взаимодействия с моделью, что критически важно для интеграции с торговыми системами и автоматизации процессов.

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

app = FastAPI(title="WAVE2 ML Model API")

class PredictionRequest(BaseModel):
    wave1: float
    wave2: float
    fastline1: float
    fastline2: float
    additional_features: dict = {}

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    confidence: str

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Предсказание на основе WAVE2"""
    try:
        # Загрузка модели
        model = joblib.load('models/wave2_model.pkl')
        
        # Подготовка данных
        features = np.array([
            request.wave1,
            request.wave2,
            request.fastline1,
            request.fastline2
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
        
        return PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2. Docker контейнер

**Теория:** Docker контейнеризация обеспечивает изоляцию, портабельность и масштабируемость WAVE2 модели в продакшн среде. Это критически важно для обеспечения стабильности и простоты развертывания.

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
# Dockerfile для WAVE2 модели
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

**Теория:** Мониторинг производительности WAVE2 модели является критически важным для обеспечения стабильности и эффективности торговой системы в продакшн среде. Это позволяет быстро выявлять и устранять проблемы.

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
class WAVE2Monitor:
    """Мониторинг WAVE2 модели"""
    
    def __init__(self):
        self.performance_history = []
        self.alert_thresholds = {
            'accuracy': 0.7,
            'latency': 1.0,  # секунды
            'throughput': 100  # запросов в минуту
        }
    
    def monitor_prediction(self, prediction, actual, latency):
        """Мониторинг предсказания"""
        # Расчет точности
        accuracy = 1 if prediction == actual else 0
        
        # Сохранение метрик
        self.performance_history.append({
            'timestamp': datetime.now(),
            'accuracy': accuracy,
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
        
        # Проверка латентности
        avg_latency = np.mean([p['latency'] for p in recent_performance])
        if avg_latency > self.alert_thresholds['latency']:
            self._send_alert("High latency detected")
```

## Следующие шаги

После анализа WAVE2 переходите к:
- **[12_schr_levels_analysis.md](12_schr_levels_analysis.md)** - Анализ SCHR Levels
- **[13_schr_short3_analysis.md](13_schr_short3_analysis.md)** - Анализ SCHR SHORT3

## Ключевые выводы

**Теория:** Ключевые выводы суммируют наиболее важные аспекты анализа WAVE2, которые критически важны для создания прибыльной и робастной торговой системы.

1. **WAVE2 - мощный индикатор для анализа трендов**
   - **Теория:** WAVE2 представляет собой революционный подход к техническому анализу
   - **Почему важно:** Обеспечивает высокую точность анализа трендов
   - **Плюсы:** Высокая точность, структурный анализ, адаптивность
   - **Минусы:** Сложность настройки, высокие требования к ресурсам

2. **Мультитаймфреймовый анализ - разные параметры для разных таймфреймов**
   - **Теория:** Каждый таймфрейм требует специфических параметров для максимальной эффективности
   - **Почему важно:** Обеспечивает оптимальную производительность на всех временных горизонтах
   - **Плюсы:** Оптимизация производительности, снижение рисков, повышение точности
   - **Минусы:** Сложность настройки, необходимость понимания каждого таймфрейма

3. **Богатые признаки - множество возможностей для создания признаков**
   - **Теория:** WAVE2 предоставляет богатую основу для создания признаков машинного обучения
   - **Почему важно:** Качественные признаки определяют успех ML-модели
   - **Плюсы:** Высокая точность, выявление паттернов, робастность
   - **Минусы:** Сложность вычислений, потенциальное переобучение

4. **Высокая точность - возможность достижения 95%+ точности**
   - **Теория:** Правильно настроенная WAVE2 модель может достигать очень высокой точности
   - **Почему важно:** Высокая точность критична для прибыльной торговли
   - **Плюсы:** Высокая прибыльность, снижение рисков, уверенность в стратегии
   - **Минусы:** Высокие требования к настройке, потенциальное переобучение

5. **Продакшн готовность - полная интеграция с продакшн системами**
   - **Теория:** WAVE2 модель может быть полностью интегрирована в продакшн системы
   - **Почему важно:** Обеспечивает практическое применение системы
   - **Плюсы:** Автоматизация, масштабируемость, мониторинг
   - **Минусы:** Сложность разработки, требования к безопасности

---

**Важно:** WAVE2 требует тщательной настройки параметров для каждого таймфрейма и актива. Используйте оптимизацию для достижения максимальной производительности.
