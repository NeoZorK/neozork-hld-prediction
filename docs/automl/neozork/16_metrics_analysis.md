# 16. Метрики and анализ - Измерение производительности системы

**Goal:** Понять, как правильно измерять and анализировать производительность ML-системы for достижения доходности 100%+ in месяц.

## Введение in метрики производительности

**Теория:** Метрики производительности представляют собой количественные показатели, которые позволяют объективно оценивать эффективность ML-системы in финансовой торговле. in контексте высокочастотной торговли and алгоритмических стратегий, правильный выбор and интерпретация метрик критически важны for:

1. **Оценки реальной доходности** - понимания того, действительно ли система генерирует прибыль
2. **Управления рисками** - контроля потенциальных потерь and просадок
3. **Оптимизации стратегии** - выявления слабых мест and возможностей for улучшения
4. **Сравнения подходов** - выбора лучших алгоритмов and параметров
5. **Monitoringа стабильности** - отслеживания деградации производительности во времени

**Почему метрики критически важны in финансовой торговле:**
- **Объективная оценка:** Обеспечивают объективную оценку производительности без эмоциональных искажений
- **Принятие решений:** Критически важны for принятия правильных торговых решений
- **Оптимизация:** Помогают оптимизировать parameters стратегии and алгоритмы
- **Сравнение:** Позволяют сравнивать различные торговые стратегии and подходы
- **Риск-менеджмент:** Обеспечивают контроль рисков and защиту капитала

### Проблемы без правильных метрик

**Теория:** Отсутствие правильных метрик приводит к серьезным проблемам in оценке and управлении ML-системой. Эти проблемы могут привести к катастрофическим потерям and неправильным решениям.

1. **Ложное чувство успеха - система кажется прибыльной, но on самом деле проигрывает**
 - **Теория:** Неправильные метрики могут создавать иллюзию успеха
 - **Почему проблематично:** Может привести к продолжению использования неэффективной системы
 - **Плюсы:** Временное психологическое удовлетворение
 - **Минусы:** Реальные потери, неправильные решения

2. **Неправильная оптимизация - оптимизация not тех параметров**
 - **Теория:** Неправильные метрики приводят к оптимизации not тех параметров
 - **Почему проблематично:** Ресурсы тратятся on неэффективные улучшения
 - **Плюсы:** Видимость активности
 - **Минусы:** Неэффективное использование ресурсов, отсутствие реальных улучшений

3. **Игнорирование рисков - фокус только on прибыли, игнорирование рисков**
 - **Теория:** Неправильные метрики могут игнорировать важные риски
 - **Почему проблематично:** Может привести к катастрофическим потерям
 - **Плюсы:** Простота фокуса
 - **Минусы:** Высокие риски, потенциальные катастрофические потери

4. **Отсутствие сравнения - нет бенчмарков for сравнения**
 - **Теория:** Без сравнения невозможно понять относительную эффективность
 - **Почему проблематично:** Невозможно оценить реальную эффективность
 - **Плюсы:** Простота
 - **Минусы:** Отсутствие контекста, неправильная оценка эффективности

5. **Неправильные выводы - принятие решений on basis неполных данных**
 - **Теория:** Неправильные метрики приводят к неправильным выводам
 - **Почему проблематично:** Может привести к катастрофическим решениям
 - **Плюсы:** Быстрота принятия решений
 - **Минусы:** Неправильные решения, потенциальные потери

### Наш подход к метрикам

**Теория:** Наш подход к метрикам основан on использовании комплексной системы метрик, которая обеспечивает полное понимание производительности системы. Это критически важно for создания эффективных ML-систем.

**Почему наш подход эффективен:**
- **Комплексность:** Обеспечивает комплексную оценку производительности
- **Объективность:** Обеспечивает объективную оценку
- **Сравнимость:** Позволяет сравнивать различные подходы
- **Практичность:** Обеспечивает практические инсайты

**Мы используем:**
- **Многоуровневые метрики**
 - **Теория:** Метрики on различных уровнях системы
 - **Почему важно:** Обеспечивает полное понимание производительности
 - **Плюсы:** Комплексная оценка, детальное понимание
 - **Минусы:** Сложность анализа, высокие требования к ресурсам

- **Временные метрики**
 - **Теория:** Метрики, учитывающие временные аспекты
 - **Почему важно:** Обеспечивает понимание динамики производительности
 - **Плюсы:** Понимание динамики, выявление трендов
 - **Минусы:** Сложность расчета, высокие требования к данным

- **Риск-скорректированные метрики**
 - **Теория:** Метрики, учитывающие риски
 - **Почему важно:** Критически важно for понимания реальной эффективности
 - **Плюсы:** Учет рисков, реалистичная оценка
 - **Минусы:** Сложность расчета, необходимость понимания рисков

- **Сравнительные метрики**
 - **Теория:** Метрики for сравнения with бенчмарками
 - **Почему важно:** Обеспечивает контекст for оценки эффективности
 - **Плюсы:** Контекст, относительная оценка
 - **Минусы:** Необходимость бенчмарков, сложность сравнения

- **Прогнозные метрики**
 - **Теория:** Метрики for оценки предсказательной способности
 - **Почему важно:** Критически важно for ML-систем
 - **Плюсы:** Оценка предсказательной способности, валидация модели
 - **Минусы:** Сложность расчета, высокие требования к данным

## Базовые метрики производительности

**Теория:** Базовые метрики производительности представляют собой фундаментальные показатели, которые позволяют оценить основную производительность системы. Эти метрики критически важны for понимания эффективности системы.

**Почему базовые метрики критичны:**
- **Фундаментальная оценка:** Обеспечивают фундаментальную оценку производительности
- **Простота понимания:** Легко понимаются and интерпретируются
- **Сравнимость:** Позволяют сравнивать различные системы
- **Практичность:** Обеспечивают практические инсайты

### 1. Метрики доходности

**Теория:** Метрики доходности представляют собой фундаментальные показатели, которые измеряют способность торговой системы генерировать прибыль. in контексте алгоритмической торговли эти метрики критически важны for:

- **Оценки финансовой эффективности** - понимания того, насколько прибыльна система
- **Сравнения стратегий** - выбора лучших торговых подходов
- **Planирования инвестиций** - определения размера позиций and капитала
- **Оценки успеха** - понимания достижения целевых показателей доходности

**Детальное объяснение каждой метрики:**

1. **Общая доходность (Total Return)** - суммарная прибыль/убыток за весь период
2. **Годовая доходность (Annualized Return)** - доходность, приведенная к годовому периоду
3. **CAGR (Compound Annual Growth Rate)** - среднегодовая доходность with учетом сложного процента
4. **Периодические доходности** - доходность on различным временным интервалам

**Практическое применение:** Эти метрики используются for первоначальной оценки стратегии, сравнения with бенчмарками and принятия решений о продолжении торговли.

**Полный функциональный код with импортами and примерами:**

```python
# Необходимые импорты for всех примеров in этом файле
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Union
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

# configuration for корректного отображения
plt.style.use('seaborn-v0_8')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class ReturnMetrics:
 """
 Класс for расчета метрик доходности торговой системы.

 Этот класс предоставляет методы for расчета различных показателей доходности,
 которые критически важны for оценки эффективности торговых стратегий.
 """

 def __init__(self, trading_days_per_year: int = 252):
 """
 Инициализация класса метрик доходности.

 Args:
 trading_days_per_year (int): Количество торговых дней in году (on умолчанию 252)
 """
 self.trading_days_per_year = trading_days_per_year
 self.metrics = {}

 def calculate_total_return(self, returns: pd.Series) -> float:
 """
 Расчет общей доходности за весь период.

 Общая доходность показывает суммарную прибыль or убыток за весь период торговли.
 Это базовая метрика, которая показывает общую эффективность стратегии.

 Args:
 returns (pd.Series): Серия доходностей (например, дневные доходности)

 Returns:
 float: Общая доходность in виде десятичной дроби (0.1 = 10%)

 Example:
 >>> returns = pd.Series([0.01, 0.02, -0.01, 0.03])
 >>> metrics = ReturnMetrics()
 >>> total_return = metrics.calculate_total_return(returns)
 >>> print(f"Общая доходность: {total_return:.2%}")
 """
 if returns.empty:
 return 0.0

 # Общая доходность = произведение (1 + доходность) - 1
 total_return = (1 + returns).prod() - 1
 return float(total_return)

 def calculate_annualized_return(self, returns: pd.Series) -> float:
 """
 Расчет годовой доходности.

 Годовая доходность показывает, какую доходность система генерировала бы
 in среднем за год, если бы работала with такой же эффективностью.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Годовая доходность in виде десятичной дроби

 Example:
 >>> returns = pd.Series([0.01] * 252) # 1% in день in течение года
 >>> metrics = ReturnMetrics()
 >>> annual_return = metrics.calculate_annualized_return(returns)
 >>> print(f"Годовая доходность: {annual_return:.2%}")
 """
 if returns.empty:
 return 0.0

 # Средняя дневная доходность * количество торговых дней in году
 mean_daily_return = returns.mean()
 annualized_return = mean_daily_return * self.trading_days_per_year
 return float(annualized_return)

 def calculate_compound_annual_growth_rate(self, returns: pd.Series) -> float:
 """
 Расчет CAGR (Compound Annual Growth Rate).

 CAGR показывает среднегодовую доходность with учетом сложного процента.
 Это более точная метрика for долгосрочной оценки, чем простая средняя.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: CAGR in виде десятичной дроби

 Example:
 >>> returns = pd.Series([0.1, 0.2, -0.05, 0.15]) # 4 дня торговли
 >>> metrics = ReturnMetrics()
 >>> cagr = metrics.calculate_compound_annual_growth_rate(returns)
 >>> print(f"CAGR: {cagr:.2%}")
 """
 if returns.empty:
 return 0.0

 # Общая доходность
 total_return = self.calculate_total_return(returns)

 # Количество лет
 years = len(returns) / self.trading_days_per_year

 if years <= 0:
 return 0.0

 # CAGR = (1 + общая_доходность)^(1/годы) - 1
 cagr = (1 + total_return) ** (1 / years) - 1
 return float(cagr)

 def calculate_monthly_returns(self, returns: pd.Series) -> pd.Series:
 """
 Расчет месячных доходностей.

 Месячные доходности показывают производительность on месяцам,
 что важно for выявления сезонных паттернов and месячной стабильности.

 Args:
 returns (pd.Series): Серия доходностей with временными метками

 Returns:
 pd.Series: Месячные доходности

 Example:
 >>> dates = pd.date_range('2023-01-01', periods=365, freq='D')
 >>> returns = pd.Series(np.random.normal(0.001, 0.02, 365), index=dates)
 >>> metrics = ReturnMetrics()
 >>> monthly = metrics.calculate_monthly_returns(returns)
 >>> print(monthly.head())
 """
 if returns.empty:
 return pd.Series(dtype=float)

 # Группировка on месяцам and суммирование доходностей
 monthly_returns = returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
 return monthly_returns

 def calculate_weekly_returns(self, returns: pd.Series) -> pd.Series:
 """
 Расчет недельных доходностей.

 Недельные доходности полезны for analysis краткосрочной производительности
 and выявления недельных паттернов in торговле.

 Args:
 returns (pd.Series): Серия доходностей with временными метками

 Returns:
 pd.Series: Недельные доходности
 """
 if returns.empty:
 return pd.Series(dtype=float)

 # Группировка on неделям and суммирование доходностей
 weekly_returns = returns.resample('W').apply(lambda x: (1 + x).prod() - 1)
 return weekly_returns

 def calculate_daily_returns(self, returns: pd.Series) -> pd.Series:
 """
 Расчет дневных доходностей.

 Дневные доходности - это базовые данные for всех остальных расчетов.
 Они показывают ежедневную производительность системы.

 Args:
 returns (pd.Series): Серия доходностей with временными метками

 Returns:
 pd.Series: Дневные доходности (то же самое, что входные данные)
 """
 return returns

 def get_all_return_metrics(self, returns: pd.Series) -> Dict[str, float]:
 """
 Расчет всех метрик доходности.

 Удобный метод for получения всех основных метрик доходности
 in одном вызове.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 Dict[str, float]: Словарь with метриками доходности
 """
 metrics = {
 'total_return': self.calculate_total_return(returns),
 'annualized_return': self.calculate_annualized_return(returns),
 'cagr': self.calculate_compound_annual_growth_rate(returns),
 'mean_daily_return': returns.mean(),
 'median_daily_return': returns.median(),
 'std_daily_return': returns.std(),
 'min_daily_return': returns.min(),
 'max_daily_return': returns.max()
 }

 # Добавляем периодические метрики если есть временные метки
 if not returns.empty and hasattr(returns.index, 'to_pydatetime'):
 monthly_returns = self.calculate_monthly_returns(returns)
 if not monthly_returns.empty:
 metrics.update({
 'mean_monthly_return': monthly_returns.mean(),
 'std_monthly_return': monthly_returns.std(),
 'positive_months_ratio': (monthly_returns > 0).mean(),
 'best_month': monthly_returns.max(),
 'worst_month': monthly_returns.min()
 })

 return metrics

# Практический example использования
def example_return_metrics():
 """
 Практический example использования метрик доходности.

 Этот example показывает, как создать тестовые данные and рассчитать
 различные метрики доходности for торговой стратегии.
 """
 print("=== example использования метрик доходности ===\n")

 # create тестовых данных
 np.random.seed(42)
 dates = pd.date_range('2023-01-01', periods=252, freq='D')

 # Симуляция доходностей with трендом and волатильностью
 trend = 0.0005 # 0.05% in день
 volatility = 0.02 # 2% волатильность
 returns = pd.Series(
 np.random.normal(trend, volatility, len(dates)),
 index=dates
 )

 # create экземпляра класса
 metrics = ReturnMetrics()

 # Расчет всех метрик
 all_metrics = metrics.get_all_return_metrics(returns)

 # Вывод результатов
 print("Результаты анализа доходности:")
 print("-" * 40)
 for metric, value in all_metrics.items():
 if 'return' in metric or 'cagr' in metric:
 print(f"{metric:25}: {value:8.2%}")
 else:
 print(f"{metric:25}: {value:8.4f}")

 # Дополнительный анализ
 print(f"\nДополнительная информация:")
 print(f"Период анализа: {len(returns)} дней")
 print(f"Положительных дней: {(returns > 0).sum()} ({(returns > 0).mean():.1%})")
 print(f"Отрицательных дней: {(returns < 0).sum()} ({(returns < 0).mean():.1%})")

 return all_metrics

# Launch примера
if __name__ == "__main__":
 example_return_metrics()
```

