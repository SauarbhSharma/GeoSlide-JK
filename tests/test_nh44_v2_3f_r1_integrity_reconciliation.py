import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd, numpy as np
from pathlib import Path

class TestNH44V23FR1IntegrityReconciliation(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_rob = pd.read_csv(self.reports_dir / "v2_3f_scenario_segment_robustness.csv")
        self.df_cell_r1 = pd.read_csv(self.reports_dir / "v2_3f_r1_native_cell_reconciliation.csv")
        self.df_spearman_r1 = pd.read_csv(self.reports_dir / "v2_3f_r1_scenario_pairwise_spearman.csv")
        self.df_unc_r1 = pd.read_csv(self.reports_dir / "v2_3f_r1_uncertainty_reconciliation.csv")
        self.df_stab_r1 = pd.read_csv(self.reports_dir / "v2_3f_r1_stability_count_reconciliation.csv")
        self.df_val_r1 = pd.read_csv(self.reports_dir / "v2_3f_r1_validation_audit_results.csv")

    def test_01_segment_and_scenario_counts(self):
        self.assertEqual(self.df_rob["segment_id"].nunique(), 158)
        self.assertEqual(self.df_rob["scenario_id"].nunique(), 6)
        self.assertEqual(len(self.df_rob), 948)

    def test_02_native_cell_reconciliation_vector(self):
        counts = sorted(self.df_cell_r1["assigned_segments_count"].tolist())
        self.assertEqual(counts, [18, 20, 20, 20, 20, 20, 20, 20])
        self.assertEqual(sum(counts), 158)
        self.assertEqual(int(np.min(counts)), 18)
        self.assertEqual(float(np.median(counts)), 20.0)
        self.assertEqual(int(np.max(counts)), 20)

    def test_03_complete_six_pair_spearman_coverage(self):
        # 5 active scenarios S1-S5 x 6 pairs = 30 rows, plus 6 pooled rows = 36 total rows
        self.assertEqual(len(self.df_spearman_r1), 36)
        s2_pairs = self.df_spearman_r1[self.df_spearman_r1["scenario_id"] == "S2"]
        self.assertEqual(len(s2_pairs), 6)

    def test_04_dhi_b_vs_dhi_d_spearman_equals_1_000(self):
        s2_bd = self.df_spearman_r1[(self.df_spearman_r1["scenario_id"] == "S2") & (self.df_spearman_r1["pair"] == "DHI_B vs DHI_D")].iloc[0]
        self.assertEqual(s2_bd["spearman_rho"], 1.000)
        self.assertEqual(s2_bd["status"], "MONOTONICALLY_REDUNDANT")

    def test_05_iqr_numerical_example(self):
        # Verify 3-item quantile calculation formula: numpy.percentile([10, 20, 30], 75) - numpy.percentile([10, 20, 30], 25) = 10.0
        arr = np.array([10.0, 20.0, 30.0])
        iqr = float(np.percentile(arr, 75) - np.percentile(arr, 25))
        self.assertEqual(iqr, 10.0)

    def test_06_stability_row_vs_segment_counts(self):
        active_row = self.df_stab_r1[self.df_stab_r1["category"] == "STABLE_CONSENSUS (range <= 15.0%)"].iloc[0]
        self.assertEqual(active_row["row_count"], 790)
        self.assertEqual(active_row["unique_segment_count"], 158)

    def test_07_no_landslide_leakage(self):
        for col in self.df_rob.columns:
            self.assertNotIn("landslide", col.lower())

    def test_08_no_operational_warnings(self):
        for col in self.df_rob.columns:
            self.assertNotIn("alert_level", col.lower())

    def test_09_v2_3f_r1_validation_status(self):
        self.assertTrue((self.df_val_r1["status"] == "PASS").all())

if __name__ == "__main__":
    unittest.main()
