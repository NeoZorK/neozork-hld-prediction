# 11. Анализ индикатора WAVE2 - create высокоточной ML-модели

**Goal:** Максимально использовать индикатор WAVE2 for создания робастной and прибыльной ML-модели with точностью более 95%.

## Что такое WAVE2?

**Теория:** WAVE2 представляет собой революционный подход к техническому анализу, основанный on теории волн Эллиотта and современных методах цифровой обработки сигналов. Это not просто индикатор, а комплексная система Analysis рыночной структуры, которая выявляет скрытые паттерны and тренды.

### Определение and принцип работы

**Теория:** WAVE2 основан on принципе двойной волновой системы, где каждая волна анализирует различные аспекты рыночной динамики. Это позволяет получать более точные and надежные сигналы on сравнению with традиционными индикаторами.

**WAVE2** - это продвинутый трендовый индикатор, который использует двойную волновую system for генерации торговых сигналов. in отличие from простых indicators, WAVE2 анализирует структуру рынка, а not просто сглаживает цену.

**Почему WAVE2 превосходит традиционные индикаторы:**
- **Структурный анализ:** Анализирует структуру рынка, а not просто сглаживает цену
- **Двойная волновая система:** Использует две волны for более точного Analysis
- **Адаптивность:** Адаптируется к различным рыночным условиям
- **Точность:** Обеспечивает более высокую точность Predictions

**Плюсы:**
- Высокая точность сигналов
- Адаптивность к рыночным условиям
- Структурный Market Analysis
- Меньше ложных сигналов

**Минусы:**
- Сложность settings параметров
- Высокие требования к вычислительным ресурсам
- Необходимость глубокого понимания теории

### Ключевые особенности WAVE2

**Теория:** Ключевые особенности WAVE2 определяют его уникальные возможности for Analysis финансовых рынков. Каждый parameter имеет теоретическое обоснование and практическое применение for различных рыночных условий.

**Почему эти особенности критичны:**
- **Двойная волновая система:** Обеспечивает более точный анализ трендов
- **Адаптивные parameters:** Позволяют настраивать индикатор под различные условия
- **МультиTimeframesый анализ:** Обеспечивает анализ on разных временных горизонтах
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
 Analysisтор WAVE2 индикатора for создания высокоточной ML-модели.

 WAVE2 - это продвинутый трендовый индикатор, который использует двойную волновую system
 for генерации торговых сигналов. in отличие from простых indicators, WAVE2 анализирует
 структуру рынка, а not просто сглаживает цену.

 Теория: WAVE2 основан on принципе двойной волновой системы, где каждая волна анализирует
 различные аспекты рыночной динамики. Это позволяет получать более точные and надежные
 сигналы on сравнению with традиционными индикаторами.
 """

 def __init__(self):
 """
 Инициализация WAVE2 Analysisтора with оптимальными параметрами.

 parameters подобраны on basis многолетнего Analysis различных рыночных условий
 and обеспечивают максимальную эффективность for большинства торговых инструментов.
 """
 self.parameters = {
 'long1': 339, # Первый длинный период - основной трендовый компонент
 'fast1': 10, # Первый быстрый период - быстрый отклик on изменения
 'trend1': 2, # Первый трендовый период - определение тренда
 'tr1': 'fast', # Первое торговое правило - логика генерации сигналов
 'long2': 22, # Второй длинный период - дополнительный трендовый компонент
 'fast2': 11, # Второй быстрый период - быстрый отклик второй волны
 'trend2': 4, # Второй трендовый период - определение тренда второй волны
 'tr2': 'fast', # Второе торговое правило - логика второй волны
 'global_tr': 'prime', # Глобальное торговое правило - общая логика
 'sma_period': 22 # Период SMA - сглаживание for фильтрации шума
 }

 # Валидация параметров
 self._validate_parameters()

 def _validate_parameters(self):
 """Валидация параметров WAVE2 for обеспечения корректной работы."""
 params = self.parameters

 # check логических ограничений
 assert params['long1'] > params['fast1'], "long1 должен быть больше fast1"
 assert params['long2'] > params['fast2'], "long2 должен быть больше fast2"
 assert params['long1'] > params['long2'], "long1 должен быть больше long2"
 assert params['fast1'] > 0 and params['fast2'] > 0, "Быстрые периоды должны быть положительными"
 assert params['trend1'] > 0 and params['trend2'] > 0, "Трендовые периоды должны быть положительными"

 print("✓ parameters WAVE2 валидированы успешно")

 def get_parameters(self) -> Dict:
 """Получение текущих параметров WAVE2."""
 return self.parameters.copy()

 def update_parameters(self, new_params: Dict):
 """update параметров WAVE2 with валидацией."""
 self.parameters.update(new_params)
 self._validate_parameters()
 print("✓ parameters WAVE2 обновлены")
```

### Structure данных WAVE2

**Теория:** Structure данных WAVE2 представляет собой комплексную system признаков, которая обеспечивает полный анализ рыночной динамики. Каждый компонент имеет специфическое назначение and вносит вклад in общую точность Predictions.

**Почему Structure данных критична:**
- **Полнота Analysis:** Обеспечивает всесторонний анализ рыночной ситуации
- **Точность сигналов:** Каждый компонент повышает точность Predictions
- **Гибкость:** Позволяет адаптироваться к различным рыночным условиям
- **integration with ML:** Оптимизирована for машинного обучения

```python
# Основные колонки WAVE2 in parquet файлах
WAVE2_columns = {
 # Основные волны
 'wave1': 'Первая волна - основной трендовый компонент',
 'wave2': 'Вторая волна - дополнительный трендовый компонент',
 'fastline1': 'Быстрая линия первой волны',
 'fastline2': 'Быстрая линия второй волны',

 # Торговые сигналы
 'Wave1': 'Сигнал первой волны (-1, 0, 1)',
 'Wave2': 'Сигнал второй волны (-1, 0, 1)',
 '_signal': 'Финальный торговый сигнал',
 '_Direction': 'Направление сигнала',
 '_Lastsignal': 'Последний подтвержденный сигнал',

 # Визуальные элементы
 '_Plot_Color': 'Цвет for отображения',
 '_Plot_Wave': 'Значение волны for отображения',
 '_Plot_FastLine': 'Значение быстрой линии for отображения',

 # Дополнительные components
 'ecore1': 'Первый экор (экспоненциальное ядро)',
 'ecore2': 'Второй экор (экспоненциальное ядро)'
}

class WAVE2dataLoader:
 """
 Загрузчик данных WAVE2 из различных источников.

 Поддерживает загрузку из parquet файлов, CSV файлов and прямую генерацию
 WAVE2 индикатора on basis OHLCV данных.
 """

 def __init__(self, data_path: str = "data/indicators/parquet/"):
 """
 Инициализация загрузчика данных WAVE2.

 Args:
 data_path: Path to folder with data WAVE2
 """
 self.data_path = data_path
 self.required_columns = ['wave1', 'wave2', 'fastline1', 'fastline2',
 'Wave1', 'Wave2', '_signal']

 def load_wave2_data(self, symbol: str = "GBPUSD", Timeframe: str = "H1") -> pd.dataFrame:
 """
 Loading data WAVE2 из parquet файла.

 Args:
 symbol: Trading symbol (например, GBPUSD)
 Timeframe: Timeframe (M1, M5, H1, H4, D1)

 Returns:
 dataFrame with data WAVE2
 """
 try:
 file_path = f"{self.data_path}{symbol}_{Timeframe}_WAVE2.parquet"
 data = pd.read_parquet(file_path)

 # check наличия required columns
 missing_columns = [col for col in self.required_columns if col not in data.columns]
 if missing_columns:
 raise ValueError(f"Отсутствуют необходимые колонки: {missing_columns}")

 # installation индекса времени
 if 'datetime' in data.columns:
 data['datetime'] = pd.to_datetime(data['datetime'])
 data.set_index('datetime', inplace=True)

 print(f"✓ Загружены data WAVE2: {symbol} {Timeframe}, {len(data)} записей")
 return data

 except FileNotfoundError:
 print(f"⚠️ File not found: {file_path}")
 print("Создаем синтетические data WAVE2 for демонстрации...")
 return self._generate_synthetic_wave2_data()

 def _generate_synthetic_wave2_data(self, n_periods: int = 1000) -> pd.dataFrame:
 """
 Генерация синтетических данных WAVE2 for демонстрации.

 Args:
 n_periods: Количество periods for генерации

 Returns:
 dataFrame with синтетическими данными WAVE2
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
 _signal = np.where((Wave1 == Wave2) & (Wave1 != 0), Wave1, 0)

 # create dataFrame
 data = pd.dataFrame({
 'Close': prices,
 'wave1': wave1,
 'wave2': wave2,
 'fastline1': fastline1,
 'fastline2': fastline2,
 'Wave1': Wave1,
 'Wave2': Wave2,
 '_signal': _signal,
 '_Direction': np.where(_signal > 0, 1, np.where(_signal < 0, -1, 0)),
 '_Lastsignal': _signal,
 'ecore1': wave1 * 0.9,
 'ecore2': wave2 * 0.9
 })

 # create временного индекса
 data.index = pd.date_range(start='2023-01-01', periods=n_periods, freq='H')

 print(f"✓ Созданы синтетические data WAVE2: {len(data)} записей")
 return data

 def validate_wave2_data(self, data: pd.dataFrame) -> bool:
 """
 Валидация данных WAVE2 on корректность.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 True если data корректны, False иначе
 """
 try:
 # check наличия columns
 missing_columns = [col for col in self.required_columns if col not in data.columns]
 if missing_columns:
 print(f"❌ Отсутствуют колонки: {missing_columns}")
 return False

 # check on NaN значения
 nan_columns = data[self.required_columns].isnull().any()
 if nan_columns.any():
 print(f"❌ foundы NaN значения in колонках: {nan_columns[nan_columns].index.toList()}")
 return False

 # check диапазонов сигналов
 signal_columns = ['Wave1', 'Wave2', '_signal']
 for col in signal_columns:
 unique_values = data[col].unique()
 if not all(val in [-1, 0, 1] for val in unique_values if not pd.isna(val)):
 print(f"❌ Некорректные значения in {col}: {unique_values}")
 return False

 print("✓ data WAVE2 валидированы успешно")
 return True

 except Exception as e:
 print(f"❌ Ошибка валидации: {e}")
 return False

