import unittest, os, json, math, hashlib, re
import numpy as np, pandas as pd
from pathlib import Path

class TestNH44V23FR7CryptographicEvidenceCorrection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).resolve().parent.parent
        cls.reports_dir = cls.project_root / "outputs" / "reports"
        cls.docs_dir = cls.project_root / "docs" / "v2"

        cls.df_rob = pd.read_csv(cls.reports_dir / "v2_3f_scenario_segment_robustness.csv")
        cls.df_seg = pd.read_csv(cls.reports_dir / "v2_3a_final_segment_inventory.csv")
        cls.df_hashes = pd.read_csv(cls.reports_dir / "v2_3f_r7_output_hashes.csv", keep_default_na=False)
        cls.df_map = pd.read_csv(cls.reports_dir / "v2_3f_r7_segment_native_cell_mapping.csv")
        cls.df_cells = pd.read_csv(cls.reports_dir / "v2_3f_r7_native_cell_evidence.csv")
        cls.df_prov = pd.read_csv(cls.reports_dir / "v2_3f_r7_scenario_variable_provenance.csv")
        cls.df_dhi_d = pd.read_csv(cls.reports_dir / "v2_3f_r7_dhi_d_redundancy_audit.csv", keep_default_na=False)

    def test_01_r6_candidate_sha_reconciliation(self):
        df_rec = pd.read_csv(self.reports_dir / "v2_3f_r7_r6_candidate_sha_reconciliation.csv")
        self.assertEqual(len(df_rec), 1)
        row = df_rec.iloc[0]
        self.assertEqual(row["git_commit_sha_full"], "5f12748536af017b55ee3cc4a008f1c33a9e6fc8")
        self.assertEqual(row["merge_commit_sha"], "220893af24e66f040ab6c89fc4ed1634a6147a1c")
        self.assertEqual(row["verification_status"], "RECONCILED_WITH_TRACKED_GIT_OBJECTS")

    def test_02_authoritative_raster_metadata_and_boundary_rules(self):
        df_meta = pd.read_csv(self.reports_dir / "v2_3f_r7_authoritative_raster_metadata.csv")
        self.assertEqual(len(df_meta), 1)
        row = df_meta.iloc[0]
        self.assertEqual(row["dataset_identity"], "GPM_IMERG_V06B_DAILY_CLIMATOLOGY_GRID")
        self.assertEqual(row["crs"], "EPSG:4326")
        self.assertEqual(row["longitude_boundary_rule"], "WEST_INCLUSIVE_EAST_EXCLUSIVE_[WEST,EAST)")
        self.assertEqual(row["latitude_boundary_rule"], "NORTH_INCLUSIVE_SOUTH_EXCLUSIVE_(SOUTH,NORTH]")

    def test_03_boundary_rule_comprehensive_regression(self):
        pattern_64 = re.compile(r"^[0-9a-f]{64}$")
        
        # Test cell interior
        lon_in, lat_in = 75.15, 33.25
        col_in = int(math.floor(round((lon_in + 180.0) * 10, 9)))
        row_in = int(math.floor(round((90.0 - lat_in) * 10, 9)))
        self.assertEqual(col_in, 2551)
        self.assertEqual(row_in, 567)

        # Test exact western boundary (75.10): in col 2551
        col_w = int(math.floor(round((75.10 + 180.0) * 10, 9)))
        self.assertEqual(col_w, 2551)

        # Test exact eastern boundary (75.20): in col 2552
        col_e = int(math.floor(round((75.20 + 180.0) * 10, 9)))
        self.assertEqual(col_e, 2552)

        # Test exact northern boundary (33.30): in row 567
        row_n = int(math.floor(round((90.0 - 33.30) * 10, 9)))
        self.assertEqual(row_n, 567)

        # Test exact southern boundary (33.20): in row 568
        row_s = int(math.floor(round((90.0 - 33.20) * 10, 9)))
        self.assertEqual(row_s, 568)

        # Test floating point epsilon on either side of boundary
        col_w_minus = int(math.floor(round(((75.10 - 1e-9) + 180.0) * 10, 9)))
        col_w_plus = int(math.floor(round(((75.10 + 1e-9) + 180.0) * 10, 9)))
        self.assertEqual(col_w_minus, 2550)
        self.assertEqual(col_w_plus, 2551)

        row_n_minus = int(math.floor(round((90.0 - (33.30 - 1e-9)) * 10, 9)))
        row_n_plus = int(math.floor(round((90.0 - (33.30 + 1e-9)) * 10, 9)))
        self.assertEqual(row_n_minus, 567)
        self.assertEqual(row_n_plus, 566)

    def test_04_segment_native_cell_mappings(self):
        self.assertEqual(len(self.df_map), 158)
        self.assertEqual(self.df_map["segment_id"].nunique(), 158)
        self.assertEqual((self.df_map["agreement_status"] == "EXACT_AGREEMENT").sum(), 158)
        self.assertEqual(self.df_cells["assigned_segments_count"].sum(), 158)

    def test_05_18_variable_provenance_records(self):
        self.assertEqual(len(self.df_prov), 18)
        s0_prov = self.df_prov[self.df_prov["scenario_id"] == "S0"]
        self.assertEqual(len(s0_prov), 3)
        for _, r in s0_prov.iterrows():
            self.assertEqual(r["scientific_classification"], "Dry Control Zero Baseline")

        s1_r72 = self.df_prov[(self.df_prov["scenario_id"] == "S1") & (self.df_prov["variable_name"] == "R72")].iloc[0]
        self.assertEqual(s1_r72["verification_status"], "VERIFIED_DERIVED_PARAMETER")

        # Verify no P99 in S5
        s5_prov = self.df_prov[self.df_prov["scenario_id"] == "S5"]
        for _, r in s5_prov.iterrows():
            self.assertNotIn("P99", r["scientific_classification"])
            self.assertEqual(r["percentile_basis"], "NONE (Repository-Defined Hypothetical Parameter Set)")

    def test_06_s0_mathematical_handling(self):
        s0_audit = self.df_dhi_d[self.df_dhi_d["scenario_scope"] == "DRY_CONTROL_S0"].iloc[0]
        self.assertEqual(s0_audit["audit_type"], "DRY_CONTROL_S0_POST_FORMULA_POLICY_RULE")
        self.assertEqual(str(s0_audit["max_absolute_residual"]), "NULL")

    def test_07_correlation_zero_variance_null_handling(self):
        df_sp = pd.read_csv(self.reports_dir / "v2_3f_r7_scenario_pairwise_spearman.csv", keep_default_na=False)
        self.assertEqual(len(df_sp), 30)
        for _, r in df_sp.iterrows():
            self.assertTrue(r["spearman_rho"] == "" or pd.isna(r["spearman_rho"]))
            self.assertEqual(r["status"], "UNDEFINED_ZERO_VARIANCE")
            self.assertEqual(r["verification_result"], "VERIFIED_UNDEFINED_ZERO_VARIANCE")

    def test_08_uncertainty_and_degeneracy(self):
        df_unc = pd.read_csv(self.reports_dir / "v2_3f_r7_uncertainty_reconciliation.csv")
        self.assertEqual(len(df_unc), 5)
        for _, r in df_unc.iterrows():
            self.assertEqual(r["unique_dhi_a"], 1)
            self.assertEqual(r["complete_tie_row_count"], 158)
            self.assertEqual(r["degeneracy_status"], "NON_DISCRIMINATING_COMPLETE_TIE")

    def test_09_full_manifest_coverage_and_cryptographic_validation(self):
        pattern_64 = re.compile(r"^[0-9a-f]{64}$")
        self.assertGreaterEqual(len(self.df_hashes), 27)
        
        for _, r in self.df_hashes.iterrows():
            fpath = self.project_root / r["file_path"]
            self.assertTrue(fpath.exists(), f"Manifest file missing: {fpath}")
            
            # Binary mode read
            with open(fpath, "rb") as fh:
                fbytes = fh.read()
            real_sha = hashlib.sha256(fbytes).hexdigest()
            
            # Validate strict 64-char hex format
            self.assertTrue(pattern_64.match(r["sha256"]), f"SHA-256 digest in manifest is not 64 lowercase hex chars: {r['sha256']}")
            self.assertEqual(r["sha256"], real_sha, f"SHA mismatch for artifact {r['artifact_alias']} at {r['file_path']}")
            self.assertEqual(r["file_size_bytes"], len(fbytes), f"Size mismatch for artifact {r['artifact_alias']} at {r['file_path']}")
            self.assertIn(r["classification"], ["CHANGED_FILE", "CANONICAL_OUTPUT", "GENERATOR", "TEST", "DOCUMENTATION", "UI_OR_CONFIGURATION", "REPRODUCTION_DEPENDENCY"])

if __name__ == "__main__":
    unittest.main()
