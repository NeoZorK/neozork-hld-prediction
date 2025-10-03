# 15. Оптимизация портфолио - Создание прибыльного портфолио

**Цель:** Создать прибыльный портфолио с доходностью более 100% в месяц.

## Почему большинство портфолио не прибыльны?

### Основные проблемы

1. **Отсутствие диверсификации**
2. **Неправильное распределение активов**
3. **Игнорирование корреляций**
4. **Отсутствие риск-менеджмента**
5. **Неправильный выбор активов**

### Наш подход

**Мы используем:**
- ML-оптимизацию портфолио
- Динамическое перебалансирование
- Мультиактивный анализ
- Продвинутый риск-менеджмент
- Блокчейн-интеграцию

## ML-оптимизация портфолио

### 1. Предсказание доходности активов

```python
class AssetReturnPredictor:
    """Предсказание доходности активов"""
    
    def __init__(self, assets):
        self.assets = assets
        self.models = {}
        self.feature_engineers = {}
        
        # Инициализация моделей для каждого актива
        for asset in assets:
            self.models[asset] = self._create_model()
            self.feature_engineers[asset] = self._create_feature_engineer()
    
    def _create_model(self):
        """Создание модели для предсказания доходности"""
        return XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
    
    def _create_feature_engineer(self):
        """Создание инженера признаков"""
        return FeatureEngineer()
    
    def train(self, asset, data):
        """Обучение модели для актива"""
        # Создание признаков
        features = self.feature_engineers[asset].create_features(data)
        
        # Создание целевой переменной
        target = self._create_target(data)
        
        # Обучение модели
        self.models[asset].fit(features, target)
        
        return self.models[asset]
    
    def predict_returns(self, asset, data):
        """Предсказание доходности актива"""
        # Создание признаков
        features = self.feature_engineers[asset].create_features(data)
        
        # Предсказание
        predicted_return = self.models[asset].predict(features)
        
        return predicted_return
    
    def _create_target(self, data):
        """Создание целевой переменной"""
        # Доходность на следующий период
        future_price = data['Close'].shift(-1)
        current_price = data['Close']
        
        return (future_price - current_price) / current_price
```

### 2. Оптимизация весов портфолио

```python
class PortfolioOptimizer:
    """Оптимизатор портфолио"""
    
    def __init__(self, assets, risk_free_rate=0.02):
        self.assets = assets
        self.risk_free_rate = risk_free_rate
        self.optimizer = self._create_optimizer()
    
    def _create_optimizer(self):
        """Создание оптимизатора"""
        return {
            'method': 'SLSQP',
            'constraints': [
                {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}  # Сумма весов = 1
            ],
            'bounds': [(0, 1) for _ in range(len(self.assets))]  # Веса от 0 до 1
        }
    
    def optimize_portfolio(self, expected_returns, cov_matrix, risk_tolerance=0.5):
        """Оптимизация портфолио"""
        from scipy.optimize import minimize
        
        def objective(weights):
            """Целевая функция"""
            portfolio_return = np.dot(weights, expected_returns)
            portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            
            # Sharpe Ratio
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_risk
            
            # Возвращаем отрицательное значение для максимизации
            return -sharpe_ratio
        
        # Начальные веса
        initial_weights = np.ones(len(self.assets)) / len(self.assets)
        
        # Оптимизация
        result = minimize(
            objective,
            initial_weights,
            method=self.optimizer['method'],
            bounds=self.optimizer['bounds'],
            constraints=self.optimizer['constraints']
        )
        
        return result.x
    
    def optimize_with_constraints(self, expected_returns, cov_matrix, constraints):
        """Оптимизация с дополнительными ограничениями"""
        from scipy.optimize import minimize
        
        def objective(weights):
            portfolio_return = np.dot(weights, expected_returns)
            portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            return -portfolio_return + constraints['risk_tolerance'] * portfolio_risk
        
        # Объединение ограничений
        all_constraints = self.optimizer['constraints'] + constraints.get('additional', [])
        
        result = minimize(
            objective,
            np.ones(len(self.assets)) / len(self.assets),
            method='SLSQP',
            bounds=self.optimizer['bounds'],
            constraints=all_constraints
        )
        
        return result.x
```

