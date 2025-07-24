#!/usr/bin/env python3
"""
Comprehensive test runner for streamlit_lightweight_charts_pro.

This script runs all tests with detailed reporting and coverage analysis.
Updated for the new test directory structure.
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class TestRunner:
    """Comprehensive test runner with detailed reporting."""

    def __init__(self):
        """Initialize the test runner."""
        self.project_root = Path(__file__).parent
        self.test_results = {}
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def run_command(self, command: List[str], capture_output: bool = True) -> Dict[str, Any]:
        """Run a command and return results."""
        try:
            if capture_output:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    cwd=self.project_root,
                    timeout=300,  # 5 minute timeout
                )
            else:
                result = subprocess.run(command, cwd=self.project_root, timeout=300)

            return {
                "returncode": result.returncode,
                "stdout": result.stdout if capture_output else None,
                "stderr": result.stderr if capture_output else None,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": None,
                "stderr": "Command timed out after 5 minutes",
                "success": False,
            }
        except Exception as e:
            return {"returncode": -1, "stdout": None, "stderr": str(e), "success": False}

    def check_dependencies(self) -> bool:
        """Check if all required dependencies are installed."""
        print("🔍 Checking dependencies...")

        required_packages = ["pytest", "pytest-cov", "pandas", "numpy", "streamlit"]

        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)

        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print("Please install missing packages:")
            print(f"pip install {' '.join(missing_packages)}")
            return False

        print("✅ All dependencies are installed")
        return True

    def run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests."""
        print("\n🧪 Running unit tests...")

        command = [
            "python",
            "-m",
            "pytest",
            "tests/unit/",
            "-v",
            "--tb=short",
            "--durations=10",
            "--maxfail=10",
        ]

        result = self.run_command(command)

        if result["success"]:
            print("✅ Unit tests passed")
        else:
            print("❌ Unit tests failed")
            if result["stderr"]:
                print(f"Error: {result['stderr']}")

        return result

    def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests."""
        print("\n🔗 Running integration tests...")

        command = [
            "python",
            "-m",
            "pytest",
            "tests/integration/",
            "-v",
            "--tb=short",
            "--durations=10",
            "--maxfail=10",
        ]

        result = self.run_command(command)

        if result["success"]:
            print("✅ Integration tests passed")
        else:
            print("❌ Integration tests failed")
            if result["stderr"]:
                print(f"Error: {result['stderr']}")

        return result

    def run_e2e_tests(self) -> Dict[str, Any]:
        """Run end-to-end tests."""
        print("\n🌐 Running end-to-end tests...")

        command = [
            "python",
            "-m",
            "pytest",
            "tests/e2e/",
            "-v",
            "--tb=short",
            "--durations=10",
            "--maxfail=10",
        ]

        result = self.run_command(command)

        if result["success"]:
            print("✅ End-to-end tests passed")
        else:
            print("❌ End-to-end tests failed")
            if result["stderr"]:
                print(f"Error: {result['stderr']}")

        return result

    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests."""
        print("\n⚡ Running performance tests...")

        command = [
            "python",
            "-m",
            "pytest",
            "tests/performance/",
            "-v",
            "--tb=short",
            "--durations=10",
            "--maxfail=10",
        ]

        result = self.run_command(command)

        if result["success"]:
            print("✅ Performance tests passed")
        else:
            print("❌ Performance tests failed")
            if result["stderr"]:
                print(f"Error: {result['stderr']}")

        return result

    def run_coverage_analysis(self) -> Dict[str, Any]:
        """Run coverage analysis."""
        print("\n📊 Running coverage analysis...")

        command = [
            "python",
            "-m",
            "pytest",
            "tests/",
            "--cov=streamlit_lightweight_charts_pro",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-report=json:coverage.json",
            "--cov-fail-under=80",
        ]

        result = self.run_command(command)

        if result["success"]:
            print("✅ Coverage analysis completed")
        else:
            print("❌ Coverage analysis failed")
            if result["stderr"]:
                print(f"Error: {result['stderr']}")

        return result

    def run_linting(self) -> Dict[str, Any]:
        """Run code linting."""
        print("\n🔍 Running code linting...")

        command = [
            "python",
            "-m",
            "pylint",
            "streamlit_lightweight_charts_pro/",
            "--rcfile=.pylintrc",
            "--output-format=text",
            "--score=y",
        ]

        result = self.run_command(command)

        if result["success"]:
            print("✅ Code linting passed")
        else:
            print("⚠️  Code linting issues found")
            if result["stdout"]:
                print(result["stdout"])

        return result

    def run_type_checking(self) -> Dict[str, Any]:
        """Run type checking."""
        print("\n🔍 Running type checking...")

        try:
            import mypy  # type: ignore

            command = [
                "python",
                "-m",
                "mypy",
                "streamlit_lightweight_charts_pro/",
                "--ignore-missing-imports",
                "--no-strict-optional",
            ]

            result = self.run_command(command)

            if result["success"]:
                print("✅ Type checking passed")
            else:
                print("⚠️  Type checking issues found")
                if result["stdout"]:
                    print(result["stdout"])

            return result
        except ImportError:
            print("⚠️  mypy not installed, skipping type checking")
            return {"success": True, "skipped": True}

    def run_security_scan(self) -> Dict[str, Any]:
        """Run security scanning."""
        print("\n🔒 Running security scan...")

        try:
            import bandit  # type: ignore

            command = [
                "python",
                "-m",
                "bandit",
                "-r",
                "streamlit_lightweight_charts_pro/",
                "-f",
                "json",
                "-o",
                "bandit-report.json",
            ]

            result = self.run_command(command)

            if result["success"]:
                print("✅ Security scan completed")
            else:
                print("⚠️  Security issues found")
                if result["stdout"]:
                    print(result["stdout"])

            return result
        except ImportError:
            print("⚠️  bandit not installed, skipping security scan")
            return {"success": True, "skipped": True}

    def generate_test_report(self) -> str:
        """Generate a comprehensive test report."""
        print("\n📋 Generating test report...")

        total_tests = len(self.test_results)
        passed_tests = sum(
            1 for result in self.test_results.values() if result.get("success", False)
        )
        failed_tests = total_tests - passed_tests

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    COMPREHENSIVE TEST REPORT                 ║
╚══════════════════════════════════════════════════════════════╝

