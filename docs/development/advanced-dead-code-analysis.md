# Advanced Dead Code and Duplicate Code Analysis

## Overview

The Advanced Dead Code Analyzer provides comprehensive and accurate analysis of your codebase using sophisticated AST-based algorithms. Unlike the basic analyzer, this tool uses precise function call tracking and import analysis to minimize false positives.

## 🚀 Key Features

### 1. **Accurate Dead Code Detection**
- **AST-based Analysis**: Uses Python's Abstract Syntax Tree for precise function call detection
- **Function Call Tracking**: Tracks actual function calls, not just text matches
- **Class Instantiation Detection**: Identifies classes that are never instantiated
- **Confidence Scores**: Each result includes a confidence score (0.0-1.0)

### 2. **Advanced Dead Library Analysis**
- **Import Tracking**: Analyzes actual import statements across the entire codebase
- **Package Mapping**: Handles package name to import name mappings (e.g., `scikit-learn` → `sklearn`)
- **Optional Package Detection**: Identifies development/testing dependencies
- **Usage Context**: Distinguishes between production and test usage

### 3. **Duplicate Code Detection**
- **Similarity Analysis**: Uses difflib for accurate code similarity detection
- **Configurable Thresholds**: Adjustable similarity and minimum line thresholds
- **Cross-file Comparison**: Finds duplicates across different files
- **Normalized Comparison**: Ignores whitespace and comments

### 4. **Interactive Menu**
- **User-friendly Interface**: Choose what to analyze interactively
- **Flexible Options**: Configure output format, verbosity, and file locations
- **Guided Workflow**: Step-by-step analysis selection

## 🛠️ Tools

### 1. Advanced Analyzer (`scripts/analysis/dead-code/advanced_dead_code_analyzer.py`)
The core analysis engine with sophisticated algorithms.

**Features:**
- AST-based function call detection
- Import tracking across codebase
- Duplicate code similarity analysis
- Confidence scoring for results
- Detailed reporting with context

### 2. Interactive Runner (`scripts/analysis/dead-code/run_advanced_analysis.sh`)
User-friendly bash script with interactive menu.

**Features:**
- Interactive menu for analysis selection
- Environment detection (Docker vs native)
- Colored output for better readability
- Flexible output options (text/JSON)
- Progress tracking

## 📋 Usage

### Quick Start

```bash
# Interactive menu (recommended)
./scripts/analysis/dead-code/run_advanced_analysis.sh --interactive

# Run all analyses
./scripts/analysis/dead-code/run_advanced_analysis.sh --all

# Analyze specific types
./scripts/analysis/dead-code/run_advanced_analysis.sh --dead-code --verbose
./scripts/analysis/dead-code/run_advanced_analysis.sh --dead-libraries
./scripts/analysis/dead-code/run_advanced_analysis.sh --duplicate-code
```

### Command Line Options

```bash
./scripts/analysis/dead-code/run_advanced_analysis.sh [OPTIONS]

Options:
  --dead-code          Analyze dead code (functions/classes never called)
  --dead-libraries     Analyze dead libraries (unused dependencies)
  --duplicate-code     Analyze duplicate code
  --all                Run all analyses
  --interactive        Use interactive menu
  --output-dir DIR     Save results to directory
  --verbose            Verbose output
  --json               Output in JSON format
  --help               Show this help message
```

### Direct Python Usage

```bash
# Run analyzer directly
uv run python scripts/analysis/dead-code/advanced_dead_code_analyzer.py --interactive

# Specific analyses
uv run python scripts/analysis/dead-code/advanced_dead_code_analyzer.py --dead-code --verbose
uv run python scripts/analysis/dead-code/advanced_dead_code_analyzer.py --all --output-format json
```

## 📊 Understanding Results

### Dead Code Results

```
❌ FUNCTION: unused_function
   File: src/calculation/metrics.py:45
   Severity: high
   Confidence: 0.90
   Reason: Function is never called anywhere in the codebase
   ⚠️  PUBLIC API - Review carefully!
```

**Fields Explained:**
- **Confidence**: How certain the analyzer is (0.0-1.0)
- **Severity**: high/medium/low based on usage and visibility
- **Reason**: Detailed explanation of why it's considered dead
- **Public API**: Warning for public functions that need careful review

### Dead Libraries Results

```
❌ Package: unused-package
   Import: unused_package
   Confidence: 0.95
   Reason: Package is not imported anywhere in the codebase
   Note: Optional package (dev/test)
```

**Fields Explained:**
- **Package**: Name in requirements.txt
- **Import**: Actual import name used in code
- **Confidence**: Certainty level
- **Optional**: Whether it's a development/testing dependency

### Duplicate Code Results

```
🔄 Duplicate: 15 lines
   File 1: src/utils/helper.py:10-25
   File 2: src/calculation/helper.py:5-20
   Similarity: 0.93
   Code: def process_data(data):...
```

**Fields Explained:**
- **Size**: Number of duplicate lines
- **Files**: Locations of duplicate code
- **Similarity**: How similar the code blocks are (0.0-1.0)

## 🔧 Advanced Configuration

### Duplicate Code Detection Settings