### 2. Метрики риска

**Теория:** Метрики риска представляют собой критически важные показатели, которые измеряют уровень риска, связанного with торговой системой. in алгоритмической торговле управление рисками является основой for сохранения капитала and обеспечения долгосрочной прибыльности.

**Почему метрики риска критически важны:**
- **Управление рисками** - предотвращение катастрофических потерь
- **Защита капитала** - сохранение торгового капитала for будущих операций
- **Planирование позиций** - определение оптимального размера позиций
- **Сравнение стратегий** - выбор менее рискованных подходов
- **Соответствие регуляторным требованиям** - соблюдение лимитов риска

**Детальное объяснение основных метрик риска:**

1. **Волатильность (Volatility)** - стандартное отклонение доходностей, мера нестабильности
2. **Максимальная просадка (Max Drawdown)** - наибольшая потеря from пика to минимума
3. **Value at Risk (VaR)** - максимальная ожидаемая потеря with заданной вероятностью
4. **Conditional VaR (CVaR)** - средняя потеря in худших сценариях
5. **Downside Deviation** - волатильность только отрицательных доходностей

**Практическое применение:** Эти метрики используются for установления лимитов риска, определения размера позиций and Monitoringа стабильности системы.

**Полный функциональный код with детальными объяснениями:**

```python
class RiskMetrics:
 """
 Класс for расчета метрик риска торговой системы.

 Этот класс предоставляет методы for расчета различных показателей риска,
 которые критически важны for управления рисками in алгоритмической торговле.
 """

 def __init__(self, trading_days_per_year: int = 252):
 """
 Инициализация класса метрик риска.

 Args:
 trading_days_per_year (int): Количество торговых дней in году
 """
 self.trading_days_per_year = trading_days_per_year
 self.metrics = {}

 def calculate_volatility(self, returns: pd.Series, annualized: bool = True) -> float:
 """
 Расчет волатильности доходностей.

 Волатильность измеряет степень изменчивости доходностей and является
 основным показателем риска. Высокая волатильность означает высокий риск.

 Args:
 returns (pd.Series): Серия доходностей
 annualized (bool): Приводить ли к годовому периоду

 Returns:
 float: Волатильность (стандартное отклонение доходностей)

 Example:
 >>> returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
 >>> risk_metrics = RiskMetrics()
 >>> vol = risk_metrics.calculate_volatility(returns)
 >>> print(f"Волатильность: {vol:.2%}")
 """
 if returns.empty:
 return 0.0

 volatility = returns.std()

 if annualized:
 volatility *= np.sqrt(self.trading_days_per_year)

 return float(volatility)

 def calculate_max_drawdown(self, returns: pd.Series) -> float:
 """
 Расчет максимальной просадки.

 Максимальная просадка показывает наибольшую потерю from пика to минимума
 за весь период торговли. Это критически важная метрика for оценки
 максимального риска системы.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Максимальная просадка in виде десятичной дроби

 Example:
 >>> returns = pd.Series([0.1, -0.05, 0.2, -0.15, 0.1])
 >>> risk_metrics = RiskMetrics()
 >>> max_dd = risk_metrics.calculate_max_drawdown(returns)
 >>> print(f"Максимальная просадка: {max_dd:.2%}")
 """
 if returns.empty:
 return 0.0

 # Кумулятивные доходности
 cumulative_returns = (1 + returns).cumprod()

 # Бегущий максимум
 running_max = cumulative_returns.expanding().max()

 # Просадка = (текущее значение - максимум) / максимум
 drawdown = (cumulative_returns - running_max) / running_max

 # Максимальная просадка (наибольшая отрицательная)
 max_drawdown = drawdown.min()

 return float(max_drawdown)

 def calculate_value_at_risk(self, returns: pd.Series, confidence_level: float = 0.05) -> float:
 """
 Расчет Value at Risk (VaR).

 VaR показывает максимальную ожидаемую потерю with заданной вероятностью
 за определенный период времени. Например, VaR 5% означает, что
 with вероятностью 95% потери not превысят этого значения.

 Args:
 returns (pd.Series): Серия доходностей
 confidence_level (float): Уровень доверия (0.05 = 5% VaR)

 Returns:
 float: VaR in виде десятичной дроби

 Example:
 >>> returns = pd.Series(np.random.normal(0.001, 0.02, 1000))
 >>> risk_metrics = RiskMetrics()
 >>> var_5 = risk_metrics.calculate_value_at_risk(returns, 0.05)
 >>> print(f"VaR 5%: {var_5:.2%}")
 """
 if returns.empty:
 return 0.0

 # VaR = процентиль доходностей on уровне confidence_level
 var = np.percentile(returns, confidence_level * 100)

 return float(var)

 def calculate_conditional_var(self, returns: pd.Series, confidence_level: float = 0.05) -> float:
 """
 Расчет Conditional Value at Risk (CVaR).

 CVaR (также известный как Expected Shortfall) показывает среднюю потерю
 in худших сценариях, которые превышают VaR. Это более консервативная
 мера риска, чем VaR.

 Args:
 returns (pd.Series): Серия доходностей
 confidence_level (float): Уровень доверия

 Returns:
 float: CVaR in виде десятичной дроби

 Example:
 >>> returns = pd.Series(np.random.normal(0.001, 0.02, 1000))
 >>> risk_metrics = RiskMetrics()
 >>> cvar = risk_metrics.calculate_conditional_var(returns, 0.05)
 >>> print(f"CVaR 5%: {cvar:.2%}")
 """
 if returns.empty:
 return 0.0

 # Сначала рассчитываем VaR
 var = self.calculate_value_at_risk(returns, confidence_level)

 # CVaR = средняя доходность среди тех, что хуже VaR
 tail_returns = returns[returns <= var]

 if len(tail_returns) == 0:
 return 0.0

 cvar = tail_returns.mean()

 return float(cvar)

 def calculate_downside_deviation(self, returns: pd.Series, target_return: float = 0.0) -> float:
 """
 Расчет Downside Deviation.

 Downside Deviation измеряет волатильность только отрицательных доходностей
 относительно целевого уровня доходности. Это более точная мера риска,
 чем общая волатильность, так как учитывает только нежелательные отклонения.

 Args:
 returns (pd.Series): Серия доходностей
 target_return (float): Целевой уровень доходности

 Returns:
 float: Downside Deviation

 Example:
 >>> returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
 >>> risk_metrics = RiskMetrics()
 >>> dd = risk_metrics.calculate_downside_deviation(returns, 0.0)
 >>> print(f"Downside Deviation: {dd:.2%}")
 """
 if returns.empty:
 return 0.0

 # Только доходности ниже целевого уровня
 downside_returns = returns[returns < target_return]

 if len(downside_returns) == 0:
 return 0.0

 # Стандартное отклонение downside доходностей
 downside_deviation = downside_returns.std()

 return float(downside_deviation)

 def calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
 """
 Расчет коэффициента Шарпа.

 Коэффициент Шарпа показывает избыточную доходность on единицу риска.
 Это одна из самых важных метрик for оценки эффективности торговой стратегии.

 Args:
 returns (pd.Series): Серия доходностей
 risk_free_rate (float): Безрисковая ставка (годовая)

 Returns:
 float: Коэффициент Шарпа

 Example:
 >>> returns = pd.Series(np.random.normal(0.001, 0.02, 252))
 >>> risk_metrics = RiskMetrics()
 >>> sharpe = risk_metrics.calculate_sharpe_ratio(returns)
 >>> print(f"Коэффициент Шарпа: {sharpe:.2f}")
 """
 if returns.empty:
 return 0.0

 # Годовая доходность
 annual_return = returns.mean() * self.trading_days_per_year

 # Годовая волатильность
 annual_volatility = self.calculate_volatility(returns, annualized=True)

 if annual_volatility == 0:
 return 0.0

 # Коэффициент Шарпа = (доходность - безрисковая ставка) / волатильность
 sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility

 return float(sharpe_ratio)

 def calculate_sortino_ratio(self, returns: pd.Series, target_return: float = 0.0) -> float:
 """
 Расчет коэффициента Сортино.

 Коэффициент Сортино аналогичен коэффициенту Шарпа, но использует
 downside deviation вместо общей волатильности. Это более точная
 мера for оценки эффективности, так как учитывает только нежелательные риски.

 Args:
 returns (pd.Series): Серия доходностей
 target_return (float): Целевой уровень доходности

 Returns:
 float: Коэффициент Сортино
 """
 if returns.empty:
 return 0.0

 # Годовая доходность
 annual_return = returns.mean() * self.trading_days_per_year

 # Downside deviation
 downside_dev = self.calculate_downside_deviation(returns, target_return)

 if downside_dev == 0:
 return 0.0

 # Коэффициент Сортино = (доходность - целевая доходность) / downside deviation
 sortino_ratio = (annual_return - target_return) / downside_dev

 return float(sortino_ratio)

 def get_all_risk_metrics(self, returns: pd.Series, risk_free_rate: float = 0.02) -> Dict[str, float]:
 """
 Расчет всех метрик риска.

 Удобный метод for получения всех основных метрик риска in одном вызове.

 Args:
 returns (pd.Series): Серия доходностей
 risk_free_rate (float): Безрисковая ставка

 Returns:
 Dict[str, float]: Словарь with метриками риска
 """
 metrics = {
 'volatility': self.calculate_volatility(returns),
 'max_drawdown': self.calculate_max_drawdown(returns),
 'var_5pct': self.calculate_value_at_risk(returns, 0.05),
 'var_1pct': self.calculate_value_at_risk(returns, 0.01),
 'cvar_5pct': self.calculate_conditional_var(returns, 0.05),
 'cvar_1pct': self.calculate_conditional_var(returns, 0.01),
 'downside_deviation': self.calculate_downside_deviation(returns),
 'sharpe_ratio': self.calculate_sharpe_ratio(returns, risk_free_rate),
 'sortino_ratio': self.calculate_sortino_ratio(returns)
 }

 return metrics

# Практический example использования метрик риска
def example_risk_metrics():
 """
 Практический example использования метрик риска.

 Этот example показывает, как рассчитать различные метрики риска
 for торговой стратегии and интерпретировать результаты.
 """
 print("=== example использования метрик риска ===\n")

 # create тестовых данных with различными характеристиками риска
 np.random.seed(42)
 dates = pd.date_range('2023-01-01', periods=252, freq='D')

 # Симуляция доходностей with трендом and волатильностью
 trend = 0.0008 # 0.08% in день
 volatility = 0.025 # 2.5% волатильность
 returns = pd.Series(
 np.random.normal(trend, volatility, len(dates)),
 index=dates
 )

 # Добавляем несколько экстремальных событий for демонстрации
 extreme_days = [50, 100, 200]
 for day in extreme_days:
 returns.iloc[day] = -0.08 # -8% in день

 # create экземпляра класса
 risk_metrics = RiskMetrics()

 # Расчет всех метрик риска
 all_metrics = risk_metrics.get_all_risk_metrics(returns)

 # Вывод результатов
 print("Результаты анализа риска:")
 print("-" * 50)
 for metric, value in all_metrics.items():
 if 'ratio' in metric:
 print(f"{metric:20}: {value:8.2f}")
 else:
 print(f"{metric:20}: {value:8.2%}")

 # Интерпретация результатов
 print(f"\nИнтерпретация результатов:")
 print(f"Волатильность: {all_metrics['volatility']:.1%} - {'Высокая' if all_metrics['volatility'] > 0.2 else 'Умеренная' if all_metrics['volatility'] > 0.1 else 'Низкая'}")
 print(f"Максимальная просадка: {all_metrics['max_drawdown']:.1%} - {'Критическая' if all_metrics['max_drawdown'] < -0.2 else 'Высокая' if all_metrics['max_drawdown'] < -0.1 else 'Приемлемая'}")
 print(f"Коэффициент Шарпа: {all_metrics['sharpe_ratio']:.2f} - {'Отличный' if all_metrics['sharpe_ratio'] > 2 else 'Хороший' if all_metrics['sharpe_ratio'] > 1 else 'Слабый' if all_metrics['sharpe_ratio'] > 0 else 'Плохой'}")

 return all_metrics

# Launch примера
if __name__ == "__main__":
 example_risk_metrics()
```

