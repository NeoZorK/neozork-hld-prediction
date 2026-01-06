# Advanced themes AutoML

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Whoy advanced themes are critical

**Why do 95% of ML engineers not know about advanced techniques?** Because they focus on basic algorithms, not knowing that modern methhods can produce in 10-100 times better results.

### Problems without knowledge of advanced topics
- **Oldest methhods**: Use technology 5 years ago
- ** Bad results**: not can reach state-of-the-art performance
- ** Loss of competitiveness**: From teams using modern techniques
- **Restricted opportunities**:not can solve complex problems

### The benefits of knowledge of advanced topics
- ** Best results**: State-of-the-art performance
- ** Competitiveness**: Use the most modern methhods
- ** Resolution of complex problems**: Could Work with multimodal data
- ** Innovation**: Can create new solutions

## Introduction in advanced topics

<img src="images/optimized/advanced_topics_overView.png" alt="AutoML topics" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Figure 18.1: Overview of advanced themes and current directions in AutoML - main categories and methods*

**Why advanced topics are the future of ML?** Because they solve problems that cannot be solved by traditional methods: automatic architecture design, learning on small data, multimodal understanding.

** Main categories of advanced topics:**
- **Neural Architectural Search (NAS)**: Automatic search for optimal architectures of neuronetworks
- **Meta-Learning**: Learning how to learn about new challenges
- **Multi-Modal Learning**: Working with different data types simultaneously
- **Federated Learning**: Distributed learning with privacy
- **Continual Learning**: Continuing learning without forgetting previous knowledge
**Quantum Machine Learning**: Use of quantum calculations for ML

This section covers cutting-edge topics and current directions in the areas of automated machine learning, integrating neuroarchic research, meta-learning, multimodal learning and other Cutting-edge technoLogsy.

## Neural Architecture Search (NAS)

<img src="images/optimized/neural_architecture_search.png" alt="Neural Architecture Search" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 18.2: Neural architecture Search - methods automatic search for neuronetworks architecture*

**NAS methods:**
- **DARTS (Differtiable)**: Differentiated gradient descent search
- **ENAS (Efficient)**: Effective RNN search
- **Random Research**: Random Search in Architecture Space
- **Evolutionary Search**: Evolution search with genetic algorithms
- **Reinforce Learning**: Searching through learning with reinforcement
- **Bayesian Optimization**: Bayesian Architecture Optimization

### 1. Differentiable Architecture Search (DARTS)

Why is DARTS a revolution in the design of neuronetworks?

** The benefits of DARTS:**
- **Speed**: in 1000 times faster than random search
-**Quality**: Finds architectures better built by man.
- ** Flexibility**: Can search for any type of transaction
- **Stability**: Workinget with large datasets

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DARTS(nn.Module):
""Differentiable architecture Search - Automatic Design of neuronetworks""

 def __init__(self, input_channels, output_channels, num_ops=8):
 super(DARTS, self).__init__()
 self.input_channels = input_channels
 self.output_channels = output_channels
 self.num_ops = num_ops

# Operations - Candidates for Architecture
 self.ops = nn.ModuleList([
 nn.Conv2d(input_channels, output_channels, 1, bias=False), # 1x1 conv
 nn.Conv2d(input_channels, output_channels, 3, padding=1, bias=False), # 3x3 conv
 nn.Conv2d(input_channels, output_channels, 5, padding=2, bias=False), # 5x5 conv
 nn.MaxPool2d(3, stride=1, padding=1), # Max pooling
 nn.AvgPool2d(3, stride=1, padding=1), # Average pooling
 nn.Identity() if input_channels == output_channels else None, # Identity
 nn.Conv2d(input_channels, output_channels, 3, padding=1, dilation=2, bias=False), # Dilated conv
 nn.Conv2d(input_channels, output_channels, 3, padding=1, dilation=3, bias=False) # Dilated conv
 ])

# Architectural weights - which is optimized
 self.alpha = nn.Parameter(torch.randn(num_ops))

 def forward(self, x):
# Softmax for Architectural Weights - Normalizing Weights
 weights = F.softmax(self.alpha, dim=0)

# A weighted amount of transactions - a combination of all transactions
 output = sum(w * op(x) for w, op in zip(weights, self.ops) if op is not None)

 return output
```

** DARTS Detailed Descriptions: **

- **'input_channels'**: Number of channels
- `3': RGB images (standard)
- `1': Grayscale images
- `4': RGBA images
`64': Interlayers
- `256': Deep layers
- Application: Measuring input data

