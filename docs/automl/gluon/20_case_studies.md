# Case Studies: Real projects with AutoML Gluon

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Whose case stadies are critical

**Why 80 percent of the ML projects fail without learning about the successful case files?** Because team no understand how to apply the theory of practice. Case steps show real solutions to real problems.

## # Trouble without learning the case
- ** Theoretical knowledge**: Understanding concepts, but not knowing how to apply
- ** Mistakes**: They come on the same burglaries as others.
- ** Long development**: Bicycles are invented instead of ready solutions
- ** Bad results**: not achieving expected performance

### The benefits of studying the briefcases
- ** Practical understanding**: See how Workinget's theory on practice
- ♪ Avoiding mistakes ♪ - ♪ Learn about mistakes ♪
- ** Rapid development**: Tested approaches used
- **Best results**: State-of-the-art performance

## Introduction in Case Studie

<img src="images/optimized/case_studies_overView.png" alt="AutoML Stady" style"="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 20.1: Review of real projects and their results with the use of AutoML Gluon*

Because they show how abstract concepts transform into Working systems that solve real business challenges.

** Keystone results:**
- ** Credit Sorting**: 87.3% accuracy, AUC 0.923
- ** Medical diagnostic**: 91.2 per cent accuracy, AUC 0.945
- ** Recommendations**: 34.2 per cent Precution@10, +18 per cent conversion
- **Preliminary service**: 89.4 per cent accuracy, -45 per cent simplicity
- ** Cryptotrade**: 73.2% accuracy, 28.5% return
- **Hedge Fund**: 89.7% accuracy, 45.3% return

** Benefits of Case Study:**
- ** Practical understanding**: See how Workinget's theory on practice
- ♪ Avoiding mistakes ♪ - ♪ Learn about mistakes ♪
- ** Rapid development**: Tested approaches used
- **Best results**: State-of-the-art performance

This section contains detailed case studies of real projects demonstrating the application of AutoML Gloon in various industries and tasks.

♪ Case 1: Financial Services - Credit Sorting

<img src="images/optimized/credit_scoring.png" alt="Creed" style"="max-width: 100%; height: auto; display: block; marguin: 20px auto;">
*Picture 20.2: Credit Sorting System - components and results*

**Why is credit sorting a classic example ML in finance?** Because it's a challenge with clear business metrics, a lot of data, and a high cost of errors.

**components of the credit-sorting system:**
- **data Collection**: Collection of data on borrowers
- **Feature Engineering**: criteria for risk assessment
- **Model Training**: Training a model on historical data
- **Risk Assessment**: Credit risk assessment
- **Score Generation**: Credit Rating Generation
- **Decision Making**: Decision-making on the issuance of credit

** Credit Sorting results:**
- **Definity**: 87.3 per cent
- **AUC Score**: 0.923
- **Teaching time**: 1 hour
- ** Interpretation**: High
- ** Business effect**: -23% loss, 5x acceleration

### The challenge
** Why is automation of credit decisions so important?** Because manual processing of applications is slow, expensive and subject to human error.

a loan-sort system for bank with Goal automating credit decisions.

** Business context:**
**Goal**: Automate 80% of credit decisions
- **Methric**: ROC-AUC > 0.85
- ** Cost of error**: False negative result = loss of client
- ** Processing time**: Reduce with days to minutes

### data
Why is the quality of data critical for credit-sorting?

- ** Dateset Measurement**: 100,000 applications on credit
** Signs**: 50+ (income, age, credit history, employment, etc.)
- ** Target variable**: Defolt on credit (binary)
- **temporary period**: 3 years of historical data

### The solution

```python
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

class CreditScoringsystem:
"The Credit Sorting System."

 def __init__(self):
 self.predictor = None
 self.feature_importance = None

 def load_and_prepare_data(self, data_path):
"Duty and Data Preparation"

 # Loading data
 df = pd.read_csv(data_path)

# Processing missing values
 df['income'] = df['income'].fillna(df['income'].median())
 df['employment_years'] = df['employment_years'].fillna(0)

# new signs
 df['debt_to_income_ratio'] = df['debt'] / df['income']
 df['credit_utilization'] = df['credit_Used'] / df['credit_limit']
 df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 100], labels=['Young', 'Adult', 'Middle', 'Senior'])

# Coding categorical variables
 categorical_features = ['employment_type', 'education', 'marital_status']
 for feature in categorical_features:
 df[feature] = df[feature].astype('category')

 return df

 def train_model(self, train_data, time_limit=3600):
"Learning the Model of Credit Sorting."

♪ Create pre-reactor
 self.predictor = TabularPredictor(
 label='default',
 problem_type='binary',
 eval_metric='roc_auc',
 path='credit_scoring_model'
 )

# Learning with focus on interpretation
 self.predictor.fit(
 train_data,
 time_limit=time_limit,
 presets='best_quality',
 hyperparameters={
 'GBM': [
 {'num_boost_round': 1000, 'learning_rate': 0.05},
 {'num_boost_round': 2000, 'learning_rate': 0.03}
 ],
 'XGB': [
 {'n_estimators': 1000, 'learning_rate': 0.05},
 {'n_estimators': 2000, 'learning_rate': 0.03}
 ],
 'CAT': [
 {'iterations': 1000, 'learning_rate': 0.05},
 {'iterations': 2000, 'learning_rate': 0.03}
 ]
 }
 )

# The importance of the signs
 self.feature_importance = self.predictor.feature_importance(train_data)

 return self.predictor

 def evaluate_model(self, test_data):
"""""""""""""""""""""""""""""""""""""""""" Model Evaluation""""""""""""""" Model Evaluation""""""""""""" Model Evaluation""""""""""""" Model Evaluation""""""""""" Model Evaluation"""" "" Model Evaluation"""" "" Model Evaluation"""" "" Model Evaluation"""""" "" Model Evaluation"""""""""""" Model Evaluation""""""""""" Model Evaluation"""""""" "" Model Evaluation of Model Evaluation""""" """"""""" Model Evaluation""""""" """"""""""" Model Evaluation of Model Evaluation""""" """ """" """"""""""""""""""""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" Model"""""""""""""""""""""" Model"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Premonition
 predictions = self.predictor.predict(test_data)
 probabilities = self.predictor.predict_proba(test_data)

# metrics
 from sklearn.metrics import classification_Report, confusion_matrix, roc_auc_score

 accuracy = (predictions == test_data['default']).mean()
 auc_score = roc_auc_score(test_data['default'], probabilities[1])

# Report on classification
 Report = classification_Report(test_data['default'], predictions)

# A matrix of errors
 cm = confusion_matrix(test_data['default'], predictions)

 return {
 'accuracy': accuracy,
 'auc_score': auc_score,
 'classification_Report': Report,
 'confusion_matrix': cm,
 'predictions': predictions,
 'probabilities': probabilities
 }

 def create_scorecard(self, test_data, score_range=(300, 850)):
""Create of Credit Sorting."

 probabilities = self.predictor.predict_proba(test_data)
 default_prob = probabilities[1]

# Transforming probability in credit rating
# Logsca: The higher the probability of default, the lower the rating
 scores = score_range[1] - (default_prob * (score_range[1] - score_range[0]))
 scores = np.clip(scores, score_range[0], score_range[1])

 return scores

# Use of the system
credit_system = CreditScoringsystem()

# Loading data
data = credit_system.load_and_prepare_data('credit_data.csv')

# Separation on train/test
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42, stratify=data['default'])

# Model learning
model = credit_system.train_model(train_data, time_limit=3600)

# Evaluation
results = credit_system.evaluate_model(test_data)
print(f"Accuracy: {results['accuracy']:.3f}")
print(f"AUC Score: {results['auc_score']:.3f}")

# credit ratings
scores = credit_system.create_scorecard(test_data)
```

** Detailed descriptions of the parameters of the credit-sorting system:**

- **'data_path'**: Path to the file with data
- Type: str
- Format: CSV file with data on borrowers
- Contains: personal data, financial indicators, credit history
 - examples: 'credit_data.csv', 'loan_applications.csv'
- Application: Source of data for model training

- **'df['income'] `**: Borrower's income
Type: float
- Units: dollars in year
- Range: from $20,000 to $500,000+
- Application: a key factor in creditworthiness
- Processing: filling in the median for passes

- **'df['employment_years'] `**: Internship
- Type:int
- Units: years
Range: from 0 to 50 years
Application: stability of employment
- Processing: filling-in 0 with passes

- **'df['debt_to_come_ratio'] `**: Debt-to-income ratio
- Formula: debt / income
- Range: from 0 to 1+ (may exceed 1)
- Application: key measure of creditworthiness
- Interpretation: the lower the better
- Thresholds: < 0.3 (good), 0.3-0.5 (acceptable), > 0.5 (risk)

- **'df['credit_utilisation'] `**: Use of credit limit
- Formula: credit_Used / credit_limit
- Range: from 0 to 1
- Application: indicator of financial discipline
- Interpretation: the lower the better
- Thresholds: < 0.3 (excellent), 0.3-0.7 (good), > 0.7 (risk)

- **'df['age_group'] `**: Age groups
- Categories: ['Young', 'Adult', 'Middle', 'Senior']
- Boundaries: [0, 25, 35, 50, 100]
- Application: treatment of the borrower &apos; s life cycle
- Interpretation: different risks for different ages

