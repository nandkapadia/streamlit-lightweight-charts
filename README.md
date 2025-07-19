# streamlit-lightweight-charts-pro
Enhanced Streamlit wrapper for performant Tradingview's Financial: `lightweight-charts` with ultra-simplified API and performance optimizations

The Lightweight Charts library is the best choice to display financial data as an interactive chart on a web page without affecting loading speed and performance.

- [Features Demo](https://www.tradingview.com/lightweight-charts/)
- [Documentation](https://tradingview.github.io/lightweight-charts/)
- [GitHub](https://github.com/tradingview/lightweight-charts)
- [Pypi](https://pypi.org/project/streamlit-lightweight-charts/)

### Versions
- Version 0.7.19 - FIX: React build was not been commited
- Version 0.7.20 - Example loading from CSV
- Version 0.8.0 - OOP API with composite charts, trade visualization, and annotation systems

## How to install:
```
python -m pip install streamlit-lightweight-charts-pro
```

## Development Setup

For contributors and developers:

### Install Development Dependencies
```bash
# Install the package in development mode with linting tools
pip install -e ".[dev]"

# Or install development dependencies separately
make install-dev
```

### Code Quality Tools

The project uses several tools to maintain code quality:

- **Black**: Code formatting (line length: 100)
- **isort**: Import sorting (compatible with Black)
- **pylint**: Code quality checks
- **pre-commit**: Automatic checks before commits

### Running Linting Tools

```bash
# Run all linting tools and fix issues
make lint

# Check for issues without fixing
make lint-check

# Format code only
make format

# Run tests
make test

# Run tests with coverage
make test-cov
```

### Pre-commit Hooks

Install pre-commit hooks to automatically run linting on commits:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hook scripts
pre-commit install

# Run against all files (optional)
pre-commit run --all-files
```

### Manual Linting

You can also run individual tools:

```bash
# Format code
black streamlit_lightweight_charts examples tests

# Sort imports
isort streamlit_lightweight_charts examples tests

# Check code quality
pylint streamlit_lightweight_charts examples tests
```

## New in Version 0.8.0: Object-Oriented API

The library now provides a clean, type-safe object-oriented API alongside the original dictionary-based approach.

### Quick Start with OOP API

```python
from streamlit_lightweight_charts_pro import SinglePaneChart, CandlestickSeries
from streamlit_lightweight_charts.data import OhlcData
import pandas as pd

# Create data
data = [
    OhlcData(time=pd.Timestamp('2024-01-01'), open=100, high=105, low=98, close=102),
    OhlcData(time=pd.Timestamp('2024-01-02'), open=102, high=108, low=101, close=106),
    # ... more data
]

# Create and render chart
chart = SinglePaneChart(series=[CandlestickSeries(data=data)])
chart.render(key='candlestick_chart')
```

### Composite Charts - New Feature!

Pre-built chart combinations for common financial visualizations:

#### PriceVolumeChart
The most common financial chart with price and volume:
```python
from streamlit_lightweight_charts import PriceVolumeChart
import pandas as pd

# Load your DataFrame with OHLC and volume data
df = pd.read_csv('stock_data.csv', index_col='date', parse_dates=True)

# Create price-volume chart with one line
chart = PriceVolumeChart(
    df=df,
    price_type='candlestick',  # or 'line', 'area', 'bar'
    price_height=400,
    volume_height=100
)
chart.render(key='price_volume')
```

#### Other Composite Charts
- **ComparisonChart**: Compare multiple instruments with normalization

### Trade Visualization - New Feature!

Visualize trades directly on candlestick charts with multiple styles:

```python
from streamlit_lightweight_charts import (
    CandlestickChart, Trade, TradeType, 
    TradeVisualization, TradeVisualizationOptions
)

# Create trades
trades = [
    Trade(
        entry_time=pd.Timestamp('2024-01-01'),
        entry_price=100,
        exit_time=pd.Timestamp('2024-01-05'),
        exit_price=105,
        quantity=100,
        trade_type=TradeType.LONG,
        id="T001"
    )
]

# Create chart with trades
chart = CandlestickChart(
    data=ohlc_data,
    trades=trades,
    trade_visualization_options=TradeVisualizationOptions(
        style=TradeVisualization.BOTH  # Shows markers and rectangles
    )
)
```

**Visualization Styles:**
- `MARKERS` - Entry/exit arrows
- `RECTANGLES` - Boxes from entry to exit
- `BOTH` - Markers + rectangles
- `LINES` - Simple connecting lines
- `ARROWS` - Directional arrows
- `ZONES` - Colored background zones

### Auto-Sizing Charts - New Feature!

Automatically size charts to fit their container dimensions with responsive behavior:

```python
from streamlit_lightweight_charts import CandlestickChart

# Full auto-sizing
chart = CandlestickChart(
    data=ohlc_data,
    chart_options={
        "autoSize": True,
        "minWidth": 300,
        "maxWidth": 1200,
        "minHeight": 200,
        "maxHeight": 800,
    }
)

# Auto-width only (fixed height)
chart = CandlestickChart(
    data=ohlc_data,
    chart_options={
        "autoWidth": True,
        "height": 400,  # Fixed height
        "minWidth": 300,
        "maxWidth": 1200,
    }
)

# Auto-height only (fixed width)
chart = CandlestickChart(
    data=ohlc_data,
    chart_options={
        "autoHeight": True,
        "width": 600,  # Fixed width
        "minHeight": 200,
        "maxHeight": 800,
    }
)
```

**Features:**
- ✅ **Responsive Design**: Charts automatically resize when container changes
- ✅ **Size Constraints**: Set minimum and maximum dimensions
- ✅ **Flexible Options**: Auto-size width, height, or both
- ✅ **Performance**: Uses ResizeObserver for efficient updates
- ✅ **Streamlit Integration**: Works seamlessly with Streamlit's responsive layout

### Fit Content on Load - New Feature!

Automatically fit charts to their content when first displayed, ensuring all data is visible:

```python
from streamlit_lightweight_charts import CandlestickChart

# Default behavior - chart fits to content automatically
chart = CandlestickChart(
    data=ohlc_data,
    chart_options={
        "fit_content_on_load": True  # This is the default
    }
)

# Disable fit content behavior
chart = CandlestickChart(
    data=ohlc_data,
    chart_options={
        "fit_content_on_load": False
    }
)
```

**Features:**
- ✅ **Automatic Fitting**: Charts automatically show all data when first displayed
- ✅ **Configurable**: Can be enabled/disabled per chart
- ✅ **Smart Timing**: Fits content after chart is fully initialized
- ✅ **Error Handling**: Gracefully handles cases where fitting fails
- ✅ **Default Behavior**: Enabled by default for better user experience

### Range Switcher - New Feature!

Add professional time range switching to any chart, similar to TradingView:

```python
from streamlit_lightweight_charts import CandlestickChart

# Create chart with range switcher
chart = CandlestickChart(
    data=ohlc_data,
    range_switcher={
        "ranges": [
            {"label": "1D", "seconds": 86400},
            {"label": "1W", "seconds": 604800},
            {"label": "1M", "seconds": 2592000},
            {"label": "3M", "seconds": 7776000},
            {"label": "6M", "seconds": 15552000},
            {"label": "1Y", "seconds": 31536000},
            {"label": "ALL", "seconds": None}
        ],
        "position": "top-right",
        "visible": True,
        "defaultRange": "1M"
    }
)
```

**Range Switcher Features:**
- **Professional Styling**: Matches TradingView's design with proper fonts, colors, and spacing
- **Active State Management**: Visual feedback for the currently selected range
- **Hover Effects**: Smooth transitions and hover states for better UX
- **Flexible Positioning**: Can be positioned in any corner of the chart
- **Customizable Ranges**: Easy to add or modify time ranges
- **Callback Support**: Ready for event handling and integration

**Available Time Ranges:**
- **1D**: Last 24 hours
- **1W**: Last 7 days
- **1M**: Last 30 days
- **3M**: Last 90 days
- **6M**: Last 180 days
- **1Y**: Last 365 days
- **ALL**: Show all available data

### Benefits of the OOP API
- **Type Safety**: Full type hints and IDE autocompletion
- **Cleaner Code**: No more nested dictionaries
- **Data Validation**: Automatic validation of chart data
- **Pandas Integration**: Seamless DataFrame support with timezone handling
- **Extensible**: Easy to create custom chart types

### Documentation
- [TIME_HANDLING_GUIDE.md](TIME_HANDLING_GUIDE.md) - Advanced timezone and datetime handling
- [SPECIALIZED_CHARTS_GUIDE.md](SPECIALIZED_CHARTS_GUIDE.md) - Using specialized chart classes
- [COMPOSITE_CHARTS_GUIDE.md](COMPOSITE_CHARTS_GUIDE.md) - Pre-built chart combinations

### Migration from Dictionary API
The original dictionary-based API is still fully supported. The OOP API is an optional enhancement for better developer experience.

---

## Original Dictionary-Based API

### How to use:
```
from streamlit_lightweight_charts import render_chart

render_chart(charts: <List of Dicts> , key: <str>)
```

### API
- charts: `<List of Dicts>`

    - [chart](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions): `<Dict>`

    - [series](https://tradingview.github.io/lightweight-charts/docs/series-types): `<List of Dicts>`

        - [type](https://tradingview.github.io/lightweight-charts/docs/series-types): `<str-enum>`
            [ Area, Bar, Baseline, Candlestick, Histogram, Line ]

        - data: `<List of Dicts>` accordingly to series type

        - options: `<Dict>` with style options

        - priceScale: `<Dict>` optional

        - markers: `<List of Dicts>` optional

        - rangeSwitcher: `<Dict>` optional - Add time range switching functionality

            - ranges: `<List of Dicts>` - List of time ranges
                - label: `<str>` - Display text (e.g., "1D", "1W", "1M")
                - seconds: `<int or None>` - Duration in seconds (None for "ALL")
            - position: `<str>` - Position of switcher ("top-left", "top-right", "bottom-left", "bottom-right")
            - visible: `<bool>` - Whether the range switcher is visible
            - defaultRange: `<str>` - Default selected range label

- key: `<str>` when creating multiple charts in one page

<br/>

# e.g.:
<br />

# Overlaid Charts

[![Price with Volume Chart](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/PriceVolumeChart.png?raw=true)](https://freyastreamlit-streamlit-lightw-examplespricevolumechart-j8ldyo.streamlit.app/)

### [Click for a working sample on Streamlit Cloud ⬆](https://freyastreamlit-streamlit-lightw-examplespricevolumechart-j8ldyo.streamlit.app/)
<br />

```python
import streamlit as st
from streamlit_lightweight_charts import render_chart
import streamlit_lightweight_charts.dataSamples as data

priceVolumeChartOptions = {
    "height": 400,
    "rightPriceScale": {
        "scaleMargins": {
            "top": 0.2,
            "bottom": 0.25,
        },
        "borderVisible": False,
    },
    "overlayPriceScales": {
        "scaleMargins": {
            "top": 0.7,
            "bottom": 0,
        }
    },
    "layout": {
        "background": {
            "type": 'solid',
            "color": '#131722'
        },
        "textColor": '#d1d4dc',
    },
    "grid": {
        "vertLines": {
            "color": 'rgba(42, 46, 57, 0)',
        },
        "horzLines": {
            "color": 'rgba(42, 46, 57, 0.6)',
        }
    }
}

priceVolumeSeries = [
    {
        "type": 'Area',
        "data": data.priceVolumeSeriesArea,
        "options": {
            "topColor": 'rgba(38,198,218, 0.56)',
            "bottomColor": 'rgba(38,198,218, 0.04)',
            "lineColor": 'rgba(38,198,218, 1)',
            "lineWidth": 2,
        }
    },
    {
        "type": 'Histogram',
        "data": data.priceVolumeSeriesHistogram,
        "options": {
            "color": '#26a69a',
            "priceFormat": {
                "type": 'volume',
            },
            "priceScaleId": "" # set as an overlay setting,
        },
        "priceScale": {
            "scaleMargins": {
                "top": 0.7,
                "bottom": 0,
            }
        }
    }
]
st.subheader("Price and Volume Series Chart")

render_chart([
    {
        "chart": priceVolumeChartOptions,
        "series": priceVolumeSeries
    }
], 'priceAndVolume')
```
---
<br />

[![Overlaid Areas Chart](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/OverlaidAreasChart.png?raw=true)](https://freyastreamlit-streamlit-ligh-examplesoverlaidareaschart-3pg5tr.streamlit.app/)

### [Click for a working sample on Streamlit Cloud ⬆](https://freyastreamlit-streamlit-ligh-examplesoverlaidareaschart-3pg5tr.streamlit.app/)
<br />

```python
import streamlit as st
from streamlit_lightweight_charts import render_chart
import streamlit_lightweight_charts.dataSamples as data

overlaidAreaSeriesOptions = {
    "height": 400,
    "rightPriceScale": {
        "scaleMargins": {
            "top": 0.1,
            "bottom": 0.1,
        },
        "mode": 2, # PriceScaleMode: 0-Normal, 1-Logarithmic, 2-Percentage, 3-IndexedTo100
        "borderColor": 'rgba(197, 203, 206, 0.4)',
    },
    "timeScale": {
        "borderColor": 'rgba(197, 203, 206, 0.4)',
    },
    "layout": {
        "background": {
            "type": 'solid',
            "color": '#100841'
        },
        "textColor": '#ffffff',
    },
    "grid": {
        "vertLines": {
            "color": 'rgba(197, 203, 206, 0.4)',
            "style": 1, # LineStyle: 0-Solid, 1-Dotted, 2-Dashed, 3-LargeDashed
        },
        "horzLines": {
            "color": 'rgba(197, 203, 206, 0.4)',
            "style": 1, # LineStyle: 0-Solid, 1-Dotted, 2-Dashed, 3-LargeDashed
        }
    }
}

seriesOverlaidChart = [
    {
        "type": 'Area',
        "data": data.seriesMultipleChartArea01,
        "options": {
            "topColor": 'rgba(255, 192, 0, 0.7)',
            "bottomColor": 'rgba(255, 192, 0, 0.3)',
            "lineColor": 'rgba(255, 192, 0, 1)',
            "lineWidth": 2,
        },
        "markers": [
            {
                "time": '2019-04-08',
                "position": 'aboveBar',
                "color": 'rgba(255, 192, 0, 1)',
                "shape": 'arrowDown',
                "text": 'H',
                "size": 3
            },
            {
                "time": '2019-05-13',
                "position": 'belowBar',
                "color": 'rgba(255, 192, 0, 1)',
                "shape": 'arrowUp',
                "text": 'L',
                "size": 3
            },
        ]
    },
    {
        "type": 'Area',
        "data": data.seriesMultipleChartArea02,
        "options": {
            "topColor": 'rgba(67, 83, 254, 0.7)',
            "bottomColor": 'rgba(67, 83, 254, 0.3)',
            "lineColor": 'rgba(67, 83, 254, 1)',
            "lineWidth": 2,
        },
        "markers": [

            {
                "time": '2019-05-03',
                "position": 'aboveBar',
                "color": 'rgba(67, 83, 254, 1)',
                "shape": 'arrowDown',
                "text": 'PEAK',
                "size": 3
            },
        ]
    }
]
st.subheader("Overlaid Series with Markers")

render_chart([
    {
        "chart": overlaidAreaSeriesOptions,
        "series": seriesOverlaidChart
    }
], 'overlaid')
```
---

# Streamlit integration

[![Data Toggling for an Area Chart](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/DataToggling.png?raw=true)](https://freyastreamlit-streamlit-lightweigh-examplesdatatoggling-cbni35.streamlit.app/)

### [Click for a working sample on Streamlit Cloud ⬆](https://freyastreamlit-streamlit-lightweigh-examplesdatatoggling-cbni35.streamlit.app/)
<br />

```python
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data

chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

st.subheader("Data Toggling for an Area Chart")

data_select = st.sidebar.radio('Select data source:', ('Area 01', 'Area 02'))

if data_select == 'Area 01':
    renderLightweightCharts( [
        {
            "chart": chartOptions,
            "series": [{
                "type": 'Area',
                "data": data.seriesMultipleChartArea01,
                "options": {}
            }],
        }
    ], 'area')
else:
    renderLightweightCharts( [
        {
            "chart": chartOptions,
            "series": [{
                "type": 'Area',
                "data": data.seriesMultipleChartArea02,
                "options": {}
            }],
        }
    ], 'area')
```
---
<br />

![Multi Pane Chart with Pandas](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/MultiPaneChartsWithPandas.png?raw=true)

```python
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

import json
import numpy as np
import yfinance as yf
import pandas as pd
import pandas_ta as ta

COLOR_BULL = 'rgba(38,166,154,0.9)' # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350

# Request historic pricing data via finance.yahoo.com API
df = yf.Ticker('AAPL').history(period='4mo')[['Open', 'High', 'Low', 'Close', 'Volume']]

# Some data wrangling to match required format
df = df.reset_index()
df.columns = ['time','open','high','low','close','volume']                  # rename columns
df['time'] = df['time'].dt.strftime('%Y-%m-%d')                             # Date to string
df['color'] = np.where(  df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)  # bull or bear
df.ta.macd(close='close', fast=6, slow=12, signal=5, append=True)           # calculate macd

# export to JSON format
candles = json.loads(df.to_json(orient = "records"))
volume = json.loads(df.rename(columns={"volume": "value",}).to_json(orient = "records"))
macd_fast = json.loads(df.rename(columns={"MACDh_6_12_5": "value"}).to_json(orient = "records"))
macd_slow = json.loads(df.rename(columns={"MACDs_6_12_5": "value"}).to_json(orient = "records"))
df['color'] = np.where(  df['MACD_6_12_5'] > 0, COLOR_BULL, COLOR_BEAR)  # MACD histogram color
macd_hist = json.loads(df.rename(columns={"MACD_6_12_5": "value"}).to_json(orient = "records"))


chartMultipaneOptions = [
    {
        "width": 600,
        "height": 400,
        "layout": {
            "background": {
                "type": "solid",
                "color": 'white'
            },
            "textColor": "black"
        },
        "grid": {
            "vertLines": {
                "color": "rgba(197, 203, 206, 0.5)"
                },
            "horzLines": {
                "color": "rgba(197, 203, 206, 0.5)"
            }
        },
        "crosshair": {
            "mode": 0
        },
        "priceScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)"
        },
        "timeScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)",
            "barSpacing": 15
        },
        "watermark": {
            "visible": True,
            "fontSize": 48,
            "horzAlign": 'center',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.3)',
            "text": 'AAPL - D1',
        }
    },
    {
        "width": 600,
        "height": 100,
        "layout": {
            "background": {
                "type": 'solid',
                "color": 'transparent'
            },
            "textColor": 'black',
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(42, 46, 57, 0)',
            },
            "horzLines": {
                "color": 'rgba(42, 46, 57, 0.6)',
            }
        },
        "timeScale": {
            "visible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'left',
            "vertAlign": 'top',
            "color": 'rgba(171, 71, 188, 0.7)',
            "text": 'Volume',
        }
    },
    {
        "width": 600,
        "height": 200,
        "layout": {
            "background": {
                "type": "solid",
                "color": 'white'
            },
            "textColor": "black"
        },
        "timeScale": {
            "visible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'left',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.7)',
            "text": 'MACD',
        }
    }
]