- ** `output_channels'**: Number of output channels
`64': Standard number for primary layers
- `128': Increased number for middle layers
- `256': A large number for deep layers
- `512': Very large number of for very deep layers
Application: Determination of the capacity of the layer

- **'num_ops=8'**: Number of candidate transactions
`8': Standard quantity (recommended)
`4': Minimum number (rapid education)
- `12': Large quantity (detail search)
- `16': Very large quantity (very detailed search)
Application: Diversity of architectural options

- **'nn.Conv2d(input_channels, output_channels, 1, bias=False)'**: 1x1 fold
- `1': Size of kernel (1x1)
- `bias=False': No offset (recommended)
- Application: point stack for channel changes
- Benefits: rapid, effective

- **'nn.Conv2d(input_channels, output_channels, 3, padding=1, bis=False)'**: 3x3 folding
- `3': Size of kernel (3x3)
- `adding=1': Filling for size preservation
- Application: standard set-up for extraction
- Benefits: balance between quality and speed

- **'nn.Conv2d(input_channels, output_channels, 5, padding=2, bis=False)'**: 5x5 folding
- `5': Size of kernel (5x5)
- `adding=2': Filling for size preservation
- Application: a large stack for global features
- Benefits: capture of the big pathers

- **`nn.MaxPool2d(3, stride=1, padding=1)`**: Max pooling
- `3': Window size (3x3)
- `stride=1': Step 1 for size preservation
- `adding=1': Filling for size preservation
- Application: removal of maximum values
- Benefits: invariance to shifts

- **`nn.AvgPool2d(3, stride=1, padding=1)`**: Average pooling
- `3': Window size (3x3)
- `stride=1': Step 1 for size preservation
- `adding=1': Filling for size preservation
- Application: recovery of mean values
- Benefits: noise smoothing

- **'nn.Identity()'**: Equivalent operation
- Application: when input_channels ==output_channels
- Benefits: Data missing without change
- Use: for kip connections

- **'dilation=2'**: Dilated folding
- `2': Dilatation factor
- Application: increase of prescription field
- Benefits: capture of large pathers without increasing parameters

- **'dilation=3'**: Dilated folding
- `3': Dilatation factor
- Application: an even larger prescription field
- Benefits: Very large pathers

- **'self.alpha = nn. Parameter(torch.randn(num_ops)'**: Architectural weights
- `torch.randn(num_ops)': Accidental initialization
- `nn.Parameter': Training parameters
Application: Optimizing architecture
- Range: from - to + - (normalized through softmax)

- **'F.softmax(self.alpha, dim=0)'**: Normalization of weights
- `dim=0': Normalization on operations
Results: weights from 0 to 1, sum = 1
- Application: Probability distribution on operations
- Interpretation: the importance of each operation

# The use of DARTS
def search_architecture(train_loader, val_loader, epochs=50):
"Looking for architecture with help DARTS."

 model = DARTS(input_channels=3, output_channels=64)
 optimizer = torch.optim.Adam(model.parameters(), lr=0.025)

 for epoch in range(epochs):
# Update architectural balance
 model.train()
 for batch_idx, (data, target) in enumerate(train_loader):
 optimizer.zero_grad()
 output = model(data)
 loss = F.cross_entropy(output, target)
 loss.backward()
 optimizer.step()

# validation
 model.eval()
 val_loss = 0
 with torch.no_grad():
 for data, target in val_loader:
 output = model(data)
 val_loss += F.cross_entropy(output, target).item()

 print(f'Epoch {epoch}, Validation Loss: {val_loss:.4f}')

 return model
```

** Detailed description of architecture search parameters:**

- **'training_loader'**: Training Data uploader
- Type: DataLoader
- Contained: Batchi (data, Target)
Application: training in architectural balance
- Recommendation: balanced tramps

- **/ `val_loader'**: Validation Data uploader
- Type: DataLoader
- Contained: Batchi (data, Target)
Application: Quality assessment of architecture
Recommendation: independent from train_loader

- **'peochs=50'**: Number of learning eras
`50': Standard quantity (recommended)
- `25': Rapid learning (less accurate)
- `100': Long learning (more precise)
- `200': Very long education (very precise)
Application: monitoring of the time of instruction

- **'input_channels=3'**: Number of entry channels
- `3': RGB images (standard)
- `1': Grayscale images
- `4': RGBA images
- Application: conformity with input data

- **'output_channels=64'**: Number of output channels
`64': Standard number for primary layers
- `32': Less channels (rapid)
- `128': More channels (quality)
- `256': A lot of channels (very good)
Application: balance between speed and quality

- **'torch.optim.Adam(model.parameters(), lr=0.025)'**: Adam Optimizer
- `model.parameters()': All models
- `lr=0.025':Learning rent (recommended for DARTS)
- `0.01': Less Learning Rate (stable)
- `0.05': Larger lightning rent (rapid)
- `0.1': Very large lightning rent (may be unstable)

- **'model.train()'**: Learning mode
- Including: dropout, batch normalitation in training mode
- Disables: Determinated behaviour
Application: activation of training components

- **'optimizer.zero_rad()'**: No gradients
- Clear: accumulated gradients
- Application: preventing the accumulation of gradients
- Mandatory: before each backward pass

