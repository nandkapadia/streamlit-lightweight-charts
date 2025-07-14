"""Utility functions for converting pandas DataFrames to chart data."""

from typing import List, Optional, Union, Dict, Any
import pandas as pd
from ..data import (
    SingleValueData, OhlcData, HistogramData, BaselineData
)


def df_to_line_data(
    df: pd.DataFrame,
    value_column: str = 'close',
    time_column: Optional[str] = None
) -> List[SingleValueData]:
    """
    Convert a pandas DataFrame to line chart data.
    
    Args:
        df: DataFrame with data
        value_column: Column name for values
        time_column: Column name for time (if None, uses index)
        
    Returns:
        List of SingleValueData points
    """
    data = []
    
    if time_column is None:
        # Use index as time
        for timestamp, row in df.iterrows():
            data.append(SingleValueData(
                time=timestamp,
                value=row[value_column]
            ))
    else:
        # Use specified column as time
        for _, row in df.iterrows():
            data.append(SingleValueData(
                time=row[time_column],
                value=row[value_column]
            ))
    
    return data


def df_to_ohlc_data(
    df: pd.DataFrame,
    open_column: str = 'open',
    high_column: str = 'high',
    low_column: str = 'low',
    close_column: str = 'close',
    time_column: Optional[str] = None
) -> List[OhlcData]:
    """
    Convert a pandas DataFrame to OHLC chart data.
    
    Args:
        df: DataFrame with OHLC data
        open_column: Column name for open prices
        high_column: Column name for high prices
        low_column: Column name for low prices
        close_column: Column name for close prices
        time_column: Column name for time (if None, uses index)
        
    Returns:
        List of OhlcData points
    """
    data = []
    
    if time_column is None:
        # Use index as time
        for timestamp, row in df.iterrows():
            data.append(OhlcData(
                time=timestamp,
                open=row[open_column],
                high=row[high_column],
                low=row[low_column],
                close=row[close_column]
            ))
    else:
        # Use specified column as time
        for _, row in df.iterrows():
            data.append(OhlcData(
                time=row[time_column],
                open=row[open_column],
                high=row[high_column],
                low=row[low_column],
                close=row[close_column]
            ))
    
    return data


def df_to_histogram_data(
    df: pd.DataFrame,
    value_column: str = 'volume',
    color_column: Optional[str] = None,
    time_column: Optional[str] = None,
    positive_color: str = '#26a69a',
    negative_color: str = '#ef5350'
) -> List[HistogramData]:
    """
    Convert a pandas DataFrame to histogram chart data.
    
    Args:
        df: DataFrame with data
        value_column: Column name for values
        color_column: Column name for colors (optional)
        time_column: Column name for time (if None, uses index)
        positive_color: Color for positive values (if color_column not specified)
        negative_color: Color for negative values (if color_column not specified)
        
    Returns:
        List of HistogramData points
    """
    data = []
    
    if time_column is None:
        # Use index as time
        for timestamp, row in df.iterrows():
            value = row[value_column]
            
            # Determine color
            if color_column is not None:
                color = row[color_column]
            else:
                color = positive_color if value >= 0 else negative_color
            
            data.append(HistogramData(
                time=timestamp,
                value=value,
                color=color
            ))
    else:
        # Use specified column as time
        for _, row in df.iterrows():
            value = row[value_column]
            
            # Determine color
            if color_column is not None:
                color = row[color_column]
            else:
                color = positive_color if value >= 0 else negative_color
            
            data.append(HistogramData(
                time=row[time_column],
                value=value,
                color=color
            ))
    
    return data


def df_to_baseline_data(
    df: pd.DataFrame,
    value_column: str = 'value',
    time_column: Optional[str] = None
) -> List[BaselineData]:
    """
    Convert a pandas DataFrame to baseline chart data.
    
    Args:
        df: DataFrame with data
        value_column: Column name for values
        time_column: Column name for time (if None, uses index)
        
    Returns:
        List of BaselineData points
    """
    data = []
    
    if time_column is None:
        # Use index as time
        for timestamp, row in df.iterrows():
            data.append(BaselineData(
                time=timestamp,
                value=row[value_column]
            ))
    else:
        # Use specified column as time
        for _, row in df.iterrows():
            data.append(BaselineData(
                time=row[time_column],
                value=row[value_column]
            ))
    
    return data


def resample_df_for_charts(
    df: pd.DataFrame,
    freq: str,
    agg_dict: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    """
    Resample a DataFrame to a different frequency for charting.
    
    Args:
        df: DataFrame with datetime index
        freq: Resampling frequency (e.g., '1D', '1H', '5T')
        agg_dict: Dictionary of aggregation functions for each column
                  Default is to use OHLC for numeric columns
        
    Returns:
        Resampled DataFrame
    """
    if agg_dict is None:
        # Default aggregation for common columns
        agg_dict = {}
        
        if 'open' in df.columns:
            agg_dict['open'] = 'first'
        if 'high' in df.columns:
            agg_dict['high'] = 'max'
        if 'low' in df.columns:
            agg_dict['low'] = 'min'
        if 'close' in df.columns:
            agg_dict['close'] = 'last'
        if 'volume' in df.columns:
            agg_dict['volume'] = 'sum'
        
        # For other numeric columns, use mean
        for col in df.select_dtypes(include=['number']).columns:
            if col not in agg_dict:
                agg_dict[col] = 'mean'
    
    return df.resample(freq).agg(agg_dict)


def df_to_data(
    df: pd.DataFrame,
    chart_type: str,
    **kwargs
) -> Union[List[SingleValueData], List[OhlcData], List[HistogramData], List[BaselineData]]:
    """
    Convert DataFrame to appropriate data type based on chart type.
    
    Args:
        df: DataFrame with data
        chart_type: Type of chart ('line', 'area', 'candlestick', 'bar', 'histogram', 'baseline')
        **kwargs: Additional arguments passed to specific converter functions
        
    Returns:
        List of appropriate data points
    """
    chart_type = chart_type.lower()
    
    if chart_type in ['line', 'area']:
        return df_to_line_data(df, **kwargs)
    elif chart_type in ['candlestick', 'bar']:
        return df_to_ohlc_data(df, **kwargs)
    elif chart_type == 'histogram':
        return df_to_histogram_data(df, **kwargs)
    elif chart_type == 'baseline':
        return df_to_baseline_data(df, **kwargs)
    else:
        raise ValueError(f"Unknown chart type: {chart_type}")