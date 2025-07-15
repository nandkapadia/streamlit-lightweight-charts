# Enhanced Trade Visualization & Annotation System Guide

## Overview

The streamlit-lightweight-charts package now includes comprehensive enhanced features for trade visualization and annotation systems. These features provide powerful tools for financial analysis, trading strategy visualization, and chart annotation.

## Table of Contents

1. [Enhanced Trade Visualization](#enhanced-trade-visualization)
2. [Annotation System](#annotation-system)
3. [Frontend Implementation](#frontend-implementation)
4. [Usage Examples](#usage-examples)
5. [API Reference](#api-reference)
6. [Best Practices](#best-practices)

## Enhanced Trade Visualization

### Features

- **6 Visualization Styles**: markers, rectangles, both, lines, arrows, zones
- **Automatic P&L Calculation**: Profit/loss calculation with percentage
- **Custom Tooltips**: Rich trade information on hover
- **Color Coding**: Different colors for long/short, profit/loss
- **Trade Metadata**: ID, notes, quantity, trade type
- **Interactive Elements**: Click handlers and hover effects

### Trade Configuration

```python
from streamlit_lightweight_charts import TradeConfig, TradeVisualizationOptions

# Create a trade with full configuration
trade = TradeConfig(
    entryTime='2024-01-05',
    entryPrice=102.50,
    exitTime='2024-01-12',
    exitPrice=105.75,
    quantity=100,
    tradeType='long',  # 'long' or 'short'
    id='T001',
    notes='Breakout trade on earnings announcement',
    text='P&L: +$325 (+3.17%)'  # Custom tooltip text
)

# P&L is automatically calculated
print(f"P&L: ${trade.pnl:,.0f}")
print(f"P&L %: {trade.pnlPercentage:.2f}%")
print(f"Profitable: {trade.isProfitable}")
```

### Visualization Options

```python
# Configure trade visualization
trade_options = TradeVisualizationOptions(
    style='markers',  # 'markers', 'rectangles', 'both', 'lines', 'arrows', 'zones'
    
    # Marker options
    entryMarkerColorLong='#2196F3',
    entryMarkerColorShort='#FF9800',
    exitMarkerColorProfit='#4CAF50',
    exitMarkerColorLoss='#F44336',
    markerSize=2,
    showPnlInMarkers=True,
    
    # Rectangle options
    rectangleFillOpacity=0.2,
    rectangleBorderWidth=1,
    rectangleColorProfit='#4CAF50',
    rectangleColorLoss='#F44336',
    
    # Line options
    lineWidth=2,
    lineStyle='dashed',  # 'solid', 'dotted', 'dashed', 'large_dashed', 'sparse_dotted'
    lineColorProfit='#4CAF50',
    lineColorLoss='#F44336',
    
    # Arrow options
    arrowSize=10,
    arrowColorProfit='#4CAF50',
    arrowColorLoss='#F44336',
    
    # Zone options
    zoneOpacity=0.1,
    zoneColorLong='#2196F3',
    zoneColorShort='#FF9800',
    zoneExtendBars=5,
    
    # Annotation options
    showTradeId=True,
    showQuantity=True,
    showTradeType=True,
    annotationFontSize=12,
    annotationBackground='rgba(255, 255, 255, 0.8)'
)
```

### Visualization Styles

#### 1. Markers Style
- Entry and exit markers with arrows
- Color-coded by trade type and profitability
- Customizable size and text

#### 2. Rectangles Style
- Rectangular overlays showing trade duration
- Color-coded by profitability
- Adjustable opacity and border

#### 3. Both Style
- Combines markers and rectangles
- Maximum visual information

#### 4. Lines Style
- Trend lines connecting entry to exit
- Different line styles available
- Color-coded by profitability

#### 5. Arrows Style
- Arrow annotations pointing from entry to exit
- Size and color customization
- P&L percentage display

#### 6. Zones Style
- Extended rectangular zones around trade periods
- Useful for showing trade context
- Extendable beyond exact entry/exit times

## Annotation System

### Features

- **6 Annotation Types**: text, arrow, shape, line, rectangle, circle
- **Annotation Layers**: Organize annotations into visible/invisible layers
- **Rich Styling**: Colors, fonts, borders, opacity
- **Tooltips**: Hover information for annotations
- **Positioning**: Above, below, or inline positioning

### Annotation Types

```python
from streamlit_lightweight_charts import Annotation, createAnnotationLayer

# Text annotation
text_annotation = Annotation(
    time='2024-01-10',
    price=104.50,
    text='Earnings Report',
    type='text',
    position='above',
    backgroundColor='rgba(255, 193, 7, 0.9)',
    textColor='#000000',
    fontSize=12,
    tooltip='Q4 2023 earnings exceeded expectations'
)

# Arrow annotation
arrow_annotation = Annotation(
    time='2024-01-15',
    price=103.80,
    text='Breakout',
    type='arrow',
    position='above',
    color='#2196F3',
    fontSize=14,
    tooltip='Price broke above resistance level'
)

# Shape annotation
shape_annotation = Annotation(
    time='2024-02-01',
    price=105.20,
    text='RSI Divergence',
    type='shape',
    position='inline',
    backgroundColor='rgba(255, 152, 0, 0.3)',
    borderColor='#FF9800',
    fontSize=10,
    tooltip='Bearish RSI divergence detected'
)

# Line annotation
line_annotation = Annotation(
    time='2024-01-25',
    price=104.80,
    text='Trend Line',
    type='line',
    position='inline',
    color='#9C27B0',
    borderWidth=2,
    tooltip='Major trend line support'
)

# Rectangle annotation
rectangle_annotation = Annotation(
    time='2024-02-10',
    price=107.50,
    text='Consolidation',
    type='rectangle',
    position='inline',
    backgroundColor='rgba(156, 39, 176, 0.2)',
    borderColor='#9C27B0',
    fontSize=10,
    tooltip='Price consolidation zone'
)

# Circle annotation
circle_annotation = Annotation(
    time='2024-02-15',
    price=108.20,
    text='Target',
    type='circle',
    position='above',
    backgroundColor='rgba(244, 67, 54, 0.3)',
    borderColor='#F44336',
    fontSize=8,
    tooltip='Price target reached'
)
```

### Annotation Layers

```python
# Create annotation layers
technical_layer = createAnnotationLayer(
    name="Technical Analysis",
    annotations=[
        text_annotation,
        arrow_annotation
    ]
)

fundamental_layer = createAnnotationLayer(
    name="Fundamental Events",
    annotations=[
        shape_annotation,
        line_annotation
    ]
)

# Layers can be controlled independently
technical_layer.visible = True
technical_layer.opacity = 0.8

fundamental_layer.visible = False
fundamental_layer.opacity = 1.0
```

## Frontend Implementation

### TypeScript Interfaces

The frontend includes comprehensive TypeScript interfaces for type safety:

```typescript
// Trade Configuration
interface TradeConfig {
  entryTime: string
  entryPrice: number
  exitTime: string
  exitPrice: number
  quantity: number
  tradeType: 'long' | 'short'
  id?: string
  notes?: string
  text?: string
  pnl?: number
  pnlPercentage?: number
  isProfitable?: boolean
}

// Trade Visualization Options
interface TradeVisualizationOptions {
  style: 'markers' | 'rectangles' | 'both' | 'lines' | 'arrows' | 'zones'
  // ... extensive configuration options
}

// Annotation System
interface Annotation {
  time: string
  price: number
  text: string
  type: 'text' | 'arrow' | 'shape' | 'line' | 'rectangle' | 'circle'
  position: 'above' | 'below' | 'inline'
  // ... styling options
}

interface AnnotationLayer {
  name: string
  annotations: Annotation[]
  visible: boolean
  opacity: number
}
```

### Utility Functions

#### Trade Visualization
```typescript
import { createTradeVisualElements } from './tradeVisualization'

const visualElements = createTradeVisualElements(
  trades,
  options,
  chartData
)

// Returns: { markers, shapes, annotations }
```

#### Annotation System
```typescript
import { createAnnotationVisualElements } from './annotationSystem'

const visualElements = createAnnotationVisualElements(
  annotations,
  layers
)

// Returns: { markers, shapes, texts }
```

## Usage Examples

### Basic Trade Visualization

```python
import streamlit as st
from streamlit_lightweight_charts import (
    renderLightweightCharts, TradeConfig, TradeVisualizationOptions
)

# Create trades
trades = [
    TradeConfig(
        entryTime='2024-01-05',
        entryPrice=102.50,
        exitTime='2024-01-12',
        exitPrice=105.75,
        quantity=100,
        tradeType='long',
        id='T001'
    )
]

# Configure visualization
trade_options = TradeVisualizationOptions(
    style='markers',
    showPnlInMarkers=True,
    showTradeId=True
)

# Add to series
series_config = SeriesConfig(
    type='Candlestick',
    data=price_data,
    trades=trades,
    tradeVisualizationOptions=trade_options
)
```

### Advanced Annotation System

```python
# Create annotations
annotations = [
    Annotation(
        time='2024-01-10',
        price=104.50,
        text='Earnings Report',
        type='text',
        position='above',
        backgroundColor='rgba(255, 193, 7, 0.9)',
        tooltip='Q4 2023 earnings exceeded expectations'
    )
]

# Create layers
layers = [
    createAnnotationLayer(
        name="Technical Analysis",
        annotations=technical_annotations
    ),
    createAnnotationLayer(
        name="Fundamental Events",
        annotations=fundamental_annotations
    )
]

# Add to chart
chart_config = ChartConfig(
    series=[series_config],
    annotations=annotations,
    annotationLayers=layers
)
```

### Interactive Controls

```python
# Sidebar controls for trade visualization
trade_style = st.sidebar.selectbox(
    "Trade Style",
    ['markers', 'rectangles', 'both', 'lines', 'arrows', 'zones']
)

entry_color = st.sidebar.color_picker("Entry Color", "#2196F3")
exit_color = st.sidebar.color_picker("Exit Color", "#4CAF50")

# Layer visibility controls
for layer in annotation_layers:
    layer.visible = st.sidebar.checkbox(f"Show {layer.name}", layer.visible)
    layer.opacity = st.sidebar.slider(f"{layer.name} Opacity", 0.0, 1.0, layer.opacity)
```

## API Reference

### TradeConfig

| Parameter | Type | Description |
|-----------|------|-------------|
| entryTime | str | Entry timestamp |
| entryPrice | float | Entry price |
| exitTime | str | Exit timestamp |
| exitPrice | float | Exit price |
| quantity | int | Trade quantity |
| tradeType | str | 'long' or 'short' |
| id | str | Trade identifier |
| notes | str | Trade notes |
| text | str | Custom tooltip text |

### TradeVisualizationOptions

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| style | str | 'markers' | Visualization style |
| entryMarkerColorLong | str | '#2196F3' | Long entry marker color |
| entryMarkerColorShort | str | '#FF9800' | Short entry marker color |
| exitMarkerColorProfit | str | '#4CAF50' | Profitable exit color |
| exitMarkerColorLoss | str | '#F44336' | Loss exit color |
| markerSize | int | 2 | Marker size |
| showPnlInMarkers | bool | False | Show P&L in markers |
| rectangleFillOpacity | float | 0.2 | Rectangle fill opacity |
| showTradeId | bool | False | Show trade ID |
| showQuantity | bool | False | Show quantity |
| showTradeType | bool | False | Show trade type |

### Annotation

| Parameter | Type | Description |
|-----------|------|-------------|
| time | str | Annotation timestamp |
| price | float | Annotation price level |
| text | str | Annotation text |
| type | str | Annotation type |
| position | str | Position relative to price |
| color | str | Annotation color |
| backgroundColor | str | Background color |
| fontSize | int | Font size |
| tooltip | str | Hover tooltip |

## Best Practices

### Trade Visualization

1. **Choose Appropriate Style**: Use markers for quick overview, rectangles for detailed analysis
2. **Color Consistency**: Maintain consistent color schemes across charts
3. **Information Density**: Don't overcrowd charts with too many trades
4. **Tooltip Content**: Include relevant trade information in tooltips
5. **Performance**: Limit the number of trades for large datasets

### Annotation System

1. **Layer Organization**: Group related annotations into layers
2. **Visual Hierarchy**: Use different annotation types for different importance levels
3. **Color Coding**: Use consistent colors for similar annotation types
4. **Tooltip Information**: Provide meaningful information in tooltips
5. **Opacity Management**: Use opacity to show/hide annotation layers

### Performance Considerations

1. **Data Size**: Limit annotations and trades for large datasets
2. **Layer Management**: Disable unused annotation layers
3. **Update Frequency**: Batch updates when possible
4. **Memory Usage**: Clean up unused annotations and trades

### Accessibility

1. **Color Contrast**: Ensure sufficient contrast for text annotations
2. **Tooltip Information**: Provide alternative information for screen readers
3. **Keyboard Navigation**: Support keyboard navigation for interactive elements
4. **Screen Reader Support**: Include descriptive text for visual elements

## Migration Guide

### From Previous Version

If you're upgrading from a previous version:

1. **Trade Configuration**: Update trade objects to use `TradeConfig` class
2. **Visualization Options**: Use `TradeVisualizationOptions` for configuration
3. **Annotation System**: Replace custom annotations with `Annotation` class
4. **Layer Management**: Use `createAnnotationLayer` for layer organization

### Example Migration

```python
# Old way
trade = {
    'entry_time': '2024-01-05',
    'entry_price': 102.50,
    'exit_time': '2024-01-12',
    'exit_price': 105.75,
    'quantity': 100,
    'type': 'long'
}

# New way
trade = TradeConfig(
    entryTime='2024-01-05',
    entryPrice=102.50,
    exitTime='2024-01-12',
    exitPrice=105.75,
    quantity=100,
    tradeType='long'
)
```

## Troubleshooting

### Common Issues

1. **Trades Not Displaying**: Check trade data format and visualization options
2. **Annotations Not Visible**: Verify layer visibility and opacity settings
3. **Performance Issues**: Reduce number of trades/annotations or use layers
4. **Color Issues**: Ensure color values are valid hex codes or rgba strings

### Debug Tips

1. **Console Logging**: Check browser console for JavaScript errors
2. **Data Validation**: Verify trade and annotation data formats
3. **Layer Visibility**: Check layer visibility and opacity settings
4. **Chart Configuration**: Ensure proper chart and series configuration

## Conclusion

The enhanced trade visualization and annotation system provides powerful tools for financial analysis and chart annotation. By following the best practices and using the provided examples, you can create rich, interactive financial charts with comprehensive trade analysis and annotation capabilities.

For more examples and advanced usage, see the `EnhancedTradeVisualizationExample.py` file in the examples directory. 