### 3. Динамическое перебалансирование

```python
class DynamicRebalancer:
    """Динамическое перебалансирование портфолио"""
    
    def __init__(self, rebalancing_threshold=0.05):
        self.rebalancing_threshold = rebalancing_threshold
        self.current_weights = None
        self.target_weights = None
        self.last_rebalancing = None
    
    def should_rebalance(self, current_weights, target_weights):
        """Проверка необходимости перебалансирования"""
        # Расчет отклонения весов
        weight_deviation = np.abs(current_weights - target_weights)
        
        # Проверка превышения порога
        max_deviation = np.max(weight_deviation)
        
        return max_deviation > self.rebalancing_threshold
    
    def calculate_rebalancing_trades(self, current_weights, target_weights, portfolio_value):
        """Расчет сделок для перебалансирования"""
        trades = []
        
        for i, (current, target) in enumerate(zip(current_weights, target_weights)):
            if abs(current - target) > 0.001:  # Минимальное отклонение
                trade_amount = (target - current) * portfolio_value
                trades.append({
                    'asset': i,
                    'amount': trade_amount,
                    'current_weight': current,
                    'target_weight': target
                })
        
        return trades
    
    def execute_rebalancing(self, trades, portfolio):
        """Выполнение перебалансирования"""
        executed_trades = []
        
        for trade in trades:
            # Выполнение сделки
            success = portfolio.execute_trade(
                asset=trade['asset'],
                amount=trade['amount']
            )
            
            if success:
                executed_trades.append(trade)
                print(f"Rebalancing trade executed: {trade}")
        
        return executed_trades
```

## Мультиактивный анализ

### 1. Анализ корреляций

```python
class CorrelationAnalyzer:
    """Анализ корреляций между активами"""
    
    def __init__(self):
        self.correlation_matrix = None
        self.correlation_history = []
    
    def calculate_correlation_matrix(self, returns):
        """Расчет матрицы корреляций"""
        self.correlation_matrix = returns.corr()
        return self.correlation_matrix
    
    def analyze_correlation_stability(self, returns, window=252):
        """Анализ стабильности корреляций"""
        rolling_correlations = []
        
        for i in range(window, len(returns)):
            window_returns = returns.iloc[i-window:i]
            corr_matrix = window_returns.corr()
            rolling_correlations.append(corr_matrix)
        
        # Анализ изменений корреляций
        correlation_changes = []
        for i in range(1, len(rolling_correlations)):
            change = np.abs(rolling_correlations[i] - rolling_correlations[i-1])
            correlation_changes.append(change)
        
        return {
            'rolling_correlations': rolling_correlations,
            'correlation_changes': correlation_changes,
            'stability_score': self._calculate_stability_score(correlation_changes)
        }
    
    def _calculate_stability_score(self, correlation_changes):
        """Расчет оценки стабильности корреляций"""
        # Среднее изменение корреляций
        mean_change = np.mean([np.mean(change.values) for change in correlation_changes])
        
        # Стабильность = 1 - среднее изменение
        stability = 1 - mean_change
        
        return max(0, min(1, stability))
    
    def identify_correlation_clusters(self, correlation_matrix, threshold=0.7):
        """Идентификация кластеров корреляций"""
        from scipy.cluster.hierarchy import linkage, dendrogram
        from scipy.spatial.distance import squareform
        
        # Преобразование корреляций в расстояния
        distances = 1 - np.abs(correlation_matrix)
        
        # Кластеризация
        linkage_matrix = linkage(squareform(distances), method='ward')
        
        # Определение кластеров
        clusters = self._extract_clusters(linkage_matrix, threshold)
        
        return clusters
    
    def _extract_clusters(self, linkage_matrix, threshold):
        """Извлечение кластеров из матрицы связей"""
        from scipy.cluster.hierarchy import fcluster
        
        clusters = fcluster(linkage_matrix, threshold, criterion='distance')
        
        # Группировка активов по кластерам
        cluster_groups = {}
        for i, cluster_id in enumerate(clusters):
            if cluster_id not in cluster_groups:
                cluster_groups[cluster_id] = []
            cluster_groups[cluster_id].append(i)
        
        return cluster_groups
```

