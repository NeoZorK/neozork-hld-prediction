#05. ♪ Model training

**Goal:** Learn to train effective ML models for financial data.

## Choice of algorithms for trading

**Theory:** The choice of financial data algorithms is critical to the success of ML systems. Financial data have unique features that require special approaches to model learning.

## # Why does not all algorithms fit?

**Theory:** Financial data have specific characteristics that make many standard ML algorithms ineffective or even dangerous. Understanding these features is critical for selecting the right algorithms.

** Financial data have features:**

**1. Instability**
**Theory:** Data distributions change over time due to changes in market conditions
- **why is it problematic: ** Standard algorithms imply static
- ** Impacts:** Models quickly get old, down.
- ** Plus: ** The possibility of adapting to changes
- **Disadvantages:**Complicity of learning, need for regular updating

**2. High volatility**
- **Theory:** Financial data contain a lot of noise and random fluctuations.
- What's the problem?
- ** Consequences:** False signals, retraining, instability
- ** Plus: ** Opportunity to identify real pathers
- **Disadvantages:** Noise filtering complexity, risk of re-training

**3. Inequitability**
- **Theory:** Rare but important events (crises, collapses) have a disproportionate impact
- Why is it problematic:** Standard algorithms can ignore rare events
- ** Impacts: ** Models may take critical events into account
- ** Plus:** Possible detection of anomalies
- **Disadvantages:** Class balance complexity, risk of ignoring important events

**4. Correlations**
- **Theory:** Signs are often highly correlated, which can lead to multicollinearity
- **Why is it problematic:** Correlated signs can distort results
- ** Impact: ** Model instability, complexity of interpretation
- ** Plus:** Opportunity to detect dependencies
- **Disadvantages:** Processing complexity, retraining risk

### Best algorithms for finance

**Theory:** The choice of algorithms for financial data should be based on their ability to work with non-permanent, noisy and corroded data. Some algorithms have shown particular efficiency in the financial sphere.

**1. Ansemble methhods**
- # Why is it effective ## Combining multiple models, reducing risk of retraining
- ** Plus:** High accuracy, emission resistance, interpretability
- **Disadvantages:** High computing costs, complexity Settings
- ** Application:** Random Forest, XGBost, LightGBM for classification and regression

**2. Neuronets**
- Why can't they model complex non-liner dependencies?
- ** Plus:** High flexibility, learning ability for complex pathists
- **Disadvantages:** Demands a lot of data, complexity of interpretation, risk of retraining
- ** Application:** LSTM, GRU for time series, Transformer for sequences

**3. SVM (Support Vector Machine)**
- Why is it effective? - Good Working with non-linear addictions.
- ** Plus: ** Effective on small data, emission-resistant
- **Disadvantages:** Slow learning on big data, complexity Settings
- ** Application: ** Classification of price directions

**4. Logistic Regression**
- Why is it effective:** Simple, interpreted, fast
- ** Plus:** Easy interpretation, fast Working, stability
- **Disadvantages:** Limited ability to model complex dependencies
- ** Application: ** Basic models, interpretable systems

** Further considerations:**
- **Regularization:** Important for prevention of retraining
- **Cross-validation:** Critical for time series
- ** Hyperparametric optimization:** Can significantly improve performance
- ** Ansemble:** Combination of algorithms often exceeds individual models

## Ansemble methhods

**Theory:** Ansamball methhods combine multiple models for improving performance. They are particularly effective for financial data because they reduce risk of re-training and increase stability of productions.

**Why ansemble methhods are effective for finance:**
- ** Risk reduction: ** Model combination reduces risk of errors
- ** Emission stability:** Different models on- and different responses on emissions
- **Stability:** Ansambles are more stable than individual models
- ** Interpretation: ** The importance of the topics can be analysed

### 1. Random Forest

**Theory:** Random Forest is a core tree ensemble that uses the bugging boots to create multiple models. Each tree is taught on random sub-sampling of data and features.

** Random Forest detailed theory:**

** Working principle:**
1. **Bootstrap Sampling:** Each tree is taught on random sample with return (usually 63% of data)
2. **Feature Randomness:** On each node of the tree, a random set of features is selected
3. **Voting/Averaging:** Final Adoption is the average or voting (classification) all trees

**Why Random Forest is effective for finance:**
- ** Retraining stability:** Multiple trees reduce the risk of retraining on noise
- ** Emission treatment:** Trees on-- Different responses to emissions, reducing their impact
- ** Interpretability:** The importance of the signs can be analysed through feature importation
- **Structure:** paralle train trees allows large amounts of data to be processed
- ** Resistance to multicollinearity:** Accidental selection of indicators reduces correlations

** Mathematical framework:**
- **Bootstrap:** for each tree t, learn on sample D_t obtained from D with return
- **Feature Selection:** on each node selects PP signs from p accessible
- **Predication:** ~ = (1/T) * ~(t=1 to T) f_t(x) where T is the number of trees

** Plus Random Forest:**
- High accuracy on most tasks
- Retraining resistance
- Inspirability through feature importation
- Speed of instruction and prediction
- Workinget with missing values
-not requires a scale of the topics

**Mine Random Forest:**
- Could be less accurate on very complex data.
- Settings are required (n_estimators, max_dept, etc.)
- Could be redundant for simple tasks.
- Bad Working with very diluted data
- They can relearning on very small datasets.
** Practical implementation Random Forest:**

What does this code do?
1. ** Data division:** Creates a learning and test sample with the retention of class proportions
2. **create model:** Sets up parameters Random Forest for financial data
3. **Learning:** Training model on learning data
4. ** Evaluation:** Checks performance on training and test samples

** Explanation of parameters:**
- `n_estimators=100': Number of trees in the forest (more = better but slower)
- `max_dept=10': Maximum tree depth (prevention)
- `min_samples_split=5': Minimum sample for node separation
- `min_samples_leaf=2': Minimum sample in sheet
- `n_jobs=1': Uses all available processor kernels

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_Report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def train_random_forest(X, y, test_size=0.2, random_state=42):
 """
Training Random Forest for Financial Data

 Args:
X (array-lake): Signal matrix (samples, features)
y (array-lake): Target variables (samples,)
test_size (float): Percentage of test data (0.0-1.0)
Random_state (int): Seed for reproducibility

 Returns:
tuple: (Learned model, metrics, importance of topics)
 """

"print("===Random Forest training===)
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
(pint(f"Classes: {np.unique(y, return_counts=True)})

# Disaggregation of data with retention of proportion of classes
 X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=test_size, random_state=random_state, stratify=y
 )

Print(f "Learning sample: {X_training.chape[0]} samples")
print(f"tests sample: {X_test.chape[0]} samples)

# rent model with optimized parameters for finance
 rf = RandomForestClassifier(
n_estimators=100, #Number of trees
max_dept=10, # Maximum depth (prevention)
min_samples_split=5, #Minimum for node separation
min_samples_leaf=2, #Minimum in sheet
max_features='sqrt', #Number of signs for separation
 bootstrap=True, # Bootstrap sampling
oob_score=True, # Out-of-bag evaluation
 random_state=random_state,
 n_jobs=-1, # parallel training
 verbose=0
 )

"Print("n Parameters of model:")
 print(f"n_estimators: {rf.n_estimators}")
 print(f"max_depth: {rf.max_depth}")
 print(f"max_features: {rf.max_features}")

# Model learning
Print('n Model Training...')
 rf.fit(X_train, y_train)

# Premonition
 y_train_pred = rf.predict(X_train)
 y_test_pred = rf.predict(X_test)

# Performance evaluation
 train_score = rf.score(X_train, y_train)
 test_score = rf.score(X_test, y_test)
 oob_score = rf.oob_score_

== Results============================)=========================)=================Prent(f)========= Results====)
 print(f"Train accuracy: {train_score:.4f}")
 print(f"Test accuracy: {test_score:.4f}")
 print(f"OOB score: {oob_score:.4f}")

# Detailed Report
 print(f"\n=== Classification Report (Test) ===")
 print(classification_Report(y_test, y_test_pred))

# The importance of signs
 feature_importance = rf.feature_importances_
 feature_names = [f'feature_{i}' for i in range(X.shape[1])]

# creative dataFrame with the importance of signs
 importance_df = pd.dataFrame({
 'feature': feature_names,
 'importance': feature_importance
 }).sort_values('importance', ascending=False)

== sync, corrected by elderman == @elder_man
 print(importance_df.head(10))

# metrics for return
 metrics = {
 'train_accuracy': train_score,
 'test_accuracy': test_score,
 'oob_score': oob_score,
 'feature_importance': importance_df,
 'confusion_matrix': confusion_matrix(y_test, y_test_pred)
 }

 return rf, metrics, importance_df

def plot_feature_importance(importance_df, top_n=15):
"Visualization of Significance""

 plt.figure(figsize=(10, 8))
 top_features = importance_df.head(top_n)

 sns.barplot(data=top_features, x='importance', y='feature')
plt.title(f'Purity of the signs (Top {top_n})')
plt.xlabel('value')
plt.ylabel('Creatures')
 plt.tight_layout()
 plt.show()

# Example of use:
def example_random_forest_usage():
""example of Random Forest""

# creative synthetic data for demonstration
 np.random.seed(42)
 n_samples, n_features = 1000, 20

# Signal generation
 X = np.random.randn(n_samples, n_features)

# the target variable with some Logska
 y = np.zeros(n_samples)
 for i in range(n_samples):
 if X[i, 0] > 0.5 and X[i, 1] < -0.3:
y[i] = 1 # Class 1
 elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
y[i] = 2 # Class 2
 else:
y[i] = 0 #Class 0

===Example of Random Forest================Random Forest===========================================)===========Random Forest========* Random Forest==============*Random Forest======================="Random Forest============* Random Forest======

# Model learning
 model, metrics, importance_df = train_random_forest(X, y)

# Visualizing the importance of signs
 plot_feature_importance(importance_df)

 return model, metrics

# Launch examples (upstream for testing)
# model, metrics = example_random_forest_usage()
```

### 2. XGBoost

**Theory:** XGBost (eXtreme Gradient Boosting) is an advanced implementation of gradient boutting, which is particularly effective for financial data because of its ability to handle non-linear dependencies and emissions.

** Detailed XGBoost theory:**

** Working principle:**
1. **Gradient Boosting:** consistently adds trees, each of which corrects previous mistakes
2. **Regularization:** uses L1 and L2 regularization for prevention of retraining
3. **Parollel Processing:** Optimized for parallel calculations
4. **Missing Value Handling:** Automatically processing missing values

**Why XGBoost is effective for finance:**
- ** High accuracy:** Often shows better results on table data
- ** Emission treatment:** Resistance to abnormal values
- **Feature importation:** Allows analysis of the importance of the topics
- **Structure:** Optimized for speed
- **Regularization:** In-house protection from retraining

** Mathematical framework:**
- **Objective Function:** L(φ) = Σ l(yi, ŷi) + Σ Ω(fk)
- **Gradient Boosting:** F_m(x) = F_{m-1}(x) + γ_m * h_m(x)
- **Regularization:** Ω(f) = γT + (1/2)λ||w||²

** Key variables:**
- `learning_rate': Learning speed (0.01-0.3)
- `max_dept': Tree depth (3-10)
- `n_estimators': Number of Boosters (50-1000)
- `subsample': Proportion of samples for each tree (0.6-1.0)
- `colsample_bytree': Percentage of signs for each tree (0.6-1.0)

** Practical implementation of XGBost:**

What does this code do?
1. **configuring parameters:** Optimizes paragraphs for financial data
2. **Early Stopping:** Prevents retraining through validation
3. ** Evaluation performance:** Uses instruments appropriate for finance
4. **Feature importation:** Analyses the importance of the topics

```python
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_Report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

def train_xgboost(X, y, test_size=0.2, random_state=42, early_stopping_rounds=10):
 """
XGBoost training for financial data

 Args:
X (array-lake): Signal matrix (samples, features)
y (array-lake): Target variables (samples,)
test_size (float): Percentage of test data (0.0-1.0)
Random_state (int): Seed for reproducibility
Early_stopping_runds (int): Number of rounds for flash-stapping

 Returns:
tuple: (Learned model, metrics, importance of topics)
 """

"spint("==== XGBoost training===)
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
(pint(f"Classes: {np.unique(y, return_counts=True)})

# Data sharing
 X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=test_size, random_state=random_state, stratify=y
 )

Print(f "Learning sample: {X_training.chape[0]} samples")
print(f"tests sample: {X_test.chape[0]} samples)

# Optimized paragraphs for financial data
 params = {
'objective': 'multi:softprob', # Multiclass classification with probabilities
'num_class': Len(np.unique(y)), #Number of classes
'max_dept': 6, # Tree depth (prevention)
'learning_rate': 0.1 # Learning speed
'n_estimators': 100, #Number of Boosters
'subsample': 0.8, # Proportion of samples for each tree
'colsample_bytree': 0.8, # Proportion of signs for each tree
'reg_alpha': 0.1 #L1 regularization
'reg_lambda': 1.0, #L2 regularization
 'random_state': random_state,
 'n_jobs': -1, # parallel training
'verbosity': 0 # Disable output
 }

"Prent("n Parameters XGBost:")
 for key, value in params.items():
 print(f"{key}: {value}")

♪ Create Model
 xgb_model = xgb.XGBClassifier(**params)

# Learning with a heartful stopping
Print('n Model Training...')
 xgb_model.fit(
 X_train, y_train,
 eval_set=[(X_test, y_test)],
 early_stopping_rounds=early_stopping_rounds,
 verbose=False
 )

# Premonition
 y_train_pred = xgb_model.predict(X_train)
 y_test_pred = xgb_model.predict(X_test)
 y_test_proba = xgb_model.predict_proba(X_test)

# Performance evaluation
 train_accuracy = accuracy_score(y_train, y_train_pred)
 test_accuracy = accuracy_score(y_test, y_test_pred)

== Results============================)=========================)=================Prent(f)========= Results====)
 print(f"Train accuracy: {train_accuracy:.4f}")
 print(f"Test accuracy: {test_accuracy:.4f}")
 print(f"Best iteration: {xgb_model.best_iteration}")
 print(f"Best score: {xgb_model.best_score:.4f}")

# Detailed Report
 print(f"\n=== Classification Report (Test) ===")
 print(classification_Report(y_test, y_test_pred))

# The importance of signs
 feature_importance = xgb_model.feature_importances_
 feature_names = [f'feature_{i}' for i in range(X.shape[1])]

# creative dataFrame with the importance of signs
 importance_df = pd.dataFrame({
 'feature': feature_names,
 'importance': feature_importance
 }).sort_values('importance', ascending=False)

== sync, corrected by elderman == @elder_man
 print(importance_df.head(10))

# metrics for return
 metrics = {
 'train_accuracy': train_accuracy,
 'test_accuracy': test_accuracy,
 'best_iteration': xgb_model.best_iteration,
 'best_score': xgb_model.best_score,
 'feature_importance': importance_df,
 'confusion_matrix': confusion_matrix(y_test, y_test_pred),
 'predictions': y_test_pred,
 'probabilities': y_test_proba
 }

 return xgb_model, metrics, importance_df

def plot_xgboost_importance(importance_df, top_n=15):
"Visualization of the Importance of XGBost Signs""

 plt.figure(figsize=(12, 8))
 top_features = importance_df.head(top_n)

 sns.barplot(data=top_features, x='importance', y='feature')
plt.title(f' Importance of XGBost (Top {top_n})')
plt.xlabel('value')
plt.ylabel('Creatures')
 plt.tight_layout()
 plt.show()

def plot_learning_curve(model, X_train, y_train, X_test, y_test):
"Visualization of the learning curve."

# Obtaining learning results
 results = model.evals_result()

 plt.figure(figsize=(12, 4))

# The error schedule
 plt.subplot(1, 2, 1)
 plt.plot(results['validation_0']['mlogloss'], label='Train')
 plt.plot(results['validation_1']['mlogloss'], label='Test')
 plt.title('Learning Curve - Log Loss')
 plt.xlabel('Iterations')
 plt.ylabel('Log Loss')
 plt.legend()
 plt.grid(True)

# Accuracy schedule
 plt.subplot(1, 2, 2)
 train_acc = [1 - x for x in results['validation_0']['mlogloss']]
 test_acc = [1 - x for x in results['validation_1']['mlogloss']]
 plt.plot(train_acc, label='Train')
 plt.plot(test_acc, label='Test')
 plt.title('Learning Curve - Accuracy')
 plt.xlabel('Iterations')
 plt.ylabel('Accuracy')
 plt.legend()
 plt.grid(True)

 plt.tight_layout()
 plt.show()

# Example of use:
def example_xgboost_usage():
""example XGBost""

# creative synthetic data for demonstration
 np.random.seed(42)
 n_samples, n_features = 1000, 20

# Evidence generation with some structure
 X = np.random.randn(n_samples, n_features)

# the target variable with non-linear relationships
 y = np.zeros(n_samples)
 for i in range(n_samples):
# Complex non-liner dependency
 score = (X[i, 0] ** 2 + X[i, 1] * X[i, 2] +
 np.sin(X[i, 3]) + X[i, 4] * X[i, 5])

 if score > 2.0:
y[i] = 2 # Class 2
 elif score > 0.5:
y[i] = 1 # Class 1
 else:
y[i] = 0 #Class 0

"print("== example use of XGBost===)

# Model learning
 model, metrics, importance_df = train_xgboost(X, y)

