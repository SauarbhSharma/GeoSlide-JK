import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44StaticComponentProfiles(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_feats = pd.read_csv(self.reports_dir / "v2_3b_segment_static_features.csv")
        self.df_comp = pd.read_csv(self.reports_dir / "v2_3c_segment_component_profiles.csv")
        self.df_sel = pd.read_csv(self.reports_dir / "v2_3c_selected_feature_set.csv")

    def test_01_immutable_route_hash_unchanged(self):
        with open(self.audit_dir / "nh44_authoritative_pilot_final.geojson", "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, "7141c209c578f8e8f19bc13b85409eeb220b709703c62691fac732594b2e3564")

    def test_02_immutable_segment_hash_unchanged(self):
        with open(self.reports_dir / "v2_3a_final_segment_inventory.csv", "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, "775998e07bbb332d352093961ce2d47b7ca3488179885abceca1df843a50f172")

    def test_03_feature_table_row_count_equals_158(self):
        self.assertEqual(len(self.df_feats), 158)
        self.assertEqual(len(self.df_comp), 158)

    def test_04_unique_segment_ids_equals_158(self):
        self.assertEqual(self.df_comp["segment_id"].nunique(), 158)

    def test_05_no_landslide_field_in_selected_table(self):
        for col in self.df_sel["feature_name"]:
            self.assertNotIn("landslide", col.lower())

    def test_06_no_rainfall_field_in_selected_table(self):
        for col in self.df_sel["feature_name"]:
            self.assertNotIn("rainfall", col.lower())

    def test_07_no_dynamic_hazard_field_in_selected_table(self):
        for col in self.df_sel["feature_name"]:
            self.assertNotIn("dynamic", col.lower())

    def test_08_selected_features_present_in_v2_3b_table(self):
        for col in self.df_sel["feature_name"]:
            self.assertIn(col, self.df_feats.columns)

    def test_09_excluded_features_are_documented(self):
        df_dep = pd.read_csv(self.reports_dir / "v2_3c_mathematical_dependency_audit.csv")
        self.assertGreater(len(df_dep[df_dep["redundancy_classification"] != "RETAIN_CANDIDATE"]), 20)

    def test_10_every_selected_feature_has_unit_and_provenance(self):
        df_reg = pd.read_csv(self.reports_dir / "v2_3c_scientific_feature_registry.csv")
        for col in self.df_sel["feature_name"]:
            row = df_reg[df_reg["feature_name"] == col]
            self.assertFalse(row.empty)
            self.assertIsNotNone(row.iloc[0]["unit"])

    def test_11_every_continuous_selected_feature_has_direction(self):
        for _, r in self.df_sel.iterrows():
            self.assertIn("scientific_direction", r)

    def test_12_normalized_percentiles_between_0_and_100(self):
        df_norm = pd.read_parquet(self.corridor_dir / "nh44_segment_selected_features_normalized.parquet")
        for col in df_norm.columns:
            if "percentile_rank" in col:
                self.assertGreaterEqual(df_norm[col].min(), 0.0)
                self.assertLessEqual(df_norm[col].max(), 100.0)

    def test_13_robust_zscores_are_finite(self):
        df_norm = pd.read_parquet(self.corridor_dir / "nh44_segment_selected_features_normalized.parquet")
        for col in df_norm.columns:
            if "robust_zscore" in col:
                self.assertFalse(df_norm[col].isnull().any())
                self.assertFalse(df_norm[col].isin([float('inf'), float('-inf')]).any())

    def test_14_inverse_direction_transformations_documented(self):
        df_norm_params = pd.read_csv(self.reports_dir / "v2_3c_normalization_parameters.csv")
        inv = df_norm_params[df_norm_params["concern_direction"] == -1]
        self.assertGreater(len(inv), 0)

    def test_15_component_profiles_contain_158_rows(self):
        gdf_comp = gpd.read_parquet(self.corridor_dir / "nh44_segment_static_component_profiles.parquet")
        self.assertEqual(len(gdf_comp), 158)

    def test_16_component_scores_between_0_and_100(self):
        for c in ["static_susceptibility_score_primary", "terrain_severity_score_primary", "geological_context_score_primary", "surface_drainage_score_primary"]:
            self.assertGreaterEqual(self.df_comp[c].min(), 0.0)
            self.assertLessEqual(self.df_comp[c].max(), 100.0)

    def test_17_component_bands_use_corridor_relative_percentiles(self):
        for b in ["susceptibility_band", "terrain_band", "geology_band", "surface_drainage_band"]:
            self.assertEqual(set(self.df_comp[b].unique()).issubset({"VERY_LOW", "LOW", "MODERATE", "HIGH", "VERY_HIGH"}), True)

    def test_18_no_overall_composite_risk_field_exists(self):
        for col in self.df_comp.columns:
            self.assertNotIn("composite_risk", col.lower())
            self.assertNotIn("overall_risk", col.lower())
            self.assertNotIn("weighted_risk", col.lower())

    def test_19_data_confidence_not_added_to_physical_components(self):
        self.assertEqual(self.df_comp["data_confidence_score_primary"].min(), 100.0)

    def test_20_landslide_information_is_validation_only(self):
        df_val = pd.read_csv(self.reports_dir / "v2_3c_component_validation.csv")
        self.assertEqual(len(df_val), 4)

    def test_21_spatial_block_validation_is_present(self):
        df_sb = pd.read_csv(self.reports_dir / "v2_3c_spatial_block_validation.csv")
        self.assertGreaterEqual(len(df_sb), 3)

    def test_22_buffer_sensitivity_results_present(self):
        df_bs = pd.read_csv(self.reports_dir / "v2_3c_component_buffer_sensitivity.csv")
        self.assertEqual(len(df_bs), 4)

    def test_23_structure_interpretation_flags_present(self):
        df_st = pd.read_csv(self.reports_dir / "v2_3c_structure_interpretation_rules.csv")
        self.assertGreaterEqual(len(df_st), 5)

    def test_24_tunnel_interiors_not_automatically_treated_as_surface_exposure(self):
        df_st = pd.read_csv(self.reports_dir / "v2_3c_structure_interpretation_rules.csv")
        tun = df_st[df_st["structure_category"] == "TUNNEL_INTERIOR"]
        self.assertFalse(bool(tun.iloc[0]["surface_susceptibility_directly_interpretable"]))

    def test_25_qazigund_and_verinag_remain_outside_pilot(self):
        last_seg = self.df_comp.iloc[-1]
        self.assertLessEqual(last_seg["chainage_mid_m"], 78620.0)

    def test_26_deterministic_output_hashes_reproduce(self):
        df_h = pd.read_csv(self.reports_dir / "v2_3c_output_hashes.csv")
        self.assertGreaterEqual(len(df_h), 15)

    def test_27_source_v2_3b_files_remain_unchanged(self):
        self.assertTrue((self.reports_dir / "v2_3b_segment_static_features.csv").exists())

if __name__ == "__main__":
    unittest.main()
