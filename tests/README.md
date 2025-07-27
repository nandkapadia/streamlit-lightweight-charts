# Tests Directory

This directory contains all tests for the Streamlit Lightweight Charts Pro library.

## Directory Structure

```
tests/
├── unit/                    # Unit tests organized by functionality
│   ├── data/               # Data classes tests
│   ├── series/             # Series classes tests
│   ├── options/            # Options classes tests
│   ├── frontend/           # Frontend integration tests
│   ├── type_definitions/   # Type definitions tests
│   ├── utils/              # Utils module tests
│   ├── component/          # Component module tests
│   ├── logging/            # Logging module tests
│   └── README.md           # Detailed unit test documentation
├── integration/            # Integration tests
│   └── README.md           # Integration test documentation
├── performance/            # Performance tests
│   └── README.md           # Performance test documentation
├── e2e/                    # End-to-end tests
│   └── README.md           # E2E test documentation
├── conftest.py             # Shared test configuration and fixtures
├── pytest.ini             # Pytest configuration
├── run_tests.py            # Enhanced test runner script
└── README.md               # This file
```

## Test Categories

### Unit Tests (`unit/`)
Comprehensive unit tests for individual components:
- **Data Classes**: BaseData, LineData, AreaData, BarData, CandlestickData, HistogramData, BaselineData, BandData, Marker
- **Series Classes**: LineSeries, AreaSeries, BarSeries, CandlestickSeries, HistogramSeries, BaselineSeries, BandSeries
- **Options Classes**: ChartOptions, LayoutOptions, InteractionOptions, and all other option classes
- **Frontend Integration**: JSON serialization, rendering compatibility
- **Type Definitions**: Color validation, background classes, enums
- **Utils Module**: Data utilities, DataFrame conversion, trade visualization
- **Component Module**: Streamlit component integration, chart rendering
- **Logging Module**: Logging configuration, log output validation

### Integration Tests (`integration/`)
Tests for component interactions:
- Series and data integration
- Options and series integration
- Backend to frontend data flow
- Component interaction workflows
- Cross-module dependencies

### Performance Tests (`performance/`)
Performance and load testing:
- Large dataset handling
- Memory usage optimization
- Rendering performance
- Scalability characteristics
- Resource consumption monitoring

### End-to-End Tests (`e2e/`)
Full application testing:
- Complete chart rendering workflows
- User interaction flows
- Browser compatibility
- Real-world usage scenarios
- Visual regression testing

## Running Tests

### Enhanced Test Runner
```bash
# List all available test categories
python tests/run_tests.py --list

# Run all tests
python tests/run_tests.py

# Run specific test types
python tests/run_tests.py unit              # All unit tests
python tests/run_tests.py integration       # All integration tests
python tests/run_tests.py performance       # All performance tests
python tests/run_tests.py e2e               # All E2E tests

# Run specific unit test categories
python tests/run_tests.py data              # Data tests only
python tests/run_tests.py series            # Series tests only
python tests/run_tests.py options           # Options tests only
python tests/run_tests.py frontend          # Frontend tests only
python tests/run_tests.py type_definitions  # Type definitions tests only
python tests/run_tests.py utils             # Utils tests only
python tests/run_tests.py component         # Component tests only
python tests/run_tests.py logging           # Logging tests only

# Run with options
python tests/run_tests.py data -v           # Verbose output
python tests/run_tests.py series -c         # With coverage
python tests/run_tests.py options -c --html # With HTML coverage report
python tests/run_tests.py unit -p           # Parallel execution
python tests/run_tests.py --file test_file.py # Run specific test file
```

### Traditional pytest Commands
```bash
# All tests
python -m pytest tests/ -v

# Unit tests only
python -m pytest tests/unit/ -v

# Specific categories
python -m pytest tests/unit/data/ -v
python -m pytest tests/unit/series/ -v
python -m pytest tests/unit/options/ -v
python -m pytest tests/unit/frontend/ -v
python -m pytest tests/unit/type_definitions/ -v
python -m pytest tests/unit/utils/ -v
python -m pytest tests/unit/component/ -v
python -m pytest tests/unit/logging/ -v

# Integration tests
python -m pytest tests/integration/ -v

# Performance tests
python -m pytest tests/performance/ -v

# E2E tests
python -m pytest tests/e2e/ -v

# With coverage
python -m pytest tests/ --cov=streamlit_lightweight_charts_pro --cov-report=html
```

