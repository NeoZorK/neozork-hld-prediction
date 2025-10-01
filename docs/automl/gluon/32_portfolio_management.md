# Углубленное описание методик для создания и управления портфолио, успешные методы диверсификации

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему управление портфолио - основа успешного инвестирования

**Почему 90% инвесторов теряют деньги?** Потому что они не понимают принципов управления портфолио. Правильная диверсификация и управление рисками - это единственный способ создать стабильно прибыльный портфолио.

### Что дает правильное управление портфолио?
- **Стабильность**: Снижение волатильности и рисков
- **Доходность**: Оптимизация доходности при заданном уровне риска
- **Робастность**: Устойчивость к рыночным шокам
- **Масштабируемость**: Возможность управления большими капиталами

### Что происходит без правильного управления портфолио?
- **Высокие риски**: Концентрация в одном активе или секторе
- **Нестабильность**: Резкие колебания стоимости портфолио
- **Потери**: Значительные потери во время кризисов
- **Разочарование**: Недостижение инвестиционных целей

## Теоретические основы управления портфолио

### Математические принципы

**Оптимизация портфолио как задача оптимизации:**

```
max w^T μ - λ/2 * w^T Σ w
subject to: w^T 1 = 1, w ≥ 0
```

Где:
- `w` - веса активов в портфолио
- `μ` - ожидаемая доходность активов
- `Σ` - ковариационная матрица активов
- `λ` - коэффициент риска

**Критерии качества портфолио:**

1. **Доходность**: E[R_p] = w^T μ
2. **Риск**: Var[R_p] = w^T Σ w
3. **Коэффициент Шарпа**: (E[R_p] - r_f) / √Var[R_p]
4. **VaR**: P(R_p ≤ VaR) = α

### Типы портфолио

**1. Консервативное портфолио**
- Низкий риск, низкая доходность
- Облигации, депозиты
- Подходит для консервативных инвесторов

**2. Сбалансированное портфолио**
- Средний риск, средняя доходность
- Смесь акций и облигаций
- Подходит для большинства инвесторов

**3. Агрессивное портфолио**
- Высокий риск, высокая доходность
- Акции, альтернативные инвестиции
- Подходит для агрессивных инвесторов

**4. Диверсифицированное портфолио**
- Оптимальное соотношение риск/доходность
- Различные классы активов
- Наиболее эффективное

## Продвинутые методики создания портфолио

### 1. Классические методы оптимизации

**Markowitz Mean-Variance Optimization:**

```python
def markowitz_optimization(expected_returns, cov_matrix, risk_aversion=1.0, 
                          target_return=None, target_volatility=None):
    """Оптимизация портфолио по Markowitz"""
    from scipy.optimize import minimize
    
    n_assets = len(expected_returns)
    
    # Ограничения
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]  # Сумма весов = 1
    
    if target_return is not None:
        constraints.append({
            'type': 'eq', 
            'fun': lambda w: np.dot(w, expected_returns) - target_return
        })
    
    if target_volatility is not None:
        constraints.append({
            'type': 'eq', 
            'fun': lambda w: np.sqrt(np.dot(w, np.dot(cov_matrix, w))) - target_volatility
        })
    
    # Границы
    bounds = [(0, 1) for _ in range(n_assets)]  # Веса от 0 до 1
    
    # Целевая функция
    def objective(w):
        portfolio_return = np.dot(w, expected_returns)
        portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
        return -portfolio_return + risk_aversion * portfolio_variance
    
    # Начальные веса
    x0 = np.ones(n_assets) / n_assets
    
    # Оптимизация
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed")
    
# Пример использования
weights = markowitz_optimization(expected_returns, cov_matrix, risk_aversion=1.0)
```

**Black-Litterman Model:**

