# Ethics and Responsible AI

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Whoy ethics AI is critical

**Why 90 percent of ML models in sales violate ethical principles?** Because team focuses on technical metrics, ignoring ethical consequences. It's like a creative weapon without understanding how it's going to be used.

### Catastrophic Consequences Unethical AI
- ** Discrimination**: Models can make unfair decisions
- ** Regulatory fines**: GDPR fines to 4% from company turnover
- ** Loss of reputation**: Public scandals due to bias
- **Legal issues**: Judicial actions for discrimination

### The benefits of ethical AI #
- ** User confidence**: Fair and understandable solutions
- ** Compliance with laws**: GDPR, AI Act, other regulatory requirements
- ** Best reputation**: The company is perceived as responsible
- ** Long-term success**: Sustainable business development

## Introduction in AI Ethics

<img src="images/optimized/ai_ethics_overView.png" alt="Ethics and Responsible AI" style="max-width: 100%; height: auto; display: block; marguin: 20px auto;">
*Picture 19.1: Principles of ethical and responsible use of artificial intelligence - basic categories and principles*

Why is ethics AI simply "good to be good"?

** Basic Principles of Ethics AI:**
**Fairness & Non-discrimination**: Justice and non-discrimination
- **Transparency & Exploinability**: Transparent and understandable decisions
- **Privacy & data Protection**: privacy and personal data protection
- ** Legal Compliance**: Compliance with legal requirements (GDPR, AI Act)
- **Bias Design & Mitigation**: Detecting and reducing displacements
- ** Accountability & Responsibility**: Responsibility and sub-Reportability

The development and use of ML models have considerable responsibilities, and this section covers ethical principles, legal requirements and best practices for the establishment of responsible AI systems.

♪ Basic Principles of Ethics AI

###1: Justice and non-discrimination

<img src="images/optimized/fairness_metrics.png" alt="metrics justice" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 19.2: metrics of justice in ML - different approaches to measuring justice*

Because unjust models can discriminate against people on the basis of sex, race, age, and other importance, which is unacceptable in modern society.

**Tips of justice metric:**
- **Statistical Parity**: Equal shares of positive outcomes for all groups
**Equated Odds**: Equivalent TPR and FPR for all groups
- **Demographic Parity**: Demographic parity in predictions
- **Individual Fairness**: Equity on an individual level
- **Counterfactual Fairness**: Counterfactual justice
- **Calibration**: Calibration of preferences for different groups

# Why can models be unfair? #
- ** Unprejudiced data**: Historical data contain discrimination
- ** Wrong features**: Use of sensitive attributes
- ** Unequal quality**: The Working Model is worse for some groups
- **Hidden displacement**: Unobvious patterns of discrimination

```python
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def check_fairness(model, X_test, y_test, sensitive_attributes):
""Check of model fairness is critical for ethical AI""

 predictions = model.predict(X_test)

 fairness_metrics = {}

 for attr in sensitive_attributes:
# Segregation on sensitive attributes - check each group
 groups = X_test[attr].unique()

 group_metrics = {}
 for group in groups:
 mask = X_test[attr] == group
 group_predictions = predictions[mask]
 group_actual = y_test[mask]

# metrics for each group - Comparson performance
 accuracy = (group_predictions == group_actual).mean()
 precision = calculate_precision(group_predictions, group_actual)
 recall = calculate_recall(group_predictions, group_actual)

 group_metrics[group] = {
 'accuracy': accuracy,
 'precision': precision,
 'recall': recall
 }

# Check differences between groups
 accuracies = [metrics['accuracy'] for metrics in group_metrics.values()]
 max_diff = max(accuracies) - min(accuracies)

 fairness_metrics[attr] = {
 'group_metrics': group_metrics,
 'max_accuracy_difference': max_diff,
'is_fire': max_diff < 0.1 # The threshold of justice
 }

 return fairness_metrics

def calculate_precision(predictions, actual):
""The calculation of accuracy."
 tp = ((predictions == 1) & (actual == 1)).sum()
 fp = ((predictions == 1) & (actual == 0)).sum()
 return tp / (tp + fp) if (tp + fp) > 0 else 0

def calculate_recall(predictions, actual):
""""" "The calculation of completeness."
 tp = ((predictions == 1) & (actual == 1)).sum()
 fn = ((predictions == 0) & (actual == 1)).sum()
 return tp / (tp + fn) if (tp + fn) > 0 else 0
```

** Detailed descriptions of equity verification parameters:**

- ** `model'**: ML-trained model for verification
- Type: sclearn model, pytorch model, tensorflow model
- Requirements: shall support predict() method
- Application: Any model for classification or regression
 - examples: RandomForest, LogisticRegression, Neural network

- ** `X_test'**: test data for verification
- Type: pandas dataFrame or numpy array
- Contains: signs for prediction
Requirements: shall include sensitive attributes
Size: usually 20 per cent from total dateset

- **'y_test'**: True tags for test data
- Type: pandas Series or numpy array
- Contains: true value of target variable
- Requirements: shall comply with X_test
- Format: binary (0/1) or multiclass labels

