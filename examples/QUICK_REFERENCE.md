# Quick Reference Guide

## 🚀 Start Here

### First Time User
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the main example
streamlit run pane_heights_example.py
```

### Chart Type Examples
```bash
# Line Charts
streamlit run line_charts/line_chart_basic.py

# Candlestick Charts  
streamlit run candlestick_charts/basic_candlestick_chart.py

# Bar Charts
streamlit run bar_charts/basic_bar_chart.py

# Area Charts
streamlit run area_charts/basic_area_chart.py

# Histogram Charts
streamlit run histogram_charts/basic_histogram_chart.py

# Baseline Charts
streamlit run baseline_charts/basic_baseline_chart.py
```

## 📁 Directory Map

```
examples/
├── 🎯 pane_heights_example.py     # Start here - Multi-pane demo
├── 📸 images/                     # Screenshots and demos
├── 🧪 tests/                      # Test files
├── 🚀 advanced_features/          # Advanced functionality
├── 📈 line_charts/               # Line chart examples
├── 🕯️ candlestick_charts/        # OHLC chart examples
├── 📊 bar_charts/                # Bar chart examples
├── 🎨 area_charts/               # Area chart examples
├── 📊 histogram_charts/          # Histogram examples
├── 📏 baseline_charts/           # Baseline examples
├── 🔧 base_series/               # Series functionality
└── 🎨 background_shade_charts/   # Background examples
```

## 🎯 By Use Case

### 📊 Basic Charts
- **Line**: `line_charts/line_chart_basic.py`
- **Bar**: `bar_charts/basic_bar_chart.py`
- **Area**: `area_charts/basic_area_chart.py`

### 📈 Financial Charts
- **Candlestick**: `candlestick_charts/basic_candlestick_chart.py`
- **Volume**: `histogram_charts/basic_histogram_chart.py`
- **Multi-pane**: `pane_heights_example.py`

### 🚀 Advanced Features
- **Auto-sizing**: `advanced_features/auto_size_example.py`
- **Real-time**: `advanced_features/update_methods_example.py`
- **Annotations**: `advanced_features/annotation_structure_test.py`

### 🧪 Testing
- **Error Handling**: `tests/comprehensive_error_test.py`
- **Performance**: `tests/fit_content_test.py`
- **Validation**: `tests/error_handling_test.py`

## 🔧 Common Commands

### Running Examples
```bash
# Basic example
streamlit run pane_heights_example.py

# Chart type examples
streamlit run [chart_type]/basic_[chart_type]_chart.py

# Advanced features
streamlit run advanced_features/[feature_name].py
```

### Testing
```bash
# Run all tests
cd tests && pytest

# Run specific test
pytest comprehensive_error_test.py -v
```

### Development
```bash
# Install in development mode
pip install -e .

# Build frontend
cd streamlit_lightweight_charts_pro/frontend && npm run build
```

## 📚 Data Sources

### Sample Data
```python
from advanced_features.data_samples import (
    get_line_data,
    get_candlestick_data,
    get_bar_data,
    get_volume_data
)
```

### Real Data
```python
import pandas as pd

# Load CSV
df = pd.read_csv('your_data.csv')

# Convert to chart data
from streamlit_lightweight_charts_pro.data import LineData
data = [LineData(time=row['time'], value=row['value']) for _, row in df.iterrows()]
```

## 🎨 Customization

### Chart Options
```python
from streamlit_lightweight_charts_pro import ChartOptions, LayoutOptions

options = ChartOptions(
    width=800,
    height=600,
    layout=LayoutOptions(
        background_options={"color": "#ffffff"},
        text_color="#000000"
    )
)
```

### Series Styling
```python
from streamlit_lightweight_charts_pro import LineSeries, LineOptions

series = LineSeries(
    data=data,
    options=LineOptions(
        color="#2196F3",
        line_width=2
    )
)
```

## 🚨 Troubleshooting

### Common Issues
1. **Import Errors**: Check `pip install -r requirements.txt`
2. **Rendering Issues**: Rebuild frontend with `npm run build`
3. **Data Errors**: Validate data format in examples
4. **Performance Issues**: Check browser console for errors

### Debug Mode
```bash
# Run with debug output
streamlit run pane_heights_example.py --logger.level debug
```

## 📞 Getting Help

1. **Check Examples**: Start with `pane_heights_example.py`
2. **Review Documentation**: See main README.md
3. **Test Basic Functionality**: Try simple chart types first
4. **Check Console**: Browser developer tools for errors
5. **Report Issues**: Create GitHub issue with details

---

**Happy Charting! 📊✨** 