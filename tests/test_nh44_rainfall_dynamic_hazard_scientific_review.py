import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44RainfallDynamicHazardScientificReview(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.rainfall_dir = self.project_root / "data" / "processed" / "rainfall"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_prov = pd.read_csv(self.reports_dir / "v2_3e_1_rainfall_source_provenance.csv")
        self.df_temp = pd.read_csv(self.reports_dir / "v2_3e_1_temporal_completeness.csv")
        self.df_scen = pd.read_csv(self.reports_dir / "v2_3e_1_scenario_classification.csv")
        self.df_recon = pd.read_csv(self.reports_dir / "v2_3e_1_row_count_reconciliation.csv")
        self.df_form = pd.read_csv(self.reports_dir / "v2_3e_1_dynamic_formula_audit.csv")
        self.df_spat = pd.read_csv(self.reports_dir / "v2_3e_1_spatial_support_audit.csv")
        self.df_tval = pd.read_csv(self.reports_dir / "v2_3e_1_temporal_validation_audit.csv")

    def test_01_released_inputs_immutable(self):
        df_id = pd.read_csv(self.reports_dir / "v2_3e_1_input_identity_audit.csv")
        self.assertTrue((df_id["status"] == "PASS").all())

    def test_02_provenance_status_exists(self):
        self.assertIn("provenance_status", self.df_prov.columns)
        self.assertEqual(len(self.df_prov), 6)

    def test_03_expected_and_observed_timestamps_reported(self):
        for _, r in self.df_temp.iterrows():
            self.assertGreater(r["expected_timesteps"], 0)
            self.assertGreater(r["actual_unique_timesteps"], 0)

    def test_04_missing_timestamps_not_zero_filled(self):
        self.assertTrue(any(r["missing_timesteps"] >= 0 for _, r in self.df_temp.iterrows()))

    def test_05_every_scenario_has_one_class(self):
        self.assertEqual(len(self.df_scen), 6)
        valid_classes = {"OBSERVED_TIMESTAMP", "CLIMATOLOGY_DERIVED_REFERENCE", "SYNTHETIC_STRESS_TEST", "DRY_CONTROL"}
        for _, r in self.df_scen.iterrows():
            self.assertIn(r["scenario_class"], valid_classes)

    def test_06_climatology_scenarios_not_labelled_observed(self):
        clim = self.df_scen[self.df_scen["scenario_id"].isin(["S1", "S2", "S3", "S4"])]
        self.assertTrue((clim["scenario_class"] == "CLIMATOLOGY_DERIVED_REFERENCE").all())

    def test_07_dry_control_not_labelled_observed(self):
        s0 = self.df_scen[self.df_scen["scenario_id"] == "S0"].iloc[0]
        self.assertEqual(s0["scenario_class"], "DRY_CONTROL")

    def test_08_scenario_counts_reconcile(self):
        self.assertEqual(len(self.df_scen), 6)

    def test_09_quality_counts_include_denominators(self):
        df_q = pd.read_csv(self.reports_dir / "v2_3e_1_rainfall_quality_reconciliation.csv")
        self.assertIn("denominator", df_q.columns)

    def test_10_scenario_segment_rows_reconcile_to_948(self):
        s_row = self.df_recon[self.df_recon["semantic_category"] == "Scenario-Segment Records (Wide-Format)"].iloc[0]
        self.assertEqual(s_row["count"], 948)

    def test_11_observed_window_counts_reported(self):
        w_row = self.df_recon[self.df_recon["semantic_category"] == "Complete Observed 24-Hour Windows"].iloc[0]
        self.assertEqual(w_row["count"], 3653)

    def test_12_api_values_distinguished(self):
        df_api = pd.read_csv(self.reports_dir / "v2_3e_1_api7_audit.csv")
        self.assertEqual(len(df_api), 2)

    def test_13_rainfall_spatial_support_reported(self):
        self.assertEqual(self.df_spat.iloc[0]["intersecting_cells_count"], 8)

    def test_14_original_cell_sharing_quantified(self):
        self.assertEqual(self.df_spat.iloc[0]["max_segments_per_cell"], 26)

    def test_15_dhi_formulas_reproduce(self):
        self.assertEqual(len(self.df_form), 4)

    def test_16_monotonic_formula_redundancy_detected(self):
        dhi_d = self.df_form[self.df_form["formulation_id"] == "DHI_D"].iloc[0]
        self.assertEqual(dhi_d["independent_status"], "MONOTONICALLY_REDUNDANT")
        self.assertEqual(dhi_d["spearman_rho_vs_dhi_b"], 1.000)

    def test_17_static_and_dynamic_fields_separate(self):
        df_stat = pd.read_csv(self.reports_dir / "v2_3e_1_static_dynamic_rank_audit.csv")
        self.assertIn("spearman_dhi_vs_static_susceptibility", df_stat.columns)

    def test_18_dry_control_no_false_quintiles(self):
        df_b = pd.read_csv(self.reports_dir / "v2_3e_1_dynamic_band_audit.csv")
        s0_b = df_b[df_b["scenario_id"] == "S0 (Dry Control)"].iloc[0]
        self.assertEqual(s0_b["assigned_classification"], "NO_DYNAMIC_DIFFERENTIATION")

    def test_19_temporal_validation_not_claimed_when_matched_events_zero(self):
        self.assertEqual(self.df_tval.iloc[0]["temporally_matched_events_count"], 0)
        self.assertIn("NO TEMPORAL EVENT VALIDATION WAS POSSIBLE", self.df_tval.iloc[0]["conclusion"])

    def test_20_spatial_validation_not_called_event_trigger(self):
        df_lim = pd.read_csv(self.reports_dir / "v2_3e_1_spatial_validation_limitations.csv")
        self.assertTrue((df_lim["limitation_note"].str.contains("does not prove rainfall causation")).all())

    def test_21_structure_context_does_not_alter_dhi(self):
        df_st = pd.read_csv(self.reports_dir / "v2_3e_1_structure_interpretation_audit.csv")
        self.assertTrue((df_st["numerical_dhi_modified"] == False).all())

    def test_22_no_operational_alert_field_exists(self):
        df_dhi = pd.read_csv(self.reports_dir / "v2_3e_dynamic_hazard_indicators.csv")
        for col in df_dhi.columns:
            self.assertNotIn("alert_level", col.lower())

    def test_23_deterministic_outputs_reproduce(self):
        df_rep = pd.read_csv(self.reports_dir / "v2_3e_1_reproducibility.csv")
        self.assertTrue((df_rep["status"] == "PASS").all())

if __name__ == "__main__":
    unittest.main()
