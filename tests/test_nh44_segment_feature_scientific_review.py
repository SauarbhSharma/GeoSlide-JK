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
        self.df_immut = pd.read_csv(self.reports_dir / "v2_3b_1_input_immutability_audit.csv")

    def test_01_immutability_release_tag(self):
        val = self.df_immut[self.df_immut["metric"] == "v2_3a_release_tag"]["observed"].iloc[0]
        self.assertEqual(val, "v2.3a-nh44-authoritative-baseline")

    def test_02_immutability_route_sha256(self):
        val = self.df_immut[self.df_immut["metric"] == "authoritative_route_sha256"]["observed"].iloc[0]
        self.assertEqual(val, "7141c209c578f8e8f19bc13b85409eeb220b709703c62691fac732594b2e3564")

    def test_03_immutability_segment_raw_sha256(self):
        val = self.df_immut[self.df_immut["metric"] == "authoritative_segment_raw_sha256"]["observed"].iloc[0]
        self.assertEqual(val, "775998e07bbb332d352093961ce2d47b7ca3488179885abceca1df843a50f172")

    def test_04_immutability_route_length(self):
        val = float(self.df_immut[self.df_immut["metric"] == "authoritative_route_length_m"]["observed"].iloc[0])
        self.assertAlmostEqual(val, 78619.370, places=3)

    def test_05_immutability_segment_counts(self):
        tot = int(self.df_immut[self.df_immut["metric"] == "total_segment_count"]["observed"].iloc[0])
        nom = int(self.df_immut[self.df_immut["metric"] == "nominal_500m_segment_count"]["observed"].iloc[0])
        res = float(self.df_immut[self.df_immut["metric"] == "residual_segment_length_m"]["observed"].iloc[0])
        self.assertEqual(tot, 158)
        self.assertEqual(nom, 157)
        self.assertAlmostEqual(res, 119.370, places=3)

    def test_06_table_structure_integrity(self):
        self.assertEqual(len(self.df_feats), 158)
        self.assertEqual(self.df_feats["segment_id"].nunique(), 158)
        self.assertEqual(len(self.df_feats.columns), len(set(self.df_feats.columns)))
        self.assertEqual(list(self.df_feats["chainage_start_m"]), sorted(list(self.df_feats["chainage_start_m"])))

    def test_07_valid_ranges_and_no_nan_inf(self):
        df_range = pd.read_csv(self.reports_dir / "v2_3b_1_feature_range_audit.csv")
        for _, r in df_range.iterrows():
            self.assertEqual(r["nan_count"], 0)
            self.assertEqual(r["inf_count"], 0)
            self.assertTrue(r["scientific_range_valid"])

    def test_08_coverage_matrix_complete(self):
        df_cov = pd.read_csv(self.reports_dir / "v2_3b_1_segment_layer_coverage_matrix.csv")
        self.assertEqual(len(df_cov[df_cov["coverage_category"] == "COMPLETE"]), 158)

    def test_09_fraction_sums_equal_one(self):
        df_frac = pd.read_csv(self.reports_dir / "v2_3b_1_fraction_validation.csv")
        self.assertTrue(all(df_frac["susceptibility_sum_valid"]))
        self.assertTrue(all(df_frac["landcover_sum_valid"]))
        self.assertTrue(all(df_frac["structure_sum_valid"]))

    def test_10_susceptibility_ordering_and_high_sums(self):
        df_sus = pd.read_csv(self.reports_dir / "v2_3b_1_susceptibility_spot_checks.csv")
        self.assertTrue(all(df_sus["monotonic_ordering_valid"]))
        self.assertTrue(all(df_sus["high_sum_valid"]))

    def test_11_structure_length_reconciliation(self):
        df_st = pd.read_csv(self.reports_dir / "v2_3b_1_structure_scientific_audit.csv")
        for _, r in df_st.iterrows():
            self.assertLessEqual(r["reconciliation_diff_m"], 0.01)

    def test_12_landslide_leakage_isolation(self):
        for col in self.df_feats.columns:
            self.assertNotIn("landslide_count", col)

        df_ls = pd.read_csv(self.reports_dir / "v2_3b_landslide_validation_context.csv")
        self.assertEqual(len(df_ls), 158)
        self.assertEqual(df_ls.iloc[0]["usage_restriction"], "VALIDATION_CONTEXT_ONLY_NOT_MODEL_INPUT")

    def test_13_deterministic_reproducibility(self):
        df_rep = pd.read_csv(self.reports_dir / "v2_3b_1_reproducibility.csv")
        self.assertTrue(all(df_rep["status"] == "PASS"))

if __name__ == "__main__":
    unittest.main()
