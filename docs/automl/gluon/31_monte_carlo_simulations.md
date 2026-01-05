# In-depth describe Monte carlo - creative and profitable strategies

**Author:** Shcherbyna Rostyslav
**Date:** 2024

# Who Monte Carlo simulations are the key to robotic strategies

### ♪ ♪ The importance of Monte Carlo simulations for the creation of robotic strategies

```mermaid
graph TD
A[ML-Strategy] - • B {Have Monte Carlo been tested?}

B-~ ~ No~ C[95 per cent of strategies fail]
C -> D[~ False confidence in results]
C --> E[~ Unexpected loss in real trade]
C --> F[~ Instable performance]
C --> G[~ time and money]

B -->\\\\H[5% of successful strategies]
H -> I[ ] Coherence on multiple scenarios]
H -> J[~ Management risks and potential losses]
H -> K[~ Optimization of parameters for stability]
H -> L[~ Statistical confidence in results]

I -> M [Texting on 10,000+ scenarios]
J --> N [Essentence to VaR and Spected Shortfall]
K --> O[configration for maximum stability]
L --> P [Confidence intervals and quantiles]

M --> Q [Patching strategy]
 N --> Q
 O --> Q
 P --> Q

Q -> R[~ effective trade in real terms]

 style A fill:#e3f2fd
 style H fill:#c8e6c9
 style C fill:#ffcdd2
 style R fill:#4caf50
```

**Why is 95% of ML strategies failing in real trade?** Because they not have been tested enough on different scenarios. Monte Carlo simulations are the only way to test how your strategy will be Working in thousands of different market conditions.

♪ ♪ What gives Monte Carlo simulations ♪

- **Platitude**: heck strategy on multiple scenarios
- **Manage risk**: Understanding potential losses
** Optimization**: configurization of parameters for maximum stability
- ** Confidence**: Statistical confidence in results

### What happens without Monte Carlo simulations

- **Fast confidence**: The Workinget Strategy only on historical data
- ** Surprising loss**: Real results are worse than expected
- ** Instability**: The Workinget Strategy is unstable
- ** Disappointing**: Loss of time and money

## Monte carlo simulations theory

### Mathematical principles

**Monte carlo as a statistical task:**

```math
P(Strategy_Success) = ∫ P(Success|Parameters, Market_Conditions) × P(Market_Conditions) d(Market_Conditions)
```

Where:

`P(Strategy_Success)' is the probability of strategy success
- `P(Success\Parameters, Market_Conditions)' is the probability of success under specified parameters and market conditions
`P(Market_Conditions)' - distribution of market conditions

**Monte Carlo quality criteria for simulations:**

1. **Statistical significance**: p-value < 0.05
2. ** Economic significance**: Sharpe > 1.0 in 95% of cases
3. **Plativity**: Results are stable on different scenarios
4. **Manage risk**: VaR < 5% in 95% of cases

♪# ♪ Monte carlo types of simulations

*# * * comparison types of Monte Carlo simulations

```mermaid
graph TB
A[Tips Monte Carlo simulations] - • B [Parametric simulations]
A -> C [Non-parametric simulations]
A -> D [Hybrid simulations]
A -> E [Simulation Butstrap]

B -> B1[Use known distributions<br/>Normal, t-distribution, Mixture]
B --> B2[~ Rapid calculations]
B -> B3[. . . . . . . . . . . . . . .
B -> B4[~ Analytical formulae]
B -> B5[~ Simplicity of implementation]

C --> C1 [Use historical data<br/>Bootstrap, Permutation]
C --> C2[~ More realistic]
C --> C3[~ Slow calculation]
C -> C4[ ] Retain the data structure]
C --> C5[\\\\\\t\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\t\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\t\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\t\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

D -> D1 [Combination of parameter and non-parametric<br/>GARCH, Capula]
D -> D2[~ Balance between speed and realistic]
D -> D3[~ Most popular]
D -> D4[~ Intellectual models]
D -> D5[~ Complex implementation]

E --> E1 [Incident sample with return<br/>Block Bootstrap]
E --> E2[
E --> E3[~ Good for time series]
E --> E4[~ Simplicity of understanding]
E -> E5[~ average speed]

 style A fill:#e3f2fd
 style B fill:#ffcdd2
 style C fill:#fff3e0
 style D fill:#c8e6c9
 style E fill:#4caf50
```

#### 1. Parametric simulations

- Use known distributions.
- Quick calculations.
- Requires distribution assumptions

####2 # Non-arametric simulations

- Using historical data
- More realistic.
- Slow calculations.

♪### 3. Hybrid simulations

- Combination of parameter and non-parametric
- Balance between speed and feasibility
- Most popular.

#### 4. Boostrop simulations

- Random sample with return
- Retain the data structure
- Good for the time series.

# The advanced Monte Carlo simulation techniques

### 1.1 Parametric simulations

### ♪ process parameter simulations

```mermaid
graph TD
A [Reference data] -> B [Selection of the type of distribution]
B -> C [Normal distribution]
B -> D[t-distribution]
B -> E [Mixed distributions]

C --> F [Checking of parameters<br/>mean, std]
D --> G[Engine t-distribution <br/>df, loc, scale]
E --> H[GMM<br/>n_components, weights]

F -> I [Initiation of simulations<br/>n_simulations = 10,000]
 G --> I
 H --> I

I -> J [Simulation cycle]
J --> K[Generation of incidental returns<br/>np.random.normal/t.rvs/gmm.sample]

K -> L [Cumulative return calculation<br/>cumprod(1 + returns) - 1]
L -> M [Quality metric calculation]

M --> N[Sharp coefficient<br/>mean/std* sqrt(252)]
M --> O[Maximum draught<br/>calculate_max_drawdown]
M --> P[Total return<br/>cumulative_return]

N -> Q [Save simulation results]
 O --> Q
 P --> Q

Q --> R {All simulations complete?}
R --\\\\\\\\J
R-~\\\S[Statistical analysis of results]

S -> T [Metric distribution]
S --> U [Confidence interval]
S-> V[Quantile and VaR]

T -> W [Priority assessment of strategy]
 U --> W
 V --> W

W --> X {Strategy of Robast?}
X-~ ♪ Yeah ♪ Y[~ Ready to go]
X-~ ~ No ~ Z[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ } } } } } } } } } } } } } } } } } }  } } } } } } } } } } } } } } }

Z -> AA [configration of distribution parameters]
AA --> BB[Return testing]
 BB --> B

 style A fill:#e3f2fd
 style I fill:#fff3e0
 style S fill:#c8e6c9
 style Y fill:#4caf50
 style Z fill:#ff9800
```

**Normal distribution:**

```python
def normal_monte_carlo(returns, n_simulations=10000, time_horizon=252):
 """
Monte Carlo simulation with normal distribution

 Parameters:
 -----------
 returns : array-like
Massive historical returns for distribution.
Shall contain numerical values in decimal format (e.g. 0.01 for 1 per cent).
Minimum length: 30 observations for statistical significance.
Type: numpy.narray, pandas.Serys or List

 n_simulations : int, default=10000
Number of simulations for Monte Carlo Analysis.
Recommended values:
- Minimum: 1000 (for rapid testing)
- Optimal: 10,000 (for balance of accuracy and performance)
- Maximum: 100,000 (for high accuracy but slow)
Impacts on the accuracy of statistical estimates and the time of implementation.

 time_horizon : int, default=252
temporary horizon of simulations in trade days.
Standard values:
252 days = 1 trade year (252 working days)
126 days = 6 months
504 days = 2 years
- 756 days = 3 years
Should be a positive whole number.

 Returns:
 --------
 pd.dataFrame
DataFrame with simulation results containing columns:
- 'cumulative_return': flat - cumulative returns over the period
- 'sharpe': float = Sharp coefficient (annual)
- 'max_drawdown': float = maximum draught (negative)
- 'returns': array - a set of returns for each simulation

 Raises:
 -------
 ValueError
If returns empty or contains non-numerical values
If n_simulations <=0
If time_horizon <=0

 Examples:
 ---------
 >>> import numpy as np
>> returns = np.random.normal(0.001, 0.02, 1000) # 0.1% average return, 2% volatility
 >>> simulations = normal_monte_carlo(returns, n_simulations=5000, time_horizon=252)
>>print(f) Average Sharp coefficient: {simulations['sharpe']mean(: 2f}})
>> preint(f"95% prosediance quintile: {`max_drawdown'] Quantile(0.95:2f}})

 Notes:
 ------
- function assumes that returns follow normal distribution
- Sharp coefficient is calculated as mean/std * sqrt(252) for the annual value
- The maximum draught shall be calculated as the maximum drop from peak
- for more accurate results it is recommended to use >=1000 simulations
 """
# Validation of input parameters
 if len(returns) == 0:
Raise ValueError ("Massive returns not may be empty")

 if not all(isinstance(x, (int, float)) for x in returns):
Raise ValueError("All elements of returns shall be numerical")

 if n_simulations <= 0:
Raise ValueError("n_simulations should be a positive number")

 if time_horizon <= 0:
Raise ValueError("time_horizon must be a positive number")

# Parameters distribution
mean_return = np.mean(returns) # Average return
std_return = np.std(returns, ddof=1) # Standard deviation (unplaced estimate)

# Simulations
 simulations = []
 for i in range(n_simulations):
# Generating random returns from normal distribution
 # loc=mean_return, scale=std_return
 random_returns = np.random.normal(mean_return, std_return, time_horizon)

# Calculation of cumulative return: (1 + r1) * (1 + r2) * * (1 + rn) - 1
 cumulative_return = np.prod(1 + random_returns) - 1

# quality metrics
sharpe = np.mean(random_returns) / np.std(random_returns) * np.sqrt(252) # Annual Sharpe
max_drawdown = calculate_max_drawdown(random_returns) # Maximum draught

 simulations.append({
 'cumulative_return': cumulative_return,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'returns': random_returns
 })

 return pd.dataFrame(simulations)

# example use with detailed parameters
returns = np.random.normal(0.001, 0.02, 1000) # 0.1% average return, 2% volatility
normal_simulations = normal_monte_carlo(
Returns=returns, # Historical data
n_simulations=1000, # 10,000 simulations for high accuracy
Time_horizon = 252 #1 trade year
)
```

** Student t-distribution:**

```python
def t_distribution_monte_carlo(returns, n_simulations=10000, time_horizon=252):
 """
Monte Carlo simulation with t-distribution of the Studiant

Uses t-distribution for profit modelling with heavy tails,
Which is more realistic for financial data versus normal distribution.

 Parameters:
 -----------
 returns : array-like
Massive historical returns for t-distribution parameters.
Shall contain numerical values in decimal format.
Minimum length: 50 observations for reliable assessment of degrees of freedom.
Type: numpy.narray, pandas.Serys or List

 n_simulations : int, default=10000
Number of simulations for Monte Carlo Analysis.
Recommended values:
- Minimum: 1000 (for rapid testing)
- Optimal: 10,000 (for balance of accuracy and performance)
- Maximum: 100,000 (for high accuracy)

 time_horizon : int, default=252
temporary horizon of simulations in trade days.
Standard values:
- 252 days = 1 trade year
126 days = 6 months
504 days = 2 years
Should be a positive whole number.

 Returns:
 --------
 pd.dataFrame
DataFrame with simulation results containing columns:
- 'cumulative_return': flat - cumulative returns over the period
- 'sharpe': float = Sharp coefficient (annual)
- 'max_drawdown': float = maximum draught (negative)
- 'returns': array - a set of returns for each simulation

 Raises:
 -------
 ValueError
If returns empty or contains non-numerical values
If n_simulations <=0
If time_horizon <=0
If not able to match t-distribution to data

 Examples:
 ---------
 >>> import numpy as np
 >>> from scipy import stats
>># Data generation with "hard tails"
 >>> returns = stats.t.rvs(df=3, loc=0.001, scale=0.02, size=1000)
 >>> simulations = t_distribution_monte_carlo(returns, n_simulations=5000, time_horizon=252)
>>print(f) Average Sharp coefficient: {simulations['sharpe']mean(: 2f}})
>>print(f) "Staffs of freedom: {stats.t.fit(returns)[0]:.2f}")

 Notes:
 ------
- t-distribution is better suited for data with extreme values
- Freedom stairs (df) define the "load of tails" of distribution
- When df -> ~ t-distribution approaches normal
- At df < 3 dispersion not defined
- function automatically adds parameters: df, loc, scale
 """
 from scipy import stats

# Validation of input parameters
 if len(returns) == 0:
Raise ValueError ("Massive returns not may be empty")

 if not all(isinstance(x, (int, float)) for x in returns):
Raise ValueError("All elements of returns shall be numerical")

 if n_simulations <= 0:
Raise ValueError("n_simulations should be a positive number")

 if time_horizon <= 0:
Raise ValueError("time_horizon must be a positive number")

 try:
# T-distribution to data
# Returns: df (levels of freedom), loc (shift), scale (scale)
 df, loc, scale = stats.t.fit(returns)

# check the parameters' valitude
 if df <= 0 or scale <= 0:
Raise ValueError("not could match valide t-distribution to data")

 except Exception as e:
Raise ValueError(f "Apparent t-distribution error: {str(e)}")

# Simulations
 simulations = []
 for i in range(n_simulations):
# Generation of random returns from t-distribution
# df - degrees of freedom, loc - medium, scale - standard deviation
 random_returns = stats.t.rvs(df, loc=loc, scale=scale, size=time_horizon)

# Calculation of cumulative returns
 cumulative_return = np.prod(1 + random_returns) - 1

# quality metrics
 sharpe = np.mean(random_returns) / np.std(random_returns) * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(random_returns)

 simulations.append({
 'cumulative_return': cumulative_return,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'returns': random_returns
 })

 return pd.dataFrame(simulations)