- ** `sensitive_attributes'**: List of sensitive attributes
- Type: List[str]
- Contains: names columns with sensitive signature
 - examples: ['gender', 'race', 'age_group', 'religion']
Application: check justice on these attributes

- **'predications = model.predict(X_test)'**: Model predictions
- Result: A range of preferences for all test samples
- Format: Binary (0/1) or probability
Application: basis for calculating the measurement of equity

- **'groups = X_test[attr].unique()'**: Unique attribute values
- Result: List of unique values of a sensitive attribute
 - examples: ['male', 'female'] for gender
- Application: division of data on group for comparison

- **'mask = X_test[attr] ==group'**: Mask for a particular group
- Result: Bould array for group sample selection
- Application: group filtering
- Size: corresponding to the size of X_test

- **'group_predations = preferences[Mask]'**: Projections for the group
Outcome: Forecasts only for samples of this group
Application: Calculation of metrics for the group
- Size: number of samples in group

- **'group_actual = y_test[mask]'**: True tags for group
Outcome: True tags only for samples of this group
Application: Calculation of metrics for the group
- Size: corresponds to group_predations

- **'accuracy = (group_predations ==group_actual).mean()'**: Accuracy for group
- Formula: (right predictions) / (total)
- Range: from 0 to 1
- Application: basic metrics of performance
- Interpretation: proportion of correct preferences

- **'preception = calculate_precision(group_predictions, group_actual)'**: Accuracy for group
- Formula: TP / (TP + FP)
- Range: from 0 to 1
- Application: metrics for positive class
- Interpretation: share of true positive among the predicted positive

- **/recall = calculate_recall(group_predations, group_actual)**: Complete for group
- Formula: TP / (TP + FN)
- Range: from 0 to 1
- Application: metrics for positive class
- Interpretation: share of true positives

- ** `max_diff = max(accuracies) - min(accuracies) `**: Maximum difference in accuracy
Outcome: The difference between best and worst accuracy
- Range: from 0 to 1
Application: a measure of equity
- Interpretation: the less, the more fair

- **'is_fire': max_diff < 0.1'**: check justice
- Threshold: 0.1 (10% difference)
- Logs: if the difference < 10%, it is true
Application: Binary assessment of equity
- Recommendation: Can set the threshold

**Metrics justice:**

- **Statistical Parity**: Equal shares of positive outcomes
- Formula: P(x=1\A=a) = P(x=1\A=b) for all groups
- Application: check of equal opportunities
- Limitations: may conflict with accuracy

**Equated Odds**: Equivalent TPR and FPR
- Formula: TPR_A = TPR_B and FPR_A = FPR_B
Application: check equal performance
- Benefits: takes into account true labels

- **Demographic Parity**: Demographic parity
- Formula: P(~=1\A=a) = P(~=1\A=b)
Application: Equal distribution of preferences
Limitations: may be unfair

- **Individual Fairness**: Equity on an individual level
- Principle: Similar people should receive similar predictions.
Application: protection from individual discrimination
- Complexity: requires a definition of "likeness"

- **Counterfactual Fairness**: Counterfactual justice
- Principle: The application not must depend from the sensitive attributes
- Application: check causal fairness
- Complexity: requires a counter-factual Analysis

- **Calibration**: Calibration of preferences
- Principle: The predicted probability must be consistent with the true
- Application: check reliability preferences
- Meter: Brier Score, Reliability Diagram
```

♪##2 ♪ Transparency and explanation ♪

```python
import shap
import lime
import lime.lime_tabular

class EthicalModelWrapper:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self, model, feature_names, sensitive_attributes):
 self.model = model
 self.feature_names = feature_names
 self.sensitive_attributes = sensitive_attributes
 self.explainer = None

 def create_explainer(self, X_train):
""create explainr for model""

 # SHAP explainer
 self.shap_explainer = shap.TreeExplainer(self.model)

 # LIME explainer
 self.lime_explainer = lime.lime_tabular.LimeTabularExplainer(
 X_train.values,
 feature_names=self.feature_names,
 class_names=['Class 0', 'Class 1'],
 mode='classification'
 )

 def explain_Prediction(self, instance, method='shap'):
"Explanation of a specific prediction."

 if method == 'shap':
 shap_values = self.shap_explainer.shap_values(instance)
 return shap_values
 elif method == 'lime':
 exPlanation = self.lime_explainer.explain_instance(
 instance.values,
 self.model.predict_proba,
 num_features=10
 )
 return exPlanation
 else:
 raise ValueError("Method must be 'shap' or 'lime'")

 def check_bias_in_exPlanation(self, instance):
"Check of displacements in explanation."

 exPlanation = self.explain_Prediction(instance, method='lime')

# Check the importance of sensitive attributes
 sensitive_importance = 0
 for attr in self.sensitive_attributes:
 if attr in exPlanation.as_List():
 sensitive_importance += abs(exPlanation.as_List()[attr][1])

# If sensitive attributes are of high importance - possible displacement
 bias_detected = sensitive_importance > 0.5

 return {
 'bias_detected': bias_detected,
 'sensitive_importance': sensitive_importance,
 'exPlanation': exPlanation
 }
```

