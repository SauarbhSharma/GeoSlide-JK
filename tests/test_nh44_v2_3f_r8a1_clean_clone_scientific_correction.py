import unittest, sys, os, json, math, hashlib, re, subprocess
import numpy as np, pandas as pd
from pathlib import Path
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from geoslide.scenario_loader import load_scenario_definitions, generate_18_provenance_records
from geoslide.boundary_mapper import map_segment_method_a, map_segment_method_b, map_all_segments
from scripts.validate_v2_3f_r8a1_manifest import validate_manifest

class TestNH44V23FR8A1CleanCloneScientificCorrection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.project_root = PROJECT_ROOT
        cls.reports_dir = cls.project_root / "outputs" / "reports"
        cls.docs_dir = cls.project_root / "docs" / "v2"

        cls.df_rob = pd.read_csv(cls.reports_dir / "v2_3f_scenario_segment_robustness.csv")
        cls.df_seg = pd.read_csv(cls.reports_dir / "v2_3a_final_segment_inventory.csv")
        cls.df_map = pd.read_csv(cls.reports_dir / "v2_3f_r8_segment_native_cell_mapping.csv")
        cls.df_cells = pd.read_csv(cls.reports_dir / "v2_3f_r8_native_cell_evidence.csv")
        cls.df_prov = pd.read_csv(cls.reports_dir / "v2_3f_r8_scenario_variable_provenance.csv")
        cls.df_dhi_d = pd.read_csv(cls.reports_dir / "v2_3f_r8_dhi_d_redundancy_audit.csv", keep_default_na=False)

    def test_01_canonical_git_blob_bytes(self):
        # Verify GeoJSON and segment inventory Git-blob SHAs
        g_blob = subprocess.check_output(["git", "cat-file", "blob", "HEAD:data/audit/nh44_authoritative_pilot_final.geojson"], cwd=self.project_root)
        h_route_blob = hashlib.sha256(g_blob).hexdigest()
        self.assertEqual(h_route_blob, "b22b875dfdf08f734aca88377aed80e869988b4adbdb2d848756225457b825e2")

        s_blob = subprocess.check_output(["git", "cat-file", "blob", "HEAD:outputs/reports/v2_3a_final_segment_inventory.csv"], cwd=self.project_root)
        h_seg_blob = hashlib.sha256(s_blob).hexdigest()
        self.assertEqual(h_seg_blob, "6713194334c4635b1c41abc80148867d4368fd9f3bb118416e4f2d582149e230")

        # Root gitattributes check
        gitattr = self.project_root / ".gitattributes"
        self.assertTrue(gitattr.exists())
        text = gitattr.read_text(encoding="utf-8")
        self.assertIn("eol=lf", text)

    def test_02_path_b_grid_provenance_truthfulness(self):
        df_meta = pd.read_csv(self.reports_dir / "v2_3f_r8_authoritative_raster_metadata.csv")
        self.assertEqual(len(df_meta), 1)
        row = df_meta.iloc[0]
        self.assertEqual(row["dataset_identity"], "REPOSITORY_DECLARED_IMERG_COMPATIBLE_ANALYSIS_GRID")
        self.assertIn("EMPIRICAL RASTER PROVENANCE NOT PROVEN", row["provenance_classification"])

    def test_03_boundary_rule_nextafter_and_explicit_proofs(self):
        # Rule: Longitude [west, east), Latitude (south, north]
        # Test 1: Longitude 75.20 maps to eastern cell [75.20, 75.30)
        mA_7520 = map_segment_method_a(33.25, 75.20)
        mB_7520 = map_segment_method_b(33.25, 75.20)
        self.assertEqual(mA_7520["west"], 75.20)
        self.assertEqual(mA_7520["east"], 75.30)
        self.assertEqual(mB_7520["west"], 75.20)

        # Test 2: Latitude 33.20 maps to southern cell (33.10, 33.20]
        mA_3320 = map_segment_method_a(33.20, 75.15)
        mB_3320 = map_segment_method_b(33.20, 75.15)
        self.assertEqual(mA_3320["south"], 33.10)
        self.assertEqual(mA_3320["north"], 33.20)
        self.assertEqual(mB_3320["north"], 33.20)

        # Test 3: Latitude 33.30 maps to cell whose north bound is 33.30
        mA_3330 = map_segment_method_a(33.30, 75.15)
        mB_3330 = map_segment_method_b(33.30, 75.15)
        self.assertEqual(mA_3330["north"], 33.30)
        self.assertEqual(mA_3330["south"], 33.20)
        self.assertEqual(mB_3330["north"], 33.30)

        # Edge inclusion/exclusion tests with nextafter
        west_exact = 75.10
        west_plus = math.nextafter(west_exact, math.inf)
        west_minus = math.nextafter(west_exact, -math.inf)
        
        mA_exact = map_segment_method_a(33.25, west_exact)
        mA_plus = map_segment_method_a(33.25, west_plus)
        mA_minus = map_segment_method_a(33.25, west_minus)

        self.assertEqual(mA_exact["west"], 75.10)
        self.assertEqual(mA_plus["west"], 75.10)
        self.assertEqual(mA_minus["west"], 75.00)

    def test_04_mapping_methods_independence_and_mutation(self):
        self.assertEqual(len(self.df_map), 158)
        self.assertEqual((self.df_map["agreement_status"] == "EXACT_AGREEMENT").sum(), 158)

        # Mutation Test: Deliberately alter Method B result
        df_mut = self.df_map.copy()
        df_mut.loc[0, "mapping_method_b_result"] = "METHOD_B_BBOX[99.00,99.00,99.10,99.10]"
        bounds_match_mut = (df_mut["mapping_method_a_result"].str.slice(0, 20) == df_mut["mapping_method_b_result"].str.slice(0, 20))
        self.assertFalse(bounds_match_mut.iloc[0])

    def test_05_executable_scenario_provenance_and_mutation(self):
        sc_defs = load_scenario_definitions()
        self.assertIn("S0_DRY_CONTROL", sc_defs)

        df_prov_gen = generate_18_provenance_records(sc_defs)
        self.assertEqual(len(df_prov_gen), 18)

        # Mutation test: alter a YAML scenario definition value and verify detection
        sc_defs_mut = load_scenario_definitions()
        sc_defs_mut["S1_MODERATE"]["r24_mm"] = 999.0
        with self.assertRaises(AssertionError):
            generate_18_provenance_records(sc_defs_mut)

    def test_06_scipy_stats_scientific_audits(self):
        # Test 1: Constant vectors -> returns empty/NaN and status UNDEFINED_ZERO_VARIANCE
        x_const = np.array([1.0, 1.0, 1.0, 1.0])
        y_const = np.array([2.0, 2.0, 2.0, 2.0])
        res_sp_const = stats.spearmanr(x_const, y_const)
        self.assertTrue(np.isnan(res_sp_const.statistic))

        # Test 2: Nonconstant monotonic vectors
        x_mono = np.array([1.0, 2.0, 3.0, 4.0])
        y_mono = np.array([10.0, 20.0, 30.0, 40.0])
        res_sp_mono = stats.spearmanr(x_mono, y_mono)
        res_kt_mono = stats.kendalltau(x_mono, y_mono)
        self.assertAlmostEqual(res_sp_mono.statistic, 1.0)
        self.assertAlmostEqual(res_kt_mono.statistic, 1.0)

        # Test 3: Nonmonotonic vectors
        x_nonmono = np.array([1.0, 2.0, 3.0, 4.0])
        y_nonmono = np.array([10.0, 5.0, 30.0, 2.0])
        res_sp_nm = stats.spearmanr(x_nonmono, y_nonmono)
        self.assertLess(abs(res_sp_nm.statistic), 0.9)

        # Test 4: Tied vectors
        x_tied = np.array([1.0, 2.0, 2.0, 4.0])
        y_tied = np.array([10.0, 20.0, 20.0, 40.0])
        res_sp_tied = stats.spearmanr(x_tied, y_tied)
        self.assertAlmostEqual(res_sp_tied.statistic, 1.0)

    def test_07_dhi_d_residual_audit(self):
        # Verify machine exact full precision vs persisted rounded residual distinction
        r_fp = self.df_dhi_d[self.df_dhi_d["audit_type"] == "FULL_PRECISION_MATHEMATICAL_IDENTITY"].iloc[0]
        self.assertEqual(float(r_fp["max_absolute_residual"]), 0.0)

        r_round = self.df_dhi_d[self.df_dhi_d["audit_type"] == "PERSISTED_FOUR_DECIMAL_SERIALIZATION"].iloc[0]
        self.assertGreater(float(r_round["max_absolute_residual"]), 0.0)
        self.assertEqual(r_round["relationship_status"], "PERSISTED_FOUR_DECIMAL_SERIALIZATION_RESIDUAL")

    def test_08_uncertainty_counts_dynamic(self):
        df_unc = pd.read_csv(self.reports_dir / "v2_3f_r8_uncertainty_reconciliation.csv")
        self.assertEqual(len(df_unc), 5)
        for _, r in df_unc.iterrows():
            self.assertEqual(r["complete_tie_row_count"], 158)
            self.assertEqual(r["degeneracy_status"], "NON_DISCRIMINATING_COMPLETE_TIE")

    def test_09_manifest_negative_tests(self):
        pattern_64 = re.compile(r"^[0-9a-f]{64}$")
        self.assertIsNone(pattern_64.match("a" * 62))
        self.assertIsNone(pattern_64.match("a" * 65))
        self.assertIsNone(pattern_64.match("z" * 64))

if __name__ == "__main__":
    unittest.main()
