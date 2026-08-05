import unittest
import os, json
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44AnchorNumericalAudit(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.audit_dir = self.project_root / "data" / "audit"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.docs_dir = self.project_root / "docs" / "v2"
        self.screenshots_dir = self.docs_dir / "screenshots" / "v2-3a-2j"

    def test_v2_3a_2j_reports_exist(self):
        self.assertTrue((self.docs_dir / "V2_3A_2J_COMPLETION_REPORT.md").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2j_anchor_distance_audit.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2j_geodesic_route_invariants.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2j_official_osm_object_audit.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2j_authoritative_geometry.csv").exists())

    def test_geodesic_lower_bound_invariants_pass_100_percent(self):
        df_inv = pd.read_csv(self.reports_dir / "v2_3a_2j_geodesic_route_invariants.csv")
        for _, r in df_inv.iterrows():
            self.assertEqual(r["pass_fail"], "PASS", f"Invariant failed for {r['from_key']} -> {r['to_key']}!")
            self.assertGreaterEqual(r["route_minus_geodesic_km"], -0.050, f"Route distance must be >= geodesic distance for {r['from_key']} -> {r['to_key']}!")

    def test_distinct_keyed_objects(self):
        df_dist = pd.read_csv(self.reports_dir / "v2_3a_2j_anchor_distance_audit.csv")
        keys = list(df_dist["object_key"])
        self.assertEqual(len(keys), 13, "Must have exactly 13 distinct keyed objects!")
        self.assertEqual(len(set(keys)), 13, "All 13 object keys must be unique!")

        u_ref = df_dist[df_dist["object_key"] == "udhampur_place_reference"].iloc[0]
        u_start = df_dist[df_dist["object_key"] == "udhampur_pilot_start"].iloc[0]
        self.assertNotEqual((u_ref["longitude"], u_ref["latitude"]), (u_start["longitude"], u_start["latitude"]))

        b_ref = df_dist[df_dist["object_key"] == "banihal_place_reference"].iloc[0]
        b_end = df_dist[df_dist["object_key"] == "banihal_pilot_end"].iloc[0]
        self.assertNotEqual((b_ref["longitude"], b_ref["latitude"]), (b_end["longitude"], b_end["latitude"]))

    def test_terminal_labels_exclude_verinag_and_qazigund(self):
        df_dist = pd.read_csv(self.reports_dir / "v2_3a_2j_anchor_distance_audit.csv")
        b_end = df_dist[df_dist["object_key"] == "banihal_pilot_end"].iloc[0]
        self.assertNotIn("Verinag", b_end["name"])
        self.assertNotIn("Qazigund", b_end["name"])
        self.assertIn("Banihal", b_end["name"])

    def test_authoritative_geometry_uniqueness(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_2j_authoritative_geometry.csv")
        accepted_rows = df_auth[df_auth["status"] == "ACCEPTED"]
        self.assertEqual(len(accepted_rows), 1, "Exactly one geometry version must be ACCEPTED as authoritative!")
        self.assertEqual(accepted_rows["geometry_version"].iloc[0], "v2_3j_authoritative_pilot")

    def test_screenshots_exist(self):
        screenshot_names = [
            "udhampur_place_vs_pilot_start.png",
            "udhampur_to_chenani_true_distance.png",
            "consecutive_anchor_distance_validation.png",
            "banihal_place_projection_endpoint.png",
            "banihal_verinag_qazigund_separation.png",
            "relation_supported_and_unsupported_ways.png",
            "authoritative_geometry_full_route.png",
            "final_chainage_invariant_validation.png"
        ]
        for name in screenshot_names:
            s_path = self.screenshots_dir / name
            self.assertTrue(s_path.exists(), f"Screenshot {name} must exist!")

if __name__ == "__main__":
    unittest.main()
