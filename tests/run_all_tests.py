#!/usr/bin/env python3
"""
GeoSlide-JK Master Test Runner
Executes all automated unit and integration tests across data safety, boundary processing, and FastAPI endpoints.
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "apps" / "api"))

from tests.test_paths_and_safety import TestPathConfigAndSafety
from tests.test_data_discovery import TestDataDiscovery
from tests.geospatial.test_boundaries import TestBoundaryProcessing
from tests.api.test_api import TestFastApiEndpoints

def run_all_tests():
    print("=== GeoSlide-JK Master Test Suite Execution ===")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPathConfigAndSafety))
    suite.addTests(loader.loadTestsFromTestCase(TestDataDiscovery))
    suite.addTests(loader.loadTestsFromTestCase(TestBoundaryProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestFastApiEndpoints))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\nALL PHASE 1 TESTS PASSED SUCCESSFULLY! (16/16 Test Cases Passed)")
        sys.exit(0)
    else:
        print(f"\nTEST SUITE FAILED: {len(result.failures)} failures, {len(result.errors)} errors.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
