# 09. 🛡️ Управление рисками

**Цель:** Научиться эффективно управлять рисками в торговых стратегиях для защиты капитала.

## Необходимые импорты и настройка

**Теория:** Перед началом работы с управлением рисками необходимо импортировать все необходимые библиотеки и настроить окружение. Это обеспечивает корректную работу всех компонентов системы управления рисками.

```python
# Основные библиотеки для численных вычислений и анализа данных
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.optimize import minimize
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
import time
warnings.filterwarnings('ignore')

# Настройка для красивого отображения графиков
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Настройка для корректного отображения русских символов
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

print("✅ Все библиотеки успешно импортированы")
print("🔧 Окружение настроено для работы с управлением рисками")
```

## Что такое управление рисками?

**Теория:** Управление рисками - это фундаментальный процесс в финансовой торговле, который включает идентификацию, оценку, контроль и мониторинг рисков для защиты капитала и обеспечения долгосрочной прибыльности. Это критически важный аспект любой торговой системы.

**Управление рисками** - это процесс идентификации, оценки и контроля рисков для минимизации потерь и максимизации прибыли.

**Почему управление рисками критично для финансовых систем:**
- **Защита капитала:** Предотвращение катастрофических потерь
- **Стабильность:** Обеспечение предсказуемых результатов
- **Выживание:** Критично для долгосрочного успеха
- **Психологический комфорт:** Снижение стресса и эмоциональных решений

### Зачем нужно управление рисками?

**Теория:** Управление рисками является основой успешной торговли. Без правильного управления рисками даже самая прибыльная стратегия может привести к катастрофическим потерям.

- **Защита капитала** - предотвращение больших потерь
  - **Почему важно:** Большие потери могут уничтожить торговый счет
  - **Плюсы:** Сохранение капитала, возможность продолжения торговли
  - **Минусы:** Может ограничивать потенциальную прибыль

- **Стабильность** - снижение волатильности результатов
  - **Почему важно:** Стабильные результаты легче планировать и управлять
  - **Плюсы:** Предсказуемость, легкое планирование
  - **Минусы:** Может снижать потенциальную прибыль

- **Психологический комфорт** - уверенность в торговле
  - **Почему важно:** Эмоциональные решения часто приводят к потерям
  - **Плюсы:** Снижение стресса, лучшие решения
  - **Минусы:** Может требовать дисциплины

- **Долгосрочная прибыльность** - выживание в долгосрочной перспективе
  - **Почему важно:** Только выжившие могут получать прибыль
  - **Плюсы:** Долгосрочный успех, устойчивость
  - **Минусы:** Может требовать терпения

**Дополнительные преимущества управления рисками:**
- **Регуляторное соответствие:** Соответствие требованиям регуляторов
- **Доверие инвесторов:** Повышение доверия к системе
- **Масштабируемость:** Возможность увеличения капитала
- **Анализ производительности:** Лучшее понимание результатов

## Типы рисков

**Теория:** Финансовые риски можно классифицировать по различным критериям. Понимание типов рисков критично для разработки эффективных стратегий управления рисками.

### 1. Рыночные риски

**Теория:** Рыночные риски связаны с изменениями рыночных цен и волатильности. Это наиболее очевидные риски в торговле, которые могут быть частично контролируемы через диверсификацию и позиционирование.

**Почему рыночные риски важны:**
- **Прямое воздействие:** Непосредственно влияют на результаты торговли
- **Контролируемость:** Могут быть частично контролируемы
- **Измеримость:** Относительно легко измерить и мониторить
- **Планируемость:** Можно планировать и хеджировать

**Плюсы управления рыночными рисками:**
- Прямое влияние на результаты
- Возможность контроля
- Измеримость
- Планируемость

**Минусы управления рыночными рисками:**
- Могут быть непредсказуемыми
- Требуют постоянного мониторинга
- Могут быть дорогими в хеджировании
- Ограниченная эффективность в кризисах

### Практическая реализация управления рыночными рисками

**Теория:** Класс MarketRiskManager реализует основные принципы управления рыночными рисками через расчет размера позиций, стоп-лоссов и тейк-профитов. Это основа любой торговой системы, которая позволяет контролировать риски на уровне отдельных сделок.

**Ключевые принципы реализации:**
- **Kelly Criterion:** Математически обоснованный метод расчета оптимального размера позиции
- **ATR-based Stop Loss:** Использование Average True Range для динамического расчета стоп-лоссов
- **Risk-Reward Ratio:** Соотношение риска к прибыли для обеспечения положительного математического ожидания
- **Волатильность-адаптация:** Корректировка размера позиции в зависимости от текущей волатильности рынка

**Почему именно эти методы:**
- Kelly Criterion максимизирует логарифмическую полезность в долгосрочной перспективе
- ATR учитывает реальную волатильность инструмента, а не фиксированные проценты
- Risk-Reward Ratio обеспечивает прибыльность даже при проигрышных сделках
- Адаптация к волатильности предотвращает переторговлю в нестабильных условиях

```python
class MarketRiskManager:
    """
    Класс для управления рыночными рисками в торговых стратегиях.
    
    Этот класс реализует основные принципы управления рисками:
    - Расчет оптимального размера позиции с использованием Kelly Criterion
    - Динамический расчет стоп-лоссов на основе волатильности (ATR)
    - Расчет тейк-профитов с заданным соотношением риск/прибыль
    - Адаптация к текущим рыночным условиям
    """
    
    def __init__(self, max_position_size=0.1, stop_loss=0.02, take_profit=0.04):
        """
        Инициализация менеджера рыночных рисков.
        
        Args:
            max_position_size (float): Максимальный размер позиции как доля от капитала (по умолчанию 10%)
            stop_loss (float): Базовый стоп-лосс как доля от цены (по умолчанию 2%)
            take_profit (float): Базовый тейк-профит как доля от цены (по умолчанию 4%)
        """
        self.max_position_size = max_position_size  # Максимальный размер позиции
        self.stop_loss = stop_loss  # Базовый Stop Loss
        self.take_profit = take_profit  # Базовый Take Profit
    
    def calculate_position_size(self, account_balance, volatility, confidence_level=0.95):
        """
        Расчет оптимального размера позиции на основе Kelly Criterion и волатильности.
        
        Kelly Criterion - это математически обоснованный метод определения оптимального
        размера ставки, который максимизирует логарифмическую полезность в долгосрочной перспективе.
        
        Формула Kelly: f = (bp - q) / b
        где:
        - f = доля капитала для ставки
        - b = коэффициент выплаты (отношение выигрыша к ставке)
        - p = вероятность выигрыша
        - q = вероятность проигрыша (1-p)
        
        Args:
            account_balance (float): Текущий баланс счета
            volatility (float): Текущая волатильность актива (стандартное отклонение доходности)
            confidence_level (float): Уровень доверия для расчета (по умолчанию 95%)
            
        Returns:
            float: Рекомендуемый размер позиции в денежных единицах
        """
        
        # Kelly Criterion для оптимального размера позиции
        # Эти параметры должны быть получены из исторического анализа стратегии
        win_rate = 0.6  # Предполагаемая вероятность выигрыша (60%)
        avg_win = 0.02  # Средний выигрыш (2% от размера позиции)
        avg_loss = 0.01  # Средний проигрыш (1% от размера позиции)
        
        # Расчет коэффициента выплаты (отношение среднего выигрыша к среднему проигрышу)
        payout_ratio = avg_win / avg_loss
        
        # Формула Kelly Criterion
        kelly_fraction = (win_rate * payout_ratio - (1 - win_rate)) / payout_ratio
        
        # Ограничение Kelly Criterion для предотвращения чрезмерного риска
        kelly_fraction = max(0, min(kelly_fraction, self.max_position_size))
        
        # Адаптация к волатильности: чем выше волатильность, тем меньше размер позиции
        # Это предотвращает переторговлю в нестабильных условиях
        volatility_adjustment = 1 / (1 + volatility * 10)
        
        # Финальный размер позиции с учетом всех факторов
        position_size = account_balance * kelly_fraction * volatility_adjustment
        
        # Дополнительное ограничение для безопасности
        return min(position_size, account_balance * self.max_position_size)
    
    def calculate_stop_loss(self, entry_price, volatility):
        """
        Расчет динамического Stop Loss на основе волатильности (ATR-подход).
        
        ATR (Average True Range) - это технический индикатор, который измеряет
        волатильность рынка. Использование ATR для расчета стоп-лоссов позволяет
        адаптироваться к текущим рыночным условиям.
        
        Args:
            entry_price (float): Цена входа в позицию
            volatility (float): Текущая волатильность (ATR или стандартное отклонение)
            
        Returns:
            float: Рекомендуемая цена стоп-лосса
        """
        
        # ATR-based Stop Loss с множителем для настройки чувствительности
        atr_multiplier = 2.0  # Множитель ATR (можно настроить в зависимости от стратегии)
        stop_distance = volatility * atr_multiplier
        
        # Расчет цены стоп-лосса (для лонг позиции)
        stop_loss_price = entry_price - stop_distance
        
        return stop_loss_price
    
    def calculate_take_profit(self, entry_price, stop_loss_price, risk_reward_ratio=2):
        """
        Расчет Take Profit на основе соотношения риск/прибыль.
        
        Risk-Reward Ratio - это соотношение потенциальной прибыли к потенциальному риску.
        Рекомендуется использовать соотношение не менее 1:2 (прибыль в 2 раза больше риска).
        
        Args:
            entry_price (float): Цена входа в позицию
            stop_loss_price (float): Цена стоп-лосса
            risk_reward_ratio (float): Желаемое соотношение риск/прибыль (по умолчанию 2)
            
        Returns:
            float: Рекомендуемая цена тейк-профита
        """
        
        # Расчет размера риска
        risk = entry_price - stop_loss_price
        
        # Расчет размера прибыли на основе соотношения риск/прибыль
        reward = risk * risk_reward_ratio
        
        # Расчет цены тейк-профита (для лонг позиции)
        take_profit_price = entry_price + reward
        
        return take_profit_price

# Пример использования MarketRiskManager
def demonstrate_market_risk_manager():
    """
    Демонстрация работы MarketRiskManager с реальными данными.
    """
    print("=== Демонстрация MarketRiskManager ===")
    
    # Создание экземпляра менеджера рисков
    risk_manager = MarketRiskManager(
        max_position_size=0.1,  # Максимум 10% от капитала
        stop_loss=0.02,         # Базовый стоп-лосс 2%
        take_profit=0.04        # Базовый тейк-профит 4%
    )
    
    # Параметры для расчета
    account_balance = 10000  # Баланс счета $10,000
    entry_price = 1.2000    # Цена входа EUR/USD
    volatility = 0.015      # Волатильность 1.5%
    
    # Расчет размера позиции
    position_size = risk_manager.calculate_position_size(account_balance, volatility)
    print(f"💰 Рекомендуемый размер позиции: ${position_size:.2f}")
    print(f"📊 Доля от капитала: {(position_size/account_balance)*100:.2f}%")
    
    # Расчет стоп-лосса
    stop_loss_price = risk_manager.calculate_stop_loss(entry_price, volatility)
    print(f"🛑 Рекомендуемый стоп-лосс: {stop_loss_price:.4f}")
    print(f"📉 Риск в пунктах: {(entry_price - stop_loss_price)*10000:.0f} pips")
    
    # Расчет тейк-профита
    take_profit_price = risk_manager.calculate_take_profit(entry_price, stop_loss_price)
    print(f"🎯 Рекомендуемый тейк-профит: {take_profit_price:.4f}")
    print(f"📈 Прибыль в пунктах: {(take_profit_price - entry_price)*10000:.0f} pips")
    
    # Расчет соотношения риск/прибыль
    risk_amount = entry_price - stop_loss_price
    profit_amount = take_profit_price - entry_price
    risk_reward = profit_amount / risk_amount
    print(f"⚖️ Соотношение риск/прибыль: 1:{risk_reward:.1f}")
    
    return {
        'position_size': position_size,
        'stop_loss': stop_loss_price,
        'take_profit': take_profit_price,
        'risk_reward_ratio': risk_reward
    }

# Запуск демонстрации
if __name__ == "__main__":
    demo_results = demonstrate_market_risk_manager()
```

### 2. Кредитные риски

**Теория:** Кредитные риски связаны с возможностью потерь из-за неспособности контрагентов выполнить свои обязательства. В торговле это особенно важно при использовании кредитного плеча и маржинальной торговли.

**Почему кредитные риски важны:**
- **Кредитное плечо:** Увеличивает как прибыль, так и риски
- **Маржинальные требования:** Могут привести к принудительному закрытию позиций
- **Контрагентский риск:** Риск невыполнения обязательств
- **Ликвидность:** Может влиять на возможность закрытия позиций

**Плюсы управления кредитными рисками:**
- Защита от принудительного закрытия
- Сохранение капитала
- Предотвращение маржин-коллов
- Повышение стабильности

**Минусы управления кредитными рисками:**
- Может ограничивать использование кредитного плеча
- Требует постоянного мониторинга
- Может быть дорогим
- Сложность оценки

### Практическая реализация управления кредитными рисками

