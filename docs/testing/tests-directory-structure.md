# Tests Directory Structure

This document provides a comprehensive overview of the test directory structure for the NeoZork HLD Prediction project.

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container testing. Current version: v0.5.3

## 📁 Directory Structure

### 🐳 Docker Tests (`docker/`)
> **Note**: Docker tests are available but Docker support is limited to v0.5.2 and earlier versions.

- **test_docker_complete_workflow.py** - Complete workflow testing for Docker environment
- **test_docker_fix_verification.py** - Verification of Docker fixes
- **test_docker_interactive_input.py** - Interactive input testing in Docker
- **test_docker_fix_issue.py** - Docker issue diagnosis and testing
- **fix_docker_input_issue.py** - Docker input handling fixes
- **test_uv_docker.py** - UV package manager in Docker
- **test_uv_only_mode.py** - UV-only mode testing
- **test_uv_simple.py** - Simple UV tests
- **test_container.py** - Container functionality testing
- **test_container_mql5_feed_paths.py** - MQL5 feed path testing
- **test_docker_base.py** - Base Docker functionality
- **test_docker_config.py** - Docker configuration testing
- **test_docker_tests.py** - Docker test framework
- **test_dockerfile.py** - Dockerfile validation
- **test_ide_configs.py** - IDE configuration testing
- **test_interactive_mode.py** - Interactive mode in Docker
- **test_mql5_feed_access.py** - MQL5 feed access testing
- **test_uv_commands.py** - UV command testing

### 🎮 Interactive Tests (`interactive/`)
- **test_interactive_automated.py** - Automated interactive system testing
- **test_gap_verification_fix.py** - Gap verification and fixing
- **test_gap_fixing_with_nan.py** - Gap fixing with NaN handling
- **test_gap_fixing_issue.py** - Gap fixing issue resolution
- **test_docker_eof_fix.py** - Docker EOF handling fixes
- **test_data_fixing_error_handling.py** - Data fixing error handling
- **test_data_manager_memory_fix.py** - Data manager memory fixes
- **test_analysis_runner_fixes.py** - Analysis runner fixes
- **test_data_manager_fixes.py** - Data manager fixes
- **test_data_manager_memory_optimization.py** - Memory optimization
- **test_data_manager_memory.py** - Memory management testing
- **test_core.py** - Core interactive system testing
- **test_core_fast.py** - Fast core testing
- **test_visualization_manager.py** - Visualization manager testing
- **test_menu_manager.py** - Menu manager testing
- **test_restore_backup.py** - Backup restoration testing
- **test_menu_improvements.py** - Menu improvements
- **test_interactive_system_fixes.py** - Interactive system fixes
- **test_menu_exit_commands.py** - Menu exit command testing
- **test_data_manager.py** - Data manager testing
- **test_feature_engineering_manager.py** - Feature engineering testing
- **test_comprehensive_data_quality_check.py** - Comprehensive data quality testing
- **test_analysis_runner.py** - Analysis runner testing

### 🔧 Common Tests (`common/`)
- **test_environment_check.py** - Environment checking utilities
- **test_logger.py** - Logging functionality testing

### 🛠️ Utility Tests (`utils/`)
- **backup_functions.py** - Backup functionality utilities
- **test_backup_fix.py** - Backup fixing testing
- **test_point_size_determination.py** - Point size determination
- **test_utils.py** - General utility testing

### 📊 Calculation Tests (`calculation/`)
- Technical indicator calculation testing
- Mathematical function validation
- Performance optimization testing

### 🎯 CLI Tests (`cli/`)
- Command-line interface testing
- Argument parsing validation
- User interaction testing

### 📈 Data Tests (`data/`)
- Data loading and validation
- Data format testing
- Data source integration testing

### 🔍 EDA Tests (`eda/`)
- Exploratory data analysis testing
- Data quality assessment
- Statistical analysis validation

### 📤 Export Tests (`export/`)
- Data export functionality
- Format conversion testing
- Output validation

### 🔗 Integration Tests (`integration/`)
- End-to-end workflow testing
- Component integration testing
- System-wide functionality validation

### 🤖 ML Tests (`ml/`)
- Machine learning model testing
- Feature engineering validation
- Prediction accuracy testing

### 🖥️ MCP Tests (`mcp/`)
- Model Context Protocol testing
- Server communication validation
- IDE integration testing

### 🐳 Native Container Tests (`native-container/`)
- Apple Silicon container testing
- Native performance validation
- Container optimization testing

### 📊 Plotting Tests (`plotting/`)
- Visualization functionality testing
- Chart generation validation
- Plot customization testing

### 📝 Script Tests (`scripts/`)
- Utility script testing
- Automation validation
- Script integration testing

### 📁 Source Tests (`src/`)
- Source code functionality testing
- Module integration validation
- Core feature testing

### 📋 Summary Tests (`summary/`)
- Test result summarization
- Coverage reporting
- Performance metrics

### 🔄 Workflow Tests (`workflow/`)
- Workflow automation testing
- Process validation
- Pipeline testing

## 🚀 Running Tests

### Run All Tests
```bash
uv run pytest tests -n auto
```

### Run Specific Test Categories
```bash
# Docker tests
uv run pytest tests/docker/ -n auto

# Interactive tests
uv run pytest tests/interactive/ -n auto

# ML tests
uv run pytest tests/ml/ -n auto

# All calculation tests
uv run pytest tests/calculation/ -n auto
```

### Run with Coverage
```bash
uv run pytest tests/ --cov=src -n auto
```

### Run Fast Tests Only
```bash
uv run pytest tests/ -m "not slow" -n auto
```

## 📋 Test Categories

### 🔴 Critical Tests
- Core functionality validation
- Data integrity checks
- Security validation

### 🟡 Important Tests
- Feature functionality
- Integration testing
- Performance validation

### 🟢 Nice-to-Have Tests
- Edge case handling
- Documentation examples
- User experience testing

## 🧪 Test Development

### Adding New Tests
1. Create test file in appropriate subdirectory
2. Follow naming convention: `test_*.py`
3. Use descriptive test names
4. Include proper assertions and error handling
5. Add to appropriate test category

### Test Standards
- Use pytest framework
- Follow AAA pattern (Arrange, Act, Assert)
- Include proper error handling
- Use descriptive test names
- Maintain test isolation

### Test Documentation
- Document complex test scenarios
- Explain test purpose and expected behavior
- Include setup and teardown instructions
- Document test dependencies

---

**Last Updated**: 2025-01-27  
**Total Test Files**: 100+  
**Test Coverage**: Comprehensive  
**Framework**: pytest with UV
