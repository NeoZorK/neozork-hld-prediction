# In-depth describe methodologies for the creation and management of Portfolio, successful methods of diversification

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Who Management Portfolio is the basis for successful investment

### # The need to manage Portfolio for successful investment

```mermaid
graph TD
A[Investor] -- > B {Right Management Portfolio?}

B--~ ~ No ~ C[90 per cent of investors lose money]
C --> D[\\\\\\risk_br/> Concentration in one asset]
C --> E[> Instability<br/> Resilient fluctuations in value]
C --> F[________________ significant losses<br/> During crises]
C -> G[~ Failure to achieve objectives<br/> Disappointing in investment]

B -->\\\\H[10% successful investors]
H -> I[the stability<br/> Reducing volatility and risks]
H -> J[ ] Optimization of return <br/> At specified risk level]
H --> K[~ Robacity<br/> Resistance to market shocks]
H --> L[>Size <br/>Management with large capital]

I-> M [Divergization of assets]
J -> N [Optimization of Weights]
K --> O[Management risk]
L -> P [professional approach]

M --> Q [Successful Portfolio]
 N --> Q
 O --> Q
 P --> Q

Q -> R[~ Stablely profitable investments]

 style A fill:#e3f2fd
 style H fill:#c8e6c9
 style C fill:#ffcdd2
 style R fill:#4caf50
```

**Why 90 percent of investors lose money?** Because they don't understand the principles of Portfolio governance.

### What gives the right Management Portfolio?

- **Stability**: Reducing volatility and risks
- ** Income**: Optimization of return at specified risk level
- **Platitude**: Resistance to market shocks
- **Stability**: Potential to manage large capital

### What's going on without the right control of Portfolio?

- ** High risks**: Concentration in one asset or sector
- ** Instability**: severe fluctuations in the cost of Portfolio
- ** Loss**: Significant losses during crises
- ** Disappointing**: Failure to achieve investment objectives

## Portfolio's control theory

### Mathematical principles

**Porthfolio Optimization as Optimization:**

```math
max w^T μ - λ/2 * w^T Σ w
subject to: w^T 1 = 1, w ≥ 0
```

Where:

- `w' is the weight of assets in Portfolio
- ```' is the expected return on assets
- ``` - the asset matrix
&lt; &gt; = risk factor

** Portfolio quality criteria: **

1. ** Income**: E[R_p] = w\T μ
2. **Rsc**: Var[R_p] = w\T \w
3. ** Sharp coefficient**: (E[R_p] - r_f) / GVar[R_p]
4. **VaR**: P(R_p ≤ VaR) = α

### Portfolio types

### ♪ Portfolio type comparison

```mermaid
graph TB
A[Porthfolio Type] -> B [Conservative Portfolio]
A -> C [A balanced Portfolio]
A -> D [Aggressive Portfolio]
A -> E [Diversified Portfolio]

B --> B1[Low risk, low return<br/>Risk: 5-10%, Return: 3-6%]
B --> B2 [Librations, deposits<br/>Government banks, CDs]
B -> B3[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\(\\\\\\ \\\\\\\\\\\\\\\\\\\\\\\\\\B3\\\\\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\/ }F}Penishers, rookie]
B -> B4[________________ Protection of capital<br/> Minimal loss]
B -> B5[~ Stable growth<br/> Projected results]

C --> C1 [Medial risk, average return<br/>Risk: 10-15%, Return: 6-10%]
C --> C2 [Mixture of shares and bonds<br/>60% Stocks, 40% Bonds]
C --> C3[ ] is appropriate for most investors <br/> Average age, experience]
C --> C4[# Risk balance and return <br/> Optimal ratio]
C-> C5[------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

D -> D1 [High risk, high return<br/>Risk: 15-25%, Return: 10-15%]
D -> D2[Alternative investments<br/>Stocks, REITs, Commodities]
D -> D3[\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\ \\\\\\\\\\\\\ \\\\ \\\\\\\\ \\\\\ \\\\\\\\\ \\\\\\\ \\\\\\\ \\\\/\\\\\\\\\\\\\\\\\\\\\\\\ \\ \ \\\ \\\\\\\\\ \\\\\\\ \\\\\\\\\\\\\\\\\\ \\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\ \ \ \ \ \ \ \/ \/ \\/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \ \/ \/ \ \ \ \ \ \ \ \ \ \ }/ \ } Young/ }/ }/ } Young/ } Young/ } Young/ } Young/} Young/ } Young/
D -> D4[] High growth potential <br/> Maximum return]
D -> D5[\\\\\\\br/> Relevant variations]

E --> E1 [Optimal risk/income ratio<br/>Risk: 8-12%, Return: 8-12%]
E --> E2 [various asset classes<br/>Stocks, Bonds, REITs, Commodities, Cash]
E --> E3[: Most effective <br/> Professional investors]
E -> E4[> Maximum diversification<br/> Reduction of correlations]
E -> E5[ should be taken as an approach <br/> Mathematical optimization]

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style C fill:#fff3e0
 style D fill:#ffcdd2
 style E fill:#4caf50
```

♪###1 ♪ Conservative Portfolio ♪

- Low risk, low return
- Bonds, deposits
- Good for conservative investors.

#### 2. Balanced Portfolio

- Average risk, average return
- Exchange of shares and bonds
- Suitable for most investors.

#### 3, aggressive Portfolio

- High risk, high return
- Alternative investments
- Good for aggressive investors.

#### 4. Diversified Portfolio

- Optimal risk/income ratio
- Different asset classes
- Most effective

## Advances in Portfolio

### 1. Classical methhods optimization

### ♪ methhods optimise Portfolio

```mermaid
graph TD
A[methods optimization of Portfolio] -> B [Classical methhods]
A -> C [ Contemporary methhods]
 A --> D[ML-methods]

 B --> B1[Markowitz Mean-Variance<br/>max w^T μ - λ/2 * w^T Σ w]
 B --> B2[Black-Litterman Model<br/>Incorporates market Views]
 B --> B3[Capital Asset Pricing Model<br/>CAPM framework]

 C --> C1[Risk Parity Portfolio<br/>Equal risk contribution]
 C --> C2[Minimum Variance Portfolio<br/>Minimize Portfolio variance]
 C --> C3[Maximum Sharpe Portfolio<br/>Maximize Sharpe ratio]
 C --> C4[Equal Weight Portfolio<br/>1/N allocation]

 D --> D1[Clustering-based Portfolio<br/>K-means, Hierarchical]
 D --> D2[ML-based Optimization<br/>Random Forest, Neural networks]
 D --> D3[Factor-based Portfolio<br/>Fama-French factors]
 D --> D4[Reinforcement Learning<br/>Dynamic optimization]

B1 -> E[Target function<br/>Utility = Return - *Risk]
B2 -> F[Inclusion of views<br/>P * μ = Q + .]
C1 -> G [Equivalent contribution in risk<br/>w_i * \_i = constant]
C2 -> H[Minimization of dispersion<br/>min w\T \w]
C3-> I[Maximization Sharpe<br/>max ( μ-r_f) / .]

D1-> J[asset classification<br/>Similar assets grouped]
D2 --> K[ML prediction<br/>Predict returns/risks]
D3 -> L[Factor model<br/>R = α + β * F + ≤]
D4-> M[Adjustative training<br/>Q-learning, Policy Gradient]

E --> N [Porthfolio Optimization]
 F --> N
 G --> N
 H --> N
 I --> N
 J --> N
 K --> N
 L --> N
 M --> N

N --> O[Otimal weights<br/>w* = argmax Utility]
O-> P[Evaluation performance<br/>Sharpe, VaR, Max DD]

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
Optimization of Portfolio on Markowitz

 Parameters:
 -----------
 expected_returns : array-like, shape (n_assets,)
Expected asset returns. There should be a one-dimensional or List array.
with expected returns for each asset in Portfolio.
Example: [0.08, 0.12, 0.06, 0.10] for 4 assets

 cov_matrix : array-like, shape (n_assets, n_assets)
The assets matrix should be a square matrix.
size n_assets x n_assets where element (i,j) represents
(i) and (j). The matrix shall be symmetrical
and positively defined.

 risk_aversion : float, default=1.0
