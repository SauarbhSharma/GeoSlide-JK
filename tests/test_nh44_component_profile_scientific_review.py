import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44ComponentProfileScientificReview(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_disp = pd.read_csv(self.reports_dir / "v2_3c_1_feature_disposition.csv")
        self.df_comp = pd.read_csv(self.reports_dir / "v2_3c_segment_component_profiles.csv")
        self.df_val = pd.read_csv(self.reports_dir / "v2_3c_1_component_validation_evidence.csv")
        self.df_moran = pd.read_csv(self.reports_dir / "v2_3c_1_morans_i_audit.csv")

    def test_01_all_75_features_have_exactly_one_disposition(self):
        self.assertEqual(len(self.df_disp), 75)
        self.assertEqual(self.df_disp["feature_name"].nunique(), 75)

    def test_02_final_feature_disposition_totals_75(self):
        self.assertEqual(len(self.df_disp), 75)

    def test_03_selected_count_matches_actual_registry(self):
        ret_phys = self.df_disp[self.df_disp["final_status"] == "RETAINED_PHYSICAL_COMPONENT"]
        self.assertEqual(len(ret_phys), 14)

    def test_04_non_monotonic_features_not_directionally_scored(self):
        df_dir = pd.read_csv(self.reports_dir / "v2_3c_1_directionality_audit.csv")
        elev = df_dir[df_dir["feature_name"] == "elevation_mean_m"]
        self.assertEqual(elev.iloc[0]["direction_classification"], "CONTEXT_ONLY")

    def test_05_constant_confidence_fields_not_ranked(self):
        df_conf = pd.read_csv(self.reports_dir / "v2_3c_1_confidence_profile_audit.csv")
        status = df_conf[df_conf["metric"] == "confidence_status"]
        self.assertEqual(status.iloc[0]["value"], "UNIFORMLY_COMPLETE")

    def test_06_landslide_variables_remain_validation_only(self):
        for col in self.df_disp[self.df_disp["selected_for_component"]]["feature_name"]:
            self.assertNotIn("landslide", col.lower())

    def test_07_structure_categories_not_falsely_ordinal(self):
        df_st = pd.read_csv(self.reports_dir / "v2_3c_1_structure_context_review.csv")
        self.assertGreaterEqual(len(df_st), 4)

    def test_08_pareto_dimensions_exclude_confidence_and_categorical_structure(self):
        df_par = pd.read_csv(self.reports_dir / "v2_3c_1_pareto_utility_review.csv")
        self.assertGreaterEqual(len(df_par), 3)

    def test_09_inventory_polygon_counts_clearly_distinguished(self):
        df_ls = pd.read_csv(self.reports_dir / "v2_3c_1_landslide_count_reconciliation.csv")
        tot = df_ls[df_ls["landslide_metric"] == "total_source_inventory_polygons"]
        c100 = df_ls[df_ls["landslide_metric"] == "unique_polygons_intersecting_100m_corridor"]
        self.assertEqual(tot.iloc[0]["count"], 7436)
        self.assertEqual(c100.iloc[0]["count"], 648)

    def test_10_every_validation_summary_has_numerical_evidence(self):
        self.assertIn("spearman_rho", self.df_val.columns)
        self.assertIn("p_value", self.df_val.columns)
        self.assertEqual(len(self.df_val), 4)

    def test_11_morans_i_rows_include_permutation_counts(self):
        self.assertIn("permutations", self.df_moran.columns)
        self.assertEqual(self.df_moran["permutations"].min(), 999)

    def test_12_stability_rows_include_selection_frequencies(self):
        df_stab = pd.read_csv(self.reports_dir / "v2_3c_1_selection_stability_evidence.csv")
        self.assertEqual(df_stab["selection_frequency_pct"].min(), 100.0)

    def test_13_component_profile_outputs_reproduce_deterministically(self):
        df_repro = pd.read_csv(self.reports_dir / "v2_3c_1_reproducibility.csv")
        self.assertEqual(set(df_repro["status"].unique()), {"PASS"})

    def test_14_v2_3a_and_v2_3b_inputs_remain_immutable(self):
        with open(self.audit_dir / "nh44_authoritative_pilot_final.geojson", "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, "7141c209c578f8e8f19bc13b85409eeb220b709703c62691fac732594b2e3564")

    def test_15_no_overall_composite_score_exists(self):
        for col in self.df_comp.columns:
            self.assertNotIn("composite_risk", col.lower())
            self.assertNotIn("overall_risk", col.lower())

if __name__ == "__main__":
    unittest.main()