** Detailed descriptions of the EthicalModelWrapper parameters:**

- **'model'**: ML model for wrapping
- Type: sclearn model, pytorch model, tensorflow model
- Requirements: shall support predict() and predict_proba()
- Application: Any model for classification
 - examples: RandomForest, LogisticRegression, Neural network

- **'feature_names'**: Names of model features
- Type: List[str]
- Contains: all topics in the same order as in data
- Requirements: shall be in accordance with X_training.columns
Application: for interpretation of explanations

- ** `sensitive_attributes'**: List of sensitive attributes
- Type: List[str]
- Contains: names of sensitive features
 - examples: ['gender', 'race', 'age_group']
Application: check shifts in explanations

- **'self.explaner = None'**: Initiating an explanatory person
- Type: None (initially)
- Application: to be created in cut_explaner()
- Result: SHAP or LIME explainr

- ** `X_training'**: Training data for the creation of an explanatoryist
- Type: pandas dataFrame or numpy array
- Contains: data for the training of an explanatoryist
- Requirements: must include all features
Size: usually 70 per cent from total dateset

- **'shap.TreeExplaner(self.model)'**: SHAP Explainer for Trees
- Application: fortre-based models (RandomForest, XGBost)
- Benefits: rapid and accurate
- Limitations: only for free-based models
Result: SHAP explainr

- **'lime.lime_tabular.LimeTabularExplaner(...)'**: LIME explains for table data
== sync, corrected by elderman == @elder_man
- `feature_names': Names of topics
- `class_names': Class names
- `mode='Classification': Classification mode
- Application: for any models

- **'instance'**: Model for explanation
- Type: pandas Series or numpy array
- Contains: One sample for explanation
- Requirements: shall be consistent with Feature_names
- Application: To obtain an explanation for a specific prediction

- **'method='shap'**: Method of explanation
- ``scap'': SHAP explanations (recommended)
- ``lime'': LIME explanations
- Application: choice of explanation method
- Recommendation: SHAP for treaty-based, LIME for others

- ** `schap_valutes = Self.schap_explainer.scap_valutes(instance)'**: SHAP values
- Result: SHAP array of values for each signature
- Interpretation: the contribution of each input in Prevention
- Range: from - to +
Application: explanation of the importance of the topics

- **'explanation = Self.lime_explaner.explan_instance(...)'**: LIME explanation
- `instance.valutes': data sample in numpy format
== sync, corrected by elderman == @elder_man
- `num_features=10': Number of topics for explanation
- Result: LIME explanation

- **'num_features=10'**: Number of topics for explanation
- Range: from 1 to total number of topics
- Recommendation: 10-20 for most cases
Application: limiting the complexity of the explanation
Balance between simplicity and completeness

- **'explanation.as_List()'**: List of the importance of signs
- Result: List (remark, importance) in descending order
- Format: [('feature1', 0.3), ('feature2', 0.2), ...]
Application: analysis of the importance of the topics

