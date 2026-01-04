# Advanced configuring AutoML Gluon

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Whoy advanced configuration is critical

**Why 90 percent of AutoML Gluon not users use advanced Settings?** Because they don't understand what power they're missing. It's like driving Ferrari on first gear - the car is going, but not showing its possibilities.

### What does advanced configuration do?
- **Total**: The Working on 10-30% models are better
- **Speed**: Training accelerates in 2 to 5 times
You know exactly what's going on.
- **Optimization**: Model adjusted to fit your data

### What happens without advanced configuration?
- ** Average results**: Working models "how it works"
- ** Sized education**: Spend your time on non-optimal Settings
- ** Underutilization of resources**: GPU and CPU Working are inefficient
- ** Disappointing**:not understand why the results are improving.

## configurization of hyperparameters

<img src="images/optimized/monte_carlo_Analisis.png" alt="configuring hyperparameters" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 1: Process Settings and Optimizing Hyperparameter*

Why are hyperparameters the key to success? Because they define how the algorithm learns. It's like a configuration musical instrument - the correct configuration gives a beautiful sound.

### ♪ Hyperparameter optimization strategies

<img src="images/optimized/robustness_Analysis.png" alt="Emtimization strategies" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
♪ Figure 2: Different hyperparameter optimization strategies ♪

♪ Why do different strategies matter? ♪ ♪ Because different tasks require different approaches to optimization:

- **Grid Search**: Systematic search on the grid of parameters
- **Random Search**: Random Search**: Random search in the parameter space
- **Bayesian Optimization**: Smart search with previous results
- **Evolutionary Algorithms**: Genetic algorithms for optimization
- **Multi-Object Optimization**: Optimization of several metrics simultaneously
- **Early Stopping**: Stopping without improvement
- **Resource allocation**: Distribution of resources between different algorithms

###create caste hyperparameter

Because standard Settings are suitable for average cases, and your data can be special.

```python
# Detailed configuring for each algorithm
hyperparameters = {
'GBM': #Gradient Boosting Machine - one of the best algorithms
 {
# Rapid configuring for experiments
'num_boost_round': 100, #The number of trees (more = accurate but slower)
'num_leaves': 31, #maximum number of leaves in wood
'learning_rate': 0.1 # Learning speed (less = stable)
'feature_fraction': 0.9, # Proportion of signs for each tree (prevention)
'Bagging_fraction': 0.8, # Proportion of data for each tree
'Bagging_freq': 5, #Bagging frequency
'min_data_in_leaf': 20, # Minimum data in sheet (prevention)
'min_sum_hessian_in_leaf': 1e-3, #minimum amount of gradients in sheet
'labbda_l1':0.0, #L1 regularization (Lasso)
'labbda_l2':0.0, #L2 regularization (Ridge)
'min_gain_to_split':0.0, #minimum increase for separation
'max_dept': -1, # Maximum depth (-1 = no limit)
'Save_binary':True, #Save Binary files
'Seed': 0, # Seed for Reproducibility
'feature_fraction_seated': 2, #seed for selection of topics
'Bagging_seed': 3, # Seed for Bagging
'drop_seed': 4, # Seed for dropout
'verbose': -1, # Output level (-1 = quiet)
'keep_training_boster': False #not save intermediate models
 },
 {
# A thorough conference for final education
'num_boost_round': 200, #more trees for better accuracy
'num_laves': 63, #Big leaves for complex pathers
'Learning_rate': 0.05, #Little speed for stability
'feature_fraction': 0.8, # Less signs for prevention of retraining
'Bagging_fraction': 0.7, # Less data for greater diversity
'Bagging_freeq': 5, # Same bugging frequency
'min_data_in_leaf': 10, # Less data in sheet for details
'min_sum_hessian_in_leaf': 1e-3, # Same minimum gradient
'labbda_l1': 0.1 #L1 regularization for the selection of topics
'labbda_l2': 0.1 #L2 regularization for smoothing
'min_gain_to_split': 0.0, # Same minimum increase
'max_dept': -1, # No depth limit
'Save_binary':True, #Save Binary files
'Seed': 0, # Seed for Reproducibility
'feature_fraction_seated': 2, #seed for selection of topics
'Bagging_seed': 3, # Seed for Bagging
'drop_seed': 4, # Seed for dropout
'verbose': -1, # Quiet Mode
 'keep_training_booster': False
 }
 ],
'CAT': [ # CatBoost - Excellent algorithm for categorical data
 {
# Basic configuring CatBoost
'items: 100, # Quantity of iterations (more = more precisely)
'learning_rate': 0.1 # Learning speed
'dept': 6, # Tree depth (more=more difficult)
'l2_leaf_reg': 3.0, #L2 regularization for leaves
 'bootstrap_type': 'Bayesian',
 'random_strength': 1.0,
 'bagging_temperature': 1.0,
 'od_type': 'Iter',
 'od_wait': 20,
 'verbose': False
 },
 {
 'iterations': 200,
 'learning_rate': 0.05,
 'depth': 8,
 'l2_leaf_reg': 5.0,
 'bootstrap_type': 'Bayesian',
 'random_strength': 1.0,
 'bagging_temperature': 1.0,
 'od_type': 'Iter',
 'od_wait': 20,
 'verbose': False
 }
 ],
 'XGB': [
 {
 'n_estimators': 100,
 'max_depth': 6,
 'learning_rate': 0.1,
 'subsample': 0.8,
 'colsample_bytree': 0.8,
 'reg_alpha': 0.0,
 'reg_lambda': 1.0,
 'random_state': 0
 },
 {
 'n_estimators': 200,
 'max_depth': 8,
 'learning_rate': 0.05,
 'subsample': 0.9,
 'colsample_bytree': 0.9,
 'reg_alpha': 0.1,
 'reg_lambda': 1.0,
 'random_state': 0
 }
 ],
 'RF': [
 {
 'n_estimators': 100,
 'max_depth': 10,
 'min_samples_split': 2,
 'min_samples_leaf': 1,
 'max_features': 'sqrt',
 'bootstrap': True,
 'random_state': 0
 }
 ],
 'KNN': [
 {
 'n_neighbors': 5,
 'weights': 'uniform',
 'algorithm': 'auto',
 'leaf_size': 30,
 'p': 2,
 'metric': 'minkowski'
 }
 ]
}

predictor.fit(train_data, hyperparameters=hyperparameters)
```

#### ♪ Detailed describe of hyperparameter parameters

**parameters LightGBM (GBM):**

**`num_boost_round`:**
- ** Which means**: Number of trees (busters) in ensemble
- ** Why do you need**: More trees = better accuracy but slower learning
- ** Recommended values**:
- ** Rapid experiments**: `50-100'
- ** Standard tasks**: `100-300'
- ** Critical tasks**: `300-1000'
- ** Maximum quality**: `1000+'
- ** Impact on performance**:
- ** Few trees**: Rapid learning, but there may be a lack of education
- ** Multitrees**: Slow learning, but maybe retraining
- **Optimal**: Depends from the complexity of the data
- ** Practical examples**:
- ** Simple data**: `50-100' trees
- ** Complex data**: `200-500' trees
- **Very complex data**: `500+' trees

**`num_leaves`:**
- ** Which means**: Maximum number of leaves in wood
- # Why do you need # # More leaves = more complicated model, but the risk of retraining #
- ** Recommended values**:
- ** Simple data**: `31-63'
- **Medical data**: `63-127'
- ** Complex data**: `127-255'
- **Very complex data**: `255+'
- **The effect on the model**:
- ** Few leaves**: Simple model, less retraining
- ** Lots of leaves**: Complicated model, more retraining
- **Optimal**: Balance between complexity and retraining

**`learning_rate`:**
- ** Meaning**: Learning speed (gradient descent step)
- # Why do you need # # Less speed = more stable education but slower #
- ** Recommended values**:
- **Early education**: `0.1-0.3'
- ** Standard education**: `0.05-0.1'
- **Early education**: `0.01-0.05'
- **Effects on learning**:
- ** High speed**: Rapid learning, but it can be unstable
- **low speed**: Slow learning but stable
- **Optimal**: Depends from data and number of trees

**`feature_fraction`:**
- ** Which means**: Proportion of signs for each tree
- What's the point?
- ** Recommended values**:
- ** Multiple features**: `0.5-0.8'
- ** Average**: `0.8-0.9'
- ** Few features**: `0.9-1.0'
- **The effect on the model**:
- **Little share**: More diversity, less retraining
- **Big share**: Less diversity, more retraining
- **Optimal**: Depends from the number of topics

**`bagging_fraction`:**
- ** Which means**: Percentage of data taken for each tree
- What's the point?
- ** Recommended values**:
- **Big data**: `0.5-0.8'
- **Medical data**: `0.8-0.9'
- **Lowered data**: `0.9-1.0'
- **The effect on the model**:
- **Little share**: More diversity, less retraining
- **Big share**: Less diversity, more retraining
- **Optimal**: Depends from the size of the data

**`min_data_in_leaf`:**
- ** Meaning**: Minimum number of data in the tree sheet
- What's the point?
- ** Recommended values**:
- **Big data**: `10-50'
- **Medical data**: `20-100'
- **Lowered data**: `50-200'
- **The effect on the model**:
- **Lower**: More detailed model, risk retraining
- ** Large**: More generic model, less retraining
- **Optimal**: Depends from the size of the data and the complexity of the task

**`lambda_l1` and `lambda_l2`:**
- ** Meaning**: L1 and L2 regularization for prevention of retraining
- # Why do you need # # L1 picks the signs, L2 smooths the model #
- ** Recommended values**:
**L1 regularization**: `0.0-0.1' (selection of topics)
- **L2 regularization**: `0.0-0.1' (smoothing)
- **The effect on the model**:
- **L1 > 0**: Selectes unimportant features
- **L2 > 0**: Grinds the weight of the model
- **Both > 0**: Combined effect

### Optimization of hyperparameters

```python
# configuration search for hyperparameters
from autogluon.core import Space