📊 SUMMARY:
   Total Test Suites: {total_tests}
   Passed: {passed_tests}
   Failed: {failed_tests}
   Success Rate: {(passed_tests/total_tests*100):.1f}%

⏱️  EXECUTION TIME:
   Start: {self.start_time}
   End: {self.end_time}
   Duration: {(self.end_time - self.start_time).total_seconds():.2f} seconds 

📋 DETAILED RESULTS:
"""

        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            skipped = " (SKIPPED)" if result.get("skipped", False) else ""
            report += f"   {test_name}: {status}{skipped}\n"

        report += "\n🔍 RECOMMENDATIONS:\n"

        if failed_tests == 0:
            report += "   🎉 All tests passed! The codebase is in excellent condition.\n"
        else:
            report += "   ⚠️  Some tests failed. Please review the failures above.\n"

        if self.test_results.get("coverage", {}).get("success", False):
            report += "   📊 Coverage analysis completed. Check htmlcov/ for detailed report.\n"

        if self.test_results.get("linting", {}).get("success", False):
            report += "   🔍 Code quality checks passed.\n"

        report += "\n📁 ARTIFACTS:\n"
        report += "   - Coverage report: htmlcov/\n"
        report += "   - Coverage data: coverage.json\n"
        report += "   - Security report: bandit-report.json (if available)\n"

        return report

    def save_test_results(self):
        """Save test results to JSON file."""
        results_file = self.project_root / "test_results.json"

        results_data = {
            "timestamp": self.end_time.isoformat(),
            "duration": (self.end_time - self.start_time).total_seconds(),
            "results": self.test_results,
        }

        with open(results_file, "w") as f:
            json.dump(results_data, f, indent=2)

        print(f"\n💾 Test results saved to: {results_file}")

    def run_all_tests(self) -> bool:
        """Run all tests and return overall success status."""
        print("🚀 Starting comprehensive test suite...")

        self.start_time = time.time()

        # Check dependencies first
        if not self.check_dependencies():
            return False

        # Run all test suites
        test_suites = [
            ("unit_tests", self.run_unit_tests),
            ("integration_tests", self.run_integration_tests),
            ("e2e_tests", self.run_e2e_tests),
            ("performance_tests", self.run_performance_tests),
            ("coverage", self.run_coverage_analysis),
            ("linting", self.run_linting),
            ("type_checking", self.run_type_checking),
            ("security_scan", self.run_security_scan),
        ]

        for test_name, test_func in test_suites:
            self.test_results[test_name] = test_func()

        self.end_time = time.time()

        # Generate and display report
        report = self.generate_test_report()
        print(report)

        # Save results
        self.save_test_results()

        # Return overall success
        overall_success = all(
            result.get("success", False) or result.get("skipped", False)
            for result in self.test_results.values()
        )

        if overall_success:
            print("🎉 All critical tests passed!")
        else:
            print("❌ Some tests failed. Please review the report above.")

        return overall_success


def main():
    """Main entry point."""
    runner = TestRunner()
    success = runner.run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
