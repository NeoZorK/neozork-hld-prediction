# Dead Code and Dead Libraries Analysis

This document describes how to use the dead code and dead libraries analysis tools in the project.

## Overview

The project includes comprehensive tools for finding and fixing:
- **Dead Code**: Unused functions, classes, and variables
- **Dead Libraries**: Unused dependencies in requirements.txt
- **Dead Files**: Python files that are not imported anywhere
- **Unused Imports**: Import statements that are not used

## Tools

### 1. Dead Code Analyzer (`scripts/analysis/dead-code/dead_code_analyzer.py`)

The main analysis tool that scans the entire codebase for dead code and libraries.

#### Usage

```bash
# Run all analyses
python scripts/analysis/dead_code_analyzer.py --all

# Run specific analyses
python scripts/analysis/dead_code_analyzer.py --dead-code --dead-libraries

# Verbose output
python scripts/analysis/dead_code_analyzer.py --all --verbose

# Save results to JSON file
python scripts/analysis/dead_code_analyzer.py --all --output-format json --output-file results.json

# With uv (recommended)
uv run python scripts/analysis/dead_code_analyzer.py --all
```

#### Options

- `--dead-code`: Analyze dead code (functions, classes, variables)
- `--dead-libraries`: Analyze dead libraries (unused dependencies)
- `--dead-files`: Analyze dead files (unused modules)
- `--all`: Run all analyses (default)
- `--verbose`: Verbose output with context
- `--output-format`: Output format (text, json, html)
- `--output-file`: Save results to file

### 2. Dead Code Fixer (`scripts/analysis/dead-code/fix_dead_code.py`)

Automatically fixes issues found by the analyzer.

#### Usage

```bash
# Apply fixes using analysis results
python scripts/analysis/fix_dead_code.py --analysis-file results.json

# Dry run (show what would be fixed)
python scripts/analysis/fix_dead_code.py --analysis-file results.json --dry-run

# Apply all fixes
python scripts/analysis/fix_dead_code.py --analysis-file results.json --all

# With uv
uv run python scripts/analysis/fix_dead_code.py --analysis-file results.json
```

#### Options

- `--analysis-file`: Use results from dead_code_analyzer.py
- `--fix-imports`: Remove unused imports
- `--fix-functions`: Remove dead functions
- `--fix-requirements`: Update requirements.txt
- `--fix-files`: Delete dead files
- `--all`: Apply all fixes
- `--dry-run`: Show what would be fixed without applying
- `--backup-dir`: Specify backup directory

### 3. Analysis Runner (`scripts/analysis/dead-code/run_dead_code_analysis.sh`)

Convenient bash script that combines analysis and fixing.

#### Usage

```bash
# Run all analyses
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all

# Run specific analyses
./scripts/analysis/dead-code/run_dead_code_analysis.sh --dead-libraries --dead-files

# Save results to directory
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --output-dir ./results

# Apply fixes after analysis
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix

# Dry run with fixes
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix --dry-run

# Verbose output
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --verbose
```

#### Options

- `--dead-code`: Analyze dead code
- `--dead-libraries`: Analyze dead libraries
- `--dead-files`: Analyze dead files
- `--all`: Run all analyses
- `--output-dir`: Save results to directory
- `--verbose`: Verbose output
- `--fix`: Apply fixes after analysis
- `--dry-run`: Show what would be fixed without applying

## Workflow Examples

### Basic Analysis

```bash
# 1. Run comprehensive analysis
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --output-dir ./analysis_results

# 2. Review results
cat analysis_results/analysis_summary.txt

# 3. Apply fixes (optional)
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix --dry-run
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix
```

### Focused Analysis

```bash
# Analyze only dead libraries
./scripts/analysis/dead-code/run_dead_code_analysis.sh --dead-libraries --verbose

# Analyze only dead code in source files
./scripts/analysis/dead-code/run_dead_code_analysis.sh --dead-code --output-dir ./dead_code_results
```

### Safe Cleanup

```bash
# 1. Run analysis and save results
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --output-dir ./cleanup_results

# 2. Review what would be fixed
./scripts/analysis/dead-code/fix_dead_code.py --analysis-file cleanup_results/dead_code_analysis.json --dry-run

# 3. Apply fixes
./scripts/analysis/dead-code/fix_dead_code.py --analysis-file cleanup_results/dead_code_analysis.json

# 4. Run tests to ensure nothing broke
uv run pytest tests -n auto
```

## Understanding Results

### Dead Code Analysis

The analyzer identifies:
- **Unused Functions**: Functions that are defined but never called
- **Unused Classes**: Classes that are defined but never instantiated
- **Unused Variables**: Variables that are assigned but never used

Example output:
```
🔍 DEAD CODE ANALYSIS (3 items found)
----------------------------------------
❌ FUNCTION: calculate_old_metric
   File: src/calculation/old_metrics.py:45
   Severity: high

❌ CLASS: LegacyIndicator
   File: src/calculation/legacy.py:12
   Severity: medium
```

