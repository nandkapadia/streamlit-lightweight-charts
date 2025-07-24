import numpy as np
import pandas as pd
import streamlit as st

from streamlit_lightweight_charts_pro import Chart
from streamlit_lightweight_charts_pro.charts.series import AreaSeries
from streamlit_lightweight_charts_pro.type_definitions import ColumnNames

st.title("Price and Volume Series Chart sample")

# Generate synthetic OHLC and volume data
dates = pd.date_range(start="2023-03-01", end="2024-05-31", freq="B")
np.random.seed(42)
prices = np.cumsum(np.random.normal(0, 0.5, len(dates))) + 58
opens = prices + np.random.normal(0, 0.2, len(dates))
highs = np.maximum(opens, prices) + np.random.uniform(0, 0.5, len(dates))
lows = np.minimum(opens, prices) - np.random.uniform(0, 0.5, len(dates))
volumes = np.random.randint(1_000_000, 3_500_000, len(dates))

price_df = pd.DataFrame(
    {
        ColumnNames.DATETIME.value: dates,
        ColumnNames.OPEN.value: opens,
        ColumnNames.HIGH.value: highs,
        ColumnNames.LOW.value: lows,
        ColumnNames.CLOSE.value: prices,
        "volume": volumes,
    }
)

# Step 1: Convert to DataFrame
sma_df = pd.DataFrame({"datetime": dates, "volume": volumes})

# Step 2: Calculate SMA
sma_df["volume_sma"] = sma_df["volume"].rolling(window=14).mean()

# Drop the 'volume' column from sma_df
sma_df = sma_df.drop(columns=["volume"])

chart = Chart.from_price_volume_dataframe(price_df)

area_series = AreaSeries(
    data=sma_df, column_mapping={"datetime": "datetime", "value": "volume_sma"}
)
area_series.pane_id = 1
area_series.overlay = False

chart.add_series(area_series)

chart.render()