**'F.cross_entropy(output, Target)'**: financing losses
- `output': Model predictions
- `target': True tags
- Application: classification
Alternatives: F.mse_loss for regression

- **'loss.backward()'**: Reverse distribution
- Computes gradients on all parameters
- Application: preparation for the updating of weights
- Mandatory: before optimizer.step()

- **'optimizer.step()'**: update parameters
- It's up-to-date.
Application: Optimization of architectural weights
- Result: improve architecture

- **'model.eval()'**: Evaluation mode
- Including: determinized behaviour
- Disables: dropout, batch normalitation in training mode
- Application: Stable assessment on validation

- **'torch.no_grad()'**: Disable the gradients
- Disables: Calculating gradients
- Application: acceleration validation
- Savings: memory and computation

- **'val_loss +=F.cross_entropy(output, Target).item()'**: Accumulation of losses
- `.item()': Conversion in Python flat
- Application: Avoiding the accumulation of gradients
- Result: scalar value of loss
```

### 2. Efficient Neural Architecture Search (ENAS)

```python
class ENAS(nn.Module):
 """Efficient Neural Architecture Search"""

 def __init__(self, num_nodes=5, num_ops=8):
 super(ENAS, self).__init__()
 self.num_nodes = num_nodes
 self.num_ops = num_ops

# Controller (RNN)
 self.controller = nn.LSTM(32, 32, num_layers=2, batch_first=True)
 self.controller_output = nn.Linear(32, num_nodes * num_ops)

# Operations
 self.ops = nn.ModuleList([
 nn.Conv2d(3, 64, 3, padding=1),
 nn.Conv2d(3, 64, 5, padding=2),
 nn.MaxPool2d(3, stride=1, padding=1),
 nn.AvgPool2d(3, stride=1, padding=1),
 nn.Conv2d(3, 64, 1),
 nn.Conv2d(3, 64, 3, padding=1, dilation=2),
 nn.Conv2d(3, 64, 3, padding=1, dilation=3),
 nn.Identity()
 ])

 def sample_architecture(self):
"Sampling Architecture."
# Architectural generation via controller
 hidden = torch.zeros(2, 1, 32) # LSTM hidden state
 outputs = []

 for i in range(self.num_nodes):
 output, hidden = self.controller(torch.randn(1, 1, 32), hidden)
 logits = self.controller_output(output)
 logits = logits.View(self.num_nodes, self.num_ops)
 probs = F.softmax(logits[i], dim=0)
 action = torch.multinomial(probs, 1)
 outputs.append(action.item())

 return outputs

 def forward(self, x, architecture=None):
 if architecture is None:
 architecture = self.sample_architecture()

# Application of architecture
 for i, op_idx in enumerate(architecture):
 x = self.ops[op_idx](x)

 return x
```

** Detailed description of ENAS parameters:**

- **'num_nodes=5'**: Number of nodes in architecture
`5': Standard quantity (recommended)
- `3': Simple architecture (rapid)
- `8': Complex architecture (quality)
- `10': Very complex architecture (very high quality)
- Application: control of architecture complexity

- **'num_ops=8'**: Number of candidate transactions
`8': Standard quantity (recommended)
`4': Minimum number (rapid education)
- `12': Large quantity (detail search)
- `16': Very large quantity (very detailed search)
Application: Diversity of architectural options

- **'nn.LSTM(32, 32, number_layers=2, batch_first=True)'**: LSTM controller
`32': Size of entry and hidden state
- `num_layers=2': Number of layers of LSTM
- `batch_first=True': First dimension - batch
- Application: the generation of architectural solutions
- Benefits: taking into account consistency of decisions

- **'nn.Linear(32, number_nodes*num_ops)'**: Control outlet
- `32': Entrance Size (dimension of Hidden State LSTM)
- `num_nodes * number_ops': Size of output (all possible solutions)
- Application: Transforming Hidden State in Logsta
Outcome: Probability for each transaction in each node

**'torch.zeros(2, 1, 32)'**: Initiating the Hidden State of LSTM
- `2': Number of layers of LSTM
- `1': Batch size (one sample)
`32': Size of hidden state
- Application: Initial state for generation
Outcome: Determinated initialization

**'torch.randn(1, 1, 32)'**: Entry Tensor for LSTM
 - `1`: Batch size
 - `1`: Sequence length
 - `32`: Feature dimension
- Application: input data for controller
Alternatives: Learnable embeddings can be used

- **'logits.View(self.num_nodes,self.num_ops)'**: Change of Logs
- `num_nodes': Number of nodes
- `num_ops': Number of transactions
- Application: Logs on Node Group
- Result: matrix (num_nodes, num_ops)

- **'F.softmax(logits[i], dim=0)'**: Normalization of probabilities
- `logits[i]': Logs for the i-th node
- `dim=0': Normalization on operations
- Result: probability from 0 to 1, sum = 1
- Application: Probability distribution on operations