```python
def black_litterman_optimization(market_caps, cov_matrix, risk_aversion=3.0, 
                                views=None, view_confidences=None):
    """Оптимизация портфолио по Black-Litterman"""
    n_assets = len(market_caps)
    
    # Рыночные веса
    market_weights = market_caps / np.sum(market_caps)
    
    # Ожидаемая доходность рынка
    market_return = risk_aversion * np.dot(cov_matrix, market_weights)
    
    if views is not None:
        # Матрица взглядов
        P = np.array(views)
        n_views = len(views)
        
        # Уверенность во взглядах
        if view_confidences is None:
            view_confidences = np.ones(n_views) * 0.1
        
        # Матрица ковариации взглядов
        Omega = np.diag(view_confidences)
        
        # Ожидаемые доходности взглядов
        Q = np.array([view[1] for view in views])
        
        # Black-Litterman формулы
        tau = 1.0  # Масштабирующий параметр
        M1 = np.linalg.inv(tau * cov_matrix)
        M2 = np.dot(P.T, np.dot(np.linalg.inv(Omega), P))
        M3 = np.dot(P.T, np.dot(np.linalg.inv(Omega), Q))
        
        # Ожидаемые доходности
        expected_returns = np.dot(np.linalg.inv(M1 + M2), 
                                np.dot(M1, market_return) + M3)
        
        # Ковариационная матрица
        portfolio_cov = np.linalg.inv(M1 + M2)
    else:
        expected_returns = market_return
        portfolio_cov = cov_matrix
    
    # Оптимизация Markowitz
    weights = markowitz_optimization(expected_returns, portfolio_cov, risk_aversion)
    
    return weights, expected_returns, portfolio_cov

# Пример использования
weights, expected_returns, portfolio_cov = black_litterman_optimization(
    market_caps, cov_matrix, risk_aversion=3.0, views=views
)
```

### 2. Современные методы оптимизации

**Risk Parity Portfolio:**

```python
def risk_parity_optimization(cov_matrix, target_risk=None):
    """Оптимизация портфолио с равным риском"""
    from scipy.optimize import minimize
    
    n_assets = len(cov_matrix)
    
    # Целевая функция - минимизация суммы квадратов разностей рисков
    def objective(w):
        portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
        individual_risks = np.sqrt(np.diag(cov_matrix))
        target_risks = w * individual_risks
        
        # Нормализация
        if target_risk is not None:
            target_risks = target_risks / np.sum(target_risks) * target_risk
        
        return np.sum((target_risks - target_risks.mean()) ** 2)
    
    # Ограничения
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1) for _ in range(n_assets)]
    
    # Начальные веса
    x0 = np.ones(n_assets) / n_assets
    
    # Оптимизация
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed")

# Пример использования
weights = risk_parity_optimization(cov_matrix, target_risk=0.1)
```

**Minimum Variance Portfolio:**

```python
def minimum_variance_optimization(cov_matrix):
    """Оптимизация портфолио с минимальной дисперсией"""
    from scipy.optimize import minimize
    
    n_assets = len(cov_matrix)
    
    # Целевая функция - минимизация дисперсии
    def objective(w):
        return np.dot(w, np.dot(cov_matrix, w))
    
    # Ограничения
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1) for _ in range(n_assets)]
    
    # Начальные веса
    x0 = np.ones(n_assets) / n_assets
    
    # Оптимизация
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed")

# Пример использования
weights = minimum_variance_optimization(cov_matrix)
```

**Maximum Sharpe Portfolio:**

```python
def maximum_sharpe_optimization(expected_returns, cov_matrix, risk_free_rate=0.02):
    """Оптимизация портфолио с максимальным коэффициентом Шарпа"""
    from scipy.optimize import minimize
    
    n_assets = len(expected_returns)
    
    # Целевая функция - максимизация коэффициента Шарпа
    def objective(w):
        portfolio_return = np.dot(w, expected_returns)
        portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
        sharpe = (portfolio_return - risk_free_rate) / np.sqrt(portfolio_variance)
        return -sharpe  # Минимизируем отрицательный Sharpe
    
    # Ограничения
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1) for _ in range(n_assets)]
    
    # Начальные веса
    x0 = np.ones(n_assets) / n_assets
    
    # Оптимизация
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed")

# Пример использования
weights = maximum_sharpe_optimization(expected_returns, cov_matrix, risk_free_rate=0.02)
```

### 3. Машинное обучение в управлении портфолио

**Clustering-based Portfolio:**

