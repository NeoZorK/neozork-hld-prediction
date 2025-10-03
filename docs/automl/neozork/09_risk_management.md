# 09. 🛡️ Управление рисками

**Цель:** Научиться эффективно управлять рисками в торговых стратегиях для защиты капитала.

## Что такое управление рисками?

**Управление рисками** - это процесс идентификации, оценки и контроля рисков для минимизации потерь и максимизации прибыли.

### Зачем нужно управление рисками?
- **Защита капитала** - предотвращение больших потерь
- **Стабильность** - снижение волатильности результатов
- **Психологический комфорт** - уверенность в торговле
- **Долгосрочная прибыльность** - выживание в долгосрочной перспективе

## Типы рисков

### 1. Рыночные риски
```python
class MarketRiskManager:
    def __init__(self, max_position_size=0.1, stop_loss=0.02, take_profit=0.04):
        self.max_position_size = max_position_size  # Максимальный размер позиции
        self.stop_loss = stop_loss  # Stop Loss
        self.take_profit = take_profit  # Take Profit
    
    def calculate_position_size(self, account_balance, volatility, confidence_level=0.95):
        """Расчет размера позиции на основе волатильности"""
        
        # Kelly Criterion для оптимального размера позиции
        win_rate = 0.6  # Предполагаемая вероятность выигрыша
        avg_win = 0.02  # Средний выигрыш
        avg_loss = 0.01  # Средний проигрыш
        
        kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
        
        # Ограничение Kelly Criterion
        kelly_fraction = max(0, min(kelly_fraction, self.max_position_size))
        
        # Учет волатильности
        volatility_adjustment = 1 / (1 + volatility * 10)
        
        # Финальный размер позиции
        position_size = account_balance * kelly_fraction * volatility_adjustment
        
        return min(position_size, account_balance * self.max_position_size)
    
    def calculate_stop_loss(self, entry_price, volatility):
        """Расчет Stop Loss на основе волатильности"""
        
        # ATR-based Stop Loss
        atr_multiplier = 2.0
        stop_distance = volatility * atr_multiplier
        
        stop_loss_price = entry_price - stop_distance
        
        return stop_loss_price
    
    def calculate_take_profit(self, entry_price, stop_loss_price, risk_reward_ratio=2):
        """Расчет Take Profit"""
        
        risk = entry_price - stop_loss_price
        reward = risk * risk_reward_ratio
        
        take_profit_price = entry_price + reward
        
        return take_profit_price
```

### 2. Кредитные риски
```python
class CreditRiskManager:
    def __init__(self, max_leverage=3.0, margin_requirement=0.3):
        self.max_leverage = max_leverage
        self.margin_requirement = margin_requirement
    
    def calculate_margin_requirement(self, position_value, asset_volatility):
        """Расчет требования к марже"""
        
        # Базовое требование к марже
        base_margin = position_value * self.margin_requirement
        
        # Дополнительная маржа для волатильных активов
        volatility_margin = position_value * asset_volatility * 0.1
        
        total_margin = base_margin + volatility_margin
        
        return total_margin
    
    def check_margin_call(self, account_balance, margin_used, position_value):
        """Проверка маржин-колла"""
        
        margin_ratio = margin_used / account_balance
        
        if margin_ratio > 0.8:  # 80% маржи использовано
            return True, "Предупреждение: высокая загрузка маржи"
        elif margin_ratio > 0.9:  # 90% маржи использовано
            return True, "КРИТИЧНО: маржин-колл!"
        
        return False, "Маржа в норме"
```

### 3. Операционные риски
```python
class OperationalRiskManager:
    def __init__(self, max_daily_trades=10, max_slippage=0.001):
        self.max_daily_trades = max_daily_trades
        self.max_slippage = max_slippage
        self.daily_trades = 0
    
    def check_trading_limits(self):
        """Проверка лимитов торговли"""
        
        if self.daily_trades >= self.max_daily_trades:
            return False, "Достигнут дневной лимит торгов"
        
        return True, "Торговля разрешена"
    
    def calculate_slippage(self, order_size, market_volume, price):
        """Расчет проскальзывания"""
        
        # Проскальзывание зависит от размера ордера относительно объема
        volume_ratio = order_size / market_volume
        
        if volume_ratio < 0.01:  # Малый ордер
            slippage = 0.0001
        elif volume_ratio < 0.1:  # Средний ордер
            slippage = 0.0005
        else:  # Большой ордер
            slippage = 0.002
        
        return min(slippage, self.max_slippage)
```

## Продвинутые техники управления рисками

