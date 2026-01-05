# 01. environment installation on macOS M1 Pro

**Goal:** Create optimal environment for development robust ML systems on macOS M1 Pro.

## Why macOS M1 Pro ideal for ML?

**M1 Pro chip revolutionized ML on Mac:**

```
┌─────────────────────────────────────────────────────────────────┐
│ M1 Pro Architecture │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ CPU │ │ GPU │ │ Neural │ │
│ │ 8 Cores │ │ 16 Cores │ │ Engine │ │
│ │ │ │ │ │ 16 Cores │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ │
│ │ │ │ │
│ └────────────────┼────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Unified Memory (32GB) │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ data │ │ Models │ │ cache │ │ Temp │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

Performance Comparison (Relative to Intel i9):
┌─────────────────┬──────────┬──────────┬──────────┐
│ Task │ CPU │ GPU │ NE │
├─────────────────┼──────────┼──────────┼──────────┤
│ Matrix Math │ 2.5x │ 8.0x │ 15.0x │
│ Neural networks │ 3.0x │ 10.0x │ 20.0x │
│ data Processing │ 2.0x │ 5.0x │ 8.0x │
│ Energy Usage │ 0.3x │ 0.2x │ 0.1x │
└─────────────────┴──────────┴──────────┴──────────┘
```

### Unified Memory Architecture (UMA)
**Theory:** UMA allows CPU and GPU use used well-owned memory with out-of-date data from between products.This is critical for ML work, what large datasets and require fast access to memory models.

```
Traditional Architecture (x86 + Discrete GPU):
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ CPU │ │ Memory │ │ GPU │
│ │ │ (32GB) │ │ │
│ ┌───────┐ │ │ │ │ ┌───────┐ │
│ │ data │ │◄───┤ │ │ │ data │ │
│ └───────┘ │ │ │ │ └───────┘ │
│ │ │ │ │ │
└─────────────┘ └─────────────┘ └─────────────┘
 ▲ │ ▲
 │ │ │
 └───────────────────┼───────────────────┘
 │
 Slow data Copy
 (3-5x slower)

M1 Pro Unified Memory:
┌─────────────────────────────────────────────────────────┐
│ Unified Memory (32GB) │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ data │ │ Models │ │ cache │ │ Temp │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│ ▲ ▲ ▲ ▲ │
│ │ │ │ │ │
│ ┌────┴─────┐ ┌───┴───┐ ┌─────┴─────┐ ┌───┴───┐ │
│ │ CPU │ │ GPU │ │ Neural │ │ I/O │ │
│ │ 8 Cores │ │16 Cores│ │ Engine │ │ │ │
│ └──────────┘ └────────┘ └──────────┘ └───────┘ │
└─────────────────────────────────────────────────────────┘
 Direct Access
 (No copying needed)
 (3-5x faster)
```

**Practical advantages:**
- **Speed:** Data are not copied between CPU and GPU, which speds up by 3-5 times
- **Memory efficiency:** One dataset is used by both CPU and GPU simultaneously
- **Scalability:** up to 32GB shared memory for large models
- **Programming simplicity:** no need to manage data transfer between devices

**Disadvantages:**
- Limited memory compared to discrete GPUs (to 32GB vs 80GB+ on RTX A100)
- Lower performance for very large models

### Neural Engine
**Theory:**Specialized 16-nuclear processor for machine lightning, optimized for operations with frameworks and neural networks.

```
Neural Engine Performance:
┌─────────────────────────────────────────────────────────────┐
│ Neural Engine (16 Cores) │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Core 1 │ │ Core 2 │ │ Core 3 │ │ Core 4 │ │
│ │ Matrix │ │ Matrix │ │ Matrix │ │ Matrix │ │
│ │ Ops │ │ Ops │ │ Ops │ │ Ops │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Core 5 │ │ Core 6 │ │ Core 7 │ │ Core 8 │ │
│ │ Matrix │ │ Matrix │ │ Matrix │ │ Matrix │ │
│ │ Ops │ │ Ops │ │ Ops │ │ Ops │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Core 9 │ │ Core 10 │ │ Core 11 │ │ Core 12 │ │
│ │ Matrix │ │ Matrix │ │ Matrix │ │ Matrix │ │
│ │ Ops │ │ Ops │ │ Ops │ │ Ops │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Core 13 │ │ Core 14 │ │ Core 15 │ │ Core 16 │ │
│ │ Matrix │ │ Matrix │ │ Matrix │ │ Matrix │ │
│ │ Ops │ │ Ops │ │ Ops │ │ Ops │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘

Performance Comparison (TOPS - Trillions of Operations per Second):
┌─────────────────┬──────────┬──────────┬──────────┐
│ Operation │ CPU │ GPU │ NE │
├─────────────────┼──────────┼──────────┼──────────┤
│ Matrix Multiply │ 0.5 │ 4.0 │ 11.0 │
│ Convolution │ 0.3 │ 6.0 │ 15.0 │
│ Activation │ 0.8 │ 2.0 │ 8.0 │
│ Energy (W) │ 15 │ 25 │ 2 │
└─────────────────┴──────────┴──────────┴──────────┘
```

** Benefits:**
- **Specialization:** Optimized for ML operations
- ** Energy efficiency:** Consumption in 10 times less energy than GPU
- **Speed:** to 11 TOPS.
- **Automatic optimization:** Apple automatically uses Neural Energy for suitable operations

**Restrictions:**
- Working only with certain types of operations
- Less flexibility matched to CUDA
- Limited support for user operations

### MLX Framework
**Theory:** Apple-specific frame, unWorking for maximum use of M1/M2/M3 chips.

```
MLX Framework Architecture:
┌─────────────────────────────────────────────────────────────┐
│ MLX Framework │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Python API Layer │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ mlx │ │ mlx.nn │ │ mlx.opt │ │ mlx.lm │ │ │
│ │ │ .core │ │ │ │ │ │ │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Device Management Layer │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ CPU │ │ GPU │ │ NE │ │ Auto │ │ │
│ │ │ 8 Cores │ │16 Cores │ │16 Cores │ │ Select │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Metal Performance Shaders │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ Matrix │ │ Conv │ │ RNN │ │ Attn │ │ │
│ │ │ Ops │ │ Ops │ │ Ops │ │ Ops │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

Performance vs Other Frameworks:
┌─────────────────┬──────────┬──────────┬──────────┐
│ Framework │ Speed │ Memory │ Energy │
├─────────────────┼──────────┼──────────┼──────────┤
│ PyTorch (CPU) │ 1.0x │ 1.0x │ 1.0x │
│ PyTorch (MPS) │ 3.0x │ 0.8x │ 0.5x │
│ TensorFlow │ 2.5x │ 0.9x │ 0.6x │
│ MLX │ 8.0x │ 0.7x │ 0.3x │
└─────────────────┴──────────┴──────────┴──────────┘
```

** Key features:**
- **Indirect integration:** Direct access to Neural Engineering and GPU
- **PyTorch compatibility:** Easy migration of existing code
- ** Automatic optimization:** Automatic choice of the best device for each operation
- **Unified API:** Unified Interface for CPU, GPU and National Energy

** Plus:**
- Maximum performance on Apple Silicon
- Easy use
- Energy efficiency
- Automatic optimization

**Disadvantages:**
- Reference to Apple ecosystem
- Smaller community competing to PyTorch/TensorFlow
- Limited support to some operations

## System requirements

```
system Requirements Visualization:
┌─────────────────────────────────────────────────────────────┐
│ macOS M1 Pro ML Requirements │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ MINIMUM REQUIREMENTS │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ macOS │ │ RAM │ │ Storage │ │Internet │ │ │
│ │ │ 12.0+ │ │ 16GB │ │ 100GB │ │ Stable │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ │ ▲ ▲ ▲ ▲ │ │
│ │ │ │ │ │ │ │
│ │ Basic Small Small Download │ │
│ │ Support Models datasets Libraries │ │
│ └─────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ RECOMMENDED REQUIREMENTS │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ macOS │ │ RAM │ │ Storage │ │ GPU │ │ │
│ │ │ 14.0+ │ │ 32GB+ │ │ 500GB+ │ │M1 Pro+ │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ │ ▲ ▲ ▲ ▲ │ │
│ │ │ │ │ │ │ │
│ │ Latest Large Large Maximum │ │
│ │ Features Models datasets Performance │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Minimum requirements
**Theory:**The minimum requirements determine the basic functionality of the system. for Robst ML systems is critical to have sufficient resources for data processing and model learning.

- **macOS:** 12.0+ (Monterey)
- **Why:** Support for MLX Framework and Optimisms for M1
- ** Plus:** Stability, compatibility with ML libraries
- **Disadvantages:** Limited opportunities to compete for new versions

- **RAM:** 16GB (recommended 32GB)
- **Theory:** ML models require significant memory for data storage and intermediate calculations
- **16GB:** Minimum for Small Models and Datasets
- **32GB:** Optimally for most ML objectives, allows Working with larger datasets
- ** Plus:** Rapid processing, with large models
- **Disadvantages:** High cost, limited availability

- **Storage:** 100GB available
- **Theory:** ML projects require a lot of space for data, models and cache.
- ** Plus:** Enough for small projects
- **Disadvantages:** may not be enough for big datasets

- **Internet:** Stable connection
- ♪ Why: ♪ Loading big datasets, extradate libraries, accessing cloud services ♪
- ** Plus:** Workability with external data
- **Disadvantages:**dependency from Internet connection

### Recommended claims
**Theory: ** Recommended requirements ensure optimal performance and comfort with large ML projects.

- **macOS:** 14.0+ (Sonoma)
- **Why:** Newest optimization for M1, improved ML-frame support
- ** Plus:** Maximum performance, new opportunities
- **Disadvantages:** May be less stable on early stages

- **RAM:** 32GB+
- **Theory:** Big ML models and datesets require a lot of memory.
- ** Plus:** Working with big models, parallel processing
- **Disadvantages:** High cost, surplus for simple tasks

- **Storage:** 500GB+ SSD
- **Theory:** SSD provides quick access to data, critical for ML work
- ** Plus:** Rapid Loading Data, quick access to models
- **Disadvantages:** High cost compared to HDD

- **GPU:** M1 Pro/Max/Ultra
- **Theory:** More powerful chips provide better performance for ML
- **M1 Pro:** Good balance between performance and value
- **M1 Max:** Maximum performance for professional tasks
- **M1 Ultra:** Extreme performance for research tasks
- ** Plus:** High performance, energy efficiency
- **Disadvantages:** High cost, limited availability

## installation of the basic environment

### 1. installation Homebrew

**Theory:** Homebrew is a package manager for machos that facilitates installation and management software. For ML projects, it is critical to have centralized management relationships.

```
Homebrew Package Management:
┌─────────────────────────────────────────────────────────────┐
│ Homebrew Ecosystem │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ package installation │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ brew │ │ brew │ │ brew │ │ brew │ │ │
│ │ │ install │ │ List │ │ update │ │ upgrade │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ML-Specific Packages │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ cmake │ │pkg-config│ │ ta-lib │ │ opencv │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ M1 Optimization │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ ARM64 │ │ Native │ │ Fast │ │ Auto │ │ │
│ │ │ Builds │ │ Support │ │ install │ │ Deps │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

