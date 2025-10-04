# 13. Анализ SCHR SHORT3 - Создание высокоточной ML-модели

**Цель:** Максимально использовать индикатор SCHR SHORT3 для создания робастной и прибыльной ML-модели с точностью более 95%.

## Что такое SCHR SHORT3?

**Теория:** SCHR SHORT3 представляет собой революционный подход к краткосрочной торговле, который использует алгоритмический анализ для выявления краткосрочных торговых возможностей. Это критически важно для скальпинга и краткосрочной торговли.

**Почему SCHR SHORT3 критичен:**
- **Краткосрочная торговля:** Специализируется на краткосрочных торговых возможностях
- **Высокая точность:** Обеспечивает высокую точность краткосрочных сигналов
- **Алгоритмический анализ:** Использует продвинутые алгоритмы анализа
- **Структурный анализ:** Анализирует краткосрочную структуру рынка

**Математическая основа SCHR SHORT3:**

SCHR SHORT3 основан на комбинации нескольких математических принципов:

1. **Краткосрочная волатильность:** σ_short = √(Σ(ln(P_t/P_{t-1}))² / n)
2. **Краткосрочный моментум:** M_short = (P_t - P_{t-k}) / P_{t-k}
3. **Краткосрочная сила сигнала:** S_short = |M_short| / σ_short
4. **Краткосрочное направление:** D_short = sign(M_short)

Где:
- P_t - цена в момент времени t
- k - период для расчета моментума
- n - окно для расчета волатильности

### Определение и принцип работы

**Теория:** SCHR SHORT3 основан на принципе анализа краткосрочной структуры рынка для выявления краткосрочных торговых возможностей. Это позволяет получать более точные и надежные сигналы по сравнению с традиционными краткосрочными индикаторами.

**SCHR SHORT3** - это продвинутый индикатор для краткосрочной торговли, который использует алгоритмический анализ для определения краткосрочных торговых возможностей. В отличие от простых краткосрочных индикаторов, SCHR SHORT3 анализирует краткосрочную структуру рынка и генерирует высокоточные сигналы.

**Почему SCHR SHORT3 превосходит традиционные индикаторы:**
- **Структурный анализ:** Анализирует краткосрочную структуру рынка
- **Алгоритмический подход:** Использует продвинутые алгоритмы
- **Высокая точность:** Обеспечивает высокую точность сигналов
- **Адаптивность:** Адаптируется к различным рыночным условиям

**Плюсы:**
- Высокая точность сигналов
- Адаптивность к рыночным условиям
- Структурный анализ рынка
- Меньше ложных сигналов

**Минусы:**
- Сложность настройки параметров
- Высокие требования к вычислительным ресурсам
- Необходимость глубокого понимания теории

### Ключевые особенности SCHR SHORT3

**Теория:** Ключевые особенности SCHR SHORT3 определяют его уникальные характеристики для краткосрочной торговли. Эти особенности критически важны для понимания принципов работы индикатора и его применения в торговых стратегиях.

**Почему ключевые особенности важны:**
- **Понимание принципов:** Помогают понять принципы работы индикатора
- **Оптимизация параметров:** Критически важны для оптимизации параметров
- **Адаптация стратегий:** Позволяют адаптировать торговые стратегии
- **Повышение эффективности:** Помогают повысить эффективность торговли

**Плюсы:**
- Четкое понимание принципов
- Возможность оптимизации
- Адаптация стратегий
- Повышение эффективности

**Минусы:**
- Сложность понимания
- Необходимость настройки
- Потенциальные ошибки в применении

**Детальное объяснение кода:**

Данный код создает основной класс `SCHRShort3Analyzer` для анализа краткосрочных сигналов. Каждый параметр имеет критическое значение:

- **short_term_threshold (0.6):** Определяет минимальный уровень уверенности для генерации сигнала. Значение 0.6 означает, что сигнал генерируется только при 60%+ уверенности.
- **short_term_strength (0.7):** Характеризует интенсивность краткосрочного движения. Высокое значение указывает на сильные краткосрочные тренды.
- **short_term_direction (0.8):** Определяет направление краткосрочного движения (1 = вверх, -1 = вниз, 0 = боковое движение).
- **short_term_volatility (1.2):** Множитель волатильности для корректировки сигналов в зависимости от рыночной нестабильности.
- **short_term_momentum (0.9):** Сила краткосрочного импульса, критически важная для определения продолжительности сигнала.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import warnings
warnings.filterwarnings('ignore')

class SCHRShort3Analyzer:
    """
    Анализатор краткосрочных сигналов SCHR SHORT3
    
    Этот класс реализует комплексный анализ краткосрочных торговых сигналов,
    используя алгоритмические методы для выявления краткосрочных возможностей.
    """
    
    def __init__(self):
        """
        Инициализация анализатора с оптимальными параметрами
        
        Параметры подобраны на основе исторического анализа и обеспечивают
        баланс между чувствительностью и стабильностью сигналов.
        """
        self.parameters = {
            'short_term_threshold': 0.6,     # Порог краткосрочного сигнала (60% уверенности)
            'short_term_strength': 0.7,      # Сила краткосрочного сигнала (70% интенсивности)
            'short_term_direction': 0.8,     # Направление краткосрочного сигнала (80% четкости)
            'short_term_volatility': 1.2,   # Волатильность краткосрочного сигнала (120% от базовой)
            'short_term_momentum': 0.9       # Моментум краткосрочного сигнала (90% импульса)
        }
        
        # Дополнительные параметры для анализа
        self.analysis_windows = {
            'micro': 3,      # Микро-анализ (3 периода)
            'short': 5,      # Краткосрочный анализ (5 периодов)
            'medium': 10,    # Среднесрочный анализ (10 периодов)
            'long': 20       # Долгосрочный анализ (20 периодов)
        }
        
        # Инициализация результатов анализа
        self.analysis_results = {}
        self.signal_history = []
        
    def calculate_short_term_volatility(self, prices, window=5):
        """
        Расчет краткосрочной волатильности
        
        Args:
            prices: Массив цен
            window: Окно для расчета волатильности
            
        Returns:
            Массив значений краткосрочной волатильности
        """
        log_returns = np.log(prices / prices.shift(1))
        return log_returns.rolling(window=window).std() * np.sqrt(252)
    
    def calculate_short_term_momentum(self, prices, period=5):
        """
        Расчет краткосрочного моментума
        
        Args:
            prices: Массив цен
            period: Период для расчета моментума
            
        Returns:
            Массив значений краткосрочного моментума
        """
        return (prices - prices.shift(period)) / prices.shift(period)
    
    def generate_short_term_signal(self, data):
        """
        Генерация краткосрочного торгового сигнала
        
        Args:
            data: DataFrame с рыночными данными
            
        Returns:
            Словарь с сигналами и метриками
        """
        # Расчет базовых индикаторов
        volatility = self.calculate_short_term_volatility(data['Close'])
        momentum = self.calculate_short_term_momentum(data['Close'])
        
        # Расчет силы сигнала
        signal_strength = abs(momentum) / volatility
        signal_strength = signal_strength.fillna(0)
        
        # Определение направления
        signal_direction = np.where(momentum > 0, 1, 
                                  np.where(momentum < 0, -1, 0))
        
        # Генерация финального сигнала
        final_signal = np.where(
            signal_strength > self.parameters['short_term_threshold'],
            signal_direction,
            0
        )
        
        return {
            'signal': final_signal,
            'strength': signal_strength,
            'direction': signal_direction,
            'volatility': volatility,
            'momentum': momentum
        }
```

### Структура данных SCHR SHORT3

**Теория:** Структура данных SCHR SHORT3 определяет формат и содержание данных, которые используются для анализа краткосрочных торговых возможностей. Правильная структура данных критически важна для эффективного анализа и обучения ML-моделей.

**Почему структура данных важна:**
- **Стандартизация:** Обеспечивает стандартизацию данных
- **Эффективность анализа:** Повышает эффективность анализа
- **ML-совместимость:** Обеспечивает совместимость с ML-алгоритмами
- **Интерпретируемость:** Облегчает интерпретацию результатов

**Плюсы:**
- Стандартизация данных
- Повышение эффективности
- ML-совместимость
- Улучшение интерпретируемости

**Минусы:**
- Сложность структуры
- Потенциальные проблемы с данными
- Необходимость валидации

**Детальное объяснение структуры данных:**

Структура данных SCHR SHORT3 спроектирована для максимальной эффективности анализа краткосрочных сигналов. Каждая колонка имеет специфическое назначение:

- **short_term_signal:** Основной сигнал (-1=продажа, 0=удержание, 1=покупка)
- **short_term_strength:** Интенсивность сигнала (0-1, где 1 = максимальная сила)
- **short_term_direction:** Направление движения (1=вверх, -1=вниз, 0=боковое)
- **short_term_volatility:** Уровень волатильности для корректировки рисков
- **short_term_momentum:** Сила краткосрочного импульса

```python
# Основные колонки SCHR SHORT3 в parquet файлах
SCHR_SHORT3_COLUMNS = {
    # Основные краткосрочные сигналы
    'short_term_signal': 'Краткосрочный сигнал (-1, 0, 1)',
    'short_term_strength': 'Сила краткосрочного сигнала',
    'short_term_direction': 'Направление краткосрочного сигнала',
    'short_term_volatility': 'Волатильность краткосрочного сигнала',
    'short_term_momentum': 'Моментум краткосрочного сигнала',
    
    # Дополнительные сигналы
    'short_buy_signal': 'Краткосрочный сигнал покупки',
    'short_sell_signal': 'Краткосрочный сигнал продажи',
    'short_hold_signal': 'Краткосрочный сигнал удержания',
    'short_reverse_signal': 'Краткосрочный сигнал разворота',
    
    # Краткосрочная статистика
    'short_hits': 'Количество краткосрочных касаний',
    'short_breaks': 'Количество краткосрочных пробоев',
    'short_bounces': 'Количество краткосрочных отскоков',
    'short_accuracy': 'Точность краткосрочных сигналов'
}

def create_schr_short3_data_structure():
    """
    Создание структуры данных для SCHR SHORT3 анализа
    
    Эта функция создает полную структуру данных с примерами значений
    для демонстрации работы с SCHR SHORT3 индикаторами.
    """
    # Создание примера данных
    np.random.seed(42)
    n_samples = 1000
    
    # Базовые рыночные данные
    dates = pd.date_range('2023-01-01', periods=n_samples, freq='1min')
    
    # Генерация реалистичных ценовых данных
    price_base = 100.0
    returns = np.random.normal(0, 0.001, n_samples)
    prices = [price_base]
    
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    # Создание DataFrame
    data = pd.DataFrame({
        'timestamp': dates,
        'Open': prices,
        'High': [p * (1 + abs(np.random.normal(0, 0.002))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.002))) for p in prices],
        'Close': prices,
        'Volume': np.random.randint(1000, 10000, n_samples)
    })
    
    # Расчет SCHR SHORT3 индикаторов
    analyzer = SCHRShort3Analyzer()
    signals = analyzer.generate_short_term_signal(data)
    
    # Добавление SCHR SHORT3 колонок
    data['short_term_signal'] = signals['signal']
    data['short_term_strength'] = signals['strength']
    data['short_term_direction'] = signals['direction']
    data['short_term_volatility'] = signals['volatility']
    data['short_term_momentum'] = signals['momentum']
    
    # Дополнительные сигналы
    data['short_buy_signal'] = (data['short_term_signal'] == 1).astype(int)
    data['short_sell_signal'] = (data['short_term_signal'] == -1).astype(int)
    data['short_hold_signal'] = (data['short_term_signal'] == 0).astype(int)
    data['short_reverse_signal'] = (data['short_term_signal'] != data['short_term_signal'].shift(1)).astype(int)
    
    # Статистика
    data['short_hits'] = data['short_term_signal'].rolling(10).apply(lambda x: (x != 0).sum())
    data['short_breaks'] = data['short_reverse_signal'].rolling(10).sum()
    data['short_bounces'] = ((data['short_term_signal'] == 1) & (data['short_term_signal'].shift(1) == -1)).rolling(10).sum()
    
    # Расчет точности (упрощенный)
    future_returns = data['Close'].pct_change().shift(-1)
    correct_signals = (
        ((data['short_term_signal'] == 1) & (future_returns > 0)) |
        ((data['short_term_signal'] == -1) & (future_returns < 0)) |
        ((data['short_term_signal'] == 0) & (abs(future_returns) < 0.001))
    )
    data['short_accuracy'] = correct_signals.rolling(20).mean() * 100
    
    return data

# Пример использования
if __name__ == "__main__":
    # Создание данных
    schr_data = create_schr_short3_data_structure()
    
    # Вывод информации о данных
    print("SCHR SHORT3 Data Structure:")
    print(f"Shape: {schr_data.shape}")
    print(f"Columns: {list(schr_data.columns)}")
    print("\nFirst 5 rows:")
    print(schr_data.head())
    
    # Статистика по сигналам
    print("\nSignal Statistics:")
    print(f"Buy signals: {schr_data['short_buy_signal'].sum()}")
    print(f"Sell signals: {schr_data['short_sell_signal'].sum()}")
    print(f"Hold signals: {schr_data['short_hold_signal'].sum()}")
    print(f"Average accuracy: {schr_data['short_accuracy'].mean():.2f}%")
```

## Анализ SCHR SHORT3 по таймфреймам

**Теория:** Анализ SCHR SHORT3 по различным таймфреймам критически важен для понимания поведения индикатора на разных временных горизонтах. Каждый таймфрейм требует специфических параметров и подходов для максимальной эффективности.

**Почему анализ по таймфреймам критичен:**
- **Оптимизация производительности:** Каждый таймфрейм требует специфических параметров
- **Снижение рисков:** Различные таймфреймы имеют разные уровни риска
- **Повышение точности:** Специфические параметры повышают точность
- **Адаптация стратегий:** Позволяет адаптировать стратегии к таймфреймам

### M1 (1 минута) - Скальпинг

**Теория:** M1 таймфрейм представляет собой наиболее агрессивный подход к краткосрочной торговле, где каждое движение цены может быть торговой возможностью. Это требует специальных параметров и подходов для минимизации рисков.

**Почему M1 анализ важен:**
- **Максимальная частота:** Предоставляет максимальное количество торговых возможностей
- **Скальпинг:** Идеален для скальпинга
- **Быстрые сигналы:** Обеспечивает быстрые торговые сигналы
- **Высокие риски:** Требует особого внимания к управлению рисками

**Плюсы:**
- Максимальная частота сигналов
- Идеален для скальпинга
- Быстрые торговые возможности
- Высокий потенциал прибыли

**Минусы:**
- Высокие риски
- Требует постоянного внимания
- Высокие комиссии
- Потенциальный стресс

**Детальное объяснение M1 анализа:**

M1 (1-минутный) таймфрейм представляет собой наиболее агрессивный подход к краткосрочной торговле. Параметры специально настроены для:

- **Низкий порог (0.4):** Позволяет улавливать даже слабые краткосрочные движения
- **Высокая волатильность (1.5):** Учитывает повышенную нестабильность на M1
- **Быстрая реакция:** Сигналы генерируются быстрее для скальпинга

```python
class SCHRShort3M1Analysis:
    """
    Анализ SCHR SHORT3 на 1-минутном таймфрейме для скальпинга
    
    Этот класс специализируется на анализе кратчайших временных интервалов,
    обеспечивая максимальную частоту торговых сигналов для скальпинга.
    """
    
    def __init__(self):
        self.timeframe = 'M1'
        self.optimal_params = {
            'short_term_threshold': 0.4,    # Более низкий порог для M1 (40% уверенности)
            'short_term_strength': 0.5,     # Меньшая сила сигнала (50% интенсивности)
            'short_term_direction': 0.6,   # Меньшее направление (60% четкости)
            'short_term_volatility': 1.5,  # Высокая волатильность (150% от базовой)
            'short_term_momentum': 0.7     # Меньший моментум (70% импульса)
        }
        
        # Специфичные параметры для M1
        self.micro_windows = [1, 2, 3, 5]  # Окна для микро-анализа
        self.scalping_threshold = 0.001    # Минимальное движение для скальпинга
        
    def analyze_m1_features(self, data):
        """
        Анализ признаков для M1 таймфрейма
        
        Args:
            data: DataFrame с рыночными данными на M1
            
        Returns:
            Словарь с извлеченными признаками
        """
        features = {}
        
        # Микро-краткосрочные сигналы
        features['micro_short_signals'] = self._detect_micro_short_signals(data)
        
        # Быстрые краткосрочные паттерны
        features['fast_short_patterns'] = self._detect_fast_short_patterns(data)
        
        # Микро-краткосрочные отскоки
        features['micro_short_bounces'] = self._detect_micro_short_bounces(data)
        
        # Скальпинг краткосрочные сигналы
        features['scalping_short_signals'] = self._calculate_scalping_short_signals(data)
        
        # Микро-волатильность
        features['micro_volatility'] = self._calculate_micro_volatility(data)
        
        # Микро-моментум
        features['micro_momentum'] = self._calculate_micro_momentum(data)
        
        return features
    
    def _detect_micro_short_signals(self, data):
        """
        Детекция микро-краткосрочных сигналов
        
        Анализирует самые краткие временные интервалы для выявления
        мгновенных торговых возможностей.
        """
        signals = []
        
        for window in self.micro_windows:
            # Расчет микро-сигналов для каждого окна
            micro_returns = data['Close'].pct_change(window)
            micro_volatility = data['Close'].rolling(window).std()
            
            # Нормализация сигналов
            normalized_signals = micro_returns / micro_volatility
            normalized_signals = normalized_signals.fillna(0)
            
            # Генерация сигналов
            micro_signal = np.where(
                abs(normalized_signals) > self.optimal_params['short_term_threshold'],
                np.sign(normalized_signals),
                0
            )
            
            signals.append({
                'window': window,
                'signals': micro_signal,
                'strength': abs(normalized_signals),
                'returns': micro_returns
            })
        
        return signals
    
    def _detect_fast_short_patterns(self, data):
        """
        Детекция быстрых краткосрочных паттернов
        
        Выявляет повторяющиеся паттерны в краткосрочных движениях цены.
        """
        patterns = {}
        
        # Паттерн "V" (быстрый разворот)
        price_changes = data['Close'].pct_change()
        v_pattern = (
            (price_changes.shift(1) < -0.001) &  # Предыдущий период - падение
            (price_changes > 0.001)              # Текущий период - рост
        )
        patterns['v_pattern'] = v_pattern.astype(int)
        
        # Паттерн "Inverted V" (быстрый пик)
        inverted_v_pattern = (
            (price_changes.shift(1) > 0.001) &   # Предыдущий период - рост
            (price_changes < -0.001)             # Текущий период - падение
        )
        patterns['inverted_v_pattern'] = inverted_v_pattern.astype(int)
        
        # Паттерн "Doji" (неопределенность)
        doji_pattern = (
            abs(data['Open'] - data['Close']) / data['Close'] < 0.0001
        )
        patterns['doji_pattern'] = doji_pattern.astype(int)
        
        return patterns
    
    def _detect_micro_short_bounces(self, data):
        """
        Детекция микро-краткосрочных отскоков
        
        Выявляет быстрые отскоки от уровней поддержки/сопротивления.
        """
        bounces = {}
        
        # Расчет скользящих максимумов и минимумов
        rolling_max = data['High'].rolling(5).max()
        rolling_min = data['Low'].rolling(5).min()
        
        # Отскок от минимума
        bounce_from_low = (
            (data['Low'] <= rolling_min.shift(1)) &  # Касание минимума
            (data['Close'] > data['Low'])            # Закрытие выше минимума
        )
        bounces['bounce_from_low'] = bounce_from_low.astype(int)
        
        # Отскок от максимума
        bounce_from_high = (
            (data['High'] >= rolling_max.shift(1)) &  # Касание максимума
            (data['Close'] < data['High'])            # Закрытие ниже максимума
        )
        bounces['bounce_from_high'] = bounce_from_high.astype(int)
        
        return bounces
    
    def _calculate_scalping_short_signals(self, data):
        """
        Расчет скальпинг краткосрочных сигналов
        
        Генерирует сигналы специально для скальпинга с учетом
        минимальных движений и быстрых изменений.
        """
        # Микро-изменения цены
        micro_changes = data['Close'].pct_change()
        
        # Скальпинг сигналы на основе микро-изменений
        scalping_signals = np.where(
            abs(micro_changes) > self.scalping_threshold,
            np.sign(micro_changes),
            0
        )
        
        # Фильтрация по силе сигнала
        signal_strength = abs(micro_changes) / data['Close'].rolling(3).std()
        filtered_signals = np.where(
            signal_strength > self.optimal_params['short_term_strength'],
            scalping_signals,
            0
        )
        
        return {
            'signals': filtered_signals,
            'strength': signal_strength,
            'changes': micro_changes
        }
    
    def _calculate_micro_volatility(self, data):
        """Расчет микро-волатильности"""
        return data['Close'].rolling(3).std() / data['Close']
    
    def _calculate_micro_momentum(self, data):
        """Расчет микро-моментума"""
        return data['Close'].pct_change(3)

