.PHONY: help install-dev lint lint-check format test clean

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-dev:  ## Install development dependencies
	pip install -e ".[dev]"

lint:  ## Run all linting tools and fix issues
	python lint.py --fix

lint-check:  ## Check for linting issues without fixing
	python lint.py --check

format:  ## Format code with black and isort
	isort streamlit_lightweight_charts examples tests
	black streamlit_lightweight_charts examples tests

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ --cov=streamlit_lightweight_charts --cov-report=html --cov-report=term

clean:  ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete 