import unittest
import os
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44MainlineTopology(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.audit_dir = self.project_root / "data" / "audit"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.docs_dir = self.project_root / "docs" / "v2"

    def test_v2_3a_2_documentation_and_reports_exist(self):
        self.assertTrue((self.docs_dir / "V2_3A_2_CANDIDATE_NETWORK_STATUS.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2_OSM_RELATION_AUDIT.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2_TERMINAL_DECISION.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2_TOPOLOGY_AUDIT.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2_MAINLINE_SELECTION.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2_STRUCTURE_AUDIT.md").exists())

    def test_mainline_data_package_integrity(self):
        main_parquet = self.audit_dir / "nh44_pilot_mainline_source_edges.parquet"
        excl_geojson = self.audit_dir / "nh44_excluded_branch_edges.geojson"
        order_csv = self.audit_dir / "nh44_pilot_mainline_edge_order.csv"
        struct_csv = self.audit_dir / "nh44_mainline_structure_inventory.csv"

        self.assertTrue(main_parquet.exists())
        self.assertTrue(excl_geojson.exists())
        self.assertTrue(order_csv.exists())
        self.assertTrue(struct_csv.exists())

        gdf_main = gpd.read_parquet(main_parquet)
        df_order = pd.read_csv(order_csv)

        self.assertEqual(len(gdf_main), len(df_order), "Mainline edge counts must match order table")
        self.assertEqual(df_order['osm_way_id'].nunique(), len(df_order), "Mainline must have zero repeated way IDs")

    def test_visual_validation_hashes_unique(self):
        csv_path = self.reports_dir / "v2_3a_2_visual_validation.csv"
        self.assertTrue(csv_path.exists())
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 10, "Must contain 10 V2-3A.2 screenshots")
        self.assertEqual(df['md5_hash'].nunique(), 10, "All 10 screenshot MD5 hashes must be unique")

if __name__ == "__main__":
    unittest.main()