# Пример использования M1 анализа
def demonstrate_m1_analysis():
    """Демонстрация M1 анализа"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Инициализация анализатора
    m1_analyzer = SCHRShort3M1Analysis()
    
    # Анализ признаков
    features = m1_analyzer.analyze_m1_features(test_data)
    
    print("M1 Analysis Results:")
    print(f"Micro signals detected: {len(features['micro_short_signals'])}")
    print(f"Fast patterns found: {sum(features['fast_short_patterns']['v_pattern'])}")
    print(f"Micro bounces: {sum(features['micro_short_bounces']['bounce_from_low'])}")
    
    return features

if __name__ == "__main__":
    demonstrate_m1_analysis()
```

### M5 (5 минут) - Краткосрочная торговля

**Теория:** M5 таймфрейм представляет собой оптимальный баланс между частотой сигналов и их качеством для краткосрочной торговли. Это наиболее популярный таймфрейм для краткосрочных торговых стратегий.

**Почему M5 анализ важен:**
- **Оптимальный баланс:** Хорошее соотношение частоты и качества сигналов
- **Снижение шума:** Меньше рыночного шума по сравнению с M1
- **Краткосрочная торговля:** Идеален для краткосрочной торговли
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

**Детальное объяснение M5 анализа:**

M5 (5-минутный) таймфрейм обеспечивает оптимальный баланс между частотой сигналов и их качеством. Параметры настроены для:

- **Средний порог (0.5):** Баланс между чувствительностью и стабильностью
- **Средняя волатильность (1.3):** Умеренная корректировка на волатильность
- **Стабильные сигналы:** Меньше ложных сигналов по сравнению с M1

```python
class SCHRShort3M5Analysis:
    """
    Анализ SCHR SHORT3 на 5-минутном таймфрейме
    
    Этот класс обеспечивает оптимальный баланс между частотой сигналов
    и их качеством для краткосрочной торговли.
    """
    
    def __init__(self):
        self.timeframe = 'M5'
        self.optimal_params = {
            'short_term_threshold': 0.5,    # Средний порог (50% уверенности)
            'short_term_strength': 0.6,     # Средняя сила (60% интенсивности)
            'short_term_direction': 0.7,    # Среднее направление (70% четкости)
            'short_term_volatility': 1.3,   # Средняя волатильность (130% от базовой)
            'short_term_momentum': 0.8      # Средний моментум (80% импульса)
        }
        
        # Специфичные параметры для M5
        self.short_windows = [3, 5, 8, 13]  # Окна для краткосрочного анализа
        self.impulse_threshold = 0.002      # Минимальное движение для импульса
        
    def analyze_m5_features(self, data):
        """
        Анализ признаков для M5 таймфрейма
        
        Args:
            data: DataFrame с рыночными данными на M5
            
        Returns:
            Словарь с извлеченными признаками
        """
        features = {}
        
        # Краткосрочные паттерны
        features['short_patterns'] = self._detect_short_patterns(data)
        
        # Быстрые импульсы
        features['quick_impulses'] = self._detect_quick_impulses(data)
        
        # Краткосрочная волатильность
        features['short_volatility'] = self._analyze_short_volatility(data)
        
        # Краткосрочные тренды
        features['short_trends'] = self._detect_short_trends(data)
        
        # Краткосрочные уровни
        features['short_levels'] = self._calculate_short_levels(data)
        
        return features
    
    def _detect_short_patterns(self, data):
        """
        Детекция краткосрочных паттернов
        
        Выявляет классические краткосрочные паттерны на M5 таймфрейме.
        """
        patterns = {}
        
        # Паттерн "Hammer" (молот)
        hammer = (
            (data['Close'] > data['Open']) &  # Бычий день
            (data['Low'] < data['Open'] - 2 * (data['Open'] - data['Close'])) &  # Длинная тень
            (data['High'] - data['Close']) < (data['Open'] - data['Close'])  # Короткая верхняя тень
        )
        patterns['hammer'] = hammer.astype(int)
        
        # Паттерн "Shooting Star" (падающая звезда)
        shooting_star = (
            (data['Open'] > data['Close']) &  # Медвежий день
            (data['High'] > data['Open'] + 2 * (data['Open'] - data['Close'])) &  # Длинная верхняя тень
            (data['Close'] - data['Low']) < (data['Open'] - data['Close'])  # Короткая нижняя тень
        )
        patterns['shooting_star'] = shooting_star.astype(int)
        
        # Паттерн "Doji" (неопределенность)
        doji = (
            abs(data['Open'] - data['Close']) / data['Close'] < 0.0005
        )
        patterns['doji'] = doji.astype(int)
        
        # Паттерн "Engulfing" (поглощение)
        bullish_engulfing = (
            (data['Close'].shift(1) < data['Open'].shift(1)) &  # Предыдущий день - медвежий
            (data['Close'] > data['Open']) &  # Текущий день - бычий
            (data['Open'] < data['Close'].shift(1)) &  # Открытие ниже закрытия предыдущего
            (data['Close'] > data['Open'].shift(1))  # Закрытие выше открытия предыдущего
        )
        patterns['bullish_engulfing'] = bullish_engulfing.astype(int)
        
        bearish_engulfing = (
            (data['Close'].shift(1) > data['Open'].shift(1)) &  # Предыдущий день - бычий
            (data['Close'] < data['Open']) &  # Текущий день - медвежий
            (data['Open'] > data['Close'].shift(1)) &  # Открытие выше закрытия предыдущего
            (data['Close'] < data['Open'].shift(1))  # Закрытие ниже открытия предыдущего
        )
        patterns['bearish_engulfing'] = bearish_engulfing.astype(int)
        
        return patterns
    
    def _detect_quick_impulses(self, data):
        """
        Детекция быстрых импульсов
        
        Выявляет краткосрочные импульсные движения цены.
        """
        impulses = {}
        
        # Быстрый рост
        quick_rise = (
            (data['Close'] - data['Open']) / data['Open'] > self.impulse_threshold
        )
        impulses['quick_rise'] = quick_rise.astype(int)
        
        # Быстрое падение
        quick_fall = (
            (data['Open'] - data['Close']) / data['Open'] > self.impulse_threshold
        )
        impulses['quick_fall'] = quick_fall.astype(int)
        
        # Импульсная волатильность
        impulse_volatility = data['High'] - data['Low']
        avg_volatility = impulse_volatility.rolling(20).mean()
        high_volatility_impulse = (impulse_volatility > 1.5 * avg_volatility)
        impulses['high_volatility_impulse'] = high_volatility_impulse.astype(int)
        
        return impulses
    
    def _analyze_short_volatility(self, data):
        """
        Анализ краткосрочной волатильности
        
        Рассчитывает различные метрики волатильности для M5 таймфрейма.
        """
        volatility_metrics = {}
        
        # Стандартная волатильность
        returns = data['Close'].pct_change()
        volatility_metrics['std_volatility'] = returns.rolling(20).std()
        
        # ATR (Average True Range)
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift(1))
        low_close = np.abs(data['Low'] - data['Close'].shift(1))
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        volatility_metrics['atr'] = true_range.rolling(14).mean()
        
        # Нормализованная волатильность
        volatility_metrics['normalized_volatility'] = (
            volatility_metrics['std_volatility'] / data['Close']
        )
        
        # Волатильность волатильности
        volatility_metrics['vol_of_vol'] = volatility_metrics['std_volatility'].rolling(10).std()
        
        return volatility_metrics
    
    def _detect_short_trends(self, data):
        """
        Детекция краткосрочных трендов
        
        Определяет направление краткосрочных трендов на M5.
        """
        trends = {}
        
        # Скользящие средние для трендов
        sma_5 = data['Close'].rolling(5).mean()
        sma_10 = data['Close'].rolling(10).mean()
        sma_20 = data['Close'].rolling(20).mean()
        
        # Восходящий тренд
        uptrend = (
            (sma_5 > sma_10) & 
            (sma_10 > sma_20) & 
            (data['Close'] > sma_5)
        )
        trends['uptrend'] = uptrend.astype(int)
        
        # Нисходящий тренд
        downtrend = (
            (sma_5 < sma_10) & 
            (sma_10 < sma_20) & 
            (data['Close'] < sma_5)
        )
        trends['downtrend'] = downtrend.astype(int)
        
        # Боковой тренд
        sideways = ~(uptrend | downtrend)
        trends['sideways'] = sideways.astype(int)
        
        # Сила тренда
        trend_strength = abs(sma_5 - sma_20) / sma_20
        trends['trend_strength'] = trend_strength
        
        return trends
    
    def _calculate_short_levels(self, data):
        """
        Расчет краткосрочных уровней поддержки/сопротивления
        
        Определяет ключевые уровни для краткосрочной торговли.
        """
        levels = {}
        
        # Скользящие максимумы и минимумы
        rolling_max = data['High'].rolling(20).max()
        rolling_min = data['Low'].rolling(20).min()
        
        # Уровни сопротивления
        resistance = (data['High'] >= rolling_max.shift(1))
        levels['resistance'] = resistance.astype(int)
        
        # Уровни поддержки
        support = (data['Low'] <= rolling_min.shift(1))
        levels['support'] = support.astype(int)
        
        # Пробои уровней
        resistance_break = (data['Close'] > rolling_max.shift(1))
        support_break = (data['Close'] < rolling_min.shift(1))
        
        levels['resistance_break'] = resistance_break.astype(int)
        levels['support_break'] = support_break.astype(int)
        
        return levels

# Пример использования M5 анализа
def demonstrate_m5_analysis():
    """Демонстрация M5 анализа"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Инициализация анализатора
    m5_analyzer = SCHRShort3M5Analysis()
    
    # Анализ признаков
    features = m5_analyzer.analyze_m5_features(test_data)
    
    print("M5 Analysis Results:")
    print(f"Short patterns detected: {len(features['short_patterns'])}")
    print(f"Quick impulses: {sum(features['quick_impulses']['quick_rise'])}")
    print(f"Average volatility: {features['short_volatility']['std_volatility'].mean():.4f}")
    print(f"Uptrend periods: {sum(features['short_trends']['uptrend'])}")
    
    return features

if __name__ == "__main__":
    demonstrate_m5_analysis()
```

### H1 (1 час) - Среднесрочная торговля

**Теория:** H1 таймфрейм представляет собой среднесрочный подход к краткосрочной торговле, где сигналы более стабильны, но менее часты. Это идеально подходит для трейдеров, которые не могут постоянно следить за рынком.

**Почему H1 анализ важен:**
- **Стабильность:** Более стабильные сигналы
- **Среднесрочная торговля:** Идеален для среднесрочной торговли
- **Меньше шума:** Значительно меньше рыночного шума
- **Удобство:** Более удобен для трейдеров

**Плюсы:**
- Высокая стабильность сигналов
- Идеален для среднесрочной торговли
- Минимальный рыночный шум
- Удобство использования

**Минусы:**
- Меньше торговых возможностей
- Более медленные сигналы
- Потенциальные упущенные возможности

**Детальное объяснение H1 анализа:**

H1 (часовой) таймфрейм обеспечивает стабильные сигналы с меньшей частотой. Параметры настроены для:

- **Стандартный порог (0.6):** Высокая уверенность в сигналах
- **Стандартная волатильность (1.2):** Умеренная корректировка
- **Стабильные сигналы:** Меньше ложных срабатываний

```python
class SCHRShort3H1Analysis:
    """
    Анализ SCHR SHORT3 на часовом таймфрейме
    
    Этот класс обеспечивает стабильные краткосрочные сигналы
    для среднесрочной торговли с меньшей частотой, но высокой точностью.
    """
    
    def __init__(self):
        self.timeframe = 'H1'
        self.optimal_params = {
            'short_term_threshold': 0.6,    # Стандартный порог (60% уверенности)
            'short_term_strength': 0.7,     # Стандартная сила (70% интенсивности)
            'short_term_direction': 0.8,    # Стандартное направление (80% четкости)
            'short_term_volatility': 1.2,   # Стандартная волатильность (120% от базовой)
            'short_term_momentum': 0.9      # Стандартный моментум (90% импульса)
        }
        
        # Специфичные параметры для H1
        self.medium_windows = [5, 10, 20, 50]  # Окна для среднесрочного анализа
        self.trend_threshold = 0.005           # Минимальное движение для тренда
        
    def analyze_h1_features(self, data):
        """
        Анализ признаков для H1 таймфрейма
        
        Args:
            data: DataFrame с рыночными данными на H1
            
        Returns:
            Словарь с извлеченными признаками
        """
        features = {}
        
        # Среднесрочные краткосрочные сигналы
        features['medium_short_signals'] = self._detect_medium_short_signals(data)
        
        # Трендовые краткосрочные сигналы
        features['trend_short_signals'] = self._detect_trend_short_signals(data)
        
        # Среднесрочная краткосрочная волатильность
        features['medium_short_volatility'] = self._analyze_medium_short_volatility(data)
        
        # Среднесрочные паттерны
        features['medium_patterns'] = self._detect_medium_patterns(data)
        
        # Среднесрочные уровни
        features['medium_levels'] = self._calculate_medium_levels(data)
        
        return features
    
    def _detect_medium_short_signals(self, data):
        """
        Детекция среднесрочных краткосрочных сигналов
        
        Выявляет краткосрочные сигналы в контексте среднесрочных трендов.
        """
        signals = {}
        
        # Краткосрочные сигналы с учетом среднесрочного контекста
        short_returns = data['Close'].pct_change(5)  # 5-часовые изменения
        medium_returns = data['Close'].pct_change(20)  # 20-часовые изменения
        
        # Согласованность краткосрочных и среднесрочных сигналов
        signal_consistency = (
            (short_returns > 0) & (medium_returns > 0) |  # Оба восходящие
            (short_returns < 0) & (medium_returns < 0)    # Оба нисходящие
        )
        signals['consistency'] = signal_consistency.astype(int)
        
        # Сила краткосрочного сигнала в среднесрочном контексте
        signal_strength = abs(short_returns) / abs(medium_returns)
        signal_strength = signal_strength.fillna(0)
        signals['strength'] = signal_strength
        
        # Направление краткосрочного сигнала
        signal_direction = np.where(short_returns > 0, 1, 
                                  np.where(short_returns < 0, -1, 0))
        signals['direction'] = signal_direction
        
        return signals
    
    def _detect_trend_short_signals(self, data):
        """
        Детекция трендовых краткосрочных сигналов
        
        Выявляет краткосрочные сигналы, которые соответствуют общему тренду.
        """
        trend_signals = {}
        
        # Скользящие средние для определения тренда
        sma_10 = data['Close'].rolling(10).mean()
        sma_30 = data['Close'].rolling(30).mean()
        sma_50 = data['Close'].rolling(50).mean()
        
        # Определение тренда
        uptrend = (sma_10 > sma_30) & (sma_30 > sma_50)
        downtrend = (sma_10 < sma_30) & (sma_30 < sma_50)
        
        # Краткосрочные сигналы в восходящем тренде
        short_returns = data['Close'].pct_change(3)
        uptrend_signals = uptrend & (short_returns > self.trend_threshold)
        trend_signals['uptrend_signals'] = uptrend_signals.astype(int)
        
        # Краткосрочные сигналы в нисходящем тренде
        downtrend_signals = downtrend & (short_returns < -self.trend_threshold)
        trend_signals['downtrend_signals'] = downtrend_signals.astype(int)
        
        # Противоположные сигналы (потенциальные развороты)
        reversal_signals = (
            (uptrend & (short_returns < -self.trend_threshold)) |
            (downtrend & (short_returns > self.trend_threshold))
        )
        trend_signals['reversal_signals'] = reversal_signals.astype(int)
        
        # Сила тренда
        trend_strength = abs(sma_10 - sma_50) / sma_50
        trend_signals['trend_strength'] = trend_strength
        
        return trend_signals
    
    def _analyze_medium_short_volatility(self, data):
        """
        Анализ среднесрочной краткосрочной волатильности
        
        Рассчитывает волатильность в контексте среднесрочных движений.
        """
        volatility_metrics = {}
        
        # Краткосрочная волатильность
        short_volatility = data['Close'].pct_change().rolling(5).std()
        
        # Среднесрочная волатильность
        medium_volatility = data['Close'].pct_change().rolling(20).std()
        
        # Отношение краткосрочной к среднесрочной волатильности
        volatility_ratio = short_volatility / medium_volatility
        volatility_ratio = volatility_ratio.fillna(1)
        volatility_metrics['volatility_ratio'] = volatility_ratio
        
        # Нормализованная волатильность
        volatility_metrics['normalized_volatility'] = (
            short_volatility / data['Close']
        )
        
        # Волатильность волатильности
        volatility_metrics['vol_of_vol'] = short_volatility.rolling(10).std()
        
        # ATR для среднесрочного анализа
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift(1))
        low_close = np.abs(data['Low'] - data['Close'].shift(1))
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        volatility_metrics['atr'] = true_range.rolling(14).mean()
        
        return volatility_metrics
    
    def _detect_medium_patterns(self, data):
        """
        Детекция среднесрочных паттернов
        
        Выявляет классические среднесрочные паттерны на H1 таймфрейме.
        """
        patterns = {}
        
        # Паттерн "Head and Shoulders" (голова и плечи)
        # Упрощенная версия для демонстрации
        rolling_max = data['High'].rolling(20).max()
        head_shoulders = (
            (data['High'] == rolling_max) &  # Пик
            (data['High'].shift(10) < data['High']) &  # Левый плечо ниже головы
            (data['High'].shift(-10) < data['High'])   # Правое плечо ниже головы
        )
        patterns['head_shoulders'] = head_shoulders.astype(int)
        
        # Паттерн "Double Top" (двойная вершина)
        double_top = (
            (data['High'] == rolling_max) &  # Первая вершина
            (data['High'].shift(-10) == rolling_max.shift(-10)) &  # Вторая вершина
            (abs(data['High'] - data['High'].shift(-10)) / data['High'] < 0.01)  # Близкие по высоте
        )
        patterns['double_top'] = double_top.astype(int)
        
        # Паттерн "Double Bottom" (двойное дно)
        rolling_min = data['Low'].rolling(20).min()
        double_bottom = (
            (data['Low'] == rolling_min) &  # Первое дно
            (data['Low'].shift(-10) == rolling_min.shift(-10)) &  # Второе дно
            (abs(data['Low'] - data['Low'].shift(-10)) / data['Low'] < 0.01)  # Близкие по глубине
        )
        patterns['double_bottom'] = double_bottom.astype(int)
        
        # Паттерн "Triangle" (треугольник)
        # Упрощенная версия - сходящиеся максимумы и минимумы
        max_trend = data['High'].rolling(10).max()
        min_trend = data['Low'].rolling(10).min()
        triangle = (
            (max_trend == max_trend.rolling(20).max()) &  # Максимумы не растут
            (min_trend == min_trend.rolling(20).min())    # Минимумы не падают
        )
        patterns['triangle'] = triangle.astype(int)
        
        return patterns
    
    def _calculate_medium_levels(self, data):
        """
        Расчет среднесрочных уровней поддержки/сопротивления
        
        Определяет ключевые уровни для среднесрочной торговли.
        """
        levels = {}
        
        # Скользящие максимумы и минимумы для среднесрочного анализа
        rolling_max = data['High'].rolling(50).max()
        rolling_min = data['Low'].rolling(50).min()
        
        # Уровни сопротивления
        resistance = (data['High'] >= rolling_max.shift(1))
        levels['resistance'] = resistance.astype(int)
        
        # Уровни поддержки
        support = (data['Low'] <= rolling_min.shift(1))
        levels['support'] = support.astype(int)
        
        # Пробои уровней
        resistance_break = (data['Close'] > rolling_max.shift(1))
        support_break = (data['Close'] < rolling_min.shift(1))
        
        levels['resistance_break'] = resistance_break.astype(int)
        levels['support_break'] = support_break.astype(int)
        
        # Сила уровней (количество касаний)
        resistance_touches = resistance.rolling(100).sum()
        support_touches = support.rolling(100).sum()
        
        levels['resistance_strength'] = resistance_touches
        levels['support_strength'] = support_touches
        
        return levels

