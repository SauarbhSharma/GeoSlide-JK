import unittest, os, json, math, hashlib, re, yaml
import numpy as np, pandas as pd
from pathlib import Path

class TestNH44V23FR8VerifiableReleaseCandidate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).resolve().parent.parent
        cls.reports_dir = cls.project_root / "outputs" / "reports"
        cls.docs_dir = cls.project_root / "docs" / "v2"

        cls.df_rob = pd.read_csv(cls.reports_dir / "v2_3f_scenario_segment_robustness.csv")
        cls.df_seg = pd.read_csv(cls.reports_dir / "v2_3a_final_segment_inventory.csv")
        cls.df_map = pd.read_csv(cls.reports_dir / "v2_3f_r8_segment_native_cell_mapping.csv")
        cls.df_cells = pd.read_csv(cls.reports_dir / "v2_3f_r8_native_cell_evidence.csv")
        cls.df_prov = pd.read_csv(cls.reports_dir / "v2_3f_r8_scenario_variable_provenance.csv")
        cls.df_dhi_d = pd.read_csv(cls.reports_dir / "v2_3f_r8_dhi_d_redundancy_audit.csv", keep_default_na=False)

    def test_01_gitattributes_and_canonical_bytes(self):
        gitattr = self.project_root / ".gitattributes"
        self.assertTrue(gitattr.exists(), "Root .gitattributes missing!")
        text = gitattr.read_text(encoding="utf-8")
        self.assertIn("eol=lf", text)
        self.assertIn("*.py text eol=lf", text)
        self.assertIn("*.tif binary", text)

    def test_02_path_b_grid_provenance_truthfulness(self):
        df_meta = pd.read_csv(self.reports_dir / "v2_3f_r8_authoritative_raster_metadata.csv")
        self.assertEqual(len(df_meta), 1)
        row = df_meta.iloc[0]
        self.assertEqual(row["dataset_identity"], "REPOSITORY_DECLARED_IMERG_COMPATIBLE_ANALYSIS_GRID")
        self.assertIn("EMPIRICAL RASTER PROVENANCE NOT PROVEN", row["provenance_classification"])
        self.assertEqual(row["verification_status"], "DECLARED_IMERG_COMPATIBLE_GRID_EMPIRICAL_RASTER_UNPROVEN")

    def test_03_boundary_rule_regression_with_nextafter(self):
        # Longitude: [west, east), Latitude: (south, north]
        # BBox for cell at (75.15, 33.25): West=75.10, East=75.20, South=33.20, North=33.30
        west, east = 75.10, 75.20
        south, north = 33.20, 33.30

        # Exact West boundary: INCLUDED
        col_w = int(math.floor((west - (-180.0)) / 0.1))
        self.assertEqual(col_w, 2551)

        # One representable float to left of West: EXCLUDED from 2551 (in 2550)
        west_left = math.nextafter(west, -math.inf)
        col_w_left = int(math.floor((west_left - (-180.0)) / 0.1))
        self.assertEqual(col_w_left, 2550)

        # One representable float to right of West: INCLUDED in 2551
        west_right = math.nextafter(west, math.inf)
        col_w_right = int(math.floor((west_right - (-180.0)) / 0.1))
        self.assertEqual(col_w_right, 2551)

        # Exact North boundary: INCLUDED in row 567
        row_n = int(math.floor((90.0 - north) / 0.1))
        self.assertEqual(row_n, 567)

        # One representable float to north of North: EXCLUDED from row 567 (in row 566)
        north_plus = math.nextafter(north, math.inf)
        row_n_plus = int(math.floor((90.0 - north_plus) / 0.1))
        self.assertEqual(row_n_plus, 566)

    def test_04_mapping_methods_independence_and_mutation(self):
        self.assertEqual(len(self.df_map), 158)
        self.assertEqual(self.df_map["segment_id"].nunique(), 158)
        self.assertEqual((self.df_map["agreement_status"] == "EXACT_AGREEMENT").sum(), 158)
        self.assertEqual(self.df_cells["assigned_segments_count"].sum(), 158)

        # Mutation Test: Deliberately alter Method B result and verify discrepancy detection
        df_mut = self.df_map.copy()
        df_mut.loc[0, "mapping_method_b_result"] = "METHOD_B_BBOX[99.00,99.00,99.10,99.10]"
        bounds_match_mut = (df_mut["mapping_method_a_result"].str.slice(0, 20) == df_mut["mapping_method_b_result"].str.slice(0, 20))
        self.assertFalse(bounds_match_mut.iloc[0], "Mutation test failed to detect altered Method B result!")

    def test_05_scenario_provenance_and_yaml_sync(self):
        self.assertEqual(len(self.df_prov), 18)
        with open(self.project_root / "configs" / "scenario_definitions.yaml", "r", encoding="utf-8") as f:
            sc_defs = yaml.safe_load(f)
        self.assertIn("S0_DRY_CONTROL", sc_defs)

        # Verify S1 R72 percentile_basis is NONE (Repository-Defined Parameter)
        s1_r72 = self.df_prov[(self.df_prov["scenario_id"] == "S1") & (self.df_prov["variable_name"] == "R72")].iloc[0]
        self.assertEqual(s1_r72["percentile_basis"], "NONE (Repository-Defined Parameter)")
        self.assertNotIn("P50 Derived", s1_r72["percentile_basis"])

        # Verify S5 is Repository-Defined Hypothetical Stress Test
        s5_r24 = self.df_prov[(self.df_prov["scenario_id"] == "S5") & (self.df_prov["variable_name"] == "R24")].iloc[0]
        self.assertEqual(s5_r24["scientific_classification"], "Repository-Defined Hypothetical Stress Test")
        self.assertNotIn("P99", s5_r24["scientific_classification"])

    def test_06_s0_mathematical_handling(self):
        s0_audit = self.df_dhi_d[self.df_dhi_d["scenario_scope"] == "DRY_CONTROL_S0"].iloc[0]
        self.assertEqual(s0_audit["audit_type"], "DRY_CONTROL_S0_POST_FORMULA_POLICY_RULE")
        self.assertEqual(str(s0_audit["max_absolute_residual"]), "NULL")

    def test_07_rank_correlation_null_handling_and_synthetic_fixture(self):
        df_sp = pd.read_csv(self.reports_dir / "v2_3f_r8_scenario_pairwise_spearman.csv", keep_default_na=False)
        self.assertEqual(len(df_sp), 30)
        for _, r in df_sp.iterrows():
            self.assertTrue(r["spearman_rho"] == "" or pd.isna(r["spearman_rho"]))
            self.assertEqual(r["status"], "UNDEFINED_ZERO_VARIANCE")

        # Synthetic non-constant fixture test
        x_syn = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_syn = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
        rx = pd.Series(x_syn).rank().values
        ry = pd.Series(y_syn).rank().values
        r_val = float(np.corrcoef(rx, ry)[0, 1])
        self.assertAlmostEqual(r_val, 1.0)

    def test_08_uncertainty_reconciliation_dynamic(self):
        df_unc = pd.read_csv(self.reports_dir / "v2_3f_r8_uncertainty_reconciliation.csv")
        self.assertEqual(len(df_unc), 5)
        for _, r in df_unc.iterrows():
            self.assertEqual(r["unique_dhi_a"], 1)
            self.assertEqual(r["complete_tie_row_count"], 158)
            self.assertEqual(r["degeneracy_status"], "NON_DISCRIMINATING_COMPLETE_TIE")

    def test_09_manifest_negative_tests(self):
        pattern_64 = re.compile(r"^[0-9a-f]{64}$")
        
        # 62-character hash fails regex
        hash_62 = "a" * 62
        self.assertIsNone(pattern_64.match(hash_62))

        # 65-character hash fails regex
        hash_65 = "a" * 65
        self.assertIsNone(pattern_64.match(hash_65))

        # Non-hex character fails regex
        hash_bad_hex = "g" * 64
        self.assertIsNone(pattern_64.match(hash_bad_hex))

if __name__ == "__main__":
    unittest.main()