# Definition of search space
hyperparameter_space = {
 'GBM': {
 'num_boost_round': Space(50, 500),
 'num_leaves': Space(31, 127),
 'learning_rate': Space(0.01, 0.3),
 'feature_fraction': Space(0.5, 1.0),
 'bagging_fraction': Space(0.5, 1.0)
 },
 'XGB': {
 'n_estimators': Space(50, 500),
 'max_depth': Space(3, 10),
 'learning_rate': Space(0.01, 0.3),
 'subsample': Space(0.5, 1.0),
 'colsample_bytree': Space(0.5, 1.0)
 }
}

predictor.fit(
 train_data,
 hyperparameter_tune_kwargs={
 'num_trials': 20,
 'scheduler': 'local',
 'searcher': 'auto'
 }
)
```

#### ♪ Detailed descriebe optimization of hyperparameters

**parameter `num_trials' - Number of optimization attempts**

- ** Meaning**: Number of different combinations of hyperparameters for testing
- ♪ Why do you need to ♪ ♪ More trying ♪ ♪ Better quality but longer time ♪
- **on default**: `10' (10 attempts)
- ** Recommended values**:
- ** Rapid experiments**: `5-10' attempts
- ** Standard tasks**: `10-20' attempts
- ** Critical tasks**: `20-50' attempts
- ** Maximum quality**: `50+' attempts
- **Effects on time of study**:
- **5 attempts**: Rapid learning, basic quality
- **20 attempts**: Average time, good quality
- **50 attempts**: Long time, high quality
- ** Practical examples**:
- ** Prototype**: `num_trials=5'
- **Development**: `num_trials=10-20'
== sync, corrected by elderman == @elder_man
- **Optification on Resources**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- **Long time**: `num_trials=20-50'

**Parmamer `scheduler' - Task Planner**

- ** Meaning**: Planner of parallel optimization tasks
- ** Why you need**: Controls parallel search of hyperparameters
- **on default**: `'local'' (local execution)
- ** Available**:
- **'local'** - Local execution on one computer
- **'ray'** - Distributed execution through Ray
- **'dask'** - Distributed execution via Dask
- ** Practical examples**:
- **One computer**: `scheduler='local''
- **Cluster with Ray**: `scheduler='ray'
- **Cluster with Dask**: `scheduler='dask''
- ** Impact on performance**:
- **local**: Slowly but simpler in settings
- **ray/dask**: Faster but requires Settings cluster
- ** When to use**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**parameter `searcher' - Search algorithm**

- Which means**: The search algorithm for optimal hyperparameters
- What's the point?
- **on default**: ``auto'' (automatic choice)
- ** Available**:
- **'auto'** - Automatic choice of the best algorithm
- **'random'** - Random Search
- **'bayes''** - Bayesov optimization
- **'grid'** - Grid Search
- ** Practical examples**:
- ** Rapid search**: `searcher='random''
- ** Qualitative Search**: `Searcher='bayes'
- ** Full overreact**: `searcher='grid''
- **Effect on quality**:
- **random**: Quick but may miss good combinations
- **bayes**: Slowly but finds the best combinations.
- **grid**: Very slowly but guaranteed to find the optimum
- ** When to use**:
- **Speed experiments**: `searcher='random''
- ** Standard tasks**: `searcher='auto' or `searcher'='byes''
- ** Critical tasks**: `searcher='grid'

**parameter `Space' - Definition of search space**

- ** Which means**: Determines the range of values for each hyperparameter
- ** Why you need**: Limits search to reasonable limits
- **Syntax**: `Space(min_value, max_value)' for numerical parameters
- ** Practical examples**:
**Totals**: `Space(50, 500)' for the number of trees
- **Dimensions**: `Space(0.01, 0.3)' for speed of learning
- **Logsy values**: `[True, False]' for boulder parameters
- **Effect on search**:
- ** Narrow range**: Quick search but may miss optimal values
- **Speed range**: Slow search, but better chance of finding the best
- ** Recommendations on settings**:
- ** Start with the wide range**: `Space(1, 1000)' for the number of trees
- **Size on basic results**: `Space(100, 300)' after the first experiments
- **Use logarithmic scale**: for parameters with exponential influence

** Practical examples Settings Optimization:**

```python
# Rapid optimization for experiments
quick_optimization = {
 'num_trials': 5,
 'scheduler': 'local',
 'searcher': 'random'
}

# Standard optimization for development
standard_optimization = {
 'num_trials': 20,
 'scheduler': 'local',
 'searcher': 'bayes'
}

# Qualitative optimization for sales
quality_optimization = {
 'num_trials': 50,
 'scheduler': 'ray',
 'searcher': 'bayes'
}

# Full optimization for critical tasks
full_optimization = {
 'num_trials': 100,
 'scheduler': 'ray',
 'searcher': 'grid'
}
```

** Optimization on data size:**

```python
# Small data (< 1,000 lines)
small_data_optimization = {
 'num_trials': 10,
 'scheduler': 'local',
 'searcher': 'random'
}

# Average data (1000 to 10,000 lines)
medium_data_optimization = {
 'num_trials': 20,
 'scheduler': 'local',
 'searcher': 'bayes'
}

# Big data (> 10,000 lines)
large_data_optimization = {
 'num_trials': 30,
 'scheduler': 'ray',
 'searcher': 'bayes'
}
```

**Monitoring the optimization process:**

```python
# configuring with Monitoring
def optimization_callback(trial, score, hyperparameters):
"Callback for Monitoring Optimization""
 print(f"Trial {trial}: Score = {score:.4f}")
 print(f"Hyperparameters: {hyperparameters}")

predictor.fit(
 train_data,
 hyperparameter_tune_kwargs={
 'num_trials': 20,
 'scheduler': 'local',
 'searcher': 'bayes',
 'callbacks': [optimization_callback]
 }
)
```

## configuring ensemble

### ♪ Architecture ensemble

<img src="images/optimized/addanced_production_flow.png" alt="architecture ensemble" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 3: Architecture and configuring ensemble in AutoML Gluon*

♪ Why is it important to have the right configuring ensembles? ♪ ♪ 'Cause the ensembles can improve the quality of the model on 5-15%:

- **Bagging**: Training multiple models on different sub-samples
- **Boosting**: sequential transfer of models with focus on errors
**Stacking**: Training the meta-model on basic model predictions
- **Voting**: Simple voting between models
- **Blending**: Weighted association of preferences
- **Multi-Level Stacking**: Multilevel ensembles for maximum quality

### Multilevel ensembles

```python
# configuring glass
predictor.fit(
 train_data,
num_bag_folds=5, #Number of Folds for Bagging
num_bag_sects=2, #Number of Bagging Sets
num_stack_levels=2 # Glassing levels
Stack_ensemble_levels=[0,1], #What levels to use for glass
Ag_args_fit={'num_gpus': 1, 'num_cpus': 4} # Resources for learning
)
```

#### ♪ Detailed descriebe ensemble parameters

**parameter `num_bag_folds' - Number of folds for bagging**

- ** Which means**: Number of folds for creating an ensemble through bagging
- ** Why you need**: Creates a variety of models for greater stability
- **on default**: `8' (8 folds)
- ** Recommended values**:
- **Early education**: `3-5' folds
- ** Standard education**: `5-8' folds
- ** Qualitative education**: `8-12' folds
- ** Maximum quality**: `12-20' folds
- **Effect on quality**:
- **Lower folds**: Faster learning but less stable results
- ** Lots of folds**: Slow learning but more stable results
- ** Optimization in time**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- **Long time**: `num_bag_folds=10-15'
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**parameter `num_bag_sets' - Number of bagging sets**

- ** Meaning**: Number of independent bagging sets (number of ensembles)
- ** Why you need**: Creates several independent ensembles for quality improvement
- **on default**: `1' (one ensemble)
- ** Recommended values**:
- **Early education**: `1' set
- ** Standard education**: `1-2' sets
- ** Qualitative education**: `2-3' sets
- ** Maximum quality**: `3-5' sets
- **Effect on quality**:
- **One set**: Faster but may be less stable
- ** Several sets**: Slower but more stable results
- **Optification on Resources**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- **Long time**: `num_bag_sects=2-3'
- ** Practical examples**:
- ** Rapid experiments**: `num_bag_sects=1'
- ** Standard tasks**: `num_bag_sects=1-2'
== sync, corrected by elderman == @elder_man

**parameter `num_stack_levels' - Glassing levels**

- ** Meaning**: Number of levels of glassing (multilevel ensembles)
- ** Why you need**: Creates hierarchical ensembles for maximum quality
- **on default**: `0' (without glassing)
- ** Recommended values**:
- **Early education**: `0' (without glassing)
- ** Standard education**: `0-1' level
- ** Qualitative education**: `1-2' levels
- ** Maximum quality**: `2-3' level
- **Effect on quality**:
- ** Without glass**: Faster, but less accurate
- ** With glass**: Slower but often more accurate results
- ** Optimization in time**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- **For a long time**: `num_stack_levels=2'
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**parameter `stack_ensemble_levels' - Levels for glassing**

- ** Meaning**: What levels of models to use for the creation of glass
- What's it for?
- **on default**: `[0] ` (base models only)
- ** Available**:
- ** `[0]'** - Basic models only (without glass)
- ** `[0, 1]'** - Basic models + first level of glassing
- ** `[0, 1, 2] `** - Basic models + two levels of glass
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- **Effect on quality**:
- ** Basic**: Faster, but less accurate
- **Stencing**: Slower but often more accurate results
- ** When to use**:
- ** Rapid experiments**: `stack_ensemble_levels=[0] `
- ** Standard tasks**: `stack_ensemble_levels=[0, 1] `
- ** Critical tasks**: `stack_ensemble_levels=[0, 1, 2] `