# Пример использования H1 анализа
def demonstrate_h1_analysis():
    """Демонстрация H1 анализа"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Инициализация анализатора
    h1_analyzer = SCHRShort3H1Analysis()
    
    # Анализ признаков
    features = h1_analyzer.analyze_h1_features(test_data)
    
    print("H1 Analysis Results:")
    print(f"Medium signals detected: {len(features['medium_short_signals'])}")
    print(f"Trend signals: {sum(features['trend_short_signals']['uptrend_signals'])}")
    print(f"Average volatility ratio: {features['medium_short_volatility']['volatility_ratio'].mean():.4f}")
    print(f"Patterns found: {sum(features['medium_patterns']['head_shoulders'])}")
    
    return features

if __name__ == "__main__":
    demonstrate_h1_analysis()
```

## Создание признаков для ML

**Теория:** Создание признаков для машинного обучения на основе SCHR SHORT3 является критически важным этапом для достижения высокой точности предсказаний. Качественные признаки определяют успех ML-модели.

**Почему создание признаков критично:**
- **Качество данных:** Качественные признаки определяют качество модели
- **Точность предсказаний:** Хорошие признаки повышают точность предсказаний
- **Робастность:** Правильные признаки обеспечивают робастность модели
- **Интерпретируемость:** Понятные признаки облегчают интерпретацию результатов

### 1. Базовые признаки SCHR SHORT3

**Теория:** Базовые признаки SCHR SHORT3 представляют собой фундаментальные компоненты для анализа краткосрочных торговых возможностей. Они обеспечивают основу для более сложных признаков и являются основой для ML-модели.

**Почему базовые признаки важны:**
- **Фундаментальная основа:** Обеспечивают базовую информацию о краткосрочных сигналах
- **Простота интерпретации:** Легко понимаются и интерпретируются
- **Стабильность:** Обеспечивают стабильную основу для анализа
- **Эффективность:** Минимальные вычислительные требования

**Плюсы:**
- Фундаментальная основа
- Простота интерпретации
- Стабильность
- Эффективность

**Минусы:**
- Ограниченная информативность
- Потенциальная потеря информации
- Необходимость дополнительных признаков

**Детальное объяснение создания признаков:**

Создание признаков для ML является критически важным этапом. Каждый тип признаков решает специфическую задачу:

- **Базовые признаки:** Фундаментальная информация о краткосрочных сигналах
- **Лаговые признаки:** Учитывают временные зависимости
- **Скользящие признаки:** Выявляют тренды и паттерны

```python
class SCHRShort3FeatureEngineer:
    """
    Создание признаков на основе SCHR SHORT3
    
    Этот класс обеспечивает комплексное создание признаков для машинного обучения,
    включая базовые, лаговые, скользящие и продвинутые признаки.
    """
    
    def __init__(self):
        self.lag_periods = [1, 2, 3, 5, 10, 20]  # Периоды для лаговых признаков
        self.rolling_windows = [5, 10, 20, 50]   # Окна для скользящих признаков
        self.feature_names = []  # Список созданных признаков
    
    def create_basic_features(self, data):
        """
        Создание базовых признаков
        
        Базовые признаки представляют собой фундаментальные компоненты
        для анализа краткосрочных торговых сигналов.
        
        Args:
            data: DataFrame с рыночными данными и SCHR SHORT3 индикаторами
            
        Returns:
            DataFrame с базовыми признаками
        """
        features = pd.DataFrame(index=data.index)
        
        # 1. Основные краткосрочные сигналы
        features['short_term_signal'] = data['short_term_signal']
        features['short_term_strength'] = data['short_term_strength']
        features['short_term_direction'] = data['short_term_direction']
        features['short_term_volatility'] = data['short_term_volatility']
        features['short_term_momentum'] = data['short_term_momentum']
        
        # 2. Дополнительные сигналы
        features['short_buy_signal'] = data['short_buy_signal']
        features['short_sell_signal'] = data['short_sell_signal']
        features['short_hold_signal'] = data['short_hold_signal']
        features['short_reverse_signal'] = data['short_reverse_signal']
        
        # 3. Статистика
        features['short_hits'] = data['short_hits']
        features['short_breaks'] = data['short_breaks']
        features['short_bounces'] = data['short_bounces']
        features['short_accuracy'] = data['short_accuracy']
        
        # 4. Дополнительные базовые признаки
        features['price_change'] = data['Close'].pct_change()
        features['volume_change'] = data['Volume'].pct_change()
        features['high_low_ratio'] = data['High'] / data['Low']
        features['close_open_ratio'] = data['Close'] / data['Open']
        
        # 5. Нормализованные признаки
        features['normalized_strength'] = data['short_term_strength'] / data['short_term_strength'].rolling(20).mean()
        features['normalized_volatility'] = data['short_term_volatility'] / data['short_term_volatility'].rolling(20).mean()
        features['normalized_momentum'] = data['short_term_momentum'] / data['short_term_momentum'].rolling(20).mean()
        
        self.feature_names.extend(features.columns.tolist())
        return features
    
    def create_lag_features(self, data):
        """
        Создание лаговых признаков
        
        Лаговые признаки учитывают временные зависимости и помогают
        модели учитывать историческую информацию.
        
        Args:
            data: DataFrame с рыночными данными
            
        Returns:
            DataFrame с лаговыми признаками
        """
        features = pd.DataFrame(index=data.index)
        
        for lag in self.lag_periods:
            # Лаги краткосрочных сигналов
            features[f'short_term_signal_lag_{lag}'] = data['short_term_signal'].shift(lag)
            features[f'short_term_strength_lag_{lag}'] = data['short_term_strength'].shift(lag)
            features[f'short_term_direction_lag_{lag}'] = data['short_term_direction'].shift(lag)
            features[f'short_term_volatility_lag_{lag}'] = data['short_term_volatility'].shift(lag)
            features[f'short_term_momentum_lag_{lag}'] = data['short_term_momentum'].shift(lag)
            
            # Изменения краткосрочных сигналов
            features[f'short_term_signal_change_{lag}'] = data['short_term_signal'] - data['short_term_signal'].shift(lag)
            features[f'short_term_strength_change_{lag}'] = data['short_term_strength'] - data['short_term_strength'].shift(lag)
            features[f'short_term_direction_change_{lag}'] = data['short_term_direction'] - data['short_term_direction'].shift(lag)
            features[f'short_term_volatility_change_{lag}'] = data['short_term_volatility'] - data['short_term_volatility'].shift(lag)
            features[f'short_term_momentum_change_{lag}'] = data['short_term_momentum'] - data['short_term_momentum'].shift(lag)
            
            # Процентные изменения
            features[f'short_term_strength_pct_change_{lag}'] = data['short_term_strength'].pct_change(lag)
            features[f'short_term_volatility_pct_change_{lag}'] = data['short_term_volatility'].pct_change(lag)
            features[f'short_term_momentum_pct_change_{lag}'] = data['short_term_momentum'].pct_change(lag)
            
            # Лаги ценовых данных
            features[f'close_lag_{lag}'] = data['Close'].shift(lag)
            features[f'high_lag_{lag}'] = data['High'].shift(lag)
            features[f'low_lag_{lag}'] = data['Low'].shift(lag)
            features[f'volume_lag_{lag}'] = data['Volume'].shift(lag)
            
            # Изменения ценовых данных
            features[f'close_change_{lag}'] = data['Close'] - data['Close'].shift(lag)
            features[f'high_change_{lag}'] = data['High'] - data['High'].shift(lag)
            features[f'low_change_{lag}'] = data['Low'] - data['Low'].shift(lag)
            features[f'volume_change_{lag}'] = data['Volume'] - data['Volume'].shift(lag)
        
        self.feature_names.extend(features.columns.tolist())
        return features
    
    def create_rolling_features(self, data):
        """
        Создание скользящих признаков
        
        Скользящие признаки выявляют тренды, паттерны и статистические
        характеристики в различных временных окнах.
        
        Args:
            data: DataFrame с рыночными данными
            
        Returns:
            DataFrame со скользящими признаками
        """
        features = pd.DataFrame(index=data.index)
        
        for window in self.rolling_windows:
            # Скользящие средние
            features[f'short_term_signal_sma_{window}'] = data['short_term_signal'].rolling(window).mean()
            features[f'short_term_strength_sma_{window}'] = data['short_term_strength'].rolling(window).mean()
            features[f'short_term_direction_sma_{window}'] = data['short_term_direction'].rolling(window).mean()
            features[f'short_term_volatility_sma_{window}'] = data['short_term_volatility'].rolling(window).mean()
            features[f'short_term_momentum_sma_{window}'] = data['short_term_momentum'].rolling(window).mean()
            
            # Скользящие стандартные отклонения
            features[f'short_term_signal_std_{window}'] = data['short_term_signal'].rolling(window).std()
            features[f'short_term_strength_std_{window}'] = data['short_term_strength'].rolling(window).std()
            features[f'short_term_direction_std_{window}'] = data['short_term_direction'].rolling(window).std()
            features[f'short_term_volatility_std_{window}'] = data['short_term_volatility'].rolling(window).std()
            features[f'short_term_momentum_std_{window}'] = data['short_term_momentum'].rolling(window).std()
            
            # Скользящие максимумы и минимумы
            features[f'short_term_signal_max_{window}'] = data['short_term_signal'].rolling(window).max()
            features[f'short_term_signal_min_{window}'] = data['short_term_signal'].rolling(window).min()
            features[f'short_term_strength_max_{window}'] = data['short_term_strength'].rolling(window).max()
            features[f'short_term_strength_min_{window}'] = data['short_term_strength'].rolling(window).min()
            
            # Скользящие квантили
            features[f'short_term_signal_q25_{window}'] = data['short_term_signal'].rolling(window).quantile(0.25)
            features[f'short_term_signal_q75_{window}'] = data['short_term_signal'].rolling(window).quantile(0.75)
            features[f'short_term_strength_q25_{window}'] = data['short_term_strength'].rolling(window).quantile(0.25)
            features[f'short_term_strength_q75_{window}'] = data['short_term_strength'].rolling(window).quantile(0.75)
            
            # Скользящие корреляции
            features[f'signal_strength_corr_{window}'] = data['short_term_signal'].rolling(window).corr(data['short_term_strength'])
            features[f'signal_direction_corr_{window}'] = data['short_term_signal'].rolling(window).corr(data['short_term_direction'])
            features[f'strength_volatility_corr_{window}'] = data['short_term_strength'].rolling(window).corr(data['short_term_volatility'])
            
            # Скользящие суммы
            features[f'short_buy_signal_sum_{window}'] = data['short_buy_signal'].rolling(window).sum()
            features[f'short_sell_signal_sum_{window}'] = data['short_sell_signal'].rolling(window).sum()
            features[f'short_hold_signal_sum_{window}'] = data['short_hold_signal'].rolling(window).sum()
            features[f'short_reverse_signal_sum_{window}'] = data['short_reverse_signal'].rolling(window).sum()
            
            # Скользящие средние для ценовых данных
            features[f'close_sma_{window}'] = data['Close'].rolling(window).mean()
            features[f'high_sma_{window}'] = data['High'].rolling(window).mean()
            features[f'low_sma_{window}'] = data['Low'].rolling(window).mean()
            features[f'volume_sma_{window}'] = data['Volume'].rolling(window).mean()
            
            # Скользящие стандартные отклонения для ценовых данных
            features[f'close_std_{window}'] = data['Close'].rolling(window).std()
            features[f'volume_std_{window}'] = data['Volume'].rolling(window).std()
        
        self.feature_names.extend(features.columns.tolist())
        return features
    
    def create_advanced_features(self, data):
        """
        Создание продвинутых признаков
        
        Продвинутые признаки представляют собой сложные комбинации
        базовых признаков для выявления скрытых паттернов.
        
        Args:
            data: DataFrame с рыночными данными
            
        Returns:
            DataFrame с продвинутыми признаками
        """
        features = pd.DataFrame(index=data.index)
        
        # 1. Согласованность сигналов
        features['signal_consistency'] = (
            (data['short_term_signal'] == data['short_buy_signal']) |
            (data['short_term_signal'] == data['short_sell_signal'])
        ).astype(int)
        
        # 2. Сила краткосрочного сигнала
        features['short_signal_strength'] = data['short_term_strength'] * data['short_term_direction']
        
        # 3. Волатильность краткосрочного сигнала
        features['short_volatility_normalized'] = data['short_term_volatility'] / data['Close']
        
        # 4. Моментум краткосрочного сигнала
        features['short_momentum_normalized'] = data['short_term_momentum'] / data['Close']
        
        # 5. Точность краткосрочных сигналов
        features['short_accuracy_normalized'] = data['short_accuracy'] / 100
        
        # 6. Частота краткосрочных сигналов
        features['short_signal_frequency'] = (
            data['short_hits'] + data['short_breaks'] + data['short_bounces']
        ) / 3
        
        # 7. Эффективность краткосрочных сигналов
        features['short_signal_efficiency'] = data['short_accuracy'] / features['short_signal_frequency']
        features['short_signal_efficiency'] = features['short_signal_efficiency'].fillna(0)
        
        # 8. Дивергенция краткосрочных сигналов
        features['short_signal_divergence'] = data['short_term_signal'] - data['short_term_signal'].rolling(10).mean()
        
        # 9. Ускорение краткосрочных сигналов
        features['short_signal_acceleration'] = data['short_term_signal'].diff().diff()
        
        # 10. Корреляция краткосрочных сигналов
        features['short_signal_correlation'] = data['short_term_signal'].rolling(20).corr(data['short_term_strength'])
        
        # 11. Индекс силы сигнала
        features['signal_strength_index'] = (
            data['short_term_strength'] * data['short_term_direction'] * data['short_term_momentum']
        )
        
        # 12. Индекс волатильности сигнала
        features['signal_volatility_index'] = (
            data['short_term_volatility'] * data['short_term_strength']
        )
        
        # 13. Комбинированный индекс
        features['combined_signal_index'] = (
            features['signal_strength_index'] * features['signal_volatility_index']
        )
        
        self.feature_names.extend(features.columns.tolist())
        return features
    
    def create_all_features(self, data):
        """
        Создание всех признаков
        
        Объединяет все типы признаков в один DataFrame.
        
        Args:
            data: DataFrame с рыночными данными
            
        Returns:
            DataFrame со всеми признаками
        """
        # Создание всех типов признаков
        basic_features = self.create_basic_features(data)
        lag_features = self.create_lag_features(data)
        rolling_features = self.create_rolling_features(data)
        advanced_features = self.create_advanced_features(data)
        
        # Объединение всех признаков
        all_features = pd.concat([
            basic_features,
            lag_features,
            rolling_features,
            advanced_features
        ], axis=1)
        
        # Удаление столбцов с NaN значениями
        all_features = all_features.dropna()
        
        print(f"Created {len(all_features.columns)} features")
        print(f"Feature names: {self.feature_names[:10]}...")  # Показываем первые 10
        
        return all_features

# Пример использования создания признаков
def demonstrate_feature_engineering():
    """Демонстрация создания признаков"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Инициализация инженера признаков
    feature_engineer = SCHRShort3FeatureEngineer()
    
    # Создание всех признаков
    features = feature_engineer.create_all_features(test_data)
    
    print("Feature Engineering Results:")
    print(f"Total features: {len(features.columns)}")
    print(f"Data shape: {features.shape}")
    print(f"Missing values: {features.isnull().sum().sum()}")
    
    return features

if __name__ == "__main__":
    demonstrate_feature_engineering()
