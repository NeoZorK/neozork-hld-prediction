# Examples of AutoML Gluon

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Whoy examples is critical

**Why do 90% of developers start with examples and not with documentation?** Because examples show how the Workinget theory on practice. It's like driving learning - first you watch how others drive.

### Problems without practical examples
- ** Long study**: Months on understanding basic concepts
- ** Misuses in implementation**: Misuse of API
- ** Ineffective solutions**: Inventing a bicycle
- ** Disappointing**: Complexity scares off the beginners

### The benefits of good examples
- ** Quick start**: from ideas to Working Code over hours
- **Regular Pathways**: Studying best practices on examples
- **Confidence**: Understanding how everything is Working
- **Inspiration**: Ideas for their own projects

## Introduction in examples

<img src="images/optimized/metrics_comparison_Detained.png" alt="comparison metric and tasks" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 1: Comparative metric for classification and regression - ROC Curve, Prection-Recall, Conference Matrix, metrics regression*

**Why examples is the language of machine lightning?** Because they translate complex algorithms in understandable numbers. It's like an interpreter between technical details and business results.

**Tips of examples in AutoML Gloon:**
- ** Basic examples**: Simple tasks for understanding the framework
- ** Advanced examples**: Complex scenarios for experienced users
- ** Real projects**: Full solutions to real business challenges
- **Specialized examples**: for specific domains (health, finance)

In this section, the practical uses of AutoML Gluon for various tasks are presented. Each example includes a complete code, explanations and best practices.

## example 1: Bank client classification

<img src="images/optimized/bank_classification_Analysis.png" alt="Bank example" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 2: example classification of bank customers - ROC Curve, Precion-Recall, Conference Matrix, importance of signs*

Because it's a classic example ML in finance -- understandable, important, and with clear business metrics.

** Key aspects of bank ML:**
- ** Financial risk**: Client credit rating
- ** Regulation**: Compliance with banking standards
- ** Interpretation**: Explainability of decisions for regulators
- **justice**: Prevention of discrimination
- **Monitoring**: Real-time quality tracking
- **A/B testing**: comparison of models on real data

### The challenge
Because the wrong decision could cost the bank millions of dollars, it's like a medical diagnosis, but for money.

Probability of bank client default on financial indicators.

** Business context:**
- **Goal**: minimize losses from bad loans
- **Methric**: ROC-AUC (important accuracy for positive cases)
- ** Cost of error**: False negative result is more than false positive
- ** Data item**: Usually 100K-1M records

### data
Because real bank data are confidential, but Structure and Pathers remain the same.

```python
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularPredictor
import matplotlib.pyplot as plt
import seaborn as sns

# creative synthetic data for banking task
def create_bank_data(n_samples=10000):
 """
quality of synthetic bank data - simulating real bank data

 Parameters:
 -----------
 n_samples : int, default=10000
Sample size for generation:
- 1000-5000: Small datasets (rapid testing)
- 5000-20000: Average datesets (quality and speed balance)
- 20000+: large datasets (maximum quality)

 Returns:
 --------
 pd.dataFrame
Synthetic bank data:
- Numbers: age, income, credit rating, debt/income
- Categories: status of employment, education, marital status
- Timelines: date of application
- Target variable: default_risk (0/1)

 Notes:
 ------
Structure of banking data:
- 20 numbers (age, income, credit rating, etc.)
- 15 informative features (influence default)
- 5 excess (corred by informative)
- 3 absolute priority (status, education, marital status)
- Time tags for Trends

Business context:
- Task: Placing default on credit
- Target variable: default_risk (0 - no default, 1 - default)
- Application: credit adjustment, risk management
 """

# Data generation with realistic parameters
 X, y = make_classification(
n_samples=n_samples, # Sample size
n_features=20, #Number of topics
n_informative=15, #Informational signs (important for predictions)
n_redendant=5, #Excess (corred)
n_classes=2, # Binary classification (defolt/not default)
Random_state=42 # Reproducibility of results
 )

# Create dataFrame with meaningful names
 feature_names = [
 'age', 'income', 'credit_score', 'debt_ratio', 'employment_years',
 'loan_amount', 'interest_rate', 'payment_history', 'savings_balance',
 'investment_value', 'credit_cards', 'late_payments', 'bankruptcies',
 'foreclosures', 'collections', 'inquiries', 'credit_utilization',
 'account_age', 'payment_frequency', 'credit_mix'
 ]

 data = pd.dataFrame(X, columns=feature_names)
 data['default_risk'] = y

# add categorical variables
 data['employment_status'] = np.random.choice(['employed', 'unemployed', 'self_employed'], n_samples)
 data['education'] = np.random.choice(['high_school', 'bachelor', 'master', 'phd'], n_samples)
 data['marital_status'] = np.random.choice(['single', 'married', 'divorced'], n_samples)

# add time variables
 data['application_date'] = pd.date_range('2020-01-01', periods=n_samples, freq='D')

 return data

# data quality
bank_data = create_bank_data(10000)
print("Bank data shape:", bank_data.shape)
print("Default rate:", bank_data['default_risk'].mean())
```

### Data preparation
```python
def prepare_bank_data(data):
 """
Preparation of bank data for machine lightning

 Parameters:
 -----------
 data : pd.dataFrame
Reference bank data:
- Contains numerical and categorical characteristics
- May contain missing values
- May contain emissions

 Returns:
 --------
 pd.dataFrame
Data compiled:
- Missed values filled
- New signs created
- OWrkingne emissions
- Ready for model training.

 Notes:
 ------
Data production process:
1. Filling out the missing median values
2. New features (feature engineering)
3. IQR emission treatment
4. Data normalization

New signs:
- debt_to_income: debt-to-income ratio
- credit_utilization_ratio: credit utilization factor
- payment_state: stability of payments

Emission treatment:
- IQR method (Interquartile Range)
- Replacement of emissions on boundary values
- Maintaining the target variable
 """

# Processing missing values
# Median is more emission-resistant than average
 data = data.fillna(data.median())

# the new signs (feature engineering)
# Combining existing signs for quality improvement
Data['debt_to_income'] = data['debt_ratio']* data['income'] # Debt-to-income ratio
Data['credit_utilisation_ratio'] = data['credit_utilisation'] / (data['credit_score'] + 1) # Credit utilization factor
data['payment_ability'] = data['payability_history'] /(data['late_payments'] + 1) #Stable payments

# IQR emission treatment
# IQR = Q3 - Q1, emissions: < Q1 - 1.5*IQR or > Q3 + 1.5*IQR
 numeric_columns = data.select_dtypes(include=[np.number]).columns
 for col in numeric_columns:
'Default_risk': #not processing target variable
Q1 = data[col]. Quantile(0.25) # First quartile
Q3 = data[col]. Quantile(0.75) # Third quartile
IQR = Q3 - Q1 # Interquartile Wave
# Replacement of emissions on boundary values
 data[col] = np.where(data[col] < Q1 - 1.5 * IQR, Q1 - 1.5 * IQR, data[col])
 data[col] = np.where(data[col] > Q3 + 1.5 * IQR, Q3 + 1.5 * IQR, data[col])

 return data

# Data production
bank_data_processed = prepare_bank_data(bank_data)
```