```python
def clustering_portfolio_optimization(returns, n_clusters=5, method='kmeans'):
    """Оптимизация портфолио на основе кластеризации"""
    from sklearn.cluster import KMeans, AgglomerativeClustering
    from sklearn.preprocessing import StandardScaler
    
    # Нормализация данных
    scaler = StandardScaler()
    returns_scaled = scaler.fit_transform(returns)
    
    # Кластеризация
    if method == 'kmeans':
        clusterer = KMeans(n_clusters=n_clusters, random_state=42)
    elif method == 'hierarchical':
        clusterer = AgglomerativeClustering(n_clusters=n_clusters)
    else:
        raise ValueError(f"Unknown clustering method: {method}")
    
    clusters = clusterer.fit_predict(returns_scaled)
    
    # Создание портфолио для каждого кластера
    portfolio_weights = {}
    
    for cluster_id in range(n_clusters):
        cluster_returns = returns[clusters == cluster_id]
        
        if len(cluster_returns) > 1:
            # Оптимизация внутри кластера
            cluster_cov = np.cov(cluster_returns.T)
            cluster_expected_returns = np.mean(cluster_returns, axis=0)
            
            # Минимальная дисперсия внутри кластера
            cluster_weights = minimum_variance_optimization(cluster_cov)
            
            # Нормализация весов
            cluster_weights = cluster_weights / np.sum(cluster_weights)
            
            portfolio_weights[cluster_id] = {
                'weights': cluster_weights,
                'assets': cluster_returns.columns[clusters == cluster_id].tolist()
            }
    
    return portfolio_weights

# Пример использования
clustering_portfolio = clustering_portfolio_optimization(returns, n_clusters=5, method='kmeans')
```

**ML-based Portfolio Optimization:**

```python
def ml_portfolio_optimization(returns, features, model, n_portfolios=1000):
    """Оптимизация портфолио с использованием машинного обучения"""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    
    # Подготовка данных
    X = features
    y = returns
    
    # Разделение на train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Обучение модели
    model.fit(X_train, y_train)
    
    # Предсказания
    predictions = model.predict(X_test)
    
    # Создание множества портфолио
    portfolios = []
    
    for i in range(n_portfolios):
        # Случайные веса
        weights = np.random.dirichlet(np.ones(len(returns.columns)))
        
        # Ожидаемая доходность портфолио
        portfolio_return = np.dot(weights, predictions.mean(axis=0))
        
        # Риск портфолио
        portfolio_variance = np.dot(weights, np.dot(predictions.cov(), weights))
        
        # Коэффициент Шарпа
        sharpe = portfolio_return / np.sqrt(portfolio_variance)
        
        portfolios.append({
            'weights': weights,
            'return': portfolio_return,
            'variance': portfolio_variance,
            'sharpe': sharpe
        })
    
    # Выбор лучшего портфолио
    best_portfolio = max(portfolios, key=lambda x: x['sharpe'])
    
    return best_portfolio, portfolios

# Пример использования
best_portfolio, all_portfolios = ml_portfolio_optimization(returns, features, model)
```

## Методы диверсификации

### 1. Классическая диверсификация

**Географическая диверсификация:**

```python
def geographic_diversification(returns_by_country, max_weight_per_country=0.3):
    """Географическая диверсификация портфолио"""
    n_countries = len(returns_by_country)
    
    # Ограничения по странам
    constraints = []
    bounds = []
    
    for i in range(n_countries):
        # Максимальный вес на страну
        constraints.append({
            'type': 'ineq',
            'fun': lambda w, i=i: max_weight_per_country - w[i]
        })
        bounds.append((0, max_weight_per_country))
    
    # Сумма весов = 1
    constraints.append({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    
    # Ожидаемые доходности по странам
    expected_returns = np.array([returns.mean() for returns in returns_by_country.values()])
    
    # Ковариационная матрица
    cov_matrix = np.cov([returns for returns in returns_by_country.values()])
    
    # Оптимизация
    from scipy.optimize import minimize
    
    def objective(w):
        portfolio_return = np.dot(w, expected_returns)
        portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
        return -portfolio_return + 0.5 * portfolio_variance
    
    x0 = np.ones(n_countries) / n_countries
    
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed")

# Пример использования
country_weights = geographic_diversification(returns_by_country, max_weight_per_country=0.3)
```