```

### 2. Продвинутые признаки

**Теория:** Продвинутые признаки SCHR SHORT3 представляют собой сложные комбинации базовых признаков, которые выявляют скрытые паттерны и взаимосвязи в данных краткосрочных сигналов. Они критически важны для достижения высокой точности ML-модели.

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

**Детальное объяснение продвинутых признаков:**

Продвинутые признаки представляют собой сложные математические комбинации базовых признаков, которые выявляют скрытые паттерны и взаимосвязи. Каждый признак решает специфическую задачу:

- **Согласованность сигналов:** Проверяет соответствие различных типов сигналов
- **Нормализованные признаки:** Приводят данные к единому масштабу
- **Эффективность сигналов:** Оценивает качество сигналов относительно их частоты

```python
def create_advanced_schr_short3_features(data):
    """
    Создание продвинутых признаков SCHR SHORT3
    
    Эта функция создает сложные комбинации базовых признаков для выявления
    скрытых паттернов и взаимосвязей в данных краткосрочных сигналов.
    
    Args:
        data: DataFrame с рыночными данными и SCHR SHORT3 индикаторами
        
    Returns:
        DataFrame с продвинутыми признаками
    """
    features = pd.DataFrame(index=data.index)
    
    # 1. Согласованность сигналов
    # Проверяет, соответствуют ли различные типы сигналов друг другу
    features['signal_consistency'] = (
        (data['short_term_signal'] == data['short_buy_signal']) |
        (data['short_term_signal'] == data['short_sell_signal'])
    ).astype(int)
    
    # 2. Сила краткосрочного сигнала
    # Комбинирует силу и направление для получения общей силы сигнала
    features['short_signal_strength'] = data['short_term_strength'] * data['short_term_direction']
    
    # 3. Волатильность краткосрочного сигнала (нормализованная)
    # Нормализует волатильность относительно цены для сравнения между активами
    features['short_volatility_normalized'] = data['short_term_volatility'] / data['Close']
    
    # 4. Моментум краткосрочного сигнала (нормализованный)
    # Нормализует моментум относительно цены
    features['short_momentum_normalized'] = data['short_term_momentum'] / data['Close']
    
    # 5. Точность краткосрочных сигналов (нормализованная)
    # Приводит точность к шкале 0-1
    features['short_accuracy_normalized'] = data['short_accuracy'] / 100
    
    # 6. Частота краткосрочных сигналов
    # Средняя частота различных типов сигналов
    features['short_signal_frequency'] = (
        data['short_hits'] + data['short_breaks'] + data['short_bounces']
    ) / 3
    
    # 7. Эффективность краткосрочных сигналов
    # Отношение точности к частоте сигналов
    features['short_signal_efficiency'] = data['short_accuracy'] / features['short_signal_frequency']
    features['short_signal_efficiency'] = features['short_signal_efficiency'].fillna(0)
    
    # 8. Дивергенция краткосрочных сигналов
    # Отклонение текущего сигнала от скользящего среднего
    features['short_signal_divergence'] = data['short_term_signal'] - data['short_term_signal'].rolling(10).mean()
    
    # 9. Ускорение краткосрочных сигналов
    # Вторая производная сигнала (изменение скорости изменения)
    features['short_signal_acceleration'] = data['short_term_signal'].diff().diff()
    
    # 10. Корреляция краткосрочных сигналов
    # Корреляция между сигналом и его силой
    features['short_signal_correlation'] = data['short_term_signal'].rolling(20).corr(data['short_term_strength'])
    
    # 11. Индекс силы сигнала
    # Комбинированный индекс силы, учитывающий все компоненты
    features['signal_strength_index'] = (
        data['short_term_strength'] * 
        data['short_term_direction'] * 
        data['short_term_momentum']
    )
    
    # 12. Индекс волатильности сигнала
    # Индекс, учитывающий волатильность и силу сигнала
    features['signal_volatility_index'] = (
        data['short_term_volatility'] * 
        data['short_term_strength']
    )
    
    # 13. Комбинированный индекс
    # Объединяет силу и волатильность сигнала
    features['combined_signal_index'] = (
        features['signal_strength_index'] * 
        features['signal_volatility_index']
    )
    
    # 14. Относительная сила сигнала
    # Сила сигнала относительно исторических значений
    features['relative_signal_strength'] = (
        data['short_term_strength'] / 
        data['short_term_strength'].rolling(50).mean()
    )
    
    # 15. Относительная волатильность сигнала
    # Волатильность сигнала относительно исторических значений
    features['relative_signal_volatility'] = (
        data['short_term_volatility'] / 
        data['short_term_volatility'].rolling(50).mean()
    )
    
    # 16. Индекс стабильности сигнала
    # Обратная величина стандартного отклонения сигнала
    features['signal_stability_index'] = 1 / (data['short_term_signal'].rolling(20).std() + 1e-8)
    
    # 17. Индекс изменчивости сигнала
    # Коэффициент вариации сигнала
    features['signal_variability_index'] = (
        data['short_term_signal'].rolling(20).std() / 
        (data['short_term_signal'].rolling(20).mean().abs() + 1e-8)
    )
    
    # 18. Индекс тренда сигнала
    # Наклон линейной регрессии сигнала
    def calculate_trend_slope(series, window=10):
        """Расчет наклона тренда для серии"""
        slopes = []
        for i in range(len(series)):
            if i < window:
                slopes.append(0)
            else:
                y = series.iloc[i-window:i].values
                x = np.arange(len(y))
                if len(y) > 1 and not np.isnan(y).all():
                    slope = np.polyfit(x, y, 1)[0]
                    slopes.append(slope)
                else:
                    slopes.append(0)
        return pd.Series(slopes, index=series.index)
    
    features['signal_trend_slope'] = calculate_trend_slope(data['short_term_signal'])
    
    # 19. Индекс цикличности сигнала
    # Автокорреляция сигнала с различными лагами
    features['signal_cyclicality'] = data['short_term_signal'].rolling(20).apply(
        lambda x: x.autocorr(lag=1) if len(x) > 1 else 0
    )
    
    # 20. Индекс асимметрии сигнала
    # Асимметрия распределения сигнала
    features['signal_skewness'] = data['short_term_signal'].rolling(20).skew()
    
    # 21. Индекс эксцесса сигнала
    # Эксцесс распределения сигнала
    features['signal_kurtosis'] = data['short_term_signal'].rolling(20).kurt()
    
    # 22. Индекс энтропии сигнала
    # Энтропия Шеннона для сигнала
    def calculate_entropy(series, bins=10):
        """Расчет энтропии Шеннона"""
        if len(series) < 2:
            return 0
        hist, _ = np.histogram(series.dropna(), bins=bins)
        hist = hist[hist > 0]  # Убираем нулевые значения
        prob = hist / hist.sum()
        entropy = -np.sum(prob * np.log2(prob + 1e-8))
        return entropy
    
    features['signal_entropy'] = data['short_term_signal'].rolling(20).apply(
        lambda x: calculate_entropy(x) if len(x) > 1 else 0
    )
    
    # 23. Индекс фрактальности сигнала
    # Упрощенная мера фрактальности (Hurst exponent)
    def calculate_hurst_exponent(series):
        """Расчет экспоненты Херста"""
        if len(series) < 10:
            return 0.5
        try:
            lags = range(2, min(20, len(series)//2))
            tau = [np.sqrt(np.std(np.subtract(series[lag:], series[:-lag]))) for lag in lags]
            poly = np.polyfit(np.log(lags), np.log(tau), 1)
            return poly[0] * 2.0
        except:
            return 0.5
    
    features['signal_hurst_exponent'] = data['short_term_signal'].rolling(50).apply(
        lambda x: calculate_hurst_exponent(x) if len(x) > 10 else 0.5
    )
    
    # 24. Индекс персистентности сигнала
    # Мера персистентности тренда
    features['signal_persistence'] = np.abs(features['signal_hurst_exponent'] - 0.5)
    
    # 25. Индекс случайности сигнала
    # Обратная величина персистентности
    features['signal_randomness'] = 1 - features['signal_persistence']
    
    return features

# Пример использования продвинутых признаков
def demonstrate_advanced_features():
    """Демонстрация создания продвинутых признаков"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Создание продвинутых признаков
    advanced_features = create_advanced_schr_short3_features(test_data)
    
    print("Advanced Features Results:")
    print(f"Total advanced features: {len(advanced_features.columns)}")
    print(f"Data shape: {advanced_features.shape}")
    print(f"Missing values: {advanced_features.isnull().sum().sum()}")
    
    # Статистика по признакам
    print("\nFeature Statistics:")
    print(advanced_features.describe())
    
    return advanced_features

if __name__ == "__main__":
    demonstrate_advanced_features()
```

### 3. Временные признаки

**Теория:** Временные признаки SCHR SHORT3 учитывают временные аспекты краткосрочной торговой динамики, включая циклы, сезонность и временные паттерны краткосрочных сигналов. Они критически важны для понимания временной структуры краткосрочной торговли.

**Почему временные признаки важны:**
- **Временная структура:** Учитывают временные аспекты краткосрочных сигналов
- **Циклические паттерны:** Выявляют повторяющиеся паттерны краткосрочных сигналов
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

**Детальное объяснение временных признаков:**

Временные признаки учитывают временные аспекты краткосрочной торговой динамики. Они критически важны для понимания:

- **Временные циклы:** Повторяющиеся паттерны во времени
- **Сезонность:** Временные зависимости в данных
- **Временные интервалы:** Промежутки между событиями

```python
def create_temporal_schr_short3_features(data):
    """
    Создание временных признаков SCHR SHORT3
    
    Эта функция создает признаки, учитывающие временные аспекты
    краткосрочной торговой динамики, включая циклы и сезонность.
    
    Args:
        data: DataFrame с рыночными данными и SCHR SHORT3 индикаторами
        
    Returns:
        DataFrame с временными признаками
    """
    features = pd.DataFrame(index=data.index)
    
    # 1. Время с последнего краткосрочного сигнала
    # Рассчитывает количество периодов с последнего сигнала
    def calculate_time_since_short_signal(data):
        """Расчет времени с последнего краткосрочного сигнала"""
        signal_indices = data[data['short_term_signal'] != 0].index
        time_since = []
        
        for i, idx in enumerate(data.index):
            if i == 0:
                time_since.append(0)
            else:
                # Находим последний сигнал до текущего момента
                prev_signals = signal_indices[signal_indices < idx]
                if len(prev_signals) > 0:
                    last_signal_idx = prev_signals[-1]
                    time_since.append(data.index.get_loc(idx) - data.index.get_loc(last_signal_idx))
                else:
                    time_since.append(i)
        
        return pd.Series(time_since, index=data.index)
    
    features['time_since_short_signal'] = calculate_time_since_short_signal(data)
    
    # 2. Частота краткосрочных сигналов
    # Рассчитывает частоту сигналов в различных временных окнах
    def calculate_short_signal_frequency(data, windows=[5, 10, 20, 50]):
        """Расчет частоты краткосрочных сигналов"""
        frequencies = {}
        
        for window in windows:
            # Частота всех сигналов
            frequencies[f'signal_frequency_{window}'] = (
                data['short_term_signal'].rolling(window).apply(
                    lambda x: (x != 0).sum() / window
                )
            )
            
            # Частота покупок
            frequencies[f'buy_frequency_{window}'] = (
                data['short_buy_signal'].rolling(window).sum() / window
            )
            
            # Частота продаж
            frequencies[f'sell_frequency_{window}'] = (
                data['short_sell_signal'].rolling(window).sum() / window
            )
            
            # Частота удержаний
            frequencies[f'hold_frequency_{window}'] = (
                data['short_hold_signal'].rolling(window).sum() / window
            )
        
        return frequencies
    
    frequency_features = calculate_short_signal_frequency(data)
    features = pd.concat([features, pd.DataFrame(frequency_features, index=data.index)], axis=1)
    
    # 3. Длительность краткосрочного тренда
    # Рассчитывает длительность текущего тренда
    def calculate_short_trend_duration(data):
        """Расчет длительности краткосрочного тренда"""
        trend_durations = []
        current_trend = 0
        current_duration = 0
        
        for i, signal in enumerate(data['short_term_signal']):
            if i == 0:
                trend_durations.append(0)
                current_trend = signal
                current_duration = 1
            else:
                if signal == current_trend and signal != 0:
                    current_duration += 1
                else:
                    current_trend = signal
                    current_duration = 1
                
                trend_durations.append(current_duration)
        
        return pd.Series(trend_durations, index=data.index)
    
    features['short_trend_duration'] = calculate_short_trend_duration(data)
    
    # 4. Циклические паттерны краткосрочных сигналов
    # Выявляет повторяющиеся паттерны в сигналах
    def detect_short_cyclical_patterns(data):
        """Детекция циклических паттернов"""
        patterns = {}
        
        # Автокорреляция с различными лагами
        for lag in [1, 2, 3, 5, 10, 20]:
            patterns[f'signal_autocorr_{lag}'] = data['short_term_signal'].rolling(50).apply(
                lambda x: x.autocorr(lag=lag) if len(x) > lag else 0
            )
        
        # Сезонные компоненты (если есть временная информация)
        if hasattr(data.index, 'hour'):
            # Час дня
            patterns['hour_of_day'] = data.index.hour
            patterns['is_market_open'] = ((data.index.hour >= 9) & (data.index.hour <= 16)).astype(int)
        
        if hasattr(data.index, 'dayofweek'):
            # День недели
            patterns['day_of_week'] = data.index.dayofweek
            patterns['is_weekend'] = (data.index.dayofweek >= 5).astype(int)
        
        if hasattr(data.index, 'day'):
            # День месяца
            patterns['day_of_month'] = data.index.day
        
        if hasattr(data.index, 'month'):
            # Месяц года
            patterns['month_of_year'] = data.index.month
        
        return patterns
    
    cyclical_features = detect_short_cyclical_patterns(data)
    features = pd.concat([features, pd.DataFrame(cyclical_features, index=data.index)], axis=1)
    
    # 5. Временные интервалы между сигналами
    # Рассчитывает статистики временных интервалов
    def calculate_signal_intervals(data):
        """Расчет временных интервалов между сигналами"""
        intervals = {}
        
        # Средний интервал между сигналами
        signal_indices = data[data['short_term_signal'] != 0].index
        if len(signal_indices) > 1:
            interval_diffs = signal_indices.to_series().diff().dt.total_seconds() / 60  # в минутах
            intervals['avg_signal_interval'] = interval_diffs.rolling(10).mean()
            intervals['std_signal_interval'] = interval_diffs.rolling(10).std()
            intervals['min_signal_interval'] = interval_diffs.rolling(10).min()
            intervals['max_signal_interval'] = interval_diffs.rolling(10).max()
        else:
            intervals['avg_signal_interval'] = pd.Series(0, index=data.index)
            intervals['std_signal_interval'] = pd.Series(0, index=data.index)
            intervals['min_signal_interval'] = pd.Series(0, index=data.index)
            intervals['max_signal_interval'] = pd.Series(0, index=data.index)
        
        return intervals
    
    interval_features = calculate_signal_intervals(data)
    features = pd.concat([features, pd.DataFrame(interval_features, index=data.index)], axis=1)
    
    # 6. Временные тренды
    # Анализирует тренды во времени
    def calculate_temporal_trends(data):
        """Расчет временных трендов"""
        trends = {}
        
        # Тренд частоты сигналов
        signal_counts = data['short_term_signal'].rolling(20).apply(lambda x: (x != 0).sum())
        trends['signal_frequency_trend'] = signal_counts.rolling(10).apply(
            lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0
        )
        
        # Тренд силы сигналов
        trends['signal_strength_trend'] = data['short_term_strength'].rolling(20).apply(
            lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0
        )
        
        # Тренд волатильности сигналов
        trends['signal_volatility_trend'] = data['short_term_volatility'].rolling(20).apply(
            lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0
        )
        
        return trends
    
    trend_features = calculate_temporal_trends(data)
    features = pd.concat([features, pd.DataFrame(trend_features, index=data.index)], axis=1)
    
    # 7. Временные индексы
    # Создает различные временные индексы
    def create_temporal_indexes(data):
        """Создание временных индексов"""
        indexes = {}
        
        # Индекс времени (нормализованный)
        if hasattr(data.index, 'hour'):
            indexes['time_index'] = (
                data.index.hour * 60 + 
                data.index.minute
            ) / (24 * 60)  # Нормализация к [0, 1]
        
        # Индекс дня недели (нормализованный)
        if hasattr(data.index, 'dayofweek'):
            indexes['weekday_index'] = data.index.dayofweek / 6  # Нормализация к [0, 1]
        
        # Индекс месяца (нормализованный)
        if hasattr(data.index, 'month'):
            indexes['month_index'] = data.index.month / 12  # Нормализация к [0, 1]
        
        # Циклические индексы (синус и косинус)
        if hasattr(data.index, 'hour'):
            hour_rad = 2 * np.pi * data.index.hour / 24
            indexes['hour_sin'] = np.sin(hour_rad)
            indexes['hour_cos'] = np.cos(hour_rad)
        
        if hasattr(data.index, 'dayofweek'):
            day_rad = 2 * np.pi * data.index.dayofweek / 7
            indexes['day_sin'] = np.sin(day_rad)
            indexes['day_cos'] = np.cos(day_rad)
        
        if hasattr(data.index, 'month'):
            month_rad = 2 * np.pi * data.index.month / 12
            indexes['month_sin'] = np.sin(month_rad)
            indexes['month_cos'] = np.cos(month_rad)
        
        return indexes
    
    temporal_indexes = create_temporal_indexes(data)
    features = pd.concat([features, pd.DataFrame(temporal_indexes, index=data.index)], axis=1)
    
    return features

# Пример использования временных признаков
def demonstrate_temporal_features():
    """Демонстрация создания временных признаков"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Создание временных признаков
    temporal_features = create_temporal_schr_short3_features(test_data)
    
    print("Temporal Features Results:")
    print(f"Total temporal features: {len(temporal_features.columns)}")
    print(f"Data shape: {temporal_features.shape}")
    print(f"Missing values: {temporal_features.isnull().sum().sum()}")
    
    # Статистика по признакам
    print("\nTemporal Feature Statistics:")
    print(temporal_features.describe())
    
    return temporal_features

if __name__ == "__main__":
    demonstrate_temporal_features()
```

## Создание целевых переменных

**Теория:** Создание целевых переменных является критически важным этапом для обучения ML-модели на основе SCHR SHORT3. Правильно определенные целевые переменные определяют успех всей системы машинного обучения.

**Почему создание целевых переменных критично:**
- **Определение задачи:** Четко определяет задачу машинного обучения
- **Качество обучения:** Качественные целевые переменные улучшают обучение
- **Интерпретируемость:** Понятные целевые переменные облегчают интерпретацию
- **Практическая применимость:** Обеспечивают практическую применимость результатов

### 1. Направление краткосрочного движения

**Теория:** Направление краткосрочного движения является наиболее важной целевой переменной для торговых систем на основе SCHR SHORT3. Она определяет основную задачу - предсказание направления краткосрочных движений цены.

**Почему направление краткосрочного движения важно:**
- **Основная задача:** Основная задача торговых систем на основе краткосрочных сигналов
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

**Детальное объяснение создания целевых переменных:**

Создание целевых переменных является критически важным этапом. Каждый тип целевой переменной решает специфическую задачу:

- **Направление движения:** Основная задача классификации
- **Сила движения:** Оценка интенсивности изменений
- **Волатильность:** Управление рисками

```python
def create_short_direction_target(data, horizon=1, threshold=0.001):
    """
    Создание целевой переменной - направление краткосрочного движения
    
    Эта функция создает целевую переменную для классификации направления
    краткосрочных движений цены на основе SCHR SHORT3 сигналов.
    
    Args:
        data: DataFrame с рыночными данными
        horizon: Горизонт предсказания (количество периодов вперед)
        threshold: Порог для определения значимых движений
        
    Returns:
        Series с целевой переменной (0=down, 1=hold, 2=up)
    """
    future_price = data['Close'].shift(-horizon)
    current_price = data['Close']
    
    # Процентное изменение
    price_change = (future_price - current_price) / current_price
    
    # Классификация направления с учетом порога
    target = pd.cut(
        price_change,
        bins=[-np.inf, -threshold, threshold, np.inf],
        labels=[0, 1, 2],  # 0=down, 1=hold, 2=up
        include_lowest=True
    )
    
    return target.astype(int)

def create_short_strength_target(data, horizon=1):
    """
    Создание целевой переменной - сила краткосрочного движения
    
    Эта функция создает целевую переменную для оценки силы
    краткосрочных движений цены.
    
    Args:
        data: DataFrame с рыночными данными
        horizon: Горизонт предсказания
        
    Returns:
        Series с целевой переменной (0=weak, 1=medium, 2=strong, 3=very_strong)
    """
    future_price = data['Close'].shift(-horizon)
    current_price = data['Close']
    
    # Процентное изменение
    price_change = (future_price - current_price) / current_price
    
    # Классификация силы на основе абсолютного изменения
    target = pd.cut(
        abs(price_change),
        bins=[0, 0.001, 0.005, 0.01, np.inf],
        labels=[0, 1, 2, 3],  # 0=weak, 1=medium, 2=strong, 3=very_strong
        include_lowest=True
    )
    
    return target.astype(int)

def create_short_volatility_target(data, horizon=1):
    """
    Создание целевой переменной - волатильность краткосрочного движения
    
    Эта функция создает целевую переменную для оценки волатильности
    краткосрочных движений цены.
    
    Args:
        data: DataFrame с рыночными данными
        horizon: Горизонт предсказания
        
    Returns:
        Series с целевой переменной (0=low, 1=medium, 2=high, 3=very_high)
    """
    # Расчет волатильности как стандартного отклонения изменений
    returns = data['Close'].pct_change()
    volatility = returns.rolling(horizon).std()
    
    # Классификация волатильности
    target = pd.cut(
        volatility,
        bins=[0, 0.01, 0.02, 0.05, np.inf],
        labels=[0, 1, 2, 3],  # 0=low, 1=medium, 2=high, 3=very_high
        include_lowest=True
    )
    
    return target.astype(int)

def create_short_momentum_target(data, horizon=1):
    """
    Создание целевой переменной - моментум краткосрочного движения
    
    Эта функция создает целевую переменную для оценки моментума
    краткосрочных движений цены.
    
    Args:
        data: DataFrame с рыночными данными
        horizon: Горизонт предсказания
        
    Returns:
        Series с целевой переменной (0=negative, 1=neutral, 2=positive)
    """
    future_price = data['Close'].shift(-horizon)
    current_price = data['Close']
    
    # Процентное изменение
    price_change = (future_price - current_price) / current_price
    
    # Классификация моментума
    target = pd.cut(
        price_change,
        bins=[-np.inf, -0.001, 0.001, np.inf],
        labels=[0, 1, 2],  # 0=negative, 1=neutral, 2=positive
        include_lowest=True
    )
    
    return target.astype(int)

def create_short_accuracy_target(data, horizon=1):
    """
    Создание целевой переменной - точность краткосрочных сигналов
    
    Эта функция создает целевую переменную для оценки точности
    краткосрочных сигналов на основе фактических движений цены.
    
    Args:
        data: DataFrame с рыночными данными
        horizon: Горизонт предсказания
        
    Returns:
        Series с целевой переменной (0=incorrect, 1=correct)
    """
    future_price = data['Close'].shift(-horizon)
    current_price = data['Close']
    
    # Процентное изменение
    price_change = (future_price - current_price) / current_price
    
    # Определение правильности сигнала
    correct_signals = (
        ((data['short_term_signal'] == 1) & (price_change > 0)) |  # Покупка при росте
        ((data['short_term_signal'] == -1) & (price_change < 0)) |  # Продажа при падении
        ((data['short_term_signal'] == 0) & (abs(price_change) < 0.001))  # Удержание при боковом движении
    )
    
    return correct_signals.astype(int)

def create_short_risk_target(data, horizon=1):
    """
    Создание целевой переменной - риск краткосрочного движения
    
    Эта функция создает целевую переменную для оценки риска
    краткосрочных движений цены.
    
    Args:
        data: DataFrame с рыночными данными
        horizon: Горизонт предсказания
        
    Returns:
        Series с целевой переменной (0=low_risk, 1=medium_risk, 2=high_risk)
    """
    # Расчет максимальной просадки
    future_price = data['Close'].shift(-horizon)
    current_price = data['Close']
    
    # Процентное изменение
    price_change = (future_price - current_price) / current_price
    
    # Расчет риска как комбинации волатильности и максимальной просадки
    volatility = data['Close'].pct_change().rolling(horizon).std()
    max_drawdown = abs(price_change)
    
    # Комбинированный индекс риска
    risk_index = volatility * max_drawdown
    
    # Классификация риска
    target = pd.cut(
        risk_index,
        bins=[0, 0.01, 0.05, np.inf],
        labels=[0, 1, 2],  # 0=low_risk, 1=medium_risk, 2=high_risk
        include_lowest=True
    )
    
    return target.astype(int)

def create_all_targets(data, horizon=1):
    """
    Создание всех целевых переменных
    
    Эта функция создает все типы целевых переменных для комплексного
    анализа краткосрочных движений цены.
    
    Args:
        data: DataFrame с рыночными данными
        horizon: Горизонт предсказания
        
    Returns:
        DataFrame со всеми целевыми переменными
    """
    targets = pd.DataFrame(index=data.index)
    
    # Создание всех типов целевых переменных
    targets['direction'] = create_short_direction_target(data, horizon)
    targets['strength'] = create_short_strength_target(data, horizon)
    targets['volatility'] = create_short_volatility_target(data, horizon)
    targets['momentum'] = create_short_momentum_target(data, horizon)
    targets['accuracy'] = create_short_accuracy_target(data, horizon)
    targets['risk'] = create_short_risk_target(data, horizon)
    
    # Удаление строк с NaN значениями
    targets = targets.dropna()
    
    print(f"Created {len(targets.columns)} target variables")
    print(f"Target distribution:")
    for col in targets.columns:
        print(f"{col}: {targets[col].value_counts().to_dict()}")
    
    return targets

# Пример использования создания целевых переменных
def demonstrate_target_creation():
    """Демонстрация создания целевых переменных"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Создание всех целевых переменных
    targets = create_all_targets(test_data)
    
    print("Target Creation Results:")
    print(f"Total targets: {len(targets.columns)}")
    print(f"Data shape: {targets.shape}")
    print(f"Missing values: {targets.isnull().sum().sum()}")
    
    return targets

if __name__ == "__main__":
    demonstrate_target_creation()
```

### 2. Сила краткосрочного движения

**Теория:** Сила краткосрочного движения представляет собой важную целевую переменную для торговых систем на основе SCHR SHORT3. Она определяет интенсивность краткосрочных движений цены и помогает в управлении рисками.

**Почему сила краткосрочного движения важна:**
- **Управление рисками:** Помогает в управлении рисками
- **Оптимизация позиций:** Позволяет оптимизировать размер позиций
- **Фильтрация сигналов:** Помогает фильтровать слабые сигналы
- **Повышение эффективности:** Может повысить эффективность торговли

**Плюсы:**
- Улучшение управления рисками
- Оптимизация позиций
- Фильтрация сигналов
- Повышение эффективности

**Минусы:**
- Сложность определения
- Потенциальная нестабильность
- Сложность интерпретации
- Высокие требования к данным

```python
def create_short_strength_target(data, horizon=1):
    """Создание целевой переменной - сила краткосрочного движения"""
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

### 3. Волатильность краткосрочного движения

**Теория:** Волатильность краткосрочного движения является критически важной целевой переменной для SCHR SHORT3, так как она определяет уровень риска и неопределенности в краткосрочных торговых операциях.

**Почему волатильность краткосрочного движения важна:**
- **Управление рисками:** Критически важно для управления рисками
- **Размер позиций:** Помогает определить оптимальный размер позиций
- **Фильтрация сигналов:** Помогает фильтровать сигналы в условиях высокой волатильности
- **Адаптация стратегий:** Позволяет адаптировать стратегии к уровню волатильности

**Плюсы:**
- Критически важно для управления рисками
- Помощь в определении размера позиций
- Фильтрация сигналов
- Адаптация стратегий

**Минусы:**
- Сложность измерения
- Потенциальная нестабильность
- Сложность интерпретации
- Высокие требования к данным

```python
def create_short_volatility_target(data, horizon=1):
    """Создание целевой переменной - волатильность краткосрочного движения"""
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

## ML-модели для SCHR SHORT3

**Теория:** ML-модели для SCHR SHORT3 представляют собой комплексную систему машинного обучения, которая использует различные алгоритмы для анализа данных SCHR SHORT3 и генерации торговых сигналов. Это критически важно для создания высокоточных торговых систем.

**Почему ML-модели критичны:**
- **Высокая точность:** Обеспечивают высокую точность предсказаний
- **Адаптивность:** Могут адаптироваться к изменениям рынка
- **Автоматизация:** Автоматизируют процесс анализа и принятия решений
- **Масштабируемость:** Могут обрабатывать большие объемы данных

### 1. Классификатор краткосрочных сигналов

**Теория:** Классификатор краткосрочных сигналов является основной задачей для торговых систем на основе SCHR SHORT3, где модель должна предсказать краткосрочные торговые сигналы. Это критически важно для принятия торговых решений.

**Почему классификатор краткосрочных сигналов важен:**
- **Основная задача:** Основная задача торговых систем на основе краткосрочных сигналов
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

**Детальное объяснение ML-моделей:**

ML-модели для SCHR SHORT3 представляют собой комплексную систему машинного обучения. Каждый тип модели решает специфическую задачу:

- **Классификатор:** Предсказывает направление движения
- **Регрессор:** Оценивает силу и интенсивность движений
- **Deep Learning:** Выявляет сложные нелинейные зависимости

```python
class SCHRShort3Classifier:
    """
    Классификатор на основе SCHR SHORT3
    
    Этот класс реализует ансамбль различных алгоритмов машинного обучения
    для классификации краткосрочных торговых сигналов.
    """
    
    def __init__(self):
        self.models = {
            'xgboost': XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            ),
            'lightgbm': LGBMClassifier(
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
            'neural_network': MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=42
            )
        }
        self.ensemble = VotingClassifier(
            estimators=list(self.models.items()),
            voting='soft'
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self, X, y):
        """
        Обучение модели
        
        Args:
            X: Признаки для обучения
            y: Целевая переменная
            
        Returns:
            Обученная модель
        """
        # Разделение на train/validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Нормализация признаков
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # Обучение ансамбля
        self.ensemble.fit(X_train_scaled, y_train)
        
        # Валидация
        val_score = self.ensemble.score(X_val_scaled, y_val)
        print(f"Validation accuracy: {val_score:.4f}")
        
        # Детальная оценка
        y_pred = self.ensemble.predict(X_val_scaled)
        print("\nClassification Report:")
        print(classification_report(y_val, y_pred))
        
        # Матрица ошибок
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_val, y_pred))
        
        self.is_trained = True
        return self.ensemble
    
    def predict(self, X):
        """
        Предсказание
        
        Args:
            X: Признаки для предсказания
            
        Returns:
            Предсказания
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X_scaled = self.scaler.transform(X)
        return self.ensemble.predict(X_scaled)
    
    def predict_proba(self, X):
        """
        Предсказание вероятностей
        
        Args:
            X: Признаки для предсказания
            
        Returns:
            Вероятности предсказаний
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X_scaled = self.scaler.transform(X)
        return self.ensemble.predict_proba(X_scaled)
    
    def get_feature_importance(self):
        """
        Получение важности признаков
        
        Returns:
            Словарь с важностью признаков для каждой модели
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")
        
        importance = {}
        for name, model in self.models.items():
            if hasattr(model, 'feature_importances_'):
                importance[name] = model.feature_importances_
            elif hasattr(model, 'coef_'):
                importance[name] = abs(model.coef_[0])
        
        return importance

class SCHRShort3Regressor:
    """
    Регрессор для прогнозирования краткосрочных движений
    
    Этот класс реализует ансамбль регрессионных алгоритмов
    для прогнозирования силы и интенсивности краткосрочных движений.
    """
    
    def __init__(self):
        self.models = {
            'xgboost': XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            ),
            'lightgbm': LGBMRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                verbose=-1
            ),
            'catboost': CatBoostRegressor(
                iterations=100,
                depth=6,
                learning_rate=0.1,
                random_state=42,
                verbose=False
            ),
            'neural_network': MLPRegressor(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=42
            )
        }
        self.ensemble = VotingRegressor(
            estimators=list(self.models.items())
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def train(self, X, y):
        """
        Обучение регрессора
        
        Args:
            X: Признаки для обучения
            y: Целевая переменная
            
        Returns:
            Обученная модель
        """
        # Разделение на train/validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Нормализация признаков
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # Обучение ансамбля
        self.ensemble.fit(X_train_scaled, y_train)
        
        # Валидация
        val_score = self.ensemble.score(X_val_scaled, y_val)
        print(f"Validation R² score: {val_score:.4f}")
        
        # Детальная оценка
        y_pred = self.ensemble.predict(X_val_scaled)
        mse = np.mean((y_val - y_pred) ** 2)
        mae = np.mean(abs(y_val - y_pred))
        
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"Mean Absolute Error: {mae:.4f}")
        
        self.is_trained = True
        return self.ensemble
    
    def predict(self, X):
        """
        Предсказание
        
        Args:
            X: Признаки для предсказания
            
        Returns:
            Предсказания
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X_scaled = self.scaler.transform(X)
        return self.ensemble.predict(X_scaled)

class SCHRShort3DeepModel:
    """
    Deep Learning модель для SCHR SHORT3
    
    Этот класс реализует нейронную сеть для анализа
    сложных нелинейных зависимостей в краткосрочных сигналах.
    """
    
    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.model = self._build_model()
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def _build_model(self):
        """
        Построение нейронной сети
        
        Returns:
            Скомпилированная модель Keras
        """
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
        from tensorflow.keras.optimizers import Adam
        from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
        
        model = Sequential([
            Dense(512, activation='relu', input_dim=self.input_dim),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dropout(0.2),
            
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.2),
            
            Dense(32, activation='relu'),
            Dropout(0.1),
            
            Dense(self.output_dim, activation='softmax')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, X, y, epochs=100, batch_size=32):
        """
        Обучение модели
        
        Args:
            X: Признаки для обучения
            y: Целевая переменная
            epochs: Количество эпох
            batch_size: Размер батча
            
        Returns:
            История обучения
        """
        from tensorflow.keras.utils import to_categorical
        from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
        
        # Разделение на train/validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Нормализация признаков
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # One-hot encoding для y
        y_train_encoded = to_categorical(y_train)
        y_val_encoded = to_categorical(y_val)
        
        # Callbacks
        callbacks = [
            EarlyStopping(patience=10, restore_best_weights=True),
            ReduceLROnPlateau(factor=0.5, patience=5)
        ]
        
        # Обучение
        history = self.model.fit(
            X_train_scaled, y_train_encoded,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_val_scaled, y_val_encoded),
            callbacks=callbacks,
            verbose=1
        )
        
        self.is_trained = True
        return history
    
    def predict(self, X):
        """
        Предсказание
        
        Args:
            X: Признаки для предсказания
            
        Returns:
            Предсказания
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        return np.argmax(predictions, axis=1)
    
    def predict_proba(self, X):
        """
        Предсказание вероятностей
        
        Args:
            X: Признаки для предсказания
            
        Returns:
            Вероятности предсказаний
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

# Пример использования ML-моделей
def demonstrate_ml_models():
    """Демонстрация ML-моделей"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Создание признаков
    feature_engineer = SCHRShort3FeatureEngineer()
    features = feature_engineer.create_all_features(test_data)
    
    # Создание целевых переменных
    targets = create_all_targets(test_data)
    
    # Выравнивание индексов
    common_index = features.index.intersection(targets.index)
    features = features.loc[common_index]
    targets = targets.loc[common_index]
    
    # Тестирование классификатора
    print("Testing Classifier:")
    classifier = SCHRShort3Classifier()
    classifier.train(features, targets['direction'])
    
    # Тестирование регрессора
    print("\nTesting Regressor:")
    regressor = SCHRShort3Regressor()
    regressor.train(features, targets['strength'])
    
    # Тестирование Deep Learning модели
    print("\nTesting Deep Learning Model:")
    deep_model = SCHRShort3DeepModel(features.shape[1], len(targets['direction'].unique()))
    deep_model.train(features, targets['direction'])
    
    return classifier, regressor, deep_model

