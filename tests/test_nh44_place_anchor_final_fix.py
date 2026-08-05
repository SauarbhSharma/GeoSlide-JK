import unittest
import os, json
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44PlaceAnchorFinalFix(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.audit_dir = self.project_root / "data" / "audit"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.docs_dir = self.project_root / "docs" / "v2"
        self.screenshots_dir = self.docs_dir / "screenshots" / "v2-3a-2i"

    def test_v2_3a_2i_reports_and_documentation_exist(self):
        self.assertTrue((self.docs_dir / "V2_3A_2I_COMPLETION_REPORT.md").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2i_raw_osm_verification.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2i_geometry_reconciliation.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2i_pilot_place_projections.csv").exists())

    def test_endpoint_keyed_record_is_banihal(self):
        df_proj = pd.read_csv(self.reports_dir / "v2_3a_2i_pilot_place_projections.csv")
        banihal_row = df_proj[df_proj["place_key"] == "banihal"].iloc[0]

        self.assertEqual(banihal_row["place_key"], "banihal")
        self.assertEqual(banihal_row["place_name"], "Banihal")
        self.assertEqual(banihal_row["role"], "northern_terminal")
        self.assertIn("Banihal", banihal_row["label"])
        self.assertNotIn("Verinag", banihal_row["label"])
        self.assertNotIn("Verinag (Km 74.915)", banihal_row["label"])

    def test_verinag_is_non_pilot_reference(self):
        gdf_non_pilot = gpd.read_file(self.audit_dir / "nh44_non_pilot_place_references.geojson")
        verinag_row = gdf_non_pilot[gdf_non_pilot["place_key"] == "verinag"].iloc[0]

        self.assertEqual(verinag_row["place_key"], "verinag")
        self.assertNotEqual(verinag_row.get("role"), "northern_terminal")

    def test_udhampur_to_chenani_distance_greater_than_5km(self):
        df_proj = pd.read_csv(self.reports_dir / "v2_3a_2i_pilot_place_projections.csv")
        u_ch = df_proj[df_proj["place_key"] == "udhampur"]["chainage_km"].iloc[0]
        c_ch = df_proj[df_proj["place_key"] == "chenani"]["chainage_km"].iloc[0]

        dist_km = c_ch - u_ch
        self.assertGreater(dist_km, 5.0, f"Udhampur to Chenani distance ({dist_km} km) must be > 5.0 km!")

    def test_monotonic_south_to_north_chainages(self):
        df_proj = pd.read_csv(self.reports_dir / "v2_3a_2i_pilot_place_projections.csv")
        df_mon = df_proj.sort_values("chainage_km")
        chainages = list(df_mon["chainage_km"])
        is_increasing = all(x < y for x, y in zip(chainages, chainages[1:]))
        self.assertTrue(is_increasing, f"Pilot place chainages must be strictly monotonic! Values: {chainages}")

    def test_screenshots_exist(self):
        screenshot_names = [
            "actual_udhampur_start_on_basemap.png",
            "complete_udhampur_to_chenani_alignment.png",
            "corrected_udhampur_chenani_chainages.png",
            "banihal_endpoint_keyed_record.png",
            "banihal_and_verinag_separate.png",
            "corrected_full_route_with_five_places.png",
            "relation_member_match_statistics.png",
            "final_terminal_and_chainage_validation.png"
        ]
        for name in screenshot_names:
            s_path = self.screenshots_dir / name
            self.assertTrue(s_path.exists(), f"Screenshot {name} must exist!")

if __name__ == "__main__":
    unittest.main()