### 2. Анализ волатильности

```python
class VolatilityAnalyzer:
    """Анализ волатильности активов"""
    
    def __init__(self):
        self.volatility_history = []
        self.volatility_forecasts = {}
    
    def calculate_volatility(self, returns, window=252):
        """Расчет волатильности"""
        volatility = returns.rolling(window).std() * np.sqrt(252)
        return volatility
    
    def analyze_volatility_regimes(self, volatility):
        """Анализ режимов волатильности"""
        # Классификация режимов волатильности
        low_vol_threshold = volatility.quantile(0.33)
        high_vol_threshold = volatility.quantile(0.67)
        
        regimes = pd.cut(
            volatility,
            bins=[-np.inf, low_vol_threshold, high_vol_threshold, np.inf],
            labels=['low', 'medium', 'high']
        )
        
        return regimes
    
    def forecast_volatility(self, returns, horizon=1):
        """Прогнозирование волатильности"""
        from arch import arch_model
        
        # GARCH модель для прогнозирования волатильности
        model = arch_model(returns, vol='Garch', p=1, q=1)
        fitted_model = model.fit()
        
        # Прогноз волатильности
        forecast = fitted_model.forecast(horizon=horizon)
        
        return forecast.variance.iloc[-1, 0]
    
    def calculate_volatility_adjusted_returns(self, returns, volatility):
        """Расчет доходности, скорректированной на волатильность"""
        # Sharpe Ratio
        sharpe_ratio = returns / volatility
        
        # Volatility-adjusted returns
        adjusted_returns = returns / volatility
        
        return adjusted_returns
```

## Продвинутый риск-менеджмент

### 1. Value at Risk (VaR)

```python
class VaRCalculator:
    """Калькулятор Value at Risk"""
    
    def __init__(self, confidence_level=0.05):
        self.confidence_level = confidence_level
    
    def calculate_historical_var(self, returns):
        """Расчет исторического VaR"""
        # Сортировка доходности
        sorted_returns = np.sort(returns)
        
        # Индекс для VaR
        var_index = int(self.confidence_level * len(sorted_returns))
        
        # VaR
        var = sorted_returns[var_index]
        
        return var
    
    def calculate_parametric_var(self, returns, confidence_level=0.05):
        """Расчет параметрического VaR"""
        # Предположение о нормальном распределении
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        
        # Z-score для заданного уровня доверия
        from scipy.stats import norm
        z_score = norm.ppf(confidence_level)
        
        # VaR
        var = mean_return + z_score * std_return
        
        return var
    
    def calculate_monte_carlo_var(self, returns, n_simulations=10000, confidence_level=0.05):
        """Расчет VaR методом Монте-Карло"""
        # Параметры распределения
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        
        # Генерация случайных доходностей
        simulated_returns = np.random.normal(mean_return, std_return, n_simulations)
        
        # Сортировка
        sorted_returns = np.sort(simulated_returns)
        
        # VaR
        var_index = int(confidence_level * len(sorted_returns))
        var = sorted_returns[var_index]
        
        return var
    
    def calculate_conditional_var(self, returns, confidence_level=0.05):
        """Расчет Conditional VaR (CVaR)"""
        # Сортировка доходности
        sorted_returns = np.sort(returns)
        
        # Индекс для VaR
        var_index = int(confidence_level * len(sorted_returns))
        
        # CVaR - среднее значение в хвосте распределения
        tail_returns = sorted_returns[:var_index]
        cvar = np.mean(tail_returns)
        
        return cvar
```

