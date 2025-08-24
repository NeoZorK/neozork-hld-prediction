# ML Documentation Usage Instructions

## Quick Navigation

### 🚀 Start Here
1. **Main Index**: [docs/ml/index.md](index.md) - Complete ML documentation hub
2. **Module Overview**: [docs/ml/ml-module-overview.md](ml-module-overview.md) - Architecture and roadmap
3. **Feature Engineering**: [docs/ml/feature_engineering_guide.md](feature_engineering_guide.md) - Usage guide

### 🔧 Source Code Reference
- **Brief Overview**: [src/ml/README.md](../../src/ml/README.md) - Quick reference with links

## Navigation Paths

### From Main Documentation
```
docs/index.md → Machine Learning section → ML Documentation
```

### From Guides
```
docs/guides/index.md → Machine Learning Guide
```

### From Root README
```
README.md → Development Tools → Machine Learning Platform
```

## File Descriptions

### 📚 Documentation Files
- **`index.md`** - Main ML documentation index with all sections
- **`ml-module-overview.md`** - Complete ML module architecture and roadmap
- **`feature_engineering_guide.md`** - Feature engineering system usage guide
- **`CHANGES_SUMMARY.md`** - User-friendly summary of recent changes
- **`README_MOVED_SUMMARY.md`** - Technical details of documentation move

### 🔧 Source Files
- **`src/ml/README.md`** - Brief overview with links to full documentation

## Quick Commands

### View Documentation
```bash
# View main ML index
cat docs/ml/index.md

# View module overview
cat docs/ml/ml-module-overview.md

# View feature engineering guide
cat docs/ml/feature_engineering_guide.md
```

### Run ML Features
```bash
# Run feature engineering demo
uv run python scripts/demo_feature_engineering.py

# Run ML tests
uv run pytest tests/ml/ -n auto
```

## Common Use Cases

### For New Users
1. Start with [ml-module-overview.md](ml-module-overview.md) for understanding
2. Read [feature_engineering_guide.md](feature_engineering_guide.md) for usage
3. Use [index.md](index.md) for navigation

### For Developers
1. Check [src/ml/README.md](../../src/ml/README.md) for quick reference
2. Use [docs/ml/](.) for complete documentation
3. Follow links for specific topics

### For Contributors
1. Review [README_MOVED_SUMMARY.md](README_MOVED_SUMMARY.md) for technical details
2. Check [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) for recent updates
3. Use [index.md](index.md) for documentation structure

## Support

### Getting Help
- **Documentation**: Check the guides and examples
- **Tests**: Run tests to verify functionality
- **Demo**: Use the demo script as reference
- **Issues**: Report bugs and feature requests

### Common Issues
1. **Import Errors** - Ensure all dependencies installed
2. **Memory Issues** - Reduce feature count or enable parallel processing
3. **Slow Performance** - Check data size and configuration
4. **Missing Features** - Verify data has required OHLCV columns

---

**Status**: ✅ Complete | **Last Updated**: December 2024