Risk-restraint factor.
and risk in targeted financings. The greater the value, the greater
Investor avoids risk:
- 0.5: Aggressive investor (low tolerance of risk)
- 1.0: Moderate investor (standard value)
2.0: Conservative investor (high tolerance of risk)
- 5.0: Very conservative investor

 target_return : float, optional, default=None
Portfolio target return. if specified, optimization will
Find Portfolio with minimum risk at a specified return.
Should be in the same format as and excepted_returns (e.g. 0.10 for 10 per cent).
If None is optimized on the criterion of maximizing utility.

 target_volatility : float, optional, default=None
Target stability Portfolio. if specified, optimization will be
Find Portfolio with maximum yield at specified volatility.
Should be in the same format as and excepted_returns (e.g. 0.15 for 15%).
If None is optimized on the criterion of maximizing utility.

 Returns:
 --------
 array-like, shape (n_assets,)
The optimal weight of assets in Portfolio is 1.0.
Each element represents the share of capital invested in the asset in question.

 Raises:
 -------
 ValueError
If optimization n has been successful (e.g. incompatible restrictions)

 Notes:
 ------
Target function: max w\T * μ - (\\2) * w\T* * * * ww
where w is the weight, μ is the expected return,

Limitations:
- Weight sum = 1 (full investment)
- Weights >=0 (no short sales)
- Additional limits on yield or volatility (if specifides)
 """
 from scipy.optimize import minimize

 n_assets = len(expected_returns)

# Limitations
Construints = [{'type': 'eq', 'fun': lambda w: np.sum(w)-1}] #Amount of weights = 1

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

# Borders
Sounds = [(0, 1) for _ in ring(n_assets)] # Weights from 0 to 1

# Target function
 def objective(w):
 Portfolio_return = np.dot(w, expected_returns)
 Portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
 return -Portfolio_return + risk_aversion * Portfolio_variance

# Primary Weights
 x0 = np.ones(n_assets) / n_assets

# Optimization
 result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

 if result.success:
 return result.x
 else:
 raise ValueError("Optimization failed")

# Example of use
weights = markowitz_optimization(expected_returns, cov_matrix, risk_aversion=1.0)
```

**Black-Litterman Model:**

```python
def black_litterman_optimization(market_caps, cov_matrix, risk_aversion=3.0,
 Views=None, View_confidences=None):
 """
Optimizing Portfolio on Black-Litterman

The Black-Litterman model combines market weights with subjective views
Investor for more stable and intuitive weights Portfolio.

 Parameters:
 -----------
 market_caps : array-like, shape (n_assets,)
Market capitalization of assets: used for calculating market weights
As a starting point for optimization, there must be a one-dimensional array or List.
with market capitalizations for each asset.
Example: [1000000, 2000000, 500,000, 1500000] for 4 assets

 cov_matrix : array-like, shape (n_assets, n_assets)
The assets matrix should be a square matrix.
size n_assets x n_assets where element (i,j) represents
(i) and (j). The matrix shall be symmetrical
and positively defined.

 risk_aversion : float, default=3.0
Market risk rejection rate. Usually takes values from 1.0 to 5.0.
The more important the market avoids risk:
- 1.0-2.0: Low risk tolerance (aggressive market)
3.0: Standard value for developed markets
- 4.0-5.0: High risk tolerance (conservative market)

 Views : List of tuples, optional, default=None
Subjective views of the investor on assets.
A motorcade (P, Q), where P is an asset vector, Q is the expected return.
Format: [(P1, Q1), (P2, Q2), ...]
 example: [([1, 0, 0, 0], 0.12), ([0, 1, -1, 0], 0.05)]
- First look: asset 1 will yield 12%
- Second look: asset 2 will be on 5% better than asset 3
If None, only the market model is used.

 View_confidences : array-like, optional, default=None
There must be a one-dimensional array.
with the same number of elements as the Views.
positive (more than confidence):
- 0.1: Low confidence (negative view)
- 0.5: Average confidence
- 1.0: High confidence (strong look)
If None, the value of 0.1 for all views is used.

 Returns:
 --------
 tuple
 (weights, expected_returns, Portfolio_cov)

 weights : array-like, shape (n_assets,)
The optimal weight of assets in Portfolio is 1.0.

 expected_returns : array-like, shape (n_assets,)
Expected asset returns with regard to investor &apos; s views.

 Portfolio_cov : array-like, shape (n_assets, n_assets)
Portfolio covariation matrix with views.

 Raises:
 -------
 ValueError
If input dimensions not match or optimization not has succeeded

 Notes:
 ------
The Black-Litterman model addresses the instability of the classic
Optimization of Markowitz by:
1. Using market weights as a starting point
2. Inclusion of investor subjective views
3. Balance between market data and views

Expected return formula:
 E[R] = [(τΣ)^(-1) + P^T * Ω^(-1) * P]^(-1) * [(τΣ)^(-1) * Π + P^T * Ω^(-1) * Q]
where a scale parameter, a matrix of confidence in views
 """
 n_assets = len(market_caps)

♪ Market weights
 market_weights = market_caps / np.sum(market_caps)

# Expected market returns
 market_return = risk_aversion * np.dot(cov_matrix, market_weights)

 if Views is not None:
# A matrix of views
 P = np.array(Views)
 n_Views = len(Views)

# Confidence in the eyes
 if View_confidences is None:
 View_confidences = np.ones(n_Views) * 0.1

# The vision matrix
 Omega = np.diag(View_confidences)

# Expected returns of views
 Q = np.array([View[1] for View in Views])

# Black-Litterman formulas
tau = 1.0 #Speeding parameter
 M1 = np.linalg.inv(tau * cov_matrix)
 M2 = np.dot(P.T, np.dot(np.linalg.inv(Omega), P))
 M3 = np.dot(P.T, np.dot(np.linalg.inv(Omega), Q))

# Expected returns
 expected_returns = np.dot(np.linalg.inv(M1 + M2),
 np.dot(M1, market_return) + M3)

# The matrix
 Portfolio_cov = np.linalg.inv(M1 + M2)
 else:
 expected_returns = market_return
 Portfolio_cov = cov_matrix

# Optimizing Markowitz
 weights = markowitz_optimization(expected_returns, Portfolio_cov, risk_aversion)

 return weights, expected_returns, Portfolio_cov

# Example of use
weights, expected_returns, Portfolio_cov = black_litterman_optimization(
 market_caps, cov_matrix, risk_aversion=3.0, Views=Views
)
```

♪##2. ♪ Modern methhods optimization ♪

**Risk Parity Portfolio:**

```python
def risk_parity_optimization(cov_matrix, target_risk=None):
 """
Optimizing Portfolio with equal contribution in risk

Rick Parity is a Portfolio optimization method where every asset
It makes an equal contribution in total risk Portfolio.
A balanced distribution of risk among assets.

 Parameters:
 -----------
 cov_matrix : array-like, shape (n_assets, n_assets)
The assets matrix should be a square matrix.
size n_assets x n_assets where element (i,j) represents
(i) and (j). The matrix shall be symmetrical
and positively defined.

 target_risk : float, optional, default=None
Target risk level Portfolio. if specific, Portfolio will be
Optimized for achieving this level of risk with equal
Distribution of in-risk contribution between assets.
- None: Optimization without limitation on overall risk
- 0.10: Target risk 10% (standard deviation)
- 0.15: Target risk 15%
- 0.20: Target risk 20%

 Returns:
 --------
 array-like, shape (n_assets,)
The optimal weight of assets in Portfolio is 1.0.
Each asset makes an equal contribution in total risk Portfolio.

 Raises:
 -------
 ValueError
If optimization n has succeeded or covariation matrix is incorrect

 Notes:
 ------
Risk Parity solves the problem:
 min Σᵢ Σⱼ (wᵢ * σᵢ - wⱼ * σⱼ)²
 subject to: Σᵢ wᵢ = 1, wᵢ ≥ 0

where wi is the weight of asset i, ,i is the volatility of asset i

The advantages of Rick Paraity:
1. More stable weights compared to Markowitz
2. Better diversification of risk
3. Less sensitivity to errors in parameter evaluation
4. More intuitive risk distribution

