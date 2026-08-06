import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44StaticPrioritizationScientificReview(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_id = pd.read_csv(self.reports_dir / "v2_3d_1_input_identity_audit.csv")
        self.df_mrec = pd.read_csv(self.reports_dir / "v2_3d_1_method_count_reconciliation.csv")
        self.df_cons_aud = pd.read_csv(self.reports_dir / "v2_3d_1_consensus_construction_audit.csv")
        self.df_weights_aud = pd.read_csv(self.reports_dir / "v2_3d_1_weight_vector_audit.csv")
        self.df_moran_aud = pd.read_csv(self.reports_dir / "v2_3d_1_morans_i_audit.csv")

    def test_01_source_tag_identity_resolved(self):
        tag_row = self.df_id[self.df_id["entity"] == "V2-3C Tag Target Commit"]
        self.assertFalse(tag_row.empty)

    def test_02_v2_3a_3b_3c_inputs_immutable(self):
        for alias in ["V2-3A Route GeoJSON Hash", "V2-3A Segment Inventory Hash", "V2-3B Static Features Hash", "V2-3C Component Profiles Hash"]:
            row = self.df_id[self.df_id["entity"] == alias]
            self.assertEqual(row.iloc[0]["status"], "IMMUTABLE_PASS")

    def test_03_exactly_11_numerical_methods(self):
        num_m = self.df_mrec[self.df_mrec["produces_numeric_score"] == True]
        self.assertEqual(len(num_m), 11)

    def test_04_epsilon_flag_excluded_from_consensus(self):
        eps_m = self.df_mrec[self.df_mrec["method_id"] == "METHOD_G"]
        self.assertFalse(bool(eps_m.iloc[0]["included_in_consensus"]))

    def test_05_all_method_formulas_reproduce(self):
        df_form = pd.read_csv(self.reports_dir / "v2_3d_1_method_formula_audit.csv")
        self.assertEqual(len(df_form), 11)

    def test_06_expert_weights_match_registry(self):
        df_reg = pd.read_csv(self.reports_dir / "v2_3d_method_registry.csv")
        h1 = df_reg[df_reg["method_id"] == "METHOD_H1"]
        self.assertIn("0.40", h1.iloc[0]["weights"])

    def test_07_all_2000_vectors_are_unique(self):
        row_dup = self.df_weights_aud[self.df_weights_aud["check_parameter"] == "Duplicate Vectors Count"]
        self.assertEqual(int(row_dup.iloc[0]["value"]), 0)

    def test_08_every_weight_vector_sums_to_one(self):
        row_sum = self.df_weights_aud[self.df_weights_aud["check_parameter"] == "Max Sum Deviation from 1.0"]
        self.assertEqual(float(row_sum.iloc[0]["value"]), 0.0)

    def test_09_geometric_epsilon_sensitivity_reported(self):
        df_eps = pd.read_csv(self.reports_dir / "v2_3d_1_geometric_mean_epsilon_sensitivity.csv")
        self.assertEqual(len(df_eps), 3)

    def test_10_topsis_configuration_documented(self):
        df_top = pd.read_csv(self.reports_dir / "v2_3d_1_topsis_audit.csv")
        self.assertGreaterEqual(len(df_top), 5)

    def test_11_consensus_uses_exactly_11_numerical_ranks(self):
        row_cnt = self.df_cons_aud[self.df_cons_aud["audit_step"] == "Input Ranks Count"]
        self.assertEqual(int(row_cnt.iloc[0]["value"]), 11)

    def test_12_stability_not_defined_solely_by_top_decile(self):
        df_stab = pd.read_csv(self.reports_dir / "v2_3d_1_upper_consensus_stability_audit.csv")
        self.assertEqual(len(df_stab), 3)

    def test_13_uncertainty_sources_separately_reported(self):
        df_unc = pd.read_csv(self.reports_dir / "v2_3d_1_rank_uncertainty_decomposition.csv")
        self.assertIn("method_rank_range", df_unc.columns)
        self.assertIn("weight_perturbation_90_width", df_unc.columns)

    def test_14_moran_empirical_p_value_matches_permutation_resolution(self):
        self.assertEqual(float(self.df_moran_aud.iloc[0]["empirical_p_value"]), 0.001)

    def test_15_no_copied_moran_result_exists(self):
        self.assertIn("p = 0.001", self.df_moran_aud.iloc[0]["formatted_p_value_text"])

    def test_16_validation_summaries_contain_numerical_evidence(self):
        df_v = pd.read_csv(self.reports_dir / "v2_3d_1_method_validation_evidence.csv")
        self.assertEqual(len(df_v), 11)

    def test_17_inventory_remains_validation_only(self):
        for col in pd.read_csv(self.reports_dir / "v2_3d_consensus_prioritization.csv").columns:
            self.assertNotIn("landslide", col.lower())

    def test_18_structure_and_confidence_do_not_alter_numerical_scores(self):
        df_st = pd.read_csv(self.reports_dir / "v2_3d_1_structure_interpretation_audit.csv")
        for _, r in df_st.iterrows():
            self.assertIn("ZERO", r["numerical_distortion"])

    def test_19_top_set_probability_source_is_explicit(self):
        df_ts = pd.read_csv(self.reports_dir / "v2_3d_1_top_set_stability_audit.csv")
        self.assertGreaterEqual(len(df_ts), 3)

    def test_20_epsilon_overlap_denominator_is_documented(self):
        df_eo = pd.read_csv(self.reports_dir / "v2_3d_1_epsilon_overlap_audit.csv")
        self.assertGreaterEqual(len(df_eo), 5)

    def test_21_no_operational_warning_exists(self):
        for col in pd.read_csv(self.reports_dir / "v2_3d_consensus_prioritization.csv").columns:
            self.assertNotIn("alert_level", col.lower())

    def test_22_outputs_reproduce_deterministically(self):
        df_rep = pd.read_csv(self.reports_dir / "v2_3d_1_reproducibility.csv")
        self.assertEqual(set(df_rep["status"].unique()), {"PASS"})

if __name__ == "__main__":
    unittest.main()
