"""
Unit tests for BackgroundData class.

This module contains comprehensive unit tests for the BackgroundData class,
testing data construction, validation, serialization, and edge cases.
"""

import pandas as pd
import pytest
from datetime import datetime

from streamlit_lightweight_charts_pro.data.background_data import BackgroundData


class TestBackgroundDataConstruction:
    """Test BackgroundData construction and initialization."""
    
    def test_basic_construction(self):
        """Test basic BackgroundData construction with required fields."""
        data = BackgroundData(time="2024-01-01", value=0.5)
        
        assert data.value == 0.5
        assert data.minColor == "#FFFFFF"
        assert data.maxColor == "#2196F3"
        assert isinstance(data.time, (int, str))
    
    def test_construction_with_custom_colors(self):
        """Test BackgroundData construction with custom colors."""
        data = BackgroundData(
            time="2024-01-01",
            value=0.75,
            minColor="#FF0000",
            maxColor="#00FF00"
        )
        
        assert data.value == 0.75
        assert data.minColor == "#FF0000"
        assert data.maxColor == "#00FF00"
    
    def test_construction_with_timestamp(self):
        """Test BackgroundData construction with timestamp."""
        timestamp = 1704067200
        data = BackgroundData(time=timestamp, value=0.3)
        
        assert data.time == timestamp
        assert data.value == 0.3
    
    def test_construction_with_datetime(self):
        """Test BackgroundData construction with datetime object."""
        dt = datetime(2024, 1, 1, 10, 0, 0)
        data = BackgroundData(time=dt, value=0.6)
        
        assert isinstance(data.time, (int, str))
        assert data.value == 0.6


class TestBackgroundDataValidation:
    """Test BackgroundData validation."""
    
    def test_invalid_min_color(self):
        """Test BackgroundData with invalid minColor."""
        with pytest.raises(ValueError, match="Invalid minColor format"):
            BackgroundData(
                time="2024-01-01",
                value=0.5,
                minColor="invalid_color"
            )
    
    def test_invalid_max_color(self):
        """Test BackgroundData with invalid maxColor."""
        with pytest.raises(ValueError, match="Invalid maxColor format"):
            BackgroundData(
                time="2024-01-01",
                value=0.5,
                maxColor="not_a_color"
            )
    
    def test_rgba_colors(self):
        """Test BackgroundData with rgba colors."""
        data = BackgroundData(
            time="2024-01-01",
            value=0.5,
            minColor="rgba(255, 0, 0, 0.5)",
            maxColor="rgba(0, 255, 0, 0.8)"
        )
        
        assert data.minColor == "rgba(255, 0, 0, 0.5)"
        assert data.maxColor == "rgba(0, 255, 0, 0.8)"
    
    def test_hex_colors_with_hash(self):
        """Test BackgroundData with hex colors including hash."""
        data = BackgroundData(
            time="2024-01-01",
            value=0.5,
            minColor="#FF0000",
            maxColor="#00FF00"
        )
        
        assert data.minColor == "#FF0000"
        assert data.maxColor == "#00FF00"


class TestBackgroundDataSerialization:
    """Test BackgroundData serialization."""
    
    def test_to_dict_basic(self):
        """Test basic to_dict conversion."""
        data = BackgroundData(time="2024-01-01", value=0.5)
        result = data.to_dict()
        
        assert "time" in result
        assert result["value"] == 0.5
        assert result["minColor"] == "#FFFFFF"
        assert result["maxColor"] == "#2196F3"
    
    def test_to_dict_with_custom_colors(self):
        """Test to_dict with custom colors."""
        data = BackgroundData(
            time="2024-01-01",
            value=0.75,
            minColor="#FF0000",
            maxColor="#00FF00"
        )
        result = data.to_dict()
        
        assert result["value"] == 0.75
        assert result["minColor"] == "#FF0000"
        assert result["maxColor"] == "#00FF00"
    
    def test_to_dict_preserves_all_fields(self):
        """Test that to_dict preserves all fields."""
        data = BackgroundData(
            time=1704067200,
            value=0.9,
            minColor="#123456",
            maxColor="#ABCDEF"
        )
        result = data.to_dict()
        
        assert result["time"] == 1704067200
        assert result["value"] == 0.9
        assert result["minColor"] == "#123456"
        assert result["maxColor"] == "#ABCDEF"


