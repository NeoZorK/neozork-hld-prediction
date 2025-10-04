# 06. 📈 Бэктестинг

**Цель:** Научиться правильно проводить бэктестинг торговых стратегий и избегать типичных ошибок.

## Что такое бэктестинг?

**Теория:** Бэктестинг - это фундаментальный метод оценки торговых стратегий, который позволяет протестировать их на исторических данных перед реальным использованием. Это критически важный этап в разработке торговых систем, так как помогает выявить потенциальные проблемы и оценить производительность.

**Бэктестинг** - это тестирование торговой стратегии на исторических данных для оценки её потенциальной прибыльности.

**Почему бэктестинг критичен для финансовых систем:**
- **Снижение рисков:** Позволяет выявить проблемы до реального использования
- **Оценка производительности:** Дает представление о потенциальной прибыльности
- **Оптимизация:** Помогает найти лучшие параметры стратегии
- **Валидация:** Проверяет работоспособность стратегии на разных условиях

### Зачем нужен бэктестинг?

**Теория:** Бэктестинг служит нескольким критически важным целям в разработке торговых систем. Понимание этих целей помогает правильно проводить бэктестинг и интерпретировать результаты.

- **Проверка стратегии** на исторических данных
  - **Почему важно:** Позволяет убедиться, что стратегия работает на реальных данных
  - **Плюсы:** Объективная оценка производительности, выявление проблем
  - **Минусы:** Исторические данные могут не отражать будущие условия

- **Оценка рисков** и потенциальных потерь
  - **Почему важно:** Помогает понять максимальные потери и волатильность
  - **Плюсы:** Планирование рисков, управление капиталом
  - **Минусы:** Прошлые риски могут не отражать будущие

- **Оптимизация параметров** стратегии
  - **Почему важно:** Позволяет найти лучшие настройки для стратегии
  - **Плюсы:** Улучшение производительности, адаптация к данным
  - **Минусы:** Риск переобучения, необходимость валидации

- **Сравнение** разных подходов
  - **Почему важно:** Позволяет выбрать лучшую стратегию из нескольких вариантов
  - **Плюсы:** Объективное сравнение, выбор оптимального решения
  - **Минусы:** Необходимость корректного сравнения, учет статистической значимости

**Дополнительные цели бэктестинга:**
- **Валидация логики:** Проверка правильности реализации стратегии
- **Тестирование на разных условиях:** Проверка стабильности на различных рыночных условиях
- **Оценка транзакционных издержек:** Учет комиссий, спредов и проскальзывания
- **Планирование капитала:** Определение необходимого размера капитала

## Типичные ошибки бэктестинга

**Теория:** Бэктестинг подвержен множеству ошибок, которые могут привести к ложным результатам и неправильным выводам. Понимание этих ошибок критично для проведения корректного бэктестинга.

### 1. Look-ahead bias (Предвзятость будущего)

**Теория:** Look-ahead bias - это использование информации из будущего при принятии торговых решений в прошлом. Это одна из самых распространенных и опасных ошибок в бэктестинге.

**Почему это проблематично:**
- **Нереалистичность:** В реальной торговле будущая информация недоступна
- **Завышенные результаты:** Приводит к искусственно завышенной производительности
- **Ложная уверенность:** Создает иллюзию успешности стратегии
- **Финансовые потери:** Приводит к потерям при реальном использовании

**Плюсы избегания look-ahead bias:**
- Реалистичные результаты
- Честная оценка производительности
- Снижение рисков
- Повышение доверия к результатам

**Минусы избегания look-ahead bias:**
- Более сложная реализация
- Возможное снижение производительности
- Необходимость тщательной проверки
```python
# ❌ НЕПРАВИЛЬНО - используем будущие данные
def bad_backtest(df):
    for i in range(len(df)):
        # Используем данные из будущего!
        if df.iloc[i]['Close'] > df.iloc[i+1]['Close']:  # ОШИБКА!
            signal = 'BUY'
        else:
            signal = 'SELL'
    return signals

# ✅ ПРАВИЛЬНО - используем только прошлые данные
def good_backtest(df):
    signals = []
    for i in range(len(df)):
        # Используем только данные до текущего момента
        if i > 0 and df.iloc[i]['Close'] > df.iloc[i-1]['Close']:
            signal = 'BUY'
        else:
            signal = 'SELL'
        signals.append(signal)
    return signals
```

### 2. Survivorship bias (Выживания)

**Теория:** Survivorship bias - это ошибка, возникающая при тестировании только на "выживших" активах, игнорируя те, которые прекратили существование. Это приводит к завышенной оценке производительности стратегии.

**Почему это проблематично:**
- **Завышенные результаты:** Игнорирование неудачных активов искажает результаты
- **Нереалистичность:** В реальной торговле приходится работать со всеми активами
- **Ложная уверенность:** Создает иллюзию успешности стратегии
- **Финансовые потери:** Приводит к потерям при реальном использовании

**Плюсы учета survivorship bias:**
- Реалистичные результаты
- Честная оценка производительности
- Снижение рисков
- Повышение доверия к результатам

**Минусы учета survivorship bias:**
- Более сложная реализация
- Необходимость доступа к полным данным
- Возможное снижение производительности
```python
# ❌ НЕПРАВИЛЬНО - тестируем только на "выживших" активах
def bad_survivorship_test():
    # Тестируем только на активах, которые существуют сейчас
    symbols = ['AAPL', 'GOOGL', 'MSFT']  # Все успешные компании
    return backtest_symbols(symbols)

# ✅ ПРАВИЛЬНО - включаем все активы, включая "мертвые"
def good_survivorship_test():
    # Включаем все активы, которые торговались в период
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'ENRON', 'LEHMAN']  # Включая банкротов
    return backtest_symbols(symbols)
```

### 3. Overfitting (Переобучение)

**Теория:** Overfitting - это ошибка, возникающая при чрезмерной оптимизации параметров стратегии на исторических данных. Это приводит к стратегии, которая работает только на обучающих данных, но не на новых данных.

**Почему это проблематично:**
- **Нереалистичность:** Стратегия может не работать на новых данных
- **Завышенные результаты:** Производительность на исторических данных не отражает реальную производительность
- **Ложная уверенность:** Создает иллюзию успешности стратегии
- **Финансовые потери:** Приводит к потерям при реальном использовании

**Плюсы избегания overfitting:**
- Реалистичные результаты
- Честная оценка производительности
- Снижение рисков
- Повышение доверия к результатам

**Минусы избегания overfitting:**
- Более сложная реализация
- Необходимость валидации
- Возможное снижение производительности
- Необходимость разделения данных
```python
# ❌ НЕПРАВИЛЬНО - оптимизируем на всех данных
def bad_optimization(df):
    # Оптимизируем параметры на всех данных
    best_params = optimize_parameters(df)  # Переобучение!
    return backtest_with_params(df, best_params)

# ✅ ПРАВИЛЬНО - разделяем на train/test
def good_optimization(df):
    # Разделяем данные
    train_data = df[:int(len(df)*0.7)]
    test_data = df[int(len(df)*0.7):]
    
    # Оптимизируем на train
    best_params = optimize_parameters(train_data)
    
    # Тестируем на test
    return backtest_with_params(test_data, best_params)
```

## Правильный бэктестинг

**Теория:** Правильный бэктестинг требует тщательной структуры и учета всех аспектов торговли. Основные принципы включают:

1. **Четкое разделение логики** - отделение стратегии от исполнения
2. **Учет транзакционных издержек** - комиссии, спреды, проскальзывание
3. **Правильное управление позициями** - открытие, закрытие, переворот
4. **Точный расчет метрик** - доходность, риск, просадки
5. **Валидация результатов** - проверка корректности расчетов

### 1. Структура бэктестинга

**Теория:** Класс Backtester является основой для проведения бэктестинга. Он инкапсулирует всю логику торговли, управление капиталом и расчет метрик. Правильная структура позволяет:

- **Модульность:** Легко тестировать разные стратегии
- **Расширяемость:** Добавлять новые функции без изменения основной логики
- **Отладка:** Легко находить и исправлять ошибки
- **Валидация:** Проверять корректность расчетов

**Ключевые компоненты:**
- **Управление капиталом:** Отслеживание доступного капитала и позиций
- **Исполнение сделок:** Логика открытия и закрытия позиций
- **Расчет метрик:** Оценка производительности стратегии
- **Ведение истории:** Запись всех торговых операций

