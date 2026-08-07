import unittest
import os, json, hashlib, subprocess
import pandas as pd
import geopandas as gpd, numpy as np
from pathlib import Path

class TestNH44V23FR3ScientificIntegrity(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"

        self.df_rob = pd.read_csv(self.reports_dir / "v2_3f_scenario_segment_robustness.csv")
        self.df_native = pd.read_csv(self.reports_dir / "v2_3f_r3_native_gpm_cell_evidence.csv")
        self.df_support = pd.read_csv(self.reports_dir / "v2_3f_r3_derived_support_location_evidence.csv")
        self.df_mapping = pd.read_csv(self.reports_dir / "v2_3f_r3_segment_native_cell_mapping.csv")
        self.df_scen = pd.read_csv(self.reports_dir / "v2_3f_r3_authoritative_scenario_definitions.csv")
        self.df_spearman = pd.read_csv(self.reports_dir / "v2_3f_r3_scenario_pairwise_spearman.csv", keep_default_na=False)
        self.df_super = pd.read_csv(self.reports_dir / "v2_3f_r3_artifact_supersession_table.csv")

    def test_01_native_gpm_resolution_disambiguation(self):
        self.assertEqual(len(self.df_native), 2)
        cell1 = self.df_native[self.df_native["native_cell_id"] == "GPM_NATIVE_33.25N_75.15E"].iloc[0]
        cell2 = self.df_native[self.df_native["native_cell_id"] == "GPM_NATIVE_33.25N_75.25E"].iloc[0]
        self.assertEqual(cell1["assigned_segments_count"], 98)
        self.assertEqual(cell2["assigned_segments_count"], 60)
        self.assertEqual(cell1["assigned_segments_count"] + cell2["assigned_segments_count"], 158)

    def test_02_derived_support_locations_count(self):
        self.assertEqual(len(self.df_support), 8)
        counts = sorted(self.df_support["assigned_segments_count"].tolist())
        self.assertEqual(counts, [18, 20, 20, 20, 20, 20, 20, 20])
        self.assertEqual(sum(counts), 158)

    def test_03_segment_mapping_cardinality(self):
        self.assertEqual(len(self.df_mapping), 158)
        self.assertEqual(self.df_mapping["segment_id"].nunique(), 158)

    def test_04_zero_variance_spearman_null_handling(self):
        for sc in ["S1", "S2", "S3", "S4", "S5"]:
            sc_sub = self.df_spearman[self.df_spearman["scenario_id"] == sc]
            for _, row in sc_sub.iterrows():
                self.assertEqual(row["spearman_rho"], "")
                self.assertEqual(row["status"], "UNDEFINED_ZERO_VARIANCE")
                self.assertEqual(row["reason"], "CONSTANT_INPUT_VECTOR")

    def test_05_scenario_input_source_existence(self):
        for _, row in self.df_scen.iterrows():
            src_path = self.project_root / row["input_source"]
            self.assertTrue(src_path.exists(), f"Input source file does not exist: {src_path}")

    def test_06_s4_and_s5_classification(self):
        s4 = self.df_scen[self.df_scen["scenario_id"] == "S4"].iloc[0]
        s5 = self.df_scen[self.df_scen["scenario_id"] == "S5"].iloc[0]
        self.assertEqual(s4["scenario_class"], "COMPOUND_STRESS_TEST")
        self.assertEqual(s5["scenario_class"], "SYNTHETIC_STRESS_TEST")

    def test_07_artifact_supersession_table(self):
        self.assertTrue((self.df_super["status"] == "SUPERSEDED_BY_R3").all())

    def test_08_r3_reproducibility_script(self):
        res = subprocess.run(["python", "scripts/run_v2_3f_r3_reproducibility.py"], capture_output=True, text=True, cwd=str(self.project_root))
        self.assertEqual(res.returncode, 0)

    def test_09_no_landslide_leakage(self):
        for col in self.df_rob.columns:
            self.assertNotIn("landslide", col.lower())

    def test_10_no_operational_warnings(self):
        for col in self.df_rob.columns:
            self.assertNotIn("alert_level", col.lower())

if __name__ == "__main__":
    unittest.main()
