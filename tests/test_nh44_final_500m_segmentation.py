import unittest
import os, json, math
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44Final500mSegmentation(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

    def test_segment_count_equals_ceiling(self):
        df_seg = pd.read_csv(self.reports_dir / "v2_3a_final_segment_inventory.csv")
        self.assertEqual(len(df_seg), 158)

    def test_non_final_segments_are_500m(self):
        df_seg = pd.read_csv(self.reports_dir / "v2_3a_final_segment_inventory.csv")
        non_final = df_seg[df_seg["terminal_segment"] == False]
        for _, r in non_final.iterrows():
            self.assertAlmostEqual(r["nominal_length_m"], 500.0, places=1)
            self.assertAlmostEqual(r["actual_geometry_length_m"], 500.0, places=1)

    def test_final_residual_segment_length(self):
        df_seg = pd.read_csv(self.reports_dir / "v2_3a_final_segment_inventory.csv")
        final_seg = df_seg[df_seg["terminal_segment"] == True].iloc[0]
        self.assertAlmostEqual(final_seg["actual_geometry_length_m"], 119.37, places=2)

    def test_segment_monotonicity_and_no_gaps(self):
        df_seg = pd.read_csv(self.reports_dir / "v2_3a_final_segment_inventory.csv")
        for i in range(len(df_seg) - 1):
            curr_end = df_seg.iloc[i]["end_chainage_m"]
            next_start = df_seg.iloc[i+1]["start_chainage_m"]
            self.assertEqual(curr_end, next_start)

    def test_sum_of_segments_matches_route_length(self):
        df_seg = pd.read_csv(self.reports_dir / "v2_3a_final_segment_inventory.csv")
        total_m = df_seg["actual_geometry_length_m"].sum()
        self.assertAlmostEqual(total_m, 78619.37, places=1)

    def test_source_route_sha256_in_segments(self):
        df_seg = pd.read_csv(self.reports_dir / "v2_3a_final_segment_inventory.csv")
        with open(self.audit_dir / "nh44_authoritative_manifest_final.json", "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for _, r in df_seg.iterrows():
            self.assertEqual(r["source_route_sha256"], manifest["file_hashes"]["final_geojson"])

if __name__ == "__main__":
    unittest.main()