# example use with detailed parameters
Returns = np.random.normal(0.001, 0.02, 1000) # Historical data
t_simulations = t_distribution_monte_carlo(
Returns=returns, # Historical data for fitning
n_simulations=1000, # 10,000 simulations
Time_horizon = 252 #1 trade year
)
```

** Mixed distributions:**

```python
def mixture_monte_carlo(returns, n_simulations=10000, time_horizon=252, n_components=3):
 """
Monte Carlo simulation with mixed distributions (Gauussian Mixture Model)

Uses a mixture of several normal distributions for modelling
complex patterns in financial data, including multi-modality and asymmetries.

 Parameters:
 -----------
 returns : array-like
Massive historical returns for mixed distribution.
Shall contain numerical values in decimal format.
Minimum length: 100 observations for reliable evaluation of GMM parameters.
Type: numpy.narray, pandas.Serys or List

 n_simulations : int, default=10000
Number of simulations for Monte Carlo Analysis.
Recommended values:
- Minimum: 1000 (for rapid testing)
- Optimal: 10,000 (for balance of accuracy and performance)
- Maximum: 100,000 (for high accuracy)

 time_horizon : int, default=252
temporary horizon of simulations in trade days.
Standard values:
- 252 days = 1 trade year
126 days = 6 months
504 days = 2 years
Should be a positive whole number.

 n_components : int, default=3
Number of components in mixed distribution.
Recommended values:
- 2: A simple bimodical model (fore/bear market)
- 3: Standard model (bare/side/bear)
4-5: Complex models with multiple modes
- 6+: Very complex models (may lead to retraining)

It affects the complexity of the model and the timing of the fit-in.

 Returns:
 --------
 pd.dataFrame
DataFrame with simulation results containing columns:
- 'cumulative_return': flat - cumulative returns over the period
- 'sharpe': float = Sharp coefficient (annual)
- 'max_drawdown': float = maximum draught (negative)
- 'returns': array - a set of returns for each simulation

 Raises:
 -------
 ValueError
If returns empty or contains non-numerical values
If n_simulations <=0
If time_horizon <=0
If n_components < 1
If not able to bring GMM to the data

 Examples:
 ---------
 >>> import numpy as np
>># Data generation with multimodal distribution
 >>> returns = np.concatenate([
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
... np.random.normal(0.005, 0.005, 500) #Side market
 ... ])
 >>> simulations = mixture_monte_carlo(returns, n_components=3, n_simulations=5000)
>>print(f) Average Sharp coefficient: {simulations['sharpe']mean(: 2f}})
>>print(f "Number of components: 3)"

 Notes:
 ------
- GMM automatically determines the weights and variables of each component
- The model can detect hidden market regimes
- More components = more flexible model, but risk retraining
- Uses the EM algorithm for setting parameters
- Random_state=42 ensures reproducible results
 """
 from sklearn.mixture import GaussianMixture

# Validation of input parameters
 if len(returns) == 0:
Raise ValueError ("Massive returns not may be empty")

 if not all(isinstance(x, (int, float)) for x in returns):
Raise ValueError("All elements of returns shall be numerical")

 if n_simulations <= 0:
Raise ValueError("n_simulations should be a positive number")

 if time_horizon <= 0:
Raise ValueError("time_horizon must be a positive number")

 if n_components < 1:
Raise ValueError("n_components must be >=1)

 try:
# Mixed distribution (Gauussian Mixture Model)
# n_components = number of normal distributions in mixture
# Random_state - for reproducible results
 gmm = GaussianMixture(n_components=n_components, random_state=42)

# Model to data (requires 2D array)
 gmm.fit(returns.reshape(-1, 1))

# Check success
 if not gmm.converged_:
Raise ValueError("GMM nnot combined when data are applied")

 except Exception as e:
Raise ValueError(f "Approved GMM: {str(e)}")

# Simulations
 simulations = []
 for i in range(n_simulations):
#Mixed random income generation
# Sample() returns (samples, labels), take only samples
 random_returns = gmm.sample(time_horizon)[0].flatten()

# Calculation of cumulative returns
 cumulative_return = np.prod(1 + random_returns) - 1

# quality metrics
 sharpe = np.mean(random_returns) / np.std(random_returns) * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(random_returns)

 simulations.append({
 'cumulative_return': cumulative_return,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'returns': random_returns
 })

 return pd.dataFrame(simulations)

# example use with detailed parameters
Returns = np.random.normal(0.001, 0.02, 1000) # Historical data
mixture_simulations = mixture_monte_carlo(
Returns=returns, # Historical data for fitning
n_simulations=1000, # 10,000 simulations
Time_horizon=252, #1 trade year
n_components=3 #3 components (bare/side/bear)
)
```

### 1.2 Non-arametric simulations

### ♪ process non-parametric simulations

```mermaid
graph TD
A [historical data] - • B [Selection of non-parametric simulation method]
B -> C [Boutstrap simulation]
B -> D [Reshift simulations]

C --> E[configuration of the parameters of the butstrap<br/>block_size = 5<br/>n_simulations = 10,000]
D --> F[configuration of conversions<br/>n_simulations = 10,000<br/>time_horizon = 252]

E --> G [Cycle of simulations]
G --> H[create data blocks<br/>block_start = random.randint]
H --> I [Early choice of block<br/>block = data[start:start+size]]
I --> J[add block to sample<br/>bootstrap_returns.extend(block)]

J --> K{Age reached?<br/>len(bootstrap_returs) >=time_horizon}
K--~ No-H
K -->\\\\\L[Strive to the appropriate length <br/>bootstrap_returns[:time_horizon]]

F --> M[shift simulation cycle]
M-> N[Incident data conversion<br/>np.random.permutation(returns)]
N --> O[Track to appropriate length<br/>permuted_returns[:time_horizon]]

L -> P [Quality metric calculation]
 O --> P

P -> Q [cumulative return<br/>cumprod(1 + returns) - 1]
P-> R[Sharp coefficient<br/>mean/std* sqrt(252)]
P --> S[Macial draught<br/>calculate_max_drawdown]

Q -> T [Conservation of results]
 R --> T
 S --> T

T --> U {All simulations complete?}
U-~ * No * G
U-~ * No * M
U-~\\\\V[Analysis of results]

V --> W[comparison with historical data]
V -> X [Evaluability assessment]
V -> Y[Statistical tests]

W -> Z [Quality assessment of simulations]
 X --> Z
 Y --> Z

Z --> AA {Quality simulations?}
AA --\\\\\b [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ for the evaluation of the strategy]
AA --\\\\\c[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/}}}}}/\\\\\\\/}}/}/}/}/}/}/}/}/}/}/====================================================================================================================================================

CC --> DD [change of lock_size]
CC --> EE[change in simulations]
 DD --> G
 EE --> G

 style A fill:#e3f2fd
 style G fill:#fff3e0
 style M fill:#fff3e0
 style V fill:#c8e6c9
 style BB fill:#4caf50
 style CC fill:#ff9800
```

**Simulation button:**

```python
def bootstrap_monte_carlo(returns, n_simulations=10000, time_horizon=252, block_size=5):
 """
Butstrap Monte Carlo Simulation with block sample

Uses a block boot for maintaining the temporial data structure
and autocorrosions in financial time series.

 Parameters:
 -----------
 returns : array-like
Massive historical returns for sample butstrap.
Shall contain numerical values in decimal format.
Minimum length: 100 observations for reliable sample butstrap.
Type: numpy.narray, pandas.Serys or List

 n_simulations : int, default=10000
Number of simulations for Monte Carlo Analysis.
Recommended values:
- Minimum: 1000 (for rapid testing)
- Optimal: 10,000 (for balance of accuracy and performance)
- Maximum: 100,000 (for high accuracy)

 time_horizon : int, default=252
temporary horizon of simulations in trade days.
Standard values:
- 252 days = 1 trade year
126 days = 6 months
504 days = 2 years
Should be a positive whole number.

 block_size : int, default=5
Size of the block for sample boots in trade days.
Recommended values:
- 1: Simple bootstrap (dropped autocorn)
- 3-5: Short blocks (saves short-term auto-coupling)
- 10-20: Medium blocks (balance between structure and flexibility)
- 50+: Long blocks (maintains long-term pavements)

It affects the maintenance of the time structure of the data.

 Returns:
 --------
 pd.dataFrame
DataFrame with simulation results containing columns:
- 'cumulative_return': flat - cumulative returns over the period
- 'sharpe': float = Sharp coefficient (annual)
- 'max_drawdown': float = maximum draught (negative)
- 'returns': array - a set of returns for each simulation

 Raises:
 -------
 ValueError
If returns empty or contains non-numerical values
If n_simulations <=0
If time_horizon <=0
If block_size <=0
If block_size >= Len(returns)

 Examples:
 ---------
 >>> import numpy as np
 >>> returns = np.random.normal(0.001, 0.02, 1000)
 >>> simulations = bootstrap_monte_carlo(
 ... returns,
 ... n_simulations=5000,
 ... time_horizon=252,
 ... block_size=10
 ... )
>>print(f) Average Sharp coefficient: {simulations['sharpe']mean(: 2f}})
>> preint(f" Unit size: 10 days")

 Notes:
 ------
- The Block Boutstrap saves autocorn in data.
- Big block_size better saves the time structure.
- Less block_size gives more variety in the sample.
- The optimal lock_size depends on the nature of the data
- Method n requires assumptions about data distribution
 """
# Validation of input parameters
 if len(returns) == 0:
Raise ValueError ("Massive returns not may be empty")

 if not all(isinstance(x, (int, float)) for x in returns):
Raise ValueError("All elements of returns shall be numerical")

 if n_simulations <= 0:
Raise ValueError("n_simulations should be a positive number")

 if time_horizon <= 0:
Raise ValueError("time_horizon must be a positive number")

 if block_size <= 0:
Raise ValueError("block_size should be a positive number")

 if block_size >= len(returns):
Raise ValueError("block_size should be less than the length of returns")

# Convergence in numpy array for effectiveness
 returns = np.array(returns)

 simulations = []

 for i in range(n_simulations):
♪ the sample booth with blocks ♪
 bootstrap_returns = []

# Generating blocks to reach the desired length
 while len(bootstrap_returns) < time_horizon:
# Random selection of the unit's initial position
# Note that the no block has to go beyond the array
 max_start = len(returns) - block_size
 if max_start < 0:
Raise ValueError("block_size longer than returns")

 block_start = np.random.randint(0, max_start + 1)
 block = returns[block_start:block_start + block_size]
 bootstrap_returns.extend(block)

# Tenderloin to appropriate length
 bootstrap_returns = np.array(bootstrap_returns[:time_horizon])

# Calculation of cumulative returns
 cumulative_return = np.prod(1 + bootstrap_returns) - 1

# quality metrics
 sharpe = np.mean(bootstrap_returns) / np.std(bootstrap_returns) * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(bootstrap_returns)

 simulations.append({
 'cumulative_return': cumulative_return,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'returns': bootstrap_returns
 })

 return pd.dataFrame(simulations)

# example use with detailed parameters
Returns = np.random.normal(0.001, 0.02, 1000) # Historical data
bootstrap_simulations = bootstrap_monte_carlo(
Returns=returns, # Historical data for sample butstrap
n_simulations=1000, # 10,000 simulations
Time_horizon=252, #1 trade year
Block_size=5 # Blocks on 5 days for autocorration preservation
)
```

** Reset simulations:**

```python
def permutation_monte_carlo(returns, n_simulations=10000, time_horizon=252):
 """
The Monte Carlo Reset Simulation

Uses random resets of historical data for creation
Simulations with no distributional assumptions, but lose the temporal structure.

 Parameters:
 -----------
 returns : array-like
Massive historical returns for reshuffling.
Shall contain numerical values in decimal format.
Minimum length: 50 observations for reliable conversion.
Type: numpy.narray, pandas.Serys or List

 n_simulations : int, default=10000
Number of simulations for Monte Carlo Analysis.
Recommended values:
- Minimum: 1000 (for rapid testing)
- Optimal: 10,000 (for balance of accuracy and performance)
- Maximum: 100,000 (for high accuracy)

 time_horizon : int, default=252
temporary horizon of simulations in trade days.
Standard values:
- 252 days = 1 trade year
126 days = 6 months
504 days = 2 years
Should be a positive whole number.
If time_horizon > Len(returns), the entire length of returns is used.

 Returns:
 --------
 pd.dataFrame
DataFrame with simulation results containing columns:
- 'cumulative_return': flat - cumulative returns over the period
- 'sharpe': float = Sharp coefficient (annual)
- 'max_drawdown': float = maximum draught (negative)
- 'returns': array - a set of returns for each simulation

 Raises:
 -------
 ValueError
If returns empty or contains non-numerical values
If n_simulations <=0
If time_horizon <=0

 Examples:
 ---------
 >>> import numpy as np
 >>> returns = np.random.normal(0.001, 0.02, 1000)
 >>> simulations = permutation_monte_carlo(
 ... returns,
 ... n_simulations=5000,
 ... time_horizon=252
 ... )
>>print(f) Average Sharp coefficient: {simulations['sharpe']mean(: 2f}})
>>print(f "Reset length: {len(returns)}")

 Notes:
 ------
- Change completely destroys the time structure of the data
- Maintains empirical income distribution
- not requires assumptions about parameter distribution
- It's good for a random hypothesis test.
- Less realistic for financial data with auto-coordination
 """
# Validation of input parameters
 if len(returns) == 0:
Raise ValueError ("Massive returns not may be empty")

 if not all(isinstance(x, (int, float)) for x in returns):
Raise ValueError("All elements of returns shall be numerical")

 if n_simulations <= 0:
Raise ValueError("n_simulations should be a positive number")

 if time_horizon <= 0:
Raise ValueError("time_horizon must be a positive number")

# Convergence in numpy array for effectiveness
 returns = np.array(returns)

# Determination of actual length for simulation
 actual_horizon = min(time_horizon, len(returns))

 simulations = []

 for i in range(n_simulations):
# Random profit conversion
# np.random.permutation creates random array conversion
 permuted_returns = np.random.permutation(returns)[:actual_horizon]

# Calculation of cumulative returns
 cumulative_return = np.prod(1 + permuted_returns) - 1

# quality metrics
 sharpe = np.mean(permuted_returns) / np.std(permuted_returns) * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(permuted_returns)

 simulations.append({
 'cumulative_return': cumulative_return,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'returns': permuted_returns
 })

 return pd.dataFrame(simulations)

