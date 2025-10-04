# Углубленное описание методик для создания и управления портфолио, успешные методы диверсификации

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему управление портфолио - основа успешного инвестирования

### 🎯 Важность управления портфолио для успешного инвестирования

```mermaid
graph TD
    A[Инвестор] --> B{Правильное управление портфолио?}
    
    B -->|Нет| C[90% инвесторов теряют деньги]
    C --> D[❌ Высокие риски<br/>Концентрация в одном активе]
    C --> E[❌ Нестабильность<br/>Резкие колебания стоимости]
    C --> F[❌ Значительные потери<br/>Во время кризисов]
    C --> G[❌ Недостижение целей<br/>Разочарование в инвестициях]
    
    B -->|Да| H[10% успешных инвесторов]
    H --> I[✅ Стабильность<br/>Снижение волатильности и рисков]
    H --> J[✅ Оптимизация доходности<br/>При заданном уровне риска]
    H --> K[✅ Робастность<br/>Устойчивость к рыночным шокам]
    H --> L[✅ Масштабируемость<br/>Управление большими капиталами]
    
    I --> M[Диверсификация активов]
    J --> N[Оптимизация весов]
    K --> O[Управление рисками]
    L --> P[Профессиональный подход]
    
    M --> Q[Успешный портфолио]
    N --> Q
    O --> Q
    P --> Q
    
    Q --> R[✅ Стабильно прибыльные инвестиции]
    
    style A fill:#e3f2fd
    style H fill:#c8e6c9
    style C fill:#ffcdd2
    style R fill:#4caf50
```

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

```math
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

### 📊 Сравнение типов портфолио

```mermaid
graph TB
    A[Типы портфолио] --> B[Консервативное портфолио]
    A --> C[Сбалансированное портфолио]
    A --> D[Агрессивное портфолио]
    A --> E[Диверсифицированное портфолио]
    
    B --> B1[Низкий риск, низкая доходность<br/>Risk: 5-10%, Return: 3-6%]
    B --> B2[Облигации, депозиты<br/>Government bonds, CDs]
    B --> B3[✅ Подходит для консервативных инвесторов<br/>Пенсионеры, новички]
    B --> B4[🛡️ Защита капитала<br/>Минимальные потери]
    B --> B5[📈 Стабильный рост<br/>Предсказуемые результаты]
    
    C --> C1[Средний риск, средняя доходность<br/>Risk: 10-15%, Return: 6-10%]
    C --> C2[Смесь акций и облигаций<br/>60% Stocks, 40% Bonds]
    C --> C3[✅ Подходит для большинства инвесторов<br/>Средний возраст, опыт]
    C --> C4[⚖️ Баланс риска и доходности<br/>Оптимальное соотношение]
    C --> C5[🔄 Гибкость<br/>Возможность корректировки]
    
    D --> D1[Высокий риск, высокая доходность<br/>Risk: 15-25%, Return: 10-15%]
    D --> D2[Акции, альтернативные инвестиции<br/>Stocks, REITs, Commodities]
    D --> D3[✅ Подходит для агрессивных инвесторов<br/>Молодые, опытные]
    D --> D4[🚀 Высокий потенциал роста<br/>Максимальная доходность]
    D --> D5[⚠️ Высокая волатильность<br/>Значительные колебания]
    
    E --> E1[Оптимальное соотношение риск/доходность<br/>Risk: 8-12%, Return: 8-12%]
    E --> E2[Различные классы активов<br/>Stocks, Bonds, REITs, Commodities, Cash]
    E --> E3[✅ Наиболее эффективное<br/>Профессиональные инвесторы]
    E --> E4[🎯 Максимальная диверсификация<br/>Снижение корреляций]
    E --> E5[📊 Научный подход<br/>Математическая оптимизация]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#ffcdd2
    style E fill:#4caf50
```

#### 1. Консервативное портфолио

- Низкий риск, низкая доходность
- Облигации, депозиты
- Подходит для консервативных инвесторов

#### 2. Сбалансированное портфолио

- Средний риск, средняя доходность
- Смесь акций и облигаций
- Подходит для большинства инвесторов

#### 3. Агрессивное портфолио

- Высокий риск, высокая доходность
- Акции, альтернативные инвестиции
- Подходит для агрессивных инвесторов

#### 4. Диверсифицированное портфолио

- Оптимальное соотношение риск/доходность
- Различные классы активов
- Наиболее эффективное

## Продвинутые методики создания портфолио

### 1. Классические методы оптимизации

### 🔧 Методы оптимизации портфолио

```mermaid
graph TD
    A[Методы оптимизации портфолио] --> B[Классические методы]
    A --> C[Современные методы]
    A --> D[ML-методы]
    
    B --> B1[Markowitz Mean-Variance<br/>max w^T μ - λ/2 * w^T Σ w]
    B --> B2[Black-Litterman Model<br/>Incorporates market views]
    B --> B3[Capital Asset Pricing Model<br/>CAPM framework]
    
    C --> C1[Risk Parity Portfolio<br/>Equal risk contribution]
    C --> C2[Minimum Variance Portfolio<br/>Minimize portfolio variance]
    C --> C3[Maximum Sharpe Portfolio<br/>Maximize Sharpe ratio]
    C --> C4[Equal Weight Portfolio<br/>1/N allocation]
    
    D --> D1[Clustering-based Portfolio<br/>K-means, Hierarchical]
    D --> D2[ML-based Optimization<br/>Random Forest, Neural Networks]
    D --> D3[Factor-based Portfolio<br/>Fama-French factors]
    D --> D4[Reinforcement Learning<br/>Dynamic optimization]
    
    B1 --> E[Целевая функция<br/>Utility = Return - λ * Risk]
    B2 --> F[Включение взглядов<br/>P * μ = Q + ε]
    C1 --> G[Равный вклад в риск<br/>w_i * σ_i = constant]
    C2 --> H[Минимизация дисперсии<br/>min w^T Σ w]
    C3 --> I[Максимизация Sharpe<br/>max (μ - r_f) / σ]
    
    D1 --> J[Кластеризация активов<br/>Similar assets grouped]
    D2 --> K[ML предсказания<br/>Predict returns/risks]
    D3 --> L[Факторная модель<br/>R = α + β * F + ε]
    D4 --> M[Адаптивное обучение<br/>Q-learning, Policy gradient]
    
    E --> N[Оптимизация портфолио]
    F --> N
    G --> N
    H --> N
    I --> N
    J --> N
    K --> N
    L --> N
    M --> N
    
    N --> O[Оптимальные веса<br/>w* = argmax Utility]
    O --> P[Оценка производительности<br/>Sharpe, VaR, Max DD]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style O fill:#4caf50
