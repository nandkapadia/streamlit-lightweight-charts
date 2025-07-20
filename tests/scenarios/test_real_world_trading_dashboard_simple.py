"""Simplified real-world trading dashboard tests that work with the actual API."""

from datetime import datetime, timedelta

import numpy as np

from streamlit_lightweight_charts_pro.charts.multi_pane_chart import MultiPaneChart
from streamlit_lightweight_charts_pro.charts.price_volume_chart import PriceVolumeChart
from streamlit_lightweight_charts_pro.charts.series import (
    AreaSeries,
    HistogramSeries,
    LineSeries,
)
from streamlit_lightweight_charts_pro.charts.single_pane_chart import SinglePaneChart
from streamlit_lightweight_charts_pro.data import (
    HistogramData,
    OhlcData,
    SingleValueData,
)


class TestRealWorldTradingDashboardSimple:
    """Test real-world trading dashboard scenarios with simplified API usage."""

    def setup_method(self):
        """Set up test data for trading scenarios."""
        # Generate realistic trading data
        self.start_date = datetime(2024, 1, 1)
        self.days = 50  # Reduced for faster testing
        
        # Generate price data with realistic patterns
        np.random.seed(42)  # For reproducible tests
        self.price_data = self._generate_price_data()
        self.volume_data = self._generate_realistic_volume_data()
        
        # Calculate technical indicators
        self.sma_data = self._calculate_sma(self.price_data, period=10)
        self.rsi_data = self._calculate_rsi(self.price_data, period=14)

    def _generate_price_data(self):
        """Generate realistic OHLC price data."""
        dates = [self.start_date + timedelta(days=i) for i in range(self.days)]
        
        # Start with a base price
        base_price = 100.0
        prices = []
        
        for i in range(self.days):
            # Add trend component
            trend = 0.1 * i  # Gradual uptrend
            
            # Add volatility component
            volatility = 2.0
            noise = np.random.normal(0, volatility)
            
            # Add some cyclical patterns
            cycle = 5 * np.sin(2 * np.pi * i / 20)
            
            close_price = base_price + trend + noise + cycle
            
            # Generate OHLC from close price
            high = close_price + abs(np.random.normal(0, 1.5))
            low = close_price - abs(np.random.normal(0, 1.5))
            open_price = close_price + np.random.normal(0, 0.5)
            
            # Ensure OHLC relationship
            high = max(high, open_price, close_price)
            low = min(low, open_price, close_price)
            
            prices.append(
                OhlcData(
                time=dates[i].strftime("%Y-%m-%d"),
                    open_=round(open_price, 2),  # Use open_ instead of open
                high=round(high, 2),
                low=round(low, 2),
                    close=round(close_price, 2),
                )
            )
        
        return prices

    def _generate_realistic_volume_data(self):
        """Generate realistic volume data correlated with price movements."""
        volumes = []
        
        for i, price in enumerate(self.price_data):
            # Base volume
            base_volume = 1000000
            
            # Volume increases with price volatility
            price_change = abs(price.close - price.open)
            volatility_factor = 1 + (price_change / 10)
            
            # Add some randomness
            random_factor = np.random.uniform(0.5, 1.5)
            
            volume = int(base_volume * volatility_factor * random_factor)
            volumes.append(
                HistogramData(
                time=price.time,
                value=volume,
                    color="#26a69a" if price.close >= price.open else "#ef5350",
                )
            )
        
        return volumes

    def _calculate_sma(self, price_data, period=10):
        """Calculate Simple Moving Average."""
        sma_data = []
        
        for i in range(len(price_data)):
            if i < period - 1:
                sma_data.append(None)
            else:
                # Calculate SMA for the period
                prices = [price_data[j].close for j in range(i - period + 1, i + 1)]
                sma = sum(prices) / period
                sma_data.append(SingleValueData(time=price_data[i].time, value=round(sma, 2)))
        
        return [data for data in sma_data if data is not None]

    def _calculate_rsi(self, price_data, period=14):
        """Calculate Relative Strength Index."""
        rsi_data = []
        gains = []
        losses = []
        
        for i in range(1, len(price_data)):
            change = price_data[i].close - price_data[i - 1].close
            gains.append(max(change, 0))
            losses.append(max(-change, 0))
        
        for i in range(len(price_data)):
            if i < period:
                rsi_data.append(None)
            else:
                avg_gain = sum(gains[i - period : i]) / period
                avg_loss = sum(losses[i - period : i]) / period
                
                if avg_loss == 0:
                    rsi = 100
                else:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))
                
                rsi_data.append(SingleValueData(time=price_data[i].time, value=round(rsi, 2)))
        
        return [data for data in rsi_data if data is not None]

    def test_tradingview_equivalent_dashboard(self):
        """Test building a TradingView equivalent multi-panel trading dashboard."""
        # Create main price chart with volume - remove volume_data parameter
        price_volume_chart = PriceVolumeChart(
            data=self.price_data
            # volume_data parameter removed - not supported by PriceVolumeChart
        )
        
        # Create technical indicators
        sma_20 = self._calculate_sma(self.price_data, 20)
        sma_50 = self._calculate_sma(self.price_data, 50)
        
        # Create SMA chart
        sma_chart = SinglePaneChart(
            series=[
                LineSeries(data=sma_20, color="#2196F3", line_width=2),
                LineSeries(data=sma_50, color="#FF9800", line_width=2),
            ]
        )

        # Create RSI chart
        rsi_data = self._calculate_rsi(self.price_data, 14)
        rsi_chart = SinglePaneChart(
            series=[LineSeries(data=rsi_data, color="#9C27B0", line_width=2)]
        )
        
        # Create multi-pane dashboard
        dashboard = MultiPaneChart(charts=[price_volume_chart, sma_chart, rsi_chart])
        
        # Generate configuration
        config = dashboard.to_frontend_config()
        
        # Verify configuration
        assert "charts" in config
        assert len(config["charts"]) == 3

    def test_equity_curve_analysis(self):
        """Test building an equity curve analysis dashboard."""
        # Generate equity curve data
        equity_curve_data = self._generate_equity_curve_data()
        
        # Create equity curve chart - use top_color and bottom_color instead of fill_color
        equity_chart = SinglePaneChart(
            series=[
            AreaSeries(
                data=equity_curve_data,
                    top_color="#4CAF50",  # Use top_color instead of fill_color
                    bottom_color="#4CAF50",  # Use bottom_color instead of fill_color
                    line_color="#4CAF50",
                )
            ]
        )
        
        # Create drawdown chart
        drawdown_data = self._calculate_drawdown(equity_curve_data)
        drawdown_chart = SinglePaneChart(
            series=[
                AreaSeries(
            data=drawdown_data,
                    top_color="#f44336",  # Use top_color instead of fill_color
                    bottom_color="#f44336",  # Use bottom_color instead of fill_color
                    line_color="#f44336",
                )
            ]
        )
        
        # Create multi-pane dashboard
        dashboard = MultiPaneChart(charts=[equity_chart, drawdown_chart])
        
        # Generate configuration
        config = dashboard.to_frontend_config()
        
        # Verify configuration
        assert "charts" in config
        assert len(config["charts"]) == 2

    def _generate_equity_curve_data(self):
        """Generate realistic equity curve data from trading performance."""
        # Simulate trading performance
        initial_capital = 100000
        current_capital = initial_capital
        equity_curve = []
        
        for i, price in enumerate(self.price_data):
            # Simulate daily P&L
            if i > 0:
                # Random trading performance
                daily_return = np.random.normal(0.001, 0.02)  # 0.1% mean, 2% std
                current_capital *= 1 + daily_return
            
            equity_curve.append(SingleValueData(time=price.time, value=round(current_capital, 2)))
        
        return equity_curve

    def _calculate_benchmark_performance(self):
        """Calculate 60/40 benchmark performance."""
        # Simple 60/40 benchmark (60% stocks, 40% bonds)
        benchmark_returns = []
        
        for i in range(self.days):
            stock_return = np.random.normal(0.0008, 0.015)  # 0.08% mean, 1.5% std
            bond_return = np.random.normal(0.0003, 0.005)  # 0.03% mean, 0.5% std
            
            benchmark_return = stock_return * 0.6 + bond_return * 0.4
            benchmark_returns.append(benchmark_return)
        
        # Calculate cumulative benchmark performance
        benchmark_values = []
        cumulative_return = 1.0
        initial_value = 100000
        
        for i, daily_return in enumerate(benchmark_returns):
            cumulative_return *= 1 + daily_return
            benchmark_value = initial_value * cumulative_return
            date = self.start_date + timedelta(days=i)
            
            benchmark_values.append(
                SingleValueData(time=date.strftime("%Y-%m-%d"), value=round(benchmark_value, 2))
            )
        
        return benchmark_values

    def _calculate_drawdown(self, equity_data):
        """Calculate drawdown from equity curve."""
        drawdown_data = []
        peak = equity_data[0].value
        
        for data_point in equity_data:
            if data_point.value > peak:
                peak = data_point.value
            
            drawdown = ((data_point.value - peak) / peak) * 100
            drawdown_data.append(SingleValueData(time=data_point.time, value=drawdown))
        
        return drawdown_data

    def test_portfolio_analysis_dashboard(self):
        """Test building a portfolio analysis dashboard."""
        # Generate portfolio data for multiple assets
        portfolio_data = self._generate_portfolio_data()
        
        # Create portfolio performance chart
        portfolio_performance = self._calculate_portfolio_performance(portfolio_data)
        
        performance_chart = SinglePaneChart(
            series=[LineSeries(data=portfolio_performance, color="#2196F3", line_width=2)]
            )
        
        # Add benchmark comparison
        benchmark_data = self._calculate_benchmark_performance()
        performance_chart.add_series(LineSeries(data=benchmark_data, color="#FF9800", line_width=2))
        
        # Create asset allocation chart
        allocation_data = self._create_allocation_data(portfolio_data)
        allocation_chart = SinglePaneChart(
            series=[HistogramSeries(data=allocation_data, color="#4CAF50")]
            )
        
        # Create multi-pane dashboard
        dashboard = MultiPaneChart(charts=[performance_chart, allocation_chart])
        
        # Generate configuration
        config = dashboard.to_frontend_config()
        
        # Verify configuration - updated to match nested structure
        assert "charts" in config
        assert len(config["charts"]) == 2
        
        # Verify performance chart - series are nested inside charts[0]['charts'][0]['series']
        perf_chart = config["charts"][0]
        assert "charts" in perf_chart
        assert len(perf_chart["charts"]) == 1
        perf_chart_inner = perf_chart["charts"][0]
        assert "series" in perf_chart_inner
        assert len(perf_chart_inner["series"]) == 2  # Portfolio + Benchmark

    def _generate_portfolio_data(self):
        """Generate realistic multi-asset portfolio data."""
        # Define asset classes and their characteristics
        assets = {
            "US_Stocks": {"volatility": 0.15, "return": 0.08, "weight": 0.40},
            "Intl_Stocks": {"volatility": 0.18, "return": 0.06, "weight": 0.25},
            "Bonds": {"volatility": 0.05, "return": 0.03, "weight": 0.20},
            "Real_Estate": {"volatility": 0.12, "return": 0.05, "weight": 0.10},
            "Commodities": {"volatility": 0.20, "return": 0.04, "weight": 0.05},
        }
        
        portfolio_data = {}
        
        for asset_name, characteristics in assets.items():
            # Generate daily returns
            daily_returns = np.random.normal(
                characteristics["return"] / 252,  # Daily return
                characteristics["volatility"] / np.sqrt(252),  # Daily volatility
                self.days,
            )
            
            # Calculate cumulative returns
            cumulative_returns = np.cumprod(1 + daily_returns)
            
            # Generate price series starting at 100
            prices = 100 * cumulative_returns
            
            # Create data objects
            asset_data = []
            for i, price in enumerate(prices):
                date = self.start_date + timedelta(days=i)
                asset_data.append(
                    SingleValueData(time=date.strftime("%Y-%m-%d"), value=round(price, 2))
                )
            
            portfolio_data[asset_name] = {
                "data": asset_data,
                "weight": characteristics["weight"],
                "daily_returns": daily_returns,
            }
        
        return portfolio_data

    def _calculate_portfolio_performance(self, portfolio_data):
        """Calculate portfolio performance over time."""
        portfolio_values = []
        initial_value = 100000  # Starting portfolio value
        
        cumulative_return = 1.0
        for i in range(self.days):
            if i > 0:
                daily_return = 0
                for asset_name, asset_info in portfolio_data.items():
                    daily_return += asset_info["daily_returns"][i] * asset_info["weight"]
                cumulative_return *= 1 + daily_return
            
            portfolio_value = initial_value * cumulative_return
            date = self.start_date + timedelta(days=i)
            
            portfolio_values.append(
                SingleValueData(time=date.strftime("%Y-%m-%d"), value=round(portfolio_value, 2))
            )
        
        return portfolio_values

    def _create_allocation_data(self, portfolio_data):
        """Create asset allocation data for visualization."""
        allocation_data = []
        
        for asset_name, asset_info in portfolio_data.items():
            allocation_data.append(
                SingleValueData(
                time=asset_name,  # Use asset name as time for bar chart
                    value=asset_info["weight"] * 100,  # Convert to percentage
                )
            )
        
        return allocation_data

    def test_trading_dashboard_performance(self):
        """Test trading dashboard performance with large datasets."""
        # Generate larger dataset for performance testing
        large_days = 200  # Reduced for faster testing
        large_price_data = self._generate_large_price_data(large_days)
        self._generate_large_volume_data(large_price_data)
        
        # Create dashboard with large dataset - remove volume_data parameter
        dashboard = MultiPaneChart(
            charts=[
                PriceVolumeChart(data=large_price_data),  # Remove volume_data parameter
            SinglePaneChart(series=[LineSeries(self._calculate_sma(large_price_data, 20))]),
                SinglePaneChart(series=[LineSeries(self._calculate_rsi(large_price_data, 14))]),
            ]
        )
        
        # Test performance
        import time

        start_time = time.time()
        config = dashboard.to_frontend_config()
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 10.0
        
        # Verify large dataset was processed
        assert "charts" in config
        assert len(config["charts"]) == 3

    def _generate_large_price_data(self, days):
        """Generate large price dataset for performance testing."""
        dates = [self.start_date + timedelta(days=i) for i in range(days)]
        
        base_price = 100.0
        prices = []
        
        for i in range(days):
            # Simplified price generation for performance testing
            daily_return = np.random.normal(0.0005, 0.015)  # 0.05% daily return, 1.5% volatility
            if i == 0:
                cumulative_return = 1.0
            else:
                cumulative_return *= 1 + daily_return
            
            close_price = base_price * cumulative_return
            
            # Generate simple OHLC
            high = close_price * (1 + abs(np.random.normal(0, 0.01)))
            low = close_price * (1 - abs(np.random.normal(0, 0.01)))
            open_price = close_price * (1 + np.random.normal(0, 0.005))
            
            prices.append(
                OhlcData(
                time=dates[i].strftime("%Y-%m-%d"),
                open_=round(open_price, 2),
                high=round(high, 2),
                low=round(low, 2),
                    close=round(close_price, 2),
                )
            )
        
        return prices

    def _generate_large_volume_data(self, price_data):
        """Generate large volume dataset for performance testing."""
        volumes = []
        
        for price in price_data:
            # Simplified volume generation
            base_volume = 1000000
            random_factor = np.random.uniform(0.5, 1.5)
            volume = int(base_volume * random_factor)
            
            volumes.append(
                HistogramData(
                time=price.time,
                value=volume,
                    color="#26a69a" if price.close >= price.open else "#ef5350",
                )
            )
        
        return volumes

    def test_trading_dashboard_integration_workflow(self):
        """Test complete trading dashboard integration workflow."""
        # Simulate real trading workflow
        # 1. Load market data
        market_data = self.price_data
        volume_data = self.volume_data
        
        # 2. Calculate technical indicators
        sma_20 = self._calculate_sma(market_data, 20)
        rsi = self._calculate_rsi(market_data, 14)
        
        # 3. Generate trading signals
        signals = self._generate_trading_signals(market_data, sma_20, rsi)
        
        # 4. Create comprehensive dashboard
        dashboard = self._create_comprehensive_dashboard(
            market_data, volume_data, sma_20, rsi, signals
        )
        
        # 5. Generate final configuration
        config = dashboard.to_frontend_config()
        
        # Verify complete workflow - updated to match nested structure
        assert "charts" in config
        assert len(config["charts"]) >= 2  # Price, indicators
        
        # Verify all components are present - series are nested inside 
        # charts[0]['charts'][0]['series']
        price_chart = config["charts"][0]
        assert "charts" in price_chart
        assert len(price_chart["charts"]) == 1
        price_chart_inner = price_chart["charts"][0]
        assert "series" in price_chart_inner
        assert len(price_chart_inner["series"]) >= 1  # At least candlestick series

    def _generate_trading_signals(self, price_data, sma_20, rsi):
        """Generate trading signals based on technical indicators."""
        signals = []
        
        for i, price in enumerate(price_data):
            if i < 20:  # Need enough data for indicators
                continue
                
            # Find corresponding indicator values
            sma_20_val = next((item.value for item in sma_20 if item.time == price.time), None)
            rsi_val = next((item.value for item in rsi if item.time == price.time), None)
            
            if sma_20_val and rsi_val:
                # Simple signal logic - create signal strength as a value
                signal_strength = 0
                if price.close > sma_20_val and rsi_val < 70:
                    signal_strength = 1  # Buy signal
                elif price.close < sma_20_val and rsi_val > 30:
                    signal_strength = -1  # Sell signal

                # Only add signals when there's a signal
                if signal_strength != 0:
                    signals.append(SingleValueData(time=price.time, value=signal_strength))
        
        return signals

    def _create_comprehensive_dashboard(self, price_data, volume_data, sma_20, rsi, signals):
        """Create a comprehensive trading dashboard."""
        # Create price chart - remove volume_data parameter
        price_chart = PriceVolumeChart(data=price_data)  # Remove volume_data parameter

        # Create SMA chart
        sma_chart = SinglePaneChart(series=[LineSeries(data=sma_20, color="#2196F3", line_width=2)])

        # Create RSI chart
        rsi_chart = SinglePaneChart(series=[LineSeries(data=rsi, color="#9C27B0", line_width=2)])
        
        # Create signals chart - only if signals exist
        if signals:
            signals_chart = SinglePaneChart(
                series=[LineSeries(data=signals, color="#f44336", line_width=2)]
            )

            # Create multi-pane dashboard with signals
            dashboard = MultiPaneChart(charts=[price_chart, sma_chart, rsi_chart, signals_chart])
        else:
            # Create multi-pane dashboard without signals
            dashboard = MultiPaneChart(charts=[price_chart, sma_chart, rsi_chart])

        return dashboard