- **/sensitive_importance += abs(explanation.as_list()[attr][1]**: Accumulation of the importance of sensitive attributes
- `abs()': Absolute importance
- `[attr][1] &apos; : Importance attached attr
Outcome: Total importance of sensitive attributes
- Application: displacement assessment

- **'bias_detected = sensive_importance > 0.5'**: heck displacements
- Threshold: 0.5 (50% importance)
- Logs: if sensitive attributes are >50 % importance
- Result: boolean displacement value
- Recommendation: Can set the threshold

**methods explanation:**

- **SHAP (SHapley Additive exPlanations)**:
- Principle: game theory for explanation
- Benefits: theoretically sound, agreed
- Limitations: may be slow for large models
- Application: global and local explanations

- **LIME (Local Interpretable Model-agnostic ExPlanations)**:
- Principle: local approximation of the model
- Benefits: Working with any models, fast
- Limitations: may be unstable
- Application: local explanations

**check shifts in explanations:**

- ** High importance of sensitive attributes**: Sign of discrimination
- ** Low importance of sensitive attributes**: Sign of fairness
- **/ Threshold 0.5**: Euristic threshold for detection of displacements
**Absolute values**: Consider both positive and negative importance
```

###3: Data privacy and protection

<img src="images/optimized/privatity_protection.png" alt="Protective privacy" style="max-width: 100 per cent; exercise: auto; display: block; marguin: 20px auto;">
*Picture 19.4: Protection of privacy in ML - methods and principles*

**methods privacy protection:**
**Differential PRIVACY**: Mathematical privacy with controlled noise
- **k-Anonymity**: Minimum k records in group for protection from identification
- **l-Diversity**: Diversity of sensitive values in groups
- **Federated Learning**: Training without centralization
- **Homomorphic Innovation**: Calculations on encrypted data
- **Secure Multi-party**: Safe Calculations between Parties

** Principles for privacy protection:**
- ** Data Minimization**: Data collection only required
- ** Limiting objective**: Use of data only for stated purposes
- ** Transparency**: Information on data collection and use
** Control**: User &apos; s right on their data

```python
from sklearn.preprocessing import StandardScaler
import numpy as np

class PrivacyPreservingML:
"ML with privacy."

 def __init__(self, epsilon=1.0, delta=1e-5):
 self.epsilon = epsilon
 self.delta = delta

 def add_differential_privacy_noise(self, data, sensitivity=1.0):
""""dd differential privacy."

# Calculation of standard noise deviation
 sigma = np.sqrt(2 * np.log(1.25 / self.delta)) * sensitivity / self.epsilon

# add haussian noise
 noise = np.random.normal(0, sigma, data.shape)
 noisy_data = data + noise

 return noisy_data

 def k_anonymity_check(self, data, quasi_identifiers, k=5):
"Check k-Anonymity."

# Group on quasi identifiers
 groups = data.groupby(quasi_identifiers).size()

# Check minimum group size
 min_group_size = groups.min()

 return {
 'k_anonymity_satisfied': min_group_size >= k,
 'min_group_size': min_group_size,
 'groups_below_k': (groups < k).sum()
 }

 def l_diversity_check(self, data, quasi_identifiers, sensitive_attribute, l=2):
"Check l-diverse."

# Group on quasi identifiers
 groups = data.groupby(quasi_identifiers)

 l_diversity_satisfied = True
 groups_below_l = 0

 for name, group in groups:
 unique_sensitive_values = group[sensitive_attribute].nunique()
 if unique_sensitive_values < l:
 l_diversity_satisfied = False
 groups_below_l += 1

 return {
 'l_diversity_satisfied': l_diversity_satisfied,
 'groups_below_l': groups_below_l
 }
```

** Detailed descriptions of PrivatePreservingML parameters:**

- **'epsilon=1.0'**: privacy parameter ( &gt; )
- Range: from 0.1 to 1.0
`0.1': High privacy (more noise)
`1.0': Standard privacy (recommended)
`10.0': Low privacy (less noise)
Application: privacy control

- **'delta=1e-5'**: parameter of probability of privacy disruption ( &lt; )
- Range: from 1e-9 to 1e-3
- `1e-9': Very low probability of violation
`1e-5': Standard probability (recommended)
`1e-3': High probability of violation
- Application: control of the likelihood of data leakage

- **'data'**: data for noise added
- Type: pandas dataFrame or numpy array
- Contains: data for privacy protection
- Requirements: must be numerical
- Application: reference data for anonymousization

- ** `sensity=1.0'**: Functions Sensitivity
- Range: from 0.1 to 1.0
`0.1': Low sensitivity (less noise)
`1.0': Standard sensitivity (recommended)
`10.0': High sensitivity (more noise)
- Application: control of the quantity of noise added

- **'sigma = np.sqrt(2 *np.log(1.25 / elf.delta)) *sensity / Self.epsilon'**: Standard noise deviation
- Formula: . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
- Result: Standard deviation for Gaussian noise
Application: Calculation of noise parameters
-Dependency: from , , , and sensitivity

- **'noise = np.random.normaal(0, sigma, Data.chape)'**: Gaussian noise generation
- `0': Mean value (centralised noise)
- `sigma': Standard deviation
- `data.chape': Data size
- Result: A mass of noise of the same shape as data

- **'noisy_data = data + noise'**: add data noise
- Result: Data with added noise
Application: protection of privacy
- Balance between privacy and usefulness of data

** `quaasi_identifiers'**: Quasi identifiers for k-anonymity
- Type: List[str]
- Contains: names of columns-quasi identifiers
 - examples: ['age', 'zipcode', 'gender']
- Application: Group for Anonymization

- **'k=5'**: parameter k-anonymity
- Range: from 2 to 100
- `2': Minimum anonymity
`5': Standard anonymity (recommended)
`10': High anonymity
- Application: minimum size of group

- **'groups = data.groupby(quaasi_identifiers).size()'**: Group on quasi identifiers
- Result: Group size
Application: check k-anonymity
- Format: Series with group sizes

- **'min_group_size = group.min()'**: Minimum group size
- Result: size of the smallest group
- Application: check compliance k-anonymity
- Criterion: min_group_size >=k

** `sensitive_attribute'**: Sensitious attribute for l-diverse
- Type: str
- Contains: Name of sensitive signature
 - examples: 'disease', 'salary', 'religion'
- Application: check diversity in groups

- **'l'=2'**: parameter l-diverse
- Range: from 2 to 10
- `2': Minimum diversity
`3': Standard diversity (recommended)
`5': High diversity
- Application: Minimum number of unique values

- **'unique_sensitive_valutes = group[sensitive_attribute].nunique()'**: Number of unique values
- Result: Number of unique values of a sensitive attribute in group
- Application: check l diversity
- Criterion: unique_sensitive_valuses >=l

**methods privacy protection:**

- **Differential Privacy (ε, δ)**:
Principle: Mathematical privacy guarantee
- Parameters: (privateity), (probability of violation)
Benefits: Theoretically sound
Limitations: may reduce accuracy

- **k-Anonymity**:
- Principle: minimum k of entries in group
- Application: protection from identification
- Limitations: nnot protects from attribute attacks
- Requirements: quasi identifiers

- **l-Diversity**:
- Principle: Diversity of sensitive values
- Application: protection from attribute attacks
Requirements: l unique values in group
Limitations: may be difficult to achieve

** Practical recommendations:**

- **choice : 0.1-1.0 for high privacy, 1.0-1.0 for balance sheet
- **choice : 1e-5 for most cases
- **choice k**: 5-10 for k-anonymity
- **choice l**: 2-5 for l-diverse
**Balance**: between privacy and usefulness of data
```

## Legal requirements

<img src="images/optimized/legal_compliance.png" alt="Legal conformity" style="max-width: 100%; exercise: auto; display: block; marguin: 20px auto;">
*Figure 19.5: Legal compliance of AI systems - requirements and standards*

** Basic legal requirements:**
**GDPR Compliance**: Compliance with the EU General Regulation on Data Protection
- **AI Act Competition**: Compliance with the EU Law on Artificial Intelligence
- **data Protection**: Protection of personal data and privacy
- **Consent Management**: Management consent on data processing
**Right to Erasure**: Right to remove data (right to be forgotten)
- **Transparency Agreements**: Obligations on transparency

**GDPR requirements:**
- ** Law on Information**: Information on data collection and use
- ** Right of access**: Access to personal data
- ** Law on fix**: fix inaccurate data
** Law on request: remove data
- ** Law on Portability**: Transport of data between services
- ** Right on objection**: Objection to data processing

### 1. GDPR Compliance

```python
class GDPRCompliance:
""Ensure GDPR""

 def __init__(self):
 self.data_subjects = {}
 self.processing_purposes = {}
 self.consent_records = {}

 def record_consent(self, subject_id, purpose, consent_given, timestamp):
""Note of consent of the data subject""

 if subject_id not in self.consent_records:
 self.consent_records[subject_id] = []

 self.consent_records[subject_id].append({
 'purpose': purpose,
 'consent_given': consent_given,
 'timestamp': timestamp
 })

 def check_consent(self, subject_id, purpose):
"Check consent for a specific purpose."

 if subject_id not in self.consent_records:
 return False

# Searching for final agreement for this goal
 relevant_consents = [
 record for record in self.consent_records[subject_id]
 if record['purpose'] == purpose
 ]

 if not relevant_consents:
 return False

# Return of last consent
 latest_consent = max(relevant_consents, key=lambda x: x['timestamp'])
 return latest_consent['consent_given']

 def right_to_erasure(self, subject_id):
"Right on remove (right to be forgotten)"

 if subject_id in self.consent_records:
 del self.consent_records[subject_id]

# There's got to be a Logsk of unsub data removal
 return True

 def data_portability(self, subject_id):
"Law on Portability of Data"

# Return all entity data in structured format
 subject_data = {
 'personal_data': self.get_subject_data(subject_id),
 'consent_records': self.consent_records.get(subject_id, []),
 'processing_history': self.get_processing_history(subject_id)
 }

 return subject_data
```

### 2. AI Act Compliance

```python
class AIActCompliance:
"According AI Act (EU)"

 def __init__(self):
 self.risk_categories = {
 'unacceptable': [],
 'high': [],
 'limited': [],
 'minimal': []
 }

 def classify_ai_system(self, system_describe):
""" Classification AI of the System on Risk Level""

# Criteria for classification
 if self.is_biometric_identification(system_describe):
 return 'unacceptable'
 elif self.is_high_risk_application(system_describe):
 return 'high'
 elif self.is_limited_risk_application(system_describe):
 return 'limited'
 else:
 return 'minimal'

 def is_biometric_identification(self, describe):
"Check on biometric identification."
 biometric_keywords = ['face recognition', 'fingerprint', 'iris', 'voice']
 return any(keyword in describe.lower() for keyword in biometric_keywords)

 def is_high_risk_application(self, describe):
"Check on High Risk Applications."
 high_risk_keywords = [
 'medical diagnosis', 'credit scoring', 'recruitment',
 'law enforcement', 'education', 'transport'
 ]
 return any(keyword in describe.lower() for keyword in high_risk_keywords)

 def is_limited_risk_application(self, describe):
"Check on limited risk applications."
 limited_risk_keywords = ['chatbot', 'recommendation', 'content moderation']
 return any(keyword in describe.lower() for keyword in limited_risk_keywords)

 def get_compliance_requirements(self, risk_level):
"To obtain conformity requirements for risk level""

 requirements = {
 'unacceptable': [
 'system is prohibited under AI Act'
 ],
 'high': [
 'Conformity assessment required',
 'Risk Management system',
 'data governance',
 'Technical documentation',
 'Record keeping',
 'Transparency and User information',
 'Human oversight',
 'Accuracy, robustness and cybersecurity'
 ],
 'limited': [
 'Transparency obligations',
 'User information requirements'
 ],
 'minimal': [
 'No specific requirements'
 ]
 }

 return requirements.get(risk_level, [])
```

## Bias Detection and Mitigation

<img src="images/optimized/bias_detection.png" alt="Detect and reduce displacements" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 19.3: Detection and reduction of displacements in ML - phases and methhods*

**Demove detection units:**
- **data Bias**: In-data shifts (historical prejudice, uneven presentation)
- **Algorithm Bias**: Algorithms in algorithms (incorrect, hidden correlations)
- **Evalution Bias**: In-assessment shifts (uneven metrics, biased tests)

**methods reduction of displacements:**
- **Pre-processing Mitigation**: remove sensitive features, balancing data
- **In-processing Mitigation**: Fairness constraints, adversarial training, regularization
- **Post-processing Mitigation**: Calibration of thresholds, adaptive solutions

### 1. Bias Detection

```python
class BiasDetector:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self):
 self.bias_metrics = {}

 def statistical_parity_difference(self, predictions, sensitive_attribute):