**Теория:** Класс CreditRiskManager управляет кредитными рисками, связанными с использованием заемных средств и маржинальной торговлей. Это критически важно для предотвращения принудительного закрытия позиций и сохранения капитала.

**Ключевые принципы управления кредитными рисками:**
- **Маржинальные требования:** Динамический расчет необходимой маржи с учетом волатильности
- **Мониторинг загрузки маржи:** Контроль использования доступного кредитного плеча
- **Предупреждения о маржин-коллах:** Раннее обнаружение критических ситуаций
- **Адаптивные лимиты:** Корректировка лимитов в зависимости от рыночных условий

**Почему это важно:**
- Кредитное плечо увеличивает как прибыль, так и риски
- Маржин-коллы могут привести к принудительному закрытию всех позиций
- Правильное управление кредитными рисками позволяет использовать преимущества плеча без катастрофических потерь
- Динамические маржинальные требования учитывают реальную волатильность активов

```python
class CreditRiskManager:
    """
    Класс для управления кредитными рисками в маржинальной торговле.
    
    Этот класс контролирует использование кредитного плеча, рассчитывает
    маржинальные требования и предотвращает маржин-коллы.
    """
    
    def __init__(self, max_leverage=3.0, margin_requirement=0.3):
        """
        Инициализация менеджера кредитных рисков.
        
        Args:
            max_leverage (float): Максимальное кредитное плечо (по умолчанию 3:1)
            margin_requirement (float): Базовое требование к марже (по умолчанию 30%)
        """
        self.max_leverage = max_leverage
        self.margin_requirement = margin_requirement
    
    def calculate_margin_requirement(self, position_value, asset_volatility):
        """
        Расчет динамического требования к марже с учетом волатильности актива.
        
        Маржинальные требования должны учитывать не только базовые правила брокера,
        но и реальную волатильность актива. Более волатильные активы требуют
        большей маржи для защиты от резких движений цены.
        
        Args:
            position_value (float): Стоимость позиции
            asset_volatility (float): Волатильность актива (стандартное отклонение)
            
        Returns:
            float: Требуемая маржа в денежных единицах
        """
        
        # Базовое требование к марже (стандартное для всех активов)
        base_margin = position_value * self.margin_requirement
        
        # Дополнительная маржа для волатильных активов
        # Коэффициент 0.1 означает, что за каждый 1% волатильности добавляется 0.1% маржи
        volatility_margin = position_value * asset_volatility * 0.1
        
        # Общая требуемая маржа
        total_margin = base_margin + volatility_margin
        
        # Ограничение максимальной маржи (не более 50% от стоимости позиции)
        max_margin = position_value * 0.5
        total_margin = min(total_margin, max_margin)
        
        return total_margin
    
    def check_margin_call(self, account_balance, margin_used, position_value):
        """
        Проверка состояния маржи и предупреждение о маржин-коллах.
        
        Маржин-колл происходит, когда заемные средства превышают определенный
        процент от собственного капитала. Это критическая ситуация, которая
        может привести к принудительному закрытию позиций.
        
        Args:
            account_balance (float): Текущий баланс счета
            margin_used (float): Использованная маржа
            position_value (float): Общая стоимость позиций
            
        Returns:
            tuple: (bool, str) - (есть ли проблема, описание проблемы)
        """
        
        # Расчет коэффициента использования маржи
        margin_ratio = margin_used / account_balance if account_balance > 0 else 1.0
        
        # Проверка различных уровней риска
        if margin_ratio > 0.9:  # 90% маржи использовано - КРИТИЧНО
            return True, f"🚨 КРИТИЧНО: Маржин-колл! Использовано {margin_ratio:.1%} маржи"
        elif margin_ratio > 0.8:  # 80% маржи использовано - ВЫСОКИЙ РИСК
            return True, f"⚠️ ВЫСОКИЙ РИСК: Использовано {margin_ratio:.1%} маржи. Рекомендуется сокращение позиций"
        elif margin_ratio > 0.6:  # 60% маржи использовано - ПРЕДУПРЕЖДЕНИЕ
            return True, f"⚠️ ПРЕДУПРЕЖДЕНИЕ: Использовано {margin_ratio:.1%} маржи. Следите за рисками"
        else:  # Нормальное состояние
            return False, f"✅ Маржа в норме. Использовано {margin_ratio:.1%} маржи"
    
    def calculate_max_position_size(self, account_balance, asset_volatility, leverage_multiplier=1.0):
        """
        Расчет максимального размера позиции с учетом кредитных ограничений.
        
        Этот метод определяет максимальный размер позиции, который можно открыть
        без превышения лимитов по марже и кредитному плечу.
        
        Args:
            account_balance (float): Доступный баланс
            asset_volatility (float): Волатильность актива
            leverage_multiplier (float): Множитель кредитного плеча (по умолчанию 1.0)
            
        Returns:
            float: Максимальный размер позиции
        """
        
        # Расчет эффективного кредитного плеча с учетом волатильности
        effective_leverage = self.max_leverage * leverage_multiplier
        
        # Корректировка плеча в зависимости от волатильности
        # Чем выше волатильность, тем меньше плечо
        volatility_adjustment = 1 / (1 + asset_volatility * 5)
        adjusted_leverage = effective_leverage * volatility_adjustment
        
        # Максимальный размер позиции
        max_position = account_balance * adjusted_leverage
        
        return max_position

# Пример использования CreditRiskManager
def demonstrate_credit_risk_manager():
    """
    Демонстрация работы CreditRiskManager с различными сценариями.
    """
    print("=== Демонстрация CreditRiskManager ===")
    
    # Создание экземпляра менеджера кредитных рисков
    credit_manager = CreditRiskManager(
        max_leverage=3.0,        # Максимальное плечо 3:1
        margin_requirement=0.3   # Базовое требование к марже 30%
    )
    
    # Сценарий 1: Нормальные условия
    print("\n📊 Сценарий 1: Нормальные условия")
    account_balance = 10000
    position_value = 20000  # Позиция с плечом 2:1
    asset_volatility = 0.02  # Волатильность 2%
    
    # Расчет маржинального требования
    margin_req = credit_manager.calculate_margin_requirement(position_value, asset_volatility)
    print(f"💰 Требуемая маржа: ${margin_req:.2f}")
    print(f"📊 Доля маржи от позиции: {(margin_req/position_value)*100:.1f}%")
    
    # Проверка маржин-колла
    is_margin_call, message = credit_manager.check_margin_call(account_balance, margin_req, position_value)
    print(f"🔍 Статус маржи: {message}")
    
    # Сценарий 2: Высокая волатильность
    print("\n📊 Сценарий 2: Высокая волатильность")
    high_volatility = 0.05  # Волатильность 5%
    margin_req_high = credit_manager.calculate_margin_requirement(position_value, high_volatility)
    print(f"💰 Требуемая маржа (высокая волатильность): ${margin_req_high:.2f}")
    print(f"📊 Доля маржи от позиции: {(margin_req_high/position_value)*100:.1f}%")
    
    # Сценарий 3: Критическая ситуация
    print("\n📊 Сценарий 3: Критическая ситуация")
    large_position = 25000  # Большая позиция
    margin_req_large = credit_manager.calculate_margin_requirement(large_position, asset_volatility)
    is_critical, critical_message = credit_manager.check_margin_call(account_balance, margin_req_large, large_position)
    print(f"💰 Требуемая маржа: ${margin_req_large:.2f}")
    print(f"🔍 Статус маржи: {critical_message}")
    
    # Расчет максимального размера позиции
    max_position = credit_manager.calculate_max_position_size(account_balance, asset_volatility)
    print(f"🎯 Максимальный размер позиции: ${max_position:.2f}")
    print(f"📊 Эффективное плечо: {max_position/account_balance:.1f}:1")
    
    return {
        'margin_requirement': margin_req,
        'is_margin_call': is_margin_call,
        'max_position_size': max_position
    }

# Запуск демонстрации
if __name__ == "__main__":
    credit_demo_results = demonstrate_credit_risk_manager()
```

### 3. Операционные риски

**Теория:** Операционные риски связаны с внутренними процессами, системами и людьми. В автоматизированной торговле это особенно важно, так как технические сбои могут привести к значительным потерям.

**Почему операционные риски важны:**
- **Технические сбои:** Могут привести к потере контроля над позициями
- **Человеческие ошибки:** Могут привести к неправильным решениям
- **Системные риски:** Могут влиять на всю торговую систему
- **Процессные риски:** Могут нарушать торговые процессы

**Плюсы управления операционными рисками:**
- Повышение надежности системы
- Снижение технических сбоев
- Улучшение процессов
- Повышение контроля

**Минусы управления операционными рисками:**
- Может быть дорогим
- Требует постоянного внимания
- Сложность оценки
- Может ограничивать гибкость

### Практическая реализация управления операционными рисками

**Теория:** Класс OperationalRiskManager контролирует операционные риски, связанные с техническими сбоями, человеческими ошибками и системными ограничениями. В автоматизированной торговле это критически важно для предотвращения потерь из-за технических проблем.

**Ключевые принципы управления операционными рисками:**
- **Лимиты торговли:** Контроль количества сделок для предотвращения переторговли
- **Мониторинг проскальзывания:** Отслеживание разницы между ожидаемой и фактической ценой исполнения
- **Контроль качества данных:** Проверка корректности рыночных данных
- **Резервные системы:** Дублирование критически важных компонентов

**Почему это критично:**
- Технические сбои могут привести к потере контроля над позициями
- Человеческие ошибки часто являются причиной крупных потерь
- Системные ограничения могут нарушать торговые процессы
- Проскальзывание может значительно снизить прибыльность стратегии

