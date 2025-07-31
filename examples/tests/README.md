# Test Files

This directory contains test files and validation scripts for the Streamlit Lightweight Charts Pro library.

## 📁 Contents

### 🧪 Test Files
- **Error Handling Tests**: Comprehensive error scenarios and edge cases
- **Performance Tests**: Large dataset handling and performance validation
- **Compatibility Tests**: Cross-browser and device compatibility
- **Integration Tests**: End-to-end functionality testing

### 🔍 Validation Scripts
- **Data Validation**: Ensuring data format compliance
- **Configuration Validation**: Testing chart option combinations
- **Rendering Validation**: Visual output verification

## 🚀 Running Tests

### Individual Test Files
```bash
# Run specific test file
python comprehensive_error_test.py

# Run performance test
python fit_content_test.py

# Run error handling test
python error_handling_test.py
```

### Using pytest (Recommended)
```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest comprehensive_error_test.py -v
```

## 🎯 Test Categories

### Error Handling Tests
- **Invalid Data**: Testing with malformed or missing data
- **Configuration Errors**: Invalid chart options and parameters
- **Edge Cases**: Boundary conditions and extreme values
- **Exception Handling**: Proper error messages and recovery

### Performance Tests
- **Large Datasets**: Testing with thousands of data points
- **Memory Usage**: Monitoring memory consumption
- **Rendering Speed**: Chart rendering performance
- **Update Performance**: Real-time update efficiency

### Compatibility Tests
- **Browser Compatibility**: Cross-browser functionality
- **Device Testing**: Mobile and tablet compatibility
- **Screen Resolution**: Different display sizes
- **Operating Systems**: Cross-platform compatibility

### Integration Tests
- **End-to-End**: Complete workflow testing
- **Component Integration**: Chart component interactions
- **Data Flow**: Data processing and rendering pipeline
- **User Interactions**: Click, hover, and scroll events

## 📊 Test Coverage

### Chart Types
- ✅ Line Charts
- ✅ Candlestick Charts
- ✅ Bar Charts
- ✅ Area Charts
- ✅ Histogram Charts
- ✅ Baseline Charts

### Features
- ✅ Pane Heights
- ✅ Auto-sizing
- ✅ Real-time Updates
- ✅ Annotations
- ✅ Trade Visualization
- ✅ Custom Styling

### Data Formats
- ✅ Time Series Data
- ✅ OHLC Data
- ✅ Volume Data
- ✅ DataFrame Integration
- ✅ CSV Import/Export

## 🛠️ Writing Tests

### Test Structure
```python
#!/usr/bin/env python3
"""
Test Description

This test validates [specific functionality].
"""

import pytest
from streamlit_lightweight_charts_pro import Chart, ChartOptions

def test_specific_functionality():
    """Test description."""
    # Setup
    chart = Chart(options=ChartOptions())
    
    # Test execution
    result = chart.some_function()
    
    # Assertions
    assert result is not None
    assert result == expected_value
```

### Best Practices
1. **Clear Test Names**: Descriptive test function names
2. **Isolated Tests**: Each test should be independent
3. **Proper Setup/Teardown**: Clean test environment
4. **Meaningful Assertions**: Test specific outcomes
5. **Error Testing**: Include negative test cases

### Test Data
- Use realistic but manageable dataset sizes
- Include edge cases and boundary conditions
- Test with various data formats
- Validate data integrity

## 🔍 Debugging Tests

### Common Issues
1. **Import Errors**: Check PYTHONPATH and dependencies
2. **Rendering Issues**: Verify frontend build is up to date
3. **Data Format Errors**: Validate data structure
4. **Performance Issues**: Monitor resource usage

### Debugging Tools
- **pytest -s**: Show print statements
- **pytest -v**: Verbose output
- **pytest --tb=short**: Short traceback format
- **pytest -x**: Stop on first failure

### Logging
```python
import logging

# Set up logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_with_logging():
    logger.debug("Test starting")
    # Test code
    logger.debug("Test completed")
```

## 📈 Performance Benchmarks

### Baseline Metrics
- **Chart Creation**: < 100ms for basic charts
- **Data Loading**: < 500ms for 1000 data points
- **Rendering**: < 200ms for initial render
- **Updates**: < 50ms for single point updates

### Memory Usage
- **Basic Chart**: < 50MB memory usage
- **Large Dataset**: < 200MB for 10,000 points
- **Multi-pane**: < 100MB per additional pane

## 🚨 Error Scenarios

### Data Errors
- Missing required fields
- Invalid data types
- Out-of-range values
- Malformed timestamps

### Configuration Errors
- Invalid option values
- Conflicting settings
- Missing dependencies
- Unsupported combinations

### Rendering Errors
- Canvas creation failures
- Memory allocation errors
- Browser compatibility issues
- Performance degradation

## 📋 Test Checklist

### Before Running Tests
- [ ] Install all dependencies
- [ ] Update frontend build
- [ ] Clear browser cache
- [ ] Check system resources

### Test Execution
- [ ] Run basic functionality tests
- [ ] Execute error handling tests
- [ ] Perform performance benchmarks
- [ ] Validate visual output

### After Tests
- [ ] Review test results
- [ ] Check for memory leaks
- [ ] Validate error messages
- [ ] Document any issues

## 🎯 Continuous Integration

### Automated Testing
- **GitHub Actions**: Automated test runs on commits
- **Code Coverage**: Track test coverage metrics
- **Performance Monitoring**: Automated performance tests
- **Regression Testing**: Prevent breaking changes

### Test Reports
- **HTML Reports**: Detailed test results
- **Coverage Reports**: Code coverage analysis
- **Performance Reports**: Benchmark comparisons
- **Error Reports**: Detailed error analysis

---

**Maintain high quality through comprehensive testing! 🧪✨** 