# example использования загрузчика данных
def load_and_validate_wave2_data():
 """example загрузки and валидации данных WAVE2."""
 loader = WAVE2dataLoader()

 # Loading data
 data = loader.load_wave2_data("GBPUSD", "H1")

 # Валидация данных
 is_valid = loader.validate_wave2_data(data)

 if is_valid:
 print(f"✓ data загружены and валидированы: {data.shape}")
 print(f"✓ Колонки: {List(data.columns)}")
 print(f"✓ Период: {data.index[0]} - {data.index[-1]}")
 return data
 else:
 print("❌ data not прошли валидацию")
 return None

# Launch примера
if __name__ == "__main__":
 wave2_data = load_and_validate_wave2_data()
```

## Анализ WAVE2 on Timeframeм

**Теория:** Анализ WAVE2 on различным Timeframeм является критически важным for создания робастной торговой системы. Каждый Timeframe имеет свои особенности and требует специфических параметров for достижения максимальной эффективности.

**Почему мультиTimeframesый анализ критичен:**
- **Различные рыночные циклы:** Каждый Timeframe отражает разные рыночные циклы
- **Оптимизация параметров:** Разные parameters for разных временных горизонтов
- **Снижение рисков:** Диверсификация on Timeframeм снижает общие риски
- **Повышение точности:** Комбинирование сигналов with разных Timeframes

### M1 (1 minutesа) - Скальпинг

**Теория:** M1 Timeframe предназначен for скальпинга and требует максимально быстрой реакции on изменения рынка. parameters WAVE2 for M1 оптимизированы for выявления краткосрочных возможностей.

**Почему M1 анализ важен:**
- **Высокая частота сигналов:** Обеспечивает множество торговых возможностей
- **Быстрая реакция:** Позволяет быстро реагировать on изменения рынка
- **Высокий потенциал прибыли:** Множество сделок может дать высокую прибыль
- **Требует точности:** Высокие требования к точности сигналов

**Плюсы:**
- Высокая частота торговых возможностей
- Быстрая реакция on изменения
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
 Анализ WAVE2 on 1-minutesном Timeframeе for скальпинга.

 M1 Timeframe предназначен for скальпинга and требует максимально быстрой реакции
 on изменения рынка. parameters WAVE2 for M1 оптимизированы for выявления
 краткосрочных возможностей with минимальной задержкой.

 Теория: M1 анализ основан on принципе быстрого реагирования on микро-изменения
 рынка, что требует специальных алгоритмов for фильтрации шума and выявления
 значимых сигналов.
 """

 def __init__(self):
 """Инициализация Analysisтора M1 with оптимизированными параметрами."""
 self.Timeframe = 'M1'
 self.optimal_params = {
 'long1': 50, # Более короткий период for M1 - быстрый отклик
 'fast1': 5, # Очень быстрый отклик - минимальная задержка
 'trend1': 1, # Минимальный трендовый период - мгновенная реакция
 'long2': 15, # Короткий второй период - дополнительная фильтрация
 'fast2': 3, # Очень быстрая вторая волна - быстрая адаптация
 'trend2': 1 # Минимальный тренд - максимальная чувствительность
 }

 # Пороги for M1 Analysis
 self.thresholds = {
 'min_volatility': 0.0001, # Минимальная волатильность for сигнала
 'max_spread': 0.0005, # Максимальный спред for trading
 'min_trend_strength': 0.001, # Минимальная сила тренда
 'max_noise_level': 0.0002 # Максимальный уровень шума
 }

 def analyze_m1_features(self, data: pd.dataFrame) -> Dict:
 """
 Анализ признаков for M1 Timeframe.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with приsignми for M1 Analysis
 """
 features = {}

 # Микро-тренды - анализ краткосрочных трендов
 features['micro_trend'] = self._detect_micro_trend(data)

 # Быстрые развороты - детекция мгновенных разворотов
 features['quick_reversal'] = self._detect_quick_reversal(data)

 # Скальпинг сигналы - специальные сигналы for скальпинга
 features['scalping_signal'] = self._detect_scalping_signal(data)

 # Микро-волатильность - анализ краткосрочной волатильности
 features['micro_volatility'] = self._calculate_micro_volatility(data)

 # Микро-моментум - анализ краткосрочного моментума
 features['micro_momentum'] = self._calculate_micro_momentum(data)

 # Быстрые пересечения - анализ пересечений линий
 features['fast_crossovers'] = self._detect_fast_crossovers(data)

 return features

 def _detect_micro_trend(self, data: pd.dataFrame) -> Dict:
 """
 Детекция микро-трендов for M1 Analysis.

 Микро-тренды представляют собой краткосрочные движения цены,
 которые могут быть использованы for скальпинга.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о микро-трендах
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

 def _detect_quick_reversal(self, data: pd.dataFrame) -> Dict:
 """
 Детекция быстрых разворотов for M1 Analysis.

 Быстрые развороты представляют собой мгновенные изменения направления
 движения цены, которые критически важны for скальпинга.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о быстрых разворотах
 """
 wave1 = data['wave1']
 fastline1 = data['fastline1']

 # Изменение направления wave1
 wave1_direction_change = (wave1.diff() > 0) != (wave1.diff().shift(1) > 0)

 # Изменение направления fastline1
 fastline1_direction_change = (fastline1.diff() > 0) != (fastline1.diff().shift(1) > 0)

 # simultaneouslyе изменение направления обеих линий
 simultaneous_reversal = wave1_direction_change & fastline1_direction_change

 # Сила разворота - величина изменения
 reversal_strength = abs(wave1.diff()) + abs(fastline1.diff())

 # Быстрый разворот - разворот with высокой силой
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

 def _detect_scalping_signal(self, data: pd.dataFrame) -> Dict:
 """
 Детекция скальпинг сигналов for M1 Analysis.

 Скальпинг сигналы представляют собой специальные паттерны,
 которые оптимальны for краткосрочной торговли.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о скальпинг сигналах
 """
 wave1 = data['wave1']
 fastline1 = data['fastline1']
 wave2 = data['wave2']
 fastline2 = data['fastline2']

 # Согласованность сигналов обеих волн
 signal_consistency = (data['Wave1'] == data['Wave2']) & (data['Wave1'] != 0)

 # Быстрое пересечение - пересечение in течение короткого времени
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

 def _calculate_micro_volatility(self, data: pd.dataFrame) -> Dict:
 """
 Расчет микро-волатильности for M1 Analysis.

 Микро-волатильность представляет собой краткосрочные колебания цены,
 которые критически важны for управления рисками при скальпинге.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о микро-волатильности
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

 def _calculate_micro_momentum(self, data: pd.dataFrame) -> Dict:
 """
 Расчет микро-моментума for M1 Analysis.

 Микро-моментум представляет собой скорость изменения цены
 on краткосрочных интервалах.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о микро-моментуме
 """
 wave1 = data['wave1']
 fastline1 = data['fastline1']

 # Моментум wave1
 wave1_momentum = wave1.diff(3) # 3-периодный моментум

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

 def _detect_fast_crossovers(self, data: pd.dataFrame) -> Dict:
 """
 Детекция быстрых пересечений for M1 Analysis.

 Быстрые пересечения представляют собой моменты, когда
 волны пересекают свои быстрые линии.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о быстрых пересечениях
 """
 wave1 = data['wave1']
 fastline1 = data['fastline1']
 wave2 = data['wave2']
 fastline2 = data['fastline2']

 # Пересечения wave1 and fastline1
 wave1_cross_up = (wave1 > fastline1) & (wave1.shift(1) <= fastline1.shift(1))
 wave1_cross_down = (wave1 < fastline1) & (wave1.shift(1) >= fastline1.shift(1))

 # Пересечения wave2 and fastline2
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

 def generate_m1_signals(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 Генерация торговых сигналов for M1 Timeframe.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 dataFrame with торговыми сигналами
 """
 # Анализ признаков
 features = self.analyze_m1_features(data)

 # create dataFrame with сигналами
 signals = pd.dataFrame(index=data.index)

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

 # Фильтрация on волатильности
 high_vol = features['micro_volatility']['high_volatility']
 signals['filtered_signal'] = np.where(
 high_vol,
 signals['combined_signal'],
 0
 )

 return signals

# example использования M1 Analysis
def run_m1_Analysis_example():
 """example Launchа M1 Analysis WAVE2."""
 # Loading data
 loader = WAVE2dataLoader()
 data = loader.load_wave2_data("GBPUSD", "M1")

 # create Analysisтора M1
 m1_analyzer = WAVE2M1Analysis()

 # Генерация сигналов
 signals = m1_analyzer.generate_m1_signals(data)

 # Анализ результатов
 print(f"✓ Сгенерировано {len(signals)} сигналов")
 print(f"✓ Сигналов on покупку: {(signals['filtered_signal'] > 0).sum()}")
 print(f"✓ Сигналов on продажу: {(signals['filtered_signal'] < 0).sum()}")

 return signals

# Launch примера
if __name__ == "__main__":
 m1_signals = run_m1_Analysis_example()
```

### M5 (5 minutes) - Краткосрочная торговля

**Теория:** M5 Timeframe представляет собой оптимальный баланс между частотой сигналов and их качеством. Это наиболее популярный Timeframe for краткосрочной торговли, обеспечивающий хорошее соотношение возможностей and рисков.

**Почему M5 анализ важен:**
- **Оптимальный баланс:** Хорошее соотношение частоты and качества сигналов
- **Снижение шума:** Меньше рыночного шума on сравнению with M1
- **Достаточная частота:** Достаточно сигналов for активной торговли
- **Стабильность:** Более стабильные сигналы

**Плюсы:**
- Оптимальный баланс частоты and качества
- Меньше рыночного шума
- Стабильные сигналы
- Подходит for большинства стратегий

**Минусы:**
- Меньше торговых возможностей чем M1
- Требует больше времени for Analysis
- Потенциальные задержки in сигналах

