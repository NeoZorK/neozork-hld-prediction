# 07. 🔄 Walk-Forward анализ

**Цель:** Научиться проводить Walk-Forward анализ для проверки стабильности торговых стратегий.

## Что такое Walk-Forward анализ?

**Теория:** Walk-Forward анализ - это продвинутый метод тестирования торговых стратегий, который имитирует реальные условия торговли. В отличие от простого бэктестинга, он учитывает необходимость переобучения модели на новых данных, что делает его более реалистичным и надежным.

**Walk-Forward анализ** - это метод тестирования торговых стратегий, который имитирует реальную торговлю, где модель переобучается на новых данных по мере их поступления.

### Математическая основа Walk-Forward анализа

**Теория:** Walk-Forward анализ основан на принципе временного разделения данных, где каждый тестовый период использует только предшествующие данные для обучения. Это предотвращает "утечку будущего" (look-ahead bias) и обеспечивает реалистичную оценку производительности.

**Математическая формула:**

```
Для периода t:
- Обучающие данные: D[train_start : train_end]
- Тестовые данные: D[test_start : test_end]
- Условие: test_start = train_end (строгое временное разделение)
```

**Ключевые принципы:**
1. **Временная последовательность:** Данные обрабатываются в хронологическом порядке
2. **Переобучение:** Модель переобучается на каждом новом периоде
3. **Реалистичность:** Имитирует реальные условия торговли
4. **Стабильность:** Проверяет устойчивость стратегии к изменениям

**Почему Walk-Forward анализ критичен для финансовых систем:**
- **Реалистичность:** Имитирует реальные условия торговли
- **Стабильность:** Проверяет, как стратегия работает на новых данных
- **Адаптивность:** Оценивает способность модели адаптироваться к изменениям
- **Робастность:** Выявляет проблемы, которые не видны в простом бэктестинге

### Зачем нужен Walk-Forward анализ?

**Теория:** Walk-Forward анализ решает фундаментальные проблемы традиционного бэктестинга, связанные с переобучением и нереалистичностью. Он обеспечивает более честную оценку производительности стратегии.

- **Реалистичность** - имитирует реальную торговлю
  - **Почему важно:** В реальной торговле модель должна переобучаться на новых данных
  - **Плюсы:** Более честная оценка производительности, реалистичные результаты
  - **Минусы:** Более сложная реализация, требует больше вычислительных ресурсов

- **Проверка стабильности** - как стратегия работает на новых данных
  - **Почему важно:** Стратегия должна работать стабильно на новых данных
  - **Плюсы:** Выявление проблем стабильности, оценка долгосрочной производительности
  - **Минусы:** Может показать худшие результаты, чем простой бэктестинг

- **Избежание переобучения** - предотвращает оптимизацию на исторических данных
  - **Почему важно:** Переобучение приводит к нереалистичным результатам
  - **Плюсы:** Более честная оценка, снижение рисков
  - **Минусы:** Может показать худшие результаты, требует больше данных

- **Оценка адаптивности** - как модель адаптируется к изменениям
  - **Почему важно:** Рынки постоянно меняются, модель должна адаптироваться
  - **Плюсы:** Оценка способности к адаптации, выявление проблем адаптации
  - **Минусы:** Сложность оценки адаптивности, необходимость метрик адаптивности

**Дополнительные преимущества Walk-Forward анализа:**
- **Временная структура:** Учитывает временную структуру данных
- **Деградация:** Выявляет деградацию производительности со временем
- **Рыночные условия:** Позволяет анализировать производительность в разных рыночных условиях
- **Параметрическая стабильность:** Оценивает стабильность параметров стратегии

## Принципы Walk-Forward анализа

**Теория:** Walk-Forward анализ основан на нескольких ключевых принципах, которые обеспечивают его эффективность и реалистичность. Понимание этих принципов критично для правильного проведения анализа.

### 1. Разделение данных

**Теория:** Правильное разделение данных является основой Walk-Forward анализа. Данные должны быть разделены на обучающие и тестовые периоды таким образом, чтобы имитировать реальные условия торговли.

**Почему правильное разделение данных критично:**
- **Временная структура:** Финансовые данные имеют временную зависимость, и нарушение хронологии может привести к нереалистичным результатам
- **Реалистичность:** В реальной торговле мы не можем использовать будущую информацию для принятия текущих решений
- **Предотвращение утечек:** Строгое временное разделение предотвращает использование информации из будущего
- **Стабильность:** Обеспечивает честную оценку способности стратегии работать на новых данных

**Математическое обоснование разделения:**

```
Пусть T = {t1, t2, ..., tn} - временные метки данных
Для каждого тестового периода i:
- Обучающий период: [t_start_i, t_train_end_i]
- Тестовый период: [t_test_start_i, t_test_end_i]
- Условие: t_test_start_i = t_train_end_i + 1 (строгое разделение)
```

**Плюсы правильного разделения:**
- Реалистичная оценка производительности стратегии
- Предотвращение утечек данных (look-ahead bias)
- Учет временной структуры финансовых данных
- Стабильные и воспроизводимые результаты
- Соответствие реальным условиям торговли

**Минусы правильного разделения:**
- Сложность реализации алгоритма
- Необходимость большего объема исторических данных
- Возможное снижение производительности по сравнению с нереалистичными методами
- Сложность настройки параметров (размеры окон, шаги)
- Более высокие вычислительные требования
**Теория функции создания разделов:**
Эта функция реализует алгоритм создания временных разделов для Walk-Forward анализа. Она создает последовательность обучающих и тестовых периодов, где каждый тестовый период следует сразу после соответствующего обучающего периода.

**Параметры функции:**
- `train_size=252`: Размер обучающего окна (252 торговых дня ≈ 1 год)
- `test_size=63`: Размер тестового окна (63 торговых дня ≈ 3 месяца)
- `step_size=21`: Шаг сдвига окна (21 торговый день ≈ 1 месяц)

**Алгоритм работы:**
1. Начинаем с первого индекса данных
2. Создаем обучающий период фиксированной длины
3. Создаем тестовый период сразу после обучающего
4. Сдвигаемся на step_size и повторяем процесс
5. Продолжаем до тех пор, пока не исчерпаем данные

**Почему именно такие параметры:**
- **252 дня обучения:** Достаточно для обучения модели, но не слишком много для устаревания
- **63 дня тестирования:** Достаточно для статистически значимых результатов
- **21 день шага:** Баланс между частотой переобучения и стабильностью