```

**Markowitz Mean-Variance Optimization:**

```python
def markowitz_optimization(expected_returns, cov_matrix, risk_aversion=1.0, 
                          target_return=None, target_volatility=None):
    """
    Оптимизация портфолио по Markowitz
    
    Parameters:
    -----------
    expected_returns : array-like, shape (n_assets,)
        Ожидаемые доходности активов. Должен быть одномерный массив или список
        с ожидаемыми доходностями для каждого актива в портфолио.
        Пример: [0.08, 0.12, 0.06, 0.10] для 4 активов
        
    cov_matrix : array-like, shape (n_assets, n_assets)
        Ковариационная матрица активов. Должна быть квадратной матрицей
        размером n_assets x n_assets, где элемент (i,j) представляет
        ковариацию между активами i и j. Матрица должна быть симметричной
        и положительно определенной.
        
    risk_aversion : float, default=1.0
        Коэффициент неприятия риска. Определяет баланс между доходностью
        и риском в целевой функции. Чем больше значение, тем больше
        инвестор избегает риска:
        - 0.5: Агрессивный инвестор (низкое неприятие риска)
        - 1.0: Умеренный инвестор (стандартное значение)
        - 2.0: Консервативный инвестор (высокое неприятие риска)
        - 5.0: Очень консервативный инвестор
        
    target_return : float, optional, default=None
        Целевая доходность портфолио. Если указана, оптимизация будет
        искать портфолио с минимальным риском при заданной доходности.
        Должна быть в том же формате, что и expected_returns (например, 0.10 для 10%).
        Если None, оптимизируется по критерию максимизации полезности.
        
    target_volatility : float, optional, default=None
        Целевая волатильность портфолио. Если указана, оптимизация будет
        искать портфолио с максимальной доходностью при заданной волатильности.
        Должна быть в том же формате, что и expected_returns (например, 0.15 для 15%).
        Если None, оптимизируется по критерию максимизации полезности.
        
    Returns:
    --------
    array-like, shape (n_assets,)
        Оптимальные веса активов в портфолио. Сумма весов равна 1.0.
        Каждый элемент представляет долю капитала, инвестированного в соответствующий актив.
        
    Raises:
    -------
    ValueError
        Если оптимизация не удалась (например, несовместимые ограничения)
        
    Notes:
    ------
    Целевая функция: max w^T * μ - (λ/2) * w^T * Σ * w
    где w - веса, μ - ожидаемые доходности, Σ - ковариационная матрица, λ - risk_aversion
    
    Ограничения:
    - Сумма весов = 1 (полное инвестирование)
    - Веса >= 0 (запрет коротких продаж)
    - Дополнительные ограничения на доходность или волатильность (если указаны)
    """
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
    """
    Оптимизация портфолио по модели Black-Litterman
    
    Модель Black-Litterman объединяет рыночные веса с субъективными взглядами
    инвестора для получения более стабильных и интуитивных весов портфолио.
    
    Parameters:
    -----------
    market_caps : array-like, shape (n_assets,)
        Рыночные капитализации активов. Используются для расчета рыночных весов
        как отправной точки оптимизации. Должен быть одномерный массив или список
        с рыночными капитализациями для каждого актива.
        Пример: [1000000, 2000000, 500000, 1500000] для 4 активов
        
    cov_matrix : array-like, shape (n_assets, n_assets)
        Ковариационная матрица активов. Должна быть квадратной матрицей
        размером n_assets x n_assets, где элемент (i,j) представляет
        ковариацию между активами i и j. Матрица должна быть симметричной
        и положительно определенной.
        
    risk_aversion : float, default=3.0
        Коэффициент неприятия риска рынка. Обычно принимает значения от 1.0 до 5.0.
        Чем больше значение, тем больше рынок избегает риска:
        - 1.0-2.0: Низкое неприятие риска (агрессивный рынок)
        - 3.0: Стандартное значение для развитых рынков
        - 4.0-5.0: Высокое неприятие риска (консервативный рынок)
        
    views : list of tuples, optional, default=None
        Субъективные взгляды инвестора на активы. Каждый взгляд представлен
        кортежем (P, Q), где P - вектор активов, Q - ожидаемая доходность.
        Формат: [(P1, Q1), (P2, Q2), ...]
        Пример: [([1, 0, 0, 0], 0.12), ([0, 1, -1, 0], 0.05)]
        - Первый взгляд: актив 1 будет иметь доходность 12%
        - Второй взгляд: актив 2 будет на 5% лучше актива 3
        Если None, используется только рыночная модель.
        
    view_confidences : array-like, optional, default=None
        Уверенность в каждом взгляде. Должен быть одномерный массив
        с тем же количеством элементов, что и views. Значения должны быть
        положительными (чем больше, тем выше уверенность):
        - 0.1: Низкая уверенность (слабый взгляд)
        - 0.5: Средняя уверенность
        - 1.0: Высокая уверенность (сильный взгляд)
        Если None, используется значение 0.1 для всех взглядов.
        
    Returns:
    --------
    tuple
        (weights, expected_returns, portfolio_cov)
        
        weights : array-like, shape (n_assets,)
            Оптимальные веса активов в портфолио. Сумма весов равна 1.0.
            
        expected_returns : array-like, shape (n_assets,)
            Ожидаемые доходности активов с учетом взглядов инвестора.
            
        portfolio_cov : array-like, shape (n_assets, n_assets)
            Ковариационная матрица портфолио с учетом взглядов.
            
    Raises:
    -------
    ValueError
        Если размеры входных данных не совпадают или оптимизация не удалась
        
    Notes:
    ------
    Модель Black-Litterman решает проблему нестабильности классической
    оптимизации Markowitz путем:
    1. Использования рыночных весов как отправной точки
    2. Включения субъективных взглядов инвестора
    3. Балансирования между рыночными данными и взглядами
    
    Формула ожидаемых доходностей:
    E[R] = [(τΣ)^(-1) + P^T * Ω^(-1) * P]^(-1) * [(τΣ)^(-1) * Π + P^T * Ω^(-1) * Q]
    где τ - масштабирующий параметр, Ω - матрица уверенности во взглядах
    """
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
    """
    Оптимизация портфолио с равным вкладом в риск (Risk Parity)
    
    Risk Parity - это метод оптимизации портфолио, при котором каждый актив
    вносит равный вклад в общий риск портфолио. Это приводит к более
    сбалансированному распределению риска между активами.
    
    Parameters:
    -----------
    cov_matrix : array-like, shape (n_assets, n_assets)
        Ковариационная матрица активов. Должна быть квадратной матрицей
        размером n_assets x n_assets, где элемент (i,j) представляет
        ковариацию между активами i и j. Матрица должна быть симметричной
        и положительно определенной.
        
    target_risk : float, optional, default=None
        Целевой уровень риска портфолио. Если указан, портфолио будет
        оптимизировано для достижения этого уровня риска при равном
        распределении вклада в риск между активами.
        - None: Оптимизация без ограничения на общий риск
        - 0.10: Целевой риск 10% (стандартное отклонение)
        - 0.15: Целевой риск 15%
        - 0.20: Целевой риск 20%
        
    Returns:
    --------
    array-like, shape (n_assets,)
        Оптимальные веса активов в портфолио. Сумма весов равна 1.0.
        Каждый актив вносит равный вклад в общий риск портфолио.
        
    Raises:
    -------
    ValueError
        Если оптимизация не удалась или ковариационная матрица некорректна
        
    Notes:
    ------
    Risk Parity решает задачу:
    min Σᵢ Σⱼ (wᵢ * σᵢ - wⱼ * σⱼ)²
    subject to: Σᵢ wᵢ = 1, wᵢ ≥ 0
    
    где wᵢ - вес актива i, σᵢ - волатильность актива i
    
    Преимущества Risk Parity:
    1. Более стабильные веса по сравнению с Markowitz
    2. Лучшая диверсификация риска
    3. Меньшая чувствительность к ошибкам в оценке параметров
    4. Более интуитивное распределение риска
    
    Недостатки:
    1. Может не максимизировать доходность
    2. Может быть неоптимальным для инвесторов с разными предпочтениями
    """
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
    """
    Оптимизация портфолио с минимальной дисперсией (Minimum Variance Portfolio)
    
    Minimum Variance Portfolio - это портфолио с наименьшей возможной
    дисперсией (риском) среди всех возможных портфолио. Это консервативный
    подход, который минимизирует волатильность портфолио.
    
    Parameters:
    -----------
    cov_matrix : array-like, shape (n_assets, n_assets)
        Ковариационная матрица активов. Должна быть квадратной матрицей
        размером n_assets x n_assets, где элемент (i,j) представляет
        ковариацию между активами i и j. Матрица должна быть симметричной
        и положительно определенной.
        
    Returns:
    --------
    array-like, shape (n_assets,)
        Оптимальные веса активов в портфолио с минимальной дисперсией.
        Сумма весов равна 1.0.
        
    Raises:
    -------
    ValueError
        Если оптимизация не удалась или ковариационная матрица некорректна
        
    Notes:
    ------
    Minimum Variance Portfolio решает задачу:
    min w^T * Σ * w
    subject to: Σᵢ wᵢ = 1, wᵢ ≥ 0
    
    где w - веса активов, Σ - ковариационная матрица
    
    Аналитическое решение:
    w* = (Σ^(-1) * 1) / (1^T * Σ^(-1) * 1)
    
    где 1 - вектор из единиц
    
    Преимущества:
    1. Минимальный риск среди всех возможных портфолио
    2. Простота расчета и интерпретации
    3. Стабильность весов
    4. Подходит для консервативных инвесторов
    
    Недостатки:
    1. Может иметь низкую доходность
    2. Не учитывает ожидаемые доходности
    3. Может быть неоптимальным для инвесторов с другими предпочтениями
    4. Чувствительность к ошибкам в оценке ковариационной матрицы
    """
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
    """
    Оптимизация портфолио с максимальным коэффициентом Шарпа
    
    Maximum Sharpe Portfolio - это портфолио, которое максимизирует
    коэффициент Шарпа (отношение избыточной доходности к риску).
    Это оптимальный портфолио для инвесторов, которые хотят максимизировать
    доходность на единицу риска.
    
    Parameters:
    -----------
    expected_returns : array-like, shape (n_assets,)
        Ожидаемые доходности активов. Должен быть одномерный массив или список
        с ожидаемыми доходностями для каждого актива в портфолио.
        Пример: [0.08, 0.12, 0.06, 0.10] для 4 активов
        
    cov_matrix : array-like, shape (n_assets, n_assets)
        Ковариационная матрица активов. Должна быть квадратной матрицей
        размером n_assets x n_assets, где элемент (i,j) представляет
        ковариацию между активами i и j. Матрица должна быть симметричной
        и положительно определенной.
        
    risk_free_rate : float, default=0.02
        Безрисковая процентная ставка. Используется для расчета избыточной
        доходности в коэффициенте Шарпа. Обычно принимает значения:
        - 0.01: 1% (очень низкая ставка)
        - 0.02: 2% (стандартное значение для развитых рынков)
        - 0.03: 3% (умеренная ставка)
        - 0.05: 5% (высокая ставка)
        
    Returns:
    --------
    array-like, shape (n_assets,)
        Оптимальные веса активов в портфолио с максимальным коэффициентом Шарпа.
        Сумма весов равна 1.0.
        
    Raises:
    -------
    ValueError
        Если оптимизация не удалась или входные данные некорректны
        
    Notes:
    ------
    Maximum Sharpe Portfolio решает задачу:
    max (w^T * μ - r_f) / √(w^T * Σ * w)
    subject to: Σᵢ wᵢ = 1, wᵢ ≥ 0
    
    где w - веса активов, μ - ожидаемые доходности, Σ - ковариационная матрица,
    r_f - безрисковая ставка
    
    Коэффициент Шарпа:
    Sharpe = (E[R_p] - r_f) / σ_p
    
    где E[R_p] - ожидаемая доходность портфолио, σ_p - волатильность портфолио
    
    Преимущества:
    1. Максимизирует доходность на единицу риска
    2. Учитывает как доходность, так и риск
    3. Широко используется в практике
    4. Интуитивно понятный показатель
    
    Недостатки:
    1. Чувствительность к ошибкам в оценке параметров
    2. Предполагает нормальное распределение доходностей
    3. Не учитывает асимметрию и эксцесс распределения
    4. Может быть нестабильным при изменении параметров
    """
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

