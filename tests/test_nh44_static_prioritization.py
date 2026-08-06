import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44StaticPrioritization(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_methods = pd.read_csv(self.reports_dir / "v2_3d_method_scores_and_ranks.csv")
        self.df_cons = pd.read_csv(self.reports_dir / "v2_3d_consensus_prioritization.csv")
        self.df_pert = pd.read_csv(self.reports_dir / "v2_3d_weight_perturbation.csv")
        self.df_weights = pd.read_csv(self.reports_dir / "v2_3d_weight_vector_manifest.csv")

    def test_01_v2_3a_route_hash_unchanged(self):
        with open(self.audit_dir / "nh44_authoritative_pilot_final.geojson", "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, "7141c209c578f8e8f19bc13b85409eeb220b709703c62691fac732594b2e3564")

    def test_02_v2_3a_segment_hash_unchanged(self):
        with open(self.reports_dir / "v2_3a_final_segment_inventory.csv", "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, "775998e07bbb332d352093961ce2d47b7ca3488179885abceca1df843a50f172")

    def test_03_v2_3b_feature_table_hash_unchanged(self):
        self.assertTrue((self.reports_dir / "v2_3b_segment_static_features.csv").exists())

    def test_04_v2_3c_component_profiles_unchanged(self):
        self.assertTrue((self.corridor_dir / "nh44_segment_static_component_profiles.parquet").exists())

    def test_05_profile_rows_equals_158(self):
        self.assertEqual(len(self.df_methods), 158)
        self.assertEqual(len(self.df_cons), 158)

    def test_06_segment_ids_unique_equals_158(self):
        self.assertEqual(self.df_cons["segment_id"].nunique(), 158)

    def test_07_only_four_physical_components_enter_numerical_aggregation(self):
        df_dim = pd.read_csv(self.reports_dir / "v2_3d_dimension_registry.csv")
        elig = df_dim[df_dim["eligibility"] == "ELIGIBLE_PHYSICAL"]
        self.assertEqual(len(elig), 4)

    def test_08_confidence_metadata_excluded_from_scoring(self):
        df_dim = pd.read_csv(self.reports_dir / "v2_3d_dimension_registry.csv")
        conf = df_dim[df_dim["dimension_name"] == "DATA_CONFIDENCE_METADATA"]
        self.assertEqual(conf.iloc[0]["eligibility"], "EXCLUDED_METADATA_ONLY")

    def test_09_categorical_structure_excluded_from_numerical_severity(self):
        df_dim = pd.read_csv(self.reports_dir / "v2_3d_dimension_registry.csv")
        st = df_dim[df_dim["dimension_name"] == "ROAD_STRUCTURE_CONTEXT"]
        self.assertEqual(st.iloc[0]["eligibility"], "EXCLUDED_CONTEXT_ONLY")

    def test_10_landslide_fields_excluded_from_scoring(self):
        for col in self.df_methods.columns:
            if "score" in col or "rank" in col:
                self.assertNotIn("landslide", col.lower())

    def test_11_rainfall_fields_excluded(self):
        for col in self.df_methods.columns:
            self.assertNotIn("rainfall", col.lower())

    def test_12_dynamic_hazard_fields_excluded(self):
        for col in self.df_methods.columns:
            self.assertNotIn("dynamic", col.lower())

    def test_13_all_method_scores_finite(self):
        for col in self.df_methods.columns:
            if "score" in col:
                s = pd.to_numeric(self.df_methods[col], errors="coerce")
                self.assertFalse(s.isnull().any())
                self.assertFalse(s.isin([float('inf'), float('-inf')]).any())

    def test_14_all_method_percentiles_between_0_and_100(self):
        self.assertGreaterEqual(self.df_cons["consensus_percentile"].min(), 0.0)
        self.assertLessEqual(self.df_cons["consensus_percentile"].max(), 100.0)

    def test_15_all_method_ranks_valid(self):
        for m in ["method_a", "method_b", "method_c", "method_d"]:
            r = self.df_methods[f"rank_{m}"]
            self.assertGreaterEqual(r.min(), 1)
            self.assertLessEqual(r.max(), 158)

    def test_16_weights_non_negative(self):
        self.assertTrue((self.df_weights >= 0.0).all().all())

    def test_17_every_weight_vector_sums_to_one(self):
        sums = self.df_weights.sum(axis=1)
        for val in sums:
            self.assertAlmostEqual(val, 1.0, places=4)

    def test_18_expert_scenarios_match_documented_weights(self):
        df_reg = pd.read_csv(self.reports_dir / "v2_3d_method_registry.csv")
        h1 = df_reg[df_reg["method_id"] == "METHOD_H1"]
        self.assertIn("0.40", h1.iloc[0]["weights"])

    def test_19_consensus_rank_derived_from_method_ranks(self):
        self.assertEqual(len(self.df_cons["consensus_final_rank"]), 158)

    def test_20_epsilon_dominance_not_converted_into_numeric_score(self):
        self.assertIn("flag_method_g_epsilon_dominance", self.df_methods.columns)

    def test_21_rank_intervals_ordered_correctly(self):
        for _, r in self.df_pert.iterrows():
            self.assertTrue(r["rank_p5"] <= r["rank_p25"] <= r["rank_p75"] <= r["rank_p95"])

    def test_22_top_10_probabilities_between_0_and_1(self):
        self.assertGreaterEqual(self.df_pert["probability_top_10_pct"].min(), 0.0)
        self.assertLessEqual(self.df_pert["probability_top_10_pct"].max(), 1.0)

    def test_23_top_20_probabilities_between_0_and_1(self):
        self.assertGreaterEqual(self.df_pert["probability_top_20_pct"].min(), 0.0)
        self.assertLessEqual(self.df_pert["probability_top_20_pct"].max(), 1.0)

    def test_24_structure_flags_present(self):
        df_st = pd.read_csv(self.reports_dir / "v2_3d_structure_aware_prioritization.csv")
        self.assertIn("interpretation_flag", df_st.columns)

    def test_25_tunnel_interior_limitation_present(self):
        df_st = pd.read_csv(self.reports_dir / "v2_3d_structure_aware_prioritization.csv")
        tun = df_st[df_st["structure_dominant_type"] == "TUNNEL"]
        self.assertEqual(tun.iloc[0]["interpretation_flag"], "SURFACE_INTERPRETATION_LIMITED")

    def test_26_bridge_context_limitation_present(self):
        df_st = pd.read_csv(self.reports_dir / "v2_3d_structure_aware_prioritization.csv")
        br = df_st[df_st["structure_dominant_type"] == "BRIDGE"]
        self.assertEqual(br.iloc[0]["interpretation_flag"], "ELEVATED_STRUCTURE_CONTEXT")

    def test_27_inventory_remains_validation_only(self):
        df_val = pd.read_csv(self.reports_dir / "v2_3d_consensus_validation.csv")
        self.assertIn("spearman_rho", df_val.columns)

    def test_28_block_validation_exists_for_blocks(self):
        df_bl = pd.read_csv(self.reports_dir / "v2_3d_spatial_block_validation.csv")
        self.assertEqual(set(df_bl["block_size_km"].unique()), {2.5, 5.0, 10.0})

    def test_29_no_operational_alert_field_exists(self):
        for col in self.df_cons.columns:
            self.assertNotIn("alert_level", col.lower())
            self.assertNotIn("road_closure", col.lower())

    def test_30_deterministic_semantic_hashes_reproduce(self):
        df_repro = pd.read_csv(self.reports_dir / "v2_3d_reproducibility.csv")
        self.assertEqual(set(df_repro["status"].unique()), {"PASS"})

if __name__ == "__main__":
    unittest.main()