### 3. Метрики эффективности

**Теория:** Метрики эффективности представляют собой комплексные показатели, которые измеряют эффективность торговой системы with учетом рисков. Эти метрики критически важны for понимания реальной эффективности системы, так как они учитывают not только доходность, но and связанные with ней риски.

**Почему метрики эффективности критически важны:**
- **Реальная оценка эффективности** - показывают истинную эффективность with учетом рисков
- **Сравнение стратегий** - позволяют объективно сравнивать различные торговые подходы
- **Оптимизация параметров** - помогают найти оптимальные settings системы
- **Управление рисками** - обеспечивают баланс между доходностью and риском
- **Принятие решений** - дают количественную основу for торговых решений

**Детальное объяснение основных метрик эффективности:**

1. **Коэффициент Шарпа (Sharpe Ratio)** - избыточная доходность on единицу общего риска
2. **Коэффициент Сортино (Sortino Ratio)** - избыточная доходность on единицу downside риска
3. **Коэффициент Калмара (Calmar Ratio)** - доходность относительно максимальной просадки
4. **Information Ratio** - избыточная доходность относительно tracking error
5. **Коэффициент Трейнора (Treynor Ratio)** - доходность относительно систематического риска

**Практическое применение:** Эти метрики используются for выбора лучших стратегий, оптимизации параметров and управления портфелем.

**Полный функциональный код with детальными объяснениями:**

```python
class EfficiencyMetrics:
 """
 Класс for расчета метрик эффективности торговой системы.

 Этот класс предоставляет методы for расчета различных показателей эффективности,
 которые учитывают как доходность, так and риски торговой стратегии.
 """

 def __init__(self, risk_free_rate: float = 0.02, trading_days_per_year: int = 252):
 """
 Инициализация класса метрик эффективности.

 Args:
 risk_free_rate (float): Безрисковая ставка (годовая)
 trading_days_per_year (int): Количество торговых дней in году
 """
 self.risk_free_rate = risk_free_rate
 self.trading_days_per_year = trading_days_per_year
 self.metrics = {}

 def calculate_sharpe_ratio(self, returns: pd.Series) -> float:
 """
 Расчет коэффициента Шарпа.

 Коэффициент Шарпа показывает избыточную доходность on единицу общего риска.
 Это одна из самых важных метрик for оценки эффективности торговой стратегии.

 Формула: (E[R] - Rf) / σ(R)
 где E[R] - ожидаемая доходность, Rf - безрисковая ставка, σ(R) - волатильность

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Коэффициент Шарпа

 Example:
 >>> returns = pd.Series(np.random.normal(0.001, 0.02, 252))
 >>> eff_metrics = EfficiencyMetrics()
 >>> sharpe = eff_metrics.calculate_sharpe_ratio(returns)
 >>> print(f"Коэффициент Шарпа: {sharpe:.2f}")
 """
 if returns.empty:
 return 0.0

 # Годовая доходность
 annual_return = returns.mean() * self.trading_days_per_year

 # Годовая волатильность
 annual_volatility = returns.std() * np.sqrt(self.trading_days_per_year)

 if annual_volatility == 0:
 return 0.0

 # Коэффициент Шарпа
 sharpe_ratio = (annual_return - self.risk_free_rate) / annual_volatility

 return float(sharpe_ratio)

 def calculate_sortino_ratio(self, returns: pd.Series, target_return: float = 0.0) -> float:
 """
 Расчет коэффициента Сортино.

 Коэффициент Сортино аналогичен коэффициенту Шарпа, но использует
 downside deviation вместо общей волатильности. Это более точная
 мера for оценки эффективности, так как учитывает только нежелательные риски.

 Формула: (E[R] - T) / σ_down(R)
 где T - целевая доходность, σ_down(R) - downside deviation

 Args:
 returns (pd.Series): Серия доходностей
 target_return (float): Целевой уровень доходности

 Returns:
 float: Коэффициент Сортино
 """
 if returns.empty:
 return 0.0

 # Годовая доходность
 annual_return = returns.mean() * self.trading_days_per_year

 # Downside deviation
 downside_returns = returns[returns < target_return]
 if len(downside_returns) == 0:
 return np.inf if annual_return > target_return else 0.0

 downside_deviation = downside_returns.std() * np.sqrt(self.trading_days_per_year)

 if downside_deviation == 0:
 return 0.0

 # Коэффициент Сортино
 sortino_ratio = (annual_return - target_return) / downside_deviation

 return float(sortino_ratio)

 def calculate_calmar_ratio(self, returns: pd.Series) -> float:
 """
 Расчет коэффициента Калмара.

 Коэффициент Калмара показывает отношение годовой доходности к максимальной просадке.
 Это важная метрика for оценки способности системы восстанавливаться после потерь.

 Формула: Annual Return / |Max Drawdown|

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Коэффициент Калмара
 """
 if returns.empty:
 return 0.0

 # Годовая доходность
 annual_return = returns.mean() * self.trading_days_per_year

 # Максимальная просадка
 cumulative_returns = (1 + returns).cumprod()
 running_max = cumulative_returns.expanding().max()
 drawdown = (cumulative_returns - running_max) / running_max
 max_drawdown = abs(drawdown.min())

 if max_drawdown == 0:
 return np.inf if annual_return > 0 else 0.0

 # Коэффициент Калмара
 calmar_ratio = annual_return / max_drawdown

 return float(calmar_ratio)

 def calculate_information_ratio(self, returns: pd.Series, benchmark_returns: pd.Series) -> float:
 """
 Расчет Information Ratio.

 Information Ratio показывает избыточную доходность относительно tracking error.
 Это важная метрика for оценки эффективности активного управления.

 Формула: (E[R] - E[Rb]) / σ(R - Rb)
 где Rb - доходность бенчмарка

 Args:
 returns (pd.Series): Серия доходностей стратегии
 benchmark_returns (pd.Series): Серия доходностей бенчмарка

 Returns:
 float: Information Ratio
 """
 if returns.empty or benchmark_returns.empty:
 return 0.0

 # Выравниваем индексы
 common_index = returns.index.intersection(benchmark_returns.index)
 if len(common_index) == 0:
 return 0.0

 returns_aligned = returns.loc[common_index]
 benchmark_aligned = benchmark_returns.loc[common_index]

 # Избыточные доходности
 excess_returns = returns_aligned - benchmark_aligned

 # Tracking error
 tracking_error = excess_returns.std() * np.sqrt(self.trading_days_per_year)

 if tracking_error == 0:
 return 0.0

 # Information Ratio
 information_ratio = excess_returns.mean() * self.trading_days_per_year / tracking_error

 return float(information_ratio)

 def calculate_treynor_ratio(self, returns: pd.Series, market_returns: pd.Series) -> float:
 """
 Расчет коэффициента Трейнора.

 Коэффициент Трейнора показывает доходность относительно систематического риска (beta).
 Это важная метрика for оценки эффективности in контексте рыночного риска.

 Формула: (E[R] - Rf) / β
 где β - бета стратегии относительно рынка

 Args:
 returns (pd.Series): Серия доходностей стратегии
 market_returns (pd.Series): Серия доходностей рынка

 Returns:
 float: Коэффициент Трейнора
 """
 if returns.empty or market_returns.empty:
 return 0.0

 # Выравниваем индексы
 common_index = returns.index.intersection(market_returns.index)
 if len(common_index) < 2:
 return 0.0

 returns_aligned = returns.loc[common_index]
 market_aligned = market_returns.loc[common_index]

 # Расчет беты
 covariance = np.cov(returns_aligned, market_aligned)[0, 1]
 market_variance = np.var(market_aligned)

 if market_variance == 0:
 return 0.0

 beta = covariance / market_variance

 if beta == 0:
 return 0.0

 # Годовая доходность
 annual_return = returns_aligned.mean() * self.trading_days_per_year

 # Коэффициент Трейнора
 treynor_ratio = (annual_return - self.risk_free_rate) / beta

 return float(treynor_ratio)

 def calculate_omega_ratio(self, returns: pd.Series, threshold: float = 0.0) -> float:
 """
 Расчет Omega Ratio.

 Omega Ratio показывает отношение прибыли к убыткам относительно заданного порога.
 Это более полная мера эффективности, чем коэффициент Шарпа.

 Формула: ∫[threshold to ∞] (1 - F(x)) dx / ∫[-∞ to threshold] F(x) dx

 Args:
 returns (pd.Series): Серия доходностей
 threshold (float): Пороговый уровень доходности

 Returns:
 float: Omega Ratio
 """
 if returns.empty:
 return 0.0

 # Прибыли and убытки относительно порога
 gains = returns[returns > threshold] - threshold
 losses = threshold - returns[returns < threshold]

 if len(losses) == 0:
 return np.inf if len(gains) > 0 else 0.0

 # Omega Ratio
 omega_ratio = gains.sum() / losses.sum()

 return float(omega_ratio)

 def get_all_efficiency_metrics(self, returns: pd.Series,
 benchmark_returns: Optional[pd.Series] = None,
 market_returns: Optional[pd.Series] = None) -> Dict[str, float]:
 """
 Расчет всех метрик эффективности.

 Удобный метод for получения всех основных метрик эффективности in одном вызове.

 Args:
 returns (pd.Series): Серия доходностей стратегии
 benchmark_returns (pd.Series, optional): Доходности бенчмарка
 market_returns (pd.Series, optional): Доходности рынка

 Returns:
 Dict[str, float]: Словарь with метриками эффективности
 """
 metrics = {
 'sharpe_ratio': self.calculate_sharpe_ratio(returns),
 'sortino_ratio': self.calculate_sortino_ratio(returns),
 'calmar_ratio': self.calculate_calmar_ratio(returns),
 'omega_ratio': self.calculate_omega_ratio(returns)
 }

 if benchmark_returns is not None:
 metrics['information_ratio'] = self.calculate_information_ratio(returns, benchmark_returns)

 if market_returns is not None:
 metrics['treynor_ratio'] = self.calculate_treynor_ratio(returns, market_returns)

 return metrics

# Практический example использования метрик эффективности
def example_efficiency_metrics():
 """
 Практический example использования метрик эффективности.

 Этот example показывает, как рассчитать различные метрики эффективности
 and сравнить две торговые стратегии.
 """
 print("=== example использования метрик эффективности ===\n")

 # create тестовых данных for двух стратегий
 np.random.seed(42)
 dates = pd.date_range('2023-01-01', periods=252, freq='D')

 # Стратегия 1: Высокая доходность, высокая волатильность
 strategy1_returns = pd.Series(
 np.random.normal(0.0015, 0.03, len(dates)),
 index=dates
 )

 # Стратегия 2: Умеренная доходность, низкая волатильность
 strategy2_returns = pd.Series(
 np.random.normal(0.0008, 0.015, len(dates)),
 index=dates
 )

 # Бенчмарк (рыночный индекс)
 benchmark_returns = pd.Series(
 np.random.normal(0.0005, 0.02, len(dates)),
 index=dates
 )

 # create экземпляра класса
 eff_metrics = EfficiencyMetrics()

 # Расчет метрик for обеих стратегий
 strategy1_metrics = eff_metrics.get_all_efficiency_metrics(
 strategy1_returns, benchmark_returns, benchmark_returns
 )
 strategy2_metrics = eff_metrics.get_all_efficiency_metrics(
 strategy2_returns, benchmark_returns, benchmark_returns
 )

 # Вывод результатов
 print("Сравнение метрик эффективности:")
 print("-" * 60)
 print(f"{'Метрика':<20} {'Стратегия 1':<15} {'Стратегия 2':<15}")
 print("-" * 60)

 for metric in strategy1_metrics.keys():
 val1 = strategy1_metrics[metric]
 val2 = strategy2_metrics[metric]
 print(f"{metric:<20} {val1:<15.3f} {val2:<15.3f}")

 # Определение лучшей стратегии
 print(f"\nАнализ результатов:")
 if strategy1_metrics['sharpe_ratio'] > strategy2_metrics['sharpe_ratio']:
 print("Стратегия 1 имеет лучший коэффициент Шарпа")
 else:
 print("Стратегия 2 имеет лучший коэффициент Шарпа")

 if strategy1_metrics['calmar_ratio'] > strategy2_metrics['calmar_ratio']:
 print("Стратегия 1 имеет лучший коэффициент Калмара")
 else:
 print("Стратегия 2 имеет лучший коэффициент Калмара")

 return strategy1_metrics, strategy2_metrics

# Launch примера
if __name__ == "__main__":
 example_efficiency_metrics()
```