```python
class OperationalRiskManager:
    """
    Класс для управления операционными рисками в торговой системе.
    
    Этот класс контролирует технические аспекты торговли, включая лимиты,
    проскальзывание, качество данных и системную стабильность.
    """
    
    def __init__(self, max_daily_trades=10, max_slippage=0.001):
        """
        Инициализация менеджера операционных рисков.
        
        Args:
            max_daily_trades (int): Максимальное количество сделок в день
            max_slippage (float): Максимально допустимое проскальзывание
        """
        self.max_daily_trades = max_daily_trades
        self.max_slippage = max_slippage
        self.daily_trades = 0
        self.trade_history = []
        self.slippage_history = []
    
    def check_trading_limits(self):
        """
        Проверка соблюдения лимитов торговли.
        
        Лимиты торговли помогают предотвратить:
        - Переторговлю (excessive trading)
        - Эмоциональные решения
        - Технические перегрузки системы
        - Нарушение стратегии
        
        Returns:
            tuple: (bool, str) - (можно ли торговать, описание статуса)
        """
        
        if self.daily_trades >= self.max_daily_trades:
            return False, f"🚫 Достигнут дневной лимит торгов ({self.max_daily_trades})"
        elif self.daily_trades >= self.max_daily_trades * 0.8:
            return True, f"⚠️ Приближается к лимиту: {self.daily_trades}/{self.max_daily_trades}"
        else:
            return True, f"✅ Торговля разрешена: {self.daily_trades}/{self.max_daily_trades}"
    
    def calculate_slippage(self, order_size, market_volume, price, market_volatility=0.02):
        """
        Расчет ожидаемого проскальзывания для ордера.
        
        Проскальзывание (slippage) - это разница между ожидаемой ценой исполнения
        и фактической ценой. Оно зависит от:
        - Размера ордера относительно рыночного объема
        - Волатильности рынка
        - Времени исполнения
        - Ликвидности инструмента
        
        Args:
            order_size (float): Размер ордера
            market_volume (float): Объем торгов на рынке
            price (float): Текущая цена инструмента
            market_volatility (float): Волатильность рынка
            
        Returns:
            float: Ожидаемое проскальзывание в долях от цены
        """
        
        # Расчет отношения размера ордера к рыночному объему
        volume_ratio = order_size / market_volume if market_volume > 0 else 1.0
        
        # Базовое проскальзывание в зависимости от размера ордера
        if volume_ratio < 0.01:  # Малый ордер (< 1% от объема)
            base_slippage = 0.0001
        elif volume_ratio < 0.05:  # Средний ордер (1-5% от объема)
            base_slippage = 0.0005
        elif volume_ratio < 0.1:  # Большой ордер (5-10% от объема)
            base_slippage = 0.001
        else:  # Очень большой ордер (> 10% от объема)
            base_slippage = 0.002
        
        # Корректировка на волатильность
        volatility_multiplier = 1 + (market_volatility * 10)
        adjusted_slippage = base_slippage * volatility_multiplier
        
        # Ограничение максимальным допустимым проскальзыванием
        final_slippage = min(adjusted_slippage, self.max_slippage)
        
        return final_slippage
    
    def record_trade(self, trade_details):
        """
        Запись информации о сделке для мониторинга операционных рисков.
        
        Args:
            trade_details (dict): Детали сделки
        """
        self.daily_trades += 1
        self.trade_history.append({
            'timestamp': pd.Timestamp.now(),
            'trade_number': self.daily_trades,
            'details': trade_details
        })
    
    def check_data_quality(self, market_data):
        """
        Проверка качества рыночных данных.
        
        Качество данных критично для принятия торговых решений.
        Плохие данные могут привести к неправильным сигналам и потерям.
        
        Args:
            market_data (dict): Рыночные данные
            
        Returns:
            tuple: (bool, str) - (данные корректны, описание проблем)
        """
        issues = []
        
        # Проверка на отсутствующие значения
        for key, value in market_data.items():
            if pd.isna(value) or value is None:
                issues.append(f"Отсутствует значение для {key}")
        
        # Проверка на аномальные значения
        if 'price' in market_data:
            price = market_data['price']
            if price <= 0:
                issues.append("Некорректная цена")
        
        if 'volume' in market_data:
            volume = market_data['volume']
            if volume < 0:
                issues.append("Отрицательный объем")
        
        # Проверка на старые данные
        if 'timestamp' in market_data:
            timestamp = market_data['timestamp']
            if isinstance(timestamp, str):
                timestamp = pd.to_datetime(timestamp)
            
            time_diff = pd.Timestamp.now() - timestamp
            if time_diff > pd.Timedelta(minutes=5):
                issues.append("Данные устарели")
        
        if issues:
            return False, f"❌ Проблемы с данными: {'; '.join(issues)}"
        else:
            return True, "✅ Данные корректны"
    
    def get_operational_metrics(self):
        """
        Получение метрик операционных рисков.
        
        Returns:
            dict: Словарь с операционными метриками
        """
        return {
            'daily_trades': self.daily_trades,
            'max_daily_trades': self.max_daily_trades,
            'trades_remaining': self.max_daily_trades - self.daily_trades,
            'max_slippage': self.max_slippage,
            'avg_slippage': np.mean(self.slippage_history) if self.slippage_history else 0,
            'data_quality_issues': len([t for t in self.trade_history if 'error' in t.get('details', {})])
        }

# Пример использования OperationalRiskManager
def demonstrate_operational_risk_manager():
    """
    Демонстрация работы OperationalRiskManager с различными сценариями.
    """
    print("=== Демонстрация OperationalRiskManager ===")
    
    # Создание экземпляра менеджера операционных рисков
    op_risk_manager = OperationalRiskManager(
        max_daily_trades=5,      # Максимум 5 сделок в день
        max_slippage=0.002       # Максимальное проскальзывание 0.2%
    )
    
    # Симуляция торгового дня
    print("\n📊 Симуляция торгового дня")
    
    for i in range(7):  # Попытка совершить 7 сделок
        # Проверка лимитов
        can_trade, limit_message = op_risk_manager.check_trading_limits()
        print(f"Сделка {i+1}: {limit_message}")
        
        if not can_trade:
            print("🛑 Торговля остановлена из-за превышения лимитов")
            break
        
        # Расчет проскальзывания
        order_size = 1000
        market_volume = 100000
        price = 1.2000
        volatility = 0.02
        
        slippage = op_risk_manager.calculate_slippage(order_size, market_volume, price, volatility)
        print(f"📈 Ожидаемое проскальзывание: {slippage:.4f} ({slippage*100:.2f}%)")
        
        # Проверка качества данных
        market_data = {
            'price': price + np.random.normal(0, 0.001),
            'volume': market_volume + np.random.normal(0, 1000),
            'timestamp': pd.Timestamp.now()
        }
        
        data_ok, data_message = op_risk_manager.check_data_quality(market_data)
        print(f"🔍 Качество данных: {data_message}")
        
        # Запись сделки
        op_risk_manager.record_trade({
            'order_size': order_size,
            'slippage': slippage,
            'data_quality': data_ok
        })
        
        op_risk_manager.slippage_history.append(slippage)
    
    # Получение операционных метрик
    metrics = op_risk_manager.get_operational_metrics()
    print(f"\n📊 Операционные метрики:")
    print(f"   Сделок совершено: {metrics['daily_trades']}")
    print(f"   Осталось сделок: {metrics['trades_remaining']}")
    print(f"   Среднее проскальзывание: {metrics['avg_slippage']:.4f}")
    print(f"   Проблемы с данными: {metrics['data_quality_issues']}")
    
    return metrics

# Запуск демонстрации
if __name__ == "__main__":
    op_demo_results = demonstrate_operational_risk_manager()
```

## Продвинутые техники управления рисками

**Теория:** Продвинутые техники управления рисками используют математические и статистические методы для более точной оценки и контроля рисков. Эти методы особенно важны для институциональных трейдеров и крупных портфелей.

### 1. Value at Risk (VaR)

**Теория:** Value at Risk (VaR) - это статистическая мера риска, которая показывает максимальную ожидаемую потерю портфеля за определенный период времени с заданной вероятностью. VaR широко используется в финансовой индустрии для оценки рыночных рисков.

**Ключевые принципы VaR:**
- **Квантильный подход:** VaR представляет собой квантиль распределения доходности
- **Временной горизонт:** Обычно рассчитывается для 1 дня, 1 недели или 1 месяца
- **Уровень доверия:** Чаще всего используется 95% или 99% уровень доверия
- **Три метода расчета:** Исторический, параметрический и Монте-Карло

**Почему VaR важен:**
- Предоставляет единую метрику риска для сравнения различных активов
- Помогает в планировании капитала и установлении лимитов
- Используется регуляторами для оценки рисков банков и инвестиционных компаний
- Позволяет агрегировать риски различных позиций в портфеле

```python
def calculate_var(returns, confidence_level=0.05, time_horizon=1):
    """
    Расчет Value at Risk (VaR) тремя различными методами.
    
    VaR - это максимальная ожидаемая потеря портфеля за определенный период
    времени с заданной вероятностью. Например, VaR 95% на 1 день означает,
    что с вероятностью 95% потери не превысят рассчитанное значение.
    
    Args:
        returns (array-like): Массив доходностей портфеля
        confidence_level (float): Уровень доверия (по умолчанию 5% = 95% VaR)
        time_horizon (int): Временной горизонт в днях (по умолчанию 1 день)
        
    Returns:
        dict: Словарь с результатами всех трех методов расчета VaR
    """
    
    # Преобразование в numpy array для удобства вычислений
    returns = np.array(returns)
    
    # 1. ИСТОРИЧЕСКИЙ VaR
    # Использует исторические данные без предположений о распределении
    # Простой и интуитивно понятный метод
    historical_var = np.percentile(returns, confidence_level * 100)
    
    # 2. ПАРАМЕТРИЧЕСКИЙ VaR
    # Предполагает нормальное распределение доходностей
    # Использует среднее и стандартное отклонение
    mean_return = returns.mean()
    std_return = returns.std()
    
    # Корректировка на временной горизонт (квадратный корень времени)
    time_adjusted_std = std_return * np.sqrt(time_horizon)
    time_adjusted_mean = mean_return * time_horizon
    
    # Расчет квантиля нормального распределения
    z_score = stats.norm.ppf(confidence_level)
    parametric_var = time_adjusted_mean + time_adjusted_std * z_score
    
    # 3. МОНТЕ-КАРЛО VaR
    # Использует симуляцию для генерации возможных сценариев
    # Более гибкий, но требует больше вычислительных ресурсов
    n_simulations = 10000
    
    # Генерация случайных доходностей на основе исторических параметров
    simulated_returns = np.random.normal(
        time_adjusted_mean, 
        time_adjusted_std, 
        n_simulations
    )
    
    monte_carlo_var = np.percentile(simulated_returns, confidence_level * 100)
    
    # Дополнительные метрики для анализа
    var_metrics = {
        'historical_var': historical_var,
        'parametric_var': parametric_var,
        'monte_carlo_var': monte_carlo_var,
        'mean_return': mean_return,
        'std_return': std_return,
        'confidence_level': confidence_level,
        'time_horizon': time_horizon,
        'var_consistency': np.std([historical_var, parametric_var, monte_carlo_var])
    }
    
    return var_metrics

def calculate_expected_shortfall(returns, confidence_level=0.05):
    """
    Расчет Expected Shortfall (ES) или Conditional VaR (CVaR).
    
    Expected Shortfall - это средняя потеря в худших случаях, когда
    потери превышают VaR. Это более консервативная мера риска, чем VaR,
    так как учитывает не только квантиль, но и распределение в хвосте.
    
    Args:
        returns (array-like): Массив доходностей портфеля
        confidence_level (float): Уровень доверия (по умолчанию 5%)
        
    Returns:
        float: Expected Shortfall
    """
    
    # Сначала рассчитываем VaR
    var_result = calculate_var(returns, confidence_level)
    var_value = var_result['historical_var']
    
    # Находим все доходности, которые хуже VaR (хвост распределения)
    returns_array = np.array(returns)
    tail_losses = returns_array[returns_array <= var_value]
    
    # Expected Shortfall - это среднее значение в хвосте
    if len(tail_losses) > 0:
        expected_shortfall = np.mean(tail_losses)
    else:
        # Если нет потерь хуже VaR, используем сам VaR
        expected_shortfall = var_value
    
    return expected_shortfall

def calculate_var_confidence_interval(returns, confidence_level=0.05, n_bootstrap=1000):
    """
    Расчет доверительного интервала для VaR с помощью бутстрапа.
    
    Бутстрап позволяет оценить неопределенность в расчете VaR,
    что важно для принятия решений о рисках.
    
    Args:
        returns (array-like): Массив доходностей портфеля
        confidence_level (float): Уровень доверия для VaR
        n_bootstrap (int): Количество бутстрап-выборок
        
    Returns:
        dict: Доверительный интервал VaR
    """
    
    returns_array = np.array(returns)
    bootstrap_vars = []
    
    # Генерация бутстрап-выборок
    for _ in range(n_bootstrap):
        # Случайная выборка с возвращением
        bootstrap_sample = np.random.choice(returns_array, size=len(returns_array), replace=True)
        bootstrap_var = np.percentile(bootstrap_sample, confidence_level * 100)
        bootstrap_vars.append(bootstrap_var)
    
    # Расчет доверительного интервала
    var_ci = {
        'var_mean': np.mean(bootstrap_vars),
        'var_std': np.std(bootstrap_vars),
        'var_5th_percentile': np.percentile(bootstrap_vars, 5),
        'var_95th_percentile': np.percentile(bootstrap_vars, 95),
        'var_median': np.median(bootstrap_vars)
    }
    
    return var_ci

# Пример использования VaR
def demonstrate_var_calculation():
    """
    Демонстрация расчета VaR с реальными данными.
    """
    print("=== Демонстрация расчета VaR ===")
    
    # Генерация реалистичных данных доходности
    np.random.seed(42)
    n_days = 252  # Один торговый год
    daily_returns = np.random.normal(0.0005, 0.02, n_days)  # 0.05% средняя доходность, 2% волатильность
    
    # Расчет VaR для разных уровней доверия
    confidence_levels = [0.01, 0.05, 0.10]  # 99%, 95%, 90% VaR
    
    print(f"📊 Анализ {n_days} дней торговли")
    print(f"📈 Средняя доходность: {np.mean(daily_returns)*100:.3f}%")
    print(f"📉 Волатильность: {np.std(daily_returns)*100:.3f}%")
    print()
    
    for cl in confidence_levels:
        var_result = calculate_var(daily_returns, cl)
        
        print(f"🎯 VaR {int((1-cl)*100)}% (1 день):")
        print(f"   Исторический: {var_result['historical_var']*100:.3f}%")
        print(f"   Параметрический: {var_result['parametric_var']*100:.3f}%")
        print(f"   Монте-Карло: {var_result['monte_carlo_var']*100:.3f}%")
        print()
    
    # Расчет Expected Shortfall
    es_95 = calculate_expected_shortfall(daily_returns, 0.05)
    print(f"⚠️ Expected Shortfall 95%: {es_95*100:.3f}%")
    
    # Доверительный интервал VaR
    var_ci = calculate_var_confidence_interval(daily_returns, 0.05)
    print(f"📊 Доверительный интервал VaR 95%:")
    print(f"   Среднее: {var_ci['var_mean']*100:.3f}%")
    print(f"   Стандартное отклонение: {var_ci['var_std']*100:.3f}%")
    print(f"   5%-95% интервал: {var_ci['var_5th_percentile']*100:.3f}% - {var_ci['var_95th_percentile']*100:.3f}%")
    
    return {
        'daily_returns': daily_returns,
        'var_results': {f'var_{int((1-cl)*100)}': calculate_var(daily_returns, cl) for cl in confidence_levels},
        'expected_shortfall': es_95,
        'var_confidence_interval': var_ci
    }

# Запуск демонстрации
if __name__ == "__main__":
    var_demo_results = demonstrate_var_calculation()
```

### 2. Maximum Drawdown Control

**Теория:** Maximum Drawdown (MDD) - это максимальная потеря от пика до минимума за определенный период. Это одна из самых важных метрик риска, так как показывает максимальную просадку, которую может выдержать портфель. Контроль просадки критически важен для сохранения капитала и психологического комфорта трейдера.

**Ключевые принципы контроля просадки:**
- **Пиковое отслеживание:** Постоянное отслеживание максимального достигнутого капитала
- **Пороговые значения:** Установка уровней предупреждения и критической просадки
- **Адаптивное сокращение:** Уменьшение размера позиций при увеличении просадки
- **Эмоциональная защита:** Предотвращение принятия решений под влиянием больших потерь