### Model learning
```python
def train_bank_model(data):
 """
Training model for bank tasking default classification

 Parameters:
 -----------
 data : pd.dataFrame
Bank data produced:
- Contains the target variable 'default_risk'
- OWorkingn missing values and emissions
- New signs created

 Returns:
 --------
 tuple
 (predictor, test_data):
- Predicator: TabularPredicator model trained
- test_data: test data for evaluation

 Notes:
 ------
Training process:
1. Data sharing on train/test (80/20)
2. Strategized separation (class ratio retention)
3. The pre-indexor with settings for a banking task
4. configurization of hyperparameters for different algorithms
5. Learning with high quality and Bagging

Settings for banking:
- Problem_type: 'binary'
Eval_metric: 'roc_auc' (ROC-AUC for unbalanced data)
- presets: 'high_quality'
- number_bag_folds: 5 (bagging for stability)
- Time_limit: 1800s (30 minutes)
 """

# Separation on train/test
# Strategized division retains class proportions
 train_data, test_data = train_test_split(
 data,
test_size = 0.2, # 20% for testing
Random_state=42, #Reproducibility
stratehy=data['default_risk'] #Strategy on target
 )

# a pre-indexor with settings for a banking task
 predictor = TabularPredictor(
Label='default_risk', #Target variable
Problem_type='binary', #binary classification
Eval_metric='roc_auc', #ROC-AUC for unbalanced data
path='./bank_models' #A path for model preservation
 )

# configuring hyperparameters for banking task
# Optimized for binic classification with unbalanced data
 hyperparameters = {
 'GBM': [ # Gradient Boosting Machine (LightGBM)
 {
'num_boost_round':200, #Number of iterations of buzting (100-500)
'learning_rate': 0.1 # Learning speed (0.01-0.3)
'num_laves': 31, #Number of leaves in wood (10-100)
'feature_fraction': 0.9, # Proportion of signs for each tree (0.5-1.0)
'bagging_fraction': 0.8, # Proportion of data for each tree (0.5-1.0)
'min_data_in_leaf': 20 # Minimum sample in sheet (10-100)
 }
 ],
 'XGB': [ # XGBoost
 {
'n_estimators': 200, #Number of trees (100-1000)
'learning_rate': 0.1 # Learning speed (0.01-0.3)
'max_dept': 6, # Maximum tree depth (3-10)
'subsample': 0.8, # Proportion of sample for learning (0.5-1.0)
'colsample_bytree': 0.8 # Proportion of signs for wood (0.5-1.0)
 }
 ],
 'CAT': [ # CatBoost
 {
'eaters': 200, #Number of iterations (100-1000)
'learning_rate': 0.1 # Learning speed (0.01-0.3)
'dept': 6, # Tree depth (3-10)
'l2_leaf_reg': 3.0 #L2 regularization (1.0-10.0)
 }
 ]
 }

# Training model with optimized parameters
 predictor.fit(
Train_data, #data for learning
Hyperparameters=hyperparameters, #Settings algorithms
Time_limit= 1800, #Learning time in seconds (30 minutes)
presets='high_quality', # pre-installation of quality (high_quality for maximum quality)
num_bag_folds=5, #Number of folds for bagging (3-10)
num_bag_sects=1 # Number of Bagging Sets (1-3)
 )

 return predictor, test_data

# Model learning
bank_predictor, bank_test_data = train_bank_model(bank_data_processed)
```

### Quality assessment
```python
def evaluate_bank_model(predictor, test_data):
 """
Quality assessment of the banking model for the classification of default

 Parameters:
 -----------
 predictor : TabularPredictor
Trained model for evaluation:
- Should be trained on banking data.
- Supports predict() and predict_proba()
- Provides information on the importance of the signs

 test_data : pd.dataFrame
test data for evaluation:
- Contains the target variable 'default_risk'
- It has the same characteristics as learning data.
- not involved in model training

 Returns:
 --------
 Dict[str, Any]
Model evaluation results:
- performance: quality metrics (accuracy, roc_auc, précis, recall)
- Feature_importance: the importance of signs for prediction
- Leaderboard: comparison of different models
- Preventions: class predictions (0/1)
- probabilities: Class probability

 Notes:
 ------
evaluation tools for banking purposes:
- ROC-AUC: Main metrics for unbalanced data
- Precion: percentage of correct preferences default
- Recall: share of Foundation defaults
- F1-score: harmonic mean precision and recall
- Accuracy: Total accuracy of classification

Analysis of the importance of the topics:
- Shows what factors are important for predicting default.
- Helps you understand Logsk's model.
- Used for feature selection
 """

# Class predictions (0 - no default, 1 - default)
 predictions = predictor.predict(test_data)

# Probability of classes (for Model Analysis)
 probabilities = predictor.predict_proba(test_data)

# Model quality assessment
# Automatic calculation of metrics for binaric classification
 performance = predictor.evaluate(test_data)

# Analysis of the importance of the signs
♪ Shows the contribution of each of them ♪
 feature_importance = predictor.feature_importance()

# Model leader
# Comparison of different algorithms and their combinations
 leaderboard = predictor.leaderboard(test_data)

 return {
'Performance': performance, # quality metrics
'feature_importance':theature_importance, #The importance of signs
'Leaderboard': leaderboard, #comparison models
'Predications': preferences, #Pressions of classes
'Probabilities': Probabilities # Class Probabilities
 }

# Model evaluation
bank_results = evaluate_bank_model(bank_predictor, bank_test_data)

print("Bank Model Performance:")
for metric, value in bank_results['performance'].items():
 print(f"{metric}: {value:.4f}")

print("\nTop 10 Feature importance:")
print(bank_results['feature_importance'].head(10))
```

### Visualization of results

# Why is visualization critical to understanding the metric? # 'Cause pictures show what the numbers hide:

**ROC Curve**: Shows the quality of class separation at different thresholds
- **Precion-Recall**: Shows the balance between accuracy and completeness
**Confusion Matrix**: Visualizes the types of model errors
- **Feature import**: Shows what factors are important for predicting

