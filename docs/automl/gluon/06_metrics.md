# metrics and quality assessment in AutoML Gluon

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Who metrics is critical

Why is 80% of ML projects failing because of the wrong choice of metrics?

♪ ♪ What's going on without the right metric?
The model looks good, but Working's not good.
- ** Wrong decisions**: Choose a bad model instead of a good one.
- ** Loss of time**: Spend months on inefficient approaches
- ** Business failures**: No model solves real problems

♪ ♪ What gives the right choice of metric?
- ** Exact assessment**: You know exactly the quality of the model.
- **The right choice**: Choose the best model for the task
- ** Rapid iteration**: Quickly find problems and fix them.
- ** Business success**: The model really helps business.

## Introduction in metrics

<img src="images/optimized/metrics_comparison.png" alt="comparison metric" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 1: Comparative metric for classification and regression*

<img src="images/optimized/metrics_Detained.png" alt="Detail visualization of metric" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 2: Detailed visualization of metrics - ROC Curve, Precion-Recall, Conference Matrix, Accuracy vs Threshold, F1 Score vs Threshold*

**Why metrics is the language of machine lightning?** Because they translate complex algorithms in understandable numbers. It's like an interpreter between technical details and business results.

metrics in AutoML Gloon are used for:
- ** Model quality assessments**: Understanding how good the model is
- ** Comparisons of different algorithms**: Choice of a better algorithm for a task
- ** Selection of the best model**: Automatic selection of the best model
- **Monitoringa performance**: Quality tracking in sales

## metrics for classification

<img src="images/optimized/robustness_Analesis.png" alt="metrics classification" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Figure 3: metrics for classification tasks and their interpretation*

**Why does classification require special metrics?** Because not only the correct answers but also the types of errors are important here. False responses and omissions have different prices.

###\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\######\\\\\\\\\\\\\\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\##########\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

Why is it important to understand the types of errors?

- **True Positive (TP)**: Correctly predicted positive cases
- **True Negative (TN)**: Correctly predicted negative cases
- **False Positive (FP)**: False Reactions (I-type errors)
- **False Negative (FN)**: Mistakes (Speed II)
- **Precision**: Accuracy is the proportion of the positives predicted
- **Recall**: Fullness - share of all positives
- **F1-Score**: Harmonic average precision and recall

### Basic metrics

#### Accuracy
Because it's intuitively understandable, it's just a percentage of the right answers.

When does Accuracy insane?
- Unbalanced (99 per cent of the same class)
- Different importance of errors (medical diagnosis)
- With little data

```python
# Percentage of correct preferences
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_true, y_pred)
print(f"Accuracy: {accuracy:.4f}")
```

** Detailed describe parameters accuracy_score:**

**function accuracy_score:**
- ** Designation**: Calculation of the accuracy of the classification (percentage of correct preferences)
- **parameters**:
- **'y_tree'**: True class labels
-** Type**: Array-lake
- **describe**: Massive of true class tags
 - **examples**: [0, 1, 1, 0, 1], ['cat', 'dog', 'cat']
- **'y_pred'**: Presumed class labels
-** Type**: Array-lake
- **describe**: Mass of predicted class tags
 - **examples**: [0, 1, 0, 0, 1], ['cat', 'dog', 'dog']
- **'normalyze'**: Normalization of result (on default True)
-**Teep**: bool
- **describe**:True - returns the share of correct preferences, False - quantity
** `sample_white'**: Weights for examples (on default None)
-** Type**: Array-lake or None
- **describe**: Weights for each example in calculating accuracy
**Return value**: float - accuracy of classification (0.0 - 1.0)
- ** Use**:
** Rapid evaluation**: Initial model quality assessment
- **comparison models**: comparison different algorithms
- **Monitoring**: Quality tracking during training

# Why can Accuracy be deceiving? #
- The model can just predict the majority class.
- not shows what errors make the model
-not takes into account the importance of different types of errors

#### ♪ Detailed descriebe parameters of classification metric

**Methric Accuracy:**
- ** Which means**: Percentage of correct productions from total
- **Formoule**: `(TP + TN) / (TP + TN + FP + FN) `
- ** Value range**: `[0,1]' (0% - 100%)
- ** When to use**:
** Balanced data**: When classes are approximately equal on number
- ** Simple tasks**: When all mistakes are equally important
- ** Rapid evaluation**: for initial quality assessment
- ** When not used**:
- ** Unbalanced data**: When one class is much larger
- ** Critical errors**: When different types of errors are of different importance
- ** Medical diagnosis**: When false denials are more dangerous than false diarrhea
- ** Practical examples**:
- ** Good accuracy**: `> 0.9' (90 per cent+)
- ** Acceptable accuracy**: `0.8-0.9' (80-90 per cent)
- ** Bad accuracy**: `< 0.8' (< 80 per cent)
- ** Limitations**:
**not shows the types of errors:** not distinguish between false positions and denials
- **Material class**: May be high when predicting only one class
- **not takes into account the importance**: All errors are considered equally important

#### Precion (Total)
Because it shows how much you can trust the positive predictions of the model.

When is Precion especially important?
- Medical diagnosis (fake diagnosis is dangerous)
- Detection of fraud (falsification of roads)
- Spam filters (important letters not should be in spam)

```python
# Proportion of positive cases correctly predicted
from sklearn.metrics import precision_score

precision = precision_score(y_true, y_pred, average='binary')
print(f"Precision: {precision:.4f}")

# for multi-class classification
== sync, corrected by elderman == @elder_man
===Precution_micro===Précion_score(y_tree, y_pred, average='micro') #Global average
```

**/ Detailed descrie parameters precision_score:**

**function precision_score:**
- ** Designation**: Calculation of accuracy (precision) for classification
- **parameters**:
- **'y_tree'**: True class labels
-** Type**: Array-lake
- **describe**: Massive of true class tags
 - **examples**: [0, 1, 1, 0, 1], ['cat', 'dog', 'cat']
- **'y_pred'**: Presumed class labels
-** Type**: Array-lake
- **describe**: Mass of predicted class tags
 - **examples**: [0, 1, 0, 0, 1], ['cat', 'dog', 'dog']
- ** `overrange'**: Averaging type (on default 'binary')
- **Typ**: str or None
- **describe**: Method of averaging for multiclass classification
- **Options**: 'binary', 'micro', 'macro', 'weighted', 'samples', None
** `sample_white'**: Weights for examples (on default None)
-** Type**: Array-lake or None
- **describe**: Weights for each example in the calculation of the definition
- ** `Zero_diviction'**: Value when dividing on zero (on default 'warn')
- ** Type**: str or float
- **describe**: What to return when the definition not is specified
- **Options**: 'warn', 0, 1
- **Return value**: float or array - definition for each class
- ** Averages**:
- **'binary'**: for binary classification (on default)
- **'micro'**: Global average (takes into account the number of examples)
- **'macro'**: Average arithmetical on classes (equal weights)
- **'weated'**: Average weighted on number of examples
- **'samples'**: Precion for each example separately
** `Nene'**: Precion for each class separately
- ** Use**:
- ** Critical false position**: When the road has been broken
- **Medical diagnosis**: When false diagnosis is dangerous
- ** Detection of fraud**: When false accusations are made on the road

# Why do you need different types of averaging? #
- **macro**: Each class has equal weight (good for unbalanced data)
- **micro**: Considers the number of examples in each class (good for balanced data)

**Methic Precion:**
- Which means**: Proportion of correctly predicted positive cases from all predicted positive
- **Formoule**: `TP / (TP + FP) `
- ** Value range**: `[0,1]' (0% - 100%)
- ** When to use**:
- ** Critical false position**: When the road has been broken
- **Medical diagnosis**: When false diagnosis is dangerous
- ** Detection of fraud**: When false accusations are made on the road
- **Spam filter**: When important letters not should be in spam
- ** When not used**:
- ** Critical false denials**: When omissions are more dangerous than false operations
- ** Unbalanced data**: When a positive class is very rare
- ** Practical examples**:
- ** Excellent accuracy**: `> 0.95' (95 per cent+)
- ** Good accuracy**: `0.8-0.95' (80-95 per cent)
- ** Acceptable accuracy**: `0.6-0.8' (60-80 per cent)
- ** Bad accuracy**: `< 0.6' (< 60%)
- **parameter `average`**:
- **'binary'**: for binary classification (on default)
- **'macro'**: Average arithmetical on classes (equal weights)
- **'micro'**: Global average (weight on number of examples)
- **'weated'**: Average weighted on number of examples
- ** Averaging type selection**:
- ** Unbalanced data**: Use `'macro''
- ** Balanced data**: Use `'micro''
- **All classes are important**: Use `'macro''
- **Amount of total value**: Use `'micro''

### Recall
```python
# Proportion of positive cases that were correctly predicted
from sklearn.metrics import recall_score

recall = recall_score(y_true, y_pred, average='binary')
print(f"Recall: {recall:.4f}")

# for multi-class classification
recall_macro = recall_score(y_true, y_pred, average='macro')
recall_micro = recall_score(y_true, y_pred, average='micro')
```

** Detailed describe parameters recall_score:**

**function recall_score:**
- ** Designation**: Calculation of completeness for classification
- **parameters**:
- **'y_tree'**: True class labels
-** Type**: Array-lake
- **describe**: Massive of true class tags
 - **examples**: [0, 1, 1, 0, 1], ['cat', 'dog', 'cat']
- **'y_pred'**: Presumed class labels
-** Type**: Array-lake
- **describe**: Mass of predicted class tags
 - **examples**: [0, 1, 0, 0, 1], ['cat', 'dog', 'dog']