**Settings ensemble strategies:**

```python
# Strategy 1: Fast ensembles
quick_ensemble = {
 'num_bag_folds': 3,
 'num_bag_sets': 1,
 'num_stack_levels': 0,
 'stack_ensemble_levels': [0]
}

# Strategy 2: Standard ensembles
standard_ensemble = {
 'num_bag_folds': 5,
 'num_bag_sets': 1,
 'num_stack_levels': 1,
 'stack_ensemble_levels': [0, 1]
}

# Strategy 3: Qualitative ensembles
quality_ensemble = {
 'num_bag_folds': 8,
 'num_bag_sets': 2,
 'num_stack_levels': 1,
 'stack_ensemble_levels': [0, 1]
}

# Strategy 4: Maximum Quality
maximum_ensemble = {
 'num_bag_folds': 10,
 'num_bag_sets': 3,
 'num_stack_levels': 2,
 'stack_ensemble_levels': [0, 1, 2]
}
```

**Optification of data size ensembles:**

```python
# Small data (< 1,000 lines)
small_data_ensemble = {
 'num_bag_folds': 3,
 'num_bag_sets': 1,
 'num_stack_levels': 0,
 'stack_ensemble_levels': [0]
}

# Average data (1000 to 10,000 lines)
medium_data_ensemble = {
 'num_bag_folds': 5,
 'num_bag_sets': 1,
 'num_stack_levels': 1,
 'stack_ensemble_levels': [0, 1]
}

# Big data (> 10,000 lines)
large_data_ensemble = {
 'num_bag_folds': 8,
 'num_bag_sets': 2,
 'num_stack_levels': 1,
 'stack_ensemble_levels': [0, 1]
}
```

**Effects of ensemble on performance:**

```python
# Analysis of the effects of parameters
def analyze_ensemble_impact():
"Analysis of the impact of ensemble parameters on time and quality"

# Formats for testing
 configs = [
{'name': 'Quick', 'num_bag_folds': 3, 'num_bag_sets': 1, 'num_stack_levels': 0},
{'name': 'standard', 'num_bag_folds': 5, 'num_bag_sets': 1, 'num_stack_levels': 1},
{'name': 'Quality', 'num_bag_folds': 8, 'num_bag_sets': 2, 'num_stack_levels': 1},
{'name': 'Maximum', 'num_bag_folds':10, 'num_bag_sets': 3, 'num_stack_levels':2}
 ]

 for config in configs:
(f \n\config['name']} the ensemble:)
 print(f" Bag folds: {config['num_bag_folds']}")
 print(f" Bag sets: {config['num_bag_sets']}")
 print(f" Stack levels: {config['num_stack_levels']}")

# Time estimate (example)
 time_multiplier = (config['num_bag_folds'] * config['num_bag_sets'] *
 (2 ** config['num_stack_levels']))
pint(f) Estimated time: {time_multiplier}x base")

# Launch Analysis
analyze_ensemble_impact()
```

** Recommendations on choice of ensemble strategy:**

```python
# Recommendations on the choice of strategy
def choose_ensemble_strategy(data_size, time_limit, quality_requirement):
"Selection of the ensemble strategy on basic requirements"

 if data_size < 1000:
# Small data are simple ensembles
 return {
 'num_bag_folds': 3,
 'num_bag_sets': 1,
 'num_stack_levels': 0,
 'stack_ensemble_levels': [0]
 }
 elif data_size < 10000:
# Middle data - balanced ensembles
if time_limit < 1800: # Less than 30 minutes
 return {
 'num_bag_folds': 3,
 'num_bag_sets': 1,
 'num_stack_levels': 0,
 'stack_ensemble_levels': [0]
 }
 else:
 return {
 'num_bag_folds': 5,
 'num_bag_sets': 1,
 'num_stack_levels': 1,
 'stack_ensemble_levels': [0, 1]
 }
 else:
# Big data - quality ensemble
 if quality_requirement == 'high':
 return {
 'num_bag_folds': 8,
 'num_bag_sets': 2,
 'num_stack_levels': 1,
 'stack_ensemble_levels': [0, 1]
 }
 else:
 return {
 'num_bag_folds': 5,
 'num_bag_sets': 1,
 'num_stack_levels': 1,
 'stack_ensemble_levels': [0, 1]
 }

# Examples of use
small_data_config = choose_ensemble_strategy(500, 600, 'medium')
medium_data_config = choose_ensemble_strategy(5000, 1800, 'high')
large_data_config = choose_ensemble_strategy(50000, 3600, 'high')

"Conference for Small Data:", small_data_config
"conference for average data:", medium_data_config
"Conference for Big Data:", large_data_config
```

### Castle ensembles

```python
from autogluon.tabular.models import AbstractModel

class CustomEnsembleModel(AbstractModel):
 def __init__(self, **kwargs):
 super().__init__(**kwargs)
 self.models = []

 def _fit(self, X, y, **kwargs):
# Logs of caste ensemble education
 pass

 def _predict(self, X, **kwargs):
# Logs to predict the caste ensemble
 pass

# Use of caste ensemble
predictor.fit(
 train_data,
 custom_ensemble_model=CustomEnsembleModel
)
```

## configurization of resources

### * Management resources

<img src="images/optimized/apple_silicon_optimization.png" alt="Manage resources" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 4: Optimization and Management of Resources in AutoML Gluon*

**Why is the correct configuring of resources important?** Because it determines the performance and effectiveness of learning:

- **CPU Optimization**: Optimizing the use of processors
- **GPU acceleration**: Accelerating learning with graphic processors
- **Memorial Management**: Management Operational Memory
- **Parolle Processing**: Parallel task processing
- **Resource allocation**: Distribution of resources between algorithms
- **Lod Balancing**: Load balance between componentsy

### CPU and GPU Settings

```python
#configuring resources for learning
ag_args_fit = {
'num_cpus': 8, #Number of CPU kernels
'num_gpus': 1, #Number of GPU
'Memory_limit': 16, #Rememise in GB
'time_limit': 3600 # Time limit in seconds
}

predictor.fit(
 train_data,
 ag_args_fit=ag_args_fit
)
```

#### ♪ Detailed describe resource parameters

**parameter `ag_args_fit' - Arguments for learning**

- ** Meaning**: dictionary with resource parameters for model learning
- ** Why you need**: Monitors the use of CPU, GPU, memory and time
- **on default**: `{} &apos; (automatic definition)
- ** Main items**:
- **'num_cpus'**: Number of CPUs for training
- **'num_gpus'**: Number of GPUs for learning
- **'memory_limit'**: Memory Limited in gigabytes
- **'time_limit'**: Time limit in seconds

**parameter `num_cpus' - Number of CPU kernels**

- ** Which means**: Number of CPU kernels, Use for training
- ** Why do you need**: Accelerates learning through parallel calculations
- **on default**: `none' (automatic definition)
- ** Recommended values**:
- ** Minor tasks**: `2-4' kernels
- ** Standard tasks**: `4-8' kernels
- **Big tasks**: `8-16' kernels
- ** Maximum performance**: `16+' kernels
- ** Impact on performance**:
Slow learning, but stable Working.
- ** Lots of kernels**: Rapid learning, but it can be unstable.
- **Optimal**: 70-80% from available kernels
- ** Practical examples**:
- **Development**: `num_cpus=4'
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**parameter `num_gpus' - Amount of GPU**

- ** Which means**: Number of GPUs for learning
- # Why do you need**: Accelerates the learning of neural networks in 10-100 times
- **on default**: `none' (automatic definition)
- ** Recommended values**:
- No GPU**: `0' (CPU only)
- **One GPU**: `1'
- ** Several GPU**: `2+'
- ** Impact on performance**:
- ** Without GPU**: Slow learning of neural networks
- **with GPU**: Rapid learning of neural networks
- ** Plural GPU**: Even faster but harder to confer
- ** Practical examples**:
- **Development**: `num_gpus=1'
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**parameter `memory_limit' - Memory Limited**

- ** Meaning**: Maximum use of RAM in gigabytes
- ** Why you need**: Prevents memory overcrowding, controls resources
- **on default**: `none' (no restrictions)
- ** Recommended values**:
- **Lowered data (< 1MB)**: `2-4' GB
- ** Average data (1-100MB)**: `4-8' GB
- **Big data (100MB-1GB)**: `8-16' GB
- **Very large data (> 1GB)**: `16-32' GB
- ** Impact on performance**:
- # A lot of memory**: Slow Working, possible mistakes
- ** Enough memory**: Fast Working, stability
- ** Lots of memory**: Maximum speed, big data processing
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**parameter `time_limit' - Time limit**

- ** Which means**: Maximum learning time in seconds
- ** Why you need**: Controls the time of learning, prevents endless learning
- **on default**: `none' (no restrictions)
- ** Recommended values**:
- ** Rapid experiments**: `600' (10 minutes)
- ** Standard tasks**: `3600' (1 hour)
- ** Critical tasks**: `7200' (2 hours)
- ** Maximum quality**: `14400' (4 hours)
- **Effect on quality**:
- **Little time**: Basic accuracy, quick results
- ** Average time**: Good accuracy, balanced approach
- **Long time**: Maximum accuracy, best models
- ** Practical examples**:
- ** Prototype**: `time_limit=300'
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**Parmamer `scheduler' - Task Planner**

- ** Which means**: Plann parallel tasks algorithm
- ** Why do you need**: manages the allocation of tasks on resources
- **on default**: `none' (automatic choice)
- ** Capable types**:
- **'LocalScheduler'** - Local Implementation
- **'RayScheduler'** - Distributed by Ray
- ** `DaskScheduler'** - Distributed execution via Dask
- ** Practical examples**:
- **One computer**: `LocalScheduler(num_cpus=8,num_gpus=1)'
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**Settings Resource Strategies:**