# Visualizing the importance of signs
 plot_xgboost_importance(importance_df)

 return model, metrics

# Launch examples (upstream for testing)
# model, metrics = example_xgboost_usage()
```

### 3. LightGBM

**Theory:** LightGBM (Light Gradient Bosting Machine) is the rapid and effective implementation of gradient buzting, unworking Microsoft. Particularly effective for large datasets and financial data, thanks to an optimized tree construction algorithm.

**LightGBM detailed theory:**

** Working principle:**
1. **Leaf-wise Groveth:** Builds trees on leaves and not on levels (like XGBost)
2. **Gradient-based one-side Sampling (GOSS):** uses only large gradient samples
3. **Exclusive Feature Bundling (EFB):** Grouping mutually exclusive features
4. **Categorical Feature Support:** Automatically processing categorical features

**Why LightGBM is effective for finance:**
- **Speed:** in 10-100 times faster than XGBost on Big Data
-** Memory:** Use less memory due to optimization
- * Accuracy: ** often shows better results
- **Categoral signs:** Excellent Working with financial categories
- **Regularization:** In-house protection from retraining

** Mathematical framework:**
- **Leaf-wise Groveth:** Picks the page with the maximum increase in information
- **GOSS:** uses top-a per cent of samples with large gradients + random b per cent of the rest
- **EFB:** Groups signs with low correlation

** Key variables:**
- `num_leaves': Number of leaves (31-255)
- `learning_rate': Learning speed (0.01-0.3)
- `feature_fraction': Percentage of topics (0.6-1.0)
- `bagging_fraction': Percentage of samples (0.6-1.0)
- `min_data_in_leaf': Minimum data in sheet (20-100)

**LightGBM implementation:**

What does this code do?
1. **Optified paragraphs:**configuring for financial data
2. **Early Stopping:** Prevention of retraining
3. **validation:** Monitoring performance
4. **Feature importation:** Analysis of the importance of topics

```python
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_Report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

def train_lightgbm(X, y, test_size=0.2, random_state=42, early_stopping_rounds=10):
 """
LightGBM training for financial data

 Args:
X (array-lake): Signal matrix (samples, features)
y (array-lake): Target variables (samples,)
test_size (float): Percentage of test data (0.0-1.0)
Random_state (int): Seed for reproducibility
Early_stopping_runds (int): Number of rounds for flash-stapping

 Returns:
tuple: (Learned model, metrics, importance of topics)
 """

"Prent("===LightGBM training===)
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
(pint(f"Classes: {np.unique(y, return_counts=True)})

# Data sharing
 X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=test_size, random_state=random_state, stratify=y
 )

Print(f "Learning sample: {X_training.chape[0]} samples")
print(f"tests sample: {X_test.chape[0]} samples)

# Optimized paragraphs for financial data
 params = {
'objective': 'multi-class', # Multi-class classification
'num_class': Len(np.unique(y)), #Number of classes
'boosting_type': 'gbdt', # Type of Boosting (Gradient Bosting Decision Tree)
'num_laves': 31, #Number of leaves (2\max_dept-1)
'learning_rate': 0.05, #Learning speed
'feature_fraction': 0.9, # Proportion of signs for each tree
'Bagging_fraction': 0.8, # Proportion of samples for each tree
'Bagging_freq': 5, #Bagging frequency
'min_data_in_leaf': 20, #minimum data in sheet
'min_sum_hessian_in_leaf': 1e-3, #minimum sum of Hessian in sheet
'labbda_l1': 0.1 #L1 regularization
'labbda_l2': 1.0, #L2 regularization
'min_ain_to_split':0.0, #minimum increase for separation
'max_dept': -1, # Maximum depth (-1 = unlimited)
'Save_binary':True, #Preserve binary files
'Seed': Random_state, #Seed for Reproducibility
 'feature_fraction_seed': random_state,
 'bagging_seed': random_state,
 'drop_seed': random_state,
 'data_random_seed': random_state,
'verbose': -1, # Disable output
 'n_jobs': -1 # parallel training
 }

"LightGBM:"
 for key, value in params.items():
 print(f"{key}: {value}")

# LightGBM datasets
 train_data = lgb.dataset(X_train, label=y_train)
 test_data = lgb.dataset(X_test, label=y_test, reference=train_data)

# Model learning
Print('n Model Training...')
 model = lgb.train(
 params,
 train_data,
 valid_sets=[test_data],
 num_boost_round=100,
 callbacks=[
 lgb.early_stopping(early_stopping_rounds),
lgb.log_evaluation(0) # Disable output of progress
 ]
 )

# Premonition
 y_train_pred = model.predict(X_train, num_iteration=model.best_iteration)
 y_test_pred = model.predict(X_test, num_iteration=model.best_iteration)

# Transforming probabilities in classes
 y_train_pred_class = np.argmax(y_train_pred, axis=1)
 y_test_pred_class = np.argmax(y_test_pred, axis=1)

# Performance evaluation
 train_accuracy = accuracy_score(y_train, y_train_pred_class)
 test_accuracy = accuracy_score(y_test, y_test_pred_class)

== Results============================)=========================)=================Prent(f)========= Results====)
 print(f"Train accuracy: {train_accuracy:.4f}")
 print(f"Test accuracy: {test_accuracy:.4f}")
 print(f"Best iteration: {model.best_iteration}")

# Detailed Report
 print(f"\n=== Classification Report (Test) ===")
 print(classification_Report(y_test, y_test_pred_class))

# The importance of signs
 feature_importance = model.feature_importance(importance_type='gain')
 feature_names = [f'feature_{i}' for i in range(X.shape[1])]

# creative dataFrame with the importance of signs
 importance_df = pd.dataFrame({
 'feature': feature_names,
 'importance': feature_importance
 }).sort_values('importance', ascending=False)

== sync, corrected by elderman == @elder_man
 print(importance_df.head(10))

# metrics for return
 metrics = {
 'train_accuracy': train_accuracy,
 'test_accuracy': test_accuracy,
 'best_iteration': model.best_iteration,
 'feature_importance': importance_df,
 'confusion_matrix': confusion_matrix(y_test, y_test_pred_class),
 'predictions': y_test_pred_class,
 'probabilities': y_test_pred
 }

 return model, metrics, importance_df

def plot_lightgbm_importance(importance_df, top_n=15):
"Visualization of the Significance of LightGBM""

 plt.figure(figsize=(12, 8))
 top_features = importance_df.head(top_n)

 sns.barplot(data=top_features, x='importance', y='feature')
plt.title(f' Importance of LightGBM Signs (Top {top_n})')
plt.xlabel('value')
plt.ylabel('Creatures')
 plt.tight_layout()
 plt.show()

def plot_lightgbm_learning_curve(model):
"Visualization of the LightGBM Learning Curve."

# Learning history
 history = model.evals_result_

 plt.figure(figsize=(12, 4))

# The error schedule
 plt.subplot(1, 2, 1)
 train_loss = history['training']['multi_logloss']
 valid_loss = history['valid_0']['multi_logloss']

 plt.plot(train_loss, label='Train')
 plt.plot(valid_loss, label='Validation')
 plt.title('Learning Curve - Multi Log Loss')
 plt.xlabel('Iterations')
 plt.ylabel('Multi Log Loss')
 plt.legend()
 plt.grid(True)

# Accuracy schedule
 plt.subplot(1, 2, 2)
 train_acc = [1 - x for x in train_loss]
 valid_acc = [1 - x for x in valid_loss]

 plt.plot(train_acc, label='Train')
 plt.plot(valid_acc, label='Validation')
 plt.title('Learning Curve - Accuracy')
 plt.xlabel('Iterations')
 plt.ylabel('Accuracy')
 plt.legend()
 plt.grid(True)

 plt.tight_layout()
 plt.show()

# Example of use:
def example_lightgbm_usage():
""example of LightGBM""

# creative synthetic data for demonstration
 np.random.seed(42)
 n_samples, n_features = 1000, 20

# Evidence generation with some structure
 X = np.random.randn(n_samples, n_features)

# the target variable with non-linear relationships
 y = np.zeros(n_samples)
 for i in range(n_samples):
# Complex non-liner dependency
 score = (X[i, 0] ** 2 + X[i, 1] * X[i, 2] +
 np.sin(X[i, 3]) + X[i, 4] * X[i, 5])

 if score > 2.0:
y[i] = 2 # Class 2
 elif score > 0.5:
y[i] = 1 # Class 1
 else:
y[i] = 0 #Class 0

===Example use of LightGBM ===)

# Model learning
 model, metrics, importance_df = train_lightgbm(X, y)

# Visualizing the importance of signs
 plot_lightgbm_importance(importance_df)

# Visualization of the learning curve
 plot_lightgbm_learning_curve(model)

 return model, metrics

# Launch examples (upstream for testing)
# model, metrics = example_lightgbm_usage()
```

♪ Neuronets

**Theory:** Neuronets are a powerful tool for modelling complex non-linear dependencies in financial data, particularly effective for identifying hidden patterns and interactions between signature data.

**Why neural networks are effective for finance:**
- **Nelinearity:** Can model complex non-liner dependencies
- **Explosion:** Automatically identify the interaction between the subsigns
- ** Adaptation: ** May adapt to changing market conditions
- **Scalability:** Good Working with large volumes of data

###1, simple neural net

**Theory:** The Full-Leyer Perceptron network consists of several layers of neurons connected by the balance. Each neuron applies a non-linear activation function to the weighted input sum.

**architecture network:**
**Intake layer:** Number of neurons = number of topics
- ** Hidden layers:** 2-3 layers with 64-256 neurons each
** Output layer:** Number of neurons = number of classes
- **Dropout:**Regularization for prevention of retraining
- **Action:** ReLU for hidden layers, Softmax for the weekend

** Practical implementation:**

What does this code do?
1. **create architecture:** Determines the structure of the neural network
2. ** Training:** Uses backup for balance optimization
3. **Regularization: ** Applies the draft for prevention of retraining
4. **validation:** Monitor performance in learning

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import dataLoader, Tensordataset
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_Report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

class TradingNN(nn.Module):
 """
Neural network for trade preferences

 architecture:
- Input layer: input_size neurons
- 3 hidden layers: each hidden_size neurons
- Output layer: num_classes of neurons
- Dropout: 0.2 for regularization
- Activation: ReLU for hidden layers
 """

 def __init__(self, input_size, hidden_size=128, num_classes=3, dropout_rate=0.2):
 super(TradingNN, self).__init__()

# Definition of layers
 self.fc1 = nn.Linear(input_size, hidden_size)
 self.fc2 = nn.Linear(hidden_size, hidden_size)
 self.fc3 = nn.Linear(hidden_size, hidden_size)
 self.fc4 = nn.Linear(hidden_size, num_classes)

# Regularization
 self.dropout = nn.Dropout(dropout_rate)

# Function activation
 self.relu = nn.ReLU()

# Initiating weights
 self._initialize_weights()

 def _initialize_weights(self):
"Initiating weights for better convergence."
 for m in self.modules():
 if isinstance(m, nn.Linear):
 nn.init.xavier_uniform_(m.weight)
 nn.init.constant_(m.bias, 0)

 def forward(self, x):
""""""""""""""""
# First hidden layer
 x = self.relu(self.fc1(x))
 x = self.dropout(x)

# Second hidden layer
 x = self.relu(self.fc2(x))
 x = self.dropout(x)

# Third hidden layer
 x = self.relu(self.fc3(x))
 x = self.dropout(x)

# The output layer (without activation - to be applied in loss function)
 x = self.fc4(x)

 return x

def train_neural_network(X, y, epochs=100, batch_size=32, learning_rate=0.001,
 test_size=0.2, random_state=42):
 """
Training of the neural network for trade preferences

 Args:
X (array-lake): Signs matrix
y (array-lake): Target variables
epochs (int): Number of learning ages
Batch_size (int): Batch size
Learning_rate (float): Learning speed
test_size (float): Percentage of test data
Random_state (int): Seed for reproducibility

 Returns:
Tuple: (Learned model, metrics, history of learning)
 """

"print("===Nerural network training===)
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
(pint(f"Classes: {np.unique(y, return_counts=True)})

# Data sharing
 X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=test_size, random_state=random_state, stratify=y
 )

Print(f "Learning sample: {X_training.chape[0]} samples")
print(f"tests sample: {X_test.chape[0]} samples)

# Conversion into PyTorch Tensor
 X_train_tensor = torch.FloatTensor(X_train)
 y_train_tensor = torch.LongTensor(y_train)
 X_test_tensor = torch.FloatTensor(X_test)
 y_test_tensor = torch.LongTensor(y_test)

# Create Dataset and DataLoader
 train_dataset = Tensordataset(X_train_tensor, y_train_tensor)
 train_dataloader = dataLoader(train_dataset, batch_size=batch_size, shuffle=True)

♪ Create Model
 model = TradingNN(X.shape[1], num_classes=len(np.unique(y)))

# Function loss and optimization
 criterion = nn.CrossEntropyLoss()
 optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# History of learning
 train_losses = []
 train_accuracies = []
 test_accuracies = []

prent(f"\nParameters of instruction:")
 print(f"Epochs: {epochs}")
 print(f"Batch size: {batch_size}")
 print(f"Learning rate: {learning_rate}")
 print(f"Model parameters: {sum(p.numel() for p in model.parameters())}")

# Training
Print('n Started training...')
 model.train()

 for epoch in range(epochs):
 epoch_loss = 0.0
 correct = 0
 total = 0

 for batch_X, batch_y in train_dataloader:
# The de-grading
 optimizer.zero_grad()

# Straight through
 outputs = model(batch_X)
 loss = criterion(outputs, batch_y)

# The way back
 loss.backward()
 optimizer.step()

# Statistics
 epoch_loss += loss.item()
 _, predicted = torch.max(outputs.data, 1)
 total += batch_y.size(0)
 correct += (predicted == batch_y).sum().item()

# Calculation of metrics
 avg_loss = epoch_loss / len(train_dataloader)
 train_accuracy = correct / total

 train_losses.append(avg_loss)
 train_accuracies.append(train_accuracy)

# Evaluation on test data
 model.eval()
 with torch.no_grad():
 test_outputs = model(X_test_tensor)
 _, test_predicted = torch.max(test_outputs.data, 1)
 test_accuracy = accuracy_score(y_test, test_predicted.numpy())
 test_accuracies.append(test_accuracy)
 model.train()

# Conclusion of progress
 if epoch % 10 == 0 or epoch == epochs - 1:
 print(f'Epoch {epoch:3d}/{epochs}: '
 f'Loss: {avg_loss:.4f}, '
 f'Train Acc: {train_accuracy:.4f}, '
 f'Test Acc: {test_accuracy:.4f}')

# Final evaluation
 model.eval()
 with torch.no_grad():
 test_outputs = model(X_test_tensor)
 _, test_predicted = torch.max(test_outputs.data, 1)
 test_predictions = test_predicted.numpy()
 test_probabilities = torch.softmax(test_outputs, dim=1).numpy()

 # metrics
 final_accuracy = accuracy_score(y_test, test_predictions)

== Final results====================================)=======Prent(f)========= Final results======)
 print(f"Test accuracy: {final_accuracy:.4f}")

# Detailed Report
 print(f"\n=== Classification Report ===")
 print(classification_Report(y_test, test_predictions))

# History of learning
 history = {
 'train_losses': train_losses,
 'train_accuracies': train_accuracies,
 'test_accuracies': test_accuracies
 }

# metrics for return
 metrics = {
 'test_accuracy': final_accuracy,
 'confusion_matrix': confusion_matrix(y_test, test_predictions),
 'predictions': test_predictions,
 'probabilities': test_probabilities,
 'history': history
 }

 return model, metrics, history

def plot_training_history(history):
"Visualization of the history of learning."

 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Loss schedule
 ax1.plot(history['train_losses'], label='Train Loss')
 ax1.set_title('Training Loss')
 ax1.set_xlabel('Epoch')
 ax1.set_ylabel('Loss')
 ax1.legend()
 ax1.grid(True)

# Accuracy schedule
 ax2.plot(history['train_accuracies'], label='Train Accuracy')
 ax2.plot(history['test_accuracies'], label='Test Accuracy')
 ax2.set_title('Training and Test Accuracy')
 ax2.set_xlabel('Epoch')
 ax2.set_ylabel('Accuracy')
 ax2.legend()
 ax2.grid(True)

 plt.tight_layout()
 plt.show()

# Example of use:
def example_neural_network_usage():
"example of Neuronet Use""

# creative synthetic data
 np.random.seed(42)
 n_samples, n_features = 1000, 20

# Signal generation
 X = np.random.randn(n_samples, n_features)

# the target variable with non-linear relationships
 y = np.zeros(n_samples)
 for i in range(n_samples):
# Complex non-liner dependency
 score = (X[i, 0] ** 2 + X[i, 1] * X[i, 2] +
 np.sin(X[i, 3]) + X[i, 4] * X[i, 5])

 if score > 2.0:
y[i] = 2 # Class 2
 elif score > 0.5:
y[i] = 1 # Class 1
 else:
y[i] = 0 #Class 0

"print("== example use of the neural network===)

# Model learning
 model, metrics, history = train_neural_network(X, y, epochs=50)

# Visualization of the history of learning
 plot_training_history(history)

 return model, metrics

# Launch examples (upstream for testing)
# model, metrics = example_neural_network_usage()
```

###2. LSTM for time series

**Theory:** LSTM (Long Short-Term Memory) is a special type of respiratory neural network that is not Working for work with time sequences. LSTM is particularly effective for financial data because it can remember long-term dependencies and pathites.

** Detailed LSTM theory:**

** Working principle:**
1. **Forget Gate: ** Decides what information to forget from previous status
2. **Input Gate:** Decides which new information to save
3. ** Update Gate:** Updates cell state
4. ** Output Gate: ** Decides what information to output

**Why LSTM is effective for finance:**
- ** Temporary dependencies:** May memorize long time intervals
- ** Resistance to gradient disappearance:** Addresses RNN problem
- ** Cycling:** Perfectly suited for time series
- ** Context information:** Taking into account history for decision-making

** Mathematical framework:**
- **Forget Gate:** f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
- **Input Gate:** i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
- **Cell State:** C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C)
- **Update:** C_t = f_t * C_{t-1} + i_t * C̃_t
- **Output Gate:** o_t = σ(W_o · [h_{t-1}, x_t] + b_o)
- **Hidden State:** h_t = o_t * tanh(C_t)

** Practical implementation of LSTM:**

What does this code do?
1. **create sequences:** converts data into time series format
2. **architecture LSTM:**
3. **Learning: ** Uses Backup through time (BPTT)
4. **validation:** Assesses performance on time data

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import dataLoader, Tensordataset
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_Report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

class LSTMTradingModel(nn.Module):
 """