- ** `overrange'**: Averaging type (on default 'binary')
- **Typ**: str or None
- **describe**: Method of averaging for multiclass classification
- **Options**: 'binary', 'micro', 'macro', 'weighted', 'samples', None
** `sample_white'**: Weights for examples (on default None)
-** Type**: Array-lake or None
- **describe**: Weights for each example when calculating recall
- ** `Zero_diviction'**: Value when dividing on zero (on default 'warn')
- ** Type**: str or float
- **describe**: What to return when recall not specified
- **Options**: 'warn', 0, 1
- **Return value**: float or array - recall for each class
- ** Averages**:
- **'binary'**: for binary classification (on default)
- **'micro'**: Global average (takes into account the number of examples)
- **'macro'**: Average arithmetical on classes (equal weights)
- **'weated'**: Average weighted on number of examples
- **'samples'**: Recall for each example separately
- ** `Nene'**: Recall for each class separately
- ** Use**:
- ** Critical false denials**: When omissions are more dangerous than false operations
- **Medical diagnosis**: When the absence of a disease is more dangerous than a false diagnosis
- ** Fraud detection**: When fraud is more expensive than false accusations

**Metric Recall:**
- ** Meaning**: Percentage of positive cases that were correctly predicted
- **Formoule**: `TP / (TP + FN) `
- ** Value range**: `[0,1]' (0% - 100%)
- ** When to use**:
- ** Critical false denials**: When omissions are more dangerous than false operations
- **Medical diagnosis**: When the absence of a disease is more dangerous than a false diagnosis
- ** Fraud detection**: When fraud is more expensive than false accusations
- ** Search for information**: When it's important to find all relevant documents
- ** When not used**:
- ** Critical false position**: When the road has been broken
- ** Unbalanced data**: When a positive class is very rare
- ** Practical examples**:
- ** Excellent completeness**: `> 0.95' (95 per cent+)
- **Good completeness**: `0.8-0.95' (80-95 per cent)
** Acceptable completeness**: `0.6-0.8' (60-80 per cent)
- ** Bad completeness**: `< 0.6' (< 60%)
- **parameter `average`**:
- **'binary'**: for binary classification (on default)
- **'macro'**: Average arithmetical on classes (equal weights)
- **'micro'**: Global average (weight on number of examples)
- **'weated'**: Average weighted on number of examples
- ** Averaging type selection**:
- ** Unbalanced data**: Use `'macro''
- ** Balanced data**: Use `'micro''
- **All classes are important**: Use `'macro''
- **Amount of total value**: Use `'micro''

#### F1-Score
```python
# Harmonic average precinct and recall
from sklearn.metrics import f1_score

f1 = f1_score(y_true, y_pred, average='binary')
print(f"F1-Score: {f1:.4f}")

# for multi-class classification
f1_macro = f1_score(y_true, y_pred, average='macro')
f1_micro = f1_score(y_true, y_pred, average='micro')
```

**/ Detailed descrie parameters f1_score:**

**function f1_score:**
- ** Designation**: Calculation of F1-measures (harmonic average precision and recall)
- **parameters**:
- **'y_tree'**: True class labels
-** Type**: Array-lake
- **describe**: Massive of true class tags
 - **examples**: [0, 1, 1, 0, 1], ['cat', 'dog', 'cat']
- **'y_pred'**: Presumed class labels
-** Type**: Array-lake
- **describe**: Mass of predicted class tags
 - **examples**: [0, 1, 0, 0, 1], ['cat', 'dog', 'dog']
- ** `overrange'**: Averaging type (on default 'binary')
- **Typ**: str or None
- **describe**: Method of averaging for multiclass classification
- **Options**: 'binary', 'micro', 'macro', 'weighted', 'samples', None
** `sample_white'**: Weights for examples (on default None)
-** Type**: Array-lake or None
- **describe**: Weights for each example when calculating F1-score
- ** `Zero_diviction'**: Value when dividing on zero (on default 'warn')
- ** Type**: str or float
- **describe**: What to return when F1-score not specified
- **Options**: 'warn', 0, 1
- **Return value**: float or array - F1-score for each class
- ** Averages**:
- **'binary'**: for binary classification (on default)
- **'micro'**: Global average (takes into account the number of examples)
- **'macro'**: Average arithmetical on classes (equal weights)
- **'weated'**: Average weighted on number of examples
- **'samples'**: F1-score for each example separately
** `Nene'**: F1-score for each class separately
- ** Use**:
- ** Budget preparation and review**: When both accuracy and completeness are important
- ** Unbalanced data**: F1-score good Workinget with unbalanced data
- **comparison models**: Good metrics for comparing different algorithms

### Moved metrics

#### ROC AUC
```python
# Area under ROC curve
from sklearn.metrics import roc_auc_score

# for binary classification
roc_auc = roc_auc_score(y_true, y_prob)
print(f"ROC AUC: {roc_auc:.4f}")

# for multi-class classification
roc_auc_ovo = roc_auc_score(y_true, y_prob, multi_class='ovo')
roc_auc_ovr = roc_auc_score(y_true, y_prob, multi_class='ovr')
```

** Detailed describe parameters roc_auc_score:**

**function roc_auc_score:**
- ** Designation**: Calculation of the area under the ROC curve (AUC)
- **parameters**:
- **'y_tree'**: True class labels
-** Type**: Array-lake
- **describe**: Massive of true class tags (0 and 1 for binary classification)
- **examples**: [0, 1, 1, 0, 1], [0, 1, 2, 0, 1] (multi-class)
**'y_score'**: Projected probabilities or estimates
-** Type**: Array-lake
- **describe**: Massive probabilities of the positive class or estimates
 - **examples**: [0.1, 0.9, 0.8, 0.2, 0.7]
- **'overage'**: Type of averaging for multiclass classification (on default 'macro')
- **Typ**: str or None
- **describe**: Mode of averaging AUC for multiclass classification
- **Options**: 'Macro', 'micro', 'weighted', 'samples', None
- ** `multi_class'**: Strategy for multiclass classification (on default 'raise')
- **Typ**: str
- **describe**: AUC computation strategy for multiclass classification
- **Options**: 'raise', 'ovr', 'ovo'
** `sample_white'**: Weights for examples (on default None)
-** Type**: Array-lake or None
- **describe**: Weights for each example when calculating AUC
- **'max_fpr'**: Maximum FPR for partial AUC (on default Non)
- ** Type**: float or None
- **describe**: Maximum False Positative Rate for the calculation of partial AUC
**Return value**: float - AUC (0.0 - 1.0)
- ** Multi-class classification strategies**:
- **'ovr' (One-vs-Rest)**: Each class versus the others
- ** Benefits**: Compute faster
- ** Disadvantages**: Could be inaccurate for unbalanced data
- ** `'oovo'' (One-vs-One)**: Each class against each other
- ** Benefits**: More accurate assessment for unbalanced data
- ** Disadvantages**: Calculated more expensive
- ** Use**:
**binary classification**: Quality assessment of grade separation
- ** Unbalanced data**: ROC AUC is resistant to class imbalance
- **comparison models**: Good metrics for comparing different algorithms

**/ Detailed describe of ROC AUC parameters:**

**ROC AUC Meter:**
- Which means**: Area under the ROC curve
- **Formoule**: ``TPR d(FPR)'' where TPR = TP/(TP+FN), FPR = FP/(FP+TN)
- ** Value range**: `[0,1]' (0% - 100%)
- ** When to use**:
**binary classification**: When to assess the quality of grade segregation
- ** Unbalanced data**: ROC AUC is resistant to class imbalance
- **comparison models**: Good metrics for comparing different algorithms
- **Search selection**: Helps find the optimum classification threshold
- ** When not used**:
- ** Multiclass Classification**: It is difficult to interpret
- ** Critical false statements**:not takes into account the importance of different errors
- ** Practical examples**:
- ** Excellent quality**: `> 0.9' (90 per cent+)
- ** Good quality**: `0.8-0.9' (80-90 per cent)
** Acceptable quality**: `0.7-0.8' (70-80 per cent)
- ** Bad quality**: `< 0.7' (< 70 per cent)
- **parameter `multi_class`**:
- ** `'oovo'' (One-vs-One)**: Each class is compared with each other
- ** Benefits**: More accurate assessment for unbalanced data
- ** Disadvantages**: Calculated more expensive for a large number of classes
- ** When to use**: When classes are unbalanced
- **'ovr' (One-vs-Rest)**: Each class is compared with the others
- ** Benefits**: Compute faster
- ** Disadvantages**: Could be inaccurate for unbalanced data
- ** When to use**: When classes are balanced
- **parameter `overage'** (for multiclass classification):
- **'macro'**: Average arithmetical on classes (equal weights)
- **'micro'**: Global average (weight on number of examples)
- **'weated'**: Average weighted on number of examples
- ** Interpretation**:
- **0.5**: Random Predation (not better than random)
**0.7-0.8**: Acceptable quality
- **0.8-0.9**: Good quality
- **0.9+**: Excellent quality
**1.0**: Perfect division of classes

#### PR AUC
```python
# Area under Precion-Recall curve
from sklearn.metrics import average_precision_score

pr_auc = average_precision_score(y_true, y_prob)
print(f"PR AUC: {pr_auc:.4f}")
```

** Detailed describe of PR AUC parameters:**

**PR AUC Meter:**
- Which means**: Area under Precion-Recall curve
- **Formoula**: `\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\} where} where} where} where} where} where} where/} where/} where/} where} where/} where/} where/} where/} where/} where/} where/} where/}==============================================================================================================********************************************************************************
- ** Value range**: `[0,1]' (0% - 100%)
- ** When to use**:
- ** Unbalanced data**: PR AUC is better than ROC AUC for rare classes
- ** Critical false position**: When the road has been broken
- **Medical diagnostics**: When accuracy of positive preferences is important
- ** Detection of fraud**: When false accusations are made on the road
- ** When not used**:
- ** Balanced data**: ROC AUC may be more informative
- ** Critical false denials**: When omissions are more dangerous than false operations
- ** Practical examples**:
- ** Excellent quality**: `> 0.8' (80 per cent+)
- ** Good quality**: `0.6-0.8' (60-80 per cent)
** Acceptable quality**: `0.4-0.6' (40-60 per cent)
- ** Bad quality**: `< 0.4' (< 40 per cent)
- ** Benefits before ROC AUC**:
- ** Unbalanced data**: More informative for rare classes
- ** Practical interpretation**: directly related with preparation and review
- ** Sensitivity to imbalance**: Better reflects quality on rare classes
- ** Disadvantages**:
- **Complicity of interpretation**: Less intuitive than ROC AUC
- **dependency from the threshold**: May be unstable when changing the threshold
- ** Interpretation**:
- **0.0**: Model not better than random
**0.3-0.5**: Acceptable quality
- **0.5-0.7**: Good quality
- **0.7+**: Excellent quality
- **1.0**: Perfect quality

#### Log Loss
```python
# Logarithmic function loss
from sklearn.metrics import log_loss

