import unittest
import os, json, hashlib, subprocess
import pandas as pd
import geopandas as gpd, numpy as np
from pathlib import Path

class TestNH44V23FR5AuthoritativeCorrection(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.reports_dir = self.project_root / "outputs" / "reports"

        self.df_rob = pd.read_csv(self.reports_dir / "v2_3f_scenario_segment_robustness.csv")
        self.df_meta = pd.read_csv(self.reports_dir / "v2_3f_r5_authoritative_raster_metadata.csv")
        self.df_native = pd.read_csv(self.reports_dir / "v2_3f_r5_native_cell_evidence.csv")
        self.df_mapping = pd.read_csv(self.reports_dir / "v2_3f_r5_segment_native_cell_mapping.csv")
        self.df_recon = pd.read_csv(self.reports_dir / "v2_3f_r5_native_mapping_path_reconciliation.csv")
        self.df_support = pd.read_csv(self.reports_dir / "v2_3f_r5_derived_support_location_evidence.csv")
        self.df_scen = pd.read_csv(self.reports_dir / "v2_3f_r5_authoritative_scenario_definitions.csv")
        self.df_var_prov = pd.read_csv(self.reports_dir / "v2_3f_r5_scenario_variable_provenance.csv")
        self.df_spearman = pd.read_csv(self.reports_dir / "v2_3f_r5_scenario_pairwise_spearman.csv", keep_default_na=False)
        self.df_unc = pd.read_csv(self.reports_dir / "v2_3f_r5_uncertainty_reconciliation.csv")
        self.df_dhi_d = pd.read_csv(self.reports_dir / "v2_3f_r5_dhi_d_redundancy_audit.csv")
        self.df_hashes = pd.read_csv(self.reports_dir / "v2_3f_r5_output_hashes.csv")

    def test_01_authoritative_raster_metadata_completeness(self):
        self.assertEqual(len(self.df_meta), 1)
        row = self.df_meta.iloc[0]
        self.assertEqual(row["dataset_identity"], "GPM_IMERG_V06B_DAILY_CLIMATOLOGY_GRID")
        self.assertEqual(row["crs"], "EPSG:4326")
        self.assertEqual(row["coordinate_convention"], "PIXEL_CENTER")
        self.assertEqual(row["representative_point_method"], "SEGMENT_MIDPOINT_INTERSECTION")

    def test_02_native_2d_cell_evidence_cardinality(self):
        self.assertEqual(len(self.df_native), 11)
        sum_segs = self.df_native["assigned_segments_count"].sum()
        self.assertEqual(sum_segs, 158)
        for _, row in self.df_native.iterrows():
            self.assertEqual(len(row["segment_ids_sha256"]), 64)
            self.assertEqual(row["raster_crs"], "EPSG:4326")

    def test_03_segment_mapping_path_reconciliation(self):
        self.assertEqual(len(self.df_mapping), 158)
        self.assertEqual(self.df_mapping["segment_id"].nunique(), 158)
        self.assertTrue((self.df_mapping["agreement_status"] == "EXACT_AGREEMENT").all())
        recon_row = self.df_recon.iloc[0]
        self.assertEqual(recon_row["exact_agreement_count"], 158)
        self.assertEqual(recon_row["discrepancy_count"], 0)

    def test_04_support_locations_role_unproven(self):
        self.assertEqual(len(self.df_support), 8)
        for _, row in self.df_support.iterrows():
            self.assertEqual(row["proven_scientific_role"], "ROLE_UNPROVEN")
            self.assertFalse(row["used_in_scientific_calculation"])

    def test_05_scenario_provenance_and_keys(self):
        self.assertEqual(len(self.df_scen), 6)
        for _, row in self.df_scen.iterrows():
            src_path = self.project_root / row["exact_tracked_source_path"]
            self.assertTrue(src_path.exists(), f"Source file does not exist: {src_path}")
            if row["scenario_id"] in ["S4", "S5"]:
                self.assertEqual(row["scenario_class"], "REPOSITORY_DEFINED_HYPOTHETICAL_STRESS_TEST")
                self.assertIn("NONE", row["percentile_basis"])

    def test_06_zero_variance_spearman_undefined_status(self):
        for sc in ["S1", "S2", "S3", "S4", "S5"]:
            sc_sub = self.df_spearman[self.df_spearman["scenario_id"] == sc]
            for _, row in sc_sub.iterrows():
                self.assertEqual(row["spearman_rho"], "")
                self.assertEqual(row["status"], "UNDEFINED_ZERO_VARIANCE")
                self.assertEqual(row["reason"], "CONSTANT_INPUT_VECTOR")

    def test_07_dhi_d_exact_full_precision_identity(self):
        fp_row = self.df_dhi_d[self.df_dhi_d["audit_type"] == "FULL_PRECISION_MATHEMATICAL_IDENTITY"].iloc[0]
        self.assertEqual(fp_row["max_absolute_residual"], 0.0)
        self.assertEqual(fp_row["verification_status"], "VERIFIED_EXACT_MACHINE_PRECISION")

        ser_row = self.df_dhi_d[self.df_dhi_d["audit_type"] == "PERSISTED_FOUR_DECIMAL_SERIALIZATION"].iloc[0]
        self.assertLess(ser_row["max_absolute_residual"], 1e-4)
        self.assertEqual(ser_row["verification_status"], "ROUNDED_SERIALIZATION_CONSISTENT")

    def test_08_uncertainty_and_degeneracy_completeness(self):
        self.assertEqual(len(self.df_unc), 5)
        for _, row in self.df_unc.iterrows():
            self.assertEqual(row["mean_percentile_range"], 0.0)
            self.assertEqual(row["mean_iqr"], 0.0)
            self.assertEqual(row["degenerate_tied_row_count"], 158)
            self.assertEqual(row["degeneracy_status"], "NON_DISCRIMINATING_COMPLETE_TIE")

    def test_09_full_manifest_coverage_and_reproducibility(self):
        self.assertGreaterEqual(len(self.df_hashes), 25)
        for _, row in self.df_hashes.iterrows():
            fpath = self.project_root / row["file_path"]
            self.assertTrue(fpath.exists(), f"Manifest file missing: {fpath}")
            with open(fpath, "rb") as fh:
                fbytes = fh.read()
            real_sha = hashlib.sha256(fbytes).hexdigest()
            self.assertEqual(row["sha256"], real_sha, f"SHA mismatch for artifact {row['artifact_alias']} at {row['file_path']}")
            self.assertEqual(row["file_size_bytes"], len(fbytes), f"Size mismatch for artifact {row['artifact_alias']} at {row['file_path']}")

    def test_10_no_landslide_leakage_and_warnings(self):
        for col in self.df_rob.columns:
            self.assertNotIn("landslide", col.lower())
            self.assertNotIn("alert_level", col.lower())

if __name__ == "__main__":
    unittest.main()