LSTM model for trade preferences on time series

 architecture:
- LSTM layers: for processing time sequences
- Dropout: for regularization
- Full layer: for final classification
 """

 def __init__(self, input_size, hidden_size=64, num_layers=2, num_classes=3, dropout_rate=0.2):
 super(LSTMTradingModel, self).__init__()

 self.hidden_size = hidden_size
 self.num_layers = num_layers

# LSTM layers
 self.lstm = nn.LSTM(
 input_size=input_size,
 hidden_size=hidden_size,
 num_layers=num_layers,
 batch_first=True,
 dropout=dropout_rate if num_layers > 1 else 0,
 bidirectional=False
 )

# A complete layer for classification
 self.fc = nn.Linear(hidden_size, num_classes)

# Dropout for regularization
 self.dropout = nn.Dropout(dropout_rate)

# Initiating weights
 self._initialize_weights()

 def _initialize_weights(self):
"Initiation of LSTM Weights"
 for name, param in self.named_parameters():
 if 'weight_ih' in name:
 nn.init.xavier_uniform_(param.data)
 elif 'weight_hh' in name:
 nn.init.orthogonal_(param.data)
 elif 'bias' in name:
 param.data.fill_(0)
# installation for better initialization
 n = param.size(0)
 param.data[(n//4):(n//2)].fill_(1)

 def forward(self, x):
 """
Direct Passage through LSTM

 Args:
x: Incoming data forms (batch_size, sequence_length, input_size)

 Returns:
Output data forms (batch_size, num_classes)
 """
 batch_size = x.size(0)

# Initiating a Hidden State
 h0 = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=x.device)
 c0 = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=x.device)

 # LSTM forward pass
 lstm_out, (hn, cn) = self.lstm(x, (h0, c0))

# Take the last exit from the sequence
 last_output = lstm_out[:, -1, :] # (batch_size, hidden_size)

# Applying dropout
 last_output = self.dropout(last_output)

# Final classification
 output = self.fc(last_output)

 return output

def create_sequences(X, y, sequence_length):
 """
set sequences for LSTM

 Args:
X: Signal matrix (samples, features)
y: Target variables (samples,)
Sequence_langth: Sequence length

 Returns:
X_seq: Signs sequences (samples-seq_len+1, seq_len, Features)
y_seq: Target variables for sequences (samples-seq_len+1,)
 """
 X_seq, y_seq = [], []

 for i in range(sequence_length, len(X)):
 X_seq.append(X[i-sequence_length:i])
 y_seq.append(y[i])

 return np.array(X_seq), np.array(y_seq)

def train_lstm_model(X, y, sequence_length=10, epochs=100, batch_size=32,
 learning_rate=0.001, test_size=0.2, random_state=42):
 """
LSTM training model for trade preferences

 Args:
X: Indicator matrix
y: Target variables
Sequence_langth: Length of time sequence
epochs: Number of learning ages
Batch_size: The dimensions of the batch
Learning_rate: Learning speed
test_size: Percentage of test data
Random_state: Seed for reproducibility

 Returns:
Tuple: (Learned model, metrics, history of learning)
 """

"print("===LSTM model training===)
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
(pint(f"Classes: {np.unique(y, return_counts=True)})
Print(f "Long sequence: {sequence_length}")

# Create sequences
 X_seq, y_seq = create_sequences(X, y, sequence_length)
Print(f "Symmetry measurement: {X_seq.chape}")

# Data sharing
 X_train, X_test, y_train, y_test = train_test_split(
 X_seq, y_seq, test_size=test_size, random_state=random_state, stratify=y_seq
 )

Print(f "Learning sample: {X_training.scape[0]} sequences")
print(f"tests sample: {X_test.chape[0]} sequences")

# Conversion into PyTorch Tensor
 X_train_tensor = torch.FloatTensor(X_train)
 y_train_tensor = torch.LongTensor(y_train)
 X_test_tensor = torch.FloatTensor(X_test)
 y_test_tensor = torch.LongTensor(y_test)

# Create Dataset and DataLoader
 train_dataset = Tensordataset(X_train_tensor, y_train_tensor)
 train_dataloader = dataLoader(train_dataset, batch_size=batch_size, shuffle=True)

♪ Create Model
 model = LSTMTradingModel(
 input_size=X.shape[1],
 num_classes=len(np.unique(y)),
 hidden_size=64,
 num_layers=2
 )

# Function loss and optimization
 criterion = nn.CrossEntropyLoss()
 optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# History of learning
 train_losses = []
 train_accuracies = []
 test_accuracies = []

prent(f"\nParameters of instruction:")
 print(f"Epochs: {epochs}")
 print(f"Batch size: {batch_size}")
 print(f"Learning rate: {learning_rate}")
 print(f"Sequence length: {sequence_length}")
 print(f"Model parameters: {sum(p.numel() for p in model.parameters())}")

# Training
Print('n Started training...')
 model.train()

 for epoch in range(epochs):
 epoch_loss = 0.0
 correct = 0
 total = 0

 for batch_X, batch_y in train_dataloader:
# The de-grading
 optimizer.zero_grad()

# Straight through
 outputs = model(batch_X)
 loss = criterion(outputs, batch_y)

# The way back
 loss.backward()

# Grading gradients for stability
 torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

 optimizer.step()

# Statistics
 epoch_loss += loss.item()
 _, predicted = torch.max(outputs.data, 1)
 total += batch_y.size(0)
 correct += (predicted == batch_y).sum().item()

# Calculation of metrics
 avg_loss = epoch_loss / len(train_dataloader)
 train_accuracy = correct / total

 train_losses.append(avg_loss)
 train_accuracies.append(train_accuracy)

# Evaluation on test data
 model.eval()
 with torch.no_grad():
 test_outputs = model(X_test_tensor)
 _, test_predicted = torch.max(test_outputs.data, 1)
 test_accuracy = accuracy_score(y_test, test_predicted.numpy())
 test_accuracies.append(test_accuracy)
 model.train()

# Conclusion of progress
 if epoch % 10 == 0 or epoch == epochs - 1:
 print(f'Epoch {epoch:3d}/{epochs}: '
 f'Loss: {avg_loss:.4f}, '
 f'Train Acc: {train_accuracy:.4f}, '
 f'Test Acc: {test_accuracy:.4f}')

# Final evaluation
 model.eval()
 with torch.no_grad():
 test_outputs = model(X_test_tensor)
 _, test_predicted = torch.max(test_outputs.data, 1)
 test_predictions = test_predicted.numpy()
 test_probabilities = torch.softmax(test_outputs, dim=1).numpy()

 # metrics
 final_accuracy = accuracy_score(y_test, test_predictions)

== Final results====================================)=======Prent(f)========= Final results======)
 print(f"Test accuracy: {final_accuracy:.4f}")

# Detailed Report
 print(f"\n=== Classification Report ===")
 print(classification_Report(y_test, test_predictions))

# History of learning
 history = {
 'train_losses': train_losses,
 'train_accuracies': train_accuracies,
 'test_accuracies': test_accuracies
 }

# metrics for return
 metrics = {
 'test_accuracy': final_accuracy,
 'confusion_matrix': confusion_matrix(y_test, test_predictions),
 'predictions': test_predictions,
 'probabilities': test_probabilities,
 'history': history
 }

 return model, metrics, history

def plot_lstm_training_history(history):
"Visualization of LSTM Learning History."

 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Loss schedule
 ax1.plot(history['train_losses'], label='Train Loss')
 ax1.set_title('LSTM Training Loss')
 ax1.set_xlabel('Epoch')
 ax1.set_ylabel('Loss')
 ax1.legend()
 ax1.grid(True)

# Accuracy schedule
 ax2.plot(history['train_accuracies'], label='Train Accuracy')
 ax2.plot(history['test_accuracies'], label='Test Accuracy')
 ax2.set_title('LSTM Training and Test Accuracy')
 ax2.set_xlabel('Epoch')
 ax2.set_ylabel('Accuracy')
 ax2.legend()
 ax2.grid(True)

 plt.tight_layout()
 plt.show()

# Example of use:
def example_lstm_usage():
""example using LSTM""

# of synthetic time data
 np.random.seed(42)
 n_samples, n_features = 1000, 10
 sequence_length = 10

# Identity generation with temporary structure
 X = np.random.randn(n_samples, n_features)

# a target variable with time dependency
 y = np.zeros(n_samples)
 for i in range(n_samples):
# Temporary dependency: current value depends from previous
 if i < sequence_length:
y[i] = 0 # Initial values
 else:
# Complex temporary dependency
 recent_sum = np.sum(X[i-sequence_length:i, 0])
 recent_volatility = np.std(X[i-sequence_length:i, 1])

 if recent_sum > 2.0 and recent_volatility < 1.0:
y[i] = 2 # Class 2
 elif recent_sum > 0.5 or recent_volatility > 1.5:
y[i] = 1 # Class 1
 else:
y[i] = 0 #Class 0

===Example use of LSTM ===)

# Model learning
 model, metrics, history = train_lstm_model(
 X, y,
 sequence_length=sequence_length,
 epochs=50
 )

# Visualization of the history of learning
 plot_lstm_training_history(history)

 return model, metrics

# Launch examples (upstream for testing)
# model, metrics = example_lstm_usage()
```

## Validation of models

**Theory:** the validation of models for financial data is critical, as standard methhods cross-validation can lead to data release (data drain) due to the temporary nature of financial data.

**Why the standard cross-validation note fits:**
- **data Leakage:** Future data can flow in a learning sample
- ** Temporary dependency:** Financial data has a temporary structure
- ** Non-permanentity:** Distributions change over time
- ** Reality: ** Need to simulate real trade conditions

### 1. Time Series Cross Validation

**Theory:** Time Series Cross Planning (TSV) is a special method of validation for time series that prevents data release using only past data for predicting futures.

** Operating principle TSCV:**
1. **Temporary separation:** data divided in time and not accidental
2. **Stop sequence:** Each sample shall include previous samples.
3. ** Reality:** Simulates real terms of trade
4. ** Prevention of trafficking:** Future data are never used for learning

** Practical implementation of TSCV:**

What does this code do?
1. **Temporary separation:** Creates temporary folds without intersections
2. ** History training: ** Each model is taught only on past data
3. ** Testimony on the future:** Projections on future data
4. **metrics:** Computes different metrics for each fold

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
 f1_score, confusion_matrix, classification_Report)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Tuple

def time_series_cv(model, X, y, n_splits=5, test_size=None, random_state=42):
 """
Cross-evaluation for time series

 Args:
Model: Model for validation (should have meths fat and predict)
X: Signal matrix (samples, features)
y: Target variables (samples,)
n_splits: Number of folds
test_size: Tests fold size (if None is automatically calculated)
Random_state: Seed for reproducibility

 Returns:
dict: Results of validation with metrics for each fold
 """

 print("=== Time Series Cross Validation ===")
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
Print(f "Number of Folds: {n_splits}")
(pint(f"Classes: {np.unique(y, return_counts=True)})

 # create TimeSeriesSplit
 tscv = TimeSeriesSplit(n_splits=n_splits, test_size=test_size)

# Lists for storing results
 fold_scores = []
 fold_predictions = []
 fold_confusion_matrices = []

prent(f)(n Starts validation...)

 for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
 print(f"\n--- Fold {fold + 1}/{n_splits} ---")

# Data sharing
 X_train, X_test = X[train_idx], X[test_idx]
 y_train, y_test = y[train_idx], y[test_idx]

 print(f"Train size: {len(train_idx)} ({len(train_idx)/len(X)*100:.1f}%)")
 print(f"Test size: {len(test_idx)} ({len(test_idx)/len(X)*100:.1f}%)")
 print(f"Train period: {train_idx[0]} - {train_idx[-1]}")
 print(f"Test period: {test_idx[0]} - {test_idx[-1]}")

# Create copies of the model for each fold
 fold_model = type(model)(**model.get_params())

# Model learning
Print("model training...")
 fold_model.fit(X_train, y_train)

# Premonition
 y_pred = fold_model.predict(X_test)
 y_pred_proba = fold_model.predict_proba(X_test) if hasattr(fold_model, 'predict_proba') else None

# Calculation of metrics
 accuracy = accuracy_score(y_test, y_pred)
 precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
 recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
 f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

# A matrix of errors
 cm = confusion_matrix(y_test, y_pred)

# Retaining results
 fold_score = {
 'fold': fold + 1,
 'accuracy': accuracy,
 'precision': precision,
 'recall': recall,
 'f1': f1,
 'train_size': len(train_idx),
 'test_size': len(test_idx)
 }

 fold_scores.append(fold_score)
 fold_predictions.append({
 'y_true': y_test,
 'y_pred': y_pred,
 'y_pred_proba': y_pred_proba
 })
 fold_confusion_matrices.append(cm)

 print(f"Accuracy: {accuracy:.4f}")
 print(f"Precision: {precision:.4f}")
 print(f"Recall: {recall:.4f}")
 print(f"F1: {f1:.4f}")

# The aggregate results
 results = {
 'fold_scores': fold_scores,
 'fold_predictions': fold_predictions,
 'fold_confusion_matrices': fold_confusion_matrices,
 'mean_accuracy': np.mean([s['accuracy'] for s in fold_scores]),
 'std_accuracy': np.std([s['accuracy'] for s in fold_scores]),
 'mean_precision': np.mean([s['precision'] for s in fold_scores]),
 'mean_recall': np.mean([s['recall'] for s in fold_scores]),
 'mean_f1': np.mean([s['f1'] for s in fold_scores])
 }

# Conclusion of outcome
===TSCV results==========================TSCV=======)=====TSCV results
 print(f"Mean Accuracy: {results['mean_accuracy']:.4f} ± {results['std_accuracy']:.4f}")
 print(f"Mean Precision: {results['mean_precision']:.4f}")
 print(f"Mean Recall: {results['mean_recall']:.4f}")
 print(f"Mean F1: {results['mean_f1']:.4f}")

 return results

def plot_tscv_results(results, figsize=(15, 10)):
"Visualization of the results of the Time Series Cross Validation"

 fig, axes = plt.subplots(2, 2, figsize=figsize)

# Data extraction
 fold_scores = results['fold_scores']
 folds = [s['fold'] for s in fold_scores]
 accuracies = [s['accuracy'] for s in fold_scores]
 precisions = [s['precision'] for s in fold_scores]
 recalls = [s['recall'] for s in fold_scores]
 f1_scores = [s['f1'] for s in fold_scores]

# The chart of accuracy on the folks
 axes[0, 0].plot(folds, accuracies, 'o-', label='Accuracy')
 axes[0, 0].axhline(y=results['mean_accuracy'], color='r', linestyle='--',
 label=f'Mean: {results["mean_accuracy"]:.3f}')
 axes[0, 0].set_title('Accuracy by Fold')
 axes[0, 0].set_xlabel('Fold')
 axes[0, 0].set_ylabel('Accuracy')
 axes[0, 0].legend()
 axes[0, 0].grid(True)

# The chart on the folds
 axes[0, 1].plot(folds, accuracies, 'o-', label='Accuracy')
 axes[0, 1].plot(folds, precisions, 's-', label='Precision')
 axes[0, 1].plot(folds, recalls, '^-', label='Recall')
 axes[0, 1].plot(folds, f1_scores, 'd-', label='F1')
 axes[0, 1].set_title('Metrics by Fold')
 axes[0, 1].set_xlabel('Fold')
 axes[0, 1].set_ylabel('Score')
 axes[0, 1].legend()
 axes[0, 1].grid(True)

# Box flat metric
 metrics_data = [accuracies, precisions, recalls, f1_scores]
 metrics_labels = ['Accuracy', 'Precision', 'Recall', 'F1']
 axes[1, 0].boxplot(metrics_data, labels=metrics_labels)
 axes[1, 0].set_title('Distribution of Metrics')
 axes[1, 0].set_ylabel('Score')
 axes[1, 0].grid(True)

# Aggregated error matrix
 if results['fold_confusion_matrices']:
# Summarize all error matrices
 total_cm = np.sum(results['fold_confusion_matrices'], axis=0)

# Normalize for interest
 total_cm_norm = total_cm.astype('float') / total_cm.sum(axis=1)[:, np.newaxis]

 sns.heatmap(total_cm_norm, annot=True, fmt='.2f', cmap='Blues', ax=axes[1, 1])
 axes[1, 1].set_title('Aggregated Confusion Matrix')
 axes[1, 1].set_xlabel('Predicted')
 axes[1, 1].set_ylabel('True')

 plt.tight_layout()
 plt.show()

def analyze_tscv_stability(results):
"The Analysis of Stability of TSCV Results"

 fold_scores = results['fold_scores']
 accuracies = [s['accuracy'] for s in fold_scores]

"print("===TSCV stability analysis===)
 print(f"Accuracy - Min: {min(accuracies):.4f}, Max: {max(accuracies):.4f}")
 print(f"Accuracy - Range: {max(accuracies) - min(accuracies):.4f}")
 print(f"Accuracy - Std: {np.std(accuracies):.4f}")
 print(f"Accuracy - CV: {np.std(accuracies) / np.mean(accuracies):.4f}")

# Trends analysis
 if len(accuracies) >= 3:
# Checking, is there a trend (improve/degradation over time)
 from scipy import stats
 slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(accuracies)), accuracies)

Print(f"\nTrend accuracy:")
(positive = improve))
 print(f"R-squared: {r_value**2:.4f}")
 print(f"P-value: {p_value:.4f}")

 if p_value < 0.05:
 if slope > 0:
"Statistically significant improve over time"
 else:
"Statistically significant deterioration over time"
 else:
"No statistically significant trend"

# Example of use:
def example_tscv_usage():
""Example Use Time Series Cross Planning""

 from sklearn.ensemble import RandomForestClassifier

# of synthetic time data
 np.random.seed(42)
 n_samples, n_features = 1000, 20

# Identity generation with temporary structure
 X = np.random.randn(n_samples, n_features)

# a target variable with time dependency
 y = np.zeros(n_samples)
 for i in range(n_samples):
# Temporary dependency
 if i < 100:
 y[i] = 0
 elif i < 500:
 y[i] = 1 if X[i, 0] > 0 else 0
 else:
 y[i] = 2 if X[i, 0] > 0.5 else (1 if X[i, 0] > -0.5 else 0)

 print("=== example Time Series Cross Validation ===")

♪ Create Model
 model = RandomForestClassifier(n_estimators=50, random_state=42)

# Implementation of TSCV
 results = time_series_cv(model, X, y, n_splits=5)

# Visualization of results
 plot_tscv_results(results)

# Analysis of stability
 analyze_tscv_stability(results)

 return results

# Launch examples (upstream for testing)
# results = example_tscv_usage()
```

### 2. Walk-Forward Validation

**Theory:** Walk-Forward Planning (WFV) is a method of validation that simulates the real trade environment, where the model is constantly re-trained on new data and makes predictions on the next period.

** Operating principle WFV:**
1. **Slipping window:** Learning sample has a fixed size
2. ** Step forward:** Window moves on a fixed step
3. ** Reality:** Simulates the real trade environment
4. ** Adaptation: ** Model adapts to new data

**Why WFV is effective for finance:**
- ** Reality:** Precisely simulates the real trade environment.
- ** Adaptation: ** Model continuously updated
- **Stability:** Shows how the Workinget model in the long term
- ** Data Drift:** Helps to detect when a model becomes obsolete

** Practical implementation of WFV:**

What does this code do?
1. **Slipping window:** Creates fixed size instructional samples
2. ** Step-by-step testing:** Test the model on the following data
3. **retraining:** The model is re-trained on each step
4. **metrics:** Traces activity over time

```python
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
 f1_score, confusion_matrix)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Tuple

def walk_forward_validation(model, X, y, train_size=1000, step_size=100,
 min_test_size=50, random_state=42):
 """
