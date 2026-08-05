import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44FinalAuthoritativeBaseline(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.audit_dir = self.project_root / "data" / "audit"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.docs_dir = self.project_root / "docs" / "v2"
        self.screenshots_dir = self.docs_dir / "screenshots" / "v2-3a-final"

    def test_01_exactly_one_authoritative_geometry(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertEqual(len(df_auth), 1)

    def test_02_authoritative_route_is_one_linestring(self):
        gdf = gpd.read_file(self.audit_dir / "nh44_authoritative_pilot_final.geojson")
        self.assertEqual(len(gdf), 1)
        self.assertEqual(gdf.geometry.iloc[0].geom_type, "LineString")

    def test_03_connected_components_is_one(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertEqual(df_auth["connected_components"].iloc[0], 1)

    def test_04_endpoint_count_is_two(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertEqual(df_auth["endpoints"].iloc[0], 2)

    def test_05_branch_node_count_is_zero(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertEqual(df_auth["branch_nodes"].iloc[0], 0)

    def test_06_cycle_count_is_zero(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertEqual(df_auth["cycles"].iloc[0], 0)

    def test_07_repeated_edge_count_is_zero(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertEqual(df_auth["repeated_edges"].iloc[0], 0)

    def test_08_artificial_connector_count_is_zero(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertEqual(df_auth["artificial_connectors"].iloc[0], 0)

    def test_09_vertex_count_matches_manifest(self):
        with open(self.audit_dir / "nh44_authoritative_manifest_final.json", "r", encoding="utf-8") as f:
            manifest = json.load(f)
        gdf = gpd.read_file(self.audit_dir / "nh44_authoritative_pilot_final.geojson")
        self.assertEqual(len(gdf.geometry.iloc[0].coords), manifest["route_vertex_count"])

    def test_10_route_sha256_matches_manifest(self):
        with open(self.audit_dir / "nh44_authoritative_manifest_final.json", "r", encoding="utf-8") as f:
            manifest = json.load(f)
        with open(self.audit_dir / "nh44_authoritative_pilot_final.geojson", "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, manifest["file_hashes"]["final_geojson"])

    def test_11_route_length_matches_active_reports(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertAlmostEqual(df_auth["route_length_km"].iloc[0], 78.619, places=3)

    def test_12_banihal_endpoint_chainage_equals_length(self):
        df_anchors = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_anchors.csv")
        b_end = df_anchors[df_anchors["anchor_id"] == "banihal_pilot_endpoint"].iloc[0]
        self.assertAlmostEqual(b_end["chainage_kilometres"], 78.619, places=3)

    def test_13_udhampur_chainage_is_zero(self):
        df_anchors = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_anchors.csv")
        u_start = df_anchors[df_anchors["anchor_id"] == "udhampur_north_pilot_start"].iloc[0]
        self.assertEqual(u_start["chainage_kilometres"], 0.0)

    def test_14_anchor_order_strictly_monotonic(self):
        df_anchors = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_anchors.csv")
        chainages = list(df_anchors["chainage_kilometres"])
        self.assertEqual(chainages, sorted(chainages))
        self.assertEqual(len(chainages), len(set(chainages)))

    def test_15_route_distance_ge_geodesic_distance(self):
        df_anchors = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_anchors.csv")
        for _, r in df_anchors.iterrows():
            if r["previous_anchor"] != "N/A":
                self.assertGreaterEqual(r["route_minus_geodesic_margin_km"], -0.050)

    def test_16_projected_anchors_on_route(self):
        df_anchors = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_anchors.csv")
        for _, r in df_anchors.iterrows():
            self.assertEqual(r["reference_to_route_distance_m"], 0.0)

    def test_17_banihal_projection_and_endpoint_match(self):
        df_term = pd.read_csv(self.reports_dir / "v2_3a_final_terminal_reference_audit.csv")
        b_proj = df_term[df_term["object_key"] == "banihal_highway_projection"].iloc[0]
        b_end = df_term[df_term["object_key"] == "banihal_pilot_end"].iloc[0]
        self.assertEqual(b_proj["route_chainage_km"], b_end["route_chainage_km"])

    def test_18_qazigund_and_verinag_outside_pilot(self):
        df_term = pd.read_csv(self.reports_dir / "v2_3a_final_terminal_reference_audit.csv")
        q = df_term[df_term["object_key"] == "qazigund_place_reference"].iloc[0]
        v = df_term[df_term["object_key"] == "verinag_place_reference"].iloc[0]
        self.assertFalse(q["included_in_pilot"])
        self.assertFalse(v["included_in_pilot"])

    def test_19_max_authoritative_route_to_source_distance(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertLessEqual(df_auth["maximum_route_to_source_distance_m"].iloc[0], 0.5)

    def test_20_no_anchor_to_anchor_replacement(self):
        gdf = gpd.read_file(self.audit_dir / "nh44_authoritative_pilot_final.geojson")
        self.assertGreater(len(gdf.geometry.iloc[0].coords), 100)

    def test_21_longitude_range_greater_than_0_01(self):
        gdf = gpd.read_file(self.audit_dir / "nh44_authoritative_pilot_final.geojson")
        bounds = gdf.geometry.iloc[0].bounds
        self.assertGreater(bounds[2] - bounds[0], 0.01)

    def test_22_endpoint_geodesic_distance_le_route_length(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertLessEqual(df_auth["endpoint_geodesic_distance_km"].iloc[0], df_auth["route_length_km"].iloc[0])

    def test_23_overall_sinuosity_gt_1_0(self):
        df_auth = pd.read_csv(self.reports_dir / "v2_3a_final_authoritative_geometry.csv")
        self.assertGreater(df_auth["sinuosity"].iloc[0], 1.0)

    def test_24_screenshot_route_sha256_equals_manifest(self):
        df_manifest = pd.read_csv(self.reports_dir / "v2_3a_final_screenshot_manifest.csv")
        with open(self.audit_dir / "nh44_authoritative_manifest_final.json", "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for _, r in df_manifest.iterrows():
            self.assertEqual(r["route_sha256"], manifest["file_hashes"]["final_geojson"])

    def test_25_screenshot_markers_equal_anchors(self):
        df_manifest = pd.read_csv(self.reports_dir / "v2_3a_final_screenshot_manifest.csv")
        for _, r in df_manifest.iterrows():
            self.assertIn("78.619 km", r["displayed_chainages"])

    def test_26_screenshot_titles_equal_authoritative_values(self):
        df_manifest = pd.read_csv(self.reports_dir / "v2_3a_final_screenshot_manifest.csv")
        for _, r in df_manifest.iterrows():
            self.assertAlmostEqual(r["displayed_route_length_km"], 78.619, places=3)

    def test_27_no_active_stale_chainages(self):
        df_stale = pd.read_csv(self.reports_dir / "v2_3a_final_stale_value_scan.csv")
        c_status = df_stale[df_stale["scan_target"].astype(str) == "54.978"]["status"].iloc[0]
        self.assertEqual(c_status, "CLEAN")

    def test_28_source_edge_provenance_statuses_recorded(self):
        df_prov = pd.read_csv(self.reports_dir / "v2_3a_final_source_edge_provenance.csv")
        self.assertGreater(len(df_prov), 0)

    def test_29_unverified_local_objects_labeled_local(self):
        df_prov = pd.read_csv(self.reports_dir / "v2_3a_final_source_edge_provenance.csv")
        for _, r in df_prov.iterrows():
            self.assertEqual(r["source_provenance_status"], "LOCAL REFERENCE — NOT INDEPENDENTLY VERIFIED AS OSM")

    def test_30_only_canonical_geometry_passed_to_segmentation(self):
        gdf_seg = gpd.read_file(self.project_root / "data" / "processed" / "corridor" / "nh44_segments_500m_final.geojson")
        with open(self.audit_dir / "nh44_authoritative_manifest_final.json", "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for _, r in gdf_seg.iterrows():
            self.assertEqual(r["source_route_sha256"], manifest["file_hashes"]["final_geojson"])

if __name__ == "__main__":
    unittest.main()
