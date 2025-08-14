# Dead Code Analysis - Quick Start

Quick guide to get started with dead code and dead libraries analysis.

## 🚀 Quick Commands

### Basic Analysis
```bash
# Run all analyses (recommended)
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all

# With uv (native environment)
uv run python scripts/analysis/dead-code/dead_code_analyzer.py --all
```

### Save Results
```bash
# Save results to directory
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --output-dir ./results
```

### Apply Fixes
```bash
# Dry run first (see what would be fixed)
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix --dry-run

# Apply fixes
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix
```

## 📋 Common Workflows

### 1. Quick Check
```bash
# Just check for dead libraries (safest)
./scripts/analysis/dead-code/run_dead_code_analysis.sh --dead-libraries
```

### 2. Full Cleanup
```bash
# 1. Analyze and save results
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --output-dir ./cleanup

# 2. Review results
cat cleanup/analysis_summary.txt

# 3. Apply fixes
./scripts/analysis/dead-code/run_dead_code_analysis.sh --all --fix

# 4. Test everything works
uv run pytest tests -n auto
```

### 3. Safe Gradual Cleanup
```bash
# Step 1: Remove unused libraries
./scripts/analysis/dead-code/run_dead_code_analysis.sh --dead-libraries --fix

# Step 2: Remove unused imports
./scripts/analysis/dead-code/run_dead_code_analysis.sh --dead-code --fix

# Step 3: Remove dead files (most risky)
./scripts/analysis/dead-code/run_dead_code_analysis.sh --dead-files --fix
```

## 🔧 Key Tools

| Tool | Purpose | Command |
|------|---------|---------|
| **Analyzer** | Find dead code/libraries | `python scripts/analysis/dead-code/dead_code_analyzer.py --all` |
| **Fixer** | Apply fixes | `python scripts/analysis/dead-code/fix_dead_code.py --analysis-file results.json` |
| **Runner** | Combined tool | `./scripts/analysis/dead-code/run_dead_code_analysis.sh --all` |

## ⚠️ Safety Tips

1. **Always use `--dry-run` first**
2. **Backups are automatic** - check `backups/` directory
3. **Run tests after fixes** - `uv run pytest tests -n auto`
4. **Review results** before applying fixes

## 🆘 If Something Goes Wrong

```bash
# Find latest backup
ls -la backups/

# Restore specific file
cp backups/dead_code_fix_*/src/calculation/old_file.py src/calculation/

# Restore everything
cp -r backups/dead_code_fix_*/src/ ./
```

## 📊 Understanding Output

### Dead Code
```
❌ FUNCTION: unused_function
   File: src/calculation/metrics.py:45
   Severity: high
```

### Dead Libraries
```
❌ Package: matplotlib-inline
   Import: matplotlib_inline
   Usage count: 0
```

### Dead Files
```
❌ File: src/old_analysis.py
   Size: 2048 bytes
   Reason: Not imported anywhere
```

## 🎯 Next Steps

1. Read the [full documentation](dead-code-analysis.md)
2. Integrate into your CI/CD pipeline
3. Set up regular analysis in your workflow
4. Use with other code quality tools

## 📞 Need Help?

- Check the [full documentation](dead-code-analysis.md)
- Review backup files if something went wrong
- Run tests to ensure functionality is preserved
- Consult the project documentation for specific patterns