installation Process:
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Download Script │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ curl -fsSL https://raw.githubUsercontent.com/... │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ Step 2: install to /opt/homebrew/ (M1) │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ /bin/bash -c "$(curl -fsSL ...)" │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ Step 3: Add to PATH │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Why Homebrew for ML:**
- ** Centralized Management:** All dependencies in one place
- **Automatic conflict resolution:** Smart Management versions
- **Optimization for M1:**Apple Silicon's Positive Support
- ** Rich ecosystem:** Thousands of packages for ML and scientific calculations

** Plus:**
- Simplicity installation and updating
- Automatic resolution dependencies
- Optimization for M1
- Large community and support

**Disadvantages:**
- Could conflict with systems packages.
- Requires regular updating
- Some bags may be obsolete.

```bash
# installation Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubUsercontent.com/Homebrew/install/HEAD/install.sh)"

# add in PATH for M1
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

** Important points for M1:**
- **Stallation:** `/opt/homebrew/' instead of `/usr/local/'
- **architecture:** Automatic installation ARM64 versions
- **Compatibility:** Support for both ARM64 and x86_64 packages via Rosetta

### 2. installation uv (Ultra-fast Python package manager)

**Theory:** uv is a modern Python package manager, written on Rust, which provides maximum speed and reliability of installation preferences. for robust ML systems is critical to have a fast and reliable bag manager.

```
uv vs pip Performance Comparison:
┌─────────────────────────────────────────────────────────────┐
│ Package Manager Speed Test │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ installation Speed │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ Package │ │ pip │ │ uv │ │ Speedup │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ │ numpy │ 45s │ 3s │ 15x │ │ │
│ │ pandas │ 60s │ 4s │ 15x │ │ │
│ │ scikit │ 90s │ 6s │ 15x │ │ │
│ │ torch │ 180s │ 12s │ 15x │ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Key Features │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ Rust │ │Parallel │ │ cache │ │ Lock │ │ │
│ │ │ Fast │ │ installs│ │ Smart │ │ files │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

uv Architecture:
┌─────────────────────────────────────────────────────────────┐
│ uv Package Manager │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Rust Core Engine │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ Fast │ │Parallel │ │ Safe │ │ Memory │ │ │
│ │ │ Parsing│ │ Downloads│ │ Rust │ │ Efficient│ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Python integration │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ uv │ │ uv │ │ uv │ │ uv │ │ │
│ │ │ add │ │ sync │ │ run │ │ init │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

# Why uv instead of pip? #
- **Speed:** in 10-100 times faster than pip due to Rust and parallel processing
- ** Reliability: ** Determinated assemblies ensure reproducibility
- **Compatibility:** Full compatibility with the pip and existing projects
- **Cashing:** Smart caches dependencies accelerates reinstallation
- ** Safety:** Automatic heck integrity of packages
- **Management versions:** Advanced version conflict resolution

** Plus uv:**
- Extreme speed installation
- Reliability and reproducibility
- Modern approach to the management of addictions
- Excellent integration with existing projects
Automatic Management Virtual Environments

**Minuses uv:**
- Relatively new instrument (less community)
- Some packages may require additional Settings
- Dependency from Rust (larger installation)

```bash
# installation uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# add in PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# installation check
uv --version
```

** Critical for ML projects:**
- **Preducibility:** Determinated assemblies provide the same results on different machines
- **Speed:** Rapid installation critical for CI/CD and development
- ** Reliability:** Minimization of installation errors
- **Management versions:** Exact Management versions of the ML library

### 3. Installation Python through uv

**Theory:** Python's choice is critical for ML projects. Python 3.11 provides an optimal balance between productivity, stability and support for the ML library on M1.

**Why Python 3.11 for M1:**
- **Performance:** to 25% faster than Python 3.10 due to optimization
- **Compatibility:** Full support for all ML libraries
- **Stability:**Mature version with corrected bugs
- **Optification for M1:**ARM64 architecture best support
- ** Memory:** Better use of memory

** Plus Python 3.11:**
- High performance
- Excellent compatibility with ML libraries
- Stability and reliability
- Optimization for M1
- Supporting Python &apos; s Modern Opportunities

**Mine Python 3.11:**
- Some old libraries can be supported.
- Requires an update of the existing code
- Larger size matched to older versions

```bash
# installation Python 3.11
uv python install 3.11

# installation check
uv python List
```

** Alternative versions:**
- **Python 3.10:** More stable but slower
- **Python 3.12:** Newest but may be less stable
- **Python 3.9:** Obsolete, not recommended for new projects

** Critical for ML:**
- **Reproduction:** Same version of Python on all machines
- **Performance:** Rapid execution of ML-algorithms
- **Compatibility:** Support for all read ML library
- **Stability:** Minimalization of errors during model training

## installation MLX Framework

### What is MLX?

**Theory:** MLX (Machine Learning eXtended) is the Specialized Framework of Apple for Machine Learning, which is designed to maximize the use of Apple Silicon chips. This is critical for Robst ML systems because it provides optimal performance on M1/M2/M3.

**MLX is an Apple-specific frame for ML:**

**Intentional support M1/M2/M3:**
- **Theory:** MLX uses all of Apple Silicon chips, including CPU, GPU and Neural Engineering
- **Practical promotions:** to 10x acceleration combined to PyTorch on M1
- ** Automatic optimization:** Automatic choice of the best device for each operation
- ** Energy efficiency:** Consumption in 5-10 times less energy than CUDA

**Unified Memory:**
- **Theory:** MLX uses a single memory for CPU and GPU, which eliminates the need to copy data
- **Practical promotions:**Working with big models without GPU memory limitations
- **Speed:** Data available instantly for all devices
- **Simple:**no lost to manage data transfer between declarations

**Neural Engine:**
- **Theory:** Automatic use of Neural Engineering for suitable operations
- **Practical promotions:** to 20x acceleration for certain ML operations
- ** Energy efficiency:**Neural Energy consumes minimum energy
- **Specialization:** Optimized for operations with frameworks and non-ural networks

**PyTorch compatibility:**
- **Theory:** MLX provides an API similar to PyTorch, which makes migration easier
- **Practical promotions:** Easy migration of the existing code
- **Reverse compatibility:** Support for most PyTorch operations
- **Learning:** Minimum time on new API

** Plus MLX:**
- Maximum performance on Apple Silicon
- Energy efficiency
- Easy use
- Automatic optimization
- Excellent integration with Apple ecosystem

**Minuses MLX:**
- A link to Apple Silicon (no support for other platforms)
- Smaller community competing to PyTorch/TensorFlow
- Limited support to some operations
- Fewer models and examples produced

### installation MLX

**Theory:** installation MLX Framework requires a correct Settings project and understanding of the Apple Silicon architecture. for robot ML systems is critical to fine-tune the environment with the very beginning.

**Why the right installation is critical:**
- ** Architectural compatibility:** MLX Working only on Apple Silicon and requires correct Settings
- **dependencies:** MLX has specific dependencies to be installed in the correct order.
- **Performance:** Wrong installation can lead to significant loss of performance
- **Stability:** Correct configurization ensures system stability

**Taps installation MLX:**

**1. project activity:**
- **Theory:** the creation of a separate project provides isolation and reproducibility
- ** Practice: ** Use of uv for project management provides determinable assemblies

**2. Initiating uv project:**
- **Theory:** uv init creates project structure with correct settings for Python 3.11
- ** Practice:** This ensures correct management relationships and virtual environments

**3. installation MLX:**
- **Theory:** MLX is the main frame for work with Apple Silicon.
- ** Practice:** installation through uv ensures correct version and compatibility

**4. Additional preferences:**
- **mlx-lm:** Specialized tools for language models
- **mlx-examples:**Prepared examples and templates for quick start

```bash
# the project's creation
mkdir neozork-ml-system
cd neozork-ml-system

# Initiating uv project
uv init --python 3.11

# installation MLX
uv add mlx

# installation of additional dependencies
uv ad mlx-lm # for language models
uv add mlx-examples # examples use
```

** Critical for ML projects:**
- **Reproducibility:** Correct configuration gives the same results on different machines.
- **Performance:** Optimal configuring MLX provides maximum performance
- **Compatibility:** Correct institutionalization ensures compatibility with other ML libraries
- **Scalability:** Correct configuration allows easy project scale

### check MLX

** Full test MLX Framework:**

```python
# test_mlx_complete.py
"""
Full MLX Framework for M1 Pro
Launch: uv run python test_mlx_complete.py
"""

import mlx.core as mx
import mlx.nn as nn
import time
import numpy as np

def test_mlx_basic_operations():
"The MLX Basic Operations Test"
"print("===MLX basic operations test===)

# Create arrays
 a = mx.array([1, 2, 3, 4, 5])
 b = mx.array([5, 4, 3, 2, 1])

# Basic operations
 c = a + b
 d = a * b
 e = mx.sum(a)

 print(f"a: {a}")
 print(f"b: {b}")
 print(f"a + b: {c}")
 print(f"a * b: {d}")
 print(f"sum(a): {e}")

# Check results
 assert c.toList() == [6, 6, 6, 6, 6]
 assert d.toList() == [5, 8, 9, 8, 5]
 assert e.item() == 15

"Working operations are correct"
 return True

def test_mlx_neural_network():
""Neron Network Test on MLX""
Prent("\n===MLX neural network test===)

# creative simple neural network
 class SimpleNet(nn.Module):
 def __init__(self):
 super().__init__()
 self.linear1 = nn.Linear(10, 50)
 self.linear2 = nn.Linear(50, 1)
 self.dropout = nn.Dropout(0.1)

 def __call__(self, x):
 x = mx.tanh(self.linear1(x))
 x = self.dropout(x)
 return self.linear2(x)

# Create testy data
 x = mx.random.normal((100, 10))
 model = SimpleNet()

# Straight through
 output = model(x)

pprint(f) "Incoming data shupe: {x.chape}")
print(f) "Exit data shupe: {output.chape}")
Print(f" Average output value: {mx.mean(output).item(:4f}})
spring(f" Standard exit deviation: {mx.std(output).item():4f})

# Check form of exit
 assert output.shape == (100, 1)

"Pint("♪ Neural Workinget Network Correct")
 return True

def test_mlx_performance():
"Test performance MLX."
("\n=== Test performance MLX===)

# A matrix operation test
 sizes = [1000, 2000, 5000]

 for size in sizes:
prent(f)(ntest matrix(size) x(size}:)

# creative large matrices
 a = mx.random.normal((size, size))
 b = mx.random.normal((size, size))

# A matrix multiplication test
 start_time = time.time()
 c = mx.matmul(a, b)
 end_time = time.time()

 duration = end_time - start_time
Print(f" Multiplicity time: {duration:.3f}seconds")
 print(f" performance: {size**3 / duration / 1e9:.2f} GFLOPS")

# Check result
 assert c.shape == (size, size)

"Print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\))(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\))))((\(\\\\\\\\\\(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)})})})})}((((\\\\\\\\\\\\\\\\\\\\\\\)})})})})})}(((((((((((((((\\\\\\\\\\\\\\\\\\\\\\\\\\\\)}})})}}(((((((((((((((((((\)})})})}}}})}))}(((((((((((((((((\\\\\\\\\)))))))})))))))))(((((((((((((((((((
 return True

def test_mlx_device_info():
"Text of Information on Devices."
=== Information on the MLX devices========================MLX======)======The MLX devices

# Information on accessible devices
(pint(f) Accessable devices: {mx.devises()})
pprint(f) "Device: {mx.default_device()}")

# Test of work on different devices
 for device in mx.devices():
Print(f)\ntest on device: {device})
 with mx.device(device):
 a = mx.array([1, 2, 3, 4, 5])
 b = mx.array([5, 4, 3, 2, 1])
 c = a + b
