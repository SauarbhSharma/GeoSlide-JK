#!/usr/bin/env python3
"""
GeoSlide-JK Master Test Runner
Discovers and executes all Phase 1, Phase 1.1, and Phase 2 test suites.
"""

import sys
import unittest
import importlib.util
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "apps" / "api"))
sys.path.insert(0, str(PROJECT_ROOT))

def run_all_tests():
    print("=== GeoSlide-JK Master Test Suite Execution ===")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_files = sorted(list((PROJECT_ROOT / "tests").rglob("test_*.py")))
    for tf in test_files:
        rel_path = tf.relative_to(PROJECT_ROOT)
        mod_name = str(rel_path.with_suffix("")).replace("\\", ".").replace("/", ".")
        spec = importlib.util.spec_from_file_location(mod_name, tf)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = mod
        spec.loader.exec_module(mod)
        s = loader.loadTestsFromModule(mod)
        suite.addTest(s)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\n=== TEST SUITE SUMMARY ===")
    print(f"Total tests run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print(f"\nSUCCESS: All {result.testsRun} test cases PASSED cleanly!")
        return 0
    else:
        print(f"\nFAILURE: {len(result.failures)} failures, {len(result.errors)} errors out of {result.testsRun} tests.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

