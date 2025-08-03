# Advanced Features Examples

This directory contains examples demonstrating advanced functionality of the Streamlit Lightweight Charts Pro library.

## 📁 Contents

### 🎛️ Auto-sizing Example
- **File**: `auto_size_example.py`
- **Description**: Demonstrates dynamic chart sizing based on container dimensions
- **Features**: Responsive layouts, automatic resizing, container adaptation

### 🔄 Update Methods Example
- **File**: `update_methods_example.py`
- **Description**: Shows real-time data updates and dynamic chart modifications
- **Features**: Live data streaming, chart updates, performance optimization

### 📊 Multi-pane Legends Example
- **File**: `multi_pane_legends_example.py`
- **Description**: Complex legend configurations for multi-pane charts
- **Features**: Custom legend positioning, multi-series legends, interactive legends

### 📈 Data Samples
- **File**: `data_samples.py`
- **Description**: Comprehensive data generation utilities for all chart types
- **Features**: Sample datasets, data formatting, realistic test data

### 🏷️ Annotation Structure
- **File**: `annotation_structure_test.py`
- **Description**: Advanced annotation systems and configurations
- **Features**: Text annotations, arrows, shapes, custom styling

## 🚀 Running Examples

### Auto-sizing Example
```bash
streamlit run auto_size_example.py
```

### Update Methods Example
```bash
streamlit run update_methods_example.py
```

### Data Samples
```bash
# Import and use in other examples
from data_samples import get_line_data, get_candlestick_data
```

## 🎯 Use Cases

### Auto-sizing
- **Responsive dashboards**: Charts that adapt to different screen sizes
- **Embedded applications**: Charts that fit within containers
- **Mobile applications**: Optimized for various device sizes

### Real-time Updates
- **Trading applications**: Live price updates
- **Monitoring dashboards**: Real-time metrics
- **Live data feeds**: Streaming data visualization

### Multi-pane Legends
- **Complex charts**: Multiple series with custom legends
- **Professional dashboards**: Advanced legend positioning
- **Custom layouts**: Tailored legend configurations

### Data Samples
- **Development**: Quick data for testing
- **Prototyping**: Sample data for new features
- **Documentation**: Consistent examples across documentation

### Annotations
- **Trading signals**: Entry/exit points, support/resistance
- **Event markers**: Important dates, announcements
- **Custom overlays**: User-defined annotations

## 🔧 Advanced Configuration

### Auto-sizing Options
```python
chart = Chart(
    options=ChartOptions(
        auto_size=True,
        width=800,
        height=600
    )
)
```

### Update Methods
```python
# Update series data
series.setData(new_data)

# Update chart options
chart.update_options(height=700)

# Real-time updates
def update_chart():
    # Add new data point
    series.update(new_point)
```

### Custom Legends
```python
# Legend configuration
legend_options = LegendOptions(
    visible=True,
    position="top-right",
    font_size=12
)
```

### Advanced Annotations
```python
# Create custom annotation
annotation = create_text_annotation(
    time="2024-01-01",
    price=100,
    text="Important Event",
    color="#FF0000"
)
```

## 📚 Integration

These advanced features can be combined to create sophisticated charting applications:

1. **Start with basic examples** from the main chart type directories
2. **Add auto-sizing** for responsive behavior
3. **Implement real-time updates** for live data
4. **Customize legends** for professional appearance
5. **Add annotations** for enhanced functionality

## 🛠️ Development Tips

### Performance Optimization
- Use efficient data structures for large datasets
- Implement proper cleanup for real-time updates
- Optimize rendering for smooth animations

### Best Practices
- Follow the example structure for consistency
- Add proper error handling for real-time features
- Test thoroughly across different screen sizes
- Document custom configurations

### Debugging
- Use browser console for frontend debugging
- Check Python logs for backend issues
- Validate data formats before rendering
- Test with different data sizes

---

**Explore these advanced features to unlock the full potential of Streamlit Lightweight Charts Pro! 🚀** 