```python
class WAVE2M5Analysis:
 """
 Анализ WAVE2 on 5-minutesном Timeframeе for краткосрочной торговли.

 M5 Timeframe представляет собой оптимальный баланс между частотой сигналов
 and их качеством. Это наиболее популярный Timeframe for краткосрочной торговли,
 обеспечивающий хорошее соотношение возможностей and рисков.

 Теория: M5 анализ основан on принципе оптимального баланса между скоростью
 реакции and качеством сигналов, что позволяет эффективно торговать краткосрочные
 движения with минимальным риском.
 """

 def __init__(self):
 """Инициализация Analysisтора M5 with оптимизированными параметрами."""
 self.Timeframe = 'M5'
 self.optimal_params = {
 'long1': 100, # Оптимальный for M5 - баланс скорости and стабильности
 'fast1': 10, # Быстрый отклик - достаточная чувствительность
 'trend1': 2, # Короткий тренд - быстрая адаптация
 'long2': 30, # Средний второй период - дополнительная фильтрация
 'fast2': 8, # Быстрая вторая волна - быстрая реакция
 'trend2': 2 # Короткий тренд - оптимальная чувствительность
 }

 # Пороги for M5 Analysis
 self.thresholds = {
 'min_volatility': 0.0005, # Минимальная волатильность for сигнала
 'max_spread': 0.001, # Максимальный спред for trading
 'min_trend_strength': 0.002, # Минимальная сила тренда
 'max_noise_level': 0.0005, # Максимальный уровень шума
 'min_pattern_strength': 0.001 # Минимальная сила паттерна
 }

 def analyze_m5_features(self, data: pd.dataFrame) -> Dict:
 """
 Анализ признаков for M5 Timeframe.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with приsignми for M5 Analysis
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

 # Консолидация - анализ periods консолидации
 features['consolidation'] = self._detect_consolidation(data)

 return features

 def _detect_short_pattern(self, data: pd.dataFrame) -> Dict:
 """
 Детекция краткосрочных паттернов for M5 Analysis.

 Краткосрочные паттерны представляют собой повторяющиеся структуры
 in движении цены, которые могут быть использованы for прогнозирования.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о краткосрочных паттернах
 """
 wave1 = data['wave1']
 fastline1 = data['fastline1']
 wave2 = data['wave2']
 fastline2 = data['fastline2']

 # Паттерн "Двойное дно" - два минимума on близком уровне
 double_bottom = self._detect_double_bottom(wave1, window=10)

 # Паттерн "Двойная вершина" - два максимума on близком уровне
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

 # Фильтруем минимумы on силе
 strong_mins = local_mins & (series < series.rolling(20).quantile(0.3))

 # Ищем пары близких минимумов
 double_bottom = pd.Series(False, index=series.index)
 min_indices = series[strong_mins].index

 for i in range(len(min_indices) - 1):
 if min_indices[i+1] - min_indices[i] <= window * 2:
 # checking близость значений
 if abs(series[min_indices[i]] - series[min_indices[i+1]]) < series.std() * 0.1:
 double_bottom[min_indices[i]:min_indices[i+1]] = True

 return double_bottom

 def _detect_double_top(self, series: pd.Series, window: int = 10) -> pd.Series:
 """Детекция паттерна 'Двойная вершина'."""
 # Находим локальные максимумы
 local_maxs = series.rolling(window, center=True).max() == series

 # Фильтруем максимумы on силе
 strong_maxs = local_maxs & (series > series.rolling(20).quantile(0.7))

 # Ищем пары близких максимумов
 double_top = pd.Series(False, index=series.index)
 max_indices = series[strong_maxs].index

 for i in range(len(max_indices) - 1):
 if max_indices[i+1] - max_indices[i] <= window * 2:
 # checking близость значений
 if abs(series[max_indices[i]] - series[max_indices[i+1]]) < series.std() * 0.1:
 double_top[max_indices[i]:max_indices[i+1]] = True

 return double_top

 def _detect_triangle(self, wave1: pd.Series, fastline1: pd.Series, window: int = 15) -> pd.Series:
 """Детекция паттерна 'Треугольник'."""
 # Скользящие максимумы and минимумы
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

 # Флаг - импульс with последующей консолидацией
 flag = impulse.shift(window) & consolidation

 return flag

 def _detect_pennant(self, wave1: pd.Series, fastline1: pd.Series, window: int = 12) -> pd.Series:
 """Детекция паттерна 'Вымпел'."""
 # Сходящиеся волны
 wave_convergence = abs(wave1 - fastline1).rolling(window).mean()
 convergence_trend = wave_convergence.diff(window) < 0

 # Снижение волатильности
 volatility_reduction = wave1.rolling(window).std() < wave1.rolling(window * 2).std() * 0.7

 # Вымпел - сходимость with снижением волатильности
 pennant = convergence_trend & volatility_reduction

 return pennant

 def _detect_quick_impulse(self, data: pd.dataFrame) -> Dict:
 """
 Детекция быстрых импульсов for M5 Analysis.

 Быстрые импульсы представляют собой резкие движения цены,
 которые могут быть использованы for краткосрочной торговли.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о быстрых импульсах
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

 def _calculate_short_volatility(self, data: pd.dataFrame) -> Dict:
 """
 Расчет краткосрочной волатильности for M5 Analysis.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о краткосрочной волатильности
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

 def _detect_short_trend(self, data: pd.dataFrame) -> Dict:
 """Детекция краткосрочных трендов for M5 Analysis."""
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

 def _detect_impulse_movement(self, data: pd.dataFrame) -> Dict:
 """Детекция импульсных движений for M5 Analysis."""
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

 def _detect_consolidation(self, data: pd.dataFrame) -> Dict:
 """Детекция консолидации for M5 Analysis."""
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

 def _calculate_pattern_strength(self, data: pd.dataFrame) -> pd.Series:
 """Расчет силы паттернов."""
 wave1 = data['wave1']
 fastline1 = data['fastline1']

 # Сила паттерна - стабильность соотношения
 pattern_strength = 1 / (abs(wave1 - fastline1) / (abs(fastline1) + 1e-8) + 1e-8)

 return pattern_strength

 def _determine_pattern_direction(self, data: pd.dataFrame) -> pd.Series:
 """Определение направления паттернов."""
 wave1 = data['wave1']
 fastline1 = data['fastline1']

 # Направление паттерна
 pattern_direction = np.where(wave1 > fastline1, 1, -1)

 return pattern_direction

 def generate_m5_signals(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 Генерация торговых сигналов for M5 Timeframe.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 dataFrame with торговыми сигналами
 """
 # Анализ признаков
 features = self.analyze_m5_features(data)

 # create dataFrame with сигналами
 signals = pd.dataFrame(index=data.index)

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

 # Фильтрация on волатильности
 normal_vol = ~features['short_volatility']['high_volatility']
 signals['filtered_signal'] = np.where(
 normal_vol,
 signals['combined_signal'],
 0
 )

 return signals

# example использования M5 Analysis
def run_m5_Analysis_example():
 """example Launchа M5 Analysis WAVE2."""
 # Loading data
 loader = WAVE2dataLoader()
 data = loader.load_wave2_data("GBPUSD", "M5")

 # create Analysisтора M5
 m5_analyzer = WAVE2M5Analysis()

 # Генерация сигналов
 signals = m5_analyzer.generate_m5_signals(data)

 # Анализ результатов
 print(f"✓ Сгенерировано {len(signals)} сигналов")
 print(f"✓ Сигналов on покупку: {(signals['filtered_signal'] > 0).sum()}")
 print(f"✓ Сигналов on продажу: {(signals['filtered_signal'] < 0).sum()}")

 return signals

# Launch примера
if __name__ == "__main__":
 m5_signals = run_m5_Analysis_example()
```

### H1 (1 час) - Среднесрочная торговля

**Теория:** H1 Timeframe предназначен for среднесрочной торговли and Analysis основных трендов. Это критически важный Timeframe for понимания общей рыночной динамики and принятия стратегических решений.

**Почему H1 анализ важен:**
- **Анализ трендов:** Обеспечивает анализ основных рыночных трендов
- **Стратегические решения:** Подходит for принятия стратегических торговых решений
- **Снижение шума:** Минимальное влияние рыночного шума
- **Стабильность:** Наиболее стабильные and надежные сигналы

**Плюсы:**
- Анализ основных трендов
- Стабильные сигналы
- Минимальное влияние шума
- Подходит for стратегических решений

**Минусы:**
- Меньше торговых возможностей
- Медленная реакция on изменения
- Требует больше времени for Analysis
- Потенциальные упущенные возможности