### 🤖 Интеграция машинного обучения в управление портфолио

```mermaid
graph TD
    A[ML в управлении портфолио] --> B[Предсказание доходностей]
    A --> C[Кластеризация активов]
    A --> D[Оптимизация портфолио]
    A --> E[Управление рисками]
    A --> F[Динамическая ребалансировка]
    
    B --> B1[Time Series Models<br/>LSTM, GRU, Transformer]
    B --> B2[Ensemble Methods<br/>Random Forest, XGBoost]
    B --> B3[Deep Learning<br/>Neural Networks, CNN]
    B --> B4[Feature Engineering<br/>Technical indicators, Sentiment]
    
    C --> C1[K-means Clustering<br/>Group similar assets]
    C --> C2[Hierarchical Clustering<br/>Dendrogram-based grouping]
    C --> C3[DBSCAN<br/>Density-based clustering]
    C --> C4[Gaussian Mixture<br/>Probabilistic clustering]
    
    D --> D1[Reinforcement Learning<br/>Q-learning, Policy Gradient]
    D --> D2[Genetic Algorithms<br/>Evolutionary optimization]
    D --> D3[Bayesian Optimization<br/>Gaussian Process optimization]
    D --> D4[Multi-objective Optimization<br/>Pareto frontier]
    
    E --> E1[VaR Prediction<br/>ML-based VaR estimation]
    E --> E2[Stress Testing<br/>Scenario generation with ML]
    E --> E3[Anomaly Detection<br/>Outlier detection in returns]
    E --> E4[Regime Detection<br/>Market regime classification]
    
    F --> F1[Signal Generation<br/>ML-based trading signals]
    F --> F2[Threshold Optimization<br/>Dynamic rebalancing thresholds]
    F --> F3[Transaction Cost Modeling<br/>Cost-aware rebalancing]
    F --> F4[Market Microstructure<br/>Order book analysis]
    
    B1 --> G[ML Pipeline]
    B2 --> G
    B3 --> G
    B4 --> G
    C1 --> G
    C2 --> G
    C3 --> G
    C4 --> G
    D1 --> G
    D2 --> G
    D3 --> G
    D4 --> G
    E1 --> G
    E2 --> G
    E3 --> G
    E4 --> G
    F1 --> G
    F2 --> G
    F3 --> G
    F4 --> G
    
    G --> H[Обучение моделей<br/>Train on historical data]
    H --> I[Валидация<br/>Cross-validation, Walk-forward]
    I --> J[Деплой в продакшен<br/>Real-time predictions]
    J --> K[Мониторинг производительности<br/>Model performance tracking]
    
    K --> L{Модель эффективна?}
    L -->|Да| M[✅ Продолжить использование]
    L -->|Нет| N[❌ Переобучить модель]
    
    N --> O[Анализ деградации<br/>Identify performance decline]
    O --> P[Обновление данных<br/>Include new market data]
    P --> Q[Переобучение<br/>Retrain with updated data]
    Q --> R[Валидация обновленной модели<br/>Test on out-of-sample data]
    R --> S[Деплой обновленной модели<br/>Replace old model]
    S --> K
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#ffcdd2
    style F fill:#e1f5fe
    style M fill:#4caf50
    style N fill:#ff9800
```

