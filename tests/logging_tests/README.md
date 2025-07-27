# Logging Module Tests

This directory contains unit tests for the `logging_config.py` module of Streamlit Lightweight Charts Pro.

## Purpose

Logging tests focus on:
- Logging configuration setup
- Log level management
- Log format validation
- Log output verification

## Test Categories

### Logging Configuration
- Logger setup and initialization
- Log level configuration
- Handler configuration
- Formatter setup

### Log Output Validation
- Log message formatting
- Log level filtering
- Log output destinations
- Log rotation and retention

### Error Logging
- Exception logging
- Error message formatting
- Stack trace handling
- Error context preservation

### Performance Logging
- Performance metric logging
- Timing information
- Resource usage logging
- Performance threshold monitoring

## Running Logging Tests

```bash
# All logging tests
python -m pytest tests/logging/ -v

# Specific logging test
python -m pytest tests/logging/test_logging_config.py -v

# With coverage
python -m pytest tests/logging/ --cov=streamlit_lightweight_charts_pro.logging_config
```

## Test Patterns

### Logging Configuration Testing
```python
def test_logging_configuration():
    """Test logging configuration setup."""
    # Test logger initialization
    logger = setup_logging()
    assert logger is not None
    assert logger.name == 'streamlit_lightweight_charts_pro'
    
    # Test log level
    assert logger.level == logging.INFO
    
    # Test handlers
    assert len(logger.handlers) > 0
    assert any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers)
```

### Log Output Testing
```python
def test_log_message_output():
    """Test log message output and formatting."""
    import io
    from contextlib import redirect_stdout
    
    # Capture log output
    log_output = io.StringIO()
    
    with redirect_stdout(log_output):
        logger = setup_logging()
        logger.info("Test log message")
    
    # Verify log output
    output = log_output.getvalue()
    assert "Test log message" in output
    assert "INFO" in output
    assert "streamlit_lightweight_charts_pro" in output
```

### Error Logging Testing
```python
def test_error_logging():
    """Test error logging functionality."""
    import io
    from contextlib import redirect_stdout
    
    # Capture log output
    log_output = io.StringIO()
    
    with redirect_stdout(log_output):
        logger = setup_logging()
        
        try:
            raise ValueError("Test error")
        except ValueError as e:
            logger.error("An error occurred", exc_info=True)
    
    # Verify error log output
    output = log_output.getvalue()
    assert "ERROR" in output
    assert "An error occurred" in output
    assert "ValueError: Test error" in output
    assert "Traceback" in output
```

### Performance Logging Testing
```python
def test_performance_logging():
    """Test performance logging functionality."""
    import io
    import time
    from contextlib import redirect_stdout
    
    # Capture log output
    log_output = io.StringIO()
    
    with redirect_stdout(log_output):
        logger = setup_logging()
        
        # Log performance metric
        start_time = time.time()
        time.sleep(0.1)  # Simulate work
        duration = time.time() - start_time
        
        logger.info(f"Operation completed in {duration:.3f} seconds")
    
    # Verify performance log output
    output = log_output.getvalue()
    assert "Operation completed" in output
    assert "seconds" in output
```

## Mock Testing

### Log Handler Mock
```python
class MockLogHandler(logging.Handler):
    """Mock log handler for testing."""
    
    def __init__(self):
        super().__init__()
        self.logs = []
    
    def emit(self, record):
        self.logs.append({
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name
        })

def test_logging_with_mock_handler():
    """Test logging with mock handler."""
    # Setup mock handler
    mock_handler = MockLogHandler()
    logger = logging.getLogger('test_logger')
    logger.addHandler(mock_handler)
    logger.setLevel(logging.INFO)
    
    # Log messages
    logger.info("Test info message")
    logger.error("Test error message")
    
    # Verify logged messages
    assert len(mock_handler.logs) == 2
    assert mock_handler.logs[0]['level'] == 'INFO'
    assert mock_handler.logs[0]['message'] == 'Test info message'
    assert mock_handler.logs[1]['level'] == 'ERROR'
    assert mock_handler.logs[1]['message'] == 'Test error message'
```

## Log Level Testing

```python
@pytest.mark.parametrize("log_level,expected_output", [
    (logging.DEBUG, True),
    (logging.INFO, True),
    (logging.WARNING, True),
    (logging.ERROR, True),
    (logging.CRITICAL, True),
])
def test_log_levels(log_level, expected_output):
    """Test different log levels."""
    import io
    from contextlib import redirect_stdout
    
    log_output = io.StringIO()
    
    with redirect_stdout(log_output):
        logger = setup_logging()
        logger.log(log_level, f"Test {logging.getLevelName(log_level)} message")
    
    output = log_output.getvalue()
    if expected_output:
        assert logging.getLevelName(log_level) in output
    else:
        assert logging.getLevelName(log_level) not in output
```

## Future Enhancements

- **Log rotation testing**: File rotation and retention testing
- **Log performance testing**: Logging performance impact
- **Structured logging testing**: JSON log format testing
- **Log aggregation testing**: Centralized logging system testing 