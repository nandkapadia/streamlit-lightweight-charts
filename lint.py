#!/usr/bin/env python3
"""
Linting script for streamlit-lightweight-charts.

This script runs all configured linting tools:
- isort: Import sorting
- black: Code formatting
- pylint: Code quality checks

Usage:
    python lint.py [--check] [--fix]
    
Options:
    --check: Only check for issues, don't fix them
    --fix: Fix issues automatically (default)
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running {description}...")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"❌ {description} failed with return code {result.returncode}")
            return False
        else:
            print(f"✅ {description} completed successfully")
            return True
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run linting tools on the codebase")
    parser.add_argument(
        "--check", 
        action="store_true", 
        help="Only check for issues, don't fix them"
    )
    parser.add_argument(
        "--fix", 
        action="store_true", 
        help="Fix issues automatically (default)"
    )
    
    args = parser.parse_args()
    
    # Default to fix mode if no mode specified
    if not args.check and not args.fix:
        args.fix = True
    
    # Define the directories to lint
    directories = [
        "streamlit_lightweight_charts",
        "examples",
        "tests",
    ]
    
    # Filter out non-existent directories
    directories = [d for d in directories if Path(d).exists()]
    
    if not directories:
        print("❌ No valid directories found to lint")
        sys.exit(1)
    
    print(f"🔍 Linting directories: {', '.join(directories)}")
    
    success = True
    
    # Run isort
    if args.check:
        isort_cmd = ["python", "-m", "isort", "--check-only", "--diff"] + directories
    else:
        isort_cmd = ["python", "-m", "isort"] + directories
    
    success &= run_command(isort_cmd, "isort (import sorting)")
    
    # Run black
    if args.check:
        black_cmd = ["black", "--check", "--diff"] + directories
    else:
        black_cmd = ["black"] + directories
    
    success &= run_command(black_cmd, "black (code formatting)")
    
    # Run pylint
    pylint_cmd = ["python", "-m", "pylint"] + directories
    success &= run_command(pylint_cmd, "pylint (code quality)")
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 All linting tools completed successfully!")
        sys.exit(0)
    else:
        print("❌ Some linting tools failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main() 