if __name__ == "__main__":
    demonstrate_ml_models()
```

### 2. Регрессор для прогнозирования краткосрочных движений

**Теория:** Регрессор для прогнозирования краткосрочных движений представляет собой более сложную задачу, где модель должна предсказать конкретные значения краткосрочных движений цены. Это критически важно для точного управления позициями.

**Почему регрессор важен:**
- **Точность прогнозов:** Обеспечивает более точные прогнозы краткосрочных движений
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
class SCHRShort3Regressor:
    """Регрессор для прогнозирования краткосрочных движений"""
    
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
        """Предсказание краткосрочных движений"""
        return self.ensemble.predict(X)
```

### 3. Deep Learning модель

**Теория:** Deep Learning модели представляют собой наиболее сложные и мощные алгоритмы машинного обучения, которые могут выявлять сложные нелинейные зависимости в данных SCHR SHORT3. Это критически важно для достижения максимальной точности.

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
class SCHRShort3DeepModel:
    """Deep Learning модель для SCHR SHORT3"""
    
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

## Бэктестинг SCHR SHORT3 модели

**Теория:** Бэктестинг SCHR SHORT3 модели является критически важным этапом для валидации эффективности торговой стратегии на основе краткосрочных сигналов. Это позволяет оценить производительность модели на исторических данных перед реальным использованием.

**Почему бэктестинг критичен:**
- **Валидация стратегии:** Позволяет проверить эффективность стратегии
- **Оценка рисков:** Помогает оценить потенциальные риски
- **Оптимизация параметров:** Позволяет оптимизировать параметры стратегии
- **Уверенность:** Повышает уверенность в стратегии

### 1. Стратегия бэктестинга

**Теория:** Стратегия бэктестинга определяет методологию тестирования SCHR SHORT3 модели на исторических данных. Правильная стратегия критически важна для получения достоверных результатов.

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

**Детальное объяснение бэктестинга:**

Бэктестинг SCHR SHORT3 модели является критически важным этапом для валидации эффективности торговой стратегии. Он позволяет:

- **Проверить эффективность:** Оценить производительность на исторических данных
- **Оптимизировать параметры:** Найти оптимальные настройки
- **Управлять рисками:** Оценить потенциальные риски