# example use with detailed parameters
Returns = np.random.normal(0.001, 0.02, 1000) # Historical data
permutation_simulations = permutation_monte_carlo(
Returns=returns, # Historical data for conversions
n_simulations=1000, # 10,000 simulations
Time_horizon = 252 #1 trade year (or all length returns)
)
```

### 1.3 Hybrid simulations

### ♪ Architecture hybrid simulations

```mermaid
graph TD
A [historical data] --> B [Hybrid method selection]
B -> C[GARCH simulations]
B --> D[Copula simulations]

C -> E[GarCH model being prepared<br/>arch_model(returns, vol='Garch', p=1, q=1)]
D -> F[Placing of marginal distributions<br/>gaussian_kde(returns)]

E --> G [GARCH_br/>omega, alpha, beta]
F --> H[create copiles<br/>gaussian_popula]

G --> I [GARCH simulation cycle<br/>n_simulations = 10,000]
H --> J [Cycle of Simulations<br/>n_simulations = 10,000]

I -> K[Vulnerability engineering<br/>GARCH(omega, alpha, beta)]
K --> L[Generation of returns<br/>returs = volatility * random_normal]

J --> M[Generation of even variables<br/>uniform_vars = np.random.uniform]
M --> N[Collation conversion<br/>retourns = inverse_cdf(uniform_vars)]

L -> O [Quality metric calculation]
 N --> O

O -> P[cumulative return<br/>cumprod(1 + returns) - 1]
O -> Q[Sharp coefficient<br/>mean/std* sqrt(252)]
O-> R[Macial draught<br/>calculate_max_drawdown]
O -> S [Volatility<br/>rolling_std(returns)]

P -> T [Conservation of results]
 Q --> T
 R --> T
 S --> T

T --> U {All simulations complete?}
U-~ * No * I
U-~ * No * J
U-~\\\\V[Hybrid result analysis]

V --> W[comparison with parameter]
V --> X[comparison with non-parametric]
V -> Y [Simulation quality assessment]

W -> Z [appraising the benefits of the hybrid approach]
 X --> Z
 Y --> Z

Z-> AA {Hybrid approach is effective?}
AA --\\\\\b [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ for strategy]
AA --\\\\\C [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\models model]

CC --> DD[configuring GARCH parameters<br/>p, q, vol]
CC --> EE[configration Copula parameters<br/>marginal distributions]
 DD --> E
 EE --> F

 style A fill:#e3f2fd
 style C fill:#c8e6c9
 style D fill:#fff3e0
 style V fill:#f3e5f5
 style BB fill:#4caf50
 style CC fill:#ff9800
```

**GARCH simulations:**

```python
def garch_monte_carlo(returns, n_simulations=10000, time_horizon=252, p=1, q=1, vol='Garch'):
 """
GARCH Monte carlo simulation

Using the GARCH (Generalized Autoregrassive Conditional Heteroskedasticity) model
for modelling time-changing volatility in financial data.

 Parameters:
 -----------
 returns : array-like
Massive historical returns for the HARCH model.
Shall contain numerical values in decimal format.
Minimum length: 100 observations for a reliable assessment of HARCH parameters.
Type: numpy.narray, pandas.Serys or List

 n_simulations : int, default=10000
Number of simulations for Monte Carlo Analysis.
Recommended values:
- Minimum: 1000 (for rapid testing)
- Optimal: 10,000 (for balance of accuracy and performance)
- Maximum: 100,000 (for high accuracy)

 time_horizon : int, default=252
temporary horizon of simulations in trade days.
Standard values:
- 252 days = 1 trade year
126 days = 6 months
504 days = 2 years
Should be a positive whole number.

 p : int, default=1
Number of ARCH lags (conditional heteroscedity).
Recommended values:
- 1: Standard HARCH(1.1) model
- 2: GARCH(2.1) with additional ARCH lag
- 3+: Complex models (may lead to retraining)

 q : int, default=1
The number of GARCH lags (conditional heteroscedity).
Recommended values:
- 1: Standard HARCH(1.1) model
- 2: GARCH(1.2) with additional GarCH lag
- 3+: Complex models (may lead to retraining)

 vol : str, default='Garch'
Type of volatility model.
Available options:
- 'Garch': Standard GarCH Model
- 'EGARCH': Exponential HARCH (takes into account asymmetries)
 - 'GJR-GARCH': Glosten-Jagannathan-Runkle GARCH
 - 'TGARCH': Threshold GARCH

 Returns:
 --------
 pd.dataFrame
DataFrame with simulation results containing columns:
- 'cumulative_return': flat - cumulative returns over the period
- 'sharpe': float = Sharp coefficient (annual)
- 'max_drawdown': float = maximum draught (negative)
- 'returns': array - a set of returns for each simulation

 Raises:
 -------
 ValueError
If returns empty or contains non-numerical values
If n_simulations <=0
If time_horizon <=0
If p < 0 or q < 0
If not able to match the GARCH model to the data

 Examples:
 ---------
 >>> import numpy as np
 >>> returns = np.random.normal(0.001, 0.02, 1000)
 >>> simulations = garch_monte_carlo(
 ... returns,
 ... n_simulations=5000,
 ... time_horizon=252,
 ... p=1, q=1, vol='Garch'
 ... )
>>print(f) Average Sharp coefficient: {simulations['sharpe']mean(: 2f}})
>>print(f"GARCH model: HARCH(1.1))

 Notes:
 ------
- GARCH models take into account the clustering of volatility
- Parameters p and q determine the complexity of the model
- Large p,q can lead to retraining
- EARCH and GJR-GARCH are better suited for asymmetrical data
- Demands installation of the arch library: pip install arch
 """
 from arch import arch_model

# Validation of input parameters
 if len(returns) == 0:
Raise ValueError ("Massive returns not may be empty")

 if not all(isinstance(x, (int, float)) for x in returns):
Raise ValueError("All elements of returns shall be numerical")

 if n_simulations <= 0:
Raise ValueError("n_simulations should be a positive number")

 if time_horizon <= 0:
Raise ValueError("time_horizon must be a positive number")

 if p < 0 or q < 0:
Raise ValueError("p and q shall be non-negative")

 try:
# GARCH model
# vol - type of volatile model
# p = number of ARCH lags
#q is the amount of HARCH lags
 model = arch_model(returns, vol=vol, p=p, q=q)
Fitted_model = model.fit(disp='off') # Disable the optimization output

# Check success
 if not fitted_model.convergence_flag:
raise ValueError("GARCH model nt connected when adjusted")

 except Exception as e:
Raise ValueError(f "Approved model HARCH: {str(e)}")

# Simulations
 simulations = []
 for i in range(n_simulations):
 try:
# Income generation with GARCH volatility
# method='simulation' uses Monte carlo for forecasting
 simulated_returns = fitted_model.forecast(horizon=time_horizon, method='simulation')

# Retrieving profits from forecasting
# mean contains average projected returns
 random_returns = simulated_returns.mean.iloc[-1].values

# check of the strength of the data generated
 if len(random_returns) != time_horizon:
Raise ValueError

 except Exception as e:
# In case of generation error, Use simple normal distribution
 mean_return = np.mean(returns)
 std_return = np.std(returns)
 random_returns = np.random.normal(mean_return, std_return, time_horizon)

# Calculation of cumulative returns
 cumulative_return = np.prod(1 + random_returns) - 1

# quality metrics
 sharpe = np.mean(random_returns) / np.std(random_returns) * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(random_returns)

 simulations.append({
 'cumulative_return': cumulative_return,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'returns': random_returns
 })

 return pd.dataFrame(simulations)

# example use with detailed parameters
Returns = np.random.normal(0.001, 0.02, 1000) # Historical data
garch_simulations = garch_monte_carlo(
Returns=returns, # Historical data for HARCH
n_simulations=1000, # 10,000 simulations
Time_horizon=252, #1 trade year
p=1, #1 ARCH lag
q=1, #1 GARCH lags
vol='Garch' # Standard GarCH Model
)
```

**Copula simulations:**

```python
def copula_monte_carlo(returns, n_simulations=10000, time_horizon=252, copula_type='gaussian'):
 """
Copula Monte carlo simulation

Using cops for modelling dependencies between variables,
Maintaining marginal distributions and structure of dependencies.

 Parameters:
 -----------
 returns : array-like
A mass of historical returns for a cop.
Shall contain numerical values in decimal format.
Minimum length: 100 observations for a reliable estimate of the coil.
Type: numpy.narray, pandas.Serys or List

 n_simulations : int, default=10000
Number of simulations for Monte Carlo Analysis.
Recommended values:
- Minimum: 1000 (for rapid testing)
- Optimal: 10,000 (for balance of accuracy and performance)
- Maximum: 100,000 (for high accuracy)

 time_horizon : int, default=252
temporary horizon of simulations in trade days.
Standard values:
- 252 days = 1 trade year
126 days = 6 months
504 days = 2 years
Should be a positive whole number.

 copula_type : str, default='gaussian'
Type of copule for modelling dependencies.
Available options:
- 'Gaussian': Gaussov's cop.
- 't': t-coast (tail dependencies)
- 'clayton': Clayton dig.
- 'gumbel': Knuckle gumble.
- 'Frank': Frank's a cop.

 Returns:
 --------
 pd.dataFrame
DataFrame with simulation results containing columns:
- 'cumulative_return': flat - cumulative returns over the period
- 'sharpe': float = Sharp coefficient (annual)
- 'max_drawdown': float = maximum draught (negative)
- 'returns': array - a set of returns for each simulation

 Raises:
 -------
 ValueError
If returns empty or contains non-numerical values
If n_simulations <=0
If time_horizon <=0
If copula_type not supported
If not able to get the cop to the data

 Examples:
 ---------
 >>> import numpy as np
 >>> returns = np.random.normal(0.001, 0.02, 1000)
 >>> simulations = copula_monte_carlo(
 ... returns,
 ... n_simulations=5000,
 ... time_horizon=252,
 ... copula_type='gaussian'
 ... )
>>print(f) Average Sharp coefficient: {simulations['sharpe']mean(: 2f}})
>>print(f) Type: Gaussian)

 Notes:
 ------
- Capules share marginal distributions and dependencies
- The Gaussian cop is suitable for linear dependencies.
- T-asse better simulates tail dependencies.
- Archimedes of the cop (Clayton, Gumbel, Frank) for asymmetric dependencies
- Demands installation of the Scypy Library
 """
 from scipy.stats import gaussian_kde

# Validation of input parameters
 if len(returns) == 0:
Raise ValueError ("Massive returns not may be empty")

 if not all(isinstance(x, (int, float)) for x in returns):
Raise ValueError("All elements of returns shall be numerical")

 if n_simulations <= 0:
Raise ValueError("n_simulations should be a positive number")

 if time_horizon <= 0:
Raise ValueError("time_horizon must be a positive number")

 if copula_type not in ['gaussian', 't', 'clayton', 'gumbel', 'frank']:
Raise ValueError(f "Unsupported type of cop: {copula_type}")

 try:
# Pushing marginal distributions with KDE aid
# Gaussian KDE creates a nonparametric density estimate
 kde = gaussian_kde(returns)

# KDE's check of validity
 if kde.covariance_factor <= 0:
raise ValueError("not has been able to create valide KDE")

 except Exception as e:
Raise ValueError(f "Approved adjustment of marginal distributions: {str(e)}")

# Simulations
 simulations = []
 for i in range(n_simulations):
 try:
#Compulsory profit generation from KDE
# resample() generates random samples from KDE
 random_returns = kde.resample(time_horizon).flatten()

# check of the strength of the data generated
 if len(random_returns) != time_horizon:
Raise ValueError

 except Exception as e:
# In case of generation error, Use simple normal distribution
 mean_return = np.mean(returns)
 std_return = np.std(returns)
 random_returns = np.random.normal(mean_return, std_return, time_horizon)

# Calculation of cumulative returns
 cumulative_return = np.prod(1 + random_returns) - 1

# quality metrics
 sharpe = np.mean(random_returns) / np.std(random_returns) * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(random_returns)

 simulations.append({
 'cumulative_return': cumulative_return,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'returns': random_returns
 })

 return pd.dataFrame(simulations)

# example use with detailed parameters
Returns = np.random.normal(0.001, 0.02, 1000) # Historical data
copula_simulations = copula_monte_carlo(
Returns=returns, # Historical data for collage
n_simulations=1000, # 10,000 simulations
Time_horizon=252, #1 trade year
Copula_type='Gaussian' # Gaussov digs for linear dependencies
)
```

♪##4 ♪ Stress testing ♪

♪# ♪ Stress-test scenarios Monte carlo ♪

```mermaid
graph TD
A [historical data] --> B [Definition of stress scenarios]
B --> C[market collapse<br/>volatility_multiplier: 3.0<br/>return_shift: -0.1]
B -> D[High volatility<br/>volatility_multiplier: 2.0<br/>return_shift: 0.0]
B --> E[Low volatility<br/>volatility_multiplier: 0.5<br/>return_shift: 0.0]
B --> F[Pressual scenarios<br/>n_regimes: 3]

C --> G [Use of stress scenario<br/>strapped_returns = apply_strasse_scenario]
 D --> G
 E --> G
F --> H [Definition of market regimes<br/>GauussianMixture(n_components=3)]

G --> I [ Stress-stimulation cycle<br/>n_simulations = 10,000]
H --> J[Cycle of Mode Simulations<br/>n_simulations = 10,000]

I -> K[Running sample of stress data<br/>np.random.choice(strapped_returns)]
J --> L[Generation of mode sequence<br/>regime_sequence = gmm.sample]
L --> M[Generation of returns for each mode<br/>regime_returns = returns[regime]]

K-> N [Metric calculation for stress scenario]
 M --> N

N -> O[cumulative return<br/>cumprod(1 + returns) - 1]
N --> P[Sharp coefficient<br/>mean/std* sqrt(252)]
N --> Q[Maximum draught<br/>calculate_max_drawdown]
N -> R [The probability of loss<br/>P(return < 0)]

O -> S [Save the results on scenarios]
 P --> S
 Q --> S
 R --> S