**Секторальная диверсификация:**

```python
def sectoral_diversification(returns_by_sector, max_weight_per_sector=0.25):
    """Секторальная диверсификация портфолио"""
    n_sectors = len(returns_by_sector)
    
    # Ограничения по секторам
    constraints = []
    bounds = []
    
    for i in range(n_sectors):
        # Максимальный вес на сектор
        constraints.append({
            'type': 'ineq',
            'fun': lambda w, i=i: max_weight_per_sector - w[i]
        })
        bounds.append((0, max_weight_per_sector))
    
    # Сумма весов = 1
    constraints.append({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    
    # Ожидаемые доходности по секторам
    expected_returns = np.array([returns.mean() for returns in returns_by_sector.values()])
    
    # Ковариационная матрица
    cov_matrix = np.cov([returns for returns in returns_by_sector.values()])
    
    # Оптимизация
    from scipy.optimize import minimize
    
    def objective(w):
        portfolio_return = np.dot(w, expected_returns)
        portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
        return -portfolio_return + 0.5 * portfolio_variance
    
    x0 = np.ones(n_sectors) / n_sectors
    
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed")

# Пример использования
sector_weights = sectoral_diversification(returns_by_sector, max_weight_per_sector=0.25)
```

### 2. Продвинутые методы диверсификации

**Factor-based Diversification:**

```python
def factor_diversification(returns, factors, max_factor_exposure=0.5):
    """Диверсификация на основе факторов"""
    from sklearn.linear_model import LinearRegression
    
    n_assets = len(returns.columns)
    n_factors = len(factors.columns)
    
    # Регрессия доходностей на факторы
    factor_loadings = np.zeros((n_assets, n_factors))
    
    for i, asset in enumerate(returns.columns):
        model = LinearRegression()
        model.fit(factors, returns[asset])
        factor_loadings[i] = model.coef_
    
    # Ограничения по факторам
    constraints = []
    bounds = [(0, 1) for _ in range(n_assets)]
    
    for j in range(n_factors):
        # Максимальная экспозиция к фактору
        constraints.append({
            'type': 'ineq',
            'fun': lambda w, j=j: max_factor_exposure - np.dot(w, factor_loadings[:, j])
        })
        constraints.append({
            'type': 'ineq',
            'fun': lambda w, j=j: max_factor_exposure + np.dot(w, factor_loadings[:, j])
        })
    
    # Сумма весов = 1
    constraints.append({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    
    # Ожидаемые доходности
    expected_returns = returns.mean().values
    
    # Ковариационная матрица
    cov_matrix = returns.cov().values
    
    # Оптимизация
    from scipy.optimize import minimize
    
    def objective(w):
        portfolio_return = np.dot(w, expected_returns)
        portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
        return -portfolio_return + 0.5 * portfolio_variance
    
    x0 = np.ones(n_assets) / n_assets
    
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed")

# Пример использования
factor_weights = factor_diversification(returns, factors, max_factor_exposure=0.5)
```

**Correlation-based Diversification:**

```python
def correlation_diversification(returns, max_correlation=0.7):
    """Диверсификация на основе корреляций"""
    # Корреляционная матрица
    corr_matrix = returns.corr()
    
    # Поиск активов с низкой корреляцией
    selected_assets = []
    remaining_assets = list(returns.columns)
    
    # Выбор первого актива
    first_asset = remaining_assets[0]
    selected_assets.append(first_asset)
    remaining_assets.remove(first_asset)
    
    # Выбор остальных активов
    while remaining_assets:
        best_asset = None
        best_score = -1
        
        for asset in remaining_assets:
            # Средняя корреляция с уже выбранными активами
            avg_correlation = corr_matrix.loc[asset, selected_assets].mean()
            
            # Оценка диверсификации
            diversification_score = 1 - avg_correlation
            
            if diversification_score > best_score:
                best_score = diversification_score
                best_asset = asset
        
        if best_asset and best_score > (1 - max_correlation):
            selected_assets.append(best_asset)
            remaining_assets.remove(best_asset)
        else:
            break
    
    # Оптимизация весов для выбранных активов
    selected_returns = returns[selected_assets]
    expected_returns = selected_returns.mean().values
    cov_matrix = selected_returns.cov().values
    
    # Равные веса
    weights = np.ones(len(selected_assets)) / len(selected_assets)
    
    return weights, selected_assets

# Пример использования
weights, selected_assets = correlation_diversification(returns, max_correlation=0.7)
```