```python
class WAVE2H1Analysis:
 """
 Анализ WAVE2 on часовом Timeframeе for среднесрочной торговли.

 H1 Timeframe предназначен for среднесрочной торговли and Analysis основных трендов.
 Это критически важный Timeframe for понимания общей рыночной динамики and
 принятия стратегических торговых решений.

 Теория: H1 анализ основан on принципе Analysis основных рыночных трендов,
 что позволяет принимать стратегические решения with минимальным влиянием
 рыночного шума and максимальной стабильностью сигналов.
 """

 def __init__(self):
 """Инициализация Analysisтора H1 with оптимизированными параметрами."""
 self.Timeframe = 'H1'
 self.optimal_params = {
 'long1': 200, # Стандартный for H1 - стабильный анализ трендов
 'fast1': 20, # Средний отклик - баланс скорости and стабильности
 'trend1': 5, # Средний тренд - достаточная фильтрация
 'long2': 50, # Средний второй период - дополнительная стабильность
 'fast2': 15, # Средняя вторая волна - оптимальная чувствительность
 'trend2': 3 # Средний тренд - стабильное определение направления
 }

 # Пороги for H1 Analysis
 self.thresholds = {
 'min_volatility': 0.001, # Минимальная волатильность for сигнала
 'max_spread': 0.002, # Максимальный спред for trading
 'min_trend_strength': 0.005, # Минимальная сила тренда
 'max_noise_level': 0.001, # Максимальный уровень шума
 'min_trend_duration': 5, # Минимальная длительность тренда
 'max_trend_duration': 50 # Максимальная длительность тренда
 }

 def analyze_h1_features(self, data: pd.dataFrame) -> Dict:
 """
 Анализ признаков for H1 Timeframe.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with приsignми for H1 Analysis
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

 # Поддержка and сопротивление - анализ уровней
 features['support_resistance'] = self._detect_support_resistance(data)

 # Трендовые каналы - анализ каналов
 features['trend_channels'] = self._detect_trend_channels(data)

 return features

 def _detect_medium_trend(self, data: pd.dataFrame) -> Dict:
 """
 Детекция среднесрочных трендов for H1 Analysis.

 Среднесрочные тренды представляют собой основные движения цены
 on часовом Timeframeе, которые критически важны for стратегических решений.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о среднесрочных трендах
 """
 wave1 = data['wave1']
 fastline1 = data['fastline1']
 wave2 = data['wave2']
 fastline2 = data['fastline2']

 # Основной тренд - пересечение wave1 and fastline1
 main_trend = np.where(wave1 > fastline1, 1, -1)

 # Дополнительный тренд - пересечение wave2 and fastline2
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

 def _detect_trend_reversal(self, data: pd.dataFrame) -> Dict:
 """
 Детекция трендовых разворотов for H1 Analysis.

 Трендовые развороты представляют собой критические моменты изменения
 направления основного тренда, которые критически важны for торговых решений.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о трендовых разворотах
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

 def _calculate_medium_volatility(self, data: pd.dataFrame) -> Dict:
 """
 Расчет среднесрочной волатильности for H1 Analysis.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о среднесрочной волатильности
 """
 wave1 = data['wave1']
 fastline1 = data['fastline1']

 # Среднесрочная волатильность
 medium_volatility = wave1.rolling(24).std() # 24 часа

 # Относительная волатильность
 relative_volatility = medium_volatility / medium_volatility.rolling(168).mean() # 1 неделя

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

 def _detect_trend_patterns(self, data: pd.dataFrame) -> Dict:
 """
 Детекция трендовых паттернов for H1 Analysis.

 Трендовые паттерны представляют собой повторяющиеся структуры
 in движении цены, которые характерны for среднесрочных трендов.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о трендовых паттернах
 """
 wave1 = data['wave1']
 fastline1 = data['fastline1']

 # Паттерн "Восходящий тренд" - последовательные повышения
 uptrend_pattern = self._detect_uptrend_pattern(wave1, window=10)

 # Паттерн "Нисходящий тренд" - последовательные понижения
 downtrend_pattern = self._detect_downtrend_pattern(wave1, window=10)

 # Паттерн "Треугольник" - сходящиеся линии тренда
 triangle_pattern = self._detect_triangle_pattern(wave1, fastline1, window=20)

 # Паттерн "Клин" - сходящиеся линии with наклоном
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

 # Восходящий тренд - and повышения, and понижения растут
 uptrend = higher_highs & higher_lows

 return uptrend

 def _detect_downtrend_pattern(self, series: pd.Series, window: int = 10) -> pd.Series:
 """Детекция паттерна 'Нисходящий тренд'."""
 # Последовательные понижения
 lower_highs = series.rolling(window).max() < series.rolling(window).max().shift(1)
 lower_lows = series.rolling(window).min() < series.rolling(window).min().shift(1)

 # Нисходящий тренд - and повышения, and понижения падают
 downtrend = lower_highs & lower_lows

 return downtrend

 def _detect_triangle_pattern(self, wave1: pd.Series, fastline1: pd.Series, window: int = 20) -> pd.Series:
 """Детекция паттерна 'Треугольник'."""
 # Скользящие максимумы and минимумы
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
 # Сходящиеся волны with наклоном
 wave_convergence = abs(wave1 - fastline1).rolling(window).mean()
 convergence_trend = wave_convergence.diff(window) < 0

 # Наклон in одну сторону
 wave_trend = wave1.rolling(window).mean().diff(window)
 consistent_trend = abs(wave_trend) > wave_trend.rolling(window * 2).std()

 # Клин - сходимость with наклоном
 wedge = convergence_trend & consistent_trend

 return wedge

 def _detect_flag_pattern(self, series: pd.Series, window: int = 12) -> pd.Series:
 """Детекция паттерна 'Флаг'."""
 # Предшествующий импульс
 impulse = series.diff(window).abs() > series.rolling(24).std() * 1.5

 # Консолидация после импульса
 consolidation = series.rolling(window).std() < series.rolling(24).std() * 0.6

 # Флаг - импульс with последующей консолидацией
 flag = impulse.shift(window) & consolidation

 return flag

 def _detect_support_resistance(self, data: pd.dataFrame) -> Dict:
 """
 Детекция уровней поддержки and сопротивления for H1 Analysis.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией об уровнях поддержки and сопротивления
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

 # Фильтрация on силе
 strong_maxs = local_maxs & (series > series.rolling(50).quantile(0.7))

 return strong_maxs

 def _find_support_levels(self, series: pd.Series, window: int = 20) -> pd.Series:
 """Поиск уровней поддержки."""
 # Локальные минимумы
 local_mins = series.rolling(window, center=True).min() == series

 # Фильтрация on силе
 strong_mins = local_mins & (series < series.rolling(50).quantile(0.3))

 return strong_mins

 def _calculate_distance_to_levels(self, series: pd.Series, levels: pd.Series) -> pd.Series:
 """Расчет расстояния to уровней."""
 # Находим ближайшие уровни
 level_values = series[levels]
 if len(level_values) == 0:
 return pd.Series(0, index=series.index)

 # Минимальное расстояние to любого уровня
 distances = []
 for i, value in enumerate(series):
 if len(level_values) > 0:
 min_distance = min(abs(value - level_values))
 distances.append(min_distance)
 else:
 distances.append(0)

 return pd.Series(distances, index=series.index)

 def _detect_level_break(self, series: pd.Series, levels: pd.Series, direction: str = 'up') -> pd.Series:
 """Детекция breakthrough уровней."""
 if direction == 'up':
 # Пробитие сопротивления вверх
 break_up = series > series[levels].max()
 return break_up
 else:
 # Пробитие поддержки вниз
 break_down = series < series[levels].min()
 return break_down

 def _detect_trend_channels(self, data: pd.dataFrame) -> Dict:
 """
 Детекция трендовых каналов for H1 Analysis.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 Словарь with информацией о трендовых каналах
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
 # Верхняя and нижняя границы канала
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
 # Верхняя and нижняя границы канала
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
 # Верхняя and нижняя границы канала
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

 def _calculate_pattern_strength(self, data: pd.dataFrame) -> pd.Series:
 """Расчет силы паттернов."""
 wave1 = data['wave1']
 fastline1 = data['fastline1']

 # Сила паттерна - стабильность соотношения
 pattern_strength = 1 / (abs(wave1 - fastline1) / (abs(fastline1) + 1e-8) + 1e-8)

 return pattern_strength

 def _determine_pattern_direction(self, data: pd.dataFrame) -> pd.Series:
 """Определение направления паттернов."""
 wave1 = data['wave1']
 fastline1 = data['fastline1']

 # Направление паттерна
 pattern_direction = np.where(wave1 > fastline1, 1, -1)

 return pattern_direction

 def generate_h1_signals(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 Генерация торговых сигналов for H1 Timeframe.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 dataFrame with торговыми сигналами
 """
 # Анализ признаков
 features = self.analyze_h1_features(data)

 # create dataFrame with сигналами
 signals = pd.dataFrame(index=data.index)

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

 # Фильтрация on волатильности
 normal_vol = features['medium_volatility']['normal_volatility']
 signals['filtered_signal'] = np.where(
 normal_vol,
 signals['combined_signal'],
 0
 )

 return signals

# example использования H1 Analysis
def run_h1_Analysis_example():
 """example Launchа H1 Analysis WAVE2."""
 # Loading data
 loader = WAVE2dataLoader()
 data = loader.load_wave2_data("GBPUSD", "H1")

 # create Analysisтора H1
 h1_analyzer = WAVE2H1Analysis()

 # Генерация сигналов
 signals = h1_analyzer.generate_h1_signals(data)

 # Анализ результатов
 print(f"✓ Сгенерировано {len(signals)} сигналов")
 print(f"✓ Сигналов on покупку: {(signals['filtered_signal'] > 0).sum()}")
 print(f"✓ Сигналов on продажу: {(signals['filtered_signal'] < 0).sum()}")

 return signals

# Launch примера
if __name__ == "__main__":
 h1_signals = run_h1_Analysis_example()
```

## create признаков for ML

**Теория:** create признаков for машинного обучения on basis WAVE2 является критически важным этапом for достижения высокой точности Predictions. Качественные признаки определяют успех ML-модели.

**Почему create признаков критично:**
- **Качество данных:** Качественные признаки определяют качество модели
- **Точность Predictions:** Хорошие признаки повышают точность Predictions
- **Робастность:** Правильные признаки обеспечивают робастность модели
- **Интерпретируемость:** Понятные признаки облегчают интерпретацию результатов

### 1. Базовые признаки WAVE2

**Теория:** Базовые признаки WAVE2 представляют собой фундаментальные components for Analysis рыночной динамики. Они обеспечивают основу for более сложных признаков and являются основой for ML-модели.

**Почему базовые признаки важны:**
- **Фундаментальная основа:** Обеспечивают базовую информацию о рынке
- **Простота интерпретации:** Легко понимаются and интерпретируются
- **Стабильность:** Обеспечивают стабильную основу for Analysis
- **Эффективность:** Минимальные вычислительные требования

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif
import talib