## Продвинутые метрики

**Теория:** Продвинутые метрики представляют собой сложные показатели, которые обеспечивают глубокое понимание производительности торговой системы. Эти метрики выходят за рамки базовых показателей доходности and риска, предоставляя детальную информацию о стабильности, адаптивности and предсказательной способности системы.

**Почему продвинутые метрики критически важны:**
- **Глубокое понимание производительности** - выявление скрытых паттернов and характеристик
- **Детальный анализ системы** - понимание внутренних механизмов работы стратегии
- **Оптимизация параметров** - точная configuration системы for максимальной эффективности
- **Prediction будущей производительности** - оценка устойчивости стратегии во времени
- **Управление рисками** - выявление потенциальных проблем to их возникновения

### 1. Метрики стабильности

**Теория:** Метрики стабильности представляют собой показатели, которые измеряют стабильность and предсказуемость производительности торговой системы. in алгоритмической торговле стабильность критически важна for долгосрочного успеха, так как нестабильные системы могут показывать отличные результаты in краткосрочной перспективе, но терпеть неудачу in долгосрочной.

**Почему метрики стабильности критически важны:**
- **Надежность системы** - оценка способности системы поддерживать производительность
- **Предсказуемость результатов** - понимание того, насколько стабильны результаты
- **Управление рисками** - выявление periods нестабильности
- **Planирование инвестиций** - принятие решений о размере капитала
- **Оптимизация стратегии** - выявление параметров, влияющих on стабильность

**Детальное объяснение метрик стабильности:**

1. **Коэффициент консистентности** - доля положительных periods
2. **Коэффициент стабильности** - обратная величина коэффициента вариации
3. **Соотношение выигрышей к проигрышам** - средний выигрыш к среднему проигрышу
4. **Profit Factor** - отношение общей прибыли к общим убыткам

**Полный функциональный код with детальными объяснениями:**

```python
class StabilityMetrics:
 """
 Класс for расчета метрик стабильности торговой системы.

 Этот класс предоставляет методы for оценки стабильности and предсказуемости
 производительности торговой стратегии.
 """

 def __init__(self):
 """Инициализация класса метрик стабильности."""
 self.metrics = {}

 def calculate_consistency_ratio(self, returns: pd.Series) -> float:
 """
 Расчет коэффициента консистентности.

 Коэффициент консистентности показывает долю положительных periods
 from общего количества periods. Высокий коэффициент означает
 стабильную положительную производительность.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Коэффициент консистентности (0-1)

 Example:
 >>> returns = pd.Series([0.01, -0.02, 0.03, 0.01, -0.01])
 >>> stability = StabilityMetrics()
 >>> consistency = stability.calculate_consistency_ratio(returns)
 >>> print(f"Консистентность: {consistency:.2%}")
 """
 if returns.empty:
 return 0.0

 positive_returns = (returns > 0).sum()
 total_returns = len(returns)
 consistency_ratio = positive_returns / total_returns

 return float(consistency_ratio)

 def calculate_stability_ratio(self, returns: pd.Series) -> float:
 """
 Расчет коэффициента стабильности.

 Коэффициент стабильности основан on обратной величине коэффициента вариации.
 Высокий коэффициент означает низкую волатильность относительно средней доходности.

 Формула: 1 - (σ / |μ|)
 где σ - стандартное отклонение, μ - средняя доходность

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Коэффициент стабильности (0-1)
 """
 if returns.empty:
 return 0.0

 mean_return = returns.mean()
 std_return = returns.std()

 if mean_return == 0:
 return 0.0

 coefficient_of_variation = std_return / abs(mean_return)
 stability_ratio = max(0, 1 - coefficient_of_variation)

 return float(stability_ratio)

 def calculate_win_loss_ratio(self, returns: pd.Series) -> float:
 """
 Расчет соотношения выигрышей к проигрышам.

 Win/Loss Ratio показывает отношение среднего выигрыша к среднему проигрышу.
 Высокий коэффициент означает, что выигрыши значительно превышают проигрыши.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Соотношение выигрышей к проигрышам
 """
 if returns.empty:
 return 0.0

 winning_returns = returns[returns > 0]
 losing_returns = returns[returns < 0]

 if len(losing_returns) == 0:
 return np.inf if len(winning_returns) > 0 else 0.0

 avg_win = winning_returns.mean() if len(winning_returns) > 0 else 0.0
 avg_loss = abs(losing_returns.mean())

 win_loss_ratio = avg_win / avg_loss

 return float(win_loss_ratio)

 def calculate_profit_factor(self, returns: pd.Series) -> float:
 """
 Расчет Profit Factor.

 Profit Factor показывает отношение общей прибыли к общим убыткам.
 Значение больше 1 означает прибыльность, больше 2 - хорошую прибыльность.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Profit Factor
 """
 if returns.empty:
 return 0.0

 gross_profit = returns[returns > 0].sum()
 gross_loss = abs(returns[returns < 0].sum())

 if gross_loss == 0:
 return np.inf if gross_profit > 0 else 0.0

 profit_factor = gross_profit / gross_loss

 return float(profit_factor)

 def calculate_recovery_factor(self, returns: pd.Series) -> float:
 """
 Расчет Recovery Factor.

 Recovery Factor показывает отношение общей прибыли к максимальной просадке.
 Высокий коэффициент означает способность быстро восстанавливаться после потерь.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Recovery Factor
 """
 if returns.empty:
 return 0.0

 # Общая прибыль
 total_profit = returns[returns > 0].sum()

 # Максимальная просадка
 cumulative_returns = (1 + returns).cumprod()
 running_max = cumulative_returns.expanding().max()
 drawdown = (cumulative_returns - running_max) / running_max
 max_drawdown = abs(drawdown.min())

 if max_drawdown == 0:
 return np.inf if total_profit > 0 else 0.0

 recovery_factor = total_profit / max_drawdown

 return float(recovery_factor)

 def get_all_stability_metrics(self, returns: pd.Series) -> Dict[str, float]:
 """
 Расчет всех метрик стабильности.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 Dict[str, float]: Словарь with метриками стабильности
 """
 metrics = {
 'consistency_ratio': self.calculate_consistency_ratio(returns),
 'stability_ratio': self.calculate_stability_ratio(returns),
 'win_loss_ratio': self.calculate_win_loss_ratio(returns),
 'profit_factor': self.calculate_profit_factor(returns),
 'recovery_factor': self.calculate_recovery_factor(returns)
 }

 return metrics

# Практический example использования метрик стабильности
def example_stability_metrics():
 """
 Практический example использования метрик стабильности.
 """
 print("=== example использования метрик стабильности ===\n")

 # create тестовых данных
 np.random.seed(42)
 dates = pd.date_range('2023-01-01', periods=252, freq='D')

 # Стабильная стратегия
 stable_returns = pd.Series(
 np.random.normal(0.0005, 0.01, len(dates)),
 index=dates
 )

 # Нестабильная стратегия
 unstable_returns = pd.Series(
 np.random.normal(0.001, 0.05, len(dates)),
 index=dates
 )

 # create экземпляра класса
 stability = StabilityMetrics()

 # Расчет метрик for обеих стратегий
 stable_metrics = stability.get_all_stability_metrics(stable_returns)
 unstable_metrics = stability.get_all_stability_metrics(unstable_returns)

 # Вывод результатов
 print("Сравнение метрик стабильности:")
 print("-" * 50)
 print(f"{'Метрика':<20} {'Стабильная':<12} {'Нестабильная':<12}")
 print("-" * 50)

 for metric in stable_metrics.keys():
 val1 = stable_metrics[metric]
 val2 = unstable_metrics[metric]
 print(f"{metric:<20} {val1:<12.3f} {val2:<12.3f}")

 return stable_metrics, unstable_metrics

# Launch примера
if __name__ == "__main__":
 example_stability_metrics()
```

