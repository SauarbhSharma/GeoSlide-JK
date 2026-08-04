import unittest
import os
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44MainlineRepair(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.audit_dir = self.project_root / "data" / "audit"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.docs_dir = self.project_root / "docs" / "v2"

    def test_v2_3a_2r_documentation_and_reports_exist(self):
        self.assertTrue((self.docs_dir / "V2_3A_2R_FAILURE_DIAGNOSIS.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2R_MAINLINE_REPAIR_REPORT.md").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2r_terminal_nodes.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2r_edge_classification_reconciliation.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2r_edge_adjacency.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2r_length_reconciliation.csv").exists())

    def test_repaired_data_packages_and_kml_exist(self):
        main_parquet = self.audit_dir / "nh44_repaired_mainline_source_edges.parquet"
        main_geojson = self.audit_dir / "nh44_repaired_mainline_source_edges.geojson"
        excl_geojson = self.audit_dir / "nh44_excluded_branch_edges.geojson"
        val_geojson = self.audit_dir / "nh44_repaired_mainline_validation.geojson"
        order_csv = self.audit_dir / "nh44_repaired_mainline_order.csv"
        struct_csv = self.audit_dir / "nh44_repaired_mainline_structure_inventory.csv"
        kml_file = self.audit_dir / "nh44_repaired_mainline.kml"

        self.assertTrue(main_parquet.exists())
        self.assertTrue(main_geojson.exists())
        self.assertTrue(excl_geojson.exists())
        self.assertTrue(val_geojson.exists())
        self.assertTrue(order_csv.exists())
        self.assertTrue(struct_csv.exists())
        self.assertTrue(kml_file.exists())

    def test_selected_and_excluded_ids_are_disjoint(self):
        csv_path = self.reports_dir / "v2_3a_2r_edge_classification_reconciliation.csv"
        self.assertTrue(csv_path.exists())
        df = pd.read_csv(csv_path)

        sel_ids = set(df[df['authoritative_classification'] == 'SELECTED_MAINLINE']['source_edge_id'])
        excl_ids = set(df[df['authoritative_classification'] == 'EXCLUDED_BRANCH']['source_edge_id'])

        overlap = sel_ids.intersection(excl_ids)
        self.assertEqual(len(overlap), 0, f"Selected and Excluded edge IDs must be disjoint! Found overlap: {overlap}")

    def test_repaired_mainline_spans_all_mandatory_sectors(self):
        val_geojson = self.audit_dir / "nh44_repaired_mainline_validation.geojson"
        gdf_val = gpd.read_file(val_geojson)
        b = gdf_val.total_bounds # [minx, miny, maxx, maxy]

        self.assertLess(b[1], 33.00, "Mainline must span south to Udhampur (lat < 33.00)")
        self.assertGreater(b[3], 33.40, "Mainline must span north to Banihal (lat > 33.40)")

    def test_zero_edge_adjacency_failures(self):
        csv_path = self.reports_dir / "v2_3a_2r_edge_adjacency.csv"
        self.assertTrue(csv_path.exists())
        df = pd.read_csv(csv_path)
        adj_failures = df[df['continuity_status'] != 'PASS (Connected <= 0.5m)']
        self.assertEqual(len(adj_failures), 0, "Must have zero edge adjacency continuity failures!")

if __name__ == "__main__":
    unittest.main()