class WAVE2FeatureEngineer:
 """
 create признаков on basis WAVE2 for машинного обучения.

 Этот класс предоставляет комплексные методы for создания различных типов
 признаков on basis данных WAVE2, including базовые, лаговые, скользящие,
 технические and продвинутые признаки.

 Теория: Качественные признаки являются основой успешного машинного обучения.
 WAVE2 предоставляет богатую основу for создания признаков, которые могут
 выявлять скрытые паттерны and взаимосвязи in рыночных данных.
 """

 def __init__(self):
 """Инициализация инженера признаков WAVE2."""
 self.lag_periods = [1, 2, 3, 5, 10, 20, 50]
 self.rolling_windows = [5, 10, 20, 50, 100]
 self.scaler = StandardScaler()
 self.feature_names = []

 # Пороги for создания признаков
 self.thresholds = {
 'min_correlation': 0.1,
 'max_correlation': 0.9,
 'min_volatility': 0.001,
 'max_volatility': 0.1
 }

 def create_basic_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 create базовых признаков WAVE2.

 Базовые признаки представляют собой фундаментальные components
 for Analysis рыночной динамики on basis WAVE2.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 dataFrame with базовыми приsignми
 """
 features = pd.dataFrame(index=data.index)

 # 1. Основные волны - базовые components WAVE2
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

 # 4. Расстояния to нуля - анализ абсолютных значений
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

 def create_lag_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 create лаговых признаков WAVE2.

 Лаговые признаки представляют собой исторические значения,
 которые помогают модели учитывать временные dependencies.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 dataFrame with лаговыми приsignми
 """
 features = pd.dataFrame(index=data.index)

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

 def create_rolling_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 create скользящих признаков WAVE2.

 Скользящие признаки представляют собой статистические характеристики
 за различные временные окна, которые помогают выявить тренды and паттерны.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 dataFrame со скользящими приsignми
 """
 features = pd.dataFrame(index=data.index)

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

 # Скользящие максимумы and минимумы
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

 def create_technical_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 create технических признаков WAVE2.

 Технические признаки включают различные технические индикаторы,
 которые помогают анализировать рыночную динамику.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 dataFrame with техническими приsignми
 """
 features = pd.dataFrame(index=data.index)

 # RSI for волн
 features['wave1_rsi_14'] = talib.RSI(data['wave1'].values, timeperiod=14)
 features['wave2_rsi_14'] = talib.RSI(data['wave2'].values, timeperiod=14)
 features['fastline1_rsi_14'] = talib.RSI(data['fastline1'].values, timeperiod=14)
 features['fastline2_rsi_14'] = talib.RSI(data['fastline2'].values, timeperiod=14)

 # MACD for волн
 macd1, macd_signal1, macd_hist1 = talib.MACD(data['wave1'].values)
 features['wave1_macd'] = macd1
 features['wave1_macd_signal'] = macd_signal1
 features['wave1_macd_hist'] = macd_hist1

 macd2, macd_signal2, macd_hist2 = talib.MACD(data['wave2'].values)
 features['wave2_macd'] = macd2
 features['wave2_macd_signal'] = macd_signal2
 features['wave2_macd_hist'] = macd_hist2

 # Bollinger Bands for волн
 bb_upper1, bb_middle1, bb_lower1 = talib.BBANDS(data['wave1'].values)
 features['wave1_bb_upper'] = bb_upper1
 features['wave1_bb_middle'] = bb_middle1
 features['wave1_bb_lower'] = bb_lower1
 features['wave1_bb_width'] = (bb_upper1 - bb_lower1) / bb_middle1
 features['wave1_bb_position'] = (data['wave1'] - bb_lower1) / (bb_upper1 - bb_lower1 + 1e-8)

 # Stochastic for волн
 stoch_k1, stoch_d1 = talib.STOCH(data['wave1'].values, data['wave1'].values, data['wave1'].values)
 features['wave1_stoch_k'] = stoch_k1
 features['wave1_stoch_d'] = stoch_d1

 # ADX for волн
 features['wave1_adx_14'] = talib.ADX(data['wave1'].values, data['wave1'].values, data['wave1'].values, timeperiod=14)
 features['wave1_plus_di_14'] = talib.PLUS_DI(data['wave1'].values, data['wave1'].values, data['wave1'].values, timeperiod=14)
 features['wave1_minus_di_14'] = talib.MINUS_DI(data['wave1'].values, data['wave1'].values, data['wave1'].values, timeperiod=14)

 # Williams %R for волн
 features['wave1_williams_r_14'] = talib.WILLR(data['wave1'].values, data['wave1'].values, data['wave1'].values, timeperiod=14)

 # CCI for волн
 features['wave1_cci_14'] = talib.CCI(data['wave1'].values, data['wave1'].values, data['wave1'].values, timeperiod=14)

 return features

 def create_advanced_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 create продвинутых признаков WAVE2.

 Продвинутые признаки представляют собой сложные комбинации
 базовых признаков, которые выявляют скрытые паттерны.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 dataFrame with продвинутыми приsignми
 """
 features = pd.dataFrame(index=data.index)

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

 def create_temporal_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 create временных признаков WAVE2.

 Временные признаки учитывают временные аспекты рыночной динамики,
 including циклы, сезонность and временные паттерны.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 dataFrame with временными приsignми
 """
 features = pd.dataFrame(index=data.index)

 # 1. Время with последнего сигнала
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

 def _calculate_time_since_signal(self, data: pd.dataFrame) -> pd.Series:
 """Расчет времени with последнего сигнала."""
 signal_changes = (data['_signal'] != data['_signal'].shift(1))
 time_since = pd.Series(0, index=data.index)

 last_signal_time = 0
 for i, is_change in enumerate(signal_changes):
 if is_change and data['_signal'].iloc[i] != 0:
 last_signal_time = i
 time_since.iloc[i] = i - last_signal_time

 return time_since

 def _calculate_signal_frequency(self, data: pd.dataFrame) -> pd.Series:
 """Расчет частоты сигналов."""
 window = 50
 signal_frequency = data['_signal'].rolling(window).apply(
 lambda x: (x != 0).sum() / len(x), raw=True
 )
 return signal_frequency

 def _calculate_trend_duration(self, data: pd.dataFrame) -> pd.Series:
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

 def _detect_cyclical_pattern(self, data: pd.dataFrame) -> pd.Series:
 """Детекция циклических паттернов."""
 # Анализ автокорреляции
 wave1_autocorr = data['wave1'].rolling(20).apply(
 lambda x: x.autocorr(lag=1) if len(x) > 1 else 0, raw=False
 )

 # Циклический паттерн - высокая автокорреляция
 cyclical_pattern = (wave1_autocorr > 0.5).astype(int)

 return cyclical_pattern

 def create_all_features(self, data: pd.dataFrame) -> pd.dataFrame:
 """
 create всех признаков WAVE2.

 Args:
 data: dataFrame with data WAVE2

 Returns:
 dataFrame со allи приsignми
 """
 print("create базовых признаков...")
 basic_features = self.create_basic_features(data)

 print("create лаговых признаков...")
 lag_features = self.create_lag_features(data)

 print("create скользящих признаков...")
 rolling_features = self.create_rolling_features(data)

 print("create технических признаков...")
 technical_features = self.create_technical_features(data)

 print("create продвинутых признаков...")
 advanced_features = self.create_advanced_features(data)

 print("create временных признаков...")
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

 # remove columns with NaN значениями
 all_features = all_features.dropna()

 print(f"✓ Создано {len(all_features.columns)} признаков")
 print(f"✓ Размер данных: {all_features.shape}")

 return all_features

 def select_best_features(self, X: pd.dataFrame, y: pd.Series, k: int = 50) -> pd.dataFrame:
 """
 Выбор лучших признаков for ML модели.

 Args:
 X: dataFrame with приsignми
 y: Series with целевой переменной
 k: Количество лучших признаков

 Returns:
 dataFrame with отобранными приsignми
 """
 # remove columns with бесконечными значениями
 X_clean = X.replace([np.inf, -np.inf], np.nan).dropna()

 # Выбор лучших признаков
 selector = SelectKBest(score_func=f_classif, k=min(k, X_clean.shape[1]))
 X_selected = selector.fit_transform(X_clean, y[X_clean.index])

 # Получение названий отобранных признаков
 selected_features = X_clean.columns[selector.get_support()].toList()

 print(f"✓ Отобрано {len(selected_features)} лучших признаков")

 return pd.dataFrame(X_selected, columns=selected_features, index=X_clean.index)

# example использования инженера признаков
def run_feature_engineering_example():
 """example создания признаков WAVE2."""
 # Loading data
 loader = WAVE2dataLoader()
 data = loader.load_wave2_data("GBPUSD", "H1")

 # create инженера признаков
 feature_engineer = WAVE2FeatureEngineer()

 # create всех признаков
 features = feature_engineer.create_all_features(data)

 # create целевой переменной
 target = (data['Close'].shift(-1) > data['Close']).astype(int)
 target = target[features.index]

 # Выбор лучших признаков
 selected_features = feature_engineer.select_best_features(features, target, k=30)

 print(f"✓ Финальный набор признаков: {selected_features.shape}")

 return selected_features, target

# Launch примера
if __name__ == "__main__":
 features, target = run_feature_engineering_example()
```

### 2. Продвинутые признаки

**Теория:** Продвинутые признаки WAVE2 представляют собой сложные комбинации базовых признаков, которые выявляют скрытые паттерны and взаимосвязи in рыночных данных. Они критически важны for достижения высокой точности ML-модели.

**Почему продвинутые признаки критичны:**
- **Выявление паттернов:** Обнаруживают скрытые паттерны in данных
- **Повышение точности:** Значительно повышают точность Predictions
- **Робастность:** Обеспечивают устойчивость к рыночному шуму
- **Адаптивность:** Позволяют модели адаптироваться к изменениям рынка

**Плюсы:**
- Высокая точность Predictions
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
 """create продвинутых признаков WAVE2"""
 features = pd.dataFrame(index=data.index)

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

**Теория:** Временные признаки WAVE2 учитывают временные аспекты рыночной динамики, including циклы, сезонность and временные паттерны. Они критически важны for понимания временной структуры рынка.

**Почему временные признаки важны:**
- **Временная Structure:** Учитывают временные аспекты рынка
- **Циклические паттерны:** Выявляют повторяющиеся паттерны
- **Сезонность:** Учитывают сезонные эффекты
- **Временные dependencies:** Анализируют dependencies во времени

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
 """create временных признаков WAVE2"""
 features = pd.dataFrame(index=data.index)

 # 1. Время with последнего сигнала
 features['time_since_signal'] = self._calculate_time_since_signal(data)

 # 2. Частота сигналов
 features['signal_frequency'] = self._calculate_signal_frequency(data)

 # 3. Длительность тренда
 features['trend_duration'] = self._calculate_trend_duration(data)

 # 4. Циклические паттерны
 features['cyclical_pattern'] = self._detect_cyclical_pattern(data)

 return features
```

## create целевых переменных

**Теория:** create целевых переменных является критически важным этапом for обучения ML-модели. Правильно определенные целевые переменные определяют успех всей системы машинного обучения.

**Почему create целевых переменных критично:**
- **Определение задачи:** Четко определяет задачу машинного обучения
- **Качество обучения:** Качественные целевые переменные улучшают обучение
- **Интерпретируемость:** Понятные целевые переменные облегчают интерпретацию
- **Практическая применимость:** Обеспечивают практическую применимость результатов

### 1. Направление цены

**Теория:** Направление цены является наиболее фундаментальной целевой переменной for торговых систем. Она определяет основную задачу - Prediction направления движения цены.