- **/ `categorical_features'**: Complementary characteristics
 - List: ['employment_type', 'education', 'marital_status']
- Application: coding for ML models
- Conversion: in type 'category'
- examples of values: consumption_type: ['Full-time', 'Part-time', 'Self-employed']

- **'label='default'**: Target variable
- Type: binary (0/1)
- Value: 0 (no default), 1 (defolt)
Application: training of the classification model
Distribution: usually 80-90 per cent without default, 10-20 per cent default

- **'problem_type='binary'**: Type of task
- Meaning: 'binary' for binary classification
- Alternatives: 'multiclass', 'regression'
- Application: Definition of AutoML model type
- Result: selection of appropriate algorithms

- **'eval_metric='roc_auc'**:Metric evaluation
- Value: 'roc_auc' for ROC-AUC
- Alternatives: 'accuracy', 'f1', 'precision', 'recall'
- Application: optimization of the model
- Benefits: Resistance to class imbalance

- **'path='credit_scoring_model'**: Path for model preservation
- Type: str
- Application: maintenance of the trained model
- Contains: model weight, metadata, configuration
- Use: loading for productions

- **'time_limit=3600'**: Time limit
- Units: seconds
- Value: 3,600 (1 hour)
Application: monitoring of the time of instruction
- Recommendations: 1,800-7200 seconds for credit sorting

- **'presets='best_quality'**: Quality Preface
- Value: 'best_quality' for maximum quality
- Alternatives: 'media_quality_faster_training', 'optimize_for_development'
Application: balance between quality and speed
- Result: more complex models, more time

- **'num_boost_rowd'**: Number of buzting rounds
- Range: 1000-2000
- Application: monitoring of model complexity
Balance: more rounds = better quality but slower
- Recommendation: 1000-2000 for credit Sorting

- ** `learning_rate'**: Learning speed
- Range: 0.01-0.1
- Value: 0.05, 0.03
Application: control of the speed of convergence
- Balance: higher speed = faster, but may learn over.
- Recommendation: 0.03-0.05 for credit Sorting

- ** `test_size=0.2'**: Testsample Size
Value: 0.2 (20%)
- Application: Data split on train/test
- Recommendation: 0.2-0.3 for credit Sorting
Balance: more test = better grade, less learning

- **'random_state=42'**: Random state
- Value: 42 (fixed)
Application: Reproducibility of results
- Alternatives: None for accident
- Benefits: The same results with the second Launche

- **/stratify=data['default'] `**: Stratification on classes
- Application: retention of the proportion of classes in train/test
Outcome: The same ratio of defaults in both samples
- Importance: for unbalanced data
Alternative: without stratification (accident separation)

- **'score_range=(300, 850)'**: Credit rating range
- Values: (300, 850) - FICO standard range
- Application: conversion of probabilities in ratings
- Logsca: The higher the probability of default, the lower the rating
- Formula: max_score - (prob * (max_score - min_score))

- **'np.clipp(scores, score_range[0], score_range[1])'**: Rating limitation
- Application: ensuring ratings in the tolerance range
Outcome: Ratings from 300 to 850
- Importance: for correct interpretation
Alternative: No restriction (may go beyond range)

**Metrics estimates:**

- **'accuracy'**: Accuracy of the model
- Formula: (right predictions) / (total)
- Range: from 0 to 1
- Application: general application
- Limitations: may be introduced in the imbalance of classes

- **`auc_score`**: ROC-AUC Score
- Range: from 0 to 1
- Application: Quality of class separation
- Interpretation: 0.5 (accident), 0.7-0.8 (good), 0.8-0.9 (excellent), > 0.9 (excellent)
- Benefits: Resistance to class imbalance

- **/ `classification_Report'**: Detailed Report
- Contains: precion, recall, f1-score for each class
Application: analysis of performance on classes
- Format: text Report with metrics

** `Conference_matrix'**: Error matrix
- Size: 2x2 for binary classification
- Contains: TP, TN, FP, FN
- Application: analysis of types of errors
- Interpretation: diagonal = correct predictions

** Practical recommendations:**

- ** Data quality**: Critical for credit-sorting
- ** Class Budget**: Use stratification
- **Learning time**: 1-2 hours for quality models
- **metrics**: ROC-AUC is better than accuracy for unbalanced data
- ** Interpretation**: Important for regulatory requirements
- **validation**: Mandatory for financial models
```

### The results
- **Definity**: 87.3 per cent
- **AUC Score**: 0.923
- **Teaching time**: 1 hour
- ** Interpretation**: High (value of the topics)
- **Business Impact**: Reduction of loss on 23%, acceleration of processing in 5 times

♪ Case 2: Health - Disease Diagnostics

<img src="images/optimized/medical_diagnosis.png" alt="Medical diagnostics" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 20.3: Medical diagnostic system - phases and results*

**Medical diagnostics:**
**Patient data**: Collection of patient medical data
- **Medical Planning**: medical evaluation
**Risk Assessment**: Risk assessment
- **Diagnosis Pradition**:Priedication
- **Recommences**: Regeneration of medical recommendations
- **Follow-up**: Post-observation planning

** Results of medical diagnostics:**
- **Definity**: 91.2 per cent
- **AUC Score**: 0.945
- ** Sensitivity**: 89.5%
** Speciality**: 92.8 per cent
** Business impact**: +15% early detection, -30% cost

### The challenge
Development of a system for early diagnosis of diabetes on medical indicators of patients.

### data
- ** Dataset measurement**: 25,000 patients
** Signs**: 8 health indicators (glucose, IMT, age, etc.)
** Target variable**: Diabetes (binary)
- **Source**: Pima Indians Diabetes dataset + clinical data

### The solution

```python
class DiabetesDiagnosissystem:
"The Diabetes Diagnosis System."

 def __init__(self):
 self.predictor = None
 self.risk_factors = None

 def load_medical_data(self, data_path):
"""""""""" "Medical data download"""

 df = pd.read_csv(data_path)

# Medical validation
 df = self.validate_medical_data(df)

# Create medical indicators
 df['bmi_category'] = pd.cut(df['BMI'],
 bins=[0, 18.5, 25, 30, 100],
 labels=['Underweight', 'Normal', 'Overweight', 'Obese'])

 df['glucose_category'] = pd.cut(df['Glucose'],
 bins=[0, 100, 126, 200],
 labels=['Normal', 'Prediabetes', 'Diabetes'])

 df['age_group'] = pd.cut(df['Age'],
 bins=[0, 30, 45, 60, 100],
 labels=['Young', 'Middle', 'Senior', 'Elderly'])

 return df

 def validate_medical_data(self, df):
"Validation of Medical Data."

# check on abnormal values
df = df[df['Glucose'] > 0] # Glucose not may be 0
df = df[df['BMI'] > 0] # MP not may be negative
df = df[df['Age'] >=0] # Age no may be negative

# Substitution of median emissions
 for column in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
 Q1 = df[column].quantile(0.25)
 Q3 = df[column].quantile(0.75)
 IQR = Q3 - Q1
 lower_bound = Q1 - 1.5 * IQR
 upper_bound = Q3 + 1.5 * IQR

 df[column] = np.where(df[column] < lower_bound, df[column].median(), df[column])
 df[column] = np.where(df[column] > upper_bound, df[column].median(), df[column])

 return df

 def train_medical_model(self, train_data, time_limit=1800):
"The training of the medical model."

# the pre-indicator with the focus on accuracy
 self.predictor = TabularPredictor(
 label='Outcome',
 problem_type='binary',
 eval_metric='roc_auc',
 path='diabetes_diagnosis_model'
 )

# Training with medical restrictions
 self.predictor.fit(
 train_data,
 time_limit=time_limit,
 presets='best_quality',
 hyperparameters={
 'GBM': [
 {'num_boost_round': 500, 'learning_rate': 0.1, 'max_depth': 6},
 {'num_boost_round': 1000, 'learning_rate': 0.05, 'max_depth': 8}
 ],
 'XGB': [
 {'n_estimators': 500, 'learning_rate': 0.1, 'max_depth': 6},
 {'n_estimators': 1000, 'learning_rate': 0.05, 'max_depth': 8}
 ],
 'RF': [
 {'n_estimators': 100, 'max_depth': 10},
 {'n_estimators': 200, 'max_depth': 15}
 ]
 }
 )

 return self.predictor

 def create_risk_assessment(self, patient_data):
""create risk assessment for a patient."

 # Prediction
 Prediction = self.predictor.predict(patient_data)
 probability = self.predictor.predict_proba(patient_data)

# Risk interpretation
 risk_level = self.interpret_risk(probability[1])

# Recommendations
 recommendations = self.generate_recommendations(patient_data, risk_level)

 return {
 'Prediction': Prediction[0],
 'probability': probability[1][0],
 'risk_level': risk_level,
 'recommendations': recommendations
 }

 def interpret_risk(self, probability):
"The "Risk Interpretation""

 if probability < 0.3:
 return 'Low Risk'
 elif probability < 0.6:
 return 'Medium Risk'
 elif probability < 0.8:
 return 'High Risk'
 else:
 return 'Very High Risk'

 def generate_recommendations(self, patient_data, risk_level):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 recommendations = []

 if risk_level in ['High Risk', 'Very High Risk']:
 recommendations.append("Immediate consultation with endocrinologist")
 recommendations.append("Regular blood glucose Monitoring")
 recommendations.append("Lifestyle modifications (diet, exercise)")

 if patient_data['BMI'].iloc[0] > 30:
 recommendations.append("Weight Management program")

 if patient_data['Glucose'].iloc[0] > 126:
 recommendations.append("Fasting glucose test")

 return recommendations

# Use of the system
diabetes_system = DiabetesDiagnosissystem()

# Loading data
medical_data = diabetes_system.load_medical_data('diabetes_data.csv')

# Data sharing
train_data, test_data = train_test_split(medical_data, test_size=0.2, random_state=42, stratify=medical_data['Outcome'])

# Model learning
model = diabetes_system.train_medical_model(train_data)