### Test Markers
```bash
# Run tests by markers
python -m pytest tests/ -m "unit"           # Unit tests only
python -m pytest tests/ -m "integration"    # Integration tests only
python -m pytest tests/ -m "performance"    # Performance tests only
python -m pytest tests/ -m "e2e"            # E2E tests only
python -m pytest tests/ -m "slow"           # Slow running tests
python -m pytest tests/ -m "fast"           # Fast running tests
```

## Test Statistics

### Current Coverage
- **Unit Tests**: 12+ test files, ~200+ test cases
- **Data Classes**: ✅ Complete coverage
- **Series Classes**: ✅ Complete coverage
- **Options Classes**: ✅ Complete coverage
- **Frontend Integration**: ✅ Complete coverage
- **Type Definitions**: ✅ Complete coverage (100% for colors.py)
- **Utils Module**: 🔄 In development
- **Component Module**: 🔄 In development
- **Logging Module**: 🔄 In development

### Test Results Summary
- **Passing**: ~95% of tests pass
- **Failing**: ~5% (known issues with time normalization and NaN handling)
- **Coverage**: High coverage across all components

## Test Quality Standards

### Code Quality
- **PEP 8 compliant** code style (100 character line limit)
- **Type hints** for all functions and methods
- **Comprehensive docstrings** following Google style
- **Clear naming conventions** for tests and test classes

### Test Quality
- **Descriptive test names** that explain the scenario
- **Proper setup and teardown** for test isolation
- **Edge case coverage** for robustness
- **Error handling tests** for validation
- **Frontend compatibility** validation where applicable
- **Performance thresholds** for performance tests

### Documentation
- **README files** for each test category
- **Clear examples** of how to run tests
- **Coverage reports** for transparency
- **Test patterns** documentation for consistency

## Shared Test Infrastructure

### Common Fixtures (`conftest.py`)
- **Sample data fixtures**: Timestamps, values, OHLC data, DataFrames
- **Series fixtures**: All series types with sample data
- **Options fixtures**: Chart options with various configurations
- **Performance fixtures**: Large datasets and performance thresholds
- **Mock fixtures**: Streamlit, browser, and other external dependencies

### Test Data Factory
```python
# Create test data with specific parameters
data = TestDataFactory.create_line_data(count=100, start_date="2023-01-01")
candlestick_data = TestDataFactory.create_candlestick_data(count=50)
```

### Performance Testing Utilities
```python
# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    'data_creation': 0.1,    # seconds
    'serialization': 0.05,   # seconds
    'validation': 0.01,      # seconds
    'memory_usage': 100,     # MB
    'rendering': 1.0,        # seconds
}
```

## Adding New Tests

### Guidelines
1. **Place in appropriate directory** based on functionality
2. **Follow naming conventions**: `test_<class_name>.py`
3. **Include comprehensive coverage**: construction, validation, serialization, edge cases
4. **Add to appropriate `__init__.py`** if creating new categories
5. **Update README files** if adding new test categories
6. **Use shared fixtures** from `conftest.py` when possible

### Test Patterns
- **Data Class Tests**: Construction, validation, serialization, inheritance
- **Series Class Tests**: Construction, method chaining, DataFrame conversion, frontend compatibility
- **Options Class Tests**: Construction, validation, serialization, default values
- **Frontend Tests**: JSON format validation, rendering compatibility
- **Integration Tests**: Component interactions, data flow, workflows
- **Performance Tests**: Large datasets, memory usage, scalability
- **E2E Tests**: Complete workflows, user interactions, browser compatibility

## Continuous Integration

Tests are automatically run:
- **On every commit** to ensure code quality
- **Before releases** to prevent regressions
- **With coverage reporting** to maintain high coverage
- **On multiple Python versions** for compatibility
- **With performance monitoring** to detect regressions

## Known Issues

### Current Test Failures
- **Time normalization**: Some tests expect different time formats
- **NaN handling**: Implementation converts NaN to 0.0, tests expect NaN preservation
- **Abstract class testing**: Some assumptions about abstract class behavior

### Planned Improvements
- **Integration tests**: Component interaction testing
- **Performance tests**: Large dataset and memory usage testing
- **E2E tests**: Full application workflow testing
- **Test automation**: Automated test generation for new components
- **Visual regression testing**: Screenshot comparison for rendered charts

## Contributing

When contributing to tests:

1. **Follow existing patterns** for consistency
2. **Add tests for new functionality** before merging
3. **Update documentation** when adding new test categories
4. **Ensure all tests pass** before submitting PRs
5. **Maintain high coverage** standards 
6. **Use shared fixtures** from `conftest.py`
7. **Follow performance guidelines** for performance tests 