log_loss_score = log_loss(y_true, y_prob)
print(f"Log Loss: {log_loss_score:.4f}")
```

**Detail describe parameters Log Loss:**

**Metrick Log Loss:**
- ** Meaning**: Logarithmic function of losses (Logsstic function of losses)
- **Formoula**: `-1/N* \[y*log(p) + (1-y)*log(1-p)] / where p is the probability of a positive class
- ** Value range**: `[0, +] &apos; (0 = ideal Pradition, +\] - worst)
- ** When to use**:
- ** Probability Assessment**: When not only predictions but also their confidence matter
- ** Unbalanced data**: Log Loss is sensitive to probability quality
- **comparison models**: Good metric for probabilities quality comparison
- ** Model calibration**: Helps to assess how well the probability is calibrated
- ** When not used**:
- ** Only predictions**: When only classes are important and no probability are important
- **Very unbalanced data**: May be unstable
- ** Practical examples**:
- ** Excellent quality**: `< 0.1' (very low error)
- ** Good quality**: `0.1-0.3' (low error)
- ** Acceptable quality**: `0.3-0.5' (moderate error)
- ** Bad quality**: `> 0.5' (high error)
- **parameter `eps'** (on default 1e-15):
- ** Designation**: Minimum value for probabilities (failure log(0))
- ** Recommended values**: `1e-15' to `1e-7'
- **Effluence**: Too important can distort results
- **parameter `normalyze'** (on default True):
- **True**: Normalized error (done on number of examples)
- **False**: Total error
- **parameter `sample_weight`**:
- ** Designation**: Weights for each example
- ** Use**: For unbalanced or important examples
- ** Interpretation**:
- **0.0**: Perfect Predation.
- **0.1-0.3**: Very good quality
- **0.3-0.5**: Good quality
**0.5-0.7**: Acceptable quality
- **> 0.7**: Poor quality
- **+**: Worst possible implementation

#### Balanced Accuracy
```python
# Balanced accuracy for unbalanced data
from sklearn.metrics import balanced_accuracy_score

balanced_acc = balanced_accuracy_score(y_true, y_pred)
print(f"Balanced Accuracy: {balanced_acc:.4f}")
```

**/ Detailed describe parameters of Balanced Accuracy:**

**Balanced Accuracy Meter:**
- ** Meaning**: Mean arithmetic sensitivity (recall) for each class
- **Formoula**: `(Sensitity + Specification) / 2' where Sensity = TP/(TP+FN), Specification = TN/(TN+FP)
- ** Value range**: `[0,1]' (0% - 100%)
- ** When to use**:
- ** Unbalanced data**: When one class is much larger than the other
- **Medical diagnostics**: When false depositions and false denials are important
- ** Fraud detection**: When both omissions and false reactions are important
- **comparison of models**: More equitable assessment for unbalanced data
- ** When not used**:
- ** Balanced data**: Normal accuracy may be more informative
- ** Critical errors**: When different types of errors are of different importance
- ** Practical examples**:
- ** Excellent quality**: `> 0.9' (90 per cent+)
- ** Good quality**: `0.8-0.9' (80-90 per cent)
** Acceptable quality**: `0.7-0.8' (70-80 per cent)
- ** Bad quality**: `< 0.7' (< 70 per cent)
- ** Benefits prior to normal Accuracy**:
- **justice**: Each class has equal weight
- ** Resistance to imbalance**: not dependent on from class distribution
- ** Interpretation**: Shows average quality on classes
- ** Disadvantages**:
**not takes into account the importance**: All classes are considered equally important
- ** May be deceiving**: The high not guarantees good quality
- ** Interpretation**:
- **0.5**: Random Predation (not better than random)
**0.7-0.8**: Acceptable quality
- **0.8-0.9**: Good quality
- **0.9+**: Excellent quality
- **1.0**: Perfect quality

### metrics for unbalanced data

#### Matthews Correlation Coefficient (MCC)
```python
from sklearn.metrics import matthews_corrcoef

mcc = matthews_corrcoef(y_true, y_pred)
print(f"MCC: {mcc:.4f}")
```

**/ Detailed descrie parameters MCC:**

**Metrick Matthews Correlation Associate (MCC):**
- ** Meaning**: Correlation between true and foretold classes
- **Formoula**: `(TP*TN - FP*FN) / sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN) `
- ** Range**: `[-1, 1]' (1 - worst, 0 - accidental, 1 - ideal)
- ** When to use**:
- ** Unbalanced data**: MSC is resistant to class imbalance
- **comparison models**: Good metrics for comparing different algorithms
- **Medical diagnostic**: When all types of errors matter
- ** Fraud detection**: When both omissions and false reactions are important
- ** When not used**:
- ** Balanced data**: Could be less informative than accuracy
- ** Only predictions**: When only classes are important and no correlation
- ** Practical examples**:
- ** Excellent quality**: `> 0.7' (strong correlation)
- ** Good quality**: `0.5-0.7' (moderate correlation)
- ** Acceptable quality**: `0.3-0.5' (low correlation)
- ** Poor quality**: `< 0.3' (very weak correlation)
- ** Benefits**:
- ** Resistance to imbalance**: not dependent on from class distribution
- ** Symmetry**: Single sensitivity to all types of errors
- ** Interpretation**: Shows the quality of correlation
- ** Disadvantages**:
- **Complicity of interpretation**: Less intuitive than accuracy
- ** Computation complexity**: Requires more calculation
- ** Interpretation**:
- **1.0**: Perfect correlation (all predictions are correct)
- **0.7-1.0**: Strong correlation
**0.5-0.7**: Moderate correlation
- **0.3-0.5**: Weak correlation
- **0.0**: No correlation (accident)
- **-1.0**: Negative correlation (all predictions are wrong)

#### Cohen's Kappa
```python
from sklearn.metrics import cohen_kappa_score

kappa = cohen_kappa_score(y_true, y_pred)
print(f"Cohen's Kappa: {kappa:.4f}")
```

**Detail describe parameters Cohen's Kappa:**

**Methric Cohen's Kappa:**
- ** Meaning**: Coherence between true and predicted classes with random consent
- **Formoula**: `(Po-Pe) / (1-Pe)' where Po is the observed agreement, Pe is the expected accidental agreement
- ** Range**: `[-1, 1]' (1 - worst, 0 - accidental, 1 - ideal)
- ** When to use**:
- ** Unbalanced data**: Kappa takes into account accidental consent
- **comparison models**: Good metrics for comparing different algorithms
- **Medical diagnostic**: When all types of errors matter
- ** Fraud detection**: When both omissions and false reactions are important
- ** When not used**:
- ** Balanced data**: Could be less informative than accuracy
- ** Only predictions**: When only classes are important and no consistency
- ** Practical examples**:
- ** Excellent quality**: `> 0.8' (almost perfect agreement)
- ** Good quality**: `0.6-0.8' (significant agreement)
- ** Acceptable quality**: `0.4-0.6' (moderate consent)
- ** Poor quality**: `< 0.4' (negative agreement)
- ** Benefits**:
- **Measurement of accident**: Considers accidental agreement
- ** Resistance to imbalance**: not dependent on from class distribution
- ** Interpretation**: Shows the quality of consistency
- ** Disadvantages**:
- **Complicity of interpretation**: Less intuitive than accuracy
- ** Computation complexity**: Requires more calculation
- ** Interpretation**:
- **1.0**: Perfect consent (all predictions are correct)
- **0.8-1.0**: Almost perfect agreement
**0.6-0.8**: Substantive agreement
**0.4-0.6**: Moderate consent
**0.2-0.4**: Weak agreement
- **0.0**: No consent (accident)
- **-1.0**: Negative consent (all predictions are wrong)

## metrics for regression

<img src="images/optimized/performance_comparison.png" alt="metrics regression" style="max-width: 100 per cent; exercise: auto; display: lock; marguin: 20px auto;">
*Picture 4: metrics for regression tasks and their interpretation*

Why does regression require other metrics?** Because here we predict continuous values and no classes.

### ♪ The key concepts of regression metric

** Why is it important to understand the types of errors in regression?** Because different metrics show different aspects of quality:

- **MAE (Mean Absolute Error)**: Average absolute error - simple and understandable metric
- **MSE (Mean Squared Error)**: Medium error - fines big mistakes harder
- **RMSE (Root Mean Squared Error)**: root of MSE in the same units as target variable
**R2 (Office of Determination)**: Determination coefficient - percentage of explained variance
- **MAPE (Mean Absolute Percentage Error)**: Average absolute percentage error
- **MAE vs MSE**: MAE is less sensitive to emissions, MSE more severely fines large errors

### Basic metrics

#### Mean Absolute Error (MAE)
```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_true, y_pred)
print(f"MAE: {mae:.4f}")
```

** Detailed describe parameters mean_absolute_error:**

**function mean_absolute_error:**
- ** Designation**: Calculation of average absolute error (MAE)
- **parameters**:
- **'y_tree'**: True values
-** Type**: Array-lake
- **describe**: Mass of true values of target variable
 - **examples**: [1.5, 2.3, 3.1, 4.0], [100, 200, 150, 300]
- **'y_pred'**: Projected values
-** Type**: Array-lake
- **describe**: Mass of predicted values
 - **examples**: [1.2, 2.5, 2.8, 4.2], [95, 210, 145, 320]