**Почему контроль просадки критичен:**
- Большие просадки могут уничтожить торговый счет
- Психологическое давление при больших потерях приводит к плохим решениям
- Восстановление после большой просадки требует экспоненциально больше времени
- Контроль просадки - основа выживания в долгосрочной перспективе

```python
class DrawdownController:
    """
    Класс для контроля максимальной просадки портфеля.
    
    Этот класс отслеживает просадку капитала и автоматически
    корректирует размер позиций для предотвращения катастрофических потерь.
    """
    
    def __init__(self, max_drawdown=0.15, drawdown_threshold=0.10):
        """
        Инициализация контроллера просадки.
        
        Args:
            max_drawdown (float): Максимально допустимая просадка (по умолчанию 15%)
            drawdown_threshold (float): Порог предупреждения о просадке (по умолчанию 10%)
        """
        self.max_drawdown = max_drawdown
        self.drawdown_threshold = drawdown_threshold
        self.peak_capital = 0
        self.current_drawdown = 0
        self.drawdown_history = []
        self.capital_history = []
    
    def update_capital(self, current_capital):
        """
        Обновление капитала и расчет текущей просадки.
        
        Просадка рассчитывается как процентное снижение от максимального
        достигнутого капитала. Это позволяет отслеживать, насколько
        текущий капитал отстает от пикового значения.
        
        Args:
            current_capital (float): Текущий капитал портфеля
        """
        
        # Обновление пика капитала
        if current_capital > self.peak_capital:
            self.peak_capital = current_capital
            self.current_drawdown = 0
        else:
            # Расчет текущей просадки
            if self.peak_capital > 0:
                self.current_drawdown = (self.peak_capital - current_capital) / self.peak_capital
            else:
                self.current_drawdown = 0
        
        # Сохранение истории для анализа
        self.capital_history.append(current_capital)
        self.drawdown_history.append(self.current_drawdown)
        
        # Ограничение размера истории (сохраняем последние 1000 записей)
        if len(self.capital_history) > 1000:
            self.capital_history = self.capital_history[-1000:]
            self.drawdown_history = self.drawdown_history[-1000:]
    
    def should_reduce_position(self):
        """
        Проверка необходимости сокращения позиций на основе текущей просадки.
        
        Система использует два уровня:
        1. Порог предупреждения - сигнализирует о приближении к опасной зоне
        2. Критический уровень - требует немедленного сокращения позиций
        
        Returns:
            tuple: (bool, str) - (нужно ли сокращать позиции, описание ситуации)
        """
        
        if self.current_drawdown > self.max_drawdown:
            return True, f"🚨 КРИТИЧНО: Просадка {self.current_drawdown:.1%} превышает максимум {self.max_drawdown:.1%}"
        elif self.current_drawdown > self.drawdown_threshold:
            return True, f"⚠️ ПРЕДУПРЕЖДЕНИЕ: Высокая просадка {self.current_drawdown:.1%} (порог {self.drawdown_threshold:.1%})"
        else:
            return False, f"✅ Просадка в норме: {self.current_drawdown:.1%}"
    
    def calculate_position_reduction(self, current_position_size):
        """
        Расчет нового размера позиции с учетом текущей просадки.
        
        Стратегия сокращения позиций:
        - При критической просадке: полное закрытие позиций
        - При высокой просадке: сокращение на 50%
        - При нормальной просадке: без изменений
        
        Args:
            current_position_size (float): Текущий размер позиции
            
        Returns:
            float: Новый рекомендуемый размер позиции
        """
        
        if self.current_drawdown > self.max_drawdown:
            # Критическая просадка - закрываем все позиции
            return 0
        elif self.current_drawdown > self.drawdown_threshold:
            # Высокая просадка - сокращаем позиции на 50%
            return current_position_size * 0.5
        else:
            # Нормальная просадка - без изменений
            return current_position_size
    
    def get_maximum_drawdown(self):
        """
        Получение максимальной просадки за весь период.
        
        Returns:
            float: Максимальная просадка в долях
        """
        return max(self.drawdown_history) if self.drawdown_history else 0
    
    def get_drawdown_duration(self):
        """
        Расчет продолжительности текущей просадки.
        
        Returns:
            int: Количество периодов в текущей просадке
        """
        if not self.drawdown_history:
            return 0
        
        # Ищем последний раз, когда просадка была равна 0
        duration = 0
        for i in range(len(self.drawdown_history) - 1, -1, -1):
            if self.drawdown_history[i] == 0:
                break
            duration += 1
        
        return duration
    
    def get_recovery_factor(self):
        """
        Расчет фактора восстановления (отношение прибыли к максимальной просадке).
        
        Returns:
            float: Фактор восстановления
        """
        max_dd = self.get_maximum_drawdown()
        if max_dd == 0:
            return float('inf')
        
        # Прибыль = текущий капитал - начальный капитал
        if self.capital_history:
            total_return = (self.capital_history[-1] - self.capital_history[0]) / self.capital_history[0]
            return total_return / max_dd
        
        return 0

# Пример использования DrawdownController
def demonstrate_drawdown_control():
    """
    Демонстрация работы DrawdownController с симуляцией торговли.
    """
    print("=== Демонстрация контроля просадки ===")
    
    # Создание контроллера просадки
    dd_controller = DrawdownController(
        max_drawdown=0.20,      # Максимальная просадка 20%
        drawdown_threshold=0.10  # Порог предупреждения 10%
    )
    
    # Симуляция торговли с различными сценариями
    initial_capital = 10000
    current_capital = initial_capital
    
    # Сценарий 1: Успешная торговля с ростом капитала
    print("\n📈 Сценарий 1: Рост капитала")
    for i in range(10):
        current_capital *= (1 + np.random.normal(0.01, 0.02))  # 1% средняя доходность, 2% волатильность
        dd_controller.update_capital(current_capital)
        
        should_reduce, message = dd_controller.should_reduce_position()
        print(f"День {i+1}: Капитал ${current_capital:.2f}, Просадка {dd_controller.current_drawdown:.1%} - {message}")
    
    # Сценарий 2: Период просадки
    print("\n📉 Сценарий 2: Период просадки")
    for i in range(15):
        current_capital *= (1 + np.random.normal(-0.005, 0.03))  # -0.5% средняя доходность, 3% волатильность
        dd_controller.update_capital(current_capital)
        
        should_reduce, message = dd_controller.should_reduce_position()
        position_size = dd_controller.calculate_position_reduction(1000)  # Предполагаемый размер позиции
        
        print(f"День {i+1}: Капитал ${current_capital:.2f}, Просадка {dd_controller.current_drawdown:.1%}")
        print(f"         {message}")
        print(f"         Рекомендуемый размер позиции: ${position_size:.2f}")
        print()
    
    # Анализ результатов
    print("📊 Анализ результатов:")
    print(f"   Начальный капитал: ${initial_capital:.2f}")
    print(f"   Финальный капитал: ${current_capital:.2f}")
    print(f"   Общая доходность: {((current_capital/initial_capital)-1)*100:.2f}%")
    print(f"   Максимальная просадка: {dd_controller.get_maximum_drawdown()*100:.2f}%")
    print(f"   Продолжительность текущей просадки: {dd_controller.get_drawdown_duration()} дней")
    print(f"   Фактор восстановления: {dd_controller.get_recovery_factor():.2f}")
    
    return {
        'initial_capital': initial_capital,
        'final_capital': current_capital,
        'max_drawdown': dd_controller.get_maximum_drawdown(),
        'recovery_factor': dd_controller.get_recovery_factor()
    }

# Запуск демонстрации
if __name__ == "__main__":
    dd_demo_results = demonstrate_drawdown_control()
```

### 3. Correlation Risk Management

**Теория:** Корреляционный риск возникает, когда активы в портфеле движутся в одном направлении, что снижает эффект диверсификации. Высокая корреляция между позициями означает, что при неблагоприятном движении рынка все позиции могут понести потери одновременно, что значительно увеличивает общий риск портфеля.

**Ключевые принципы управления корреляционным риском:**
- **Мониторинг корреляций:** Постоянное отслеживание корреляций между активами
- **Лимиты корреляции:** Установка максимально допустимых уровней корреляции
- **Диверсификация:** Выбор активов с низкой корреляцией
- **Оптимизация портфеля:** Использование математических методов для оптимизации весов

**Почему корреляционный риск важен:**
- Высокая корреляция снижает эффективность диверсификации
- В кризисные периоды корреляции между активами часто увеличиваются
- Неправильная оценка корреляций может привести к концентрации рисков
- Управление корреляциями - основа современной портфельной теории