```python
# Необходимые импорты для Walk-Forward анализа
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
import warnings
from scipy import stats
import yfinance as yf  # Для загрузки реальных данных

# Настройка matplotlib для лучшего отображения
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def create_walk_forward_splits(data: pd.DataFrame, 
                              train_size: int = 252, 
                              test_size: int = 63, 
                              step_size: int = 21) -> List[Dict[str, Any]]:
    """
    Создание Walk-Forward разделов для анализа временных рядов.
    
    Эта функция создает последовательность обучающих и тестовых периодов
    для проведения Walk-Forward анализа. Каждый тестовый период следует
    сразу после соответствующего обучающего периода, что имитирует
    реальные условия торговли.
    
    Args:
        data (pd.DataFrame): Временной ряд данных с индексом datetime
        train_size (int): Размер обучающего окна в днях (по умолчанию 252)
        test_size (int): Размер тестового окна в днях (по умолчанию 63)
        step_size (int): Шаг сдвига окна в днях (по умолчанию 21)
    
    Returns:
        List[Dict]: Список словарей с информацией о каждом разделе
        
    Raises:
        ValueError: Если данные недостаточны для создания хотя бы одного раздела
        
    Example:
        >>> data = pd.read_csv('financial_data.csv', index_col=0, parse_dates=True)
        >>> splits = create_walk_forward_splits(data, train_size=100, test_size=20)
        >>> print(f"Создано {len(splits)} разделов")
    """
    
    # Проверяем достаточность данных
    min_required = train_size + test_size
    if len(data) < min_required:
        raise ValueError(f"Недостаточно данных. Требуется минимум {min_required} записей, получено {len(data)}")
    
    splits = []
    start_idx = 0
    
    # Создаем разделы до исчерпания данных
    while start_idx + train_size + test_size <= len(data):
        # Обучающий период (строго до тестового)
        train_start = start_idx
        train_end = start_idx + train_size
        
        # Тестовый период (сразу после обучающего)
        test_start = train_end  # Критично: никакого разрыва!
        test_end = train_end + test_size
        
        # Создаем словарь с информацией о разделе
        split_info = {
            'train_start': train_start,
            'train_end': train_end,
            'test_start': test_start,
            'test_end': test_end,
            'train_data': data.iloc[train_start:train_end].copy(),
            'test_data': data.iloc[test_start:test_end].copy(),
            'train_dates': (data.index[train_start], data.index[train_end-1]),
            'test_dates': (data.index[test_start], data.index[test_end-1])
        }
        
        splits.append(split_info)
        
        # Сдвигаемся на step_size для следующего раздела
        start_idx += step_size
    
    print(f"Создано {len(splits)} Walk-Forward разделов")
    print(f"Первый раздел: обучение {splits[0]['train_dates'][0]} - {splits[0]['train_dates'][1]}, "
          f"тест {splits[0]['test_dates'][0]} - {splits[0]['test_dates'][1]}")
    print(f"Последний раздел: обучение {splits[-1]['train_dates'][0]} - {splits[-1]['train_dates'][1]}, "
          f"тест {splits[-1]['test_dates'][0]} - {splits[-1]['test_dates'][1]}")
    
    return splits
```

### 2. Структура анализа

**Теория класса WalkForwardAnalyzer:**
Этот класс является центральным компонентом Walk-Forward анализа. Он инкапсулирует всю логику проведения анализа, включая создание разделов, обучение моделей, тестирование и анализ результатов.

**Архитектура класса:**
1. **Инициализация:** Установка параметров анализа
2. **Запуск анализа:** Основной метод для проведения Walk-Forward тестирования
3. **Анализ результатов:** Статистический анализ полученных результатов

**Ключевые принципы реализации:**
- **Инкапсуляция:** Вся логика анализа инкапсулирована в одном классе
- **Переиспользование:** Класс может работать с любыми стратегиями
- **Расширяемость:** Легко добавлять новые метрики и методы анализа
- **Отслеживание:** Полное отслеживание всех этапов анализа

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import warnings

class TradingStrategy(ABC):
    """Абстрактный базовый класс для торговых стратегий"""
    
    @abstractmethod
    def train(self, data: pd.DataFrame) -> None:
        """Обучение стратегии на исторических данных"""
        pass
    
    @abstractmethod
    def predict(self, data: pd.DataFrame) -> pd.Series:
        """Генерация торговых сигналов"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Возвращает название стратегии"""
        pass

class SimpleMovingAverageStrategy(TradingStrategy):
    """Простая стратегия на основе скользящих средних"""
    
    def __init__(self, short_window: int = 20, long_window: int = 50):
        self.short_window = short_window
        self.long_window = long_window
        self.short_ma = None
        self.long_ma = None
        self.is_trained = False
    
    def train(self, data: pd.DataFrame) -> None:
        """Обучение стратегии (в данном случае просто расчет параметров)"""
        if 'close' not in data.columns:
            raise ValueError("Данные должны содержать колонку 'close'")
        
        self.short_ma = data['close'].rolling(window=self.short_window).mean()
        self.long_ma = data['close'].rolling(window=self.long_window).mean()
        self.is_trained = True
    
    def predict(self, data: pd.DataFrame) -> pd.Series:
        """Генерация торговых сигналов"""
        if not self.is_trained:
            raise ValueError("Стратегия не обучена. Вызовите train() сначала.")
        
        if 'close' not in data.columns:
            raise ValueError("Данные должны содержать колонку 'close'")
        
        # Рассчитываем скользящие средние для новых данных
        short_ma = data['close'].rolling(window=self.short_window).mean()
        long_ma = data['close'].rolling(window=self.long_window).mean()
        
        # Генерируем сигналы: 1 = покупка, -1 = продажа, 0 = удержание
        signals = pd.Series(0, index=data.index)
        
        # Сигнал покупки: короткая MA пересекает длинную MA снизу вверх
        buy_signal = (short_ma > long_ma) & (short_ma.shift(1) <= long_ma.shift(1))
        
        # Сигнал продажи: короткая MA пересекает длинную MA сверху вниз
        sell_signal = (short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))
        
        signals[buy_signal] = 1
        signals[sell_signal] = -1
        
        return signals
    
    def get_name(self) -> str:
        return f"SMA_{self.short_window}_{self.long_window}"