```python
def visualize_bank_results(results, test_data):
"Visualization of the results of the banking model."

 fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# ROC curve
 from sklearn.metrics import roc_curve, auc
 fpr, tpr, _ = roc_curve(test_data['default_risk'], results['probabilities'][1])
 roc_auc = auc(fpr, tpr)

 axes[0, 0].plot(fpr, tpr, label=f'ROC AUC = {roc_auc:.3f}')
 axes[0, 0].plot([0, 1], [0, 1], 'k--')
 axes[0, 0].set_xlabel('False Positive Rate')
 axes[0, 0].set_ylabel('True Positive Rate')
 axes[0, 0].set_title('ROC Curve')
 axes[0, 0].legend()

# Precion-Recall curve
 from sklearn.metrics import precision_recall_curve
 precision, recall, _ = precision_recall_curve(test_data['default_risk'], results['probabilities'][1])

 axes[0, 1].plot(recall, precision)
 axes[0, 1].set_xlabel('Recall')
 axes[0, 1].set_ylabel('Precision')
 axes[0, 1].set_title('Precision-Recall Curve')

# The importance of signs
 results['feature_importance'].head(10).plot(kind='barh', ax=axes[1, 0])
 axes[1, 0].set_title('Top 10 Feature importance')

# Distribution of probabilities
 axes[1, 1].hist(results['probabilities'][1], bins=50, alpha=0.7)
 axes[1, 1].set_xlabel('Default Probability')
 axes[1, 1].set_ylabel('Frequency')
 axes[1, 1].set_title('Distribution of Default Probabilities')

 plt.tight_layout()
 plt.show()

# Visualization
visualize_bank_results(bank_results, bank_test_data)
```

## example 2: Price forecasting on real estate

<img src="images/optimized/real_estate_regression_Anallysis.png" alt="example real estate" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 3: example of price forecasting on real estate – predictions vs fact, distribution of errors, importance of signs, quality metrics*

Why is real estate a great example for regression?

** Key aspects of regression in real estate:**
- ** Multiple factors**: Area, area, floor, year of construction
- ** Continuous target variable**: Price in rubles
- **Feature Engineering**: new features from existing
- **validation**: check on retraining
- ** Interpretation**: Understanding the impact of each factor
- **quality indicators**: RMSE, MAE, R2 for accuracy evaluation

### The challenge
Pricing real estate prices on object characteristics.

### data
```python
def create_real_estate_data(n_samples=5000):
 """
of Synthetic Real Estate Data for Regressive Analysis

 Parameters:
 -----------
 n_samples : int, default=5000
Sample size for generation:
- 1000-3000: small datasets (rapid testing)
- 3000-10000: average datesets (quality and speed balance)
- 10,000+: large datasets (maximum quality)

 Returns:
 --------
 pd.dataFrame
Synthetic Real Estate Data:
- Numerical characteristics: area, bedrooms, bathrooms, age
- Binary features: garage, pool, garden
- Categories: district, type of real estate, state
- Target variable: price in rubles

 Notes:
 ------
The structure of real estate data:
- 7 digits (area, bedrooms, bathrooms, age)
- 3 bins (garage, pool, garden)
- 3 qualifiers (region, type, status)
- Target variable: price (continuous)

Business Logging Prices:
- Basic price: 100,000 roubles
- Area: +1,000 roubles/m2
- Bedrooms: +10,000 roubles per bedroom
- Bathrooms: +5,000 rubles per bathroom
- Garage: +15,000 roubles
- Basin: +25,000 roubles
- Garden: +10,000 roubles
Age: -2,000 rubles per year
- Noise: ± 20,000 roubles (accidental component)
 """

np.random.seed(42) # Reproducibility of results

# Basic characteristics of real estate
 data = pd.dataFrame({
'Area': np.random.normal(120, 30, n_samples), #The area (m2) is the normal distribution
'Bedrooms': np.random.poisson(3, n_samples), #Number of bedrooms - Poisson distribution
'Bathrooms': np.random.poisson(2, n_samples), #The number of baths - Poisson's distribution
'age': np.random.exponential(10, n_samples), # Age(years) - exponential distribution
'garage': np.random.binomial(1, 0.7, n_samples), #presence garage (70% probability)
'pool': np.random.binomial(1, 0.2, n_samples), #p.random.binomial (20% probability)
'garden': np.random.binomial(1, 0.6, n_samples) #presence garden (60% probability)
 })

# All the variables
 data['location'] = np.random.choice(['downtown', 'suburbs', 'rural'], n_samples)
 data['property_type'] = np.random.choice(['hoUse', 'apartment', 'townhoUse'], n_samples)
 data['condition'] = np.random.choice(['excellent', 'good', 'fair', 'poor'], n_samples)

# of target variable (price)
 base_price = 100000
 price = (base_price +
 data['area'] * 1000 +
 data['bedrooms'] * 10000 +
 data['bathrooms'] * 5000 +
 data['garage'] * 15000 +
 data['pool'] * 25000 +
 data['garden'] * 10000 -
 data['age'] * 2000)

# add noise
 price += np.random.normal(0, 20000, n_samples)
Data['price'] = np.maximum(price, 50000) # Minimum price

 return data

# data quality
real_estate_data = create_real_estate_data(5000)
print("Real estate data shape:", real_estate_data.shape)
print("Price statistics:")
print(real_estate_data['price'].describe())
```

### Data preparation
```python
def prepare_real_estate_data(data):
"The production of real estate data."

# new signs
 data['area_per_bedroom'] = data['area'] / (data['bedrooms'] + 1)
 data['total_rooms'] = data['bedrooms'] + data['bathrooms']
 data['age_category'] = pd.cut(data['age'], bins=[0, 5, 15, 30, 100], labels=['new', 'recent', 'old', 'very_old'])

# Emissions treatment
 data['area'] = np.where(data['area'] > 300, 300, data['area'])
 data['age'] = np.where(data['age'] > 50, 50, data['age'])

 return data

# Data production
real_estate_processed = prepare_real_estate_data(real_estate_data)
```

### Model learning
```python
def train_real_estate_model(data):
"Teaching the Model for Real Estate"

# Separation on train/test
 train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

♪ Create pre-reactor
 predictor = TabularPredictor(
 label='price',
 problem_type='regression',
 eval_metric='rmse',
 path='./real_estate_models'
 )

# Configuring hyperparameters for regression
 hyperparameters = {
 'GBM': [
 {
 'num_boost_round': 300,
 'learning_rate': 0.1,
 'num_leaves': 31,
 'feature_fraction': 0.9,
 'bagging_fraction': 0.8,
 'min_data_in_leaf': 20
 }
 ],
 'XGB': [
 {
 'n_estimators': 300,
 'learning_rate': 0.1,
 'max_depth': 6,
 'subsample': 0.8,
 'colsample_bytree': 0.8
 }
 ],
 'RF': [
 {
 'n_estimators': 200,
 'max_depth': 15,
 'min_samples_split': 5,
 'min_samples_leaf': 2
 }
 ]
 }

# Model learning
 predictor.fit(
 train_data,
 hyperparameters=hyperparameters,
 time_limit=1800, # 30 minutes
 presets='high_quality',
 num_bag_folds=5,
 num_bag_sets=1
 )

 return predictor, test_data

# Model learning
real_estate_predictor, real_estate_test_data = train_real_estate_model(real_estate_processed)
```