**Clustering-based Portfolio:**

```python
def clustering_portfolio_optimization(returns, n_clusters=5, method='kmeans'):
    """
    Оптимизация портфолио на основе кластеризации активов
    
    Этот метод группирует активы в кластеры на основе их доходностей,
    а затем создает оптимизированные портфолио для каждого кластера.
    Это позволяет лучше диверсифицировать портфолио и учитывать
    сходство между активами.
    
    Parameters:
    -----------
    returns : pandas.DataFrame, shape (n_periods, n_assets)
        Матрица доходностей активов. Строки представляют временные периоды,
        столбцы - активы. Данные должны быть в формате pandas DataFrame
        с индексами дат и названиями активов в столбцах.
        Пример: DataFrame с индексами дат и столбцами ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
        
    n_clusters : int, default=5
        Количество кластеров для группировки активов. Рекомендуемые значения:
        - 3-5: Для небольшого портфолио (10-20 активов)
        - 5-8: Для среднего портфолио (20-50 активов)
        - 8-12: Для большого портфолио (50+ активов)
        - Слишком мало кластеров: может не учесть различия между активами
        - Слишком много кластеров: может привести к переобучению
        
    method : str, default='kmeans'
        Метод кластеризации для группировки активов. Доступные варианты:
        - 'kmeans': K-means кластеризация (быстрая, подходит для сферических кластеров)
        - 'hierarchical': Иерархическая кластеризация (медленная, подходит для кластеров любой формы)
        
    Returns:
    --------
    dict
        Словарь с информацией о кластерах и их весах. Ключи - ID кластера,
        значения - словари с ключами:
        - 'weights': array-like, shape (n_assets_in_cluster,)
            Оптимальные веса активов в кластере
        - 'assets': list
            Список названий активов в кластере
            
    Raises:
    -------
    ValueError
        Если метод кластеризации неизвестен или данные некорректны
        
    Notes:
    ------
    Алгоритм работы:
    1. Нормализация данных доходностей
    2. Кластеризация активов по доходностям
    3. Для каждого кластера:
       - Расчет ковариационной матрицы
       - Оптимизация весов (минимальная дисперсия)
       - Нормализация весов
    4. Возврат весов для каждого кластера
    
    Преимущества:
    1. Учитывает сходство между активами
    2. Лучшая диверсификация
    3. Снижение корреляций внутри кластеров
    4. Более стабильные веса
    
    Недостатки:
    1. Зависимость от выбора количества кластеров
    2. Чувствительность к выбросам
    3. Может не работать для малого количества активов
    """
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
    """
    Оптимизация портфолио с использованием машинного обучения
    
    Этот метод использует ML-модели для предсказания доходностей активов,
    а затем создает множество портфолио и выбирает лучший по коэффициенту Шарпа.
    Это позволяет учитывать сложные нелинейные зависимости в данных.
    
    Parameters:
    -----------
    returns : pandas.DataFrame, shape (n_periods, n_assets)
        Матрица доходностей активов. Строки представляют временные периоды,
        столбцы - активы. Данные должны быть в формате pandas DataFrame
        с индексами дат и названиями активов в столбцах.
        Пример: DataFrame с индексами дат и столбцами ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
        
    features : pandas.DataFrame, shape (n_periods, n_features)
        Матрица признаков для ML-модели. Строки представляют временные периоды,
        столбцы - признаки. Может включать технические индикаторы,
        макроэкономические данные, новостные данные и т.д.
        Пример: DataFrame с признаками ['RSI', 'MACD', 'Volume', 'GDP_growth']
        
    model : sklearn-compatible model
        Обученная ML-модель для предсказания доходностей. Должна иметь методы
        fit() и predict(). Рекомендуемые модели:
        - RandomForestRegressor: Хорошо работает с нелинейными зависимостями
        - XGBRegressor: Высокая производительность, устойчивость к переобучению
        - LinearRegression: Простая и быстрая модель
        - LSTM/GRU: Для временных рядов (требует специальной подготовки данных)
        
    n_portfolios : int, default=1000
        Количество портфолио для генерации и оценки. Рекомендуемые значения:
        - 100-500: Быстрый анализ, низкая точность
        - 1000: Стандартное значение, хороший баланс скорости и точности
        - 5000-10000: Высокая точность, медленный анализ
        - Больше портфолио: лучше покрытие пространства решений
        
    Returns:
    --------
    tuple
        (best_portfolio, all_portfolios)
        
        best_portfolio : dict
            Лучший портфолио по коэффициенту Шарпа с ключами:
            - 'weights': array-like, shape (n_assets,)
                Оптимальные веса активов
            - 'return': float
                Ожидаемая доходность портфолио
            - 'variance': float
                Дисперсия портфолио
            - 'sharpe': float
                Коэффициент Шарпа портфолио
                
        all_portfolios : list
            Список всех сгенерированных портфолио с теми же ключами,
            что и best_portfolio
            
    Raises:
    -------
    ValueError
        Если размеры данных не совпадают или модель некорректна
        
    Notes:
    ------
    Алгоритм работы:
    1. Разделение данных на train/test (80/20)
    2. Обучение ML-модели на исторических данных
    3. Предсказание доходностей на тестовых данных
    4. Генерация n_portfolios случайных весов
    5. Расчет метрик для каждого портфолио
    6. Выбор портфолио с максимальным коэффициентом Шарпа
    
    Преимущества:
    1. Учитывает сложные нелинейные зависимости
    2. Использует множество признаков
    3. Адаптируется к изменяющимся условиям рынка
    4. Может учитывать качественные факторы
    
    Недостатки:
    1. Требует качественных данных и признаков
    2. Может переобучаться на исторических данных
    3. Сложность интерпретации результатов
    4. Зависимость от выбора модели и параметров
    """
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

### 🌐 Стратегии диверсификации портфолио

```mermaid
graph TD
    A[Стратегии диверсификации] --> B[Классическая диверсификация]
    A --> C[Продвинутые методы]
    A --> D[Факторная диверсификация]
    
    B --> B1[Географическая диверсификация<br/>Разные страны и регионы]
    B --> B2[Секторальная диверсификация<br/>Различные отрасли экономики]
    B --> B3[Временная диверсификация<br/>Dollar-cost averaging]
    B --> B4[Классовая диверсификация<br/>Stocks, Bonds, REITs, Commodities]
    
    C --> C1[Корреляционная диверсификация<br/>Низкие корреляции между активами]
    C --> C2[Факторная диверсификация<br/>Различные факторы риска]
    C --> C3[Стилевая диверсификация<br/>Value, Growth, Momentum, Quality]
    C --> C4[Размерная диверсификация<br/>Large, Mid, Small cap]
    
    D --> D1[Fama-French факторы<br/>Market, Size, Value]
    D --> D2[Макроэкономические факторы<br/>Interest rates, Inflation, GDP]
    D --> D3[Технические факторы<br/>Momentum, Volatility, Liquidity]
    D --> D4[Фундаментальные факторы<br/>P/E, P/B, ROE, Debt/Equity]
    
    B1 --> E[Ограничения по странам<br/>max_weight_per_country ≤ 30%]
    B2 --> F[Ограничения по секторам<br/>max_weight_per_sector ≤ 25%]
    C1 --> G[Максимальная корреляция<br/>max_correlation ≤ 0.7]
    C2 --> H[Максимальная экспозиция к фактору<br/>max_factor_exposure ≤ 0.5]
    
    E --> I[Оптимизация весов]
    F --> I
    G --> I
    H --> I
    
    I --> J[Диверсифицированный портфолио]
    J --> K[Снижение рисков<br/>Lower portfolio volatility]
    J --> L[Улучшение Sharpe ratio<br/>Better risk-adjusted returns]
    J --> M[Устойчивость к шокам<br/>Resilience to market shocks]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style J fill:#4caf50