```python
class SCHRShort3Backtester:
    """
    Бэктестер для SCHR SHORT3 модели
    
    Этот класс реализует комплексный бэктестинг торговой стратегии
    на основе краткосрочных сигналов SCHR SHORT3.
    """
    
    def __init__(self, model, data, initial_capital=100000, commission=0.001):
        self.model = model
        self.data = data
        self.initial_capital = initial_capital
        self.commission = commission
        self.results = {}
        self.trades = []
    
    def backtest(self, start_date, end_date):
        """
        Бэктестинг стратегии
        
        Args:
            start_date: Начальная дата тестирования
            end_date: Конечная дата тестирования
            
        Returns:
            Словарь с результатами бэктестинга
        """
        # Фильтрация данных по датам
        mask = (self.data.index >= start_date) & (self.data.index <= end_date)
        test_data = self.data[mask]
        
        if len(test_data) == 0:
            raise ValueError("No data found for the specified date range")
        
        # Предсказания модели
        predictions = self.model.predict(test_data)
        
        # Расчет доходности
        returns = self._calculate_returns(test_data, predictions)
        
        # Метрики производительности
        metrics = self._calculate_metrics(returns)
        
        # Детальный анализ сделок
        trade_analysis = self._analyze_trades()
        
        return {
            'returns': returns,
            'metrics': metrics,
            'predictions': predictions,
            'trades': trade_analysis,
            'data': test_data
        }
    
    def _calculate_returns(self, data, predictions):
        """
        Расчет доходности
        
        Args:
            data: Данные для тестирования
            predictions: Предсказания модели
            
        Returns:
            Список доходностей
        """
        returns = []
        position = 0
        capital = self.initial_capital
        
        for i, (date, row) in enumerate(data.iterrows()):
            if i == 0:
                continue
            
            # Сигнал модели
            signal = predictions[i]
            
            # Логика торговли на основе краткосрочных сигналов
            if signal == 1 and position <= 0:  # Краткосрочная покупка
                if position < 0:  # Закрытие короткой позиции
                    self._close_position(date, row, position, capital)
                position = 1
                self._open_position(date, row, position, capital)
            elif signal == -1 and position >= 0:  # Краткосрочная продажа
                if position > 0:  # Закрытие длинной позиции
                    self._close_position(date, row, position, capital)
                position = -1
                self._open_position(date, row, position, capital)
            elif signal == 0:  # Без сигнала
                if position != 0:  # Закрытие позиции
                    self._close_position(date, row, position, capital)
                position = 0
            
            # Расчет доходности
            if position != 0:
                current_return = (row['Close'] - data.iloc[i-1]['Close']) / data.iloc[i-1]['Close']
                returns.append(current_return * position)
            else:
                returns.append(0)
        
        return returns
    
    def _open_position(self, date, row, position, capital):
        """Открытие позиции"""
        self.trades.append({
            'date': date,
            'action': 'open',
            'position': position,
            'price': row['Close'],
            'capital': capital
        })
    
    def _close_position(self, date, row, position, capital):
        """Закрытие позиции"""
        self.trades.append({
            'date': date,
            'action': 'close',
            'position': position,
            'price': row['Close'],
            'capital': capital
        })
    
    def _calculate_metrics(self, returns):
        """
        Расчет метрик производительности
        
        Args:
            returns: Список доходностей
            
        Returns:
            Словарь с метриками
        """
        returns = np.array(returns)
        
        # Базовая статистика
        total_return = np.sum(returns)
        annualized_return = total_return * 252
        
        # Волатильность
        volatility = np.std(returns) * np.sqrt(252)
        
        # Sharpe Ratio
        risk_free_rate = 0.02
        sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # Максимальная просадка
        cumulative_returns = np.cumsum(returns)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = cumulative_returns - running_max
        max_drawdown = np.min(drawdown)
        
        # Win Rate
        win_rate = np.sum(returns > 0) / len(returns) if len(returns) > 0 else 0
        
        # Profit Factor
        gross_profit = np.sum(returns[returns > 0])
        gross_loss = abs(np.sum(returns[returns < 0]))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf
        
        # Специфичные метрики для краткосрочных сигналов
        short_signal_accuracy = self._calculate_short_signal_accuracy(returns)
        short_signal_frequency = self._calculate_short_signal_frequency(returns)
        short_signal_efficiency = self._calculate_short_signal_efficiency(returns)
        
        return {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'short_signal_accuracy': short_signal_accuracy,
            'short_signal_frequency': short_signal_frequency,
            'short_signal_efficiency': short_signal_efficiency
        }
    
    def _calculate_short_signal_accuracy(self, returns):
        """Расчет точности краткосрочных сигналов"""
        # Упрощенный расчет точности
        return np.sum(returns > 0) / len(returns) if len(returns) > 0 else 0
    
    def _calculate_short_signal_frequency(self, returns):
        """Расчет частоты краткосрочных сигналов"""
        # Упрощенный расчет частоты
        return len(returns[returns != 0]) / len(returns) if len(returns) > 0 else 0
    
    def _calculate_short_signal_efficiency(self, returns):
        """Расчет эффективности краткосрочных сигналов"""
        # Упрощенный расчет эффективности
        return np.mean(returns[returns != 0]) if len(returns[returns != 0]) > 0 else 0
    
    def _analyze_trades(self):
        """Анализ сделок"""
        if not self.trades:
            return {}
        
        # Группировка сделок по позициям
        open_trades = [t for t in self.trades if t['action'] == 'open']
        close_trades = [t for t in self.trades if t['action'] == 'close']
        
        # Расчет прибыли/убытка по сделкам
        trade_pnl = []
        for i in range(min(len(open_trades), len(close_trades))):
            open_trade = open_trades[i]
            close_trade = close_trades[i]
            
            pnl = (close_trade['price'] - open_trade['price']) * open_trade['position']
            trade_pnl.append(pnl)
        
        return {
            'total_trades': len(trade_pnl),
            'profitable_trades': len([pnl for pnl in trade_pnl if pnl > 0]),
            'losing_trades': len([pnl for pnl in trade_pnl if pnl < 0]),
            'average_pnl': np.mean(trade_pnl) if trade_pnl else 0,
            'max_profit': max(trade_pnl) if trade_pnl else 0,
            'max_loss': min(trade_pnl) if trade_pnl else 0
        }
    
    def plot_results(self, results):
        """
        Построение графиков результатов
        
        Args:
            results: Результаты бэктестинга
        """
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # График доходности
        cumulative_returns = np.cumsum(results['returns'])
        axes[0, 0].plot(cumulative_returns)
        axes[0, 0].set_title('Cumulative Returns')
        axes[0, 0].set_ylabel('Returns')
        
        # График просадки
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = cumulative_returns - running_max
        axes[0, 1].fill_between(range(len(drawdown)), drawdown, 0, alpha=0.3)
        axes[0, 1].set_title('Drawdown')
        axes[0, 1].set_ylabel('Drawdown')
        
        # Распределение доходности
        axes[1, 0].hist(results['returns'], bins=50, alpha=0.7)
        axes[1, 0].set_title('Returns Distribution')
        axes[1, 0].set_xlabel('Returns')
        axes[1, 0].set_ylabel('Frequency')
        
        # Метрики производительности
        metrics = results['metrics']
        metric_names = ['Total Return', 'Sharpe Ratio', 'Win Rate', 'Profit Factor']
        metric_values = [
            metrics['total_return'],
            metrics['sharpe_ratio'],
            metrics['win_rate'],
            metrics['profit_factor']
        ]
        
        axes[1, 1].bar(metric_names, metric_values)
        axes[1, 1].set_title('Performance Metrics')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()

# Пример использования бэктестера
def demonstrate_backtesting():
    """Демонстрация бэктестинга"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Создание признаков
    feature_engineer = SCHRShort3FeatureEngineer()
    features = feature_engineer.create_all_features(test_data)
    
    # Создание целевых переменных
    targets = create_all_targets(test_data)
    
    # Выравнивание индексов
    common_index = features.index.intersection(targets.index)
    features = features.loc[common_index]
    targets = targets.loc[common_index]
    
    # Обучение модели
    classifier = SCHRShort3Classifier()
    classifier.train(features, targets['direction'])
    
    # Создание бэктестера
    backtester = SCHRShort3Backtester(classifier, test_data)
    
    # Бэктестинг
    start_date = test_data.index[100]
    end_date = test_data.index[-1]
    results = backtester.backtest(start_date, end_date)
    
    print("Backtesting Results:")
    print(f"Total Return: {results['metrics']['total_return']:.4f}")
    print(f"Sharpe Ratio: {results['metrics']['sharpe_ratio']:.4f}")
    print(f"Win Rate: {results['metrics']['win_rate']:.4f}")
    print(f"Max Drawdown: {results['metrics']['max_drawdown']:.4f}")
    
    return results

if __name__ == "__main__":
    demonstrate_backtesting()
```

### 2. Метрики производительности

**Теория:** Метрики производительности являются критически важными для оценки эффективности SCHR SHORT3 модели. Они обеспечивают количественную оценку различных аспектов производительности торговой стратегии на основе краткосрочных сигналов.

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

**Детальное объяснение метрик производительности:**

Метрики производительности являются критически важными для оценки эффективности SCHR SHORT3 модели. Каждая метрика решает специфическую задачу:

- **Финансовые метрики:** Оценивают прибыльность и риски
- **Статистические метрики:** Анализируют распределение доходности
- **Специфичные метрики:** Оценивают качество краткосрочных сигналов

```python
def calculate_schr_short3_performance_metrics(returns):
    """
    Расчет метрик производительности для SCHR SHORT3
    
    Эта функция рассчитывает комплексный набор метрик для оценки
    эффективности торговой стратегии на основе краткосрочных сигналов.
    
    Args:
        returns: Список доходностей
        
    Returns:
        Словарь с метриками производительности
    """
    returns = np.array(returns)
    
    if len(returns) == 0:
        return {}
    
    # Базовая статистика
    total_return = np.sum(returns)
    annualized_return = total_return * 252
    
    # Волатильность
    volatility = np.std(returns) * np.sqrt(252)
    
    # Sharpe Ratio
    risk_free_rate = 0.02
    sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
    
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
    
    # Специфичные метрики для краткосрочных сигналов
    short_signal_accuracy = calculate_short_signal_accuracy(returns)
    short_signal_frequency = calculate_short_signal_frequency(returns)
    short_signal_efficiency = calculate_short_signal_efficiency(returns)
    
    # Дополнительные метрики
    calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
    sortino_ratio = calculate_sortino_ratio(returns, risk_free_rate)
    omega_ratio = calculate_omega_ratio(returns, risk_free_rate)
    
    # Метрики риска
    var_95 = calculate_var(returns, 0.05)
    cvar_95 = calculate_cvar(returns, 0.05)
    max_consecutive_losses = calculate_max_consecutive_losses(returns)
    
    # Метрики стабильности
    stability_ratio = calculate_stability_ratio(returns)
    consistency_ratio = calculate_consistency_ratio(returns)
    
    return {
        'total_return': total_return,
        'annualized_return': annualized_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'sortino_ratio': sortino_ratio,
        'calmar_ratio': calmar_ratio,
        'omega_ratio': omega_ratio,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'var_95': var_95,
        'cvar_95': cvar_95,
        'max_consecutive_losses': max_consecutive_losses,
        'stability_ratio': stability_ratio,
        'consistency_ratio': consistency_ratio,
        'short_signal_accuracy': short_signal_accuracy,
        'short_signal_frequency': short_signal_frequency,
        'short_signal_efficiency': short_signal_efficiency
    }

def calculate_short_signal_accuracy(returns):
    """Расчет точности краткосрочных сигналов"""
    return np.sum(returns > 0) / len(returns) if len(returns) > 0 else 0

def calculate_short_signal_frequency(returns):
    """Расчет частоты краткосрочных сигналов"""
    return len(returns[returns != 0]) / len(returns) if len(returns) > 0 else 0

def calculate_short_signal_efficiency(returns):
    """Расчет эффективности краткосрочных сигналов"""
    return np.mean(returns[returns != 0]) if len(returns[returns != 0]) > 0 else 0

def calculate_sortino_ratio(returns, risk_free_rate=0.02):
    """Расчет Sortino Ratio"""
    excess_returns = returns - risk_free_rate / 252
    downside_returns = excess_returns[excess_returns < 0]
    
    if len(downside_returns) == 0:
        return np.inf
    
    downside_volatility = np.std(downside_returns) * np.sqrt(252)
    return np.mean(excess_returns) * np.sqrt(252) / downside_volatility if downside_volatility > 0 else 0

def calculate_omega_ratio(returns, risk_free_rate=0.02):
    """Расчет Omega Ratio"""
    excess_returns = returns - risk_free_rate / 252
    positive_returns = excess_returns[excess_returns > 0]
    negative_returns = excess_returns[excess_returns < 0]
    
    if len(negative_returns) == 0:
        return np.inf
    
    return np.sum(positive_returns) / abs(np.sum(negative_returns)) if np.sum(negative_returns) != 0 else np.inf

def calculate_var(returns, confidence_level=0.05):
    """Расчет Value at Risk (VaR)"""
    return np.percentile(returns, confidence_level * 100)

def calculate_cvar(returns, confidence_level=0.05):
    """Расчет Conditional Value at Risk (CVaR)"""
    var = calculate_var(returns, confidence_level)
    return np.mean(returns[returns <= var])

def calculate_max_consecutive_losses(returns):
    """Расчет максимального количества последовательных убытков"""
    max_losses = 0
    current_losses = 0
    
    for ret in returns:
        if ret < 0:
            current_losses += 1
            max_losses = max(max_losses, current_losses)
        else:
            current_losses = 0
    
    return max_losses

def calculate_stability_ratio(returns):
    """Расчет коэффициента стабильности"""
    if len(returns) < 2:
        return 0
    
    # Коэффициент вариации
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    
    return mean_return / std_return if std_return > 0 else 0

def calculate_consistency_ratio(returns):
    """Расчет коэффициента консистентности"""
    if len(returns) < 2:
        return 0
    
    # Процент положительных периодов
    positive_periods = np.sum(returns > 0)
    total_periods = len(returns)
    
    return positive_periods / total_periods

def calculate_advanced_metrics(returns):
    """
    Расчет продвинутых метрик производительности
    
    Args:
        returns: Список доходностей
        
    Returns:
        Словарь с продвинутыми метриками
    """
    returns = np.array(returns)
    
    if len(returns) == 0:
        return {}
    
    # Метрики распределения
    skewness = calculate_skewness(returns)
    kurtosis = calculate_kurtosis(returns)
    
    # Метрики автокорреляции
    autocorr_1 = calculate_autocorrelation(returns, 1)
    autocorr_5 = calculate_autocorrelation(returns, 5)
    
    # Метрики тренда
    trend_strength = calculate_trend_strength(returns)
    mean_reversion = calculate_mean_reversion(returns)
    
    # Метрики волатильности
    volatility_clustering = calculate_volatility_clustering(returns)
    volatility_persistence = calculate_volatility_persistence(returns)
    
    return {
        'skewness': skewness,
        'kurtosis': kurtosis,
        'autocorr_1': autocorr_1,
        'autocorr_5': autocorr_5,
        'trend_strength': trend_strength,
        'mean_reversion': mean_reversion,
        'volatility_clustering': volatility_clustering,
        'volatility_persistence': volatility_persistence
    }

def calculate_skewness(returns):
    """Расчет асимметрии"""
    return np.mean((returns - np.mean(returns)) ** 3) / (np.std(returns) ** 3)

def calculate_kurtosis(returns):
    """Расчет эксцесса"""
    return np.mean((returns - np.mean(returns)) ** 4) / (np.std(returns) ** 4) - 3

def calculate_autocorrelation(returns, lag):
    """Расчет автокорреляции"""
    if len(returns) <= lag:
        return 0
    
    return np.corrcoef(returns[:-lag], returns[lag:])[0, 1]

def calculate_trend_strength(returns):
    """Расчет силы тренда"""
    if len(returns) < 2:
        return 0
    
    # Линейная регрессия
    x = np.arange(len(returns))
    slope = np.polyfit(x, returns, 1)[0]
    
    return slope

def calculate_mean_reversion(returns):
    """Расчет силы возврата к среднему"""
    if len(returns) < 2:
        return 0
    
    # AR(1) коэффициент
    returns_lag = returns[:-1]
    returns_current = returns[1:]
    
    if len(returns_lag) == 0:
        return 0
    
    correlation = np.corrcoef(returns_lag, returns_current)[0, 1]
    return -correlation  # Отрицательная корреляция указывает на возврат к среднему

def calculate_volatility_clustering(returns):
    """Расчет кластеризации волатильности"""
    if len(returns) < 2:
        return 0
    
    # Корреляция между абсолютными значениями
    abs_returns = np.abs(returns)
    return np.corrcoef(abs_returns[:-1], abs_returns[1:])[0, 1]

def calculate_volatility_persistence(returns):
    """Расчет персистентности волатильности"""
    if len(returns) < 2:
        return 0
    
    # GARCH(1,1) упрощенная версия
    abs_returns = np.abs(returns)
    return np.corrcoef(abs_returns[:-1], abs_returns[1:])[0, 1]

# Пример использования метрик производительности
def demonstrate_performance_metrics():
    """Демонстрация расчета метрик производительности"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Создание признаков
    feature_engineer = SCHRShort3FeatureEngineer()
    features = feature_engineer.create_all_features(test_data)
    
    # Создание целевых переменных
    targets = create_all_targets(test_data)
    
    # Выравнивание индексов
    common_index = features.index.intersection(targets.index)
    features = features.loc[common_index]
    targets = targets.loc[common_index]
    
    # Обучение модели
    classifier = SCHRShort3Classifier()
    classifier.train(features, targets['direction'])
    
    # Создание бэктестера
    backtester = SCHRShort3Backtester(classifier, test_data)
    
    # Бэктестинг
    start_date = test_data.index[100]
    end_date = test_data.index[-1]
    results = backtester.backtest(start_date, end_date)
    
    # Расчет метрик
    basic_metrics = calculate_schr_short3_performance_metrics(results['returns'])
    advanced_metrics = calculate_advanced_metrics(results['returns'])
    
    print("Basic Performance Metrics:")
    for key, value in basic_metrics.items():
        print(f"{key}: {value:.4f}")
    
    print("\nAdvanced Performance Metrics:")
    for key, value in advanced_metrics.items():
        print(f"{key}: {value:.4f}")
    
    return basic_metrics, advanced_metrics

if __name__ == "__main__":
    demonstrate_performance_metrics()
```

## Оптимизация параметров SCHR SHORT3

**Теория:** Оптимизация параметров SCHR SHORT3 является критически важным этапом для достижения максимальной эффективности торговой стратегии на основе краткосрочных сигналов. Правильно оптимизированные параметры могут значительно повысить производительность системы.

**Почему оптимизация параметров критична:**
- **Максимизация производительности:** Позволяет достичь максимальной производительности
- **Адаптация к рынку:** Помогает адаптироваться к различным рыночным условиям
- **Снижение рисков:** Может снизить риски стратегии
- **Повышение прибыльности:** Может значительно повысить прибыльность

### 1. Генетический алгоритм

**Теория:** Генетический алгоритм представляет собой эволюционный метод оптимизации, который имитирует процесс естественного отбора для поиска оптимальных параметров SCHR SHORT3. Это особенно эффективно для сложных многомерных задач оптимизации.

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

**Детальное объяснение оптимизации параметров:**

Оптимизация параметров SCHR SHORT3 является критически важным этапом для достижения максимальной эффективности. Каждый метод оптимизации решает специфическую задачу:

- **Генетический алгоритм:** Глобальная оптимизация с учетом множественных локальных минимумов
- **Bayesian Optimization:** Интеллектуальный поиск с учетом предыдущих оценок
- **Grid Search:** Систематический перебор параметров