### Dead Libraries Analysis

The analyzer identifies:
- **Unused Dependencies**: Packages in requirements.txt that are not imported
- **Test-Only Dependencies**: Packages only used in test files
- **Optional Dependencies**: Development/testing packages

Example output:
```
📦 DEAD LIBRARIES ANALYSIS (2 items found)
----------------------------------------
❌ Package: matplotlib-inline
   Import: matplotlib_inline
   Usage count: 0
   Note: Optional package (dev/test)

❌ Package: old-trading-lib
   Import: old_trading_lib
   Usage count: 1
   Used in: tests/test_legacy.py
```

### Dead Files Analysis

The analyzer identifies:
- **Unused Modules**: Python files that are not imported anywhere
- **Orphaned Files**: Files that may have been left behind after refactoring

Example output:
```
📁 DEAD FILES ANALYSIS (1 items found)
----------------------------------------
❌ File: src/old_analysis.py
   Size: 2048 bytes
   Last modified: 2024-01-15T10:30:00
   Reason: Not imported anywhere
```

## Safety Features

### Automatic Backups

The fixer automatically creates backups before making changes:
- All modified files are backed up to `backups/dead_code_fix_TIMESTAMP/`
- Original file structure is preserved
- Timestamp ensures no conflicts

### Dry Run Mode

Always use `--dry-run` first to see what would be changed:
```bash
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix --dry-run
```

### Selective Fixing

You can apply only specific types of fixes:
```bash
# Only remove unused imports
python scripts/analysis/dead-code/fix_dead_code.py --analysis-file results.json --fix-imports

# Only update requirements.txt
python scripts/analysis/dead-code/fix_dead_code.py --analysis-file results.json --fix-requirements
```

## Best Practices

### 1. Regular Analysis

Run dead code analysis regularly as part of your development workflow:
```bash
# Add to your pre-commit hooks or CI pipeline
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --output-dir ./analysis
```

### 2. Review Before Fixing

Always review the analysis results before applying fixes:
```bash
# 1. Run analysis
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --output-dir ./review

# 2. Review results
cat review/analysis_summary.txt

# 3. Check specific items
grep "high" review/dead_code_analysis.json
```

### 3. Test After Fixing

Always run tests after applying fixes:
```bash
# Apply fixes
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix

# Run tests
uv run pytest tests -n auto

# If tests fail, restore from backup
cp -r backups/dead_code_fix_*/src/ ./
```

### 4. Gradual Cleanup

For large codebases, clean up gradually:
```bash
# Start with dead libraries (safest)
./scripts/analysis/dead-code/run_dead_code_analysis.sh --dead-libraries --fix

# Then unused imports
./scripts/analysis/dead-code/run_dead_code_analysis.sh --dead-code --fix

# Finally, dead files (most risky)
./scripts/analysis/dead-code/run_dead_code_analysis.sh --dead-files --fix
```

## Troubleshooting

### Common Issues

1. **False Positives**: Some functions may be used dynamically or through reflection
2. **Test Dependencies**: Libraries only used in tests may be flagged as dead
3. **Plugin Systems**: Functions used as plugins may not be detected

### Manual Review

For complex cases, manually review flagged items:
```bash
# Get detailed context
python scripts/analysis/dead-code/dead_code_analyzer.py --all --verbose

# Search for specific usage patterns
grep -r "function_name" src/
```

### Restoring from Backup

If something goes wrong, restore from backup:
```bash
# Find latest backup
ls -la backups/

# Restore specific files
cp backups/dead_code_fix_20240115_143022/src/calculation/old_metrics.py src/calculation/

# Restore entire directory
cp -r backups/dead_code_fix_20240115_143022/src/ ./
```

## Integration with CI/CD

Add dead code analysis to your CI pipeline:

```yaml
# .github/workflows/dead-code-analysis.yml
name: Dead Code Analysis

on: [push, pull_request]

jobs:
  dead-code-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install uv
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH
      
      - name: Install dependencies
        run: uv sync
      
      - name: Run dead code analysis
        run: |
          ./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --output-dir ./analysis_results
      
      - name: Upload analysis results
        uses: actions/upload-artifact@v3
        with:
          name: dead-code-analysis
          path: analysis_results/
      
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const summary = fs.readFileSync('./analysis_results/analysis_summary.txt', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Dead Code Analysis Results\n\n\`\`\`\n${summary}\n\`\`\``
            });
```

## Related Tools

- **Requirements Analyzer**: `scripts/analysis/analyze_requirements.py` - Legacy tool for analyzing dependencies
- **Test Coverage**: `scripts/analysis/generate_test_coverage.py` - Ensure removed code doesn't break tests
- **Code Quality**: Use with linting tools like flake8, pylint, or ruff

## Support

For issues or questions about dead code analysis:
1. Check the analysis results for false positives
2. Review the backup files if something went wrong
3. Run tests to ensure functionality is preserved
4. Consult the project documentation for specific patterns