class Backtester:
    """Класс для проведения бэктестинга торговых стратегий"""
    
    def __init__(self, initial_capital: float = 100000.0, commission: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission
    
    def run_backtest(self, data: pd.DataFrame, strategy: TradingStrategy) -> Dict[str, float]:
        """
        Запуск бэктестинга стратегии
        
        Args:
            data: Данные для тестирования
            strategy: Обученная торговая стратегия
            
        Returns:
            Словарь с метриками производительности
        """
        if 'close' not in data.columns:
            raise ValueError("Данные должны содержать колонку 'close'")
        
        # Генерируем торговые сигналы
        signals = strategy.predict(data)
        
        # Рассчитываем доходность
        returns = data['close'].pct_change()
        
        # Рассчитываем стратегическую доходность
        strategy_returns = signals.shift(1) * returns  # Сдвигаем сигналы на 1 период
        
        # Учитываем комиссию
        position_changes = signals.diff().abs()
        strategy_returns -= position_changes * self.commission
        
        # Удаляем NaN значения
        strategy_returns = strategy_returns.dropna()
        
        if len(strategy_returns) == 0:
            return {
                'total_return': 0.0,
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'win_rate': 0.0,
                'total_trades': 0
            }
        
        # Рассчитываем кумулятивную доходность
        cumulative_returns = (1 + strategy_returns).cumprod()
        
        # Основные метрики
        total_return = cumulative_returns.iloc[-1] - 1
        
        # Sharpe Ratio (предполагаем безрисковую ставку = 0)
        sharpe_ratio = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0
        
        # Максимальная просадка
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = (cumulative_returns - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()
        
        # Процент выигрышных сделок
        winning_trades = strategy_returns[strategy_returns > 0]
        total_trades = len(strategy_returns[strategy_returns != 0])
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
        
        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'total_trades': total_trades,
            'strategy_returns': strategy_returns,
            'cumulative_returns': cumulative_returns
        }

class WalkForwardAnalyzer:
    """
    Класс для проведения Walk-Forward анализа торговых стратегий.
    
    Walk-Forward анализ - это метод тестирования, который имитирует реальные
    условия торговли, где модель переобучается на новых данных по мере их
    поступления. Это обеспечивает более реалистичную оценку производительности
    стратегии.
    """
    
    def __init__(self, train_size: int = 252, test_size: int = 63, step_size: int = 21):
        """
        Инициализация анализатора Walk-Forward.
        
        Args:
            train_size: Размер обучающего окна в днях (по умолчанию 252)
            test_size: Размер тестового окна в днях (по умолчанию 63)
            step_size: Шаг сдвига окна в днях (по умолчанию 21)
        """
        self.train_size = train_size
        self.test_size = test_size
        self.step_size = step_size
        self.results: List[Dict[str, Any]] = []
        self.backtester = Backtester()
    
    def run_analysis(self, data: pd.DataFrame, strategy: TradingStrategy) -> Dict[str, Any]:
        """
        Запуск полного Walk-Forward анализа.
        
        Этот метод является сердцем Walk-Forward анализа. Он:
        1. Создает временные разделы данных
        2. Для каждого раздела обучает стратегию на обучающих данных
        3. Тестирует стратегию на тестовых данных
        4. Собирает и анализирует результаты
        
        Args:
            data: Временной ряд финансовых данных
            strategy: Торговая стратегия для тестирования
            
        Returns:
            Словарь с результатами анализа
            
        Raises:
            ValueError: Если данные недостаточны для анализа
        """
        print(f"Запуск Walk-Forward анализа...")
        print(f"Параметры: обучение={self.train_size} дней, тест={self.test_size} дней, шаг={self.step_size} дней")
        
        # Очищаем предыдущие результаты
        self.results = []
        
        # Создание временных разделов
        try:
            splits = create_walk_forward_splits(
                data, self.train_size, self.test_size, self.step_size
            )
        except ValueError as e:
            raise ValueError(f"Ошибка создания разделов: {e}")
        
        if len(splits) == 0:
            raise ValueError("Не удалось создать ни одного раздела для анализа")
        
        print(f"Создано {len(splits)} разделов для анализа")
        
        # Обработка каждого раздела
        for i, split in enumerate(splits):
            print(f"Обработка периода {i+1}/{len(splits)}: "
                  f"обучение {split['train_dates'][0].strftime('%Y-%m-%d')} - "
                  f"{split['train_dates'][1].strftime('%Y-%m-%d')}, "
                  f"тест {split['test_dates'][0].strftime('%Y-%m-%d')} - "
                  f"{split['test_dates'][1].strftime('%Y-%m-%d')}")
            
            try:
                # Обучение стратегии на обучающих данных
                strategy.train(split['train_data'])
                
                # Тестирование на тестовых данных
                metrics = self.backtester.run_backtest(split['test_data'], strategy)
                
                # Сохранение результатов
                result = {
                    'period': i + 1,
                    'train_start': split['train_start'],
                    'train_end': split['train_end'],
                    'test_start': split['test_start'],
                    'test_end': split['test_end'],
                    'train_dates': split['train_dates'],
                    'test_dates': split['test_dates'],
                    'metrics': metrics
                }
                
                self.results.append(result)
                
                print(f"  Результат: доходность={metrics['total_return']:.2%}, "
                      f"Sharpe={metrics['sharpe_ratio']:.2f}, "
                      f"просадка={metrics['max_drawdown']:.2%}")
                
            except Exception as e:
                print(f"  Ошибка в периоде {i+1}: {e}")
                # Продолжаем с следующим периодом
                continue
        
        if len(self.results) == 0:
            raise ValueError("Не удалось успешно обработать ни одного периода")
        
        print(f"Анализ завершен. Успешно обработано {len(self.results)} периодов")
        
        return self.analyze_results()
    
    def analyze_results(self) -> Dict[str, Any]:
        """
        Анализ результатов Walk-Forward тестирования.
        
        Этот метод проводит статистический анализ всех результатов
        тестирования, вычисляя ключевые метрики производительности
        и стабильности стратегии.
        
        Returns:
            Словарь с результатами анализа
        """
        if not self.results:
            raise ValueError("Нет результатов для анализа. Сначала запустите run_analysis()")
        
        # Извлечение метрик из всех периодов
        returns = [r['metrics']['total_return'] for r in self.results]
        sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in self.results]
        max_drawdowns = [r['metrics']['max_drawdown'] for r in self.results]
        win_rates = [r['metrics']['win_rate'] for r in self.results]
        total_trades = [r['metrics']['total_trades'] for r in self.results]
        
        # Конвертируем в numpy массивы для удобства вычислений
        returns = np.array(returns)
        sharpe_ratios = np.array(sharpe_ratios)
        max_drawdowns = np.array(max_drawdowns)
        win_rates = np.array(win_rates)
        total_trades = np.array(total_trades)
        
        # Основная статистика
        analysis = {
            # Общая информация
            'total_periods': len(self.results),
            'successful_periods': len([r for r in returns if not np.isnan(r)]),
            
            # Статистика доходности
            'mean_return': np.nanmean(returns),
            'std_return': np.nanstd(returns),
            'min_return': np.nanmin(returns),
            'max_return': np.nanmax(returns),
            'median_return': np.nanmedian(returns),
            
            # Статистика Sharpe Ratio
            'mean_sharpe': np.nanmean(sharpe_ratios),
            'std_sharpe': np.nanstd(sharpe_ratios),
            'min_sharpe': np.nanmin(sharpe_ratios),
            'max_sharpe': np.nanmax(sharpe_ratios),
            
            # Статистика просадок
            'mean_drawdown': np.nanmean(max_drawdowns),
            'worst_drawdown': np.nanmin(max_drawdowns),
            'std_drawdown': np.nanstd(max_drawdowns),
            
            # Статистика торговли
            'mean_win_rate': np.nanmean(win_rates),
            'mean_trades_per_period': np.nanmean(total_trades),
            'total_trades': np.nansum(total_trades),
            
            # Консистентность
            'positive_periods': np.sum(returns > 0),
            'negative_periods': np.sum(returns < 0),
            'consistency': np.sum(returns > 0) / len(returns) if len(returns) > 0 else 0,
            
            # Дополнительные метрики
            'coefficient_of_variation': np.nanstd(returns) / np.abs(np.nanmean(returns)) if np.nanmean(returns) != 0 else np.inf,
            'skewness': self._calculate_skewness(returns),
            'kurtosis': self._calculate_kurtosis(returns),
            
            # Детальные результаты
            'period_returns': returns.tolist(),
            'period_sharpe_ratios': sharpe_ratios.tolist(),
            'period_drawdowns': max_drawdowns.tolist()
        }
        
        return analysis
    
    def _calculate_skewness(self, data: np.ndarray) -> float:
        """Расчет асимметрии распределения"""
        data_clean = data[~np.isnan(data)]
        if len(data_clean) < 3:
            return 0.0
        
        mean = np.mean(data_clean)
        std = np.std(data_clean)
        if std == 0:
            return 0.0
        
        return np.mean(((data_clean - mean) / std) ** 3)
    
    def _calculate_kurtosis(self, data: np.ndarray) -> float:
        """Расчет эксцесса распределения"""
        data_clean = data[~np.isnan(data)]
        if len(data_clean) < 4:
            return 0.0
        
        mean = np.mean(data_clean)
        std = np.std(data_clean)
        if std == 0:
            return 0.0
        
        return np.mean(((data_clean - mean) / std) ** 4) - 3