S --> T {All simulations complete?}
T-~ No I
T-~ ~ No~ J
T-~ ♪ Yeah ♪ U[ Stress Results Analysis]

U --> V[comparison scenarios<br/>crash vs high_vol vs low_vol vs regulations]
U -> W[Strategy sustainability assessment<br/>performance under page]
U -> X [VaR and ES calculation for each scenario]

V -> Y [Priority assessment of the strategy]
 W --> Y
 X --> Y

Y --> Z {The Strategy is coping with stress?}
Z --\\\\\\A [\\\\Laughing Strategy]
Z--~ ~ No ~ BB[~ Needs to be refined risk management]

BB --> CC[configration of strategy parameters]
BB --> DD[add safeguard mechanisms]
CC-> EE[Re-stress-test]
 DD --> EE
 EE --> B

 style A fill:#e3f2fd
 style C fill:#ffcdd2
 style D fill:#fff3e0
 style E fill:#e8f5e8
 style F fill:#f3e5f5
 style AA fill:#4caf50
 style BB fill:#ff9800
```

** Extreme scenarios:**

```python
def stress_test_monte_carlo(returns, n_simulations=10000, time_horizon=252,
 stress_scenarios=None):
 """
Monte Carlo simulation with stress-testing

Runs Monte Carlo simulations for various stress scenarios
To assess the sustainability of a strategy in extreme market conditions.

 Parameters:
 -----------
 returns : array-like
Massive historical returns for the base scenario.
Shall contain numerical values in decimal format.
Minimum length: 100 observations for reliable assessment.
Type: numpy.narray, pandas.Serys or List

 n_simulations : int, default=10000
Number of simulations for Monte Carlo Analysis.
Recommended values:
- Minimum: 1000 (for rapid testing)
- Optimal: 10,000 (for balance of accuracy and performance)
- Maximum: 100,000 (for high accuracy)

 time_horizon : int, default=252
temporary horizon of simulations in trade days.
Standard values:
- 252 days = 1 trade year
126 days = 6 months
504 days = 2 years
Should be a positive whole number.

 stress_scenarios : dict, optional
Stress scenario dictionary for testing.
If None, standard scenarios are used.

Structure script:
 {
 'scenario_name': {
'volatility_multiplier': float, # Vulnerability multiplier
'return_shift': float, # Average return shift
'Tail_risk_multiplier': float # Tail risk multiplier (optimal)
 }
 }

Standard scenarios:
 - 'market_crash': volatility_multiplier=3.0, return_shift=-0.1
 - 'high_volatility': volatility_multiplier=2.0, return_shift=0.0
 - 'low_volatility': volatility_multiplier=0.5, return_shift=0.0
 - 'extreme_tail': volatility_multiplier=4.0, return_shift=-0.15, tail_risk_multiplier=2.0

 Returns:
 --------
 dict
A dictionary with simulation results for each scenario.
The keys are scenario names, values are pd.dataFrame with results.

Structure dataFrame for each scenario:
- 'cumulative_return': flat - cumulative returns over the period
- 'sharpe': float = Sharp coefficient (annual)
- 'max_drawdown': float = maximum draught (negative)
- 'returns': array - a set of returns for each simulation

 Raises:
 -------
 ValueError
If returns empty or contains non-numerical values
If n_simulations <=0
If time_horizon <=0
If stress_scenarios contain non-dead parameters

 Examples:
 ---------
 >>> import numpy as np
 >>> returns = np.random.normal(0.001, 0.02, 1000)
 >>>
>> # User scenarios
 >>> custom_scenarios = {
 ... 'crash_2008': {'volatility_multiplier': 4.0, 'return_shift': -0.2},
 ... 'covid_2020': {'volatility_multiplier': 3.5, 'return_shift': -0.15}
 ... }
 >>>
 >>> stress_simulations = stress_test_monte_carlo(
 ... returns,
 ... n_simulations=5000,
 ... time_horizon=252,
 ... stress_scenarios=custom_scenarios
 ... )
 >>>
>>print(f) Scenarios: {List(stress_simulations.keys()}})
 >>> print(f"Crash 2008 Sharpe: {stress_simulations['crash_2008']['sharpe'].mean():.2f}")

 Notes:
 ------
- Stress testing helps assess the sustainability of the strategy
- volatility_multiplier > 1 increases volatility
- return_shift < 0 creates a negative yield shift
- Tail_risk_multiplier reinforces extreme events
- It is recommended to test historical crises
 """
# Validation of input parameters
 if len(returns) == 0:
Raise ValueError ("Massive returns not may be empty")

 if not all(isinstance(x, (int, float)) for x in returns):
Raise ValueError("All elements of returns shall be numerical")

 if n_simulations <= 0:
Raise ValueError("n_simulations should be a positive number")

 if time_horizon <= 0:
Raise ValueError("time_horizon must be a positive number")

# Standard stress scenarios
 if stress_scenarios is None:
 stress_scenarios = {
 'market_crash': {
 'volatility_multiplier': 3.0,
 'return_shift': -0.1,
'Describe': 'The market collapse: high volatility, negative returns'
 },
 'high_volatility': {
 'volatility_multiplier': 2.0,
 'return_shift': 0.0,
'Describe': 'High volatility: normal return, increased risk'
 },
 'low_volatility': {
 'volatility_multiplier': 0.5,
 'return_shift': 0.0,
'Describe': 'Low volatility: normal return, reduced risk'
 },
 'extreme_tail': {
 'volatility_multiplier': 4.0,
 'return_shift': -0.15,
 'tail_risk_multiplier': 2.0,
'Describe': 'Extrematic tails: maximum risk and loss'
 }
 }

# validation of scenarios
 for scenario_name, params in stress_scenarios.items():
 if 'volatility_multiplier' not in params or 'return_shift' not in params:
raise ValueError(f"Scenario_name scenario should contain volatility_multiplier and return_shift")

 if params['volatility_multiplier'] <= 0:
raise ValueError(f"volatility_multiplier in scenario {scenario_name} should be positive")

# Convergence in numpy array for effectiveness
 returns = np.array(returns)

 all_simulations = {}

 for scenario_name, scenario_params in stress_scenarios.items():
# Stress scenario application
 stressed_returns = apply_stress_scenario(returns, scenario_params)

# Simulations for the script
 simulations = []
 for i in range(n_simulations):
# Generating random returns from stress data
 random_returns = np.random.choice(stressed_returns, size=time_horizon, replace=True)

# Calculation of cumulative returns
 cumulative_return = np.prod(1 + random_returns) - 1

# quality metrics
 sharpe = np.mean(random_returns) / np.std(random_returns) * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(random_returns)

 simulations.append({
 'cumulative_return': cumulative_return,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'returns': random_returns
 })

 all_simulations[scenario_name] = pd.dataFrame(simulations)

 return all_simulations

def apply_stress_scenario(returns, scenario_params):
 """
Applying the stress scenario to historical data

 Parameters:
 -----------
 returns : array-like
Background historical returns

 scenario_params : dict
Parameters stress scenario:
- volatility_multiplier: float is the factor of volatility
- return_shift: float = shift in average return
- tail_risk_multiplier: flat, optional - tail risk multiplier

 Returns:
 --------
 array
Changed post-stress scenario returns
 """
 returns = np.array(returns)

# Basic parameters
 volatility_multiplier = scenario_params['volatility_multiplier']
 return_shift = scenario_params['return_shift']
 tail_risk_multiplier = scenario_params.get('tail_risk_multiplier', 1.0)

# Application of change in yield
 stressed_returns = returns + return_shift

# Application of the volatility factor
 mean_return = np.mean(stressed_returns)
 stressed_returns = (stressed_returns - mean_return) * volatility_multiplier + mean_return

# Tail risk application (enhance extremes)
 if tail_risk_multiplier > 1.0:
# Found extremes (beyond 2 standard deviations)
 std_return = np.std(stressed_returns)
 extreme_mask = np.abs(stressed_returns - mean_return) > 2 * std_return

# Increase extreme values
 stressed_returns[extreme_mask] = (
 (stressed_returns[extreme_mask] - mean_return) * tail_risk_multiplier + mean_return
 )

 return stressed_returns

# example use with detailed parameters
Returns = np.random.normal(0.001, 0.02, 1000) # Historical data

# User's stress scenarios
custom_scenarios = {
 'financial_crisis_2008': {
 'volatility_multiplier': 4.0,
 'return_shift': -0.2,
 'tail_risk_multiplier': 2.5,
'Describe': 'Financial crisis 2008: Extreme losses and volatility'
 },
 'covid_crash_2020': {
 'volatility_multiplier': 3.5,
 'return_shift': -0.15,
 'tail_risk_multiplier': 2.0,
'Describe': 'COVID-19 crash 2020: rapid and deep losses'
 },
 'dotcom_bubble': {
 'volatility_multiplier': 2.5,
 'return_shift': -0.12,
'Describe': 'Scream of dotcoms: technoLogsy bubble'
 }
}

stress_simulations = stress_test_monte_carlo(
Returns=returns, # Historical data
n_simulations=1000, # 10,000 simulations
Time_horizon=252, #1 trade year
page_scenarios=customer_scenarios # User scenarios
)
```

**Pressed simulations:**

```python
def regime_monte_carlo(returns, n_simulations=10000, time_horizon=252, n_regimes=3):
 """
Monte Carlo simulation with market regimes

Using the Gaussian Mixture Model for the identification of hidden market regimes
and generation of simulations with changes between modes.

 Parameters:
 -----------
 returns : array-like
Massive historical returns to identify regimes.
Shall contain numerical values in decimal format.
Minimum length: 200 observations for reliable identification of modes.
Type: numpy.narray, pandas.Serys or List

 n_simulations : int, default=10000
Number of simulations for Monte Carlo Analysis.
Recommended values:
- Minimum: 1000 (for rapid testing)
- Optimal: 10,000 (for balance of accuracy and performance)
- Maximum: 100,000 (for high accuracy)

 time_horizon : int, default=252
temporary horizon of simulations in trade days.
Standard values:
- 252 days = 1 trade year
126 days = 6 months
504 days = 2 years
Should be a positive whole number.

 n_regimes : int, default=3
Number of market regimes for modelling.
Recommended values:
- 2: A simple model (fore/bear market)
- 3: Standard model (bare/side/bear)
4-5: Complex models with multiple modes
- 6+: Very complex models (may lead to retraining)

It affects the complexity of the model and the interpretation of regimes.

 Returns:
 --------
 pd.dataFrame
DataFrame with simulation results containing columns:
- 'cumulative_return': flat - cumulative returns over the period
- 'sharpe': float = Sharp coefficient (annual)
- 'max_drawdown': float = maximum draught (negative)
- 'returns': array - a set of returns for each simulation
- 'regime_sequence':array is the sequence of modes for each simulation

 Raises:
 -------
 ValueError
If returns empty or contains non-numerical values
If n_simulations <=0
If time_horizon <=0
If n_regimes < 2
If not able to bring GMM to the data

 Examples:
 ---------
 >>> import numpy as np
>># Data generation with different modes
 >>> bull_market = np.random.normal(0.002, 0.01, 300)
 >>> bear_market = np.random.normal(-0.001, 0.015, 200)
 >>> sideways = np.random.normal(0.0005, 0.005, 500)
 >>> returns = np.concatenate([bull_market, bear_market, sideways])
 >>>
 >>> simulations = regime_monte_carlo(
 ... returns,
 ... n_simulations=5000,
 ... time_horizon=252,
 ... n_regimes=3
 ... )
>>print(f) Average Sharp coefficient: {simulations['sharpe']mean(: 2f}})
>>print(f "Number of modes: 3)"

 Notes:
 ------
- GMM automatically identifies hidden modes in data
- Each regime is characterized by its distribution of income
- Regimes can be interpreted as market conditions
- More modes = more flexible model, but risk retraining
- Random_state=42 ensures reproducible results
 """
 from sklearn.mixture import GaussianMixture

# Validation of input parameters
 if len(returns) == 0:
Raise ValueError ("Massive returns not may be empty")

 if not all(isinstance(x, (int, float)) for x in returns):
Raise ValueError("All elements of returns shall be numerical")

 if n_simulations <= 0:
Raise ValueError("n_simulations should be a positive number")

 if time_horizon <= 0:
Raise ValueError("time_horizon must be a positive number")

 if n_regimes < 2:
Raise ValueError("n_regimes must be >=2")

 try:
# Defining modes with the help of Gaussian Mixture Model
# n_components is the number of modes
# Random_state - for reproducible results
 gmm = GaussianMixture(n_components=n_regimes, random_state=42)

# Model to data (requires 2D array)
 gmm.fit(returns.reshape(-1, 1))

# Check success
 if not gmm.converged_:
Raise ValueError("GMM nnot combined when data are applied")

 except Exception as e:
Raise ValueError(f "Approved GMM: {str(e)}")

# Convergence in numpy array for effectiveness
 returns = np.array(returns)

# Preliminary definition of regimes for historical data
 historical_regimes = gmm.predict(returns.reshape(-1, 1)).flatten()

# Simulations
 simulations = []
 for i in range(n_simulations):
# Mode sequence generation
# Sample() returns (samples, labels), take only labels
 regime_sequence = gmm.sample(time_horizon)[1].flatten()

# Income generation for each regime
 random_returns = []
 for regime in regime_sequence:
# We find historical returns for this regime
 regime_returns = returns[historical_regimes == regime]

 if len(regime_returns) > 0:
# A random sample of the regime's profits
 random_returns.append(np.random.choice(regime_returns))
 else:
# If mode no met in historical data, Use total sample
 random_returns.append(np.random.choice(returns))

 random_returns = np.array(random_returns)

# Calculation of cumulative returns
 cumulative_return = np.prod(1 + random_returns) - 1

# quality metrics
 sharpe = np.mean(random_returns) / np.std(random_returns) * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(random_returns)

 simulations.append({
 'cumulative_return': cumulative_return,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'returns': random_returns,
 'regime_sequence': regime_sequence
 })

 return pd.dataFrame(simulations)