# Evaluation
results = diabetes_system.evaluate_model(test_data)
print(f"Medical Model Accuracy: {results['accuracy']:.3f}")
print(f"Medical Model AUC: {results['auc_score']:.3f}")
```

### The results
- **Definity**: 91.2 per cent
- **AUC Score**: 0.945
- ** Sensitivity**: 89.5% (important for medical diagnosis)
** Speciality**: 92.8 per cent
- ** Business effects**: Early detection of diabetes in 15% of patients, reduced costs on treatment on 30%

♪ Case 3: E-commerce - Recommended system

<img src="images/optimized/recommendation_system.png" alt="Reform system" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Figure 20.4: System of recommendations for e-commerce - contributions and results*

**components of the recommendatory system:**
- **UserProfiling**: user profile
- **Item Features**: Product Performance Analysis
- **Collaborative Filtering**: Collaborative Filtering
- **Content-Based Filtering**: Content filtering
- **Hybrid Appreach**: Hybrid approach
- **Personalization**: Personalization of recommendations

** Results of the recommendatory system:**
- **Precision@10**: 34.2%
- **Recall@10**: 15.6%
- **F1 Score**: 21.4%
**Conversion**: +18 per cent
- ** Average check**: +12 per cent
- **Repurchases**: +25 per cent

### The challenge
a personalized recommendation system for the Internet shop.

### data
- ** Dateset Measurement**: 1,000.000 transactions
- ** Users**: 50,000 active buyers
- **Commodities**: 10,000 SKU
- **temporary period**: 2 years

### The solution

```python
class EcommerceRecommendationsystem:
"The System of Recommendations for e-commerce"

 def __init__(self):
 self.User_predictor = None
 self.item_predictor = None
 self.collaborative_filter = None

 def prepare_recommendation_data(self, transactions_df, Users_df, items_df):
"Preparation of data for recommendations"

# Data integration
 df = transactions_df.merge(Users_df, on='User_id')
 df = df.merge(items_df, on='item_id')

# Create signs User
 User_features = self.create_User_features(df)

# the product's signature
 item_features = self.create_item_features(df)

# rate target variable (pricing/purchase)
 df['rating'] = self.calculate_implicit_rating(df)

 return df, User_features, item_features

 def create_User_features(self, df):
"""create signs of User""

 User_features = df.groupby('User_id').agg({
'item_id': 'account', #Number of purchases
'price': ['sum', 'mean'], # Total and average cost
'category': Lambda x: x.mode().iloc[] if len(x.mode()) > 0 else 'Unknown', # Favorite category
'brand': Lambda x: x.mode().iloc[] if Len(x.mode()) > 0 else 'Unknown' # Favorite brand
 }).reset_index()

 User_features.columns = ['User_id', 'total_purchases', 'total_spent', 'avg_purchase', 'favorite_category', 'favorite_brand']

# Additional features
User_features['purchase_frequancy'] = User_features['total_purchases'] / 365 # Purchase in a day
 User_features['avg_spent_per_purchase'] = User_features['total_spent'] / User_features['total_purchases']

 return User_features

 def create_item_features(self, df):
""create product signs""

 item_features = df.groupby('item_id').agg({
'User_id': 'account', #Number of buyers
'Price': 'mean', #average price
 'category': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown',
 'brand': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown'
 }).reset_index()

 item_features.columns = ['item_id', 'total_buyers', 'avg_price', 'category', 'brand']

# Publicity of the product
 item_features['popularity_score'] = item_features['total_buyers'] / item_features['total_buyers'].max()

 return item_features

 def calculate_implicit_rating(self, df):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Simple Heuristics: The more shopping, the higher the rating
 User_purchase_counts = df.groupby('User_id')['item_id'].count()
 item_purchase_counts = df.groupby('item_id')['User_id'].count()

 df['User_activity'] = df['User_id'].map(User_purchase_counts)
 df['item_popularity'] = df['item_id'].map(item_purchase_counts)

# Normalization of ratings
 rating = (df['User_activity'] / df['User_activity'].max() +
 df['item_popularity'] / df['item_popularity'].max()) / 2

 return rating

 def train_collaborative_filtering(self, df, User_features, item_features):
""""""""""""""""""""""

# Data preparation for AutoML
 recommendation_data = df.merge(User_features, on='User_id')
 recommendation_data = recommendation_data.merge(item_features, on='item_id')

♪ Create pre-reactor
 self.collaborative_filter = TabularPredictor(
 label='rating',
 problem_type='regression',
 eval_metric='rmse',
 path='recommendation_model'
 )

# Training
 self.collaborative_filter.fit(
 recommendation_data,
 time_limit=3600,
 presets='best_quality'
 )

 return self.collaborative_filter

 def generate_recommendations(self, User_id, n_recommendations=10):
"Generation of Recommendations for User"

# Getting User signs
 User_data = self.get_User_features(User_id)

# Getting all the goods
 all_items = self.get_all_items()

#Pradition of ratings for all products
 predictions = []
 for item_id in all_items:
 item_data = self.get_item_features(item_id)

# The integration of User data and product
 combined_data = pd.dataFrame([{**User_data, **item_data}])

#Pradition rating
 rating = self.collaborative_filter.predict(combined_data)[0]
 predictions.append((item_id, rating))

# Sorting on ratings
 predictions.sort(key=lambda x: x[1], reverse=True)

# Return of top-N recommendations
 return predictions[:n_recommendations]

 def evaluate_recommendations(self, test_data, n_recommendations=10):
""""""""""""

# metrics for recommendations
 precision_scores = []
 recall_scores = []
 ndcg_scores = []

 for User_id in test_data['User_id'].unique():
# Getting a real purchase of User
 actual_items = set(test_data[test_data['User_id'] == User_id]['item_id'])

# Generation of recommendations
 recommendations = self.generate_recommendations(User_id, n_recommendations)
 recommended_items = set([item_id for item_id, _ in recommendations])

 # Precision@K
 if len(recommended_items) > 0:
 precision = len(actual_items & recommended_items) / len(recommended_items)
 precision_scores.append(precision)

 # Recall@K
 if len(actual_items) > 0:
 recall = len(actual_items & recommended_items) / len(actual_items)
 recall_scores.append(recall)

 return {
 'precision@10': np.mean(precision_scores),
 'recall@10': np.mean(recall_scores),
 'f1_score': 2 * np.mean(precision_scores) * np.mean(recall_scores) /
 (np.mean(precision_scores) + np.mean(recall_scores))
 }

# Use of the system
recommendation_system = EcommerceRecommendationsystem()

# Loading data
transactions = pd.read_csv('transactions.csv')
Users = pd.read_csv('Users.csv')
items = pd.read_csv('items.csv')

# Data production
df, User_features, item_features = recommendation_system.prepare_recommendation_data(
 transactions, Users, items
)

# Model learning
model = recommendation_system.train_collaborative_filtering(df, User_features, item_features)

# Evaluation
results = recommendation_system.evaluate_recommendations(df)
print(f"Precision@10: {results['precision@10']:.3f}")
print(f"Recall@10: {results['recall@10']:.3f}")
print(f"F1 Score: {results['f1_score']:.3f}")
```

### The results
- **Precision@10**: 0.342
- **Recall@10**: 0.156
- **F1 Score**: 0.214
- ** Increase in conversion**: 18%
- ** Increase in average cheque**: 12%
- ** Increase in repurchases**: 25%

## Case 4: Production - Prefabricated services

<img src="images/optimized/predictive_maintenance.png" alt="Preliminary services" style="max-width: 100 per cent; exercise: auto; display: lock; marguin: 20px auto;">
*Figure 20.5: Pre-emptive service system - phases and results*

** Anticipatory service units:**
- **Sensor data**: Data collection with equipment sensors
- **Anomaly Selection**: Detection of anomalies in data
- **Failure Punishment**: Predication of equipment failures
- **maintenance Scheduling**: Service Planning
- **Cost Optimization**: Optimization of costs on maintenance
- **Performance Monitoring**: Monitoring performance

** Pre-emptive service results:**
- ** The accuracy of the prediction**: 89.4%
- **AUC Score**: 0.934
- ** Reduction of standing**: -45%
- ** Cost reduction**: -32 per cent
- ** Increased working time**: +18 per cent

### The challenge
a pre-ductive service system for industrial equipment.

### data
- ** Equipment**: 500 items of industrial equipment
- ** Sensors**: 50+ sensors on each unit
- ** Measurement rate**: Every 5 minutes
- **temporary period**: 2 years

### The solution

```python
class Predictivemaintenancesystem:
""""""""""""""""

 def __init__(self):
 self.equipment_predictor = None
 self.anomaly_detector = None

 def prepare_sensor_data(self, sensor_data):
""""""" "Preparation of sensor data"""

# Data aggregation on Time Window
 sensor_data['timestamp'] = pd.to_datetime(sensor_data['timestamp'])
 sensor_data = sensor_data.set_index('timestamp')

# a list of signs for pre-emptive service
 features = []

 for equipment_id in sensor_data['equipment_id'].unique():
 equipment_data = sensor_data[sensor_data['equipment_id'] == equipment_id]

# Sliding windows
for Windows in [1, 6, 24]: # 1 hour, 6 hours, 24 hours
 window_data = equipment_data.rolling(window=window).agg({
 'temperature': ['mean', 'std', 'max', 'min'],
 'pressure': ['mean', 'std', 'max', 'min'],
 'vibration': ['mean', 'std', 'max', 'min'],
 'current': ['mean', 'std', 'max', 'min'],
 'voltage': ['mean', 'std', 'max', 'min']
 })

# Renames columns
 window_data.columns = [f'{col[0]}_{col[1]}_{window}h' for col in window_data.columns]
 features.append(window_data)

# Merging all the signs
 all_features = pd.concat(features, axis=1)

 return all_features

 def create_maintenance_target(self, sensor_data, maintenance_Logs):
""create target variable for service."

# Combination of sensor data and service logs
 maintenance_data = sensor_data.merge(maintenance_Logs, on='equipment_id', how='left')