** `sample_white'**: Weights for examples (on default None)
-** Type**: Array-lake or None
- **describe**: Weights for each example when calculating MAE
 - **examples**: [1.0, 2.0, 1.5, 0.5]
**/ 'multioutput'**: Type of averaging for multidimensional exits (on default 'uniform_overage')
- ** Type**: str or array-lake
- **describe**: Mode of averaging for multidimensional exits
- **Options**: 'uniform_overage', 'raw_valutes', array balance
- **Return value**: float or array - MAE for each output
- ** Averagings for multidimensional exits**:
- **'uniform_overage'**: Equivalent average on all exits
- **'raw_valutes'**: Returns MAE for each exit separately
- **array balance**: Weighted average with given balance
- ** Use**:
- ** Assessment of accuracy**: When an average error of preferences is important
- ** Emission stability**: MAE is less sensitive to emissions than MSE
- ** Interpretation**: Easy to interpret (average error in target variable units)

**/ Detailed describe of MAE parameters:**

**Mean Absolute Error (MAE):**
- ** Meaning**: Average absolute error between true and predicted values
- **Formoule**: `(1/n)' * ♪ y_pred ♪
- ** Value range**: `[0, +] &apos; (0 = ideal Pradition, +\] - worst)
- ** When to use**:
- ** Assessment of accuracy**: When an average error of preferences is important
- ** Emission stability**: MAE is less sensitive to emissions than MSE
- ** Interpretation**: Easy to interpret (average error in target variable units)
- **comparison models**: Good metrics for comparing different algorithms
- ** When not used**:
- ** Critical big mistakes**: When big mistakes are much worse than small ones
- **Optimization**: MAE not differentiated in zero
- ** Practical examples**:
- ** Excellent quality**: `< 0.1* std(y_tree)' (very low error)
- ** Good quality**: `0.1-0.3 * std(y_tree)' (low error)
- ** Acceptable quality**: `0.3-0.5 * std(y_tree)' (moderate error)
- ** Bad quality**: `> 0.5 * std(y_tree) ` (high error)
- **parameter `sample_weight`**:
- ** Designation**: Weights for each example
- ** Use**: for important examples or unbalanced data
- ** Benefits**:
- ** Interpretation**: Shows average error in units of target variable
- ** Emission stability**: Less sensitive to extremes
- **Simple**: Easy to understand and figure out
- ** Disadvantages**:
**not differentiated**:not suitable for gradient optimization
- **not takes into account the importance**: All errors are considered equally important
- ** Interpretation**:
- **0.0**: Perfect Predation (all predictions accurate)
- **< 0.1 * std**: Very good quality
- **0.1-0.3 * std**: Good quality
**0.3-0.5 * std**: Acceptable quality
- **> 0.5 * std**: Poor quality

#### Mean Squared Error (MSE)
```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_true, y_pred)
print(f"MSE: {mse:.4f}")
```

** Detailed describe parameters mean_squared_error:**

**function mean_squared_error:**
- ** Designation**: Calculation of average square error (MSE)
- **parameters**:
- **'y_tree'**: True values
-** Type**: Array-lake
- **describe**: Mass of true values of target variable
 - **examples**: [1.5, 2.3, 3.1, 4.0], [100, 200, 150, 300]
- **'y_pred'**: Projected values
-** Type**: Array-lake
- **describe**: Mass of predicted values
 - **examples**: [1.2, 2.5, 2.8, 4.2], [95, 210, 145, 320]
** `sample_white'**: Weights for examples (on default None)
-** Type**: Array-lake or None
- **describe**: Weights for each example when calculating MSE
 - **examples**: [1.0, 2.0, 1.5, 0.5]
**/ 'multioutput'**: Type of averaging for multidimensional exits (on default 'uniform_overage')
- ** Type**: str or array-lake
- **describe**: Mode of averaging for multidimensional exits
- **Options**: 'uniform_overage', 'raw_valutes', array balance
- ** `squared'**: Return MSE or RMSE (on default True)
-**Teep**: bool
-**describe**:True - returns MSE, False - returns RMSE
- **Return value**: float or array - MSE for each output
- ** Averagings for multidimensional exits**:
- **'uniform_overage'**: Equivalent average on all exits
- **'raw_valutes'**: Returns MSE for each exit separately
- **array balance**: Weighted average with given balance
- ** Use**:
- **Optimization**: MSE is differentiated and suitable for gradient optimization
- ** Critical big mistakes**: When big mistakes are much worse than small ones
- ** Training in neural networks**: Standard function of losses for regression

**/ Detailed describe of MSE parameters:**

**Mean Squared Error (MSE):**
- ** Meaning**: Average square error between true and predicted values
- **Formoula**: `(1/n)' * \(y_tree - y_pred)2'
- ** Value range**: `[0, +] &apos; (0 = ideal Pradition, +\] - worst)
- ** When to use**:
- **Optimization**: MSE is differentiated and suitable for gradient optimization
- ** Critical big mistakes**: When big mistakes are much worse than small ones
- **comparison models**: Good metrics for comparing different algorithms
- ** Training in neural networks**: Standard function of losses for regression
- ** When not used**:
- ** Emissions**: MSE is very sensitive to extreme values
- ** Interpretability**: It is difficult to interpret (square of units of target variable)
- ** Practical examples**:
- ** Excellent quality**: `<0.01*var(y_tree)' (very low error)
- ** Good quality**: `0.01-0.1 * var(y_tree)' (low error)
- ** Acceptable quality**: `0.1-0.5 * var(y_tree)' (moderate error)
- ** Bad quality**: `> 0.5 * var(y_tree) ` (high error)
- **parameter `sample_weight`**:
- ** Designation**: Weights for each example
- ** Use**: for important examples or unbalanced data
- ** Benefits**:
- **Difference**: Suitable for gradient optimization
- ♪ Feelings of big mistakes ♪ ♪ Big mistakes are more punitive ♪
- ** Mathematical properties**: has good mathematical properties
- ** Disadvantages**:
- ** Emission sensitivity**: Very sensitive to extreme values
- ** Complexity of interpretation**: It is difficult to interpret (square of units)
- ** Inequitability of fines**: Quadratic fine may be too severe
- ** Interpretation**:
- **0.0**: Perfect Predation (all predictions accurate)
- **< 0.01 * var**: Very good quality
- **0.01-0.1 * var**: Good quality
**0.1-0.5 * var**: Acceptable quality
- **> 0.5 * var**: Poor quality

#### Root Mean Squared Error (RMSE)
```python
import numpy as np

rmse = np.sqrt(mean_squared_error(y_true, y_pred))
print(f"RMSE: {rmse:.4f}")
```

**/ Detailed describe of RMSE parameters: **/

**Root Mean Squared Error (RMSE):**
- ** Meaning**: root of the average square error between true and predicted values
- **Formoula**: `sqrt((1/n)* \\(y_tree - y_pred)2`
- ** Value range**: `[0, +] &apos; (0 = ideal Pradition, +\] - worst)
- ** When to use**:
- ** Interpretation**: RMSE in the same units as the target variable
- ** Critical big mistakes**: When big mistakes are much worse than small ones
- **comparison models**: Good metrics for comparing different algorithms
- ** Training in neural networks**: Standard metrics for regression
- ** When not used**:
- ** Emissions**: RMSE is very sensitive to extreme values
- ** Unequal fines**: Quadratic fine may be too severe
- ** Practical examples**:
- ** Excellent quality**: `< 0.1* std(y_tree)' (very low error)
- ** Good quality**: `0.1-0.3 * std(y_tree)' (low error)
- ** Acceptable quality**: `0.3-0.5 * std(y_tree)' (moderate error)
- ** Bad quality**: `> 0.5 * std(y_tree) ` (high error)
- ** Benefits**:
- ** Interpretation**: in the same units as the target variable
- ♪ Feelings of big mistakes ♪ ♪ Big mistakes are more punitive ♪
- ** Mathematical properties**: has good mathematical properties
- ** Disadvantages**:
- ** Emission sensitivity**: Very sensitive to extreme values
- ** Inequitability of fines**: Quadratic fine may be too severe
- ** Computation difficulty**: The quadratic root must be calculated
- ** Interpretation**:
- **0.0**: Perfect Predation (all predictions accurate)
- **< 0.1 * std**: Very good quality
- **0.1-0.3 * std**: Good quality
**0.3-0.5 * std**: Acceptable quality
- **> 0.5 * std**: Poor quality

#### R² Score
```python
from sklearn.metrics import r2_score

r2 = r2_score(y_true, y_pred)
print(f"R² Score: {r2:.4f}")
```

**/ Detailed descrie parameters r2_score:**

**function r2_score:**
- ** Designation**: Calculation of the determination coefficient (R2)
- **parameters**:
- **'y_tree'**: True values
-** Type**: Array-lake
- **describe**: Mass of true values of target variable
 - **examples**: [1.5, 2.3, 3.1, 4.0], [100, 200, 150, 300]
- **'y_pred'**: Projected values
-** Type**: Array-lake
- **describe**: Mass of predicted values
 - **examples**: [1.2, 2.5, 2.8, 4.2], [95, 210, 145, 320]
** `sample_white'**: Weights for examples (on default None)
-** Type**: Array-lake or None
- **describe**: Weights for each example when calculating R2
 - **examples**: [1.0, 2.0, 1.5, 0.5]
**/ 'multioutput'**: Type of averaging for multidimensional exits (on default 'uniform_overage')
- ** Type**: str or array-lake
- **describe**: Mode of averaging for multidimensional exits
- **Options**: 'uniform_overage', 'raw_valutes', array balance
- **Return value**: float or array - R2 for each exit
- ** Averagings for multidimensional exits**:
- **'uniform_overage'**: Equivalent average on all exits
- **'raw_valutes'**: Returns R2 for each exit separately
- **array balance**: Weighted average with given balance
- ** Use**:
- ** Quality assessment**: When you need to understand how well the model explains data
- **comparison models**: Good metrics for comparing different algorithms
- ** Interpretation**: Easy to interpret (percentage of explained variance)