Walk-Forward validation for time series

 Args:
Model: Model for validation (should have meths fat and predict)
X: Signal matrix (samples, features)
y: Target variables (samples,)
Train_size: The size of the learning window
step_size: Size of step for moving the window
min_test_size: Minimum tests sample size
Random_state: Seed for reproducibility

 Returns:
dict: Walk-forward performance results
 """

 print("=== Walk-Forward Validation ===")
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
Print(f) Training window measurement: {training_size})
pprint(f) Step measurement: {step_size})
(pint(f"Classes: {np.unique(y, return_counts=True)})

# Calculation of the number of iterations
 n_iterations = (len(X) - train_size) // step_size
(f "Number of iterations: {n_items}")

# Lists for storing results
 iteration_results = []
 all_predictions = []
 all_true_labels = []

(f) Started walk-forward validation...)

 for i in range(n_iterations):
 start_idx = i * step_size
 train_end_idx = start_idx + train_size
 test_start_idx = train_end_idx
 test_end_idx = min(test_start_idx + step_size, len(X))

# check minimum tests sample size
 if test_end_idx - test_start_idx < min_test_size:
Print(f "Iteration {i+1}: Insufficient data for testing, missing")
 continue

Print(f)(\n--- Iteration {i+1}/{n_items}--)
Print(f"Learning period: {start_idx} - {training_end_idx-1})
pprint(f"tests period: {test_start_idx} - {test_end_idx-1})

# Data sharing
 X_train = X[start_idx:train_end_idx]
 y_train = y[start_idx:train_end_idx]
 X_test = X[test_start_idx:test_end_idx]
 y_test = y[test_start_idx:test_end_idx]

 print(f"Train size: {len(X_train)}")
 print(f"Test size: {len(X_test)}")

# creative copies of the model for each iteration
 fold_model = type(model)(**model.get_params())

# Model learning
Print("model training...")
 fold_model.fit(X_train, y_train)

# Premonition
 y_pred = fold_model.predict(X_test)
 y_pred_proba = fold_model.predict_proba(X_test) if hasattr(fold_model, 'predict_proba') else None

# Calculation of metrics
 accuracy = accuracy_score(y_test, y_pred)
 precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
 recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
 f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

# A matrix of errors
 cm = confusion_matrix(y_test, y_pred)

# Retaining results
 iteration_result = {
 'iteration': i + 1,
 'train_start': start_idx,
 'train_end': train_end_idx - 1,
 'test_start': test_start_idx,
 'test_end': test_end_idx - 1,
 'accuracy': accuracy,
 'precision': precision,
 'recall': recall,
 'f1': f1,
 'train_size': len(X_train),
 'test_size': len(X_test),
 'confusion_matrix': cm
 }

 iteration_results.append(iteration_result)
 all_predictions.extend(y_pred)
 all_true_labels.extend(y_test)

 print(f"Accuracy: {accuracy:.4f}")
 print(f"Precision: {precision:.4f}")
 print(f"Recall: {recall:.4f}")
 print(f"F1: {f1:.4f}")

# The aggregate results
 if iteration_results:
 accuracies = [r['accuracy'] for r in iteration_results]
 precisions = [r['precision'] for r in iteration_results]
 recalls = [r['recall'] for r in iteration_results]
 f1_scores = [r['f1'] for r in iteration_results]

 results = {
 'iteration_results': iteration_results,
 'all_predictions': np.array(all_predictions),
 'all_true_labels': np.array(all_true_labels),
 'mean_accuracy': np.mean(accuracies),
 'std_accuracy': np.std(accuracies),
 'mean_precision': np.mean(precisions),
 'mean_recall': np.mean(recalls),
 'mean_f1': np.mean(f1_scores),
 'n_iterations': len(iteration_results)
 }

# Conclusion of outcome
"print(f"\n===Walk-Forward totals================================Walk-Forward====)
(f "Number of iterations: {results['n_iterations']}")
 print(f"Mean Accuracy: {results['mean_accuracy']:.4f} ± {results['std_accuracy']:.4f}")
 print(f"Mean Precision: {results['mean_precision']:.4f}")
 print(f"Mean Recall: {results['mean_recall']:.4f}")
 print(f"Mean F1: {results['mean_f1']:.4f}")

# Total accuracy on all predictions
 overall_accuracy = accuracy_score(all_true_labels, all_predictions)
 print(f"Overall Accuracy: {overall_accuracy:.4f}")

 else:
"No results for Analysis"
 results = None

 return results

def plot_walk_forward_results(results, figsize=(15, 12)):
"Visualization of Walk-Forward results."

 if results is None:
"No data for visualization"
 return

 fig, axes = plt.subplots(2, 2, figsize=figsize)

# Data extraction
 iteration_results = results['iteration_results']
 iterations = [r['iteration'] for r in iteration_results]
 accuracies = [r['accuracy'] for r in iteration_results]
 precisions = [r['precision'] for r in iteration_results]
 recalls = [r['recall'] for r in iteration_results]
 f1_scores = [r['f1'] for r in iteration_results]

# A graph of accuracy on iterations
 axes[0, 0].plot(iterations, accuracies, 'o-', label='Accuracy')
 axes[0, 0].axhline(y=results['mean_accuracy'], color='r', linestyle='--',
 label=f'Mean: {results["mean_accuracy"]:.3f}')
 axes[0, 0].set_title('Accuracy by Iteration')
 axes[0, 0].set_xlabel('Iteration')
 axes[0, 0].set_ylabel('Accuracy')
 axes[0, 0].legend()
 axes[0, 0].grid(True)

# Chart all metrics on iterations
 axes[0, 1].plot(iterations, accuracies, 'o-', label='Accuracy')
 axes[0, 1].plot(iterations, precisions, 's-', label='Precision')
 axes[0, 1].plot(iterations, recalls, '^-', label='Recall')
 axes[0, 1].plot(iterations, f1_scores, 'd-', label='F1')
 axes[0, 1].set_title('Metrics by Iteration')
 axes[0, 1].set_xlabel('Iteration')
 axes[0, 1].set_ylabel('Score')
 axes[0, 1].legend()
 axes[0, 1].grid(True)

# Slipping average accuracy
Windows_size = max(1, Len(accuracies) //5) # 20% from total iterations
 if window_size > 1:
 rolling_accuracy = pd.Series(accuracies).rolling(window=window_size).mean()
 axes[1, 0].plot(iterations, accuracies, 'o-', alpha=0.3, label='Raw Accuracy')
 axes[1, 0].plot(iterations, rolling_accuracy, 'r-', linewidth=2,
 label=f'Rolling Mean (window={window_size})')
 axes[1, 0].set_title('Accuracy with Rolling Mean')
 axes[1, 0].set_xlabel('Iteration')
 axes[1, 0].set_ylabel('Accuracy')
 axes[1, 0].legend()
 axes[1, 0].grid(True)
 else:
 axes[1, 0].plot(iterations, accuracies, 'o-')
 axes[1, 0].set_title('Accuracy by Iteration')
 axes[1, 0].set_xlabel('Iteration')
 axes[1, 0].set_ylabel('Accuracy')
 axes[1, 0].grid(True)

# Common error matrix
 if len(results['all_true_labels']) > 0:
 overall_cm = confusion_matrix(results['all_true_labels'], results['all_predictions'])
 overall_cm_norm = overall_cm.astype('float') / overall_cm.sum(axis=1)[:, np.newaxis]

 sns.heatmap(overall_cm_norm, annot=True, fmt='.2f', cmap='Blues', ax=axes[1, 1])
 axes[1, 1].set_title('Overall Confusion Matrix')
 axes[1, 1].set_xlabel('Predicted')
 axes[1, 1].set_ylabel('True')

 plt.tight_layout()
 plt.show()

def analyze_walk_forward_stability(results):
"Analysis of the stability of the results of the Walk-Forward validation"

 if results is None:
"No data for Analysis"
 return

 iteration_results = results['iteration_results']
 accuracies = [r['accuracy'] for r in iteration_results]

"print("===Walk-Forward stability analysis===)
 print(f"Accuracy - Min: {min(accuracies):.4f}, Max: {max(accuracies):.4f}")
 print(f"Accuracy - Range: {max(accuracies) - min(accuracies):.4f}")
 print(f"Accuracy - Std: {np.std(accuracies):.4f}")
 print(f"Accuracy - CV: {np.std(accuracies) / np.mean(accuracies):.4f}")

# Trends analysis
 if len(accuracies) >= 3:
 from scipy import stats
 slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(accuracies)), accuracies)

Print(f"\nTrend accuracy:")
(positive = improve))
 print(f"R-squared: {r_value**2:.4f}")
 print(f"P-value: {p_value:.4f}")

 if p_value < 0.05:
 if slope > 0:
"Statistically significant improve over time"
 else:
"Statistically significant deterioration over time"
 else:
"No statistically significant trend"

# Stability analysis (slip window)
 if len(accuracies) >= 10:
 window_size = max(3, len(accuracies) // 5)
 rolling_std = pd.Series(accuracies).rolling(window=window_size).std()

Print(f) /nStability (slipping standard deviation, window={window_size}):)
 print(f"Mean Rolling Std: {rolling_std.mean():.4f}")
 print(f"Max Rolling Std: {rolling_std.max():.4f}")

# Check on degradation performance
 recent_acc = np.mean(accuracies[-window_size:])
 early_acc = np.mean(accuracies[:window_size])
 degradation = early_acc - recent_acc

Print(f"n Degradation performance:")
 print(f"Early accuracy: {early_acc:.4f}")
 print(f"Recent accuracy: {recent_acc:.4f}")
 print(f"Degradation: {degradation:.4f}")

if demobilization > 0.05: # 5 per cent degradation
PRint(("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}})}==((\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}}}})}================================================================================================================================================================================================================================================================================================
elif demobilization > 0.02: # 2% degradation
"preint("~ Prevention: Moderate degradation of performance")
 else:
Print("\\\performance is stable")

# Example of use:
def example_walk_forward_usage():
""example of Walk-Forward validation""

 from sklearn.ensemble import RandomForestClassifier

# of synthetic time data
 np.random.seed(42)
 n_samples, n_features = 2000, 20

# Identity generation with temporary structure
 X = np.random.randn(n_samples, n_features)

# a target variable with time dependency and drift
 y = np.zeros(n_samples)
 for i in range(n_samples):
# Drift: Pathers change over time
 if i < 500:
# Early period: simple pathers
 y[i] = 1 if X[i, 0] > 0 else 0
 elif i < 1000:
# Average period: more complex pathologies
 y[i] = 2 if X[i, 0] > 0.5 else (1 if X[i, 0] > -0.5 else 0)
 else:
# Latest period: Pathers change again
 y[i] = 1 if X[i, 0] > -0.2 else (2 if X[i, 0] > 0.8 else 0)

 print("=== example Walk-Forward validation ===")

♪ Create Model
 model = RandomForestClassifier(n_estimators=50, random_state=42)

# Implementation of Walk-Forward validation
 results = walk_forward_validation(
 model, X, y,
 train_size=500,
 step_size=100
 )

# Visualization of results
 plot_walk_forward_results(results)

# Analysis of stability
 analyze_walk_forward_stability(results)

 return results

# Launch examples (upstream for testing)
# results = example_walk_forward_usage()
```

## Hyperparametric optimization

**Theory:** Hyperparametric optimization is a process to find the best parameters of a model for achieving maximum performance. For financial data, this is critical, because incorrect parameters can lead to re-learning or failure.

**Why optimization is important for finance:**
- **retraining:** Financial data tends to be re-trained
- **Stability:** The right parameters ensure stability
- **Performance:** Optimal parameters improve accuracy
- ** Risk:** Balance between accuracy and stability

**methods optimization:**
1. **Grid Search:** Full range of all combinations of parameters
2. **Random Search:** Random Search:** Random Search in the Space of Parameters
3. **Bayesian Optimization:** Smart search with previous results
4. **Optuna:** Modern library for optimization

### 1. Grid Search

**Theory:**Grid Search is a method of full overtaking that tests all possible combinations of parameters from a given grid. Although it may be computationally expensive, it guarantees that optimum parameters are found in a given space.

** Grid Search working principle:**
1. **Network definition:** The range of values for each parameter is given
2. ** Full overtaking: ** All parameter combinations are tested
3. **Cross-validation:** Each combination is evaluated with CV aid
4. ** Choice of the best:** Combination with better productivity is selected

**Grid Search Plus:**
- Guarantees that optimum parameters are found in the grid.
- Simple in understanding and implementation
- Good Workinget with small parameters

**Minuses of Grid Search:**
- Calculatingly expensive.
- not scale on larger parameters
- Could be ineffective for continuous parameters

**Grid Search Practical Implementation:**

What does this code do?
1. **Network Definition:** Creates a set of parameters for Random Forest
2. **Cross-validation:** Uses Time Series CV for Financial Data
3. **Search:** Test all parameter combinations
4. ** Assessment:** Returns the best model and parameters

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_Report
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple

def optimize_random_forest(X, y, param_grid=None, cv_folds=5,
 scoring='accuracy', n_jobs=-1, random_state=42):
 """
Optimizing Random Forest with Grid Search

 Args:
X: Signal matrix (samples, features)
y: Target variables (samples,)
Param_grid: Search option grid
cv_folds: Number of folds for cross-validation
scoring: Metrique for evaluation
n_jobs: Number of parallel processes
Random_state: Seed for reproducibility

 Returns:
Tuple: (best model, best parameters, search results)
 """

 print("=== Grid Search for Random Forest ===")
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
(pint(f"Classes: {np.unique(y, return_counts=True)})

# The default option grid
 if param_grid is None:
 param_grid = {
 'n_estimators': [50, 100, 200],
 'max_depth': [5, 10, 15, None],
 'min_samples_split': [2, 5, 10],
 'min_samples_leaf': [1, 2, 4],
 'max_features': ['sqrt', 'log2', None]
 }

Print(f"\n Parameters Grid:")
 for param, values in param_grid.items():
 print(f"{param}: {values}")

# Calculation of total combinations
 total_combinations = 1
 for values in param_grid.values():
 total_combinations *= len(values)
(f "Total_combinations")
"Total_combinations * cv_folds})

# the core model
 rf = RandomForestClassifier(random_state=random_state, n_jobs=1)

# Create Time Series CV for Financial Data
 tscv = TimeSeriesSplit(n_splits=cv_folds)

 # Grid Search
 grid_search = GridSearchCV(
 estimator=rf,
 param_grid=param_grid,
 cv=tscv,
 scoring=scoring,
 n_jobs=n_jobs,
 verbose=1,
 return_train_score=True
 )

(f) Started by Grid Search...)
 grid_search.fit(X, y)

# Results
 best_model = grid_search.best_estimator_
 best_params = grid_search.best_params_
 best_score = grid_search.best_score_

== sync, corrected by elderman == @elder_man
Print(f "Best accuracy: {best_score:.4f}")
pint(f "Best parameters:")
 for param, value in best_params.items():
 print(f" {param}: {value}")

# Analysis of results
 results_df = pd.dataFrame(grid_search.cv_results_)

# Top five combinations
 top_results = results_df.nlargest(5, 'mean_test_score')[
 ['params', 'mean_test_score', 'std_test_score']
 ]

Print(f)\nTop-5 combinations:)
 for i, (_, row) in enumerate(top_results.iterrows(), 1):
 print(f"{i}. Score: {row['mean_test_score']:.4f} ± {row['std_test_score']:.4f}")
 print(f" Params: {row['params']}")

 return best_model, best_params, grid_search

def plot_grid_search_results(grid_search, param_name, figsize=(12, 8)):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 results_df = pd.dataFrame(grid_search.cv_results_)

# Filtering on the parameter
 param_results = results_df[results_df['param_' + param_name].notna()]

 if param_results.empty:
print(f"No data for parameter {param_name}")
 return

# Grouping on parameter values
 param_values = param_results['param_' + param_name].unique()
 mean_scores = []
 std_scores = []

 for value in param_values:
 value_results = param_results[param_results['param_' + param_name] == value]
 mean_scores.append(value_results['mean_test_score'].mean())
 std_scores.append(value_results['std_test_score'].mean())

# creative graphics
 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

# Schedule of average values
 ax1.errorbar(param_values, mean_scores, yerr=std_scores,
 marker='o', capsize=5, capthick=2)
 ax1.set_title(f'Grid Search Results: {param_name}')
 ax1.set_xlabel(param_name)
 ax1.set_ylabel('Mean Test Score')
 ax1.grid(True, alpha=0.3)

# Standard deviation schedule
 ax2.bar(param_values, std_scores, alpha=0.7)
 ax2.set_title(f'Score Variability: {param_name}')
 ax2.set_xlabel(param_name)
 ax2.set_ylabel('Std Test Score')
 ax2.grid(True, alpha=0.3)

 plt.tight_layout()
 plt.show()

def analyze_grid_search_stability(grid_search):
"Analysis of the Stability of Grid Search Results"

 results_df = pd.dataFrame(grid_search.cv_results_)

"print("===Grid Search Stability Analysis===)

# Best results
 best_score = grid_search.best_score_
 best_std = results_df.loc[grid_search.best_index_, 'std_test_score']

pprint(f "Best result:")
 print(f" Score: {best_score:.4f} ± {best_std:.4f}")
 print(f" CV: {best_std / best_score:.4f}")

# Analysis of stability
 all_scores = results_df['mean_test_score']
 all_stds = results_df['std_test_score']

(f) General statistics:)
 print(f" Score range: {all_scores.min():.4f} - {all_scores.max():.4f}")
 print(f" Mean std: {all_stds.mean():.4f}")
 print(f" Max std: {all_stds.max():.4f}")

# Top 10 results
 top_10 = results_df.nlargest(10, 'mean_test_score')

print(f)\nTop-10 results:)
 for i, (_, row) in enumerate(top_10.iterrows(), 1):
 print(f"{i:2d}. {row['mean_test_score']:.4f} ± {row['std_test_score']:.4f} - {row['params']}")

# Example of use:
def example_grid_search_usage():
""example of Great Search""

# creative synthetic data
 np.random.seed(42)
 n_samples, n_features = 1000, 20

# Signal generation
 X = np.random.randn(n_samples, n_features)

# the target variable
 y = np.zeros(n_samples)
 for i in range(n_samples):
 if X[i, 0] > 0.5 and X[i, 1] < -0.3:
 y[i] = 1
 elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
 y[i] = 2
 else:
 y[i] = 0

 print("=== example Grid Search ===")

# A simple grid for demonstration
 param_grid = {
 'n_estimators': [50, 100],
 'max_depth': [5, 10],
 'min_samples_split': [2, 5]
 }

# Implementation of the Great Search
 best_model, best_params, grid_search = optimize_random_forest(
 X, y, param_grid=param_grid, cv_folds=3
 )

# Analysis of results
 analyze_grid_search_stability(grid_search)

# Visualization (if precent data)
 if 'n_estimators' in best_params:
 plot_grid_search_results(grid_search, 'n_estimators')

 return best_model, best_params, grid_search

# Launch examples (upstream for testing)
# best_model, best_params, grid_search = example_grid_search_usage()
```

###2. Optuna optimization

**Theory:** Optuna is a modern library for hyperparametric optimization that uses Bayesian Optimization and other advanced methods for effective search for optimum parameters.

** Optuna working principle:**
1. **Bayesian Optimization:** uses previous results for selecting the following parameters
2. **Tree-Structured Parzen Estimator (TPE):** Effective algorithm for optimization
3. **Pruning:** Stops the non-prospecting tests before
4. **Parallation:** Supports parallel testing

**Why Optuna is effective for finance:**
- ** Effectiveness:** Finds good parameters faster than Great Search.
- **Scalability:**Workinget with larger parameters
- **Pruning:** Savings in computing resources
- ** Flexibility: ** Easily tailored to specific tasks

** Practical implementation of Optuna:**

What does this code do?
1. **Identification of space:** Creates search space
2. **Designation function for optimization:**
3. ** Tests: ** Performs many tests with different parameters
4. **Pruning:** Stops non-prospective tests

```python
import numpy as np
import pandas as pd
import optuna
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import accuracy_score, classification_Report
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

def optimize_xgboost_optuna(X, y, n_trials=100, cv_folds=5,
 timeout=None, n_jobs=1, random_state=42):
 """
Optimizing XGBoost with Optuna

 Args:
X: Signal matrix (samples, features)
y: Target variables (samples,)
n_trials: Number of tests
cv_folds: Number of folds for cross-validation
timeout: Maximum optimization time in seconds
n_jobs: Number of parallel processes
Random_state: Seed for reproducibility

 Returns:
top: (Best parameters, Studio object, best model)
 """

== sync, corrected by elderman == @elder_man
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
(pint(f"Classes: {np.unique(y, return_counts=True)})
(f "Number of tests: {n_trials}")

# Create Time Series CV for Financial Data
 tscv = TimeSeriesSplit(n_splits=cv_folds)

 def objective(trial):
 """Objective function for Optuna"""

# Definition of the parameters
 params = {
 'objective': 'multi:softprob',
 'num_class': len(np.unique(y)),
 'max_depth': trial.suggest_int('max_depth', 3, 12),
 'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
 'n_estimators': trial.suggest_int('n_estimators', 50, 500),
 'subsample': trial.suggest_float('subsample', 0.6, 1.0),
 'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
 'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 10.0),
 'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 10.0),
 'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
 'gamma': trial.suggest_float('gamma', 0.0, 5.0),
 'random_state': random_state,
 'n_jobs': 1,
 'verbosity': 0
 }

♪ Create Model
 model = xgb.XGBClassifier(**params)

# Cross-validation
 try:
 scores = cross_val_score(
 model, X, y,
 cv=tscv,
 scoring='accuracy',
 n_jobs=1
 )
 return scores.mean()
 except Exception as e:
# Return the bad result in error
 return 0.0

 # create study
 study = optuna.create_study(
 direction='maximize',
 sampler=optuna.samplers.TPESampler(seed=random_state),
 pruner=optuna.pruners.MedianPruner(
 n_startup_trials=10,
 n_warmup_steps=5,
 interval_steps=1
 )
 )

# Optimization
Print(f) Started optimization...)
 study.optimize(
 objective,
 n_trials=n_trials,
 timeout=timeout,
 n_jobs=n_jobs,
 show_progress_bar=True
 )

# Results
 best_params = study.best_params_
 best_score = study.best_value

*Prent(f"\n===Optuna results====)
Print(f "Best accuracy: {best_score:.4f}")
pint(f "Best parameters:")
 for param, value in best_params.items():
 print(f" {param}: {value}")

# the best model
 best_model = xgb.XGBClassifier(**best_params)
 best_model.fit(X, y)

# Analysis of results
(pint(f'\n=== Optimization analysis===)
(f "Number of completed tests: {len(studie.trials)}")
(f) Number of interrupted tests: {len([t for t in study.trials if t.state ==optuna.trial.TialStatate.PRUNED]}}

 return best_params, study, best_model

def plot_optuna_results(study, figsize=(15, 10)):
"Visualization of Optuna Results""

 fig, axes = plt.subplots(2, 2, figsize=figsize)

# Timetable of the Optimisation History
 trials = study.trials
 trial_numbers = [t.number for t in trials if t.state == optuna.trial.TrialState.COMPLETE]
 values = [t.value for t in trials if t.state == optuna.trial.TrialState.COMPLETE]

 axes[0, 0].plot(trial_numbers, values, 'o-', alpha=0.7)
 axes[0, 0].set_title('Optimization History')
 axes[0, 0].set_xlabel('Trial Number')
 axes[0, 0].set_ylabel('Objective Value')
 axes[0, 0].grid(True, alpha=0.3)

# A schedule of the importance of parameters
 try:
 importance = optuna.importance.get_param_importances(study)
 params = List(importance.keys())
 importances = List(importance.values())

 axes[0, 1].barh(params, importances)
 axes[0, 1].set_title('Parameter importance')
 axes[0, 1].set_xlabel('importance')
 axes[0, 1].grid(True, alpha=0.3)
 except Exception as e:
 axes[0, 1].text(0.5, 0.5, f'importance not available:\n{str(e)}',
 ha='center', va='center', transform=axes[0, 1].transAxes)
 axes[0, 1].set_title('Parameter importance')

# Timetable for distribution of values
 if len(values) > 0:
 axes[1, 0].hist(values, bins=20, alpha=0.7, edgecolor='black')
 axes[1, 0].axvline(np.mean(values), color='red', linestyle='--',
 label=f'Mean: {np.mean(values):.4f}')
 axes[1, 0].axvline(np.max(values), color='green', linestyle='--',
 label=f'Best: {np.max(values):.4f}')
 axes[1, 0].set_title('Value Distribution')
 axes[1, 0].set_xlabel('Objective Value')
 axes[1, 0].set_ylabel('Frequency')
 axes[1, 0].legend()
 axes[1, 0].grid(True, alpha=0.3)

# Convergence schedule
 if len(values) > 1:
 best_values = np.maximum.accumulate(values)
 axes[1, 1].plot(trial_numbers, best_values, 'g-', linewidth=2, label='Best Value')
 axes[1, 1].plot(trial_numbers, values, 'o-', alpha=0.3, label='all Values')
 axes[1, 1].set_title('Convergence')
 axes[1, 1].set_xlabel('Trial Number')
 axes[1, 1].set_ylabel('Best Objective Value')
 axes[1, 1].legend()
 axes[1, 1].grid(True, alpha=0.3)

 plt.tight_layout()
 plt.show()

def analyze_optuna_study(study):
"Analysis of Optuna Studio Results"

===Optuna Study Analysis===================Optuna Study============================================Principle==================Optuna Study)===========================================Principles===========* Opuna Studie)

# Basic statistics
 trials = study.trials
 COMPLETED_trials = [t for t in trials if t.state == optuna.trial.TrialState.COMPLETE]
 pruned_trials = [t for t in trials if t.state == optuna.trial.TrialState.PRUNED]

all tests: {len(trials)})
(f" Completed: {len(COMPLETED_trials)})
(f) Interrupted: {len(prened_trials}})

 if COMPLETED_trials:
 values = [t.value for t in COMPLETED_trials]
Print(f"\nStatistics of values:")
Best: {max(valutes):4f}})
pprint(f" Worst: {min(valutes): 4f}})
Middle: {np.mean(valutes): 4f})
standard deviation: {np.std(valutes): 4f})

# Convergence analysis
 best_values = np.maximum.accumulate(values)
 improvement = best_values[-1] - best_values[0]
(f'nAdvance: {improvement:.4f})

# Analysis of stability
 recent_trials = min(10, len(values))
 recent_values = values[-recent_trials:]
 recent_std = np.std(recent_values)
prent(f) "Stability (last test {recent_trials}): {recent_std:.4f}")

# Analysis of parameters
 if COMPLETED_trials:
Print(f"\nAnalysis of parameters:")
 param_names = List(COMPLETED_trials[0].params.keys())

 for param_name in param_names:
 param_values = [t.params[param_name] for t in COMPLETED_trials]
 if isinstance(param_values[0], (int, float)):
 print(f" {param_name}: {min(param_values):.4f} - {max(param_values):.4f}")
 else:
 unique_values = List(set(param_values))
 print(f" {param_name}: {unique_values}")

# Example of use:
def example_optuna_usage():
""Example of Optuna""

# creative synthetic data
 np.random.seed(42)
 n_samples, n_features = 1000, 20

# Signal generation
 X = np.random.randn(n_samples, n_features)

# the target variable
 y = np.zeros(n_samples)
 for i in range(n_samples):
 if X[i, 0] > 0.5 and X[i, 1] < -0.3:
 y[i] = 1
 elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
 y[i] = 2
 else:
 y[i] = 0

"spint("== example Optuna optimization===)

# Optimization
 best_params, study, best_model = optimize_xgboost_optuna(
 X, y, n_trials=50, cv_folds=3
 )

# Visualization of results
 plot_optuna_results(study)

# Analysis of results
 analyze_optuna_study(study)

 return best_params, study, best_model

# Launch examples (upstream for testing)
# best_params, study, best_model = example_optuna_usage()
```

## Implementation of ensemble methods

**Theory:** Ansemble meths combine several models for improving performance. This is particularly important in the financial sphere, as different models can identify different variables in data.

**Why are ensembles effective for finance:**
- ** Risk reduction: ** Model combination reduces risk of errors
- ** Diversity: ** Different models identify different patterns
- **Stability:** Ansambles are more stable than individual models
- **Purity:** Emission and noise resistant

**Tips of ensemble:**
1. **Voting: **Simple voting of models
2. **Stacking:** Meta-model is being trained on basic model predictions
3. **Blending:** Weighted combination of preferences
4. **Bagging:** Training on different sub-samples

### 1. Voting Classifier

**Theory:** Voting Classifier is a simple ensemble method that combines the predictions of several models through a vote.

**Voting principle:**
1. **Hard Voting:** Each model votes for the class, the class with the majority vote
2. **Soft Voting:** Each model returns probability, calculates average and selects class with maximum probability

** Plus Voting:**
- Simplicity of implementation
- Good Workinget with diverse models
- Easy to interpret.

**Minuses Voting:**
-not takes into account the quality of individual models
- Could be ineffective with bad models.

** Practical implementation of Voting Classifier:**

What does this code do?
1. **create models:** Identify basic models for an ensemble
2. **Voting:** Sets the type of voting (hard/soft)
3. **Learning:** Trains the whole band
4. ** Evaluation:** Checks the performance of the ensemble

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_Report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Tuple

def create_ensemble_model(X, y, voting='soft', test_size=0.2, random_state=42):
 """
Create ensemble model with Voting Classifier

 Args:
X: Signal matrix (samples, features)
y: Target variables (samples,)
voting: Type of voting ('hard' or 'soft')
test_size: Percentage of test data
Random_state: Seed for reproducibility

 Returns:
Tuple: (embalming model, metrics, individual models)
 """

 print("=== create Voting Ensemble ===")
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
(pint(f"Classes: {np.unique(y, return_counts=True)})
(f) Type of voting: {volting})

# Data sharing
 X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=test_size, random_state=random_state, stratify=y
 )

Print(f "Learning sample: {X_training.chape[0]} samples")
print(f"tests sample: {X_test.chape[0]} samples)

#ake individual models
 models = {
 'rf': RandomForestClassifier(
 n_estimators=100,
 max_depth=10,
 random_state=random_state,
 n_jobs=-1
 ),
 'xgb': xgb.XGBClassifier(
 n_estimators=100,
 max_depth=6,
 learning_rate=0.1,
 random_state=random_state,
 n_jobs=-1,
 verbosity=0
 ),
 'lgb': lgb.LGBMClassifier(
 n_estimators=100,
 max_depth=6,
 learning_rate=0.1,
 random_state=random_state,
 n_jobs=-1,
 verbose=-1
 )
 }

(f'nIndividual Models:)
 for name, model in models.items():
 print(f" {name}: {type(model).__name__}")

 # create Voting Classifier
 ensemble = VotingClassifier(
 estimators=List(models.items()),
 voting=voting,
 n_jobs=-1
 )

# Ensemble education
(f) Ensemble education...)
 ensemble.fit(X_train, y_train)

# The ensemble's predictions
 y_pred_ensemble = ensemble.predict(X_test)
 y_pred_proba_ensemble = ensemble.predict_proba(X_test)

# The ensemble's evaluation
 ensemble_accuracy = accuracy_score(y_test, y_pred_ensemble)

== sync, corrected by elderman == @elder_man
 print(f"Ensemble accuracy: {ensemble_accuracy:.4f}")

# Individual model evaluation
 individual_scores = {}
 individual_predictions = {}

Prent(f'\n=== Individual model results===)
 for name, model in models.items():
# Individual model training
 model.fit(X_train, y_train)

# Premonition
 y_pred = model.predict(X_test)
 y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None

# Evaluation
 accuracy = accuracy_score(y_test, y_pred)
 individual_scores[name] = accuracy
 individual_predictions[name] = y_pred

 print(f"{name}: {accuracy:.4f}")

# Comparson of results
== sync, corrected by elderman ==
 best_individual = max(individual_scores, key=individual_scores.get)
 best_individual_score = individual_scores[best_individual]

print(f) "Best individual model: {best_individual}({best_individual_score:.4f})")
(f "Ansemble: {ensemble_accuracy:.4f}")
 print(f"improve: {ensemble_accuracy - best_individual_score:.4f}")

# Detailed Report
 print(f"\n=== Classification Report (Ensemble) ===")
 print(classification_Report(y_test, y_pred_ensemble))

# metrics for return
 metrics = {
 'ensemble_accuracy': ensemble_accuracy,
 'individual_scores': individual_scores,
 'best_individual': best_individual,
 'improvement': ensemble_accuracy - best_individual_score,
 'confusion_matrix': confusion_matrix(y_test, y_pred_ensemble),
 'predictions': y_pred_ensemble,
 'probabilities': y_pred_proba_ensemble
 }

 return ensemble, metrics, models

def plot_ensemble_comparison(metrics, figsize=(12, 8)):
"Visualization of ensemble comparison and individual models"

 fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

# Accuracy schedule
 models = List(metrics['individual_scores'].keys()) + ['Ensemble']
 scores = List(metrics['individual_scores'].values()) + [metrics['ensemble_accuracy']]
 colors = ['lightblue'] * len(metrics['individual_scores']) + ['red']

 bars = ax1.bar(models, scores, color=colors, alpha=0.7)
 ax1.set_title('Model Performance Comparison')
 ax1.set_ylabel('Accuracy')
 ax1.set_ylim(0, 1)

# add values on column
 for bar, score in zip(bars, scores):
 height = bar.get_height()
 ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
 f'{score:.3f}', ha='center', va='bottom')

 ax1.grid(True, alpha=0.3)

# An improvement schedule
 individual_scores = List(metrics['individual_scores'].values())
 ensemble_score = metrics['ensemble_accuracy']
 improvements = [ensemble_score - score for score in individual_scores]

 ax2.bar(metrics['individual_scores'].keys(), improvements,
 color='green', alpha=0.7)
 ax2.set_title('Improvement over Individual Models')
 ax2.set_ylabel('Improvement')
 ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
 ax2.grid(True, alpha=0.3)

 plt.tight_layout()
 plt.show()

def analyze_ensemble_diversity(individual_predictions, y_test):
"Analysis of Ensemble Diversity."

"print("===A ensemble diversity analysis===)

# Calculation of consistency between models
 model_names = List(individual_predictions.keys())
 n_models = len(model_names)

# Coherence matrix
 agreement_matrix = np.zeros((n_models, n_models))

 for i, model1 in enumerate(model_names):
 for j, model2 in enumerate(model_names):
 if i != j:
 agreement = np.mean(individual_predictions[model1] == individual_predictions[model2])
 agreement_matrix[i, j] = agreement

Print(f "Coherence matrix:")
(f "Medical consistency: {np.mean(agrement_matrix): 4f}")
(f "Minimum consistency: {np.min(agrement_matrix): 4f}")
(f) Maximum consistency: {np.max(agrement_matrix): 4f})

# Mistake analysis
 correct_predictions = {}
 for name, pred in individual_predictions.items():
 correct_predictions[name] = (pred == y_test)

# Cases where all models are wrong
 all_wrong = np.all([~correct_predictions[name] for name in model_names], axis=0)
 all_wrong_count = np.sum(all_wrong)

# Cases where all models were right
 all_correct = np.all([correct_predictions[name] for name in model_names], axis=0)
 all_correct_count = np.sum(all_correct)

Prent(f'nanalysis of errors:)
print(f) "All models are right: {all_control_account}({all_control_account/len(y_test)*100:.1f}%")
(f) All models were wrong: {all_wrong_account}({all_wrong_account/len(y_test)*100:.1f}%)

# Cases where opinions were divided
 mixed_cases = len(y_test) - all_correct_count - all_wrong_count
spring(f "Mixed cases: {mixed_cases}({mixed_cases/len(y_test)*100:.1f}%")

# Example of use:
def example_voting_ensemble_usage():
""example of Voting Ensemble""

# creative synthetic data
 np.random.seed(42)
 n_samples, n_features = 1000, 20

# Signal generation
 X = np.random.randn(n_samples, n_features)

# the target variable
 y = np.zeros(n_samples)
 for i in range(n_samples):
 if X[i, 0] > 0.5 and X[i, 1] < -0.3:
 y[i] = 1
 elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
 y[i] = 2
 else:
 y[i] = 0

 print("=== example Voting Ensemble ===")

# Create ensemble
 ensemble, metrics, models = create_ensemble_model(X, y, voting='soft')

# Visualization of results
 plot_ensemble_comparison(metrics)

# Analysis of diversity
 individual_predictions = {}
 for name, model in models.items():
 individual_predictions[name] = model.predict(X)

 analyze_ensemble_diversity(individual_predictions, y)

 return ensemble, metrics, models

# Launch examples (upstream for testing)
# ensemble, metrics, models = example_voting_ensemble_usage()
```

### 2. Stacking

**Theory:** Stacking (Stacked Generalization) is an advanced ensemble method that uses a meta-model for combining basic models. Meta-model is being trained on the predictions of basic models, allowing it to find the best ways to combine them.

**Stacking principle:**
1. ** Basic models:** Training on baseline data
2. ** Projections: ** Basic models make predictions on validation data
3. **Metha Model: ** Training on basic model predictions
4. **FinalPedication:** Meta Model combines the predictions of basic models

** Plus Stacking:**
- More complex model combinations
- Meta-model can learn non-linear dependencies.
- He often shows better results than Voting.

**Stacking Minuses:**
- More complex implementation
- Requires more computing resources
- Maybe relearning when you're in the wrong setting.

** Practical implementation of Stacking:**

What does this code do?
1. ** Basic models:** Identifys a range of models
2. **Metha-model:** Picks a model for combining preferences
3. **Cross-validation:** Usees CV for prevention of retraining
4. **Learning:** Trains the whole stack of models

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_Report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Tuple

def create_stacking_model(X, y, test_size=0.2, cv_folds=5, random_state=42):
 """
creative Stacking Model

 Args:
X: Signal matrix (samples, features)
y: Target variables (samples,)
test_size: Percentage of test data
cv_folds: Number of folds for cross-validation
Random_state: Seed for reproducibility

 Returns:
tuple: (stacking model, metrics, basic models)
 """

== sync, corrected by elderman == @elder_man
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
(pint(f"Classes: {np.unique(y, return_counts=True)})
print(f "Number of CV Folds: {cv_folds}")

# Data sharing
 X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=test_size, random_state=random_state, stratify=y
 )

Print(f "Learning sample: {X_training.chape[0]} samples")
print(f"tests sample: {X_test.chape[0]} samples)

# square basic models
 base_models = [
 ('rf', RandomForestClassifier(
 n_estimators=100,
 max_depth=10,
 random_state=random_state,
 n_jobs=-1
 )),
 ('xgb', xgb.XGBClassifier(
 n_estimators=100,
 max_depth=6,
 learning_rate=0.1,
 random_state=random_state,
 n_jobs=-1,
 verbosity=0
 )),
 ('lgb', lgb.LGBMClassifier(
 n_estimators=100,
 max_depth=6,
 learning_rate=0.1,
 random_state=random_state,
 n_jobs=-1,
 verbose=-1
 )),
 ('svm', SVC(
 probability=True,
 random_state=random_state
 )),
 ('mlp', MLPClassifier(
 hidden_layer_sizes=(100, 50),
 max_iter=500,
 random_state=random_state
 ))
 ]

(f'n Basic Models:)
 for name, model in base_models:
 print(f" {name}: {type(model).__name__}")

# creative meta-model
 meta_models = {
 'logistic': LogisticRegression(random_state=random_state, max_iter=1000),
 'rf_meta': RandomForestClassifier(n_estimators=50, random_state=random_state),
 'xgb_meta': xgb.XGBClassifier(n_estimators=50, random_state=random_state, verbosity=0)
 }

Print(f"\nMeta-model:")
 for name, model in meta_models.items():
 print(f" {name}: {type(model).__name__}")

# Testing of different meta-models
 best_meta_model = None
 best_score = 0
 meta_scores = {}

(f) Testing meta-models...)

 for meta_name, meta_model in meta_models.items():
# Create Stacking Model
 stacking_model = StackingClassifier(
 estimators=base_models,
 final_estimator=meta_model,
 cv=cv_folds,
 n_jobs=-1
 )

# Cross-validation
 scores = cross_val_score(
 stacking_model, X_train, y_train,
 cv=cv_folds, scoring='accuracy'
 )

 mean_score = scores.mean()
 meta_scores[meta_name] = mean_score

 print(f" {meta_name}: {mean_score:.4f} ± {scores.std():.4f}")

 if mean_score > best_score:
 best_score = mean_score
 best_meta_model = meta_model

The best meta-model:(max(meta_scores, key=meta_scores.get)})

# Create final Stacking model
 final_stacking_model = StackingClassifier(
 estimators=base_models,
 final_estimator=best_meta_model,
 cv=cv_folds,
 n_jobs=-1
 )

# Training
(f'n Training Stacking Model...)
 final_stacking_model.fit(X_train, y_train)

# Premonition
 y_pred_stacking = final_stacking_model.predict(X_test)
 y_pred_proba_stacking = final_stacking_model.predict_proba(X_test)

# Stacking model evaluation
 stacking_accuracy = accuracy_score(y_test, y_pred_stacking)

(f'\n===Stacking model results===)
 print(f"Stacking accuracy: {stacking_accuracy:.4f}")

# Assessment of basic models
 base_scores = {}
 base_predictions = {}

===Background model results========Background model results===)
 for name, model in base_models:
# Training the basic model
 model.fit(X_train, y_train)

# Premonition
 y_pred = model.predict(X_test)
 y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None

# Evaluation
 accuracy = accuracy_score(y_test, y_pred)
 base_scores[name] = accuracy
 base_predictions[name] = y_pred

 print(f"{name}: {accuracy:.4f}")

# Comparson of results
== sync, corrected by elderman ==
 best_base = max(base_scores, key=base_scores.get)
 best_base_score = base_scores[best_base]

print(f"Best basic model: {best_base}({best_base_score:.4f})")
(f"Stacking model: {stacking_accuracy:.4f})
 print(f"improve: {stacking_accuracy - best_base_score:.4f}")

# Detailed Report
 print(f"\n=== Classification Report (Stacking) ===")
 print(classification_Report(y_test, y_pred_stacking))

# metrics for return
 metrics = {
 'stacking_accuracy': stacking_accuracy,
 'base_scores': base_scores,
 'meta_scores': meta_scores,
 'best_base': best_base,
 'best_meta': max(meta_scores, key=meta_scores.get),
 'improvement': stacking_accuracy - best_base_score,
 'confusion_matrix': confusion_matrix(y_test, y_pred_stacking),
 'predictions': y_pred_stacking,
 'probabilities': y_pred_proba_stacking
 }

 return final_stacking_model, metrics, base_models

def plot_stacking_results(metrics, figsize=(15, 10)):
"Visualization of Stacking Results."

 fig, axes = plt.subplots(2, 2, figsize=figsize)

# Schedule for comparison of basic models and Stacking
 models = List(metrics['base_scores'].keys()) + ['Stacking']
 scores = List(metrics['base_scores'].values()) + [metrics['stacking_accuracy']]
 colors = ['lightblue'] * len(metrics['base_scores']) + ['red']

 bars = axes[0, 0].bar(models, scores, color=colors, alpha=0.7)
 axes[0, 0].set_title('Base Models vs Stacking')
 axes[0, 0].set_ylabel('Accuracy')
 axes[0, 0].set_ylim(0, 1)

# add values on column
 for bar, score in zip(bars, scores):
 height = bar.get_height()
 axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
 f'{score:.3f}', ha='center', va='bottom')

 axes[0, 0].grid(True, alpha=0.3)

# Meta-model graphics
 meta_models = List(metrics['meta_scores'].keys())
 meta_scores = List(metrics['meta_scores'].values())

 bars = axes[0, 1].bar(meta_models, meta_scores, color='green', alpha=0.7)
 axes[0, 1].set_title('Meta-Model Performance')
 axes[0, 1].set_ylabel('Accuracy')
 axes[0, 1].set_ylim(0, 1)

# add values on column
 for bar, score in zip(bars, meta_scores):
 height = bar.get_height()
 axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
 f'{score:.3f}', ha='center', va='bottom')

 axes[0, 1].grid(True, alpha=0.3)

# An improvement schedule
 base_scores = List(metrics['base_scores'].values())
 stacking_score = metrics['stacking_accuracy']
 improvements = [stacking_score - score for score in base_scores]

 axes[1, 0].bar(metrics['base_scores'].keys(), improvements,
 color='orange', alpha=0.7)
 axes[1, 0].set_title('Stacking Improvement over Base Models')
 axes[1, 0].set_ylabel('Improvement')
 axes[1, 0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
 axes[1, 0].grid(True, alpha=0.3)

# A matrix of errors
 cm = metrics['confusion_matrix']
 sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 1])
 axes[1, 1].set_title('Confusion Matrix (Stacking)')
 axes[1, 1].set_xlabel('Predicted')
 axes[1, 1].set_ylabel('True')

 plt.tight_layout()
 plt.show()

def analyze_stacking_contribution(stacking_model, X_test, y_test):
"Analysis of the Contribution of Basic Models in Stacking"

"print("=== Analysis of the contribution of basic models===)

# Obtaining basic models
 base_predictions = stacking_model.transform(X_test)

# The Meta Model Weights
 if hasattr(stacking_model.final_estimator_, 'coef_'):
# for linear models
 weights = stacking_model.final_estimator_.coef_[0]
spring(f) Meta-model weights: {weights})

# Analysis of the importance of basic models
 base_names = [name for name, _ in stacking_model.estimators]
 for name, weight in zip(base_names, weights):
 print(f" {name}: {weight:.4f}")

# Analysis of correlations between basic models
 base_predictions_df = pd.dataFrame(
 base_predictions,
 columns=[name for name, _ in stacking_model.estimators]
 )

 correlation_matrix = base_predictions_df.corr()

prent(f"\nCoordination matrix of basic models:")
 print(correlation_matrix.round(3))

# Analysis of diversity
 mean_correlation = correlation_matrix.values[np.triu_indices_from(correlation_matrix.values, k=1)].mean()
*Mean correlation: {mean_control:.4f})

 if mean_correlation < 0.5:
"Prent("♪ Good diversity of basic models")
 elif mean_correlation < 0.7:
print("\'Memated diversity of basic models")
 else:
printh("\\\ low diversity of basic models")

# Example of use:
def example_stacking_usage():
""example Stacking""

# creative synthetic data
 np.random.seed(42)
 n_samples, n_features = 1000, 20

# Signal generation
 X = np.random.randn(n_samples, n_features)

# the target variable
 y = np.zeros(n_samples)
 for i in range(n_samples):
 if X[i, 0] > 0.5 and X[i, 1] < -0.3:
 y[i] = 1
 elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
 y[i] = 2
 else:
 y[i] = 0

 print("=== example Stacking ===")

# Create Stacking Model
 stacking_model, metrics, base_models = create_stacking_model(X, y)

# Visualization of results
 plot_stacking_results(metrics)

# Analysis of the contribution of basic models
 analyze_stacking_contribution(stacking_model, X, y)

 return stacking_model, metrics, base_models

# Launch examples (upstream for testing)
# stacking_model, metrics, base_models = example_stacking_usage()
```

## Performance evaluation

**Theory:** Evaluation of the performance of models for financial data requires a special approach, as standard metrics can not reflect the real effectiveness of trade strategy.

**Why standard metrics are not enough:**
- ** The accuracy of n is equal to the profitability:** High accuracy can not mean the profitability
- ** Classic imbalance:** Financial data often have class imbalances
- ** Time-dependency:** Important sequence of preferences
- ** Risk return: ** Risk to be taken into account and not only return

**Tip metrics:**
1. ** Classification metrics:** Accuracy, Precion, Recall, F1
2. **Trade metrics:** Sharpe Ratio, Maximum Drawdown, Win Rate
3. **Temporary metrics:** Stability in time
4. **Pictic metrics:** VaR, CVAR, Volatility

♪##1. metrics classification

**Theory:** Classification metrics measures the quality of the prescriptions of the model on basis of the correct classification of samples on classes.

** Basic metrics:**
**Accuracy:** Proportion of correctly classified samples
- **Precion:** Share of true positive among the predicted positive
- **Recall:** Share of true positive in all positive
- **F1-Score:** Harmonic Middle Precion and Recall

** Practical implementation of classification metric:**

What does this code do?
1. **Treaths:** Receives model predictions
2. **Metric calculation:** Calculates different quality metrics
3. ** Visualization:** Creates graphs for Analysis
4. **Analysis:** Inserts results

```python
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
 f1_score, confusion_matrix, classification_Report,
 roc_auc_score, roc_curve, precision_recall_curve)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple, List

def evaluate_model(model, X_test, y_test, model_name="Model"):
 """