class TestBackgroundDataProperties:
    """Test BackgroundData properties."""
    
    def test_required_columns(self):
        """Test required_columns property."""
        data = BackgroundData(time="2024-01-01", value=0.5)
        required = data.required_columns
        
        assert "time" in required
        assert "value" in required
        assert "minColor" in required
        assert "maxColor" in required
    
    def test_optional_columns(self):
        """Test optional_columns property."""
        data = BackgroundData(time="2024-01-01", value=0.5)
        optional = data.optional_columns
        
        # BackgroundData has no additional optional columns
        assert isinstance(optional, set)


class TestBackgroundDataEdgeCases:
    """Test BackgroundData edge cases."""
    
    def test_extreme_values(self):
        """Test BackgroundData with extreme values."""
        # Value below 0
        data1 = BackgroundData(time="2024-01-01", value=-0.5)
        assert data1.value == -0.5
        
        # Value above 1
        data2 = BackgroundData(time="2024-01-01", value=1.5)
        assert data2.value == 1.5
        
        # Very large value
        data3 = BackgroundData(time="2024-01-01", value=1000000)
        assert data3.value == 1000000
    
    def test_zero_value(self):
        """Test BackgroundData with zero value."""
        data = BackgroundData(time="2024-01-01", value=0)
        assert data.value == 0
    
    def test_same_min_max_colors(self):
        """Test BackgroundData with same min and max colors."""
        data = BackgroundData(
            time="2024-01-01",
            value=0.5,
            minColor="#FF0000",
            maxColor="#FF0000"
        )
        
        assert data.minColor == "#FF0000"
        assert data.maxColor == "#FF0000"
    
    def test_pandas_timestamp(self):
        """Test BackgroundData with pandas timestamp."""
        ts = pd.Timestamp("2024-01-01 10:00:00")
        data = BackgroundData(time=ts, value=0.7)
        
        assert isinstance(data.time, (int, str))
        assert data.value == 0.7


class TestBackgroundDataIntegration:
    """Test BackgroundData integration scenarios."""
    
    def test_dataframe_compatibility(self):
        """Test BackgroundData compatibility with DataFrame operations."""
        # Create multiple data points
        data_points = [
            BackgroundData("2024-01-01", 0.2, "#FF0000", "#00FF00"),
            BackgroundData("2024-01-02", 0.5, "#FF0000", "#00FF00"),
            BackgroundData("2024-01-03", 0.8, "#FF0000", "#00FF00"),
        ]
        
        # Convert to dictionaries
        dicts = [d.to_dict() for d in data_points]
        
        # Create DataFrame
        df = pd.DataFrame(dicts)
        
        assert len(df) == 3
        assert "time" in df.columns
        assert "value" in df.columns
        assert "minColor" in df.columns
        assert "maxColor" in df.columns
    
    def test_serialization_roundtrip(self):
        """Test serialization roundtrip."""
        original = BackgroundData(
            time="2024-01-01",
            value=0.65,
            minColor="#123456",
            maxColor="#FEDCBA"
        )
        
        # Serialize
        serialized = original.to_dict()
        
        # Create new instance from serialized data
        # Note: We need to handle time conversion
        new_data = BackgroundData(
            time=serialized["time"],
            value=serialized["value"],
            minColor=serialized["minColor"],
            maxColor=serialized["maxColor"]
        )
        
        assert new_data.value == original.value
        assert new_data.minColor == original.minColor
        assert new_data.maxColor == original.maxColor