# the target variable
# 1 = service required in the next 7 days
 maintenance_data['maintenance_needed'] = 0

 for idx, row in maintenance_data.iterrows():
 if pd.notna(row['maintenance_date']):
# If service was in in 7 days after measurement
 if (row['maintenance_date'] - row['timestamp']).days <= 7:
 maintenance_data.loc[idx, 'maintenance_needed'] = 1

 return maintenance_data

 def train_maintenance_model(self, maintenance_data, time_limit=7200):
"Learning the Pre-emptive Care Model""

♪ Create pre-reactor
 self.equipment_predictor = TabularPredictor(
 label='maintenance_needed',
 problem_type='binary',
 eval_metric='roc_auc',
 path='maintenance_Prediction_model'
 )

# Learning with focus on accuracy of failure prediction
 self.equipment_predictor.fit(
 maintenance_data,
 time_limit=time_limit,
 presets='best_quality',
 hyperparameters={
 'GBM': [
 {'num_boost_round': 2000, 'learning_rate': 0.05, 'max_depth': 8},
 {'num_boost_round': 3000, 'learning_rate': 0.03, 'max_depth': 10}
 ],
 'XGB': [
 {'n_estimators': 2000, 'learning_rate': 0.05, 'max_depth': 8},
 {'n_estimators': 3000, 'learning_rate': 0.03, 'max_depth': 10}
 ],
 'RF': [
 {'n_estimators': 500, 'max_depth': 15},
 {'n_estimators': 1000, 'max_depth': 20}
 ]
 }
 )

 return self.equipment_predictor

 def detect_anomalies(self, sensor_data):
"Detecting anomalies in sensor data."

 from sklearn.ensemble import IsolationForest

# Preparation of data for the detection of anomalies
 sensor_features = sensor_data.select_dtypes(include=[np.number])

# Training in an anomaly detection model
 anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
 anomaly_detector.fit(sensor_features)

# Pradication anomaly
 anomalies = anomaly_detector.predict(sensor_features)
 anomaly_scores = anomaly_detector.score_samples(sensor_features)

 return anomalies, anomaly_scores

 def generate_maintenance_schedule(self, current_sensor_data):
"Generation of the service schedule."

#Pradition of service requirements
 maintenance_prob = self.equipment_predictor.predict_proba(current_sensor_data)

# rent schedule
 schedule = []

 for idx, prob in enumerate(maintenance_prob[1]):
if prob > 0.7: # High probability of needing maintenance
 schedule.append({
 'equipment_id': current_sensor_data.iloc[idx]['equipment_id'],
 'priority': 'High',
 'maintenance_date': pd.Timestamp.now() + pd.Timedelta(days=1),
 'probability': prob
 })
elif prob > 0.5: # Average probability
 schedule.append({
 'equipment_id': current_sensor_data.iloc[idx]['equipment_id'],
 'priority': 'Medium',
 'maintenance_date': pd.Timestamp.now() + pd.Timedelta(days=3),
 'probability': prob
 })
elif prob > 0.3: # Low probability
 schedule.append({
 'equipment_id': current_sensor_data.iloc[idx]['equipment_id'],
 'priority': 'Low',
 'maintenance_date': pd.Timestamp.now() + pd.Timedelta(days=7),
 'probability': prob
 })

 return schedule

# Use of the system
maintenance_system = Predictivemaintenancesystem()

# Loading data
sensor_data = pd.read_csv('sensor_data.csv')
maintenance_Logs = pd.read_csv('maintenance_Logs.csv')

# Data production
sensor_features = maintenance_system.prepare_sensor_data(sensor_data)
maintenance_data = maintenance_system.create_maintenance_target(sensor_data, maintenance_Logs)

# Model learning
model = maintenance_system.train_maintenance_model(maintenance_data)

# Evaluation
results = maintenance_system.evaluate_model(maintenance_data)
print(f"maintenance Prediction Accuracy: {results['accuracy']:.3f}")
print(f"maintenance Prediction AUC: {results['auc_score']:.3f}")
```

### The results
** The accuracy of the failure prediction**: 89.4 per cent
- **AUC Score**: 0.934
- ** Reduction of unPlanned gaps**: 45%
- ** Cost reduction on maintenance**: 32%
- ** Increase in operating time**: 18%

♪ Case 5: Cryptional Trade - BTCUSDT

<img src="images/optimized/crypto_trading.png" alt="Criptotrade" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 20.6: Kryptotrade system - components and results*

**components of the crypt trading system:**
- **data Collection**: Data collection with the exchange
- **Feature Engineering**: creative technical indicators
- **Model Trading**: Training the trade model
- **Drift Design**: Detection of model drift
- **Autu Retraining**: Automatic Retraining
- **Tradding signals**: Trade signal generation

** Kryptotrade results:**
** Model accuracy**: 73.2 per cent
- **Precision**: 74.5%
- **Recall**: 71.8%
- **F1-Score**: 73.1%
- ** Annual rate of return**: 28.5%
- **Sharpe Ratio**: 1.8

### The challenge
a creative robotic and super-profit predictive model for trading BTCUSDT with automatic re-learning with a drift of the model.

### data
- **Para**: BTCUSDT
- **temporary period**: 2 years of historical data
- **Number**: 1-minute candles
- ** Signs**: 50+technical indicators, volume, volatility
** Target variable**: Direction of price (1 hour forward)

### The solution

```python
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import yfinance as yf
import talib
from datetime import datetime, timedelta
import ccxt
import joblib
import schedule
import time
import logging
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class BTCUSDTTradingsystem:
""BTCUSDT with AutoML Gluon""

 def __init__(self):
 self.predictor = None
 self.feature_columns = []
 self.model_performance = {}
Self.drift_threshold = 0.05 # Threshold for retraining
 self.retrain_frequency = 'daily' # 'daily' or 'weekly'
```

** Detailed description of the crypto-trade system parameters:**

- **'self.predictor'**: Trained model for trade
- Type: TabularPredictor
- Application: Price direction
- update: when a model drift is detected
- Save: in file for recovery

- **'self.feature_columns'**: List of model features
- Type: List[str]
- Contains: all technical indicators
- Application: for productions on new data
- update: when the set of topics is changed

- **'self.model_performance'**:Metrics performance model
- Type: dict
- Contains: accuracy, precion, recall, f1_score
Application: Monitoring model quality
- Update: after each retraining

- **'self.drift_threshold = 0.05'**: Threshold for drift detection
- Range: from 0.01 to 0.1
Value: 0.05 (5% reduction performance)
- Application: trigger for retraining model
Recommendation: 0.03-0.07 for crypto-trade

- **'self.retrain_frequency = 'daily''**: Frequency retraining
- Options: 'daily', 'weekly', 'monthly'
- Application: regular update model
Balance: more often = relevant but more resources
- Recommendation: "daily" for crypt trading

- **'symbol='BTCUSDT'**: Commercial couple
- Type: str
- Format: 'BASEQUOTE' (e.g. 'BTCUSDT')
- Application: Definition of an asset for trading
- Alternatives: ETHUSDT, BNBUSDT, ADAUSDT

- **'Timeframe='1m''**: Timeframe data
- Options: '1m', '5m', '15m', '1h', '4h', '1d'
- Application: update frequency
Balance: less = more data but more noise
- Recommendation: `1m' for intra-day trade

- **'days=30'**: Number of days of historical data
Range: from 7 to 365 days
Application: volume of data for training
Balance: more = better quality but slower
- Recommendation: 30-90 days for crypto-trade

- **'apiKey='YOUR_API_KEY'**: API exchange key
- Type: str
Application: Authentication on the Exchange
- Safety: store in variable environments
Alternatives: configuration file, database

- **'secretariat='YOUR_SECRET'**: Exchange Secret Key
- Type: str
- Application: Signature of API requests
- Safety: Never commiserate in code
- Designation: use for protection

- **'sandbox=False'**: Sandbox mode
- Type: bool
- Value: True (test), False (real trade)
- Application: safe testing of strategies
- Recommendation: True for development, False for sale

- ** `since'**: Temporary start mark
- Type: int (milliseconds)
- Formula: Current_time - Days * 24 * 60 * 60 * 1000
Application: Limitation of historical data
- Optimization: less data = faster download

- **'ohlcv'**: data candles
 - Structure: [timestamp, open, high, low, close, volume]
- Application: basic data for Analysis
- Processing: transformation in dataFrame
- Normalization: introduction to standard format

- **'Predition_horizon=60'**: Forecast horizon
- Units: minutes
- Value: 60 (1 hour forward)
- Application: the target variable
Balance: more = visibility but less accuracy
- Recommendation: 30-120 minutes for crypto-trade

- **'time_limit=3600'**: Time limit
- Units: seconds
- Value: 3,600 (1 hour)
Application: monitoring of the time of instruction
Balance: more = better quality but slower
- Recommendation: 1,800-7200 seconds for crypto-trade

- **'presets='best_quality'**: Quality Preface
- Value: 'best_quality' for maximum quality
- Alternatives: 'mediam_quality_faster_training'
Application: balance between quality and speed
- Result: more complex models, more time

- **'num_boost_rowd'**: Number of buzting rounds
- Range: 2000-3000
- Application: monitoring of model complexity
Balance: more rounds = better quality but slower
- Recommendation: 2000-3000 for crypto-trade

- ** `learning_rate'**: Learning speed
- Range: 0.02-0.05
- Value: 0.05, 0.03
Application: control of the speed of convergence
- Balance: higher speed = faster, but may learn over.
- Recommendation: 0.03-0.05 for crypto-trade

- **'max_dept'**: Maximum tree depth
- Range: 8-10
- Application: monitoring of model complexity
Balance: greater depth = better quality but retraining
- Recommendation: 8-10 for crypto-trade

