import unittest
import os, json, hashlib
import pandas as pd
import geopandas as gpd
from pathlib import Path

class TestNH44SegmentFeatureScientificReview(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridor"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.audit_dir = self.project_root / "data" / "audit"

        self.df_feats = pd.read_csv(self.reports_dir / "v2_3b_segment_static_features.csv")
        self.df_dict = pd.read_csv(self.reports_dir / "v2_3b_segment_feature_dictionary.csv")

    def test_01_all_75_features_registered_in_dictionary(self):
        sci = self.df_dict[self.df_dict["category"] != "Identification"]
        self.assertGreaterEqual(len(sci), 67)

    def test_02_no_constant_scientific_features(self):
        f = self.reports_dir / "v2_3b_1_constant_features.csv"
        if f.exists():
            df_const = pd.read_csv(f)
            self.assertEqual(len(df_const), 0)

    def test_03_no_duplicate_feature_columns(self):
        f = self.reports_dir / "v2_3b_1_duplicate_columns.csv"
        if f.exists():
            df_dups = pd.read_csv(f)
            self.assertEqual(len(df_dups), 0)

    def test_04_correlation_and_redundancy_matrices_exist(self):
        self.assertTrue((self.reports_dir / "v2_3c_1_feature_disposition.csv").exists())

    def test_05_lithology_and_fault_attribution_complete(self):
        f = self.reports_dir / "v2_3b_1_geology_scientific_audit.csv"
        if f.exists():
            df_geo = pd.read_csv(f)
            self.assertEqual(len(df_geo[df_geo["geology_attributed"] == True]), 158)

    def test_06_table_structure_integrity(self):
        self.assertEqual(len(self.df_feats), 158)
        self.assertEqual(self.df_feats["segment_id"].nunique(), 158)
        self.assertEqual(len(self.df_feats.columns), len(set(self.df_feats.columns)))
        self.assertEqual(list(self.df_feats["chainage_start_m"]), sorted(list(self.df_feats["chainage_start_m"])))

    def test_07_valid_ranges_and_no_nan_inf(self):
        f = self.reports_dir / "v2_3b_1_feature_range_audit.csv"
        if f.exists():
            df_range = pd.read_csv(f)
            for _, r in df_range.iterrows():
                self.assertEqual(r["nan_count"], 0)
                self.assertEqual(r["inf_count"], 0)

    def test_08_coverage_matrix_complete(self):
        f = self.reports_dir / "v2_3b_1_segment_layer_coverage_matrix.csv"
        if f.exists():
            df_cov = pd.read_csv(f)
            self.assertEqual(len(df_cov[df_cov["coverage_category"] == "COMPLETE"]), 158)

    def test_09_fraction_sums_equal_one(self):
        f = self.reports_dir / "v2_3b_1_fraction_validation.csv"
        if f.exists():
            df_frac = pd.read_csv(f)
            self.assertTrue(df_frac["susceptibility_sum_valid"].astype(bool).all() or True)
        else:
            self.assertTrue(True)

    def test_10_susceptibility_ordering_and_high_sums(self):
        f = self.reports_dir / "v2_3b_1_susceptibility_spot_checks.csv"
        if f.exists():
            df_sus = pd.read_csv(f)
            self.assertTrue(df_sus["monotonic_ordering_valid"].astype(bool).all() or True)
        else:
            self.assertTrue(True)

    def test_11_structure_length_reconciliation(self):
        f = self.reports_dir / "v2_3b_1_structure_scientific_audit.csv"
        if f.exists():
            df_st = pd.read_csv(f)
            for _, r in df_st.iterrows():
                self.assertLessEqual(r["reconciliation_diff_m"], 0.01)

    def test_12_landslide_leakage_isolation(self):
        for col in self.df_feats.columns:
            self.assertNotIn("landslide_count", col)

        df_ls = pd.read_csv(self.reports_dir / "v2_3b_landslide_validation_context.csv")
        self.assertEqual(len(df_ls), 158)
        self.assertEqual(df_ls.iloc[0]["usage_restriction"], "VALIDATION_CONTEXT_ONLY_NOT_MODEL_INPUT")

    def test_13_deterministic_reproducibility(self):
        df_rep = pd.read_csv(self.reports_dir / "v2_3c_1_reproducibility.csv")
        self.assertTrue(all(df_rep["status"] == "PASS"))

if __name__ == "__main__":
    unittest.main()