**Почему направление цены важно:**
- **Фундаментальная задача:** Основная задача торговых систем
- **Простота интерпретации:** Легко понимается and интерпретируется
- **Практическая применимость:** Непосредственно применимо in торговле
- **Универсальность:** Подходит for различных торговых стратегий

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
 """create целевой переменной - направление цены"""
 future_price = data['Close'].shift(-horizon)
 current_price = data['Close']

 # Процентное изменение
 price_change = (future_price - current_price) / current_price

 # Классификация направления
 target = pd.cut(
 price_change,
 bins=[-np.inf, -0.001, 0.001, np.inf],
 labels=[0, 1, 2], # 0=down, 1=hold, 2=up
 include_lowest=True
 )

 return target.astype(int)
```

### 2. Сила движения

**Теория:** Сила движения представляет собой более сложную целевую переменную, которая учитывает not только направление, но and интенсивность движения цены. Это критически важно for оптимизации торговых стратегий.

**Почему сила движения важна:**
- **Интенсивность движения:** Учитывает силу движения цены
- **Оптимизация стратегий:** Позволяет оптимизировать торговые стратегии
- **Management рисками:** Помогает in управлении рисками
- **Повышение прибыльности:** Может повысить общую прибыльность

**Плюсы:**
- Учет интенсивности движения
- Оптимизация стратегий
- improve управления рисками
- Потенциальное повышение прибыльности

**Минусы:**
- Сложность определения
- Потенциальная нестабильность
- Сложность интерпретации
- Высокие требования к данным

```python
def create_movement_strength_target(data, horizon=1):
 """create целевой переменной - сила движения"""
 future_price = data['Close'].shift(-horizon)
 current_price = data['Close']

 # Процентное изменение
 price_change = (future_price - current_price) / current_price

 # Классификация силы
 target = pd.cut(
 abs(price_change),
 bins=[0, 0.001, 0.005, 0.01, np.inf],
 labels=[0, 1, 2, 3], # 0=weak, 1=medium, 2=strong, 3=very_strong
 include_lowest=True
 )

 return target.astype(int)
```

### 3. Волатильность

**Теория:** Волатильность является критически важной характеристикой финансовых рынков, которая определяет уровень риска and потенциальную прибыльность. Анализ волатильности критичен for создания робастных торговых систем.

**Почему волатильность важна:**
- **Management рисками:** Критически важно for управления рисками
- **Оптимизация позиций:** Помогает оптимизировать размеры позиций
- **Адаптация стратегий:** Позволяет адаптировать стратегии к рыночным условиям
- **Prediction рисков:** Помогает предсказывать потенциальные риски

**Плюсы:**
- Критически важно for управления рисками
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
 """create целевой переменной - волатильность"""
 future_prices = data['Close'].shift(-horizon)
 current_prices = data['Close']

 # Расчет волатильности
 volatility = data['Close'].rolling(horizon).std()

 # Классификация волатильности
 target = pd.cut(
 volatility,
 bins=[0, 0.01, 0.02, 0.05, np.inf],
 labels=[0, 1, 2, 3], # 0=low, 1=medium, 2=high, 3=very_high
 include_lowest=True
 )

 return target.astype(int)
```

## ML-модели for WAVE2

**Теория:** ML-модели for WAVE2 представляют собой комплексную system машинного обучения, которая использует различные алгоритмы for Analysis данных WAVE2 and генерации торговых сигналов. Это критически важно for создания высокоточных торговых систем.

**Почему ML-модели критичны:**
- **Высокая точность:** Обеспечивают высокую точность Predictions
- **Адаптивность:** Могут адаптироваться к изменениям рынка
- **Автоматизация:** Автоматизируют процесс Analysis and принятия решений
- **Масштабируемость:** Могут обрабатывать большие объемы данных

### 1. Классификация сигналов

**Теория:** Классификация сигналов является основной задачей for торговых систем, где модель должна предсказать направление движения цены. Это критически важно for принятия торговых решений.

**Почему классификация сигналов важна:**
- **Основная задача:** Основная задача торговых систем
- **Практическая применимость:** Непосредственно применимо in торговле
- **Простота интерпретации:** Легко интерпретируется
- **Универсальность:** Подходит for различных стратегий

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
from sklearn.metrics import classification_Report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import joblib