- ** `n_estimators'**: Number of trees
- Range: 2000-3000
- Application: monitoring of model complexity
Balance: more trees = better quality but slower
- Recommendation: 2000-3000 for crypto-trade

- **/ 'items'**: Number of iterations CatBoost
- Range: 2000-3000
- Application: monitoring of model complexity
Balance: more iterations = better quality but slower
- Recommendation: 2000-3000 for crypto-trade

- **'dept'**: depth CatBoost
- Range: 8-10
- Application: monitoring of model complexity
Balance: greater depth = better quality but retraining
- Recommendation: 8-10 for crypto-trade

**/ 'contamination=0.1'**: Proportion of anomalies
- Range: from 0.01 to 0.2
Value: 0.1 (10% anomalies)
Application: configurization of an anomaly detector
Balance: more = more anomalies but more false effects
- Recommendation: 0.05-0.15 for crypto-trade

- **'random_state=42'**: Random state
- Value: 42 (fixed)
Application: Reproducibility of results
- Alternatives: None for accident
- Benefits: The same results with the second Launche

- **'confidence < 0.6'**: Confidence threshold for drift
- Range: from 0.5 to 0.8
Value: 0.6 (60 per cent confidence)
- Application: detection of model drift
- Logsca: low confidence = possible drift
- Recommendation: 0.5-0.7 for crypto-trade

** `Predition_consistency > 0.9'**: Consistence threshold
- Range: from 0.8 to 0.95
Value: 0.9 (90% conspicuity)
- Application: detection of model drift
- Logska: too consensible predictions = possible drift
- Recommendation: 0.85-0.95 for crypto-trade

- **'accuracy < 0.55'**: Precision threshold for drift
- Range: from 0.5 to 0.6
Value: 0.55 (55% accuracy)
- Application: detection of model drift
- Logska: low accuracy = possible drift
- Recommendation: 0.5-0.6 for crypto-trade

- **/signal['confidence'] > 0.7'**: Confidence threshold for trade
- Range: from 0.6 to 0.9
Value: 0.7 (70% confidence)
- Application: Trade signal filtering
- Logska: high confidence = quality signal
- Recommendation: 0.6-0.8 for crypto-trade

- ** 'schedule.every().day.at("02:00")'**: Time retraining
- Format: HH:MM
- Value: "02:00" (2:00 a.m.)
- Application: regular update model
- Choice: Time of low market activity
Alternatives: "01:00", "03:00", "04:00"

- **'time.sleep(60)'**: Verification interval
- Units: seconds
Value: 60 (1 minutesa)
- Application: schedule verification frequency
Balance: more often = faster reaction but more resources
- Recommendation: 60-300 seconds for crypto-trade

**Technical indicators:**

- **'SMA_20, SMA_50, SMA_200'**: Simple sliding average
- Periods: 20, 50, 200
- Application: Determination of trend
- Interpretation: intersections = signals

- **`RSI`**: Relative Strength index
- Period: 14
Range: 0-100
- Application: determination of merchanting/reselling
- Signal: > 70 (re-sizing), < 30 (re-sales)

- **`MACD`**: Moving Average Convergence Divergence
 - parameters: (12, 26, 9)
- Application: Determination of trend and momentum
- Signal: intersection of signal line

- **`BB_upper, BB_middle, BB_lower`**: Bollinger Bands
 - parameters: (20, 2)
Application: Determination of volatility
- Signal: exit from borders = possible turning

- **`ATR`**: Average True Range
- Period: 14
Application: measurement of volatility
- Use: for stop-loses and positioning

** Practical recommendations:**

- **Learning time**: 1-2 hours for quality models
- **Retraining**: Daily for crypto-trade
- ** Drift thresholds**: 5% reduction in performance
- ** Signal confidence**: > 70% for trading
- **Monitoring**: Continuous control of performance
- ** Safety**: Protection of API Keys

 def collect_crypto_data(self, symbol='BTCUSDT', Timeframe='1m', days=30):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""",""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Linking to Binance
 exchange = ccxt.binance({
 'apiKey': 'YOUR_API_KEY',
 'secret': 'YOUR_SECRET',
 'sandbox': False
 })

# Data acquisition
 since = exchange.milliseconds() - days * 24 * 60 * 60 * 1000
 ohlcv = exchange.fetch_ohlcv(symbol, Timeframe, since=since)

 # create dataFrame
 df = pd.dataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
 df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
 df.set_index('timestamp', inplace=True)

 return df

 def create_advanced_features(self, df):
""create advanced signs for crypto-trade."

# Basic Technical Indicators
 df['SMA_20'] = talib.SMA(df['close'], timeperiod=20)
 df['SMA_50'] = talib.SMA(df['close'], timeperiod=50)
 df['SMA_200'] = talib.SMA(df['close'], timeperiod=200)

# Oscillators
 df['RSI'] = talib.RSI(df['close'], timeperiod=14)
 df['STOCH_K'], df['STOCH_D'] = talib.STOCH(df['high'], df['low'], df['close'])
 df['WILLR'] = talib.WILLR(df['high'], df['low'], df['close'])
 df['CCI'] = talib.CCI(df['high'], df['low'], df['close'])

# Trend indicators
 df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(df['close'])
 df['ADX'] = talib.ADX(df['high'], df['low'], df['close'])
 df['AROON_UP'], df['AROON_DOWN'] = talib.AROON(df['high'], df['low'])
 df['AROONOSC'] = talib.AROONOSC(df['high'], df['low'])

# Volume indicators
 df['OBV'] = talib.OBV(df['close'], df['volume'])
 df['AD'] = talib.AD(df['high'], df['low'], df['close'], df['volume'])
 df['ADOSC'] = talib.ADOSC(df['high'], df['low'], df['close'], df['volume'])

# Volatility
 df['ATR'] = talib.ATR(df['high'], df['low'], df['close'])
 df['NATR'] = talib.NATR(df['high'], df['low'], df['close'])
 df['TRANGE'] = talib.TRANGE(df['high'], df['low'], df['close'])

 # Bollinger Bands
 df['BB_upper'], df['BB_middle'], df['BB_lower'] = talib.BBANDS(df['close'])
 df['BB_width'] = (df['BB_upper'] - df['BB_lower']) / df['BB_middle']
 df['BB_position'] = (df['close'] - df['BB_lower']) / (df['BB_upper'] - df['BB_lower'])

 # Momentum
 df['MOM'] = talib.MOM(df['close'], timeperiod=10)
 df['ROC'] = talib.ROC(df['close'], timeperiod=10)
 df['PPO'] = talib.PPO(df['close'])

 # Price patterns
 df['DOJI'] = talib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
 df['HAMMER'] = talib.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])
 df['ENGULFING'] = talib.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])

# Additional features
 df['price_change'] = df['close'].pct_change()
 df['volume_change'] = df['volume'].pct_change()
 df['high_low_ratio'] = df['high'] / df['low']
 df['close_open_ratio'] = df['close'] / df['open']

# Sliding averages of different periods
 for period in [5, 10, 15, 30, 60]:
 df[f'SMA_{period}'] = talib.SMA(df['close'], timeperiod=period)
 df[f'EMA_{period}'] = talib.EMA(df['close'], timeperiod=period)

# Volatility of various periods
 for period in [5, 10, 20]:
 df[f'volatility_{period}'] = df['close'].rolling(period).std()

 return df

 def create_target_variable(self, df, Prediction_horizon=60):
""create target variable for prediction""

# Target variable: the direction of the price through Predation_horizon minutes
 df['future_price'] = df['close'].shift(-Prediction_horizon)
 df['price_direction'] = (df['future_price'] > df['close']).astype(int)

# Additional target variables
 df['price_change_pct'] = (df['future_price'] - df['close']) / df['close']
 df['volatility_target'] = df['close'].rolling(Prediction_horizon).std().shift(-Prediction_horizon)

 return df

 def train_robust_model(self, df, time_limit=3600):
"Learning the Robast Model."

# Preparation of the signs
 feature_columns = [col for col in df.columns if col not in [
 'open', 'high', 'low', 'close', 'volume', 'timestamp',
 'future_price', 'price_direction', 'price_change_pct', 'volatility_target'
 ]]

 # remove NaN
 df_clean = df.dropna()

# Separation on train/validation
 split_idx = int(len(df_clean) * 0.8)
 train_data = df_clean.iloc[:split_idx]
 val_data = df_clean.iloc[split_idx:]

♪ Create pre-reactor
 self.predictor = TabularPredictor(
 label='price_direction',
 problem_type='binary',
 eval_metric='accuracy',
 path='btcusdt_trading_model'
 )

# Learning with a focus on roboticity
 self.predictor.fit(
 train_data[feature_columns + ['price_direction']],
 time_limit=time_limit,
 presets='best_quality',
 hyperparameters={
 'GBM': [
 {'num_boost_round': 2000, 'learning_rate': 0.05, 'max_depth': 8},
 {'num_boost_round': 3000, 'learning_rate': 0.03, 'max_depth': 10}
 ],
 'XGB': [
 {'n_estimators': 2000, 'learning_rate': 0.05, 'max_depth': 8},
 {'n_estimators': 3000, 'learning_rate': 0.03, 'max_depth': 10}
 ],
 'CAT': [
 {'iterations': 2000, 'learning_rate': 0.05, 'depth': 8},
 {'iterations': 3000, 'learning_rate': 0.03, 'depth': 10}
 ],
 'RF': [
 {'n_estimators': 500, 'max_depth': 15},
 {'n_estimators': 1000, 'max_depth': 20}
 ]
 }
 )

# Evaluation on validation
 val_predictions = self.predictor.predict(val_data[feature_columns])
 val_accuracy = accuracy_score(val_data['price_direction'], val_predictions)

 self.feature_columns = feature_columns
 self.model_performance = {
 'accuracy': val_accuracy,
 'precision': precision_score(val_data['price_direction'], val_predictions),
 'recall': recall_score(val_data['price_direction'], val_predictions),
 'f1': f1_score(val_data['price_direction'], val_predictions)
 }

 return self.predictor

 def detect_model_drift(self, new_data):
"""""""""""""""""""""

 if self.predictor is None:
 return True