```python
# Strategy 1: Minimum resources
minimal_resources = {
 'num_cpus': 2,
 'num_gpus': 0,
 'memory_limit': 4,
 'time_limit': 1800
}

# Strategy 2: Standard resources
standard_resources = {
 'num_cpus': 8,
 'num_gpus': 1,
 'memory_limit': 16,
 'time_limit': 3600
}

# Strategy 3: Maximum resources
maximum_resources = {
 'num_cpus': 16,
 'num_gpus': 2,
 'memory_limit': 32,
 'time_limit': 7200
}
```

**Optification of resources on data size:**

```python
# Small data (< 1,000 lines)
small_data_resources = {
 'num_cpus': 2,
 'num_gpus': 0,
 'memory_limit': 4,
 'time_limit': 600
}

# Average data (1000 to 10,000 lines)
medium_data_resources = {
 'num_cpus': 4,
 'num_gpus': 1,
 'memory_limit': 8,
 'time_limit': 1800
}

# Big data (> 10,000 lines)
large_data_resources = {
 'num_cpus': 8,
 'num_gpus': 1,
 'memory_limit': 16,
 'time_limit': 3600
}
```

**Monitoring resource use:**

```python
# Monitoring resources during training
def monitor_resources():
"Monitoring Resource Utilization"
 import psutil

# CPU use
 cpu_percent = psutil.cpu_percent(interval=1)
 print(f"CPU usage: {cpu_percent}%")

# Memory
 memory = psutil.virtual_memory()
 print(f"Memory usage: {memory.percent}%")

# GPU (if available)
 try:
 import torch
 if torch.cuda.is_available():
 gpu_memory = torch.cuda.memory_allocated() / 1e9
 print(f"GPU memory: {gpu_memory:.2f} GB")
 except importError:
 pass

# Use of Monitoring
predictor.fit(
 train_data,
 ag_args_fit=standard_resources,
 callbacks=[monitor_resources]
)
```

### parallel training

```python
# Configuring parallel learning
from autogluon.core import scheduler

# Local Planner
local_scheduler = scheduler.LocalScheduler(
 num_cpus=8,
 num_gpus=1
)

predictor.fit(
 train_data,
 scheduler=local_scheduler
)
```

#### ♪ Detailed describe Planners

**LocalScheduler - Local Planner**

- ** Which means**: Planner for Single Computer Tasks
- ** Why you need**: Simple and efficient Local Development Plan
- **parameters**:
- **'num_cpus'**: Number of CPU kernels
- **'num_gpus'**: Number of GPUs
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- ** Benefits**: Simplicity Settings, stability
- ** Disadvantages**: Limited scalability

**RayScheduler - Ray Planner**

- ** Meaning**: Planner for distributed execution through Ray
- ** Why do you need**: Scaling up on clusters for big tasks
- **parameters**:
- **'num_cpus'**: Total number of CPU kernels
- **'num_gpus'**: Total GPU
- **'ray_address'**: Ray Cluster Address
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
- **Ray Cluster**: `RayScheduler(num_cpus=32,num_gpus=4, Ray_address='ray://head:10001') `
- ** Benefits**: High scaleability, failure stability
- ** Disadvantages**: Settings complexity, additional dependencies

**DaskScheduler-Dask Planner**

- ** Which means**: Planner for distributed execution via Dask
- Why do you need to scale on clusters with Dask?
- **parameters**:
- **'num_cpus'**: Total number of CPU kernels
- **'num_gpus'**: Total GPU
- **'dask_address'**: Dask Cluster Address
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- ** Benefits**: integration with Dask ecosystem
- ** Disadvantages**: Settings complexity, additional dependencies

**Plancing selection:**

```python
# Recommendations on the choice of Planner
def choose_scheduler(resource_type, cluster_available=False):
"Selection of Planner on Resources"

 if not cluster_available:
# Local development
 return scheduler.LocalScheduler(
 num_cpus=8,
 num_gpus=1
 )
 elif resource_type == 'ray':
# Ray Cluster
 return scheduler.RayScheduler(
 num_cpus=32,
 num_gpus=4,
 ray_address='auto'
 )
 elif resource_type == 'dask':
# Dask Cluster
 return scheduler.DaskScheduler(
 num_cpus=32,
 num_gpus=4,
 dask_address='auto'
 )
 else:
# on default local
 return scheduler.LocalScheduler(
 num_cpus=8,
 num_gpus=1
 )

# Examples of use
local_scheduler = choose_scheduler('local', cluster_available=False)
ray_scheduler = choose_scheduler('ray', cluster_available=True)
dask_scheduler = choose_scheduler('dask', cluster_available=True)
```

## Working with big data

### Inframental education

```python
# Training on Parts
chunk_size = 10000
for i in range(0, len(train_data), chunk_size):
 chunk = train_data[i:i+chunk_size]
 if i == 0:
 predictor.fit(chunk)
 else:
 predictor.fit(chunk, refit_full=True)
```

### Education distributed

```python
#configuring for distributed education
from autogluon.core import scheduler

# Ray Planner for distributed learning
ray_scheduler = scheduler.RayScheduler(
 num_cpus=32,
 num_gpus=4,
 ray_address='auto'
)

predictor.fit(
 train_data,
 scheduler=ray_scheduler
)
```

## configuration validation

♪ ## ♪ Strategies to promote ♪

<img src="images/optimized/validation_methods.png" alt="Validation strategies" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 5: Different strategies for validation and their application*

**Why is the correct strategy of validation important?** Because it ensures the reliability and quality of models:

- **Holdout Planning**: Simple division on train/test (70/30)
- **Cross-Validation**: K-fold cross-evaluation for a more reliable assessment
**Time Series Split**: Special validation for time series
**Stratefied Split**: Maintaining the proportion of classes divided
**Walk-Forward Analysis**: Rolling window for time series
- **Bootstrap Planning**: Random sample with return
- **Monte Carlo Planning**: Multiple random divisions

### Castle strategies validation

```python
from sklearn.model_selection import TimeSeriesSplit

# Temporary validation for time series
def time_series_split(X, y, n_splits=5):
 tscv = TimeSeriesSplit(n_splits=n_splits)
 for train_idx, val_idx in tscv.split(X):
 yield train_idx, val_idx

predictor.fit(
 train_data,
 validation_strategy='custom',
 custom_validation_strategy=time_series_split
)
```

#### ♪ Detailed describe caste-based strategies validation

**parameter `validation_strategy' - Strategy for validation**

- ** Meaning**: Type of strategy of validation for model learning
- ** Why do you need**: Identify how to separate data on learning and validation samples
- **on default**: ``auto'' (automatic choice)
- ** Available**:
- **'auto'** - Automatic choice of strategy
- **`'holdout'`** - Holdout validation
- **'kfold'** - K-fold cross-validation
- **'security'** - Castle strategy
- ** Practical examples**:
- ** Standard tasks**: `validation_strategy='auto'''
- **Temporary rows**: `validation_strategy='custom'''
- ** Unbalanced data**: `validation_strategy='custom''

**parameter `custom_validation_strategy' - Castle strategy**

- ** Meaning**: function for the creation of caste-based data divisions
- ** Why do you need**: Allows specific strategies to be implemented
- **on default**: `none' (not used)
- ** Requirements for functions**:
- **Inductions**: `(X, y, n_splits)' or `(X, y)'
- **Return value**: Cortage generator `(training_idx, val_idx)'
- ** Data Type**: Indexes should be numpy arrays or lists
- ** Practical examples**:
- ** Time series**: `TimeSeriesSplit'
- **Strategized**: `StratefiedKFold'
- **Group**: `GroupKFold'

**TimeSeriesSplit - Temporary validation**

- ** Meaning**: Strategy of validation for time series
- Why do you need to**: Prevents data from leaking from the future in the past
- **parameters**:
- ** `n_splits'**: Number of folds (on default 5)
- **'max_training_size'**: Maximum sample size
- ** `test_size'**: Tests sample size
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
- ** Long rows**: `TimeSeriesSplit(n_splits=10)'
 - **Limited memory**: `TimeSeriesSplit(n_splits=5, max_train_size=1000)`
- ** When to use**:
**Temporary series**: Mandatory for temporary data
- ** Consequent data**: When order matters
- ** Projection**: When to predict the future

**StratefiedKFold - Strategized validation**

- ** Which means**: Strategy of satisfaction with the retention of the proportion of classes
- ** Why you need**: Ensures equal distribution of classes in folds
- **parameters**:
- ** `n_splits'**: Number of folds (on default 5)
- ** `shuffle'**: Do you mix data (on default False)
- **'random_state'**: Seed for reproducibility
- ** Practical examples**:
- ** Unbalanced data**: `StratefiedKFold(n_splits=5, shuffle=True)'
- **Preducibility**: `StratefiedKFold(n_splits=5, shuffle=True, random_state=42)'
- A lot of folds**: `StratefiedKFold(n_splits=10, shuffle=True)'
- ** When to use**:
- ** Unbalanced data**: When classes are presented unevenly
- ** Classification**: for classification purposes
- **Lowered data**: When to maintain class proportions

**GroupKFold - Group validation**

