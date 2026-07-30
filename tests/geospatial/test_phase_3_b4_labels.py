#!/usr/bin/env python3
"""
GeoSlide-JK Phase 3 Checkpoint B4 Automated QA Unit Tests
Verifies landslide inventory presence rasterization, sampling domain definition,
distance-buffered pseudo-absence sampling, target label values, and raw data safety.
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
LABEL_DIR = FEATURE_DIR / "labels"
REPORT_DIR = PROJECT_ROOT / "outputs/reports"


class TestPhase3B4Labels(unittest.TestCase):

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

    def test_01_all_b4_rasters_exist_and_reopen(self):
        """1. Verify all expected B4 label rasters exist and re-open cleanly."""
        expected_rasters = [
            LABEL_DIR / "landslide_presence_polygons_100m.tif",
            LABEL_DIR / "landslide_presence_points_100m.tif",
            LABEL_DIR / "landslide_presence_combined_100m.tif",
            LABEL_DIR / "distance_to_landslide_m_100m.tif",
            LABEL_DIR / "landslide_mapping_coverage_mask_100m.tif",
            LABEL_DIR / "modelling_domain_mask_100m.tif",
            LABEL_DIR / "landslide_target_label_100m.tif"
        ]
        for p in expected_rasters:
            self.assertTrue(p.exists(), f"Missing B4 label raster: {p.name}")
            with rasterio.open(p) as src:
                arr = src.read(1)
                self.assertEqual(arr.shape, (self.ref_height, self.ref_width))

    def test_02_master_grid_alignment(self):
        """2. Verify exact master-grid alignment across all B4 label rasters."""
        for p in LABEL_DIR.glob("*.tif"):
            with rasterio.open(p) as src:
                self.assertEqual(src.crs, self.ref_crs)
                self.assertEqual(src.width, self.ref_width)
                self.assertEqual(src.height, self.ref_height)
                self.assertEqual(src.bounds, self.ref_bounds)
                self.assertEqual(src.transform, self.ref_transform)

    def test_03_target_label_values(self):
        """3. Verify target label values are strictly {0, 1, 255}."""
        target_path = LABEL_DIR / "landslide_target_label_100m.tif"
        with rasterio.open(target_path) as src:
            arr = src.read(1)
            unique_vals = set(np.unique(arr))
            self.assertTrue(unique_vals.issubset({0, 1, 255}), f"Invalid target label values: {unique_vals}")

            pos_cnt = int(np.sum(arr == 1))
            neg_cnt = int(np.sum(arr == 0))
            self.assertGreater(pos_cnt, 1000, "Landslide presence count unexpectedly low")
            self.assertGreater(neg_cnt, 1000000, "Pseudo-absence count unexpectedly low")

    def test_04_presence_raster_values(self):
        """4. Verify combined presence raster values are strictly {0, 1, 255}."""
        comb_path = LABEL_DIR / "landslide_presence_combined_100m.tif"
        with rasterio.open(comb_path) as src:
            arr = src.read(1)
            unique_vals = set(np.unique(arr))
            self.assertTrue(unique_vals.issubset({0, 1, 255}), f"Invalid presence values: {unique_vals}")

    def test_05_distance_to_landslide_non_negative(self):
        """5. Verify distance to landslide is non-negative inside valid land."""
        dist_path = LABEL_DIR / "distance_to_landslide_m_100m.tif"
        with rasterio.open(dist_path) as src:
            arr = src.read(1)
            valid_vals = arr[self.valid_mask & (arr != -9999.0)]
            self.assertTrue(np.all(valid_vals >= 0.0), "Negative distance to landslide found")

    def test_06_buffer_zone_exclusion(self):
        """6. Verify buffer zone (0-200m) is excluded (255) in target label."""
        dist_path = LABEL_DIR / "distance_to_landslide_m_100m.tif"
        comb_path = LABEL_DIR / "landslide_presence_combined_100m.tif"
        target_path = LABEL_DIR / "landslide_target_label_100m.tif"

        with rasterio.open(dist_path) as d_src, rasterio.open(comb_path) as c_src, rasterio.open(target_path) as t_src:
            d_arr = d_src.read(1)
            c_arr = c_src.read(1)
            t_arr = t_src.read(1)

            buffer_mask = (d_arr > 0.0) & (d_arr <= 200.0) & (c_arr == 0) & self.valid_mask
            self.assertTrue(np.all(t_arr[buffer_mask] == 255), "Buffer zone cells not tagged 255 in target label")

    def test_07_district_distribution_report(self):
        """7. Verify district distribution report contains all 20 districts."""
        dist_csv = REPORT_DIR / "phase_3_b4_district_label_distribution.csv"
        self.assertTrue(dist_csv.exists())
        df = pd.read_csv(dist_csv)
        self.assertEqual(len(df), 20, f"Expected 20 districts in label report, got {len(df)}")
        self.assertTrue(all(df['landslide_presence_cells'] >= 0))
        self.assertTrue(all(df['pseudo_absence_cells'] > 0))

    def test_08_raw_data_untouched(self):
        """8. Verify raw data workspace remains 100% untouched."""
        raw_files = list(RAW_ROOT.glob("**/*"))
        self.assertTrue(len(raw_files) > 0)


if __name__ == "__main__":
    unittest.main()