## Управление рисками портфолио

### 1. Value at Risk (VaR)

**Historical VaR:**

```python
def historical_var(returns, confidence_level=0.95):
    """Исторический VaR"""
    # Сортировка доходностей
    sorted_returns = np.sort(returns)
    
    # Индекс для VaR
    var_index = int((1 - confidence_level) * len(sorted_returns))
    
    # VaR
    var = sorted_returns[var_index]
    
    return var

# Пример использования
var_95 = historical_var(portfolio_returns, confidence_level=0.95)
```

**Parametric VaR:**

```python
def parametric_var(returns, confidence_level=0.95):
    """Параметрический VaR"""
    from scipy import stats
    
    # Параметры нормального распределения
    mean_return = returns.mean()
    std_return = returns.std()
    
    # Z-score для заданного уровня доверия
    z_score = stats.norm.ppf(1 - confidence_level)
    
    # VaR
    var = mean_return + z_score * std_return
    
    return var

# Пример использования
var_95 = parametric_var(portfolio_returns, confidence_level=0.95)
```

**Monte Carlo VaR:**

```python
def monte_carlo_var(returns, confidence_level=0.95, n_simulations=10000):
    """Monte Carlo VaR"""
    # Параметры распределения
    mean_return = returns.mean()
    std_return = returns.std()
    
    # Симуляции
    simulations = np.random.normal(mean_return, std_return, n_simulations)
    
    # VaR
    var = np.percentile(simulations, (1 - confidence_level) * 100)
    
    return var

# Пример использования
var_95 = monte_carlo_var(portfolio_returns, confidence_level=0.95, n_simulations=10000)
```

### 2. Expected Shortfall (ES)

```python
def expected_shortfall(returns, confidence_level=0.95):
    """Expected Shortfall (Conditional VaR)"""
    # VaR
    var = historical_var(returns, confidence_level)
    
    # Ожидаемый убыток при превышении VaR
    es = returns[returns <= var].mean()
    
    return es

# Пример использования
es_95 = expected_shortfall(portfolio_returns, confidence_level=0.95)
```

### 3. Максимальная просадка

```python
def maximum_drawdown(returns):
    """Максимальная просадка"""
    # Кумулятивная доходность
    cumulative_returns = (1 + returns).cumprod()
    
    # Скользящий максимум
    running_max = cumulative_returns.expanding().max()
    
    # Просадка
    drawdown = (cumulative_returns - running_max) / running_max
    
    # Максимальная просадка
    max_drawdown = drawdown.min()
    
    return max_drawdown

# Пример использования
max_dd = maximum_drawdown(portfolio_returns)
```

## Динамическое управление портфолио

### 1. Ребалансировка

**Временная ребалансировка:**

```python
def time_based_rebalancing(returns, target_weights, rebalance_freq='M'):
    """Ребалансировка по времени"""
    # Создание индекса для ребалансировки
    if rebalance_freq == 'D':
        rebalance_dates = returns.index
    elif rebalance_freq == 'W':
        rebalance_dates = returns.index[::7]
    elif rebalance_freq == 'M':
        rebalance_dates = returns.index[::30]
    elif rebalance_freq == 'Q':
        rebalance_dates = returns.index[::90]
    else:
        raise ValueError(f"Unknown rebalance frequency: {rebalance_freq}")
    
    # Ребалансировка
    rebalanced_returns = []
    current_weights = target_weights.copy()
    
    for i, date in enumerate(returns.index):
        if date in rebalance_dates:
            current_weights = target_weights.copy()
        
        # Доходность портфолио
        portfolio_return = np.dot(current_weights, returns.loc[date])
        rebalanced_returns.append(portfolio_return)
    
    return pd.Series(rebalanced_returns, index=returns.index)

# Пример использования
rebalanced_returns = time_based_rebalancing(returns, target_weights, rebalance_freq='M')
```

**Пороговая ребалансировка:**