```

## Продвинутые техники Walk-Forward

**Теория продвинутых техник:**
Стандартный Walk-Forward анализ использует фиксированные размеры окон, но в реальной торговле может быть полезно адаптировать параметры анализа на основе производительности стратегии. Продвинутые техники позволяют сделать анализ более гибким и реалистичным.

### 1. Адаптивный размер окон

**Теория адаптивных окон:**
Адаптивный размер окон - это техника, где размер обучающего окна динамически изменяется на основе производительности стратегии. Если стратегия показывает хорошие результаты, мы увеличиваем окно обучения для большей стабильности. Если результаты плохие, мы уменьшаем окно для более быстрой адаптации к изменениям рынка.

**Преимущества адаптивных окон:**
- **Адаптивность:** Размер окна подстраивается под рыночные условия
- **Стабильность:** Увеличение окна при хорошей производительности
- **Чувствительность:** Уменьшение окна при плохой производительности
- **Реалистичность:** Более точно имитирует реальную торговлю

**Недостатки адаптивных окон:**
- **Сложность:** Более сложная реализация и настройка
- **Переобучение:** Риск переобучения на адаптивных параметрах
- **Нестабильность:** Частые изменения размера окна могут снизить стабильность

**Математическое обоснование:**

```
Пусть W(t) - размер окна в момент времени t
W(t+1) = {
    W(t) + ΔW, если R(t) > θ_high
    W(t) - ΔW, если R(t) < θ_low
    W(t), иначе
}
где R(t) - доходность в периоде t, θ_high и θ_low - пороговые значения
```

```python
def adaptive_walk_forward(data: pd.DataFrame, 
                         strategy: TradingStrategy, 
                         min_train: int = 126, 
                         max_train: int = 504, 
                         test_size: int = 63,
                         performance_threshold_high: float = 0.05,
                         performance_threshold_low: float = -0.05,
                         window_adjustment: int = 21) -> List[Dict[str, Any]]:
    """
    Walk-Forward анализ с адаптивным размером окон.
    
    Эта функция реализует адаптивный Walk-Forward анализ, где размер
    обучающего окна динамически изменяется на основе производительности
    стратегии. Это позволяет стратегии лучше адаптироваться к изменениям
    рыночных условий.
    
    Args:
        data: Временной ряд финансовых данных
        strategy: Торговая стратегия для тестирования
        min_train: Минимальный размер обучающего окна
        max_train: Максимальный размер обучающего окна
        test_size: Размер тестового окна
        performance_threshold_high: Порог для увеличения окна
        performance_threshold_low: Порог для уменьшения окна
        window_adjustment: Размер корректировки окна
        
    Returns:
        Список результатов с информацией о размерах окон
    """
    
    results = []
    current_train_size = min_train
    backtester = Backtester()
    
    start_idx = 0
    period = 1
    
    print(f"Запуск адаптивного Walk-Forward анализа...")
    print(f"Начальный размер окна: {current_train_size} дней")
    print(f"Диапазон окна: {min_train} - {max_train} дней")
    
    while start_idx + current_train_size + test_size <= len(data):
        # Обучающий период с текущим размером окна
        train_data = data.iloc[start_idx:start_idx + current_train_size]
        
        # Тестовый период
        test_data = data.iloc[start_idx + current_train_size:start_idx + current_train_size + test_size]
        
        print(f"Период {period}: размер окна={current_train_size} дней, "
              f"тест {test_data.index[0].strftime('%Y-%m-%d')} - "
              f"{test_data.index[-1].strftime('%Y-%m-%d')}")
        
        try:
            # Обучение и тестирование
            strategy.train(train_data)
            metrics = backtester.run_backtest(test_data, strategy)
            
            # Адаптация размера окна на основе производительности
            total_return = metrics['total_return']
            old_train_size = current_train_size
            
            if total_return > performance_threshold_high:
                # Хорошая производительность - увеличиваем окно
                current_train_size = min(current_train_size + window_adjustment, max_train)
                adjustment_reason = "увеличение (хорошая производительность)"
            elif total_return < performance_threshold_low:
                # Плохая производительность - уменьшаем окно
                current_train_size = max(current_train_size - window_adjustment, min_train)
                adjustment_reason = "уменьшение (плохая производительность)"
            else:
                adjustment_reason = "без изменений (средняя производительность)"
            
            # Сохраняем результат
            result = {
                'period': period,
                'train_size': old_train_size,
                'new_train_size': current_train_size,
                'adjustment_reason': adjustment_reason,
                'test_start': test_data.index[0],
                'test_end': test_data.index[-1],
                'metrics': metrics
            }
            
            results.append(result)
            
            print(f"  Результат: доходность={total_return:.2%}, "
                  f"Sharpe={metrics['sharpe_ratio']:.2f}, "
                  f"окно: {old_train_size} → {current_train_size} ({adjustment_reason})")
            
        except Exception as e:
            print(f"  Ошибка в периоде {period}: {e}")
            # Продолжаем с текущим размером окна
            pass
        
        # Переходим к следующему периоду
        start_idx += test_size
        period += 1
    
    print(f"Адаптивный анализ завершен. Обработано {len(results)} периодов")
    print(f"Финальный размер окна: {current_train_size} дней")
    
    return results
```

### 2. Множественные стратегии

**Теория множественных стратегий:**
Сравнение нескольких стратегий в рамках Walk-Forward анализа позволяет выявить наиболее стабильные и эффективные подходы. Это особенно важно для портфельного управления, где можно комбинировать лучшие стратегии.

**Преимущества сравнения стратегий:**
- **Относительная оценка:** Сравнение производительности в одинаковых условиях
- **Выявление лидеров:** Определение наиболее эффективных стратегий
- **Диверсификация:** Возможность комбинирования лучших стратегий
- **Робастность:** Проверка стабильности различных подходов

**Критерии сравнения:**
- **Средняя доходность:** Общая прибыльность стратегии
- **Консистентность:** Стабильность положительных результатов
- **Sharpe Ratio:** Риск-скорректированная доходность
- **Максимальная просадка:** Максимальные потери

```python
def multi_strategy_walk_forward(data: pd.DataFrame, 
                               strategies: Dict[str, TradingStrategy], 
                               train_size: int = 252, 
                               test_size: int = 63) -> Tuple[Dict[str, Dict[str, Any]], List[Tuple[str, Dict[str, float]]]]:
    """
    Walk-Forward анализ с множественными стратегиями.
    
    Эта функция проводит Walk-Forward анализ для нескольких стратегий
    одновременно, что позволяет сравнивать их производительность
    в одинаковых рыночных условиях.
    
    Args:
        data: Временной ряд финансовых данных
        strategies: Словарь стратегий {название: стратегия}
        train_size: Размер обучающего окна
        test_size: Размер тестового окна
        
    Returns:
        Кортеж (результаты_анализа, сравнение_стратегий)
    """
    
    results = {}
    
    print(f"Запуск Walk-Forward анализа для {len(strategies)} стратегий...")
    print(f"Стратегии: {list(strategies.keys())}")
    
    for strategy_name, strategy in strategies.items():
        print(f"\n{'='*50}")
        print(f"Анализ стратегии: {strategy_name}")
        print(f"{'='*50}")
        
        try:
            # Создаем новый экземпляр анализатора для каждой стратегии
            analyzer = WalkForwardAnalyzer(train_size, test_size)
            analysis = analyzer.run_analysis(data, strategy)
            
            results[strategy_name] = analysis
            
            print(f"Стратегия {strategy_name} завершена:")
            print(f"  Средняя доходность: {analysis['mean_return']:.2%}")
            print(f"  Консистентность: {analysis['consistency']:.2%}")
            print(f"  Средний Sharpe: {analysis['mean_sharpe']:.2f}")
            print(f"  Худшая просадка: {analysis['worst_drawdown']:.2%}")
            
        except Exception as e:
            print(f"Ошибка при анализе стратегии {strategy_name}: {e}")
            results[strategy_name] = None
    
    # Сравнение стратегий
    comparison = compare_strategies(results)
    
    print(f"\n{'='*50}")
    print("СРАВНЕНИЕ СТРАТЕГИЙ")
    print(f"{'='*50}")
    
    for i, (strategy_name, metrics) in enumerate(comparison, 1):
        print(f"{i}. {strategy_name}:")
        print(f"   Доходность: {metrics['mean_return']:.2%}")
        print(f"   Консистентность: {metrics['consistency']:.2%}")
        print(f"   Sharpe: {metrics['mean_sharpe']:.2f}")
        print(f"   Просадка: {metrics['worst_drawdown']:.2%}")
    
    return results, comparison