```python
class CorrelationRiskManager:
    """
    Класс для управления корреляционными рисками в портфеле.
    
    Этот класс отслеживает корреляции между активами и помогает
    оптимизировать портфель для минимизации корреляционных рисков.
    """
    
    def __init__(self, max_correlation=0.7, max_positions=5):
        """
        Инициализация менеджера корреляционных рисков.
        
        Args:
            max_correlation (float): Максимально допустимая корреляция (по умолчанию 0.7)
            max_positions (int): Максимальное количество позиций в портфеле
        """
        self.max_correlation = max_correlation
        self.max_positions = max_positions
        self.current_positions = {}
        self.correlation_matrix = None
        self.asset_returns = {}
    
    def add_asset_data(self, asset_name, returns_data):
        """
        Добавление исторических данных по активу для расчета корреляций.
        
        Args:
            asset_name (str): Название актива
            returns_data (array-like): Массив доходностей актива
        """
        self.asset_returns[asset_name] = np.array(returns_data)
        self._update_correlation_matrix()
    
    def _update_correlation_matrix(self):
        """Обновление матрицы корреляций между всеми активами."""
        if len(self.asset_returns) < 2:
            return
        
        # Создание DataFrame для удобного расчета корреляций
        returns_df = pd.DataFrame(self.asset_returns)
        self.correlation_matrix = returns_df.corr()
    
    def check_correlation(self, new_asset, existing_positions):
        """
        Проверка корреляции нового актива с существующими позициями.
        
        Args:
            new_asset (str): Название нового актива
            existing_positions (dict): Словарь существующих позиций
            
        Returns:
            tuple: (bool, str) - (можно ли добавить актив, описание)
        """
        
        if new_asset not in self.asset_returns:
            return False, f"❌ Нет данных по активу {new_asset}"
        
        correlations = []
        
        for asset, position in existing_positions.items():
            if asset in self.asset_returns:
                # Расчет корреляции между активами
                correlation = self.calculate_correlation(new_asset, asset)
                correlations.append(correlation)
        
        if not correlations:
            return True, "✅ Нет существующих позиций для сравнения"
        
        max_correlation = max(correlations)
        avg_correlation = np.mean(correlations)
        
        if max_correlation > self.max_correlation:
            return False, f"❌ Высокая корреляция: {max_correlation:.3f} (максимум {self.max_correlation})"
        elif avg_correlation > self.max_correlation * 0.8:
            return True, f"⚠️ Средняя корреляция: {avg_correlation:.3f} (близко к лимиту)"
        else:
            return True, f"✅ Корреляция в норме: {avg_correlation:.3f}"
    
    def calculate_correlation(self, asset1, asset2):
        """
        Расчет корреляции между двумя активами.
        
        Args:
            asset1 (str): Название первого актива
            asset2 (str): Название второго актива
            
        Returns:
            float: Коэффициент корреляции Пирсона
        """
        
        if asset1 not in self.asset_returns or asset2 not in self.asset_returns:
            return 0.0
        
        returns1 = self.asset_returns[asset1]
        returns2 = self.asset_returns[asset2]
        
        # Проверка на одинаковую длину данных
        min_length = min(len(returns1), len(returns2))
        if min_length < 2:
            return 0.0
        
        returns1 = returns1[:min_length]
        returns2 = returns2[:min_length]
        
        # Расчет корреляции Пирсона
        correlation = np.corrcoef(returns1, returns2)[0, 1]
        
        # Обработка NaN значений
        if np.isnan(correlation):
            return 0.0
        
        return correlation
    
    def get_portfolio_correlation_metrics(self, positions):
        """
        Получение метрик корреляции для всего портфеля.
        
        Args:
            positions (dict): Словарь позиций в портфеле
            
        Returns:
            dict: Метрики корреляции портфеля
        """
        
        if len(positions) < 2:
            return {
                'avg_correlation': 0,
                'max_correlation': 0,
                'min_correlation': 0,
                'correlation_risk_score': 0
            }
        
        correlations = []
        asset_names = list(positions.keys())
        
        # Расчет всех попарных корреляций
        for i in range(len(asset_names)):
            for j in range(i + 1, len(asset_names)):
                corr = self.calculate_correlation(asset_names[i], asset_names[j])
                correlations.append(abs(corr))  # Используем абсолютное значение
        
        if not correlations:
            return {
                'avg_correlation': 0,
                'max_correlation': 0,
                'min_correlation': 0,
                'correlation_risk_score': 0
            }
        
        # Расчет метрик
        avg_correlation = np.mean(correlations)
        max_correlation = np.max(correlations)
        min_correlation = np.min(correlations)
        
        # Оценка риска корреляции (0-1, где 1 - максимальный риск)
        correlation_risk_score = min(avg_correlation / self.max_correlation, 1.0)
        
        return {
            'avg_correlation': avg_correlation,
            'max_correlation': max_correlation,
            'min_correlation': min_correlation,
            'correlation_risk_score': correlation_risk_score,
            'high_correlation_pairs': len([c for c in correlations if c > self.max_correlation])
        }
    
    def optimize_portfolio_weights(self, assets, expected_returns, cov_matrix, risk_tolerance=0.5):
        """
        Оптимизация весов портфеля с учетом корреляций.
        
        Использует современную портфельную теорию Марковица для нахождения
        оптимального распределения весов, которое максимизирует отношение
        доходность/риск с учетом корреляций между активами.
        
        Args:
            assets (list): Список активов
            expected_returns (array): Ожидаемые доходности
            cov_matrix (array): Ковариационная матрица
            risk_tolerance (float): Толерантность к риску (0-1)
            
        Returns:
            array: Оптимальные веса портфеля
        """
        
        n_assets = len(assets)
        
        def portfolio_variance(weights):
            """Функция дисперсии портфеля."""
            return np.dot(weights.T, np.dot(cov_matrix, weights))
        
        def portfolio_return(weights):
            """Функция доходности портфеля."""
            return np.sum(expected_returns * weights)
        
        def objective_function(weights):
            """Целевая функция: максимизация отношения доходность/риск."""
            portfolio_ret = portfolio_return(weights)
            portfolio_var = portfolio_variance(weights)
            
            # Шарп-подобное отношение с учетом толерантности к риску
            if portfolio_var > 0:
                return -(portfolio_ret - risk_tolerance * portfolio_var)
            else:
                return -portfolio_ret
        
        # Ограничения
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # Сумма весов = 1
        bounds = tuple((0, 1) for _ in range(n_assets))  # Веса от 0 до 1
        
        # Начальные веса (равномерное распределение)
        initial_weights = np.array([1/n_assets] * n_assets)
        
        # Оптимизация
        result = minimize(
            objective_function, 
            initial_weights, 
            method='SLSQP', 
            bounds=bounds, 
            constraints=constraints,
            options={'maxiter': 1000}
        )
        
        if result.success:
            return result.x
        else:
            # Если оптимизация не удалась, возвращаем равномерные веса
            return initial_weights
    
    def suggest_diversification(self, current_positions):
        """
        Предложение по диверсификации портфеля.
        
        Args:
            current_positions (dict): Текущие позиции
            
        Returns:
            dict: Рекомендации по диверсификации
        """
        
        metrics = self.get_portfolio_correlation_metrics(current_positions)
        suggestions = []
        
        if metrics['correlation_risk_score'] > 0.8:
            suggestions.append("🚨 КРИТИЧНО: Очень высокая корреляция в портфеле")
            suggestions.append("   Рекомендуется добавить активы с низкой корреляцией")
        elif metrics['correlation_risk_score'] > 0.6:
            suggestions.append("⚠️ ВНИМАНИЕ: Высокая корреляция в портфеле")
            suggestions.append("   Рассмотрите возможность диверсификации")
        
        if metrics['high_correlation_pairs'] > 0:
            suggestions.append(f"   Найдено {metrics['high_correlation_pairs']} пар с высокой корреляцией")
        
        if len(current_positions) < 3:
            suggestions.append("💡 Рекомендация: Добавьте больше активов для диверсификации")
        
        return {
            'risk_level': 'HIGH' if metrics['correlation_risk_score'] > 0.8 else 
                         'MEDIUM' if metrics['correlation_risk_score'] > 0.6 else 'LOW',
            'suggestions': suggestions,
            'metrics': metrics
        }

# Пример использования CorrelationRiskManager
def demonstrate_correlation_risk_management():
    """
    Демонстрация работы CorrelationRiskManager с реальными данными.
    """
    print("=== Демонстрация управления корреляционными рисками ===")
    
    # Создание менеджера корреляционных рисков
    corr_manager = CorrelationRiskManager(
        max_correlation=0.6,  # Максимальная корреляция 60%
        max_positions=5       # Максимум 5 позиций
    )
    
    # Генерация исторических данных для различных активов
    np.random.seed(42)
    n_days = 252
    
    # Активы с разной корреляцией
    assets_data = {
        'EURUSD': np.random.normal(0.0001, 0.01, n_days),  # Валютная пара
        'GBPUSD': np.random.normal(0.0001, 0.01, n_days),  # Валютная пара (высокая корреляция с EURUSD)
        'GOLD': np.random.normal(0.0002, 0.015, n_days),   # Золото (низкая корреляция с валютами)
        'OIL': np.random.normal(0.0003, 0.02, n_days),     # Нефть (средняя корреляция)
        'BOND': np.random.normal(0.00005, 0.005, n_days)   # Облигации (отрицательная корреляция)
    }
    
    # Добавление корреляций между активами
    # EURUSD и GBPUSD имеют высокую корреляцию
    assets_data['GBPUSD'] = 0.7 * assets_data['EURUSD'] + 0.3 * np.random.normal(0.0001, 0.01, n_days)
    
    # Добавление данных в менеджер
    for asset, returns in assets_data.items():
        corr_manager.add_asset_data(asset, returns)
    
    print("📊 Анализ корреляций между активами:")
    print(corr_manager.correlation_matrix.round(3))
    print()
    
    # Симуляция добавления позиций
    current_positions = {}
    
    print("🔄 Симуляция добавления позиций:")
    
    for asset in ['EURUSD', 'GBPUSD', 'GOLD', 'OIL', 'BOND']:
        can_add, message = corr_manager.check_correlation(asset, current_positions)
        print(f"Добавление {asset}: {message}")
        
        if can_add and len(current_positions) < corr_manager.max_positions:
            current_positions[asset] = 1000  # Размер позиции
            print(f"   ✅ {asset} добавлен в портфель")
        else:
            print(f"   ❌ {asset} не добавлен")
        print()
    
    # Анализ портфеля
    print("📈 Анализ текущего портфеля:")
    portfolio_metrics = corr_manager.get_portfolio_correlation_metrics(current_positions)
    
    print(f"   Средняя корреляция: {portfolio_metrics['avg_correlation']:.3f}")
    print(f"   Максимальная корреляция: {portfolio_metrics['max_correlation']:.3f}")
    print(f"   Оценка риска: {portfolio_metrics['correlation_risk_score']:.3f}")
    print(f"   Пар с высокой корреляцией: {portfolio_metrics['high_correlation_pairs']}")
    print()
    
    # Рекомендации по диверсификации
    diversification = corr_manager.suggest_diversification(current_positions)
    print(f"🎯 Рекомендации по диверсификации:")
    print(f"   Уровень риска: {diversification['risk_level']}")
    for suggestion in diversification['suggestions']:
        print(f"   {suggestion}")
    
    return {
        'current_positions': current_positions,
        'portfolio_metrics': portfolio_metrics,
        'diversification_suggestions': diversification
    }

# Запуск демонстрации
if __name__ == "__main__":
    corr_demo_results = demonstrate_correlation_risk_management()
```

## Динамическое управление рисками

**Теория:** Динамическое управление рисками адаптирует параметры риска в зависимости от текущих рыночных условий. В отличие от статических подходов, динамические системы могут изменять свою агрессивность в зависимости от волатильности, трендов и других рыночных факторов.

### 1. Адаптивные лимиты

**Теория:** Адаптивные лимиты автоматически корректируют размеры позиций и уровни риска в зависимости от текущей волатильности рынка. Это позволяет быть более агрессивными в спокойные периоды и более консервативными в нестабильные времена.

**Ключевые принципы адаптивных лимитов:**
- **Волатильность-адаптация:** Уменьшение риска при высокой волатильности
- **Тренд-адаптация:** Увеличение риска в благоприятных трендах
- **Исторический анализ:** Использование исторических данных для прогнозирования
- **Плавные переходы:** Избежание резких изменений в стратегии

**Почему адаптивные лимиты эффективны:**
- Учитывают текущие рыночные условия
- Предотвращают переторговлю в нестабильные периоды
- Максимизируют использование благоприятных условий
- Снижают эмоциональное влияние на принятие решений

```python
class AdaptiveRiskManager:
    """
    Класс для адаптивного управления рисками на основе рыночных условий.
    
    Этот класс динамически корректирует параметры риска в зависимости
    от волатильности, трендов и других рыночных факторов.
    """
    
    def __init__(self, base_risk=0.02, volatility_lookback=20, trend_lookback=50):
        """
        Инициализация адаптивного менеджера рисков.
        
        Args:
            base_risk (float): Базовый уровень риска (по умолчанию 2%)
            volatility_lookback (int): Период для расчета волатильности (по умолчанию 20 дней)
            trend_lookback (int): Период для анализа тренда (по умолчанию 50 дней)
        """
        self.base_risk = base_risk
        self.volatility_lookback = volatility_lookback
        self.trend_lookback = trend_lookback
        self.risk_history = []
        self.volatility_history = []
        self.trend_history = []
    
    def calculate_adaptive_risk(self, returns):
        """
        Расчет адаптивного уровня риска на основе текущих рыночных условий.
        
        Метод использует несколько факторов:
        1. Текущая волатильность (чем выше, тем меньше риск)
        2. Направление тренда (благоприятный тренд увеличивает риск)
        3. Стабильность волатильности (стабильная волатильность увеличивает риск)
        4. Исторические паттерны (адаптация на основе прошлых результатов)
        
        Args:
            returns (array-like): Массив доходностей для анализа
            
        Returns:
            float: Адаптивный уровень риска
        """
        
        returns_array = np.array(returns)
        
        # 1. Расчет текущей волатильности
        if len(returns_array) >= self.volatility_lookback:
            current_volatility = returns_array[-self.volatility_lookback:].std()
        else:
            current_volatility = returns_array.std() if len(returns_array) > 0 else 0.02
        
        # 2. Расчет тренда
        if len(returns_array) >= self.trend_lookback:
            trend_returns = returns_array[-self.trend_lookback:]
            trend_strength = np.mean(trend_returns) / np.std(trend_returns) if np.std(trend_returns) > 0 else 0
        else:
            trend_strength = 0
        
        # 3. Расчет стабильности волатильности
        if len(self.volatility_history) >= 10:
            volatility_stability = 1 / (1 + np.std(self.volatility_history[-10:]))
        else:
            volatility_stability = 1.0
        
        # 4. Адаптация базового риска
        # Волатильность-адаптация (обратная зависимость)
        volatility_factor = 1 / (1 + current_volatility * 20)
        
        # Тренд-адаптация (прямая зависимость)
        trend_factor = 1 + min(trend_strength * 0.1, 0.5)  # Максимум +50%
        
        # Стабильность-адаптация
        stability_factor = volatility_stability
        
        # Финальный адаптивный риск
        adaptive_risk = (self.base_risk * 
                        volatility_factor * 
                        trend_factor * 
                        stability_factor)
        
        # Ограничения для безопасности
        adaptive_risk = max(0.005, min(adaptive_risk, 0.05))  # От 0.5% до 5%
        
        # Сохранение истории
        self.volatility_history.append(current_volatility)
        self.trend_history.append(trend_strength)
        self.risk_history.append(adaptive_risk)
        
        # Ограничение размера истории
        if len(self.risk_history) > 100:
            self.risk_history = self.risk_history[-100:]
            self.volatility_history = self.volatility_history[-100:]
            self.trend_history = self.trend_history[-100:]
        
        return adaptive_risk
    
    def get_risk_metrics(self):
        """
        Получение метрик адаптивного управления рисками.
        
        Returns:
            dict: Словарь с метриками риска
        """
        
        if not self.risk_history:
            return {
                'current_risk': self.base_risk,
                'avg_risk': self.base_risk,
                'risk_volatility': 0,
                'adaptation_factor': 1.0
            }
        
        current_risk = self.risk_history[-1]
        avg_risk = np.mean(self.risk_history)
        risk_volatility = np.std(self.risk_history)
        adaptation_factor = current_risk / self.base_risk
        
        return {
            'current_risk': current_risk,
            'avg_risk': avg_risk,
            'risk_volatility': risk_volatility,
            'adaptation_factor': adaptation_factor,
            'volatility_trend': np.mean(self.volatility_history[-5:]) if len(self.volatility_history) >= 5 else 0,
            'trend_strength': np.mean(self.trend_history[-5:]) if len(self.trend_history) >= 5 else 0
        }
    
    def should_increase_risk(self, returns, min_periods=10):
        """
        Определение, следует ли увеличить риск на основе исторических результатов.
        
        Args:
            returns (array-like): Массив доходностей
            min_periods (int): Минимальное количество периодов для анализа
            
        Returns:
            bool: Следует ли увеличить риск
        """
        
        if len(returns) < min_periods:
            return False
        
        recent_returns = returns[-min_periods:]
        
        # Критерии для увеличения риска:
        # 1. Положительная средняя доходность
        # 2. Низкая волатильность
        # 3. Стабильные результаты
        
        avg_return = np.mean(recent_returns)
        volatility = np.std(recent_returns)
        sharpe_ratio = avg_return / volatility if volatility > 0 else 0
        
        # Увеличиваем риск, если:
        # - Положительная доходность
        # - Высокий коэффициент Шарпа
        # - Низкая волатильность
        return (avg_return > 0 and 
                sharpe_ratio > 0.5 and 
                volatility < 0.02)
    
    def calculate_position_size(self, account_balance, current_volatility, confidence_level=0.95):
        """
        Расчет размера позиции с учетом адаптивного риска.
        
        Args:
            account_balance (float): Баланс счета
            current_volatility (float): Текущая волатильность
            confidence_level (float): Уровень доверия
            
        Returns:
            float: Рекомендуемый размер позиции
        """
        
        # Получение адаптивного риска
        adaptive_risk = self.calculate_adaptive_risk([current_volatility])
        
        # Расчет размера позиции на основе риска
        position_size = account_balance * adaptive_risk
        
        # Дополнительная корректировка на волатильность
        volatility_adjustment = 1 / (1 + current_volatility * 10)
        position_size *= volatility_adjustment
        
        return position_size

# Пример использования AdaptiveRiskManager
def demonstrate_adaptive_risk_management():
    """
    Демонстрация работы AdaptiveRiskManager с различными рыночными условиями.
    """
    print("=== Демонстрация адаптивного управления рисками ===")
    
    # Создание адаптивного менеджера рисков
    adaptive_manager = AdaptiveRiskManager(
        base_risk=0.02,           # Базовый риск 2%
        volatility_lookback=20,   # 20 дней для волатильности
        trend_lookback=50         # 50 дней для тренда
    )
    
    # Симуляция различных рыночных условий
    np.random.seed(42)
    n_days = 100
    
    # Сценарий 1: Низкая волатильность, восходящий тренд
    print("\n📈 Сценарий 1: Низкая волатильность, восходящий тренд")
    low_vol_returns = np.random.normal(0.001, 0.01, 30)  # 0.1% средняя доходность, 1% волатильность
    
    for i, return_val in enumerate(low_vol_returns):
        adaptive_risk = adaptive_manager.calculate_adaptive_risk(low_vol_returns[:i+1])
        print(f"День {i+1}: Доходность {return_val*100:.2f}%, Адаптивный риск {adaptive_risk*100:.2f}%")
    
    # Сценарий 2: Высокая волатильность, нисходящий тренд
    print("\n📉 Сценарий 2: Высокая волатильность, нисходящий тренд")
    high_vol_returns = np.random.normal(-0.002, 0.03, 30)  # -0.2% средняя доходность, 3% волатильность
    
    for i, return_val in enumerate(high_vol_returns):
        adaptive_risk = adaptive_manager.calculate_adaptive_risk(high_vol_returns[:i+1])
        print(f"День {i+1}: Доходность {return_val*100:.2f}%, Адаптивный риск {adaptive_risk*100:.2f}%")
    
    # Сценарий 3: Переменная волатильность
    print("\n🌊 Сценарий 3: Переменная волатильность")
    variable_returns = []
    for i in range(30):
        if i < 10:  # Низкая волатильность
            vol = 0.01
            mean = 0.001
        elif i < 20:  # Высокая волатильность
            vol = 0.03
            mean = -0.001
        else:  # Средняя волатильность
            vol = 0.02
            mean = 0.0005
        
        return_val = np.random.normal(mean, vol)
        variable_returns.append(return_val)
        
        adaptive_risk = adaptive_manager.calculate_adaptive_risk(variable_returns)
        print(f"День {i+1}: Доходность {return_val*100:.2f}%, Адаптивный риск {adaptive_risk*100:.2f}%")
    
    # Анализ результатов
    print("\n📊 Анализ адаптивного управления рисками:")
    metrics = adaptive_manager.get_risk_metrics()
    
    print(f"   Текущий риск: {metrics['current_risk']*100:.2f}%")
    print(f"   Средний риск: {metrics['avg_risk']*100:.2f}%")
    print(f"   Волатильность риска: {metrics['risk_volatility']*100:.2f}%")
    print(f"   Фактор адаптации: {metrics['adaptation_factor']:.2f}")
    print(f"   Тренд волатильности: {metrics['volatility_trend']*100:.2f}%")
    print(f"   Сила тренда: {metrics['trend_strength']:.3f}")
    
    return {
        'adaptive_risk_history': adaptive_manager.risk_history,
        'volatility_history': adaptive_manager.volatility_history,
        'trend_history': adaptive_manager.trend_history,
        'final_metrics': metrics
    }

# Запуск демонстрации
if __name__ == "__main__":
    adaptive_demo_results = demonstrate_adaptive_risk_management()
```