### Quality assessment
```python
def evaluate_real_estate_model(predictor, test_data):
""Real Model Quality Assessment""

# Premonition
 predictions = predictor.predict(test_data)

# Quality assessment
 performance = predictor.evaluate(test_data)

# Analysis of the importance of the signs
 feature_importance = predictor.feature_importance()

# Model leader
 leaderboard = predictor.leaderboard(test_data)

# Mistake analysis
 errors = test_data['price'] - predictions
 mae = np.mean(np.abs(errors))
 mape = np.mean(np.abs(errors / test_data['price'])) * 100

 return {
 'performance': performance,
 'feature_importance': feature_importance,
 'leaderboard': leaderboard,
 'predictions': predictions,
 'mae': mae,
 'mape': mape,
 'errors': errors
 }

# Model evaluation
real_estate_results = evaluate_real_estate_model(real_estate_predictor, real_estate_test_data)

print("Real Estate Model Performance:")
for metric, value in real_estate_results['performance'].items():
 print(f"{metric}: {value:.4f}")

print(f"\nMAE: {real_estate_results['mae']:.2f}")
print(f"MAPE: {real_estate_results['mape']:.2f}%")
```

### Visualization of results

**Why does visualization of regression differ from classification?** Because here we predict continuous values and not classes:

**Scatter Plot**: Shows correlation between predicted and actual values
**Error Distribution**: Demonstrates model errors (normality, emissions)
- **Feature import**: Identifys the most powerful factors on price
**Error vs Price**: Shows whether the accuracy from the range of prices depends

```python
def visualize_real_estate_results(results, test_data):
"Visualization of the Real Estate Model""

 fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Vs forecasts Actual values
 axes[0, 0].scatter(test_data['price'], results['predictions'], alpha=0.6)
 axes[0, 0].plot([test_data['price'].min(), test_data['price'].max()],
 [test_data['price'].min(), test_data['price'].max()], 'r--')
 axes[0, 0].set_xlabel('Actual Price')
 axes[0, 0].set_ylabel('Predicted Price')
 axes[0, 0].set_title('predictions vs Actual')

# The distribution of errors
 axes[0, 1].hist(results['errors'], bins=50, alpha=0.7)
 axes[0, 1].set_xlabel('Prediction Error')
 axes[0, 1].set_ylabel('Frequency')
 axes[0, 1].set_title('Distribution of Prediction Errors')

# The importance of signs
 results['feature_importance'].head(10).plot(kind='barh', ax=axes[1, 0])
 axes[1, 0].set_title('Top 10 Feature importance')

# Mistakes on Price
 axes[1, 1].scatter(test_data['price'], results['errors'], alpha=0.6)
 axes[1, 1].set_xlabel('Actual Price')
 axes[1, 1].set_ylabel('Prediction Error')
 axes[1, 1].set_title('Errors by Price Range')
 axes[1, 1].axhline(y=0, color='r', linestyle='--')

 plt.tight_layout()
 plt.show()

# Visualization
visualize_real_estate_results(real_estate_results, real_estate_test_data)
```

## example 3: Time series analysis

<img src="images/optimized/time_series_Analesis.png" alt="example time series" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 4: example time series - time series with projections, errors in time, error distribution, metrics MASE/MAPE*

**Why are time series a special type of task?** Because they have a temporary taskency and require special methods:

** Key aspects of time series:**
** Temporary dependency**: Future values depend from past
- ** Seasonality**: Repeatable time variables
- **Trends**: Long-term changes
- **Stability**: Stability of statistical properties
- **validation**: Special methods for temporary data
- ** Projection**: Adoption of future values

### The challenge
Forecasting the sale of goods on historical data.

### data
```python
def create_sales_data(n_days=365, n_products=10):
 """
quality of synthetic sales data for time series

 Parameters:
 -----------
 n_days : int, default=365
Number of days for generation:
- 30-90: short-term trends (month-quarters)
- 90-365: Medium-term trends (quarters of year)
- 365+: Long-term trends (year+)

 n_products : int, default=10
Number of products for Analysis:
- 1-5: analysis of one product
- 5-20: product line analysis
- 20+: wide range analysis

 Returns:
 --------
 pd.dataFrame
Synthetic sales data:
- Data: date of sale
- product_id: product identifier
- sales: sales
- day_of_week: day of the week (0-6)
- Month: month (1-12)
- Quarter: quarter (1-4)

 Notes:
 ------
Structure of the time series:
- Trent: linear growth in time sales
- Seasonality: weekly fluctuations (exit vs Mondays)
- Noise: accidental fluctuations (market factors)
- Negative sales: deleted (sales ≥ 0)

Time signs:
- Day_of_week: Day of the Week for Analysis weekend
- Month: Month for Season Analysis
Quarter: Quarter block for quarterly Analysis
 """

np.random.seed(42) # Reproducibility of results

# rent time series
 dates = pd.date_range('2023-01-01', periods=n_days, freq='D')

 data = []
 for product_id in range(n_products):
# Baseline trend (line sales growth)
trend = np.linspace(100, 150, n_days) # Growth with 100 to 150 sales

# Seasonality (weekly fluctuations)
region = 20 * np.sin(2 * np.pi * np.arange(n_days) / 7) # Amplitude ± 20

# Random noise (market factors)
noise = np.random.normal(0,10,n_days) # Standard deviation 10

# Sales (combination of trend, seasonality and noise)
 sales = trend + seasonality + noise
sales = np.maximum(sales, 0) # Negative sales impossible

# Create records
 for i, (date, sale) in enumerate(zip(dates, sales)):
 data.append({
 'date': date,
 'product_id': f'product_{product_id}',
 'sales': sale,
 'day_of_week': date.dayofweek,
 'month': date.month,
 'quarter': date.quarter
 })

 return pd.dataFrame(data)

# data quality
sales_data = create_sales_data(365, 10)
print("Sales data shape:", sales_data.shape)
print("Sales statistics:")
print(sales_data['sales'].describe())
```