Disadvantages:
1. May not maximize returns
2. It may not be optimal for investors to have different preferences
 """
 from scipy.optimize import minimize

 n_assets = len(cov_matrix)

# Targeted function - minimizing the amount of risk squares
 def objective(w):
 Portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
 individual_risks = np.sqrt(np.diag(cov_matrix))
 target_risks = w * individual_risks

# Normalization
 if target_risk is not None:
 target_risks = target_risks / np.sum(target_risks) * target_risk

 return np.sum((target_risks - target_risks.mean()) ** 2)

# Limitations
 constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
 bounds = [(0, 1) for _ in range(n_assets)]

# Primary Weights
 x0 = np.ones(n_assets) / n_assets

# Optimization
 result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

 if result.success:
 return result.x
 else:
 raise ValueError("Optimization failed")

# Example of use
weights = risk_parity_optimization(cov_matrix, target_risk=0.1)
```

**Minimum Variance Portfolio:**

```python
def minimum_variance_optimization(cov_matrix):
 """
Optimizing Portfolio with minimum dispersion (Minimum Variance Portfolio)

Minimum Variance Portfolio is the Portfolio with the least possible
By dispersive (Risk) among all possible Portfolio.
An approach that minimizes Portfolio's volatility.

 Parameters:
 -----------
 cov_matrix : array-like, shape (n_assets, n_assets)
The assets matrix should be a square matrix.
size n_assets x n_assets where element (i,j) represents
(i) and (j). The matrix shall be symmetrical
and positively defined.

 Returns:
 --------
 array-like, shape (n_assets,)
Optimal weight of assets in Portfolio with minimal dispersion.
The sum of the weights is 1.0.

 Raises:
 -------
 ValueError
If optimization n has succeeded or covariation matrix is incorrect

 Notes:
 ------
Minimum Variance Portfolio solves the problem:
 min w^T * Σ * w
 subject to: Σᵢ wᵢ = 1, wᵢ ≥ 0

where w is the weight of the assets, o is the covariation matrix

Analytical solution:
 w* = (Σ^(-1) * 1) / (1^T * Σ^(-1) * 1)

where 1 is a vector of units

Benefits:
1. Minimum risk among all possible Portfolio
2. Easy calculation and interpretation
3. Stability of weights
4. Good for conservative investors

Disadvantages:
1. May have low returns
2.not takes into account expected returns
3. Maybe not optimal for investors with other preferences
4. Sensitivity to errors in the assessment of the covariation matrix
 """
 from scipy.optimize import minimize

 n_assets = len(cov_matrix)

# Target function - minimize dispersion
 def objective(w):
 return np.dot(w, np.dot(cov_matrix, w))

# Limitations
 constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
 bounds = [(0, 1) for _ in range(n_assets)]

# Primary Weights
 x0 = np.ones(n_assets) / n_assets

# Optimization
 result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

 if result.success:
 return result.x
 else:
 raise ValueError("Optimization failed")

# Example of use
weights = minimum_variance_optimization(cov_matrix)
```

**Maximum Sharpe Portfolio:**

```python
def maximum_sharpe_optimization(expected_returns, cov_matrix, risk_free_rate=0.02):
 """
Optimizing Portfolio with the maximum Sharpe coefficient

Maximum Sharpe Portfolio is the Portfolio that maximizes
Sharpe coefficient (rate of excess return to risk).
It's the optimal Portfolio for investors who want to maximize
Interest rate on risk unit.

 Parameters:
 -----------
 expected_returns : array-like, shape (n_assets,)
Expected asset returns. There should be a one-dimensional or List array.
with expected returns for each asset in Portfolio.
Example: [0.08, 0.12, 0.06, 0.10] for 4 assets

 cov_matrix : array-like, shape (n_assets, n_assets)
The assets matrix should be a square matrix.
size n_assets x n_assets where element (i,j) represents
(i) and (j). The matrix shall be symmetrical
and positively defined.

 risk_free_rate : float, default=0.02
Risk-free interest rate.
In the Sharpe coefficient, usually takes the following values:
0.01: 1 per cent (very low rate)
0.02: 2% (standard value for developed markets)
- 0.03: 3% (moderate rate)
0.05: 5 per cent (high rate)

 Returns:
 --------
 array-like, shape (n_assets,)
Optimal weight of assets in Portfolio with the maximum Sharpe coefficient.
The sum of the weights is 1.0.

 Raises:
 -------
 ValueError
If optimization no has been successful or input data incorrect

 Notes:
 ------
Maximum Sharpe Portfolio solves the problem:
 max (w^T * μ - r_f) / √(w^T * Σ * w)
 subject to: Σᵢ wᵢ = 1, wᵢ ≥ 0

where w is the weight of assets, μ is the expected return,
r_f = risk-free rate

Sharp coefficient:
 Sharpe = (E[R_p] - r_f) / σ_p

where E[R_p] is the expected rate of return of Portfolio, \\p is the volatility of Portfolio

Benefits:
1. Maximize return on risk unit
2. Take into account both return and risk
3. Widely used in practice
4. Intuitive indicator

Disadvantages:
1. Sensitivity to errors in parameter evaluation
2. Suspects a normal distribution of returns
3.not takes into account the asymmetries and excesses of distribution
4. May be unstable when changing parameters
 """
 from scipy.optimize import minimize

 n_assets = len(expected_returns)

# Target function - maximization of Sharpe coefficient
 def objective(w):
 Portfolio_return = np.dot(w, expected_returns)
 Portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
 sharpe = (Portfolio_return - risk_free_rate) / np.sqrt(Portfolio_variance)
Return -sharpe # Minimize Negative Sharpe

# Limitations
 constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
 bounds = [(0, 1) for _ in range(n_assets)]

# Primary Weights
 x0 = np.ones(n_assets) / n_assets

# Optimization
 result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

 if result.success:
 return result.x
 else:
 raise ValueError("Optimization failed")

# Example of use
weights = maximum_sharpe_optimization(expected_returns, cov_matrix, risk_free_rate=0.02)
```

###3 Car training in Portfolio control

### 🤖 integration machine learning in Management Portfolio

```mermaid
graph TD
A[ML in Portfolio management] -> B[Predication of income]
A -> C [asset classification]
A -> D [Optimization of Portfolio]
A -> E[Manage of risks]
A -> F [Dynamic rebalancing]

 B --> B1[Time Series Models<br/>LSTM, GRU, Transformer]
 B --> B2[Ensemble Methods<br/>Random Forest, XGBoost]
 B --> B3[Deep Learning<br/>Neural networks, CNN]
 B --> B4[Feature Engineering<br/>Technical indicators, Sentiment]

 C --> C1[K-means Clustering<br/>Group similar assets]
 C --> C2[Hierarchical Clustering<br/>Dendrogram-based grouping]
 C --> C3[DBSCAN<br/>Density-based clustering]
 C --> C4[Gaussian Mixture<br/>ProbabiListic clustering]

 D --> D1[Reinforcement Learning<br/>Q-learning, Policy Gradient]
 D --> D2[Genetic Algorithms<br/>Evolutionary optimization]
 D --> D3[Bayesian Optimization<br/>Gaussian Process optimization]
 D --> D4[Multi-objective Optimization<br/>Pareto frontier]

 E --> E1[VaR Prediction<br/>ML-based VaR estimation]
 E --> E2[Stress testing<br/>Scenario generation with ML]
 E --> E3[Anomaly Detection<br/>Outlier detection in returns]
 E --> E4[Regime Detection<br/>Market regime classification]

 F --> F1[signal Generation<br/>ML-based trading signals]
 F --> F2[Threshold Optimization<br/>Dynamic rebalancing thresholds]
 F --> F3[Transaction Cost Modeling<br/>Cost-aware rebalancing]
 F --> F4[Market MicroStructure<br/>Order book Analysis]

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

G --> H [model training<br/>Train on historical data]
 H --> I[validation<br/>Cross-validation, Walk-forward]
I --> J [Sales in sales<br/>Real-time preferences]
 J --> K[Monitoring performance<br/>Model performance tracking]

K --> L{model is effective?}
L -->\\\\M[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\L\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\\\/(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\L/\\\\\\L\\\\\\\\/\\\\\\L\/\\\\\\\\\\\L\/\/\/\/\/\L\/\/\/\/((((\\\\\\\\\\\/\L\L\L\L\L\L\\\\\\\\\\\\\\\\\\\\\\\\\\/E/E/E/E/E/E/E/E/E/E/E/ }}}}}}}}}}}}}}}/((((((((((((((((((((((((\/)}}}}}}}}}}}}}}}}}}}}}}}}}}}}/((((((((((((((((((((((((((((((((()}}}}}}}}}}}}}}}}}}}}}})})})})})/((((((()})/(((((((((((((((((((((
L-~ ~ No~ N[~ Reschedule the model]

N --> O[Degradation analysis<br/>Identify performance decline]
O --> P[update data<br/>Include new market data]
 P --> Q[retraining<br/>Retrain with updated data]
Q --> R[validation of updated model<br/>Test on out-of-sample data]
R --> S[S[Replace updated model<br/>Replace Old model]
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
def clustering_Portfolio_optimization(returns, n_clusters=5, method='kmeans'):
 """