```

### 1. Классическая диверсификация

**Географическая диверсификация:**

```python
def geographic_diversification(returns_by_country, max_weight_per_country=0.3):
    """
    Географическая диверсификация портфолио
    
    Этот метод оптимизирует портфолио с учетом географического распределения
    активов, ограничивая максимальный вес на каждую страну. Это помогает
    снизить страновые риски и улучшить диверсификацию.
    
    Parameters:
    -----------
    returns_by_country : dict
        Словарь с доходностями по странам. Ключи - названия стран,
        значения - pandas.Series с доходностями активов в этой стране.
        Формат: {'USA': returns_usa, 'EU': returns_eu, 'Asia': returns_asia}
        где returns_usa - Series с доходностями американских активов
        
    max_weight_per_country : float, default=0.3
        Максимальный вес на одну страну в портфолио. Рекомендуемые значения:
        - 0.2: Высокая диверсификация (максимум 20% на страну)
        - 0.3: Стандартная диверсификация (максимум 30% на страну)
        - 0.4: Умеренная диверсификация (максимум 40% на страну)
        - 0.5: Низкая диверсификация (максимум 50% на страну)
        - Значение должно быть в диапазоне (0, 1]
        
    Returns:
    --------
    array-like, shape (n_countries,)
        Оптимальные веса стран в портфолио. Сумма весов равна 1.0.
        Каждый элемент представляет долю капитала, инвестированного
        в активы соответствующей страны.
        
    Raises:
    -------
    ValueError
        Если оптимизация не удалась или параметры некорректны
        
    Notes:
    ------
    Алгоритм работы:
    1. Расчет ожидаемых доходностей по странам
    2. Расчет ковариационной матрицы между странами
    3. Оптимизация с ограничениями на максимальный вес на страну
    4. Возврат оптимальных весов стран
    
    Преимущества:
    1. Снижение страновых рисков
    2. Улучшение диверсификации
    3. Учет региональных особенностей
    4. Защита от локальных кризисов
    
    Недостатки:
    1. Может ограничивать доходность
    2. Не учитывает корреляции между странами
    3. Требует качественных данных по странам
    4. Может быть неоптимальным для глобальных активов
    """
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