Integrated model evaluation

 Args:
Model: Trained model
X_test: testes
y_test: testes
Model_name: Name of model for Reports

 Returns:
dict: dictionary with metrics and results
 """

=== Model evaluation: {model_name}================= Model evaluation======* Model evaluation: {model_name}============Principals========* Model evaluation====* Model evaluation: {model_name}=========* Model evaluation========* Model evaluation:======* Model evaluation===========================================================Plots =========================================================================================================================================================================================================================================================================================================================================
Print(f "Tests sample measurement: {len(y_test)} samples")
(pint(f"Classes: {np.unique(y_test, retorn_counts=True)})

# Premonition
 y_pred = model.predict(X_test)
 y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None

# Basic metrics
 accuracy = accuracy_score(y_test, y_pred)
 precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
 recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
 f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

# metrics on classes
 precision_per_class = precision_score(y_test, y_pred, average=None, zero_division=0)
 recall_per_class = recall_score(y_test, y_pred, average=None, zero_division=0)
 f1_per_class = f1_score(y_test, y_pred, average=None, zero_division=0)

# A matrix of errors
 cm = confusion_matrix(y_test, y_pred)

# ROC AUC (for binary classification)
 roc_auc = None
 if len(np.unique(y_test)) == 2 and y_pred_proba is not None:
 roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])

# Results
 results = {
 'model_name': model_name,
 'accuracy': accuracy,
 'precision': precision,
 'recall': recall,
 'f1': f1,
 'precision_per_class': precision_per_class,
 'recall_per_class': recall_per_class,
 'f1_per_class': f1_per_class,
 'confusion_matrix': cm,
 'roc_auc': roc_auc,
 'predictions': y_pred,
 'probabilities': y_pred_proba
 }

# Conclusion of results
== Results============================)=========================)=================Prent(f)========= Results====)
 print(f"Accuracy: {accuracy:.4f}")
 print(f"Precision: {precision:.4f}")
 print(f"Recall: {recall:.4f}")
 print(f"F1-Score: {f1:.4f}")

 if roc_auc is not None:
 print(f"ROC AUC: {roc_auc:.4f}")

# Detailed Report
 print(f"\n=== Classification Report ===")
 print(classification_Report(y_test, y_pred))

 return results

def plot_classification_metrics(results, figsize=(15, 10)):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 fig, axes = plt.subplots(2, 2, figsize=figsize)

# A matrix of errors
 cm = results['confusion_matrix']
 sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
 axes[0, 0].set_title('Confusion Matrix')
 axes[0, 0].set_xlabel('Predicted')
 axes[0, 0].set_ylabel('True')

# metrics on classes
 classes = range(len(results['precision_per_class']))
 x = np.arange(len(classes))
 width = 0.25

 axes[0, 1].bar(x - width, results['precision_per_class'], width, label='Precision', alpha=0.8)
 axes[0, 1].bar(x, results['recall_per_class'], width, label='Recall', alpha=0.8)
 axes[0, 1].bar(x + width, results['f1_per_class'], width, label='F1-Score', alpha=0.8)

 axes[0, 1].set_title('Metrics per Class')
 axes[0, 1].set_xlabel('Class')
 axes[0, 1].set_ylabel('Score')
 axes[0, 1].set_xticks(x)
 axes[0, 1].set_xticklabels(classes)
 axes[0, 1].legend()
 axes[0, 1].grid(True, alpha=0.3)

# General metrics
 metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
 values = [results['accuracy'], results['precision'], results['recall'], results['f1']]

 bars = axes[1, 0].bar(metrics, values, color=['skyblue', 'lightgreen', 'lightcoral', 'gold'], alpha=0.8)
 axes[1, 0].set_title('Overall Metrics')
 axes[1, 0].set_ylabel('Score')
 axes[1, 0].set_ylim(0, 1)

# add values on column
 for bar, value in zip(bars, values):
 height = bar.get_height()
 axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
 f'{value:.3f}', ha='center', va='bottom')

 axes[1, 0].grid(True, alpha=0.3)

# ROC curve (if available)
 if results['roc_auc'] is not None:
 fpr, tpr, _ = roc_curve(results['y_test'], results['probabilities'][:, 1])
 axes[1, 1].plot(fpr, tpr, color='darkorange', lw=2,
 label=f'ROC curve (AUC = {results["roc_auc"]:.2f})')
 axes[1, 1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
 axes[1, 1].set_xlim([0.0, 1.0])
 axes[1, 1].set_ylim([0.0, 1.05])
 axes[1, 1].set_xlabel('False Positive Rate')
 axes[1, 1].set_ylabel('True Positive Rate')
 axes[1, 1].set_title('ROC Curve')
 axes[1, 1].legend(loc="lower right")
 axes[1, 1].grid(True, alpha=0.3)
 else:
 axes[1, 1].text(0.5, 0.5, 'ROC Curve not available\nfor multiclass problem',
 ha='center', va='center', transform=axes[1, 1].transAxes)
 axes[1, 1].set_title('ROC Curve')

 plt.tight_layout()
 plt.show()

def analyze_class_balance(y_test, y_pred):
"Analysis of the Class Balance."

"print("===Class balance analysis===)

# Distribution of classes
 unique_classes, counts = np.unique(y_test, return_counts=True)
 total_samples = len(y_test)

(f) Class distribution in test sample:)
 for class_label, count in zip(unique_classes, counts):
 percentage = count / total_samples * 100
(f) Class {class_label}: {account}( {operation:.1f}%))

# Analysis of preferences
 pred_unique, pred_counts = np.unique(y_pred, return_counts=True)

pprint(f"n Distributions:")
 for class_label, count in zip(pred_unique, pred_counts):
 percentage = count / total_samples * 100
(f) Class {class_label}: {account}( {operation:.1f}%))

# Analysis of the imbalance
 max_count = max(counts)
 min_count = min(counts)
 imbalance_ratio = max_count / min_count

(f'nAnalysis of the imbalance:)
Print(f" Class ratio: {imbalance_ratio:.2f}:1)

 if imbalance_ratio > 10:
"Prent(" ♪ Strong grade imbalance")
 elif imbalance_ratio > 3:
"Print(" * Moderate class imbalance")
 else:
"Prent(" * Balanced classes")

# Example of use:
def example_classification_metrics_usage():
"example of use of classification metric""

 from sklearn.ensemble import RandomForestClassifier
 from sklearn.datasets import make_classification

# creative synthetic data
 X, y = make_classification(
 n_samples=1000, n_features=20, n_classes=3,
 n_informative=15, n_redundant=5, random_state=42
 )

# Data sharing
 from sklearn.model_selection import train_test_split
 X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=0.2, random_state=42, stratify=y
 )

# Model learning
 model = RandomForestClassifier(n_estimators=100, random_state=42)
 model.fit(X_train, y_train)

"print("== example classification metric===)

# Model evaluation
 results = evaluate_model(model, X_test, y_test, "Random Forest")

# Visualization of results
 plot_classification_metrics(results)

# Class balance analysis
 analyze_class_balance(y_test, results['predictions'])

 return results

# Launch examples (upstream for testing)
# results = example_classification_metrics_usage()
```

♪##2 ♪ Trade metrics ♪

**Theory:** Trade metrics measure the real effectiveness of a trade strategy, taking into account not only accuracy of preferences but also financial results.

** Main trade instruments:**
**Sharpe Rato:** The ratio of return to risk
- **Maximum Drawdown:** Maximum loss from peak
- **Win Rate:** Share of profit-making transactions
- **Profit Factor:** Profit-loss ratio
- **Calmar Rato:** The ratio of return to maximum draught

** Practical implementation of trade metrics:**

What does this code do?
1. ** Interest calculation:** Calculates the profitability of the strategy
2. **Ricular metrics:** Assesss the risk of the strategy
3. **Trade indicators:** Analysis of trade quality
4. ** Visualization:** Creates graphs for Analysis

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple, List
from sklearn.metrics import accuracy_score

def calculate_trading_metrics(y_true, y_pred, returns, transaction_costs=0.001):
 """
Calculation of trade metrics for financial strategy

 Args:
y_tree: True classes (0:sale, 1: retention, 2: buying)
y_pred: Anticipated classes
Returns: Income of assets
Transfer_costs: Travel costs (percentage from transaction)

 Returns:
dict: dictionary with trade metrics
 """

"print("=====Methics of trade===)
number of transactions: {len(y_tree}})
Print(f "Tranction costs: {transaction_costs*100:.2f}%")

# Basic metrics
 accuracy = accuracy_score(y_true, y_pred)

# Trade signals
# 0: sales (-1), 1: retention (0), 2: buying (1)
 signal_mapping = {0: -1, 1: 0, 2: 1}
 y_true_signals = np.array([signal_mapping[label] for label in y_true])
 y_pred_signals = np.array([signal_mapping[label] for label in y_pred])

# Calculation of strategy returns
 strategy_returns = returns * y_pred_signals

# Accounting for transaction costs
 position_changes = np.diff(y_pred_signals, prepend=y_pred_signals[0])
 transaction_costs_total = np.abs(position_changes) * transaction_costs
 strategy_returns_net = strategy_returns - transaction_costs_total

# Main trade metrics
 total_return = np.sum(strategy_returns_net)
 annualized_return = np.mean(strategy_returns_net) * 252

# Volatility
 volatility = np.std(strategy_returns_net) * np.sqrt(252)

 # Sharpe Ratio
 if volatility > 0:
 sharpe_ratio = annualized_return / volatility
 else:
 sharpe_ratio = 0

# Maximum tarmac
 cumulative_returns = np.cumprod(1 + strategy_returns_net)
 running_max = np.maximum.accumulate(cumulative_returns)
 drawdown = (cumulative_returns - running_max) / running_max
 max_drawdown = np.min(drawdown)

 # Calmar Ratio
 if abs(max_drawdown) > 0:
 calmar_ratio = annualized_return / abs(max_drawdown)
 else:
 calmar_ratio = np.inf

 # Win Rate
 profitable_trades = strategy_returns_net > 0
 win_rate = np.mean(profitable_trades) if len(profitable_trades) > 0 else 0

 # Profit Factor
 gross_profit = np.sum(strategy_returns_net[strategy_returns_net > 0])
 gross_loss = abs(np.sum(strategy_returns_net[strategy_returns_net < 0]))
 profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf

# Number of transactions
 num_trades = np.sum(np.abs(position_changes))

# Average profit/loss
 avg_profit = np.mean(strategy_returns_net[strategy_returns_net > 0]) if np.any(strategy_returns_net > 0) else 0
 avg_loss = np.mean(strategy_returns_net[strategy_returns_net < 0]) if np.any(strategy_returns_net < 0) else 0

# Results
 metrics = {
 'accuracy': accuracy,
 'total_return': total_return,
 'annualized_return': annualized_return,
 'volatility': volatility,
 'sharpe_ratio': sharpe_ratio,
 'max_drawdown': max_drawdown,
 'calmar_ratio': calmar_ratio,
 'win_rate': win_rate,
 'profit_factor': profit_factor,
 'num_trades': num_trades,
 'avg_profit': avg_profit,
 'avg_loss': avg_loss,
 'strategy_returns': strategy_returns_net,
 'cumulative_returns': cumulative_returns,
 'drawdown': drawdown
 }

# Conclusion of results
(f'n===Trade metrics===)
 print(f"Accuracy: {accuracy:.4f}")
 print(f"Total Return: {total_return:.4f}")
 print(f"Annualized Return: {annualized_return:.4f}")
 print(f"Volatility: {volatility:.4f}")
 print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
 print(f"Max Drawdown: {max_drawdown:.4f}")
 print(f"Calmar Ratio: {calmar_ratio:.4f}")
 print(f"Win Rate: {win_rate:.4f}")
 print(f"Profit Factor: {profit_factor:.4f}")
 print(f"Number of Trades: {num_trades}")

 return metrics

def plot_trading_metrics(metrics, figsize=(15, 12)):
"Visualization of trade metrics."

 fig, axes = plt.subplots(2, 2, figsize=figsize)

# Cumulative returns
 cumulative_returns = metrics['cumulative_returns']
 axes[0, 0].plot(cumulative_returns, label='Strategy', linewidth=2)
 axes[0, 0].axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Break-even')
 axes[0, 0].set_title('Cumulative Returns')
 axes[0, 0].set_xlabel('Time')
 axes[0, 0].set_ylabel('Cumulative Return')
 axes[0, 0].legend()
 axes[0, 0].grid(True, alpha=0.3)

# Slide
 drawdown = metrics['drawdown']
 axes[0, 1].fill_between(range(len(drawdown)), drawdown, 0,
 color='red', alpha=0.3, label='Drawdown')
 axes[0, 1].plot(drawdown, color='red', linewidth=1)
 axes[0, 1].set_title('Drawdown')
 axes[0, 1].set_xlabel('Time')
 axes[0, 1].set_ylabel('Drawdown')
 axes[0, 1].legend()
 axes[0, 1].grid(True, alpha=0.3)

# Income distribution
 strategy_returns = metrics['strategy_returns']
 axes[1, 0].hist(strategy_returns, bins=50, alpha=0.7, edgecolor='black')
 axes[1, 0].axvline(x=0, color='red', linestyle='--', alpha=0.7)
 axes[1, 0].set_title('Return Distribution')
 axes[1, 0].set_xlabel('Return')
 axes[1, 0].set_ylabel('Frequency')
 axes[1, 0].grid(True, alpha=0.3)

# Basic metrics
 metric_names = ['Sharpe Ratio', 'Calmar Ratio', 'Win Rate', 'Profit Factor']
 metric_values = [
 metrics['sharpe_ratio'],
 metrics['calmar_ratio'],
 metrics['win_rate'],
 metrics['profit_factor']
 ]

# Limiting the value for visualization
 metric_values_limited = [min(val, 10) if val != np.inf else 10 for val in metric_values]

 bars = axes[1, 1].bar(metric_names, metric_values_limited,
 color=['skyblue', 'lightgreen', 'lightcoral', 'gold'], alpha=0.8)
 axes[1, 1].set_title('Key Trading Metrics')
 axes[1, 1].set_ylabel('Value')
 axes[1, 1].tick_params(axis='x', rotation=45)

# add values on column
 for bar, value in zip(bars, metric_values):
 height = bar.get_height()
 if value == np.inf:
 label = '∞'
 else:
 label = f'{value:.3f}'
 axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
 label, ha='center', va='bottom')

 axes[1, 1].grid(True, alpha=0.3)

 plt.tight_layout()
 plt.show()

def analyze_trading_performance(metrics):
"Analysis of trade performance."

"print("=== Trade performance analysis===)

# Assessment of the quality of strategy
 sharpe = metrics['sharpe_ratio']
 calmar = metrics['calmar_ratio']
 win_rate = metrics['win_rate']
 profit_factor = metrics['profit_factor']

Print(f'n Quality Assessment of Strategy:)

 # Sharpe Ratio
 if sharpe > 2:
(f) ♪ Great Sharpe Rato: {sharpe:.3f}")
 elif sharpe > 1:
(f) Good Sharpe Ratio: {sharpe:.3f})
 elif sharpe > 0.5:
(f) Moderate Sharpe Ratio: {sharpe:.3f})
 else:
(f) Bad Sharpe Ratio: {sharpe:.3f})

 # Calmar Ratio
 if calmar > 3:
(pint(f"\\\\calmarratio: {calmar:3f}})
 elif calmar > 1:
(f) Good Kalmar Rato: {calmar:.3f})
 elif calmar > 0.5:
(pint(f" ♪ Moderate Kalmar Rato: {calmar:.3f}})
 else:
(f) Bad Kalmar Ratio: {calmar:.3f})

 # Win Rate
 if win_rate > 0.6:
(f) High Win Rate: {win_rate:.3f})
 elif win_rate > 0.5:
♪ Good Win Rate: {win_rate:.3f} ♪
 elif win_rate > 0.4:
pint(f" ♪ Moderate Win Rate: {win_rate:.3f}")
 else:
(f) Low Win Rate: {win_rate:.3f})

 # Profit Factor
 if profit_factor > 2:
pprint(f" ♪ Excellent Profit Factor: {profit_factor:.3f}}
 elif profit_factor > 1.5:
pprint(f) ♪ Good Profit Factor: {profit_factor:.3f}}
 elif profit_factor > 1:
Print(f" ♪ Moderate Profit Factor: {profit_factor:.3f}})
 else:
(pint(f)(Bad Profit Factor: {profit_factor:.3f}})

# Overall assessment
prent(f"\ngeneral evaluation:")
 if sharpe > 1 and calmar > 1 and win_rate > 0.5 and profit_factor > 1.5:
("The Strategy shows excellent results")
 elif sharpe > 0.5 and calmar > 0.5 and win_rate > 0.4 and profit_factor > 1:
("The Strategy shows moderate results")
 else:
("The Strategy needs improvement")

# Example of use:
def example_trading_metrics_usage():
"Example using trade metrics."

# creative synthetic data
 np.random.seed(42)
 n_samples = 1000

# Income generation
returns = np.random.normal(0.001, 0.02, n_samples) # 0.1% average return, 2% volatility

# of true classes ( strategy)
 y_true = np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.4, 0.3])

# creative preferences (with some precision)
 y_pred = y_true.copy()
# Adding mistakes
 error_indices = np.random.choice(n_samples, size=int(n_samples * 0.3), replace=False)
 y_pred[error_indices] = np.random.choice([0, 1, 2], len(error_indices))

"print("===Example trade metric===)

# The calculation of the metric
 metrics = calculate_trading_metrics(y_true, y_pred, returns)

# Visualization
 plot_trading_metrics(metrics)

# Performance analysis
 analyze_trading_performance(metrics)

 return metrics

# Launch examples (upstream for testing)
# metrics = example_trading_metrics_usage()
```

## Practical example

**Theory:** The full process of training the trade model includes all stages: from producing data to estimating performance. This example demonstrates an integrated approach to the development of the ML model for financial data.

** Full process units:**
1. ** Data preparation:** Loading and pre-processing
2. ** Data Division:**Train/Validation/Test
3. ** Model learning:** Different algorithms
4. **validation:** Time Series CV
5. **Optification:** Hyperparameter tuning
6. **Anambling:** Model combination
7. ** Assessment:** Classification and trade statistics

** Practical implementation of the full process:**

What does this code do?
1. ** Full pipeline:** from data to ready model
2. ** Multiple algorithms:** Testing different approaches
3. **validation:** Uses the right methods for time series
4. **Optimization:** Finds the best parameters
5. **Anambling:** Combines the best models
6. ** Assessment: ** Analyses performance

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, classification_Report
import xgboost as xgb
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple, List
import warnings
warnings.filterwarnings('ignore')

def train_complete_trading_model(X, y, returns=None, test_size=0.2,
 validation_size=0.2, random_state=42):
 """