class WAVE2Classifier:
 """
 Классификатор on basis WAVE2 for предсказания price direction.

 Этот класс предоставляет комплексную system машинного обучения for
 Analysis данных WAVE2 and генерации торговых сигналов with высокой точностью.

 Теория: Классификация сигналов является основной задачей for торговых систем,
 где модель должна предсказать направление движения цены. WAVE2 предоставляет
 богатую основу for создания высокоточных классификаторов.
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

 # create ансамбля
 self.ensemble = VotingClassifier(
 estimators=List(self.models.items()),
 voting='soft'
 )

 # Скалер for нормализации данных
 self.scaler = StandardScaler()

 # Флаги обучения
 self.is_trained = False
 self.feature_importance = None

 def train(self, X: pd.dataFrame, y: pd.Series, test_size: float = 0.2) -> dict:
 """
 Обучение классификатора WAVE2.

 Args:
 X: dataFrame with приsignми
 y: Series with целевой переменной
 test_size: Размер тестовой выборки

 Returns:
 Словарь with результатами обучения
 """
 print("Начало обучения WAVE2 классификатора...")

 # Разделение on train/validation
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

 # Предсказания on валидационной выборке
 y_val_pred = self.ensemble.predict(X_val)
 y_val_proba = self.ensemble.predict_proba(X_val)

 # Метрики производительности
 accuracy = accuracy_score(y_val, y_val_pred)
 Report = classification_Report(y_val, y_val_pred)
 cm = confusion_matrix(y_val, y_val_pred)

 print(f"\nValidation Accuracy: {accuracy:.4f}")
 print(f"\nClassification Report:\n{Report}")
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
 'classification_Report': Report,
 'confusion_matrix': cm,
 'feature_importance': self.feature_importance
 }

 def predict(self, X: pd.dataFrame) -> np.ndarray:
 """
 Prediction класса.

 Args:
 X: dataFrame with приsignми

 Returns:
 Массив предсказанных классов
 """
 if not self.is_trained:
 raise ValueError("Модель not обучена. Сначала вызовите train().")

 return self.ensemble.predict(X)

 def predict_proba(self, X: pd.dataFrame) -> np.ndarray:
 """
 Prediction вероятностей классов.

 Args:
 X: dataFrame with приsignми

 Returns:
 Массив вероятностей for каждого класса
 """
 if not self.is_trained:
 raise ValueError("Модель not обучена. Сначала вызовите train().")

 return self.ensemble.predict_proba(X)

 def get_feature_importance(self, feature_names: List = None) -> pd.dataFrame:
 """
 Получение важности признаков.

 Args:
 feature_names: List названий признаков

 Returns:
 dataFrame with важностью признаков
 """
 if self.feature_importance is None:
 print("Важность признаков недоступна for данной модели")
 return None

 if feature_names is None:
 feature_names = [f'feature_{i}' for i in range(len(self.feature_importance))]

 importance_df = pd.dataFrame({
 'feature': feature_names,
 'importance': self.feature_importance
 }).sort_values('importance', ascending=False)

 return importance_df

 def optimize_hyperparameters(self, X: pd.dataFrame, y: pd.Series) -> dict:
 """
 Оптимизация гиперпараметров for лучших моделей.

 Args:
 X: dataFrame with приsignми
 y: Series with целевой переменной

 Returns:
 Словарь with лучшими параметрами
 """
 print("Оптимизация гиперпараметров...")

 # parameters for оптимизации
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
 print(f"Лучшие parameters for {model_name}: {grid_search.best_params_}")
 print(f"Лучший score: {grid_search.best_score_:.4f}")

 return best_params

 def save_model(self, filepath: str):
 """
 Сохранение обученной модели.

 Args:
 filepath: Путь for сохранения модели
 """
 if not self.is_trained:
 raise ValueError("Модель not обучена. Сначала вызовите train().")

 model_data = {
 'ensemble': self.ensemble,
 'scaler': self.scaler,
 'feature_importance': self.feature_importance,
 'is_trained': self.is_trained
 }

 joblib.dump(model_data, filepath)
 print(f"Модель сохранена in {filepath}")

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

# example использования классификатора
def run_classification_example():
 """example обучения and использования WAVE2 классификатора."""
 # Loading data
 loader = WAVE2dataLoader()
 data = loader.load_wave2_data("GBPUSD", "H1")

 # create признаков
 feature_engineer = WAVE2FeatureEngineer()
 features = feature_engineer.create_all_features(data)

 # create целевой переменной
 target = (data['Close'].shift(-1) > data['Close']).astype(int)
 target = target[features.index]

 # remove NaN значений
 valid_indices = features.dropna().index.intersection(target.dropna().index)
 features_clean = features.loc[valid_indices]
 target_clean = target.loc[valid_indices]

 # create and обучение классификатора
 classifier = WAVE2Classifier()
 results = classifier.train(features_clean, target_clean)

 # Предсказания
 Predictions = classifier.predict(features_clean)
 probabilities = classifier.predict_proba(features_clean)

 print(f"✓ Обучение COMPLETED")
 print(f"✓ Точность ансамбля: {results['ensemble_score']:.4f}")
 print(f"✓ Кросс-валидация: {results['cv_scores'].mean():.4f}")

 return classifier, results

# Launch примера
if __name__ == "__main__":
 classifier, results = run_classification_example()
```

### 2. Регрессия for прогнозирования цены

**Теория:** Регрессия for прогнозирования цены представляет собой более сложную задачу, где модель должна предсказать конкретное значение цены, а not только направление. Это критически важно for точного управления позициями.

**Почему регрессия важна:**
- **Точность прогнозов:** Обеспечивает более точные прогнозы
- **Management позициями:** Помогает in точном управлении позициями
- **Оптимизация стратегий:** Позволяет оптимизировать торговые стратегии
- **Management рисками:** Помогает in управлении рисками

**Плюсы:**
- Более точные прогнозы
- Лучшее Management позициями
- Оптимизация стратегий
- improve управления рисками

**Минусы:**
- Сложность обучения
- Потенциальная нестабильность
- Сложность интерпретации
- Высокие требования к данным

```python
class WAVE2Regressor:
 """Регрессор on basis WAVE2"""

 def __init__(self):
 self.models = {
 'xgboost': XGBRegressor(),
 'lightgbm': LGBMRegressor(),
 'catboost': CatBoostRegressor(),
 'neural_network': MLPRegressor()
 }
 self.ensemble = VotingRegressor(
 estimators=List(self.models.items())
 )

 def train(self, X, y):
 """Обучение регрессора"""
 self.ensemble.fit(X, y)
 return self.ensemble

 def predict(self, X):
 """Prediction цены"""
 return self.ensemble.predict(X)
```

### 3. Deep Learning модель

**Теория:** Deep Learning модели представляют собой наиболее сложные and мощные алгоритмы машинного обучения, которые могут выявлять сложные нелинейные dependencies in данных WAVE2. Это критически важно for достижения максимальной точности.

**Почему Deep Learning модели важны:**
- **Сложные dependencies:** Могут выявлять сложные нелинейные dependencies
- **Высокая точность:** Обеспечивают максимальную точность Predictions
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
 """Deep Learning модель for WAVE2"""

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

 # One-hot encoding for y
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

**Теория:** Бэктестинг WAVE2 модели является критически важным этапом for валидации эффективности торговой стратегии. Это позволяет оценить производительность модели on исторических данных перед реальным использованием.

**Почему бэктестинг критичен:**
- **Валидация стратегии:** Позволяет проверить эффективность стратегии
- **Оценка рисков:** Помогает оценить потенциальные риски
- **Оптимизация параметров:** Позволяет оптимизировать parameters стратегии
- **Уверенность:** Повышает уверенность in стратегии

### 1. Стратегия бэктестинга

**Теория:** Стратегия бэктестинга определяет методологию тестирования WAVE2 модели on исторических данных. Правильная стратегия критически важна for получения достоверных результатов.

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
- Сложность settings
- Потенциальные Issues with data
- Время on тестирование

```python
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class WAVE2Backtester:
 """
 Бэктестер for WAVE2 модели with комплексным анализом производительности.

 Этот класс предоставляет полный набор инструментов for тестирования
 WAVE2 торговых стратегий on исторических данных with детальным анализом
 производительности and рисков.

 Теория: Бэктестинг является критически важным этапом for валидации
 эффективности торговой стратегии. Правильно проведенный бэктестинг
 позволяет оценить реальную производительность стратегии перед
 использованием in реальной торговле.
 """

 def __init__(self, model, data: pd.dataFrame, initial_capital: float = 10000):
 """
 Инициализация бэктестера WAVE2.

 Args:
 model: Обученная ML модель
 data: dataFrame with историческими данными
 initial_capital: Начальный капитал for тестирования
 """
 self.model = model
 self.data = data
 self.initial_capital = initial_capital
 self.results = {}

 # parameters торговли
 self.commission = 0.001 # 0.1% комиссия
 self.slippage = 0.0005 # 0.05% проскальзывание
 self.max_position_size = 1.0 # Максимальный размер позиции

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
 Словарь with результатами бэктестинга
 """
 print(f"Начало бэктестинга WAVE2 стратегии: {start_date} - {end_date}")

 # Фильтрация данных on датам
 start_dt = pd.to_datetime(start_date)
 end_dt = pd.to_datetime(end_date)
 mask = (self.data.index >= start_dt) & (self.data.index <= end_dt)
 test_data = self.data[mask].copy()

 if len(test_data) == 0:
 raise ValueError("Нет данных for specified периода")

 print(f"Период тестирования: {len(test_data)} periods")

 # create признаков for тестирования
 feature_engineer = WAVE2FeatureEngineer()
 features = feature_engineer.create_all_features(test_data)

 # remove NaN значений
 valid_indices = features.dropna().index.intersection(test_data.index)
 features_clean = features.loc[valid_indices]
 test_data_clean = test_data.loc[valid_indices]

 # Предсказания модели
 Predictions = self.model.predict(features_clean)
 probabilities = self.model.predict_proba(features_clean)

 # Симуляция торговли
 trading_results = self._simulate_trading(
 test_data_clean, Predictions, probabilities, transaction_cost
 )

 # Расчет метрик производительности
 performance_metrics = self._calculate_performance_metrics(trading_results)

 # Анализ рисков
 risk_metrics = self._calculate_risk_metrics(trading_results)

 # Анализ сделок
 trade_Analysis = self._analyze_trades(trading_results)

 # Сохранение результатов
 self.results = {
 'trading_results': trading_results,
 'performance_metrics': performance_metrics,
 'risk_metrics': risk_metrics,
 'trade_Analysis': trade_Analysis,
 'Predictions': Predictions,
 'probabilities': probabilities,
 'test_period': (start_date, end_date),
 'data_points': len(test_data_clean)
 }

 print(f"✓ Бэктестинг завершен")
 print(f"✓ Общая доходность: {performance_metrics['total_return']:.2%}")
 print(f"✓ Sharpe Ratio: {performance_metrics['sharpe_ratio']:.2f}")
 print(f"✓ Максимальная просадка: {performance_metrics['max_drawdown']:.2%}")

 return self.results

 def _simulate_trading(self, data: pd.dataFrame, Predictions: np.ndarray,
 probabilities: np.ndarray, transaction_cost: float) -> dict:
 """
 Симуляция торговли on basis Predictions модели.

 Args:
 data: data for тестирования
 Predictions: Предсказания модели
 probabilities: Вероятности Predictions
 transaction_cost: Стоимость транзакций

 Returns:
 Словарь with результатами торговли
 """
 capital = self.initial_capital
 position = 0 # 0 = нет позиции, 1 = длинная, -1 = короткая
 equity_curve = [capital]
 trades = []
 current_trade = None

 for i, (date, row) in enumerate(data.iterrows()):
 if i == 0:
 continue

 current_price = row['Close']
 signal = Predictions[i-1] if i > 0 else 0
 confidence = probabilities[i-1].max() if i > 0 else 0

 # Фильтрация on уверенности (только высокоуверенные сигналы)
 if confidence < 0.6:
 signal = 0

 # Логика торговли
 if signal == 1 and position <= 0: # Сигнал on покупку
 if position == -1: # Закрытие короткой позиции
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

 elif signal == -1 and position >= 0: # Сигнал on продажу
 if position == 1: # Закрытие длинной позиции
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

 elif signal == 0: # Сигнал holding
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

 # update кривой капитала
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
 Словарь with метриками производительности
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
 risk_free_rate = 0.02 # 2% безрисковая ставка
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
 Словарь with метриками риска
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
 Словарь with анализом сделок
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
 duration = (trade['exit_date'] - trade['entry_date']).total_seconds() / 3600 # in часах
 trade_durations.append(duration)

 avg_trade_duration = np.mean(trade_durations) if trade_durations else 0

 # Лучшая and худшая сделки
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
 save_path: Путь for сохранения графиков
 """
 if not self.results:
 print("Нет результатов for отображения. Сначала запустите backtest().")
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

 # add значений on столбцы
 for bar, value in zip(bars, metric_values):
 axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
 f'{value:.3f}', ha='center', va='bottom')

 plt.tight_layout()

 if save_path:
 plt.savefig(save_path, dpi=300, bbox_inches='tight')
 print(f"Графики сохранены in {save_path}")

 plt.show()

 def generate_Report(self) -> str:
 """
 Генерация текстового Reportа о результатах бэктестинга.

 Returns:
 Строка with Reportом
 """
 if not self.results:
 return "Нет результатов for Reportа. Сначала запустите backtest()."

 metrics = self.results['performance_metrics']
 risk_metrics = self.results['risk_metrics']
 trade_Analysis = self.results['trade_Analysis']

 Report = f"""
WAVE2 Backtesting Report
========================

Test Period: {self.results['test_period'][0]} - {self.results['test_period'][1]}
data Points: {self.results['data_points']}

PERFORMANCE METRICS
-------------------
Total Return: {metrics['total_return']:.2%}
Annualized Return: {metrics['annualized_return']:.2%}
Volatility: {metrics['volatility']:.2%}
Sharpe Ratio: {metrics['sharpe_ratio']:.2f}
Max Drawdown: {metrics['max_drawdown']:.2%}