- **'torch.multiinomial(probs, 1)'**: Sampling operation
- `probs': Probability of operations
- `1': Number of samples
- Result: index of the selected operation
Application: Stochastic choice of operation

- **'action.item()'**: Conversion in Python in
- Transforms: Tensor in Python in
- Application: In-index use
- Result: whole number from 0 to number_ops-1

- **'self.ops[op_idx](x)'**: Application of the selected operation
- `op_idx': index of the selected operation
- `x': input data
- Application: performing a data transaction
- Result: converted data

**Operations ENAS:**

- **'nn.Conv2d(3, 64, 3, padding=1)'**: 3x3 folding
`3': Channels of entry
`64': Exit channels
- `3': Size of the kernel
- `adding=1': Filling for size preservation

- **'nn.Conv2d(3, 64, 5, padding=2)'**: 5x5 folding
- `5': Size of kernel (larger receptor field)
- `adding=2': Filling for size preservation

- **`nn.MaxPool2d(3, stride=1, padding=1)`**: Max pooling
- `3': Window size
- `stride=1': Step 1 for size preservation
- `adding=1': Filling for size preservation

- **`nn.AvgPool2d(3, stride=1, padding=1)`**: Average pooling
- `3': Window size
- `stride=1': Step 1 for size preservation
- `adding=1': Filling for size preservation

- **'nn.Conv2d(3, 64, 1) `**: 1x1 folding
- `1': Size of kernel (point fold)
- Application: Change of channels without change of size

- **'dilation=2'**: Dilated folding
- `2': Dilatation factor
- Application: increase of prescription field

- **'dilation=3'**: Dilated folding
- `3': Dilatation factor
- Application: an even larger prescription field

- **'nn.Identity()'**: Equivalent operation
- Application: Data missing without change
- Use: for kip connections
```

## Meta-Learning

<img src="images/optimized/meta_learning.png" alt="Meta-Learning" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 18.3: Meta-Learning (Learning to Learn) - methods of learning how to learn *

**Tips of meta-learning techniques:**
**MAML (Model-Agnostic)**: Universal meta-learning for any models
- **Prototypical Networks**: Learning through class prototypes
- **Matching networks**: Comparison of examples for classification
- **Reptile**: Simple and effective meta-learning
- **Meta-SGD**: Meta-learning with adaptive learning steps
- **Gradient Meta-Learning**: Meta-learning through gradients

### 1. Model-Agnostic Meta-Learning (MAML)

```python
class MAML(nn.Module):
 """Model-Agnostic Meta-Learning"""

 def __init__(self, model, lr=0.01):
 super(MAML, self).__init__()
 self.model = model
 self.lr = lr

 def forward(self, x):
 return self.model(x)

 def meta_update(self, support_set, query_set, num_inner_steps=5):
"The Meta-update Model."

# Copying the parameters
 fast_weights = {name: param.clone() for name, param in self.model.named_parameters()}

# Internal updates
 for step in range(num_inner_steps):
 # Forward pass on support set
 support_pred = self.forward_with_weights(support_set[0], fast_weights)
 support_loss = F.cross_entropy(support_pred, support_set[1])

# Gradients
 grads = torch.autograd.grad(support_loss, fast_weights.values(), create_graph=True)

# extradate balance
 fast_weights = {name: weight - self.lr * grad
 for (name, weight), grad in zip(fast_weights.items(), grads)}

# Evaluation on query set
 query_pred = self.forward_with_weights(query_set[0], fast_weights)
 query_loss = F.cross_entropy(query_pred, query_set[1])

 return query_loss

 def forward_with_weights(self, x, weights):
"Forward pass with given weights"
# Implementing forward pass with normal weights
 pass
```

** Detailed descriptions of the MAML parameters:**

- **'model'**: Basic model for meta-learning
- Type: nn.Module
- Requirements: shall support named_printers()
- Application: any model (CNN, RNN, Transformer)
 - examples: ResNet, LSTM, BERT

- **'lr=0.01'**:Learning rent for internal updates
- `0.01': Standard value (recommended)
- `0.001': Less Learning Rate (stable)
- `0.1': Larger lightning rent (rapid)
- `0.5': Very large lightning rent (may be unstable)
Application: speed of adaptation to new challenges

- **'support_set'**: Supporting Data Set
- Format: (data, labels)
- Size: usually 5-20 samples (few-shot lightning)
- Application: rapid adaptation to the new challenge
- Recommendation: balanced classes

** `Query_set'**: Request kit
- Format: (data, labels)
- Size: usually 15-100 samples
- Application: assessment of the quality of adaptation
- Recommendation: independent from support_set

- **'num_inner_steps=5'**: Number of internal steps
`5': Standard quantity (recommended)
`1': Rapid adaptation (less accurate)
`10': Slow adaptation (more precise)
- `20': Very slow adaptation (very precise)
Application: control of the speed of adaptation

- ** `fast_whites'**: Rapid weights for adaptation
- Type: dict with model parameters
- Initiation: copy of reference weights
Application: Time weights for a new task
- update: through gradient descent

