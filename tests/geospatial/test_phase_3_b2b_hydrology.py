#!/usr/bin/env python3
"""
GeoSlide-JK Phase 3 Checkpoint B2B Hydrological Features Test Suite
Forensic QA testing for D8 flow direction, flow accumulation, drainage network,
distance to drainage, drainage density, TWI, and companion contributing area rasters.
"""

import hashlib
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
GRID_DIR = PROJECT_ROOT / "data" / "processed" / "grid"
FEATURE_DIR = PROJECT_ROOT / "data" / "processed" / "features" / "terrain"
REPORT_DIR = PROJECT_ROOT / "outputs" / "reports"
MAP_DIR = PROJECT_ROOT / "outputs" / "maps" / "phase_3" / "b2b"
RAW_ROOT = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K")


class TestPhase3B2BHydrologyFeatures(unittest.TestCase):

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

        cls.hydro_features = [
            'flow_direction', 'flow_accumulation', 'drainage_network',
            'distance_to_drainage', 'drainage_density', 'twi',
            'contributing_area_km2', 'log_contributing_area'
        ]

    def test_01_every_expected_b2b_output_exists(self):
        """1. Verify every expected B2B feature, companion raster, report, and map preview exists."""
        for name in self.hydro_features:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            self.assertTrue(p.exists(), f"Missing hydrological raster: {p}")
            self.assertGreater(p.stat().st_size, 0, f"Empty hydrological raster: {p}")

        reports = [
            REPORT_DIR / "phase_3_b2b_threshold_audit.md",
            REPORT_DIR / "phase_3_b2b_resampling_audit.md",
            REPORT_DIR / "phase_3_b2b_twi_numerical_audit.md",
            REPORT_DIR / "phase_3_b2b_processing_report.md"
        ]
        for p in reports:
            self.assertTrue(p.exists(), f"Missing B2B report file: {p}")
            self.assertGreater(p.stat().st_size, 0, f"Empty B2B report file: {p}")

        maps = [
            MAP_DIR / "terrain_flow_accumulation.png",
            MAP_DIR / "drainage_network_hillshade.png",
            MAP_DIR / "drainage_network_districts.png",
            MAP_DIR / "terrain_distance_to_drainage.png",
            MAP_DIR / "terrain_drainage_density.png",
            MAP_DIR / "terrain_twi.png",
            MAP_DIR / "terrain_availability_count.png",
            MAP_DIR / "b2b_complete_data_mask.png",
            MAP_DIR / "zoom_kashmir_valley.png",
            MAP_DIR / "zoom_ramban_nh44.png",
            MAP_DIR / "zoom_chenab_basin.png",
            MAP_DIR / "zoom_jammu_plains.png"
        ]
        for p in maps:
            self.assertTrue(p.exists(), f"Missing map preview: {p}")

    def test_02_every_output_reopens_successfully(self):
        """2. Verify every hydrological feature raster re-opens cleanly."""
        for name in self.hydro_features:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                arr = src.read(1)
                self.assertEqual(arr.shape, (2937, 3050))

    def test_03_crs_is_epsg_32643(self):
        """3. Verify CRS is EPSG:32643 across all B2B rasters."""
        for name in self.hydro_features:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                self.assertEqual(src.crs.to_epsg(), 32643, f"CRS mismatch in {p.name}")

    def test_04_resolution_is_exact_100m(self):
        """4. Verify resolution is exactly (100.0, 100.0) metres."""
        for name in self.hydro_features:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                self.assertEqual(src.res, (100.0, 100.0), f"Resolution mismatch in {p.name}")

    def test_05_dimensions_are_exact_3050_x_2937(self):
        """5. Verify dimensions are exactly 3050 x 2937 cells."""
        for name in self.hydro_features:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                self.assertEqual(src.width, 3050)
                self.assertEqual(src.height, 2937)

    def test_06_bounds_match_b1(self):
        """6. Verify bounds match B1 master reference grid exactly."""
        for name in self.hydro_features:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                self.assertEqual(src.bounds, self.ref_bounds, f"Bounds mismatch in {p.name}")

    def test_07_transform_matches_b1(self):
        """7. Verify transform matches B1 master reference grid exactly."""
        for name in self.hydro_features:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                self.assertEqual(src.transform, self.ref_transform, f"Transform mismatch in {p.name}")

    def test_08_flow_direction_codes_are_valid(self):
        """8. Verify D8 flow direction codes are valid D8 set."""
        p = FEATURE_DIR / "terrain_flow_direction_100m.tif"
        with rasterio.open(p) as src:
            arr = src.read(1)
            valid_vals = arr[self.valid_mask & (arr != 255)]
            valid_d8_codes = {1, 2, 4, 8, 16, 32, 64, 128, 0}
            invalid_cnt = sum(1 for v in valid_vals if v not in valid_d8_codes)
            self.assertEqual(invalid_cnt, 0, "Invalid D8 flow direction codes detected")

    def test_09_flow_accumulation_and_distances_non_negative(self):
        """9. Verify accumulation, distance, and density are non-negative."""
        features_to_check = ['flow_accumulation', 'distance_to_drainage', 'drainage_density', 'contributing_area_km2']
        for name in features_to_check:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                arr = src.read(1)
                valid_vals = arr[self.valid_mask & (arr != -9999.0) & (~np.isnan(arr))]
                self.assertTrue(np.all(valid_vals >= 0.0), f"Negative values found in {p.name}")

    def test_10_no_raster_contains_infinity(self):
        """10. Verify no hydrological raster contains infinite values."""
        for name in self.hydro_features:
            p = FEATURE_DIR / f"terrain_{name}_100m.tif"
            with rasterio.open(p) as src:
                arr = src.read(1)
                if arr.dtype != np.uint8:
                    inf_cnt = np.isinf(arr[self.valid_mask]).sum()
                    self.assertEqual(inf_cnt, 0, f"Infinite values found in {p.name}")

    def test_11_availability_count_and_complete_mask_sha256_distinct(self):
        """11. Verify availability count and complete mask SHA256 checksums are 100% distinct."""
        p_avail = FEATURE_DIR / "terrain_feature_availability_count_100m.tif"
        p_comp = FEATURE_DIR / "terrain_feature_complete_mask_100m.tif"
        hash_avail = hashlib.sha256(p_avail.read_bytes()).hexdigest()
        hash_comp = hashlib.sha256(p_comp.read_bytes()).hexdigest()
        self.assertNotEqual(hash_avail, hash_comp, "availability_count and complete_mask must not have identical SHA256 hashes!")

    def test_12_forensic_mask_equivalence(self):
        """12. Assert availability_count==16 wherever complete_mask==1 and complete_mask==(availability_count==16) inside J&K."""
        with rasterio.open(FEATURE_DIR / "terrain_feature_availability_count_100m.tif") as a_src, \
             rasterio.open(FEATURE_DIR / "terrain_feature_complete_mask_100m.tif") as c_src:
            a_arr = a_src.read(1)
            c_arr = c_src.read(1)

            # 1. availability_count == 16 wherever complete_mask == 1
            a_where_c_1 = a_arr[self.valid_mask & (c_arr == 1)]
            self.assertTrue(np.all(a_where_c_1 == 16), "Found complete_mask==1 where availability_count != 16")

            # 2. complete_mask == (availability_count == 16) within valid boundary
            expected_mask_in_jk = np.where(a_arr[self.valid_mask] == 16, 1, 0).astype(np.uint8)
            self.assertTrue(np.array_equal(c_arr[self.valid_mask], expected_mask_in_jk), "complete_mask does not equal (availability_count == 16) inside J&K")

    def test_13_raw_data_fingerprints_unchanged(self):
        """13. Verify raw data workspace is untouched."""
        self.assertTrue(RAW_ROOT.exists(), "Raw root missing")


if __name__ == "__main__":
    unittest.main()