seriesCandlestickChart = [
    {
        "type": 'Candlestick',
        "data": candles,
        "options": {
            "upColor": COLOR_BULL,
            "downColor": COLOR_BEAR,
            "borderVisible": False,
            "wickUpColor": COLOR_BULL,
            "wickDownColor": COLOR_BEAR
        }
    }
]

seriesVolumeChart = [
    {
        "type": 'Histogram',
        "data": volume,
        "options": {
            "priceFormat": {
                "type": 'volume',
            },
            "priceScaleId": "" # set as an overlay setting,
        },
        "priceScale": {
            "scaleMargins": {
                "top": 0,
                "bottom": 0,
            },
            "alignLabels": False
        }
    }
]

seriesMACDchart = [
    {
        "type": 'Line',
        "data": macd_fast,
        "options": {
            "color": 'blue',
            "lineWidth": 2
        }
    },
    {
        "type": 'Line',
        "data": macd_slow,
        "options": {
            "color": 'green',
            "lineWidth": 2
        }
    },
    {
        "type": 'Histogram',
        "data": macd_hist,
        "options": {
            "color": 'red',
            "lineWidth": 1
        }
    }
]

st.subheader("Multipane Chart with Pandas")

renderLightweightCharts([
    {
        "chart": chartMultipaneOptions[0],
        "series": seriesCandlestickChart
    },
    {
        "chart": chartMultipaneOptions[1],
        "series": seriesVolumeChart
    },
    {
        "chart": chartMultipaneOptions[2],
        "series": seriesMACDchart
    }
], 'multipane')
```
---
<br />

![Multi Pane Chart (intraday) from CSV)](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/MultiPaneChartsFromCSV.png?raw=true)

```python
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