```python
class SCHRShort3Optimizer:
    """
    Оптимизатор параметров SCHR SHORT3
    
    Этот класс реализует различные методы оптимизации параметров
    для достижения максимальной эффективности торговой стратегии.
    """
    
    def __init__(self, data):
        self.data = data
        self.best_params = None
        self.best_score = -np.inf
        self.optimization_history = []
        
    def optimize_genetic(self, n_generations=50, population_size=100):
        """
        Оптимизация с помощью генетического алгоритма
        
        Args:
            n_generations: Количество поколений
            population_size: Размер популяции
            
        Returns:
            Лучшие параметры и оценка
        """
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
            
            # Сохранение истории
            self.optimization_history.append({
                'generation': generation,
                'best_score': self.best_score,
                'avg_score': np.mean(scores),
                'std_score': np.std(scores)
            })
            
            print(f"Generation {generation}: Best score = {self.best_score:.4f}")
        
        return self.best_params, self.best_score
    
    def _initialize_population(self, size):
        """Инициализация популяции"""
        population = []
        
        for _ in range(size):
            params = {
                'short_term_threshold': np.random.uniform(0.3, 0.9),
                'short_term_strength': np.random.uniform(0.4, 0.95),
                'short_term_direction': np.random.uniform(0.5, 0.95),
                'short_term_volatility': np.random.uniform(0.8, 2.0),
                'short_term_momentum': np.random.uniform(0.6, 0.95)
            }
            population.append(params)
        
        return population
    
    def _evaluate_population(self, population):
        """Оценка популяции"""
        scores = []
        
        for params in population:
            try:
                score = self._evaluate_parameters(params)
                scores.append(score)
            except Exception as e:
                print(f"Error evaluating parameters: {e}")
                scores.append(-np.inf)
        
        return np.array(scores)
    
    def _evaluate_parameters(self, params):
        """Оценка параметров"""
        # Создание анализатора с данными параметрами
        analyzer = SCHRShort3Analyzer()
        analyzer.parameters.update(params)
        
        # Генерация сигналов
        signals = analyzer.generate_short_term_signal(self.data)
        
        # Расчет производительности
        performance = self._calculate_performance(signals)
        
        return performance
    
    def _calculate_performance(self, signals):
        """Расчет производительности"""
        # Упрощенный расчет производительности
        signal_accuracy = np.mean(signals['signal'] != 0)
        signal_consistency = np.mean(np.abs(signals['strength']))
        
        # Комбинированная оценка
        performance = signal_accuracy * signal_consistency
        
        return performance
    
    def _select_elite(self, population, scores, top_k=10):
        """Отбор лучших особей"""
        # Сортировка по оценкам
        sorted_indices = np.argsort(scores)[::-1]
        
        # Выбор топ-K особей
        elite = [population[i] for i in sorted_indices[:top_k]]
        
        return elite
    
    def _crossover_and_mutate(self, elite, population_size):
        """Скрещивание и мутация"""
        new_population = []
        
        # Добавление элиты
        new_population.extend(elite)
        
        # Генерация новых особей
        while len(new_population) < population_size:
            # Выбор родителей
            parent1 = np.random.choice(elite)
            parent2 = np.random.choice(elite)
            
            # Скрещивание
            child = self._crossover(parent1, parent2)
            
            # Мутация
            child = self._mutate(child)
            
            new_population.append(child)
        
        return new_population
    
    def _crossover(self, parent1, parent2):
        """Скрещивание двух особей"""
        child = {}
        
        for key in parent1.keys():
            if np.random.random() < 0.5:
                child[key] = parent1[key]
            else:
                child[key] = parent2[key]
        
        return child
    
    def _mutate(self, individual, mutation_rate=0.1):
        """Мутация особи"""
        mutated = individual.copy()
        
        for key in mutated.keys():
            if np.random.random() < mutation_rate:
                # Мутация параметра
                if key == 'short_term_threshold':
                    mutated[key] = np.random.uniform(0.3, 0.9)
                elif key == 'short_term_strength':
                    mutated[key] = np.random.uniform(0.4, 0.95)
                elif key == 'short_term_direction':
                    mutated[key] = np.random.uniform(0.5, 0.95)
                elif key == 'short_term_volatility':
                    mutated[key] = np.random.uniform(0.8, 2.0)
                elif key == 'short_term_momentum':
                    mutated[key] = np.random.uniform(0.6, 0.95)
        
        return mutated
    
    def optimize_bayesian(self, n_calls=100):
        """
        Bayesian оптимизация параметров
        
        Args:
            n_calls: Количество вызовов функции
            
        Returns:
            Лучшие параметры и оценка
        """
        from skopt import gp_minimize
        from skopt.space import Real
        
        # Определение пространства поиска
        space = [
            Real(0.3, 0.9, name='short_term_threshold'),
            Real(0.4, 0.95, name='short_term_strength'),
            Real(0.5, 0.95, name='short_term_direction'),
            Real(0.8, 2.0, name='short_term_volatility'),
            Real(0.6, 0.95, name='short_term_momentum')
        ]
        
        # Оптимизация
        result = gp_minimize(
            func=self._objective_function,
            dimensions=space,
            n_calls=n_calls,
            random_state=42
        )
        
        # Сохранение результатов
        self.best_params = {
            'short_term_threshold': result.x[0],
            'short_term_strength': result.x[1],
            'short_term_direction': result.x[2],
            'short_term_volatility': result.x[3],
            'short_term_momentum': result.x[4]
        }
        self.best_score = -result.fun
        
        return self.best_params, self.best_score
    
    def _objective_function(self, params):
        """Целевая функция для оптимизации"""
        short_term_threshold, short_term_strength, short_term_direction, short_term_volatility, short_term_momentum = params
        
        # Создание параметров
        param_dict = {
            'short_term_threshold': short_term_threshold,
            'short_term_strength': short_term_strength,
            'short_term_direction': short_term_direction,
            'short_term_volatility': short_term_volatility,
            'short_term_momentum': short_term_momentum
        }
        
        # Оценка параметров
        score = self._evaluate_parameters(param_dict)
        
        # Возвращаем отрицательное значение для минимизации
        return -score
    
    def optimize_grid_search(self, param_grid):
        """
        Оптимизация с помощью Grid Search
        
        Args:
            param_grid: Сетка параметров для поиска
            
        Returns:
            Лучшие параметры и оценка
        """
        from sklearn.model_selection import ParameterGrid
        
        best_score = -np.inf
        best_params = None
        
        # Перебор всех комбинаций параметров
        for params in ParameterGrid(param_grid):
            try:
                score = self._evaluate_parameters(params)
                
                if score > best_score:
                    best_score = score
                    best_params = params
                    
                print(f"Params: {params}, Score: {score:.4f}")
                
            except Exception as e:
                print(f"Error evaluating parameters {params}: {e}")
                continue
        
        self.best_params = best_params
        self.best_score = best_score
        
        return self.best_params, self.best_score
    
    def optimize_random_search(self, n_iter=1000):
        """
        Оптимизация с помощью Random Search
        
        Args:
            n_iter: Количество итераций
            
        Returns:
            Лучшие параметры и оценка
        """
        best_score = -np.inf
        best_params = None
        
        for i in range(n_iter):
            # Генерация случайных параметров
            params = {
                'short_term_threshold': np.random.uniform(0.3, 0.9),
                'short_term_strength': np.random.uniform(0.4, 0.95),
                'short_term_direction': np.random.uniform(0.5, 0.95),
                'short_term_volatility': np.random.uniform(0.8, 2.0),
                'short_term_momentum': np.random.uniform(0.6, 0.95)
            }
            
            try:
                score = self._evaluate_parameters(params)
                
                if score > best_score:
                    best_score = score
                    best_params = params
                    
                if i % 100 == 0:
                    print(f"Iteration {i}: Best score = {best_score:.4f}")
                    
            except Exception as e:
                print(f"Error evaluating parameters: {e}")
                continue
        
        self.best_params = best_params
        self.best_score = best_score
        
        return self.best_params, self.best_score
    
    def plot_optimization_history(self):
        """Построение графика истории оптимизации"""
        if not self.optimization_history:
            print("No optimization history available")
            return
        
        import matplotlib.pyplot as plt
        
        generations = [h['generation'] for h in self.optimization_history]
        best_scores = [h['best_score'] for h in self.optimization_history]
        avg_scores = [h['avg_score'] for h in self.optimization_history]
        
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(generations, best_scores, label='Best Score', color='blue')
        plt.plot(generations, avg_scores, label='Average Score', color='red')
        plt.xlabel('Generation')
        plt.ylabel('Score')
        plt.title('Optimization Progress')
        plt.legend()
        plt.grid(True)
        
        plt.subplot(1, 2, 2)
        plt.plot(generations, best_scores, label='Best Score', color='blue')
        plt.xlabel('Generation')
        plt.ylabel('Best Score')
        plt.title('Best Score Evolution')
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()

# Пример использования оптимизатора
def demonstrate_optimization():
    """Демонстрация оптимизации параметров"""
    # Создание тестовых данных
    test_data = create_schr_short3_data_structure()
    
    # Создание оптимизатора
    optimizer = SCHRShort3Optimizer(test_data)
    
    # Генетическая оптимизация
    print("Genetic Algorithm Optimization:")
    best_params_ga, best_score_ga = optimizer.optimize_genetic(n_generations=20, population_size=50)
    print(f"Best parameters: {best_params_ga}")
    print(f"Best score: {best_score_ga:.4f}")
    
    # Bayesian оптимизация
    print("\nBayesian Optimization:")
    best_params_bo, best_score_bo = optimizer.optimize_bayesian(n_calls=50)
    print(f"Best parameters: {best_params_bo}")
    print(f"Best score: {best_score_bo:.4f}")
    
    # Random Search
    print("\nRandom Search:")
    best_params_rs, best_score_rs = optimizer.optimize_random_search(n_iter=100)
    print(f"Best parameters: {best_params_rs}")
    print(f"Best score: {best_score_rs:.4f}")
    
    return optimizer

if __name__ == "__main__":
    demonstrate_optimization()
```

### 2. Bayesian Optimization

**Теория:** Bayesian Optimization представляет собой интеллектуальный метод оптимизации, который использует байесовскую статистику для эффективного поиска оптимальных параметров SCHR SHORT3. Это особенно эффективно для дорогих в вычислении функций.

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
from skopt.space import Real

