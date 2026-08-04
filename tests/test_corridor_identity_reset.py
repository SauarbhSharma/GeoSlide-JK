import unittest
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path

class TestCorridorIdentityReset(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.docs_dir = self.project_root / "docs" / "v2"
        self.vectors_dir = self.project_root / "data" / "processed" / "vectors"

    def test_reset_documentation_and_reports_exist(self):
        self.assertTrue((self.docs_dir / "V2_3A_RESET_REJECTED_OUTPUTS.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_RESET_ROAD_SOURCE_AUDIT.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_RESET_CORRIDOR_IDENTITY_DECISION.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_RESET_RUNTIME_REPORT.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_RESET_LEGACY_CONTENT_AUDIT.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_reset_road_candidate_audit.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_reset_runtime_assets.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_reset_screenshot_validation.csv").exists())

    def test_sinthan_pass_route_rejected_from_nh44(self):
        csv_path = self.reports_dir / "v2_3a_reset_road_candidate_audit.csv"
        self.assertTrue(csv_path.exists())
        df = pd.read_csv(csv_path)
        sinthan_rows = df[df['passes_sinthan_pass'] == True]
        for _, row in sinthan_rows.iterrows():
            self.assertTrue("REJECTED" in str(row['highway_identity_verdict']),
                            f"Sinthan Pass route {row['candidate_id']} must be REJECTED")

    def test_nh44_candidate_passes_udhampur_ramban_banihal_anchors(self):
        csv_path = self.reports_dir / "v2_3a_reset_road_candidate_audit.csv"
        df = pd.read_csv(csv_path)
        accepted_df = df[df['highway_identity_verdict'].str.startswith("ACCEPTED")]
        self.assertGreater(len(accepted_df), 0, "Must have accepted NH-44 candidate features")

    def test_no_legacy_exposure_percentages_or_operational_advice(self):
        advisories_page = self.project_root / "apps" / "web" / "app" / "advisories" / "page.tsx"
        if advisories_page.exists():
            content = advisories_page.read_text(encoding="utf-8")
            self.assertNotIn("Delay non-essential transit", content)
            self.assertNotIn("Km 142.0", content)

        corridor_page = self.project_root / "apps" / "web" / "app" / "corridor" / "page.tsx"
        if corridor_page.exists():
            content = corridor_page.read_text(encoding="utf-8")
            self.assertNotIn("88%", content)
            self.assertNotIn("79%", content)
            self.assertIn("Verified NH-44 geometry under validation", content)

    def test_screenshot_hashes_are_unique(self):
        csv_path = self.reports_dir / "v2_3a_reset_screenshot_validation.csv"
        self.assertTrue(csv_path.exists())
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 5, "Must contain exactly 5 reset screenshots")
        self.assertEqual(df['md5_hash'].nunique(), 5, "All 5 screenshot MD5 hashes must be unique")

if __name__ == "__main__":
    unittest.main()