### 1. Value at Risk (VaR)
```python
def calculate_var(returns, confidence_level=0.05, time_horizon=1):
    """Расчет Value at Risk"""
    
    # Исторический VaR
    historical_var = np.percentile(returns, confidence_level * 100)
    
    # Параметрический VaR
    mean_return = returns.mean()
    std_return = returns.std()
    parametric_var = mean_return + std_return * stats.norm.ppf(confidence_level)
    
    # Монте-Карло VaR
    n_simulations = 10000
    simulated_returns = np.random.normal(mean_return, std_return, n_simulations)
    monte_carlo_var = np.percentile(simulated_returns, confidence_level * 100)
    
    return {
        'historical_var': historical_var,
        'parametric_var': parametric_var,
        'monte_carlo_var': monte_carlo_var
    }

def calculate_expected_shortfall(returns, confidence_level=0.05):
    """Расчет Expected Shortfall (Conditional VaR)"""
    
    var = calculate_var(returns, confidence_level)['historical_var']
    tail_losses = returns[returns <= var]
    expected_shortfall = np.mean(tail_losses)
    
    return expected_shortfall
```

### 2. Maximum Drawdown Control
```python
class DrawdownController:
    def __init__(self, max_drawdown=0.15, drawdown_threshold=0.10):
        self.max_drawdown = max_drawdown
        self.drawdown_threshold = drawdown_threshold
        self.peak_capital = 0
        self.current_drawdown = 0
    
    def update_capital(self, current_capital):
        """Обновление капитала и расчет просадки"""
        
        # Обновление пика капитала
        if current_capital > self.peak_capital:
            self.peak_capital = current_capital
            self.current_drawdown = 0
        else:
            # Расчет текущей просадки
            self.current_drawdown = (self.peak_capital - current_capital) / self.peak_capital
    
    def should_reduce_position(self):
        """Проверка необходимости сокращения позиций"""
        
        if self.current_drawdown > self.max_drawdown:
            return True, "КРИТИЧНО: превышена максимальная просадка"
        elif self.current_drawdown > self.drawdown_threshold:
            return True, "Предупреждение: высокая просадка"
        
        return False, "Просадка в норме"
    
    def calculate_position_reduction(self, current_position_size):
        """Расчет сокращения позиции"""
        
        if self.current_drawdown > self.max_drawdown:
            # Критическая просадка - закрываем все позиции
            return 0
        elif self.current_drawdown > self.drawdown_threshold:
            # Высокая просадка - сокращаем позиции на 50%
            return current_position_size * 0.5
        
        return current_position_size
```

### 3. Correlation Risk Management
```python
class CorrelationRiskManager:
    def __init__(self, max_correlation=0.7, max_positions=5):
        self.max_correlation = max_correlation
        self.max_positions = max_positions
        self.current_positions = {}
    
    def check_correlation(self, new_asset, existing_positions):
        """Проверка корреляции с существующими позициями"""
        
        correlations = []
        
        for asset, position in existing_positions.items():
            # Расчет корреляции (упрощенный)
            correlation = self.calculate_correlation(new_asset, asset)
            correlations.append(correlation)
        
        max_correlation = max(correlations) if correlations else 0
        
        if max_correlation > self.max_correlation:
            return False, f"Высокая корреляция: {max_correlation:.3f}"
        
        return True, "Корреляция в норме"
    
    def calculate_correlation(self, asset1, asset2):
        """Расчет корреляции между активами"""
        
        # Упрощенный расчет корреляции
        # В реальности нужно использовать исторические данные
        return np.random.uniform(0, 1)  # Заглушка
    
    def optimize_portfolio_weights(self, assets, expected_returns, cov_matrix):
        """Оптимизация весов портфеля"""
        
        from scipy.optimize import minimize
        
        def portfolio_variance(weights):
            return np.dot(weights.T, np.dot(cov_matrix, weights))
        
        def portfolio_return(weights):
            return np.sum(expected_returns * weights)
        
        # Ограничения
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # Сумма весов = 1
        bounds = tuple((0, 1) for _ in range(len(assets)))  # Веса от 0 до 1
        
        # Начальные веса
        initial_weights = np.array([1/len(assets)] * len(assets))
        
        # Оптимизация
        result = minimize(portfolio_variance, initial_weights, 
                        method='SLSQP', bounds=bounds, constraints=constraints)
        
        return result.x
```

## Динамическое управление рисками

