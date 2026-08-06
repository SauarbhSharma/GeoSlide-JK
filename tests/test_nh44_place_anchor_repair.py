import unittest
import os, json, math
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44PlaceAnchorRepair(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.audit_dir = self.project_root / "data" / "audit"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.docs_dir = self.project_root / "docs" / "v2"
        self.raw_dir = self.audit_dir / "osm_place_raw"

    def test_v2_3a_2h_documentation_and_reports_exist(self):
        self.assertTrue((self.docs_dir / "V2_3A_2H_RELATION_AUDIT.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2H_COMPLETION_REPORT.md").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2h_existing_place_reference_audit.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2h_osm_place_id_verification.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2h_verified_place_projections.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2h_route_length_reconciliation.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2h_relation_5794209_audit.csv").exists())

    def test_all_seven_raw_osm_places_verified(self):
        files = ["udhampur.json", "chenani.json", "ramban.json", "ramsoo.json", "banihal.json", "qazigund.json", "verinag.json"]
        for fname in files:
            p_path = self.raw_dir / fname
            self.assertTrue(p_path.exists(), f"Raw OSM place JSON {fname} must exist!")
            with open(p_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["verification_status"], "VERIFIED")
            self.assertGreater(data["osm_id"], 0)

    def test_distinct_udhampur_and_chenani_chainages(self):
        df_proj = pd.read_csv(self.reports_dir / "v2_3a_2h_verified_place_projections.csv")
        u_ch = df_proj[df_proj["place_name"] == "Udhampur"]["chainage_km"].iloc[0]
        c_ch = df_proj[df_proj["place_name"] == "Chenani"]["chainage_km"].iloc[0]

        self.assertNotEqual(u_ch, c_ch, f"Udhampur ({u_ch} km) and Chenani ({c_ch} km) must have distinct chainages!")
        self.assertLess(u_ch, c_ch, f"Chenani ({c_ch} km) must be greater than Udhampur ({u_ch} km)!")

    def test_strictly_monotonic_chainages(self):
        df_proj = pd.read_csv(self.reports_dir / "v2_3a_2h_verified_place_projections.csv")
        df_mon = df_proj[df_proj["place_name"].isin(["Udhampur", "Chenani", "Ramban", "Ramsoo", "Banihal"])].sort_values("chainage_km")
        chainages = list(df_mon["chainage_km"])
        is_increasing = all(x < y for x, y in zip(chainages, chainages[1:]))
        self.assertTrue(is_increasing, f"Place chainages must be strictly monotonic! Values: {chainages}")

    def test_banihal_terminal_mapping_not_verinag(self):
        df_proj = pd.read_csv(self.reports_dir / "v2_3a_2h_verified_place_projections.csv")
        banihal_row = df_proj[df_proj["place_name"] == "Banihal"].iloc[0]
        verinag_row = df_proj[df_proj["place_name"] == "Verinag"].iloc[0]

        self.assertEqual(banihal_row["place_name"], "Banihal")
        self.assertNotEqual(banihal_row["original_lat"], verinag_row["original_lat"])
        self.assertNotEqual(banihal_row["original_lon"], verinag_row["original_lon"])
        self.assertEqual(banihal_row["original_lat"], 33.438000)

if __name__ == "__main__":
    unittest.main()