- ** Meaning**: strategy of validation with the integration of groups in data
- ** Why you need**: Prevents the leakage of data between groups
- **parameters**:
- ** `n_splits'**: Number of folds (on default 5)
- ** Practical examples**:
- ** User data**: `GroupKFold(n_splits=5)'
- **Temporary groups**: `GroupKFold(n_splits=3)'
- ** When to use**:
- ** User data**: When there are user groups
** Temporary groups**: When there are temporary groups
- **Geographic data**: When there are geographical groups

** Practical examples of caste strategies:**

```python
# example 1: Temporary validation
def time_series_validation(X, y, n_splits=5):
"Temporary validation for time series"
 from sklearn.model_selection import TimeSeriesSplit

 tscv = TimeSeriesSplit(n_splits=n_splits)
 for train_idx, val_idx in tscv.split(X):
 yield train_idx, val_idx

# example 2: Strategized validation
def stratified_validation(X, y, n_splits=5):
""Stylized validation for unbalanced data""
 from sklearn.model_selection import StratifiedKFold

 skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
 for train_idx, val_idx in skf.split(X, y):
 yield train_idx, val_idx

# example 3: Group appreciation
def group_validation(X, y, groups, n_splits=5):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""G"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")")")")")")")")")")")")")")")")")")")")")")")")"""""""""""""""""""""""""""""""""""""""""""""
 from sklearn.model_selection import GroupKFold

 gkf = GroupKFold(n_splits=n_splits)
 for train_idx, val_idx in gkf.split(X, y, groups):
 yield train_idx, val_idx