### 1. Адаптивные лимиты
```python
class AdaptiveRiskManager:
    def __init__(self, base_risk=0.02, volatility_lookback=20):
        self.base_risk = base_risk
        self.volatility_lookback = volatility_lookback
        self.risk_history = []
    
    def calculate_adaptive_risk(self, returns):
        """Расчет адаптивного риска на основе волатильности"""
        
        # Расчет текущей волатильности
        current_volatility = returns.tail(self.volatility_lookback).std()
        
        # Адаптация риска
        if current_volatility > 0.03:  # Высокая волатильность
            adaptive_risk = self.base_risk * 0.5
        elif current_volatility < 0.01:  # Низкая волатильность
            adaptive_risk = self.base_risk * 1.5
        else:  # Нормальная волатильность
            adaptive_risk = self.base_risk
        
        # Ограничения
        adaptive_risk = max(0.005, min(adaptive_risk, 0.05))
        
        return adaptive_risk
    
    def update_risk_history(self, risk_level):
        """Обновление истории рисков"""
        
        self.risk_history.append(risk_level)
        
        # Ограничение истории
        if len(self.risk_history) > 100:
            self.risk_history = self.risk_history[-100:]
```

### 2. Machine Learning Risk Management
```python
class MLRiskManager:
    def __init__(self, model=None):
        self.model = model
        self.risk_features = []
        self.risk_labels = []
    
    def extract_risk_features(self, market_data):
        """Извлечение признаков для ML модели риска"""
        
        features = {
            'volatility': market_data['returns'].std(),
            'skewness': market_data['returns'].skew(),
            'kurtosis': market_data['returns'].kurtosis(),
            'volume_ratio': market_data['volume'].iloc[-1] / market_data['volume'].mean(),
            'price_momentum': market_data['close'].iloc[-1] / market_data['close'].iloc[-20] - 1,
            'rsi': self.calculate_rsi(market_data['close']),
            'macd': self.calculate_macd(market_data['close'])
        }
        
        return features
    
    def predict_risk(self, market_data):
        """Предсказание риска с помощью ML"""
        
        if self.model is None:
            return 0.02  # Дефолтный риск
        
        features = self.extract_risk_features(market_data)
        feature_vector = np.array(list(features.values())).reshape(1, -1)
        
        risk_prediction = self.model.predict(feature_vector)[0]
        
        return max(0.001, min(risk_prediction, 0.1))  # Ограничения
    
    def train_risk_model(self, historical_data, risk_labels):
        """Обучение ML модели риска"""
        
        from sklearn.ensemble import RandomForestRegressor
        
        # Извлечение признаков
        features_list = []
        for data in historical_data:
            features = self.extract_risk_features(data)
            features_list.append(list(features.values()))
        
        X = np.array(features_list)
        y = np.array(risk_labels)
        
        # Обучение модели
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        return self.model
```

## Мониторинг рисков

### 1. Real-time Risk Monitoring
```python
class RiskMonitor:
    def __init__(self, alert_thresholds):
        self.alert_thresholds = alert_thresholds
        self.alerts = []
    
    def monitor_risks(self, current_state):
        """Мониторинг рисков в реальном времени"""
        
        alerts = []
        
        # Проверка просадки
        if current_state['drawdown'] > self.alert_thresholds['max_drawdown']:
            alerts.append({
                'type': 'DRAWDOWN',
                'level': 'CRITICAL',
                'message': f"Просадка превышена: {current_state['drawdown']:.2%}"
            })
        
        # Проверка волатильности
        if current_state['volatility'] > self.alert_thresholds['max_volatility']:
            alerts.append({
                'type': 'VOLATILITY',
                'level': 'WARNING',
                'message': f"Высокая волатильность: {current_state['volatility']:.2%}"
            })
        
        # Проверка корреляции
        if current_state['max_correlation'] > self.alert_thresholds['max_correlation']:
            alerts.append({
                'type': 'CORRELATION',
                'level': 'WARNING',
                'message': f"Высокая корреляция: {current_state['max_correlation']:.3f}"
            })
        
        return alerts
    
    def send_alert(self, alert):
        """Отправка уведомления о риске"""
        
        print(f"[{alert['level']}] {alert['type']}: {alert['message']}")
        
        # В реальной системе здесь может быть отправка email, SMS, etc.
        self.alerts.append(alert)
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
    
    # 3. Создание дашборда
    risk_metrics = {
        'drawdown_history': drawdown_controller.risk_history,
        'volatility_history': [0.02] * 100,  # Упрощенный
        'returns': np.random.normal(0.001, 0.02, 100),
        'returns': np.random.normal(0.001, 0.02, 100)
    }
    
    create_risk_dashboard(risk_metrics)
    
    print("=== Система управления рисками ===")
    print(f"Финальный баланс: {account_balance:.2f}")
    print(f"Максимальная просадка: {drawdown_controller.current_drawdown:.2%}")
    print(f"Количество алертов: {len(risk_monitor.alerts)}")
    
    return {
        'final_balance': account_balance,
        'max_drawdown': drawdown_controller.current_drawdown,
        'alerts': risk_monitor.alerts
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
