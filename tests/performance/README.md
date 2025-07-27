# Performance Tests

This directory contains comprehensive performance tests for the streamlit-lightweight-charts library, focusing on OHLCV data handling and processing.

## Test Scenarios

### Dataset Sizes

The performance tests are designed around real-world trading scenarios with the following dataset sizes:

| Dataset Size | Description | Data Points | Approximate Size |
|--------------|-------------|-------------|------------------|
| **Small** | 1 day of 1-minute data | 375 candles | ~15 KB |
| **Medium** | 1 month of 1-minute data | 7,500 candles | ~300 KB |
| **Large** | 1 year of 1-minute data | 94,125 candles | ~3.8 MB |
| **Very Large** | 9 years of 1-minute data | 847,125 candles | ~34 MB |

### Real-World Context

These test scenarios are based on typical trading data requirements:
- **Trading Day**: 375 minutes (6.25 hours of market data)
- **Trading Year**: 251 trading days
- **Data Frequency**: 1-minute OHLCV candles
- **Your Use Case**: 9 years of 1-minute data = ~850,000 data points

## Performance Test Categories

### 1. Data Creation Performance
Tests the performance of creating OHLCV data objects:
- Object instantiation time
- Memory usage during creation
- Time per data point
- Memory per data point

### 2. Serialization Performance
Tests the performance of converting OHLCV objects to dictionary format:
- `to_dict()` method performance
- Memory overhead of serialization
- Time per serialization operation
- Memory efficiency of serialized data

### 3. Validation Performance
Tests the performance of data validation:
- Validation time for all data points
- Time per validation operation
- Memory usage during validation

### 4. Memory Efficiency Tests
Tests memory management and cleanup:
- Memory usage before, during, and after processing
- Memory cleanup efficiency
- Memory overhead analysis
- Garbage collection performance

### 5. Concurrent Processing Tests
Tests performance with parallel processing:
- Multi-threaded data processing
- Thread pool performance
- Concurrent serialization
- Scalability with different thread counts

### 6. Batch Processing Tests
Tests performance with batch operations:
- Batch size optimization
- Memory usage with batching
- Processing time with different batch sizes
- Memory cleanup between batches

## Running Performance Tests

### Run All Performance Tests
```bash
python -m pytest tests/performance/ -v
```

### Run Specific Test Categories
```bash
# Run only OHLCV performance tests
python -m pytest tests/performance/test_ohlcv_performance.py -v

# Run only small dataset tests
python -m pytest tests/performance/test_ohlcv_performance.py::TestOhlcvDataPerformance::test_small_dataset_creation_performance -v

# Run only large dataset tests
python -m pytest tests/performance/test_ohlcv_performance.py::TestOhlcvDataPerformance::test_large_dataset_creation_performance -v
```

### Run with Performance Markers
```bash
# Run with performance markers
python -m pytest tests/performance/ -m performance -v

# Run with specific performance thresholds
python -m pytest tests/performance/ --performance-threshold=fast -v
```

## Performance Benchmarks

### Expected Performance Characteristics

#### Small Dataset (375 candles)
- **Creation Time**: < 1 second
- **Memory Usage**: < 50 MB
- **Serialization Time**: < 1 second
- **Time per Data Point**: < 3 ms

#### Medium Dataset (7,500 candles)
- **Creation Time**: < 5 seconds
- **Memory Usage**: < 500 MB
- **Serialization Time**: < 5 seconds
- **Time per Data Point**: < 1 ms

#### Large Dataset (94,125 candles)
- **Creation Time**: < 30 seconds
- **Memory Usage**: < 5 GB
- **Serialization Time**: < 60 seconds
- **Time per Data Point**: < 1 ms

#### Very Large Dataset (847,125 candles)
- **Creation Time**: < 300 seconds (5 minutes)
- **Memory Usage**: < 50 GB
- **Serialization Time**: < 600 seconds (10 minutes)
- **Time per Data Point**: < 1 ms

### Memory Efficiency Targets

- **Memory Overhead**: < 100% of data size
- **Serialization Overhead**: < 200% of original data size
- **Cleanup Efficiency**: > 90% memory recovery
- **Memory per Data Point**: < 1 KB per OHLCV object

## Performance Monitoring

### Key Metrics Tracked

1. **Time Metrics**
   - Total processing time
   - Time per data point
   - Time per operation type

2. **Memory Metrics**
   - Peak memory usage
   - Memory per data point
   - Memory cleanup efficiency
   - Memory overhead ratios

3. **Throughput Metrics**
   - Data points processed per second
   - Operations per second
   - Memory bandwidth usage

### Performance Reporting

The tests generate detailed performance reports including:
- Processing times for each dataset size
- Memory usage patterns
- Performance per data point
- Memory efficiency metrics
- Cleanup performance

## Optimization Recommendations

### For Your 9-Year Dataset (850K candles)

1. **Batch Processing**
   - Process data in chunks of 10,000 candles
   - Use garbage collection between batches
   - Monitor memory usage during processing

2. **Memory Management**
   - Clear references after processing
   - Use explicit garbage collection
   - Monitor peak memory usage

3. **Concurrent Processing**
   - Use 4-8 worker threads for serialization
   - Balance between CPU and memory usage
   - Monitor thread pool performance

4. **Data Validation**
   - Validate data in batches
   - Skip validation for trusted data sources
   - Use lazy validation where possible

## Troubleshooting Performance Issues

### Common Performance Problems

1. **High Memory Usage**
   - Check for memory leaks
   - Use smaller batch sizes
   - Force garbage collection more frequently

2. **Slow Processing**
   - Reduce validation overhead
   - Use concurrent processing
   - Optimize data structures

3. **Memory Not Recovered**
   - Check for circular references
   - Use explicit cleanup
   - Monitor garbage collection

### Performance Debugging

```bash
# Run with memory profiling
python -m pytest tests/performance/ --profile-memory -v

# Run with detailed timing
python -m pytest tests/performance/ --profile-time -v

# Run with system monitoring
python -m pytest tests/performance/ --monitor-system -v
```

## Continuous Performance Monitoring

### Automated Performance Checks

The performance tests include automated assertions to ensure performance doesn't regress:
- Maximum processing time limits
- Memory usage thresholds
- Performance per data point targets
- Memory cleanup efficiency requirements

### Performance Regression Detection

- Baseline performance measurements
- Automated performance comparisons
- Performance trend analysis
- Alert on performance degradation

## Future Performance Enhancements

### Planned Optimizations

1. **Memory Optimization**
   - Slotted classes for reduced memory overhead
   - Memory pooling for frequently created objects
   - Lazy loading for large datasets

2. **Processing Optimization**
   - Vectorized operations where possible
   - Caching for repeated operations
   - Streaming processing for very large datasets

3. **Concurrency Improvements**
   - Async/await support
   - Process pool for CPU-intensive operations
   - Memory-mapped files for very large datasets

### Performance Testing Roadmap

- [ ] Add memory profiling tests
- [ ] Add CPU profiling tests
- [ ] Add network I/O performance tests
- [ ] Add disk I/O performance tests
- [ ] Add concurrent access performance tests
- [ ] Add stress testing for edge cases 