### 2. Stress Testing

```python
class StressTester:
    """Стресс-тестирование портфолио"""
    
    def __init__(self):
        self.stress_scenarios = {}
    
    def define_stress_scenarios(self):
        """Определение стресс-сценариев"""
        self.stress_scenarios = {
            'market_crash': {
                'description': 'Обвал рынка на 20%',
                'asset_returns': {
                    'equity': -0.20,
                    'bonds': -0.05,
                    'commodities': -0.15,
                    'crypto': -0.50
                }
            },
            'interest_rate_shock': {
                'description': 'Резкий рост процентных ставок',
                'asset_returns': {
                    'equity': -0.10,
                    'bonds': -0.15,
                    'commodities': -0.05,
                    'crypto': -0.20
                }
            },
            'inflation_surge': {
                'description': 'Резкий рост инфляции',
                'asset_returns': {
                    'equity': -0.15,
                    'bonds': -0.20,
                    'commodities': 0.10,
                    'crypto': 0.05
                }
            },
            'crypto_crash': {
                'description': 'Обвал криптовалют',
                'asset_returns': {
                    'equity': -0.05,
                    'bonds': 0.02,
                    'commodities': -0.05,
                    'crypto': -0.70
                }
            }
        }
    
    def run_stress_test(self, portfolio_weights, asset_returns):
        """Запуск стресс-теста"""
        stress_results = {}
        
        for scenario_name, scenario in self.stress_scenarios.items():
            # Расчет доходности портфолио в сценарии
            portfolio_return = 0
            for asset, weight in portfolio_weights.items():
                if asset in scenario['asset_returns']:
                    portfolio_return += weight * scenario['asset_returns'][asset]
            
            stress_results[scenario_name] = {
                'portfolio_return': portfolio_return,
                'description': scenario['description']
            }
        
        return stress_results
    
    def calculate_stress_metrics(self, stress_results):
        """Расчет метрик стресс-теста"""
        returns = [result['portfolio_return'] for result in stress_results.values()]
        
        metrics = {
            'worst_case_return': min(returns),
            'average_stress_return': np.mean(returns),
            'stress_volatility': np.std(returns),
            'stress_sharpe': np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
        }
        
        return metrics
```

## Блокчейн-интеграция для портфолио

### 1. DeFi активы

```python
class DeFiPortfolioManager:
    """Менеджер DeFi портфолио"""
    
    def __init__(self, web3_provider, private_key):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = self.web3.eth.account.from_key(private_key)
        self.defi_assets = {}
        self.yield_farming_pools = {}
    
    def add_defi_asset(self, asset_name, contract_address, abi):
        """Добавление DeFi актива"""
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        self.defi_assets[asset_name] = {
            'contract': contract,
            'address': contract_address,
            'balance': 0
        }
    
    def get_defi_balances(self):
        """Получение балансов DeFi активов"""
        balances = {}
        
        for asset_name, asset_info in self.defi_assets.items():
            try:
                balance = asset_info['contract'].functions.balanceOf(self.account.address).call()
                balances[asset_name] = balance
                self.defi_assets[asset_name]['balance'] = balance
            except Exception as e:
                print(f"Error getting balance for {asset_name}: {e}")
                balances[asset_name] = 0
        
        return balances
    
    def calculate_defi_yield(self, asset_name, time_period=30):
        """Расчет доходности DeFi актива"""
        if asset_name not in self.defi_assets:
            return 0
        
        try:
            # Получение информации о пуле
            pool_info = self.defi_assets[asset_name]['contract'].functions.poolInfo(0).call()
            
            # Расчет APR
            total_alloc_point = self.defi_assets[asset_name]['contract'].functions.totalAllocPoint().call()
            reward_per_block = self.defi_assets[asset_name]['contract'].functions.rewardPerBlock().call()
            
            pool_alloc_point = pool_info[1]
            pool_alloc_share = pool_alloc_point / total_alloc_point
            
            # APR
            blocks_per_year = 2102400
            annual_rewards = reward_per_block * pool_alloc_share * blocks_per_year
            total_staked = pool_info[0]
            
            apr = annual_rewards / total_staked if total_staked > 0 else 0
            
            # Доходность за период
            period_yield = apr * (time_period / 365)
            
            return period_yield
            
        except Exception as e:
            print(f"Error calculating yield for {asset_name}: {e}")
            return 0
```