# example 4: Castle strategy with filtering
def custom_filtered_validation(X, y, n_splits=5, filter_func=None):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""".
 from sklearn.model_selection import KFold

# Apply filter, if specifed
 if filter_func is not None:
 mask = filter_func(X, y)
 X = X[mask]
 y = y[mask]

 kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
 for train_idx, val_idx in kf.split(X):
 yield train_idx, val_idx
```

** Use of caste-based strategies:**

```python
# Temporary validation for time series
predictor.fit(
 train_data,
 validation_strategy='custom',
 custom_validation_strategy=time_series_validation
)

# Stylized validation for unbalanced data
predictor.fit(
 train_data,
 validation_strategy='custom',
 custom_validation_strategy=stratified_validation
)

# Group appreciation for grouped data
predictor.fit(
 train_data,
 validation_strategy='custom',
 custom_validation_strategy=lambda X, y: group_validation(X, y, groups)
)
```

### Structured validation

```python
from sklearn.model_selection import StratifiedKFold

# Strategized validation
def stratified_split(X, y, n_splits=5):
 skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
 for train_idx, val_idx in skf.split(X, y):
 yield train_idx, val_idx

predictor.fit(
 train_data,
 validation_strategy='custom',
 custom_validation_strategy=stratified_split
)
```

** Supplementary strategies for validation:**

```python
# example 5: development with time windows
def time_window_validation(X, y, window_size=100, step_size=50):
"Validation with temporary windows."
 n_samples = len(X)

 for start in range(0, n_samples - window_size, step_size):
 train_end = start + window_size
 val_start = train_end
 val_end = min(val_start + window_size, n_samples)

 if val_end - val_start < window_size // 2:
 break

 train_idx = List(range(start, train_end))
 val_idx = List(range(val_start, val_end))

 yield train_idx, val_idx

# example 6: appreciation with seasonality
def seasonal_validation(X, y, seasonal_period=12, n_splits=5):
"Validation with seasonality""
 n_samples = len(X)

 for i in range(n_splits):
# Learning sample: all data to a certain point
 train_end = n_samples - (n_splits - i) * seasonal_period
 val_start = train_end
 val_end = val_start + seasonal_period

 if train_end <= 0 or val_end > n_samples:
 continue

 train_idx = List(range(0, train_end))
 val_idx = List(range(val_start, val_end))

 yield train_idx, val_idx

# example 7: appreciation with distribution
def distribution_validation(X, y, n_splits=5, target_distribution=None):
""validation with the distribution of the target variable""
 from sklearn.model_selection import KFold

 if target_distribution is None:
# Use standard K-fold validation
 kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
 for train_idx, val_idx in kf.split(X):
 yield train_idx, val_idx
 else:
# Castle Logs for the maintenance of distribution
# (simplified implementation)
 kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
 for train_idx, val_idx in kf.split(X):
 yield train_idx, val_idx
```

** Recommendations on choice of strategy for validation:**

```python
# Recommendations on the choice of strategy
def choose_validation_strategy(data_type, problem_type, data_size):
"The choice of strategy to promote on database data type and task"

 if data_type == 'time_series':
# Time series - Use temporary validation
 return {
 'validation_strategy': 'custom',
 'custom_validation_strategy': time_series_validation
 }
 elif problem_type == 'classification' and data_size < 1000:
# Small classification - Use stabilised validation
 return {
 'validation_strategy': 'custom',
 'custom_validation_strategy': stratified_validation
 }
 elif data_type == 'grouped':
# Grouped data - Use group validation
 return {
 'validation_strategy': 'custom',
 'custom_validation_strategy': group_validation
 }
 else:
# Standard Data - Use Automatic Strategy
 return {
 'validation_strategy': 'auto'
 }

# Examples of use
time_series_config = choose_validation_strategy('time_series', 'regression', 5000)
classification_config = choose_validation_strategy('tabular', 'classification', 500)
grouped_config = choose_validation_strategy('grouped', 'classification', 2000)
standard_config = choose_validation_strategy('tabular', 'regression', 10000)

"Conference for time series:", time_series_config
"Conference for classification:", classification_config
"Conference for Grouped Data:", grouped_config
standard_config
```

## configuration of features

♪# ♪ Signs engineering ♪

<img src="images/optimized/advanced_topics_overView.png" alt="Engine of the signs" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
♪ Figure 6: process engineering and evidence generation ♪

**Why is the correct engineering of the signs important?** Because qualitative signs can improve the quality of the model on 10-20%:

- **Text Processing**: Text processing (TF-IDF, N-grams, embeddings)
- **Categorical Encoding**: Coding categorical variables (one-hot, label, Target)
- **Numerical Scaling**: Scaling the numbers (standard, min-max, robus)
- **DateTime Features**: Extraction of signs from time data
- **Feature Selection**: Selection of the most informative features
- **Feature Interaction**: range of interactions between axials
- **Missing Value Handling**: Processing missing values

♪## Castome signs generators ♪

```python
from autogluon.features import FeatureGenerator

# Create Castomic Signal Generator
class CustomFeatureGenerator(FeatureGenerator):
 def __init__(self, **kwargs):
 super().__init__(**kwargs)
 self.custom_features = []

 def _generate_features(self, X):
# Castomics
 X['feature_ratio'] = X['feature1'] / (X['feature2'] + 1e-8)
 X['feature_interaction'] = X['feature1'] * X['feature2']
 return X

# Use of caste generator
feature_generator = CustomFeatureGenerator()
train_data_processed = feature_generator.fit_transform(train_data)
```

#### ♪ Detailed descriebe parameters for the generation of signs

**parameter `feature_generator_kwargs' - Arguments of an indicator generator**

- ** Which means**: dictionary with parameters for Settings producing signs
- ** Why do you need**: Control, What types of signs to create and how to process them
- **on default**: `{} &apos; (standard Settings)
- ** Main parameter categories**:
- ** Textmarks**: `enable_text_*', `text_*'
- **Categorial**: `enable_categorical_*', `categorical_*'
== sync, corrected by elderman == @elder_man
- **Temporary signs**: `enable_data_*', `data_*'

** Textmarks - `enable_text_***

- ** Meaning**: parameters for text processing
- ** Why you need**: Automatically create signs from text columns
- ** Main items**:
- **'enable_text_special_features'**: Special textual features
- **'enable_text_ngram_features'**: N-gram signs
- ** `text_ngram_range'**: N-gram range (on default (1, 3))
- ** `text_max_features'**: Maximum number of topics (on default 10,000)
- ** `text_min_df'**: Minimum document frequency (on default 2)
- ** `text_max_df'**: Maximum document frequency (on default 0.95)

**parameter `enable_text_special_features' - Special text features**

- ** Which means**: Includes special features from the text
- ** Why you need**: Creates additional signs for the improvement of model quality
- **on default**: `True' (set)
- **Constructions**:
- ** Length of text**: Number of symbols
- ** Quantity of words**: Number of words in text
- ** Quantity of proposals**: Number of proposals
**Number of capital letters**: Number of capital letters
- **Number of digits**: Number of digits in text
** Quantity of puncture marks**: Number of puncture marks
- ** Practical examples**:
- **Include: `enable_text_special_features=True'
- ** Disable**: `enable_text_special_features=False'
- ** When to use**:
- **Include**: When additional signs are needed
- ** Disable**: When the text not is important

**parameter `enable_text_ngram_features' - N-gram signs**

- ** Which means**: Including creative N-gram features from the text
- ** Why you need**: Creates signs on base sequences of words/symbols
- **on default**: `True' (set)
- **Constructions**:
- **Unigrams**: Selected words
- **Bigrams**: Words
- **Trigrams**: Three words
**Character n-grams**: Symbol sequences
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
- ** Disable**: `enable_text_ngram_features=False'
- ** When to use**:
- **Include**: When the order of words is important
- ** Disable**: When the order of words is not important

**parameter `text_ngram_range' - N-gram range**

- ** Meaning**: N-gram size range for the creation of signs
- ** Why you need**: Controls the complexity of the text signs
- **on default**: `(1, 3)' (unigrams, bigrams, trigrams)
- ** Recommended values**:
- ** Simple texts**: `(1, 2)' (unigrams, bigrams)
- ** Standard texts**: `(1, 3)' (unigrams, bigrams, trigrams)
- ** Complex texts**: `(1, 4)' (unigrams, bigrams, trigrams, 4-grams)
- ** Impact on performance**:
- **Little range**: Faster, less signs
- **Big range**: Slower, bigger signs
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**parameter `text_max_features' - Maximum number of topics**

- ** Which means**: Maximum number of text features
- ** Why do you need**: Limits the number of signs for prevention of retraining
- **on default**: `10000' (10,000 features)
- ** Recommended values**:
- **Little texts**: `1000-5000' features
- ** Standard texts**: `5000-10000' characteristics
- **Big texts**: `10000-50000' features
- **Effect on quality**:
- ** Few signs**: There may be a lack of education
- ** Lots of signs**: Could be retraining.
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**parameter `text_min_df' - Minimum frequency of document**

- ** Meaning**: Minimum frequency of appearance of term in documents
- ** Why you need**: Filters out rare terms
- **on default**: `2' (the term should appear at least in 2 documents)
- ** Recommended values**:
- **Little data**: `1-2' (insert rare terms)
- ** Standard data**: `2-5' (standard filtering)
- **Big data**: `5-10' (strut filtering)
- **Effect on quality**:
- ** Low**: More signs, maybe noise
- ** High**: Less signs, less noise
- ** Practical examples**:
- ** Including rare terms**: `text_min_df=1'
- ** Standard filtering**: `text_min_df=2'
- **Star filtering**: `text_min_df=5'

**parameter `text_max_df' - Maximum document frequency**

- ** Which means**: Maximum frequency of appearance of the term in documents
- ** Why you need**: Filters out too many terms
- **on default**: `0.95' (term not should appear in 95% of documents)
- ** Recommended values**:
- ** Standard data**: `0.95' (standard filtering)
- **Big data**: `0.90' (strut filtering)
- **Very large data**: `0.85' (very strict filtering)
- **Effect on quality**:
- ** High**: More signs, maybe noise
- ** Low**: Less signs, less noise
- ** Practical examples**:
- ** Standard filtering**: `text_max_df=0.95'
== sync, corrected by elderman == @elder_man
- **Very strict filtering**: `text_max_df=0.85'

**Categorial signs - `enable_categorical_***

- ** Meaning**: parameters for the processing of categorical data
- ** Why do you need**: Automatically create signs from categorical columns
- ** Main items**:
- **/enable_categorical_encoding'**: Coding categorical features
**/ `categorical_encoding'**: Type of coding (on default 'auto')
- ** `categorical_max_levels'**: Maximum number of levels (on default 100)

**parameter `enable_categorical_encoding' - Coded categorical features**

- ** Which means**: Includes automatic coding of categorical features
- What do you need**: converts categorical data into numerical data
- **on default**: `True' (set)
- ** Code numbers**:
- **One-hot encoding**: Creates binary signs for each level
- **Label encoding**: Adds numerical tags to levels
- **Target encoding**: Coded on bases target variable
- ** Practical examples**:
- **Include: `enable_categorical_encoding=True'
- ** Disable**: `enable_categorical_encoded=False'
- ** When to use**:
- **Include**: When there are categorical data
- ** Disable**: When the categorical data are already encoded

**parameter `categorical_encoding' - Type of coding**

- ** Meaning**: Type of coding for categorical characteristics
- ** Why you need**: Chooses the best method of coding
- **on default**: ``auto'' (automatic choice)
- ** Available**:
- **'auto'** - Automatic choice
 - **`'onehot'`** - One-hot encoding
 - **`'label'`** - Label encoding
 - **`'target'`** - Target encoding
- ** Practical examples**:
- **Automatic choice**: `categorical_incoding='auto''
 - **One-hot encoding**: `categorical_encoding='onehot'`
 - **Label encoding**: `categorical_encoding='label'`
- ** When to use**:
**auto**: for most cases
- **onehot**: For categorical data with a small number of levels
- **label**: For categorical data with more levels

**parameter `categorical_max_levels' - Maximum number of levels**

- ** Meaning**: Maximum number of levels for categorical signature
- What's the point?
- **on default**: `100' (100 levels)
- ** Recommended values**:
- **Lowered data**: `10-50' levels
- ** Standard data**: `50-100' levels
- **Big data**: `100-500' levels
- ** Impact on performance**:
- **Lower levels**: Faster, less signs
- ** Many levels**: Slower, more signs
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**Personal characteristics - `enable_numeric_***

- ** Meaning**: parameters for the processing of numerical data
- ** Why do you need**: Automatically create signs from numerical columns
- ** Main items**:
- **/enable_numeric_imputation'**: Filling missing values
- **/enable_numeric_scaling'**: Scale of numerical features
- **'numeric_imputation'**: Method of filling missing values

**parameter `enable_numeric_imputation' - Filling missing values**

- ** Meaning**: Includes automatic completion of missing values
- ** Why you need**: Processing missing values in numerical data
- **on default**: `True' (set)
- **methods filling**:
- **Mean imputation**: Filling the average value
- **Medic imputation**: Filling the median
- **Mode imputation**: Fashion filling
- **Forward will**: Filling in previous value
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
- ** Disable**: `enable_numeric_imputation=False'
- ** When to use**:
- **Include**: When missing values are available
- ** Disable**: No missing values

**parameter `enable_numeric_scaling' - Scale of numerical features**

- ** Meaning**: Includes automatic scaling of numbers
- Why do you need**: Normalizes numbers for better performance
- **on default**: `True' (set)
- ** Scales**:
 - **Standard scaling**: (x - mean) / std
 - **Min-max scaling**: (x - min) / (max - min)
 - **Robust scaling**: (x - median) / IQR
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
- ** Disable**: `enable_numeric_scaling'=False'
- ** When to use**:
- **Include**: When numbers vary in scale
- ** Disable**: When the numbers have already been normalized

** Temporary signs - `enable_data_***

- ** Meaning**: variables for processing temporary data
- ** Why you need**: Automatically create signs from temporary columns
- ** Main items**:
- **/enable_data_features'**: time item
- **'data_features'**: Types of time signs

**parameter `enable_data_features' - time item**

- ** Which means**: Includes the output from the time data
- ** Why you need**: Extracts useful information from temporary columns
- **on default**: `True' (set)
- **Constructions**:
- ** Year**: Year from date
- ** Month**: Month from date
- ** Day**: Day out of date
- ** Day of the Week**: Day of the Week
- **Hour**: Timed hour
- **minutesa**: minutesa from time
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
- ** Disable**: `enable_data_features=False'
- ** When to use**:
- **Include**: When there are temporary data
- ** Disable**: When temporary data not matters

** Practical examples Settings of signs:**

```python
# example 1: Standard configration
standard_features = {
 'enable_text_special_features': True,
 'enable_text_ngram_features': True,
 'text_ngram_range': (1, 3),
 'text_max_features': 10000,
 'text_min_df': 2,
 'text_max_df': 0.95,
 'enable_categorical_encoding': True,
 'categorical_encoding': 'auto',
 'categorical_max_levels': 100,
 'enable_numeric_imputation': True,
 'enable_numeric_scaling': True,
 'enable_datetime_features': True
}

# example 2: Rapid configuring
quick_features = {
 'enable_text_special_features': False,
 'enable_text_ngram_features': True,
 'text_ngram_range': (1, 2),
 'text_max_features': 1000,
 'text_min_df': 5,
 'text_max_df': 0.90,
 'enable_categorical_encoding': True,
 'categorical_encoding': 'label',
 'categorical_max_levels': 50,
 'enable_numeric_imputation': True,
 'enable_numeric_scaling': False,
 'enable_datetime_features': False
}

# example 3: Detailed conference
Detailed_features = {
 'enable_text_special_features': True,
 'enable_text_ngram_features': True,
 'text_ngram_range': (1, 4),
 'text_max_features': 50000,
 'text_min_df': 1,
 'text_max_df': 0.85,
 'enable_categorical_encoding': True,
 'categorical_encoding': 'onehot',
 'categorical_max_levels': 500,
 'enable_numeric_imputation': True,
 'enable_numeric_scaling': True,
 'enable_datetime_features': True
}
```

** Use of indicator generation settings:**

```python
# Standard configuration
predictor.fit(
 train_data,
 feature_generator_kwargs=standard_features
)

# Rapid configuration
predictor.fit(
 train_data,
 feature_generator_kwargs=quick_features
)

# Detailed configuration
predictor.fit(
 train_data,
 feature_generator_kwargs=Detailed_features
)
```

### Text processing

```python
# configurization of text processing
text_features = {
 'enable_text_special_features': True,
 'enable_text_ngram_features': True,
 'text_ngram_range': (1, 3),
 'text_max_features': 10000,
 'text_min_df': 2,
 'text_max_df': 0.95
}

predictor.fit(
 train_data,
 feature_generator_kwargs=text_features
)
```

** Additional paragraphs of text processing:**

```python
# Expanded text processing
advanced_text_features = {
# Main variables
 'enable_text_special_features': True,
 'enable_text_ngram_features': True,
 'text_ngram_range': (1, 3),
 'text_max_features': 10000,
 'text_min_df': 2,
 'text_max_df': 0.95,

# Additional parameters
'Text_stop_words': 'english', #Stopword
'Text_lowcase':True, #Aligning to lower register
'Text_strip_accents':True, #remove accents
'Text_token_pattern': r'\b\w+\b', #Tokenization Patterne
'Text_analyzer': 'word', #Analisistor (word/char)
'Text_binary': False, #Binary signs
'Text_Use_idf':True, #Use IDF
'Text_smooth_idf':True, # smoothing IDF
'Text_sublinary_tf':False, #Subline TF
'Text_norm': 'l2' # Normalization (l1/l2)
}

# Use of expanded Settings
predictor.fit(
 train_data,
 feature_generator_kwargs=advanced_text_features
)
```

** Recommendations on the selection of indicator generation parameters:**

```python
# Recommendations on the choice of parameters
def choose_feature_parameters(data_type, text_columns, categorical_columns, numeric_columns):
"Selection of parameters for the generation of topics on database data type""

 if data_type == 'text_heavy':
# Textal data - accent on text signs
 return {
 'enable_text_special_features': True,
 'enable_text_ngram_features': True,
 'text_ngram_range': (1, 3),
 'text_max_features': 20000,
 'text_min_df': 2,
 'text_max_df': 0.95,
 'enable_categorical_encoding': True,
 'categorical_encoding': 'auto',
 'categorical_max_levels': 100,
 'enable_numeric_imputation': True,
 'enable_numeric_scaling': True,
 'enable_datetime_features': True
 }
 elif data_type == 'categorical_heavy':
# Categorical data - accent on categorical signs
 return {
 'enable_text_special_features': False,
 'enable_text_ngram_features': False,
 'enable_categorical_encoding': True,
 'categorical_encoding': 'onehot',
 'categorical_max_levels': 200,
 'enable_numeric_imputation': True,
 'enable_numeric_scaling': True,
 'enable_datetime_features': True
 }
 elif data_type == 'numeric_heavy':
# Numerical data - accent on numerals
 return {
 'enable_text_special_features': False,
 'enable_text_ngram_features': False,
 'enable_categorical_encoding': True,
 'categorical_encoding': 'label',
 'categorical_max_levels': 50,
 'enable_numeric_imputation': True,
 'enable_numeric_scaling': True,
 'enable_datetime_features': True
 }
 else:
# Mixed Data - Balanced configration
 return {
 'enable_text_special_features': True,
 'enable_text_ngram_features': True,
 'text_ngram_range': (1, 3),
 'text_max_features': 10000,
 'text_min_df': 2,
 'text_max_df': 0.95,
 'enable_categorical_encoding': True,
 'categorical_encoding': 'auto',
 'categorical_max_levels': 100,
 'enable_numeric_imputation': True,
 'enable_numeric_scaling': True,
 'enable_datetime_features': True
 }

# Examples of use
text_config = choose_feature_parameters('text_heavy', ['text_col'], [], [])
categorical_config = choose_feature_parameters('categorical_heavy', [], ['cat_col'], [])
numeric_config = choose_feature_parameters('numeric_heavy', [], [], ['num_col'])
mixed_config = choose_feature_parameters('mixed', ['text_col'], ['cat_col'], ['num_col'])

print("configuration for textual data:", text_config)
"Conference for categorical data:", classification_config)
"configration for numerical data:", numeric_config
"configuration for mixed data:", mixed_config
```

## configuration metric

### ♪ conference metric

<img src="images/optimized/metrics_Detained.png" alt="conference metric" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 7: configuring and configuring quality assessment metric*

**Why is the correct configuring metric important?** Because metrics determine how the quality of the model is assessed:

**ClassificationMetrics**: metrics for classification tasks (accuracy, preparation, recall, F1, ROC-AUC)
- **RegressionMetrics**: metrics for regression tasks (RMSE, MAE, MAPE, R2)
- **Custom Metrics**: Castle metrics for specific tasks
- **Multi-Metric Evolution**: Evaluation on Several Meths Simultaneously
- **Metric Weating**: Weighting metrics on importance
- **Threshold Optimization**: Optimization of thresholds for metrics
- **Metric Monitoring**: Monitoring metric during training

### Castle metrics

```python
from autogluon.core import Scorer

# Create caste metrics
def custom_metric(y_true, y_pred):
"Castom metric for quality assessment"
# Your Logsk calculation of metrics
 return score

custom_scorer = Scorer(
 name='custom_metric',
 score_func=custom_metric,
 greater_is_better=True
)

predictor.fit(
 train_data,
 eval_metric=custom_scorer
)
```

♪## ♪ Detailed describe Settings metric

**parameter `eval_metric'-Metric evaluation**

- ** Meaning**: Metrique for model quality evaluation
- ** Why you need**: Identifys how to measure model quality
- **on default**: ``auto'' (automatic choice)
- **Tips of metric**:
- ** Line**: Name of built-in metrics
- **List**: Several metrics
- **Scorer**: Castle Meth
- ** Practical examples**:
- One metric**: `eval_metric='accuracy''
- ** Several metrics**: `eval_metric=['accuracy', 'f1', 'roc_auc']
== sync, corrected by elderman == @elder_man

**Installed metrics for classification:**

- **'accuracy'** - Accuracy (right predictions / total)
- **'f1'** - F1-measures (harmonic average precinct and recall)
- **'f1_macro'** - F1 measures with macro-averaging
- **'f1_micro'** - F1 measures with micro-averaging
- **'f1_weighted'** - F1 measures with weighted averaging
- **'preception'** - Accuracy (trie positives / (tre positives + false positives))
- **'recall'** - Fullness (tru positives / (tree positives + false delegations))
- **'roc_auc'** - Area under ROC creve
- **'log_loss'** - Logarithmic function of losses
- **'balanced_accuracy'** - Balanced accuracy

**Installed metrics for regression:**

- **'rmese'** - The root of the mid-quadratic error
- **'mae'** - Average absolute error
- **'mape'** - Average absolute percentage error
- **'r2'** - Determination factor
- **'pearsonr'** - Pearson Correlation
- **'searmanr'** - Spearman Correlation

**parameter `Scorer' - Castle Meth**

- ** Which means**: Class for the creation of caste-based metrics
- ** Why do you need**: Allows you to create your own metrics evaluation
- ** Main items**:
- **'name'**: Name of metrics
- **'score_fund'**: function calculation of metrics
- **/green_is_better'**: Is greater value better
- ** `needs_proba'**: Is probability required
- ** `needs_threshold'**: Do you need a threshold

**parameter `name' - Name of metrics**

- What does that mean?
- ** Why do you need**: Identifies metrics in logs and results
- **on default**: `none' (automatic name)
- ** Recommendations**:
- **Unique**: Name should be unique
- ** Description**: The name must describe the metric
- **Quantity**: The title must be short
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- ** Automatic**: `name= None'

**parameter `score_fund'-function calculation of metrics**

- ** Meaning**: function for calculation of the metrics value
- Why do you need to do this?
- ** Requirements for functions**:
- **Induction paragraphs**: `(y_tree, y_pred)' or '(y_tree, y_pred, y_pred_proba)'
- **Return value**: Numerical value of metrics
- ** Error processing**: function must process errors
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- **Methrics with probabilities**: `score_fund=lambda y_tree, y_pred, y_pred_proba: roc_auc_score(y_tre, y_pred_proba)'

**parameter `greener_is_better' - Optimization direction**

- What does that mean?
- ** Why do you need**: Sets the direction of optimization
- **on default**: `True' (larger value better)
- ** Practical examples**:
- **Definity**: `greener_is_better=True' (more accuracy = better)
- ** Mistake**: `greener_is_better=False' (less error = better)
- ** When to use**:
- **True**: for a metric where more meaning is better
- **False**: for a metric where less value is better

**parameter `needs_proba' - Do you need probability**

- ** Which means**: Indicates whether probabilities are needed for calculation of metrics
- ** Why you need**: Determines whether to transfer probabilities in function
- **on default**: `False' (no probability needed)
- ** Practical examples**:
- **Turity**: `needs_proba=False' (needs to predict)
- **ROC AUC**: `needs_proba=True' (required probability)
- ** When to use**:
- **False**: For a metric that works with predictions
- **True**: for a metric that works with probabilities

**parameter `needs_threshold' - Do you need a threshold**

- ** Which means**: indicates whether a threshold for calculation of metrics is needed.
- ** Why do you need**: Determines whether to transfer the threshold in function
- **on default**: `False' (no threshold required)
- ** Practical examples**:
- **Totality**: `needs_threshold=False' (no threshold needed)
- **F1-measure**: `needs_threshold=True' (a threshold is needed)
- ** When to use**:
- **False**: for metrics not requiring a threshold
- **True**: for metrics requiring a threshold

** Practical examples of caste-based metrics:**

```python
# example 1: Simple caste meth
def custom_accuracy(y_true, y_pred):
""Castomic accuracy with additional Logska""
 from sklearn.metrics import accuracy_score

# Additional Logs
 if len(y_true) == 0:
 return 0.0

 return accuracy_score(y_true, y_pred)

custom_accuracy_scorer = Scorer(
 name='custom_accuracy',
 score_func=custom_accuracy,
 greater_is_better=True
)

# example 2: Meterics with probabilities
def custom_roc_auc(y_true, y_pred, y_pred_proba):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 from sklearn.metrics import roc_auc_score

# Additional processing
 if y_pred_proba is None:
 return 0.0

 try:
 return roc_auc_score(y_true, y_pred_proba)
 except ValueError:
 return 0.0

custom_roc_auc_scorer = Scorer(
 name='custom_roc_auc',
 score_func=custom_roc_auc,
 greater_is_better=True,
 needs_proba=True
)

# example 3: Meterics with the threshold
def custom_f1_with_threshold(y_true, y_pred, threshold=0.5):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""."""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 from sklearn.metrics import f1_score