import json
import numpy as np
import pandas as pd

COLOR_BULL = 'rgba(38,166,154,0.9)' # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350

CSVFILE = 'https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/MultiPaneChartsFromCSV.csv?raw=true'

df = pd.read_csv(CSVFILE, skiprows=0, parse_dates=['datetime'], skip_blank_lines=True)

df['time'] = df['datetime'].view('int64') // 10**9  # We will use time in UNIX timestamp
df['color'] = np.where(  df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)  # bull or bear

# export to JSON format
candles = json.loads(
    df.filter(['time','open','high','low','close'], axis=1)
      .to_json(orient = "records") )

volume = json.loads(
    df.filter(['time','volume'], axis=1)
      .rename(columns={"volume": "value",})
      .to_json(orient = "records") )

macd_fast = json.loads(
    df.filter(['time','macd_fast'], axis=1)
      .rename(columns={"macd_fast": "value"})
      .to_json(orient = "records"))

macd_slow = json.loads(
    df.filter(['time','macd_slow'], axis=1)
      .rename(columns={"macd_slow": "value"})
      .to_json(orient = "records"))

df['color'] = np.where(  df['macd_hist'] > 0, COLOR_BULL, COLOR_BEAR)  # MACD histogram color
macd_hist = json.loads(
    df.filter(['time','macd_hist'], axis=1)
      .rename(columns={"macd_hist": "value"})
      .to_json(orient = "records"))

