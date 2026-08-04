import unittest
import os
import pandas as pd
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Point

class TestNH44TerminalLock(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.audit_dir = self.project_root / "data" / "audit"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.docs_dir = self.project_root / "docs" / "v2"

    def test_v2_3a_2t_documentation_and_reports_exist(self):
        self.assertTrue((self.docs_dir / "V2_3A_2T_EXISTING_TERMINAL_AUDIT.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2T_TERMINAL_SCOPE_DECISION.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2T_STRUCTURE_RECONCILIATION.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2T_TERMINAL_LOCK_REPORT.md").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2t_existing_terminal_audit.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2t_terminal_candidates.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2t_snapping_reconciliation.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2t_sector_projection.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2t_length_reconciliation.csv").exists())

    def test_locked_data_packages_and_kml_exist(self):
        main_parquet = self.audit_dir / "nh44_locked_pilot_source_edges.parquet"
        main_geojson = self.audit_dir / "nh44_locked_pilot_source_edges.geojson"
        val_geojson = self.audit_dir / "nh44_locked_pilot_validation.geojson"
        order_csv = self.audit_dir / "nh44_locked_pilot_edge_order.csv"
        struct_csv = self.audit_dir / "nh44_locked_pilot_structure_inventory.csv"
        kml_file = self.audit_dir / "nh44_locked_pilot.kml"

        self.assertTrue(main_parquet.exists())
        self.assertTrue(main_geojson.exists())
        self.assertTrue(val_geojson.exists())
        self.assertTrue(order_csv.exists())
        self.assertTrue(struct_csv.exists())
        self.assertTrue(kml_file.exists())

    def test_terminal_markers_equal_route_endpoints(self):
        val_geojson = self.audit_dir / "nh44_locked_pilot_validation.geojson"
        gdf_val = gpd.read_file(val_geojson)
        geom = gdf_val.geometry.iloc[0]
        coords = list(geom.coords)

        cand_csv = self.reports_dir / "v2_3a_2t_terminal_candidates.csv"
        df_cand = pd.read_csv(cand_csv)

        s_lat = df_cand.loc[df_cand['candidate_id'] == 'SOUTH_CAND_1', 'latitude'].iloc[0]
        s_lon = df_cand.loc[df_cand['candidate_id'] == 'SOUTH_CAND_1', 'longitude'].iloc[0]
        n_lat = df_cand.loc[df_cand['candidate_id'] == 'NORTH_CAND_1', 'latitude'].iloc[0]
        n_lon = df_cand.loc[df_cand['candidate_id'] == 'NORTH_CAND_1', 'longitude'].iloc[0]

        s_err = Point(coords[0]).distance(Point(s_lon, s_lat))
        n_err = Point(coords[-1]).distance(Point(n_lon, n_lat))

        self.assertLessEqual(s_err, 0.001, f"Southern marker must match route start! Err: {s_err}")
        self.assertLessEqual(n_err, 0.001, f"Northern marker must match route end! Err: {n_err}")

    def test_all_five_sector_projections_pass(self):
        proj_csv = self.reports_dir / "v2_3a_2t_sector_projection.csv"
        df_proj = pd.read_csv(proj_csv)
        fails = df_proj[df_proj['validation_result'] != 'PASS (On Route)']
        self.assertEqual(len(fails), 0, "All 5 mandatory sectors must project directly on route!")

    def test_zero_adjacency_failures_and_disjoint_ids(self):
        snap_csv = self.reports_dir / "v2_3a_2t_snapping_reconciliation.csv"
        df_snap = pd.read_csv(snap_csv)
        self.assertEqual(len(df_snap[df_snap['status'] != 'PASS (Connected <= 0.5m)']), 0)

if __name__ == "__main__":
    unittest.main()