# Applying the threshold
 y_pred_binary = (y_pred >= threshold).astype(int)

 return f1_score(y_true, y_pred_binary)

custom_f1_scorer = Scorer(
 name='custom_f1',
 score_func=custom_f1_with_threshold,
 greater_is_better=True,
 needs_threshold=True
)
```

** Use of caste-based metrics:**

```python
# One caste meth
predictor.fit(
 train_data,
 eval_metric=custom_accuracy_scorer
)

# A few caste meths
predictor.fit(
 train_data,
 eval_metric=[custom_accuracy_scorer, custom_roc_auc_scorer]
)

# Mixed metrics (integral + caste)
predictor.fit(
 train_data,
 eval_metric=['accuracy', custom_f1_scorer, 'roc_auc']
)
```

### Multiple metrics

```python
# Learning with several metrics
predictor.fit(
 train_data,
 eval_metric=['accuracy', 'f1', 'roc_auc']
)
```

**Detail describe multiple metrics:**

**parameter `eval_metric' - List metric**

- ** Meaning**: List metric for model quality evaluation
- ** Why do you need**: Allows the model to be evaluated on multiple criteria
- **on default**: ``auto'' (automatic choice)
- **Tips of list elements**:
- **string**: Names of built-in metrics
== sync, corrected by elderman == @elder_man
- ** Mixed**: Combination of fixed and caste-based
- ** Practical examples**:
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man

