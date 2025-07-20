"""Portfolio analysis and risk management dashboard tests."""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from streamlit_lightweight_charts_pro.charts.multi_pane_chart import MultiPaneChart
from streamlit_lightweight_charts_pro.charts.series import (
    AreaSeries,
    BarSeries,
    HistogramSeries,
    LineSeries,
)
from streamlit_lightweight_charts_pro.charts.single_pane_chart import SinglePaneChart
from streamlit_lightweight_charts_pro.data import (
    HistogramData,
    SingleValueData,
    create_text_annotation,
)


class TestPortfolioAnalysisDashboard:
    """Test portfolio analysis and risk management dashboard scenarios."""

    def setup_method(self):
        """Set up test data for portfolio analysis."""
        # Generate multi-asset portfolio data
        self.start_date = datetime(2024, 1, 1)
        self.days = 252  # Trading days in a year
        
        # Generate data for multiple assets
        self.portfolio_data = self._generate_portfolio_data()
        self.risk_metrics = self._calculate_risk_metrics()
        self.correlation_matrix = self._calculate_correlation_matrix()
        self.performance_attribution = self._calculate_performance_attribution()

    def _generate_portfolio_data(self):
        """Generate realistic multi-asset portfolio data."""
        np.random.seed(42)  # For reproducible tests
        
        # Define asset classes and their characteristics
        assets = {
            "US_Stocks": {"volatility": 0.15, "return": 0.08, "weight": 0.40},
            "Intl_Stocks": {"volatility": 0.18, "return": 0.06, "weight": 0.25},
            "Bonds": {"volatility": 0.05, "return": 0.03, "weight": 0.20},
            "Real_Estate": {"volatility": 0.12, "return": 0.05, "weight": 0.10},
            "Commodities": {"volatility": 0.20, "return": 0.04, "weight": 0.05},
        }
        
        portfolio_data = {}
        dates = [self.start_date + timedelta(days=i) for i in range(self.days)]
        
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
            for i, (date, price) in enumerate(zip(dates, prices)):
                asset_data.append(
                    SingleValueData(time=date.strftime("%Y-%m-%d"), value=round(price, 2))
                )
            
            portfolio_data[asset_name] = {
                "data": asset_data,
                "weight": characteristics["weight"],
                "daily_returns": daily_returns,
            }
        
        return portfolio_data

    def _calculate_risk_metrics(self):
        """Calculate portfolio risk metrics."""
        # Calculate portfolio returns
        portfolio_returns = []
        dates = [self.start_date + timedelta(days=i) for i in range(self.days)]
        
        for i in range(self.days):
            daily_portfolio_return = 0
            for asset_name, asset_info in self.portfolio_data.items():
                daily_portfolio_return += asset_info["daily_returns"][i] * asset_info["weight"]
            portfolio_returns.append(daily_portfolio_return)
        
        # Calculate risk metrics
        portfolio_returns_array = np.array(portfolio_returns)
        
        # Volatility (annualized)
        volatility = np.std(portfolio_returns_array) * np.sqrt(252)
        
        # Sharpe Ratio (assuming risk-free rate of 2%)
        risk_free_rate = 0.02
        excess_returns = portfolio_returns_array - (risk_free_rate / 252)
        sharpe_ratio = np.mean(excess_returns) / np.std(portfolio_returns_array) * np.sqrt(252)
        
        # Maximum Drawdown
        cumulative_returns = np.cumprod(1 + portfolio_returns_array)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = np.min(drawdown)
        
        # Value at Risk (95% confidence)
        var_95 = np.percentile(portfolio_returns_array, 5)
        
        # Expected Shortfall (Conditional VaR)
        es_95 = np.mean(portfolio_returns_array[portfolio_returns_array <= var_95])
        
        return {
            "volatility": round(volatility * 100, 2),  # Percentage
            "sharpe_ratio": round(sharpe_ratio, 2),
            "max_drawdown": round(max_drawdown * 100, 2),  # Percentage
            "var_95": round(var_95 * 100, 2),  # Percentage
            "expected_shortfall": round(es_95 * 100, 2),  # Percentage
            "daily_returns": portfolio_returns_array,
        }

    def _calculate_correlation_matrix(self):
        """Calculate correlation matrix between assets."""
        asset_returns = {}
        for asset_name, asset_info in self.portfolio_data.items():
            asset_returns[asset_name] = asset_info["daily_returns"]
        
        # Create DataFrame for correlation calculation
        returns_df = pd.DataFrame(asset_returns)
        correlation_matrix = returns_df.corr()
        
        return correlation_matrix

    def _calculate_performance_attribution(self):
        """Calculate performance attribution analysis."""
        # Calculate contribution of each asset to portfolio return
        total_period_return = 0
        asset_contributions = {}
        
        for asset_name, asset_info in self.portfolio_data.items():
            # Calculate asset's total return over the period
            initial_price = asset_info["data"][0].value
            final_price = asset_info["data"][-1].value
            asset_return = (final_price - initial_price) / initial_price
            
            # Calculate contribution to portfolio return
            contribution = asset_return * asset_info["weight"]
            asset_contributions[asset_name] = {
                "return": round(asset_return * 100, 2),
                "contribution": round(contribution * 100, 2),
                "weight": asset_info["weight"],
            }
            
            total_period_return += contribution
        
        return {
            "total_return": round(total_period_return * 100, 2),
            "asset_contributions": asset_contributions,
        }

    def test_portfolio_overview_dashboard(self):
        """Test comprehensive portfolio overview dashboard."""
        # Create portfolio performance chart
        portfolio_performance = self._calculate_portfolio_performance()
        
        performance_chart = SinglePaneChart(
            series=[
            LineSeries(
                data=portfolio_performance,
                color="#2196F3",
                line_width=2,
                    # title parameter removed - not supported by LineSeries
                )
            ]
            )
        
        # Add benchmark comparison (e.g., 60/40 portfolio)
        benchmark_data = self._calculate_benchmark_performance()
        performance_chart.add_series(
            LineSeries(
            data=benchmark_data,
            color="#FF9800",
            line_width=2,
                # title parameter removed - not supported by LineSeries
            )
        )
        
        # Create asset allocation chart
        allocation_data = self._create_allocation_data()
        allocation_chart = SinglePaneChart(
            series=[
            BarSeries(
                data=allocation_data,
                color="#4CAF50",
                    # title parameter removed - not supported by BarSeries
                )
            ]
            )
        
        # Create risk metrics panel
        risk_chart = self._create_risk_metrics_chart()
        
        # Create multi-pane dashboard - use 'charts' parameter, not 'panes'
        dashboard = MultiPaneChart(charts=[performance_chart, allocation_chart, risk_chart])
        
        # Add performance annotations to individual chart instead of dashboard
        total_return = self.performance_attribution["total_return"]
        sharpe_ratio = self.risk_metrics["sharpe_ratio"]
        
        performance_annotation = create_text_annotation(
            portfolio_performance[-1].time,
            portfolio_performance[-1].value * 1.05,
            f"Total Return: {total_return}% | Sharpe: {sharpe_ratio}",
        )
        # Add annotation to the performance chart, not the dashboard
        performance_chart.add_annotation(performance_annotation)
        
        # Generate configuration
        config = dashboard.to_frontend_config()
        
        # Verify configuration - updated to match actual nested structure
        assert "charts" in config
        assert len(config["charts"]) == 3
        
        # Verify performance chart - series are nested inside charts[0]['charts'][0]['series']
        perf_chart = config["charts"][0]
        assert "charts" in perf_chart
        assert len(perf_chart["charts"]) == 1
        perf_chart_inner = perf_chart["charts"][0]
        assert "series" in perf_chart_inner
        assert len(perf_chart_inner["series"]) == 2  # Portfolio + Benchmark
        
        # Verify allocation chart - series are nested inside charts[1]['charts'][0]['series']
        alloc_chart = config["charts"][1]
        assert "charts" in alloc_chart
        assert len(alloc_chart["charts"]) == 1
        alloc_chart_inner = alloc_chart["charts"][0]
        assert "series" in alloc_chart_inner
        assert len(alloc_chart_inner["series"]) == 1  # Asset allocation bars

    def _calculate_portfolio_performance(self):
        """Calculate portfolio performance over time."""
        portfolio_values = []
        initial_value = 100000  # Starting portfolio value
        
        cumulative_return = 1.0
        for i in range(self.days):
            if i > 0:
                daily_return = self.risk_metrics["daily_returns"][i]
                cumulative_return *= 1 + daily_return
            
            portfolio_value = initial_value * cumulative_return
            date = self.start_date + timedelta(days=i)
            
            portfolio_values.append(
                SingleValueData(time=date.strftime("%Y-%m-%d"), value=round(portfolio_value, 2))
            )
        
        return portfolio_values

    def _calculate_benchmark_performance(self):
        """Calculate 60/40 benchmark performance."""
        # Simple 60/40 benchmark (60% stocks, 40% bonds)
        benchmark_returns = []
        
        for i in range(self.days):
            stock_return = (
                self.portfolio_data["US_Stocks"]["daily_returns"][i] * 0.6
                + self.portfolio_data["Intl_Stocks"]["daily_returns"][i] * 0.6
            ) / 2  # Average of US and International stocks
            
            bond_return = self.portfolio_data["Bonds"]["daily_returns"][i]
            
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

    def _create_allocation_data(self):
        """Create asset allocation data for visualization."""
        allocation_data = []
        
        for asset_name, asset_info in self.portfolio_data.items():
            allocation_data.append(
                SingleValueData(
                time=asset_name,  # Use asset name as time for bar chart
                    value=asset_info["weight"] * 100,  # Convert to percentage
                )
            )
        
        return allocation_data

    def _create_risk_metrics_chart(self):
        """Create risk metrics visualization chart."""
        # Create rolling volatility chart
        rolling_volatility = self._calculate_rolling_volatility()
        
        risk_chart = SinglePaneChart(series=[LineSeries(data=rolling_volatility, color="#f44336")])
        
        # Add volatility bands
        high_vol_band = [SingleValueData(item.time, 20) for item in rolling_volatility]
        low_vol_band = [SingleValueData(item.time, 10) for item in rolling_volatility]
        
        risk_chart.add_series(LineSeries(high_vol_band, color="#ff9800", line_style="dashed"))
        risk_chart.add_series(LineSeries(low_vol_band, color="#4caf50", line_style="dashed"))
        
        return risk_chart

    def _calculate_rolling_volatility(self, window=30):
        """Calculate rolling volatility."""
        rolling_vol = []
        
        for i in range(window, len(self.risk_metrics["daily_returns"])):
            window_returns = self.risk_metrics["daily_returns"][i - window : i]
            vol = np.std(window_returns) * np.sqrt(252) * 100  # Annualized percentage
            
            date = self.start_date + timedelta(days=i)
            rolling_vol.append(SingleValueData(time=date.strftime("%Y-%m-%d"), value=round(vol, 2)))
        
        return rolling_vol

    def test_risk_analysis_dashboard(self):
        """Test comprehensive risk analysis dashboard."""
        # Create drawdown analysis
        drawdown_data = self._calculate_drawdown_analysis()
        
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
        
        # Create return distribution histogram
        return_distribution = self._create_return_distribution()
        
        dist_chart = SinglePaneChart(
            series=[HistogramSeries(data=return_distribution, color="#2196F3")]
            )
        
        # Create correlation heatmap data
        correlation_data = self._create_correlation_heatmap_data()
        
        corr_chart = SinglePaneChart(series=[BarSeries(data=correlation_data, color="#4CAF50")])
        
        # Create multi-pane risk dashboard - use 'charts' parameter, not 'panes'
        risk_dashboard = MultiPaneChart(charts=[drawdown_chart, dist_chart, corr_chart])
        
        # Add risk metrics annotations to individual chart instead of dashboard
        var_annotation = create_text_annotation(
            drawdown_data[-1].time,
            drawdown_data[-1].value * 0.8,
            f"VaR (95%): {self.risk_metrics['var_95']}% | "
            f"Max DD: {self.risk_metrics['max_drawdown']}%",
        )
        # Add annotation to the drawdown chart, not the dashboard
        drawdown_chart.add_annotation(var_annotation)
        
        # Generate configuration
        config = risk_dashboard.to_frontend_config()
        
        # Verify configuration
        assert "charts" in config
        assert len(config["charts"]) == 3

    def _calculate_drawdown_analysis(self):
        """Calculate portfolio drawdown analysis."""
        portfolio_values = self._calculate_portfolio_performance()
        drawdown_data = []
        
        peak = portfolio_values[0].value
        
        for data_point in portfolio_values:
            if data_point.value > peak:
                peak = data_point.value
            
            drawdown = ((data_point.value - peak) / peak) * 100
            drawdown_data.append(SingleValueData(time=data_point.time, value=drawdown))
        
        return drawdown_data

    def _create_return_distribution(self):
        """Create return distribution histogram data."""
        returns = self.risk_metrics["daily_returns"] * 100  # Convert to percentage
        
        # Create histogram bins
        bins = np.linspace(returns.min(), returns.max(), 20)
        hist, bin_edges = np.histogram(returns, bins=bins)
        
        distribution_data = []
        for i, count in enumerate(hist):
            if count > 0:  # Only include non-zero bins
                bin_center = (bin_edges[i] + bin_edges[i + 1]) / 2
                distribution_data.append(HistogramData(time=f"{bin_center:.2f}%", value=count))
        
        return distribution_data

    def _create_correlation_heatmap_data(self):
        """Create correlation data for visualization."""
        correlation_data = []
        
        # Flatten correlation matrix for bar chart
        assets = list(self.correlation_matrix.columns)
        for i, asset1 in enumerate(assets):
            for j, asset2 in enumerate(assets):
                if i != j:  # Exclude self-correlations
                    correlation_data.append(
                        SingleValueData(
                        time=f"{asset1}-{asset2}",
                            value=round(self.correlation_matrix.iloc[i, j], 3),
                        )
                    )
        
        return correlation_data

    def test_performance_attribution_dashboard(self):
        """Test performance attribution analysis dashboard."""
        # Create contribution chart
        contribution_data = []
        for asset_name, metrics in self.performance_attribution["asset_contributions"].items():
            contribution_data.append(
                SingleValueData(time=asset_name, value=metrics["contribution"])
            )
        
        contribution_chart = SinglePaneChart(
            series=[
            BarSeries(
                data=contribution_data,
                color="#9C27B0",
                    # title parameter removed - not supported by BarSeries
                )
            ]
            )
        
        # Create rolling attribution chart
        rolling_attribution = self._calculate_rolling_attribution()
        
        rolling_chart = SinglePaneChart(
            series=[
            LineSeries(
                    data=rolling_attribution["US_Stocks"],
                color="#2196F3",
                    # title parameter removed - not supported by LineSeries
            ),
            LineSeries(
                    data=rolling_attribution["Intl_Stocks"],
                color="#FF9800",
                    # title parameter removed - not supported by LineSeries
            ),
            LineSeries(
                    data=rolling_attribution["Bonds"],
                color="#4CAF50",
                    # title parameter removed - not supported by LineSeries
                ),
            ]
            )
        
        # Create sector allocation chart
        sector_allocation = self._create_sector_allocation()
        
        sector_chart = SinglePaneChart(
            series=[
            BarSeries(
                data=sector_allocation,
                color="#607D8B",
                    # title parameter removed - not supported by BarSeries
            )
            ]
        )
        
        # Create attribution dashboard - use 'charts' parameter, not 'panes'
        attribution_dashboard = MultiPaneChart(
            charts=[contribution_chart, rolling_chart, sector_chart]
        )
        
        # Add attribution summary to individual chart instead of dashboard
        total_contribution = sum([item.value for item in contribution_data])
        # Use a valid datetime string for annotation time instead of asset name
        annotation_time = (self.start_date + timedelta(days=self.days - 1)).strftime("%Y-%m-%d")
        attribution_annotation = create_text_annotation(
            annotation_time,  # Use valid datetime string instead of asset name
            contribution_data[-1].value * 1.2,
            f"Total Attribution: {total_contribution:.2f}%",
        )
        # Add annotation to the contribution chart, not the dashboard
        contribution_chart.add_annotation(attribution_annotation)
        
        # Generate configuration
        config = attribution_dashboard.to_frontend_config()
        
        # Verify configuration
        assert "charts" in config
        assert len(config["charts"]) == 3

    def _calculate_rolling_attribution(self, window=60):
        """Calculate rolling performance attribution."""
        rolling_attribution = {}
        
        for asset_name in ["US_Stocks", "Intl_Stocks", "Bonds"]:
            asset_returns = self.portfolio_data[asset_name]["daily_returns"]
            weight = self.portfolio_data[asset_name]["weight"]
            
            rolling_data = []
            for i in range(window, len(asset_returns)):
                window_returns = asset_returns[i - window : i]
                cumulative_return = np.prod(1 + window_returns) - 1
                contribution = cumulative_return * weight * 100
                
                date = self.start_date + timedelta(days=i)
                rolling_data.append(
                    SingleValueData(time=date.strftime("%Y-%m-%d"), value=round(contribution, 2))
                )
            
            rolling_attribution[asset_name] = rolling_data
        
        return rolling_attribution

    def _create_sector_allocation(self):
        """Create sector allocation data."""
        # Simulate sector breakdown within US stocks
        sectors = {
            "Technology": 0.25,
            "Healthcare": 0.20,
            "Financials": 0.15,
            "Consumer": 0.15,
            "Industrials": 0.10,
            "Energy": 0.05,
            "Others": 0.10,
        }
        
        sector_data = []
        for sector, weight in sectors.items():
            # Adjust weight by US stocks allocation
            adjusted_weight = weight * self.portfolio_data["US_Stocks"]["weight"] * 100
            sector_data.append(SingleValueData(time=sector, value=round(adjusted_weight, 2)))
        
        return sector_data

    def test_portfolio_optimization_dashboard(self):
        """Test portfolio optimization and rebalancing dashboard."""
        # Create efficient frontier simulation
        efficient_frontier = self._calculate_efficient_frontier()
        
        frontier_chart = SinglePaneChart(
            series=[LineSeries(data=efficient_frontier, color="#2196F3")]
            )
        
        # Add current portfolio point
        current_point = SingleValueData(
            time="Current Portfolio", value=self.risk_metrics["volatility"]
        )
        frontier_chart.add_series(LineSeries(data=[current_point], color="#f44336"))
        
        # Create rebalancing schedule
        rebalancing_data = self._create_rebalancing_schedule()
        
        rebalancing_chart = SinglePaneChart(
            series=[BarSeries(data=rebalancing_data, color="#4CAF50")]
            )
        
        # Create optimization dashboard - use 'charts' parameter, not 'panes'
        optimization_dashboard = MultiPaneChart(charts=[frontier_chart, rebalancing_chart])
        
        # Generate configuration
        config = optimization_dashboard.to_frontend_config()
        
        # Verify configuration
        assert "charts" in config
        assert len(config["charts"]) == 2

    def _calculate_efficient_frontier(self):
        """Calculate efficient frontier points."""
        # Simulate different portfolio weights
        frontier_data = []
        
        for i in range(0, 101, 10):  # 0% to 100% stocks
            stock_weight = i / 100
            bond_weight = 1 - stock_weight
            
            # Calculate portfolio metrics
            portfolio_return = (
                stock_weight * 0.08 + bond_weight * 0.03  # Stock return  # Bond return
            )
            
            portfolio_vol = np.sqrt(
                (stock_weight**2) * (0.15**2)
                + (bond_weight**2) * (0.05**2)
                + 2 * stock_weight * bond_weight * 0.15 * 0.05 * 0.3  # Correlation
            )
            
            frontier_data.append(
                SingleValueData(
                    time=f"{stock_weight*100:.0f}% Stocks", value=round(portfolio_vol * 100, 2)
                )
            )
        
        return frontier_data

    def _create_rebalancing_schedule(self):
        """Create rebalancing schedule data."""
        # Simulate quarterly rebalancing impact
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        rebalancing_impact = [2.1, -1.5, 3.2, -0.8]  # Percentage impact
        
        rebalancing_data = []
        for quarter, impact in zip(quarters, rebalancing_impact):
            rebalancing_data.append(SingleValueData(time=quarter, value=impact))
        
        return rebalancing_data

    def test_portfolio_dashboard_performance(self):
        """Test portfolio dashboard performance with large datasets."""
        # Generate larger portfolio dataset
        large_days = 1000
        large_portfolio_data = self._generate_large_portfolio_data(large_days)
        
        # Create dashboard with large dataset - use 'charts' parameter, not 'panes'
        performance_data = self._calculate_large_portfolio_performance(large_portfolio_data)
        
        dashboard = MultiPaneChart(
            charts=[
            SinglePaneChart(series=[LineSeries(performance_data)]),
                SinglePaneChart(series=[LineSeries(self._calculate_rolling_volatility())]),
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
        assert len(config["charts"]) == 2

    def _generate_large_portfolio_data(self, days):
        """Generate large portfolio dataset for performance testing."""
        # Simplified large dataset generation
        portfolio_values = []
        initial_value = 100000
        
        for i in range(days):
            daily_return = np.random.normal(0.0005, 0.015)  # 0.05% daily return, 1.5% volatility
            if i == 0:
                cumulative_return = 1.0
            else:
                cumulative_return *= 1 + daily_return
            
            portfolio_value = initial_value * cumulative_return
            date = self.start_date + timedelta(days=i)
            
            portfolio_values.append(
                SingleValueData(time=date.strftime("%Y-%m-%d"), value=round(portfolio_value, 2))
            )
        
        return portfolio_values

    def _calculate_large_portfolio_performance(self, portfolio_data):
        """Calculate performance for large portfolio dataset."""
        return portfolio_data  # Return as-is for performance testing 