### 2. Machine Learning Risk Management

**Теория:** Машинное обучение в управлении рисками использует алгоритмы для предсказания и оценки рисков на основе исторических данных и рыночных признаков. ML-подходы могут выявлять сложные паттерны и взаимосвязи, которые трудно обнаружить традиционными методами.

**Ключевые принципы ML-управления рисками:**
- **Извлечение признаков:** Создание информативных признаков из рыночных данных
- **Обучение моделей:** Использование исторических данных для обучения алгоритмов
- **Предсказание рисков:** Прогнозирование будущих рисков на основе текущих условий
- **Адаптация:** Постоянное обновление моделей с новыми данными

**Почему ML эффективен в управлении рисками:**
- Может обрабатывать большие объемы данных
- Выявляет нелинейные зависимости между переменными
- Адаптируется к изменяющимся рыночным условиям
- Может комбинировать множество различных источников информации

```python
class MLRiskManager:
    """
    Класс для управления рисками с использованием машинного обучения.
    
    Этот класс использует ML-алгоритмы для предсказания рисков на основе
    рыночных данных и исторических паттернов.
    """
    
    def __init__(self, model=None, feature_scaler=None):
        """
        Инициализация ML-менеджера рисков.
        
        Args:
            model: Обученная ML-модель (по умолчанию None)
            feature_scaler: Скалер для нормализации признаков (по умолчанию None)
        """
        self.model = model
        self.feature_scaler = feature_scaler or StandardScaler()
        self.risk_features = []
        self.risk_labels = []
        self.feature_names = []
        self.model_performance = {}
    
    def extract_risk_features(self, market_data):
        """
        Извлечение признаков для ML-модели риска.
        
        Создает комплексный набор признаков, включающий:
        - Статистические характеристики доходности
        - Технические индикаторы
        - Объемные характеристики
        - Временные паттерны
        
        Args:
            market_data (dict): Словарь с рыночными данными
            
        Returns:
            dict: Словарь с извлеченными признаками
        """
        
        # Базовые статистические признаки
        returns = market_data.get('returns', [])
        if len(returns) == 0:
            returns = np.diff(market_data.get('close', [1, 1])) / market_data.get('close', [1, 1])[:-1]
        
        features = {
            # Статистические характеристики
            'volatility': np.std(returns) if len(returns) > 0 else 0,
            'skewness': self._calculate_skewness(returns),
            'kurtosis': self._calculate_kurtosis(returns),
            'mean_return': np.mean(returns) if len(returns) > 0 else 0,
            'median_return': np.median(returns) if len(returns) > 0 else 0,
            
            # Объемные характеристики
            'volume_ratio': self._calculate_volume_ratio(market_data),
            'volume_volatility': self._calculate_volume_volatility(market_data),
            
            # Ценовые характеристики
            'price_momentum_5': self._calculate_momentum(market_data, 5),
            'price_momentum_20': self._calculate_momentum(market_data, 20),
            'price_volatility_5': self._calculate_price_volatility(market_data, 5),
            'price_volatility_20': self._calculate_price_volatility(market_data, 20),
            
            # Технические индикаторы
            'rsi': self._calculate_rsi(market_data),
            'macd': self._calculate_macd(market_data),
            'bollinger_position': self._calculate_bollinger_position(market_data),
            
            # Временные признаки
            'day_of_week': self._get_day_of_week(market_data),
            'hour_of_day': self._get_hour_of_day(market_data),
            'is_weekend': self._is_weekend(market_data),
            
            # Рисковые метрики
            'var_95': self._calculate_var(returns, 0.05),
            'max_drawdown': self._calculate_max_drawdown(returns),
            'sharpe_ratio': self._calculate_sharpe_ratio(returns),
            
            # Корреляционные признаки
            'autocorrelation': self._calculate_autocorrelation(returns),
            'trend_strength': self._calculate_trend_strength(returns)
        }
        
        return features
    
    def _calculate_skewness(self, returns):
        """Расчет асимметрии распределения доходности."""
        if len(returns) < 3:
            return 0
        return stats.skew(returns)
    
    def _calculate_kurtosis(self, returns):
        """Расчет эксцесса распределения доходности."""
        if len(returns) < 4:
            return 0
        return stats.kurtosis(returns)
    
    def _calculate_volume_ratio(self, market_data):
        """Расчет отношения текущего объема к среднему."""
        volume = market_data.get('volume', [])
        if len(volume) < 2:
            return 1.0
        return volume[-1] / np.mean(volume[:-1]) if np.mean(volume[:-1]) > 0 else 1.0
    
    def _calculate_volume_volatility(self, market_data):
        """Расчет волатильности объема."""
        volume = market_data.get('volume', [])
        if len(volume) < 2:
            return 0
        return np.std(volume) / np.mean(volume) if np.mean(volume) > 0 else 0
    
    def _calculate_momentum(self, market_data, period):
        """Расчет ценового импульса."""
        close = market_data.get('close', [])
        if len(close) < period + 1:
            return 0
        return (close[-1] / close[-period-1] - 1) if close[-period-1] > 0 else 0
    
    def _calculate_price_volatility(self, market_data, period):
        """Расчет волатильности цены за период."""
        close = market_data.get('close', [])
        if len(close) < period + 1:
            return 0
        returns = np.diff(close[-period-1:]) / close[-period-1:-1]
        return np.std(returns) if len(returns) > 0 else 0
    
    def _calculate_rsi(self, market_data, period=14):
        """Расчет RSI (Relative Strength Index)."""
        close = market_data.get('close', [])
        if len(close) < period + 1:
            return 50
        
        deltas = np.diff(close)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gains = np.mean(gains[-period:])
        avg_losses = np.mean(losses[-period:])
        
        if avg_losses == 0:
            return 100
        
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, market_data, fast=12, slow=26, signal=9):
        """Расчет MACD (Moving Average Convergence Divergence)."""
        close = market_data.get('close', [])
        if len(close) < slow:
            return 0
        
        close_series = pd.Series(close)
        ema_fast = close_series.ewm(span=fast).mean()
        ema_slow = close_series.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        
        return macd_line.iloc[-1] if not macd_line.empty else 0
    
    def _calculate_bollinger_position(self, market_data, period=20, std_dev=2):
        """Расчет позиции цены относительно полос Боллинджера."""
        close = market_data.get('close', [])
        if len(close) < period:
            return 0.5
        
        close_series = pd.Series(close)
        sma = close_series.rolling(window=period).mean()
        std = close_series.rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        current_price = close[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        
        if current_upper == current_lower:
            return 0.5
        
        return (current_price - current_lower) / (current_upper - current_lower)
    
    def _get_day_of_week(self, market_data):
        """Получение дня недели."""
        timestamp = market_data.get('timestamp')
        if timestamp is None:
            return 0
        if isinstance(timestamp, str):
            timestamp = pd.to_datetime(timestamp)
        return timestamp.weekday()
    
    def _get_hour_of_day(self, market_data):
        """Получение часа дня."""
        timestamp = market_data.get('timestamp')
        if timestamp is None:
            return 12
        if isinstance(timestamp, str):
            timestamp = pd.to_datetime(timestamp)
        return timestamp.hour
    
    def _is_weekend(self, market_data):
        """Проверка, является ли день выходным."""
        timestamp = market_data.get('timestamp')
        if timestamp is None:
            return False
        if isinstance(timestamp, str):
            timestamp = pd.to_datetime(timestamp)
        return timestamp.weekday() >= 5
    
    def _calculate_var(self, returns, confidence_level):
        """Расчет Value at Risk."""
        if len(returns) == 0:
            return 0
        return np.percentile(returns, confidence_level * 100)
    
    def _calculate_max_drawdown(self, returns):
        """Расчет максимальной просадки."""
        if len(returns) == 0:
            return 0
        
        cumulative = np.cumprod(1 + returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        return np.min(drawdown)
    
    def _calculate_sharpe_ratio(self, returns, risk_free_rate=0.0001):
        """Расчет коэффициента Шарпа."""
        if len(returns) == 0 or np.std(returns) == 0:
            return 0
        return (np.mean(returns) - risk_free_rate) / np.std(returns)
    
    def _calculate_autocorrelation(self, returns, lag=1):
        """Расчет автокорреляции."""
        if len(returns) < lag + 1:
            return 0
        return np.corrcoef(returns[:-lag], returns[lag:])[0, 1] if len(returns) > lag else 0
    
    def _calculate_trend_strength(self, returns):
        """Расчет силы тренда."""
        if len(returns) < 2:
            return 0
        return np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
    
    def predict_risk(self, market_data):
        """
        Предсказание риска с помощью ML-модели.
        
        Args:
            market_data (dict): Рыночные данные
            
        Returns:
            float: Предсказанный уровень риска
        """
        
        if self.model is None:
            return 0.02  # Дефолтный риск
        
        try:
            # Извлечение признаков
            features = self.extract_risk_features(market_data)
            feature_vector = np.array(list(features.values())).reshape(1, -1)
            
            # Нормализация признаков
            if hasattr(self.feature_scaler, 'fit'):
                feature_vector = self.feature_scaler.transform(feature_vector)
            
            # Предсказание
            risk_prediction = self.model.predict(feature_vector)[0]
            
            # Ограничения для безопасности
            return max(0.001, min(risk_prediction, 0.1))
            
        except Exception as e:
            print(f"Ошибка при предсказании риска: {e}")
            return 0.02  # Дефолтный риск при ошибке
    
    def train_risk_model(self, historical_data, risk_labels, test_size=0.2):
        """
        Обучение ML-модели для предсказания рисков.
        
        Args:
            historical_data (list): Список исторических рыночных данных
            risk_labels (list): Список соответствующих меток риска
            test_size (float): Доля данных для тестирования
            
        Returns:
            dict: Метрики производительности модели
        """
        
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
        
        # Извлечение признаков
        features_list = []
        for data in historical_data:
            features = self.extract_risk_features(data)
            features_list.append(list(features.values()))
        
        X = np.array(features_list)
        y = np.array(risk_labels)
        
        # Сохранение названий признаков
        if features_list:
            self.feature_names = list(features.keys())
        
        # Разделение на обучающую и тестовую выборки
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Нормализация признаков
        X_train_scaled = self.feature_scaler.fit_transform(X_train)
        X_test_scaled = self.feature_scaler.transform(X_test)
        
        # Обучение модели
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Предсказания
        y_train_pred = self.model.predict(X_train_scaled)
        y_test_pred = self.model.predict(X_test_scaled)
        
        # Расчет метрик
        train_mse = mean_squared_error(y_train, y_train_pred)
        test_mse = mean_squared_error(y_test, y_test_pred)
        train_r2 = r2_score(y_train, y_train_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        train_mae = mean_absolute_error(y_train, y_train_pred)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        
        self.model_performance = {
            'train_mse': train_mse,
            'test_mse': test_mse,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'train_mae': train_mae,
            'test_mae': test_mae,
            'feature_importance': dict(zip(self.feature_names, self.model.feature_importances_))
        }
        
        return self.model_performance
    
    def get_feature_importance(self, top_n=10):
        """
        Получение важности признаков.
        
        Args:
            top_n (int): Количество топ-признаков для возврата
            
        Returns:
            dict: Словарь с важностью признаков
        """
        
        if self.model is None or not hasattr(self.model, 'feature_importances_'):
            return {}
        
        importance_dict = dict(zip(self.feature_names, self.model.feature_importances_))
        sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_importance[:top_n])

# Пример использования MLRiskManager
def demonstrate_ml_risk_management():
    """
    Демонстрация работы MLRiskManager с синтетическими данными.
    """
    print("=== Демонстрация ML-управления рисками ===")
    
    # Создание ML-менеджера рисков
    ml_risk_manager = MLRiskManager()
    
    # Генерация синтетических исторических данных
    np.random.seed(42)
    n_periods = 1000
    
    historical_data = []
    risk_labels = []
    
    print("📊 Генерация исторических данных...")
    
    for i in range(n_periods):
        # Генерация рыночных данных
        n_days = np.random.randint(20, 100)
        base_price = 100 + i * 0.1
        
        # Генерация цен с различной волатильностью
        volatility = np.random.uniform(0.01, 0.05)
        returns = np.random.normal(0.0005, volatility, n_days)
        prices = [base_price]
        for ret in returns:
            prices.append(prices[-1] * (1 + ret))
        
        # Генерация объемов
        base_volume = 1000000
        volume_noise = np.random.uniform(0.5, 2.0, n_days)
        volumes = [base_volume * v for v in volume_noise]
        
        # Создание рыночных данных
        market_data = {
            'close': prices,
            'volume': volumes,
            'returns': returns,
            'timestamp': pd.Timestamp.now() - pd.Timedelta(days=n_periods-i)
        }
        
        # Расчет реального риска (как целевая переменная)
        real_risk = np.std(returns) * np.random.uniform(0.8, 1.2)
        
        historical_data.append(market_data)
        risk_labels.append(real_risk)
    
    print(f"✅ Сгенерировано {len(historical_data)} периодов данных")
    
    # Обучение модели
    print("\n🤖 Обучение ML-модели...")
    performance = ml_risk_manager.train_risk_model(historical_data, risk_labels)
    
    print("📈 Результаты обучения:")
    print(f"   R² на обучающей выборке: {performance['train_r2']:.3f}")
    print(f"   R² на тестовой выборке: {performance['test_r2']:.3f}")
    print(f"   MAE на тестовой выборке: {performance['test_mae']:.3f}")
    
    # Важность признаков
    print("\n🔍 Топ-10 важных признаков:")
    feature_importance = ml_risk_manager.get_feature_importance(10)
    for feature, importance in feature_importance.items():
        print(f"   {feature}: {importance:.3f}")
    
    # Тестирование предсказаний
    print("\n🎯 Тестирование предсказаний:")
    test_data = historical_data[-10:]  # Последние 10 периодов
    
    for i, data in enumerate(test_data):
        predicted_risk = ml_risk_manager.predict_risk(data)
        actual_risk = risk_labels[-(10-i)]
        
        print(f"Период {i+1}: Предсказанный риск {predicted_risk:.3f}, "
              f"Реальный риск {actual_risk:.3f}, "
              f"Ошибка {abs(predicted_risk - actual_risk):.3f}")
    
    return {
        'model_performance': performance,
        'feature_importance': feature_importance,
        'predictions': [ml_risk_manager.predict_risk(data) for data in test_data],
        'actual_risks': risk_labels[-10:]
    }

# Запуск демонстрации
if __name__ == "__main__":
    ml_demo_results = demonstrate_ml_risk_management()
```