### 2. Метрики адаптивности

**Теория:** Метрики адаптивности представляют собой показатели, которые измеряют способность торговой системы адаптироваться к изменениям рыночных условий. in динамичной среде финансовых рынков способность к адаптации критически важна for долгосрочного успеха.

**Почему метрики адаптивности критически важны:**
- **Долгосрочная эффективность** - оценка способности системы работать in различных рыночных условиях
- **Устойчивость к изменениям** - понимание того, как система реагирует on смену режимов
- **Способность к адаптации** - измерение гибкости стратегии
- **Planирование развития** - выявление необходимости модификации системы
- **Управление рисками** - Prediction periods нестабильности

**Детальное объяснение метрик адаптивности:**

1. **Скорость адаптации** - скорость изменения параметров системы
2. **Стабильность режимов** - устойчивость к смене рыночных режимов
3. **Стабильность корреляции** - постоянство связи with рыночными индексами
4. **Коэффициент адаптивности** - общая мера способности к адаптации

**Полный функциональный код with детальными объяснениями:**

```python
class AdaptabilityMetrics:
 """
 Класс for расчета метрик адаптивности торговой системы.

 Этот класс предоставляет методы for оценки способности системы
 адаптироваться к изменениям рыночных условий.
 """

 def __init__(self, window_size: int = 252):
 """
 Инициализация класса метрик адаптивности.

 Args:
 window_size (int): Размер окна for скользящих расчетов
 """
 self.window_size = window_size
 self.metrics = {}

 def calculate_adaptation_speed(self, returns: pd.Series, window: int = None) -> float:
 """
 Расчет скорости адаптации системы.

 Скорость адаптации измеряет, насколько быстро система изменяет
 свои parameters in ответ on изменения рыночных условий.

 Args:
 returns (pd.Series): Серия доходностей
 window (int, optional): Размер окна for расчета

 Returns:
 float: Скорость адаптации
 """
 if returns.empty or len(returns) < 2:
 return 0.0

 window = window or self.window_size
 if len(returns) < window:
 window = len(returns) // 2

 # Скользящие метрики
 rolling_returns = returns.rolling(window, min_periods=window//2)
 rolling_mean = rolling_returns.mean()
 rolling_std = rolling_returns.std()

 # Изменения метрик
 mean_changes = rolling_mean.diff().abs()
 std_changes = rolling_std.diff().abs()

 # Скорость адаптации (среднее изменение параметров)
 adaptation_speed = np.nanmean(mean_changes) + np.nanmean(std_changes)

 return float(adaptation_speed)

 def calculate_regime_stability(self, returns: pd.Series, n_regimes: int = 3) -> float:
 """
 Расчет стабильности рыночных режимов.

 Стабильность режимов показывает, насколько часто система
 переключается между различными рыночными режимами.

 Args:
 returns (pd.Series): Серия доходностей
 n_regimes (int): Количество режимов for кластеризации

 Returns:
 float: Стабильность режимов (0-1)
 """
 if returns.empty or len(returns) < n_regimes * 2:
 return 0.0

 try:
 # Подготовка данных for кластеризации
 returns_reshaped = returns.values.reshape(-1, 1)

 # Кластеризация режимов
 kmeans = KMeans(n_clusters=n_regimes, random_state=42, n_init=10)
 regime_labels = kmeans.fit_predict(returns_reshaped)

 # Расчет стабильности режимов
 regime_changes = np.sum(np.diff(regime_labels) != 0)
 regime_stability = 1 - (regime_changes / (len(returns) - 1))

 return float(max(0, regime_stability))

 except Exception:
 return 0.0

 def calculate_market_correlation_stability(self, returns: pd.Series,
 market_returns: pd.Series) -> float:
 """
 Расчет стабильности корреляции with рынком.

 Стабильность корреляции показывает, насколько постоянна
 связь между системой and рыночным индексом.

 Args:
 returns (pd.Series): Серия доходностей системы
 market_returns (pd.Series): Серия доходностей рынка

 Returns:
 float: Стабильность корреляции (0-1)
 """
 if returns.empty or market_returns.empty:
 return 0.0

 # Выравниваем индексы
 common_index = returns.index.intersection(market_returns.index)
 if len(common_index) < self.window_size:
 return 0.0

 returns_aligned = returns.loc[common_index]
 market_aligned = market_returns.loc[common_index]

 # Скользящая корреляция
 rolling_correlation = returns_aligned.rolling(self.window_size).corr(market_aligned)

 # Стабильность корреляции (обратная величина стандартного отклонения)
 correlation_std = rolling_correlation.std()
 correlation_stability = max(0, 1 - correlation_std)

 return float(correlation_stability)

 def calculate_volatility_regime_adaptation(self, returns: pd.Series) -> float:
 """
 Расчет адаптации к изменениям волатильности.

 Этот показатель измеряет, насколько хорошо система
 адаптируется к изменениям волатильности рынка.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Коэффициент адаптации к волатильности
 """
 if returns.empty or len(returns) < self.window_size:
 return 0.0

 # Скользящая волатильность
 rolling_vol = returns.rolling(self.window_size).std()

 # Изменения волатильности
 vol_changes = rolling_vol.diff().abs()

 # Адаптация = обратная величина изменений волатильности
 adaptation = 1 / (1 + vol_changes.mean()) if vol_changes.mean() > 0 else 1.0

 return float(adaptation)

 def calculate_trend_adaptation(self, returns: pd.Series) -> float:
 """
 Расчет адаптации к трендовым изменениям.

 Этот показатель измеряет способность системы
 адаптироваться к изменениям тренда.

 Args:
 returns (pd.Series): Серия доходностей

 Returns:
 float: Коэффициент адаптации к тренду
 """
 if returns.empty or len(returns) < self.window_size:
 return 0.0

 # Скользящий тренд
 rolling_trend = returns.rolling(self.window_size).mean()

 # Изменения тренда
 trend_changes = rolling_trend.diff().abs()

 # Адаптация = обратная величина изменений тренда
 adaptation = 1 / (1 + trend_changes.mean()) if trend_changes.mean() > 0 else 1.0

 return float(adaptation)

 def get_all_adaptability_metrics(self, returns: pd.Series,
 market_returns: Optional[pd.Series] = None) -> Dict[str, float]:
 """
 Расчет всех метрик адаптивности.

 Args:
 returns (pd.Series): Серия доходностей системы
 market_returns (pd.Series, optional): Серия доходностей рынка

 Returns:
 Dict[str, float]: Словарь with метриками адаптивности
 """
 metrics = {
 'adaptation_speed': self.calculate_adaptation_speed(returns),
 'regime_stability': self.calculate_regime_stability(returns),
 'volatility_adaptation': self.calculate_volatility_regime_adaptation(returns),
 'trend_adaptation': self.calculate_trend_adaptation(returns)
 }

 if market_returns is not None:
 metrics['correlation_stability'] = self.calculate_market_correlation_stability(
 returns, market_returns
 )

 return metrics

# Практический example использования метрик адаптивности
def example_adaptability_metrics():
 """
 Практический example использования метрик адаптивности.
 """
 print("=== example использования метрик адаптивности ===\n")

 # create тестовых данных with различными режимами
 np.random.seed(42)
 dates = pd.date_range('2023-01-01', periods=500, freq='D')

 # Симуляция различных рыночных режимов
 returns = []
 market_returns = []

 # Режим 1: Стабильный рост
 for i in range(100):
 returns.append(np.random.normal(0.001, 0.01))
 market_returns.append(np.random.normal(0.0005, 0.008))

 # Режим 2: Высокая волатильность
 for i in range(100):
 returns.append(np.random.normal(0.0005, 0.03))
 market_returns.append(np.random.normal(0.0002, 0.025))

 # Режим 3: Нисходящий тренд
 for i in range(100):
 returns.append(np.random.normal(-0.0005, 0.015))
 market_returns.append(np.random.normal(-0.0008, 0.012))

 # Режим 4: Восстановление
 for i in range(200):
 returns.append(np.random.normal(0.0008, 0.02))
 market_returns.append(np.random.normal(0.0006, 0.018))

 returns_series = pd.Series(returns, index=dates)
 market_series = pd.Series(market_returns, index=dates)

 # create экземпляра класса
 adaptability = AdaptabilityMetrics()

 # Расчет всех метрик адаптивности
 all_metrics = adaptability.get_all_adaptability_metrics(returns_series, market_series)

 # Вывод результатов
 print("Результаты анализа адаптивности:")
 print("-" * 40)
 for metric, value in all_metrics.items():
 print(f"{metric:25}: {value:8.3f}")

 # Интерпретация результатов
 print(f"\nИнтерпретация результатов:")
 print(f"Скорость адаптации: {all_metrics['adaptation_speed']:.3f} - {'Высокая' if all_metrics['adaptation_speed'] > 0.01 else 'Умеренная' if all_metrics['adaptation_speed'] > 0.005 else 'Низкая'}")
 print(f"Стабильность режимов: {all_metrics['regime_stability']:.3f} - {'Высокая' if all_metrics['regime_stability'] > 0.8 else 'Умеренная' if all_metrics['regime_stability'] > 0.6 else 'Низкая'}")

 return all_metrics

# Launch примера
if __name__ == "__main__":
 example_adaptability_metrics()
```

### 3. Метрики предсказательной способности

**Теория:** Метрики предсказательной способности представляют собой показатели, которые измеряют качество and точность прогнозов ML-модели. in алгоритмической торговле способность точно предсказывать будущие движения цен критически важна for успеха стратегии.