**/ Detailed descrie parameters R2 Score: **/

**Methric R2 Score:**
- ** Meaning**: Proportion of variance of target variable explained by model
- **Formoule**: `1 - (SS_res / SS_tot) `where SS_res = \(y_tre - y_pred)2, SS_tot = \(y_tree - y_mean)2
- ** A range of values**: `(-, 1]' (1 - ideal Pradition, 0 - as average, negative - worse than average)
- ** When to use**:
- ** Quality assessment**: When you need to understand how well the model explains data
- **comparison models**: Good metrics for comparing different algorithms
- ** Interpretation**: Easy to interpret (percentage of explained variance)
- ** Training in neural networks**: Standard metrics for regression
- ** When not used**:
- ** Emissions**: R2 may be misleading if emissions are present
- ** Uneven data**: May be unstable for uneven data
- ** Practical examples**:
- ** Excellent quality**: `> 0.9' (90 per cent+explained dispersion)
- ** Good quality**: `0.7-0.9' (70-90 per cent of explained dispersion)
- ** Acceptable quality**: `0.5-0.7' (50-70 per cent of explained dispersion)
- ** Bad quality**: `< 0.5' (< 50% of explained dispersion)
- **parameter `sample_weight`**:
- ** Designation**: Weights for each example
- ** Use**: for important examples or unbalanced data
- ** Benefits**:
- ** Interpretability**: Shows percentage of explained variance
- **Normization**: Values from 0 to 1 are easy to compare
- ** Mathematical properties**: has good mathematical properties
- ** Disadvantages**:
- ** Emission sensitivity**: May be misleading if emissions are present
- ** Inequitability**: May be unstable for uneven data
- ** Computation difficulty**: Average value to be calculated
- ** Interpretation**:
- **1.0**: Perfect Pradition.
- **0.9-1.0**: Excellent quality
- **0.7-0.9**: Good quality
**0.5-0.7**: Acceptable quality
- **0.0-0.5**: Poor quality
- **0.0**: No better than average
- **< 0.0**: Model is worse than average

### Moved metrics

<img src="images/optimized/advanced_topics_overView.png" alt="Proved metrics" style"="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 5: Advanced metrics for Deep Analysis Model Quality*

Why do you need advanced metrics? Because basic metrics not always show a complete picture of model quality:

**MAPE (Mean Absolute Percentage Error)**: Percentage error for understanding relative accuracy
**SMAPE (Symmetric Mean Absolute Percentage Error)**: Simmetric version of MAPE
- **WAPE (Weighted Absolute Percentage Error)**: Weighted percentage error
- **Custom Metrics**: Castle metrics for specific tasks
- **BusinessMetrics**: Business-metrics linked with real KPI
**Statistical tests**: Statistical tests for model comparison

#### Mean Absolute Percentage Error (MAPE)
```python
def mape(y_true, y_pred):
 return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

mape_score = mape(y_true, y_pred)
print(f"MAPE: {mape_score:.4f}%")
```

**/ Detailed describe parameters MAPE:**

**Mean Absolute Percentage Error (MAPE):**
- ** Meaning**: Average absolute percentage error between true and predicted values
- **Formoule**: `(1/n)' * ♪ [Y_tree - y_pred] / y_tree ♪ 100'
- ** Value range**: `[0, +] &apos; (0% - ideal Pradition, +\] - worst)
- ** When to use**:
- ** Percentage interpretation**: When percentage error is important
- **comparison of different scales**: MAPE is normalized and allows comparison of different data
- ** Business-metrics**: Easy to interpret for business
- ** Time series**: Good meth for forecasting
- ** When not used**:
- ** No value**: MAPE no defined at y_tree = 0
- ** Very small**: May be unstable at very small values
- ** Emissions**: Very sensitive to extreme values
- ** Practical examples**:
- ** Excellent quality**: `< 5%' (very low error)
- ** Good quality**: `5-15%' (low error)
- ** Acceptable quality**: `15-30%' (moderate error)
- ** Bad quality**: `> 30%' (high error)
- ** Benefits**:
- ** Interpretation**: Easy to understand (percentage error)
- **Normization**: Allows comparison of different data
- ** Business Applicability**: Good for BusinessReports
- ** Disadvantages**:
- ** The problem with zero**: not determined at y_tree = 0
- ** Emission sensitivity**: Very sensitive to extreme values
- **Asymmetric**:Pension is stronger than overestimation
- ** Interpretation**:
- **0%**: Perfect Predation (all predictions are accurate)
- **< 5%**: Very good quality
**5-15%**: Good quality
**15-30%**: Acceptable quality
- **> 30%**: Poor quality

#### Symmetric Mean Absolute Percentage Error (SMAPE)
```python
def smape(y_true, y_pred):
 return np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100

smape_score = smape(y_true, y_pred)
print(f"SMAPE: {smape_score:.4f}%")
```

**/ Detailed describe of SMAPE parameters:**

**Symmetric Mean Absolute Percentage Error (SMAPE):**
- ** Meaning**: Symmetric average absolute percentage error between true and predicted values
== sync, corrected by elderman == @elder_man
- ** Value range**: `[0,200%] &apos; (0% ideal Pradition, 20% worst)
- ** When to use**:
- ** Symmetrical evaluation**: When a symmetrical error assessment is important
- **comparison of different sizes**: SMAPE is normalized and allows comparison of different data
- ** Business-metrics**: Easy to interpret for business
- ** Time series**: Good meth for forecasting
- ** When not used**:
- ** No value**: SMAPE can be unstable at y_tree = 0 or y_pred = 0
- ** Very small**: May be unstable at very small values
- ** Emissions**: Very sensitive to extreme values
- ** Practical examples**:
- ** Excellent quality**: `< 10%' (very low error)
- ** Good quality**: `10-20%' (low error)
- ** Acceptable quality**: `20-40%' (moderate error)
- ** Bad quality**: `> 40%' (high error)
- ** Benefits**:
- ** Symmetricity**: One penalty for overestimation and underestimation
- ** Interpretation**: Easy to understand (percentage error)
- **Normization**: Allows comparison of different data
- ** Business Applicability**: Good for BusinessReports
- ** Disadvantages**:
- ** The problem with zero**: May be unstable at y_tree = 0 or y_pred = 0
- ** Emission sensitivity**: Very sensitive to extreme values
- ** Computation difficulty**: Requires more calculation than MAPE
- ** Interpretation**:
- **0%**: Perfect Predation (all predictions are accurate)
- **< 10%**: Very good quality
**10-20%**: Good quality
**20-40%**: Acceptable quality
- **> 40%**: Poor quality
- **200%**: Worst possible implementation

#### Mean Absolute Scaled Error (MASE)
```python
def mase(y_true, y_pred, y_train):
# Naïve projection (later value)
 naive_forecast = np.roll(y_train, 1)
 naive_mae = np.mean(np.abs(y_train - naive_forecast))

# Model MAE
 model_mae = np.mean(np.abs(y_true - y_pred))

 return model_mae / naive_mae

mase_score = mase(y_true, y_pred, y_train)
print(f"MASE: {mase_score:.4f}")
```

**/ Detailed describe of MASE parameters:**

**Mean Absolute Scaled Error (MASE):**
- ** Meaning**: Average absolute scale error relative to naive projection
- **Formoula**: `MAE_model / MAE_naive' where MAE_naive - MAE naive projection
- ** A range of values**: `[0, + ]' (0 is ideal Pradition, 1 is naive, >1 is worse than naive)
- ** When to use**:
- ** Time series**: MASE is a special time series
- **comparison with naive prognosis**: When it's important to see if the naive projection model is better
- **Normization**: MASE is normalized and allows comparisons of different time series
- ** Projection**: Good metric for estimating the quality of projections
- ** When not used**:
**not time series**: MASE note is suitable for normal regression
- **Very short rows**: May be unstable for short time series
- ** Seasonal data**: May be unstable for heavy seasonal data
- ** Practical examples**:
- ** Excellent quality**: `< 0.5' (in 2 times better than naive)
- ** Good quality**: `0.5-0.8' (better than naive)
- ** Acceptable quality**: `0.8-1.0' (approximately as naive)
- **Bad quality**: `> 1.0' (more than naive)
- **parameter `y_train`**:
- ** Designation**: Training data for calculating a naive projection
- ** Use**: There must be the same data on which the model was trained.
- ** Benefits**:
- **Normization**: Allows comparison of different time series
- ** Interpretation**: Easy to understand (better/better than naive)
- **Sistence to scale**: not dependent on from size of data
- **Special**: Special time for time series
- ** Disadvantages**:
- **Restriction**: Only suitable for time series
- **dependency from data**: Requires training data
- ** Computation difficulty**: Requires calculation of naive projection
- ** Interpretation**:
- **0.0**: Perfect Predation (all predictions accurate)
- **< 0.5**: Very good quality (in 2+ times better than naive)
- **0.5-0.8**: Good quality (better than naive)
**0.8-1.0**: Acceptable quality (approximately as naive)
- **1.0**: As a naïve projection
- **> 1.0**: Worse than the naive forecast

## Use of metrics in AutoGluon

## configuration metric for learning

```python
from autogluon.tabular import TabularPredictor

# for classification
predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy' # or 'f1', 'roc_auc', 'log_loss'
)

# for regression
predictor = TabularPredictor(
 label='target',
 problem_type='regression',
 eval_metric='rmse' # or 'mae', 'r2'
)
```

** Detailed describe parameters TabularPredicator:**

**Class TabularPredictor:**
- ** Designation**: pre-indicator &apos; s training for table data
- **parameters of design**:
- **'label'**: Name of target variable
- **Typ**: str
- **describe**: Name of column with target variable in data
 - **examples**: 'target', 'price', 'category'