chartMultipaneOptions = [
    {
        "width": 600,
        "height": 400,
        "layout": {
            "background": {
                "type": "solid",
                "color": 'white'
            },
            "textColor": "black"
        },
        "grid": {
            "vertLines": {
                "color": "rgba(197, 203, 206, 0.5)"
                },
            "horzLines": {
                "color": "rgba(197, 203, 206, 0.5)"
            }
        },
        "crosshair": {
            "mode": 0
        },
        "priceScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)"
        },
        "timeScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)",
            "barSpacing": 10,
            "minBarSpacing": 8,
            "timeVisible": True,
            "secondsVisible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 48,
            "horzAlign": 'center',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.3)',
            "text": 'Intraday',
        }
    },
    {
        "width": 600,
        "height": 100,
        "layout": {
            "background": {
                "type": 'solid',
                "color": 'transparent'
            },
            "textColor": 'black',
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(42, 46, 57, 0)',
            },
            "horzLines": {
                "color": 'rgba(42, 46, 57, 0.6)',
            }
        },
        "timeScale": {
            "visible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'left',
            "vertAlign": 'top',
            "color": 'rgba(171, 71, 188, 0.7)',
            "text": 'Volume',
        }
    },
    {
        "width": 600,
        "height": 200,
        "layout": {
            "background": {
                "type": "solid",
                "color": 'white'
            },
            "textColor": "black"
        },
        "timeScale": {
            "visible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'left',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.7)',
            "text": 'MACD',
        }
    }
]