### ⚠️ Метрики управления рисками портфолио

```mermaid
graph TD
    A[Метрики управления рисками] --> B[Value at Risk - VaR]
    A --> C[Expected Shortfall - ES]
    A --> D[Максимальная просадка]
    A --> E[Дополнительные метрики]
    
    B --> B1[Historical VaR<br/>Percentile-based approach]
    B --> B2[Parametric VaR<br/>Normal distribution assumption]
    B --> B3[Monte Carlo VaR<br/>Simulation-based approach]
    B --> B4[Уровни доверия<br/>90%, 95%, 99%]
    
    C --> C1[Conditional VaR<br/>Average loss beyond VaR]
    C --> C2[Tail Risk<br/>Extreme loss scenarios]
    C --> C3[Coherent Risk Measure<br/>Subadditivity property]
    C --> C4[Regulatory Capital<br/>Basel III requirements]
    
    D --> D1[Peak-to-Trough<br/>Maximum decline from peak]
    D --> D2[Duration of Drawdown<br/>Time to recovery]
    D --> D3[Drawdown Frequency<br/>Number of drawdown periods]
    D --> D4[Underwater Curve<br/>Cumulative drawdown path]
    
    E --> E1[Volatility<br/>Standard deviation of returns]
    E --> E2[Beta<br/>Market sensitivity]
    E --> E3[Tracking Error<br/>Deviation from benchmark]
    E --> E4[Information Ratio<br/>Excess return per unit of tracking error]
    E --> E5[Sortino Ratio<br/>Downside deviation adjustment]
    E --> E6[Calmar Ratio<br/>Return to max drawdown ratio]
    
    B1 --> F[Расчет рисков]
    B2 --> F
    B3 --> F
    C1 --> F
    D1 --> F
    E1 --> F
    
    F --> G[Оценка рисков портфолио]
    G --> H[VaR 95%: -2.5%<br/>ES 95%: -3.8%<br/>Max DD: -15.2%]
    
    H --> I[Управление рисками]
    I --> J[Позиционирование<br/>Position sizing based on VaR]
    I --> K[Хеджирование<br/>Derivatives for risk reduction]
    I --> L[Диверсификация<br/>Correlation-based allocation]
    I --> M[Стоп-лоссы<br/>Automatic risk controls]
    
    style A fill:#e3f2fd
    style B fill:#ffcdd2
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#c8e6c9
    style I fill:#4caf50
```

### 1. Value at Risk (VaR)

**Historical VaR:**