Optimization of the Portfolio on Basis clustering of assets

This method groups assets into clusters on base of their returns,
and then create optimized Portfolio for each cluster.
This allows for a better diversification of Portfolio and takes into account
Similarity between assets.

 Parameters:
 -----------
 returns : pandas.dataFrame, shape (n_periods, n_assets)
Asset return matrix: The lines represent time periods,
Columns are assets. Data should be in pandas dataFrame format.
with index dates and asset names in columns.
Example: DataFrame with dates and columns ['AAPL', 'GOOGL', 'MSFT', 'TSLA']

 n_clusters : int, default=5
Number of clusters for asset grouping: Recommended values:
- 3-5: for a small Portfolio (10-20 assets)
- 5-8: for average Portfolio (20-50 assets)
- 8-12: for large Portfolio (50+assets)
- Too few clusters: may not take into account differences between assets
- Too many clusters: may lead to retraining.

 method : str, default='kmeans'
Method of clustering for asset grouping: options available:
- 'kmeans': K-means clustering (rapid, suitable for spherical clusters)
- 'hierarchical': Hierarchical clustering (slow, suitable for clusters of any form)

 Returns:
 --------
 dict
A dictionary with information on clusters and their weights.
values - dictionaries with keys:
 - 'weights': array-like, shape (n_assets_in_cluster,)
Optimal weight of assets in cluster
 - 'assets': List
List of asset names in cluster

 Raises:
 -------
 ValueError
If the clustering method is unknown or data incorrect

 Notes:
 ------
Work algorithm:
1. Normalization of these returns
2. Clustering of assets on returns
3. For each cluster:
- Calculation of the covariation matrix
- Balance optimization (minimum dispersion)
- Normalization of weights
4. Return of weights for each cluster

Benefits:
1. Take into account the similarities between assets
2. Better diversification
3. Decoupling correlations within clusters
4. More stable weights

Disadvantages:
1. Dependency from the selection of the number of clusters
2. Emission sensitivity
3. Maybe not Working for a small number of assets
 """
 from sklearn.cluster import KMeans, AgglomerativeClustering
 from sklearn.preprocessing import StandardScaler

# Data normalization
 scaler = StandardScaler()
 returns_scaled = scaler.fit_transform(returns)

# Clusterization
 if method == 'kmeans':
 clusterer = KMeans(n_clusters=n_clusters, random_state=42)
 elif method == 'hierarchical':
 clusterer = AgglomerativeClustering(n_clusters=n_clusters)
 else:
 raise ValueError(f"Unknown clustering method: {method}")

 clusters = clusterer.fit_predict(returns_scaled)

# Create Portfolio for each cluster
 Portfolio_weights = {}

 for cluster_id in range(n_clusters):
 cluster_returns = returns[clusters == cluster_id]

 if len(cluster_returns) > 1:
# Optimization within the cluster
 cluster_cov = np.cov(cluster_returns.T)
 cluster_expected_returns = np.mean(cluster_returns, axis=0)

# Minimum dispersion within the cluster
 cluster_weights = minimum_variance_optimization(cluster_cov)

# Normalization of weights
 cluster_weights = cluster_weights / np.sum(cluster_weights)

 Portfolio_weights[cluster_id] = {
 'weights': cluster_weights,
 'assets': cluster_returns.columns[clusters == cluster_id].toList()
 }

 return Portfolio_weights

# Example of use
clustering_Portfolio = clustering_Portfolio_optimization(returns, n_clusters=5, method='kmeans')
```

**ML-based Portfolio Optimization:**

```python
def ml_Portfolio_optimization(returns, features, model, n_Portfolios=1000):
 """
Optimizing Portfolio with the use of machine lightning

This method uses ML models for forecasting asset returns,
and then creates a bunch of Portfolios and selects the best on Sharpe coefficient.
This makes it possible to take into account complex non-linear dependencies in data.

 Parameters:
 -----------
 returns : pandas.dataFrame, shape (n_periods, n_assets)
Asset return matrix: The lines represent time periods,
Columns are assets. Data should be in pandas dataFrame format.
with index dates and asset names in columns.
Example: DataFrame with dates and columns ['AAPL', 'GOOGL', 'MSFT', 'TSLA']

 features : pandas.dataFrame, shape (n_periods, n_features)
The sign matrix for the ML model, the lines represent the time periods,
Columns are signs. May include Technical indicators,
macroeconomic data, news data, etc.
Example: DataFrame with signature ['RSI', 'MACD', 'Volume', 'GDP_growth']

 model : sklearn-compatible model
A trained ML model for forecasting returns. Should have methods.
Fit() and predict() Recommended models:
- RandomForestRegressor: Good Working with non-linear addictions
- XGBRegressor: High performance, re-training resistance
- LinearRegression: Simple and Fast Model
- LSTM/GRU: for time series (requires special data preparation)

 n_Portfolios : int, default=1000
Quantity of Portfolio for generation and estimation: Recommended values:
- 100-500: Rapid analysis, low accuracy
- 1000: Standard value, good balance of speed and accuracy
- 5000-10000: High accuracy, slow analysis
More Portfolio: Better to cover the solution space.

 Returns:
 --------
 tuple
 (best_Portfolio, all_Portfolios)

 best_Portfolio : dict
Best Portfolio on Sharp coefficient with keys:
 - 'weights': array-like, shape (n_assets,)
Optimal weight of assets
 - 'return': float
Porthfolio expected return
 - 'variance': float
Portfolio Dispersion
 - 'sharpe': float
Sharp Portfolio Coefficient

 all_Portfolios : List
List all derived Portfolio with the same keys,
that and best_Porthfolio

 Raises:
 -------
 ValueError
If the dimensions of the data not match or model is incorrect

 Notes:
 ------
Work algorithm:
1. Data sharing on train/test (80/20)
2. Training ML model on historical data
3. Pricing of returns on test data
4. Generation n_Porthfolios of random weights
5. Calculation of metrics for each Portfolio
6. Porthfolio with the maximum Sharpe coefficient

Benefits:
1. Take into account complex non-liner dependencies
2. Uses multiple features
3. Adapted to changing market conditions
4. May take into account qualitative factors