seriesCandlestickChart = [
    {
        "type": 'Candlestick',
        "data": candles,
        "options": {
            "upColor": COLOR_BULL,
            "downColor": COLOR_BEAR,
            "borderVisible": False,
            "wickUpColor": COLOR_BULL,
            "wickDownColor": COLOR_BEAR
        }
    }
]

seriesVolumeChart = [
    {
        "type": 'Histogram',
        "data": volume,
        "options": {
            "priceFormat": {
                "type": 'volume',
            },
            "priceScaleId": "" # set as an overlay setting,
        },
        "priceScale": {
            "scaleMargins": {
                "top": 0,
                "bottom": 0,
            },
            "alignLabels": False
        }
    }
]

seriesMACDchart = [
    {
        "type": 'Line',
        "data": macd_fast,
        "options": {
            "color": 'blue',
            "lineWidth": 2
        }
    },
    {
        "type": 'Line',
        "data": macd_slow,
        "options": {
            "color": 'green',
            "lineWidth": 2
        }
    },
    {
        "type": 'Histogram',
        "data": macd_hist,
        "options": {
            # "color": 'red',
            "lineWidth": 1
        }
    }
]

st.subheader("Multipane Chart (intraday) from CSV")

renderLightweightCharts([
    {
        "chart": chartMultipaneOptions[0],
        "series": seriesCandlestickChart
    },
    {
        "chart": chartMultipaneOptions[1],
        "series": seriesVolumeChart
    },
    {
        "chart": chartMultipaneOptions[2],
        "series": seriesMACDchart
    }
], 'multipane')
```
---
<br />

# Basic charts

![Line Chart](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/LineChart.png?raw=true)

```python
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

