# Utils Module Tests

This directory contains unit tests for the `utils` module of Streamlit Lightweight Charts Pro.

## Purpose

Utils tests focus on:
- Data utility functions
- Trade visualization utilities
- Helper functions and utilities

## Test Categories

### Data Utilities (`data_utils.py`)
- Data validation and cleaning
- Data format conversion
- Data type handling
- Data transformation utilities

### Trade Visualization (`trade_visualization.py`)
- Trade data processing
- Trade visualization utilities
- Trade analysis functions
- Performance metrics calculation

## Running Utils Tests

```bash
# All utils tests
python -m pytest tests/utils/ -v

# Specific utils test
python -m pytest tests/utils/test_data_utils.py -v

# With coverage
python -m pytest tests/utils/ --cov=streamlit_lightweight_charts_pro.utils
```

## Test Patterns

### Data Utility Testing
```python
def test_data_validation_utilities():
    """Test data validation utility functions."""
    # Test valid data
    valid_data = {'time': [1, 2, 3], 'value': [100, 110, 120]}
    assert validate_data_structure(valid_data) is True
    
    # Test invalid data
    invalid_data = {'time': [1, 2], 'value': [100]}  # Mismatched lengths
    assert validate_data_structure(invalid_data) is False
```

### Trade Visualization Testing
```python
def test_trade_visualization_utilities():
    """Test trade visualization utility functions."""
    # Sample trade data
    trades = [
        {'entry_time': '2023-01-01 10:00:00', 'exit_time': '2023-01-01 15:00:00', 'pnl': 100},
        {'entry_time': '2023-01-02 09:00:00', 'exit_time': '2023-01-02 16:00:00', 'pnl': -50}
    ]
    
    # Process trades
    processed_trades = process_trade_data(trades)
    
    # Verify processing
    assert len(processed_trades) == 2
    assert all('entry_time' in trade for trade in processed_trades)
    assert all('exit_time' in trade for trade in processed_trades)
    assert all('pnl' in trade for trade in processed_trades)
```

## Future Enhancements

- **Performance testing**: Large dataset processing performance
- **Memory usage testing**: Memory efficiency of utility functions
- **Error handling testing**: Comprehensive error scenario coverage
- **Integration testing**: Utility function integration with main modules 