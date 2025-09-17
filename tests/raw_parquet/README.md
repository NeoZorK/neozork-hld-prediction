# Raw Parquet Tests

This directory contains comprehensive unit tests for the raw parquet data management functionality in the NeoZork Interactive ML Trading Strategy Development system.

## Test Files

- `test_raw_parquet_analyzer.py` - Tests for RawParquetAnalyzer class (16 tests)
- `test_raw_parquet_loader.py` - Tests for RawParquetLoader class (16 tests)  
- `test_raw_parquet_processor.py` - Tests for RawParquetProcessor class (16 tests)
- `test_raw_parquet_mtf_creator.py` - Tests for RawParquetMTFCreator class (21 tests)

## Running Tests

### Run all raw parquet tests:
```bash
uv run pytest tests/raw_parquet/ -v
```

### Run specific test file:
```bash
uv run pytest tests/raw_parquet/test_raw_parquet_analyzer.py -v
```

### Run specific test method:
```bash
uv run pytest tests/raw_parquet/test_raw_parquet_analyzer.py::TestRawParquetAnalyzer::test_init -v
```

## Test Coverage

The tests provide comprehensive coverage of:
- File analysis and metadata extraction
- Data loading with various filters
- Data processing and standardization
- MTF structure creation
- Error handling and edge cases
- Progress tracking functionality

## Test Structure

Each test file follows the same structure:
- Setup and teardown methods for test isolation
- Tests for initialization and basic functionality
- Tests for core business logic
- Tests for error handling
- Tests for edge cases and boundary conditions

## Dependencies

Tests use the following testing libraries:
- `pytest` - Main testing framework
- `pandas` - Data manipulation for test data
- `numpy` - Numerical operations for test data
- `unittest.mock` - Mocking for isolated testing
- `tempfile` - Temporary file creation for tests
