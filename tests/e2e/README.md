# End-to-End Tests

This directory contains end-to-end tests that verify complete workflows from data input to chart rendering.

## Purpose

E2E tests focus on:
- Complete user workflows
- Full application integration
- Real-world usage scenarios
- Browser compatibility
- User interaction flows

## Test Categories

### Complete Chart Workflows
- Data input to chart rendering
- Multiple chart types and configurations
- Complex chart combinations
- Real-time data updates

### User Interaction Flows
- Chart interaction and responsiveness
- Data filtering and manipulation
- Chart customization workflows
- Export and sharing functionality

### Browser Compatibility
- Cross-browser rendering
- Mobile device compatibility
- Different screen resolutions
- Accessibility compliance

### Real-World Scenarios
- Financial data visualization
- Scientific data plotting
- Business intelligence dashboards
- Interactive data exploration

## Running E2E Tests

```bash
# All E2E tests
python -m pytest tests/e2e/ -v

# Specific E2E test
python -m pytest tests/e2e/test_chart_workflows.py -v

# With browser testing
python -m pytest tests/e2e/ --browser=chrome

# With visual regression testing
python -m pytest tests/e2e/ --visual-regression
```

## Test Patterns

### Complete Chart Workflow Testing
```python
def test_complete_line_chart_workflow(sample_chart_config):
    """Test complete workflow from data to rendered chart."""
    # 1. Prepare data
    data = LineData(
        time=sample_chart_config['data']['time'],
        value=sample_chart_config['data']['value']
    )
    
    # 2. Create series
    series = LineSeries(data=data)
    
    # 3. Configure chart
    options = ChartOptions(**sample_chart_config['options'])
    
    # 4. Generate chart configuration
    chart_config = {
        'series': [series.to_dict()],
        'options': options.to_dict()
    }
    
    # 5. Verify complete configuration
    assert 'series' in chart_config
    assert 'options' in chart_config
    assert len(chart_config['series']) == 1
    assert chart_config['series'][0]['type'] == 'line'
```

### User Interaction Testing
```python
def test_chart_interaction_workflow(sample_chart_config):
    """Test user interaction with charts."""
    # Create chart
    chart = create_chart_from_config(sample_chart_config)
    
    # Simulate user interactions
    interactions = [
        ('hover', {'x': 100, 'y': 200}),
        ('click', {'x': 150, 'y': 250}),
        ('zoom', {'scale': 1.5}),
        ('pan', {'deltaX': 50, 'deltaY': 0})
    ]
    
    for interaction_type, params in interactions:
        response = chart.handle_interaction(interaction_type, params)
        assert response is not None
        assert 'status' in response
```

### Browser Compatibility Testing
```python
@pytest.mark.parametrize("browser", ["chrome", "firefox", "safari"])
def test_browser_compatibility(browser, sample_chart_config):
    """Test chart rendering across different browsers."""
    # Setup browser
    driver = setup_browser(browser)
    
    try:
        # Load chart
        chart_html = generate_chart_html(sample_chart_config)
        driver.get(f"data:text/html,{chart_html}")
        
        # Wait for chart to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "lightweight-charts"))
        )
        
        # Verify chart elements
        chart_element = driver.find_element(By.CLASS_NAME, "lightweight-charts")
        assert chart_element.is_displayed()
        
        # Verify chart functionality
        canvas = driver.find_element(By.TAG_NAME, "canvas")
        assert canvas.is_displayed()
        
    finally:
        driver.quit()
```

### Real-World Scenario Testing
```python
def test_financial_data_workflow():
    """Test complete financial data visualization workflow."""
    # 1. Load financial data
    stock_data = load_stock_data("AAPL", "2023-01-01", "2023-12-31")
    
    # 2. Create candlestick chart
    candlestick_data = CandlestickData(
        time=stock_data['date'],
        open=stock_data['open'],
        high=stock_data['high'],
        low=stock_data['low'],
        close=stock_data['close']
    )
    
    # 3. Add volume histogram
    volume_data = HistogramData(
        time=stock_data['date'],
        value=stock_data['volume']
    )
    
    # 4. Create multi-pane chart
    chart = ChartBuilder()
    chart.add_series(CandlestickSeries(data=candlestick_data))
    chart.add_series(HistogramSeries(data=volume_data))
    
    # 5. Configure chart options
    options = ChartOptions(
        width=1200,
        height=800,
        layout=LayoutOptions(
            background=dict(color="#ffffff"),
            textColor="#000000"
        )
    )
    
    # 6. Generate and verify chart
    chart_config = chart.build(options)
    assert len(chart_config['series']) == 2
    assert chart_config['series'][0]['type'] == 'candlestick'
    assert chart_config['series'][1]['type'] == 'histogram'
```

## E2E Test Infrastructure

### Browser Automation
```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser_driver():
    """Setup browser driver for E2E tests."""
    driver = webdriver.Chrome()  # or Firefox, Safari
    yield driver
    driver.quit()
```

### Visual Regression Testing
```python
def test_visual_regression_chart_rendering(browser_driver, sample_chart_config):
    """Test visual regression for chart rendering."""
    # Load chart
    chart_html = generate_chart_html(sample_chart_config)
    browser_driver.get(f"data:text/html,{chart_html}")
    
    # Wait for chart to render
    WebDriverWait(browser_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "lightweight-charts"))
    )
    
    # Take screenshot
    screenshot = browser_driver.get_screenshot_as_png()
    
    # Compare with baseline
    assert compare_screenshots(screenshot, "baseline_chart.png")
```

### Performance E2E Testing
```python
def test_e2e_performance_large_dataset(sample_large_dataset):
    """Test E2E performance with large datasets."""
    import time
    
    start_time = time.time()
    
    # Create chart with large dataset
    series = LineSeries(data=sample_large_dataset)
    chart_config = series.to_dict()
    
    # Simulate rendering
    render_time = simulate_chart_rendering(chart_config)
    
    total_time = time.time() - start_time
    
    # Assert performance thresholds
    assert total_time < 5.0  # 5 seconds for complete workflow
    assert render_time < 2.0  # 2 seconds for rendering
```

## Future Enhancements

- **Automated visual regression testing**: Screenshot comparison
- **Cross-browser testing**: Multiple browser support
- **Mobile testing**: Mobile device compatibility
- **Accessibility testing**: WCAG compliance verification
- **Load testing**: High-traffic scenario simulation 