```python
def historical_var(returns, confidence_level=0.95):
    """
    Расчет исторического Value at Risk (VaR)
    
    Historical VaR - это метод расчета VaR, основанный на исторических
    данных доходностей. Он не делает предположений о распределении
    доходностей и использует эмпирические квантили.
    
    Parameters:
    -----------
    returns : array-like, shape (n_periods,)
        Массив доходностей портфолио или актива. Может быть pandas.Series
        или numpy.array. Данные должны быть в формате доходностей
        (например, 0.05 для 5% доходности).
        
    confidence_level : float, default=0.95
        Уровень доверия для расчета VaR. Определяет, какой процент
        наихудших сценариев исключается из анализа. Рекомендуемые значения:
        - 0.90: 90% уровень доверия (исключается 10% наихудших сценариев)
        - 0.95: 95% уровень доверия (стандартное значение)
        - 0.99: 99% уровень доверия (исключается 1% наихудших сценариев)
        - 0.999: 99.9% уровень доверия (исключается 0.1% наихудших сценариев)
        - Значение должно быть в диапазоне (0, 1)
        
    Returns:
    --------
    float
        Value at Risk на заданном уровне доверия. Отрицательное значение,
        представляющее максимальный ожидаемый убыток с заданной вероятностью.
        Например, если VaR = -0.05, то с вероятностью confidence_level
        убыток не превысит 5%.
        
    Raises:
    -------
    ValueError
        Если confidence_level не в диапазоне (0, 1) или данные пусты
        
    Notes:
    ------
    Формула расчета:
    VaR = percentile(returns, (1 - confidence_level) * 100)
    
    где percentile - эмпирический квантиль
    
    Преимущества:
    1. Не требует предположений о распределении
    2. Учитывает реальные исторические данные
    3. Простота расчета и интерпретации
    4. Устойчивость к выбросам
    
    Недостатки:
    1. Зависимость от исторических данных
    2. Не учитывает изменения волатильности
    3. Может быть неточным для редких событий
    4. Требует достаточно длинной истории данных
    """
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

### 🔄 Динамическое управление портфолио

```mermaid
graph TD
    A[Динамическое управление портфолио] --> B[Ребалансировка]
    A --> C[Адаптивное управление]
    A --> D[Мониторинг и контроль]
    
    B --> B1[Временная ребалансировка<br/>Fixed schedule: Daily, Weekly, Monthly]
    B --> B2[Пороговая ребалансировка<br/>When deviation > threshold]
    B --> B3[Стоимость ребалансировки<br/>Transaction costs consideration]
    B --> B4[Оптимальная частота<br/>Balance between cost and benefit]
    
    C --> C1[Volatility-based Rebalancing<br/>Adjust based on market volatility]
    C --> C2[Momentum-based Rebalancing<br/>Follow market momentum]
    C --> C3[Regime-based Rebalancing<br/>Different strategies per market regime]
    C --> C4[ML-based Rebalancing<br/>Machine learning predictions]
    
    D --> D1[Real-time Monitoring<br/>Continuous portfolio tracking]
    D --> D2[Risk Alerts<br/>VaR, ES, Drawdown warnings]
    D --> D3[Performance Tracking<br/>Sharpe, Return, Volatility]
    D --> D4[Compliance Monitoring<br/>Regulatory constraints]
    
    B1 --> E[Ребалансировочные стратегии]
    B2 --> E
    C1 --> F[Адаптивные стратегии]
    C2 --> F
    C3 --> F
    C4 --> F
    D1 --> G[Контрольные системы]
    D2 --> G
    D3 --> G
    D4 --> G
    
    E --> H[Оптимизация портфолио]
    F --> H
    G --> H
    
    H --> I[Динамические веса<br/>w_t = f(market_conditions_t)]
    I --> J[Оценка эффективности<br/>Performance vs Static portfolio]
    
    J --> K{Улучшение производительности?}
    K -->|Да| L[✅ Продолжить динамическое управление]
    K -->|Нет| M[❌ Пересмотреть стратегию]
    
    M --> N[Анализ причин<br/>Why dynamic management failed?]
    N --> O[Корректировка параметров<br/>Adjust thresholds, frequencies]
    O --> P[Повторное тестирование<br/>Backtest updated strategy]
    P --> H
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style L fill:#4caf50
    style M fill:#ff9800
```

### 1. Ребалансировка

**Временная ребалансировка:**

```python
def time_based_rebalancing(returns, target_weights, rebalance_freq='M'):
    """
    Ребалансировка портфолио по времени
    
    Этот метод выполняет ребалансировку портфолио через заданные
    временные интервалы, возвращая веса к целевым значениям.
    Это помогает поддерживать желаемое распределение активов.
    
    Parameters:
    -----------
    returns : pandas.DataFrame, shape (n_periods, n_assets)
        Матрица доходностей активов. Строки представляют временные периоды,
        столбцы - активы. Данные должны быть в формате pandas DataFrame
        с индексами дат и названиями активов в столбцах.
        
    target_weights : array-like, shape (n_assets,)
        Целевые веса активов в портфолио. Должен быть одномерный массив
        или список с весами для каждого актива. Сумма весов должна быть 1.0.
        Пример: [0.4, 0.3, 0.2, 0.1] для 4 активов
        
    rebalance_freq : str, default='M'
        Частота ребалансировки портфолио. Доступные варианты:
        - 'D': Ежедневная ребалансировка (каждый день)
        - 'W': Еженедельная ребалансировка (каждые 7 дней)
        - 'M': Ежемесячная ребалансировка (каждые 30 дней)
        - 'Q': Квартальная ребалансировка (каждые 90 дней)
        - 'Y': Годовая ребалансировка (каждые 365 дней)
        
    Returns:
    --------
    pandas.Series, shape (n_periods,)
        Временной ряд доходностей ребалансированного портфолио.
        Индекс соответствует индексу входных данных returns.
        
    Raises:
    -------
    ValueError
        Если частота ребалансировки неизвестна или данные некорректны
        
    Notes:
    ------
    Алгоритм работы:
    1. Определение дат ребалансировки на основе частоты
    2. Для каждого периода:
       - Если дата ребалансировки: установка весов = target_weights
       - Иначе: использование текущих весов
       - Расчет доходности портфолио
    3. Возврат временного ряда доходностей
    
    Преимущества:
    1. Простота реализации и понимания
    2. Предсказуемость ребалансировки
    3. Контроль транзакционных издержек
    4. Подходит для долгосрочных стратегий
    
    Недостатки:
    1. Может не учитывать рыночные условия
    2. Фиксированная частота может быть неоптимальной
    3. Не адаптируется к изменениям волатильности
    4. Может приводить к избыточной торговле
    """
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

### 📊 Мониторинг и оценка портфолио