```python
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    """Класс для хранения информации о сделке"""
    timestamp: datetime
    price: float
    quantity: float
    direction: str  # 'LONG' or 'SHORT'
    profit: float = 0.0
    commission: float = 0.0

class Backtester:
    """
    Класс для проведения бэктестинга торговых стратегий
    
    Этот класс реализует полный цикл бэктестинга:
    1. Инициализация с начальным капиталом
    2. Получение сигналов от стратегии
    3. Исполнение торговых операций
    4. Расчет метрик производительности
    5. Ведение истории сделок
    """
    
    def __init__(self, initial_capital: float = 10000, commission: float = 0.001):
        """
        Инициализация бэктестера
        
        Args:
            initial_capital: Начальный капитал для торговли
            commission: Комиссия за сделку (в долях от суммы)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.capital = initial_capital  # Текущий доступный капитал
        self.position = 0  # Текущая позиция (количество единиц актива)
        self.position_value = 0  # Стоимость текущей позиции
        self.trades: List[Trade] = []  # История сделок
        self.equity_curve: List[float] = []  # Кривая капитала
        self.daily_returns: List[float] = []  # Ежедневные доходности
        
    def run_backtest(self, data: pd.DataFrame, strategy) -> Dict[str, Any]:
        """
        Запуск полного цикла бэктестинга
        
        Args:
            data: Исторические данные (OHLCV)
            strategy: Объект стратегии с методом get_signal()
            
        Returns:
            Словарь с метриками производительности
        """
        print(f"Запуск бэктестинга на {len(data)} периодах...")
        
        # Сброс состояния
        self.capital = self.initial_capital
        self.position = 0
        self.position_value = 0
        self.trades = []
        self.equity_curve = []
        self.daily_returns = []
        
        for i, (timestamp, row) in enumerate(data.iterrows()):
            # Получаем сигнал от стратегии (только на исторических данных)
            signal = strategy.get_signal(data.iloc[:i+1])
            
            # Выполняем торговую операцию
            self.execute_trade(row, signal, timestamp)
            
            # Рассчитываем текущую стоимость портфеля
            current_equity = self.calculate_current_equity(row['Close'])
            self.equity_curve.append(current_equity)
            
            # Рассчитываем ежедневную доходность
            if i > 0:
                daily_return = (current_equity - self.equity_curve[i-1]) / self.equity_curve[i-1]
                self.daily_returns.append(daily_return)
        
        print(f"Бэктестинг завершен. Выполнено {len(self.trades)} сделок")
        return self.calculate_metrics()
    
    def execute_trade(self, row: pd.Series, signal: str, timestamp: datetime) -> None:
        """
        Выполнение торговой операции на основе сигнала
        
        Args:
            row: Текущая строка данных (OHLCV)
            signal: Торговый сигнал ('BUY', 'SELL', 'HOLD')
            timestamp: Временная метка сделки
        """
        if signal == 'BUY' and self.position <= 0:
            # Покупка: закрываем короткую позицию (если есть) и открываем длинную
            if self.position < 0:
                self.close_position(row['Close'], timestamp, 'SHORT')
            
            self.open_position(row['Close'], 'LONG', timestamp)
            
        elif signal == 'SELL' and self.position >= 0:
            # Продажа: закрываем длинную позицию (если есть) и открываем короткую
            if self.position > 0:
                self.close_position(row['Close'], timestamp, 'LONG')
            
            self.open_position(row['Close'], 'SHORT', timestamp)
            
        elif signal == 'HOLD':
            # Удерживаем текущую позицию
            pass
    
    def open_position(self, price: float, direction: str, timestamp: datetime) -> None:
        """
        Открытие новой позиции
        
        Args:
            price: Цена открытия позиции
            direction: Направление позиции ('LONG' или 'SHORT')
            timestamp: Временная метка
        """
        if direction == 'LONG':
            # Покупка: используем весь доступный капитал
            self.position = self.capital / price
            self.position_value = self.position * price
            self.capital = 0
            
            # Записываем сделку
            trade = Trade(
                timestamp=timestamp,
                price=price,
                quantity=self.position,
                direction='LONG',
                commission=self.position_value * self.commission
            )
            self.trades.append(trade)
            
        elif direction == 'SHORT':
            # Продажа: открываем короткую позицию
            self.position = -self.capital / price
            self.position_value = abs(self.position) * price
            self.capital = 0
            
            # Записываем сделку
            trade = Trade(
                timestamp=timestamp,
                price=price,
                quantity=abs(self.position),
                direction='SHORT',
                commission=self.position_value * self.commission
            )
            self.trades.append(trade)
    
    def close_position(self, price: float, timestamp: datetime, direction: str) -> None:
        """
        Закрытие текущей позиции
        
        Args:
            price: Цена закрытия позиции
            timestamp: Временная метка
            direction: Направление закрываемой позиции
        """
        if direction == 'LONG' and self.position > 0:
            # Закрываем длинную позицию
            self.capital = self.position * price * (1 - self.commission)
            profit = self.capital - self.position_value
            
            # Записываем сделку закрытия
            trade = Trade(
                timestamp=timestamp,
                price=price,
                quantity=self.position,
                direction='CLOSE_LONG',
                profit=profit,
                commission=self.position * price * self.commission
            )
            self.trades.append(trade)
            
        elif direction == 'SHORT' and self.position < 0:
            # Закрываем короткую позицию
            self.capital = -self.position * price * (1 - self.commission)
            profit = self.capital - self.position_value
            
            # Записываем сделку закрытия
            trade = Trade(
                timestamp=timestamp,
                price=price,
                quantity=abs(self.position),
                direction='CLOSE_SHORT',
                profit=profit,
                commission=abs(self.position) * price * self.commission
            )
            self.trades.append(trade)
        
        # Сбрасываем позицию
        self.position = 0
        self.position_value = 0
    
    def calculate_current_equity(self, current_price: float) -> float:
        """
        Расчет текущей стоимости портфеля
        
        Args:
            current_price: Текущая цена актива
            
        Returns:
            Текущая стоимость портфеля
        """
        if self.position > 0:  # Длинная позиция
            return self.position * current_price
        elif self.position < 0:  # Короткая позиция
            return self.capital + (-self.position * current_price)
        else:  # Нет позиции
            return self.capital
```

### 2. Расчет метрик

**Теория:** Расчет метрик производительности - это критически важный этап бэктестинга. Правильные метрики позволяют:

- **Оценить прибыльность** стратегии в абсолютном и относительном выражении
- **Измерить риск** через волатильность и просадки
- **Сравнить стратегии** между собой объективно
- **Принять решение** о внедрении стратегии в реальную торговлю

**Ключевые метрики:**
- **Доходность:** Общая, годовая, средняя
- **Риск:** Волатильность, максимальная просадка, VaR
- **Эффективность:** Sharpe ratio, Sortino ratio, Calmar ratio
- **Стабильность:** Win rate, profit factor, recovery factor

```python
def calculate_metrics(self) -> Dict[str, Any]:
    """
    Расчет комплексных метрик производительности стратегии
    
    Этот метод рассчитывает все основные метрики для оценки
    производительности торговой стратегии:
    
    1. Метрики доходности (return metrics)
    2. Метрики риска (risk metrics) 
    3. Метрики эффективности (efficiency metrics)
    4. Метрики стабильности (stability metrics)
    
    Returns:
        Словарь с рассчитанными метриками
    """
    if not self.equity_curve:
        return self._empty_metrics()
    
    # === МЕТРИКИ ДОХОДНОСТИ ===
    
    # Общая доходность (Total Return)
    # Показывает общий прирост капитала за весь период
    total_return = (self.equity_curve[-1] - self.initial_capital) / self.initial_capital
    
    # Годовая доходность (Annualized Return)
    # Приводит доходность к годовому эквиваленту для сравнения
    years = len(self.equity_curve) / 252  # 252 торговых дня в году
    if years > 0:
        annual_return = (1 + total_return) ** (1/years) - 1
    else:
        annual_return = 0
    
    # Средняя ежедневная доходность
    if self.daily_returns:
        avg_daily_return = np.mean(self.daily_returns)
    else:
        avg_daily_return = 0
    
    # === МЕТРИКИ РИСКА ===
    
    # Волатильность (Volatility)
    # Стандартное отклонение доходностей, приведенное к годовому эквиваленту
    if self.daily_returns:
        volatility = np.std(self.daily_returns) * np.sqrt(252)
    else:
        volatility = 0
    
    # Максимальная просадка (Maximum Drawdown)
    # Максимальная потеря от пика до минимума
    equity_series = pd.Series(self.equity_curve)
    running_max = equity_series.expanding().max()
    drawdown = (equity_series - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Средняя просадка
    avg_drawdown = drawdown[drawdown < 0].mean() if (drawdown < 0).any() else 0
    
    # Длительность максимальной просадки (в днях)
    max_dd_duration = self._calculate_max_drawdown_duration(drawdown)
    
    # Value at Risk (VaR) - 95% доверительный интервал
    if self.daily_returns:
        var_95 = np.percentile(self.daily_returns, 5)
    else:
        var_95 = 0
    
    # === МЕТРИКИ ЭФФЕКТИВНОСТИ ===
    
    # Sharpe Ratio
    # Отношение избыточной доходности к волатильности
    risk_free_rate = 0.02  # 2% безрисковая ставка
    if volatility > 0:
        sharpe_ratio = (annual_return - risk_free_rate) / volatility
    else:
        sharpe_ratio = 0
    
    # Sortino Ratio
    # Аналогично Sharpe, но учитывает только негативную волатильность
    if self.daily_returns:
        negative_returns = [r for r in self.daily_returns if r < 0]
        if negative_returns:
            downside_volatility = np.std(negative_returns) * np.sqrt(252)
            if downside_volatility > 0:
                sortino_ratio = (annual_return - risk_free_rate) / downside_volatility
            else:
                sortino_ratio = 0
        else:
            sortino_ratio = float('inf') if annual_return > risk_free_rate else 0
    else:
        sortino_ratio = 0
    
    # Calmar Ratio
    # Отношение годовой доходности к максимальной просадке
    if abs(max_drawdown) > 0:
        calmar_ratio = annual_return / abs(max_drawdown)
    else:
        calmar_ratio = float('inf') if annual_return > 0 else 0
    
    # === МЕТРИКИ СТАБИЛЬНОСТИ ===
    
    # Win Rate - процент прибыльных сделок
    if self.trades:
        profitable_trades = [t for t in self.trades if t.profit > 0]
        win_rate = len(profitable_trades) / len(self.trades)
        
        # Profit Factor - отношение прибыли к убыткам
        total_profit = sum(t.profit for t in self.trades if t.profit > 0)
        total_loss = abs(sum(t.profit for t in self.trades if t.profit < 0))
        profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')
        
        # Средняя прибыль и убыток
        avg_win = total_profit / len(profitable_trades) if profitable_trades else 0
        losing_trades = [t for t in self.trades if t.profit < 0]
        avg_loss = abs(sum(t.profit for t in losing_trades)) / len(losing_trades) if losing_trades else 0
        
        # Recovery Factor - отношение общей прибыли к максимальной просадке
        recovery_factor = total_profit / abs(max_drawdown) if abs(max_drawdown) > 0 else float('inf')
    else:
        win_rate = 0
        profit_factor = 0
        avg_win = 0
        avg_loss = 0
        recovery_factor = 0
    
    # === ДОПОЛНИТЕЛЬНЫЕ МЕТРИКИ ===
    
    # Коэффициент вариации (Coefficient of Variation)
    # Отношение волатильности к средней доходности
    if avg_daily_return != 0:
        coefficient_of_variation = volatility / (avg_daily_return * 252)
    else:
        coefficient_of_variation = float('inf')
    
    # Индекс стабильности (Stability Index)
    # Показывает стабильность доходности
    if self.daily_returns:
        stability_index = 1 - (np.std(self.daily_returns) / abs(avg_daily_return)) if avg_daily_return != 0 else 0
    else:
        stability_index = 0
    
    return {
        # Метрики доходности
        'total_return': total_return,
        'annual_return': annual_return,
        'avg_daily_return': avg_daily_return,
        
        # Метрики риска
        'volatility': volatility,
        'max_drawdown': max_drawdown,
        'avg_drawdown': avg_drawdown,
        'max_dd_duration': max_dd_duration,
        'var_95': var_95,
        
        # Метрики эффективности
        'sharpe_ratio': sharpe_ratio,
        'sortino_ratio': sortino_ratio,
        'calmar_ratio': calmar_ratio,
        
        # Метрики стабильности
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'recovery_factor': recovery_factor,
        
        # Дополнительные метрики
        'coefficient_of_variation': coefficient_of_variation,
        'stability_index': stability_index,
        'total_trades': len(self.trades),
        'final_capital': self.equity_curve[-1] if self.equity_curve else self.initial_capital
    }

def _calculate_max_drawdown_duration(self, drawdown: pd.Series) -> int:
    """
    Расчет длительности максимальной просадки в днях
    
    Args:
        drawdown: Серия просадок
        
    Returns:
        Максимальная длительность просадки в днях
    """
    if drawdown.empty:
        return 0
    
    # Находим периоды просадки
    in_drawdown = drawdown < 0
    drawdown_periods = []
    current_period = 0
    
    for is_dd in in_drawdown:
        if is_dd:
            current_period += 1
        else:
            if current_period > 0:
                drawdown_periods.append(current_period)
            current_period = 0
    
    # Добавляем последний период, если он есть
    if current_period > 0:
        drawdown_periods.append(current_period)
    
    return max(drawdown_periods) if drawdown_periods else 0

def _empty_metrics(self) -> Dict[str, Any]:
    """Возвращает пустые метрики при отсутствии данных"""
    return {
        'total_return': 0, 'annual_return': 0, 'avg_daily_return': 0,
        'volatility': 0, 'max_drawdown': 0, 'avg_drawdown': 0,
        'max_dd_duration': 0, 'var_95': 0, 'sharpe_ratio': 0,
        'sortino_ratio': 0, 'calmar_ratio': 0, 'win_rate': 0,
        'profit_factor': 0, 'avg_win': 0, 'avg_loss': 0,
        'recovery_factor': 0, 'coefficient_of_variation': 0,
        'stability_index': 0, 'total_trades': 0, 'final_capital': self.initial_capital
    }
```