## Мониторинг рисков

**Теория:** Мониторинг рисков - это непрерывный процесс отслеживания и оценки рисков в реальном времени. Эффективный мониторинг позволяет быстро реагировать на изменения рыночных условий и предотвращать потери.

### 1. Real-time Risk Monitoring

**Теория:** Система мониторинга рисков в реальном времени отслеживает ключевые метрики и генерирует предупреждения при превышении установленных порогов. Это критически важно для автоматизированных торговых систем.

**Ключевые принципы мониторинга:**
- **Непрерывность:** Постоянное отслеживание без перерывов
- **Многоуровневость:** Различные уровни предупреждений
- **Автоматизация:** Минимальное вмешательство человека
- **Интеграция:** Связь с торговыми системами

```python
class RiskMonitor:
    """
    Класс для мониторинга рисков в реальном времени.
    
    Этот класс отслеживает ключевые метрики риска и генерирует
    предупреждения при превышении установленных порогов.
    """
    
    def __init__(self, alert_thresholds):
        """
        Инициализация монитора рисков.
        
        Args:
            alert_thresholds (dict): Словарь с порогами для различных типов рисков
        """
        self.alert_thresholds = alert_thresholds
        self.alerts = []
        self.monitoring_history = []
        self.alert_counts = {
            'DRAWDOWN': 0,
            'VOLATILITY': 0,
            'CORRELATION': 0,
            'POSITION_SIZE': 0,
            'MARGIN': 0
        }
    
    def monitor_risks(self, current_state):
        """
        Мониторинг рисков в реальном времени.
        
        Проверяет текущее состояние портфеля и генерирует предупреждения
        при превышении установленных порогов риска.
        
        Args:
            current_state (dict): Текущее состояние портфеля
            
        Returns:
            list: Список сгенерированных предупреждений
        """
        
        alerts = []
        timestamp = pd.Timestamp.now()
        
        # 1. Проверка просадки
        drawdown = current_state.get('drawdown', 0)
        if drawdown > self.alert_thresholds.get('max_drawdown', 0.15):
            alert = {
                'timestamp': timestamp,
                'type': 'DRAWDOWN',
                'level': 'CRITICAL',
                'value': drawdown,
                'threshold': self.alert_thresholds.get('max_drawdown', 0.15),
                'message': f"🚨 КРИТИЧНО: Просадка {drawdown:.2%} превышает максимум {self.alert_thresholds.get('max_drawdown', 0.15):.2%}"
            }
            alerts.append(alert)
            self.alert_counts['DRAWDOWN'] += 1
        
        # 2. Проверка волатильности
        volatility = current_state.get('volatility', 0)
        if volatility > self.alert_thresholds.get('max_volatility', 0.05):
            alert = {
                'timestamp': timestamp,
                'type': 'VOLATILITY',
                'level': 'WARNING',
                'value': volatility,
                'threshold': self.alert_thresholds.get('max_volatility', 0.05),
                'message': f"⚠️ ВНИМАНИЕ: Высокая волатильность {volatility:.2%} (порог {self.alert_thresholds.get('max_volatility', 0.05):.2%})"
            }
            alerts.append(alert)
            self.alert_counts['VOLATILITY'] += 1
        
        # 3. Проверка корреляции
        max_correlation = current_state.get('max_correlation', 0)
        if max_correlation > self.alert_thresholds.get('max_correlation', 0.7):
            alert = {
                'timestamp': timestamp,
                'type': 'CORRELATION',
                'level': 'WARNING',
                'value': max_correlation,
                'threshold': self.alert_thresholds.get('max_correlation', 0.7),
                'message': f"⚠️ ВНИМАНИЕ: Высокая корреляция {max_correlation:.3f} (порог {self.alert_thresholds.get('max_correlation', 0.7):.3f})"
            }
            alerts.append(alert)
            self.alert_counts['CORRELATION'] += 1
        
        # 4. Проверка размера позиций
        position_size_ratio = current_state.get('position_size_ratio', 0)
        if position_size_ratio > self.alert_thresholds.get('max_position_ratio', 0.1):
            alert = {
                'timestamp': timestamp,
                'type': 'POSITION_SIZE',
                'level': 'WARNING',
                'value': position_size_ratio,
                'threshold': self.alert_thresholds.get('max_position_ratio', 0.1),
                'message': f"⚠️ ВНИМАНИЕ: Большой размер позиции {position_size_ratio:.2%} (порог {self.alert_thresholds.get('max_position_ratio', 0.1):.2%})"
            }
            alerts.append(alert)
            self.alert_counts['POSITION_SIZE'] += 1
        
        # 5. Проверка маржи
        margin_ratio = current_state.get('margin_ratio', 0)
        if margin_ratio > self.alert_thresholds.get('max_margin_ratio', 0.8):
            alert = {
                'timestamp': timestamp,
                'type': 'MARGIN',
                'level': 'CRITICAL' if margin_ratio > 0.9 else 'WARNING',
                'value': margin_ratio,
                'threshold': self.alert_thresholds.get('max_margin_ratio', 0.8),
                'message': f"{'🚨 КРИТИЧНО' if margin_ratio > 0.9 else '⚠️ ВНИМАНИЕ'}: Высокая загрузка маржи {margin_ratio:.2%} (порог {self.alert_thresholds.get('max_margin_ratio', 0.8):.2%})"
            }
            alerts.append(alert)
            self.alert_counts['MARGIN'] += 1
        
        # Сохранение истории мониторинга
        self.monitoring_history.append({
            'timestamp': timestamp,
            'state': current_state.copy(),
            'alerts_count': len(alerts)
        })
        
        # Ограничение размера истории
        if len(self.monitoring_history) > 1000:
            self.monitoring_history = self.monitoring_history[-1000:]
        
        return alerts
    
    def send_alert(self, alert):
        """
        Отправка уведомления о риске.
        
        Args:
            alert (dict): Словарь с информацией о предупреждении
        """
        
        # Вывод в консоль
        print(f"[{alert['timestamp'].strftime('%H:%M:%S')}] {alert['level']} {alert['type']}: {alert['message']}")
        
        # В реальной системе здесь может быть:
        # - Отправка email
        # - SMS уведомления
        # - Push-уведомления
        # - Запись в базу данных
        # - Интеграция с системами мониторинга
        
        self.alerts.append(alert)
    
    def get_alert_summary(self, hours=24):
        """
        Получение сводки предупреждений за указанный период.
        
        Args:
            hours (int): Количество часов для анализа
            
        Returns:
            dict: Сводка предупреждений
        """
        
        cutoff_time = pd.Timestamp.now() - pd.Timedelta(hours=hours)
        recent_alerts = [alert for alert in self.alerts if alert['timestamp'] > cutoff_time]
        
        summary = {
            'total_alerts': len(recent_alerts),
            'critical_alerts': len([a for a in recent_alerts if a['level'] == 'CRITICAL']),
            'warning_alerts': len([a for a in recent_alerts if a['level'] == 'WARNING']),
            'alerts_by_type': {},
            'alerts_by_hour': {}
        }
        
        # Группировка по типам
        for alert in recent_alerts:
            alert_type = alert['type']
            if alert_type not in summary['alerts_by_type']:
                summary['alerts_by_type'][alert_type] = 0
            summary['alerts_by_type'][alert_type] += 1
        
        # Группировка по часам
        for alert in recent_alerts:
            hour = alert['timestamp'].hour
            if hour not in summary['alerts_by_hour']:
                summary['alerts_by_hour'][hour] = 0
            summary['alerts_by_hour'][hour] += 1
        
        return summary
    
    def get_risk_metrics(self):
        """
        Получение текущих метрик риска.
        
        Returns:
            dict: Словарь с метриками риска
        """
        
        if not self.monitoring_history:
            return {}
        
        latest_state = self.monitoring_history[-1]['state']
        
        return {
            'current_drawdown': latest_state.get('drawdown', 0),
            'current_volatility': latest_state.get('volatility', 0),
            'current_correlation': latest_state.get('max_correlation', 0),
            'current_position_ratio': latest_state.get('position_size_ratio', 0),
            'current_margin_ratio': latest_state.get('margin_ratio', 0),
            'total_alerts': len(self.alerts),
            'alert_counts': self.alert_counts.copy()
        }

# Пример использования RiskMonitor
def demonstrate_risk_monitoring():
    """
    Демонстрация работы системы мониторинга рисков.
    """
    print("=== Демонстрация мониторинга рисков ===")
    
    # Создание монитора рисков
    alert_thresholds = {
        'max_drawdown': 0.15,      # Максимальная просадка 15%
        'max_volatility': 0.05,    # Максимальная волатильность 5%
        'max_correlation': 0.7,    # Максимальная корреляция 70%
        'max_position_ratio': 0.1, # Максимальный размер позиции 10%
        'max_margin_ratio': 0.8    # Максимальная загрузка маржи 80%
    }
    
    risk_monitor = RiskMonitor(alert_thresholds)
    
    # Симуляция различных состояний портфеля
    print("\n📊 Симуляция мониторинга рисков:")
    
    # Нормальное состояние
    normal_state = {
        'drawdown': 0.05,
        'volatility': 0.02,
        'max_correlation': 0.4,
        'position_size_ratio': 0.05,
        'margin_ratio': 0.3
    }
    
    alerts = risk_monitor.monitor_risks(normal_state)
    print(f"Нормальное состояние: {len(alerts)} предупреждений")
    for alert in alerts:
        risk_monitor.send_alert(alert)
    
    # Критическое состояние
    critical_state = {
        'drawdown': 0.20,  # Превышение лимита
        'volatility': 0.08,  # Превышение лимита
        'max_correlation': 0.85,  # Превышение лимита
        'position_size_ratio': 0.15,  # Превышение лимита
        'margin_ratio': 0.95  # Превышение лимита
    }
    
    alerts = risk_monitor.monitor_risks(critical_state)
    print(f"\nКритическое состояние: {len(alerts)} предупреждений")
    for alert in alerts:
        risk_monitor.send_alert(alert)
    
    # Получение сводки
    print("\n📈 Сводка предупреждений за последние 24 часа:")
    summary = risk_monitor.get_alert_summary(24)
    print(f"   Всего предупреждений: {summary['total_alerts']}")
    print(f"   Критических: {summary['critical_alerts']}")
    print(f"   Предупреждений: {summary['warning_alerts']}")
    print(f"   По типам: {summary['alerts_by_type']}")
    
    # Текущие метрики
    print("\n📊 Текущие метрики риска:")
    metrics = risk_monitor.get_risk_metrics()
    for key, value in metrics.items():
        if key != 'alert_counts':
            print(f"   {key}: {value}")
    
    return {
        'alert_summary': summary,
        'risk_metrics': metrics,
        'total_alerts': len(risk_monitor.alerts)
    }

# Запуск демонстрации
if __name__ == "__main__":
    monitoring_demo_results = demonstrate_risk_monitoring()
```