```python
def threshold_rebalancing(returns, target_weights, threshold=0.05):
    """Ребалансировка по порогу отклонения"""
    rebalanced_returns = []
    current_weights = target_weights.copy()
    
    for i, date in enumerate(returns.index):
        # Проверка отклонения весов
        weight_deviation = np.abs(current_weights - target_weights)
        max_deviation = weight_deviation.max()
        
        if max_deviation > threshold:
            current_weights = target_weights.copy()
        
        # Доходность портфолио
        portfolio_return = np.dot(current_weights, returns.loc[date])
        rebalanced_returns.append(portfolio_return)
    
    return pd.Series(rebalanced_returns, index=returns.index)

# Пример использования
rebalanced_returns = threshold_rebalancing(returns, target_weights, threshold=0.05)
```

### 2. Адаптивное управление

**Volatility-based Rebalancing:**

```python
def volatility_based_rebalancing(returns, target_weights, volatility_window=30, 
                                volatility_threshold=0.02):
    """Ребалансировка на основе волатильности"""
    rebalanced_returns = []
    current_weights = target_weights.copy()
    
    for i, date in enumerate(returns.index):
        if i >= volatility_window:
            # Расчет волатильности
            recent_returns = returns.iloc[i-volatility_window:i]
            volatility = recent_returns.std().mean()
            
            # Ребалансировка при высокой волатильности
            if volatility > volatility_threshold:
                current_weights = target_weights.copy()
        
        # Доходность портфолио
        portfolio_return = np.dot(current_weights, returns.loc[date])
        rebalanced_returns.append(portfolio_return)
    
    return pd.Series(rebalanced_returns, index=returns.index)

# Пример использования
rebalanced_returns = volatility_based_rebalancing(returns, target_weights, 
                                                 volatility_window=30, volatility_threshold=0.02)
```

**Momentum-based Rebalancing:**

```python
def momentum_based_rebalancing(returns, target_weights, momentum_window=20, 
                              momentum_threshold=0.1):
    """Ребалансировка на основе моментума"""
    rebalanced_returns = []
    current_weights = target_weights.copy()
    
    for i, date in enumerate(returns.index):
        if i >= momentum_window:
            # Расчет моментума
            recent_returns = returns.iloc[i-momentum_window:i]
            momentum = recent_returns.mean().mean()
            
            # Ребалансировка при изменении моментума
            if abs(momentum) > momentum_threshold:
                current_weights = target_weights.copy()
        
        # Доходность портфолио
        portfolio_return = np.dot(current_weights, returns.loc[date])
        rebalanced_returns.append(portfolio_return)
    
    return pd.Series(rebalanced_returns, index=returns.index)

# Пример использования
rebalanced_returns = momentum_based_rebalancing(returns, target_weights, 
                                               momentum_window=20, momentum_threshold=0.1)
```

## Мониторинг и оценка портфолио

### 1. Метрики производительности

```python
def calculate_portfolio_metrics(returns, risk_free_rate=0.02):
    """Расчет метрик производительности портфолио"""
    # Базовые метрики
    total_return = (1 + returns).prod() - 1
    annual_return = (1 + returns).mean() ** 252 - 1
    volatility = returns.std() * np.sqrt(252)
    
    # Коэффициент Шарпа
    sharpe = (annual_return - risk_free_rate) / volatility
    
    # Максимальная просадка
    max_drawdown = maximum_drawdown(returns)
    
    # Коэффициент Сортино
    downside_returns = returns[returns < 0]
    downside_volatility = downside_returns.std() * np.sqrt(252)
    sortino = (annual_return - risk_free_rate) / downside_volatility if downside_volatility > 0 else 0
    
    # Коэффициент Кальмара
    calmar = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'volatility': volatility,
        'sharpe': sharpe,
        'max_drawdown': max_drawdown,
        'sortino': sortino,
        'calmar': calmar
    }

# Пример использования
metrics = calculate_portfolio_metrics(portfolio_returns, risk_free_rate=0.02)
```

### 2. Анализ рисков