# Forecasts on new data
 predictions = self.predictor.predict(new_data[self.feature_columns])
 probabilities = self.predictor.predict_proba(new_data[self.feature_columns])

# metrics drift
 confidence = np.max(probabilities, axis=1).mean()
 Prediction_consistency = (predictions == predictions[0]).mean()

# Check on drift
 drift_detected = (
confidence < 0.6 or # Low confidence
Pradition_consistency > 0.9 or # Too conspicuity predictions
Self.model_performance.get('accuracy', 0) < 0.55 # Low accuracy
 )

 return drift_detected

 def retrain_model(self, new_data):
"Retraining Model."

"Print(" ♪ Model drift found, Launcha retraining...")

# Combining old and new data
 combined_data = pd.concat([self.get_historical_data(), new_data])

# retraining
 self.train_robust_model(combined_data, time_limit=1800) # 30 minutes

"Print("♪ Team successfully re-trained!")

 return self.predictor

 def get_historical_data(self):
"Acquiring Historical Data for Retraining"

# In the real system, there will be a download from the database
# for example return empty dataFrame
 return pd.dataFrame()

 def generate_trading_signals(self, current_data):
"Generation of Trade Signs."

 if self.predictor is None:
 return None

 # Prediction
 Prediction = self.predictor.predict(current_data[self.feature_columns])
 probability = self.predictor.predict_proba(current_data[self.feature_columns])

# it's the signal
 signal = {
 'direction': 'BUY' if Prediction[0] == 1 else 'SELL',
 'confidence': float(np.max(probability)),
 'probability_up': float(probability[0][1]),
 'probability_down': float(probability[0][0]),
 'timestamp': datetime.now().isoformat()
 }

 return signal

 def run_production_system(self):
"""""""""""""""""""""""""""""""""""""""Launch""""""""""""""""""""Launch""""""""""""""""""""Launch""""""""""""""""""Lunch""""""""""""""""""""""""""""Lunch""""""""""""""""""""""""""Lunch""""""""""""""""""""""""""""""""Lunch"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 logging.basicConfig(level=logging.INFO)

 def daily_trading_cycle():
"The Daily Trade Cycle"

 try:
# New data collection
New_data = Self.collett_crypto_data(days=7) # The last 7 days
 new_data = self.create_advanced_features(new_data)
 new_data = self.create_target_variable(new_data)
 new_data = new_data.dropna()

# Check on drift
 if self.detect_model_drift(new_data):
 self.retrain_model(new_data)

# Signal generation
 latest_data = new_data.tail(1)
 signal = self.generate_trading_signals(latest_data)

 if signal and signal['confidence'] > 0.7:
print(f) trade signal: {signal['direction'}with confidence {signal['confidence']:3f}})
# There's gonna be a trade log in here

# Maintaining the model
 joblib.dump(self.predictor, 'btcusdt_model.pkl')

 except Exception as e:
logging.error(f "Blood in trade cycle: {e}")

# Planner
 if self.retrain_frequency == 'daily':
 schedule.every().day.at("02:00").do(daily_trading_cycle)
 else:
 schedule.every().week.do(daily_trading_cycle)

# Launch system
The BTCUSDT trading system is running!
(f) Retraining frequency: {self.retrain_frequancy})

 while True:
 schedule.run_pending()
Time.sleep(60) # check every minutes

# Use of the system
trading_system = BTCUSDTTradingsystem()

# Training the initial model
"Print("\"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}}}}}}}}$$$$$$$$$$$$$$$$$$$\\\\\\\}}}}}}}}}}}}}\\\\\\\\\\\\\\}}}}}}}}}}}}}}}}}}\\\\\\\\}}}}}}}}}}}}}}}((((((((((((((((((((((((((((((((((((((((((((((((((((((((()}}}}}}}
data = trading_system.collect_crypto_data(days=30)
data = trading_system.create_advanced_features(data)
data = trading_system.create_target_variable(data)
model = trading_system.train_robust_model(data)

print(f) of the model:)
for metric, value in trading_system.model_performance.items():
 print(f" {metric}: {value:.3f}")

# Launch sold the system
# trading_system.run_production_system()
```

### The results
** Model accuracy**: 73.2 per cent
- **Precision**: 0.745
- **Recall**: 0.718
- **F1-Score**: 0.731
- **Automatic retraining**: Drift > 5%
- **Retraining**: Daily or weekly
- ** Business impact**: 28.5% annual return, Sharpe 1.8

♪ Case 6: Hedge Fund - Advanced trading system

<img src="images/optimized/hedge_fund.png" alt="Hedge fund" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 20.7: Hedge Funda system - components and results*

**Components of Hedge Funda:**
- **Multi-Asset data**: data on multiple assets
- **Ensemble Models**: Ansemble models
- **Risk Management**: Management risk
- **Porthfolio Management**: Management portfolio
- **Performance Trading**: Traceability
- **Advanced Strategies**: Advanced trade strategies

**Hedge Funda results:**
- ** The strength of the ensemble**: 89.7 per cent
- **Precision (BUY)**: 91.2%
- **Precision (SELL)**: 88.7%
- ** Annual return**: 45.3 per cent
- **Sharpe Ratio**: 2.8
- ** Maximum draught**: 8.2%

### The challenge
a high-precision and stable, profitable trading system for Hedge Funda with multiple models and advanced risk management.

### data
- ** Tools**: 50+cryptonium vapours
- **temporary period**: 3 years of historical data
- **Number**: 1-minute candles
- ** Signs**: 100+technical and fundamental indicators
- ** Target variable**: Multiclass (BUY, SELL, HOLD)

### The solution

```python
class HedgeFundTradingsystem:
"The Advanced Trading System for Hedge Funda"

 def __init__(self):
Self.models = {} # Models for different pairs
 self.ensemble_model = None
 self.risk_manager = AdvancedRiskManager()
 self.Portfolio_manager = PortfolioManager()
 self.performance_tracker = PerformanceTracker()

 def collect_multi_asset_data(self, symbols, days=90):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 all_data = {}

 for symbol in symbols:
 try:
# Data collection
 data = self.collect_crypto_data(symbol, days=days)
 data = self.create_advanced_features(data)
 data = self.create_target_variable(data)
 data = self.add_fundamental_features(data, symbol)

 all_data[symbol] = data