```python
# Adjust similarity threshold (default: 0.8)
analyzer.analyze_duplicate_code(min_similarity=0.9, min_lines=10)

# More strict settings
analyzer.analyze_duplicate_code(min_similarity=0.95, min_lines=20)
```

### Package Mappings

The analyzer includes mappings for common packages:

```python
package_to_import = {
    'scikit-learn': 'sklearn',
    'python-dateutil': 'dateutil',
    'beautifulsoup4': 'bs4',
    'pyyaml': 'yaml',
    # ... more mappings
}
```

### Confidence Scoring

**Dead Code Confidence:**
- **0.9-1.0**: High confidence (function never called)
- **0.7-0.9**: Medium confidence (public API, needs review)
- **0.5-0.7**: Low confidence (special cases, test functions)

**Dead Libraries Confidence:**
- **0.95-1.0**: Not imported anywhere
- **0.8-0.95**: Only used in tests/scripts
- **0.5-0.8**: Optional packages

## 📈 Workflow Examples

### 1. Initial Code Review

```bash
# Start with interactive menu
./scripts/analysis/dead-code/run_advanced_analysis.sh --interactive

# Choose: 1. Dead Code Analysis
# Choose: Verbose output: y
# Choose: Save to directory: ./initial_review
# Choose: JSON output: y
```

### 2. Focused Library Cleanup

```bash
# Analyze only dead libraries
./scripts/analysis/dead-code/run_advanced_analysis.sh --dead-libraries --verbose

# Review results and remove unused packages
# Update requirements.txt
# Run tests to ensure nothing breaks
```

### 3. Duplicate Code Refactoring

```bash
# Find duplicate code
./scripts/analysis/dead-code/run_advanced_analysis.sh --duplicate-code --output-dir ./duplicates

# Review high-similarity duplicates first
# Extract common functions
# Update imports
```

### 4. Comprehensive Cleanup

```bash
# Run all analyses
./scripts/analysis/dead-code/run_advanced_analysis.sh --all --verbose --output-dir ./cleanup

# Review results by confidence level
# Start with high-confidence items
# Test after each change
```

## ⚠️ Best Practices

### 1. **Review High-Confidence Items First**
- Items with confidence > 0.9 are most likely truly dead
- Public API functions need careful review even if high confidence

### 2. **Check Test Coverage**
- Run tests after removing any code
- Ensure no functionality is broken
- Use `uv run pytest tests -n auto`

### 3. **Gradual Cleanup**
- Don't remove everything at once
- Start with dead libraries (safest)
- Then unused imports
- Finally, dead functions/classes

### 4. **Context Matters**
- Review the context provided for each item
- Consider if code might be used in the future
- Check for dynamic imports or reflection

## 🔍 Troubleshooting

### False Positives

**Common Causes:**
1. **Dynamic imports**: `importlib.import_module()`
2. **Reflection**: `getattr()`, `eval()`
3. **External usage**: Functions used by other projects
4. **Configuration**: Functions called via config files

**Solutions:**
- Review the context provided
- Check for dynamic usage patterns
- Add comments to suppress warnings if needed

### Missing Imports

**If the analyzer misses imports:**
1. Check package name mappings
2. Verify import statements are valid
3. Look for conditional imports

### Performance Issues

**For large codebases:**
- Use specific analysis types instead of `--all`
- Increase verbosity to see progress
- Consider running in smaller chunks

## 🚀 Integration

### CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Run dead code analysis
  run: |
    ./scripts/analysis/dead-code/run_advanced_analysis.sh --all --output-dir ./analysis
    # Fail if too many issues found
    if [ $(grep -c "high" analysis/advanced_analysis.json) -gt 10 ]; then
      echo "Too many high-severity issues found"
      exit 1
    fi

- name: Upload analysis results
  uses: actions/upload-artifact@v2
  with:
    name: dead-code-analysis
    path: ./analysis/
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: dead-code-check
        name: Dead Code Analysis
        entry: ./scripts/analysis/dead-code/run_advanced_analysis.sh
        args: [--dead-code, --output-dir, ./pre-commit-analysis]
        language: system
        pass_filenames: false
```

## 📚 Comparison with Basic Analyzer

| Feature | Basic Analyzer | Advanced Analyzer |
|---------|----------------|-------------------|
| **Detection Method** | Text search | AST-based analysis |
| **Accuracy** | Medium (false positives) | High (minimal false positives) |
| **Confidence Scoring** | No | Yes (0.0-1.0) |
| **Duplicate Detection** | No | Yes |
| **Interactive Menu** | No | Yes |
| **Performance** | Fast | Slower but more accurate |
| **Context Information** | Basic | Detailed with reasons |

## 🎯 When to Use Each

**Use Basic Analyzer when:**
- Quick initial scan needed
- Performance is critical
- Simple text-based analysis is sufficient

**Use Advanced Analyzer when:**
- Accurate results are important
- False positives are problematic
- Detailed analysis is needed
- Duplicate code detection is required
- Interactive workflow is preferred

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the verbose output for details
3. Examine the JSON output for programmatic analysis
4. Consult the project documentation

The Advanced Dead Code Analyzer provides the most accurate and comprehensive analysis available, making it the recommended tool for serious code cleanup efforts.