**Почему метрики предсказательной способности критически важны:**
- **Качество модели** - оценка того, насколько хорошо модель предсказывает будущее
- **Валидация стратегии** - check эффективности торговых сигналов
- **Оптимизация параметров** - configuration модели for максимальной точности
- **Сравнение подходов** - выбор лучших алгоритмов and методов
- **Управление рисками** - понимание надежности прогнозов

**Детальное объяснение метрик предсказательной способности:**

1. **Точность predictions** - доля правильных predictions
2. **Точность направления** - способность предсказывать направление движения
3. **Точность величины** - способность предсказывать размер изменений
4. **Навык прогнозирования** - improve относительно простых бенчмарков

**Полный функциональный код with детальными объяснениями:**

```python
class PredictiveMetrics:
 """
 Класс for расчета метрик предсказательной способности ML-модели.

 Этот класс предоставляет методы for оценки качества прогнозов
 торговой системы and ML-моделей.
 """

 def __init__(self):
 """Инициализация класса метрик предсказательной способности."""
 self.metrics = {}

 def calculate_Prediction_accuracy(self, Predictions: np.ndarray,
 actual: np.ndarray) -> float:
 """
 Расчет точности predictions.

 Точность predictions показывает долю правильных predictions
 from общего количества predictions.

 Args:
 Predictions (np.ndarray): Предсказанные значения
 actual (np.ndarray): Фактические значения

 Returns:
 float: Точность predictions (0-1)
 """
 if len(Predictions) != len(actual):
 raise ValueError("Длины массивов Predictions and actual должны совпадать")

 if len(Predictions) == 0:
 return 0.0

 accuracy = np.mean(Predictions == actual)
 return float(accuracy)

 def calculate_directional_accuracy(self, predicted_returns: pd.Series,
 actual_returns: pd.Series) -> float:
 """
 Расчет точности направления движения.

 Точность направления показывает, насколько часто модель
 правильно предсказывает направление изменения цены.

 Args:
 predicted_returns (pd.Series): Предсказанные доходности
 actual_returns (pd.Series): Фактические доходности

 Returns:
 float: Точность направления (0-1)
 """
 if predicted_returns.empty or actual_returns.empty:
 return 0.0

 # Выравниваем индексы
 common_index = predicted_returns.index.intersection(actual_returns.index)
 if len(common_index) == 0:
 return 0.0

 pred_aligned = predicted_returns.loc[common_index]
 actual_aligned = actual_returns.loc[common_index]

 # Направления движения
 predicted_direction = np.sign(pred_aligned)
 actual_direction = np.sign(actual_aligned)

 # Точность направления
 directional_accuracy = np.mean(predicted_direction == actual_direction)

 return float(directional_accuracy)

 def calculate_magnitude_accuracy(self, predicted_returns: pd.Series,
 actual_returns: pd.Series,
 tolerance: float = 0.1) -> float:
 """
 Расчет точности величины изменений.

 Точность величины показывает, насколько точно модель
 предсказывает размер изменений in пределах заданной толерантности.

 Args:
 predicted_returns (pd.Series): Предсказанные доходности
 actual_returns (pd.Series): Фактические доходности
 tolerance (float): Допустимая относительная ошибка

 Returns:
 float: Точность величины (0-1)
 """
 if predicted_returns.empty or actual_returns.empty:
 return 0.0

 # Выравниваем индексы
 common_index = predicted_returns.index.intersection(actual_returns.index)
 if len(common_index) == 0:
 return 0.0

 pred_aligned = predicted_returns.loc[common_index]
 actual_aligned = actual_returns.loc[common_index]

 # Исключаем нулевые значения
 mask = actual_aligned != 0
 if mask.sum() == 0:
 return 0.0

 pred_filtered = pred_aligned[mask]
 actual_filtered = actual_aligned[mask]

 # Относительная ошибка
 relative_error = np.abs(pred_filtered - actual_filtered) / np.abs(actual_filtered)

 # Точность величины
 magnitude_accuracy = np.mean(relative_error <= tolerance)

 return float(magnitude_accuracy)

 def calculate_forecast_skill(self, predicted_returns: pd.Series,
 actual_returns: pd.Series,
 benchmark_returns: pd.Series) -> float:
 """
 Расчет навыка прогнозирования.

 Навык прогнозирования показывает, насколько модель
 превосходит простой бенчмарк (например, среднее значение).

 Args:
 predicted_returns (pd.Series): Предсказанные доходности
 actual_returns (pd.Series): Фактические доходности
 benchmark_returns (pd.Series): Бенчмарк доходности

 Returns:
 float: Навык прогнозирования
 """
 if (predicted_returns.empty or actual_returns.empty or
 benchmark_returns.empty):
 return 0.0

 # Выравниваем индексы
 common_index = (predicted_returns.index
 .intersection(actual_returns.index)
 .intersection(benchmark_returns.index))

 if len(common_index) == 0:
 return 0.0

 pred_aligned = predicted_returns.loc[common_index]
 actual_aligned = actual_returns.loc[common_index]
 benchmark_aligned = benchmark_returns.loc[common_index]

 # MSE модели
 model_mse = np.mean((pred_aligned - actual_aligned) ** 2)

 # MSE бенчмарка
 benchmark_mse = np.mean((benchmark_aligned - actual_aligned) ** 2)

 if benchmark_mse == 0:
 return 0.0

 # Навык прогнозирования
 forecast_skill = 1 - (model_mse / benchmark_mse)

 return float(forecast_skill)

 def calculate_information_coefficient(self, predicted_returns: pd.Series,
 actual_returns: pd.Series) -> float:
 """
 Расчет информационного коэффициента.

 Информационный коэффициент показывает корреляцию между
 предсказаниями and фактическими результатами.

 Args:
 predicted_returns (pd.Series): Предсказанные доходности
 actual_returns (pd.Series): Фактические доходности

 Returns:
 float: Информационный коэффициент
 """
 if predicted_returns.empty or actual_returns.empty:
 return 0.0

 # Выравниваем индексы
 common_index = predicted_returns.index.intersection(actual_returns.index)
 if len(common_index) < 2:
 return 0.0

 pred_aligned = predicted_returns.loc[common_index]
 actual_aligned = actual_returns.loc[common_index]

 # Корреляция
 correlation = np.corrcoef(pred_aligned, actual_aligned)[0, 1]

 return float(correlation) if not np.isnan(correlation) else 0.0

 def calculate_hit_rate(self, predicted_returns: pd.Series,
 actual_returns: pd.Series) -> float:
 """
 Расчет коэффициента попаданий.

 Коэффициент попаданий показывает долю случаев, когда
 Prediction and фактический результат имеют одинаковый знак.

 Args:
 predicted_returns (pd.Series): Предсказанные доходности
 actual_returns (pd.Series): Фактические доходности

 Returns:
 float: Коэффициент попаданий (0-1)
 """
 if predicted_returns.empty or actual_returns.empty:
 return 0.0

 # Выравниваем индексы
 common_index = predicted_returns.index.intersection(actual_returns.index)
 if len(common_index) == 0:
 return 0.0

 pred_aligned = predicted_returns.loc[common_index]
 actual_aligned = actual_returns.loc[common_index]

 # Попадания (одинаковый знак)
 hits = (pred_aligned * actual_aligned) > 0
 hit_rate = hits.mean()

 return float(hit_rate)

 def get_all_predictive_metrics(self, predicted_returns: pd.Series,
 actual_returns: pd.Series,
 benchmark_returns: Optional[pd.Series] = None) -> Dict[str, float]:
 """
 Расчет всех метрик предсказательной способности.

 Args:
 predicted_returns (pd.Series): Предсказанные доходности
 actual_returns (pd.Series): Фактические доходности
 benchmark_returns (pd.Series, optional): Бенчмарк доходности

 Returns:
 Dict[str, float]: Словарь with метриками предсказательной способности
 """
 metrics = {
 'directional_accuracy': self.calculate_directional_accuracy(
 predicted_returns, actual_returns
 ),
 'magnitude_accuracy': self.calculate_magnitude_accuracy(
 predicted_returns, actual_returns
 ),
 'information_coefficient': self.calculate_information_coefficient(
 predicted_returns, actual_returns
 ),
 'hit_rate': self.calculate_hit_rate(
 predicted_returns, actual_returns
 )
 }

 if benchmark_returns is not None:
 metrics['forecast_skill'] = self.calculate_forecast_skill(
 predicted_returns, actual_returns, benchmark_returns
 )

 return metrics

# Практический example использования метрик предсказательной способности
def example_predictive_metrics():
 """
 Практический example использования метрик предсказательной способности.
 """
 print("=== example использования метрик предсказательной способности ===\n")

 # create тестовых данных
 np.random.seed(42)
 dates = pd.date_range('2023-01-01', periods=252, freq='D')

 # Фактические доходности
 actual_returns = pd.Series(
 np.random.normal(0.0005, 0.02, len(dates)),
 index=dates
 )

 # Предсказанные доходности (with некоторой точностью)
 predicted_returns = actual_returns + np.random.normal(0, 0.01, len(dates))
 predicted_returns = pd.Series(predicted_returns, index=dates)

 # Бенчмарк (простое среднее)
 benchmark_returns = pd.Series(
 [actual_returns.mean()] * len(dates),
 index=dates
 )

 # create экземпляра класса
 predictive = PredictiveMetrics()

 # Расчет всех метрик
 all_metrics = predictive.get_all_predictive_metrics(
 predicted_returns, actual_returns, benchmark_returns
 )

 # Вывод результатов
 print("Результаты анализа предсказательной способности:")
 print("-" * 50)
 for metric, value in all_metrics.items():
 print(f"{metric:25}: {value:8.3f}")

 # Интерпретация результатов
 print(f"\nИнтерпретация результатов:")
 print(f"Точность направления: {all_metrics['directional_accuracy']:.1%} - {'Отличная' if all_metrics['directional_accuracy'] > 0.7 else 'Хорошая' if all_metrics['directional_accuracy'] > 0.6 else 'Слабая'}")
 print(f"Информационный коэффициент: {all_metrics['information_coefficient']:.3f} - {'Высокий' if all_metrics['information_coefficient'] > 0.1 else 'Умеренный' if all_metrics['information_coefficient'] > 0.05 else 'Низкий'}")

 return all_metrics

# Launch примера
if __name__ == "__main__":
 example_predictive_metrics()
```

## Временные метрики

**Теория:** Временные метрики представляют собой показатели, которые учитывают временные аспекты производительности системы. Это критически важно for понимания динамики производительности.

**Почему временные метрики критичны:**
- **Понимание динамики:** Обеспечивают понимание динамики производительности
- **Выявление трендов:** Помогают выявлять тренды
- **Planирование:** Помогают in Planировании
- **Оптимизация:** Помогают оптимизировать систему

### 1. Метрики on периодам

**Теория:** Метрики on периодам представляют собой показатели, которые измеряют производительность за различные временные периоды. Это критически важно for понимания временной динамики производительности.

**Почему метрики on периодам важны:**
- **Временная динамика:** Обеспечивают понимание временной динамики
- **Выявление паттернов:** Помогают выявлять временные паттерны
- **Planирование:** Помогают in Planировании
- **Сравнение:** Позволяют сравнивать различные периоды