## Продвинутые техники бэктестинга

**Теория:** Продвинутые техники бэктестинга позволяют получить более надежные и реалистичные оценки производительности стратегий. Эти методы помогают:

- **Избежать переобучения** через правильное разделение данных
- **Оценить стабильность** стратегии на разных периодах
- **Учесть неопределенность** через статистические методы
- **Проверить робастность** стратегии к изменениям рынка

### 1. Walk-Forward Analysis

**Теория:** Walk-Forward Analysis (WFA) - это метод тестирования стратегий, который имитирует реальную торговлю. Основная идея:

1. **Обучение на исторических данных** - стратегия обучается на прошлых данных
2. **Тестирование на следующих данных** - обученная стратегия тестируется на следующих данных
3. **Скользящее окно** - процесс повторяется с движущимся окном данных

**Преимущества WFA:**
- **Реалистичность:** Имитирует реальную торговлю
- **Избежание переобучения:** Стратегия не видит будущие данные
- **Оценка стабильности:** Показывает, как стратегия работает на разных периодах
- **Адаптивность:** Стратегия может адаптироваться к изменениям рынка

**Ключевые параметры:**
- **Train Period:** Длина обучающего периода (обычно 1-2 года)
- **Test Period:** Длина тестового периода (обычно 1-3 месяца)
- **Step Size:** Шаг сдвига окна (обычно равен test_period)

```python
def walk_forward_analysis(data: pd.DataFrame, strategy, 
                         train_period: int = 252, 
                         test_period: int = 63,
                         step_size: int = None) -> List[Dict[str, Any]]:
    """
    Проведение Walk-Forward анализа стратегии
    
    Walk-Forward анализ имитирует реальную торговлю:
    1. Обучаем стратегию на исторических данных
    2. Тестируем на следующих данных
    3. Сдвигаем окно и повторяем процесс
    
    Args:
        data: Исторические данные (OHLCV)
        strategy: Объект стратегии с методами train() и get_signal()
        train_period: Длина обучающего периода в днях (по умолчанию 252)
        test_period: Длина тестового периода в днях (по умолчанию 63)
        step_size: Шаг сдвига окна в днях (по умолчанию равен test_period)
        
    Returns:
        Список результатов для каждого тестового периода
    """
    if step_size is None:
        step_size = test_period
    
    results = []
    total_periods = len(data) - train_period - test_period
    
    print(f"Запуск Walk-Forward анализа:")
    print(f"  - Обучающий период: {train_period} дней")
    print(f"  - Тестовый период: {test_period} дней")
    print(f"  - Шаг сдвига: {step_size} дней")
    print(f"  - Всего периодов: {total_periods // step_size + 1}")
    
    for start_idx in range(0, total_periods + 1, step_size):
        # Определяем границы периодов
        train_start = start_idx
        train_end = start_idx + train_period
        test_start = train_end
        test_end = test_start + test_period
        
        # Проверяем, что у нас достаточно данных
        if test_end > len(data):
            break
        
        # Извлекаем данные для обучения и тестирования
        train_data = data.iloc[train_start:train_end].copy()
        test_data = data.iloc[test_start:test_end].copy()
        
        print(f"Период {len(results) + 1}: "
              f"Обучение {train_data.index[0].date()} - {train_data.index[-1].date()}, "
              f"Тест {test_data.index[0].date()} - {test_data.index[-1].date()}")
        
        try:
            # Обучение стратегии на исторических данных
            strategy.train(train_data)
            
            # Тестирование на следующих данных
            backtester = Backtester()
            metrics = backtester.run_backtest(test_data, strategy)
            
            # Сохраняем результаты
            results.append({
                'period': len(results) + 1,
                'train_start': train_data.index[0],
                'train_end': train_data.index[-1],
                'test_start': test_data.index[0],
                'test_end': test_data.index[-1],
                'train_days': len(train_data),
                'test_days': len(test_data),
                'metrics': metrics,
                'trades': len(backtester.trades),
                'equity_curve': backtester.equity_curve.copy()
            })
            
        except Exception as e:
            print(f"Ошибка в периоде {len(results) + 1}: {e}")
            continue
    
    print(f"Walk-Forward анализ завершен. Обработано {len(results)} периодов")
    return results

def analyze_walk_forward_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Анализ результатов Walk-Forward анализа
    
    Args:
        results: Результаты Walk-Forward анализа
        
    Returns:
        Словарь с агрегированными метриками
    """
    if not results:
        return {}
    
    # Извлекаем метрики из всех периодов
    all_returns = [r['metrics']['total_return'] for r in results]
    all_sharpe = [r['metrics']['sharpe_ratio'] for r in results]
    all_max_dd = [r['metrics']['max_drawdown'] for r in results]
    all_win_rates = [r['metrics']['win_rate'] for r in results]
    
    # Рассчитываем статистики
    analysis = {
        'total_periods': len(results),
        'avg_return': np.mean(all_returns),
        'std_return': np.std(all_returns),
        'min_return': np.min(all_returns),
        'max_return': np.max(all_returns),
        'positive_periods': sum(1 for r in all_returns if r > 0),
        'positive_periods_pct': sum(1 for r in all_returns if r > 0) / len(all_returns),
        
        'avg_sharpe': np.mean(all_sharpe),
        'std_sharpe': np.std(all_sharpe),
        'min_sharpe': np.min(all_sharpe),
        'max_sharpe': np.max(all_sharpe),
        
        'avg_max_dd': np.mean(all_max_dd),
        'worst_dd': np.min(all_max_dd),
        'avg_win_rate': np.mean(all_win_rates),
        
        'consistency_score': 1 - np.std(all_returns) / (np.mean(all_returns) + 1e-8),
        'stability_score': sum(1 for r in all_returns if r > 0) / len(all_returns)
    }
    
    return analysis
```

### 2. Monte Carlo Simulation

**Теория:** Monte Carlo симуляция - это статистический метод, который использует случайную выборку для оценки неопределенности в результатах бэктестинга. Основная идея:

1. **Случайная перестановка данных** - создаем множество случайных последовательностей торговых дней
2. **Множественные бэктесты** - тестируем стратегию на каждой перестановке
3. **Статистический анализ** - анализируем распределение результатов

**Преимущества Monte Carlo:**
- **Оценка неопределенности:** Показывает диапазон возможных результатов
- **Проверка робастности:** Тестирует стратегию на разных последовательностях
- **Статистическая значимость:** Позволяет оценить надежность результатов
- **Управление рисками:** Помогает понять худшие и лучшие сценарии

**Применение:**
- **Валидация стратегии:** Проверка, что результаты не случайны
- **Оценка рисков:** Понимание потенциальных потерь
- **Планирование капитала:** Определение необходимого размера капитала
- **Сравнение стратегий:** Статистическое сравнение разных подходов

```python
def monte_carlo_simulation(data: pd.DataFrame, strategy, 
                          n_simulations: int = 1000,
                          block_size: int = 1) -> List[Dict[str, Any]]:
    """
    Проведение Monte Carlo симуляции для оценки неопределенности результатов
    
    Monte Carlo симуляция создает множество случайных перестановок
    исторических данных и тестирует стратегию на каждой из них.
    Это позволяет оценить неопределенность и робастность результатов.
    
    Args:
        data: Исторические данные (OHLCV)
        strategy: Объект стратегии с методом get_signal()
        n_simulations: Количество симуляций (по умолчанию 1000)
        block_size: Размер блоков для перестановки (по умолчанию 1)
        
    Returns:
        Список результатов для каждой симуляции
    """
    print(f"Запуск Monte Carlo симуляции:")
    print(f"  - Количество симуляций: {n_simulations}")
    print(f"  - Размер блоков: {block_size}")
    print(f"  - Размер данных: {len(data)} периодов")
    
    results = []
    
    for i in range(n_simulations):
        if (i + 1) % 100 == 0:
            print(f"  Выполнено {i + 1}/{n_simulations} симуляций")
        
        try:
            if block_size == 1:
                # Простая перестановка (каждый день независимо)
                shuffled_data = data.sample(frac=1).reset_index(drop=True)
            else:
                # Блочная перестановка (сохраняем структуру данных)
                shuffled_data = _block_shuffle_data(data, block_size)
            
            # Бэктестинг на переставленных данных
            backtester = Backtester()
            metrics = backtester.run_backtest(shuffled_data, strategy)
            
            results.append({
                'simulation': i + 1,
                'metrics': metrics,
                'trades': len(backtester.trades),
                'final_capital': backtester.equity_curve[-1] if backtester.equity_curve else backtester.initial_capital
            })
            
        except Exception as e:
            print(f"Ошибка в симуляции {i + 1}: {e}")
            continue
    
    print(f"Monte Carlo симуляция завершена. Успешно выполнено {len(results)} симуляций")
    return results

def _block_shuffle_data(data: pd.DataFrame, block_size: int) -> pd.DataFrame:
    """
    Блочная перестановка данных для сохранения структуры
    
    Args:
        data: Исходные данные
        block_size: Размер блоков
        
    Returns:
        Переставленные данные с сохранением структуры
    """
    n_blocks = len(data) // block_size
    blocks = []
    
    for i in range(n_blocks):
        start_idx = i * block_size
        end_idx = start_idx + block_size
        block = data.iloc[start_idx:end_idx].copy()
        blocks.append(block)
    
    # Случайно переставляем блоки
    np.random.shuffle(blocks)
    
    # Объединяем блоки
    shuffled_data = pd.concat(blocks, ignore_index=True)
    
    # Добавляем оставшиеся данные, если есть
    remaining = len(data) % block_size
    if remaining > 0:
        remaining_data = data.iloc[-remaining:].copy()
        shuffled_data = pd.concat([shuffled_data, remaining_data], ignore_index=True)
    
    return shuffled_data

def analyze_monte_carlo_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Комплексный анализ результатов Monte Carlo симуляции
    
    Анализирует распределение результатов и предоставляет статистики
    для оценки неопределенности и рисков стратегии.
    
    Args:
        results: Результаты Monte Carlo симуляции
        
    Returns:
        Словарь с анализом результатов
    """
    if not results:
        return {}
    
    # Извлекаем основные метрики
    returns = [r['metrics']['total_return'] for r in results]
    sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
    max_drawdowns = [r['metrics']['max_drawdown'] for r in results]
    win_rates = [r['metrics']['win_rate'] for r in results]
    final_capitals = [r['final_capital'] for r in results]
    
    # Базовые статистики
    analysis = {
        'n_simulations': len(results),
        
        # Статистики доходности
        'return_stats': {
            'mean': np.mean(returns),
            'std': np.std(returns),
            'min': np.min(returns),
            'max': np.max(returns),
            'median': np.median(returns),
            'skewness': _calculate_skewness(returns),
            'kurtosis': _calculate_kurtosis(returns)
        },
        
        # Перцентили доходности
        'return_percentiles': {
            'p1': np.percentile(returns, 1),
            'p5': np.percentile(returns, 5),
            'p10': np.percentile(returns, 10),
            'p25': np.percentile(returns, 25),
            'p50': np.percentile(returns, 50),
            'p75': np.percentile(returns, 75),
            'p90': np.percentile(returns, 90),
            'p95': np.percentile(returns, 95),
            'p99': np.percentile(returns, 99)
        },
        
        # Вероятности
        'probabilities': {
            'positive_return': np.mean([r > 0 for r in returns]),
            'negative_return': np.mean([r < 0 for r in returns]),
            'return_above_10pct': np.mean([r > 0.1 for r in returns]),
            'return_above_20pct': np.mean([r > 0.2 for r in returns]),
            'return_below_minus10pct': np.mean([r < -0.1 for r in returns]),
            'return_below_minus20pct': np.mean([r < -0.2 for r in returns])
        },
        
        # Статистики риска
        'risk_stats': {
            'avg_max_drawdown': np.mean(max_drawdowns),
            'worst_drawdown': np.min(max_drawdowns),
            'drawdown_std': np.std(max_drawdowns),
            'avg_sharpe': np.mean(sharpe_ratios),
            'sharpe_std': np.std(sharpe_ratios),
            'min_sharpe': np.min(sharpe_ratios),
            'max_sharpe': np.max(sharpe_ratios)
        },
        
        # VaR и CVaR
        'var_cvar': {
            'var_95': np.percentile(returns, 5),
            'var_99': np.percentile(returns, 1),
            'cvar_95': np.mean([r for r in returns if r <= np.percentile(returns, 5)]),
            'cvar_99': np.mean([r for r in returns if r <= np.percentile(returns, 1)])
        },
        
        # Дополнительные метрики
        'additional': {
            'avg_win_rate': np.mean(win_rates),
            'win_rate_std': np.std(win_rates),
            'avg_trades': np.mean([r['trades'] for r in results]),
            'consistency_score': 1 - np.std(returns) / (np.mean(returns) + 1e-8),
            'stability_score': np.mean([r > 0 for r in returns])
        }
    }
    
    return analysis

def _calculate_skewness(data: List[float]) -> float:
    """Расчет асимметрии распределения"""
    if len(data) < 3:
        return 0
    mean = np.mean(data)
    std = np.std(data)
    if std == 0:
        return 0
    return np.mean([(x - mean) ** 3 for x in data]) / (std ** 3)

def _calculate_kurtosis(data: List[float]) -> float:
    """Расчет эксцесса распределения"""
    if len(data) < 4:
        return 0
    mean = np.mean(data)
    std = np.std(data)
    if std == 0:
        return 0
    return np.mean([(x - mean) ** 4 for x in data]) / (std ** 4) - 3
```