Disadvantages:
1. Requires quality data and indicators
2. May be retrained on historical data
3. Complexity of interpretation of results
4. Dependency from model and parameter selection
 """
 from sklearn.ensemble import RandomForestRegressor
 from sklearn.model_selection import train_test_split

# Data production
 X = features
 y = returns

# Separation on train/test
 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model learning
 model.fit(X_train, y_train)

# Premonition
 predictions = model.predict(X_test)

# Create of the Portfolio
 Portfolios = []

 for i in range(n_Portfolios):
# Random weights
 weights = np.random.dirichlet(np.ones(len(returns.columns)))

# Porthfolio's expected return
 Portfolio_return = np.dot(weights, predictions.mean(axis=0))

# Portfolio risk
 Portfolio_variance = np.dot(weights, np.dot(predictions.cov(), weights))

# Sharpe coefficient
 sharpe = Portfolio_return / np.sqrt(Portfolio_variance)

 Portfolios.append({
 'weights': weights,
 'return': Portfolio_return,
 'variance': Portfolio_variance,
 'sharpe': sharpe
 })

# Choosing the best Portfolio
 best_Portfolio = max(Portfolios, key=lambda x: x['sharpe'])

 return best_Portfolio, Portfolios

# Example of use
best_Portfolio, all_Portfolios = ml_Portfolio_optimization(returns, features, model)
```

## Methods diversification

### ♪ Portfolio diversification strategies

```mermaid
graph TD
A[Diversification strategies] -> B [Classical diversification]
A-> C [Processed methhods]
A -> D [Factor diversification]

B -> B1 [Geographic diversification<br/> Different countries and regions]
B -> B2 [Secret diversification<br/> Different economic sectors]
B --> B3 [Temporary diversification<br/>Dollar-cost overgrowing]
B --> B4 [Class diversification<br/>Stocks, Bonds, REITs, Commodities]

C -> C1 [Coordination diversification<br/> Low correlations between assets]
C -> C2 [Factor diversification<br/> Different risk factors]
C --> C3 [Style diversification<br/>Value, Growth, Momentum, Quality]
C --> C4 [Diversifying <br/>Large, Mid, Small Cap]

D --> D1[Fama-French factors<br/>Market, Size, Value]
D -> D2 [Macroeconomic factors<br/>Interest rates, Inflation, GDP]
D --> D3 [Technical factors<br/>Momentum, Volatility, Liquidity]
D -> D4 [Basic factors<br/>P/E, P/B, ROE, Debt/Equity]

B1 -> E [Country limits<br/>max_white_per_country ≤ 30%]
B2 -> F[Restrictions on sectors<br/>max_white_per_sector ≤ 25%]
C1-> G[Maximum correlation<br/>max_control ≤ 0.7]
C2 --> H[Maximum exposition to factor<br/>max_factor_exposure ≤ 0.5]

E -> I [Optimization of weights]
 F --> I
 G --> I
 H --> I

I -> J [Diversified Portfolio]
J --> K[Risk reduction<br/>lower Portfolio voltility]
 J --> L[improve Sharpe ratio<br/>Better risk-adjusted returns]
J --> M[Standing to shocks<br/>Resilience to market stock]

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style C fill:#fff3e0
 style D fill:#f3e5f5
 style J fill:#4caf50
```

###1: Classical diversification

**Geographic diversification:**

```python
def geographic_diversification(returns_by_country, max_weight_per_country=0.3):
 """
Geographical diversification of Portfolio

This method optimizes Portfolio with geographical distribution
By limiting the maximum weight on each country.
Reduce country risks and improve diversification.

 Parameters:
 -----------
 returns_by_country : dict
A dictionary with returns on countries. Keys are country names.
the value of the pandas.Series with the asset returns in that country.
Format: {'USA': returns_usa, 'EU': returns_eu, 'Asia': returns_asia}
where returns_usa - Series with American assets

 max_weight_per_country : float, default=0.3
Maximum weight on one country in Portfolio. Recommended values:
- 0.2: High diversification (maximum 20% on country)
- 0.3: Standard diversification (maximum 30% on country)
- 0.4: Moderate diversification (maximum 40% on country)
- 0.5: Low diversification (50 per cent maximum on country)
- The value shall be in range (0, 1]

 Returns:
 --------
 array-like, shape (n_countries,)
The optimal weights of countries in Portfolio are 1.0.
Each element represents the share of capital invested
In the assets of the country concerned.

 Raises:
 -------
 ValueError
If optimization not succeeded or parameters were incorrect

 Notes:
 ------
Work algorithm:
1. Calculation of expected returns on countries
2. Calculation of the matrix between countries
3. Optimizing with restrictions on maximum weight on the country
4. Return of optimal country weights

Benefits:
1. Country risk reduction
2. Improve diversification
3. Taking into account regional specificities
4. Protection from local crises

Disadvantages:
1. May limit returns
2.not takes into account correlations between countries
3. Requires quality data on countries
4. Could not be optimal for global assets
 """
 n_countries = len(returns_by_country)

# Limitations on countries
 constraints = []
 bounds = []

 for i in range(n_countries):
# Maximum weight on country
 constraints.append({
 'type': 'ineq',
 'fun': lambda w, i=i: max_weight_per_country - w[i]
 })
 bounds.append((0, max_weight_per_country))

# Weight sum = 1
 constraints.append({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# Expected returns on countries
 expected_returns = np.array([returns.mean() for returns in returns_by_country.values()])

# The matrix
 cov_matrix = np.cov([returns for returns in returns_by_country.values()])

# Optimization
 from scipy.optimize import minimize

 def objective(w):
 Portfolio_return = np.dot(w, expected_returns)
 Portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
 return -Portfolio_return + 0.5 * Portfolio_variance

 x0 = np.ones(n_countries) / n_countries

 result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

 if result.success:
 return result.x
 else:
 raise ValueError("Optimization failed")

# Example of use
country_weights = geographic_diversification(returns_by_country, max_weight_per_country=0.3)
```

** Sectoral diversification:**

```python
def sectoral_diversification(returns_by_sector, max_weight_per_sector=0.25):
"The Sectoral Diversification of Portfolio."
 n_sectors = len(returns_by_sector)

# Restrictions on sectors
 constraints = []
 bounds = []

 for i in range(n_sectors):
# Maximum weight on sector
 constraints.append({
 'type': 'ineq',
 'fun': lambda w, i=i: max_weight_per_sector - w[i]
 })
 bounds.append((0, max_weight_per_sector))

# Weight sum = 1
 constraints.append({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# Expected returns on sectors
 expected_returns = np.array([returns.mean() for returns in returns_by_sector.values()])

# The matrix
 cov_matrix = np.cov([returns for returns in returns_by_sector.values()])

# Optimization
 from scipy.optimize import minimize

 def objective(w):
 Portfolio_return = np.dot(w, expected_returns)
 Portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
 return -Portfolio_return + 0.5 * Portfolio_variance

 x0 = np.ones(n_sectors) / n_sectors

 result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

 if result.success:
 return result.x
 else:
 raise ValueError("Optimization failed")

# Example of use
sector_weights = sectoral_diversification(returns_by_sector, max_weight_per_sector=0.25)
```

♪##2 ♪ advanced methhods diversification

**Factor-based Diversification:**

```python
def factor_diversification(returns, factors, max_factor_exposure=0.5):
"Divertion on factors."
 from sklearn.linear_model import LinearRegression

 n_assets = len(returns.columns)
 n_factors = len(factors.columns)

# Recession of returns on factors
 factor_Loadings = np.zeros((n_assets, n_factors))

 for i, asset in enumerate(returns.columns):
 model = LinearRegression()
 model.fit(factors, returns[asset])
 factor_Loadings[i] = model.coef_

# Limitations on factors
 constraints = []
 bounds = [(0, 1) for _ in range(n_assets)]

 for j in range(n_factors):
# Maximum exposure to factor
 constraints.append({
 'type': 'ineq',
 'fun': lambda w, j=j: max_factor_exposure - np.dot(w, factor_Loadings[:, j])
 })
 constraints.append({
 'type': 'ineq',
 'fun': lambda w, j=j: max_factor_exposure + np.dot(w, factor_Loadings[:, j])
 })

# Weight sum = 1
 constraints.append({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# Expected returns
 expected_returns = returns.mean().values

# The matrix
 cov_matrix = returns.cov().values

# Optimization
 from scipy.optimize import minimize

 def objective(w):
 Portfolio_return = np.dot(w, expected_returns)
 Portfolio_variance = np.dot(w, np.dot(cov_matrix, w))
 return -Portfolio_return + 0.5 * Portfolio_variance

 x0 = np.ones(n_assets) / n_assets

 result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

 if result.success:
 return result.x
 else:
 raise ValueError("Optimization failed")

# Example of use
factor_weights = factor_diversification(returns, factors, max_factor_exposure=0.5)
```

**Correlation-based Diversification:**

```python
def correlation_diversification(returns, max_correlation=0.7):
"Divertion on base correlations."
# Correlation matrix
 corr_matrix = returns.corr()

# Searching for assets with low correlation
 selected_assets = []
 remaining_assets = List(returns.columns)

# Choice of the first asset
 first_asset = remaining_assets[0]
 selected_assets.append(first_asset)
 remaining_assets.remove(first_asset)

# Choice of the remaining assets
 while remaining_assets:
 best_asset = None
 best_score = -1

 for asset in remaining_assets:
# Average correlation with assets already selected
 avg_correlation = corr_matrix.loc[asset, selected_assets].mean()

# Assessment of diversification
 diversification_score = 1 - avg_correlation

 if diversification_score > best_score:
 best_score = diversification_score
 best_asset = asset

 if best_asset and best_score > (1 - max_correlation):
 selected_assets.append(best_asset)
 remaining_assets.remove(best_asset)
 else:
 break

# Optimizing weights for selected assets
 selected_returns = returns[selected_assets]
 expected_returns = selected_returns.mean().values
 cov_matrix = selected_returns.cov().values

# Equal weights
 weights = np.ones(len(selected_assets)) / len(selected_assets)

 return weights, selected_assets

# Example of use
weights, selected_assets = correlation_diversification(returns, max_correlation=0.7)
```

## Risk Management Portfolio

### * risk management metrics Portfolio

```mermaid
graph TD
A[risk management instruments] -> B [Value at Risk - VaR]
 A --> C[Expected Shortfall - ES]
A -> D [Maximum draught]
A -> E [Supplementary metrics]

 B --> B1[Historical VaR<br/>Percentile-based approach]
 B --> B2[Parametric VaR<br/>Normal distribution assumption]
 B --> B3[Monte Carlo VaR<br/>Simulation-based approach]
B -> B4 [Confidence levels<br/>90%, 95%, 99%]

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

B1 -> F [Risk calculation]
 B2 --> F
 B3 --> F
 C1 --> F
 D1 --> F
 E1 --> F

F --> G [Porthfolio risk assessment]
 G --> H[VaR 95%: -2.5%<br/>ES 95%: -3.8%<br/>Max DD: -15.2%]

H -> I [Management of risks]
I -> J [Position based on VaR]
I -> K[Hedgeing<br/>Derivatives for Risk production]
I --> L[Divertion<br/>Correlation-based allocation]
I --> M[Stop-losses<br/>Automatic risk control]

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
Calculation of historical Value at Risk (VAR)

Historical VaR is a method of calculating VaR based on historical
It makes assumptions about the distribution of income.
It uses empirical quantils.

 Parameters:
 -----------
 returns : array-like, shape (n_periods,)
Porthfolio or asset's income mass.
or numpy.array. data should be in the return format
(e.g. 0.05 for 5% return).

 confidence_level : float, default=0.95
Level of confidence for VAR. Determines what percentage
The worst-case scenarios are excluded from Analysis. Recommended values:
0.90: 90 per cent confidence level (excluding 10 per cent of worst scenarios)
0.95: 95 per cent confidence level (standard)
0.99: 99 per cent confidence level (excluding 1 per cent of worst scenarios)
- 0.999: 99.9 per cent confidence level (excluding 0.1 per cent of worst scenarios)
- The value shall be in range (0, 1)

 Returns:
 --------
 float
Value at Risk on a given level of trust.
Representing the maximum expected loss with the intended probability.
For example, if VaR = -0.05, with probability of conference_level
The loss not exceeds 5 per cent.

 Raises:
 -------
 ValueError
If conference_level not in range (0,1) or data is empty

 Notes:
 ------
Calculation formula:
 VaR = percentile(returns, (1 - confidence_level) * 100)

where percentile is an empirical quintile

Benefits:
1.not requires distribution assumptions
2. Taking into account real historical data
3. Simplicity of calculation and interpretation
4. Emission resistance

Disadvantages:
1. Dependency from historical data
2.not takes into account changes in volatility
3. Could be inaccurate for rare events
4. Requires a sufficiently long history of data
 """