- **'problem_type'**: Task type (on default 'auto')
- **Typ**: str
- **describe**: Type of task
- **Options**: 'auto', 'binary', 'multiclass', 'regression', 'Quantile'
- ** `eval_metric'**: Metrique for evaluation (on default 'auto')
- ** Type**: str or Scorer
- **describe**: Meterics for optimization during training
- **Options**: 'accuracy', 'f1', 'roc_auc', 'log_loss', 'rmse', 'mae', 'r2'
- **'path'**: Path for model preservation (on default 'AutogluonModels')
- **Typ**: str
- **describe**: Directorate for the preservation of trained models
- ** `verbosity'**: Output level (on default 2)
- **Typ**:int
- **describe**: Detailsation level (0-4)
**Options**: 0 (silent), 1 (minimum), 2 (normal), 3 (detailed), 4 (maximum)
- **'presets'**: Pre-installation configuration (on default 'media_quality_faster_training')
- **Typ**: str
- **describe**: Pre-established learning configurations
- **Options**: 'best_quality', 'high_quality', 'good_quality', 'media_quality', 'optimise_for_development'
- ** Use**:
- **create pre-indicator**: Initiating a pre-injector with specified parameters
- ** Model training**: The challenge of the Fit() method for learning
- **Treathing**: Challenge of predict() and predict_proba()
- ** Quality assessment**: Challenge of the evalute method()

**/ Detailed describe parameters eval_metric:**

**parameter eval_metric:**
- ** Designation**: Meterics for optimization during model learning
- **Tips of values**: Line with the name metrics or object Scorer
- **Effects on learning**: AutoGluon uses this metric to select the best models
- ** Available metrics for classification**:
- **'accuracy'**: Accuracy (on default for multiclass)
- **'f1'**: F1-score (on default for beinary)
- **'roc_auc'**: ROC AUC (good for unbalanced data)
- **'log_loss'**: Log Loss (good for probabilities)
- **'balanced_accuracy'**: Balanced accuracy
 - **`'precision'`**: Precision
 - **`'recall'`**: Recall
 - **`'mcc'`**: Matthews Correlation Coefficient
- ** Accessible metrics for regression**:
- **'romse'**: Root Mean Squared Error (on default)
 - **`'mae'`**: Mean Absolute Error
 - **`'r2'`**: R² Score
 - **`'mse'`**: Mean Squared Error
 - **`'mape'`**: Mean Absolute Percentage Error
 - **`'smape'`**: Symmetric Mean Absolute Percentage Error
- ** Recommendations on selection**:
- ** Balanced data**: ``accuracy' for classification, `'rmse' for regression
- ** Unbalanced data**: `'f1' or `'roc_auc' for classification
- **Probably important**: `'log_loss' for classification
- ** Percentage errors**: `'mape' or `'smape' for regression
- **Temporary series**: `'mae'' or `'rmse' for regression

### Multiple metrics

```python
# Learning with several metrics
predictor.fit(
 train_data,
 eval_metric=['accuracy', 'f1', 'roc_auc']
)

# Getting an all-metric
performance = predictor.evaluate(test_data)
print(performance)
```

**/ Detailed descrie parameters of the evalute method: **/

** Evalute method:**
- ** Designation**: Quality assessment of the trained model on test data
- **parameters**:
- **'data'**: test data
-** Type**: DataFrame
- **describe**: Table with test data
- **Structure**: Columns with signature + column with target variable
- **'metrics'**: metrics for computation (on default None)
- ** Type**: List or None
- **describe**: List metric for computation
- **Options**: ['accuracy', 'f1', 'roc_auc'], None (all available)
- ** `silent'**: Repress output (on default False)
-**Teep**: bool
- **describe**: Show progress in metric computation
**Return value**: dict - dictionary with metrics and their values
- **examples of returned values**:
- ** Classification**: {'accuracy': 0.85, 'f1': 0.82, 'roc_auc': 0.88}
- **Regression**: {'rmse': 0.15, 'mae': 0.12, 'r2':0.78}
- ** Use**:
- ** Quality assessment**: Collection of quality metric on test data
- **comparison models**: comparison different algorithms
- **validation**: heck of model quality before release
- **Reportability**: quality review reports
```

**/ Detailed descrie parameters of Fit method: **/

** Method Fit:**
- ** Designation**: Training the precursor on the data provided
- **parameters**:
- **'training_data'**: Training data
-** Type**: DataFrame
- **describe**: Table with learning data
- **Structure**: Columns with signature + column with target variable
** `eval_metric'**: Metrique for evaluation (on default None)
- ** Type**: str, List or Scorer
- **describe**: Metrique or List metric for optimization
- **Options**: 'accuracy', 'f1', 'roc_auc', ['accuracy', 'f1'], customary_scorer
** `time_limit'**: Limiting the time of learning (on default None)
- **Typ**:int or None
- **describe**: Maximum learning time in seconds
- **examples**: 300 (5 minutes), 3,600 (1 hour)
- **'presets'**: Pre-installation configuration (on default Non)
- **Typ**: str or None
- **describe**: Pre-established learning configurations
- **Options**: 'best_quality', 'high_quality', 'good_quality', 'mediam_quality'
- **'hyperparameters'**: Model Hyperparameters (on default None)
- ** Type**: dict or None
- **describe**: Vocabulary with hyperparameters for different algorithms
 - **examples**: {'GBM': {'num_boost_round': 100}, 'NN': {'epochs': 50}}