### 3. Bootstrap Analysis

**Теория:** Bootstrap анализ - это статистический метод, который использует повторную выборку с возвращением для оценки неопределенности в результатах. В отличие от Monte Carlo, bootstrap сохраняет временную структуру данных.

**Основные принципы:**
1. **Блочная выборка** - создаем выборки из блоков данных
2. **Сохранение структуры** - поддерживаем временные зависимости
3. **Повторная выборка** - создаем множество вариантов данных
4. **Статистический анализ** - оцениваем неопределенность результатов

**Преимущества Bootstrap:**
- **Сохранение структуры:** Учитывает временные зависимости в данных
- **Непараметричность:** Не требует предположений о распределении
- **Гибкость:** Можно адаптировать под разные типы данных
- **Надежность:** Дает консервативные оценки неопределенности

**Применение:**
- **Оценка доверительных интервалов** для метрик
- **Тестирование гипотез** о производительности стратегии
- **Сравнение стратегий** с учетом неопределенности
- **Планирование размера выборки** для тестирования

```python
def bootstrap_analysis(data: pd.DataFrame, strategy, 
                      n_bootstrap: int = 1000, 
                      block_size: int = 20) -> List[Dict[str, Any]]:
    """
    Проведение Bootstrap анализа для оценки неопределенности результатов
    
    Bootstrap анализ создает множество выборок из исходных данных
    с сохранением временной структуры. Это позволяет оценить
    неопределенность в результатах бэктестинга.
    
    Args:
        data: Исторические данные (OHLCV)
        strategy: Объект стратегии с методом get_signal()
        n_bootstrap: Количество bootstrap выборок (по умолчанию 1000)
        block_size: Размер блоков для выборки (по умолчанию 20)
        
    Returns:
        Список результатов для каждой bootstrap выборки
    """
    print(f"Запуск Bootstrap анализа:")
    print(f"  - Количество выборок: {n_bootstrap}")
    print(f"  - Размер блоков: {block_size}")
    print(f"  - Размер данных: {len(data)} периодов")
    
    results = []
    n_blocks_needed = len(data) // block_size
    
    for i in range(n_bootstrap):
        if (i + 1) % 100 == 0:
            print(f"  Выполнено {i + 1}/{n_bootstrap} выборок")
        
        try:
            # Создание bootstrap выборки с блоками
            bootstrap_data = _create_bootstrap_sample(data, block_size, n_blocks_needed)
            
            # Бэктестинг на bootstrap выборке
            backtester = Backtester()
            metrics = backtester.run_backtest(bootstrap_data, strategy)
            
            results.append({
                'bootstrap': i + 1,
                'metrics': metrics,
                'trades': len(backtester.trades),
                'final_capital': backtester.equity_curve[-1] if backtester.equity_curve else backtester.initial_capital
            })
            
        except Exception as e:
            print(f"Ошибка в bootstrap выборке {i + 1}: {e}")
            continue
    
    print(f"Bootstrap анализ завершен. Успешно выполнено {len(results)} выборок")
    return results

def _create_bootstrap_sample(data: pd.DataFrame, block_size: int, n_blocks: int) -> pd.DataFrame:
    """
    Создание bootstrap выборки с блоками
    
    Args:
        data: Исходные данные
        block_size: Размер блоков
        n_blocks: Количество блоков для выборки
        
    Returns:
        Bootstrap выборка данных
    """
    bootstrap_blocks = []
    max_start_idx = len(data) - block_size
    
    for _ in range(n_blocks):
        # Случайно выбираем начальный индекс блока
        start_idx = np.random.randint(0, max_start_idx + 1)
        end_idx = start_idx + block_size
        
        # Извлекаем блок
        block = data.iloc[start_idx:end_idx].copy()
        bootstrap_blocks.append(block)
    
    # Объединяем блоки
    bootstrap_data = pd.concat(bootstrap_blocks, ignore_index=True)
    
    return bootstrap_data

def analyze_bootstrap_results(results: List[Dict[str, Any]], confidence_level: float = 0.95) -> Dict[str, Any]:
    """
    Анализ результатов Bootstrap анализа
    
    Рассчитывает доверительные интервалы и статистики
    для оценки неопределенности результатов.
    
    Args:
        results: Результаты Bootstrap анализа
        confidence_level: Уровень доверия (по умолчанию 0.95)
        
    Returns:
        Словарь с анализом результатов
    """
    if not results:
        return {}
    
    # Извлекаем основные метрики
    returns = [r['metrics']['total_return'] for r in results]
    sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
    max_drawdowns = [r['metrics']['max_drawdown'] for r in results]
    win_rates = [r['metrics']['win_rate'] for r in results]
    
    # Рассчитываем доверительные интервалы
    alpha = 1 - confidence_level
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100
    
    analysis = {
        'n_bootstrap': len(results),
        'confidence_level': confidence_level,
        
        # Доверительные интервалы для доходности
        'return_ci': {
            'mean': np.mean(returns),
            'std': np.std(returns),
            'lower': np.percentile(returns, lower_percentile),
            'upper': np.percentile(returns, upper_percentile),
            'width': np.percentile(returns, upper_percentile) - np.percentile(returns, lower_percentile)
        },
        
        # Доверительные интервалы для Sharpe ratio
        'sharpe_ci': {
            'mean': np.mean(sharpe_ratios),
            'std': np.std(sharpe_ratios),
            'lower': np.percentile(sharpe_ratios, lower_percentile),
            'upper': np.percentile(sharpe_ratios, upper_percentile),
            'width': np.percentile(sharpe_ratios, upper_percentile) - np.percentile(sharpe_ratios, lower_percentile)
        },
        
        # Доверительные интервалы для максимальной просадки
        'drawdown_ci': {
            'mean': np.mean(max_drawdowns),
            'std': np.std(max_drawdowns),
            'lower': np.percentile(max_drawdowns, lower_percentile),
            'upper': np.percentile(max_drawdowns, upper_percentile),
            'width': np.percentile(max_drawdowns, upper_percentile) - np.percentile(max_drawdowns, lower_percentile)
        },
        
        # Доверительные интервалы для win rate
        'win_rate_ci': {
            'mean': np.mean(win_rates),
            'std': np.std(win_rates),
            'lower': np.percentile(win_rates, lower_percentile),
            'upper': np.percentile(win_rates, upper_percentile),
            'width': np.percentile(win_rates, upper_percentile) - np.percentile(win_rates, lower_percentile)
        },
        
        # Статистическая значимость
        'significance': {
            'return_significant': np.percentile(returns, lower_percentile) > 0,
            'sharpe_significant': np.percentile(sharpe_ratios, lower_percentile) > 0,
            'positive_return_prob': np.mean([r > 0 for r in returns]),
            'sharpe_above_1_prob': np.mean([s > 1 for s in sharpe_ratios])
        }
    }
    
    return analysis
```

## Учет реалистичности

**Теория:** Реалистичный бэктестинг должен учитывать все факторы, которые влияют на реальную торговлю. Игнорирование этих факторов приводит к завышенным результатам и неправильным выводам о производительности стратегии.

**Ключевые факторы реалистичности:**
- **Транзакционные издержки:** Комиссии, спреды, налоги
- **Ликвидность:** Влияние объема торгов на цену
- **Проскальзывание:** Разница между ожидаемой и фактической ценой
- **Задержки исполнения:** Время между сигналом и исполнением
- **Ограничения капитала:** Минимальные размеры позиций, маржинальные требования

### 1. Комиссии и спреды

**Теория:** Комиссии и спреды - это основные транзакционные издержки, которые значительно влияют на прибыльность стратегии. Учет этих издержек критически важен для получения реалистичных результатов.

**Типы транзакционных издержек:**
- **Комиссии:** Фиксированные или процентные платежи брокеру
- **Спреды:** Разница между ценой покупки и продажи
- **Налоги:** Подоходный налог с прибыли
- **Сборы:** Дополнительные платежи за обслуживание

**Влияние на результаты:**
- **Снижение доходности:** Прямое уменьшение прибыли
- **Изменение частоты торгов:** Высокие издержки делают частую торговлю невыгодной
- **Влияние на размер позиций:** Необходимость учитывать издержки при расчете размера
- **Изменение стратегии:** Может потребовать модификации логики торговли

