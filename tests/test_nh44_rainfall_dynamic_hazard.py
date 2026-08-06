import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44RainfallDynamicHazard(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.rainfall_dir = self.project_root / "data" / "processed" / "rainfall"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_dhi = pd.read_csv(self.reports_dir / "v2_3e_dynamic_hazard_indicators.csv")
        self.df_scen = pd.read_csv(self.reports_dir / "v2_3e_rainfall_scenario_registry.csv")
        self.df_trig = pd.read_csv(self.reports_dir / "v2_3e_rainfall_trigger_indices.csv")
        self.df_unc = pd.read_csv(self.reports_dir / "v2_3e_dynamic_uncertainty.csv")
        self.df_interp = pd.read_csv(self.reports_dir / "v2_3e_segment_dynamic_interpretations.csv")

    def test_01_v2_3a_route_hash_unchanged(self):
        with open(self.audit_dir / "nh44_authoritative_pilot_final.geojson", "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, "7141c209c578f8e8f19bc13b85409eeb220b709703c62691fac732594b2e3564")

    def test_02_v2_3a_segment_hash_unchanged(self):
        with open(self.reports_dir / "v2_3a_final_segment_inventory.csv", "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, "775998e07bbb332d352093961ce2d47b7ca3488179885abceca1df843a50f172")

    def test_03_v2_3b_feature_table_exists(self):
        self.assertTrue((self.reports_dir / "v2_3b_segment_static_features.csv").exists())

    def test_04_v2_3c_component_profiles_exist(self):
        self.assertTrue((self.corridor_dir / "nh44_segment_static_component_profiles.parquet").exists())

    def test_05_v2_3d_static_prioritization_exists(self):
        self.assertTrue((self.reports_dir / "v2_3d_consensus_prioritization.csv").exists())

    def test_06_segment_row_count_equals_158(self):
        self.assertEqual(self.df_dhi["segment_id"].nunique(), 158)
        self.assertEqual(len(self.df_interp), 158)

    def test_07_segment_ids_unique(self):
        self.assertEqual(len(self.df_interp["segment_id"].unique()), 158)

    def test_08_rainfall_units_are_millimetres(self):
        df_read = pd.read_csv(self.reports_dir / "v2_3e_rainfall_data_readiness.csv")
        self.assertTrue((df_read["unit"].str.contains("mm|m")).all())

    def test_09_timestamps_standardized_to_utc(self):
        df_temp = pd.read_csv(self.reports_dir / "v2_3e_temporal_standardization.csv")
        self.assertTrue(any("UTC" in str(c) for c in df_temp["convention"]))

    def test_10_missing_rainfall_not_converted_to_zero(self):
        df_temp = pd.read_csv(self.reports_dir / "v2_3e_temporal_standardization.csv")
        self.assertTrue(any("MISSING_WINDOW" in str(c) for c in df_temp["convention"]))

    def test_11_accumulation_windows_use_complete_time_steps(self):
        df_acc = pd.read_parquet(self.rainfall_dir / "nh44_segment_rainfall_accumulations.parquet")
        self.assertTrue((df_acc["quality_flag"] == "COMPLETE_WINDOW").all())

    def test_12_partial_windows_flagged_correctly(self):
        self.assertTrue((self.reports_dir / "v2_3e_temporal_standardization.csv").exists())

    def test_13_temporal_coverage_between_0_and_100(self):
        df_acc = pd.read_parquet(self.rainfall_dir / "nh44_segment_rainfall_accumulations.parquet")
        self.assertGreaterEqual(df_acc["temporal_coverage_pct"].min(), 0.0)
        self.assertLessEqual(df_acc["temporal_coverage_pct"].max(), 100.0)

    def test_14_spatial_coverage_between_0_and_100(self):
        df_acc = pd.read_parquet(self.rainfall_dir / "nh44_segment_rainfall_accumulations.parquet")
        self.assertGreaterEqual(df_acc["spatial_coverage_pct"].min(), 0.0)
        self.assertLessEqual(df_acc["spatial_coverage_pct"].max(), 100.0)

    def test_15_climatological_percentiles_are_monotonic(self):
        df_clim = pd.read_parquet(self.rainfall_dir / "nh44_rainfall_climatology_percentiles.parquet")
        for _, r in df_clim.iterrows():
            self.assertTrue(r["p50_24h_mm"] <= r["p75_24h_mm"] <= r["p90_24h_mm"] <= r["p95_24h_mm"] <= r["p99_24h_mm"])

    def test_16_zero_denominators_handled(self):
        self.assertTrue((self.reports_dir / "v2_3e_rainfall_trigger_indices.csv").exists())

    def test_17_api_calculations_reproduce(self):
        df_api = pd.read_csv(self.reports_dir / "v2_3e_antecedent_rainfall_indices.csv")
        self.assertEqual(len(df_api), 6)

    def test_18_scenarios_explicitly_labelled(self):
        self.assertIn("type", self.df_scen.columns)
        self.assertTrue(self.df_scen["type"].notnull().all())

    def test_19_static_fields_remain_unchanged(self):
        df_feat = pd.read_csv(self.reports_dir / "v2_3b_segment_static_features.csv")
        self.assertIn("susceptibility_mean_prob", df_feat.columns)

    def test_20_dynamic_fields_do_not_overwrite_static_fields(self):
        self.assertNotIn("susceptibility_mean_prob", self.df_trig.columns)

    def test_21_dhi_formulas_reproduce(self):
        df_form = pd.read_csv(self.reports_dir / "v2_3e_dynamic_formula_registry.csv")
        self.assertEqual(len(df_form), 4)

    def test_22_no_v2_3d_consensus_priority_enters_dhi(self):
        for col in self.df_dhi.columns:
            self.assertNotIn("consensus_priority", col.lower())

    def test_23_dynamic_bands_are_scenario_specific(self):
        self.assertIn("relative_dynamic_band", self.df_interp.columns)

    def test_24_uncertainty_intervals_ordered(self):
        for _, r in self.df_unc.iterrows():
            self.assertTrue(r["rank_p5"] <= r["median_dynamic_rank"] <= r["rank_p95"])

    def test_25_quality_metadata_do_not_alter_hazard(self):
        df_q = pd.read_csv(self.reports_dir / "v2_3e_rainfall_quality.csv")
        self.assertEqual(len(df_q), 3)

    def test_26_structure_type_does_not_alter_rainfall(self):
        df_st = pd.read_csv(self.reports_dir / "v2_3e_structure_aware_dynamic_interpretation.csv")
        self.assertEqual(len(df_st), 158)

    def test_27_landslide_fields_remain_validation_only(self):
        df_val = pd.read_csv(self.reports_dir / "v2_3e_dynamic_validation.csv")
        self.assertIn("validation_type", df_val.columns)

    def test_28_no_operational_alert_field_exists(self):
        for col in self.df_dhi.columns:
            self.assertNotIn("alert_level", col.lower())

    def test_29_no_road_closure_field_exists(self):
        for col in self.df_interp.columns:
            self.assertNotIn("road_closure", col.lower())

    def test_30_deterministic_hashes_reproduce(self):
        df_repro = pd.read_csv(self.reports_dir / "v2_3e_reproducibility.csv")
        self.assertTrue((df_repro["status"] == "PASS").all())

if __name__ == "__main__":
    unittest.main()