**Плюсы:**
- Понимание временной динамики
- Выявление паттернов
- Помощь in Planировании
- Сравнение periods

**Минусы:**
- Сложность расчета
- Высокие требования к данным
- Необходимость понимания временных рядов

```python
class TemporalMetrics:
 """Временные метрики"""

 def __init__(self):
 self.metrics = {}

 def calculate_monthly_metrics(self, returns):
 """Расчет месячных метрик"""
 monthly_returns = returns.resample('M').sum()

 metrics = {
 'monthly_return': monthly_returns.mean(),
 'monthly_volatility': monthly_returns.std(),
 'monthly_sharpe': monthly_returns.mean() / monthly_returns.std(),
 'positive_months': np.sum(monthly_returns > 0) / len(monthly_returns),
 'best_month': monthly_returns.max(),
 'worst_month': monthly_returns.min()
 }

 return metrics

 def calculate_quarterly_metrics(self, returns):
 """Расчет квартальных метрик"""
 quarterly_returns = returns.resample('Q').sum()

 metrics = {
 'quarterly_return': quarterly_returns.mean(),
 'quarterly_volatility': quarterly_returns.std(),
 'quarterly_sharpe': quarterly_returns.mean() / quarterly_returns.std(),
 'positive_quarters': np.sum(quarterly_returns > 0) / len(quarterly_returns),
 'best_quarter': quarterly_returns.max(),
 'worst_quarter': quarterly_returns.min()
 }

 return metrics

 def calculate_yearly_metrics(self, returns):
 """Расчет годовых метрик"""
 yearly_returns = returns.resample('Y').sum()

 metrics = {
 'yearly_return': yearly_returns.mean(),
 'yearly_volatility': yearly_returns.std(),
 'yearly_sharpe': yearly_returns.mean() / yearly_returns.std(),
 'positive_years': np.sum(yearly_returns > 0) / len(yearly_returns),
 'best_year': yearly_returns.max(),
 'worst_year': yearly_returns.min()
 }

 return metrics
```

### 2. Метрики сезонности

**Теория:** Метрики сезонности представляют собой показатели, которые измеряют сезонные паттерны in производительности системы. Это критически важно for понимания временных зависимостей.

**Почему метрики сезонности важны:**
- **Сезонные паттерны:** Помогают выявлять сезонные паттерны
- **Planирование:** Помогают in Planировании with учетом сезонности
- **Оптимизация:** Помогают оптимизировать систему with учетом сезонности
- **Prediction:** Помогают предсказывать будущую производительность

**Плюсы:**
- Выявление сезонных паттернов
- Помощь in Planировании
- Оптимизация with учетом сезонности
- Prediction производительности

**Минусы:**
- Сложность расчета
- Высокие требования к данным
- Необходимость длительного наблюдения

```python
class SeasonalityMetrics:
 """Метрики сезонности"""

 def __init__(self):
 self.metrics = {}

 def calculate_monthly_seasonality(self, returns):
 """Расчет месячной сезонности"""
 monthly_returns = returns.groupby(returns.index.month)

 seasonality = {}
 for month in range(1, 13):
 month_returns = monthly_returns.get_group(month)
 seasonality[month] = {
 'mean_return': month_returns.mean(),
 'volatility': month_returns.std(),
 'positive_months': np.sum(month_returns > 0) / len(month_returns)
 }

 return seasonality

 def calculate_quarterly_seasonality(self, returns):
 """Расчет квартальной сезонности"""
 quarterly_returns = returns.groupby(returns.index.quarter)

 seasonality = {}
 for quarter in range(1, 5):
 quarter_returns = quarterly_returns.get_group(quarter)
 seasonality[quarter] = {
 'mean_return': quarter_returns.mean(),
 'volatility': quarter_returns.std(),
 'positive_quarters': np.sum(quarter_returns > 0) / len(quarter_returns)
 }

 return seasonality

 def calculate_weekly_seasonality(self, returns):
 """Расчет недельной сезонности"""
 weekly_returns = returns.groupby(returns.index.dayofweek)

 seasonality = {}
 for day in range(7):
 day_returns = weekly_returns.get_group(day)
 seasonality[day] = {
 'mean_return': day_returns.mean(),
 'volatility': day_returns.std(),
 'positive_days': np.sum(day_returns > 0) / len(day_returns)
 }

 return seasonality
```

## Сравнительные метрики

**Теория:** Сравнительные метрики представляют собой показатели, которые позволяют сравнивать производительность системы with бенчмарками and аналогами. Это критически важно for понимания относительной эффективности.

**Почему сравнительные метрики критичны:**
- **Относительная оценка:** Обеспечивают относительную оценку эффективности
- **Контекст:** Предоставляют контекст for оценки
- **Сравнение:** Позволяют сравнивать различные подходы
- **Бенчмаркинг:** Помогают in бенчмаркинге

### 1. Бенчмарк сравнение

**Теория:** Бенчмарк сравнение представляет собой процесс сравнения производительности системы with эталонными показателями. Это критически важно for понимания относительной эффективности.

**Почему бенчмарк сравнение важно:**
- **Относительная оценка:** Обеспечивает относительную оценку эффективности
- **Контекст:** Предоставляет контекст for оценки
- **Сравнение:** Позволяет сравнивать with эталоном
- **Бенчмаркинг:** Помогает in бенчмаркинге

**Плюсы:**
- Относительная оценка
- Контекст for оценки
- Сравнение with эталоном
- Помощь in бенчмаркинге

**Минусы:**
- Необходимость бенчмарков
- Сложность сравнения
- Потенциальные Issues with data

```python
class BenchmarkComparison:
 """Сравнение with бенчмарками"""

 def __init__(self, benchmark_returns):
 self.benchmark_returns = benchmark_returns

 def calculate_alpha(self, returns):
 """Расчет Alpha"""
 # Регрессия доходности on бенчмарк
 from sklearn.linear_model import LinearRegression

 X = self.benchmark_returns.values.reshape(-1, 1)
 y = returns.values

 model = LinearRegression()
 model.fit(X, y)

 # Alpha = intercept
 alpha = model.intercept_
 return alpha

 def calculate_beta(self, returns):
 """Расчет Beta"""
 # Регрессия доходности on бенчмарк
 from sklearn.linear_model import LinearRegression

 X = self.benchmark_returns.values.reshape(-1, 1)
 y = returns.values

 model = LinearRegression()
 model.fit(X, y)

 # Beta = coefficient
 beta = model.coef_[0]
 return beta

 def calculate_tracking_error(self, returns):
 """Расчет Tracking Error"""
 excess_returns = returns - self.benchmark_returns
 tracking_error = np.std(excess_returns)
 return tracking_error

 def calculate_information_ratio(self, returns):
 """Расчет Information Ratio"""
 excess_returns = returns - self.benchmark_returns
 tracking_error = np.std(excess_returns)
 information_ratio = np.mean(excess_returns) / tracking_error if tracking_error > 0 else 0
 return information_ratio
```

### 2. Peer сравнение

**Теория:** Peer сравнение представляет собой процесс сравнения производительности системы with аналогичными системами. Это критически важно for понимания конкурентной позиции.

**Почему Peer сравнение важно:**
- **Конкурентная позиция:** Помогает понять конкурентную позицию
- **Сравнение with аналогами:** Позволяет сравнивать with аналогами
- **Бенчмаркинг:** Помогает in бенчмаркинге
- **Planирование:** Помогает in Planировании развития

**Плюсы:**
- Понимание конкурентной позиции
- Сравнение with аналогами
- Помощь in бенчмаркинге
- Planирование развития

**Минусы:**
- Необходимость данных об аналогах
- Сложность сравнения
- Потенциальные Issues with data

```python
class PeerComparison:
 """Сравнение with аналогами"""

 def __init__(self, peer_returns):
 self.peer_returns = peer_returns

 def calculate_percentile_rank(self, returns):
 """Расчет процентильного ранга"""
 # Сравнение with аналогами
 percentile_ranks = {}

 for metric_name, peer_metric in self.peer_returns.items():
 # Расчет метрики for нашей системы
 our_metric = self._calculate_metric(returns, metric_name)

 # Расчет процентильного ранга
 percentile_rank = np.percentile(peer_metric, our_metric)
 percentile_ranks[metric_name] = percentile_rank

 return percentile_ranks

 def calculate_relative_performance(self, returns):
 """Расчет относительной производительности"""
 relative_performance = {}

 for metric_name, peer_metric in self.peer_returns.items():
 # Расчет метрики for нашей системы
 our_metric = self._calculate_metric(returns, metric_name)

 # Расчет относительной производительности
 peer_mean = np.mean(peer_metric)
 relative_performance[metric_name] = our_metric / peer_mean

 return relative_performance

 def _calculate_metric(self, returns, metric_name):
 """Вспомогательный метод for расчета метрик"""
 if metric_name == 'sharpe_ratio':
 return returns.mean() / returns.std() if returns.std() > 0 else 0
 elif metric_name == 'total_return':
 return (1 + returns).prod() - 1
 elif metric_name == 'volatility':
 return returns.std()
 elif metric_name == 'max_drawdown':
 cumulative = (1 + returns).cumprod()
 running_max = cumulative.expanding().max()
 drawdown = (cumulative - running_max) / running_max
 return drawdown.min()
 else:
 return 0.0
```

## Прогнозные метрики

**Теория:** Прогнозные метрики представляют собой показатели, которые измеряют качество прогнозов системы. Это критически важно for оценки предсказательной способности ML-модели.

**Почему прогнозные метрики критичны:**
- **Качество прогнозов:** Критически важны for оценки качества прогнозов
- **Валидация модели:** Помогают валидировать модель
- **Оптимизация:** Помогают оптимизировать модель
- **Сравнение:** Позволяют сравнивать различные модели

### 1. Метрики прогнозирования

**Теория:** Метрики прогнозирования представляют собой показатели, которые измеряют точность прогнозов системы. Это критически важно for оценки качества ML-модели.

**Почему метрики прогнозирования важны:**
- **Точность прогнозов:** Обеспечивают оценку точности прогнозов
- **Валидация модели:** Помогают валидировать модель
- **Оптимизация:** Помогают оптимизировать модель
- **Сравнение:** Позволяют сравнивать различные модели

**Плюсы:**
- Оценка точности прогнозов
- Валидация модели
- Помощь in оптимизации
- Сравнение моделей

**Минусы:**
- Сложность расчета
- Высокие требования к данным
- Необходимость понимания ML

```python
class ForecastingMetrics:
 """Метрики прогнозирования"""

 def __init__(self):
 self.metrics = {}

 def calculate_mape(self, predicted, actual):
 """Расчет MAPE"""
 mape = np.mean(np.abs((actual - predicted) / actual)) * 100
 return mape

 def calculate_rmse(self, predicted, actual):
 """Расчет RMSE"""
 rmse = np.sqrt(np.mean((predicted - actual) ** 2))
 return rmse

 def calculate_mae(self, predicted, actual):
 """Расчет MAE"""
 mae = np.mean(np.abs(predicted - actual))
 return mae

 def calculate_r2_score(self, predicted, actual):
 """Расчет R²"""
 from sklearn.metrics import r2_score
 r2 = r2_score(actual, predicted)
 return r2
```

### 2. Метрики стабильности прогнозов

**Теория:** Метрики стабильности прогнозов представляют собой показатели, которые измеряют стабильность прогнозов системы. Это критически важно for понимания надежности прогнозов.