class SCHRShort3BayesianOptimizer:
    """Bayesian оптимизация параметров SCHR SHORT3"""
    
    def __init__(self, data):
        self.data = data
        self.space = [
            Real(0.3, 0.9, name='short_term_threshold'),
            Real(0.4, 0.95, name='short_term_strength'),
            Real(0.5, 0.95, name='short_term_direction'),
            Real(0.8, 2.0, name='short_term_volatility'),
            Real(0.6, 0.95, name='short_term_momentum')
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
        short_term_threshold, short_term_strength, short_term_direction, short_term_volatility, short_term_momentum = params
        
        # Расчет SCHR SHORT3 с данными параметрами
        schr_short3_data = self._calculate_schr_short3(short_term_threshold, short_term_strength, 
                                                       short_term_direction, short_term_volatility, short_term_momentum)
        
        # Расчет производительности
        performance = self._calculate_performance(schr_short3_data)
        
        # Возвращаем отрицательное значение для минимизации
        return -performance
```

## Продакшн деплой SCHR SHORT3 модели

**Теория:** Продакшн деплой SCHR SHORT3 модели является финальным этапом создания торговой системы на основе краткосрочных сигналов, который обеспечивает развертывание модели в реальной торговой среде. Это критически важно для практического применения системы.

**Почему продакшн деплой критичен:**
- **Практическое применение:** Обеспечивает практическое применение системы
- **Автоматизация:** Автоматизирует торговые процессы
- **Масштабируемость:** Позволяет масштабировать систему
- **Мониторинг:** Обеспечивает мониторинг производительности

### 1. API для SCHR SHORT3 модели

**Теория:** API для SCHR SHORT3 модели обеспечивает программный интерфейс для взаимодействия с моделью, что критически важно для интеграции с торговыми системами и автоматизации процессов.

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

**Детальное объяснение API для SCHR SHORT3:**

API для SCHR SHORT3 модели представляет собой критически важный компонент для интеграции с торговыми системами. Он обеспечивает программный интерфейс для получения предсказаний в реальном времени, что позволяет автоматизировать торговые процессы.

**Ключевые особенности API:**
- **RESTful архитектура:** Стандартизированный подход к созданию веб-сервисов
- **Валидация данных:** Автоматическая проверка входных параметров
- **Обработка ошибок:** Надежная обработка исключительных ситуаций
- **Документация:** Автоматическая генерация документации API

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import joblib
import numpy as np
import pandas as pd
import time
import logging
from datetime import datetime
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(
    title="SCHR SHORT3 Trading API",
    description="API для краткосрочных торговых сигналов SCHR SHORT3",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Модели данных для валидации
class SCHRShort3PredictionRequest(BaseModel):
    """Запрос на предсказание SCHR SHORT3"""
    short_term_signal: int = Field(..., description="Краткосрочный сигнал (-1, 0, 1)")
    short_term_strength: float = Field(..., ge=0, le=1, description="Сила краткосрочного сигнала")
    short_term_direction: float = Field(..., ge=-1, le=1, description="Направление краткосрочного сигнала")
    short_term_volatility: float = Field(..., ge=0, description="Волатильность краткосрочного сигнала")
    short_term_momentum: float = Field(..., ge=-1, le=1, description="Моментум краткосрочного сигнала")
    additional_features: Dict[str, Any] = Field(default={}, description="Дополнительные признаки")
    timestamp: Optional[str] = Field(default=None, description="Временная метка")

class SCHRShort3PredictionResponse(BaseModel):
    """Ответ с предсказанием SCHR SHORT3"""
    prediction: int = Field(..., description="Предсказание (-1, 0, 1)")
    probability: float = Field(..., ge=0, le=1, description="Вероятность предсказания")
    confidence: str = Field(..., description="Уровень уверенности (low, medium, high)")
    short_signal_strength: float = Field(..., description="Сила краткосрочного сигнала")
    processing_time: float = Field(..., description="Время обработки в секундах")
    timestamp: str = Field(..., description="Временная метка ответа")

class HealthResponse(BaseModel):
    """Ответ о состоянии системы"""
    status: str = Field(..., description="Статус системы")
    model_loaded: bool = Field(..., description="Загружена ли модель")
    uptime: float = Field(..., description="Время работы в секундах")
    total_predictions: int = Field(..., description="Общее количество предсказаний")

# Глобальные переменные
model = None
start_time = time.time()
total_predictions = 0
performance_metrics = []

def load_model():
    """Загрузка модели SCHR SHORT3"""
    global model
    try:
        model_path = os.getenv('MODEL_PATH', 'models/schr_short3_model.pkl')
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            logger.info(f"Model loaded successfully from {model_path}")
            return True
        else:
            logger.error(f"Model file not found: {model_path}")
            return False
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

def get_model():
    """Dependency для получения модели"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return model

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    logger.info("Starting SCHR SHORT3 API...")
    load_model()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Проверка состояния API"""
    uptime = time.time() - start_time
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        uptime=uptime,
        total_predictions=total_predictions
    )

@app.post("/predict", response_model=SCHRShort3PredictionResponse)
async def predict(
    request: SCHRShort3PredictionRequest,
    background_tasks: BackgroundTasks,
    current_model=Depends(get_model)
):
    """
    Получение предсказания на основе SCHR SHORT3
    
    Этот endpoint принимает краткосрочные сигналы и возвращает предсказание
    с вероятностью и уровнем уверенности.
    """
    global total_predictions
    
    try:
        start_time_prediction = time.time()
        
        # Подготовка данных
        features = np.array([
            request.short_term_signal,
            request.short_term_strength,
            request.short_term_direction,
            request.short_term_volatility,
            request.short_term_momentum
        ]).reshape(1, -1)
        
        # Добавление дополнительных признаков
        if request.additional_features:
            additional_features = np.array(list(request.additional_features.values()))
            features = np.concatenate([features, additional_features.reshape(1, -1)], axis=1)
        
        # Получение предсказания
        prediction = current_model.predict(features)[0]
        
        # Получение вероятностей
        if hasattr(current_model, 'predict_proba'):
            probabilities = current_model.predict_proba(features)[0]
            max_probability = np.max(probabilities)
        else:
            max_probability = 0.5  # Значение по умолчанию
        
        # Определение уровня уверенности
        if max_probability > 0.8:
            confidence = "high"
        elif max_probability > 0.6:
            confidence = "medium"
        else:
            confidence = "low"
        
        # Расчет силы краткосрочного сигнала
        short_signal_strength = request.short_term_strength * abs(request.short_term_direction)
        
        processing_time = time.time() - start_time_prediction
        total_predictions += 1
        
        # Логирование
        logger.info(f"Prediction made: {prediction}, confidence: {confidence}, time: {processing_time:.3f}s")
        
        # Сохранение метрик производительности
        performance_metrics.append({
            'timestamp': datetime.now(),
            'processing_time': processing_time,
            'prediction': prediction,
            'confidence': confidence
        })
        
        # Фоновая задача для сохранения метрик
        background_tasks.add_task(save_performance_metrics)
        
        return SCHRShort3PredictionResponse(
            prediction=int(prediction),
            probability=float(max_probability),
            confidence=confidence,
            short_signal_strength=float(short_signal_strength),
            processing_time=processing_time,
            timestamp=request.timestamp or datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    """Получение метрик производительности"""
    if not performance_metrics:
        return {"message": "No metrics available yet"}
    
    # Расчет статистики
    processing_times = [m['processing_time'] for m in performance_metrics]
    
    return {
        "total_predictions": len(performance_metrics),
        "average_processing_time": np.mean(processing_times),
        "max_processing_time": np.max(processing_times),
        "min_processing_time": np.min(processing_times),
        "recent_predictions": performance_metrics[-10:]  # Последние 10 предсказаний
    }

@app.post("/retrain")
async def retrain_model(new_data_path: str):
    """Переобучение модели с новыми данными"""
    try:
        logger.info(f"Starting model retraining with data from {new_data_path}")
        
        # Загрузка новых данных
        if not os.path.exists(new_data_path):
            raise HTTPException(status_code=404, detail="Data file not found")
        
        new_data = pd.read_parquet(new_data_path)
        
        # Здесь должна быть логика переобучения модели
        # Для демонстрации просто перезагружаем модель
        success = load_model()
        
        if success:
            logger.info("Model retraining completed successfully")
            return {"status": "success", "message": "Model retrained successfully"}
        else:
            raise HTTPException(status_code=500, detail="Model retraining failed")
            
    except Exception as e:
        logger.error(f"Error in retraining: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def save_performance_metrics():
    """Сохранение метрик производительности"""
    try:
        if performance_metrics:
            # Сохранение только последних 1000 записей
            recent_metrics = performance_metrics[-1000:]
            
            # Сохранение в файл
            metrics_df = pd.DataFrame(recent_metrics)
            metrics_df.to_csv('performance_metrics.csv', index=False)
            
    except Exception as e:
        logger.error(f"Error saving performance metrics: {e}")

# Пример использования API
def demonstrate_api_usage():
    """Демонстрация использования API"""
    import requests
    import json
    
    # URL API
    api_url = "http://localhost:8000"
    
    # Пример запроса
    request_data = {
        "short_term_signal": 1,
        "short_term_strength": 0.8,
        "short_term_direction": 0.9,
        "short_term_volatility": 1.2,
        "short_term_momentum": 0.7,
        "additional_features": {
            "volume_ratio": 1.5,
            "price_change": 0.02
        }
    }
    
    try:
        # Отправка запроса
        response = requests.post(f"{api_url}/predict", json=request_data)
        
        if response.status_code == 200:
            result = response.json()
            print("Prediction result:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. Docker контейнер

**Теория:** Docker контейнеризация обеспечивает изоляцию, портабельность и масштабируемость SCHR SHORT3 модели в продакшн среде. Это критически важно для обеспечения стабильности и простоты развертывания.

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

**Детальное объяснение Docker контейнеризации:**

Docker контейнеризация SCHR SHORT3 модели обеспечивает полную изоляцию, портабельность и масштабируемость в продакшн среде. Это критически важно для обеспечения стабильности, простоты развертывания и управления зависимостями.

**Ключевые преимущества Docker:**
- **Изоляция:** Полная изоляция модели и её зависимостей
- **Портабельность:** Легкое перенесение между различными средами
- **Масштабируемость:** Простое масштабирование и оркестрация
- **Версионирование:** Контроль версий модели и зависимостей

```dockerfile
# Dockerfile для SCHR SHORT3 модели
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Создание пользователя для безопасности
RUN useradd -m -u 1000 appuser

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание необходимых директорий
RUN mkdir -p models logs data

# Установка прав доступа
RUN chown -R appuser:appuser /app

# Переключение на пользователя приложения
USER appuser

# Открытие порта
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Docker Compose для оркестрации:**

```yaml
# docker-compose.yml для SCHR SHORT3
version: '3.8'

services:
  schr-short3-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/models/schr_short3_model.pkl
      - CONFIG_PATH=/app/config/production_config.json
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/app/models
      - ./config:/app/config
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - schr-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - schr-network

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    restart: unless-stopped
    networks:
      - schr-network

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    restart: unless-stopped
    networks:
      - schr-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - schr-short3-api
    restart: unless-stopped
    networks:
      - schr-network

volumes:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  schr-network:
    driver: bridge
```

**Конфигурация Nginx для балансировки нагрузки:**

```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream schr_api {
        server schr-short3-api:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://schr_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://schr_api/health;
            access_log off;
        }
    }
}
```

**Конфигурация Prometheus для мониторинга:**

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

scrape_configs:
  - job_name: 'schr-short3-api'
    static_configs:
      - targets: ['schr-short3-api:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

**Скрипт для развертывания:**

```bash
#!/bin/bash
# deploy.sh - Скрипт развертывания SCHR SHORT3

set -e

echo "Starting SCHR SHORT3 deployment..."

# Создание необходимых директорий
mkdir -p models config logs data monitoring/grafana/dashboards monitoring/grafana/provisioning

# Копирование конфигурационных файлов
cp production_config.json config/
cp prometheus.yml monitoring/

# Сборка и запуск контейнеров
docker-compose build
docker-compose up -d

# Ожидание готовности сервисов
echo "Waiting for services to be ready..."
sleep 30

# Проверка состояния
docker-compose ps

# Проверка health check
curl -f http://localhost:8000/health || echo "Health check failed"

echo "Deployment completed successfully!"
echo "API available at: http://localhost:8000"
echo "Grafana available at: http://localhost:3000"
echo "Prometheus available at: http://localhost:9090"
```

**Пример использования Docker:**

```python
# docker_usage_example.py
import docker
import time
import requests

def deploy_schr_short3():
    """Развертывание SCHR SHORT3 с помощью Docker API"""
    client = docker.from_env()
    
    try:
        # Сборка образа
        print("Building Docker image...")
        image, build_logs = client.images.build(
            path=".",
            tag="schr-short3:latest",
            rm=True
        )
        
        # Запуск контейнера
        print("Starting container...")
        container = client.containers.run(
            "schr-short3:latest",
            ports={'8000/tcp': 8000},
            environment={
                'MODEL_PATH': '/app/models/schr_short3_model.pkl',
                'CONFIG_PATH': '/app/config/production_config.json'
            },
            volumes={
                './models': {'bind': '/app/models', 'mode': 'rw'},
                './config': {'bind': '/app/config', 'mode': 'rw'},
                './logs': {'bind': '/app/logs', 'mode': 'rw'}
            },
            detach=True,
            name="schr-short3-container"
        )
        
        # Ожидание готовности
        print("Waiting for service to be ready...")
        time.sleep(30)
        
        # Проверка состояния
        container.reload()
        print(f"Container status: {container.status}")
        
        # Тестирование API
        try:
            response = requests.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("API is ready!")
                print(f"Health status: {response.json()}")
            else:
                print(f"API not ready: {response.status_code}")
        except Exception as e:
            print(f"Error testing API: {e}")
        
        return container
        
    except Exception as e:
        print(f"Error in deployment: {e}")
        return None

def cleanup_deployment():
    """Очистка развертывания"""
    client = docker.from_env()
    
    try:
        # Остановка и удаление контейнера
        container = client.containers.get("schr-short3-container")
        container.stop()
        container.remove()
        print("Container stopped and removed")
        
        # Удаление образа
        image = client.images.get("schr-short3:latest")
        client.images.remove(image.id)
        print("Image removed")
        
    except Exception as e:
        print(f"Error in cleanup: {e}")

if __name__ == "__main__":
    # Развертывание
    container = deploy_schr_short3()
    
    if container:
        print("Deployment successful!")
        
        # Ожидание пользователя
        input("Press Enter to cleanup...")
        
        # Очистка
        cleanup_deployment()
    else:
        print("Deployment failed!")
```

### 3. Мониторинг производительности

**Теория:** Мониторинг производительности SCHR SHORT3 модели является критически важным для обеспечения стабильности и эффективности торговой системы в продакшн среде. Это позволяет быстро выявлять и устранять проблемы.

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

**Детальное объяснение мониторинга производительности:**

Мониторинг производительности SCHR SHORT3 модели является критически важным компонентом для обеспечения стабильности и эффективности торговой системы. Он позволяет в реальном времени отслеживать ключевые метрики и быстро реагировать на проблемы.

**Ключевые аспекты мониторинга:**
- **Метрики производительности:** Точность, задержка, пропускная способность
- **Метрики краткосрочных сигналов:** Частота, точность, стабильность
- **Системные метрики:** Использование ресурсов, доступность
- **Алертинг:** Автоматические уведомления о проблемах

```python
import time
import logging
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
from dataclasses import dataclass
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import psutil
import threading

@dataclass
class AlertConfig:
    """Конфигурация алертов"""
    email_enabled: bool = True
    email_recipients: List[str] = None
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    webhook_url: str = ""
    alert_cooldown: int = 300  # 5 минут

class SCHRShort3Monitor:
    """
    Комплексный мониторинг SCHR SHORT3 модели
    
    Этот класс обеспечивает полный мониторинг производительности модели,
    включая метрики точности, задержки, системные ресурсы и алертинг.
    """
    
    def __init__(self, alert_config: AlertConfig = None):
        self.performance_history = []
        self.alert_config = alert_config or AlertConfig()
        self.last_alert_time = {}
        
        # Настройка логирования
        self.logger = logging.getLogger('SCHRShort3Monitor')
        self.logger.setLevel(logging.INFO)
        
        # Пороги для алертов
        self.alert_thresholds = {
            'accuracy': 0.7,
            'short_signal_accuracy': 0.6,
            'short_signal_frequency': 0.8,
            'latency': 1.0,
            'cpu_usage': 80.0,
            'memory_usage': 85.0,
            'disk_usage': 90.0
        }
        
        # Prometheus метрики
        self._setup_prometheus_metrics()
        
        # Запуск мониторинга системных ресурсов
        self._start_system_monitoring()
    
    def _setup_prometheus_metrics(self):
        """Настройка Prometheus метрик"""
        self.prediction_counter = Counter(
            'schr_short3_predictions_total', 
            'Total number of predictions'
        )
        
        self.prediction_duration = Histogram(
            'schr_short3_prediction_duration_seconds',
            'Prediction duration in seconds'
        )
        
        self.accuracy_gauge = Gauge(
            'schr_short3_accuracy',
            'Current accuracy of the model'
        )
        
        self.short_signal_accuracy_gauge = Gauge(
            'schr_short3_short_signal_accuracy',
            'Current short signal accuracy'
        )
        
        self.system_cpu_gauge = Gauge(
            'schr_short3_system_cpu_percent',
            'System CPU usage percentage'
        )
        
        self.system_memory_gauge = Gauge(
            'schr_short3_system_memory_percent',
            'System memory usage percentage'
        )
        
        self.system_disk_gauge = Gauge(
            'schr_short3_system_disk_percent',
            'System disk usage percentage'
        )
    
    def _start_system_monitoring(self):
        """Запуск мониторинга системных ресурсов"""
        def monitor_system():
            while True:
                try:
                    # Обновление системных метрик
                    cpu_percent = psutil.cpu_percent()
                    memory_percent = psutil.virtual_memory().percent
                    disk_percent = psutil.disk_usage('/').percent
                    
                    # Обновление Prometheus метрик
                    self.system_cpu_gauge.set(cpu_percent)
                    self.system_memory_gauge.set(memory_percent)
                    self.system_disk_gauge.set(disk_percent)
                    
                    # Проверка системных алертов
                    self._check_system_alerts(cpu_percent, memory_percent, disk_percent)
                    
                    time.sleep(10)  # Обновление каждые 10 секунд
                    
                except Exception as e:
                    self.logger.error(f"Error in system monitoring: {e}")
                    time.sleep(30)
        
        # Запуск в отдельном потоке
        system_thread = threading.Thread(target=monitor_system, daemon=True)
        system_thread.start()
    
    def monitor_prediction(self, prediction: int, actual: int, latency: float, 
                          short_signal_data: Dict[str, Any]):
        """
        Мониторинг предсказания модели
        
        Args:
            prediction: Предсказание модели
            actual: Фактическое значение
            latency: Время обработки в секундах
            short_signal_data: Данные краткосрочных сигналов
        """
        try:
            # Расчет точности
            accuracy = 1 if prediction == actual else 0
            
            # Расчет метрик краткосрочных сигналов
            short_signal_accuracy = self._calculate_short_signal_accuracy(short_signal_data)
            short_signal_frequency = self._calculate_short_signal_frequency(short_signal_data)
            
            # Создание записи о производительности
            performance_record = {
                'timestamp': datetime.now(),
                'accuracy': accuracy,
                'short_signal_accuracy': short_signal_accuracy,
                'short_signal_frequency': short_signal_frequency,
                'latency': latency,
                'prediction': prediction,
                'actual': actual,
                'short_signal_data': short_signal_data
            }
            
            # Сохранение метрик
            self.performance_history.append(performance_record)
            
            # Обновление Prometheus метрик
            self.prediction_counter.inc()
            self.prediction_duration.observe(latency)
            self.accuracy_gauge.set(accuracy)
            self.short_signal_accuracy_gauge.set(short_signal_accuracy)
            
            # Проверка алертов
            self._check_alerts()
            
            # Логирование
            self.logger.info(f"Prediction monitored: accuracy={accuracy}, "
                           f"latency={latency:.3f}s, short_signal_accuracy={short_signal_accuracy:.3f}")
            
        except Exception as e:
            self.logger.error(f"Error monitoring prediction: {e}")
    
    def _calculate_short_signal_accuracy(self, short_signal_data: Dict[str, Any]) -> float:
        """Расчет точности краткосрочных сигналов"""
        try:
            if 'short_term_signal' not in short_signal_data:
                return 0.0
            
            signal = short_signal_data['short_term_signal']
            strength = short_signal_data.get('short_term_strength', 0.0)
            
            # Упрощенный расчет точности на основе силы сигнала
            return min(strength, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating short signal accuracy: {e}")
            return 0.0
    
    def _calculate_short_signal_frequency(self, short_signal_data: Dict[str, Any]) -> float:
        """Расчет частоты краткосрочных сигналов"""
        try:
            if len(self.performance_history) < 2:
                return 0.0
            
            # Подсчет сигналов за последние 10 записей
            recent_signals = self.performance_history[-10:]
            signal_count = sum(1 for record in recent_signals 
                             if record.get('short_signal_data', {}).get('short_term_signal', 0) != 0)
            
            return signal_count / len(recent_signals)
            
        except Exception as e:
            self.logger.error(f"Error calculating short signal frequency: {e}")
            return 0.0
    
    def _check_alerts(self):
        """Проверка алертов производительности"""
        if len(self.performance_history) < 10:
            return
        
        try:
            recent_performance = self.performance_history[-10:]
            
            # Проверка точности
            avg_accuracy = np.mean([p['accuracy'] for p in recent_performance])
            if avg_accuracy < self.alert_thresholds['accuracy']:
                self._send_alert("Low accuracy detected", 
                               f"Average accuracy: {avg_accuracy:.3f}")
            
            # Проверка точности краткосрочных сигналов
            avg_short_signal_accuracy = np.mean([p['short_signal_accuracy'] for p in recent_performance])
            if avg_short_signal_accuracy < self.alert_thresholds['short_signal_accuracy']:
                self._send_alert("Low short signal accuracy detected",
                               f"Average short signal accuracy: {avg_short_signal_accuracy:.3f}")
            
            # Проверка частоты краткосрочных сигналов
            avg_short_signal_frequency = np.mean([p['short_signal_frequency'] for p in recent_performance])
            if avg_short_signal_frequency < self.alert_thresholds['short_signal_frequency']:
                self._send_alert("Low short signal frequency detected",
                               f"Average short signal frequency: {avg_short_signal_frequency:.3f}")
            
            # Проверка задержки
            avg_latency = np.mean([p['latency'] for p in recent_performance])
            if avg_latency > self.alert_thresholds['latency']:
                self._send_alert("High latency detected",
                               f"Average latency: {avg_latency:.3f}s")
                
        except Exception as e:
            self.logger.error(f"Error checking alerts: {e}")
    
    def _check_system_alerts(self, cpu_percent: float, memory_percent: float, disk_percent: float):
        """Проверка системных алертов"""
        try:
            # Проверка CPU
            if cpu_percent > self.alert_thresholds['cpu_usage']:
                self._send_alert("High CPU usage detected",
                               f"CPU usage: {cpu_percent:.1f}%")
            
            # Проверка памяти
            if memory_percent > self.alert_thresholds['memory_usage']:
                self._send_alert("High memory usage detected",
                               f"Memory usage: {memory_percent:.1f}%")
            
            # Проверка диска
            if disk_percent > self.alert_thresholds['disk_usage']:
                self._send_alert("High disk usage detected",
                               f"Disk usage: {disk_percent:.1f}%")
                
        except Exception as e:
            self.logger.error(f"Error checking system alerts: {e}")
    
    def _send_alert(self, title: str, message: str):
        """Отправка алерта"""
        try:
            # Проверка cooldown
            current_time = time.time()
            if title in self.last_alert_time:
                if current_time - self.last_alert_time[title] < self.alert_config.alert_cooldown:
                    return
            
            self.last_alert_time[title] = current_time
            
            # Логирование алерта
            self.logger.warning(f"ALERT: {title} - {message}")
            
            # Отправка email
            if self.alert_config.email_enabled and self.alert_config.email_recipients:
                self._send_email_alert(title, message)
            
            # Отправка webhook
            if self.alert_config.webhook_url:
                self._send_webhook_alert(title, message)
                
        except Exception as e:
            self.logger.error(f"Error sending alert: {e}")
    
    def _send_email_alert(self, title: str, message: str):
        """Отправка email алерта"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.alert_config.smtp_username
            msg['To'] = ', '.join(self.alert_config.email_recipients)
            msg['Subject'] = f"SCHR SHORT3 Alert: {title}"
            
            body = f"""
            SCHR SHORT3 Model Alert
            
            {title}
            
            {message}
            
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Please check the system immediately.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.alert_config.smtp_server, self.alert_config.smtp_port)
            server.starttls()
            server.login(self.alert_config.smtp_username, self.alert_config.smtp_password)
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            self.logger.error(f"Error sending email alert: {e}")
    
    def _send_webhook_alert(self, title: str, message: str):
        """Отправка webhook алерта"""
        try:
            import requests
            
            payload = {
                'title': title,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'service': 'SCHR SHORT3'
            }
            
            response = requests.post(self.alert_config.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
        except Exception as e:
            self.logger.error(f"Error sending webhook alert: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Получение сводки производительности"""
        try:
            if not self.performance_history:
                return {"message": "No performance data available"}
            
            recent_data = self.performance_history[-100:]  # Последние 100 записей
            
            return {
                'total_predictions': len(self.performance_history),
                'recent_accuracy': np.mean([p['accuracy'] for p in recent_data]),
                'recent_short_signal_accuracy': np.mean([p['short_signal_accuracy'] for p in recent_data]),
                'recent_short_signal_frequency': np.mean([p['short_signal_frequency'] for p in recent_data]),
                'recent_latency': np.mean([p['latency'] for p in recent_data]),
                'max_latency': np.max([p['latency'] for p in recent_data]),
                'min_latency': np.min([p['latency'] for p in recent_data]),
                'system_cpu': psutil.cpu_percent(),
                'system_memory': psutil.virtual_memory().percent,
                'system_disk': psutil.disk_usage('/').percent,
                'last_update': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting performance summary: {e}")
            return {"error": str(e)}
    
    def export_metrics(self, filepath: str):
        """Экспорт метрик в файл"""
        try:
            metrics_data = {
                'performance_history': self.performance_history,
                'alert_thresholds': self.alert_thresholds,
                'export_time': datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(metrics_data, f, indent=2, default=str)
            
            self.logger.info(f"Metrics exported to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error exporting metrics: {e}")
    
    def start_prometheus_server(self, port: int = 8001):
        """Запуск Prometheus сервера"""
        try:
            start_http_server(port)
            self.logger.info(f"Prometheus metrics server started on port {port}")
        except Exception as e:
            self.logger.error(f"Error starting Prometheus server: {e}")

# Пример использования мониторинга
def demonstrate_monitoring():
    """Демонстрация мониторинга SCHR SHORT3"""
    # Настройка алертов
    alert_config = AlertConfig(
        email_enabled=False,  # Отключено для демонстрации
        webhook_url="",  # Пустой для демонстрации
        alert_cooldown=60
    )
    
    # Создание монитора
    monitor = SCHRShort3Monitor(alert_config)
    
    # Запуск Prometheus сервера
    monitor.start_prometheus_server(8001)
    
    # Симуляция предсказаний
    for i in range(20):
        prediction = np.random.choice([-1, 0, 1])
        actual = np.random.choice([-1, 0, 1])
        latency = np.random.uniform(0.1, 2.0)
        
        short_signal_data = {
            'short_term_signal': prediction,
            'short_term_strength': np.random.uniform(0.5, 1.0),
            'short_term_direction': np.random.uniform(-1, 1),
            'short_term_volatility': np.random.uniform(0.5, 2.0),
            'short_term_momentum': np.random.uniform(-1, 1)
        }
        
        monitor.monitor_prediction(prediction, actual, latency, short_signal_data)
        
        # Небольшая задержка
        time.sleep(1)
    
    # Получение сводки производительности
    summary = monitor.get_performance_summary()
    print("Performance Summary:")
    print(json.dumps(summary, indent=2))
    
    # Экспорт метрик
    monitor.export_metrics('performance_metrics.json')
    
    return monitor

if __name__ == "__main__":
    demonstrate_monitoring()
```

## Следующие шаги

После анализа SCHR SHORT3 переходите к:
- **[14_advanced_practices.md](14_advanced_practices.md)** - Продвинутые практики
- **[15_portfolio_optimization.md](15_portfolio_optimization.md)** - Оптимизация портфолио

## Ключевые выводы

**Теория:** Ключевые выводы суммируют наиболее важные аспекты анализа SCHR SHORT3, которые критически важны для создания прибыльной и робастной торговой системы на основе краткосрочных сигналов.

1. **SCHR SHORT3 - мощный индикатор для краткосрочной торговли**
   - **Теория:** SCHR SHORT3 представляет собой революционный подход к краткосрочной торговле
   - **Почему важно:** Обеспечивает высокую точность краткосрочных сигналов
   - **Плюсы:** Высокая точность, краткосрочные сигналы, предсказание будущего, адаптивность
   - **Минусы:** Сложность настройки, высокие требования к ресурсам

2. **Краткосрочные сигналы - ключевой фактор для скальпинга**
   - **Теория:** Краткосрочные сигналы критически важны для скальпинга
   - **Почему важно:** Позволяет получать максимальное количество торговых возможностей
   - **Плюсы:** Максимальная частота сигналов, идеален для скальпинга, быстрые возможности
   - **Минусы:** Высокие риски, требует постоянного внимания, высокие комиссии

3. **Мультитаймфреймовый анализ - разные параметры для разных таймфреймов**
   - **Теория:** Каждый таймфрейм требует специфических параметров для максимальной эффективности
   - **Почему важно:** Обеспечивает оптимальную производительность на всех временных горизонтах
   - **Плюсы:** Оптимизация производительности, снижение рисков, повышение точности
   - **Минусы:** Сложность настройки, необходимость понимания каждого таймфрейма

4. **Высокая точность - возможность достижения 95%+ точности**
   - **Теория:** Правильно настроенная SCHR SHORT3 модель может достигать очень высокой точности
   - **Почему важно:** Высокая точность критична для прибыльной торговли
   - **Плюсы:** Высокая прибыльность, снижение рисков, уверенность в стратегии
   - **Минусы:** Высокие требования к настройке, потенциальное переобучение

5. **Продакшн готовность - полная интеграция с продакшн системами**
   - **Теория:** SCHR SHORT3 модель может быть полностью интегрирована в продакшн системы
   - **Почему важно:** Обеспечивает практическое применение системы
   - **Плюсы:** Автоматизация, масштабируемость, мониторинг
   - **Минусы:** Сложность разработки, требования к безопасности

---

**Важно:** SCHR SHORT3 требует тщательного анализа краткосрочных сигналов и адаптации параметров для каждого актива и таймфрейма.
