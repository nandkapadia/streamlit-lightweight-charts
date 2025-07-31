# Streamlit Lightweight Charts Pro - Examples

This directory contains comprehensive examples demonstrating the capabilities of the Streamlit Lightweight Charts Pro library.

## 📁 Directory Structure

```
examples/
├── README.md                    # This file
├── requirements.txt             # Python dependencies for examples
├── __init__.py                  # Package initialization
├── pane_heights_example.py      # Multi-pane chart with custom heights
├── images/                      # Screenshots and demo images
├── tests/                       # Test files and validation scripts
├── advanced_features/           # Advanced functionality examples
├── area_charts/                 # Area chart examples
├── bar_charts/                  # Bar chart examples
├── baseline_charts/             # Baseline chart examples
├── candlestick_charts/          # Candlestick chart examples
├── histogram_charts/            # Histogram chart examples
├── line_charts/                 # Line chart examples
├── base_series/                 # Base series functionality
└── background_shade_charts/     # Background shading examples
```

## 🚀 Quick Start

### Basic Examples

1. **Pane Heights Example** - Multi-pane charts with custom sizing:
   ```bash
   streamlit run pane_heights_example.py
   ```

### Chart Type Examples

Each chart type has its own directory with multiple examples:

- **Line Charts**: `line_charts/` - Basic and advanced line chart configurations
- **Candlestick Charts**: `candlestick_charts/` - OHLC data visualization
- **Bar Charts**: `bar_charts/` - Bar and histogram visualizations
- **Area Charts**: `area_charts/` - Filled area charts
- **Baseline Charts**: `baseline_charts/` - Baseline comparison charts
- **Histogram Charts**: `histogram_charts/` - Volume and distribution charts

### Advanced Features

The `advanced_features/` directory contains examples of:

- **Auto-sizing**: Dynamic chart sizing based on container
- **Update Methods**: Real-time data updates
- **Multi-pane Legends**: Complex legend configurations
- **Data Samples**: Various data format examples
- **Annotation Structure**: Advanced annotation systems

## 📊 Example Categories

### 🎯 Core Features
- **Pane Heights**: Custom multi-pane layouts with proportional sizing
- **Chart Types**: All supported chart types with configurations
- **Data Handling**: Various data formats and sources

### 🔧 Advanced Features
- **Auto-sizing**: Responsive chart sizing
- **Real-time Updates**: Dynamic data updates
- **Annotations**: Text, arrows, and shape annotations
- **Trade Visualization**: Trading-specific visualizations
- **Custom Styling**: Advanced styling options

### 🧪 Testing & Validation
- **Error Handling**: Comprehensive error scenarios
- **Performance Tests**: Large dataset handling
- **Compatibility Tests**: Cross-browser and device testing

## 📖 How to Use Examples

### Running Examples

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Basic Example**:
   ```bash
   streamlit run pane_heights_example.py
   ```

3. **Run Chart Type Examples**:
   ```bash
   # Line charts
   streamlit run line_charts/line_chart_basic.py
   
   # Candlestick charts
   streamlit run candlestick_charts/basic_candlestick_chart.py
   
   # Bar charts
   streamlit run bar_charts/basic_bar_chart.py
   ```

### Example Structure

Each example follows a consistent structure:

```python
#!/usr/bin/env python3
"""
Example Title and Description

This example demonstrates [specific functionality].
"""

import streamlit as st
from streamlit_lightweight_charts_pro import Chart, ChartOptions, ...

# 1. Page Configuration
st.set_page_config(page_title="Example Title", layout="wide")
st.title("Example Title")

# 2. Description
st.write("Description of what this example shows...")

# 3. Data Generation/Loading
# ... data preparation code ...

# 4. Chart Creation
chart = Chart(
    options=ChartOptions(...),
    series=[...]
)

# 5. Rendering
chart.render(key="unique_key")

# 6. Additional Features
# ... interactive controls, explanations, etc ...
```

## 🎨 Customization

### Chart Options
All examples demonstrate various chart options:
- **Layout Options**: Background, grid, pane configurations
- **Interaction Options**: Scroll, scale, crosshair settings
- **Styling Options**: Colors, fonts, line styles
- **Price Scale Options**: Scale positioning and formatting

### Series Configuration
Examples show how to configure different series types:
- **Data Formatting**: Time series, OHLC, volume data
- **Styling**: Colors, line styles, markers
- **Interactivity**: Tooltips, hover effects
- **Multi-pane**: Series placement across panes

## 🔍 Finding Specific Examples

### By Chart Type
- **Line Charts**: `line_charts/` directory
- **Candlestick Charts**: `candlestick_charts/` directory
- **Bar Charts**: `bar_charts/` directory
- **Area Charts**: `area_charts/` directory
- **Histogram Charts**: `histogram_charts/` directory

### By Feature
- **Pane Heights**: `pane_heights_example.py`
- **Auto-sizing**: `advanced_features/auto_size_example.py`
- **Real-time Updates**: `advanced_features/update_methods_example.py`
- **Annotations**: `advanced_features/annotation_structure_test.py`

### By Complexity
- **Basic**: Each chart type directory contains basic examples
- **Advanced**: `advanced_features/` directory
- **Testing**: `tests/` directory

## 📸 Screenshots

The `images/` directory contains screenshots of various examples:
- Chart type demonstrations
- Feature showcases
- Multi-pane layouts
- Interactive examples

## 🛠️ Development

### Adding New Examples

1. **Create the file** in the appropriate directory
2. **Follow the structure** shown above
3. **Add documentation** with clear descriptions
4. **Test thoroughly** before committing
5. **Update this README** if adding new categories

### Testing Examples

Run the test suite:
```bash
cd tests/
python -m pytest *.py
```

## 📚 Additional Resources

- **Documentation**: See the main project README
- **API Reference**: Check the source code for detailed API documentation
- **Issues**: Report bugs or request features on GitHub
- **Contributions**: Submit pull requests for improvements

## 🎯 Getting Help

If you encounter issues with the examples:

1. **Check Dependencies**: Ensure all requirements are installed
2. **Review Documentation**: Check the main project documentation
3. **Test Basic Example**: Try `pane_heights_example.py` first
4. **Check Console**: Look for error messages in the browser console
5. **Report Issues**: Create a GitHub issue with details

---

**Happy Charting! 📊✨** 