### Data preparation for time series
```python
def prepare_sales_data(data):
 """
Production of sales data for time series

 Parameters:
 -----------
 data : pd.dataFrame
Reference sales data:
- Contains columns: data, product_id, sales, day_of_week, month, quarter
- Classified on product_id and data
- May contain missing values

 Returns:
 --------
 pd.dataFrame
Prepared by Data with Time Sign:
- Lug signs: sales_lag_1, sales_lag_2, sales_lag_3, sales_lag_7, sales_lag_14, sales_lag_30
- Slipping medium: sales_ma_7, sales_ma_14, sales_ma_30
- Trend indicators: sales_trend
- Seasonal characteristics: is_weekend, is_month_start, is_month_end

 Notes:
 ------
Time signs for forecasting:
- Legacy: values of sales in previous days
- Sliding average: smooth trends over time
- Trends: direction of change in sales
- Seasonal characteristics: calendar effects (outcome, beginning/end of month)

Lug signs:
- sales_lag_1: sales yesterday (short-term dependency)
- sales_lag_7: sales a week ago (weekly seasonality)
- sales_lag_30: sales a month ago (monthly seasonality)

Sliding medium:
- sales_ma_7: average sales per week
- sales_ma_14: average sales in 2 weeks
- sales_ma_30: average monthly sales
 """

# Create lague signs
# Sorting on product and date for correct shift
 data = data.sort_values(['product_id', 'date'])

# Legacy signs (sales in previous days)
for leg in [1, 2, 3, 7, 14, 30]: # Different lags for different time dependencies
 data[f'sales_lag_{lag}'] = data.groupby('product_id')['sales'].shift(lag)

# Sliding averages (cooled trends)
for Windows in [7, 14, 30]: # Different windows for different time scales
 data[f'sales_ma_{window}'] = data.groupby('product_id')['sales'].rolling(window=window).mean().reset_index(0, drop=True)

# Traditional signs (direction of sales)
 data['sales_trend'] = data.groupby('product_id')['sales'].rolling(window=7).mean().reset_index(0, drop=True)

# Seasonal signs (calendar effects)
Data['is_weekend'] = (data['day_of_week'] >=5).astype(int) # Days off
Data['is_month_start'] = (data['data'].dt.day <=7).astype(int) # Start of month
Data['is_month_end'] = (data['data'].dt.day >=25.astype(int) # End of month

 return data

# Data production
sales_processed = prepare_sales_data(sales_data)
```

### Training the time series model
```python
def train_sales_model(data):
"Learning Model for Sales Forecasting""

# Division on train/test
 split_date = data['date'].max() - pd.Timedelta(days=30)
 train_data = data[data['date'] <= split_date]
 test_data = data[data['date'] > split_date]

♪ Create pre-reactor
 predictor = TabularPredictor(
 label='sales',
 problem_type='regression',
 eval_metric='rmse',
 path='./sales_models'
 )

# Configuring hyperparameters for time series
 hyperparameters = {
 'GBM': [
 {
 'num_boost_round': 200,
 'learning_rate': 0.1,
 'num_leaves': 31,
 'feature_fraction': 0.9,
 'bagging_fraction': 0.8,
 'min_data_in_leaf': 20
 }
 ],
 'XGB': [
 {
 'n_estimators': 200,
 'learning_rate': 0.1,
 'max_depth': 6,
 'subsample': 0.8,
 'colsample_bytree': 0.8
 }
 ]
 }

# Model learning
 predictor.fit(
 train_data,
 hyperparameters=hyperparameters,
 time_limit=1800, # 30 minutes
 presets='high_quality',
num_bag_folds=3, # Less folds for time series
 num_bag_sets=1
 )

 return predictor, test_data

# Model learning
sales_predictor, sales_test_data = train_sales_model(sales_processed)
```

### Quality assessment of time series
```python
def evaluate_sales_model(predictor, test_data):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""The quality of the sales model"""""""""""""""""""""""""""the quality evaluation of the sales model""""" """"" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""the quality of the sales model"" """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Premonition
 predictions = predictor.predict(test_data)

# Quality assessment
 performance = predictor.evaluate(test_data)

# Analysis of the importance of the signs
 feature_importance = predictor.feature_importance()

# Analysis on products
 product_performance = {}
 for product_id in test_data['product_id'].unique():
 product_data = test_data[test_data['product_id'] == product_id]
 product_predictions = predictions[test_data['product_id'] == product_id]

 mae = np.mean(np.abs(product_data['sales'] - product_predictions))
 mape = np.mean(np.abs((product_data['sales'] - product_predictions) / product_data['sales'])) * 100

 product_performance[product_id] = {
 'mae': mae,
 'mape': mape
 }

 return {
 'performance': performance,
 'feature_importance': feature_importance,
 'product_performance': product_performance,
 'predictions': predictions
 }

# Model evaluation
sales_results = evaluate_sales_model(sales_predictor, sales_test_data)

print("Sales Model Performance:")
for metric, value in sales_results['performance'].items():
 print(f"{metric}: {value:.4f}")

print("\nProduct Performance:")
for product, perf in sales_results['product_performance'].items():
 print(f"{product}: MAE={perf['mae']:.2f}, MAPE={perf['mape']:.2f}%")
```

### Visualization of time series

**Why is visualization of time series special?** Because time is an additional dimension that needs to be considered:

- **Time Series Plot**: Shows trends, seasonality and the quality of forecasts over time
- **Error Analysis**: Shows how errors are distributed in time
- **Feature import**: Identifys what time signs are important
- **Performance by Product**: Compares the quality of the forecast for different products

```python
def visualize_sales_results(results, test_data):
"Visualization of the results of the sales model."

 fig, axes = plt.subplots(2, 2, figsize=(15, 12))

#amporial row for one product
 product_id = test_data['product_id'].iloc[0]
 product_data = test_data[test_data['product_id'] == product_id]
 product_predictions = results['predictions'][test_data['product_id'] == product_id]

 axes[0, 0].plot(product_data['date'], product_data['sales'], label='Actual', alpha=0.7)
 axes[0, 0].plot(product_data['date'], product_predictions, label='Predicted', alpha=0.7)
 axes[0, 0].set_title(f'Sales Forecast for {product_id}')
 axes[0, 0].set_xlabel('Date')
 axes[0, 0].set_ylabel('Sales')
 axes[0, 0].legend()

# The distribution of errors
 errors = test_data['sales'] - results['predictions']
 axes[0, 1].hist(errors, bins=30, alpha=0.7)
 axes[0, 1].set_xlabel('Prediction Error')
 axes[0, 1].set_ylabel('Frequency')
 axes[0, 1].set_title('Distribution of Prediction Errors')

# The importance of signs
 results['feature_importance'].head(10).plot(kind='barh', ax=axes[1, 0])
 axes[1, 0].set_title('Top 10 Feature importance')

# product performance
 products = List(results['product_performance'].keys())
 maes = [results['product_performance'][p]['mae'] for p in products]

 axes[1, 1].bar(products, maes)
 axes[1, 1].set_xlabel('Product')
 axes[1, 1].set_ylabel('MAE')
 axes[1, 1].set_title('Performance by Product')
 axes[1, 1].tick_params(axis='x', rotation=45)

 plt.tight_layout()
 plt.show()

# Visualization
visualize_sales_results(sales_results, sales_test_data)
```