- **`support_pred = self.forward_with_weights(support_set[0], fast_weights)`**: Prediction on support set
 - `support_set[0]`: data support set
- `fast_weights': Current fast weights
Results: model predictions
- Application: Calculation of loss for adaptation

**'F.cross_entropy(support_pred, support_set[1])'**: financing of losses
- `support_pred': Model predictions
- `support_set[1]': True labels
- Application: classification
Alternatives: F.mse_loss for regression

- **'torch.autograd.grad(support_loss, fast_whites.valutes(), creation_graph=True)'**: Calculation of gradients
- `support_loss': Losses on support set
- `fast_whites.valutes()': parameters for differentiation
- `create_graph=True': Retaining the row for the second order
Outcome: gradients on parameters
- Application: extradate of fast weights

- **/weight - Self.lr * rad'**: extra weight
- `weight': Current weight
 - `self.lr`: Learning rate
- `grad': Weight Gradient
- Result: new weight
- Application: gradient descent

- **`query_pred = self.forward_with_weights(query_set[0], fast_weights)`**: Prediction on query set
 - `query_set[0]`: data query set
- `fast_weights': Adapted weights
Results: Forecasts on query set
- Application: assessment of the quality of adaptation

- **/query_loss = F.cross_entropy(query_pred, query_set[1]) `**: Loss on query set
- `Query_pred': Projections on query set
- `query_set[1]': True marks query set
Outcome: Final losses
- Application: meta-training

**MAML key features:**

- **Model-Agnostic**: Workinget with any models
- **Few-Shot Learning**: Rapid adaptation to new challenges
- **Meta-Learning**: Learning how to learn
- **Gradient-Based**: Uses gradients for adaptation
- **Second-Order**: Considers second-order gradients

** APPLICATION MAML:**

- **Few-Shot Classification**: Classification with few examples
- **Few-Shot Regulation**: Regression with few examples
- **Domain Adaptation**: Adaptation to new domains
- **Task Adaptation**: Adaptation to new challenges
- **Continual Learning**: Continuing education
```

### 2. Prototypical networks

```python
class Prototypicalnetworks(nn.Module):
 """Prototypical networks for few-shot learning"""

 def __init__(self, input_dim, hidden_dim=64):
 super(Prototypicalnetworks, self).__init__()
 self.encoder = nn.Sequential(
 nn.Linear(input_dim, hidden_dim),
 nn.ReLU(),
 nn.Linear(hidden_dim, hidden_dim),
 nn.ReLU(),
 nn.Linear(hidden_dim, hidden_dim)
 )

 def forward(self, support_set, query_set, num_classes):
 """Forward pass for few-shot learning"""

# Coding support set
 support_embeddings = self.encoder(support_set)

# Calculation of class prototypes
 prototypes = []
 for i in range(num_classes):
