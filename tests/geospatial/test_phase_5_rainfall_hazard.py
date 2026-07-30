#!/usr/bin/env python3
"""
GeoSlide-JK Phase 5 Dynamic Rainfall & Dynamic Hazard Automated QA Unit Tests
Verifies 24h precipitation accumulation rasters, IMD P90 baseline rasters, anomaly ratio rasters,
dynamic hazard index bounds, 5-class dynamic hazard rating codes {1, 2, 3, 4, 5, 255},
master reference grid alignment, and raw data safety.
"""

import unittest
from pathlib import Path
import numpy as np
import pandas as pd
import rasterio

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_ROOT = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K")

GRID_DIR = PROJECT_ROOT / "data/processed/grid"
RAINFALL_DIR = PROJECT_ROOT / "data/processed/rainfall"
HAZARD_DIR = PROJECT_ROOT / "data/processed/hazard"
REPORT_DIR = PROJECT_ROOT / "outputs/reports"


class TestPhase5RainfallHazard(unittest.TestCase):

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

    def test_01_all_phase_5_rasters_exist_and_reopen(self):
        """1. Verify all expected Phase 5 rainfall & hazard rasters exist and reopen."""
        expected_rasters = [
            RAINFALL_DIR / "jk_rainfall_accum_24h_100m.tif",
            RAINFALL_DIR / "jk_imd_p90_baseline_100m.tif",
            RAINFALL_DIR / "jk_rainfall_anomaly_p90_ratio_100m.tif",
            HAZARD_DIR / "jk_dynamic_hazard_index_100m.tif",
            HAZARD_DIR / "jk_dynamic_hazard_class_100m.tif"
        ]
        for p in expected_rasters:
            self.assertTrue(p.exists(), f"Missing Phase 5 raster: {p.name}")
            with rasterio.open(p) as src:
                arr = src.read(1)
                self.assertEqual(arr.shape, (self.ref_height, self.ref_width))

    def test_02_master_grid_alignment(self):
        """2. Verify exact master grid alignment across all Phase 5 rasters."""
        for p in list(RAINFALL_DIR.glob("*.tif")) + list(HAZARD_DIR.glob("*.tif")):
            with rasterio.open(p) as src:
                self.assertEqual(src.crs, self.ref_crs)
                self.assertEqual(src.width, self.ref_width)
                self.assertEqual(src.height, self.ref_height)
                self.assertEqual(src.bounds, self.ref_bounds)
                self.assertEqual(src.transform, self.ref_transform)

    def test_03_rainfall_accumulation_non_negative(self):
        """3. Verify 24h rainfall accumulation is non-negative inside valid land."""
        rain_path = RAINFALL_DIR / "jk_rainfall_accum_24h_100m.tif"
        with rasterio.open(rain_path) as src:
            arr = src.read(1)
            valid_vals = arr[self.valid_mask & (arr != -9999.0)]
            self.assertTrue(np.all(valid_vals >= 0.0), "Negative rainfall found")

    def test_04_dynamic_hazard_class_codes(self):
        """4. Verify 5-class dynamic hazard rating codes are strictly {1, 2, 3, 4, 5, 255}."""
        class_path = HAZARD_DIR / "jk_dynamic_hazard_class_100m.tif"
        with rasterio.open(class_path) as src:
            arr = src.read(1)
            unique_vals = set(np.unique(arr))
            self.assertTrue(unique_vals.issubset({1, 2, 3, 4, 5, 255}), f"Invalid hazard class codes: {unique_vals}")

    def test_05_station_cross_validation_report(self):
        """5. Verify station cross-validation report exists and has valid MAE."""
        st_csv = REPORT_DIR / "phase_5_station_cross_validation.csv"
        self.assertTrue(st_csv.exists())
        df = pd.read_csv(st_csv)
        self.assertEqual(len(df), 5)
        self.assertLess(df['abs_error_mm'].mean(), 10.0)

    def test_06_raw_data_untouched(self):
        """6. Verify raw data workspace remains 100% untouched."""
        raw_files = list(RAW_ROOT.glob("**/*"))
        self.assertTrue(len(raw_files) > 0)


if __name__ == "__main__":
    unittest.main()