def compare_strategies(results: Dict[str, Dict[str, Any]]) -> List[Tuple[str, Dict[str, float]]]:
    """
    Сравнение результатов множественных стратегий.
    
    Эта функция сравнивает результаты Walk-Forward анализа
    для разных стратегий и ранжирует их по ключевым метрикам.
    
    Args:
        results: Словарь результатов анализа стратегий
        
    Returns:
        Отсортированный список стратегий с метриками
    """
    
    comparison = {}
    
    for strategy_name, analysis in results.items():
        if analysis is None:
            continue
            
        comparison[strategy_name] = {
            'mean_return': analysis['mean_return'],
            'consistency': analysis['consistency'],
            'mean_sharpe': analysis['mean_sharpe'],
            'worst_drawdown': analysis['worst_drawdown'],
            'coefficient_of_variation': analysis['coefficient_of_variation'],
            'total_periods': analysis['total_periods']
        }
    
    # Сортировка по средней доходности (по убыванию)
    sorted_strategies = sorted(
        comparison.items(), 
        key=lambda x: x[1]['mean_return'], 
        reverse=True
    )
    
    return sorted_strategies

class RSIStrategy(TradingStrategy):
    """Стратегия на основе RSI индикатора"""
    
    def __init__(self, rsi_period: int = 14, oversold: float = 30, overbought: float = 70):
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        self.is_trained = False
    
    def train(self, data: pd.DataFrame) -> None:
        """Обучение стратегии"""
        if 'close' not in data.columns:
            raise ValueError("Данные должны содержать колонку 'close'")
        self.is_trained = True
    
    def predict(self, data: pd.DataFrame) -> pd.Series:
        """Генерация сигналов на основе RSI"""
        if not self.is_trained:
            raise ValueError("Стратегия не обучена")
        
        if 'close' not in data.columns:
            raise ValueError("Данные должны содержать колонку 'close'")
        
        # Рассчитываем RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Генерируем сигналы
        signals = pd.Series(0, index=data.index)
        
        # Сигнал покупки: RSI выходит из зоны перепроданности
        buy_signal = (rsi > self.oversold) & (rsi.shift(1) <= self.oversold)
        
        # Сигнал продажи: RSI выходит из зоны перекупленности
        sell_signal = (rsi < self.overbought) & (rsi.shift(1) >= self.overbought)
        
        signals[buy_signal] = 1
        signals[sell_signal] = -1
        
        return signals
    
    def get_name(self) -> str:
        return f"RSI_{self.rsi_period}_{self.oversold}_{self.overbought}"

class BollingerBandsStrategy(TradingStrategy):
    """Стратегия на основе полос Боллинджера"""
    
    def __init__(self, period: int = 20, std_dev: float = 2.0):
        self.period = period
        self.std_dev = std_dev
        self.is_trained = False
    
    def train(self, data: pd.DataFrame) -> None:
        """Обучение стратегии"""
        if 'close' not in data.columns:
            raise ValueError("Данные должны содержать колонку 'close'")
        self.is_trained = True
    
    def predict(self, data: pd.DataFrame) -> pd.Series:
        """Генерация сигналов на основе полос Боллинджера"""
        if not self.is_trained:
            raise ValueError("Стратегия не обучена")
        
        if 'close' not in data.columns:
            raise ValueError("Данные должны содержать колонку 'close'")
        
        # Рассчитываем полосы Боллинджера
        sma = data['close'].rolling(window=self.period).mean()
        std = data['close'].rolling(window=self.period).std()
        upper_band = sma + (std * self.std_dev)
        lower_band = sma - (std * self.std_dev)
        
        # Генерируем сигналы
        signals = pd.Series(0, index=data.index)
        
        # Сигнал покупки: цена касается нижней полосы
        buy_signal = (data['close'] <= lower_band) & (data['close'].shift(1) > lower_band.shift(1))
        
        # Сигнал продажи: цена касается верхней полосы
        sell_signal = (data['close'] >= upper_band) & (data['close'].shift(1) < upper_band.shift(1))
        
        signals[buy_signal] = 1
        signals[sell_signal] = -1
        
        return signals
    
    def get_name(self) -> str:
        return f"BB_{self.period}_{self.std_dev}"
```

### 3. Rolling Window vs Expanding Window

```python
def rolling_walk_forward(data, strategy, window_size=252, test_size=63):
    """Rolling Window Walk-Forward"""
    
    results = []
    start_idx = 0
    
    while start_idx + window_size + test_size <= len(data):
        # Обучающий период (фиксированное окно)
        train_data = data.iloc[start_idx:start_idx + window_size]
        
        # Тестовый период
        test_data = data.iloc[start_idx + window_size:start_idx + window_size + test_size]
        
        # Обучение и тестирование
        strategy.train(train_data)
        backtester = Backtester()
        metrics = backtester.run_backtest(test_data, strategy)
        
        results.append(metrics)
        start_idx += test_size
    
    return results

def expanding_walk_forward(data, strategy, min_train=126, test_size=63):
    """Expanding Window Walk-Forward"""
    
    results = []
    start_idx = 0
    train_size = min_train
    
    while start_idx + train_size + test_size <= len(data):
        # Обучающий период (расширяющееся окно)
        train_data = data.iloc[:start_idx + train_size]
        
        # Тестовый период
        test_data = data.iloc[start_idx + train_size:start_idx + train_size + test_size]
        
        # Обучение и тестирование
        strategy.train(train_data)
        backtester = Backtester()
        metrics = backtester.run_backtest(test_data, strategy)
        
        results.append(metrics)
        start_idx += test_size
        train_size += test_size  # Расширяем окно
    
    return results
```

## Анализ стабильности

### 1. Стабильность производительности

```python
def analyze_stability(results):
    """Анализ стабильности результатов"""
    
    returns = [r['metrics']['total_return'] for r in results]
    
    # Коэффициент вариации
    cv = np.std(returns) / np.abs(np.mean(returns))
    
    # Тренд производительности
    x = np.arange(len(returns))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, returns)
    
    # Стабильность Sharpe Ratio
    sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
    sharpe_stability = 1 - np.std(sharpe_ratios) / np.abs(np.mean(sharpe_ratios))
    
    return {
        'coefficient_of_variation': cv,
        'performance_trend': slope,
        'trend_significance': p_value,
        'sharpe_stability': sharpe_stability,
        'return_consistency': 1 - cv
    }