**Methric selection strategies:**

```python
# Strategy 1: Basic metrics
basic_metrics = ['accuracy', 'f1', 'roc_auc']

# Strategy 2: Detailed metrics
Detailed_metrics = [
 'accuracy', 'f1', 'f1_macro', 'f1_micro', 'f1_weighted',
 'precision', 'recall', 'roc_auc', 'log_loss'
]

# Strategy 3: Specialized metrics
specialized_metrics = [
'f1_macro', #for unbalanced data
'roc_auc', #for ranking
'log_loss' # for probabilities
]

# Strategy 4: Castle metrics
custom_metrics = [
 custom_accuracy_scorer,
 custom_roc_auc_scorer,
 custom_f1_scorer
]
```

**Optification on task type:**

```python
# Classification - Standard metrics
classification_metrics = ['accuracy', 'f1', 'roc_auc']

# Classification - unbalanced data
imbalanced_metrics = ['f1_macro', 'roc_auc', 'balanced_accuracy']

# Classification - ranking
ranking_metrics = ['roc_auc', 'log_loss', 'precision']

# Regression is standard metrics
regression_metrics = ['rmse', 'mae', 'r2']

# Regression - percentage errors
percentage_metrics = ['mape', 'mae', 'r2']

# Regression is a correlation
correlation_metrics = ['pearsonr', 'spearmanr', 'r2']
```

**Monitoring multiple metrics:**

```python
# Callback for Monitoring metric
def metrics_monitor(epoch, Logs):
"Monitoring Metrics during Studying."
 print(f"Epoch {epoch}:")
 for metric_name, metric_value in Logs.items():
 print(f" {metric_name}: {metric_value:.4f}")

# Learning with Monitoring
predictor.fit(
 train_data,
 eval_metric=['accuracy', 'f1', 'roc_auc'],
 callbacks=[metrics_monitor]
)
```

** Recommendations on choice of metric:**

```python
# Recommendations on choice of metric
def choose_metrics(problem_type, data_characteristics):
"Selection of a metric on database type of task and characteristics of data""

 if problem_type == 'classification':
 if data_characteristics == 'balanced':
 return ['accuracy', 'f1', 'roc_auc']
 elif data_characteristics == 'imbalanced':
 return ['f1_macro', 'roc_auc', 'balanced_accuracy']
 elif data_characteristics == 'ranking':
 return ['roc_auc', 'log_loss', 'precision']
 else:
 return ['accuracy', 'f1', 'roc_auc']
 elif problem_type == 'regression':
 if data_characteristics == 'standard':
 return ['rmse', 'mae', 'r2']
 elif data_characteristics == 'percentage':
 return ['mape', 'mae', 'r2']
 elif data_characteristics == 'correlation':
 return ['pearsonr', 'spearmanr', 'r2']
 else:
 return ['rmse', 'mae', 'r2']
 else:
 return ['accuracy', 'f1', 'roc_auc']

# Examples of use
balanced_classification = choose_metrics('classification', 'balanced')
imbalanced_classification = choose_metrics('classification', 'imbalanced')
standard_regression = choose_metrics('regression', 'standard')
percentage_regression = choose_metrics('regression', 'percentage')

"Metrics for Balanced Classification:", based_classification
"metrics for unbalanced classification:"
"metrics for standard regression:", standard_regression
"metrics for percentage regression:" percentage_regression)
```

** Additional capabilities of Settings metric:**

```python
# configuring the weight of the metric
weighted_metrics = {
 'accuracy': 0.4,
 'f1': 0.3,
 'roc_auc': 0.3
}

# Configuring thresholds for metrics
threshold_metrics = {
 'f1': 0.5,
 'precision': 0.6,
 'recall': 0.4
}

# configuration averaging for metrics
averaging_metrics = {
 'f1': 'macro',
 'precision': 'weighted',
 'recall': 'micro'
}
```

** Use of metric settings:**

```python
# Learning with weights of metrics
predictor.fit(
 train_data,
 eval_metric=weighted_metrics
)

# Training with thresholds of metrics
predictor.fit(
 train_data,
 eval_metric=threshold_metrics
)

# Learning with average metric
predictor.fit(
 train_data,
 eval_metric=averaging_metrics
)
```

## configuring Logs

### Detailed Logs

```python
import logging

# configuring Logs
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 handlers=[
 logging.FileHandler('autogluon.log'),
 logging.StreamHandler()
 ]
)

# Learning with detailed Logs
predictor.fit(
 train_data,
verbosity=3, # Maximum Logs
 log_to_file=True
)
```

### Monitoring learning

```python
# Callback for Monitoring
def training_monitor(epoch, Logs):
 print(f"Epoch {epoch}: {Logs}")

predictor.fit(
 train_data,
 callbacks=[training_monitor]
)
```

## configuring for sale

♪ ♪ ♪ Sold to configuration ♪

<img src="images/optimized/producation_architecture.png" alt="Selled configuration" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
♪ Figure 8: Architecturation and configuring for sale ♪

**Why is the correct sale of configuration important?** Because it ensures stability and performance in real terms:

- **Model Optimization**: Optimizing the model for rapid inference
- **Resource Consultants**: Accounting for resource constraints in sales
- **Scalability**: Scale for heavy loads
- **Monitoring**: Monitoring performance and quality
- **Versioning**: Management with model versions
- **A/B test**: Testing different versions of models
- **Rollback Strategy**: Rollback Strategy for Problems

### Optimization for the Depletion

```python
# Settings for sale
production_config = {
 'presets': 'optimize_for_deployment',
 'ag_args_fit': {
 'num_cpus': 4,
 'num_gpus': 0,
 'memory_limit': 8
 },
 'hyperparameters': {
 'GBM': [{'num_boost_round': 100}],
 'XGB': [{'n_estimators': 100}],
 'RF': [{'n_estimators': 100}]
 }
}

predictor.fit(train_data, **production_config)
```

♪ ♪ Model compression ♪

```python
# Maintaining a compressed model
predictor.save(
 'production_model',
 save_space=True,
 compress=True
)
```

## examples advanced configuration

### ♪ Integrated configration

<img src="images/optimized/production_comparison.png" alt="integrated conference" style"="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
♪ Figure 9: Comparson of different configuration approaches ♪

**Why are the examples of the complex configuration important?** Because they show how to combine all Settings for maximum efficiency:

- **Hyperparameter Tuning**: Thin configurization of algorithm parameters
- **Ensemble Configuration**: Optimal configurization ensemble
- **Resource Management**: Effective Management Resources
- **Feature Engineering**: Advanced Engineering of Signs
- **Validation Strategy**: A reliable strategy for validation
- **Metrics Selection**: Selection of suitable metrics
- ** Production Optimization**: Optimization for sales

### Full configuring for sale

```python
from autogluon.tabular import TabularPredictor
import pandas as pd

# the pre-indexor with full configuration
predictor = TabularPredictor(
 label='target',
 problem_type='auto',
 eval_metric='auto',
 path='./models',
 verbosity=2
)

# Advanced hyperparameters
advanced_hyperparameters = {
 'GBM': [
 {
 'num_boost_round': 1000,
 'num_leaves': 31,
 'learning_rate': 0.1,
 'feature_fraction': 0.9,
 'bagging_fraction': 0.8,
 'bagging_freq': 5,
 'min_data_in_leaf': 20,
 'min_sum_hessian_in_leaf': 1e-3,
 'lambda_l1': 0.0,
 'lambda_l2': 0.0,
 'min_gain_to_split': 0.0,
 'max_depth': -1,
 'save_binary': True,
 'seed': 0,
 'feature_fraction_seed': 2,
 'bagging_seed': 3,
 'drop_seed': 4,
 'verbose': -1,
 'keep_training_booster': False
 }
 ],
 'CAT': [
 {
 'iterations': 1000,
 'learning_rate': 0.1,
 'depth': 6,
 'l2_leaf_reg': 3.0,
 'bootstrap_type': 'Bayesian',
 'random_strength': 1.0,
 'bagging_temperature': 1.0,
 'od_type': 'Iter',
 'od_wait': 20,
 'verbose': False
 }
 ],
 'XGB': [
 {
 'n_estimators': 1000,
 'max_depth': 6,
 'learning_rate': 0.1,
 'subsample': 0.8,
 'colsample_bytree': 0.8,
 'reg_alpha': 0.0,
 'reg_lambda': 1.0,
 'random_state': 0
 }
 ]
}

# Settings of resources
ag_args_fit = {
 'num_cpus': 8,
 'num_gpus': 1,
 'memory_limit': 16,
 'time_limit': 3600
}

# Training with full configuration
predictor.fit(
 train_data,
 hyperparameters=advanced_hyperparameters,
 num_bag_folds=5,
 num_bag_sets=2,
 num_stack_levels=1,
 ag_args_fit=ag_args_fit,
 presets='best_quality',
 time_limit=3600,
 holdout_frac=0.2,
 verbosity=2
)
```

## Next steps

After advanced configuration, go to:
- [Work with metrics](./04_metrics.md)
- [Methods of validation](./05_validation.md)
- [Selled by default](./06_production.md)