```python
def analyze_portfolio_risks(returns, confidence_levels=[0.90, 0.95, 0.99]):
    """Анализ рисков портфолио"""
    risks = {}
    
    for level in confidence_levels:
        # VaR
        var = historical_var(returns, level)
        
        # ES
        es = expected_shortfall(returns, level)
        
        # Максимальная просадка
        max_dd = maximum_drawdown(returns)
        
        risks[level] = {
            'var': var,
            'es': es,
            'max_drawdown': max_dd
        }
    
    return risks

# Пример использования
risks = analyze_portfolio_risks(portfolio_returns, confidence_levels=[0.90, 0.95, 0.99])
```

### 3. Визуализация портфолио

```python
def visualize_portfolio_performance(returns, benchmark_returns=None, save_path=None):
    """Визуализация производительности портфолио"""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Настройка стиля
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Создание фигуры
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Кумулятивная доходность
    cumulative_returns = (1 + returns).cumprod()
    axes[0, 0].plot(cumulative_returns.index, cumulative_returns.values, label='Портфолио')
    
    if benchmark_returns is not None:
        benchmark_cumulative = (1 + benchmark_returns).cumprod()
        axes[0, 0].plot(benchmark_cumulative.index, benchmark_cumulative.values, 
                       label='Бенчмарк', linestyle='--')
    
    axes[0, 0].set_title('Кумулятивная доходность')
    axes[0, 0].set_xlabel('Дата')
    axes[0, 0].set_ylabel('Кумулятивная доходность')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # 2. Распределение доходностей
    axes[0, 1].hist(returns, bins=50, alpha=0.7, edgecolor='black')
    axes[0, 1].axvline(returns.mean(), color='red', linestyle='--', 
                      label=f'Среднее: {returns.mean():.4f}')
    axes[0, 1].set_title('Распределение доходностей')
    axes[0, 1].set_xlabel('Доходность')
    axes[0, 1].set_ylabel('Частота')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # 3. Просадка
    cumulative_returns = (1 + returns).cumprod()
    running_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - running_max) / running_max
    
    axes[1, 0].fill_between(drawdown.index, drawdown.values, 0, alpha=0.3, color='red')
    axes[1, 0].plot(drawdown.index, drawdown.values, color='red')
    axes[1, 0].set_title('Просадка')
    axes[1, 0].set_xlabel('Дата')
    axes[1, 0].set_ylabel('Просадка')
    axes[1, 0].grid(True)
    
    # 4. Скользящий коэффициент Шарпа
    rolling_sharpe = returns.rolling(252).mean() / returns.rolling(252).std() * np.sqrt(252)
    axes[1, 1].plot(rolling_sharpe.index, rolling_sharpe.values)
    axes[1, 1].axhline(y=1.0, color='red', linestyle='--', label='Sharpe = 1.0')
    axes[1, 1].set_title('Скользящий коэффициент Шарпа')
    axes[1, 1].set_xlabel('Дата')
    axes[1, 1].set_ylabel('Коэффициент Шарпа')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

# Пример использования
visualize_portfolio_performance(portfolio_returns, benchmark_returns, 
                              save_path='portfolio_performance.png')
```

## Заключение

Управление портфолио - это основа успешного инвестирования. Правильная диверсификация и управление рисками позволяют:

1. **Создать стабильный портфолио** - снизить волатильность и риски
2. **Оптимизировать доходность** - максимизировать доходность при заданном уровне риска
3. **Управлять рисками** - контролировать потенциальные потери
4. **Адаптироваться к изменениям** - динамически управлять портфолио

### Ключевые принципы:

1. **Диверсификация** - не кладите все яйца в одну корзину
2. **Управление рисками** - контролируйте VaR и максимальную просадку
3. **Ребалансировка** - регулярно корректируйте веса
4. **Мониторинг** - постоянно отслеживайте производительность
5. **Адаптивность** - приспосабливайтесь к изменяющимся условиям

### Следующие шаги:

После освоения управления портфолио вы готовы к созданию полноценных торговых систем, которые объединяют:
- [Feature Generation](./26_feature_generation_advanced.md)
- [Бэктестинг](./27_backtesting_methods.md)
- [Walk-forward анализ](./28_walk_forward_analysis.md)
- [Monte Carlo симуляции](./29_monte_carlo_simulations.md)
- Управление портфолио (текущая глава)