seriesLineChart = [{
    "type": 'Line',
    "data": [
        { "time": '2018-12-22', "value": 32.51 },
        { "time": '2018-12-23', "value": 31.11 },
        { "time": '2018-12-24', "value": 27.02 },
        { "time": '2018-12-25', "value": 27.32 },
        { "time": '2018-12-26', "value": 25.17 },
        { "time": '2018-12-27', "value": 28.89 },
        { "time": '2018-12-28', "value": 25.46 },
        { "time": '2018-12-29', "value": 23.92 },
        { "time": '2018-12-30', "value": 22.68 },
        { "time": '2018-12-31', "value": 22.67 },
    ],
    "options": {}
}]

st.subheader("Line Chart with Watermark")

renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesLineChart
    }
], 'line')
```
---
<br />

![Area Chart](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/AreaChart.png?raw=true)

```python
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

seriesAreaChart = [{
    "type": 'Area',
    "data": [
        { "time": '2018-12-22', "value": 32.51 },
        { "time": '2018-12-23', "value": 31.11 },
        { "time": '2018-12-24', "value": 27.02 },
        { "time": '2018-12-25', "value": 27.32 },
        { "time": '2018-12-26', "value": 25.17 },
        { "time": '2018-12-27', "value": 28.89 },
        { "time": '2018-12-28', "value": 25.46 },
        { "time": '2018-12-29', "value": 23.92 },
        { "time": '2018-12-30', "value": 22.68 },
        { "time": '2018-12-31', "value": 22.67 },
    ],
    "options": {}
}]