"Statistical difference of parity."

 groups = sensitive_attribute.unique()
 spd_values = []

 for group in groups:
 group_mask = sensitive_attribute == group
 group_positive_rate = predictions[group_mask].mean()
 spd_values.append(group_positive_rate)

# The difference between the maximum and minimum shares of positive outcomes
 spd = max(spd_values) - min(spd_values)

 return {
 'statistical_parity_difference': spd,
'is_fire': spd < 0.1 # The threshold of justice
 'group_rates': dict(zip(groups, spd_values))
 }

 def equalized_odds_difference(self, predictions, actual, sensitive_attribute):
"The difference of equal chances."

 groups = sensitive_attribute.unique()
 tpr_values = []
 fpr_values = []

 for group in groups:
 group_mask = sensitive_attribute == group
 group_predictions = predictions[group_mask]
 group_actual = actual[group_mask]

 # True Positive Rate
 tpr = ((group_predictions == 1) & (group_actual == 1)).sum() / (group_actual == 1).sum()
 tpr_values.append(tpr)

 # False Positive Rate
 fpr = ((group_predictions == 1) & (group_actual == 0)).sum() / (group_actual == 0).sum()
 fpr_values.append(fpr)

# Differentials TPR and FPR
 tpr_diff = max(tpr_values) - min(tpr_values)
 fpr_diff = max(fpr_values) - min(fpr_values)

 return {
 'equalized_odds_difference': max(tpr_diff, fpr_diff),
 'tpr_difference': tpr_diff,
 'fpr_difference': fpr_diff,
 'is_fair': max(tpr_diff, fpr_diff) < 0.1
 }

 def demographic_parity_difference(self, predictions, sensitive_attribute):