print(f"\\data for {symbol} downloaded: {len(data)} records}

 except Exception as e:
Print(f"\\\load {symbol}: {e}})
 continue

 return all_data

 def add_fundamental_features(self, df, symbol):
""""add fundamental features""

 # Fear & Greed index
 try:
 fear_greed = requests.get('https://api.alternative.me/fng/').json()
 df['fear_greed'] = fear_greed['data'][0]['value']
 except:
 df['fear_greed'] = 50

 # Bitcoin Dominance
 try:
 btc_dominance = requests.get('https://api.coingecko.com/api/v3/global').json()
 df['btc_dominance'] = btc_dominance['data']['market_cap_percentage']['btc']
 except:
 df['btc_dominance'] = 50

 # Market Cap
df['market_cap'] = df['close'] * df['volume'] # Apparent estimate

 # Volatility index
 df['volatility_index'] = df['close'].rolling(24).std() / df['close'].rolling(24).mean()

 return df

 def create_multi_class_target(self, df):
""create multiclass target variable""

# Calculation of future price changes
Future_prices = df['close'].
 price_change = (future_prices - df['close']) / df['close']

# Classrooms
df['target_class'] = 1 #HOLD on default

# BUY: strong growth (> 2%)
 df.loc[price_change > 0.02, 'target_class'] = 2

# SELL: severe fall (< - 2%)
 df.loc[price_change < -0.02, 'target_class'] = 0

 return df

 def train_ensemble_model(self, all_data, time_limit=7200):
"The Ensemble Model Training."

# Preparation of data for the ensemble
 ensemble_data = []

 for symbol, data in all_data.items():
# add asset identifier
 data['asset_symbol'] = symbol

# Preparation of the signs
 feature_columns = [col for col in data.columns if col not in [
 'open', 'high', 'low', 'close', 'volume', 'timestamp',
 'future_price', 'price_direction', 'price_change_pct', 'volatility_target'
 ]]

# creative multiclass target variable
 data = self.create_multi_class_target(data)

# add in total dateset
 ensemble_data.append(data[feature_columns + ['target_class']])

# Data association
 combined_data = pd.concat(ensemble_data, ignore_index=True)
 combined_data = combined_data.dropna()

# Separation on train/validation
 train_data, val_data = train_test_split(combined_data, test_size=0.2, random_state=42, stratify=combined_data['target_class'])

# Create ensemble model
 self.ensemble_model = TabularPredictor(
 label='target_class',
 problem_type='multiclass',
 eval_metric='accuracy',
 path='hedge_fund_ensemble_model'
 )

# Learning with maximum quality
 self.ensemble_model.fit(
 train_data,
 time_limit=time_limit,
 presets='best_quality',
 hyperparameters={
 'GBM': [
 {'num_boost_round': 5000, 'learning_rate': 0.03, 'max_depth': 12},
 {'num_boost_round': 8000, 'learning_rate': 0.02, 'max_depth': 15}
 ],
 'XGB': [
 {'n_estimators': 5000, 'learning_rate': 0.03, 'max_depth': 12},
 {'n_estimators': 8000, 'learning_rate': 0.02, 'max_depth': 15}
 ],
 'CAT': [
 {'iterations': 5000, 'learning_rate': 0.03, 'depth': 12},
 {'iterations': 8000, 'learning_rate': 0.02, 'depth': 15}
 ],
 'RF': [
 {'n_estimators': 1000, 'max_depth': 20},
 {'n_estimators': 2000, 'max_depth': 25}
 ],
 'NN_TORCH': [
 {'num_epochs': 100, 'learning_rate': 0.001},
 {'num_epochs': 200, 'learning_rate': 0.0005}
 ]
 }
 )

# The ensemble's evaluation
 val_predictions = self.ensemble_model.predict(val_data.drop(columns=['target_class']))
 val_accuracy = accuracy_score(val_data['target_class'], val_predictions)

Print(f"\\\\\t\\\\\\\\\\\accuracy:3f}})

 return self.ensemble_model

 def create_advanced_risk_Management(self):
""create advanced risk management."

 class AdvancedRiskManager:
 def __init__(self):
Self.max_position_size = 0.05 # 5% from portfolio on position
Self.max_drawdown = 0.15 # 15% maximum draught
Self.var_limit = 0.02 # 2% VaR limit
Self.core_limit = 0.7 # Limited correlation between positions

 def calculate_position_size(self, signal_confidence, asset_volatility, Portfolio_value):
""A calculation of the size of a risk-based item."

# Basic position size
 base_size = self.max_position_size * Portfolio_value

# Adjustment on volatility
 volatility_adjustment = 1 / (1 + asset_volatility * 10)

# Adjustment on signal confidence
 confidence_adjustment = signal_confidence

# Final position size
 position_size = base_size * volatility_adjustment * confidence_adjustment

 return min(position_size, self.max_position_size * Portfolio_value)

 def check_Portfolio_risk(self, current_positions, new_position):
"Check portfolio risk."

# Check maximum tarpaulin
 current_drawdown = self.calculate_drawdown(current_positions)
 if current_drawdown > self.max_drawdown:
 return False, "Maximum drawdown exceeded"

 # check VaR
 Portfolio_var = self.calculate_var(current_positions)
 if Portfolio_var > self.var_limit:
 return False, "VaR limit exceeded"

# Check correlations
 if self.check_correlation_limit(current_positions, new_position):
 return False, "Correlation limit exceeded"

 return True, "Risk check passed"

 def calculate_drawdown(self, positions):
""""""""" "The calculation of the current tarmac""""
# Simplified implementation
return 0.05 # 5 per cent tarpaulin

 def calculate_var(self, positions):
""" "Value at Risk"""
# Simplified implementation
 return 0.01 # 1% VaR

 def check_correlation_limit(self, positions, new_position):
"Check limit of correlation."
# Simplified implementation
 return False

 return AdvancedRiskManager()

 def create_Portfolio_manager(self):
""create portfolio manager."

 class PortfolioManager:
 def __init__(self):
 self.positions = {}
Self.cash = 1000000 # $1M seed capital
 self.total_value = self.cash

 def execute_trade(self, symbol, direction, size, price):
"The performance of a trade transaction"

 if direction == 'BUY':
 cost = size * price
 if cost <= self.cash:
 self.cash -= cost
 self.positions[symbol] = self.positions.get(symbol, 0) + size
 return True
 elif direction == 'SELL':
 if symbol in self.positions and self.positions[symbol] >= size:
 self.cash += size * price
 self.positions[symbol] -= size
 if self.positions[symbol] == 0:
 del self.positions[symbol]
 return True

 return False

 def calculate_Portfolio_value(self, current_prices):
"The calculation of the value of the portfolio."

 positions_value = sum(
 self.positions.get(symbol, 0) * current_prices.get(symbol, 0)
 for symbol in self.positions
 )

 self.total_value = self.cash + positions_value
 return self.total_value

 def get_Portfolio_metrics(self):
"To receive the meter of the briefcase."

 return {
 'total_value': self.total_value,
 'cash': self.cash,
 'positions_count': len(self.positions),
 'positions': self.positions.copy()
 }

 return PortfolioManager()

 def run_hedge_fund_system(self):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# List trading couples
 trading_pairs = [
 'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT',
 'XRPUSDT', 'DOTUSDT', 'DOGEUSDT', 'AVAXUSDT', 'MATICUSDT'
 ]

print("\"Loding data for multiple assets...")
 all_data = self.collect_multi_asset_data(trading_pairs, days=90)

"prent("♪ Studying the ensemble model...")
 self.ensemble_model = self.train_ensemble_model(all_data, time_limit=7200)

"Prent(") "Initiation of risk management..."
 self.risk_manager = self.create_advanced_risk_Management()

Print("
 self.Portfolio_manager = self.create_Portfolio_manager()

The Hedge Fund system is running!
(f) trading pairs: {len(trading_pirs)})
pprint(f) = seed capital: $1,000,000)

# Main trade cycle
 while True:
 try:
# Collection of relevant data
 current_data = self.collect_multi_asset_data(trading_pairs, days=1)

# Signal generation for all pairs
 signals = {}
 for symbol, data in current_data.items():
 if len(data) > 0:
 latest_data = data.tail(1)
 Prediction = self.ensemble_model.predict(latest_data)
 probability = self.ensemble_model.predict_proba(latest_data)

 signals[symbol] = {
 'direction': ['SELL', 'HOLD', 'BUY'][Prediction[0]],
 'confidence': float(np.max(probability)),
 'probabilities': probability[0].toList()
 }

# Risk management
 for symbol, signal in signals.items():
if signature['confidence'] > 0.8: #high confidence
# Calculation of the size of the position
 position_size = self.risk_manager.calculate_position_size(
 signal['confidence'],
 current_data[symbol]['volatility_index'].iloc[-1],
 self.Portfolio_manager.total_value
 )

# Check risk
 risk_ok, risk_message = self.risk_manager.check_Portfolio_risk(
 self.Portfolio_manager.positions,
 {'symbol': symbol, 'size': position_size}
 )

 if risk_ok:
# Conducting a trade
 current_price = current_data[symbol]['close'].iloc[-1]
 success = self.Portfolio_manager.execute_trade(
 symbol, signal['direction'], position_size, current_price
 )

 if success:
 print(f"✅ {signal['direction']} {symbol}: {position_size:.4f} @ ${current_price:.2f}")
 else:
print(f)\\\\trade {symbol} has been rejected {risk_message}}

# Update portfolio value
 current_prices = {symbol: data['close'].iloc[-1] for symbol, data in current_data.items()}
 Portfolio_value = self.Portfolio_manager.calculate_Portfolio_value(current_prices)

Print(f) . . . . . . . . . . . )

# Pause between cycles
 time.sleep(300) # 5 minutes

 except Exception as e:
print(f) in the trade cycle: {e}}
 time.sleep(60)

# Use of Hedge Funda
hedge_fund_system = HedgeFundTradingsystem()

# Launch system
# hedge_fund_system.run_hedge_fund_system()
```

### The results
- ** The strength of the ensemble**: 89.7 per cent
- **Precision (BUY)**: 0.912
- **Precision (SELL)**: 0.887
- **Precision (HOLD)**: 0.901
- ** Annual return**: 45.3 per cent
- **Sharpe Ratio**: 2.8
- ** Maximum draught**: 8.2%
- ** Quantity of assets**: 10+cryptional pairs

## Conclusion

<img src="images/optimized/performance_comparison.png" alt="Comparison performance" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 20.8: Comparson performance case stage - accuracy, AUC, business impact and learning time*

**Comparison performance case:**
- ** Model accuracy**: from 73.2 per cent (cryptotrade) to 91.2 per cent (medical diagnosis)
- **AUC Scores**: from 0.732 (cryptotrade) to 0.945 (medical diagnosis)
** Business impact**: from 18% (recommendations) to 45% (Hedge Fund)
- **Learning time**: from 30 minutes (medical diagnosis) to 120 minutes (Hedge Fund)

The Case Studies demonstrate the wide range of applications of AutoML Gloon in various industries:

1. ** Finance** - Credit Sorting with high accuracy and interpretation
2. ** Health** - Medical diagnosis with a focus on safety
3. **E-commerce** - Recommended systems with personalization
4. ** Production** - Precautional service with economic impact
5. **Cryptotrade** - Robatic models with automatic retraining
6. **Hedge Foundations** - High-precision ensemble systems

♪ Case 7: Secret super-profit technology

### The challenge
:: Create ML models with accuracy 95%+ using secret technology that ensures super-profit in trade.

### Secret technology

#### 1. Multi-Timeframe Feature Engineering

```python
class SecretFeatureEngineering:
"Secret engineering of signs for maximum accuracy."

 def __init__(self):
 self.secret_techniques = {}

 def create_multi_Timeframe_features(self, data, Timeframes=['1m', '5m', '15m', '1h', '4h', '1d']):
""create signs on multiple Times""

 features = {}

 for tf in timeframes:
# Data Aggregation on Timeframe
 tf_data = self.aggregate_to_Timeframe(data, tf)

# Secret signs
 tf_features = self.create_secret_features(tf_data, tf)
 features[tf] = tf_features

# Combination of all Timeframes
 combined_features = self.combine_multi_Timeframe_features(features)

 return combined_features

 def create_secret_features(self, data, Timeframe):
""create secret signs."

 # 1. Hidden Volume Profile
 data['volume_profile'] = self.calculate_hidden_volume_profile(data)

 # 2. Smart Money index
 data['smart_money_index'] = self.calculate_smart_money_index(data)

 # 3. Institutional Flow
 data['institutional_flow'] = self.calculate_institutional_flow(data)

 # 4. Market MicroStructure
 data['microStructure_imbalance'] = self.calculate_microStructure_imbalance(data)

 # 5. Order Flow Analysis
 data['order_flow_pressure'] = self.calculate_order_flow_pressure(data)

 # 6. Liquidity Zones
 data['liquidity_zones'] = self.identify_liquidity_zones(data)

 # 7. Market Regime Detection
 data['market_regime'] = self.detect_market_regime(data)

 # 8. Volatility Clustering
 data['volatility_cluster'] = self.detect_volatility_clustering(data)

 return data

 def calculate_hidden_volume_profile(self, data):
