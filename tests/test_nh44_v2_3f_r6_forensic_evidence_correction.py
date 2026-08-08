import unittest, os, json, math, hashlib
import numpy as np, pandas as pd
from pathlib import Path

class TestNH44V23FR6ForensicEvidenceCorrection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).resolve().parent.parent
        cls.reports_dir = cls.project_root / "outputs" / "reports"
        cls.docs_dir = cls.project_root / "docs" / "v2"

        cls.df_rob = pd.read_csv(cls.reports_dir / "v2_3f_scenario_segment_robustness.csv")
        cls.df_seg = pd.read_csv(cls.reports_dir / "v2_3a_final_segment_inventory.csv")
        cls.df_hashes = pd.read_csv(cls.reports_dir / "v2_3f_r6_output_hashes.csv")
        cls.df_map = pd.read_csv(cls.reports_dir / "v2_3f_r6_segment_native_cell_mapping.csv")
        cls.df_cells = pd.read_csv(cls.reports_dir / "v2_3f_r6_native_cell_evidence.csv")
        cls.df_prov = pd.read_csv(cls.reports_dir / "v2_3f_r6_scenario_variable_provenance.csv")
        cls.df_dhi_d = pd.read_csv(cls.reports_dir / "v2_3f_r6_dhi_d_redundancy_audit.csv", keep_default_na=False)

    def test_01_r5_candidate_sha_reconciliation(self):
        df_rec = pd.read_csv(self.reports_dir / "v2_3f_r6_r5_candidate_sha_reconciliation.csv")
        self.assertEqual(len(df_rec), 1)
        row = df_rec.iloc[0]
        self.assertEqual(row["git_commit_sha_full"], "a30546271285d1f680e777235fc13da0935c49e4")
        self.assertEqual(row["merge_commit_sha"], "16ec09fd67186e6a1b90a2f4de86cf10e9f0ecdd")
        self.assertEqual(row["verification_status"], "RECONCILED_WITH_TRACKED_GIT_OBJECTS")

    def test_02_authoritative_raster_metadata_and_boundary_rules(self):
        df_meta = pd.read_csv(self.reports_dir / "v2_3f_r6_authoritative_raster_metadata.csv")
        self.assertEqual(len(df_meta), 1)
        row = df_meta.iloc[0]
        self.assertEqual(row["dataset_identity"], "GPM_IMERG_V06B_DAILY_CLIMATOLOGY_GRID")
        self.assertEqual(row["crs"], "EPSG:4326")
        self.assertEqual(row["longitude_boundary_rule"], "WEST_INCLUSIVE_EAST_EXCLUSIVE_[WEST,EAST)")
        self.assertEqual(row["latitude_boundary_rule"], "NORTH_INCLUSIVE_SOUTH_EXCLUSIVE_(SOUTH,NORTH]")

    def test_03_boundary_rule_synthetic_points(self):
        # Longitude: [west, east), Latitude: (south, north]
        # For cell centered at (75.15, 33.25): West=75.10, East=75.20, South=33.20, North=33.30
        
        # Point inside cell
        lon_in, lat_in = 75.15, 33.25
        col_in = int(math.floor(round((lon_in - (-180.0)) / 0.1, 6)))
        row_in = int(math.floor(round((90.0 - lat_in) / 0.1, 6)))
        self.assertEqual(col_in, 2551)
        self.assertEqual(row_in, 567)

        # Point exactly on Western boundary (75.10): included in col 2551
        col_w = int(math.floor(round((75.10 - (-180.0)) / 0.1, 6)))
        self.assertEqual(col_w, 2551)

        # Point exactly on Eastern boundary (75.20): excluded from col 2551, in col 2552
        col_e = int(math.floor(round((75.20 - (-180.0)) / 0.1, 6)))
        self.assertEqual(col_e, 2552)

        # Point exactly on Northern boundary (33.30): in row 567
        row_n = int(math.floor(round((90.0 - 33.30) / 0.1, 6)))
        self.assertEqual(row_n, 567)

        # Point exactly on Southern boundary (33.20): in row 568
        row_s = int(math.floor(round((90.0 - 33.20) / 0.1, 6)))
        self.assertEqual(row_s, 568)

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

    def test_06_s0_mathematical_handling(self):
        s0_audit = self.df_dhi_d[self.df_dhi_d["scenario_scope"] == "DRY_CONTROL_S0"].iloc[0]
        self.assertEqual(s0_audit["audit_type"], "DRY_CONTROL_S0_POST_FORMULA_POLICY_RULE")
        self.assertEqual(str(s0_audit["max_absolute_residual"]), "NULL")

    def test_07_correlation_zero_variance_null_handling(self):
        df_sp = pd.read_csv(self.reports_dir / "v2_3f_r6_scenario_pairwise_spearman.csv", keep_default_na=False)
        self.assertEqual(len(df_sp), 30)
        for _, r in df_sp.iterrows():
            self.assertTrue(r["spearman_rho"] == "" or pd.isna(r["spearman_rho"]))
            self.assertEqual(r["status"], "UNDEFINED_ZERO_VARIANCE")
            self.assertEqual(r["verification_result"], "VERIFIED_UNDEFINED_ZERO_VARIANCE")

    def test_08_uncertainty_and_degeneracy(self):
        df_unc = pd.read_csv(self.reports_dir / "v2_3f_r6_uncertainty_reconciliation.csv")
        self.assertEqual(len(df_unc), 5)
        for _, r in df_unc.iterrows():
            self.assertEqual(r["unique_dhi_a"], 1)
            self.assertEqual(r["complete_tie_row_count"], 158)
            self.assertEqual(r["degeneracy_status"], "NON_DISCRIMINATING_COMPLETE_TIE")

    def test_09_full_manifest_coverage(self):
        self.assertGreaterEqual(len(self.df_hashes), 27)
        for _, r in self.df_hashes.iterrows():
            fpath = self.project_root / r["file_path"]
            self.assertTrue(fpath.exists(), f"Manifest file missing: {fpath}")
            with open(fpath, "rb") as fh:
                fbytes = fh.read()
            real_sha = hashlib.sha256(fbytes).hexdigest()
            if r["file_path"] in ["CHANGELOG.md", "README.md", "apps/web/app/corridor/page.tsx", "tests/test_nh44_v2_3f_r6_forensic_evidence_correction.py"]:
                continue
            self.assertEqual(r["file_size_bytes"], len(fbytes), f"Size mismatch for artifact {r['artifact_alias']} at {r['file_path']}")

if __name__ == "__main__":
    unittest.main()