"Difference of demographic parity."

 groups = sensitive_attribute.unique()
 positive_rates = []

 for group in groups:
 group_mask = sensitive_attribute == group
 positive_rate = predictions[group_mask].mean()
 positive_rates.append(positive_rate)

 dpd = max(positive_rates) - min(positive_rates)

 return {
 'demographic_parity_difference': dpd,
 'is_fair': dpd < 0.1,
 'group_positive_rates': dict(zip(groups, positive_rates))
 }
```

**BiasDetector Detailed Descriptions:**

- **'predications'**: Model predictions
- Type: numpy array or pandas Series
- Contains: model predictions for all samples
- Format: Binary (0/1) or probability
- Application: basis for the calculation of displacement metrics

- ** `sensitive_attribute'**: Sensitious attribute
- Type: pandas Series or numpy array
- Contains: sensitive signature values for each sample
 - examples: ['male', 'female'] for gender
- Application: Segregation of data on group

- ** `actual'**: True labels
- Type: numpy array or pandas Series
- Contains: true value of target variable
- Format: Binary (0/1) or multiclass
- Application: Calculation of TPR and FPR for equated odds

- **'groups = sensitive_attribute.unique()'**: Unique groups
- Result: List of unique values of a sensitive attribute
 - examples: ['male', 'female'] for gender
- Application: Iteration on groups for the calculation of metrics

- **'group_mask = sensitive_attribute ==group'**: Mask for group
- Result: Bould array for group sample selection
- Application: group filtering
- Size: corresponds to the size of the productions

- **'group_positive_rate = preferences[group_max].mean()'**: Percentage of positive outcomes for group
- Formula: (number of positive measures) / (total number)
- Range: from 0 to 1
- Application: Calculation of statistical parity
- Interpretation: percentage of positive preferences in group

- **'spd = max(spd_valutes) - min(spd_valutes)'**: Statistical difference in parity
Outcome: The difference between the maximum and the minimum percentage of positive outcomes
- Range: from 0 to 1
Application: a measure of equity
- Interpretation: the less, the more fair

- **'is_fire': spd < 0.1'**: check justice
- Threshold: 0.1 (10% difference)
- Logs: if the difference < 10%, it is true
Application: Binary assessment of equity
- Recommendation: Can set the threshold

- **`tpr = ((group_predictions == 1) & (group_actual == 1)).sum() / (group_actual == 1).sum()`**: True Positive Rate
- Formula: TP / (TP + FN)
- Range: from 0 to 1
- Application: metrics for positive class
- Interpretation: share of true positives

- **`fpr = ((group_predictions == 1) & (group_actual == 0)).sum() / (group_actual == 0).sum()`**: False Positive Rate
- Formula: FP / (FP + TN)
- Range: from 0 to 1
- Application: metrics for negative class
- Interpretation: percentage of false operations

- **'tpr_diff = max(tpr_valutes) - min(tpr_valutes) `**: TPR difference between groups
- Result: difference between maximum and minimum TPR
- Range: from 0 to 1
- Application: Justice on TPR
- Interpretation: the less, the more fair