- **'feature_metadata'**: Metadata signs (on default None)
-** Type**: FeatureMetadata or None
- **describe**: Metadata on the types and properties of the topics
** `holdout_frac'**: Percentage of data for validation (on default 0.1)
- **Typ**: float
**describe**: Percentage of data for internal validation (0.0 - 1.0)
- ** Recommendations**: 0.1-0.2 for large datasets, 0.2-0.3 for small
- **Return value**: None (model retained inside pre-indicator)
- ** Use**:
- ** Model training**: Basic method for pre-rector education
- **configuring metric**: specific metric for optimization
** Time control**: limitation of time of study
**configuring parameters**: specific hyperparameters for algorithms

**/ Detailed descrie parameters of multiple metrics: **/

**parameter eval_metric (List metric):**
** Designation**: List metric for model quality evaluation
- **Tips of values**: List line with names of metrics
- **Effect on learning**: AutoGluon uses the first metric for optimization, the rest for Monitoring
- ** Benefits**:
- ** Integrated assessment**: Allows assessment of the model on multiple criteria
- **Monitoring**: Helps track quality during training
- **comparison**: Simplifies comparison of different models
- ** Recommendations on selection**:
- ** Main metric**: First in list - for optimization
- ** Additional metrics**: Others for Monitoring
- ** Diversity**: Choose metrics that measure different aspects of quality
- **examples of combinations**:
- ** Classification**: `['accuracy', `f1', 'roc_auc'] `
== sync, corrected by elderman == @elder_man
- ** Unbalanced data**: `['f1', 'roc_auc', 'balanced_accuracy'] `
- **Probability**: `['log_loss', 'roc_auc', 'accuracy'] `

### Castle metrics

```python
from autogluon.core import Scorer

# Create caste metrics
def custom_metric(y_true, y_pred):
"Castom metric for quality assessment"
# Your Logsk calculation
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

**/ Detailed descrie parameters of caste-based metrics:**

** Class Scorer:**
- ** Designation**: cut user metrics for AutoGluon
- **parameters**:
- **'name'**: Name of metrics (line)
- **'score_fund'**: finance for computation of metrics
- **'green_is_better'**: True if more value is better, False if less
- **function score_func**:
- **Inductions**: `y_tree', `y_pred' (numpy arrays)
**Return value**: Number (float)
- ** Demands**: Should be vectorized and Working with numpy arrays
- **parameter greater_is_better**:
- **True**: More metrics means better quality (accuracy, f1, r2)
- **False**: Lower value metrics means better quality (mae, mse, log_loss)
- **examples caste-based metrics**:
- ** Business-metrics**: Revenue, loss, conversion
- ** Specialized metrics**: for specific domains
- ** Combination metrics**: Mixing several metrics
- ** Weighted metrics**: with regard to the importance of examples
- ** Recommendations**:
- **Simple**: function should be simple and quick
- **Vocation**: Use numpy operation for performance
- ** Error processing**: Add checks on input accuracy
- **documentation**: Document the appointment of metrics well

## Performance analysis

♪# ♪ Model leader

```python
# Getting a leaderboard
leaderboard = predictor.leaderboard(test_data)
print(leaderboard)

# A detailed leaderboard
leaderboard_Detailed = predictor.leaderboard(
 test_data,
 extra_info=True,
 silent=False
)
```

** Detailed describe parameters of the leaderboard method:**

**Leaderboard method:**
- ** Designation**: Collection of model rating on quality
- **parameters**:
- **'data'**: test data (on default None)
- ** Type**: DataFrame or None
- **describe**: Table with test data for evaluation
- **Structure**: Columns with signature + column with target variable
- **'extra_info'**: Additional information (on default False)
-**Teep**: bool
- **describe**: Do you want to show additional information on models
- ** Additional information**: Model size, number of topics, hyperparameters
- ** `silent'**: Repress output (on default True)
-**Teep**: bool
- **describe**: Show progress in metric computation
- **Return value**: dataFrame - table with metrics for each model
- **Wheelboards**:
- **'model'**: Model name
- **'score_val'**: Value of basic instruments on validation
- **'score_test'**: Value of basic metrics on the test (if given data)
- **'fit_time'**: Model learning time
- **'pred_time'**: The prediction time
- **'stack_level'**: Glass level (for ensemble models)
- ** Additional columns (extra_info=True)**:
- **'num_features'**: Number of topics
- **/memory_size'**: The size of the model in memory
- **'num_models'**: Number of models in ensemble
- **'hyperparameters'**: Model Hyperparameters
- ** Use**:
- **comparison of models**: Choice of a better model
- ** Performance Analysis**: Understanding strengths and weaknesses
- **Optification**: Selection of parameters for further Settings

** Detailed describe of the leaderboard parameters:**

**Leaderboard method:**
- ** Designation**: Collection of model rating on quality
- **parameters**:
- ** `test_data'**: test data for evaluation (almost)
- ** `extra_info'**: Show additional information (on default False)
- ** `silent'**: Repress output (on default True)
- **Return value**: dataFrame with metrics for each model
- **Wheelboards**:
- **'model'**: Model name
- **'score_val'**: Value of basic instruments on validation
- **'score_test'**: Value of basic metrics on the test (if given test_data)
- **'fit_time'**: Model learning time
- **'pred_time'**: The prediction time
- **'stack_level'**: Glass level (for ensemble models)
- ** Additional information (extra_info=True)**:
- **'num_features'**: Number of topics
- **/memory_size'**: The size of the model in memory
- **'num_models'**: Number of models in ensemble
- **'hyperparameters'**: Model Hyperparameters
- ** Use**:
- **comparison of models**: Choice of a better model
- ** Performance Analysis**: Understanding strengths and weaknesses
- **Optification**: Selection of parameters for further Settings

### Signal importance analysis

```python
# The importance of signs
feature_importance = predictor.feature_importance()
print(feature_importance)

# Visualizing the importance of signs
import matplotlib.pyplot as plt

feature_importance.plot(kind='barh', figsize=(10, 8))
plt.title('Feature importance')
plt.xlabel('importance')
plt.show()
```

**/ Detailed describe parameters of the mode_importance method: **/

**Feature_importance method:**
- ** Designation**: Recognition of the importance of signs for a better model
- **parameters**:
- **'data'**: data for calculating importance (on default None)
- ** Type**: DataFrame or None
- **describe**: data for calculating the importance of topics
- **Structure**: Columns with signature + column with target variable
- **'model'**: Model for Analysis (on default Non)
- **Typ**: str or None
- **describe**: Name of model for Analysis of importance
- **Options**: Headboard model name, Noe (best model)
** `subsample'**: Subsample size (on default 10,000)
- **Typ**:int or None
- **describe**: Number of examples for calculating importance
- ** Recommendations**: 10,000 for rapid computation, None for all data
- **'num_shuffle_sets'**: Number of resets (on default 1)
- **Typ**:int
- **describe**: Number of resets for stability
- ** Recommendations**: 1 for rapid calculation, 3-5 for stability
- **Return value**: Series - the importance of each sign
- **methods calculation of importance**:
- **Permutation import**: Reset and measure quality drop
- **SHAP Values**: Shapley Additive Applications for Explanations
- **Tree-based import**: for decision trees (Gini, Information Gain)
- ** Interpretation**:
- ** High importance**: A sign strongly influences predictions
- ** Low importance**: A sign has little influence on predictions
- ** Negative importance**: A sign may affect model quality
- ** Use**:
- ** Selection of topics**: Selection of the most important topics
- ** Model interpretation**: Understanding Logs of model operation
- ** Data Analysis**: Identification of the most informative indicators
** Optimization**: improvised data quality

** Detailed describe parameters Analysis of the importance of signs:**

**Feature_importance method:**
- ** Designation**: Recognition of the importance of signs for a better model
- **Return value**: Series with the importance of each sign
- **methods calculation of importance**:
- **Permutation import**: Reset and measure quality drop
- **SHAP Values**: Shapley Additive Applications for Explanations
- **Tree-based import**: for decision trees (Gini, Information Gain)
- ** Interpretation**:
- ** High importance**: A sign strongly influences predictions
- ** Low importance**: A sign has little influence on predictions
- ** Negative importance**: A sign may affect model quality
- ** Use**:
- ** Selection of topics**: Selection of the most important topics
- ** Model interpretation**: Understanding Logs of model operation
- ** Data Analysis**: Identification of the most informative indicators
** Optimization**: improvised data quality

### Error analysis

```python
# Analysis of errors for classification
from sklearn.metrics import classification_Report, confusion_matrix

# Report on classification
print(classification_Report(y_true, y_pred))

# A matrix of errors
cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:")
print(cm)

# Visualization of the error matrix
import seaborn as sns
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.show()
```

**/ Detailed descrie parameters classification_Report:**

**function classification_Report:**
- ** Designation**: Detailed Report on Quality of Classification
- **parameters**:
- **'y_tree'**: True class labels
-** Type**: Array-lake
- **describe**: Massive of true class tags
 - **examples**: [0, 1, 1, 0, 1], ['cat', 'dog', 'cat']
- **'y_pred'**: Presumed class labels
-** Type**: Array-lake
- **describe**: Mass of predicted class tags
 - **examples**: [0, 1, 0, 0, 1], ['cat', 'dog', 'dog']
- **'target_names'**: Classnames (on default Non)
- ** Type**: List or None
- **describe**: List of class names for Reporta
 - **examples**: ['negative', 'positive'], ['cat', 'dog', 'bird']
- **'labels'**: List of classes for Reporta (on default None)
- ** Type**: List or None
- **describe**: List of classes for inclusion in Report
 - **examples**: [0, 1], ['cat', 'dog']
** `sample_white'**: Weights for examples (on default None)
-** Type**: Array-lake or None
- **describe**: Weights for each example when calculating metrics
- **'digits'**: Number of digits after decimal place (on default 2)
- **Typ**:int
- **describe**: Number of digits after decimal point in conclusion
- ** Recommendations**: 2-4 for reading
- ** `Zero_diviction'**: Value when dividing on zero (on default 'warn')
- ** Type**: str or float
- **describe**: What to return when the not metric is defined
- **Options**: 'warn', 0, 1
- **Return value**: str - text Report with metrics
- **Returnable metrics**:
**Precision**: Accuracy for each class
- **Recall**: Completeness for each class
**F1-score**: F1-measures for each class
- **Support**: Number of examples in each class
- **Macro avg**: Average arithmetic on classes
- **Weighted avg**: Average weighted on number of examples
- ** Use**:
- ** Detailed analysis**: Understanding quality on each class
- ** Identification of problems**: Searching classes with poor quality
- **comparison models**: Detailed comparison of different algorithms

** Detailed describe parameters confusion_matrix:**

**function confusion_matrix:**
- ** Designation**: Error matrix for Analysis types of errors
- **parameters**:
- **'y_tree'**: True class labels
-** Type**: Array-lake
- **describe**: Massive of true class tags
 - **examples**: [0, 1, 1, 0, 1], ['cat', 'dog', 'cat']
- **'y_pred'**: Presumed class labels
-** Type**: Array-lake
- **describe**: Mass of predicted class tags
 - **examples**: [0, 1, 0, 0, 1], ['cat', 'dog', 'dog']
- **'labels'**: List classes for matrices (on default None)
- ** Type**: List or None
- **describe**: List of classes for inclusion in the matrix
 - **examples**: [0, 1], ['cat', 'dog']
** `sample_white'**: Weights for examples (on default None)
-** Type**: Array-lake or None
- **describe**: Weights for each example when calculating the matrix
- **'normalyze'**: Normalization of the matrix (on default None)
- **Typ**: str or None
- **describe**: Method of normalization of the matrix
- **Options**: None, 'tree', 'pred', 'all'
- **Return value**: narray - error matrix
- **Elements of the matrix**:
- **TP (True Positive)**: Correctly predicted positive classes
- **TN (True Negative)**: Correctly predicted negative classes
- **FP (False Positive)**: Incorrectly predicted positive classes
- **FN (False Negative)**: Wrongly predicted negative classes
- ** Use**:
- **Analysis of errors**: Understanding the types of model errors
- ** Calibrication**: configurization of the classification threshold
** Interpretation**: Explanation of the model

** Detailed describe parameters Analysis errors:**

**function classification_Report:**
- ** Designation**: Detailed Report on Quality of Classification
- **parameters**:
- **'y_tree'**: True class labels
- **'y_pred'**: Presumed class labels
- **'target_names'**: Class names (traditional)
- **'labels'**: List of classes for Reporta (traditional)
- **/sample_weight'**: Weights for examples (traditional)
- **'digits'**: Number of digits after decimal place (on default 2)
- **Returnable metrics**:
**Precision**: Accuracy for each class
- **Recall**: Completeness for each class
**F1-score**: F1-measures for each class
- **Support**: Number of examples in each class
- **Macro avg**: Average arithmetic on classes
- **Weighted avg**: Average weighted on number of examples
- ** Use**:
- ** Detailed analysis**: Understanding quality on each class
- ** Identification of problems**: Searching classes with poor quality
- **comparison models**: Detailed comparison of different algorithms

**function confusion_matrix:**
- ** Designation**: Error matrix for Analysis types of errors
- **parameters**:
- **'y_tree'**: True class labels
- **'y_pred'**: Presumed class labels
- **'labels'**: List classes for matrices (optimal)
- **/sample_weight'**: Weights for examples (traditional)
- **/normalize'**: Normalization of matrix (optimal)
- **Elements of the matrix**:
- **TP (True Positive)**: Correctly predicted positive classes
- **TN (True Negative)**: Correctly predicted negative classes
- **FP (False Positive)**: Incorrectly predicted positive classes
- **FN (False Negative)**: Wrongly predicted negative classes
- ** Use**:
- **Analysis of errors**: Understanding the types of model errors
- ** Calibrication**: configurization of the classification threshold
** Interpretation**: Explanation of the model

## metrics for time series

### metrics for forecasting

```python
# Mean Absolute Scaled Error (MASE)
def mase_time_series(y_true, y_pred, y_train, seasonal_period=1):
"MASE for Time Series"
# Naïve projection
 naive_forecast = np.roll(y_train, seasonal_period)
 naive_mae = np.mean(np.abs(y_train - naive_forecast))

# Model MAE
 model_mae = np.mean(np.abs(y_true - y_pred))

 return model_mae / naive_mae

# Symmetric Mean Absolute Percentage Error (SMAPE)
def smape_time_series(y_true, y_pred):
"SMAPE for Time Series"
 return np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100
```

**/ Detailed descrie parameters time series metric: **/

**function mase_time_series:**
- ** Designation**: MASE for time series with seasonality
- **parameters**:
- **'y_tree'**: True time series values
- **'y_pred'**: Projected values
- **'y_training'**: Training data for calculating a naive projection
- ** `seasonal_period'**: Seasonal period (on default 1)
- ** Specialities**:
- ** Seasonality**: Considers seasonal variables in data
- **Naïve projection**: Uses the value with previous period
- **Normization**: Allows comparison of different time series
- ** Interpretation**:
- **< 0.5**: Model in 2+ times better than naive projection
- **0.5-0.8**: Model is better than naïve projection
- **0.8-1.0**: Model about as naive as forecast
- **> 1.0**: Model worse than naive projection

**function smape_time_series:**
- ** Designation**: SMAPE for time series
- **parameters**:
- **'y_tree'**: True time series values
- **'y_pred'**: Projected values
- ** Specialities**:
- ** Symmetricity**: One penalty for overestimation and underestimation
- ** Percentage interpretation**: Easy to understand (percentage error)
- **Normization**: Allows comparison of different time series
- ** Interpretation**:
- **< 10%**: Very good quality
**10-20%**: Good quality
**20-40%**: Acceptable quality
- **> 40%**: Poor quality

### metrics for financial data

```python
# Sharpe Ratio
def sharpe_ratio(returns, risk_free_rate=0.02):
""Sharp Coefficient."
 excess_returns = returns - risk_free_rate
 return np.mean(excess_returns) / np.std(excess_returns)

# Maximum Drawdown
def max_drawdown(cumulative_returns):
"Maximal prosperity."
 peak = np.maximum.accumulate(cumulative_returns)
 drawdown = (cumulative_returns - peak) / peak
 return np.min(drawdown)

# Calmar Ratio
def calmar_ratio(returns, max_dd):
"Calmar's Coefficient."
 annual_return = np.mean(returns) * 252
 return annual_return / abs(max_dd)
```

**/ Detailed descrie parameters financial data metric:**

**function sharpe_ratio:**
- ** Designation**: Measurement of return with risk
- **parameters**:
- **'returns'**: Income massity (e.g. daily returns)
- **'risk_free_rate'**: Risk-free rate (on default 0.02 = 2%)
- **Formoula**: `(mean(returns) - risk_free_rate) / std(returns)'
- ** Interpretation**:
- **> 1.0**: Excellent return with risk
- **0.5-1.0**: Good return with risk
- **0.0-0.5**: Acceptable return with risk
- **< 0.0**: Poor return with risk
- ** Use**:
- **comparison of strategies**: Choice of a better trade strategy
- ** Risk assessment**: Understanding the return/risk ratio
- **Optification of Portfolio**: Risk balance and return

**function max_drawdown:**
- ** Designation**: Measurement of the maximum draught of the Portfolio
- **parameters**:
**/ `cumulative_returns'**: Cumulative returns (cumulative)
- **Formoula**: `min((cumulative_returns-peak) / peak)'
- ** Interpretation**:
- **> -0.1**: Very low draught (< 10%)
- **-0.1 to -0.2**: Low draught (10-20%)
**-0.2 to -0.3**: Moderate draught (20-30 per cent)
- **< -0.3**: High draught (> 30%)
- ** Use**:
- **Manage risk**: Control of maximum loss
- **comparison of strategies**: Choice of less risky strategies
- ** Optimization**: configurization of parameters for the reduction of precipitation

**function calmar_ratio:**
- ** Designation**: Measurement of yield relative to maximum draught
- **parameters**:
- **'returns'**: Income Massive
- ** `max_d'**: Maximum draught (negative number)
- **Formoula**: `annual_return / abs(max_ddd)'
- ** Interpretation**:
- **> 2.0**: Excellent rate of return on draught
- **1.0-2.0**: Good rate of return on tarmac
**0.5-1.0**: Acceptable rate of return on draught
- **< 0.5**: Poor rate of return on landing
- ** Use**:
- **comparison of strategies**: Choice of strategies with better return/gap ratio
- ** Quality assessment**: Understanding the effectiveness of risk management
- ** Optimization**: configurization of parameters for improving the ratio

♪ Monitoring metric

*## Real-time metric tracking

```python
import logging
from datetime import datetime

class MetricsLogger:
 def __init__(self, log_file='metrics.log'):
 self.log_file = log_file
 self.metrics_history = []

 def log_metrics(self, metrics_dict):
""Logstrance Meterick."
 timestamp = datetime.now()
 metrics_dict['timestamp'] = timestamp
 self.metrics_history.append(metrics_dict)

# Recording in file
 with open(self.log_file, 'a') as f:
 f.write(f"{timestamp}: {metrics_dict}\n")

 def get_metrics_trend(self, metric_name):
"Getting a trend of metrics""
 return [m[metric_name] for m in self.metrics_history if metric_name in m]

# Use
metrics_logger = MetricsLogger()

# Logslation of metric
metrics = {
 'accuracy': 0.85,
 'f1_score': 0.82,
 'roc_auc': 0.88
}
metrics_logger.log_metrics(metrics)
```

** Detailed describe parameters Monitoringa metric:**

**Class MetricsLogger:**
- ** Designation**: Logs and tracking of real-time metrics
- **parameters of design**:
- **'log_file'**: Path to log file (on default 'metrics.log')
- **methods**:
- **'log_metrics(metrics_dict)'**: Metric Logs
- **'get_metrics_trind(metric_name)'**: Obtaining trend metrics
- **parameters log_metrics**:
**'metrics_dict'**: dictionary with metrics and their values
- **parameters get_metrics_trend**:
- **'metric_name'**: Name of metrics for trend
- **Return value**: List values of metrics in time
- ** Use**:
- **Monitorizing quality**: Monitoring model quality change
- ** Identification of problems**: Detection of degradation performance
- ** Trends Analysis**: Understanding the dynamics of metrics
- **Reportability**: quality review reports

♪ ♪ Alerates on metrics

```python
class MetricsAlert:
 def __init__(self, threshold=0.8, metric_name='accuracy'):
 self.threshold = threshold
 self.metric_name = metric_name

 def check_alert(self, current_metric):
"Check Alert."
 if current_metric < self.threshold:
 print(f"ALERT: {self.metric_name} = {current_metric} < {self.threshold}")
 return True
 return False

# Use
alert = MetricsAlert(threshold=0.8, metric_name='accuracy')
if alert.check_alert(0.75):
# Sending notes
 pass
```

**/ Detailed descrie parameters of allerates on metrics: **/

**Class MetricsAlert:**
- ** Designation**: cut allerates when the quality of the metric falls
- **parameters of design**:
** `threshold'**: threshold value metrics (on default 0.8)
** `metric_name'**: Name of metrics for Monitoring (on default 'accuracy')
- **methods**:
- **'chesk_alert(current_metric)'**: kheck allert
- **parameters check_alert**:
- **'urrent_metric'**: Current value of metrics
- **Return value**: True if allergic to Workingle, False if not
- ** Use**:
- **Monitorizing quality**: Automatic problem detection
- **notification**: Sending allerates when quality falls
** Control**: Maintenance of the quality of the model on a given level
- ** Automation**: Automatic Response on Problem

## examples using metrics

<img src="images/optimized/production_architecture.png" alt="examples using metrics" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Figure 6: Practical uses of metrics in real projects*

* Why are practical examples important? ** Because they show how to apply metrics in real tasks:

- ** Selection of metric on task type**: Classification vs regression vs ranking
- ** Interpretation of results**: How to understand metric values
- **comparison models**: How to compare different algorithms
- **Monitoring in sales**: How to track quality in real time
- ** Business-metrics**: Technical metrics with business outcomes
- **A/B testing**: How to use devices for testing

### Full example model evaluation

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# data quality
X, y = make_classification(
 n_samples=10000,
 n_features=20,
 n_informative=15,
 n_redundant=5,
 n_classes=2,
 random_state=42
)

data = pd.dataFrame(X, columns=[f'feature_{i}' for i in range(20)])
data['target'] = y

# Data sharing
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# creative and model learning
predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy'
)

