# Unit Tests Organization

This directory contains unit tests for the Streamlit Lightweight Charts Pro library, organized by functionality.

## Directory Structure

```
tests/unit/
├── data/                    # Data classes tests
│   ├── __init__.py
│   ├── test_base_data.py           # BaseData abstract class tests
│   ├── test_line_data.py           # LineData concrete class tests
│   └── test_marker.py              # Marker data class tests
├── series/                  # Series classes tests
│   ├── __init__.py
│   ├── test_series_base.py         # Series abstract base class tests
│   ├── test_line_series.py         # LineSeries basic functionality tests
│   ├── test_line_series_extended.py # LineSeries extended functionality tests
│   └── test_line_series_json_format.py # Frontend JSON compatibility tests
├── options/                 # Options classes tests
│   ├── __init__.py
│   ├── test_line_options.py        # LineOptions styling tests
│   ├── test_price_format_options.py # PriceFormatOptions tests
│   └── test_price_line_options.py  # PriceLineOptions tests
└── frontend/                # Frontend integration tests
    ├── __init__.py
    └── test_frontend_price_lines.py # Frontend price lines integration tests
```

## Test Categories

### Data Tests (`data/`)
Tests for data classes that represent chart data points:
- **BaseData**: Abstract base class for all data points
- **LineData**: Concrete implementation for line series data
- **Marker**: Data class for series markers

### Series Tests (`series/`)
Tests for series classes that represent chart series:
- **Series**: Abstract base class for all series
- **LineSeries**: Concrete implementation for line series
- **JSON Format**: Tests ensuring frontend compatibility

### Options Tests (`options/`)
Tests for configuration and styling options:
- **LineOptions**: Line series styling options
- **PriceFormatOptions**: Price formatting configuration
- **PriceLineOptions**: Price line styling options

### Frontend Tests (`frontend/`)
Tests for frontend integration and rendering:
- **Price Lines**: Frontend price line integration
- **JSON Serialization**: Frontend data format compatibility

## Running Tests

### Run all unit tests:
```bash
python -m pytest tests/unit/ -v
```

### Run tests by category:
```bash
# Data tests only
python -m pytest tests/unit/data/ -v

# Series tests only
python -m pytest tests/unit/series/ -v

# Options tests only
python -m pytest tests/unit/options/ -v

# Frontend tests only
python -m pytest tests/unit/frontend/ -v
```

### Run specific test files:
```bash
# Line series tests
python -m pytest tests/unit/series/test_line_series.py -v

# JSON format tests
python -m pytest tests/unit/series/test_line_series_json_format.py -v
```

## Test Coverage

### Current Coverage Status:
- **Data Classes**: ✅ Complete coverage
- **Series Classes**: ✅ Complete coverage
- **Options Classes**: ✅ Complete coverage
- **Frontend Integration**: ✅ Complete coverage

### Test Statistics:
- **Total Test Files**: 12
- **Total Test Cases**: ~69 tests
- **Coverage**: High coverage across all components

## Test Patterns

### Data Class Tests:
- Construction with valid/invalid data
- Serialization (`to_dict()`)
- Validation and error handling
- Inheritance and class properties

### Series Class Tests:
- Construction with different data types
- Method chaining functionality
- DataFrame conversion
- Price lines and markers integration
- Frontend JSON compatibility

### Options Class Tests:
- Construction and validation
- Serialization to camelCase
- Enum value handling
- Default value behavior

### Frontend Integration Tests:
- JSON format validation
- Frontend rendering compatibility
- Data serialization accuracy

## Adding New Tests

When adding new tests:

1. **Place in appropriate directory** based on functionality
2. **Follow naming convention**: `test_<class_name>.py`
3. **Include comprehensive coverage**: construction, validation, serialization, edge cases
4. **Add to appropriate `__init__.py`** if creating new categories
5. **Update this README** if adding new test categories

## Test Quality Standards

- **PEP 8 compliant** code style
- **Comprehensive docstrings** for all test methods
- **Clear test names** that describe the scenario being tested
- **Proper error handling** tests
- **Edge case coverage** for robustness
- **Frontend compatibility** validation where applicable 