```mermaid
graph TD
    A[Мониторинг и оценка портфолио] --> B[Метрики производительности]
    A --> C[Анализ рисков]
    A --> D[Визуализация]
    A --> E[Отчетность]
    
    B --> B1[Доходность<br/>Total Return, Annual Return]
    B --> B2[Риск-скорректированная доходность<br/>Sharpe Ratio, Sortino Ratio]
    B --> B3[Просадки<br/>Max Drawdown, Drawdown Duration]
    B --> B4[Стабильность<br/>Volatility, Coefficient of Variation]
    B --> B5[Эффективность<br/>Calmar Ratio, Information Ratio]
    
    C --> C1[Value at Risk<br/>VaR 90%, 95%, 99%]
    C --> C2[Expected Shortfall<br/>Conditional VaR]
    C --> C3[Корреляционный анализ<br/>Asset correlations, Factor exposures]
    C --> C4[Стресс-тестирование<br/>Scenario analysis, Monte Carlo]
    C --> C5[Регуляторные риски<br/>Basel III, Solvency II]
    
    D --> D1[Кумулятивная доходность<br/>Cumulative return chart]
    D --> D2[Распределение доходностей<br/>Return distribution histogram]
    D --> D3[Просадки<br/>Drawdown chart]
    D --> D4[Скользящие метрики<br/>Rolling Sharpe, Volatility]
    D --> D5[Сравнение с бенчмарком<br/>Portfolio vs Benchmark]
    D --> D6[Анализ вклада активов<br/>Asset contribution analysis]
    
    E --> E1[Ежедневные отчеты<br/>Daily performance summary]
    E --> E2[Еженедельные отчеты<br/>Weekly risk and return analysis]
    E --> E3[Ежемесячные отчеты<br/>Monthly portfolio review]
    E --> E4[Квартальные отчеты<br/>Quarterly attribution analysis]
    E --> E5[Алерты и уведомления<br/>Risk alerts, Performance alerts]
    
    B1 --> F[Расчет метрик]
    B2 --> F
    B3 --> F
    B4 --> F
    B5 --> F
    C1 --> F
    C2 --> F
    C3 --> F
    C4 --> F
    C5 --> F
    
    F --> G[Анализ производительности]
    G --> H[Сравнение с целями<br/>Performance vs Target]
    G --> I[Сравнение с бенчмарком<br/>Performance vs Benchmark]
    G --> J[Анализ трендов<br/>Performance trends over time]
    
    H --> K[Оценка портфолио]
    I --> K
    J --> K
    
    K --> L{Портфолио эффективен?}
    L -->|Да| M[✅ Продолжить текущую стратегию]
    L -->|Нет| N[❌ Требует корректировки]
    
    N --> O[Анализ проблем<br/>Identify underperformance causes]
    O --> P[Корректировка стратегии<br/>Adjust allocation, rebalance]
    P --> Q[Мониторинг изменений<br/>Track improvement]
    Q --> K
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#ffcdd2
    style D fill:#fff3e0
    style E fill:#f3e5f5
    style M fill:#4caf50
    style N fill:#ff9800
```

### 1. Метрики производительности

```python
def calculate_portfolio_metrics(returns, risk_free_rate=0.02):
    """
    Расчет метрик производительности портфолио
    
    Эта функция рассчитывает комплексный набор метрик для оценки
    производительности портфолио, включая доходность, риск и
    риск-скорректированные показатели.
    
    Parameters:
    -----------
    returns : pandas.Series or array-like, shape (n_periods,)
        Временной ряд доходностей портфолио. Может быть pandas.Series
        с индексами дат или numpy.array. Данные должны быть в формате
        доходностей (например, 0.05 для 5% доходности).
        
    risk_free_rate : float, default=0.02
        Безрисковая процентная ставка для расчета риск-скорректированных
        метрик. Обычно принимает значения:
        - 0.01: 1% (очень низкая ставка)
        - 0.02: 2% (стандартное значение для развитых рынков)
        - 0.03: 3% (умеренная ставка)
        - 0.05: 5% (высокая ставка)
        
    Returns:
    --------
    dict
        Словарь с метриками производительности портфолио:
        
        total_return : float
            Общая доходность за весь период. Рассчитывается как
            (1 + returns).prod() - 1
            
        annual_return : float
            Годовая доходность. Рассчитывается как
            (1 + returns).mean() ** 252 - 1 (предполагается 252 торговых дня)
            
        volatility : float
            Годовая волатильность (стандартное отклонение доходностей).
            Рассчитывается как returns.std() * sqrt(252)
            
        sharpe : float
            Коэффициент Шарпа - отношение избыточной доходности к риску.
            Рассчитывается как (annual_return - risk_free_rate) / volatility
            
        max_drawdown : float
            Максимальная просадка - наибольшее падение от пика до минимума.
            Отрицательное значение, где -0.15 означает просадку 15%
            
        sortino : float
            Коэффициент Сортино - отношение избыточной доходности к
            downside-риску. Учитывает только отрицательные доходности.
            
        calmar : float
            Коэффициент Кальмара - отношение годовой доходности к
            максимальной просадке. Показывает доходность на единицу риска.
            
    Raises:
    -------
    ValueError
        Если данные пусты или некорректны
        
    Notes:
    ------
    Формулы расчета:
    - Total Return: (1 + r₁) * (1 + r₂) * ... * (1 + rₙ) - 1
    - Annual Return: (1 + mean(r))^252 - 1
    - Volatility: std(r) * sqrt(252)
    - Sharpe: (Annual Return - Risk Free Rate) / Volatility
    - Max Drawdown: min((cumprod(1 + r) / cummax(cumprod(1 + r))) - 1)
    - Sortino: (Annual Return - Risk Free Rate) / Downside Volatility
    - Calmar: Annual Return / |Max Drawdown|
    
    Интерпретация метрик:
    - Sharpe > 1.0: Хорошая производительность
    - Sortino > 1.5: Отличная производительность
    - Calmar > 1.0: Хорошая производительность
    - Max Drawdown < -0.20: Высокий риск
    """
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

### Ключевые принципы

1. **Диверсификация** - не кладите все яйца в одну корзину
2. **Управление рисками** - контролируйте VaR и максимальную просадку
3. **Ребалансировка** - регулярно корректируйте веса
4. **Мониторинг** - постоянно отслеживайте производительность
5. **Адаптивность** - приспосабливайтесь к изменяющимся условиям

### Следующие шаги

После освоения управления портфолио вы готовы к созданию полноценных торговых систем, которые объединяют:

- [Feature Generation](./26_feature_generation_advanced.md)
- [Бэктестинг](./27_backtesting_methods.md)
- [Walk-forward анализ](./28_walk_forward_analysis.md)
- [Monte Carlo симуляции](./29_monte_carlo_simulations.md)
- Управление портфолио (текущая глава)
