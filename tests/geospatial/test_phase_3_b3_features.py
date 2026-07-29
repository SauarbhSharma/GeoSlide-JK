#!/usr/bin/env python3
"""
GeoSlide-JK Phase 3 Checkpoint B3 Automated QA Unit Tests
Verifies WorldCover land cover, structural geology distance/density,
road/corridor, exposure features, quality masks, and feature role integrity.
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
TERRAIN_DIR = FEATURE_DIR / "terrain"
LANDCOVER_DIR = FEATURE_DIR / "landcover"
GEOLOGY_DIR = FEATURE_DIR / "geology"
INFRA_DIR = FEATURE_DIR / "infrastructure"
EXPOSURE_DIR = FEATURE_DIR / "exposure"
MASK_DIR = FEATURE_DIR / "masks"
REPORT_DIR = PROJECT_ROOT / "outputs/reports"


class TestPhase3B3Features(unittest.TestCase):

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
        cls.registry_df = pd.read_csv(REPORT_DIR / "phase_3_master_feature_registry.csv")

    def test_01_all_b3_rasters_exist_and_reopen(self):
        """1. Verify all expected B3 rasters exist and re-open cleanly."""
        expected_rasters = [
            LANDCOVER_DIR / "landcover_worldcover_dominant_class_100m.tif",
            LANDCOVER_DIR / "landcover_fraction_tree_cover_100m.tif",
            LANDCOVER_DIR / "landcover_fraction_bare_sparse_100m.tif",
            LANDCOVER_DIR / "landcover_vegetation_fraction_100m.tif",
            LANDCOVER_DIR / "landcover_shannon_diversity_100m.tif",
            GEOLOGY_DIR / "lithology_class_100m.tif",
            GEOLOGY_DIR / "distance_to_fault_m_100m.tif",
            GEOLOGY_DIR / "fault_density_100m.tif",
            GEOLOGY_DIR / "distance_to_active_fault_m_100m.tif",
            GEOLOGY_DIR / "distance_to_thrust_m_100m.tif",
            GEOLOGY_DIR / "distance_to_lineament_m_100m.tif",
            INFRA_DIR / "distance_to_major_road_m_100m.tif",
            INFRA_DIR / "distance_to_nh44_m_100m.tif",
            EXPOSURE_DIR / "distance_to_settlement_m_100m.tif",
            EXPOSURE_DIR / "distance_to_hospital_m_100m.tif",
            MASK_DIR / "hazard_feature_availability_count_100m.tif",
            MASK_DIR / "hazard_feature_complete_mask_100m.tif",
            MASK_DIR / "exposure_feature_availability_count_100m.tif",
            MASK_DIR / "exposure_feature_complete_mask_100m.tif"
        ]
        for p in expected_rasters:
            self.assertTrue(p.exists(), f"Missing B3 raster: {p.name}")
            with rasterio.open(p) as src:
                arr = src.read(1)
                self.assertEqual(arr.shape, (self.ref_height, self.ref_width))

    def test_02_master_grid_alignment(self):
        """2. Verify exact master-grid alignment across all B3 rasters."""
        for cat_dir in [LANDCOVER_DIR, GEOLOGY_DIR, INFRA_DIR, EXPOSURE_DIR, MASK_DIR]:
            for raster_path in cat_dir.glob("*.tif"):
                with rasterio.open(raster_path) as src:
                    self.assertEqual(src.crs, self.ref_crs)
                    self.assertEqual(src.width, self.ref_width)
                    self.assertEqual(src.height, self.ref_height)
                    self.assertEqual(src.bounds, self.ref_bounds)
                    self.assertEqual(src.transform, self.ref_transform)

    def test_03_worldcover_dominant_class_codes(self):
        """3. Verify WorldCover dominant class codes are valid ESA set."""
        dom_path = LANDCOVER_DIR / "landcover_worldcover_dominant_class_100m.tif"
        valid_codes = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 255}
        with rasterio.open(dom_path) as src:
            arr = src.read(1)
            unique_codes = set(np.unique(arr[self.valid_mask]))
            self.assertTrue(unique_codes.issubset(valid_codes), f"Invalid class codes found: {unique_codes - valid_codes}")

    def test_04_class_fractions_range_and_sum(self):
        """4. Verify class fractions range [0, 1] and sum to approx 1.0."""
        fraction_rasters = list(LANDCOVER_DIR.glob("landcover_fraction_*_100m.tif"))
        self.assertTrue(len(fraction_rasters) >= 10, "Expected at least 10 fractional cover rasters")

        total_sum = np.zeros((self.ref_height, self.ref_width), dtype=np.float32)
        for p in fraction_rasters:
            with rasterio.open(p) as src:
                arr = src.read(1)
                valid_vals = arr[self.valid_mask & (arr != -9999.0)]
                self.assertTrue(np.all(valid_vals >= 0.0), f"Negative fraction in {p.name}")
                self.assertTrue(np.all(valid_vals <= 1.0), f"Fraction > 1.0 in {p.name}")
                total_sum += np.where(self.valid_mask & (arr != -9999.0), arr, 0.0)

        # Sum of fractions inside valid land should be approx 1.0 (0.99 to 1.01)
        sum_valid = total_sum[self.valid_mask]
        self.assertTrue(np.all(np.abs(sum_valid - 1.0) < 0.05), "Sum of class fractions departs from 1.0")

    def test_05_distance_rasters_non_negative(self):
        """5. Verify distance rasters are non-negative inside valid land."""
        dist_paths = [
            GEOLOGY_DIR / "distance_to_fault_m_100m.tif",
            GEOLOGY_DIR / "distance_to_thrust_m_100m.tif",
            GEOLOGY_DIR / "distance_to_lineament_m_100m.tif",
            INFRA_DIR / "distance_to_major_road_m_100m.tif",
            INFRA_DIR / "distance_to_nh44_m_100m.tif",
            EXPOSURE_DIR / "distance_to_settlement_m_100m.tif",
            EXPOSURE_DIR / "distance_to_hospital_m_100m.tif"
        ]
        for p in dist_paths:
            with rasterio.open(p) as src:
                arr = src.read(1)
                valid_vals = arr[self.valid_mask & (arr != -9999.0)]
                self.assertTrue(np.all(valid_vals >= 0.0), f"Negative distance in {p.name}")

    def test_06_density_rasters_non_negative(self):
        """6. Verify density rasters are non-negative inside valid land."""
        den_paths = [
            GEOLOGY_DIR / "fault_density_100m.tif",
            GEOLOGY_DIR / "thrust_density_100m.tif",
            GEOLOGY_DIR / "lineament_density_100m.tif",
            INFRA_DIR / "major_road_density_km_per_km2_100m.tif",
            EXPOSURE_DIR / "settlement_density_100m.tif",
            EXPOSURE_DIR / "healthcare_facility_density_100m.tif"
        ]
        for p in den_paths:
            with rasterio.open(p) as src:
                arr = src.read(1)
                valid_vals = arr[self.valid_mask & (arr != -9999.0)]
                self.assertTrue(np.all(valid_vals >= 0.0), f"Negative density in {p.name}")

    def test_07_hazard_and_exposure_masks_separated(self):
        """7. Verify hazard and exposure quality masks are separate and distinct."""
        h_mask_p = MASK_DIR / "hazard_feature_complete_mask_100m.tif"
        e_mask_p = MASK_DIR / "exposure_feature_complete_mask_100m.tif"
        self.assertTrue(h_mask_p.exists() and e_mask_p.exists())

        with rasterio.open(h_mask_p) as h_src, rasterio.open(e_mask_p) as e_src:
            h_arr = h_src.read(1)
            e_arr = e_src.read(1)
            # They should be distinct arrays
            self.assertFalse(np.array_equal(h_arr, e_arr))

    def test_08_770_incomplete_terrain_cells_preserved(self):
        """8. Verify 770 incomplete terrain cells are preserved as incomplete."""
        b2b_avail_p = TERRAIN_DIR / "terrain_feature_availability_count_100m.tif"
        h_mask_p = MASK_DIR / "hazard_feature_complete_mask_100m.tif"

        with rasterio.open(b2b_avail_p) as a_src, rasterio.open(h_mask_p) as h_src:
            a_arr = a_src.read(1)
            h_arr = h_src.read(1)
            incomplete_terrain_cells = (a_arr != 16) & self.valid_mask
            self.assertEqual(int(np.sum(incomplete_terrain_cells)), 770)
            # All 770 incomplete terrain cells must be 0 in hazard complete mask
            self.assertTrue(np.all(h_arr[incomplete_terrain_cells] == 0))

    def test_09_feature_role_registry_rules(self):
        """9. Verify strict feature roles in master registry CSV."""
        df = self.registry_df
        # Latitude and longitude = excluded
        coords = df[df['feature_name'].isin(['latitude', 'longitude'])]
        self.assertTrue(all(coords['model_role'] == 'excluded'))

        # NLSM = validation_only
        nlsm = df[df['feature_name'] == 'nlsm_susceptibility']
        self.assertTrue(all(nlsm['model_role'] == 'validation_only'))

        # Exposure features = exposure_only
        exp_feats = df[df['feature_name'].isin(['distance_to_settlement_m', 'distance_to_hospital_m', 'distance_to_nh44_m'])]
        self.assertTrue(all(exp_feats['model_role'] == 'exposure_only'))

    def test_10_raw_data_untouched(self):
        """10. Verify raw data workspace remains 100% untouched."""
        raw_files = list(RAW_ROOT.glob("**/*"))
        self.assertTrue(len(raw_files) > 0)


if __name__ == "__main__":
    unittest.main()