## example 4: Multi-class classification

<img src="images/optimized/multimedia_classification_Analysis.png" alt="example multiclass classification" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 5: example multiclass classification - Confusion Matrix, accuracy on classes, distribution of preferences, quality metrics*

Why is multiclass classification more difficult than binary?

** Key aspects of multi-class classification:**
- ** Multiple classes**: More than 2 categories for classification
- ** Class balance**: Unequal distribution of examples
- **quality metrics**: Accuracy, Precion, Recall for each class
- **Feature Engineering**: Image extraction
- **validation**: Strategized data separation
** Interpretation**: Understanding the solutions of the model

### The challenge
Classification of images on base of recovered topics.

### data
```python
def create_image_data(n_samples=5000, n_features=100):
 """
quality of synthetic image data for multi-class classification

 Parameters:
 -----------
 n_samples : int, default=5000
Sample size for generation:
- 1000-3000: small datasets (rapid testing)
- 3000-10000: average datesets (quality and speed balance)
- 10,000+: large datasets (maximum quality)

 n_features : int, default=100
Number of images:
50-100: Basic characteristics (colour, texture)
- 100-500: extended features (forms, objects)
- 500+: complex features (deep characteristics)

 Returns:
 --------
 pd.dataFrame
Synthetic data images:
- Numerical characteristics: Feature_0, Feature_1, ..., Feature_n
- Category: Class, image_size, resolution
- Numerical metadata: color_channels

 Notes:
 ------
Structure of images:
- n_features of numerical characteristics (extracted characteristics)
- 5 classes of objects: cat, dog, Bird, car,tree
- 3 image sizes: small, medium, large
- 2 types of flowers: grayscale (1), RGB (3)
- 3 permits: low, medium, high

Business context:
- Objective: Classification of objects on images
Application: computer vision, automatic marking
- metrics: accuracy, precision, recall for each class
- Validation: Stratification of classes
 """

np.random.seed(42) # Reproducibility of results

# square image signs (extracted features)
# Normal distribution mimics real CNN
 features = np.random.randn(n_samples, n_features)

#free target classes (5 categories of objects)
 n_classes = 5
Classes = ['cat', 'dog', 'bird', 'car', 'tree'] #5 classes of objects
y = np.random.choice(n_classes, n_samples) # Random class distribution

# Create dataFrame with signature
 feature_names = [f'feature_{i}' for i in range(n_features)]
 data = pd.dataFrame(features, columns=feature_names)
Data['class'] = [classes[i] for i in y] # Target variable

# add image metadata
data['image_size'] = np.random.choice(['small', 'mediam', 'large', n_samples) # Image size
Data['color_channels'] = np.random.choice[1, 3], n_samples] #Number of color channels
data['resolution'] = np.random.choice(['low', 'mediam', 'high', n_samples) # Image resolution

 return data

# data quality
image_data = create_image_data(5000, 100)
print("Image data shape:", image_data.shape)
print("Class distribution:")
print(image_data['class'].value_counts())
```

### Data preparation
```python
def prepare_image_data(data):
 """
Preparation of image data for multiclass classification

 Parameters:
 -----------
 data : pd.dataFrame
Reference data images:
- Contains numerical features (feature_0, feature_1, ...)
- Contains categorical features (class, image_size, resolution)
- Contains metadata (color_channels)

 Returns:
 --------
 pd.dataFrame
Data images produced:
- aggregates created (feature_sum, feature_mean, feature_std)
- Numerical signs normalized
- Ready for model training.

 Notes:
 ------
Data production process:
1. total aggregates (sum, average, standard deviation)
2. Normalization of numbers (z-score normalization)
3. Maintaining the categorical characteristics without change

Disaggregated characteristics:
- Feature_sum: sum of all topics (total "activity" of the image)
- Feature_mean: mean value of the topics (average brightness)
- Feature_std: standard deviation of the topics (variability)

Normalization:
- Z-score normalization: (x-mean) / std
- Applicable to all numerical signature other than color_channels
- Ensures the sustainability of education
 """

# the new signs (feature engineering)
# The aggregates help the model understand the general characteristics of the image
== sync, corrected by elderman == @elder_man
Data['feature_mean'] = data.select_dtypes(include=[np.number]).mean(axis=1) # Average value of the topics
Data['feature_std'] = data.select_dtypes(include=[np.number]).std(axis=1) # Standard deviation of topics

# Normalization of signs (z-score normalization)
# Normalization improves stability and speed of learning
 numeric_columns = data.select_dtypes(include=[np.number]).columns
 for col in numeric_columns:
if col != 'color_channels': # no normalization of metadata
Data[col] = (data[col] - data[col].mean() / data[col].std() #Z-score normalization

 return data

# Data production
image_processed = prepare_image_data(image_data)
```

### Model learning
```python
def train_image_model(data):
"Learning Model for Image Classification""

# Separation on train/test
 train_data, test_data = train_test_split(data, test_size=0.2, random_state=42, stratify=data['class'])

♪ Create pre-reactor
 predictor = TabularPredictor(
 label='class',
 problem_type='multiclass',
 eval_metric='accuracy',
 path='./image_models'
 )

#configuring hyperparameters for multiclass classification
 hyperparameters = {
 'GBM': [
 {
 'num_boost_round': 200,
 'learning_rate': 0.1,
 'num_leaves': 31,
 'feature_fraction': 0.9,
 'bagging_fraction': 0.8,
 'min_data_in_leaf': 20
 }
 ],
 'XGB': [
 {
 'n_estimators': 200,
 'learning_rate': 0.1,
 'max_depth': 6,
 'subsample': 0.8,
 'colsample_bytree': 0.8
 }
 ],
 'RF': [
 {
 'n_estimators': 200,
 'max_depth': 15,
 'min_samples_split': 5,
 'min_samples_leaf': 2
 }
 ]
 }

# Model learning
 predictor.fit(
 train_data,
 hyperparameters=hyperparameters,
 time_limit=1800, # 30 minutes
 presets='high_quality',
 num_bag_folds=5,
 num_bag_sets=1
 )

 return predictor, test_data

# Model learning
image_predictor, image_test_data = train_image_model(image_processed)
```