Full training of the trade model

 Args:
X: Signal matrix (samples, features)
y: Target variables (samples,)
Returns: Income of assets (samples,)
test_size: Percentage of test data
validation_size: Percentage of validation data
Random_state: Seed for reproducibility

 Returns:
dict: Training results and indicators
 """

"print("===The full training of the trade model===)
print(f" Data measurement: {X.scape[0]} samples, {X.scape[1]} topics")
(pint(f"Classes: {np.unique(y, return_counts=True)})

# 1. Data-sharing
print(f"\n1. Data-sharing...)

# First, let's separate the testy data
 X_temp, X_test, y_temp, y_test = train_test_split(
 X, y, test_size=test_size, random_state=random_state, stratify=y
 )

# Then share the rest of the data on transit and validation
 X_train, X_val, y_train, y_val = train_test_split(
 X_temp, y_temp, test_size=validation_size/(1-test_size),
 random_state=random_state, stratify=y_temp
 )

(pint(f" Train: {X_training.chape[0]} samples)
print(f"Validation: {X_val.chape[0]} samples")
(pint(f" Test: {X_test.ship[0]} samples)

#2 Training basic models
Print(f'\n2. Training basic models...)

 models = {}
 model_scores = {}

 # Random Forest
"Random Forest training..."
 rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=random_state)
 rf.fit(X_train, y_train)
 rf_score = rf.score(X_val, y_val)
 models['rf'] = rf
 model_scores['rf'] = rf_score
 print(f" Validation accuracy: {rf_score:.4f}")

 # XGBoost
"Learning XGBost..."
 xgb_model = xgb.XGBClassifier(n_estimators=100, max_depth=6, random_state=random_state, verbosity=0)
 xgb_model.fit(X_train, y_train)
 xgb_score = xgb_model.score(X_val, y_val)
 models['xgb'] = xgb_model
 model_scores['xgb'] = xgb_score
 print(f" Validation accuracy: {xgb_score:.4f}")

 # LightGBM
"LightGBM training..."
 lgb_model = lgb.LGBMClassifier(n_estimators=100, max_depth=6, random_state=random_state, verbose=-1)
 lgb_model.fit(X_train, y_train)
 lgb_score = lgb_model.score(X_val, y_val)
 models['lgb'] = lgb_model
 model_scores['lgb'] = lgb_score
 print(f" Validation accuracy: {lgb_score:.4f}")

 # 3. Time Series Cross Validation
 print(f"\n3. Time Series Cross Validation...")

# Uniting Train and validation for CV
 X_cv = np.vstack([X_train, X_val])
 y_cv = np.hstack([y_train, y_val])

# Choosing the best model for CV
 best_model_name = max(model_scores, key=model_scores.get)
 best_model = models[best_model_name]

({model_scores[best_model_name]:4f})

# We're doing TSCV
 tscv = TimeSeriesSplit(n_splits=5)
 cv_scores = []

 for fold, (train_idx, val_idx) in enumerate(tscv.split(X_cv)):
 X_fold_train, X_fold_val = X_cv[train_idx], X_cv[val_idx]
 y_fold_train, y_fold_val = y_cv[train_idx], y_cv[val_idx]

# Creating a copy of the model
 fold_model = type(best_model)(**best_model.get_params())
 fold_model.fit(X_fold_train, y_fold_train)

 fold_score = fold_model.score(X_fold_val, y_fold_val)
 cv_scores.append(fold_score)

 print(f" Fold {fold+1}: {fold_score:.4f}")

 cv_mean = np.mean(cv_scores)
 cv_std = np.std(cv_scores)
 print(f" CV Mean: {cv_mean:.4f} ± {cv_std:.4f}")

# 4. Create ensemble
(f'n4...)

# Choosing top three models
 top_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)[:3]

 ensemble_models = []
 for name, score in top_models:
 ensemble_models.append((name, models[name]))
 print(f" {name}: {score:.4f}")

 # Creating Voting Classifier
 ensemble = VotingClassifier(
 estimators=ensemble_models,
 voting='soft',
 n_jobs=-1
 )

# Ensemble education
 ensemble.fit(X_train, y_train)
 ensemble_score = ensemble.score(X_val, y_val)
 print(f" Ensemble validation accuracy: {ensemble_score:.4f}")

#5: Evaluation on test data
pprint(f"\n5. Evaluation on test data...)

# The prediction of all models
 test_predictions = {}
 test_scores = {}

 for name, model in models.items():
 pred = model.predict(X_test)
 score = accuracy_score(y_test, pred)
 test_predictions[name] = pred
 test_scores[name] = score
 print(f" {name}: {score:.4f}")

# Ansemble
 ensemble_pred = ensemble.predict(X_test)
 ensemble_score = accuracy_score(y_test, ensemble_pred)
 test_predictions['ensemble'] = ensemble_pred
 test_scores['ensemble'] = ensemble_score
 print(f" Ensemble: {ensemble_score:.4f}")

♪ 6. Trade metrics (if available)
 trading_metrics = None
 if returns is not None:
pprint(f"\n6. Calculation of trade metric...)

# Use only test data for trade metrics
 test_returns = returns[-len(y_test):]

# Computing metrics for an ensemble
 trading_metrics = calculate_trading_metrics(
 y_test, ensemble_pred, test_returns
 )

# 7. Results
== Final results=======================Prent(f)=======The total results====)
print(f"Best individual model: {max(test_scores, key=test_scores.get)})
"Best individual score: {max(test_scores.valutes():4f}")
 print(f"Ensemble score: {ensemble_score:.4f}")
 print(f"CV score: {cv_mean:.4f} ± {cv_std:.4f}")

 if trading_metrics:
 print(f"Sharpe Ratio: {trading_metrics['sharpe_ratio']:.4f}")
 print(f"Max Drawdown: {trading_metrics['max_drawdown']:.4f}")
 print(f"Win Rate: {trading_metrics['win_rate']:.4f}")

# Detailed Report
 print(f"\n=== Classification Report (Ensemble) ===")
 print(classification_Report(y_test, ensemble_pred))

# Results for return
 results = {
 'models': models,
 'ensemble': ensemble,
 'model_scores': model_scores,
 'test_scores': test_scores,
 'cv_scores': cv_scores,
 'cv_mean': cv_mean,
 'cv_std': cv_std,
 'test_predictions': test_predictions,
 'trading_metrics': trading_metrics,
 'best_model': best_model_name,
 'ensemble_score': ensemble_score
 }

 return results

def plot_complete_results(results, figsize=(15, 12)):
"Visualization of Full Learning Results""

 fig, axes = plt.subplots(2, 2, figsize=figsize)

# Comparrison of models
 models = List(results['test_scores'].keys())
 scores = List(results['test_scores'].values())

 bars = axes[0, 0].bar(models, scores, color='skyblue', alpha=0.8)
 axes[0, 0].set_title('Model Performance Comparison')
 axes[0, 0].set_ylabel('Accuracy')
 axes[0, 0].set_ylim(0, 1)
 axes[0, 0].tick_params(axis='x', rotation=45)

# add values on column
 for bar, score in zip(bars, scores):
 height = bar.get_height()
 axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
 f'{score:.3f}', ha='center', va='bottom')

 axes[0, 0].grid(True, alpha=0.3)

# CV results
 cv_scores = results['cv_scores']
 axes[0, 1].plot(range(1, len(cv_scores)+1), cv_scores, 'o-', linewidth=2, markersize=8)
 axes[0, 1].axhline(y=results['cv_mean'], color='red', linestyle='--',
 label=f'Mean: {results["cv_mean"]:.3f}')
 axes[0, 1].set_title('Cross-Validation Scores')
 axes[0, 1].set_xlabel('Fold')
 axes[0, 1].set_ylabel('Accuracy')
 axes[0, 1].legend()
 axes[0, 1].grid(True, alpha=0.3)

# Trade statistics (if available)
 if results['trading_metrics']:
 trading_metrics = results['trading_metrics']

# Cumulative returns
 cumulative_returns = trading_metrics['cumulative_returns']
 axes[1, 0].plot(cumulative_returns, linewidth=2)
 axes[1, 0].axhline(y=1, color='black', linestyle='--', alpha=0.5)
 axes[1, 0].set_title('Cumulative Returns')
 axes[1, 0].set_xlabel('Time')
 axes[1, 0].set_ylabel('Cumulative Return')
 axes[1, 0].grid(True, alpha=0.3)

# Main trade metrics
 metric_names = ['Sharpe', 'Calmar', 'Win Rate', 'Profit Factor']
 metric_values = [
 trading_metrics['sharpe_ratio'],
 trading_metrics['calmar_ratio'],
 trading_metrics['win_rate'],
 trading_metrics['profit_factor']
 ]

# Limiting the value for visualization
 metric_values_limited = [min(val, 10) if val != np.inf else 10 for val in metric_values]

 bars = axes[1, 1].bar(metric_names, metric_values_limited,
 color=['skyblue', 'lightgreen', 'lightcoral', 'gold'], alpha=0.8)
 axes[1, 1].set_title('Trading Metrics')
 axes[1, 1].set_ylabel('Value')
 axes[1, 1].tick_params(axis='x', rotation=45)

# add values on column
 for bar, value in zip(bars, metric_values):
 height = bar.get_height()
 if value == np.inf:
 label = '∞'
 else:
 label = f'{value:.3f}'
 axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
 label, ha='center', va='bottom')

 axes[1, 1].grid(True, alpha=0.3)
 else:
 axes[1, 0].text(0.5, 0.5, 'Trading metrics\nnot available',
 ha='center', va='center', transform=axes[1, 0].transAxes)
 axes[1, 0].set_title('Trading Metrics')

 axes[1, 1].text(0.5, 0.5, 'Trading metrics\nnot available',
 ha='center', va='center', transform=axes[1, 1].transAxes)
 axes[1, 1].set_title('Trading Metrics')

 plt.tight_layout()
 plt.show()

# Example of use:
def example_complete_training_usage():
"Example full trade model learning."

# creative synthetic data
 np.random.seed(42)
 n_samples, n_features = 2000, 20

# Signal generation
 X = np.random.randn(n_samples, n_features)

# the target variable
 y = np.zeros(n_samples)
 for i in range(n_samples):
 if X[i, 0] > 0.5 and X[i, 1] < -0.3:
 y[i] = 1
 elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
 y[i] = 2
 else:
 y[i] = 0

# Income generation
 returns = np.random.normal(0.001, 0.02, n_samples)

===Example full training of the trade model===)

# Full-time education
 results = train_complete_trading_model(X, y, returns)

# Visualization of results
 plot_complete_results(results)

 return results

# Launch examples (upstream for testing)
# results = example_complete_training_usage()
```

## Next steps

**Theory:** After successful training, the model comes in a validation and testing phase. Next steps are critical to ensuring the reliability of the trade strategy.

** Why every step is important:**

1. **Bexting** - check model on historical data
- **Goal:** Make sure that the Workinget model is on the data she's seen.
 - **methods:** Walk-forward Analysis, Monte Carlo simulation
- **Criteria:** Stability of results, lack of retraining

2. ** evaluation on out-of-sample data** - Testing on new data
- **Goal:** Check model generality
- **Period:** Usually 20-30% from total data volume
- **Criteria:**comparison with benchmarking, statistical significance

3. **Optimization of parameters** - Thin configration model
- **Goal:** Maximize performance while minimizing risk
 - **methods:** Grid search, Bayesian optimization, Genetic algorithms
- **Criteria:** Resistance to parameter changes

4. **Monitoring performance** - Real-time tracking
- **Goal:** Identify model degradation in a timely manner
 - **metrics:** Accuracy, Sharpe ratio, Drawdown, Win rate
- ** Actions:** Retraining, stoppage, parameter adjustments

** Practical recommendations:**

- ** Start with backup** is the basis for all future decisions
- **Use Walk-forward analysis** - it's the most realistic for financial data
- ** Test on different market conditions** - bull/bear market, volatility
- ** Check the stability of the results** - avoid retraining
- ** Document all experiments** - It'll help in future iterations.

**Structure of the following steps:**

```
Training of the model ♪ Becketting ♪ promotion ♪ Optimizing ♪ Monitoring ♪
 ↓ ↓ ↓ ↓ ↓
Accuracy Historical Out-of-parameters
on Train performance time model time
```

After training the model, go to:
- **[06_backtesting.md](06_backtesting.md)** - Trade Strategy Becketting
- **[07_validation.md](07_validation.md)** -validation of models
- **[08_optimization.md](08_optimization.md)** - Optimization of parameters
- **[09_Monitoring.md](09_Monitoring.md)** - Monitoring performance
- **[07_walk_forward_Analisis.md](07_walk_forward_Anallysis.md)** - Walk-forward analysis

## Key findings

**Theory:** Training in ML models for financial data is specific and requires a special approach. Understanding these principles is critical for successful trade strategies.

** Basic principles of successful learning:**

###1. ** Ansambal methhods outnumber single models**
- Why:** Financial data are complex and unstable
- ** Benefits:** Reduced retraining, increased stability
- ** Recommendations:** Use Voting, Stacking, Bagging
- ** Practice:** Combine 3-5 different algorithms

###2. ** Time series require special validation**
- ** Problem: ** Standard CV disrupts the time structure
- ** Decision:** Time Series CV, Walk-Forward Planning
- **Criteria:** Time sequence, absence of data release
- **Practice:** Always Use temporary Methods validation

### 3. **Optimization of hyperparameters is critical**
- **Goal:** Find an optimum balance of bias-variance
- **methods:** Grid Search, Random Search, Bayesian optimization
- **Criteria:** Stability, performance, speed
- ** Practice:** Start with simple methods, move on to complicated methods

###4. ** Trading metrics are more important than classification**
- ** Cause:** Accuracy no reflects real profitability
- ** Key metrics:** Sharpe Ratio, Max Drawdown, Win Rate
- ** Analise:** Consider metrics in complex
- ** Practice:** Optimize on trade metrics and not on accuracy

###5. ** The quality of data determines success**
- **Influence:** Bad data = bad model
- ** Demands:** Clean, normalization, feature engineering
- **check:** Analysis of distributions, correlations, emissions
- ** Practice:** Investing time in data production

### 6. **Regularization prevents retraining**
- ** Problem:** Financial data tend to be re-trained
- **methods:** L1/L2 regularization, dropout, early stopping
- **Balance:** Model complexity vs. synthesis capacity
- ** Practice:** Start with simple models, make things more difficult

### 7. **Monitoring and adaptation necessary**
- **Reality:** Markets change constantly
- ** Actions:** Regular retraining, Monitoring metric
- **Criteria:** Degradation performance, market change
♪ Practice: ♪ Automation of the process ♪

** Practical recommendations:**

1. ** Start with simple** - Random Forest, then move on to complex
2. **Use correct validation** - Time Series CV for time series
3. **Optimize on trade metrics** - not on accuracy
4. ** Test on different periods** - bull/bear market
5. **Document all experiments** - this will help in the future
6. **Planize Monitoring** - Model to be supported

**Typical errors:**

Use of standard CV for time series
- Optimization only on accuracy
- Ignoring trade metrics
- Absence of Monitoring performance
- Retraining on historical data

** Successful strategy:**

- ♪ The correct walliation (Time Series CV)
- Ansemble methhods
- Optimization of trade metrics
- Regular Monitoring
- Adaptation to market changes

** Conclusion:**

Training in ML models for finance is an iterative process that requires a thorough understanding of both the machining and financial markets. Success comes to those who correctly validate models, use appropriate metrics, and constantly adapt to market changes.

---

It's important:**no chasing for high accuracy - more important is stable profitability!