st.subheader("Area Chart with Watermark")
renderLightweightCharts( [
    {
        "chart": chartOptions,
        "series": seriesAreaChart,
    }
], 'area')
```
---
<br />

![Histogram Chart](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/HistogramChart.png?raw=true)

```python
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

seriesHistogramChart = [{
    "type": 'Histogram',
    "data": [
        { "value": 1, "time": 1642425322 },
        { "value": 8, "time": 1642511722 },
        { "value": 10, "time": 1642598122 },
        { "value": 20, "time": 1642684522 },
        { "value": 3, "time": 1642770922, "color": 'red' },
        { "value": 43, "time": 1642857322 },
        { "value": 41, "time": 1642943722, "color": 'red' },
        { "value": 43, "time": 1643030122 },
        { "value": 56, "time": 1643116522 },
        { "value": 46, "time": 1643202922, "color": 'red' }
    ],
    "options": { "color": '#26a69a' }
}]

st.subheader("Histogram Chart with Watermark")

renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesHistogramChart
    }
], 'histogram')
```
---
<br />

![Bar Chart](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/BarChart.png?raw=true)

```python
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

seriesBarChart = [{
    "type": 'Bar',
    "data": [
        { "open": 10, "high": 10.63, "low": 9.49, "close": 9.55, "time": 1642427876 },
        { "open": 9.55, "high": 10.30, "low": 9.42, "close": 9.94, "time": 1642514276 },
        { "open": 9.94, "high": 10.17, "low": 9.92, "close": 9.78, "time": 1642600676 },
        { "open": 9.78, "high": 10.59, "low": 9.18, "close": 9.51, "time": 1642687076 },
        { "open": 9.51, "high": 10.46, "low": 9.10, "close": 10.17, "time": 1642773476 },
        { "open": 10.17, "high": 10.96, "low": 10.16, "close": 10.47, "time": 1642859876 },
        { "open": 10.47, "high": 11.39, "low": 10.40, "close": 10.81, "time": 1642946276 },
        { "open": 10.81, "high": 11.60, "low": 10.30, "close": 10.75, "time": 1643032676 },
        { "open": 10.75, "high": 11.60, "low": 10.49, "close": 10.93, "time": 1643119076 },
        { "open": 10.93, "high": 11.53, "low": 10.76, "close": 10.96, "time": 1643205476 }
    ],
    "options": {
        "upColor": '#26a69a',
        "downColor": '#ef5350'
    }
}]

st.subheader("Bar Chart with Watermark")
renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesBarChart
    }
], 'bar')
```
---
<br />

![Candlestick Chart](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/CandlestickChart.png?raw=true)

```python
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

seriesCandlestickChart = [{
    "type": 'Candlestick',
    "data": [
        { "open": 10, "high": 10.63, "low": 9.49, "close": 9.55, "time": 1642427876 },
        { "open": 9.55, "high": 10.30, "low": 9.42, "close": 9.94, "time": 1642514276 },
        { "open": 9.94, "high": 10.17, "low": 9.92, "close": 9.78, "time": 1642600676 },
        { "open": 9.78, "high": 10.59, "low": 9.18, "close": 9.51, "time": 1642687076 },
        { "open": 9.51, "high": 10.46, "low": 9.10, "close": 10.17, "time": 1642773476 },
        { "open": 10.17, "high": 10.96, "low": 10.16, "close": 10.47, "time": 1642859876 },
        { "open": 10.47, "high": 11.39, "low": 10.40, "close": 10.81, "time": 1642946276 },
        { "open": 10.81, "high": 11.60, "low": 10.30, "close": 10.75, "time": 1643032676 },
        { "open": 10.75, "high": 11.60, "low": 10.49, "close": 10.93, "time": 1643119076 },
        { "open": 10.93, "high": 11.53, "low": 10.76, "close": 10.96, "time": 1643205476 }
    ],
    "options": {
        "upColor": '#26a69a',
        "downColor": '#ef5350',
        "borderVisible": False,
        "wickUpColor": '#26a69a',
        "wickDownColor": '#ef5350'
    }
}]

st.subheader("Candlestick Chart with Watermark")

renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }
], 'candlestick')
```
---
<br />

![Baseline Chart](https://github.com/freyastreamlit/streamlit-lightweight-charts/blob/main/examples/BaselineChart.png?raw=true)

```python
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