# Sorting the returns
 sorted_returns = np.sort(returns)

 # index for VaR
 var_index = int((1 - confidence_level) * len(sorted_returns))

 # VaR
 var = sorted_returns[var_index]

 return var

# Example of use
var_95 = historical_var(Portfolio_returns, confidence_level=0.95)
```

**Parametric VaR:**

```python
def parametric_var(returns, confidence_level=0.95):
"The Parametric VaR"
 from scipy import stats

# Parameters normal distribution
 mean_return = returns.mean()
 std_return = returns.std()

# Z-score for a given level of trust
 z_score = stats.norm.ppf(1 - confidence_level)

 # VaR
 var = mean_return + z_score * std_return

 return var

# Example of use
var_95 = parametric_var(Portfolio_returns, confidence_level=0.95)
```

**Monte Carlo VaR:**

```python
def monte_carlo_var(returns, confidence_level=0.95, n_simulations=10000):
 """Monte Carlo VaR"""
# Parameters distribution
 mean_return = returns.mean()
 std_return = returns.std()

# Simulations
 simulations = np.random.normal(mean_return, std_return, n_simulations)

 # VaR
 var = np.percentile(simulations, (1 - confidence_level) * 100)

 return var

# Example of use
var_95 = monte_carlo_var(Portfolio_returns, confidence_level=0.95, n_simulations=10000)
```

### 2. Expected Shortfall (ES)

```python
def expected_shortfall(returns, confidence_level=0.95):
 """Expected Shortfall (Conditional VaR)"""
 # VaR
 var = historical_var(returns, confidence_level)

# Anticipated loss over VaR
 es = returns[returns <= var].mean()

 return es

# Example of use
es_95 = expected_shortfall(Portfolio_returns, confidence_level=0.95)
```

###3 # The maximum tarmac #

```python
def maximum_drawdown(returns):
"Maximal prosperity."
# Cumulative returns
 cumulative_returns = (1 + returns).cumprod()

# A rolling maximum
 running_max = cumulative_returns.expanding().max()

# Slide
 drawdown = (cumulative_returns - running_max) / running_max

# Maximum tarmac
 max_drawdown = drawdown.min()

 return max_drawdown

# Example of use
max_dd = maximum_drawdown(Portfolio_returns)
```

## Dynamic Management Portfolio

### ♪ Dynamic Management Portfolio

```mermaid
graph TD
A [Dinical Management Portfolio] -> B [Rebalance]
A-> C[Advancative Management]
A-> D[Monitoring and control]

B --> B1 [Temporary rebalancing<br/>Fixed class: Daily, Weekly, Monthly]
B --> B2 [Target rebalancing<br/>When development > threshold]
B --> B3 [The cost of rebalancing<br/>Transaction costs consultation]
B --> B4 [Otimal frequency<br/>Balance between cost and benefit]

 C --> C1[Volatility-based Rebalancing<br/>Adjust based on market volatility]
 C --> C2[Momentum-based Rebalancing<br/>Follow market momentum]
 C --> C3[Regime-based Rebalancing<br/>Different strategies per market regime]
 C --> C4[ML-based Rebalancing<br/>Machine learning predictions]

 D --> D1[Real-time Monitoring<br/>Continuous Portfolio tracking]
 D --> D2[Risk Alerts<br/>VaR, ES, Drawdown warnings]
 D --> D3[Performance Tracking<br/>Sharpe, Return, Volatility]
 D --> D4[Compliance Monitoring<br/>Regulatory constraints]

B1 -> E [Rebalancing strategies]
 B2 --> E
C1-> F[Adjustative strategies]
 C2 --> F
 C3 --> F
 C4 --> F
D1-> G [control systems]
 D2 --> G
 D3 --> G
 D4 --> G

E -> H [Optimization of Portfolio]
 F --> H
 G --> H

H --> I [Dynamic weights<br/>w_t = f(market_conditions_t)]
I -> J[Efficiency evaluation<br/>Performance vs Statistical Portfolio]

 J --> K{improve performance?}
K--~ ♪ Yeah ♪ L[~ Continue dynamic Management]
K-----------no-- no-- M-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

M --> N[Analysis of causes<br/> Whoy dynamic management failed?]
N --> O [Corresponding parameters<br/>Adjust theseolds, frequencies]
O-> P[Re-testing<br/>Backtest up-date strategy]
 P --> H

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style C fill:#fff3e0
 style D fill:#f3e5f5
 style L fill:#4caf50
 style M fill:#ff9800
