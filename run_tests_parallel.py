#!/usr/bin/env python3
"""
Script to run tests with parallel execution options.

This script provides various ways to run tests with parallel execution
using pytest-xdist for improved performance.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_tests_parallel(workers="auto", test_path="tests", coverage=True, markers=None):
    """
    Run tests with parallel execution.
    
    Args:
        workers: Number of worker processes ('auto' for automatic detection)
        test_path: Path to test directory
        coverage: Whether to run with coverage
        markers: Specific test markers to run
    """
    cmd = [
        sys.executable, "-m", "pytest",
        test_path,
        "-n", str(workers),
        "--dist=loadfile",
        "--verbose",
        "--tb=short",
        "--maxfail=10",
        "--durations=10"
    ]
    
    if coverage:
        cmd.extend([
            "--cov=streamlit_lightweight_charts_pro",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov"
        ])
    
    if markers:
        cmd.extend(["-m", markers])
    
    print(f"Running tests with {workers} workers...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 80)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("-" * 80)
        print("Tests completed successfully!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print("-" * 80)
        print(f"Tests failed with exit code: {e.returncode}")
        return e.returncode


def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(
        description="Run tests with parallel execution options"
    )
    parser.add_argument(
        "-w", "--workers",
        default="auto",
        help="Number of worker processes (default: auto)"
    )
    parser.add_argument(
        "-p", "--test-path",
        default="tests",
        help="Path to test directory (default: tests)"
    )
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Disable coverage reporting"
    )
    parser.add_argument(
        "-m", "--markers",
        help="Run only tests matching given markers"
    )
    parser.add_argument(
        "--list-workers",
        action="store_true",
        help="List available worker options"
    )
    
    args = parser.parse_args()
    
    if args.list_workers:
        print("Available worker options:")
        print("  auto    - Automatically detect optimal number of workers")
        print("  logical - Use number of logical CPU cores")
        print("  physical - Use number of physical CPU cores")
        print("  N       - Use specific number of workers (e.g., 4)")
        print("  N/2     - Use half of available cores (e.g., 4/2 = 2)")
        return 0
    
    # Validate test path
    test_path = Path(args.test_path)
    if not test_path.exists():
        print(f"Error: Test path '{test_path}' does not exist")
        return 1
    
    return run_tests_parallel(
        workers=args.workers,
        test_path=str(test_path),
        coverage=not args.no_coverage,
        markers=args.markers
    )


if __name__ == "__main__":
    sys.exit(main())