seriesBaselineChart = [{
    "type": 'Baseline',
    "data": [
        { "value": 1, "time": 1642425322 },
        { "value": 8, "time": 1642511722 },
        { "value": 10, "time": 1642598122 },
        { "value": 20, "time": 1642684522 },
        { "value": 3, "time": 1642770922 },
        { "value": 43, "time": 1642857322 },
        { "value": 41, "time": 1642943722 },
        { "value": 43, "time": 1643030122 },
        { "value": 56, "time": 1643116522 },
        { "value": 46, "time": 1643202922 }
    ],
    "options": {
        "baseValue": { "type": "price", "price": 25 },
        "topLineColor": 'rgba( 38, 166, 154, 1)',
        "topFillColor1": 'rgba( 38, 166, 154, 0.28)',
        "topFillColor2": 'rgba( 38, 166, 154, 0.05)',
        "bottomLineColor": 'rgba( 239, 83, 80, 1)',
        "bottomFillColor1": 'rgba( 239, 83, 80, 0.05)',
        "bottomFillColor2": 'rgba( 239, 83, 80, 0.28)'
    }
}]

st.subheader("Baseline Chart with Watermark")

renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesBaselineChart
    }
], 'baseline')
```
---
<br />

## Range Switcher Example

Add professional time range switching to any chart, similar to TradingView:

```python
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample data
def generate_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*2)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    current_price = 100
    
    for date in date_range:
        change = np.random.normal(0, 0.015)
        current_price *= (1 + change)
        
        high = current_price * (1 + abs(np.random.normal(0, 0.008)))
        low = current_price * (1 - abs(np.random.normal(0, 0.008)))
        open_price = current_price * (1 + np.random.normal(0, 0.004))
        close_price = current_price
        
        high = max(high, open_price, close_price)
        low = min(low, open_price, close_price)
        
        data.append({
            'time': date.strftime('%Y-%m-%d'),
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close_price, 2),
        })
        
        current_price = close_price
    
    return data

# Generate data
data = generate_data()

# Chart configuration with range switcher
chart_options = {
    "width": 800,
    "height": 400,
    "layout": {
        "background": {"type": "solid", "color": "white"},
        "textColor": "black",
    },
    "grid": {
        "vertLines": {"color": "rgba(197, 203, 206, 0.5)"},
        "horzLines": {"color": "rgba(197, 203, 206, 0.5)"},
    },
    "crosshair": {"mode": 1},
    "rightPriceScale": {
        "borderColor": "rgba(197, 203, 206, 0.8)",
        "scaleMargins": {"top": 0.1, "bottom": 0.2},
    },
    "timeScale": {
        "borderColor": "rgba(197, 203, 206, 0.8)",
        "timeVisible": True,
        "secondsVisible": False,
    },
    # Range switcher configuration
    "rangeSwitcher": {
        "ranges": [
            {"label": "1D", "seconds": 86400},
            {"label": "1W", "seconds": 604800},
            {"label": "1M", "seconds": 2592000},
            {"label": "3M", "seconds": 7776000},
            {"label": "6M", "seconds": 15552000},
            {"label": "1Y", "seconds": 31536000},
            {"label": "ALL", "seconds": None}
        ],
        "position": "top-right",
        "visible": True,
        "defaultRange": "1M"
    }
}

# Series configuration
candlestick_series = [
    {
        "type": "Candlestick",
        "data": data,
        "options": {
            "upColor": "#26a69a",
            "downColor": "#ef5350",
            "borderVisible": False,
            "wickUpColor": "#26a69a",
            "wickDownColor": "#ef5350",
        },
    }
]

# Render the chart
st.subheader("📈 Chart with Range Switcher")
st.markdown("Use the buttons in the top-right corner to switch between different time ranges.")

chart_config = [
    {
        "chart": chart_options,
        "series": candlestick_series,
    }
]

renderLightweightCharts(chart_config, key="range_switcher_example")
```

**Range Switcher Features:**
- **Professional Styling**: Matches TradingView's design with proper fonts, colors, and spacing
- **Active State Management**: Visual feedback for the currently selected range
- **Hover Effects**: Smooth transitions and hover states for better UX
- **Flexible Positioning**: Can be positioned in any corner of the chart
- **Customizable Ranges**: Easy to add or modify time ranges
- **Callback Support**: Ready for event handling and integration

**Available Time Ranges:**
- **1D**: Last 24 hours
- **1W**: Last 7 days
- **1M**: Last 30 days
- **3M**: Last 90 days
- **6M**: Last 180 days
- **1Y**: Last 365 days
- **ALL**: Show all available data