### Quality assessment
```python
def evaluate_image_model(predictor, test_data):
"""""""""""""""

# Premonition
 predictions = predictor.predict(test_data)
 probabilities = predictor.predict_proba(test_data)

# Quality assessment
 performance = predictor.evaluate(test_data)

# Analysis of the importance of the signs
 feature_importance = predictor.feature_importance()

# Model leader
 leaderboard = predictor.leaderboard(test_data)

# Class analysis
 from sklearn.metrics import classification_Report, confusion_matrix

 class_Report = classification_Report(test_data['class'], predictions, output_dict=True)
 conf_matrix = confusion_matrix(test_data['class'], predictions)

 return {
 'performance': performance,
 'feature_importance': feature_importance,
 'leaderboard': leaderboard,
 'predictions': predictions,
 'probabilities': probabilities,
 'classification_Report': class_Report,
 'confusion_matrix': conf_matrix
 }

# Model evaluation
image_results = evaluate_image_model(image_predictor, image_test_data)

print("Image Model Performance:")
for metric, value in image_results['performance'].items():
 print(f"{metric}: {value:.4f}")

print("\nClassification Report:")
for class_name, metrics in image_results['classification_Report'].items():
 if isinstance(metrics, dict):
 print(f"{class_name}: {metrics}")
```

### Visualization of results

**Why does a multiclass classification require special visualization?** Because it is necessary to analyse quality on each class separately:

- **Confusion Matrix**: Shows what classes confused the model.
**Class Accuracy**: Demonstrates accuracy for each class separately
- **Predication Distribution**: Finds whether the model predicts only popular classes
- **Feature import**: Shows that what signs are important for class distinction

```python
def visualize_image_results(results, test_data):
"Visualization of the image classification model""

 fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# A matrix of errors
 import seaborn as sns
 sns.heatmap(results['confusion_matrix'], annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
 axes[0, 0].set_title('Confusion Matrix')
 axes[0, 0].set_xlabel('Predicted')
 axes[0, 0].set_ylabel('Actual')

# The importance of signs
 results['feature_importance'].head(15).plot(kind='barh', ax=axes[0, 1])
 axes[0, 1].set_title('Top 15 Feature importance')

# Distributions
 Prediction_counts = pd.Series(results['predictions']).value_counts()
 Prediction_counts.plot(kind='bar', ax=axes[1, 0])
 axes[1, 0].set_title('Distribution of predictions')
 axes[1, 0].set_xlabel('Class')
 axes[1, 0].set_ylabel('Count')
 axes[1, 0].tick_params(axis='x', rotation=45)

# Accuracy on classes
 class_accuracy = []
 for class_name in test_data['class'].unique():
 class_data = test_data[test_data['class'] == class_name]
 class_predictions = results['predictions'][test_data['class'] == class_name]
 accuracy = (class_data['class'] == class_predictions).mean()
 class_accuracy.append(accuracy)

 axes[1, 1].bar(test_data['class'].unique(), class_accuracy)
 axes[1, 1].set_title('Accuracy by Class')
 axes[1, 1].set_xlabel('Class')
 axes[1, 1].set_ylabel('Accuracy')
 axes[1, 1].tick_params(axis='x', rotation=45)

 plt.tight_layout()
 plt.show()

# Visualization
visualize_image_results(image_results, image_test_data)
```

## example 5: System sold

<img src="images/optimized/production_system_architecture.png" alt="architecture sold system" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
♪ Figure 7: Architecture sold by AutoML Gluon - components, data stream, Monitoring ♪

♪ # # The whole system is sold ♪
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import logging
from datetime import datetime
from typing import Dict, List, Any
import asyncio
import aiohttp

# configuring Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI applications
app = FastAPI(title="AutoML Gluon Production API", version="1.0.0")

# Global variables
models = {}
model_metadata = {}

class PredictionRequest(BaseModel):
 """
Request on Implementation for API sales

 Parameters:
 -----------
 model_name : str
The name of the prediction model:
- 'bank_default': default classification model
- 'real_estate': real estate price regression model
- 'sales_forest': sales forecasting model

 data : List[Dict[str, Any]]
Data for prediction:
- List dictionaries with signature
- Each dictionary is one model for prediction.
- Keys should match the signature model.
 """
 model_name: str
 data: List[Dict[str, Any]]

class PredictionResponse(BaseModel):
 """
Answer with the results of the prophecy

 Parameters:
 -----------
 predictions : List[Any]
Model predictions:
- for classification: classes (0/1, 'cat'/'dog', etc.)
- for regression: numerical values (prices, sales)

 probabilities : List[Dict[str, float]], optional
Probability of classes (for classification only):
- A dictionary with probabilities for each class
- None for regression models

 model_info : Dict[str, Any]
Model information:
- model_name: model name
- model_type: task type (classification/regression)
- Target: target variable
- Features: List of topics

 timestamp : str
Time of prediction (ISO format)
 """
 predictions: List[Any]
 probabilities: List[Dict[str, float]] = None
 model_info: Dict[str, Any]
 timestamp: str

class ModelInfo(BaseModel):
 """
Information on the in-sold system model

 Parameters:
 -----------
 model_name : str
Name of model in the system

 model_type : str
Type of model:
- 'Binary_classification': Binary classification
'multi-class classification': multi-class classification
- 'regression': regression

 performance : Dict[str, float]
Metrics performance model:
- accuracy, roc_auc, precision, recall (for classifications)
- rmse, mae, r2 (for regressions)

 features : List[str]
List of model features

 created_at : str
Model date (ISO format)
 """
 model_name: str
 model_type: str
 performance: Dict[str, float]
 features: List[str]
 created_at: str

@app.on_event("startup")
async def load_models():
 """
Loaded models with Launche sold system

 Notes:
 ------
Model loading process:
1. Loading of the banking model (classification of default)
2. Uploading of the real estate model (price rebound)
3. Reference metadata for each model
4. Logging of download results

Metadata model:
- model_type: type of task (binary_classification, regression)
- Target: target variable
- Features: List of model features

Error management:
- Logging up download errors
- Continuation of partial loading
- Returning errors through health check
 """
 global models, model_metadata