TRADE Analysis
--------------
Total Trades: {trade_Analysis['total_trades']}
Winning Trades: {trade_Analysis['winning_trades']}
Losing Trades: {trade_Analysis['losing_trades']}
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
Average Trade Duration: {trade_Analysis['avg_trade_duration']:.1f} hours
Best Trade: {trade_Analysis['best_trade']:.2%}
Worst Trade: {trade_Analysis['worst_trade']:.2%}
 """

 return Report

# example использования бэктестера
def run_backtesting_example():
 """example Launchа бэктестинга WAVE2 стратегии."""
 # Loading data
 loader = WAVE2dataLoader()
 data = loader.load_wave2_data("GBPUSD", "H1")

 # create and обучение модели
 feature_engineer = WAVE2FeatureEngineer()
 features = feature_engineer.create_all_features(data)

 target = (data['Close'].shift(-1) > data['Close']).astype(int)
 target = target[features.index]

 valid_indices = features.dropna().index.intersection(target.dropna().index)
 features_clean = features.loc[valid_indices]
 target_clean = target.loc[valid_indices]

 classifier = WAVE2Classifier()
 classifier.train(features_clean, target_clean)

 # create and Launch бэктестера
 backtester = WAVE2Backtester(classifier, data)
 results = backtester.backtest('2023-01-01', '2023-12-31')

 # Отображение результатов
 backtester.plot_results()
 print(backtester.generate_Report())

 return backtester, results

# Launch примера
if __name__ == "__main__":
 backtester, results = run_backtesting_example()
```

### 2. Метрики производительности

**Теория:** Метрики производительности являются критически важными for оценки эффективности WAVE2 модели. Они обеспечивают количественную оценку различных аспектов производительности торговой стратегии.

**Почему метрики производительности важны:**
- **Количественная оценка:** Обеспечивают количественную оценку производительности
- **Сравнение стратегий:** Позволяют сравнивать различные стратегии
- **Оптимизация:** Помогают in оптимизации параметров
- **Management рисками:** Критически важны for управления рисками

**Плюсы:**
- Количественная оценка
- Возможность сравнения
- Помощь in оптимизации
- Критически важно for управления рисками

**Минусы:**
- Сложность интерпретации
- Потенциальные Issues with data
- Необходимость понимания метрик

```python
def calculate_performance_metrics(returns):
 """Расчет метрик производительности"""
 returns = np.array(returns)

 # Базовая статистика
 total_return = np.sum(returns)
 annualized_return = total_return * 252 # Предполагаем 252 торговых дня

 # Волатильность
 volatility = np.std(returns) * np.sqrt(252)

 # Sharpe Ratio
 risk_free_rate = 0.02 # 2% безрисковая ставка
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

**Теория:** Оптимизация параметров WAVE2 является критически важным этапом for достижения максимальной эффективности торговой стратегии. Правильно оптимизированные parameters могут значительно повысить производительность системы.

**Почему оптимизация параметров критична:**
- **Максимизация производительности:** Позволяет достичь максимальной производительности
- **Адаптация к рынку:** Помогает адаптироваться к различным рыночным условиям
- **Снижение рисков:** Может снизить риски стратегии
- **Повышение прибыльности:** Может значительно повысить прибыльность

### 1. Генетический алгоритм

**Теория:** Генетический алгоритм представляет собой эволюционный метод оптимизации, который имитирует процесс естественного отбора for поиска оптимальных параметров WAVE2. Это особенно эффективно for сложных многомерных задач оптимизации.

**Почему генетический алгоритм важен:**
- **Глобальная оптимизация:** Может найти глобальный оптимум
- **Робастность:** Устойчив к локальным минимумам
- **Гибкость:** Может Workingть with различными типами параметров
- **Эффективность:** Эффективен for сложных задач

**Плюсы:**
- Глобальная оптимизация
- Робастность
- Гибкость
- Эффективность

**Минусы:**
- Сложность settings
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
 """Оптимизация with помощью генетического алгоритма"""
 # Инициализация популяции
 population = self._initialize_population(population_size)

 for generation in range(n_generations):
 # Оценка популяции
 scores = self._evaluate_population(population)

 # Отбор лучших особей
 elite = self._select_elite(population, scores, top_k=10)

 # Скрещивание and мутация
 new_population = self._crossover_and_mutate(elite, population_size)

 # update популяции
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

**Теория:** Bayesian Optimization представляет собой интеллектуальный метод оптимизации, который использует байесовскую статистику for эффективного поиска оптимальных параметров WAVE2. Это особенно эффективно for дорогих in вычислении функций.

**Почему Bayesian Optimization важен:**
- **Эффективность:** Очень эффективен for дорогих функций
- **Интеллектуальный поиск:** Использует информацию о предыдущих оценках
- **Быстрая сходимость:** Быстро сходится к оптимуму
- **Учет неопределенности:** Учитывает неопределенность in оценках

**Плюсы:**
- Высокая эффективность
- Интеллектуальный поиск
- Быстрая сходимость
- Учет неопределенности

**Минусы:**
- Сложность реализации
- Требования к данным
- Потенциальные Issues with масштабированием

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
 """Целевая function for оптимизации"""
 long1, fast1, trend1, long2, fast2, trend2 = params

 # Расчет WAVE2 with data параметрами
 wave2_data = self._calculate_wave2(long1, fast1, trend1, long2, fast2, trend2)

 # Расчет производительности
 performance = self._calculate_performance(wave2_data)

 # Возвращаем отрицательное значение for минимизации
 return -performance
```

## Продакшн деплой WAVE2 модели

**Теория:** Продакшн деплой WAVE2 модели является финальным этапом создания торговой системы, который обеспечивает развертывание модели in реальной торговой среде. Это критически важно for практического применения системы.

**Почему продакшн деплой критичен:**
- **Практическое применение:** Обеспечивает практическое применение системы
- **Автоматизация:** Автоматизирует торговые процессы
- **Масштабируемость:** Позволяет масштабировать system
- **Monitoring:** Обеспечивает Monitoring производительности

### 1. API for WAVE2 модели

**Теория:** API for WAVE2 модели обеспечивает программный interface for взаимодействия with моделью, что критически важно for интеграции with торговыми системами and автоматизации процессов.

**Почему API важен:**
- **integration:** Обеспечивает интеграцию with торговыми системами
- **Автоматизация:** Позволяет автоматизировать процессы
- **Масштабируемость:** Обеспечивает масштабируемость системы
- **Гибкость:** Обеспечивает гибкость in использовании

**Плюсы:**
- integration with системами
- Автоматизация процессов
- Масштабируемость
- Гибкость использования

**Минусы:**
- Сложность разработки
- Требования к безопасности
- Необходимость Monitoringа

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
 Prediction: int
 probability: float
 confidence: str

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
 """Prediction on basis WAVE2"""
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

 # Prediction
 Prediction = model.predict([features])[0]
 probability = model.predict_proba([features])[0].max()

 # Определение уверенности
 if probability > 0.8:
 confidence = "high"
 elif probability > 0.6:
 confidence = "medium"
 else:
 confidence = "low"

 return PredictionResponse(
 Prediction=int(Prediction),
 probability=float(probability),
 confidence=confidence
 )

 except Exception as e:
 raise HTTPException(status_code=500, detail=str(e))
```

### 2. Docker контейнер

**Теория:** Docker контейнеризация обеспечивает изоляцию, портабельность and масштабируемость WAVE2 модели in продакшн среде. Это критически важно for обеспечения стабильности and простоты развертывания.

**Почему Docker контейнер важен:**
- **Изоляция:** Обеспечивает изоляцию модели
- **Портабельность:** Позволяет легко переносить модель
- **Масштабируемость:** Упрощает масштабирование
- **Management:** Упрощает Management зависимостями

**Плюсы:**
- Изоляция модели
- Портабельность
- Масштабируемость
- Упрощение управления

**Минусы:**
- Дополнительная сложность
- Потенциальные Issues with производительностью
- Необходимость управления контейнерами

```dockerfile
# Dockerfile for WAVE2 модели
FROM python:3.11-slim

WORKDIR /app

# installation зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование модели and кода
COPY models/ ./models/
COPY src/ ./src/
COPY main.py .

# Экспорт порта
EXPOSE 8000

# Launch приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Monitoring производительности

**Теория:** Monitoring производительности WAVE2 модели является критически важным for обеспечения стабильности and эффективности торговой системы in продакшн среде. Это позволяет быстро выявлять and устранять проблемы.

**Почему Monitoring производительности важен:**
- **Стабильность:** Обеспечивает стабильность системы
- **Быстрое выявление проблем:** Позволяет быстро выявлять проблемы
- **Оптимизация:** Помогает in оптимизации производительности
- **Management рисками:** Критически важно for управления рисками

**Плюсы:**
- Обеспечение стабильности
- Быстрое выявление проблем
- Помощь in оптимизации
- Критически важно for управления рисками

**Минусы:**
- Сложность settings
- Необходимость постоянного внимания
- Потенциальные ложные срабатывания

```python
class WAVE2Monitor:
 """Monitoring WAVE2 модели"""

 def __init__(self):
 self.performance_history = []
 self.alert_thresholds = {
 'accuracy': 0.7,
 'latency': 1.0, # секунды
 'throughput': 100 # запросов in minutesу
 }

 def monitor_Prediction(self, Prediction, actual, latency):
 """Monitoring предсказания"""
 # Расчет точности
 accuracy = 1 if Prediction == actual else 0

 # Сохранение метрик
 self.performance_history.append({
 'timestamp': datetime.now(),
 'accuracy': accuracy,
 'latency': latency,
 'Prediction': Prediction,
 'actual': actual
 })

 # check алертов
 self._check_alerts()

 def _check_alerts(self):
 """check алертов"""
 if len(self.performance_history) < 10:
 return

 recent_performance = self.performance_history[-10:]

 # check точности
 avg_accuracy = np.mean([p['accuracy'] for p in recent_performance])
 if avg_accuracy < self.alert_thresholds['accuracy']:
 self._send_alert("Low accuracy detected")

 # check латентности
 avg_latency = np.mean([p['latency'] for p in recent_performance])
 if avg_latency > self.alert_thresholds['latency']:
 self._send_alert("High latency detected")
```

## Следующие шаги

После Analysis WAVE2 переходите к:
- **[12_schr_levels_Analysis.md](12_schr_levels_Analysis.md)** - Анализ SCHR Levels
- **[13_schr_short3_Analysis.md](13_schr_short3_Analysis.md)** - Анализ SCHR SHORT3

## Ключевые выводы

**Теория:** Ключевые выводы суммируют наиболее важные аспекты Analysis WAVE2, которые критически важны for создания прибыльной and робастной торговой системы.

1. **WAVE2 - мощный индикатор for Analysis трендов**
 - **Теория:** WAVE2 представляет собой революционный подход к техническому анализу
 - **Почему важно:** Обеспечивает высокую точность Analysis трендов
 - **Плюсы:** Высокая точность, структурный анализ, адаптивность
 - **Минусы:** Сложность settings, высокие требования к ресурсам

2. **МультиTimeframesый анализ - разные parameters for разных Timeframes**
 - **Теория:** Каждый Timeframe требует специфических параметров for максимальной эффективности
 - **Почему важно:** Обеспечивает оптимальную производительность on всех временных горизонтах
 - **Плюсы:** Оптимизация производительности, снижение рисков, повышение точности
 - **Минусы:** Сложность settings, необходимость понимания каждого Timeframe

3. **Богатые признаки - множество возможностей for создания признаков**
 - **Теория:** WAVE2 предоставляет богатую основу for создания признаков машинного обучения
 - **Почему важно:** Качественные признаки определяют успех ML-модели
 - **Плюсы:** Высокая точность, выявление паттернов, робастность
 - **Минусы:** Сложность вычислений, потенциальное переобучение

4. **Высокая точность - возможность достижения 95%+ точности**
 - **Теория:** Правильно настроенная WAVE2 модель может достигать очень высокой точности
 - **Почему важно:** Высокая точность критична for прибыльной торговли
 - **Плюсы:** Высокая прибыльность, снижение рисков, уверенность in стратегии
 - **Минусы:** Высокие требования к настройке, потенциальное переобучение

5. **Продакшн готовность - полная integration with продакшн системами**
 - **Теория:** WAVE2 модель может быть полностью интегрирована in продакшн системы
 - **Почему важно:** Обеспечивает практическое применение системы
 - **Плюсы:** Автоматизация, масштабируемость, Monitoring
 - **Минусы:** Сложность разработки, требования к безопасности

---

**Важно:** WAVE2 требует тщательной settings параметров for каждого Timeframe and актива. Use оптимизацию for достижения максимальной производительности.