Class_mask = (support_set[:, -1] ==(i) # We assume the last column is class
 class_embeddings = support_embeddings[class_mask]
 prototype = class_embeddings.mean(dim=0)
 prototypes.append(prototype)

 prototypes = torch.stack(prototypes)

# Coded query set
 query_embeddings = self.encoder(query_set)

# Calculation of distances to prototypes
 distances = torch.cdist(query_embeddings, prototypes)

# Premonition (near prototype)
 predictions = torch.argmin(distances, dim=1)

 return predictions, distances
```

## Multi-Modal Learning

<img src="images/optimized/multimodal_learning.png" alt="Multi-Modal Learning" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 18.4: Multi-Modal Learning - Working with different data types simultaneous *

**Tips of modalities:**
**Vision (Images)**: Image and Visual Data Processing
**Language (Text)**: Text processing and natural language
- **Audio (Sound)**: Sound and audio processing
- **Video**: Video and time sequence processing
- **Sensor data**: Data processing with sensors
- **Structured data**: Processing structured data

**methods Fusion:**
- **Early Fusion**: Early Modular Integration
- **Late Fusion**: Later integration of modes
- **Cross-Modal Actence**: Mutual attention between modes

### 1. Vision-Language Models

```python
class VisionLanguageModel(nn.Module):
"""""""""""""

 def __init__(self, image_dim=2048, text_dim=768, hidden_dim=512):
 super(VisionLanguageModel, self).__init__()

# Visual encoder
 self.vision_encoder = nn.Sequential(
 nn.Linear(image_dim, hidden_dim),
 nn.ReLU(),
 nn.Linear(hidden_dim, hidden_dim)
 )

# Text encoder
 self.text_encoder = nn.Sequential(
 nn.Linear(text_dim, hidden_dim),
 nn.ReLU(),
 nn.Linear(hidden_dim, hidden_dim)
 )

# Fusion moduule
 self.fusion = nn.Sequential(
 nn.Linear(hidden_dim * 2, hidden_dim),
 nn.ReLU(),
 nn.Linear(hidden_dim, 1)
 )

 def forward(self, images, texts):
# Image coding
 image_features = self.vision_encoder(images)

# Coding text
 text_features = self.text_encoder(texts)

# Combination of topics
 combined = torch.cat([image_features, text_features], dim=1)

 # Prediction
 output = self.fusion(combined)

 return output
```

### 2. Cross-Modal Attention

```python
class CrossModalAttention(nn.Module):
"Cross-model education for multimodal learning."

 def __init__(self, dim):
 super(CrossModalAttention, self).__init__()
 self.dim = dim

# Attention mechanisms
 self.attention = nn.MultiheadAttention(dim, num_heads=8)

# Normalization
 self.norm1 = nn.LayerNorm(dim)
 self.norm2 = nn.LayerNorm(dim)

 # Feed-forward
 self.ff = nn.Sequential(
 nn.Linear(dim, dim * 4),
 nn.ReLU(),
 nn.Linear(dim * 4, dim)
 )

 def forward(self, modality1, modality2):
# Cross-attension between modes
 attended1, _ = self.attention(modality1, modality2, modality2)
 attended1 = self.norm1(attended1 + modality1)

 attended2, _ = self.attention(modality2, modality1, modality1)
 attended2 = self.norm1(attended2 + modality2)

 # Feed-forward
 output1 = self.norm2(attended1 + self.ff(attended1))
 output2 = self.norm2(attended2 + self.ff(attended2))

 return output1, output2
```

## Federated Learning

<img src="images/optimized/federated_learning.png" alt="Federated Learning" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 18.5: Federal Learning Architecture - distributed learning with privacy *

**architecture federal education:**
- **Global Server**: Central server for model aggregation
- **Clients**: Distributed clients with local data
- **Local Training**: Local education on each client
- **Model Aggregation**: Aggregation of model updates
**Privacy Protection**: Maintaining data privacy

** Benefits of federal training:**
- **Save privacy**: Data not leaving clients
- ** Distributed data**: Training on distributed data
- **Station capacity**: Scale on multiple clients
- ** Reduction of communication**: Minimalization of data transmission
- ** Local treatment**: Data processing on device

### 1. Federated Averaging (FedAvg)

```python
class FederatedAveraging:
"Federated Overging for Distribution"

 def __init__(self, global_model, clients):
 self.global_model = global_model
 self.clients = clients

 def federated_round(self, num_epochs=5):
"One round of federal training."

# Customer training
 client_models = []
 client_weights = []

 for client in self.clients:
# Local education
 local_model = self.train_client(client, num_epochs)
 client_models.append(local_model)
Client_lights.append(len(lient.data)) # Weight proportional to data size

# Model aggregation
 self.aggregate_models(client_models, client_weights)

 def train_client(self, client, num_epochs):
"""""""""" "Learning Model on Customer""""

# Copying the global model
 local_model = copy.deepcopy(self.global_model)

# Local education
 optimizer = torch.optim.SGD(local_model.parameters(), lr=0.01)

 for epoch in range(num_epochs):
 for batch in client.data_loader:
 optimizer.zero_grad()
 output = local_model(batch[0])
 loss = F.cross_entropy(output, batch[1])
 loss.backward()
 optimizer.step()

 return local_model

 def aggregate_models(self, client_models, weights):
""Aggregation of models with weights""

 total_weight = sum(weights)

# Initiating a global model
 for param in self.global_model.parameters():
 param.data.zero_()

# Weighted averaging
 for model, weight in zip(client_models, weights):
 for global_param, local_param in zip(self.global_model.parameters(), model.parameters()):
 global_param.data += local_param.data * (weight / total_weight)
```

** Detailed description of Federated Learning parameters:**

- **/global_model'**: Global model on server
- Type: nn.Module
Application: Central model for aggregation
- Initiation: random weights or pre-trained model
- update: via local model aggregation

- **///////:////
- Type: List[Client]
- Contains: local data and models
- Application: distributed training
- Recommendation: 10 to 1,000 clients

- **'num_epochs=5'**: Number of local learning eras
`5': Standard quantity (recommended)
`1': Rapid learning (less accurate)
`10': Slow learning (more precise)
- `20': Very slow learning (very accurate)
- Application: control of local education

- **/'lient.data'**: Local data client
- Type: dataset
- Contained: Private data client
- Application: local education
- Privateity: Data not leaving client

**'len(client.data)'**: Size of client data
Application: Weight for aggregation
- Logsca: more data = more weight
- Result: Proportional impact on the global model

- **'copy.deepcopy(self.global_model)'**: Copying the global model
- Application: Initialization of the local model
Outcome: independent copy of the model
Benefits: isolation of education

- **'torch.optim.SGD(local_model.parameters(), lr=0.01)'**: SGD Optimizer
- `local_model.parameters()': parameters local model
- `lr=0.01':Learning rent (recommended for FedAvg)
- `0.001': Less Learning Rate (stable)
- `0.1': Larger lightning rent (rapid)
- Application: local optimization

- **/ 'lient.data_loader'**: Client Data uploader
- Type: DataLoader
- Contains: local data boots
- Application: Iteration on Data
- Recommendation: balanced tramps

- ** `Total_white = sum(weights)'**: Total weight all clients
- Calculation: sum of all customers &apos; weights
Application: Normalization of weights
- Result: sum of all weights

- **'param.data.zero_()'**: No global model parameters
- Application: preparation for aggregation
- Result: zero parameters
- Need: before weighted averaging

- **/global_param.data += local_param.data* (white / total_weight)**: Weighted average
- `global_param': parameter of the global model
- `local_param': local model parameter
- `weight / total_weight': Normalized weight
Outcome: weighted sum of parameters

** Key features of Federated Learning:**

- **Privacy-Preserving**: Maintaining data privacy
- **Distributed Training**: Trained
- **Communication Officer**: Effective communication
- **Fault Tolerant**: Malfunction resistance
- **Scalable**: Scale

**Federated Learning Benefits:**

- **data Privacy**: Data not leaving clients
- **Remedied Communication**: Minimization of data transmission
- **Local Processing**: Processing on the device
- **Federated Aggregation**: Aggregation of Updates
- **Global Model**: A single global model

** Application of Federal Learning:**

- **mobile Services**: Training on mobile devices
- **Iot Sensors**: Sensor training
- **healthcare**: Medical data
- **Finance**: Financial data
- **Edge Computing**: Training on network boundary
```

### 2. Differential Privacy

```python
class DifferentialPrivacy:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""d""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self, epsilon=1.0, delta=1e-5):
 self.epsilon = epsilon
 self.delta = delta

 def add_noise(self, gradients, sensitivity=1.0):
"""""dd noise for differential privacy."

# Calculation of standard noise deviation
 sigma = np.sqrt(2 * np.log(1.25 / self.delta)) * sensitivity / self.epsilon

# add haussian noise
 noise = torch.normal(0, sigma, size=gradients.shape)
 noisy_gradients = gradients + noise

 return noisy_gradients

 def clip_gradients(self, gradients, max_norm=1.0):
""""""""""""""""

# L2 Normalization
 grad_norm = torch.norm(gradients)
 if grad_norm > max_norm:
 gradients = gradients * (max_norm / grad_norm)

 return gradients
```

## Continual Learning

<img src="images/optimized/continual_learning.png" alt="Continual Learning" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 18.6: Continental Learning (Lifelong Learning) - Continuing learning without forgetting*

**Tips of methods of continuous learning:**
- **EWC**: Elastic Weighting for Knowledge Conservation
- **Provision networks**: Progressive networks with side connections
- **Memorial Replay**: Reproduction of previous examples
- **Regularization Methods**: Regulation for the prevention of oblivion
- **Architectural Methods**: Architectural changes for new challenges
- **Meta-Learning Approaches**: Meta-learning for continuous adaptation

** Disaster oblivion problem:**
- ** Forget previous tasks**: Loss of knowledge of old tasks
- ** Interference between objectives**: Conflict between new and old knowledge
- ** Need to preserve knowledge**: The importance of preserving previous experience
- **Balance between old and new**: Balance between old and new knowledge

### 1. Elastic Weight Consolidation (EWC)

```python
class ElasticWeightConsolidation:
"Elastic Weight Consultation for Continuing Learning"

 def __init__(self, model, lambda_ewc=1000):
 self.model = model
 self.lambda_ewc = lambda_ewc
 self.fisher_information = {}
 self.optimal_params = {}

 def compute_fisher_information(self, dataloader):
"Excuse Fisher's Information."

 self.model.eval()
 fisher_info = {}

 for name, param in self.model.named_parameters():
 fisher_info[name] = torch.zeros_like(param)

 for batch in dataloader:
 self.model.zero_grad()
 output = self.model(batch[0])
 loss = F.cross_entropy(output, batch[1])
 loss.backward()

 for name, param in self.model.named_parameters():
 if param.grad is not None:
 fisher_info[name] += param.grad ** 2

# Normalization
 for name in fisher_info:
 fisher_info[name] /= len(dataloader)

 self.fisher_information = fisher_info

 def ewc_loss(self, current_loss):
""""add EWC regularization to loss""

 ewc_loss = current_loss

 for name, param in self.model.named_parameters():
 if name in self.fisher_information:
 ewc_loss += (self.lambda_ewc / 2) * torch.sum(
 self.fisher_information[name] * (param - self.optimal_params[name]) ** 2
 )

 return ewc_loss
```

### 2. Progressive Neural networks

```python
class ProgressiveNeuralnetwork(nn.Module):
"Progressive National Networks for Continuing Learning"

 def __init__(self, input_dim, hidden_dim=64):
 super(ProgressiveNeuralnetwork, self).__init__()
 self.columns = nn.ModuleList()
 self.lateral_connections = nn.ModuleList()

# First column
 first_column = nn.Sequential(
 nn.Linear(input_dim, hidden_dim),
 nn.ReLU(),
 nn.Linear(hidden_dim, hidden_dim)
 )
 self.columns.append(first_column)

 def add_column(self, input_dim, hidden_dim=64):
"""add new column for a new task""

# New column
 new_column = nn.Sequential(
 nn.Linear(input_dim, hidden_dim),
 nn.ReLU(),
 nn.Linear(hidden_dim, hidden_dim)
 )
 self.columns.append(new_column)

# Side compounds with previous columns
 lateral_conn = nn.ModuleList()
 for i in range(len(self.columns) - 1):
 lateral_conn.append(nn.Linear(hidden_dim, hidden_dim))
 self.lateral_connections.append(lateral_conn)

 def forward(self, x, column_idx):
"Forward pass for a specific column."

# The main route through the current column
 output = self.columns[column_idx](x)

# Side compounds with previous columns
 for i in range(column_idx):
 lateral_output = self.lateral_connections[column_idx][i](
 self.columns[i](x)
 )
 output = output + lateral_output

 return output
```

## Quantum Machine Learning

<img src="images/optimized/quantum_ml.png" alt="Quantum Machine Learning" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 18.7: Quantum Machine Learning - Quantum calculations for ML*

**components quantum ML:**
**Quantum Neural Networks**: Quantum neural networks
**Quantum Circuits**: Quantum diagrams and algorithms
**Quantum Algorithms**: Quantum algorithms for ML
- **Quantum Gates**: Quantum valves for calculations
**Quantum Entanglement**: Quantum confusion for parallelism
- **Quantum Superposition**: Quantum Superposition for Explicit Acceleration

** Quantum benefits:**
- **Exponent acceleration**: Exponsive acceleration of calculations
- ** Parallel calculations**: Parallel processing of information
- ** Quantum superposition**: simultaneous in several states
- ** Quantum complexity**: Correlated states for calculations
- ** Quantum interference**: Interference for optimization

### 1. Quantum Neural networks

```python
# Example with use of PennyLane
import pennylane as qml
import numpy as np

def quantum_neural_network(params, x):
"Quantum neural network."

# Data coding
 for i in range(len(x)):
 qml.RY(x[i], wires=i)

# Parametricized layers
 for layer in range(len(params)):
 for i in range(len(x)):
 qml.RY(params[layer][i], wires=i)

# Entangling Gates
 for i in range(len(x) - 1):
 qml.CNOT(wires=[i, i+1])

# Measurement
 return [qml.expval(qml.PauliZ(i)) for i in range(len(x))]

# square quantum device
dev = qml.device('default.qubit', wires=4)

# create QNode
qnode = qml.QNode(quantum_neural_network, dev)

# Quantum model training
def train_quantum_model(X, y, num_layers=3):
"Learning Quantum Neural Network."

# Initiating parameters
 params = np.random.uniform(0, 2*np.pi, (num_layers, len(X[0])))

# Optimizer
 opt = qml.GradientDescentOptimizer(stepsize=0.1)

 for iteration in range(100):
# Calculation of gradients
 grads = qml.grad(qnode)(params, X[0])

# Update Options
 params = opt.step(qnode, params, X[0])

 if iteration % 10 == 0:
 print(f"Iteration {iteration}, Cost: {qnode(params, X[0])}")

 return params
```

## Conclusion

<img src="images/optimized/advanced_methods_comparison.png" alt="comparison of advanced techniques" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 18.8: Comparison of advanced AutoML techniques - complexity, complexity, learning time, data requirements*

**comparison of advanced techniques:**
- **Performance vsComplexity**: Balance between productivity and complexity
- **Training Time**: Time spent learning different methods
- **data Requirements**: Data volume requirements
- **Real-world Application**: Applicability in Real Tasks

The advanced themes of AutoML are a rapidly evolving area that includes:

1. **Neural architecture Search** - automatic search for optimal architectures
2. **Meta-Learning** - Learning how to learn
3. **Multi-Modal Learning** - Working with different data types
4. **Federated Learning** - Distributiond learning with privacy
5. **Continual Learning** - Continuing education without forgetting
6. **Quantum Machine Learning** - Quantum computing

These technoLogs offer new opportunities for more efficient, adaptive and powerful ML systems, but require a thorough understanding of both the theoretical and practical aspects of their application.