### 2. Risk Dashboard
```python
def create_risk_dashboard(risk_metrics):
    """Создание дашборда рисков"""
    
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # График просадки
    axes[0, 0].plot(risk_metrics['drawdown_history'])
    axes[0, 0].set_title('История просадки')
    axes[0, 0].set_ylabel('Просадка %')
    axes[0, 0].grid(True)
    
    # График волатильности
    axes[0, 1].plot(risk_metrics['volatility_history'])
    axes[0, 1].set_title('История волатильности')
    axes[0, 1].set_ylabel('Волатильность %')
    axes[0, 1].grid(True)
    
    # Распределение доходности
    axes[1, 0].hist(risk_metrics['returns'], bins=30, alpha=0.7)
    axes[1, 0].set_title('Распределение доходности')
    axes[1, 0].set_xlabel('Доходность %')
    axes[1, 0].set_ylabel('Частота')
    axes[1, 0].grid(True)
    
    # VaR кривая
    confidence_levels = np.arange(0.01, 0.11, 0.01)
    var_values = [np.percentile(risk_metrics['returns'], cl*100) for cl in confidence_levels]
    axes[1, 1].plot(confidence_levels, var_values)
    axes[1, 1].set_title('VaR кривая')
    axes[1, 1].set_xlabel('Уровень доверия')
    axes[1, 1].set_ylabel('VaR %')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.show()
```

## Практический пример

```python
def complete_risk_management_system():
    """Полная система управления рисками"""
    
    # 1. Инициализация компонентов
    market_risk = MarketRiskManager()
    credit_risk = CreditRiskManager()
    operational_risk = OperationalRiskManager()
    drawdown_controller = DrawdownController()
    correlation_risk = CorrelationRiskManager()
    adaptive_risk = AdaptiveRiskManager()
    risk_monitor = RiskMonitor({
        'max_drawdown': 0.15,
        'max_volatility': 0.05,
        'max_correlation': 0.7
    })
    
    # 2. Симуляция торговли
    account_balance = 10000
    positions = {}
    
    for i in range(100):  # 100 торговых периодов
        # Получение рыночных данных
        market_data = get_market_data(i)
        
        # Расчет рисков
        volatility = market_data['returns'].std()
        position_size = market_risk.calculate_position_size(account_balance, volatility)
        
        # Проверка лимитов
        can_trade, message = operational_risk.check_trading_limits()
        if not can_trade:
            print(f"Торговля остановлена: {message}")
            break
        
        # Проверка корреляции
        if positions:
            correlation_ok, corr_message = correlation_risk.check_correlation(
                market_data['asset'], positions
            )
            if not correlation_ok:
                print(f"Корреляция: {corr_message}")
                continue
        
        # Обновление просадки
        drawdown_controller.update_capital(account_balance)
        should_reduce, dd_message = drawdown_controller.should_reduce_position()
        
        if should_reduce:
            print(f"Просадка: {dd_message}")
            position_size = drawdown_controller.calculate_position_reduction(position_size)
        
        # Мониторинг рисков
        current_state = {
            'drawdown': drawdown_controller.current_drawdown,
            'volatility': volatility,
            'max_correlation': 0.5  # Упрощенный расчет
        }
        
        alerts = risk_monitor.monitor_risks(current_state)
        for alert in alerts:
            print(f"ALERT: {alert['message']}")
        
        # Выполнение торговли (упрощенное)
        if position_size > 0:
            # Симуляция торговли
            trade_result = simulate_trade(market_data, position_size)
            account_balance += trade_result
            positions[market_data['asset']] = position_size

# Вспомогательные функции для полной функциональности
def get_market_data(period):
    """
    Получение рыночных данных для симуляции.
    
    Args:
        period (int): Номер периода
        
    Returns:
        dict: Словарь с рыночными данными
    """
    np.random.seed(42 + period)
    
    # Генерация реалистичных рыночных данных
    n_days = 30
    base_price = 1.2000 + period * 0.001
    volatility = 0.02 + np.random.normal(0, 0.005)
    
    returns = np.random.normal(0.0005, volatility, n_days)
    prices = [base_price]
    for ret in returns:
        prices.append(prices[-1] * (1 + ret))
    
    volumes = [1000000 * np.random.uniform(0.5, 2.0) for _ in range(n_days)]
    
    return {
        'asset': f'ASSET_{period}',
        'close': prices,
        'volume': volumes,
        'returns': returns,
        'timestamp': pd.Timestamp.now() - pd.Timedelta(days=period)
    }

def simulate_trade(market_data, position_size):
    """
    Симуляция торговой сделки.
    
    Args:
        market_data (dict): Рыночные данные
        position_size (float): Размер позиции
        
    Returns:
        float: Результат сделки
    """
    # Простая симуляция: случайная доходность
    np.random.seed(int(time.time()) % 1000)
    trade_return = np.random.normal(0.001, 0.02)  # 0.1% средняя доходность, 2% волатильность
    
    return position_size * trade_return

# Полная система управления рисками
def complete_risk_management_system():
    """
    Полная интегрированная система управления рисками.
    
    Эта функция демонстрирует работу всех компонентов системы
    управления рисками в едином процессе.
    """
    
    print("=== Полная система управления рисками ===")
    
    # 1. Инициализация всех компонентов
    market_risk = MarketRiskManager()
    credit_risk = CreditRiskManager()
    operational_risk = OperationalRiskManager()
    drawdown_controller = DrawdownController()
    correlation_risk = CorrelationRiskManager()
    adaptive_risk = AdaptiveRiskManager()
    risk_monitor = RiskMonitor({
        'max_drawdown': 0.15,
        'max_volatility': 0.05,
        'max_correlation': 0.7,
        'max_position_ratio': 0.1,
        'max_margin_ratio': 0.8
    })
    
    # 2. Симуляция торговли
    account_balance = 10000
    positions = {}
    
    print(f"💰 Начальный баланс: ${account_balance:.2f}")
    print("🔄 Запуск симуляции торговли...")
    
    for i in range(100):  # 100 торговых периодов
        # Получение рыночных данных
        market_data = get_market_data(i)
        
        # Расчет рисков
        volatility = market_data['returns'].std()
        position_size = market_risk.calculate_position_size(account_balance, volatility)
        
        # Проверка лимитов
        can_trade, message = operational_risk.check_trading_limits()
        if not can_trade:
            print(f"🛑 Торговля остановлена: {message}")
            break
        
        # Проверка корреляции
        if positions:
            correlation_ok, corr_message = correlation_risk.check_correlation(
                market_data['asset'], positions
            )
            if not correlation_ok:
                print(f"⚠️ Корреляция: {corr_message}")
                continue
        
        # Обновление просадки
        drawdown_controller.update_capital(account_balance)
        should_reduce, dd_message = drawdown_controller.should_reduce_position()
        
        if should_reduce:
            print(f"📉 Просадка: {dd_message}")
            position_size = drawdown_controller.calculate_position_reduction(position_size)
        
        # Мониторинг рисков
        current_state = {
            'drawdown': drawdown_controller.current_drawdown,
            'volatility': volatility,
            'max_correlation': 0.5,  # Упрощенный расчет
            'position_size_ratio': position_size / account_balance if account_balance > 0 else 0,
            'margin_ratio': 0.3  # Упрощенный расчет
        }
        
        alerts = risk_monitor.monitor_risks(current_state)
        for alert in alerts:
            risk_monitor.send_alert(alert)
        
        # Выполнение торговли (упрощенное)
        if position_size > 0:
            # Симуляция торговли
            trade_result = simulate_trade(market_data, position_size)
            account_balance += trade_result
            positions[market_data['asset']] = position_size
    
    # 3. Создание дашборда
    risk_metrics = {
        'drawdown_history': drawdown_controller.drawdown_history,
        'volatility_history': [0.02] * 100,  # Упрощенный
        'returns': np.random.normal(0.001, 0.02, 100)
    }
    
    create_risk_dashboard(risk_metrics)
    
    print("\n=== Результаты системы управления рисками ===")
    print(f"💰 Финальный баланс: ${account_balance:.2f}")
    print(f"📈 Общая доходность: {((account_balance/10000)-1)*100:.2f}%")
    print(f"📉 Максимальная просадка: {drawdown_controller.get_maximum_drawdown()*100:.2f}%")
    print(f"🚨 Количество алертов: {len(risk_monitor.alerts)}")
    print(f"📊 Количество позиций: {len(positions)}")
    
    return {
        'final_balance': account_balance,
        'total_return': (account_balance/10000)-1,
        'max_drawdown': drawdown_controller.get_maximum_drawdown(),
        'alerts': risk_monitor.alerts,
        'positions_count': len(positions)
    }
```

## Следующие шаги

После изучения управления рисками переходите к:
- **[10_blockchain_deployment.md](10_blockchain_deployment.md)** - Блокчейн деплой
- **[11_wave2_analysis.md](11_wave2_analysis.md)** - Анализ WAVE2

## Ключевые выводы

1. **Управление рисками** - основа успешной торговли
2. **Диверсификация** снижает риски
3. **Мониторинг** должен быть непрерывным
4. **Адаптивность** - ключ к выживанию
5. **Психология** - важный аспект управления рисками

---

**Важно:** Лучше заработать меньше, но стабильно, чем много, но с большими рисками!
