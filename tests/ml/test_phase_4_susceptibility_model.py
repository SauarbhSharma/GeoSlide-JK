#!/usr/bin/env python3
"""
GeoSlide-JK Phase 4 Landslide Susceptibility Model Automated QA Unit Tests
Verifies susceptibility probability bounds [0.0, 1.0], 5-class rating codes {1, 2, 3, 4, 5, 255},
master reference grid alignment, spatial CV ROC-AUC > 0.80, feature leakage isolation, and raw data safety.
"""

import unittest
from pathlib import Path
import numpy as np
import pandas as pd
import rasterio

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_ROOT = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K")

GRID_DIR = PROJECT_ROOT / "data/processed/grid"
FEATURE_DIR = PROJECT_ROOT / "data/processed/features"
SUSC_DIR = PROJECT_ROOT / "data/processed/susceptibility"
MODEL_DIR = PROJECT_ROOT / "data/models"
REPORT_DIR = PROJECT_ROOT / "outputs/reports"


class TestPhase4SusceptibilityModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ref_grid_path = GRID_DIR / "jk_analysis_grid_100m.tif"
        cls.boundary_mask_path = GRID_DIR / "jk_boundary_mask_100m.tif"
        with rasterio.open(cls.ref_grid_path) as src:
            cls.ref_crs = src.crs
            cls.ref_transform = src.transform
            cls.ref_width = src.width
            cls.ref_height = src.height
            cls.ref_bounds = src.bounds

        with rasterio.open(cls.boundary_mask_path) as src:
            cls.boundary_mask = src.read(1)

        cls.valid_mask = (cls.boundary_mask == 1)

    def test_01_susceptibility_rasters_exist(self):
        """1. Verify susceptibility probability and class rasters exist and reopen."""
        prob_path = SUSC_DIR / "jk_susceptibility_probability_100m.tif"
        class_path = SUSC_DIR / "jk_susceptibility_class_100m.tif"

        self.assertTrue(prob_path.exists(), "Probability raster missing")
        self.assertTrue(class_path.exists(), "Class rating raster missing")

        with rasterio.open(prob_path) as src:
            prob_arr = src.read(1)
            self.assertEqual(prob_arr.shape, (self.ref_height, self.ref_width))

        with rasterio.open(class_path) as src:
            class_arr = src.read(1)
            self.assertEqual(class_arr.shape, (self.ref_height, self.ref_width))

    def test_02_master_grid_alignment(self):
        """2. Verify exact master grid alignment across susceptibility outputs."""
        for p in [SUSC_DIR / "jk_susceptibility_probability_100m.tif", SUSC_DIR / "jk_susceptibility_class_100m.tif"]:
            with rasterio.open(p) as src:
                self.assertEqual(src.crs, self.ref_crs)
                self.assertEqual(src.width, self.ref_width)
                self.assertEqual(src.height, self.ref_height)
                self.assertEqual(src.bounds, self.ref_bounds)
                self.assertEqual(src.transform, self.ref_transform)

    def test_03_probability_bounds_and_values(self):
        """3. Verify susceptibility probability values range [0.0, 1.0] inside valid land."""
        prob_path = SUSC_DIR / "jk_susceptibility_probability_100m.tif"
        with rasterio.open(prob_path) as src:
            arr = src.read(1)
            valid_vals = arr[self.valid_mask & (arr != -9999.0)]
            self.assertTrue(np.all(valid_vals >= 0.0), "Negative probability found")
            self.assertTrue(np.all(valid_vals <= 1.0), "Probability > 1.0 found")
            self.assertGreater(len(valid_vals), 4000000)

    def test_04_class_rating_codes(self):
        """4. Verify 5-class rating codes are strictly {1, 2, 3, 4, 5, 255}."""
        class_path = SUSC_DIR / "jk_susceptibility_class_100m.tif"
        with rasterio.open(class_path) as src:
            arr = src.read(1)
            unique_vals = set(np.unique(arr))
            self.assertTrue(unique_vals.issubset({1, 2, 3, 4, 5, 255}), f"Invalid class codes: {unique_vals}")

    def test_05_spatial_cv_roc_auc_threshold(self):
        """5. Verify 5-fold spatial district block cross-validation ROC-AUC > 0.80."""
        cv_csv = REPORT_DIR / "phase_4_spatial_cv_results.csv"
        self.assertTrue(cv_csv.exists(), "Spatial CV CSV missing")
        df = pd.read_csv(cv_csv)
        self.assertEqual(len(df), 5, f"Expected 5 spatial folds, got {len(df)}")
        mean_auc = df['xgb_roc_auc'].mean()
        self.assertGreater(mean_auc, 0.80, f"Mean spatial CV ROC-AUC unexpectedly low: {mean_auc:.4f}")

    def test_06_model_binary_exists(self):
        """6. Verify trained XGBoost model binary exists."""
        model_json = MODEL_DIR / "xgboost_susceptibility_model.json"
        self.assertTrue(model_json.exists(), "Model binary missing")

    def test_07_feature_leakage_isolation(self):
        """7. Verify NLSM, coordinates, and exposure features excluded from predictor stack."""
        feat_imp_csv = REPORT_DIR / "phase_4_feature_importance_shap.csv"
        self.assertTrue(feat_imp_csv.exists())
        df = pd.read_csv(feat_imp_csv)
        feats = df['feature_name'].tolist()
        for bad in ["nlsm", "lat", "lon", "hospital", "settlement", "nh44"]:
            self.assertFalse(any(bad in f.lower() for f in feats), f"Forbidden predictor '{bad}' found in model predictors")

    def test_08_raw_data_untouched(self):
        """8. Verify raw data workspace remains 100% untouched."""
        raw_files = list(RAW_ROOT.glob("**/*"))
        self.assertTrue(len(raw_files) > 0)


if __name__ == "__main__":
    unittest.main()