**Почему метрики стабильности прогнозов важны:**
- **Надежность прогнозов:** Обеспечивают оценку надежности прогнозов
- **Стабильность:** Помогают оценить стабильность системы
- **Управление рисками:** Критически важны for управления рисками
- **Planирование:** Помогают in Planировании

**Плюсы:**
- Оценка надежности прогнозов
- Оценка стабильности
- Помощь in управлении рисками
- Planирование

**Минусы:**
- Сложность расчета
- Высокие требования к данным
- Необходимость длительного наблюдения

```python
class ForecastStabilityMetrics:
 """Метрики стабильности прогнозов"""

 def __init__(self):
 self.metrics = {}

 def calculate_forecast_stability(self, Predictions):
 """Расчет стабильности прогнозов"""
 # Изменения прогнозов
 Prediction_changes = np.diff(Predictions)

 # Стабильность = 1 - стандартное отклонение изменений
 stability = 1 - np.std(Prediction_changes)
 return stability

 def calculate_forecast_consistency(self, Predictions, actual):
 """Расчет консистентности прогнозов"""
 # Ошибки прогнозов
 errors = Predictions - actual

 # Консистентность = 1 - коэффициент вариации ошибок
 mean_error = np.mean(errors)
 std_error = np.std(errors)

 if mean_error == 0:
 consistency = 1 - std_error
 else:
 consistency = 1 - (std_error / abs(mean_error))

 return max(0, consistency)
```

## Автоматический анализ метрик

**Теория:** Автоматический анализ метрик представляет собой систему, которая автоматически отслеживает and анализирует метрики производительности. Это критически важно for поддержания эффективности системы.

**Почему автоматический анализ критичен:**
- **Непрерывный Monitoring:** Обеспечивает непрерывный Monitoring производительности
- **Своевременное выявление проблем:** Помогает своевременно выявлять проблемы
- **Автоматизация:** Автоматизирует процесс анализа
- **Эффективность:** Обеспечивает высокую эффективность анализа

### 1. Система Monitoringа метрик

**Теория:** Система Monitoringа метрик представляет собой комплексную систему отслеживания метрик производительности. Это критически важно for своевременного выявления проблем.

**Почему система Monitoringа важна:**
- **Своевременное выявление:** Позволяет своевременно выявлять проблемы
- **Автоматизация:** Автоматизирует процесс Monitoringа
- **Предотвращение потерь:** Помогает предотвратить потери
- **Оптимизация:** Помогает оптимизировать систему

**Плюсы:**
- Своевременное выявление проблем
- Автоматизация Monitoringа
- Предотвращение потерь
- Оптимизация системы

**Минусы:**
- Сложность settings
- Потенциальные ложные срабатывания
- Высокие требования к ресурсам

```python
class MetricsMonitor:
 """Monitoring метрик"""

 def __init__(self):
 self.metrics_history = []
 self.alert_thresholds = {
 'sharpe_ratio': 1.0,
 'max_drawdown': 0.15,
 'volatility': 0.3,
 'accuracy': 0.7
 }
 self.alerts = []

 def monitor_metrics(self, returns, Predictions=None):
 """Monitoring метрик"""
 # Расчет метрик
 metrics = self._calculate_all_metrics(returns, Predictions)

 # Сохранение истории
 self.metrics_history.append({
 'timestamp': datetime.now(),
 'metrics': metrics
 })

 # check алертов
 alerts = self._check_metric_alerts(metrics)

 return {
 'metrics': metrics,
 'alerts': alerts
 }

 def _calculate_all_metrics(self, returns, Predictions=None):
 """Расчет всех метрик"""
 metrics = {}

 # Базовые метрики
 return_metrics = ReturnMetrics()
 risk_metrics = RiskMetrics()
 efficiency_metrics = EfficiencyMetrics()

 metrics.update({
 'total_return': return_metrics.calculate_total_return(returns),
 'annualized_return': return_metrics.calculate_annualized_return(returns),
 'volatility': risk_metrics.calculate_volatility(returns),
 'max_drawdown': risk_metrics.calculate_max_drawdown(returns),
 'sharpe_ratio': efficiency_metrics.calculate_sharpe_ratio(returns)
 })

 # Метрики прогнозирования
 if Predictions is not None:
 forecasting_metrics = ForecastingMetrics()
 metrics.update({
 'mape': forecasting_metrics.calculate_mape(Predictions, returns),
 'rmse': forecasting_metrics.calculate_rmse(Predictions, returns),
 'r2_score': forecasting_metrics.calculate_r2_score(Predictions, returns)
 })

 return metrics

 def _analyze_trends(self, metrics):
 """Анализ трендов метрик"""
 trends = {}
 for metric, value in metrics.items():
 if isinstance(value, (int, float)):
 if value > 0:
 trends[metric] = "Положительный"
 elif value < 0:
 trends[metric] = "Отрицательный"
 else:
 trends[metric] = "Нейтральный"
 return trends

 def _generate_recommendations(self, metrics):
 """Генерация рекомендаций on basis метрик"""
 recommendations = []

 if metrics.get('sharpe_ratio', 0) < 1.0:
 recommendations.append("Низкий коэффициент Шарпа - рассмотрите оптимизацию стратегии")

 if metrics.get('max_drawdown', 0) < -0.15:
 recommendations.append("Высокая максимальная просадка - усильте управление рисками")

 if metrics.get('volatility', 0) > 0.3:
 recommendations.append("Высокая волатильность - рассмотрите диверсификацию")

 return recommendations

 def _check_metric_alerts(self, metrics):
 """check алертов метрик"""
 alerts = []

 for metric_name, threshold in self.alert_thresholds.items():
 if metric_name in metrics:
 if metrics[metric_name] < threshold:
 alerts.append({
 'metric': metric_name,
 'value': metrics[metric_name],
 'threshold': threshold,
 'severity': 'high' if metric_name in ['sharpe_ratio', 'accuracy'] else 'medium'
 })

 return alerts
```

### 2. Автоматическая Reportность

**Теория:** Автоматическая Reportность представляет собой систему, которая автоматически генерирует Reportы on метрикам производительности. Это критически важно for эффективного управления системой.

**Почему автоматическая Reportность важна:**
- **Регулярные Reportы:** Обеспечивает регулярные Reportы
- **Автоматизация:** Автоматизирует процесс Reportности
- **Эффективность:** Обеспечивает высокую эффективность Reportности
- **Planирование:** Помогает in Planировании

**Плюсы:**
- Регулярные Reportы
- Автоматизация Reportности
- Высокая эффективность
- Помощь in Planировании

**Минусы:**
- Сложность settings
- Потенциальные Issues with шаблонами
- Высокие требования к ресурсам

```python
class MetricsReporter:
 """Автоматическая Reportность on метрикам"""

 def __init__(self):
 self.report_templates = {}
 self.report_schedules = {
 'daily': self._generate_daily_report,
 'weekly': self._generate_weekly_report,
 'monthly': self._generate_monthly_report
 }

 def generate_report(self, metrics, report_type='daily'):
 """Генерация Reportа"""
 if report_type in self.report_schedules:
 return self.report_schedules[report_type](metrics)
 else:
 return self._generate_custom_report(metrics)

 def _generate_daily_report(self, metrics):
 """Генерация дневного Reportа"""
 report = {
 'date': datetime.now().strftime('%Y-%m-%d'),
 'type': 'daily',
 'summary': {
 'total_return': metrics.get('total_return', 0),
 'volatility': metrics.get('volatility', 0),
 'sharpe_ratio': metrics.get('sharpe_ratio', 0)
 },
 'alerts': metrics.get('alerts', [])
 }

 return report

 def _generate_weekly_report(self, metrics):
 """Генерация недельного Reportа"""
 report = {
 'date': datetime.now().strftime('%Y-%m-%d'),
 'type': 'weekly',
 'summary': {
 'weekly_return': metrics.get('weekly_return', 0),
 'max_drawdown': metrics.get('max_drawdown', 0),
 'consistency_ratio': metrics.get('consistency_ratio', 0)
 },
 'trends': self._analyze_trends(metrics),
 'recommendations': self._generate_recommendations(metrics)
 }

 return report

 def _generate_monthly_report(self, metrics):
 """Генерация месячного Reportа"""
 report = {
 'date': datetime.now().strftime('%Y-%m-%d'),
 'type': 'monthly',
 'summary': {
 'monthly_return': metrics.get('monthly_return', 0),
 'annualized_return': metrics.get('annualized_return', 0),
 'volatility': metrics.get('volatility', 0),
 'sharpe_ratio': metrics.get('sharpe_ratio', 0)
 },
 'performance_analysis': self._analyze_performance(metrics),
 'risk_analysis': self._analyze_risks(metrics),
 'recommendations': self._generate_recommendations(metrics)
 }

 return report
```

## Следующие шаги

После изучения метрик and анализа переходите к:
- **[17_examples.md](17_examples.md)** - Практические examples

## Ключевые выводы

**Теория:** Ключевые выводы суммируют наиболее важные аспекты метрик and анализа for создания эффективных ML-систем with доходностью 100%+ in месяц. Эти выводы критически важны for понимания того, как правильно измерять and анализировать производительность.

1. **Многоуровневые метрики - измерение on разных уровнях**
 - **Теория:** Многоуровневые метрики обеспечивают комплексную оценку производительности
 - **Почему важно:** Обеспечивает полное понимание системы
 - **Плюсы:** Комплексная оценка, детальное понимание
 - **Минусы:** Сложность анализа, высокие требования к ресурсам

2. **Временные метрики - анализ on периодам**
 - **Теория:** Временные метрики обеспечивают понимание динамики производительности
 - **Почему важно:** Обеспечивает понимание временной динамики
 - **Плюсы:** Понимание динамики, выявление трендов
 - **Минусы:** Сложность расчета, высокие требования к данным

3. **Сравнительные метрики - сравнение with бенчмарками**
 - **Теория:** Сравнительные метрики обеспечивают относительную оценку эффективности
 - **Почему важно:** Обеспечивает контекст for оценки
 - **Плюсы:** Относительная оценка, контекст
 - **Минусы:** Необходимость бенчмарков, сложность сравнения

4. **Прогнозные метрики - оценка предсказательной способности**
 - **Теория:** Прогнозные метрики критически важны for ML-систем
 - **Почему важно:** Обеспечивает оценку качества прогнозов
 - **Плюсы:** Оценка качества прогнозов, валидация модели
 - **Минусы:** Сложность расчета, высокие требования к данным

5. **Автоматический Monitoring - непрерывный контроль метрик**
 - **Теория:** Автоматический Monitoring критически важен for поддержания эффективности
 - **Почему важно:** Обеспечивает непрерывный контроль
 - **Плюсы:** Непрерывный контроль, своевременное выявление проблем
 - **Минусы:** Сложность settings, высокие требования к ресурсам

6. **Автоматическая Reportность - регулярные Reportы**
 - **Теория:** Автоматическая Reportность критически важна for управления
 - **Почему важно:** Обеспечивает регулярные Reportы
 - **Плюсы:** Регулярные Reportы, автоматизация
 - **Минусы:** Сложность settings, высокие требования к ресурсам

---

**Важно:** Правильные метрики - это основа for принятия решений. Выбирайте метрики, которые соответствуют вашим целям and стратегии.