result: {c})

print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)})}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}}}}}}}}}}}}}}}}}}}}}}\\\\\\\\\(((((((\\\\\\\\\\\\\\\}}}}}}}}}}}}}}}}}}}}}}}}}}}(((((((((((((((((((((((((((((\\\\\\\\\\\\\\\\\}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}((((((((((((((((((
 return True

def main():
"Principal function testing."
"Prent("♪ Launch Full Test MLX Framework")
 print("=" * 50)

 try:
 # Run all tests
 test_mlx_basic_operations()
 test_mlx_neural_network()
 test_mlx_performance()
 test_mlx_device_info()

 print("\n" + "=" * 50)
all MLX tests have been successful!
"MLX Framework is ready for use on M1 Pro"

 except Exception as e:
Print(f)\n\\\\\\\\\\\\\\\\\\\\\\\\\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\n\\\\\\\\\\\\\\\\\\\\}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/) as-) as-) as-) as-) as-) as the as the as the as the as the as the as the as the as the as the as a]) as the as the as of as of as of as of as of as of as of as of as
"Do check the MLX Framework"
 return False

 return True

if __name__ == "__main__":
 main()
```

**Launch MLX test:**
```bash
# Conservation and Launch Test
uv run python test_mlx_complete.py
```

## installation of main ML libraries

**Theory:** Selection and institutionalization of the ML library is critical for the creation of a Robst ML systems. Each library will solve specific problems and should be properly integrated into the ecosystem of the project.

```
ML Libraries Ecosystem:
┌─────────────────────────────────────────────────────────────┐
│ ML Libraries Architecture │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Core Libraries │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ NumPy │ │ Pandas │ │ Scikit │ │Matplotlib│ │ │
│ │ │ Arrays │ │ dataFrames│ Learn │ │ Plots │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Financial Libraries │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │YFinance │ │ TA-Lib │ │VectorBT │ │Backtrader│ │ │
│ │ │ data │ │Indicators│ │Backtest │ │ Strategy │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Advanced ML │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │XGBoost │ │LightGBM │ │CatBoost │ │ Optuna │ │ │
│ │ │Gradient │ │Gradient │ │Gradient │ │Hyperopt │ │ │
│ │ │ Boosting│ │ Boosting│ │ Boosting│ │ │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Deep Learning │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ PyTorch │ │TensorFlow│ │Transform│ │ MLX │ │ │
│ │ │ Neural │ │ Neural │ │ ers │ │ Apple │ │ │
│ │ │ networks│ │ networks │ │ NLP │ │ Native │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

Library dependencies Graph:
┌─────────────────────────────────────────────────────────────┐
│ Dependency Chain │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ MLX │◄───┤ PyTorch │◄───┤ NumPy │◄───┤ C++ │ │
│ │(Apple) │ │(Meta) │ │(Core) │ │(system) │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│ │ │ │ │ │
│ ▼ ▼ ▼ ▼ │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Metal │ │ MPS │ │ BLAS │ │ LAPACK │ │
│ │ GPU │ │ GPU │ │ Math │ │ Math │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

** ML library selection principles:**
- ** Specialization: ** Each library has specific objectives
- **Compatibility: ** Library should work together without conflict
- **Performance:** Optimization for M1 architecture
- **Active development:** Regular updates and community support
- **documentation:** Good documentation for rapid development

♪##1 ♪ Basic dependencies ♪

**Theory:** Basic libraries form the foundation of the ML system; they provide basic functionality for work with data, visualization and interactive development.

**NumPy is the basis of the numerical calculations:**
- **Theory:**NumPy provides effective operations with multidimensional arrays
- **Practice:** Basis for all ML library, optimized for M1
- ** Criticality:** Without NumPy, no Work with ML-algorithms is possible

**Pandas - Working with data:**
- **Theory:**Pandas provides powerful tools for Analysis and Data Processing
- **Practice:** DataFrame - basic data format for ML projects
- ** Criticality: ** needed for data loading, cleaning and pre-processing

**Scikit-learn - Classical ML algorithms:**
- **Theory:** Scikit-learn provides ready implementation of ML-algorithms
- ** Practice:** from simple linear models to complex ensembles
- ** Criticality:** Basis for most ML objectives

**Matplotlib and Seaborn - Visualization:**
- **Theory:** Visualization is critical for understanding data and results
- **Practice:** Matplotlib - basic graphs, Seaborn - statistical graphs
- ** Criticality: ** required for EDA and presentation of results

**Jupyter Notebook - Interactive Development:**
- **Theory:** Jupyter provides an interactive environment for experiments
- **Practice:**ideal for EDI, prototypes and demonstrations
- ** Criticality: ** Standard for ML-development

**Plotly and Dash - Interactive Graphics:**
- **Theory:** Interactive graphs improve understanding of data
- **Practice:**Plotly - interactive graphics, Dash - web applications
- ** Criticality: ** necessary for creating interactive dashboards

```bash
# installation of major libraries
uv add numpy pandas scikit-learn matplotlib seaborn
uv add jupyter notebook ipykernel
uv ad tabled dash # for interactive graphics
```

** Full test of main libraries:**

```python
# test_core_libraries.py
"""
Full test of core ML libraries for M1 Pro
Launch: uv run python test_core_libraries.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import plotly.graph_objects as go
import plotly.express as px
import time
import warnings
warnings.filterwarnings('ignore')

def test_numpy():
"Test NumPy."
"print("===NumPy Test===)

# Create arrays
 a = np.random.rand(1000, 1000)
 b = np.random.rand(1000, 1000)

# Test performance
 start_time = time.time()
 c = np.dot(a, b)
 end_time = time.time()

 print(f"NumPy Version: {np.__version__}")
Print(f"Matrix times 1000x1000:(end_time-start_time:.3f} seconds")
(pint(f" Outcome Form: {c.scape}")
"data type: {c.dtype}")

 # check BLAS
print(f"BLAS information: {np.show_config()}})

"Print" ("NumPy Works correctly")
 return True

def test_pandas():
"Test Pandas."
Print("\n===Pandas Test ===)

 # create dataFrame
 n_rows = 100000
 df = pd.dataFrame({
 'A': np.random.randn(n_rows),
 'B': np.random.randn(n_rows),
 'C': np.random.randn(n_rows),
 'category': np.random.choice(['X', 'Y', 'Z'], n_rows)
 })

 print(f"Pandas Version: {pd.__version__}")
 print(f"dataFrame shape: {df.shape}")
print(f) "DataFrame Memory: {df.memory_use(deep=True).sum() / 1024**2:.2f} MB")

# Group test
 start_time = time.time()
 grouped = df.groupby('category').agg({
 'A': ['mean', 'std'],
 'B': ['min', 'max'],
 'C': 'sum'
 })
 end_time = time.time()

spring(f) Group time: {end_time-start_time:.3f}seconds}
(f "Result of the group: \n\grouped.head()}")

"Prente Pandas Works correctly"
 return True

def test_matplotlib_seaborn():
"Text Matplotlib and Seaborn."
"print("\n===Matplotlib and Seaborn test===)

# Create testy data
 x = np.random.randn(1000)
 y = 2 * x + np.random.randn(1000) * 0.5

# Matplotlib Test
 plt.figure(figsize=(10, 6))
 plt.subplot(1, 2, 1)
 plt.scatter(x, y, alpha=0.6)
 plt.title('Matplotlib Scatter Plot')
 plt.xlabel('X')
 plt.ylabel('Y')

# Seaborn test
 plt.subplot(1, 2, 2)
 sns.scatterplot(x=x, y=y, alpha=0.6)
 plt.title('Seaborn Scatter Plot')

 plt.tight_layout()
 plt.savefig('test_plot.png', dpi=150, bbox_inches='tight')
 plt.close()

 print(f"Matplotlib Version: {plt.matplotlib.__version__}")
 print(f"Seaborn Version: {sns.__version__}")
Print("Grafik retained as test_plot.png")

"Matplotlib and Seaborn Working correctly"
 return True

def test_sklearn():
"Test Scikit-learn."
Print("\n===Scikit-learn test====)

# Create testy data
 X = np.random.randn(1000, 10)
 y = (X[:, 0] + X[:, 1] + np.random.randn(1000) * 0.1 > 0).astype(int)

# Data sharing
 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model learning
 model = RandomForestClassifier(n_estimators=100, random_state=42)

 start_time = time.time()
 model.fit(X_train, y_train)
 end_time = time.time()

# Premonition
 y_pred = model.predict(X_test)
 accuracy = accuracy_score(y_test, y_pred)

 print(f"Scikit-learn Version: {sklearn.__version__}")
Print(f) "Learning time: {end_time-start_time:.3f}seconds")
print(f "model accuracy: {accuracy:.3f}")
pprint(f) "The importance of the signs: {model.feature_importances_[:5]}}")

"spint" is correct.
 return True

def test_plotly():
"Text Plotly."
Print("\n===Plotly Test====)

# creative interactive graphics
 x = np.linspace(0, 10, 100)
 y1 = np.sin(x)
 y2 = np.cos(x)

 fig = go.Figure()
 fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='sin(x)'))
 fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='cos(x)'))

 fig.update_layout(
"Title"="Online Plotly',
 xaxis_title='X',
 yaxis_title='Y',
 hovermode='x unified'
 )

# Maintaining the schedule
 fig.write_html('test_plotly.html')

 print(f"Plotly Version: {plotly.__version__}")
print("Interactive schedule maintained as test_plottly.html")

"Plotly Works correctly"
 return True

def main():
"Principal function testing."
"Prent("♪ Launch full test of the main ML libraries")
 print("=" * 60)

 try:
 # Run all tests
 test_numpy()
 test_pandas()
 test_matplotlib_seaborn()
 test_sklearn()
 test_plotly()

 print("\n" + "=" * 60)
all the main libraries of Working are correct!
"Main ML libraries ready for use on M1 Pro")

 except Exception as e:
Print(f)\n\\\\\\\\\\\\\\\\\\\\\\\\\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}\\\\\\\\\}\\\\\\\\\\\\\\\\\\\\\\\}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}\\\\\\\\})
prent("check the installation of libraries")
 return False

 return True

if __name__ == "__main__":
 main()
```

**Launch tests of major libraries:**
```bash
# Conservation and Launch Test
uv run python test_core_libraries.py
```

♪##2 ♪ Financial libraries

**Theory:** Financial libraries are specialized for work with financial data and algorithms; they provide specific functionality for financial projects.

**YFinance - Financial Data uploading:**
- **Theory:** YFinance provides access to historical data from Yahoo Finance
- **Practice:** Simple Loading Data on Stock, Currency, Indexes
- ** Criticality:** Main source of data for financial ML projects

**Pandas-datareader - Alternative data sources:**
- **Theory:** Additional data sources for diversification
- **Practice:** FRED, Alpha Vantage, Quandl and other sources
- ** Criticality:** Reserve data sources

**TA-Lib - Technical indicators:**
- **Theory:**Technical indicators - the basis of technical Analisis
- **Practice:** RSI, MACD, Bollinger Bands and hundreds of other indicators
- ** Criticality: ** needed for trade strategies

**VectorBT - Vectorized Backtting:**
- **Theory:** Vectorized bactering provides high performance
- **Practice: ** Rapid testing of strategies on historical data
- ** Criticality: ** needed for the promotion of trade policies

**Backtrader - Alternative Baxter:**
- **Theory:** A more flexible approach to betting
- **Practice: ** Support for different types of data and strategies
- ** Criticality:** Alternative for complex strategies

```bash
# Financial data and analysis
uv add yfinance pandas-datareader
uv add ta-lib #Technical indicators
uv ad vectorbt # Vectorized backtting
uv ad backtrader # Alternative backtexter
```

♪## 3, advanced ML libraries

**Theory:** The advanced ML libraries provide modern algorithms and tools for building robst ML systems.

**XGBost, LightGBM, CatBoost - gradient bushing:**
- **Theory:** Gradient Busting is one of the most effective ML methods.
- **Practice: ** Each library has its advantages and optimization
- ** Criticality:** Basis for most ML competitions

**Optuna - hyperparametric optimization:**
- **Theory:** Automatic search for optimal hyperparameters
- **Practice:** Bayesian acceptance for effective search
- ** Criticality: ** needed to achieve maximum performance

**MLflow - MLOps:**
- **Theory:** MLOps ensures reproducibility and Management ML models
- **Practice:** Experimental tracking, model versioning
- ** Criticality: ** needed for production-ready systems

**Weights & Biases - Experiments:**
- **Theory:** Advanced tracking of experiments and visualization
- **Practice:** integration with different MLs
- ** Criticality:** Improves the process of developing ML models

```bash
# Advanced ML libraries
uv add xgboost lightgbm catboost
uv add optuna # Hyperparametric optimization
uv add mlflow # MLOps
uv ad wandb # Experiments
```

### 4. Deep Learning

**Theory:**Deep Learning libraries provide work with neural networks and modern ML-algorithms. on M1 is critical to use optimized versions.

**PyTorch - main frame:**
- **Theory:** PyTorch is the most flexible and popular frame for DL
- ** Practice:** Dynamic graphs, easy debugging
- ** Criticality: ** Standard for Research Projects

**TensorFlow - Alternative Framework:**
- **Theory:** TensorFlow provides static optimization
- ** Practice:** Better for production release
- ** Criticality: ** needed for compatibility with existing models

**Transformers - pre-trained models:**
- **Theory:** Hugging Face Transformers provides access to SOTA models
Practice:** BERT, GPT, T5 and hundreds of other models
- ** Criticality:** Basis for NLP and multimodal tasks

**Optification for M1:**
- **Theory:** M1 requires special versions of libraries
- **Practice:** Use of Metal Performance Shaders
- ** Criticality: ** needed for maximum performance

```bash
# Deep Learning (compatibility with M1)
uv add torch torchvision torchaudio
uv add tensorflow-macos tensorflow-metal # for M1
uv add transformers # Hugging Face
```

** Critically important for Robst ML systems:**
- **Compatibility:** All libraries should Work together
- **Performance:** Optimization for M1 architecture
- **Pressability:** Determinated versions of all libraries
- **Scalability:** Opportunity to work with big data

## configuration Jupyter Notebook

**Theory:**Jupyter Notebook is a critical tool for ML development that provides an interactive environment for experiments, Data Analysis and prototypes.

**Why Jupyter is critical for ML:**
- ** Interactive:** Allows to experiment with data in real time
- **Visualization:** In-house support for graphics and interactive widgets
- **documentation:** Combination of code, text and results
- ** Debugging:** Step-by-step execution of code for understanding algorithms
- **presentation:**ideal for demonstration of results and method Logsy

** The benefits of Jupiter for ML:**
- Rapid algorithm prototype.
- Interactive visualization of data
- Documentation of the development process
- Joint Working on projects
- Easy replicating experiments

**Jupyter's shortcomings:**
- Could be slow for big calculations.
- The difficulty of managing addictions
- Issues with versioning the code
-not suitable for production release

### square core for project

**Theory:** the separate Jupyter core for the project provides isolation dependency and reproducibility of results. This is critical for ML projects where the accuracy of the experiments is critical.

**Why is the individual kernel critical:**
- **Dependencies isolation:** Prevents conflicts between projects
- **Reproducibility:** Same results on different machines
- **Management versions:** Control of all libraries versions
- ** Safety:** Isolation from System Packages
- **Performance:** Optimization for a specific project

**the production process:**
1. **Initiation of the kernel:** creation of the new kernel with unique name
2. **installationdependencies:** installation all libraries
3. **configuring:**configuring parameters for best work
4. ** Testing:** heck of core performance

```bash
# Create Jupyter core
uv run python -m ipykernel install --User --name neozork-ml --display-name "NeoZorK ML"

# Launch Jupyter
uv run jupyter notebook
```

** Critical for ML projects:**
- **Reproducibility:** Same results on all machines
- **Isolation:** Conflict prevention dependencies
- **Performance:** Optimization for specific tasks
- **Management:** Easy switch between projects

### configuration Jupyter

**Theory:** The correct conference Jupyter is critical for optimal work on M1. Settings should take into account the features of the Apple Silicon architecture and the requirements of the ML projects.

** Key Settings for M1:**
- **Performance:** Optimization for M1 architecture
- **Remark:**configuration of memory limits for large datasets
- **Network:**configuring for remote access
- ** Security:** configuring access rights
- **Stability: ** Prevention of large-calculations failures

**Settings performance:**
- **iopub_data_rate_limit:** Increased data transfer limit
- **rate_limit_window:** configurization of the speed limitation window
- **memory_limit:**Restriction on the use of memory
- **timeout:**configuring timeouts for operations

**Settings safety:**
- **allow_root:**Launch permission from root (for Docker)
- **ip:**configuring IP addresses for access
- **port:**configuring port for connection
- **open_browser:** Disable automatically opening the browser

```python
# jupyter_config.py
c = get_config()

# Settings for M1
c.NotebookApp.allow_root = True
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False

# Optimization for M1
c.NotebookApp.iopub_data_rate_limit = 1000000000
c.NotebookApp.rate_limit_window = 3.0
```

** Full Jupyter configuration test:**

```python
# test_jupyter_config.py
"""
Full Jupyter configuration test for M1 Pro
Launch: uv run python test_jupyter_config.py
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def test_jupyter_installation():
"Test installation Jupyter."
"print("===A test of installation Jupyter====)

 try:
 import jupyter
 print(f"Jupyter Version: {jupyter.__version__}")

 import notebook
 print(f"Notebook Version: {notebook.__version__}")

 import ipykernel
 print(f"IPython Kernel Version: {ipykernel.__version__}")

"Jupyter installed correctly"
 return True

 except importError as e:
 print(f"❌ Jupyter not installed: {e}")
 return False

def test_jupyter_kernels():
"The Test of Accessible Jupyter Cores."
Print("\n===Jupyter core test===)

 try:
# Getting a list of the kernels
 result = subprocess.run(['jupyter', 'kernelspec', 'List'],
 capture_output=True, text=True)

 if result.returncode == 0:
pprint("Endable kernels:")
 print(result.stdout)

# Check of neozork-ml core
 if 'neozork-ml' in result.stdout:
"Prind("\\\\\\\\\\\\\\\\\\\\nozork-ml forward)}
 else:
"Prind("♪ Neozork-ml nofundo core")
"Bring the core: uv run python -m ipykernel install --User --name neozork-ml")
 else:
Print(f"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\s\\\\\\\\\\\\\\\\\\\\\\\\\\}}}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}}}\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}}}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}}}}}}}}}}}}}}}}}}}}\\\\\\\\\\\\\\\\\\\\\}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}

 except Exception as e:
Print(f"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}}}}}}}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}})

 return True

def test_jupyter_config():
"Jupyter configuration test"
Print("\n===Jupyter configuration test===)

# Paths to configuration
 config_paths = [
 Path.home() / '.jupyter' / 'jupyter_notebook_config.py',
 Path.home() / '.jupyter' / 'jupyter_notebook_config.json',
 Path.home() / '.jupyter' / 'jupyter_lab_config.py',
 Path.home() / '.jupyter' / 'jupyter_lab_config.json'
 ]

"Looking for configuration files:")
 for path in config_paths:
 if path.exists():
 print(f" ✅ found: {path}")
 else:
 print(f" ⚠️ not found: {path}")

#free basic configuration
 jupyter_dir = Path.home() / '.jupyter'
 jupyter_dir.mkdir(exist_ok=True)

 config_file = jupyter_dir / 'jupyter_notebook_config.py'

 if not config_file.exists():
Print("n Formation of basic configuration...")
 config_content = '''# Jupyter Notebook Configuration for M1 Pro
c = get_config()

# Settings for M1
c.NotebookApp.allow_root = True
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False

# Optimization for M1
c.NotebookApp.iopub_data_rate_limit = 1000000000
c.NotebookApp.rate_limit_window = 3.0

# Additional Settings
c.NotebookApp.notebook_dir = '.'
c.NotebookApp.allow_origin = '*'
c.NotebookApp.disable_check_xsrf = True
'''

 with open(config_file, 'w') as f:
 f.write(config_content)

print(f"\configuration created: {config_file}}
 else:
Print(f) already exists: {config_file})

 return True

def test_jupyter_performance():
"Test performance Jupyter."
"print("\n=== Test performance Jupyter====)

# Create test notebook
 test_notebook = {
 "cells": [
 {
 "cell_type": "code",
 "execution_count": None,
 "metadata": {},
 "outputs": [],
 "source": [
 "import numpy as np\n",
 "import time\n",
 "\n",
"# Test performance\n"
 "size = 5000\n",
 "a = np.random.rand(size, size)\n",
 "b = np.random.rand(size, size)\n",
 "\n",
 "start = time.time()\n",
 "c = np.dot(a, b)\n",
 "end = time.time()\n",
 "\n",
"print(f'Reason of matrix times x(size)}: {end-start:.3f}seconds')\n",
 "print(f'performance: {size**3 / (end - start) / 1e9:.2f} GFLOPS')"
 ]
 }
 ],
 "metadata": {
 "kernelspec": {
 "display_name": "Python 3",
 "language": "python",
 "name": "python3"
 }
 },
 "nbformat": 4,
 "nbformat_minor": 4
 }

# Maintaining the test notebook
 test_file = Path('test_performance.ipynb')
 with open(test_file, 'w') as f:
 json.dump(test_notebook, f, indent=2)

pprint(f"\tests notebook created: {test_file})
print("Stop Jupyter and open this file for testing")

 return True

def test_jupyter_startup():
"The Launcha Jupyter Test."
"print("\n===Launcha Jupyter Test=========================================)=======Lunch Jupyter test======)

"team for Launch Jupyter:")
 print("1. Jupyter Notebook:")
 print(" uv run jupyter notebook")
 print("2. Jupyter Lab:")
 print(" uv run jupyter lab")
"spint("3. with specific kernel:")
 print(" uv run jupyter notebook --kernel=neozork-ml")

port accessibility:)
 try:
 import socket
 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 result = sock.connect_ex(('localhost', 8888))
 if result == 0:
"Prent("~ Port 8888 already occupied")
 else:
port 8888 is free)
 sock.close()
 except Exception as e:
port inspection error: {e})

 return True

def main():
"Principal function testing."
print("\"Launch full Jupyter configuration test")
 print("=" * 60)

 try:
 # Run all tests
 test_jupyter_installation()
 test_jupyter_kernels()
 test_jupyter_config()
 test_jupyter_performance()
 test_jupyter_startup()

 print("\n" + "=" * 60)
Print("
"Jupyter is ready for use on M1 Pro"

 except Exception as e:
Print(f)\n\\\\\\\\\\\\\\\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}\\\\\\\\\}\\\\\\\\\\\\\\\}\\\\\\\\\\\\}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}\\\\\\\\\\\\\}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}}}}}}}}}}\\\\\\\\\\\\\\\\\\\\\\\}}}}}}}}}}}}}}}}\\\\\\\\\\\\\\\\\\for for-for for-
 return False

 return True

if __name__ == "__main__":
 main()
```

**Launch Jupyter test:**
```bash
# Conservation and Launch Test
uv run python test_jupyter_config.py
```

** Additional Settings for ML projects:**
- **Cashing:**configuring caches for processing work
- ** Parallelism:** configuring multi-accuracy for M1
- **Visualization:**configuring for interactive graphics
- ** Extensions:** installation of useful extensions

** Critically important for Robst ML systems:**
- **Stability: ** Prevention of large-calculations failures
- **Performance:** Maximum use of M1
- **Scalability:** Opportunity to work with big data
- **Reproducibility:** Same results on all machines

## Optimization for M1 Pro

**Theory:** Optimization for M1 Pro is critical for achieving maximum performance ML systems. M1 Pro has a unique architecture that requires special Settings for optimal work.

**Why optimization is critical:**
- ** Architecture:** M1 Pro has a specific architecture requiring special Settings
- **Performance:** Correct optimization can increase performance by 3-5 times
- ** Energy efficiency:** Optimization reduces energy consumption and heat
- **Stability:** Correct configuration prevents malfunctions with large calculations
- **Scalability:** Optimization allows Working with big data

** Key optimization areas:**
- **changed environment:** conference for optimum use of resources
- **NumPy:** Optimization for M1 architecture
- **PyTorch:** Use of Metal Performance Shaders
- ** Memory:** Optimization of the use of Unified Memorial
- ** Parallelism:** configurization of multi-accuracy

♪##1. configuration of the variable environments

**Theory:** The changing environment controls the behaviour of the ML library and operating system.

** Key variables for M1 Pro:**
- **PYTHONUNBUFFERED:** Provides immediate output
- **OMP_NUM_THIREDS:** Controls OpenMP flow rates
- **MKL_NUM_THIREDS:**configuring Intel MKL (if used)
- **NUMEXPR_NUM_THIREADS:**configuring NumberExpr for parallel calculations

**MLX specific variables:**
- **MLX_USE_METAL:** Inclusion of Metal Performance Shaders
- **MLX_Use_NEURAL_ENGINE:** Use of National Engineering
- **MLX_Use_CPU:** Fallback on CPU if necessary

** Optimal values for M1 Pro:**
- **8 streams:** Optimally for M1 Pro (8 production kernels)
- **Metal:** Included for GPU assessment
- **Neural Engineering:** Including for specialized operations

```bash
# ~/.zshrc
export PYTHONUNBUFFERED=1
OMP_NUM_THIREDS=8 # Optimal for M1 Pro
export MKL_NUM_THREADS=8
export NUMEXPR_NUM_THREADS=8

# MLX Optimization
export MLX_Use_METAL=1
export MLX_Use_NEURAL_ENGINE=1
```

** Full test of variable environments:**

```python
# test_environment.py
"""
Full test of environmental variables for M1 Pro
Launch: uv run python test_environment.py
"""

import os
import sys
import platform
import subprocess
import numpy as np
import torch

def test_system_info():
"The System Information Test."
"print("=== System information===)

(f "Operational system: {platform.system()} {platform.release()}")
 print(f"architecture: {platform.machine()}")
(f "Processor: {platform.processor()}")
 print(f"Python Version: {sys.version}")
(f"Python route: {sys.executable})

 # check M1 Pro
 if platform.machine() == 'arm64':
"Print(" ♪ Found by Apple Silicon (M1/M2/M3)")
 else:
("\ not Apple Silicon - some optimizations can not Working)

 return True

def test_environment_variables():
"Text of the variable environment."
"Prent("\n===Switched environment===)

# Key variables
 env_vars = {
 'PYTHONUNBUFFERED': '1',
 'OMP_NUM_THREADS': '8',
 'MKL_NUM_THREADS': '8',
 'NUMEXPR_NUM_THREADS': '8',
 'MLX_Use_METAL': '1',
 'MLX_Use_NEURAL_ENGINE': '1'
 }

Print("check variable environment:")
 for var, expected in env_vars.items():
value = os.environ.get(var, 'not 'A')
 status = "✅" if value == expected else "⚠️"
 print(f" {status} {var}: {value}")

 # check PATH
(f'nPATH contains uv: {'uv' in os.environ.get('PATH', '')})
(f"PATH contains homebrew: {'homebrew' in os.environ.get('PATH', '')})

 return True

def test_numpy_optimization():
"The NumPy Optimisation Test."
== sync, corrected by elderman == @elder_man

# Information about BLAS
"BLAS Information:")
 np.show_config()

# Test performance
"print("nTest performance NumPy:")
 sizes = [1000, 2000, 5000]

 for size in sizes:
 a = np.random.rand(size, size)
 b = np.random.rand(size, size)

 import time
 start = time.time()
 c = np.dot(a, b)
 end = time.time()

 duration = end - start
 gflops = size**3 / duration / 1e9
Print(f) Matrix {size}x {size}: {security:.3f}s, {gflops:.2f}GFLOPS}

 return True

def test_pytorch_mps():
"Test PyTorch MPS."
 print("\n=== PyTorch MPS ===")

 print(f"PyTorch Version: {torch.__version__}")
 print(f"MPS available: {torch.backends.mps.is_available()}")
Print(f"MPS built: {torch.backends.mps.is_bult()}})

 if torch.backends.mps.is_available():
 device = torch.device("mps")
"print("\mps avalable-test...")

# Test on MPS
 x = torch.randn(1000, 1000, device=device)
 y = torch.randn(1000, 1000, device=device)

 import time
 start = time.time()
 z = torch.mm(x, y)
 end = time.time()

Print(f" MPS matrix multiplication: {end-start:.3f}seconds}
print(f) result on device: {z.device})
 else:
 print("⚠️ MPS not available - Use CPU")

 return True

def test_mlx_availability():
""MLX Accessibility Test""
 print("\n=== MLX Framework ===")

 try:
 import mlx.core as mx
 print(f"MLX Version: {mx.__version__}")
(pint(f) Accessable devices: {mx.devises()})
pprint(f) "Device: {mx.default_device()}")

# A simple test
 a = mx.array([1, 2, 3, 4, 5])
 b = mx.array([5, 4, 3, 2, 1])
 c = a + b
Print(f" Transaction test: {c})

"MLX Works correctly"
 return True

 except importError:
 print("❌ MLX not installed")
 return False

def test_memory_usage():
"The "Memorial Use Test""
Print("\n===Memorial use===)

 try:
 import psutil
 process = psutil.Process()
 memory_info = process.memory_info()

Print(f" Use of memory by process: {memory_info.rss / 1024**2:.2f} MB")
"Virtual memory: {memory_info.vms / 1024**2:.2f} MB")

# System memory
 system_memory = psutil.virtual_memory()
(f) "General memory of the system: {system_memory.total / 1024**3:.2f}GB")
print(f) "Accepted memory: {system_memory.available / 1024**3:.2f}GB")
pprint(f" Use of memory: {system_memory.percent:.1f}%")

 except importError:
 print("psutil not installed - install: uv add psutil")

 return True

def main():
"Principal function testing."
"prent("\\Launch full test environment M1Pro")
 print("=" * 60)

 try:
 # Run all tests
 test_system_info()
 test_environment_variables()
 test_numpy_optimization()
 test_pytorch_mps()
 test_mlx_availability()
 test_memory_usage()

 print("\n" + "=" * 60)
Print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)))
print("check the results above for diagnostic problems")

 except Exception as e:
Print(f)\n\\\\\\\\\\\\\\\\\\\\\\\\\n\\\\\\\\\\\\\\\\\\\\\\\\\\\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}\\\\}\\\\\\\\\})
 return False

 return True

if __name__ == "__main__":
 main()
```

**Launch test environment:**
```bash
# Conservation and Launch Test
uv run python test_environment.py
```

** Critical for ML projects:**
- **Reproducibility:** Same Settings on all machines
- **Performance:** Maximum use of M1 Pro resources
- **Stability: ** Prevention of large-calculations failures
- ** Energy efficiency:** Optimal energy consumption

### 2. configuration NumPy for M1

**Theory:**NumPy is the foundation of all ML library, so its optimization is critical for the performance of the entire system. M1 Pro requires special Settings for optimal work.

**NumPy key optimization:**
- **BLAS libraries:** Use of optimized BLAS for M1
- ** Memory:** Optimization of the use of Unified Memorial
- ** Parallelism:** configurization of multi-accuracy
- **Cashing:**Cash optimization

**check optimization:**
- **Version:** Make sure the correct version is used
- **BLAS:** Check the use of optimized BLAS
- **architecture:**confirm in support of ARM64
- **Performance:** Testing on Real Tasks

** Testing performance:**
- ** Matrix operations:** Basic operations test
- ** Memory:** Test of work with large arrays
- ** Parallelism:** Multi-accuracy test
- **comparison:**comparison with reference values

```python
# numpy_config.py
import numpy as np

# Check Optimization
print(f"NumPy Version: {np.__version__}")
print(f"BLAS info: {np.show_config()}")

# Test performance
import time

# A matrix operation test
size = 5000
a = np.random.rand(size, size)
b = np.random.rand(size, size)

start = time.time()
c = np.dot(a, b)
end = time.time()

print(f"Matrix multiplication time: {end - start:.2f} seconds")
```

** Critical for ML projects:**
- **Performance:**NumPy - the basis of all calculations
- **Compatibility:** Correct Working with other libraries
- **Stability:** Prevention of computational errors
- **Scalability:**Working with big data

### 3. configuration PyTorch for M1

**Theory:** PyTorch on M1 Pro can use Metal Performance Shaders (MPS) for GPU accreditation. The correct conference is critical for maximum performance.

**MPS (Metal Performance Shaders):**
- **Theory:** MPS provides a GPU acceleration on Apple Silicon
- ** Practice:** Automatic use of GPU for suitable operations
- ** Benefits:** to 10x acceleration for certain operations
- **Restrictions:**not all operations are supported

**check MPS:**
- **capability:** heck of an MPS support
- **Device: ** Selection of the correct device
- **Performance:** Testing ancceleration
- **Compatibility:** sheck work with models

**Optification for M1 Pro:**
- ** Memory:** Use of Universaled Memorial
- ** Parallelism:** configurization of multi-accuracy
- **Cashing:** Cache optimization
- **Operations:** Choice of optimal operations

```python
# pytorch_m1_config.py
import torch

# check MPS (Metal Performance Shaders)
if torch.backends.mps.is_available():
 device = torch.device("mps")
 print("MPS available!")
else:
 device = torch.device("cpu")
 print("MPS not available, Use CPU")

# Test performance
x = torch.randn(1000, 1000, device=device)
y = torch.randn(1000, 1000, device=device)

start = time.time()
z = torch.mm(x, y)
end = time.time()

print(f"PyTorch MPS time: {end - start:.2f} seconds")
```

** Critical for ML projects:**
- **Performance:** GPU acceleration critical for large models
- **Compatibility:** Correct Working with existing code
- **Stability:** Prevention of learning failures
- **Scalability:** Opportunity to work with big data

** Additional optimization:**
- ** Mixed accuracy:** Use of float16 for calculation
- ** Gradient checks:** Optimization of memory during training
- ** Parallelism:**configuring dataLoader for multi-accuracy
- **Cashing:**Cash optimization

## the project's creation

**Theory:** the correct structure of the project is critical for Robst ML systems. A well-organized Structure ensures that the project is scalable, supportive and reproducible.

```
Project Structure Visualization:
┌─────────────────────────────────────────────────────────────┐
│ NeoZorK ML Project Structure │
├─────────────────────────────────────────────────────────────┤
│ │
│ neozork-ml-system/ │
│ ├── src/ # Source Code │
│ │ ├── data/ # data Processing │
│ │ │ ├── loaders.py # data Loaders │
│ │ │ └── preprocessors.py # data Preprocessing │
│ │ ├── features/ # Feature Engineering │
│ │ │ ├── engineering.py # Feature Creation │
│ │ │ └── indicators.py # Technical Indicators │
│ │ ├── models/ # ML Models │
│ │ │ ├── base.py # Base Classes │
│ │ │ ├── ml.py # Classical ML │
│ │ │ └── deep.py # Deep Learning │
│ │ ├── backtesting/ # Backtesting Engine │
│ │ │ ├── engine.py # Backtest Engine │
│ │ │ └── metrics.py # Performance Metrics │
│ │ └── deployment/ # Production deployment │
│ │ ├── api.py # REST API │
│ │ └── blockchain.py # Blockchain integration │
│ ├── data/ # data Storage │
│ │ ├── raw/ # Raw data │
│ │ ├── processed/ # Processed data │
│ │ └── features/ # Feature data │
│ ├── models/ # Model Storage │
│ │ ├── trained/ # Trained Models │
│ │ └── artifacts/ # Model Artifacts │
│ ├── notebooks/ # Jupyter Notebooks │
│ │ ├── 01_data_exploration.ipynb │
│ │ ├── 02_feature_engineering.ipynb │
│ │ ├── 03_model_training.ipynb │
│ │ └── 04_backtesting.ipynb │
│ ├── tests/ # Unit tests │
│ │ ├── test_data.py # data tests │
│ │ ├── test_features.py # Feature tests │
│ │ ├── test_models.py # Model tests │
│ │ └── test_backtesting.py # Backtest tests │
│ ├── config/ # Configuration │
│ │ ├── config.yaml # main Config │
│ │ └── logging.yaml # Logging Config │
│ ├── scripts/ # Automation Scripts │
│ │ ├── train.py # Training Script │
│ │ ├── backtest.py # Backtesting Script │
│ │ └── deploy.py # deployment Script │
│ ├── pyproject.toml # Project dependencies │
│ ├── README.md # Project Documentation │
│ └── .gitignore # Git Ignore Rules │
└─────────────────────────────────────────────────────────────┘

ML Pipeline Flow:
┌─────────────────────────────────────────────────────────────┐
│ ML Pipeline Flow │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ data │───▶│Features │───▶│ Models │───▶│Backtest │ │
│ │ Loading │ │Engineering│ │Training │ │ │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│ │ │ │ │ │
│ ▼ ▼ ▼ ▼ │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Raw │ │Processed│ │ Trained │ │ Results │ │
│ │ data │ │ Features│ │ Models │ │ │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Why Project Structure is critical:**
- **Scalability:** Makes it easy to add new components
- ** Maintenance:** Simplifies understanding and modification of the code
- **Reproducibility:** Provides the same structure on all machines
- ** Joint Working:**Simplifies work in team
- ** Business: ** Simplifies deployment in production

** Principles for the organization of ML projects:**
- ** Modularity:** Division on Logs
- ** Division of responsibility: ** Each moduule solves specific tasks
- **Incapsulation:** Internal implementation cover
- ** Extension: ** Possible addition of new modules
- ** Testability:** Easy testing of each module

### Project Structure

**Theory:** Project Structure should reflect the phases of the ML-pipline and provide the Logsche code organization. Each folder has a specific purpose and contains linked components.

** Main structures:**

**src/ - source code:**
- **Theory:** Contains the entire project source code
- ** Practice:** Separated on methods on functionality
- ** Criticality:** Foundation of the whole system

**data/ - data:**
- **Theory:** Storage all project data
- **Practice:** Division on rave, processed, features
- ** Criticality: ** Need for reproducibility

**models/-models:**
- **Theory:** Storage of trained models and artifacts
- **Practice:** Separation on trade and artifacts
- ** Criticality: ** Need for replication

**Notebooks/ - Experiments:**
- **Theory:**Jupyter notes for experiments and Analysis
- ** Practice:** Numbering and descriptive names
- ** Criticality: ** Documentation of the development process

**tests/ - tests:**
- **Theory:**Unt tests for all components
- ** Practice:** Conformity of structure src/
- ** Criticality: ** Code quality assurance

**config/ - configuration:**
- **Theory:** Project configuration files
- **Practice:** YAML files for settings
- ** Criticality:** Management system parameters

**scripts/ - scripts:**
- **Theory:** Playable scripts for automation
- **Practice:** Selected scripts for disferent taxes
- ** Criticality:** Automation of routine operations

```
neozork-ml-system/
├── src/
│ ├── __init__.py
│ ├── data/
│ │ ├── __init__.py
│ │ ├── loaders.py
│ │ └── preprocessors.py
│ ├── features/
│ │ ├── __init__.py
│ │ ├── engineering.py
│ │ └── indicators.py
│ ├── models/
│ │ ├── __init__.py
│ │ ├── base.py
│ │ ├── ml.py
│ │ └── deep.py
│ ├── backtesting/
│ │ ├── __init__.py
│ │ ├── engine.py
│ │ └── metrics.py
│ └── deployment/
│ ├── __init__.py
│ ├── api.py
│ └── blockchain.py
├── data/
│ ├── raw/
│ ├── processed/
│ └── features/
├── models/
│ ├── trained/
│ └── artifacts/
├── notebooks/
│ ├── 01_data_exploration.ipynb
│ ├── 02_feature_engineering.ipynb
│ ├── 03_model_training.ipynb
│ └── 04_backtesting.ipynb
├── tests/
│ ├── __init__.py
│ ├── test_data.py
│ ├── test_features.py
│ ├── test_models.py
│ └── test_backtesting.py
├── config/
│ ├── config.yaml
│ └── logging.yaml
├── scripts/
│ ├── train.py
│ ├── backtest.py
│ └── deploy.py
├── pyproject.toml
├── README.md
└── .gitignore
```

**Detail describe modules:**

**src/data/ - Working with data:**
- **loaders.py:** Loading data from various sources
- **Preprocessors.py:** Pre-processed and clear data
- ** Criticality:** Basis for all ML operations

**src/features/ - Signs engineering:**
- **englishing.py:**create new features
- **indicators.py:** Technical indicators
- ** Criticality: ** The quality of the indicators determines the quality of the model

**src/models/ - ML models:**
- **base.py:** Basic classes for models
- **ml.py:** Classical ML algorithms
- **deep.py:** Neuronets
- ** Criticality:**heart of the ML system

**src/backtesting/-backing:**
- **engine.py:**backsing engine
- **metrics.py:** Metrics performance
- ** Criticality:** evaluation of trade policies

**src/deployment/-deployment:**
- **api.py:**REST API for the model
- **blockchain.py:** integration with blocker
- ** Criticality:** Production-ready system

♪## Initiating the project

**Theory:** Project initiation consists of a core folder structure, dependency settings and environmental configuration.

** Initialization units:**
1. **create structure:**free all reference folders
2. **Initiating uv:**configuring bag manager
3. **installationdependencies:** installation all libraries
4. **configuring:**configuring project parameters
5. **Texting:** sheck workability

** Critical for ML projects:**
- **Reproduction:** Same Structure on All Machines
- **Scalability:** Possible addition of new components
- ** Supportability:** Easy understanding and modification
- ** Testability: ** Testability of each component

```bash
# creative structure
mkdir -p neozork-ml-system/{src/{data,features,models,backtesting,deployment},data/{raw,processed,features},models/{trained,artifacts},notebooks,tests,config,scripts}

# Transition in project
cd neozork-ml-system

# Initiating uv
uv init --python 3.11

# installation dependencies
uv add numpy pandas scikit-learn matplotlib seaborn
uv add jupyter notebook ipykernel
uv add yfinance ta-lib vectorbt
uv add xgboost lightgbm catboost
uv add torch torchvision
uv add mlx
uv add optuna mlflow wandb
```

** Further initialization steps:**
- **create .gitignore:** Deletion of unnecessary files from Git
- **configuring pre-committee:** Automatic heck code
- **create README:** documentation project
- **configuring CI/CD:** Automation of testing and guitar
- **create configuration:**configuring system parameters

## installation check

```
installation Verification Process:
┌─────────────────────────────────────────────────────────────┐
│ installation Verification │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ system check │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ macOS │ │ M1 Pro │ │ RAM │ │ Storage │ │ │
│ │ │ Version │ │ Chip │ │ 32GB │ │ 500GB+ │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Package check │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ uv │ │ Python │ │ Homebrew│ │ MLX │ │ │
│ │ │ 3.11+ │ │ 3.11+ │ │ Latest │ │ Latest │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Performance Test │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │ NumPy │ │ Pandas │ │ PyTorch │ │ MLX │ │ │
│ │ │ Matrix │ │ GroupBy │ │ MPS │ │ GPU │ │ │
│ │ │ Ops │ │ Ops │ │ Ops │ │ Ops │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

Expected Performance Benchmarks:
┌─────────────────┬──────────┬──────────┬──────────┐
│ Library │ Task │ Time │ Target │
├─────────────────┼──────────┼──────────┼──────────┤
│ NumPy │ 10k×10k │ <2.0s │ Matrix │
│ Pandas │ 1M rows │ <5.0s │ GroupBy │
│ PyTorch (MPS) │ 5k×5k │ <1.0s │ Matrix │
│ MLX (GPU) │ 5k×5k │ <0.5s │ Matrix │
│ Scikit-learn │ 100k×100 │ <10.0s │ RF Fit │
└─────────────────┴──────────┴──────────┴──────────┘
```

** Full test of all libraries:**

```python
# test_all_libraries.py
"""
Full test all ML libraries for M1 Pro
Launch: uv run python test_all_libraries.py
"""

import sys
import time
import warnings
warnings.filterwarnings('ignore')

def test_system_requirements():
"The System Requirements Test"
"print("== System requirements test==)

 import platform
 import psutil

# System information
{platform.system()} {platform.release()}})
 print(f"architecture: {platform.machine()}")
(f "Processor: {platform.processor()}")

# Memory
 memory = psutil.virtual_memory()
(f) General memory: {mory.total / 1024**3:.1f}GB)
print(f) "Accepted memory: {memory.available / 1024**3:.1f}GB")

 # check M1
 if platform.machine() == 'arm64':
"Apple Silicon detected"
 else:
 print("⚠️ not Apple Silicon")

 return True

def test_core_libraries():
"Text of the main libraries."
Print("\n===Main libraries test===)

 libraries = [
 ('numpy', 'np'),
 ('pandas', 'pd'),
 ('matplotlib', 'plt'),
 ('seaborn', 'sns'),
 ('sklearn', 'sklearn'),
 ('plotly', 'plotly')
 ]

 for lib_name, alias in libraries:
 try:
 if alias == 'plt':
 import matplotlib.pyplot as plt
 print(f"✅ {lib_name}: {plt.matplotlib.__version__}")
 elif alias == 'sns':
 import seaborn as sns
 print(f"✅ {lib_name}: {sns.__version__}")
 elif alias == 'sklearn':
 import sklearn
 print(f"✅ {lib_name}: {sklearn.__version__}")
 else:
 lib = __import__(lib_name)
 print(f"✅ {lib_name}: {lib.__version__}")
 except importError:
 print(f"❌ {lib_name}: not installed")

 return True

def test_financial_libraries():
"Text of financial libraries."
Prent("\n=== Financial library test===)

 financial_libs = [
 'yfinance',
 'pandas_datareader',
 'talib',
 'vectorbt',
 'backtrader'
 ]

 for lib in financial_libs:
 try:
 if lib == 'pandas_datareader':
 import pandas_datareader as pdr
 print(f"✅ {lib}: {pdr.__version__}")
 elif lib == 'talib':
 import talib
 print(f"✅ {lib}: {talib.__version__}")
 else:
 lib_module = __import__(lib)
 print(f"✅ {lib}: {lib_module.__version__}")
 except importError:
 print(f"❌ {lib}: not installed")

 return True

def test_advanced_ml_libraries():
"Text of Advanced ML libraries."
Prent("\n===A test of advanced ML libraries===)

 advanced_libs = [
 'xgboost',
 'lightgbm',
 'catboost',
 'optuna',
 'mlflow',
 'wandb'
 ]

 for lib in advanced_libs:
 try:
 lib_module = __import__(lib)
 print(f"✅ {lib}: {lib_module.__version__}")
 except importError:
 print(f"❌ {lib}: not installed")

 return True

def test_deep_learning_libraries():
"Test Deep Learning libraries."
\n===Deep Learning Library Test===)

 # PyTorch
 try:
 import torch
 print(f"✅ PyTorch: {torch.__version__}")
 print(f" MPS available: {torch.backends.mps.is_available()}")
== sync, corrected by elderman == @elder_man
 except importError:
 print("❌ PyTorch: not installed")

 # TensorFlow
 try:
 import tensorflow as tf
 print(f"✅ TensorFlow: {tf.__version__}")
 print(f" Metal available: {tf.config.List_physical_devices('GPU')}")
 except importError:
 print("❌ TensorFlow: not installed")

 # MLX
 try:
 import mlx.core as mx
 print(f"✅ MLX: {mx.__version__}")
(pint(f) Devices: {mx.devises()})
 except importError:
 print("❌ MLX: not installed")

 # Transformers
 try:
 import transformers
 print(f"✅ Transformers: {transformers.__version__}")
 except importError:
 print("❌ Transformers: not installed")

 return True

def test_jupyter_setup():
"Text Settings Jupiter."
\n===Settings Jupyter Test==============Settings Jupyter test============Settings test====================Settings Jupyter test==============Settings test=========================================Settings test======================Settingings test=====

 try:
 import jupyter
 import notebook
 import ipykernel
 print(f"✅ Jupyter: {jupyter.__version__}")
 print(f"✅ Notebook: {notebook.__version__}")
 print(f"✅ IPython Kernel: {ipykernel.__version__}")

# Check cores
 import subprocess
 result = subprocess.run(['jupyter', 'kernelspec', 'List'],
 capture_output=True, text=True)
 if result.returncode == 0:
pprint("Endable kernels:")
 print(result.stdout)
 else:
print("\\not has been able to get the list of kernels")

 except importError as e:
 print(f"❌ Jupyter: {e}")

 return True

def test_performance_benchmarks():
"The Test Performance."
Print("\n=== Test performance===)

# NumPy Test
 try:
 import numpy as np
 print("NumPy performance:")
 size = 5000
 a = np.random.rand(size, size)
 b = np.random.rand(size, size)

 start = time.time()
 c = np.dot(a, b)
 end = time.time()

 duration = end - start
 gflops = size**3 / duration / 1e9
Print(f) Matrix {size}x {size}: {security:.3f}s, {gflops:.2f}GFLOPS}

 except Exception as e:
prent(f"♪ NumPy Test: {e}})

# PyTorch MPS Test
 try:
 import torch
 if torch.backends.mps.is_available():
 print("PyTorch MPS performance:")
 device = torch.device("mps")
 size = 3000
 a = torch.randn(size, size, device=device)
 b = torch.randn(size, size, device=device)

 start = time.time()
 c = torch.mm(a, b)
 end = time.time()

 duration = end - start
 gflops = size**3 / duration / 1e9
(f) MPS matrix {size}x {size}: {security:.3f}s, {gflops:.2f}GFLOPS}
 else:
 print("⚠️ MPS not available")

 except Exception as e:
print(f"♪ PyTorch Test: {e}})

# MLX Test
 try:
 import mlx.core as mx
 print("MLX performance:")
 size = 3000
 a = mx.random.normal((size, size))
 b = mx.random.normal((size, size))

 start = time.time()
 c = mx.matmul(a, b)
 end = time.time()

 duration = end - start
 gflops = size**3 / duration / 1e9
== sync, corrected by elderman == @elder_man

 except Exception as e:
Print(f"\MLX test: {e}})

 return True

def test_environment_variables():
"Text of the variable environment."
Print("\n===A variable environment test===)

 import os

 env_vars = {
 'PYTHONUNBUFFERED': '1',
 'OMP_NUM_THREADS': '8',
 'MKL_NUM_THREADS': '8',
 'NUMEXPR_NUM_THREADS': '8',
 'MLX_Use_METAL': '1',
 'MLX_Use_NEURAL_ENGINE': '1'
 }

 for var, expected in env_vars.items():
value = os.environ.get(var, 'not 'A')
 status = "✅" if value == expected else "⚠️"
 print(f" {status} {var}: {value}")

 return True

def main():
"Principal function testing."
"Print("♪ Launch full test all libraries M1Pro")
 print("=" * 70)

 try:
 # Run all tests
 test_system_requirements()
 test_core_libraries()
 test_financial_libraries()
 test_advanced_ml_libraries()
 test_deep_learning_libraries()
 test_jupyter_setup()
 test_performance_benchmarks()
 test_environment_variables()

 print("\n" + "=" * 70)
The full test has been completed!
print("check the results above for diagnostic problems")
Prent("n Next Steps:")
"pint("1. Correct all errors ()")
print("2. Please check the warnings (.)")
print("3... run the performance tests)
"print("4. Move to the next section")

 except Exception as e:
Print(f)(\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}})
 return False

 return True

if __name__ == "__main__":
 main()
```

**Launch full test:**
```bash
# Saving and Launch Full Test
uv run python test_all_libraries.py
```

### Test performance

```python
# performance_test.py
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import torch

def test_numpy_performance():
"Test performance NumPy on M1"
 print("testing NumPy performance...")

# Big matrix
 size = 10000
 a = np.random.rand(size, size)
 b = np.random.rand(size, size)

 start = time.time()
 c = np.dot(a, b)
 end = time.time()

 print(f"NumPy matrix multiplication: {end - start:.2f} seconds")
 return end - start

def test_pandas_performance():
"The Test of Performance Pandas on M1"
 print("testing Pandas performance...")

# Big dataFrame
 n_rows = 1000000
 df = pd.dataFrame({
 'A': np.random.randn(n_rows),
 'B': np.random.randn(n_rows),
 'C': np.random.randn(n_rows)
 })

 start = time.time()
 result = df.groupby('A').agg({'B': 'mean', 'C': 'std'})
 end = time.time()

 print(f"Pandas groupby operation: {end - start:.2f} seconds")
 return end - start

def test_sklearn_performance():
"Test performance scikit-learn on M1"
 print("testing scikit-learn performance...")

# Big dateset
 n_samples = 100000
 n_features = 100

 X = np.random.randn(n_samples, n_features)
 y = np.random.randn(n_samples)

 model = RandomForestRegressor(n_estimators=100, n_jobs=-1)

 start = time.time()
 model.fit(X, y)
 end = time.time()

 print(f"RandomForest training: {end - start:.2f} seconds")
 return end - start

def test_pytorch_performance():
"Test performance PyTorch on M1"
 print("testing PyTorch performance...")

 if torch.backends.mps.is_available():
 device = torch.device("mps")
 print("Using MPS (Metal Performance Shaders)")
 else:
 device = torch.device("cpu")
 print("Using CPU")

# Big tensor
 size = 5000
 a = torch.randn(size, size, device=device)
 b = torch.randn(size, size, device=device)

 start = time.time()
 c = torch.mm(a, b)
 end = time.time()

 print(f"PyTorch matrix multiplication: {end - start:.2f} seconds")
 return end - start

if __name__ == "__main__":
 print("=== NeoZorK ML Performance Test ===")
 print("testing on macOS M1 Pro...")
 print()

 numpy_time = test_numpy_performance()
 pandas_time = test_pandas_performance()
 sklearn_time = test_sklearn_performance()
 pytorch_time = test_pytorch_performance()

 print()
 print("=== Performance Summary ===")
 print(f"NumPy: {numpy_time:.2f}s")
 print(f"Pandas: {pandas_time:.2f}s")
 print(f"Scikit-learn: {sklearn_time:.2f}s")
 print(f"PyTorch: {pytorch_time:.2f}s")

 total_time = numpy_time + pandas_time + sklearn_time + pytorch_time
 print(f"Total time: {total_time:.2f}s")
```

♪ Solving the problems

**Theory:** The resolution of problems when setting up an ML environment is critical for the success of the system. M1 Pro has specific requirements and limitations that may cause various problems.

```
Common Problems & Solutions:
┌─────────────────────────────────────────────────────────────┐
│ Troubleshooting Guide │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Problem Categories │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │Compile │ │Package │ │Architect│ │Memory │ │ │
│ │ │Errors │ │Conflicts│ │ure │ │Issues │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Solution Steps │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │Diagnose │ │Research │ │Apply │ │Test │ │ │
│ │ │Problem │ │Solution │ │Fix │ │Solution │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Prevention │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │
│ │ │Document │ │Version │ │Test │ │Monitor │ │ │
│ │ │Process │ │Control │ │Regularly│ │system │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

Problem Resolution Flow:
┌─────────────────────────────────────────────────────────────┐
│ Problem Resolution │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │Problem │───▶│Diagnose │───▶│Research │───▶│Apply │ │
│ │Occurs │ │Issue │ │Solution │ │Fix │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│ │ │ │ │ │
│ ▼ ▼ ▼ ▼ │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Log │ │ check │ │ Search │ │ Test │ │
│ │ Error │ │ Logs │ │ Docs │ │ Fix │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

* Why the problems arise:**
- ** Architectural differences:** M1 Pro uses ARM64 architecture that's different from x86_64
- **Compatibility:**not all libraries initially support Apple Silicon
- **dependencies:** Complex chains of dependencies can cause conflicts
- ** Versions:** Incompatibility of library versions
- ** Environment:** Wrong configration of variable environments

** General principles for solving problems:**
- ** Diagnostics:** Correct identification of the problem
- **Seek for solutions:** Use of official documentation and the community
- **Teching:** check decisions on test tasks
- ** Documentation: ** Recorded decisions for future use
- **Prevention:** Prevention of recurring problems

### Problem 1: Compilation errors

**Theory:** Compilation errors are often due to lack of required development tools. M1Pro requires specific compilation tools for C/C++ code.

** Causes of compilation errors:**
- ** Absence of Xcode Common Line Tools:** required for compilation of C/C++ code
- ** Lack of CMake: ** Required for many libraries to be assembled
- ** No pkg-config:** necessary for library searches
- ** Wrong architecture:** Compilation for x86_64 instead of ARM64
- **Older tools:** Old versions of development tools

** Compilation error symptoms:**
- "command not foundation" errors in the installation of packages
- Lync errors in library assembly
- Warnings about architecture incompatibility
- Code compilation errors C/C++
- Timeouts when the bags are installed

**Decision:**
1. **installation Xcode Common Line Tools:** Main development tools
2. **installation CMake:** Compilation system for C/C++ projects
3. **installation pkg-config:**
4. **check architecture:**confirm in correct architecture
5. **update tools:** latest versions

```bash
# installation Xcode Command Line Tools
xcode-select --install

# installation of additional tools
brew install cmake pkg-config
```

** Critical for ML projects:**
- **Reproduction:** Same tools on all machines
- **Performance:** The right compilation for M1 architecture
- **Stability:** Prevention of assembly errors
- **Compatibility:** compatibility with ML libraries

### Problem 2: Issues with ta-lib

**Theory:** TA-Lib (Technical Analysis Library) is a C-library for Technical Analysis, which requires compilation for M1. Problems often arise from the lack of a system library.

** Causes of problems with ta-lib:**
- ** Lack of a system library:** TA-Lib to be installed on system level
- ** Wrong architecture:** Compilation for x86_64 instead of ARM64
- ** Conflict of versions:** Incompatibility of versions of system and Python libraries
- **Issues with routes:** Wrong ways to libraries
- ** Lack of dependencies:** Missing systems dependencies

**Symptoms with ta-lib:**
- import Errors "No module named 'talib'"
- Lync errors in the Python package installation
- Mistakes "library not foundation" at import
- Warnings about architecture incompatibility
- Timeout on installation

**Decision:**
1. **installation of the System Library:** Through Homebrew for M1
2. **installation Python bending:** Through uv with the right ways
3. **check architecture:**confirm in ARM64 versions
4. **configuring routes:** The right path to libraries
5. **Texting:** sheck workability

```bash
# Installation ta-lib through Homebrew
brew install ta-lib

# installation Python binding
uv add TA-Lib
```

** Critical for financial ML projects:**
- **Technical analysis:** TA-Lib - framework for technical indicators
- **Performance:** Optimized C-realization
- **Definity:** Tested algorithms for technical Analisis
- **Compatibility:** integration with pandas and numpy

### Problem 3: Issues with PyTorch

**Theory:** PyTorch on M1 Pro requires special versions optimized for Apple Silicon. Problems often arise from the use of incorrect versions or sources of installation.

**Cause of problems with PyTorch:**
- ** Wrong Version:** Use of versions for x86_64
- ** Wrong source:** installation with PyPI instead of a special index
- ** Absence of MPS:** Wrong configuring Metal Performance Shaders
- ** Conflict dependencies:** Incompatibility with other libraries
- **Issues with CUDA:** Attempted use of CUDA on M1

** Symptoms of problems with PyTorch:**
- import Errors "No module named 'torch'"
- Mistakes "CUDA not approved" on M1
- Slow Working on CPU instead of GPU
- Linger errors on installation
- Warnings of incompatibility

**Decision:**
1. ** Use the correct index:** Special index for M1
2. **installation MPS version:** Versions with support for Metal Performance Shaders
3. **check compatibility:** Make sure in compatibility versions
4. **configuring MPS:** Correct Conference for use of GPU
5. **Texting:** sheck work on M1

```bash
# Installation of the correct version of PyTorch for M1
uv add torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

** Critical for ML projects:**
- **Performance:** GPU acceleration on M1
- **Compatibility:** Working with existing code
- **Stability:** Prevention of learning failures
- **Scalability:** Opportunity to work with big models

** Further challenges and solutions:**

** Problem 4: Issues with memory**
- ** Cause:** Deficiencies of Unified Memory for large models
- ** Decision:** Memory Optimization, Float16

** Problem 5: Issues with productivity**
- ** Cause:** Wrong configration of variable environments
- ** Decision:** Optimization of settings for M1 Pro

** Problem 6: Issues with relationships**
- ** Cause:** Conflicts between library versions
- ** Decision: ** Use of virtual environments and exact versions

** Critically important for Robst ML systems:**
- ** Diagnostics:** Rapid identification of problems
- ** Resolution: ** Effective methods to solve problems
- **Prevention:** Prevention of recurring problems
- **Documentation:** Recorded decisions for team

# # Full installation check

** Step-by-step introduction for full verification:**

### Step 1: Create test files
```bash
# Create all testy files
cat > test_mlx_complete.py << 'EOF'
# [The content of test_mlx_complete.py in the section above]
EOF

cat > test_core_libraries.py << 'EOF'
# [The content of test_core_libraries.py from the section above]
EOF

cat > test_environment.py << 'EOF'
# [The content of test_environment.py in the section above]
EOF

cat > test_jupyter_config.py << 'EOF'
# [The content of test_jupyter_config.py from the section above]
EOF

cat > test_all_libraries.py << 'EOF'
# [The contents of test_all_libraries.py from the section above]
EOF
```

### Step 2: Run all testes
```bash
# 1. MLX Framework Test
echo "==MLX Framework Test=="
uv run python test_mlx_complete.py

♪ 2. Test of the main libraries
echo "== Test of main libraries=="
uv run python test_core_libraries.py

♪ 3. Test environment
echo "== Environment test==="
uv run python test_environment.py

# 4. Jupyter Test
echo "==Jupyter test=="
uv run python test_jupyter_config.py

# 5. Full test all libraries
echo "=== Full test of all libraries==="
uv run python test_all_libraries.py
```

### Step 3: check results
```bash
# Check created files
ls -la *.png *.html *.ipynb 2>/dev/null

# Check logs
"Check of the last Launch testes..."
```

### Step 4: Additional checks
```bash
# Check versions of key components
echo "=== Check versions==="
uv run python --version
uv --version
brew --version

# Check variable environments
echo "===changed environment==="
env | grep -E "(PYTHON|OMP|MKL|NUMEXPR|MLX)" | sort

# Check available Jupyter core
== sync, corrected by elderman ==
uv run jupyter kernelspec List

# check performance
echo "== Rapid test performance=="
uv run python -c "
import numpy as np
import time
size = 2000
a = np.random.rand(size, size)
b = np.random.rand(size, size)
start = time.time()
c = np.dot(a, b)
end = time.time()
print(f'NumPy {size}x{size}: {end-start:.3f}s')
"
```

## Next steps

After successful environmental development, go to the section:
- **[02_robus_systems_fundamentals.md](02_robus_systems_fundamentals.md)** - Fundamentals of Robastic Systems

# Useful team

```bash
# Check versions
uv run python --version
uv run python -c "import numpy; print(numpy.__version__)"
uv run python -c "import torch; print(torch.__version__)"

# Launch Jupyter
uv run jupyter notebook

# Launch tests
uv run python -m pytest tests/

# Installation of New Dependencies
uv add package_name

# update dependencies
uv sync --upgrade

# Full check system
uv run python test_all_libraries.py
```

♪ Solving the problems

** If tests do not pass:**

1. ** Check Homebrew installation:**
 ```bash
 brew --version
 brew doctor
 ```

2. ** Check the installation uv:**
 ```bash
 uv --version
 uv python List
 ```

** Check the variable environments:**
 ```bash
 source ~/.zshrc
 env | grep -E "(PYTHON|OMP|MKL|NUMEXPR|MLX)"
 ```

4. **Preinstall problem libraries:**
 ```bash
 uv remove package_name
 uv add package_name
 ```

5. ** Clear the cache uv:**
 ```bash
 uv cache clean
 uv sync --reinstall
 ```

---

** It's important:** Make sure that all the performance tests are performed successfully before moving to the next section. All tests must be shown to be successful installation.