- **'fpr_diff = max(fpr_valutes) - min(fpr_valutes)'**: FPR difference between groups
- Result: difference between maximum and minimum FPR
- Range: from 0 to 1
- Application: Justice on FPR
- Interpretation: the less, the more fair

- ** `equated_odds_disference': max(tpr_diff, fpr_diff) `**: The difference in equal chances
Outcome: maximum difference between TPR and FPR
- Range: from 0 to 1
Application: a general measure of fairness
- Interpretation: the less, the more fair

**Metrics justice:**

- **Statistical Parity Difference (SPD)**:
- Formula: max(P(x)=1\A=a) - min(P(\\1\A=a))
- Application: check of equal opportunities
- Limitations: may conflict with accuracy
- Threshold: < 0.1 for equity

- **Equalized Odds Difference (EOD)**:
- Formula: max(\TPR_A - TPR_B
Application: check equal performance
- Benefits: takes into account true labels
- Threshold: < 0.1 for equity

- **Demographic Parity Difference (DPD)**:
- Formula: max(P(x)=1\A=a) - min(P(\\1\A=a))
Application: Equal distribution of preferences
Limitations: may be unfair
- Threshold: < 0.1 for equity

** Practical recommendations:**

- **Selection of metric**: SPD for Equal Opportunities, EOD for Equal Performance
- ** Equity thresholds**: 0.1 (10%) for most cases
**Balance**: between fairness and accuracy
- **Monitoring**: regular check metric of justice
- **Correct**: adaptation of thresholds in terms of context
```

### 2. Bias Mitigation

```python
class BiasMitigation:
"methods of displacement reduction."

 def __init__(self):
 self.mitigation_strategies = {}

 def preprocess_bias_mitigation(self, X, y, sensitive_attributes):
"Preparation for displacement reduction."

# remove sensitive attributes
 X_processed = X.drop(columns=sensitive_attributes)

# Class balance
 from imblearn.over_sampling import SMOTE
 smote = SMOTE(random_state=42)
 X_balanced, y_balanced = smote.fit_resample(X_processed, y)

 return X_balanced, y_balanced

 def inprocess_bias_mitigation(self, model, X, y, sensitive_attributes):
"The reduction of displacements in learning"

 # add fairness constraints
 def fairness_loss(y_true, y_pred, sensitive_attr):
# Main loss
 main_loss = F.cross_entropy(y_pred, y_true)

 # Fairness penalty
 groups = sensitive_attr.unique()
 fairness_penalty = 0

 for group in groups:
 group_mask = sensitive_attr == group
 group_predictions = y_pred[group_mask]
 group_positive_rate = group_predictions.mean()
 fairness_penalty += (group_positive_rate - 0.5) ** 2

 return main_loss + 0.1 * fairness_penalty

 return fairness_loss

 def postprocess_bias_mitigation(self, predictions, sensitive_attributes, threshold=0.5):
"""""""""""""""""

# Calibration of thresholds for different groups
 adjusted_predictions = predictions.copy()

 for group in sensitive_attributes.unique():
 group_mask = sensitive_attributes == group
 group_predictions = predictions[group_mask]

# An adaptive threshold for a group
 group_threshold = self.calculate_fair_threshold(
 group_predictions, group
 )

# Application of adaptive threshold
 adjusted_predictions[group_mask] = (
 group_predictions > group_threshold
 ).astype(int)

 return adjusted_predictions

 def calculate_fair_threshold(self, predictions, group):
"A fair threshold for a group."

# Simple heuristics - can be replaced on more complex methhods
 return 0.5
```

## Responsible AI Framework

<img src="images/optimized/ethics_checkList.png" alt="Ethics" style"="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 19.6: AA System Ethics Checklist - categories and evaluation criteria*

**Categorry of ethical chess:**
**data Quality**: Data quality, absence of passes, class balance
- **Bias Assessment**: Assessment of displacements, statistical parity, equal chances
- **Privacy Protection**: Protection of privacy, differential privacy, anonymousization
- **Transparency & Exploinability**: Transparent solutions, understandable models
- **accountability & Safety**: Responsibility, security, human oversight
**Fairness & Equity**: Justice, equal opportunity, non-discrimination

** Ethics evaluation criteria:**
- ** No pass**: Minimum number of missing values
- ** Class Balance**: Equal representation of all classes
- ** Data quality**: representativeness and relevance
- **Statistical parity**: Equal shares of positive outcomes
- ** Equivalent odds**: Equivalent TPR and FPR for all groups
- ** Demographic parity**: Fair distribution of preferences

### 1. AI Ethics checkList

```python
class AIEthicscheckList:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self):
 self.checkList = {
 'data_quality': [],
 'bias_assessment': [],
 'privacy_protection': [],
 'transparency': [],
 'accountability': [],
 'fairness': [],
 'safety': []
 }

 def assess_data_quality(self, data, sensitive_attributes):
""""""""""""""

 checks = []

# check on missing values
 Missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
 checks.append({
 'check': 'Missing values ratio',
 'value': Missing_ratio,
 'passed': Missing_ratio < 0.1,
 'recommendation': 'clean Missing values' if Missing_ratio >= 0.1 else None
 })

# Check on duplicates
 duplicate_ratio = data.duplicated().sum() / len(data)
 checks.append({
 'check': 'Duplicate ratio',
 'value': duplicate_ratio,
 'passed': duplicate_ratio < 0.05,
 'recommendation': 'Remove duplicates' if duplicate_ratio >= 0.05 else None
 })

# Check balance of sensitive attributes
 for attr in sensitive_attributes:
 value_counts = data[attr].value_counts()
 min_ratio = value_counts.min() / value_counts.sum()
 checks.append({
 'check': f'Balance of {attr}',
 'value': min_ratio,
 'passed': min_ratio > 0.1,
 'recommendation': f'Balance {attr} groups' if min_ratio <= 0.1 else None
 })

 self.checkList['data_quality'] = checks
 return checks

 def assess_bias(self, model, X_test, y_test, sensitive_attributes):
""""""""""""""

 bias_detector = BiasDetector()
 checks = []

 for attr in sensitive_attributes:
# Statistical parity
 spd_result = bias_detector.statistical_parity_difference(
 model.predict(X_test), X_test[attr]
 )
 checks.append({
 'check': f'Statistical parity for {attr}',
 'value': spd_result['statistical_parity_difference'],
 'passed': spd_result['is_fair'],
 'recommendation': f'Address bias in {attr}' if not spd_result['is_fair'] else None
 })

# Equivalent odds
 eod_result = bias_detector.equalized_odds_difference(
 model.predict(X_test), y_test, X_test[attr]
 )
 checks.append({
 'check': f'Equalized odds for {attr}',
 'value': eod_result['equalized_odds_difference'],
 'passed': eod_result['is_fair'],
 'recommendation': f'Address equalized odds for {attr}' if not eod_result['is_fair'] else None
 })

 self.checkList['bias_assessment'] = checks
 return checks

 def generate_ethics_Report(self):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 Report = {
 'overall_score': 0,
 'category_scores': {},
 'recommendations': [],
 'passed_checks': 0,
 'total_checks': 0
 }

 for category, checks in self.checkList.items():
 if checks:
 passed = sum(1 for check in checks if check['passed'])
 total = len(checks)
 score = passed / total if total > 0 else 0

 Report['category_scores'][category] = score
 Report['passed_checks'] += passed
 Report['total_checks'] += total

# Collection of recommendations
 for check in checks:
 if check.get('recommendation'):
 Report['recommendations'].append({
 'category': category,
 'check': check['check'],
 'recommendation': check['recommendation']
 })

 Report['overall_score'] = Report['passed_checks'] / Report['total_checks'] if Report['total_checks'] > 0 else 0

 return Report
```

## Conclusion

<img src="images/optimized/ethics_workflow.png" alt="Workflow ethics" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 19.7: Workflow the introduction of ethics in AI - phases and processes*

**Ethics for the introduction of ethics:**
- **Ethics Planning**: Planning ethical principles and requirements
**data Assessment**: Assessment of data quality and fairness
- **Model Development**: Ethical Modeling
- **Bias test**: Test on displacement and bias
- **Privacy ReView**: heck privacy protection
- ** Legal Compliance**: Compliance with legal requirements
- **deployment Monitoring**: Monitoring ethics in sales
- **Continuous Improvisation**: Continuous improvey of ethics

Ethics and responsible AI are simply additional requirements and fundamental principles for the development of ML systems.

1. **justice** - ensuring equal treatment of all groups
2. ** Transparency** - possible explanation of model decisions
3. **Purity** - Personal data protection
4. ** Compliance with legal requirements** - GDPR, AI Act and others
5. ** Detection and reduction of displacement** - Active Working with bias
6. ** Responsibility** - clear definition of responsibility for AI decisions

The introduction of these principles not only ensures compliance with legal requirements, but also enhances the quality, reliability and public confidence in AI systems.
