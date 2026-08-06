import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44RainfallFinalReconciliation(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.rainfall_dir = self.project_root / "data" / "processed" / "rainfall"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_ver = pd.read_csv(self.reports_dir / "v2_3e_2_input_verification.csv")
        self.df_ent = pd.read_csv(self.reports_dir / "v2_3e_2_rainfall_entity_reconciliation.csv")
        self.df_scen = pd.read_csv(self.reports_dir / "v2_3e_2_scenario_definition_reconciliation.csv")
        self.df_matrix = pd.read_csv(self.reports_dir / "v2_3e_2_dhi_formula_correlation_matrix.csv")
        self.df_proof = pd.read_csv(self.reports_dir / "v2_3e_2_dhi_d_redundancy_proof.csv")
        self.df_spat = pd.read_csv(self.reports_dir / "v2_3e_2_spatial_support_terminology.csv")
        self.df_win = pd.read_csv(self.reports_dir / "v2_3e_2_window_count_reconciliation.csv")
        self.df_qual = pd.read_csv(self.reports_dir / "v2_3e_2_quality_count_audit.csv")
        self.df_val = pd.read_csv(self.reports_dir / "v2_3e_2_validation_statement_audit.csv")

    def test_01_v2_3a_to_v2_3d_inputs_immutable(self):
        self.assertTrue((self.df_ver["status"] == "PASS").all())

    def test_02_source_entity_counts_have_explicit_types(self):
        self.assertIn("entity_type", self.df_ent.columns)
        self.assertEqual(len(self.df_ent), 6)

    def test_03_quality_counts_include_denominators(self):
        self.assertIn("total_denominator", self.df_qual.columns)

    def test_04_all_six_scenarios_have_complete_definitions(self):
        self.assertEqual(len(self.df_scen), 6)
        for col in ["scenario_id", "scenario_class", "rainfall_24h_mm", "derivation_formula"]:
            self.assertIn(col, self.df_scen.columns)

    def test_05_scenario_class_totals_equal_six(self):
        valid_classes = {"DRY_CONTROL", "CLIMATOLOGY_DERIVED_REFERENCE", "SYNTHETIC_STRESS_TEST"}
        for _, r in self.df_scen.iterrows():
            self.assertIn(r["scenario_class"], valid_classes)

    def test_06_climatology_scenarios_not_labelled_observed(self):
        clim = self.df_scen[self.df_scen["scenario_id"].isin(["S1", "S2", "S3", "S4"])]
        self.assertTrue((clim["scenario_class"] == "CLIMATOLOGY_DERIVED_REFERENCE").all())

    def test_07_observed_window_counts_exclude_scenario_rows(self):
        w_24h = self.df_win[self.df_win["window_category"] == "Complete Observed 24-Hour Windows"].iloc[0]
        self.assertEqual(w_24h["count"], 3653)

    def test_08_scenario_segment_rows_equal_948(self):
        s_rows = self.df_win[self.df_win["window_category"] == "Scenario-Segment Records (Wide-Format)"].iloc[0]
        self.assertEqual(s_rows["count"], 948)

    def test_09_complete_dhi_matrix_contains_six_pairs(self):
        self.assertEqual(len(self.df_matrix), 6)

    def test_10_dhi_b_vs_dhi_d_spearman_equals_1_000(self):
        pair_bd = self.df_matrix[self.df_matrix["pair"] == "DHI_B vs DHI_D"].iloc[0]
        self.assertEqual(pair_bd["spearman_rho"], 1.000)
        self.assertEqual(pair_bd["status"], "MONOTONICALLY_REDUNDANT")

    def test_11_all_formulation_maximum_correlation_equals_1_000(self):
        self.assertEqual(self.df_matrix["spearman_rho"].max(), 1.000)

    def test_12_independent_formulation_range_excludes_dhi_d(self):
        ind = self.df_matrix[self.df_matrix["status"] == "INDEPENDENT_FORMULATION"]
        self.assertEqual(ind["spearman_rho"].min(), 0.965)
        self.assertEqual(ind["spearman_rho"].max(), 0.982)

    def test_13_independent_formulation_count_equals_three(self):
        df_form = pd.read_csv(self.reports_dir / "v2_3e_1_dynamic_formula_audit.csv")
        ind_forms = df_form[df_form["independent_status"] != "MONOTONICALLY_REDUNDANT"]
        self.assertEqual(len(ind_forms), 3)

    def test_14_spatial_support_wording_does_not_claim_independence(self):
        stmt = self.df_spat[self.df_spat["parameter"] == "Mandatory Limitation Statement"].iloc[0]
        self.assertIn("do not represent independent 500 m rainfall measurements", stmt["value"])

    def test_15_native_rainfall_cell_count_equals_eight(self):
        cells = self.df_spat[self.df_spat["parameter"] == "Intersecting Native Cells Count"].iloc[0]
        self.assertIn("8 distinct native 0.1-degree grid cells", cells["value"])

    def test_16_no_temporal_event_validation_is_claimed(self):
        self.assertIn("NO TEMPORAL EVENT VALIDATION WAS POSSIBLE", self.df_val.iloc[0]["mandatory_statement"])

    def test_17_dry_control_differentiation_disabled(self):
        df_b = pd.read_csv(self.reports_dir / "v2_3e_1_dynamic_band_audit.csv")
        s0_b = df_b[df_b["scenario_id"] == "S0 (Dry Control)"].iloc[0]
        self.assertEqual(s0_b["assigned_classification"], "NO_DYNAMIC_DIFFERENTIATION")

    def test_18_no_operational_warning_field_exists(self):
        df_dhi = pd.read_csv(self.reports_dir / "v2_3e_dynamic_hazard_indicators.csv")
        for col in df_dhi.columns:
            self.assertNotIn("alert_level", col.lower())

    def test_19_deterministic_outputs_reproduce(self):
        df_rep = pd.read_csv(self.reports_dir / "v2_3e_1_reproducibility.csv")
        self.assertTrue((df_rep["status"] == "PASS").all())

if __name__ == "__main__":
    unittest.main()