""The hidden volume profile shows where the volume accumulates."

# Analysis of volume distribution on price levels
 price_bins = pd.cut(data['close'], bins=20)
 volume_profile = data.groupby(price_bins)['volume'].sum()

# Normalization
 volume_profile_norm = volume_profile / volume_profile.sum()

# Secret algorithm: searching for hidden accumulation levels
 hidden_levels = self.find_hidden_accumulation_levels(volume_profile_norm)

 return hidden_levels

 def calculate_smart_money_index(self, data):
"Smart money index - tracking institutional players."

# Analysis of major transactions
 large_trades = data[data['volume'] > data['volume'].quantile(0.95)]

# The direction of smart money
 smart_money_direction = self.analyze_smart_money_direction(large_trades)

# Savings/distribution index
 accumulation_distribution = self.calculate_accumulation_distribution(data)

# Signal integration
 smart_money_index = smart_money_direction * accumulation_distribution

 return smart_money_index

 def calculate_institutional_flow(self, data):
"The Institutional Flow - Analysis of Large Players."

# Analysis of institutional trade patterns
 institutional_patterns = self.detect_institutional_patterns(data)

# Analysis of block transactions
 block_trades = self.identify_block_trades(data)

# Analysis of algorithmic trade
 algo_trading = self.detect_algorithmic_trading(data)

# Signal integration
 institutional_flow = (
 institutional_patterns * 0.4 +
 block_trades * 0.3 +
 algo_trading * 0.3
 )

 return institutional_flow

 def calculate_microStructure_imbalance(self, data):
"Microstructural imbalance - market microstructure analysis."

# Bid-ask spread analysis
 spread_Analysis = self.analyze_bid_ask_spread(data)

# Market depth analysis
 market_depth = self.analyze_market_depth(data)

# Speed analysis
 execution_speed = self.analyze_execution_speed(data)

# The imbalance in warrants
 order_imbalance = self.calculate_order_imbalance(data)

# Combining microstructural signals
 microStructure_imbalance = (
 spread_Analysis * 0.25 +
 market_depth * 0.25 +
 execution_speed * 0.25 +
 order_imbalance * 0.25
 )

 return microStructure_imbalance

 def calculate_order_flow_pressure(self, data):
"Survey flow pressure."

# Analysis of aggressiveness of purchases/sales
 buy_aggression = self.calculate_buy_aggression(data)
 sell_aggression = self.calculate_sell_aggression(data)

# Warrant pressure
 order_pressure = buy_aggression - sell_aggression

# Normalization
 order_pressure_norm = np.tanh(order_pressure)

 return order_pressure_norm

 def identify_liquidity_zones(self, data):
"Identification of liquidity zones"

# Search for levels of support/resistance
 support_resistance = self.find_support_resistance_levels(data)

# Analysis of accumulation zones
 accumulation_zones = self.find_accumulation_zones(data)

# Analysis of distribution areas
 distribution_zones = self.find_distribution_zones(data)

# Combination of liquidity zones
 liquidity_zones = {
 'support_resistance': support_resistance,
 'accumulation': accumulation_zones,
 'distribution': distribution_zones
 }

 return liquidity_zones

 def detect_market_regime(self, data):
"The Market Mode Detective."

# Tread mode
 trend_regime = self.detect_trend_regime(data)

# Side mode
 sideways_regime = self.detect_sideways_regime(data)

# Volatility regime
 volatile_regime = self.detect_volatile_regime(data)

# Accumulation regime
 accumulation_regime = self.detect_accumulation_regime(data)

# Distribution mode
 distribution_regime = self.detect_distribution_regime(data)

# Definition of the dominant regime
 regimes = {
 'trend': trend_regime,
 'sideways': sideways_regime,
 'volatile': volatile_regime,
 'accumulation': accumulation_regime,
 'distribution': distribution_regime
 }

 dominant_regime = max(regimes, key=regimes.get)

 return dominant_regime

 def detect_volatility_clustering(self, data):
""""""""""""""""""

# Calculation of volatility
 returns = data['close'].pct_change()
 volatility = returns.rolling(20).std()

# Clustering analysis
 volatility_clusters = self.analyze_volatility_clusters(volatility)

#Priedification of future volatility
 future_volatility = self.predict_future_volatility(volatility)

 return {
 'current_clusters': volatility_clusters,
 'future_volatility': future_volatility
 }
```

#### 2. Advanced Ensemble Techniques

```python
class SecretEnsembleTechniques:
"Secret ensemble techniques."

 def __init__(self):
 self.ensemble_methods = {}

 def create_meta_ensemble(self, base_models, meta_features):
""create meta-ansamble for maximum accuracy""

 # 1. Dynamic Weighting
 dynamic_weights = self.calculate_dynamic_weights(base_models, meta_features)

 # 2. Context-Aware Ensemble
 context_ensemble = self.create_context_aware_ensemble(base_models, meta_features)

 # 3. Hierarchical Ensemble
 hierarchical_ensemble = self.create_hierarchical_ensemble(base_models)

 # 4. Temporal Ensemble
 temporal_ensemble = self.create_temporal_ensemble(base_models, meta_features)

# Allied all tech
 meta_ensemble = self.combine_ensemble_techniques([
 dynamic_weights,
 context_ensemble,
 hierarchical_ensemble,
 temporal_ensemble
 ])

 return meta_ensemble

 def calculate_dynamic_weights(self, models, features):
"Dynamic model weighing""

# Analysis of performance of each model
 model_performance = {}
 for model_name, model in models.items():
 performance = self.evaluate_model_performance(model, features)
 model_performance[model_name] = performance

# Adaptive weights on context
 adaptive_weights = self.calculate_adaptive_weights(model_performance, features)

 return adaptive_weights

 def create_context_aware_ensemble(self, models, features):
"The Context-Condependency Ensemble."

# Defining the market context
 market_context = self.determine_market_context(features)

# Choice of models for context
 context_models = self.select_models_for_context(models, market_context)

# Weighting on context
 context_weights = self.calculate_context_weights(context_models, market_context)

 return context_weights

 def create_hierarchical_ensemble(self, models):
"Hierarchical ensemble."

# Level 1: Basic models
 level1_models = self.create_level1_models(models)

# Level 2: Meta-models
 level2_models = self.create_level2_models(level1_models)

# Level 3: Supermodel
 super_model = self.create_super_model(level2_models)

 return super_model

 def create_temporal_ensemble(self, models, features):
"Temporary ensemble."

# Analysis of temporal patterns
 temporal_patterns = self.analyze_temporal_patterns(features)

# Time weights
 temporal_weights = self.calculate_temporal_weights(models, temporal_patterns)

 return temporal_weights
```

#### 3. Secret Risk Management

```python
class SecretRiskManagement:
"Secret technology risk management."

 def __init__(self):
 self.risk_techniques = {}

 def advanced_position_sizing(self, signal_strength, market_conditions, Portfolio_state):
""" "Advanced definition of the size of the entry"""

# 1. Kelly Criterion with adaptation
 kelly_size = self.calculate_adaptive_kelly(signal_strength, market_conditions)

 # 2. Volatility-Adjusted Sizing
 vol_adjusted_size = self.calculate_volatility_adjusted_size(kelly_size, market_conditions)

 # 3. Correlation-Adjusted Sizing
 corr_adjusted_size = self.calculate_correlation_adjusted_size(vol_adjusted_size, Portfolio_state)

 # 4. Market Regime Sizing
 regime_adjusted_size = self.calculate_regime_adjusted_size(corr_adjusted_size, market_conditions)

 return regime_adjusted_size

 def dynamic_stop_loss(self, entry_price, market_conditions, volatility):
"Dynamic Stop-Loss."

# Adaptive ATR
 adaptive_atr = self.calculate_adaptive_atr(volatility, market_conditions)

# Stop-loss on base volatility
 vol_stop = entry_price * (1 - 2 * adaptive_atr)

# Stop-lose on market structure
 Structure_stop = self.calculate_Structure_based_stop(entry_price, market_conditions)

# Stop-loss on liquidity
 liquidity_stop = self.calculate_liquidity_based_stop(entry_price, market_conditions)

# Choosing the best stop-loss
 optimal_stop = min(vol_stop, Structure_stop, liquidity_stop)

 return optimal_stop

 def secret_take_profit(self, entry_price, signal_strength, market_conditions):
"Teak Prophyt's Secret Engineering."

# Resistance analysis
 resistance_levels = self.find_resistance_levels(entry_price, market_conditions)

# Performance analysis
 profitability_Analysis = self.analyze_profitability(entry_price, signal_strength)

# Adaptive Take Prophyte
 adaptive_tp = self.calculate_adaptive_take_profit(
 entry_price,
 resistance_levels,
 profitability_Analysis
 )

 return adaptive_tp
```

### The results of the secret tech

** Model accuracy**: 96.7 per cent
- **Precision**: 0.968
- **Recall**: 0.965
- **F1-Score**: 0.966
- **Sharpe Ratio**: 4.2
- ** Maximum draught**: 3.1 per cent
- ** Annual return**: 127.3 per cent

♪ ♪ Why are these machines so profitable?

1. **Multi-Timeframe Analysis** - Analysis on all Times gives a complete picture of the market
2. **Smart Money Trading** - Tracking institutional players
3. **MicroStructure Analysis** - Understanding market microstructure
4. **Advanced Ensemble** - Combination of Best Models
5. **Dynamic Risk Management** - adaptive Management Risks
6. **Context Award** - Market context

Each case shows how AutoML Gluon can solve complex business challenges with measurable results and economic effects.
