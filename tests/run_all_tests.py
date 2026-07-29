#!/usr/bin/env python3
"""
GeoSlide-JK Master Test Runner
Discovers and executes all Phase 1, Phase 1.1, and Phase 2 test suites.
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "apps" / "api"))
sys.path.insert(0, str(PROJECT_ROOT))

def run_all_tests():
    print("=== GeoSlide-JK Master Test Suite Execution ===")
    loader = unittest.TestLoader()
    suite = loader.discover(str(PROJECT_ROOT / "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print(f"\nSUCCESS: All {result.testsRun} test cases PASSED cleanly!")
        return 0
    else:
        print(f"\nFAILURE: {len(result.failures)} failures, {len(result.errors)} errors out of {result.testsRun} tests.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