# Uploading of the banking model (classification of default)
 try:
 models['bank_default'] = TabularPredictor.load('./bank_models')
 model_metadata['bank_default'] = {
'Model_type': 'Binary_classification', #Binar classification
'Target': 'Default_risk', #Target': 'Default_risk', #Target'
'features': ['age', 'income', 'credit_score', 'debt_ratio', `employment_years'] # Main features
 }
 logger.info("Bank model loaded successfully")
 except Exception as e:
 logger.error(f"Failed to load bank model: {e}")

# Loading the real estate model (pricing rebound)
 try:
 models['real_estate'] = TabularPredictor.load('./real_estate_models')
 model_metadata['real_estate'] = {
'Model_type': 'regression', #Regression
'Target': 'price', #The target variable
'features': ['area', 'bedrooms', 'bathrooms', 'age', 'location']
 }
 logger.info("Real estate model loaded successfully")
 except Exception as e:
 logger.error(f"Failed to load real estate model: {e}")

@app.get("/health")
async def health_check():
 """
Health check endpoint for Monitoring System Status

 Returns:
 --------
 Dict[str, Any]
System status:
- Status: "healthy" if the models are loaded, "unhealthy" if not
- Lloyded_models: List loaded models
- timestamp: time of check (ISO format)

 Notes:
 ------
health check is used for:
- Monitoring system status
- Model accessibility tests
Automatic overLaunch for malfunctions
 - Load balancer health checks
 """
 loaded_models = List(models.keys())
 return {
"state": "healthy" if Lloyded_models else "unhealthy", # System status
"loaded_models": loaded_models, #List loaded models
"timestamp": datetime.now().isoformat() # Check time
 }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
 """
Endpoint for productions with the use of trained models

 Parameters:
 -----------
 request : PredictionRequest
Request on Prevention:
- model_name: model name
- Data: data for prediction

 Returns:
 --------
 PredictionResponse
Prophecy results:
- Preventions: model predictions
- probabilities: Probability of classes (for classifications)
- model_info: model information
- timestamp: time of execution

 Raises:
 -------
 HTTPException
- 404: model not present
- 500: error in carrying out the prophecy

 Notes:
 ------
Prognosis process:
1. What is the model existence
2. Data conversion in dataFrame
3. The fulfillment of the prophecy
4. Probability (for classification)
5. Formation of the response

Error management:
- Logsorring Prophecy Errors
- Returning HTTP errors with description
- Graceful handling exceptions
 """

 if request.model_name not in models:
 raise HTTPException(status_code=404, detail=f"Model {request.model_name} not found")

 try:
model = models [request.model_name]
metadata = model_metadata[request.model_name] #To receive metadata

# Data conversion in dataFrame
 df = pd.dataFrame(request.data)

# Model predictions
 predictions = model.predict(df)

# Probability of classes (for classification only)
 probabilities = None
if hasattr(model, 'predict_proba'): # check probability support
 proba = model.predict_proba(df)
Probabilities = proba.to_dict('records') # Transforming in List Vocabularies

 return PredictionResponse(
products=predications.toList(), # Conversion in List
Probabilities=Probabilities, # Classroom Probabilities
 model_info={
"model_name": request.model_name, #model name
"model_type": "metadata['model_type']," # Type of task
"Target": metadata['target'], # Target variable
"features": metadata['features'] #List of signs
 },
timeamp=datatime.now().isoformat() # Time
 )

 except Exception as e:
logger.error(f"Predication error: {e}) # Logsring error
Raise HTTPException(status_code=500, detail=str(e)) # Return of HTTP error

@app.get("/models")
async def List_models():
"List of accessible models."
 return {
 "models": List(models.keys()),
 "metadata": model_metadata
 }

@app.get("/models/{model_name}")
async def get_model_info(model_name: str):
""""""""" "model information"""
 if model_name not in models:
 raise HTTPException(status_code=404, detail=f"Model {model_name} not found")

 model = models[model_name]
 metadata = model_metadata[model_name]

 return {
 "model_name": model_name,
 "model_type": metadata['model_type'],
 "target": metadata['target'],
 "features": metadata['features'],
 "performance": model.evaluate(pd.dataFrame([{f: 0 for f in metadata['features']}]))
 }

if __name__ == "__main__":
 import uvicorn
 uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Client for testing
```python
import requests
import json

def test_production_api():
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""",""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 base_url = "http://localhost:8000"

 # health check
 response = requests.get(f"{base_url}/health")
 print("health check:", response.json())

# List models
 response = requests.get(f"{base_url}/models")
 print("available models:", response.json())

# Banking model test
 bank_data = {
 "model_name": "bank_default",
 "data": [
 {
 "age": 35,
 "income": 50000,
 "credit_score": 750,
 "debt_ratio": 0.3,
 "employment_years": 5
 }
 ]
 }

 response = requests.post(f"{base_url}/predict", json=bank_data)
 print("Bank Prediction:", response.json())

# A real estate test
 real_estate_data = {
 "model_name": "real_estate",
 "data": [
 {
 "area": 120,
 "bedrooms": 3,
 "bathrooms": 2,
 "age": 10,
 "location": "downtown"
 }
 ]
 }

 response = requests.post(f"{base_url}/predict", json=real_estate_data)
 print("Real estate Prediction:", response.json())

# Launch tests
if __name__ == "__main__":
 test_production_api()
```

## Advanced examples

<img src="images/optimized/advanced_metrics_Analesis.png" alt="Pushed examples" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 6: Advanced metrics - ROC with thresholds, Precion-Recall, comparson metric, influence of quality threshold*

♪ Why are advanced examples important ♪ ♪ 'Cause they show how to solve complex real problems ♪

**Tips of advanced examples:**
- ** Model Ansamble**: Combination of different algorithms
- **Feature Engineering**: creative complex features
- ** Hyperparametric optimization**: Automatic search for better parameters
- ** Unbalanced data**: Working with rare classes
- **Big data**: Processing of in-gigabytes-sized datasets
- ** Sales**: Deployment of models in real systems

### o example: Models' Ensemble for Financial Forecasting

Why do the ensembles often get better than single models?

- ** Model diversity**: Different algorithms find different patterns
- ** Decrease retraining**: Average reduces risk retraining
- ** Increased stability**: The result is less dependent from the specific model
- **Best synthesis ability**: The Workinget model is better on new data
- ** Automatic choice**: AutoML selects the best combinations.
- ** Interpretation**: Each model contribution can be understood

### * example: Working with unbalanced data

Because in reality, rare events rarely occur:

- ** Balancekeeping strategies**: SMOTE, undersampling, oversampling
- **quality metrics**: F1-score, Precion, Recall instead of Accuracy
- ** Cost of errors**: Different price for different types of errors
- **validation**: Strategized data separation
- **Ansambali**: Combination of models for better quality
- **Monitoring**: Quality tracking on rare classes

## Next steps

After studying the examples, go to:
- [Troubleshooting](./10_Troubleshooting.md)
- [best practice](.08_best_practices.md)