```

### 2. Анализ деградации

```python
def analyze_degradation(results):
    """Анализ деградации производительности"""
    
    returns = [r['metrics']['total_return'] for r in results]
    
    # Разделение на периоды
    n_periods = len(returns)
    first_half = returns[:n_periods//2]
    second_half = returns[n_periods//2:]
    
    # Сравнение производительности
    first_half_mean = np.mean(first_half)
    second_half_mean = np.mean(second_half)
    
    degradation = (second_half_mean - first_half_mean) / abs(first_half_mean)
    
    # Статистический тест
    t_stat, p_value = stats.ttest_ind(first_half, second_half)
    
    return {
        'first_half_mean': first_half_mean,
        'second_half_mean': second_half_mean,
        'degradation': degradation,
        't_statistic': t_stat,
        'p_value': p_value,
        'significant_degradation': p_value < 0.05 and degradation < -0.1
    }
```

### 3. Анализ адаптивности

```python
def analyze_adaptability(results, market_conditions):
    """Анализ адаптивности к рыночным условиям"""
    
    adaptability_scores = []
    
    for i, result in enumerate(results):
        # Получаем рыночные условия для периода
        period_conditions = market_conditions[i]
        
        # Анализируем производительность в разных условиях
        if period_conditions['volatility'] > 0.3:  # Высокая волатильность
            volatility_performance = result['metrics']['total_return']
        else:
            volatility_performance = result['metrics']['total_return']
        
        if period_conditions['trend'] == 'bull':  # Бычий рынок
            trend_performance = result['metrics']['total_return']
        else:  # Медвежий рынок
            trend_performance = result['metrics']['total_return']
        
        # Оценка адаптивности
        adaptability = (volatility_performance + trend_performance) / 2
        adaptability_scores.append(adaptability)
    
    return {
        'mean_adaptability': np.mean(adaptability_scores),
        'adaptability_std': np.std(adaptability_scores),
        'adaptability_trend': np.polyfit(range(len(adaptability_scores)), adaptability_scores, 1)[0]
    }
```

## Визуализация результатов

### 1. График производительности по периодам

```python
def plot_performance_by_period(results):
    """График производительности по периодам"""
    
    periods = [r['period'] for r in results]
    returns = [r['metrics']['total_return'] for r in results]
    sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Доходность
    ax1.plot(periods, returns, marker='o', linewidth=2)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    ax1.set_title('Доходность по периодам')
    ax1.set_ylabel('Доходность')
    ax1.grid(True, alpha=0.3)
    
    # Sharpe Ratio
    ax2.plot(periods, sharpe_ratios, marker='s', color='green', linewidth=2)
    ax2.axhline(y=1, color='r', linestyle='--', alpha=0.5)
    ax2.set_title('Sharpe Ratio по периодам')
    ax2.set_xlabel('Период')
    ax2.set_ylabel('Sharpe Ratio')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
```

### 2. Распределение результатов

**Теория анализа распределения:**
Анализ распределения результатов помогает понять статистические характеристики производительности стратегии. Это критично для оценки рисков и понимания поведения стратегии.

**Ключевые аспекты распределения:**
- **Нормальность:** Проверка соответствия нормальному распределению
- **Асимметрия:** Оценка перекоса результатов
- **Эксцесс:** Оценка "тяжести хвостов" распределения
- **Выбросы:** Выявление аномальных результатов

```python
def plot_results_distribution(results: List[Dict[str, Any]]) -> None:
    """
    Визуализация распределения результатов Walk-Forward анализа.
    
    Эта функция создает детальную визуализацию распределения
    ключевых метрик производительности стратегии.
    
    Args:
        results: Список результатов Walk-Forward анализа
    """
    
    if not results:
        print("Нет данных для визуализации")
        return
    
    # Извлекаем метрики
    returns = [r['metrics']['total_return'] for r in results]
    sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
    max_drawdowns = [r['metrics']['max_drawdown'] for r in results]
    
    # Создаем фигуру с подграфиками
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Распределение результатов Walk-Forward анализа', fontsize=16, fontweight='bold')
    
    # 1. Распределение доходности
    ax1 = axes[0, 0]
    ax1.hist(returns, bins=20, alpha=0.7, edgecolor='black', color='skyblue')
    ax1.axvline(np.mean(returns), color='red', linestyle='--', linewidth=2, 
                label=f'Среднее: {np.mean(returns):.3f}')
    ax1.axvline(np.median(returns), color='green', linestyle='--', linewidth=2,
                label=f'Медиана: {np.median(returns):.3f}')
    ax1.set_title('Распределение доходности', fontweight='bold')
    ax1.set_xlabel('Доходность')
    ax1.set_ylabel('Частота')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Распределение Sharpe Ratio
    ax2 = axes[0, 1]
    ax2.hist(sharpe_ratios, bins=20, alpha=0.7, edgecolor='black', color='lightgreen')
    ax2.axvline(np.mean(sharpe_ratios), color='red', linestyle='--', linewidth=2,
                label=f'Среднее: {np.mean(sharpe_ratios):.3f}')
    ax2.axvline(1.0, color='orange', linestyle='-', linewidth=2, alpha=0.7,
                label='Sharpe = 1.0')
    ax2.set_title('Распределение Sharpe Ratio', fontweight='bold')
    ax2.set_xlabel('Sharpe Ratio')
    ax2.set_ylabel('Частота')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Распределение просадок
    ax3 = axes[0, 2]
    ax3.hist(max_drawdowns, bins=20, alpha=0.7, edgecolor='black', color='lightcoral')
    ax3.axvline(np.mean(max_drawdowns), color='red', linestyle='--', linewidth=2,
                label=f'Среднее: {np.mean(max_drawdowns):.3f}')
    ax3.axvline(-0.1, color='orange', linestyle='-', linewidth=2, alpha=0.7,
                label='-10% просадка')
    ax3.set_title('Распределение максимальных просадок', fontweight='bold')
    ax3.set_xlabel('Максимальная просадка')
    ax3.set_ylabel('Частота')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Q-Q plot для доходности
    ax4 = axes[1, 0]
    from scipy import stats
    stats.probplot(returns, dist="norm", plot=ax4)
    ax4.set_title('Q-Q Plot доходности', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 5. Box plot для всех метрик
    ax5 = axes[1, 1]
    data_for_box = [returns, sharpe_ratios, [abs(x) for x in max_drawdowns]]  # Абсолютные значения просадок
    box_plot = ax5.boxplot(data_for_box, labels=['Доходность', 'Sharpe Ratio', '|Просадка|'], 
                           patch_artist=True)
    
    # Раскрашиваем box plots
    colors = ['lightblue', 'lightgreen', 'lightcoral']
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set_facecolor(color)
    
    ax5.set_title('Box Plot метрик', fontweight='bold')
    ax5.set_ylabel('Значение')
    ax5.grid(True, alpha=0.3)
    
    # 6. Кумулятивная доходность по периодам
    ax6 = axes[1, 2]
    cumulative_returns = np.cumprod([1 + r for r in returns])
    periods = range(1, len(cumulative_returns) + 1)
    ax6.plot(periods, cumulative_returns, marker='o', linewidth=2, markersize=4)
    ax6.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Начальный капитал')
    ax6.set_title('Кумулятивная доходность', fontweight='bold')
    ax6.set_xlabel('Период')
    ax6.set_ylabel('Кумулятивная доходность')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Выводим статистики
    print("\n📊 СТАТИСТИКИ РАСПРЕДЕЛЕНИЯ:")
    print(f"Доходность:")
    print(f"  Среднее: {np.mean(returns):.4f}")
    print(f"  Медиана: {np.median(returns):.4f}")
    print(f"  Стандартное отклонение: {np.std(returns):.4f}")
    print(f"  Асимметрия: {stats.skew(returns):.4f}")
    print(f"  Эксцесс: {stats.kurtosis(returns):.4f}")
    
    print(f"\nSharpe Ratio:")
    print(f"  Среднее: {np.mean(sharpe_ratios):.4f}")
    print(f"  Медиана: {np.median(sharpe_ratios):.4f}")
    print(f"  Стандартное отклонение: {np.std(sharpe_ratios):.4f}")
    print(f"  Асимметрия: {stats.skew(sharpe_ratios):.4f}")
    print(f"  Эксцесс: {stats.kurtosis(sharpe_ratios):.4f}")

def plot_cumulative_performance(results: List[Dict[str, Any]]) -> None:
    """
    Визуализация кумулятивной производительности стратегии.
    
    Эта функция создает график кумулятивной доходности и других
    ключевых метрик по периодам Walk-Forward анализа.
    
    Args:
        results: Список результатов Walk-Forward анализа
    """
    
    if not results:
        print("Нет данных для визуализации")
        return
    
    # Извлекаем данные
    periods = [r['period'] for r in results]
    returns = [r['metrics']['total_return'] for r in results]
    sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
    max_drawdowns = [r['metrics']['max_drawdown'] for r in results]
    
    # Рассчитываем кумулятивную доходность
    cumulative_returns = np.cumprod([1 + r for r in returns])
    
    # Создаем фигуру
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Кумулятивная производительность стратегии', fontsize=16, fontweight='bold')
    
    # 1. Кумулятивная доходность
    ax1 = axes[0, 0]
    ax1.plot(periods, cumulative_returns, marker='o', linewidth=2, markersize=4, color='blue')
    ax1.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Начальный капитал')
    ax1.fill_between(periods, cumulative_returns, 1.0, alpha=0.3, color='blue')
    ax1.set_title('Кумулятивная доходность', fontweight='bold')
    ax1.set_xlabel('Период')
    ax1.set_ylabel('Кумулятивная доходность')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Доходность по периодам
    ax2 = axes[0, 1]
    colors = ['green' if r > 0 else 'red' for r in returns]
    bars = ax2.bar(periods, returns, color=colors, alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax2.axhline(y=np.mean(returns), color='blue', linestyle='--', alpha=0.7, 
                label=f'Среднее: {np.mean(returns):.3f}')
    ax2.set_title('Доходность по периодам', fontweight='bold')
    ax2.set_xlabel('Период')
    ax2.set_ylabel('Доходность')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Sharpe Ratio по периодам
    ax3 = axes[1, 0]
    ax3.plot(periods, sharpe_ratios, marker='s', linewidth=2, markersize=4, color='green')
    ax3.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Sharpe = 1.0')
    ax3.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='Sharpe = 0.5')
    ax3.fill_between(periods, sharpe_ratios, 0, alpha=0.3, color='green')
    ax3.set_title('Sharpe Ratio по периодам', fontweight='bold')
    ax3.set_xlabel('Период')
    ax3.set_ylabel('Sharpe Ratio')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Просадки по периодам
    ax4 = axes[1, 1]
    ax4.bar(periods, max_drawdowns, color='red', alpha=0.7)
    ax4.axhline(y=-0.1, color='orange', linestyle='--', alpha=0.7, label='-10% просадка')
    ax4.axhline(y=-0.2, color='red', linestyle='--', alpha=0.7, label='-20% просадка')
    ax4.set_title('Максимальные просадки по периодам', fontweight='bold')
    ax4.set_xlabel('Период')
    ax4.set_ylabel('Максимальная просадка')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
```

## Полный рабочий пример

**Теория практического примера:**
Этот раздел демонстрирует полный цикл Walk-Forward анализа от загрузки данных до интерпретации результатов. Пример включает все необходимые компоненты для самостоятельного запуска анализа.

### Создание тестовых данных

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
from scipy import stats

def create_sample_data(symbol: str = "AAPL", period: str = "2y") -> pd.DataFrame:
    """
    Создание тестовых данных для Walk-Forward анализа.
    
    Эта функция загружает реальные финансовые данные и подготавливает их
    для проведения Walk-Forward анализа. Используются данные Yahoo Finance.
    
    Args:
        symbol: Символ акции (по умолчанию AAPL)
        period: Период данных (по умолчанию 2 года)
        
    Returns:
        DataFrame с подготовленными данными
    """
    
    print(f"Загрузка данных для {symbol} за период {period}...")
    
    try:
        # Загружаем данные через yfinance
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        
        if data.empty:
            raise ValueError(f"Не удалось загрузить данные для {symbol}")
        
        # Переименовываем колонки для совместимости
        data.columns = [col.lower() for col in data.columns]
        
        # Удаляем колонки, которые не нужны
        if 'adj close' in data.columns:
            data = data.drop('adj close', axis=1)
        
        # Проверяем наличие необходимых колонок
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            raise ValueError(f"Отсутствуют необходимые колонки: {missing_columns}")
        
        # Удаляем строки с NaN значениями
        data = data.dropna()
        
        print(f"Загружено {len(data)} записей")
        print(f"Период: {data.index[0].strftime('%Y-%m-%d')} - {data.index[-1].strftime('%Y-%m-%d')}")
        print(f"Колонки: {list(data.columns)}")
        
        return data
        
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        print("Создаем синтетические данные...")
        
        # Создаем синтетические данные в случае ошибки
        dates = pd.date_range(start='2022-01-01', end='2024-01-01', freq='D')
        np.random.seed(42)
        
        # Генерируем случайное блуждание с трендом
        returns = np.random.normal(0.0005, 0.02, len(dates))  # Средняя доходность 0.05% в день
        prices = 100 * np.exp(np.cumsum(returns))
        
        # Создаем OHLC данные
        data = pd.DataFrame(index=dates)
        data['close'] = prices
        data['open'] = data['close'].shift(1).fillna(data['close'])
        data['high'] = data[['open', 'close']].max(axis=1) * (1 + np.abs(np.random.normal(0, 0.01, len(dates))))
        data['low'] = data[['open', 'close']].min(axis=1) * (1 - np.abs(np.random.normal(0, 0.01, len(dates))))
        data['volume'] = np.random.randint(1000000, 10000000, len(dates))
        
        print(f"Создано {len(data)} синтетических записей")
        return data

def complete_walk_forward_analysis(data: pd.DataFrame, 
                                 strategy: TradingStrategy,
                                 train_size: int = 252, 
                                 test_size: int = 63, 
                                 step_size: int = 21) -> Dict[str, Any]:
    """
    Полный Walk-Forward анализ с детальной отчетностью.
    
    Эта функция выполняет полный цикл Walk-Forward анализа, включая:
    1. Создание анализатора
    2. Запуск анализа
    3. Анализ стабильности
    4. Анализ деградации
    5. Визуализацию результатов
    6. Генерацию отчета
    
    Args:
        data: Временной ряд финансовых данных
        strategy: Торговая стратегия для тестирования
        train_size: Размер обучающего окна
        test_size: Размер тестового окна
        step_size: Шаг сдвига окна
        
    Returns:
        Словарь с полными результатами анализа
    """
    
    print("="*60)
    print("ПОЛНЫЙ WALK-FORWARD АНАЛИЗ")
    print("="*60)
    print(f"Стратегия: {strategy.get_name()}")
    print(f"Параметры: обучение={train_size} дней, тест={test_size} дней, шаг={step_size} дней")
    print(f"Данные: {len(data)} записей с {data.index[0].strftime('%Y-%m-%d')} по {data.index[-1].strftime('%Y-%m-%d')}")
    
    # 1. Создание анализатора
    print("\n1. Создание анализатора Walk-Forward...")
    analyzer = WalkForwardAnalyzer(train_size=train_size, test_size=test_size, step_size=step_size)
    
    # 2. Запуск анализа
    print("\n2. Запуск Walk-Forward анализа...")
    analysis = analyzer.run_analysis(data, strategy)
    
    # 3. Анализ стабильности
    print("\n3. Анализ стабильности...")
    stability = analyze_stability(analyzer.results)
    
    # 4. Анализ деградации
    print("\n4. Анализ деградации...")
    degradation = analyze_degradation(analyzer.results)
    
    # 5. Визуализация
    print("\n5. Создание визуализаций...")
    try:
        plot_performance_by_period(analyzer.results)
        plot_results_distribution(analyzer.results)
        plot_cumulative_performance(analyzer.results)
    except Exception as e:
        print(f"Ошибка при создании графиков: {e}")
    
    # 6. Детальный отчет
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ WALK-FORWARD АНАЛИЗА")
    print("="*60)
    
    print(f"\n📊 ОСНОВНЫЕ МЕТРИКИ:")
    print(f"   Всего периодов: {analysis['total_periods']}")
    print(f"   Успешных периодов: {analysis['successful_periods']}")
    print(f"   Средняя доходность: {analysis['mean_return']:.2%}")
    print(f"   Стандартное отклонение: {analysis['std_return']:.2%}")
    print(f"   Медианная доходность: {analysis['median_return']:.2%}")
    print(f"   Минимальная доходность: {analysis['min_return']:.2%}")
    print(f"   Максимальная доходность: {analysis['max_return']:.2%}")
    
    print(f"\n📈 РИСК-СКОРРЕКТИРОВАННЫЕ МЕТРИКИ:")
    print(f"   Средний Sharpe Ratio: {analysis['mean_sharpe']:.2f}")
    print(f"   Стандартное отклонение Sharpe: {analysis['std_sharpe']:.2f}")
    print(f"   Минимальный Sharpe: {analysis['min_sharpe']:.2f}")
    print(f"   Максимальный Sharpe: {analysis['max_sharpe']:.2f}")
    
    print(f"\n📉 МЕТРИКИ РИСКА:")
    print(f"   Средняя просадка: {analysis['mean_drawdown']:.2%}")
    print(f"   Худшая просадка: {analysis['worst_drawdown']:.2%}")
    print(f"   Стандартное отклонение просадок: {analysis['std_drawdown']:.2%}")
    
    print(f"\n🎯 КОНСИСТЕНТНОСТЬ:")
    print(f"   Положительных периодов: {analysis['positive_periods']}")
    print(f"   Отрицательных периодов: {analysis['negative_periods']}")
    print(f"   Консистентность: {analysis['consistency']:.2%}")
    print(f"   Коэффициент вариации: {analysis['coefficient_of_variation']:.3f}")
    
    print(f"\n📊 СТАТИСТИЧЕСКИЕ ХАРАКТЕРИСТИКИ:")
    print(f"   Асимметрия: {analysis['skewness']:.3f}")
    print(f"   Эксцесс: {analysis['kurtosis']:.3f}")
    print(f"   Средний процент выигрышных сделок: {analysis['mean_win_rate']:.2%}")
    print(f"   Среднее количество сделок за период: {analysis['mean_trades_per_period']:.1f}")
    print(f"   Общее количество сделок: {analysis['total_trades']}")
    
    print(f"\n🔍 АНАЛИЗ СТАБИЛЬНОСТИ:")
    print(f"   Коэффициент вариации доходности: {stability['coefficient_of_variation']:.3f}")
    print(f"   Тренд производительности: {stability['performance_trend']:.4f}")
    print(f"   Значимость тренда (p-value): {stability['trend_significance']:.4f}")
    print(f"   Стабильность Sharpe Ratio: {stability['sharpe_stability']:.3f}")
    print(f"   Консистентность доходности: {stability['return_consistency']:.3f}")
    
    print(f"\n📉 АНАЛИЗ ДЕГРАДАЦИИ:")
    print(f"   Доходность первой половины: {degradation['first_half_mean']:.2%}")
    print(f"   Доходность второй половины: {degradation['second_half_mean']:.2%}")
    print(f"   Деградация: {degradation['degradation']:.2%}")
    print(f"   t-статистика: {degradation['t_statistic']:.3f}")
    print(f"   p-value: {degradation['p_value']:.4f}")
    print(f"   Значимая деградация: {'Да' if degradation['significant_degradation'] else 'Нет'}")
    
    # Оценка качества стратегии
    print(f"\n🏆 ОЦЕНКА КАЧЕСТВА СТРАТЕГИИ:")
    
    quality_score = 0
    quality_factors = []
    
    # Проверяем доходность
    if analysis['mean_return'] > 0.05:
        quality_score += 2
        quality_factors.append("✅ Высокая доходность")
    elif analysis['mean_return'] > 0:
        quality_score += 1
        quality_factors.append("⚠️ Положительная доходность")
    else:
        quality_factors.append("❌ Отрицательная доходность")
    
    # Проверяем Sharpe Ratio
    if analysis['mean_sharpe'] > 1.0:
        quality_score += 2
        quality_factors.append("✅ Отличный Sharpe Ratio")
    elif analysis['mean_sharpe'] > 0.5:
        quality_score += 1
        quality_factors.append("⚠️ Удовлетворительный Sharpe Ratio")
    else:
        quality_factors.append("❌ Низкий Sharpe Ratio")
    
    # Проверяем консистентность
    if analysis['consistency'] > 0.6:
        quality_score += 2
        quality_factors.append("✅ Высокая консистентность")
    elif analysis['consistency'] > 0.4:
        quality_score += 1
        quality_factors.append("⚠️ Умеренная консистентность")
    else:
        quality_factors.append("❌ Низкая консистентность")
    
    # Проверяем просадки
    if analysis['worst_drawdown'] > -0.1:
        quality_score += 1
        quality_factors.append("✅ Приемлемые просадки")
    else:
        quality_factors.append("❌ Высокие просадки")
    
    # Проверяем деградацию
    if not degradation['significant_degradation']:
        quality_score += 1
        quality_factors.append("✅ Стабильная производительность")
    else:
        quality_factors.append("❌ Значимая деградация")
    
    print(f"   Общий балл: {quality_score}/8")
    for factor in quality_factors:
        print(f"   {factor}")
    
    if quality_score >= 6:
        print("   🎉 ОТЛИЧНАЯ СТРАТЕГИЯ!")
    elif quality_score >= 4:
        print("   👍 ХОРОШАЯ СТРАТЕГИЯ")
    elif quality_score >= 2:
        print("   ⚠️ ТРЕБУЕТ УЛУЧШЕНИЯ")
    else:
        print("   ❌ НЕ РЕКОМЕНДУЕТСЯ")
    
    print("\n" + "="*60)
    
    return {
        'analysis': analysis,
        'stability': stability,
        'degradation': degradation,
        'results': analyzer.results,
        'quality_score': quality_score,
        'quality_factors': quality_factors
    }

# Пример использования
if __name__ == "__main__":
    # Загружаем данные
    data = create_sample_data("AAPL", "2y")
    
    # Создаем стратегии
    strategies = {
        'SMA_20_50': SimpleMovingAverageStrategy(20, 50),
        'SMA_10_30': SimpleMovingAverageStrategy(10, 30),
        'RSI_14': RSIStrategy(14, 30, 70),
        'BB_20': BollingerBandsStrategy(20, 2.0)
    }
    
    # Анализируем каждую стратегию
    for strategy_name, strategy in strategies.items():
        print(f"\n{'='*80}")
        print(f"АНАЛИЗ СТРАТЕГИИ: {strategy_name}")
        print(f"{'='*80}")
        
        try:
            results = complete_walk_forward_analysis(data, strategy)
        except Exception as e:
            print(f"Ошибка при анализе стратегии {strategy_name}: {e}")
    
    # Сравниваем все стратегии
    print(f"\n{'='*80}")
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ ВСЕХ СТРАТЕГИЙ")
    print(f"{'='*80}")
    
    try:
        multi_results, comparison = multi_strategy_walk_forward(data, strategies)
    except Exception as e:
        print(f"Ошибка при сравнительном анализе: {e}")
```

## Следующие шаги

После Walk-Forward анализа переходите к:
- **[08_monte_carlo_simulation.md](08_monte_carlo_simulation.md)** - Монте-Карло симуляция
- **[09_risk_management.md](09_risk_management.md)** - Управление рисками

## Ключевые выводы

1. **Walk-Forward** - самый реалистичный метод тестирования
2. **Стабильность** важнее максимальной доходности
3. **Адаптивность** - ключ к долгосрочному успеху
4. **Деградация** - нормальное явление, нужно учитывать
5. **Визуализация** помогает понять поведение стратегии

---

**Важно:** Хорошая стратегия должна работать стабильно на новых данных, а не только на исторических!