# example use with detailed parameters
Returns = np.random.normal(0.001, 0.02, 1000) # Historical data
regime_simulations = regime_monte_carlo(
Returns=returns, # Historical data for the identification of regimes
n_simulations=1000, # 10,000 simulations
Time_horizon=252, #1 trade year
n_regimes=3 #3 modes (bare/side/bear)
)
```

## Metrics quality Monte Carlo simulations

### ♪ The Monte Carlo Quarter of Simulations

```mermaid
graph TD
A[Metrics of quality Monte Carlo] --> B [Statistical metrics]
A-> C[Risk-metrics]
A --> D [Economic metrics]

B -> B1 [Distribution of results]
B1 --> B11 [average <br/>mean_sharpe]
B1 --> B12 [standard deviation<br/>std_sharpe]
B1 --> B13 [Media<br/>median_sharpe]
B1 --> B14 [Quantiles<br/>q5, q25, q75, q95]
B1 --> B15 [Optional factor<br/>std/mean]
B1 --> B16 [Asymmetry and Excess<br/>skewness, kurtosis]

B --> B2 [Confidence interval]
B2 --> B21[90 per cent confidence interval<br/>alpha = 0.1]
B2 -> B22[95% confidence interval<br/>alpha = 0.05]
B2 --> B23[99% confidence interval<br/>alpha = 0.01]
B2 --> B24[t-distribution<br/>t.ppf(1-alpha/2, n-1)]

 C --> C1[Value at Risk - VaR]
 C1 --> C11[VaR 90%<br/>quantile(0.1)]
 C1 --> C12[VaR 95%<br/>quantile(0.05)]
 C1 --> C13[VaR 99%<br/>quantile(0.01)]
C1 --> C14[VAR for Sharp coefficient<br/>sharpe_var]
C1-> C15[VAR for maximum draught<br/>drawdown_var]
C1 --> C16 [VAR for cumulative returns<br/>return_var]

 C --> C2[Expected Shortfall - ES]
 C2 --> C21[ES 90%<br/>mean(returns <= VaR_90)]
 C2 --> C22[ES 95%<br/>mean(returns <= VaR_95)]
 C2 --> C23[ES 99%<br/>mean(returns <= VaR_99)]
C2 --> C24[ES for Sharp coefficient<br/>sharpe_es]
C2 --> C25[ES for maximum draught<br/>drawdown_es]
C2 --> C26[ES for cumulative returns<br/>return_es]

D -> D1 [Approbability of success]
D1 --> D11 [Function conditions<br/>sharpe >=1.0 AND drawdown >= -0.2]
D1 -> D12 [Success probability<br/>access_condition.mean()]
D1-> D13 [Number of successful simulations<br/>n_accessfulful]
D1 --> D14 [Medical metrics for success<br/>avg_sharpe, avg_drawdown, avg_return]

D -> D2 [Recentness]
D2 --> D21 [The actual value of the portfolio<br/>initial_capital * (1 + cumulative_return)]
D2 --> D22 [average final cost<br/>mean_final_value]
D2 --> D23 [Mediant final cost<br/>median_final_value]
D2 --> D24 [final value quantiles<br/>q5_final_value, q95_final_value]
D2 -> D25 [The probability of loss<br/>P(final_value < initial_capital)]
D2 -> D26 [Approbability of significant losses<br/>P(final_value < 0.5 * initial_capital)]

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style C fill:#fff3e0
 style D fill:#f3e5f5
```

♪##1 ♪ Statistical metrics

** Results distribution:**

```python
def calculate_distribution_metrics(simulations, metrics=['sharpe', 'max_drawdown', 'cumulative_return']):
 """
Calculation of distribution metric for Monte Carlo simulations

Computes statistical characteristics of the distribution of results
Simulations for assessing the quality and sustainability of the strategy.

 Parameters:
 -----------
 simulations : pd.dataFrame
DataFrame with Monte Carlo simulations.
Should contain columns with metrics for Analysis.
Mandatory columns: 'sharpe', 'max_drawdown', 'cumulative_return'

 metrics : List, default=['sharpe', 'max_drawdown', 'cumulative_return']
List metric for calculation of distribution statistics.
Available metrics:
- 'sharpe': Sharpe coefficient
- 'max_drawdown': Maximum draught
- 'Cumulative_return': Cumulative return
- 'volatility': Volatility (if available)
- 'calmar': Calmar coefficient (if available return and drawdown)

 Returns:
 --------
 dict
A dictionary with distribution metrics for each specific metrics.
 Structure: {metric_name: {statistic_name: value}}

Statistics for each metrics:
- 'mean': Average
- 'std': Standard deviation
- 'median':
- 'q5', 'q25', 'q75', 'q95': Quantiles (5%, 25%, 75%, 75%)
'Co-officent_of_variation': The coefficient of variation (std/mean)
- 'skewness': Asymmetry (skewness)
- 'curtosis': Excess (curtosis)
- 'min', 'max': Minimum and maximum values

 Raises:
 -------
 ValueError
If simulations empty or not contain the necessary columns
If the metrics contain non-existent metrics
If all metrics are equal (std = 0)

 Examples:
 ---------
 >>> import pandas as pd
 >>> import numpy as np
 >>>
>>#free test data
 >>> simulations = pd.dataFrame({
 ... 'sharpe': np.random.normal(1.0, 0.3, 1000),
 ... 'max_drawdown': np.random.normal(-0.1, 0.05, 1000),
 ... 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
 ... })
 >>>
>># Calculation of metrics for all standard metrics
 >>> metrics = calculate_distribution_metrics(simulations)
>>print(f "Medial Sharpe: {metrics['sharpe']['mean':2f}}")
>>print(f"95% prosediance quintile: {metrics['max_drawdown']['q95':2f}})
 >>>
>># Calculation of metric only for Sharpe
 >>> sharpe_metrics = calculate_distribution_metrics(simulations, metrics=['sharpe'])
>>print(f"Asymmetry Sharpe: {sharpe_metrics['sharpe']['skewness':2f}})

 Notes:
 ------
- The coefficient of variation indicates relative variability
- Asymmetry > 0 means right-hand distribution
Excess > 3 means heavy tails (more extreme values)
Quantiles help assess risks on different levels of trust
 """
# Validation of input parameters
 if simulations.empty:
Raise ValueError ("dataFrame simulations not may be empty")

 if not isinstance(simulations, pd.dataFrame):
Raise ValueError("simulations must be pandas dataFrame")

# Check availability of requered columns
 available_metrics = simulations.columns.toList()
 Missing_metrics = [m for m in metrics if m not in available_metrics]
 if Missing_metrics:
Raise ValueError(f"Missing metrics: {Missing_metrics}. Available: {Available_metrics})

# Calidation metric
 valid_metrics = ['sharpe', 'max_drawdown', 'cumulative_return', 'volatility', 'calmar']
 invalid_metrics = [m for m in metrics if m not in valid_metrics]
 if invalid_metrics:
Raise ValueError(f "Unsupported metrics: {invalid_metrics}. Supported: {valid_metrics})

 results = {}

 for metric in metrics:
 if metric not in simulations.columns:
 continue

Data = simulations [metric]. dropna() # Remove NaN values

 if len(data) == 0:
Raise ValueError(f "No data for metrics {metric}")

# Basic statistics
 mean_val = data.mean()
 std_val = data.std()
 median_val = data.median()

# Quantile
 q5 = data.quantile(0.05)
 q25 = data.quantile(0.25)
 q75 = data.quantile(0.75)
 q95 = data.quantile(0.95)

# The coefficient of variation
 cv = std_val / abs(mean_val) if mean_val != 0 else 0

# Asymmetry and Excess
 skewness = data.skew()
 kurtosis = data.kurtosis()

# Minimum and maximum
 min_val = data.min()
 max_val = data.max()

 results[metric] = {
 'mean': mean_val,
 'std': std_val,
 'median': median_val,
 'q5': q5,
 'q25': q25,
 'q75': q75,
 'q95': q95,
 'coefficient_of_variation': cv,
 'skewness': skewness,
 'kurtosis': kurtosis,
 'min': min_val,
 'max': max_val,
 'count': len(data)
 }

 return results

# example use with detailed parameters
simulations = pd.dataFrame({
 'sharpe': np.random.normal(1.0, 0.3, 1000),
 'max_drawdown': np.random.normal(-0.1, 0.05, 1000),
 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
})

# Calculation of metrics for all standard metrics
distribution_metrics = calculate_distribution_metrics(
Simulations=simulations, # DataFrame with simulation results
 metrics=['sharpe', 'max_drawdown', 'cumulative_return'] # metrics for Analysis
)
```

** Confidence interval:**

```python
def calculate_confidence_intervals(simulations, confidence_levels=[0.90, 0.95, 0.99],
 metrics=['sharpe', 'max_drawdown', 'cumulative_return']):
 """
Calculation of confidence intervals for Monte Carlo simulations

Computes confidence intervals for different metrics on base
The results of Monte Carlo simulations for uncertainty assessment.

 Parameters:
 -----------
 simulations : pd.dataFrame
DataFrame with Monte Carlo simulations.
Should contain columns with metrics for Analysis.
Mandatory columns: 'sharpe', 'max_drawdown', 'cumulative_return'

 confidence_levels : List, default=[0.90, 0.95, 0.99]
List of confidence levels for the calculation of intervals.
Recommended values:
0.90: 90% confidence interval (α = 0.10)
0.95: 95 per cent confidence interval (α = 0.05) - standard
0.99: 99 per cent confidence interval (α = 0.01) - conservative
0.50: 50% confidence interval (interquartile width)

All values shall be in range (0,1).

 metrics : List, default=['sharpe', 'max_drawdown', 'cumulative_return']
List metric for the calculation of confidence intervals.
Available metrics:
- 'sharpe': Sharpe coefficient
- 'max_drawdown': Maximum draught
- 'Cumulative_return': Cumulative return
- 'volatility': Volatility (if available)
- 'calmar': Calmar coefficient (if avalable)

 Returns:
 --------
 dict
A dictionary with confidence intervals for each matrix and level of trust.
 Structure: {confidence_level: {metric: {'lower': value, 'upper': value}}}

for each combination level_methric confidence:
- 'lower': Lower confidence interval
- 'upper': Upper limit of confidence interval
- 'width': The width of the interval (upper-lower)
- 'center': Centre of interval ((upper + lower) / 2)

 Raises:
 -------
 ValueError
If simulations empty or not contain the necessary columns
If confidence_levels contains non-dual values
If the metrics contain non-existent metrics
If no data are available for the calculation of intervals

 Examples:
 ---------
 >>> import pandas as pd
 >>> import numpy as np
 >>>
>>#free test data
 >>> simulations = pd.dataFrame({
 ... 'sharpe': np.random.normal(1.0, 0.3, 1000),
 ... 'max_drawdown': np.random.normal(-0.1, 0.05, 1000),
 ... 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
 ... })
 >>>
>># Standard confidence intervals
 >>> intervals = calculate_confidence_intervals(simulations)
 >>> print(f"95% CI for Sharpe: {intervals[0.95]['sharpe']['lower']:.2f} - {intervals[0.95]['sharpe']['upper']:.2f}")
 >>>
>> # User confidence levels
 >>> custom_intervals = calculate_confidence_intervals(
 ... simulations,
 ... confidence_levels=[0.80, 0.95, 0.99],
 ... metrics=['sharpe', 'cumulative_return']
 ... )
>>print(f"80% CI width: {custom_intervals[0.80]['sharpe']['width':.2f}})

 Notes:
 ------
- Trust intervals show a range in which with a given probability
is the true value of metrics
- Broader intervals indicate greater uncertainty.
95 per cent interval means that in 95 per cent of cases the true value will be in this range
- for one-way intervals of the Use Quantile directly
 """
# Validation of input parameters
 if simulations.empty:
Raise ValueError ("dataFrame simulations not may be empty")

 if not isinstance(simulations, pd.dataFrame):
Raise ValueError("simulations must be pandas dataFrame")

# Calidation of confidence levels
 for level in confidence_levels:
 if not (0 < level < 1):
Raise ValueError(f "Confidence level {level} shall be in range (0,1)")

# Check availability of requered columns
 available_metrics = simulations.columns.toList()
 Missing_metrics = [m for m in metrics if m not in available_metrics]
 if Missing_metrics:
Raise ValueError(f"Missing metrics: {Missing_metrics}. Available: {Available_metrics})

# Calidation metric
 valid_metrics = ['sharpe', 'max_drawdown', 'cumulative_return', 'volatility', 'calmar']
 invalid_metrics = [m for m in metrics if m not in valid_metrics]
 if invalid_metrics:
Raise ValueError(f "Unsupported metrics: {invalid_metrics}. Supported: {valid_metrics})

 confidence_intervals = {}

 for level in confidence_levels:
 alpha = 1 - level
 lower_percentile = (alpha / 2) * 100
 upper_percentile = (1 - alpha / 2) * 100

 level_intervals = {}

 for metric in metrics:
 if metric not in simulations.columns:
 continue

 data = simulations[metric].dropna()

 if len(data) == 0:
Raise ValueError(f "No data for metrics {metric}")

# Quantile calculation for confidence interval
 lower_bound = data.quantile(lower_percentile / 100)
 upper_bound = data.quantile(upper_percentile / 100)

# Additional characteristics of the interval
 width = upper_bound - lower_bound
 center = (upper_bound + lower_bound) / 2

 level_intervals[metric] = {
 'lower': lower_bound,
 'upper': upper_bound,
 'width': width,
 'center': center,
 'level': level,
 'alpha': alpha
 }

 confidence_intervals[level] = level_intervals

 return confidence_intervals

# example use with detailed parameters
simulations = pd.dataFrame({
 'sharpe': np.random.normal(1.0, 0.3, 1000),
 'max_drawdown': np.random.normal(-0.1, 0.05, 1000),
 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
})

# Standard confidence intervals
confidence_intervals = calculate_confidence_intervals(
Simulations=simulations, # DataFrame with simulation results
confidence_levels=[0.90, 0.95, 0.99], #Confidence levels
 metrics=['sharpe', 'max_drawdown', 'cumulative_return'] # metrics for Analysis
)
```

♪##2 ♪ Risk-metrics ♪

**Value at Risk (VaR):**

```python
def calculate_var_metrics(simulations, confidence_levels=[0.90, 0.95, 0.99],
 metrics=['sharpe', 'max_drawdown', 'cumulative_return']):
 """
Calculation of Value at Risk (VAR) metric for Monte Carlo simulations

Computes Value at Risk for various metrics on base results
Monte Carlo simulations for estimating potential losses.

 Parameters:
 -----------
 simulations : pd.dataFrame
DataFrame with Monte Carlo simulations.
Should contain columns with metrics for Analysis.
Mandatory columns: 'sharpe', 'max_drawdown', 'cumulative_return'

 confidence_levels : List, default=[0.90, 0.95, 0.99]
List of confidence levels for calculation of VaR.
Recommended values:
0.90: VaR 90% (10% probability of exceedance)
- 0.95: VaR 95 per cent (5 per cent probability of exceedance) - standard
- 0.99: VaR 99 per cent (1 per cent probability of exceedance) conservative
- 0.999: VaR 99.9 per cent (0.1 per cent probability of exceedance) - extreme

All values shall be in range (0,1).

 metrics : List, default=['sharpe', 'max_drawdown', 'cumulative_return']
List metric for calculation of VaR.
Available metrics:
- 'sharpe': Sharpe coefficient (VAR shows the worst expected Sharpe)
- 'max_drawdown': Maximum draught (VaR shows the worst expected draught)
- 'Cumulative_return': Cumulative return (VaR shows the worst expected return)
- 'volatility': Volatility (if available)
- 'calmar': Calmar coefficient (if avalable)

 Returns:
 --------
 dict
A dictionary with VaR metrics for each matrix and level of trust.
 Structure: {confidence_level: {metric: var_value}}

for each combination level_methric confidence:
- VaR value (Quantile (1 - Conference_level))
- In addition: 'var_absolute' is the absolute value of VaR
- In addition: 'exceedance_prob' - probability of exceeding VaR

 Raises:
 -------
 ValueError
If simulations empty or not contain the necessary columns
If confidence_levels contains non-dual values
If the metrics contain non-existent metrics
If no data are available for calculation of VaR

 Examples:
 ---------
 >>> import pandas as pd
 >>> import numpy as np
 >>>
>>#free test data
 >>> simulations = pd.dataFrame({
 ... 'sharpe': np.random.normal(1.0, 0.3, 1000),
 ... 'max_drawdown': np.random.normal(-0.1, 0.05, 1000),
 ... 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
 ... })
 >>>
>># Standard VaR metrics
 >>> var_metrics = calculate_var_metrics(simulations)
 >>> print(f"VaR 95% for Sharpe: {var_metrics[0.95]['sharpe']:.2f}")
>>print(f"VaR 95 per cent for tare: {var_metrics[.95]['max_drawdown']:.2f})
 >>>
>> # User confidence levels
 >>> custom_var = calculate_var_metrics(
 ... simulations,
 ... confidence_levels=[0.80, 0.95, 0.99],
 ... metrics=['sharpe', 'cumulative_return']
 ... )
>> preint(f"VAR 80 per cent for return: {custom_var[0.80]['cumulative_return']:.2f})

 Notes:
 ------
- VaR shows the maximum expected loss with the intended probability
- for return: VaR 95 per cent = quintile 5 per cent (worst 5 per cent scenarios)
- for tare: VaR 95 per cent = quintile 5 per cent (worst 5 per cent)
- for Sharpe: VaR 95 per cent = quintile 5 per cent (worst 5 per cent of Sharp coefficients)
- VaR note takes into account the amount of losses outside Quantile (Use ES)
 """
# Validation of input parameters
 if simulations.empty:
Raise ValueError ("dataFrame simulations not may be empty")

 if not isinstance(simulations, pd.dataFrame):
Raise ValueError("simulations must be pandas dataFrame")

# Calidation of confidence levels
 for level in confidence_levels:
 if not (0 < level < 1):
Raise ValueError(f "Confidence level {level} shall be in range (0,1)")

# Check availability of requered columns
 available_metrics = simulations.columns.toList()
 Missing_metrics = [m for m in metrics if m not in available_metrics]
 if Missing_metrics:
Raise ValueError(f"Missing metrics: {Missing_metrics}. Available: {Available_metrics})

# Calidation metric
 valid_metrics = ['sharpe', 'max_drawdown', 'cumulative_return', 'volatility', 'calmar']
 invalid_metrics = [m for m in metrics if m not in valid_metrics]
 if invalid_metrics:
Raise ValueError(f "Unsupported metrics: {invalid_metrics}. Supported: {valid_metrics})

 var_metrics = {}

 for level in confidence_levels:
# VaR is calculated as quintile (1 - conference_level)
 var_percentile = (1 - level) * 100

 level_var = {}

 for metric in metrics:
 if metric not in simulations.columns:
 continue

 data = simulations[metric].dropna()

 if len(data) == 0:
Raise ValueError(f "No data for metrics {metric}")

# Calculation of VaR as Quantile
 var_value = data.quantile(var_percentile / 100)

# Additional characteristics
 var_absolute = abs(var_value)
 exceedance_prob = (data <= var_value).mean()

 level_var[metric] = {
 'var': var_value,
 'var_absolute': var_absolute,
 'exceedance_prob': exceedance_prob,
 'confidence_level': level,
 'percentile': var_percentile
 }

 var_metrics[level] = level_var

 return var_metrics

# example use with detailed parameters
simulations = pd.dataFrame({
 'sharpe': np.random.normal(1.0, 0.3, 1000),
 'max_drawdown': np.random.normal(-0.1, 0.05, 1000),
 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
})

# Standard VaR metrics
var_metrics = calculate_var_metrics(
Simulations=simulations, # DataFrame with simulation results
confidence_levels=[0.90, 0.95, 0.99], #Confidence levels
 metrics=['sharpe', 'max_drawdown', 'cumulative_return'] # metrics for Analysis
)
```

**Expected Shortfall (ES):**

```python
def calculate_es_metrics(simulations, confidence_levels=[0.90, 0.95, 0.99],
 metrics=['sharpe', 'max_drawdown', 'cumulative_return']):
 """
Calculation of Spected Shortfall (ES) metric for Monte Carlo simulations

Computes Advanced Shortfall (Conditional Value at Risk, CVAR)
metric on baseline results of Monte Carlo simulations for estimating expected losses
In extreme scenarios.

 Parameters:
 -----------
 simulations : pd.dataFrame
DataFrame with Monte Carlo simulations.
Should contain columns with metrics for Analysis.
Mandatory columns: 'sharpe', 'max_drawdown', 'cumulative_return'

 confidence_levels : List, default=[0.90, 0.95, 0.99]
List of confidence levels for the calculation of ES.
Recommended values:
- 0.90: ES 90% (average in the worst 10% scenarios)
- 0.95: ES 95 per cent (average in the worst 5 per cent scenarios) - standard
- 0.99: ES 99% (average in the worst 1% scenarios) - conservative
- 0.999: ES 99.9 per cent (average in the worst 0.1 per cent scenarios) - Extreme

All values shall be in range (0,1).

 metrics : List, default=['sharpe', 'max_drawdown', 'cumulative_return']
List metric for the calculation of ES.
Available metrics:
- 'sharpe': Sharpe coefficient (ES shows average Sharpe in worst scenarios)
- 'max_drawdown': Maximum draught (ES shows average draught in worst scenarios)
- 'cumulative_return': Cumulative returns (ES shows average returns in worst scenarios)
- 'volatility': Volatility (if available)
- 'calmar': Calmar coefficient (if avalable)

 Returns:
 --------
 dict
A dictionary with ES metrics for each matrix and level of trust.
 Structure: {confidence_level: {metric: es_value}}

for each combination level_methric confidence:
- ES value (average value in worst scenarios)
- In addition: 'es_absolute' is the absolute value of ES
- Additional: `Tail_account' - number of observations in tail
- In addition: 'Tail_probability' is the probability of getting into the tail.

 Raises:
 -------
 ValueError
If simulations empty or not contain the necessary columns
If confidence_levels contains non-dual values
If the metrics contain non-existent metrics
If no data are available for the calculation of ES

 Examples:
 ---------
 >>> import pandas as pd
 >>> import numpy as np
 >>>
>>#free test data
 >>> simulations = pd.dataFrame({
 ... 'sharpe': np.random.normal(1.0, 0.3, 1000),
 ... 'max_drawdown': np.random.normal(-0.1, 0.05, 1000),
 ... 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
 ... })
 >>>
>># Standard ES metrics
 >>> es_metrics = calculate_es_metrics(simulations)
 >>> print(f"ES 95% for Sharpe: {es_metrics[0.95]['sharpe']:.2f}")
>>print(f"ES 95 per cent for sediment: {es_metrics[.95]['max_drawdown']:.2f})
 >>>
>> # User confidence levels
 >>> custom_es = calculate_es_metrics(
 ... simulations,
 ... confidence_levels=[0.80, 0.95, 0.99],
 ... metrics=['sharpe', 'cumulative_return']
 ... )
>>print(f"ES 80 per cent for return: {system_es[0.80]['cumulative_return']:.2f})

 Notes:
 ------
- ES (Expected Shortfall) shows expected value in worst scenarios
- ES is always more or equal to VaR for the same level of trust.
- ES takes into account the amount of losses outside VaR (in contrast from Var)
- ES a more conservative risk measure than VaR
- ES is used in regulatory requirements (Basel III, Solvency II)
 """
# Validation of input parameters
 if simulations.empty:
Raise ValueError ("dataFrame simulations not may be empty")

 if not isinstance(simulations, pd.dataFrame):
Raise ValueError("simulations must be pandas dataFrame")

# Calidation of confidence levels
 for level in confidence_levels:
 if not (0 < level < 1):
Raise ValueError(f "Confidence level {level} shall be in range (0,1)")

# Check availability of requered columns
 available_metrics = simulations.columns.toList()
 Missing_metrics = [m for m in metrics if m not in available_metrics]
 if Missing_metrics:
Raise ValueError(f"Missing metrics: {Missing_metrics}. Available: {Available_metrics})

# Calidation metric
 valid_metrics = ['sharpe', 'max_drawdown', 'cumulative_return', 'volatility', 'calmar']
 invalid_metrics = [m for m in metrics if m not in valid_metrics]
 if invalid_metrics:
Raise ValueError(f "Unsupported metrics: {invalid_metrics}. Supported: {valid_metrics})

 es_metrics = {}

 for level in confidence_levels:
# ES is calculated as the average value in the worst scenarios (1 - conference_level)
 tail_probability = 1 - level

 level_es = {}

 for metric in metrics:
 if metric not in simulations.columns:
 continue

 data = simulations[metric].dropna()

 if len(data) == 0:
Raise ValueError(f "No data for metrics {metric}")

# Definition of the threshold for distribution tail
 threshold = data.quantile(tail_probability)

# We find observations in the tail (the worst scenarios)
 tail_data = data[data <= threshold]

 if len(tail_data) == 0:
# If there are no observations in the tail, Use minimum value
 es_value = data.min()
 tail_count = 1
 else:
# ES as average in tail
 es_value = tail_data.mean()
 tail_count = len(tail_data)

# Additional characteristics
 es_absolute = abs(es_value)
 actual_tail_prob = tail_count / len(data)

 level_es[metric] = {
 'es': es_value,
 'es_absolute': es_absolute,
 'tail_count': tail_count,
 'tail_probability': actual_tail_prob,
 'threshold': threshold,
 'confidence_level': level
 }

 es_metrics[level] = level_es

 return es_metrics

# example use with detailed parameters
simulations = pd.dataFrame({
 'sharpe': np.random.normal(1.0, 0.3, 1000),
 'max_drawdown': np.random.normal(-0.1, 0.05, 1000),
 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
})

# Standard ES metrics
es_metrics = calculate_es_metrics(
Simulations=simulations, # DataFrame with simulation results
confidence_levels=[0.90, 0.95, 0.99], #Confidence levels
 metrics=['sharpe', 'max_drawdown', 'cumulative_return'] # metrics for Analysis
)
```

♪## 3. Economic metrics

** The probability of success:**

```python
def calculate_success_probability(simulations, min_sharpe=1.0, max_drawdown=-0.2,
 min_return=0.0, max_volatility=0.3, custom_conditions=None):
 """
Calculation of the probability of success for Monte Carlo simulations

Calculates the probability that the strategy will be successful on base
The quality criteria and simulation results.

 Parameters:
 -----------
 simulations : pd.dataFrame
DataFrame with Monte Carlo simulations.
Should contain columns: 'sharpe', 'max_drawdown', 'cumulative_return'

 min_sharpe : float, default=1.0
Minimum Sharpe coefficient for successful strategy.
Recommended values:
- 0.5: Low threshold (acceptable strategy)
- 1.0: Standard threshold (good strategy)
- 1.5: High threshold (excellent strategy)
- 2.0: Very high threshold (exclusive strategy)

 max_drawdown : float, default=-0.2
Maximum permissible delay for a successful strategy.
Recommended values:
- 0.05: Very conservative (5 per cent)
-0.10: Conservative (10%)
-0.20: Moderate (20%)
-0.30: Aggressive (30%)

The value must be negative.

 min_return : float, default=0.0
Minimum cumulative returns for a successful strategy.
Recommended values:
- 0.0: No loss (0%)
- 0.05: Positive return (5 per cent)
- 0.10: Good return (10%)
- 0.20: Excellent return (20%)

 max_volatility : float, default=0.3
Maximum allowable volatility for a successful strategy.
Recommended values:
- 0.10: Low volatility (10%)
- 0.20: Moderate volatility (20%)
- 0.3: High volatility (30%)
- 0.05: Very high volatility (50%)

Only applicable if the column 'volatility' is available.

 custom_conditions : dict, optional
User conditions for success in format {column: determination}.
 examples:
 - {'sharpe': lambda x: x >= 1.5}
 - {'max_drawdown': lambda x: x >= -0.15}
 - {'cumulative_return': lambda x: x >= 0.1}

if specifed, redefinition of standard conditions.

 Returns:
 --------
 dict
A dictionary with metrics of probability of success.

Basic metrics:
- 'access_probability': flat is the probability of success (0-1)
- 'n_accessful':int is the number of successful simulations
- 'n_total':int is the total number of simulations
- 'access_rate': flat - percentage of successful simulations

for successful simulations:
- 'avg_sharpe_accessful': flat - medium Sharpe successful simulations
- 'avg_drawdown_accessful': float = average of successful simulations
- 'avg_return_accessful': float = average yield of successful simulations
- 'avg_volatility_accessful': float = average volatility of successful simulations

Additional metrics
- 'access_confidence_interval':uple - confidence interval for probability of success
- 'failure_Analisis':dict - analysis of the causes of failure

 Raises:
 -------
 ValueError
If simulations empty or not contain the necessary columns
If conditions are not appropriate
If the system_conditions contains non-existent columns

 Examples:
 ---------
 >>> import pandas as pd
 >>> import numpy as np
 >>>
>>#free test data
 >>> simulations = pd.dataFrame({
 ... 'sharpe': np.random.normal(1.0, 0.3, 1000),
 ... 'max_drawdown': np.random.normal(-0.1, 0.05, 1000),
 ... 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
 ... })
 >>>
>># Standard conditions for success
 >>> success = calculate_success_probability(simulations)
>> preint(f "Perspection of success: {access['access_probability']: 2 per cent}")
 >>>
>># Strict conditions for success
 >>> strict_success = calculate_success_probability(
 ... simulations,
 ... min_sharpe=1.5,
 ... max_drawdown=-0.1,
 ... min_return=0.1
 ... )
>>print(f"Strite probability of success: {strict_access['access_probability']: 2 per cent}")
 >>>
>># User conditions
 >>> custom_success = calculate_success_probability(
 ... simulations,
 ... custom_conditions={
 ... 'sharpe': lambda x: x >= 1.2,
 ... 'cumulative_return': lambda x: x >= 0.08
 ... }
 ... )
>>print(f) "User probability of success: {business_access['access_probability']:2%}")

 Notes:
 ------
- The probability of success shows the proportion of simulations that meet the criteria
- The confidence interval is calculated with binominal distribution
- Analysis of failures helps to understand the underlying causes of strategy failures
- It is recommended to use several levels of strictness of the criteria
 """
# Validation of input parameters
 if simulations.empty:
Raise ValueError ("dataFrame simulations not may be empty")

 if not isinstance(simulations, pd.dataFrame):
Raise ValueError("simulations must be pandas dataFrame")

# Check availability of requered columns
 required_columns = ['sharpe', 'max_drawdown', 'cumulative_return']
 Missing_columns = [col for col in required_columns if col not in simulations.columns]
 if Missing_columns:
 raise ValueError(f"Missing columns: {Missing_columns}")

# Validation of the conditions
 if max_drawdown > 0:
Raise ValueError("max_drawdown must be negative")

 if min_return < 0:
Raise ValueError("min_return must be non-negative")

 if max_volatility <= 0:
Raise ValueError("max_volatility must be positive")

# Determination of the conditions for success
 if custom_conditions is not None:
# User conditions
 success_condition = pd.Series([True] * len(simulations), index=simulations.index)

 for column, condition in custom_conditions.items():
 if column not in simulations.columns:
Raise ValueError(f)

 if not callable(condition):
Raise ValueError(f "The condition for {column} must be a function")

 success_condition &= simulations[column].apply(condition)
 else:
# Standard conditions
 success_condition = (
 (simulations['sharpe'] >= min_sharpe) &
 (simulations['max_drawdown'] >= max_drawdown) &
 (simulations['cumulative_return'] >= min_return)
 )

# Add a condition on volatility if available
 if 'volatility' in simulations.columns:
 success_condition &= (simulations['volatility'] <= max_volatility)

# Basic metrics
 n_total = len(simulations)
 n_successful = success_condition.sum()
 success_probability = success_condition.mean()
 success_rate = success_probability * 100

# metrics for successful simulations
 successful_simulations = simulations[success_condition]

 if len(successful_simulations) > 0:
 avg_sharpe = successful_simulations['sharpe'].mean()
 avg_drawdown = successful_simulations['max_drawdown'].mean()
 avg_return = successful_simulations['cumulative_return'].mean()

 if 'volatility' in simulations.columns:
 avg_volatility = successful_simulations['volatility'].mean()
 else:
 avg_volatility = None
 else:
 avg_sharpe = 0
 avg_drawdown = 0
 avg_return = 0
 avg_volatility = None

# Confidence interval for success (95 per cent)
 from scipy.stats import beta
 alpha = n_successful + 1
 beta_param = n_total - n_successful + 1
 ci_lower = beta.ppf(0.025, alpha, beta_param)
 ci_upper = beta.ppf(0.975, alpha, beta_param)

# Analysis of the causes of failure
 failed_simulations = simulations[~success_condition]
 failure_Analysis = {}

 if len(failed_simulations) > 0:
 failure_Analysis = {
 'sharpe_too_low': (failed_simulations['sharpe'] < min_sharpe).mean(),
 'drawdown_too_high': (failed_simulations['max_drawdown'] < max_drawdown).mean(),
 'return_too_low': (failed_simulations['cumulative_return'] < min_return).mean()
 }

 if 'volatility' in simulations.columns:
 failure_Analysis['volatility_too_high'] = (failed_simulations['volatility'] > max_volatility).mean()

 result = {
 'success_probability': success_probability,
 'n_successful': n_successful,
 'n_total': n_total,
 'success_rate': success_rate,
 'avg_sharpe_successful': avg_sharpe,
 'avg_drawdown_successful': avg_drawdown,
 'avg_return_successful': avg_return,
 'success_confidence_interval': (ci_lower, ci_upper),
 'failure_Analysis': failure_Analysis
 }

 if avg_volatility is not None:
 result['avg_volatility_successful'] = avg_volatility

 return result

# example use with detailed parameters
simulations = pd.dataFrame({
 'sharpe': np.random.normal(1.0, 0.3, 1000),
 'max_drawdown': np.random.normal(-0.1, 0.05, 1000),
 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
})

# Standard conditions for success
success_metrics = calculate_success_probability(
Simulations=simulations, # DataFrame with simulation results
min_sharpe = 1.0, # Minimum Sharpe
max_drawdown=-0.2, # Maximum draught
min_return=0.0, #Minimum return
max_volatility=0.3 # Maximum volatility
)
```

**Purity:**

```python
def calculate_profitability_metrics(simulations, initial_capital=100000,
 target_return=0.1, risk_free_rate=0.02):
 """
Calculation of cost-effectiveness metric for Monte Carlo simulations

Computes financial metrics of cost-effectiveness on basis of results
Monte Carlo simulations for assessing the cost-effectiveness of the strategy.

 Parameters:
 -----------
 simulations : pd.dataFrame
DataFrame with Monte Carlo simulations.
Shall contain the column `cumulative_return' with cumulative returns.

 initial_capital : float, default=100000
Initial capital for the calculation of the final value of the portfolio.
Recommended values:
- 10,000: Small portfolio ($10,000)
- 100,000: Standard portfolio ($100,000)
- 1000000: Large portfolio ($1,000,000)
- 100000: Institutional portfolio ($10,000.000)

Should be a positive number.

 target_return : float, default=0.1
Earmarked return for calculating the probability of achieving the objective.
Recommended values:
- 0.05: Conservative Goal (5 per cent)
- 0.10: Moderate Goal (10%)
- 0.15: Aggressive Goal (15%)
- 0.20: Very aggressive Goal (20%)

 risk_free_rate : float, default=0.02
Risk-free rate for calculating excess returns.
Recommended values:
- 0.01: Low rate (1 per cent)
- 0.02: Standard rate (2 per cent)
- 0.03: High rate (3 per cent)
- 0.05: Very high rate (5 per cent)

 Returns:
 --------
 dict
A dictionary with metrics of profitability.

Main cost parameters:
- 'mean_final_value': flat = average final value
- 'median_final_value': float - median final value
- 'std_final_value': flat = standard deviation of final value
== sync, corrected by elderman == @elder_man
- 'max_final_value': flat = maximum final value

Quantiles of final value:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

Probability of outcome:
- 'loss_probability': flat - probability of loss (final value < seed capital)
- 'Target_acchievation_probability': flat is the probability of achieving a target return
- 'significant_loss_probability': float - probability of significant loss (>50%)
- 'dubling_probability': flat is the probability of doubling capital

Additional metrics
- 'Excess_return': float - average excess return
- 'value_at_risk_95': float - VaR 95% for final value
- 'Expected_shotfall_95': float - ES 95% for final value

 Raises:
 -------
 ValueError
If simulations empty or not contain 'cumulative_return'
If initial_capital <=0
If Target_return < 0
If risk_free_rate < 0

 Examples:
 ---------
 >>> import pandas as pd
 >>> import numpy as np
 >>>
>>#free test data
 >>> simulations = pd.dataFrame({
 ... 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
 ... })
 >>>
>># Standard cost-effectiveness instruments
 >>> profitability = calculate_profitability_metrics(simulations)
>>print(f "Medial final value: {profitiability['mean_final_value']:,2f}")
>> preint(f "Probability of loss: {`loss_probability'': 2 per cent}")
 >>>
>># User parameters
 >>> custom_profitability = calculate_profitability_metrics(
 ... simulations,
 ... initial_capital=50000,
 ... target_return=0.12,
 ... risk_free_rate=0.025
 ... )
>>print(f "Approbability of 12%: {custom_profitiability['target_achievement_probability']: 2%}")

 Notes:
 ------
- Final value = initial_capital * (1 + cumulative_return)
- Excess return = average return - Rick_free_rate
- VaR and ES calculated for the final value of the portfolio
- Probability helps assess risks and policy options
 """
# Validation of input parameters
 if simulations.empty:
Raise ValueError ("dataFrame simulations not may be empty")

 if not isinstance(simulations, pd.dataFrame):
Raise ValueError("simulations must be pandas dataFrame")

 if 'cumulative_return' not in simulations.columns:
Raise ValueError("simulations shall contain the column 'cumulative_return')

 if initial_capital <= 0:
Raise ValueError("initial_capital must be positive")

 if target_return < 0:
Raise ValueError("target_return must be non-negative")

 if risk_free_rate < 0:
Raise ValueError("risk_free_rate must be non-negative")

# Final value of portfolio
 final_values = initial_capital * (1 + simulations['cumulative_return'])

# Basic final value statistics
 mean_final_value = final_values.mean()
 median_final_value = final_values.median()
 std_final_value = final_values.std()
 min_final_value = final_values.min()
 max_final_value = final_values.max()

# Quantile of final value
 q5_final_value = final_values.quantile(0.05)
 q25_final_value = final_values.quantile(0.25)
 q75_final_value = final_values.quantile(0.75)
 q95_final_value = final_values.quantile(0.95)

# Probability of outcome
 loss_probability = (final_values < initial_capital).mean()
 target_achievement_probability = (final_values >= initial_capital * (1 + target_return)).mean()
 significant_loss_probability = (final_values < initial_capital * 0.5).mean()
 doubling_probability = (final_values >= initial_capital * 2).mean()

# Surplus returns
 mean_return = simulations['cumulative_return'].mean()
 excess_return = mean_return - risk_free_rate

# VaR and ES for final value
 var_95 = final_values.quantile(0.05)
 es_95 = final_values[final_values <= var_95].mean()

 return {
 'mean_final_value': mean_final_value,
 'median_final_value': median_final_value,
 'std_final_value': std_final_value,
 'min_final_value': min_final_value,
 'max_final_value': max_final_value,
 'q5_final_value': q5_final_value,
 'q25_final_value': q25_final_value,
 'q75_final_value': q75_final_value,
 'q95_final_value': q95_final_value,
 'loss_probability': loss_probability,
 'target_achievement_probability': target_achievement_probability,
 'significant_loss_probability': significant_loss_probability,
 'doubling_probability': doubling_probability,
 'excess_return': excess_return,
 'value_at_risk_95': var_95,
 'expected_shortfall_95': es_95,
 'initial_capital': initial_capital,
 'target_return': target_return,
 'risk_free_rate': risk_free_rate
 }

# example use with detailed parameters
simulations = pd.dataFrame({
 'cumulative_return': np.random.normal(0.15, 0.1, 1000)
})

# Standard cost-effectiveness metrics
profitability_metrics = calculate_profitability_metrics(
Simulations=simulations, # DataFrame with simulation results
Initial_capital=100,000, #Inventory capital $100,000
Target_return=0.1 # Target return 10%
Rick_free_rate=0.02 # Risk-free rate 2%
)
```

♪ Visualization of Monte Carlo simulations

## # Dashbord of Monte Carlo Simulation Visualization

```mermaid
graph TD
A [Monte Carlo simulations results] - • B [Dashboard visualization]

B -> C [Distributions]
C --> C1[Sharp coefficient histogram<br/>with middle and quantile lines]
C --> C2 [Hystogram of maximum draught<br/>with middle and quantile lines]
C --> C3 [Cumulative return histogram<br/>with middle and quantile lines]
C --> C4[Q-Q schedule for normality<br/>scipy.stats.probplot]

B -> D [Temporary rows]
D -> D1 [Ride of return<br/>100 random trajectory]
D --> D2 [Medical route<br/>mean_cumulative_returns]
D --> D3 [Diffusion of final values<br/>histogram final_valutes]
D --> D4 [Collection of metric<br/>scatter sharpe vs drawdown]
D --> D5 [Temporary evolution of volatility<br/>rolling_volatility]

B -> E [Statistical graphs]
E --> E1[Box flat metric<br/>with emissions and quintiles]
E --> E2[Violin table distributions<br/> probability density]
E --> E3 [Coordination matrix<br/>heatmap associations]
E --> E4 [Cumulative distributions<br/>CF for each metrics]

B -> F [Comparative graphs]
F --> F1[comparison simulation techniques<br/>parmetric vs nonparametric vs hybrid]
F --> F2[comparison stress-test scenarios<br/>crash vs high_vol vs low_vol]
F --> F3[comparison confidence intervals<br/>90% vs 95% vs 99%]
F --> F4 [comparson VaR and ES<br/> different levels of confidence]

C1-> G[Interactive elements]
 C2 --> G
 C3 --> G
 C4 --> G
 D1 --> G
 D2 --> G
 D3 --> G
 D4 --> G
 D5 --> G
 E1 --> G
 E2 --> G
 E3 --> G
 E4 --> G
 F1 --> G
 F2 --> G
 F3 --> G
 F4 --> G

 G --> H[Zoom and Pan functions]
G --> I [Filtering on metrics]
G --> J [Export in different formats]
G --> K[configuration of colour patterns]
G-> L[Analysis of time series]

H-> M[Final Dashboard]
 I --> M
 J --> M
 K --> M
 L --> M

M --> N[Distribution Analysis]
M --> O [Identifying anomalies]
M --> P [Risk evaluation]
M --> Q[comparison strategies]

N -> R [Recommendations on strategy]
 O --> R
 P --> R
 Q --> R

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style G fill:#fff3e0
 style R fill:#4caf50
```

♪##1 ♪ Distributions

```python
def visualize_monte_carlo_distributions(simulations, save_path=None):
"Visualization of Monte carlo distributions of simulations."
 import matplotlib.pyplot as plt
 import seaborn as sns

# configuring style
 plt.style.Use('seaborn-v0_8')
 sns.set_palette("husl")

# Create figures
 fig, axes = plt.subplots(2, 2, figsize=(15, 10))

* 1. Sharpe coefficient distribution
 axes[0, 0].hist(simulations['sharpe'], bins=50, alpha=0.7, edgecolor='black')
 axes[0, 0].axvline(simulations['sharpe'].mean(), color='red', linestyle='--',
Label=f'Medium:
 axes[0, 0].axvline(simulations['sharpe'].quantile(0.05), color='orange', linestyle='--',
Label=f'5% quintile: {simulations["sharpe"] Quantile(0.05):2f}')
axes[0,0].set_title('Sharp coefficient distribution')
axes[0,0].set_xlabel('Sharpa's coefficient')
axes[0,0].set_ylabel('Part')
 axes[0, 0].legend()
 axes[0, 0].grid(True)

♪ 2. Distribution of maximum draught
 axes[0, 1].hist(simulations['max_drawdown'], bins=50, alpha=0.7, edgecolor='black')
 axes[0, 1].axvline(simulations['max_drawdown'].mean(), color='red', linestyle='--',
Label=f'Medium: {`max_drawdown'].mean(:2f}'
 axes[0, 1].axvline(simulations['max_drawdown'].quantile(0.95), color='orange', linestyle='--',
Label=f'95% quintile: {simulations["max_drawdown"] quantile(0.95):2f}')
axes[0,1].set_title('The maximum draught distribution')
axes[0, 1].set_xlabel('Maximal prosperity')
axes[0,1].set_ylabel('Part')
 axes[0, 1].legend()
 axes[0, 1].grid(True)

# 3. Distribution of cumulative returns
 axes[1, 0].hist(simulations['cumulative_return'], bins=50, alpha=0.7, edgecolor='black')
 axes[1, 0].axvline(simulations['cumulative_return'].mean(), color='red', linestyle='--',
Label=f'Medium: {`cumulative_return'].mean(:2f}'
 axes[1, 0].axvline(simulations['cumulative_return'].quantile(0.05), color='orange', linestyle='--',
Label=f'5% quintile: {simulations["cumulative_return" ] quantile(0.05):2f}')
axes[1, 0].set_title('cumulative return distribution')
axes[1, 0].set_xlabel('cumulative return')
axes[1, 0].set_ylabel('Part')
 axes[1, 0].legend()
 axes[1, 0].grid(True)

# 4. Q-Q chart for Sharp coefficient
 from scipy import stats
 stats.probplot(simulations['sharpe'], dist="norm", plot=axes[1, 1])
axes[1, 1].set_title('Q-Q schedule Sharpe coefficient')
 axes[1, 1].grid(True)

 plt.tight_layout()

 if save_path:
 plt.savefig(save_path, dpi=300, bbox_inches='tight')

 plt.show()

# Example of use
visualize_monte_carlo_distributions(simulations, save_path='monte_carlo_distributions.png')
```

♪##2 ♪ Time rows ♪

```python
def visualize_monte_carlo_paths(simulations, n_paths=100, save_path=None):
"Visualization of the Monte Carlo Simulation Paths."
 import matplotlib.pyplot as plt

# configuring style
 plt.style.Use('seaborn-v0_8')

# Create figures
 fig, axes = plt.subplots(2, 2, figsize=(15, 10))

♪ 1. Pathways of return
 for i in range(min(n_paths, len(simulations))):
 returns = simulations.iloc[i]['returns']
 cumulative_returns = (1 + returns).cumprod()
 axes[0, 0].plot(cumulative_returns, alpha=0.1, color='blue')

# Medium way
 mean_returns = np.mean([sim['returns'] for sim in simulations.iloc[:n_paths]], axis=0)
 mean_cumulative_returns = (1 + mean_returns).cumprod()
axes[0,0].plot(mean_cumulative_returns, color='red', linewidth=2, label='Midway')

axes[0,0].set_title('Ending Paths')
axes[0,0].set_xlabel('Time')
axes[0,0].set_ylabel('cumulative return')
 axes[0, 0].legend()
 axes[0, 0].grid(True)

♪ 2. Distribution of final values
 final_values = (1 + simulations['cumulative_return']).values
 axes[0, 1].hist(final_values, bins=50, alpha=0.7, edgecolor='black')
 axes[0, 1].axvline(final_values.mean(), color='red', linestyle='--',
Label=f'Medium: {final_valutes.mean(:2f}')
axes[0,1].set_title(' Final distribution')
axes[0,1].set_xlabel('Final')
axes[0,1].set_ylabel('Part')
 axes[0, 1].legend()
 axes[0, 1].grid(True)

# 3. Correlation between metrics
 axes[1, 0].scatter(simulations['sharpe'], simulations['max_drawdown'], alpha=0.5)
axes[1, 0].set_xlabel('Sharpa's coefficient')
axes[1, 0].set_ylabel('Maximal prosin')
axes[1, 0].set_title('Colletion: Sharpe vs Max Drawdown')
 axes[1, 0].grid(True)

# 4. Temporary evolution of volatility
 volatility_paths = []
 for i in range(min(n_paths, len(simulations))):
 returns = simulations.iloc[i]['returns']
 rolling_vol = pd.Series(returns).rolling(30).std()
 volatility_paths.append(rolling_vol)

 mean_volatility = np.mean(volatility_paths, axis=0)
axes[1, 1]. Platform(mean_volatility, color='red', linewidth=2, label='average volatility')
axes[1, 1].set_title('Temporary evolution of volatility')
axes[1, 1].set_xlabel('Time')
axes[1, 1].set_ylabel('Volatility')
 axes[1, 1].legend()
 axes[1, 1].grid(True)

 plt.tight_layout()

 if save_path:
 plt.savefig(save_path, dpi=300, bbox_inches='tight')

 plt.show()

# Example of use
visualize_monte_carlo_paths(simulations, n_paths=100, save_path='monte_carlo_paths.png')
```

♪ Automation of Monte Carlo simulations

♪# ♪ The Monte Carlo Automation Pypline

```mermaid
graph TD
A [Reference data] -> B [MonteCarloPipeleine]
B -> C [configration of parameters]

C --> D[Parametric simulations<br/>normal, t-distribution, mixture]
C --> E [Non-parametric simulations<br/>bootstrap, permutation]
C --> F[Hybrid simulations<br/>GARCH, Copenhagen]
C --> G[Stress test<br/>crash, high_vol, low_vol, regulations]

D -> H [Simulation execution<br/>n_simulations = 10,000]
 E --> H
 F --> H
 G --> H

H -> I [Quality metric calculation]
I -> J[Sharp coefficient<br/>mean/std* sqrt(252)]
I --> K[Macial draught<br/>calculate_max_drawdown]
I -> L [cumulative return<br/>cumprod(1 + returns) - 1]
 I --> M[VaR and ES<br/>quantile, expected_shortfall]

J -> N [Compilation of results on methods]
 K --> N
 L --> N
 M --> N

N -> O[Generation of the Integrated Reporta]
O -> P [Report on methods]
O -> Q [Detail results]
O -> R [Recommendations]

P --> S [Medical Sharp coefficient<br/>mean_sharpe]
P --> T[standard deviation<br/>std_sharpe]
P -> U[All successful strategies<br/>access_rate]
 P --> V[VaR 95%<br/>var_95]
 P --> W[ES 95%<br/>es_95]

Q -> X [Individual simulation results]
Q -> Y[comparison of methods]
Q -> Z[Statistical tests]

R --> AA [Evaluation of performance]
AA --> BB[Great: Sharpe > 1.5, Science > 70%]
AA --> CC[Good: Sharpe > 1.0, Communication > 50 per cent]
AA-> DD [Required for improvement: otherwise]

BB --> EE[~ Strategy is ready for action]
CC-> FF[~ Strategy requires Monitoring]
DD --> GG[~ Strategy needs further development]

EE --> HH [Business in Sales]
FF --> II [Further testing]
GG --> JJ [Optimization of parameters]

JJ --> KK[configuring distributions]
JJ --> LL [configration of simulation techniques]
KK --> MM[Return testing]
 LL --> MM
 MM --> B

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style O fill:#fff3e0
 style EE fill:#4caf50
 style FF fill:#ff9800
 style GG fill:#ffcdd2
```

###1.Pipline Monte Carlo simulations

```python
class MonteCarloPipeline:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self, data, model, metrics_calculator):
 self.data = data
 self.model = model
 self.metrics_calculator = metrics_calculator
 self.results = {}

 def run_parametric_simulations(self, n_simulations=10000, time_horizon=252,
 distribution='normal'):
""Parametric simulations."
 returns = self.data['returns']

 if distribution == 'normal':
 simulations = normal_monte_carlo(returns, n_simulations, time_horizon)
 elif distribution == 't':
 simulations = t_distribution_monte_carlo(returns, n_simulations, time_horizon)
 elif distribution == 'mixture':
 simulations = mixture_monte_carlo(returns, n_simulations, time_horizon)
 else:
 raise ValueError(f"Unknown distribution: {distribution}")

 self.results[f'parametric_{distribution}'] = simulations
 return simulations

 def run_nonparametric_simulations(self, n_simulations=10000, time_horizon=252,
 method='bootstrap'):
"Unparametric simulations."
 returns = self.data['returns']

 if method == 'bootstrap':
 simulations = bootstrap_monte_carlo(returns, n_simulations, time_horizon)
 elif method == 'permutation':
 simulations = permutation_monte_carlo(returns, n_simulations, time_horizon)
 else:
 raise ValueError(f"Unknown method: {method}")

 self.results[f'nonparametric_{method}'] = simulations
 return simulations

 def run_hybrid_simulations(self, n_simulations=10000, time_horizon=252,
 method='garch'):
"Hybrid Simulations."
 returns = self.data['returns']

 if method == 'garch':
 simulations = garch_monte_carlo(returns, n_simulations, time_horizon)
 elif method == 'copula':
 simulations = copula_monte_carlo(returns, n_simulations, time_horizon)
 else:
 raise ValueError(f"Unknown method: {method}")

 self.results[f'hybrid_{method}'] = simulations
 return simulations

 def run_stress_test_simulations(self, n_simulations=10000, time_horizon=252,
 stress_scenarios=None):
"Strike testing."
 returns = self.data['returns']

 simulations = stress_test_monte_carlo(returns, n_simulations, time_horizon,
 stress_scenarios)

 self.results['stress_test'] = simulations
 return simulations

 def generate_comprehensive_Report(self):
♪ "Generation of the Integrated Report" ♪
 Report = {
 'summary': {},
 'Detailed_results': self.results,
 'recommendations': []
 }

# Analysis of each method
 for method, simulations in self.results.items():
 if isinstance(simulations, pd.dataFrame):
# Basic metrics
 mean_sharpe = simulations['sharpe'].mean()
 std_sharpe = simulations['sharpe'].std()
 mean_max_drawdown = simulations['max_drawdown'].mean()
 success_rate = (simulations['sharpe'] > 1.0).mean()

# Risk-metrics
 var_95 = simulations['sharpe'].quantile(0.05)
 es_95 = simulations[simulations['sharpe'] <= var_95]['sharpe'].mean()

 Report['summary'][method] = {
 'mean_sharpe': mean_sharpe,
 'std_sharpe': std_sharpe,
 'mean_max_drawdown': mean_max_drawdown,
 'success_rate': success_rate,
 'var_95': var_95,
 'es_95': es_95
 }

# Recommendations
 if mean_sharpe > 1.5 and success_rate > 0.7:
Report(f)(`recommendations'): Excellent performance)
 elif mean_sharpe > 1.0 and success_rate > 0.5:
Report(f) (good performance)
 else:
Report ['recommendations'].append(f'{method}: Needs improvement")

 return Report

# Example of use
pipeline = MonteCarloPipeline(data, model, metrics_calculator)
pipeline.run_parametric_simulations(distribution='normal')
pipeline.run_nonparametric_simulations(method='bootstrap')
pipeline.run_hybrid_simulations(method='garch')
pipeline.run_stress_test_simulations()
Report = pipeline.generate_comprehensive_Report()
```

## Conclusion

Monte Carlo simulations are the key to creating robotic and profitable strategies.

1. ** Checking for consistency** strategies on multiple scenarios
2. ** Risk management** - understand potential losses
3. **Optimize parameters** for maximum stability
4. ** To obtain statistical certainty** in results

### Key principles

1. ** Multiplicity of scenarios** - Test on different conditions
2. ** Statistical significance** - check the relevance of the results
3. **Manage Risks** - consider VaR and ES
4. ** Economic significance** - test the profitability
5. **validation** - check the results on outof-sample data

### Next steps

Once you have mastered Monte Carlo simulations, go to:

- [Porthfolio Administration](./30_Porthfolio_Management.md)
