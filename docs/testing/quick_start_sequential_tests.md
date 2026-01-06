# Quick start: Sequential Test Runner

♪ What's that?

A consistent test runner is the solution for Launch testes in Docker to a folder-by- folder container, which prevents vorkers and Issues from failing with resources in parallel execution.

## Quick start

###1.Launch in Docker container

```bash
# At Launch, select 'y' for Launch testes
docker run -it your-container
# Answer 'y' on the question about Launche testes
```

###2. # Launch's hand

```bash
# Run all testes sequence
python scripts/run_sequential_tests_docker.py

# Testing the function of the ranner
python scripts/test_sequential_runner.py
```

♪## 3. Use in interactive shell

```bash
# in Docker container available team:
python scripts/run_sequential_tests_docker.py
uv run pytest tests -n auto # Old way (may cause problems)
```

## The order of the tests

The tests shall be performed in the following order:

1. **con** - Basic Utilities (7 testes, ~2s)
2. **unit**-Unit tests (335 tests, ~7s)
3. **utils** - Utilities (30 tests, ~2s)
4. **data** - Data processing
5. **calculation** - Mathematical Calculations
6. **click** - Command line
7. **plotting** - Schedules
8. **export** - Data export
9. **eda** - Data analysis
10. **interactive** - Interactive
11. **integration** - Integration tests
12. **ml** - Machine training
13. **mcp** - MCP server
14. **Docker** - Docker tests
15. **native-container** - Intact containers
16. **pocket_hedge_fund** - application
17. **saas** - SaaS application
18. **scripts** - Scripts
19. **workflow** - Business processes
20. **e2e** - End-to-end tests

## configuration

Settings are in the `tests/test_execution_order.yaml' file:

```yaml
test_folders:
 - name: "common"
 describe: "Basic utilities"
 timeout: 30
 required: true

global_Settings:
max_total_time: 3600 #1 hour
 stop_on_failure: true
 skip_empty_folders: true
```

♪ Benefits

*Stability**: No malfunctioning of vorkers
* Predictability**: Ongoing implementation
*Manage of resources**: Memory control and CPU
Easy debugging**: I see which folder caused the problem.
*Flexibility**: Adjustable timeout and parameters

# # Example output

```
============================================================
Running folder 1/20: common
describe: Basic utilities and common functions
Timeout: 30s
============================================================
2024-01-15 10:30:01 - INFO - Running tests in folder: common (1 files)
2024-01-15 10:30:05 - INFO - ✅ Folder common COMPLETED successfully in 4.23s
2024-01-15 10:30:05 - INFO - Passed: 7, Failed: 0, Skipped: 0

============================================================
Running folder 2/20: unit
describe: Unit tests for individual components
Timeout: 60s
============================================================
2024-01-15 10:30:06 - INFO - Running tests in folder: unit (20 files)
2024-01-15 10:30:15 - INFO - ✅ Folder unit COMPLETED successfully in 9.12s
2024-01-15 10:30:15 - INFO - Passed: 335, Failed: 0, Skipped: 53
```

## Resolution of problems

### tests do not start
- Check that you're in the Docker container.
- Make sure the file `tests/test_execution_order.yaml' exists

### Timeout folders
- Increase `timeout' in configuration for slow folders
- Check on the presentation of endless cycles in tests

### configuration errors
- Run `python scripts/test_sequential_runner.py' for diagnostics
- Check the YAML file syntax

## integration with CI/CD

```bash
# in CI/CD pipline
docker run --rm your-container python scripts/run_sequential_tests_docker.py
```

## Comparrison with parallel performance

( &lt;-n auto &gt; ) Consequent
|---------------------------|------------------|
♪ Vorcier malfunctions ♪ ♪ Stable Working ♪
* Unpredictable order * * Controlled order *
♪ Issues with resources ♪ ♪ Management resources ♪
♪ Faster ♪ ♪ Slower but more reliable ♪

## Conclusion

A consistent test-runner is a reliable solution for Docker environments that ensures that testes are consistently performed without malfunctioning the vorkers and with the resources.