```

*## 1. Rebalancing

** Temporary rebalancing:**

```python
def time_based_rebalancing(returns, target_weights, rebalance_freq='M'):
 """
Rebalancing Portfolio in Time

This method rebalances the Portfolio through the Zadata
Time intervals, returning weights to target values.
This helps to maintain the desired distribution of assets.

 Parameters:
 -----------
 returns : pandas.dataFrame, shape (n_periods, n_assets)
Asset return matrix: The lines represent time periods,
Columns are assets. Data should be in pandas dataFrame format.
with index dates and asset names in columns.

 target_weights : array-like, shape (n_assets,)
Target weight of assets in Portfolio.
or List with weights for each asset. The weight sum should be 1.0.
example: [0.4, 0.3, 0.2, 0.1] for 4 assets

 rebalance_freq : str, default='M'
Portfolio rebalancing frequency. Available options:
- 'D': Daily rebalancing (each day)
- 'W': Weekly rebalancing (every 7 days)
- 'M': Monthly rebalancing (every 30 days)
- 'Q': Quarterly rebalancing (every 90 days)
- 'Y': Annual rebalancing (every 365 days)

 Returns:
 --------
 pandas.Series, shape (n_periods,)
temporary series of returns of rebalanced Portfolio.
The index corresponds to the index of input data returns.

 Raises:
 -------
 ValueError
If the rebalancing frequency is unknown or data incorrect

 Notes:
 ------
Work algorithm:
1. Determination of the dates of rebalancing on base frequency
2. For each period:
- If rebalancing date: balance installation = Target_weights
- Otherwise: Use of current weights
- Calculation of the return on Portfolio
3. Return of the time series of returns

Benefits:
1. Simplicity of implementation and understanding
2. Predictability of rebalancing
3. Control of transaction costs
4. Approached for long-term strategies

Disadvantages:
1. May not take into account market conditions
2. The fixed frequency may be non-optimal
3. Not adapts to changes in volatility
4. May lead to excessive trade
 """
# creative index for rebalancing
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

# Rebalancing
 rebalanced_returns = []
 current_weights = target_weights.copy()

 for i, date in enumerate(returns.index):
 if date in rebalance_dates:
 current_weights = target_weights.copy()

# Portfolio income
 Portfolio_return = np.dot(current_weights, returns.loc[date])
 rebalanced_returns.append(Portfolio_return)

 return pd.Series(rebalanced_returns, index=returns.index)

# Example of use
rebalanced_returns = time_based_rebalancing(returns, target_weights, rebalance_freq='M')
```

** Threshold rebalancing:**

```python
def threshold_rebalancing(returns, target_weights, threshold=0.05):
"Rebalance on the deviation threshold."
 rebalanced_returns = []
 current_weights = target_weights.copy()

 for i, date in enumerate(returns.index):
# Check weight deviation
 weight_deviation = np.abs(current_weights - target_weights)
 max_deviation = weight_deviation.max()

 if max_deviation > threshold:
 current_weights = target_weights.copy()

# Portfolio income
 Portfolio_return = np.dot(current_weights, returns.loc[date])
 rebalanced_returns.append(Portfolio_return)

 return pd.Series(rebalanced_returns, index=returns.index)

# Example of use
rebalanced_returns = threshold_rebalancing(returns, target_weights, threshold=0.05)
```

♪## 2. Adaptive Management

**Volatility-based Rebalancing:**

```python
def volatility_based_rebalancing(returns, target_weights, volatility_window=30,
 volatility_threshold=0.02):
"Rebalance on baseline volatility."
 rebalanced_returns = []
 current_weights = target_weights.copy()

 for i, date in enumerate(returns.index):
 if i >= volatility_window:
# Calculation of volatility
 recent_returns = returns.iloc[i-volatility_window:i]
 volatility = recent_returns.std().mean()

# Rebalancing with high volatility
 if volatility > volatility_threshold:
 current_weights = target_weights.copy()

# Portfolio income
 Portfolio_return = np.dot(current_weights, returns.loc[date])
 rebalanced_returns.append(Portfolio_return)

 return pd.Series(rebalanced_returns, index=returns.index)

# Example of use
rebalanced_returns = volatility_based_rebalancing(returns, target_weights,
 volatility_window=30, volatility_threshold=0.02)
```

**Momentum-based Rebalancing:**

```python
def momentum_based_rebalancing(returns, target_weights, momentum_window=20,
 momentum_threshold=0.1):
"Rebalance on Bases momentum."
 rebalanced_returns = []
 current_weights = target_weights.copy()

 for i, date in enumerate(returns.index):
 if i >= momentum_window:
# Calculation of momentum
 recent_returns = returns.iloc[i-momentum_window:i]
 momentum = recent_returns.mean().mean()

# Rebalancing in changing the moment
 if abs(momentum) > momentum_threshold:
 current_weights = target_weights.copy()

# Portfolio income
 Portfolio_return = np.dot(current_weights, returns.loc[date])
 rebalanced_returns.append(Portfolio_return)

 return pd.Series(rebalanced_returns, index=returns.index)

# Example of use
rebalanced_returns = momentum_based_rebalancing(returns, target_weights,
 momentum_window=20, momentum_threshold=0.1)
```

## Monitoring and evaluation Portfolio

### Monitoring and assessment Portfolio

```mermaid
graph TD
A[Monitoring and evaluation of Portfolio] -> B [Metrics performance]
A -> C[Risk analysis]
A -> D [Visualization]
A --> E [Reportability]

B --> B1 [Property<br/>Total Return, Annual Return]
B --> B2 [Risk-corrected yield<br/>Sharpe Rato, Sortino Rato]
B --> B3 [Sediments<br/>Max Drawdown, DrawdownDuration]
B --> B4 [Stability<br/>Volatility, Office of Aviation]
B --> B5 [Efficiency<br/>Calmar Rato, Information Ratoi]

 C --> C1[Value at Risk<br/>VaR 90%, 95%, 99%]
 C --> C2[Expected Shortfall<br/>Conditional VaR]
C --> C3 [Coordination analysis<br/>Asset corporations, Factor projections]
C --> C4 [Scenario Analysis, Monte Carlo]
C --> C5 [Regulatory risks<br/>Basel III, Solvency II]

D --> D1 [Cumulative return <br/> Cumulative return chart]
D -> D2 [Retributive distribution<br/>Return distribution histogram]
D --> D3 [Sediments<br/>Drawdown chart]
D --> D4 [Slipping metrics<br/>Rolling Sharpe, Volatility]
D --> D5 [comparison with the bookmark<br/>Porthfolio vs Benchmark]
D -> D6 [Analysis of the asset contribution<br/>Asset contribution Analysis]

E --> E1[Dailly performance summary]
E --> E2[ Weekly Reports<br/>Weekly Rick and retern Analysis]
E --> E3[monthly Reports<br/>Monthly Portfolio reView]
E --> E4 [Quarterly Reports<br/>Quarterly attribution Analysis]
E --> E5[Alerts and references<br/>Risk aerts, Performance aerts]

B1-> F [Metrics calculation]
 B2 --> F
 B3 --> F
 B4 --> F
 B5 --> F
 C1 --> F
 C2 --> F
 C3 --> F
 C4 --> F
 C5 --> F

F --> G[Analysis performance]
G --> H[comparison with objectives<br/>Performance vs Target]
G --> I [comparison with benchmarking<br/>Performance vs Benchmark]
G --> J[Analysis of trends<br/>Performance lines over time]

H -> K[Porthfolio assessment]
 I --> K
 J --> K

