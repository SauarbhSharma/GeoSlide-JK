import unittest
import os, json, hashlib, subprocess
import pandas as pd
import geopandas as gpd, numpy as np
from pathlib import Path

class TestNH44V23FR4ReleaseIntegrity(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"

        self.df_rob = pd.read_csv(self.reports_dir / "v2_3f_scenario_segment_robustness.csv")
        self.df_native = pd.read_csv(self.reports_dir / "v2_3f_r4_native_gpm_cell_evidence.csv")
        self.df_support = pd.read_csv(self.reports_dir / "v2_3f_r4_derived_support_location_evidence.csv")
        self.df_mapping_native = pd.read_csv(self.reports_dir / "v2_3f_r4_segment_native_cell_mapping.csv")
        self.df_mapping_support = pd.read_csv(self.reports_dir / "v2_3f_r4_segment_support_location_mapping.csv")
        self.df_scen = pd.read_csv(self.reports_dir / "v2_3f_r4_authoritative_scenario_definitions.csv")
        self.df_spearman = pd.read_csv(self.reports_dir / "v2_3f_r4_scenario_pairwise_spearman.csv", keep_default_na=False)
        self.df_unc = pd.read_csv(self.reports_dir / "v2_3f_r4_uncertainty_reconciliation.csv")
        self.df_dhi_d = pd.read_csv(self.reports_dir / "v2_3f_r4_dhi_d_redundancy_audit.csv")
        self.df_super = pd.read_csv(self.reports_dir / "v2_3f_r4_artifact_supersession_table.csv")

    def test_01_native_gpm_cell_evidence_completeness(self):
        self.assertEqual(len(self.df_native), 2)
        for _, row in self.df_native.iterrows():
            self.assertEqual(len(row["segment_ids_sha256"]), 64)
            self.assertEqual(row["raster_crs"], "EPSG:4326")
            self.assertEqual(row["coordinate_convention"], "CENTER_POINT")
            self.assertEqual(row["longitude_spacing_deg"], 0.10)
            self.assertEqual(row["latitude_spacing_deg"], 0.10)

    def test_02_derived_support_locations_non_overlapping(self):
        self.assertEqual(len(self.df_support), 8)
        counts = sorted(self.df_support["assigned_segments_count"].tolist())
        self.assertEqual(counts, [18, 20, 20, 20, 20, 20, 20, 20])
        self.assertEqual(sum(counts), 158)
        for _, row in self.df_support.iterrows():
            self.assertEqual(len(row["segment_ids_sha256"]), 64)

    def test_03_segment_mapping_cardinalities(self):
        self.assertEqual(len(self.df_mapping_native), 158)
        self.assertEqual(self.df_mapping_native["segment_id"].nunique(), 158)
        self.assertEqual(len(self.df_mapping_support), 158)
        self.assertEqual(self.df_mapping_support["segment_id"].nunique(), 158)

    def test_04_zero_variance_spearman_undefined_status(self):
        for sc in ["S1", "S2", "S3", "S4", "S5"]:
            sc_sub = self.df_spearman[self.df_spearman["scenario_id"] == sc]
            for _, row in sc_sub.iterrows():
                self.assertEqual(row["spearman_rho"], "")
                self.assertEqual(row["status"], "UNDEFINED_ZERO_VARIANCE")
                self.assertEqual(row["reason"], "CONSTANT_INPUT_VECTOR")
                self.assertEqual(row["verification_status"], "VERIFIED_UNDEFINED_ZERO_VARIANCE")

    def test_05_dhi_d_exact_redundancy_and_exclusion(self):
        dhi_b_vals = self.df_rob["dhi_b"].values
        dhi_d_vals = self.df_rob["dhi_d"].values
        res = np.max(np.abs(dhi_d_vals - np.sqrt(dhi_b_vals)))
        self.assertLess(res, 1e-4)

        dhi_d_row = self.df_dhi_d.iloc[0]
        self.assertLess(dhi_d_row["max_absolute_residual"], 1e-4)
        self.assertEqual(dhi_d_row["consensus_exclusion_action"], "EXCLUDED_FROM_ALL_CONSENSUS_RANGE_IQR_AND_STABILITY")

    def test_06_scenario_input_source_and_key_existence(self):
        for _, row in self.df_scen.iterrows():
            src_path = self.project_root / row["input_source"]
            self.assertTrue(src_path.exists(), f"Input source file does not exist: {src_path}")
            self.assertIn("exact_key_or_column", row)
            self.assertIn("literal_source_value", row)

    def test_07_uncertainty_and_degeneracy_completeness(self):
        self.assertEqual(len(self.df_unc), 5)
        for _, row in self.df_unc.iterrows():
            self.assertEqual(row["mean_percentile_range"], 0.0)
            self.assertEqual(row["q75_percentile_range"], 0.0)
            self.assertEqual(row["q90_percentile_range"], 0.0)
            self.assertEqual(row["q95_percentile_range"], 0.0)
            self.assertEqual(row["max_percentile_range"], 0.0)
            self.assertEqual(row["mean_iqr"], 0.0)
            self.assertEqual(row["degenerate_tied_row_count"], 158)
            self.assertEqual(row["degeneracy_status"], "NON_DISCRIMINATING_COMPLETE_TIE")

    def test_08_r4_reproducibility_script(self):
        res = subprocess.run(["python", "scripts/run_v2_3f_r4_reproducibility.py"], capture_output=True, text=True, cwd=str(self.project_root))
        self.assertEqual(res.returncode, 0)

    def test_09_no_landslide_leakage(self):
        for col in self.df_rob.columns:
            self.assertNotIn("landslide", col.lower())

    def test_10_no_operational_warnings(self):
        for col in self.df_rob.columns:
            self.assertNotIn("alert_level", col.lower())

if __name__ == "__main__":
    unittest.main()