```python
class RealisticBacktester(Backtester):
    """
    Реалистичный бэктестер с учетом транзакционных издержек
    
    Этот класс расширяет базовый Backtester для учета
    реальных факторов торговли:
    - Комиссии за сделки
    - Спреды между ценами покупки и продажи
    - Минимальные размеры позиций
    - Ограничения на частоту торгов
    """
    
    def __init__(self, initial_capital: float = 10000, 
                 commission: float = 0.001, 
                 spread: float = 0.0005,
                 min_position_size: float = 100,
                 min_trade_interval: int = 1):
        """
        Инициализация реалистичного бэктестера
        
        Args:
            initial_capital: Начальный капитал
            commission: Комиссия за сделку (в долях от суммы)
            spread: Спред между ценами покупки и продажи (в долях)
            min_position_size: Минимальный размер позиции в валюте
            min_trade_interval: Минимальный интервал между сделками (в периодах)
        """
        super().__init__(initial_capital, commission)
        self.spread = spread
        self.min_position_size = min_position_size
        self.min_trade_interval = min_trade_interval
        self.last_trade_period = -min_trade_interval  # Последний период торговли
        
    def execute_trade(self, row: pd.Series, signal: str, timestamp: datetime) -> None:
        """
        Реалистичное выполнение торговых операций
        
        Учитывает:
        - Спреды между ценами покупки и продажи
        - Минимальные размеры позиций
        - Интервалы между сделками
        - Комиссии за каждую операцию
        
        Args:
            row: Текущая строка данных (OHLCV)
            signal: Торговый сигнал ('BUY', 'SELL', 'HOLD')
            timestamp: Временная метка сделки
        """
        current_period = len(self.equity_curve)
        
        # Проверяем минимальный интервал между сделками
        if current_period - self.last_trade_period < self.min_trade_interval:
            return
        
        # Рассчитываем цены с учетом спреда
        if signal == 'BUY':
            # Покупаем по цене выше рыночной (ask price)
            price = row['Close'] * (1 + self.spread)
        elif signal == 'SELL':
            # Продаем по цене ниже рыночной (bid price)
            price = row['Close'] * (1 - self.spread)
        else:
            return
        
        # Проверяем минимальный размер позиции
        if signal == 'BUY' and self.capital < self.min_position_size:
            return
        elif signal == 'SELL' and self.position_value < self.min_position_size:
            return
        
        # Выполняем сделку
        if signal == 'BUY' and self.position <= 0:
            if self.position < 0:
                # Закрываем короткую позицию
                self.close_position(price, timestamp, 'SHORT')
            
            # Открываем длинную позицию
            self.open_position(price, 'LONG', timestamp)
            self.last_trade_period = current_period
            
        elif signal == 'SELL' and self.position >= 0:
            if self.position > 0:
                # Закрываем длинную позицию
                self.close_position(price, timestamp, 'LONG')
            
            # Открываем короткую позицию
            self.open_position(price, 'SHORT', timestamp)
            self.last_trade_period = current_period
    
    def open_position(self, price: float, direction: str, timestamp: datetime) -> None:
        """
        Открытие позиции с учетом реалистичных условий
        
        Args:
            price: Цена открытия позиции (с учетом спреда)
            direction: Направление позиции ('LONG' или 'SHORT')
            timestamp: Временная метка
        """
        if direction == 'LONG':
            # Покупка: используем весь доступный капитал
            self.position = self.capital / price
            self.position_value = self.position * price
            self.capital = 0
            
            # Рассчитываем комиссию
            commission_cost = self.position_value * self.commission
            
            # Записываем сделку
            trade = Trade(
                timestamp=timestamp,
                price=price,
                quantity=self.position,
                direction='LONG',
                commission=commission_cost
            )
            self.trades.append(trade)
            
        elif direction == 'SHORT':
            # Продажа: открываем короткую позицию
            self.position = -self.capital / price
            self.position_value = abs(self.position) * price
            self.capital = 0
            
            # Рассчитываем комиссию
            commission_cost = self.position_value * self.commission
            
            # Записываем сделку
            trade = Trade(
                timestamp=timestamp,
                price=price,
                quantity=abs(self.position),
                direction='SHORT',
                commission=commission_cost
            )
            self.trades.append(trade)
    
    def close_position(self, price: float, timestamp: datetime, direction: str) -> None:
        """
        Закрытие позиции с учетом реалистичных условий
        
        Args:
            price: Цена закрытия позиции (с учетом спреда)
            timestamp: Временная метка
            direction: Направление закрываемой позиции
        """
        if direction == 'LONG' and self.position > 0:
            # Закрываем длинную позицию
            self.capital = self.position * price * (1 - self.commission)
            profit = self.capital - self.position_value
            
            # Записываем сделку закрытия
            trade = Trade(
                timestamp=timestamp,
                price=price,
                quantity=self.position,
                direction='CLOSE_LONG',
                profit=profit,
                commission=self.position * price * self.commission
            )
            self.trades.append(trade)
            
        elif direction == 'SHORT' and self.position < 0:
            # Закрываем короткую позицию
            self.capital = -self.position * price * (1 - self.commission)
            profit = self.capital - self.position_value
            
            # Записываем сделку закрытия
            trade = Trade(
                timestamp=timestamp,
                price=price,
                quantity=abs(self.position),
                direction='CLOSE_SHORT',
                profit=profit,
                commission=abs(self.position) * price * self.commission
            )
            self.trades.append(trade)
        
        # Сбрасываем позицию
        self.position = 0
        self.position_value = 0
```

### 2. Ликвидность и проскальзывание

**Теория:** Ликвидность и проскальзывание - это факторы, которые значительно влияют на реальную торговлю, но часто игнорируются в простых бэктестах. Учет этих факторов критически важен для получения реалистичных результатов.

**Что такое ликвидность:**
- **Определение:** Способность быстро купить или продать актив без значительного влияния на цену
- **Факторы:** Объем торгов, количество участников, волатильность
- **Измерение:** Спред bid-ask, глубина рынка, время исполнения

**Что такое проскальзывание:**
- **Определение:** Разница между ожидаемой ценой исполнения и фактической ценой
- **Причины:** Недостаточная ликвидность, большие объемы, волатильность
- **Типы:** Положительное (выгодное) и отрицательное (невыгодное)

**Влияние на торговлю:**
- **Снижение прибыли:** Проскальзывание уменьшает доходность
- **Изменение стратегии:** Может потребовать модификации логики
- **Управление рисками:** Необходимость учета ликвидности при планировании
- **Размер позиций:** Ограничения на максимальные объемы

```python
def calculate_slippage(volume: float, market_volume: float, price: float, 
                      volatility: float = 0.02) -> float:
    """
    Расчет проскальзывания на основе объема и ликвидности
    
    Проскальзывание зависит от:
    - Отношения объема сделки к рыночному объему
    - Волатильности актива
    - Времени исполнения
    - Глубины рынка
    
    Args:
        volume: Объем нашей сделки
        market_volume: Средний рыночный объем
        price: Текущая цена актива
        volatility: Волатильность актива (по умолчанию 2%)
        
    Returns:
        Размер проскальзывания в валюте
    """
    if market_volume <= 0:
        return 0
    
    # Отношение объема к рыночному объему
    volume_ratio = volume / market_volume
    
    # Базовое проскальзывание в зависимости от объема
    if volume_ratio < 0.001:  # Очень малый объем (< 0.1%)
        base_slippage = 0.0001
    elif volume_ratio < 0.01:  # Малый объем (0.1% - 1%)
        base_slippage = 0.0005
    elif volume_ratio < 0.05:  # Средний объем (1% - 5%)
        base_slippage = 0.001
    elif volume_ratio < 0.1:   # Большой объем (5% - 10%)
        base_slippage = 0.002
    else:  # Очень большой объем (> 10%)
        base_slippage = 0.005
    
    # Корректировка на волатильность
    volatility_multiplier = 1 + (volatility / 0.02)  # Нормализация к 2%
    
    # Итоговое проскальзывание
    total_slippage = base_slippage * volatility_multiplier
    
    return price * total_slippage

def calculate_market_impact(volume: float, market_volume: float, 
                           price: float, volatility: float = 0.02) -> float:
    """
    Расчет влияния на рынок (market impact)
    
    Market impact - это влияние нашей сделки на цену актива.
    Чем больше объем относительно рыночного, тем больше влияние.
    
    Args:
        volume: Объем нашей сделки
        market_volume: Средний рыночный объем
        price: Текущая цена актива
        volatility: Волатильность актива
        
    Returns:
        Влияние на цену в валюте
    """
    if market_volume <= 0:
        return 0
    
    # Отношение объема к рыночному объему
    volume_ratio = volume / market_volume
    
    # Коэффициент влияния (квадратичная зависимость)
    impact_coefficient = volume_ratio ** 1.5
    
    # Корректировка на волатильность
    volatility_multiplier = 1 + (volatility / 0.02)
    
    # Итоговое влияние
    total_impact = impact_coefficient * volatility_multiplier * 0.001
    
    return price * total_impact

class LiquidityAwareBacktester(RealisticBacktester):
    """
    Бэктестер с учетом ликвидности и проскальзывания
    
    Этот класс расширяет RealisticBacktester для учета:
    - Проскальзывания при исполнении сделок
    - Влияния на рынок (market impact)
    - Ограничений по ликвидности
    - Временных задержек исполнения
    """
    
    def __init__(self, initial_capital: float = 10000,
                 commission: float = 0.001,
                 spread: float = 0.0005,
                 min_position_size: float = 100,
                 min_trade_interval: int = 1,
                 max_volume_ratio: float = 0.1,
                 execution_delay: int = 0):
        """
        Инициализация бэктестера с учетом ликвидности
        
        Args:
            initial_capital: Начальный капитал
            commission: Комиссия за сделку
            spread: Спред между ценами
            min_position_size: Минимальный размер позиции
            min_trade_interval: Минимальный интервал между сделками
            max_volume_ratio: Максимальное отношение объема к рыночному
            execution_delay: Задержка исполнения в периодах
        """
        super().__init__(initial_capital, commission, spread, 
                        min_position_size, min_trade_interval)
        self.max_volume_ratio = max_volume_ratio
        self.execution_delay = execution_delay
        self.pending_orders = []  # Ожидающие исполнения ордера
        
    def execute_trade(self, row: pd.Series, signal: str, timestamp: datetime) -> None:
        """
        Выполнение торгов с учетом ликвидности
        
        Args:
            row: Текущая строка данных (OHLCV)
            signal: Торговый сигнал
            timestamp: Временная метка
        """
        # Обрабатываем ожидающие ордера
        self._process_pending_orders(row, timestamp)
        
        if signal in ['BUY', 'SELL']:
            # Рассчитываем объем сделки
            if signal == 'BUY':
                volume = self.capital / row['Close']
            else:  # SELL
                volume = abs(self.position) if self.position != 0 else 0
            
            # Проверяем ограничения по ликвидности
            if not self._check_liquidity_constraints(volume, row['Volume']):
                return
            
            # Рассчитываем проскальзывание и влияние на рынок
            slippage = calculate_slippage(volume, row['Volume'], row['Close'])
            market_impact = calculate_market_impact(volume, row['Volume'], row['Close'])
            
            # Корректируем цену
            if signal == 'BUY':
                price = row['Close'] + slippage + market_impact
            else:  # SELL
                price = row['Close'] - slippage - market_impact
            
            # Создаем ордер с задержкой исполнения
            if self.execution_delay > 0:
                self.pending_orders.append({
                    'signal': signal,
                    'price': price,
                    'volume': volume,
                    'timestamp': timestamp,
                    'execution_time': len(self.equity_curve) + self.execution_delay
                })
            else:
                # Немедленное исполнение
                self._execute_immediate_trade(signal, price, timestamp)
    
    def _check_liquidity_constraints(self, volume: float, market_volume: float) -> bool:
        """
        Проверка ограничений по ликвидности
        
        Args:
            volume: Объем нашей сделки
            market_volume: Рыночный объем
            
        Returns:
            True, если ограничения соблюдены
        """
        if market_volume <= 0:
            return False
        
        volume_ratio = volume / market_volume
        return volume_ratio <= self.max_volume_ratio
    
    def _process_pending_orders(self, row: pd.Series, timestamp: datetime) -> None:
        """
        Обработка ожидающих исполнения ордеров
        
        Args:
            row: Текущая строка данных
            timestamp: Текущая временная метка
        """
        current_period = len(self.equity_curve)
        
        # Фильтруем ордера, готовые к исполнению
        ready_orders = [order for order in self.pending_orders 
                       if order['execution_time'] <= current_period]
        
        for order in ready_orders:
            self._execute_immediate_trade(
                order['signal'], 
                order['price'], 
                order['timestamp']
            )
        
        # Удаляем исполненные ордера
        self.pending_orders = [order for order in self.pending_orders 
                              if order['execution_time'] > current_period]
    
    def _execute_immediate_trade(self, signal: str, price: float, timestamp: datetime) -> None:
        """
        Немедленное исполнение сделки
        
        Args:
            signal: Торговый сигнал
            price: Цена исполнения
            timestamp: Временная метка
        """
        # Создаем временную строку данных с скорректированной ценой
        temp_row = pd.Series({'Close': price})
        
        # Выполняем сделку через родительский метод
        super().execute_trade(temp_row, signal, timestamp)
```

