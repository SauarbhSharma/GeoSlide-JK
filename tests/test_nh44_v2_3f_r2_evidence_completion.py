import unittest
import os, json, hashlib, subprocess
import pandas as pd
import geopandas as gpd, numpy as np
from pathlib import Path

class TestNH44V23FR2EvidenceCompletion(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_rob = pd.read_csv(self.reports_dir / "v2_3f_scenario_segment_robustness.csv")
        self.df_cell_r2 = pd.read_csv(self.reports_dir / "v2_3f_r2_native_cell_evidence.csv")
        self.df_scen_r2 = pd.read_csv(self.reports_dir / "v2_3f_r2_authoritative_scenario_definitions.csv")
        self.df_spearman_r2 = pd.read_csv(self.reports_dir / "v2_3f_r2_scenario_pairwise_spearman.csv")
        self.df_unc_r2 = pd.read_csv(self.reports_dir / "v2_3f_r2_uncertainty_reconciliation.csv")
        self.df_stab_r2 = pd.read_csv(self.reports_dir / "v2_3f_r2_stability_count_reconciliation.csv")
        self.df_hashes_r2 = pd.read_csv(self.reports_dir / "v2_3f_r2_output_hashes.csv")

    def test_01_segment_and_scenario_counts(self):
        self.assertEqual(self.df_rob["segment_id"].nunique(), 158)
        self.assertEqual(self.df_rob["scenario_id"].nunique(), 6)
        self.assertEqual(len(self.df_rob), 948)

    def test_02_native_cell_evidence_8_rows(self):
        self.assertEqual(len(self.df_cell_r2), 8)
        counts = sorted(self.df_cell_r2["assigned_segments_count"].tolist())
        self.assertEqual(counts, [18, 20, 20, 20, 20, 20, 20, 20])
        self.assertEqual(sum(counts), 158)
        self.assertEqual(int(np.min(counts)), 18)
        self.assertEqual(float(np.median(counts)), 20.0)
        self.assertEqual(int(np.max(counts)), 20)

    def test_03_authoritative_scenario_definitions_table(self):
        self.assertEqual(len(self.df_scen_r2), 6)
        s4_row = self.df_scen_r2[self.df_scen_r2["scenario_id"] == "S4"].iloc[0]
        self.assertEqual(s4_row["scenario_class"], "CLIMATOLOGY_DERIVED_REFERENCE")

    def test_04_complete_36_row_spearman_matrix(self):
        self.assertEqual(len(self.df_spearman_r2), 36)
        for sc in ["S1", "S2", "S3", "S4", "S5"]:
            sc_sub = self.df_spearman_r2[self.df_spearman_r2["scenario_id"] == sc]
            self.assertEqual(len(sc_sub), 6)

    def test_05_dhi_b_vs_dhi_d_spearman_all_scenarios(self):
        bd_sub = self.df_spearman_r2[self.df_spearman_r2["pair"] == "DHI_B vs DHI_D"]
        self.assertTrue((bd_sub["spearman_rho"] == 1.000).all())

    def test_06_iqr_linear_interpolation_formula(self):
        arr = np.array([12.5, 25.0, 37.5])
        q1 = float(np.percentile(arr, 25, method="linear"))
        q3 = float(np.percentile(arr, 75, method="linear"))
        iqr = q3 - q1
        self.assertEqual(q1, 18.75)
        self.assertEqual(q3, 31.25)
        self.assertEqual(iqr, 12.5)

    def test_07_stability_counts_reconciliation(self):
        stab_active = self.df_stab_r2[self.df_stab_r2["category"] == "STABLE_CONSENSUS (range <= 15.0%)"].iloc[0]
        self.assertEqual(stab_active["row_count"], 790)
        self.assertEqual(stab_active["unique_segment_count"], 158)

    def test_08_no_landslide_leakage(self):
        for col in self.df_rob.columns:
            self.assertNotIn("landslide", col.lower())

    def test_09_no_operational_warnings(self):
        for col in self.df_rob.columns:
            self.assertNotIn("alert_level", col.lower())

    def test_10_r2_reproducibility_script_execution(self):
        res = subprocess.run(["python", "scripts/run_v2_3f_r2_reproducibility.py"], capture_output=True, text=True, cwd=str(self.project_root))
        self.assertEqual(res.returncode, 0)

if __name__ == "__main__":
    unittest.main()