### 2. Yield Farming оптимизация

```python
class YieldFarmingOptimizer:
    """Оптимизатор Yield Farming"""
    
    def __init__(self, defi_manager):
        self.defi_manager = defi_manager
        self.farming_pools = {}
        self.optimization_history = []
    
    def add_farming_pool(self, pool_name, pool_info):
        """Добавление пула для фарминга"""
        self.farming_pools[pool_name] = pool_info
    
    def optimize_farming_allocation(self, total_capital):
        """Оптимизация распределения для фарминга"""
        # Получение APR всех пулов
        pool_aprs = {}
        for pool_name, pool_info in self.farming_pools.items():
            apr = self.defi_manager.calculate_defi_yield(pool_name)
            pool_aprs[pool_name] = apr
        
        # Сортировка пулов по APR
        sorted_pools = sorted(pool_aprs.items(), key=lambda x: x[1], reverse=True)
        
        # Оптимальное распределение
        optimal_allocation = {}
        remaining_capital = total_capital
        
        for pool_name, apr in sorted_pools:
            if apr > 0.1:  # Минимальный APR 10%
                # Максимум 30% капитала в один пул
                max_allocation = min(remaining_capital * 0.3, remaining_capital)
                optimal_allocation[pool_name] = max_allocation
                remaining_capital -= max_allocation
        
        return optimal_allocation
    
    def rebalance_farming_portfolio(self, current_allocation, target_allocation):
        """Перебалансировка фарминга"""
        rebalancing_trades = []
        
        for pool_name in set(current_allocation.keys()) | set(target_allocation.keys()):
            current_amount = current_allocation.get(pool_name, 0)
            target_amount = target_allocation.get(pool_name, 0)
            
            if abs(current_amount - target_amount) > 0.01:  # Минимальное отклонение
                trade_amount = target_amount - current_amount
                rebalancing_trades.append({
                    'pool': pool_name,
                    'amount': trade_amount,
                    'action': 'stake' if trade_amount > 0 else 'unstake'
                })
        
        return rebalancing_trades
```

## Автоматическое управление портфолио

### 1. Система мониторинга

```python
class PortfolioMonitor:
    """Мониторинг портфолио"""
    
    def __init__(self):
        self.performance_metrics = {}
        self.alert_thresholds = {
            'max_drawdown': 0.15,
            'min_sharpe_ratio': 1.0,
            'max_var': 0.05
        }
        self.alerts = []
    
    def monitor_performance(self, portfolio):
        """Мониторинг производительности портфолио"""
        # Расчет метрик
        returns = portfolio.get_returns()
        metrics = self._calculate_metrics(returns)
        
        # Сохранение метрик
        self.performance_metrics[datetime.now()] = metrics
        
        # Проверка алертов
        alerts = self._check_alerts(metrics)
        
        return {
            'metrics': metrics,
            'alerts': alerts
        }
    
    def _calculate_metrics(self, returns):
        """Расчет метрик производительности"""
        metrics = {
            'total_return': np.sum(returns),
            'annualized_return': np.mean(returns) * 252,
            'volatility': np.std(returns) * np.sqrt(252),
            'sharpe_ratio': np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0,
            'max_drawdown': self._calculate_max_drawdown(returns),
            'var_95': self._calculate_var(returns, 0.05)
        }
        
        return metrics
    
    def _check_alerts(self, metrics):
        """Проверка алертов"""
        alerts = []
        
        # Проверка максимальной просадки
        if metrics['max_drawdown'] > self.alert_thresholds['max_drawdown']:
            alerts.append({
                'type': 'high_drawdown',
                'message': f"High drawdown detected: {metrics['max_drawdown']:.2%}",
                'severity': 'high'
            })
        
        # Проверка Sharpe Ratio
        if metrics['sharpe_ratio'] < self.alert_thresholds['min_sharpe_ratio']:
            alerts.append({
                'type': 'low_sharpe',
                'message': f"Low Sharpe ratio: {metrics['sharpe_ratio']:.2f}",
                'severity': 'medium'
            })
        
        # Проверка VaR
        if metrics['var_95'] > self.alert_thresholds['max_var']:
            alerts.append({
                'type': 'high_var',
                'message': f"High VaR: {metrics['var_95']:.2%}",
                'severity': 'high'
            })
        
        return alerts
```

