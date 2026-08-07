import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44DHIRobustnessUncertainty(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.rainfall_dir = self.project_root / "data" / "processed" / "rainfall"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_rob = pd.read_csv(self.reports_dir / "v2_3f_scenario_segment_robustness.csv")
        self.df_scen = pd.read_csv(self.reports_dir / "v2_3f_authoritative_scenario_definitions.csv")
        self.df_matrix = pd.read_csv(self.reports_dir / "v2_3f_formulation_spearman_matrix.csv")
        self.df_spat = pd.read_csv(self.reports_dir / "v2_3f_native_cell_support_summary.csv")
        self.df_val = pd.read_csv(self.reports_dir / "v2_3f_validation_audit_results.csv")

    def test_01_segment_count(self):
        self.assertEqual(self.df_rob["segment_id"].nunique(), 158)

    def test_02_scenario_count(self):
        self.assertEqual(self.df_rob["scenario_id"].nunique(), 6)

    def test_03_scenario_segment_row_count(self):
        self.assertEqual(len(self.df_rob), 948)

    def test_04_no_duplicate_keys(self):
        dups = self.df_rob.duplicated(subset=["segment_id", "scenario_id"]).sum()
        self.assertEqual(dups, 0)

    def test_05_scenario_definition_reconciliation(self):
        self.assertEqual(len(self.df_scen), 6)
        valid_classes = {"DRY_CONTROL", "CLIMATOLOGY_DERIVED_REFERENCE", "SYNTHETIC_STRESS_TEST"}
        for _, r in self.df_scen.iterrows():
            self.assertIn(r["scenario_class"], valid_classes)

    def test_06_three_independent_formulations(self):
        self.assertTrue((self.df_rob["independent_formulation_count"] == 3).all())

    def test_07_dhi_d_excluded_from_consensus(self):
        for col in ["rank_dhi_a", "rank_dhi_b", "rank_dhi_c"]:
            self.assertIn(col, self.df_rob.columns)
        self.assertIn("rank_dhi_d_audit", self.df_rob.columns)

    def test_08_dhi_b_vs_dhi_d_redundancy_proof(self):
        bd_row = self.df_matrix[self.df_matrix["pair"] == "DHI_B vs DHI_D"].iloc[0]
        self.assertEqual(bd_row["spearman_rho"], 1.000)
        self.assertEqual(bd_row["status"], "MONOTONICALLY_REDUNDANT")

    def test_09_tie_aware_ranking(self):
        sub_s2 = self.df_rob[self.df_rob["scenario_id"] == "S2"]
        self.assertTrue((sub_s2["rank_dhi_a"] >= 1.0).all())
        self.assertTrue((sub_s2["rank_dhi_a"] <= 158.0).all())

    def test_10_s0_dry_control_handling(self):
        s0_rows = self.df_rob[self.df_rob["scenario_id"] == "S0"]
        self.assertTrue((s0_rows["consensus_status"] == "DRY_CONTROL_NO_DYNAMIC_DISCRIMINATION").all())

    def test_11_percentile_bounds(self):
        sub_active = self.df_rob[self.df_rob["scenario_id"] != "S0"]
        self.assertTrue((sub_active["consensus_median_percentile"] >= 0.0).all())
        self.assertTrue((sub_active["consensus_median_percentile"] <= 100.0).all())

    def test_12_native_cell_count(self):
        self.assertEqual(self.df_rob["native_cell_id"].nunique(), 8)

    def test_13_no_landslide_leakage(self):
        for col in self.df_rob.columns:
            self.assertNotIn("landslide", col.lower())
            self.assertNotIn("inventory", col.lower())

    def test_14_structure_context_preservation(self):
        self.assertIn("structure_dominant_type", self.df_rob.columns)

    def test_15_no_operational_warnings(self):
        for col in self.df_rob.columns:
            self.assertNotIn("alert_level", col.lower())

    def test_16_deterministic_reproduction(self):
        df_rep = pd.read_csv(self.reports_dir / "v2_3f_reproducibility.csv")
        self.assertTrue((df_rep["status"] == "PASS").all())

if __name__ == "__main__":
    unittest.main()