predictor.fit(train_data, time_limit=300)

# Premonition
predictions = predictor.predict(test_data)
probabilities = predictor.predict_proba(test_data)

# Quality assessment
performance = predictor.evaluate(test_data)
print("Performance Metrics:")
for metric, value in performance.items():
 print(f"{metric}: {value:.4f}")

# Leaderboard
leaderboard = predictor.leaderboard(test_data)
print("\nLeaderboard:")
print(leaderboard)

# The importance of signs
feature_importance = predictor.feature_importance()
print("\nFeature importance:")
print(feature_importance.head(10))

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# ROC curve
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(test_data['target'], probabilities[1])
roc_auc = auc(fpr, tpr)
axes[0, 0].plot(fpr, tpr, label=f'ROC AUC = {roc_auc:.3f}')
axes[0, 0].plot([0, 1], [0, 1], 'k--')
axes[0, 0].set_xlabel('False Positive Rate')
axes[0, 0].set_ylabel('True Positive Rate')
axes[0, 0].set_title('ROC Curve')
axes[0, 0].legend()

# Precion-Recall curve
from sklearn.metrics import precision_recall_curve
precision, recall, _ = precision_recall_curve(test_data['target'], probabilities[1])
axes[0, 1].plot(recall, precision)
axes[0, 1].set_xlabel('Recall')
axes[0, 1].set_ylabel('Precision')
axes[0, 1].set_title('Precision-Recall Curve')

# A matrix of errors
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(test_data['target'], predictions)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 0])
axes[1, 0].set_title('Confusion Matrix')

# The importance of signs
feature_importance.head(10).plot(kind='barh', ax=axes[1, 1])
axes[1, 1].set_title('Top 10 Feature importance')

plt.tight_layout()
plt.show()
```

## Next steps

After learning with metrics, go to:
- [Methods of validation](./05_validation.md)
- [Selled by default](./06_production.md)
- [model re-training](./07_retraining.md)
