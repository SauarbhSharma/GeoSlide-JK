import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44SegmentFeatures(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_feats = pd.read_csv(self.reports_dir / "v2_3b_segment_static_features.csv")
        self.gdf_feats = gpd.read_parquet(self.corridor_dir / "nh44_segment_static_features.parquet")

    def test_01_static_features_row_count_equals_158(self):
        self.assertEqual(len(self.df_feats), 158)
        self.assertEqual(len(self.gdf_feats), 158)

    def test_02_unique_segment_ids_equals_158(self):
        self.assertEqual(self.df_feats["segment_id"].nunique(), 158)

    def test_03_exported_column_count_equals_92(self):
        self.assertEqual(len(self.df_feats.columns), 92)

    def test_04_no_constant_scientific_features(self):
        f = self.reports_dir / "v2_3b_1_constant_features.csv"
        if f.exists():
            df_const = pd.read_csv(f)
            self.assertEqual(len(df_const), 0)

    def test_05_no_duplicate_feature_columns(self):
        f = self.reports_dir / "v2_3b_1_duplicate_columns.csv"
        if f.exists():
            df_dups = pd.read_csv(f)
            self.assertEqual(len(df_dups), 0)

    def test_06_route_hash_remains_unchanged(self):
        with open(self.audit_dir / "nh44_authoritative_pilot_final.geojson", "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, "7141c209c578f8e8f19bc13b85409eeb220b709703c62691fac732594b2e3564")

    def test_07_segment_semantic_hash_remains_unchanged(self):
        df_seg = pd.read_csv(self.reports_dir / "v2_3a_final_segment_inventory.csv")
        sem_str = df_seg[["segment_id", "sequence_number", "start_chainage_m", "end_chainage_m", "actual_geometry_length_m"]].to_json()
        h = hashlib.sha256(sem_str.encode()).hexdigest()
        self.assertEqual(h, "de25ecf1f4f80450df0f1179e7c18ed26f7dbee6688bbe6c5a4448168105c5bf")

    def test_08_all_metric_distances_calculated_in_epsg_32643(self):
        crs_str = str(self.gdf_feats.crs)
        self.assertTrue("32643" in crs_str or "EPSG:32643" in crs_str)

    def test_09_susceptibility_values_within_valid_range(self):
        for _, r in self.df_feats.iterrows():
            if pd.notnull(r["susceptibility_mean_prob"]):
                self.assertGreaterEqual(r["susceptibility_mean_prob"], 0.0)
                self.assertLessEqual(r["susceptibility_mean_prob"], 1.0)

    def test_10_susceptibility_class_fractions_sum_to_1(self):
        for _, r in self.df_feats.iterrows():
            if pd.notnull(r["susceptibility_very_low_fraction"]):
                s = r["susceptibility_very_low_fraction"] + r["susceptibility_low_fraction"] + r["susceptibility_moderate_fraction"] + r["susceptibility_high_fraction"] + r["susceptibility_very_high_fraction"]
                self.assertAlmostEqual(s, 1.0, places=3)

    def test_11_landcover_fractions_sum_to_1(self):
        for _, r in self.df_feats.iterrows():
            if pd.notnull(r["landcover_builtup_fraction"]):
                s = r["landcover_builtup_fraction"] + r["landcover_cropland_fraction"] + r["landcover_forest_fraction"] + r["landcover_grassland_fraction"] + r["landcover_bareground_fraction"] + r["landcover_water_fraction"] + r["landcover_snow_ice_fraction"]
                self.assertAlmostEqual(s, 1.0, places=3)

    def test_12_structure_fractions_sum_to_1(self):
        for _, r in self.df_feats.iterrows():
            s = r["structure_open_road_fraction"] + r["structure_tunnel_fraction"] + r["structure_bridge_fraction"]
            self.assertAlmostEqual(s, 1.0, places=3)

    def test_13_valid_coverage_percentages_between_0_and_100(self):
        for _, r in self.df_feats.iterrows():
            self.assertGreaterEqual(r["valid_coverage_pct"], 0.0)
            self.assertLessEqual(r["valid_coverage_pct"], 100.0)

    def test_14_landslide_context_excluded_from_model_feature_table(self):
        for col in self.df_feats.columns:
            self.assertNotIn("landslide_count", col)

    def test_15_no_rainfall_or_dynamic_hazard_columns_present(self):
        for col in self.df_feats.columns:
            self.assertNotIn("rainfall", col.lower())
            self.assertNotIn("dynamic", col.lower())

    def test_16_no_final_composite_risk_score_present(self):
        for col in self.df_feats.columns:
            self.assertNotIn("risk_score", col.lower())
            self.assertNotIn("alert_level", col.lower())

if __name__ == "__main__":
    unittest.main()
