import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = PROJECT_ROOT / "apps" / "web"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

FORBIDDEN_PHRASES = [
    "Full J&K UT Interactive View",
    "XGBoost v0.1.0-prototype",
    "Copernicus DEM Derived",
    "Official Warning",
    "20 Whitelisted Districts",
    "Phase 2 Active",
    "Phase 4 Pending",
    "Phase 5 Scheduled",
    "Phase 6 Pending",
    "Risk & Rainfall Modules: Demo"
]

REQUIRED_TERMS = [
    "GeoSlide-JK v1.0.0",
    "Static Susceptibility Model: Trained",
    "Dynamic Hazard: Scenario / Proxy Mode",
    "20 J&K UT Districts"
]

class TestUiTruthfulness(unittest.TestCase):

    def test_no_forbidden_phrases_in_frontend(self):
        found_forbidden = []
        for file_path in FRONTEND_DIR.glob("**/*.tsx"):
            if "node_modules" in str(file_path) or ".next" in str(file_path):
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                for phrase in FORBIDDEN_PHRASES:
                    if phrase in content:
                        found_forbidden.append((file_path.name, phrase))
                        
        self.assertEqual(len(found_forbidden), 0, f"Forbidden phrases found in public UI: {found_forbidden}")

    def test_required_truthfulness_terms_present(self):
        all_code = ""
        for file_path in FRONTEND_DIR.glob("**/*.tsx"):
            if "node_modules" in str(file_path) or ".next" in str(file_path):
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                all_code += f.read() + "\n font-mono"
                
        for term in REQUIRED_TERMS:
            self.assertIn(term, all_code, f"Required truthful term missing: '{term}'")

    def test_active_fault_documentation_present(self):
        rec_md = REPORTS_DIR / "phase_2_feature_count_reconciliation.md"
        self.assertTrue(rec_md.exists(), "Reconciliation report missing")
        with open(rec_md, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Active Fault Resolution (Option B Selected)", content)
            self.assertIn("fault_type = 'active'", content)

if __name__ == "__main__":
    unittest.main()