K --> L{Porthfolio is effective?}
L -->\\\\M[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\L\\\\\\\\\\\\\\\\\\\\\\\L\\\\\\\\L\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\(\\\\\\\\\\\\\\\\\(\\\\\\\\\\\(\\\\\\\\(\\\\\\L\\\\\\\\\\L\\\L\\\\\\\\\\L\\L\\\\\\\\\\\\L\L\\\\\\L\\L\L\\\\\\L\L\\\\L\L\\\\\\\L\L\\\\\\\\L\\L\L\L\L\L\L\\\\\\\\\\\\\\\\L\L\L}}}}}}/L/L/L/L\\\\\\\\\\\\\\\\\\\\\\/L\/L}}}}}}}}}}}}}}}/L/L/L/L/L/L/L/L/L/L/L/L/}\\\\\\\\\\\\\\\\\\\\\\\\\\///(((((((((\\\\\\\\\\\}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}/((((((((((((((((((((((((((((
L --~ ~ No~ N[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\t\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/}}}}}}}}}}}}}}}}}}}}}}}}}}}}}/ [((((((((((\\\\\\\\\\\\\\\((((((((\\\\\\\\\\\\\\\\\\\\\\/}}}}}

N --> O[Analysis of problems<br/>Identify underperformance causes]
O -> P [Strategy correction<br/>Adjust allocation, rebalance]
P --> Q[Monitoring changes<br/>Track acquisition]
 Q --> K

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style C fill:#ffcdd2
 style D fill:#fff3e0
 style E fill:#f3e5f5
 style M fill:#4caf50
 style N fill:#ff9800
```

### 1. Metrics performance

```python
def calculate_Portfolio_metrics(returns, risk_free_rate=0.02):
 """
Calculation of the metric performance Portfolio

This Foundation calculates an integrated set of metrics for evaluation
Performance Portfolio, including return, risk
Risk-corrected indicators.

 Parameters:
 -----------
 returns : pandas.Series or array-like, shape (n_periods,)
temporary series of Portfolio returns.
with index dates or numpy.array. data should be in format
(e.g. 0.05 for 5% returns).

 risk_free_rate : float, default=0.02
Risk-free interest rate for calculation of risk-adjusted
normally takes the following values:
0.01: 1 per cent (very low rate)
0.02: 2% (standard value for developed markets)
- 0.03: 3% (moderate rate)
0.05: 5 per cent (high rate)

 Returns:
 --------
 dict
Vocabulary with metrics performance Portfolio:

 total_return : float
Total return for the whole period.
 (1 + returns).prod() - 1

 annual_return : float
Annual rate of return, calculated as
(1 + returns).mean() ** 252 - 1 (estimated 252 trade days)

 volatility : float
Annual volatility (standard deviation of returns).
Calculated as returns.std() * sqrt(252)

 sharpe : float
Sharpe coefficient is the ratio of excess return to risk.
Calculated as (annual_return-risk_free_rate) / volatility

 max_drawdown : float
The maximum draught is the largest drop from peak to minimum.
Negative value where -0.15 means 15 per cent drop

 sortino : float
Sortino coefficient - ratio of excess return to
It takes into account only negative returns.

 calmar : float
Calmara coefficient - ratio of annual return to
Shows a return on the unit of risk.

 Raises:
 -------
 ValueError
If data are empty or incorrect

 Notes:
 ------
Calculation formulas:
 - Total Return: (1 + r₁) * (1 + r₂) * ... * (1 + rₙ) - 1
 - Annual Return: (1 + mean(r))^252 - 1
 - Volatility: std(r) * sqrt(252)
 - Sharpe: (Annual Return - Risk Free Rate) / Volatility
 - Max Drawdown: min((cumprod(1 + r) / cummax(cumprod(1 + r))) - 1)
 - Sortino: (Annual Return - Risk Free Rate) / Downside Volatility
 - Calmar: Annual Return / |Max Drawdown|

Metric interpretation:
- Sharpe > 1.0: Good performance
- Sortino > 1.5: Excellent performance
- Kalmar > 1.0: Good performance
- Max Drawdown < -0.20: High risk
 """
# Basic metrics
 total_return = (1 + returns).prod() - 1
 annual_return = (1 + returns).mean() ** 252 - 1
 volatility = returns.std() * np.sqrt(252)

# Sharpe coefficient
 sharpe = (annual_return - risk_free_rate) / volatility

# Maximum tarmac
 max_drawdown = maximum_drawdown(returns)

# The Sortino coefficient
 downside_returns = returns[returns < 0]
 downside_volatility = downside_returns.std() * np.sqrt(252)
 sortino = (annual_return - risk_free_rate) / downside_volatility if downside_volatility > 0 else 0

# Calmar coefficient
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

# Example of use
metrics = calculate_Portfolio_metrics(Portfolio_returns, risk_free_rate=0.02)
```

♪##2 ♪ Risk analysis

```python
def analyze_Portfolio_risks(returns, confidence_levels=[0.90, 0.95, 0.99]):
""Porthfolio Risk Analysis."
 risks = {}

 for level in confidence_levels:
 # VaR
 var = historical_var(returns, level)

 # ES
 es = expected_shortfall(returns, level)

# Maximum tarmac
 max_dd = maximum_drawdown(returns)

 risks[level] = {
 'var': var,
 'es': es,
 'max_drawdown': max_dd
 }

 return risks

# Example of use
risks = analyze_Portfolio_risks(Portfolio_returns, confidence_levels=[0.90, 0.95, 0.99])
```

### 3, Visualization of Portfolio

```python
def visualize_Portfolio_performance(returns, benchmark_returns=None, save_path=None):
"Visualization of Performance Portfolio"
 import matplotlib.pyplot as plt
 import seaborn as sns

# configuring style
 plt.style.Use('seaborn-v0_8')
 sns.set_palette("husl")

# Create figures
 fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Cumulative returns
 cumulative_returns = (1 + returns).cumprod()
 axes[0, 0].plot(cumulative_returns.index, cumulative_returns.values, label='Portfolio')

 if benchmark_returns is not None:
 benchmark_cumulative = (1 + benchmark_returns).cumprod()
 axes[0, 0].plot(benchmark_cumulative.index, benchmark_cumulative.values,
Label='Benchmark', lineyle='--')

axes[0,0].set_tile('cumulative return')
axes[0,0].set_xlabel('Data')
axes[0,0].set_ylabel('cumulative return')
 axes[0, 0].legend()
 axes[0, 0].grid(True)

♪ 2. Income distribution
 axes[0, 1].hist(returns, bins=50, alpha=0.7, edgecolor='black')
 axes[0, 1].axvline(returns.mean(), color='red', linestyle='--',
Label=f'Medium: {returns.mean(:4f}'
axes[0,1].set_title('distribution of returns')
axes[0,1].set_xlabel('income')
axes[0,1].set_ylabel('Part')
 axes[0, 1].legend()
 axes[0, 1].grid(True)

# 3. Slow down
 cumulative_returns = (1 + returns).cumprod()
 running_max = cumulative_returns.expanding().max()
 drawdown = (cumulative_returns - running_max) / running_max

 axes[1, 0].fill_between(drawdown.index, drawdown.values, 0, alpha=0.3, color='red')
 axes[1, 0].plot(drawdown.index, drawdown.values, color='red')
axes[1, 0].set_title('Prossedka')
axes[1, 0].set_xlabel('Data')
axes[1, 0].set_ylabel('Prossedka')
 axes[1, 0].grid(True)

# 4. Sharpe rolling coefficient
 rolling_sharpe = returns.rolling(252).mean() / returns.rolling(252).std() * np.sqrt(252)
 axes[1, 1].plot(rolling_sharpe.index, rolling_sharpe.values)
 axes[1, 1].axhline(y=1.0, color='red', linestyle='--', label='Sharpe = 1.0')
axes[1, 1].set_title('Slip factor Sharp')
axes[1, 1].set_xlabel('Data')
axes[1, 1].set_ylabel('Sharpa's co-factor')
 axes[1, 1].legend()
 axes[1, 1].grid(True)

 plt.tight_layout()

 if save_path:
 plt.savefig(save_path, dpi=300, bbox_inches='tight')

 plt.show()

# Example of use
visualize_Portfolio_performance(Portfolio_returns, benchmark_returns,
 save_path='Portfolio_performance.png')
```

## Conclusion

Management Portfolio is the basis for successful investment.

1. ** Create stable Portfolio** - reduce volatility and risks
2. ** Optimize returns** - maximize returns at specified risk levels
** Risk management** - control potential losses
4. ** Adapt to changes** - dynamically control Portfolio

### Key principles

1. **Diversification** - not place all eggs in one basket
2. **Manage Risks** - Control VaR and maximum draught
3. ** Rebalance** - regularly adjust the weights
4. **Monitoring** - continuously monitor performance
5. ** Adaptation** - adjust to changing conditions

### Next steps

After mastering Portfolio, you are ready to create full-fledged trading systems that combine:

- [Feature Generation](./26_feature_generation_advanced.md)
- [Becketting](./27_backtesting_methods.md)
- [Walk-forward analysis](./28_walk_forward_Anallysis.md)
- [Monte Carlo simulations](./29_monte_carlo_simulations.md)
- Management Portfolio
