"""
Performance tests for PriceVolumeChart class.
"""

import pytest
import pandas as pd
import numpy as np
import time
import psutil
import os
import gc
from unittest.mock import patch, MagicMock

from streamlit_lightweight_charts_pro.charts.price_volume_chart import PriceVolumeChart


class TestPriceVolumeChartPerformance:
    """Performance test cases for PriceVolumeChart class."""

    def setup_method(self):
        """Set up test data."""
        # Create base dataset for performance testing
        self.base_dates = pd.date_range("2020-01-01", periods=100, freq="D")
        np.random.seed(42)

        self.base_prices = [100.0]
        for _ in range(99):
            self.base_prices.append(self.base_prices[-1] * (1 + np.random.normal(0, 0.02)))

        self.base_df = pd.DataFrame(
            {
                "datetime": self.base_dates,
                "open": self.base_prices,
                "high": [p * (1 + abs(np.random.normal(0, 0.01))) for p in self.base_prices],
                "low": [p * (1 - abs(np.random.normal(0, 0.01))) for p in self.base_prices],
                "close": [p * (1 + np.random.normal(0, 0.005)) for p in self.base_prices],
                "volume": np.random.randint(1000, 10000, 100),
            }
        )

        # Ensure data integrity
        self.base_df["high"] = self.base_df[["open", "close", "high"]].max(axis=1)
        self.base_df["low"] = self.base_df[["open", "close", "low"]].min(axis=1)

    def create_large_dataset(self, size):
        """Create a large dataset of specified size."""
        dates = pd.date_range("2020-01-01", periods=size, freq="D")
        np.random.seed(42)

        prices = [100.0]
        for _ in range(size - 1):
            prices.append(prices[-1] * (1 + np.random.normal(0, 0.02)))

        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": prices,
                "high": [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                "low": [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                "close": [p * (1 + np.random.normal(0, 0.005)) for p in prices],
                "volume": np.random.randint(1000, 10000, size),
            }
        )

        # Ensure data integrity
        df["high"] = df[["open", "close", "high"]].max(axis=1)
        df["low"] = df[["open", "close", "low"]].min(axis=1)

        return df

    def test_chart_creation_performance(self):
        """Test chart creation performance with different dataset sizes."""
        sizes = [100, 500, 1000, 5000, 10000]
        creation_times = {}

        for size in sizes:
            df = self.create_large_dataset(size)

            # Measure creation time
            start_time = time.time()
            chart = PriceVolumeChart(data=df)
            creation_time = time.time() - start_time

            creation_times[size] = creation_time

            # Verify chart was created correctly
            assert chart.has_volume() is True
            assert len(chart.series) == 2
            assert len(chart.get_candlestick_series().data) == size
            assert len(chart.get_volume_series().data) == size

        # Performance assertions
        assert creation_times[100] < 0.1  # Small dataset: < 100ms
        assert creation_times[500] < 0.2  # Medium dataset: < 200ms
        assert creation_times[1000] < 0.5  # Large dataset: < 500ms
        assert creation_times[5000] < 1.0  # Very large dataset: < 1s
        assert creation_times[10000] < 2.0  # Huge dataset: < 2s

    def test_configuration_generation_performance(self):
        """Test configuration generation performance."""
        sizes = [100, 500, 1000, 5000]
        config_times = {}

        for size in sizes:
            df = self.create_large_dataset(size)
            chart = PriceVolumeChart(data=df)

            # Measure configuration generation time
            start_time = time.time()
            config = chart.to_frontend_config()
            config_time = time.time() - start_time

            config_times[size] = config_time

            # Verify configuration was generated correctly
            assert "series" in config
            assert "options" in config
            assert len(config["series"]) == 2
            assert len(config["series"][0]["data"]) == size
            assert len(config["series"][1]["data"]) == size

        # Performance assertions
        assert config_times[100] < 0.05  # Small dataset: < 50ms
        assert config_times[500] < 0.1  # Medium dataset: < 100ms
        assert config_times[1000] < 0.2  # Large dataset: < 200ms
        assert config_times[5000] < 0.5  # Very large dataset: < 500ms

    def test_memory_usage_performance(self):
        """Test memory usage performance."""
        sizes = [100, 500, 1000, 5000]
        memory_usage = {}

        process = psutil.Process(os.getpid())

        for size in sizes:
            # Get initial memory
            gc.collect()
            initial_memory = process.memory_info().rss

            # Create chart
            df = self.create_large_dataset(size)
            chart = PriceVolumeChart(data=df)

            # Generate configuration
            config = chart.to_frontend_config()

            # Get final memory
            final_memory = process.memory_info().rss
            memory_increase = final_memory - initial_memory

            memory_usage[size] = memory_increase

            # Clean up
            del chart, config, df
            gc.collect()

        # Memory usage assertions (should be reasonable)
        assert memory_usage[100] < 10 * 1024 * 1024  # < 10MB for 100 points
        assert memory_usage[500] < 20 * 1024 * 1024  # < 20MB for 500 points
        assert memory_usage[1000] < 40 * 1024 * 1024  # < 40MB for 1000 points
        assert memory_usage[5000] < 100 * 1024 * 1024  # < 100MB for 5000 points

    def test_concurrent_chart_creation_performance(self):
        """Test performance when creating multiple charts concurrently."""
        import threading
        import queue

        def create_chart_thread(data, result_queue, thread_id):
            try:
                start_time = time.time()
                chart = PriceVolumeChart(data=data)
                config = chart.to_frontend_config()
                end_time = time.time()

                result_queue.put((thread_id, end_time - start_time, True))
            except Exception as e:
                result_queue.put((thread_id, 0, False, str(e)))

        # Test with different numbers of concurrent threads
        thread_counts = [1, 2, 4, 8]
        results = {}

        for thread_count in thread_counts:
            df = self.create_large_dataset(500)  # Use medium dataset
            result_queue = queue.Queue()
            threads = []

            # Create threads
            for i in range(thread_count):
                thread = threading.Thread(target=create_chart_thread, args=(df, result_queue, i))
                threads.append(thread)

            # Start all threads
            start_time = time.time()
            for thread in threads:
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            total_time = time.time() - start_time

            # Collect results
            thread_results = []
            while not result_queue.empty():
                thread_results.append(result_queue.get())

            results[thread_count] = {
                "total_time": total_time,
                "thread_results": thread_results,
                "success_count": sum(1 for r in thread_results if r[2]),
            }

        # Verify all threads succeeded
        for thread_count, result in results.items():
            assert result["success_count"] == thread_count
            assert result["total_time"] < thread_count * 1.0  # Should scale reasonably

    def test_dynamic_updates_performance(self):
        """Test performance of dynamic updates."""
        chart = PriceVolumeChart(data=self.base_df)

        # Test volume alpha updates
        alpha_update_times = []
        for alpha in np.linspace(0.1, 1.0, 10):
            start_time = time.time()
            chart.update_volume_alpha(alpha)
            update_time = time.time() - start_time
            alpha_update_times.append(update_time)

        # Test volume color updates
        color_update_times = []
        colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF"]
        for color in colors:
            start_time = time.time()
            chart.update_volume_color(color, 0.8)
            update_time = time.time() - start_time
            color_update_times.append(update_time)

        # Performance assertions
        assert max(alpha_update_times) < 0.01  # Alpha updates should be very fast
        assert max(color_update_times) < 0.01  # Color updates should be very fast

    def test_large_dataset_scalability(self):
        """Test scalability with very large datasets."""
        sizes = [10000, 20000, 50000]
        performance_metrics = {}

        for size in sizes:
            df = self.create_large_dataset(size)

            # Measure creation time
            start_time = time.time()
            chart = PriceVolumeChart(data=df)
            creation_time = time.time() - start_time

            # Measure configuration generation time
            start_time = time.time()
            config = chart.to_frontend_config()
            config_time = time.time() - start_time

            # Measure memory usage
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss
            memory_usage = initial_memory

            performance_metrics[size] = {
                "creation_time": creation_time,
                "config_time": config_time,
                "memory_usage": memory_usage,
                "data_points": size,
            }

            # Verify chart works correctly
            assert chart.has_volume() is True
            assert len(chart.get_candlestick_series().data) == size
            assert len(chart.get_volume_series().data) == size

            # Clean up
            del chart, config, df
            gc.collect()

        # Scalability assertions
        for size, metrics in performance_metrics.items():
            # Creation time should scale reasonably
            assert metrics["creation_time"] < size / 1000  # Roughly linear scaling

            # Configuration time should be reasonable
            assert metrics["config_time"] < 1.0  # Should be under 1 second

            # Memory usage should be reasonable
            assert metrics["memory_usage"] < size * 1024  # Roughly 1KB per data point

    def test_repeated_operations_performance(self):
        """Test performance of repeated operations."""
        chart = PriceVolumeChart(data=self.base_df)

        # Test repeated configuration generation
        config_times = []
        for _ in range(100):
            start_time = time.time()
            config = chart.to_frontend_config()
            config_time = time.time() - start_time
            config_times.append(config_time)

        # Test repeated volume updates
        update_times = []
        for i in range(100):
            start_time = time.time()
            chart.update_volume_alpha(i / 100)
            update_time = time.time() - start_time
            update_times.append(update_time)

        # Performance assertions
        assert max(config_times) < 0.1  # Configuration generation should be consistent
        assert max(update_times) < 0.01  # Updates should be very fast
        assert np.mean(config_times) < 0.05  # Average should be reasonable

    def test_memory_leak_performance(self):
        """Test for memory leaks during repeated operations."""
        process = psutil.Process(os.getpid())

        # Get initial memory
        gc.collect()
        initial_memory = process.memory_info().rss

        # Perform repeated operations
        for i in range(50):
            df = self.create_large_dataset(1000)
            chart = PriceVolumeChart(data=df)
            config = chart.to_frontend_config()

            # Update chart multiple times
            for j in range(10):
                chart.update_volume_alpha(j / 10)
                chart.update_volume_color(f"#{j:02x}0000", 0.8)

            # Clean up
            del chart, config, df
            gc.collect()

        # Get final memory
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be minimal (no significant leaks)
        assert memory_increase < 50 * 1024 * 1024  # Less than 50MB increase

    def test_cpu_usage_performance(self):
        """Test CPU usage during chart operations."""
        import psutil

        process = psutil.Process(os.getpid())

        # Get initial CPU usage
        initial_cpu_percent = process.cpu_percent()

        # Perform intensive operations
        for i in range(10):
            df = self.create_large_dataset(5000)
            chart = PriceVolumeChart(data=df)
            config = chart.to_frontend_config()

            # Perform updates
            for j in range(20):
                chart.update_volume_alpha(j / 20)
                chart.update_volume_color(f"#{j:02x}0000", 0.8)

            del chart, config, df
            gc.collect()

        # Get final CPU usage
        final_cpu_percent = process.cpu_percent()

        # CPU usage should be reasonable
        # Note: This is a rough test as CPU usage can vary significantly
        assert final_cpu_percent < 100  # Should not use 100% CPU

    def test_io_performance(self):
        """Test I/O performance when working with data."""
        import tempfile
        import os

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            # Write large dataset to CSV
            large_df = self.create_large_dataset(10000)
            large_df.to_csv(f.name, index=False)

        try:
            # Measure reading time
            start_time = time.time()
            df = pd.read_csv(f.name)
            read_time = time.time() - start_time

            # Measure chart creation time
            start_time = time.time()
            chart = PriceVolumeChart(data=df)
            chart_time = time.time() - start_time

            # Performance assertions
            assert read_time < 1.0  # Reading should be fast
            assert chart_time < 2.0  # Chart creation should be reasonable

            # Verify chart works
            assert chart.has_volume() is True
            assert len(chart.get_candlestick_series().data) == 10000

        finally:
            # Clean up
            os.unlink(f.name)

    def test_network_performance_simulation(self):
        """Test performance when simulating network-like conditions."""
        # Simulate network delay by adding artificial delays
        import time

        def delayed_operation(operation, delay=0.001):
            time.sleep(delay)
            return operation()

        chart = PriceVolumeChart(data=self.base_df)

        # Test operations with simulated network delays
        start_time = time.time()

        for i in range(100):
            delayed_operation(lambda: chart.update_volume_alpha(i / 100))
            delayed_operation(lambda: chart.to_frontend_config())

        total_time = time.time() - start_time

        # Total time should be reasonable even with delays
        assert total_time < 1.0  # Should complete in under 1 second

    def test_garbage_collection_performance(self):
        """Test performance impact of garbage collection."""
        import gc

        # Disable garbage collection
        gc.disable()

        # Create many charts
        charts = []
        start_time = time.time()

        for i in range(100):
            df = self.create_large_dataset(1000)
            chart = PriceVolumeChart(data=df)
            charts.append(chart)

        creation_time_without_gc = time.time() - start_time

        # Clean up
        del charts
        gc.collect()

        # Enable garbage collection
        gc.enable()

        # Create many charts with GC enabled
        charts = []
        start_time = time.time()

        for i in range(100):
            df = self.create_large_dataset(1000)
            chart = PriceVolumeChart(data=df)
            charts.append(chart)

        creation_time_with_gc = time.time() - start_time

        # Clean up
        del charts
        gc.collect()

        # Performance should be reasonable in both cases
        assert creation_time_without_gc < 10.0  # Without GC
        assert creation_time_with_gc < 15.0  # With GC (may be slightly slower)