### 2. Автоматическое управление

```python
class AutomatedPortfolioManager:
    """Автоматическое управление портфолио"""
    
    def __init__(self, portfolio, optimizer, monitor):
        self.portfolio = portfolio
        self.optimizer = optimizer
        self.monitor = monitor
        self.rebalancing_schedule = 'weekly'
        self.last_rebalancing = None
    
    def run_automated_management(self):
        """Запуск автоматического управления"""
        # Мониторинг производительности
        performance = self.monitor.monitor_performance(self.portfolio)
        
        # Проверка необходимости перебалансирования
        if self._should_rebalance():
            self._rebalance_portfolio()
        
        # Обработка алертов
        if performance['alerts']:
            self._handle_alerts(performance['alerts'])
        
        return performance
    
    def _should_rebalance(self):
        """Проверка необходимости перебалансирования"""
        # Проверка по расписанию
        if self._is_scheduled_rebalancing():
            return True
        
        # Проверка по производительности
        if self._is_performance_based_rebalancing():
            return True
        
        return False
    
    def _rebalance_portfolio(self):
        """Перебалансировка портфолио"""
        print("Starting portfolio rebalancing...")
        
        # Получение текущих весов
        current_weights = self.portfolio.get_weights()
        
        # Оптимизация новых весов
        expected_returns = self._get_expected_returns()
        cov_matrix = self._get_covariance_matrix()
        
        target_weights = self.optimizer.optimize_portfolio(
            expected_returns, cov_matrix
        )
        
        # Выполнение перебалансирования
        rebalancing_trades = self._calculate_rebalancing_trades(
            current_weights, target_weights
        )
        
        # Выполнение сделок
        for trade in rebalancing_trades:
            self.portfolio.execute_trade(trade)
        
        # Обновление времени последнего перебалансирования
        self.last_rebalancing = datetime.now()
        
        print("Portfolio rebalancing completed")
    
    def _handle_alerts(self, alerts):
        """Обработка алертов"""
        for alert in alerts:
            if alert['severity'] == 'high':
                # Критические алерты - немедленные действия
                self._handle_critical_alert(alert)
            elif alert['severity'] == 'medium':
                # Средние алерты - планирование действий
                self._handle_medium_alert(alert)
```

## Следующие шаги

После изучения оптимизации портфолио переходите к:
- **[16_metrics_analysis.md](16_metrics_analysis.md)** - Метрики и анализ
- **[17_examples.md](17_examples.md)** - Практические примеры

## Ключевые выводы

1. **ML-оптимизация** - использование машинного обучения для оптимизации портфолио
2. **Динамическое перебалансирование** - автоматическая корректировка весов
3. **Мультиактивный анализ** - учет корреляций и волатильности
4. **Продвинутый риск-менеджмент** - VaR, стресс-тестирование
5. **Блокчейн-интеграция** - использование DeFi для увеличения доходности
6. **Автоматическое управление** - полная автоматизация процесса

---

**Важно:** Оптимизация портфолио - это непрерывный процесс, требующий постоянного мониторинга и корректировки.