## Визуализация результатов

**Теория:** Визуализация результатов бэктестинга критически важна для понимания поведения стратегии. Графики помогают:

- **Выявить паттерны** в производительности стратегии
- **Обнаружить проблемы** в логике торговли
- **Сравнить стратегии** визуально
- **Понять риски** через графики просадок
- **Проверить стабильность** доходности

**Типы визуализации:**
- **Кривые капитала:** Показывают рост/падение капитала во времени
- **Графики просадок:** Визуализируют потери от пиков
- **Распределения доходности:** Показывают статистические свойства
- **Корреляционные матрицы:** Анализируют зависимости между активами
- **Тепловые карты:** Отображают производительность по периодам

### 1. Equity Curve

**Теория:** Кривая капитала (equity curve) - это основной график для анализа производительности стратегии. Она показывает изменение стоимости портфеля во времени и позволяет:

- **Оценить общую тенденцию** - растет или падает капитал
- **Выявить периоды стагнации** - когда стратегия не работает
- **Обнаружить волатильность** - насколько стабильна доходность
- **Сравнить с бенчмарком** - лучше или хуже рынка

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

def plot_equity_curve(equity_curve: List[float], 
                     dates: List[datetime] = None,
                     benchmark: List[float] = None,
                     benchmark_dates: List[datetime] = None,
                     title: str = "Equity Curve",
                     figsize: tuple = (15, 8)) -> None:
    """
    Построение кривой капитала с дополнительной информацией
    
    Args:
        equity_curve: Список значений капитала
        dates: Список дат (если есть)
        benchmark: Кривая бенчмарка для сравнения
        benchmark_dates: Даты бенчмарка
        title: Заголовок графика
        figsize: Размер графика
    """
    plt.figure(figsize=figsize)
    
    # Подготовка данных
    if dates is not None:
        x_data = dates
        x_label = "Date"
    else:
        x_data = range(len(equity_curve))
        x_label = "Period"
    
    # Основная кривая капитала
    plt.plot(x_data, equity_curve, label='Strategy', linewidth=2, color='blue')
    
    # Бенчмарк (если есть)
    if benchmark is not None:
        if benchmark_dates is not None:
            plt.plot(benchmark_dates, benchmark, label='Benchmark', 
                    linewidth=2, alpha=0.7, color='orange')
        else:
            plt.plot(x_data[:len(benchmark)], benchmark, label='Benchmark', 
                    linewidth=2, alpha=0.7, color='orange')
    
    # Начальная линия капитала
    initial_capital = equity_curve[0]
    plt.axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.5, 
                label=f'Initial Capital: ${initial_capital:,.0f}')
    
    # Форматирование
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Форматирование осей
    if dates is not None:
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=45)
    
    # Форматирование оси Y
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.tight_layout()
    plt.show()

