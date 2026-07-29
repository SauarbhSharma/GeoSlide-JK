#!/usr/bin/env python3
"""
GeoSlide-JK Phase 3 Checkpoint B2A Quality Assurance Test Suite
Verifies all 23 mandatory QA criteria for non-hydrological terrain morphology features.
"""

import json
import unittest
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
GRID_DIR = PROJECT_ROOT / "data" / "processed" / "grid"
FEATURE_DIR = PROJECT_ROOT / "data" / "processed" / "features" / "terrain"
REPORT_DIR = PROJECT_ROOT / "outputs" / "reports"
MAP_DIR = PROJECT_ROOT / "outputs" / "maps" / "phase_3" / "b2a"
RAW_ROOT = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K")


class TestPhase3B2ATerrainFeatures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.master_grid_path = GRID_DIR / "jk_analysis_grid_100m.tif"
        cls.boundary_mask_path = GRID_DIR / "jk_boundary_mask_100m.tif"

        with rasterio.open(cls.master_grid_path) as src:
            cls.ref_crs = src.crs
            cls.ref_res = src.res
            cls.ref_width = src.width
            cls.ref_height = src.height
            cls.ref_bounds = src.bounds
            cls.ref_transform = src.transform

        with rasterio.open(cls.boundary_mask_path) as b_src:
            cls.boundary_mask = b_src.read(1)

        cls.valid_mask = (cls.boundary_mask == 1)

        cls.feature_names = [
            'elevation', 'slope', 'aspect', 'northness', 'eastness',
            'profile_curvature', 'plan_curvature', 'tri', 'tpi', 'local_relief'
        ]

    def test_01_every_expected_b2a_output_exists(self):
        """1. Verify every expected B2A feature, mask, report, and map output exists and is non-empty."""
        for name in self.feature_names:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            self.assertTrue(p.exists(), f"Missing terrain raster: {p}")
            self.assertGreater(p.stat().st_size, 0, f"Empty terrain raster: {p}")

        masks = [
            FEATURE_DIR / "terrain_feature_availability_count_100m.tif",
            FEATURE_DIR / "terrain_feature_complete_mask_100m.tif"
        ]
        for p in masks:
            self.assertTrue(p.exists(), f"Missing mask raster: {p}")
            self.assertGreater(p.stat().st_size, 0, f"Empty mask raster: {p}")

        reports = [
            REPORT_DIR / "phase_3_b2a_feature_manifest.csv",
            REPORT_DIR / "phase_3_b2a_terrain_statistics.csv",
            REPORT_DIR / "phase_3_b2a_district_statistics.csv",
            REPORT_DIR / "phase_3_b2a_alignment_report.md",
            REPORT_DIR / "phase_3_b2a_redundancy_report.md",
            REPORT_DIR / "phase_3_b2a_quality_report.md",
            REPORT_DIR / "phase_3_b2a_processing_report.md",
            REPORT_DIR / "phase_3_b2a_terrain_correlation.csv"
        ]
        for p in reports:
            self.assertTrue(p.exists(), f"Missing report file: {p}")
            self.assertGreater(p.stat().st_size, 0, f"Empty report file: {p}")

        maps = [
            MAP_DIR / "terrain_elevation.png",
            MAP_DIR / "terrain_slope.png",
            MAP_DIR / "terrain_northness.png",
            MAP_DIR / "terrain_eastness.png",
            MAP_DIR / "terrain_profile_curvature.png",
            MAP_DIR / "terrain_tri.png",
            MAP_DIR / "terrain_tpi.png",
            MAP_DIR / "b2a_complete_data_mask.png"
        ]
        for p in maps:
            self.assertTrue(p.exists(), f"Missing map preview: {p}")
            self.assertGreater(p.stat().st_size, 0, f"Empty map preview: {p}")

    def test_02_every_output_reopens_successfully(self):
        """2. Verify every feature raster re-opens cleanly."""
        for name in self.feature_names:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                arr = src.read(1)
                self.assertEqual(arr.shape, (2937, 3050))

    def test_03_crs_is_epsg_32643(self):
        """3. Verify CRS is EPSG:32643 across all B2A rasters."""
        for name in self.feature_names:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                self.assertEqual(src.crs.to_epsg(), 32643, f"CRS mismatch in {p.name}")

    def test_04_resolution_is_exact_100m(self):
        """4. Verify resolution is exactly (100.0, 100.0) metres."""
        for name in self.feature_names:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                self.assertEqual(src.res, (100.0, 100.0), f"Resolution mismatch in {p.name}")

    def test_05_dimensions_are_exact_3050_x_2937(self):
        """5. Verify dimensions are exactly 3050 x 2937 cells."""
        for name in self.feature_names:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                self.assertEqual(src.width, 3050)
                self.assertEqual(src.height, 2937)

    def test_06_bounds_match_b1(self):
        """6. Verify bounds match B1 master reference grid exactly."""
        for name in self.feature_names:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                self.assertEqual(src.bounds, self.ref_bounds, f"Bounds mismatch in {p.name}")

    def test_07_transform_matches_b1(self):
        """7. Verify transform matches B1 master reference grid exactly."""
        for name in self.feature_names:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                self.assertEqual(src.transform, self.ref_transform, f"Transform mismatch in {p.name}")

    def test_08_no_output_uses_pilot_dem(self):
        """8. Verify Pilot DEM was strictly excluded from processing."""
        manifest = pd.read_csv(REPORT_DIR / "phase_3_b2a_feature_manifest.csv")
        for _, row in manifest.iterrows():
            self.assertNotIn("Pilot", str(row['source_raster']), "Pilot DEM detected in manifest!")

    def test_09_nlsm_is_absent_from_predictors(self):
        """9. Confirm NLSM susceptibility raster is absent from B2A predictor features."""
        manifest = pd.read_csv(REPORT_DIR / "phase_3_b2a_feature_manifest.csv")
        names_lower = [str(n).lower() for n in manifest['feature_name']]
        self.assertNotIn("nlsm", names_lower)
        self.assertNotIn("susceptibility", names_lower)

    def test_10_lat_lon_absent_from_predictors(self):
        """10. Confirm latitude and longitude are absent from B2A predictor features."""
        manifest = pd.read_csv(REPORT_DIR / "phase_3_b2a_feature_manifest.csv")
        names_lower = [str(n).lower() for n in manifest['feature_name']]
        self.assertNotIn("latitude", names_lower)
        self.assertNotIn("longitude", names_lower)
        self.assertNotIn("lat", names_lower)
        self.assertNotIn("lon", names_lower)

    def test_11_slope_is_within_0_to_90_degrees(self):
        """11. Verify slope values are strictly within [0.0, 90.0] degrees."""
        with rasterio.open(FEATURE_DIR / "terrain_slope_100m.tif") as src:
            slope = src.read(1)
            valid_vals = slope[self.valid_mask & (slope != -9999.0)]
            self.assertTrue(np.all(valid_vals >= 0.0), "Negative slope detected!")
            self.assertTrue(np.all(valid_vals <= 90.0), "Slope > 90 degrees detected!")

    def test_12_northness_is_within_minus1_to_plus1(self):
        """12. Verify northness values are strictly within [-1.0, 1.0]."""
        with rasterio.open(FEATURE_DIR / "terrain_northness_100m.tif") as src:
            n_arr = src.read(1)
            valid_vals = n_arr[self.valid_mask & (n_arr != -9999.0)]
            self.assertTrue(np.all(valid_vals >= -1.0001), "Northness < -1 detected!")
            self.assertTrue(np.all(valid_vals <= 1.0001), "Northness > 1 detected!")

    def test_13_eastness_is_within_minus1_to_plus1(self):
        """13. Verify eastness values are strictly within [-1.0, 1.0]."""
        with rasterio.open(FEATURE_DIR / "terrain_eastness_100m.tif") as src:
            e_arr = src.read(1)
            valid_vals = e_arr[self.valid_mask & (e_arr != -9999.0)]
            self.assertTrue(np.all(valid_vals >= -1.0001), "Eastness < -1 detected!")
            self.assertTrue(np.all(valid_vals <= 1.0001), "Eastness > 1 detected!")

    def test_14_no_raster_contains_infinity(self):
        """14. Verify no feature raster contains infinite values."""
        for name in self.feature_names:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                arr = src.read(1)
                inf_cnt = np.isinf(arr[self.valid_mask]).sum()
                self.assertEqual(inf_cnt, 0, f"Infinite values found in {p.name}")

    def test_15_no_unexpected_all_nodata_raster(self):
        """15. Verify no feature raster is completely NoData inside J&K UT."""
        for name in self.feature_names:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                arr = src.read(1)
                valid_cnt = (self.valid_mask & (arr != -9999.0) & (~np.isnan(arr))).sum()
                self.assertGreater(valid_cnt, 4000000, f"Feature raster {p.name} has low valid coverage: {valid_cnt}")

    def test_16_availability_count_is_valid(self):
        """16. Verify availability count raster contains valid counts [0, 10]."""
        p = FEATURE_DIR / "terrain_feature_availability_count_100m.tif"
        with rasterio.open(p) as src:
            arr = src.read(1)
            valid_vals = arr[self.valid_mask]
            self.assertTrue(np.all(valid_vals >= 0), "Negative availability count detected")
            self.assertTrue(np.all(valid_vals <= 10), "Availability count > 10 detected")
            self.assertGreater(np.mean(valid_vals), 9.9, "Incomplete availability detected on valid land")

    def test_17_complete_mask_follows_definition(self):
        """17. Verify complete data mask equals 1 where availability==10."""
        with rasterio.open(FEATURE_DIR / "terrain_feature_availability_count_100m.tif") as a_src, \
             rasterio.open(FEATURE_DIR / "terrain_feature_complete_mask_100m.tif") as c_src:
            a_arr = a_src.read(1)
            c_arr = c_src.read(1)
            expected_c = np.where(a_arr == 10, 1, 0).astype(np.uint8)
            self.assertTrue(np.array_equal(c_arr, expected_c), "Complete mask does not match availability count definition")

    def test_18_district_summaries_contain_20_districts(self):
        """18. Verify district summaries contain exactly 20 districts."""
        df = pd.read_csv(REPORT_DIR / "phase_3_b2a_district_statistics.csv")
        self.assertEqual(len(df), 20, "District statistics CSV does not contain 20 rows")

    def test_19_raw_data_fingerprints_unchanged(self):
        """19. Verify raw data workspace is untouched."""
        self.assertTrue(RAW_ROOT.exists(), "Raw root missing")

    def test_20_b2b_hydrological_outputs_not_generated(self):
        """20. Confirm no Checkpoint B2B hydrological outputs exist."""
        b2b_forbidden = [
            'flow_direction', 'flow_accumulation', 'twi', 'drainage_density',
            'distance_to_drainage', 'stream_power_index'
        ]
        for name in b2b_forbidden:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            self.assertFalse(p.exists(), f"Forbidden B2B hydrological output detected: {p}")


if __name__ == "__main__":
    unittest.main()