def plot_equity_curve_with_metrics(equity_curve: List[float], 
                                  metrics: Dict[str, Any],
                                  dates: List[datetime] = None,
                                  title: str = "Equity Curve with Metrics") -> None:
    """
    Построение кривой капитала с отображением ключевых метрик
    
    Args:
        equity_curve: Список значений капитала
        metrics: Словарь с метриками
        dates: Список дат
        title: Заголовок графика
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), 
                                   gridspec_kw={'height_ratios': [3, 1]})
    
    # Основной график - кривая капитала
    if dates is not None:
        ax1.plot(dates, equity_curve, linewidth=2, color='blue')
    else:
        ax1.plot(equity_curve, linewidth=2, color='blue')
    
    ax1.set_title(title, fontsize=16, fontweight='bold')
    ax1.set_ylabel('Portfolio Value ($)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Добавляем метрики на график
    metrics_text = f"""
    Total Return: {metrics.get('total_return', 0):.2%}
    Annual Return: {metrics.get('annual_return', 0):.2%}
    Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}
    Max Drawdown: {metrics.get('max_drawdown', 0):.2%}
    Win Rate: {metrics.get('win_rate', 0):.2%}
    """
    ax1.text(0.02, 0.98, metrics_text, transform=ax1.transAxes, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Нижний график - просадки
    equity_series = pd.Series(equity_curve)
    running_max = equity_series.expanding().max()
    drawdown = (equity_series - running_max) / running_max
    
    if dates is not None:
        ax2.fill_between(dates, drawdown, 0, alpha=0.3, color='red')
        ax2.plot(dates, drawdown, color='red', linewidth=1)
    else:
        ax2.fill_between(range(len(drawdown)), drawdown, 0, alpha=0.3, color='red')
        ax2.plot(drawdown, color='red', linewidth=1)
    
    ax2.set_title('Drawdown', fontsize=14)
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Drawdown %', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
    
    plt.tight_layout()
    plt.show()
```

### 2. Drawdown Chart

**Теория:** График просадок показывает максимальные потери от пиковых значений. Это критически важный график для понимания рисков стратегии:

- **Максимальная просадка** - худшая потеря от пика
- **Длительность просадок** - как долго стратегия восстанавливается
- **Частота просадок** - как часто происходят потери
- **Восстановление** - скорость возврата к пиковым значениям

```python
def plot_drawdown_analysis(equity_curve: List[float], 
                          dates: List[datetime] = None,
                          title: str = "Drawdown Analysis") -> None:
    """
    Комплексный анализ просадок
    
    Args:
        equity_curve: Список значений капитала
        dates: Список дат
        title: Заголовок графика
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
    
    equity_series = pd.Series(equity_curve)
    running_max = equity_series.expanding().max()
    drawdown = (equity_series - running_max) / running_max
    
    # График 1: Кривая капитала с пиками
    if dates is not None:
        ax1.plot(dates, equity_curve, label='Portfolio Value', linewidth=2, color='blue')
        ax1.plot(dates, running_max, label='Running Maximum', linewidth=1, 
                color='green', linestyle='--', alpha=0.7)
    else:
        ax1.plot(equity_curve, label='Portfolio Value', linewidth=2, color='blue')
        ax1.plot(running_max, label='Running Maximum', linewidth=1, 
                color='green', linestyle='--', alpha=0.7)
    
    ax1.set_title(f'{title} - Portfolio Value', fontsize=14)
    ax1.set_ylabel('Value ($)', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # График 2: Просадки
    if dates is not None:
        ax2.fill_between(dates, drawdown, 0, alpha=0.3, color='red')
        ax2.plot(dates, drawdown, color='red', linewidth=1)
    else:
        ax2.fill_between(range(len(drawdown)), drawdown, 0, alpha=0.3, color='red')
        ax2.plot(drawdown, color='red', linewidth=1)
    
    ax2.set_title('Drawdown', fontsize=14)
    ax2.set_ylabel('Drawdown %', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
    
    # График 3: Распределение просадок
    drawdown_clean = drawdown[drawdown < 0]  # Только отрицательные просадки
    if len(drawdown_clean) > 0:
        ax3.hist(drawdown_clean, bins=30, alpha=0.7, color='red', density=True)
        ax3.axvline(drawdown_clean.mean(), color='black', linestyle='--', 
                   label=f'Mean: {drawdown_clean.mean():.2%}')
        ax3.axvline(drawdown_clean.min(), color='darkred', linestyle='--', 
                   label=f'Min: {drawdown_clean.min():.2%}')
    
    ax3.set_title('Drawdown Distribution', fontsize=14)
    ax3.set_xlabel('Drawdown %', fontsize=12)
    ax3.set_ylabel('Density', fontsize=12)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
    
    plt.tight_layout()
    plt.show()

def plot_rolling_metrics(equity_curve: List[float], 
                        window: int = 252,
                        dates: List[datetime] = None) -> None:
    """
    Построение скользящих метрик
    
    Args:
        equity_curve: Список значений капитала
        window: Размер окна для расчета метрик
        dates: Список дат
    """
    equity_series = pd.Series(equity_curve)
    returns = equity_series.pct_change().dropna()
    
    # Скользящие метрики
    rolling_returns = returns.rolling(window).mean() * 252  # Годовая доходность
    rolling_vol = returns.rolling(window).std() * np.sqrt(252)  # Годовая волатильность
    rolling_sharpe = rolling_returns / rolling_vol  # Скользящий Sharpe ratio
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 10))
    
    # График 1: Скользящая доходность
    if dates is not None:
        ax1.plot(dates[1:], rolling_returns, label='Rolling Annual Return', linewidth=2)
    else:
        ax1.plot(rolling_returns, label='Rolling Annual Return', linewidth=2)
    
    ax1.set_title('Rolling Annual Return', fontsize=14)
    ax1.set_ylabel('Return', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
    
    # График 2: Скользящая волатильность
    if dates is not None:
        ax2.plot(dates[1:], rolling_vol, label='Rolling Volatility', linewidth=2, color='orange')
    else:
        ax2.plot(rolling_vol, label='Rolling Volatility', linewidth=2, color='orange')
    
    ax2.set_title('Rolling Volatility', fontsize=14)
    ax2.set_ylabel('Volatility', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
    
    # График 3: Скользящий Sharpe ratio
    if dates is not None:
        ax3.plot(dates[1:], rolling_sharpe, label='Rolling Sharpe Ratio', linewidth=2, color='green')
    else:
        ax3.plot(rolling_sharpe, label='Rolling Sharpe Ratio', linewidth=2, color='green')
    
    ax3.set_title('Rolling Sharpe Ratio', fontsize=14)
    ax3.set_xlabel('Time', fontsize=12)
    ax3.set_ylabel('Sharpe Ratio', fontsize=12)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
```

### 3. Returns Distribution

**Теория:** Анализ распределения доходности помогает понять статистические свойства стратегии:

- **Нормальность распределения** - соответствует ли доходность нормальному распределению
- **Асимметрия** - склонность к положительным или отрицательным результатам
- **Эксцесс** - частота экстремальных событий
- **Хвосты распределения** - вероятность больших потерь или прибылей

```python
from scipy import stats
import seaborn as sns

def plot_returns_analysis(returns: List[float], 
                         title: str = "Returns Analysis") -> None:
    """
    Комплексный анализ распределения доходности
    
    Args:
        returns: Список доходностей
        title: Заголовок графика
    """
    returns_series = pd.Series(returns)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # График 1: Гистограмма с нормальным распределением
    ax1.hist(returns_series, bins=50, alpha=0.7, density=True, 
             label='Returns', color='skyblue', edgecolor='black')
    
    # Нормальное распределение для сравнения
    mu, sigma = returns_series.mean(), returns_series.std()
    x = np.linspace(returns_series.min(), returns_series.max(), 100)
    normal_dist = stats.norm.pdf(x, mu, sigma)
    ax1.plot(x, normal_dist, 'r-', linewidth=2, label='Normal Distribution')
    
    ax1.set_title('Returns Distribution', fontsize=14)
    ax1.set_xlabel('Returns', fontsize=12)
    ax1.set_ylabel('Density', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # График 2: Q-Q plot для проверки нормальности
    stats.probplot(returns_series, dist="norm", plot=ax2)
    ax2.set_title('Q-Q Plot (Normal Distribution)', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    # График 3: Box plot
    ax3.boxplot(returns_series, vert=True)
    ax3.set_title('Box Plot', fontsize=14)
    ax3.set_ylabel('Returns', fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # График 4: Кумулятивная функция распределения
    sorted_returns = np.sort(returns_series)
    cumulative = np.arange(1, len(sorted_returns) + 1) / len(sorted_returns)
    ax4.plot(sorted_returns, cumulative, linewidth=2, label='Empirical CDF')
    
    # Теоретическая CDF для нормального распределения
    normal_cdf = stats.norm.cdf(sorted_returns, mu, sigma)
    ax4.plot(sorted_returns, normal_cdf, 'r--', linewidth=2, label='Normal CDF')
    
    ax4.set_title('Cumulative Distribution Function', fontsize=14)
    ax4.set_xlabel('Returns', fontsize=12)
    ax4.set_ylabel('Cumulative Probability', fontsize=12)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    # Выводим статистики
    print(f"\n=== Returns Statistics ===")
    print(f"Count: {len(returns_series)}")
    print(f"Mean: {returns_series.mean():.4f}")
    print(f"Std: {returns_series.std():.4f}")
    print(f"Skewness: {returns_series.skew():.4f}")
    print(f"Kurtosis: {returns_series.kurtosis():.4f}")
    print(f"Min: {returns_series.min():.4f}")
    print(f"Max: {returns_series.max():.4f}")
    
    # Тест на нормальность
    shapiro_stat, shapiro_p = stats.shapiro(returns_series)
    print(f"\nShapiro-Wilk Test:")
    print(f"Statistic: {shapiro_stat:.4f}")
    print(f"P-value: {shapiro_p:.4f}")
    print(f"Normal distribution: {'Yes' if shapiro_p > 0.05 else 'No'}")

def plot_risk_return_scatter(returns: List[float], 
                           window: int = 252,
                           title: str = "Risk-Return Analysis") -> None:
    """
    Анализ риск-доходность
    
    Args:
        returns: Список доходностей
        window: Размер окна для расчета
        title: Заголовок графика
    """
    returns_series = pd.Series(returns)
    
    # Скользящие метрики
    rolling_returns = returns_series.rolling(window).mean() * 252
    rolling_vol = returns_series.rolling(window).std() * np.sqrt(252)
    
    # Убираем NaN значения
    valid_data = pd.DataFrame({
        'returns': rolling_returns,
        'volatility': rolling_vol
    }).dropna()
    
    plt.figure(figsize=(12, 8))
    
    # Scatter plot
    scatter = plt.scatter(valid_data['volatility'], valid_data['returns'], 
                         c=range(len(valid_data)), cmap='viridis', alpha=0.6)
    
    # Добавляем цветовую шкалу
    cbar = plt.colorbar(scatter)
    cbar.set_label('Time', fontsize=12)
    
    # Линии постоянного Sharpe ratio
    sharpe_ratios = [0.5, 1.0, 1.5, 2.0]
    x_vol = np.linspace(valid_data['volatility'].min(), valid_data['volatility'].max(), 100)
    
    for sr in sharpe_ratios:
        y_return = sr * x_vol
        plt.plot(x_vol, y_return, '--', alpha=0.7, 
                label=f'Sharpe = {sr}')
    
    plt.xlabel('Volatility (Annualized)', fontsize=12)
    plt.ylabel('Return (Annualized)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Форматирование осей
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
    
    plt.tight_layout()
    plt.show()
```

## Практический пример

**Теория:** Полный бэктестинг включает в себя все этапы: от базового тестирования до продвинутого анализа. Этот пример демонстрирует, как объединить все изученные техники для получения комплексной оценки стратегии.

**Этапы полного бэктестинга:**
1. **Базовый бэктестинг** - основная оценка производительности
2. **Walk-Forward анализ** - проверка стабильности во времени
3. **Monte Carlo симуляция** - оценка неопределенности
4. **Bootstrap анализ** - статистическая валидация
5. **Визуализация** - графическое представление результатов
6. **Отчет** - сводка всех метрик и выводов

```python
class CompleteBacktest:
    """
    Класс для проведения полного бэктестинга стратегии
    
    Объединяет все методы анализа:
    - Базовый бэктестинг
    - Walk-Forward анализ
    - Monte Carlo симуляция
    - Bootstrap анализ
    - Визуализация результатов
    """
    
    def __init__(self, data: pd.DataFrame, strategy, 
                 initial_capital: float = 10000,
                 commission: float = 0.001,
                 spread: float = 0.0005):
        """
        Инициализация полного бэктестинга
        
        Args:
            data: Исторические данные (OHLCV)
            strategy: Объект стратегии
            initial_capital: Начальный капитал
            commission: Комиссия за сделку
            spread: Спред между ценами
        """
        self.data = data
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.spread = spread
        
        # Результаты анализа
        self.basic_results = None
        self.wf_results = None
        self.mc_results = None
        self.bootstrap_results = None
        
    def run_complete_analysis(self, 
                            wf_train_period: int = 252,
                            wf_test_period: int = 63,
                            mc_simulations: int = 1000,
                            bootstrap_samples: int = 1000,
                            bootstrap_block_size: int = 20) -> Dict[str, Any]:
        """
        Запуск полного анализа стратегии
        
        Args:
            wf_train_period: Период обучения для Walk-Forward
            wf_test_period: Период тестирования для Walk-Forward
            mc_simulations: Количество Monte Carlo симуляций
            bootstrap_samples: Количество Bootstrap выборок
            bootstrap_block_size: Размер блоков для Bootstrap
            
        Returns:
            Словарь с результатами всех анализов
        """
        print("=" * 60)
        print("ЗАПУСК ПОЛНОГО БЭКТЕСТИНГА СТРАТЕГИИ")
        print("=" * 60)
        
        # 1. Базовый бэктестинг
        print("\n1. Базовый бэктестинг...")
        self._run_basic_backtest()
        
        # 2. Walk-Forward анализ
        print("\n2. Walk-Forward анализ...")
        self._run_walk_forward_analysis(wf_train_period, wf_test_period)
        
        # 3. Monte Carlo симуляция
        print("\n3. Monte Carlo симуляция...")
        self._run_monte_carlo_analysis(mc_simulations)
        
        # 4. Bootstrap анализ
        print("\n4. Bootstrap анализ...")
        self._run_bootstrap_analysis(bootstrap_samples, bootstrap_block_size)
        
        # 5. Визуализация
        print("\n5. Создание графиков...")
        self._create_visualizations()
        
        # 6. Отчет
        print("\n6. Генерация отчета...")
        self._generate_report()
        
        return self._compile_results()
    
    def _run_basic_backtest(self) -> None:
        """Выполнение базового бэктестинга"""
        backtester = LiquidityAwareBacktester(
            initial_capital=self.initial_capital,
            commission=self.commission,
            spread=self.spread
        )
        
        self.basic_results = backtester.run_backtest(self.data, self.strategy)
        print(f"  ✓ Базовый бэктестинг завершен")
        print(f"  ✓ Выполнено {len(backtester.trades)} сделок")
        print(f"  ✓ Общая доходность: {self.basic_results['total_return']:.2%}")
    
    def _run_walk_forward_analysis(self, train_period: int, test_period: int) -> None:
        """Выполнение Walk-Forward анализа"""
        self.wf_results = walk_forward_analysis(
            self.data, self.strategy, train_period, test_period
        )
        wf_analysis = analyze_walk_forward_results(self.wf_results)
        print(f"  ✓ Walk-Forward анализ завершен")
        print(f"  ✓ Обработано {len(self.wf_results)} периодов")
        print(f"  ✓ Средняя доходность: {wf_analysis['avg_return']:.2%}")
    
    def _run_monte_carlo_analysis(self, n_simulations: int) -> None:
        """Выполнение Monte Carlo анализа"""
        self.mc_results = monte_carlo_simulation(
            self.data, self.strategy, n_simulations
        )
        mc_analysis = analyze_monte_carlo_results(self.mc_results)
        print(f"  ✓ Monte Carlo симуляция завершена")
        print(f"  ✓ Выполнено {len(self.mc_results)} симуляций")
        print(f"  ✓ Вероятность прибыли: {mc_analysis['probabilities']['positive_return']:.2%}")
    
    def _run_bootstrap_analysis(self, n_bootstrap: int, block_size: int) -> None:
        """Выполнение Bootstrap анализа"""
        self.bootstrap_results = bootstrap_analysis(
            self.data, self.strategy, n_bootstrap, block_size
        )
        bootstrap_analysis = analyze_bootstrap_results(self.bootstrap_results)
        print(f"  ✓ Bootstrap анализ завершен")
        print(f"  ✓ Выполнено {len(self.bootstrap_results)} выборок")
        print(f"  ✓ Доверительный интервал доходности: "
              f"{bootstrap_analysis['return_ci']['lower']:.2%} - "
              f"{bootstrap_analysis['return_ci']['upper']:.2%}")
    
    def _create_visualizations(self) -> None:
        """Создание всех графиков"""
        # Основные графики
        plot_equity_curve_with_metrics(
            self.basic_results.get('equity_curve', []),
            self.basic_results
        )
        
        plot_drawdown_analysis(
            self.basic_results.get('equity_curve', [])
        )
        
        if self.basic_results.get('daily_returns'):
            plot_returns_analysis(self.basic_results['daily_returns'])
            plot_risk_return_scatter(self.basic_results['daily_returns'])
        
        # Walk-Forward графики
        if self.wf_results:
            self._plot_walk_forward_results()
        
        # Monte Carlo графики
        if self.mc_results:
            self._plot_monte_carlo_results()
    
    def _plot_walk_forward_results(self) -> None:
        """Графики Walk-Forward анализа"""
        wf_returns = [r['metrics']['total_return'] for r in self.wf_results]
        wf_periods = [r['period'] for r in self.wf_results]
        
        plt.figure(figsize=(15, 6))
        plt.plot(wf_periods, wf_returns, 'o-', linewidth=2, markersize=6)
        plt.axhline(y=0, color='red', linestyle='--', alpha=0.7)
        plt.title('Walk-Forward Analysis - Returns by Period', fontsize=14)
        plt.xlabel('Period', fontsize=12)
        plt.ylabel('Return', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
        plt.tight_layout()
        plt.show()
    
    def _plot_monte_carlo_results(self) -> None:
        """Графики Monte Carlo анализа"""
        mc_returns = [r['metrics']['total_return'] for r in self.mc_results]
        
        plt.figure(figsize=(12, 8))
        
        # Гистограмма доходностей
        plt.subplot(2, 2, 1)
        plt.hist(mc_returns, bins=50, alpha=0.7, density=True)
        plt.axvline(np.mean(mc_returns), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(mc_returns):.2%}')
        plt.title('Monte Carlo Returns Distribution')
        plt.xlabel('Return')
        plt.ylabel('Density')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Кумулятивная функция распределения
        plt.subplot(2, 2, 2)
        sorted_returns = np.sort(mc_returns)
        cumulative = np.arange(1, len(sorted_returns) + 1) / len(sorted_returns)
        plt.plot(sorted_returns, cumulative, linewidth=2)
        plt.title('Cumulative Distribution Function')
        plt.xlabel('Return')
        plt.ylabel('Cumulative Probability')
        plt.grid(True, alpha=0.3)
        
        # Временной ряд доходностей
        plt.subplot(2, 2, 3)
        plt.plot(mc_returns[:100], alpha=0.7)  # Показываем первые 100
        plt.title('Monte Carlo Returns (First 100)')
        plt.xlabel('Simulation')
        plt.ylabel('Return')
        plt.grid(True, alpha=0.3)
        
        # Box plot
        plt.subplot(2, 2, 4)
        plt.boxplot(mc_returns)
        plt.title('Monte Carlo Returns Box Plot')
        plt.ylabel('Return')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _generate_report(self) -> None:
        """Генерация текстового отчета"""
        print("\n" + "=" * 60)
        print("ОТЧЕТ О РЕЗУЛЬТАТАХ БЭКТЕСТИНГА")
        print("=" * 60)
        
        # Базовые метрики
        print("\n📊 БАЗОВЫЕ МЕТРИКИ:")
        print(f"  Общая доходность: {self.basic_results['total_return']:.2%}")
        print(f"  Годовая доходность: {self.basic_results['annual_return']:.2%}")
        print(f"  Волатильность: {self.basic_results['volatility']:.2%}")
        print(f"  Sharpe Ratio: {self.basic_results['sharpe_ratio']:.2f}")
        print(f"  Максимальная просадка: {self.basic_results['max_drawdown']:.2%}")
        print(f"  Win Rate: {self.basic_results['win_rate']:.2%}")
        print(f"  Profit Factor: {self.basic_results['profit_factor']:.2f}")
        
        # Walk-Forward анализ
        if self.wf_results:
            wf_analysis = analyze_walk_forward_results(self.wf_results)
            print(f"\n🔄 WALK-FORWARD АНАЛИЗ:")
            print(f"  Периодов: {wf_analysis['total_periods']}")
            print(f"  Средняя доходность: {wf_analysis['avg_return']:.2%}")
            print(f"  Стандартное отклонение: {wf_analysis['std_return']:.2%}")
            print(f"  Положительных периодов: {wf_analysis['positive_periods_pct']:.2%}")
            print(f"  Коэффициент стабильности: {wf_analysis['consistency_score']:.2f}")
        
        # Monte Carlo анализ
        if self.mc_results:
            mc_analysis = analyze_monte_carlo_results(self.mc_results)
            print(f"\n🎲 MONTE CARLO АНАЛИЗ:")
            print(f"  Симуляций: {mc_analysis['n_simulations']}")
            print(f"  Средняя доходность: {mc_analysis['return_stats']['mean']:.2%}")
            print(f"  Вероятность прибыли: {mc_analysis['probabilities']['positive_return']:.2%}")
            print(f"  VaR (95%): {mc_analysis['var_cvar']['var_95']:.2%}")
            print(f"  CVaR (95%): {mc_analysis['var_cvar']['cvar_95']:.2%}")
        
        # Bootstrap анализ
        if self.bootstrap_results:
            bootstrap_analysis = analyze_bootstrap_results(self.bootstrap_results)
            print(f"\n📈 BOOTSTRAP АНАЛИЗ:")
            print(f"  Выборок: {bootstrap_analysis['n_bootstrap']}")
            print(f"  Доверительный интервал доходности: "
                  f"{bootstrap_analysis['return_ci']['lower']:.2%} - "
                  f"{bootstrap_analysis['return_ci']['upper']:.2%}")
            print(f"  Статистическая значимость доходности: "
                  f"{'Да' if bootstrap_analysis['significance']['return_significant'] else 'Нет'}")
    
    def _compile_results(self) -> Dict[str, Any]:
        """Компиляция всех результатов"""
        return {
            'basic_results': self.basic_results,
            'walk_forward_results': self.wf_results,
            'monte_carlo_results': self.mc_results,
            'bootstrap_results': self.bootstrap_results,
            'summary': {
                'total_return': self.basic_results['total_return'],
                'sharpe_ratio': self.basic_results['sharpe_ratio'],
                'max_drawdown': self.basic_results['max_drawdown'],
                'win_rate': self.basic_results['win_rate']
            }
        }

# Пример использования
def run_complete_backtest_example():
    """
    Пример полного бэктестинга стратегии
    
    Этот пример демонстрирует, как использовать класс CompleteBacktest
    для проведения комплексного анализа торговой стратегии.
    """
    # Создаем простую стратегию для примера
    class SimpleMovingAverageStrategy:
        def __init__(self, short_window=20, long_window=50):
            self.short_window = short_window
            self.long_window = long_window
            self.short_ma = None
            self.long_ma = None
        
        def get_signal(self, data):
            if len(data) < self.long_window:
                return 'HOLD'
            
            # Рассчитываем скользящие средние
            short_ma = data['Close'].rolling(self.short_window).mean().iloc[-1]
            long_ma = data['Close'].rolling(self.long_window).mean().iloc[-1]
            
            # Простая стратегия пересечения
            if short_ma > long_ma:
                return 'BUY'
            elif short_ma < long_ma:
                return 'SELL'
            else:
                return 'HOLD'
    
    # Генерируем тестовые данные
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    prices = 100 * np.cumprod(1 + np.random.normal(0.0005, 0.02, len(dates)))
    
    data = pd.DataFrame({
        'Open': prices * (1 + np.random.normal(0, 0.001, len(dates))),
        'High': prices * (1 + np.abs(np.random.normal(0, 0.01, len(dates)))),
        'Low': prices * (1 - np.abs(np.random.normal(0, 0.01, len(dates)))),
        'Close': prices,
        'Volume': np.random.randint(1000, 10000, len(dates))
    }, index=dates)
    
    # Создаем стратегию
    strategy = SimpleMovingAverageStrategy()
    
    # Запускаем полный анализ
    backtest = CompleteBacktest(data, strategy)
    results = backtest.run_complete_analysis()
    
    return results

# Запуск примера
if __name__ == "__main__":
    results = run_complete_backtest_example()
```

## Следующие шаги

После изучения бэктестинга переходите к:

- **[07_walk_forward_analysis.md](07_walk_forward_analysis.md)** - Детальное изучение Walk-Forward анализа
- **[08_monte_carlo_simulation.md](08_monte_carlo_simulation.md)** - Углубленное изучение Monte Carlo симуляции
- **[09_risk_management.md](09_risk_management.md)** - Управление рисками в торговых стратегиях
- **[10_portfolio_optimization.md](10_portfolio_optimization.md)** - Оптимизация портфеля стратегий

## Ключевые выводы

### 🎯 Основные принципы

1. **Избегайте look-ahead bias** - используйте только исторические данные
2. **Учитывайте реалистичность** - комиссии, спреды, ликвидность, проскальзывание
3. **Проверяйте стабильность** - используйте Walk-Forward анализ
4. **Оценивайте неопределенность** - применяйте Monte Carlo симуляцию
5. **Валидируйте статистически** - используйте Bootstrap анализ

### 📊 Метрики качества

- **Доходность:** Общая, годовая, средняя
- **Риск:** Волатильность, максимальная просадка, VaR
- **Эффективность:** Sharpe ratio, Sortino ratio, Calmar ratio
- **Стабильность:** Win rate, profit factor, recovery factor

### ⚠️ Типичные ошибки

- **Look-ahead bias** - использование будущей информации
- **Survivorship bias** - игнорирование "мертвых" активов
- **Overfitting** - переобучение на исторических данных
- **Игнорирование транзакционных издержек** - нереалистичные результаты
- **Недооценка рисков** - фокус только на доходности

### 🔧 Инструменты

- **Базовый бэктестер** - для простого тестирования
- **Реалистичный бэктестер** - с учетом транзакционных издержек
- **Бэктестер с ликвидностью** - с учетом проскальзывания
- **Walk-Forward анализ** - для проверки стабильности
- **Monte Carlo симуляция** - для оценки неопределенности
- **Bootstrap анализ** - для статистической валидации

### 📈 Визуализация

- **Кривые капитала** - для оценки общей тенденции
- **Графики просадок** - для понимания рисков
- **Распределения доходности** - для статистического анализа
- **Скользящие метрики** - для анализа стабильности

---

## 🎓 Практические рекомендации

### Для начинающих

1. Начните с простого бэктестера
2. Изучите основные метрики
3. Научитесь интерпретировать графики
4. Постепенно добавляйте реалистичность

### Для продвинутых

1. Используйте все методы анализа
2. Создавайте собственные метрики
3. Адаптируйте код под свои нужды
4. Проводите A/B тестирование стратегий

### Для профессионалов

1. Интегрируйте с реальными данными
2. Автоматизируйте процесс анализа
3. Создавайте дашборды для мониторинга
4. Разрабатывайте системы алертов

---

**💡 Помните:** Хороший бэктестинг - это не просто высокая доходность, а **стабильная, реалистичная и воспроизводимая** прибыльность, которая подтверждается множественными методами анализа!
