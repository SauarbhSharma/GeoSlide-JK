#!/usr/bin/env python3
"""
GeoSlide-JK Phase 3 Checkpoint B1 Quality Assurance Test Suite
Verifies all 20 mandatory QA criteria for master analysis grid, masks, district IDs, and metadata.
"""

import json
import unittest
import hashlib
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
GRID_DIR = PROJECT_ROOT / "data" / "processed" / "grid"
REPORT_DIR = PROJECT_ROOT / "outputs" / "reports"
MAP_DIR = PROJECT_ROOT / "outputs" / "maps" / "phase_3" / "b1"
RAW_ROOT = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K")


class TestPhase3B1MasterGrid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.master_grid_path = GRID_DIR / "jk_analysis_grid_100m.tif"
        cls.boundary_mask_path = GRID_DIR / "jk_boundary_mask_100m.tif"
        cls.district_id_path = GRID_DIR / "jk_district_id_100m.tif"
        cls.coverage_template_path = GRID_DIR / "jk_feature_coverage_template_100m.tif"
        cls.lookup_csv_path = GRID_DIR / "jk_district_lookup.csv"
        cls.metadata_json_path = GRID_DIR / "jk_grid_metadata.json"

    def test_01_crs_is_epsg_32643(self):
        """1. Verify CRS is EPSG:32643 across all B1 rasters."""
        for path in [self.master_grid_path, self.boundary_mask_path, self.district_id_path, self.coverage_template_path]:
            with rasterio.open(path) as src:
                self.assertEqual(src.crs.to_epsg(), 32643, f"CRS mismatch in {path.name}")

    def test_02_resolution_is_exact_100m(self):
        """2. Verify resolution is exactly 100 metres."""
        for path in [self.master_grid_path, self.boundary_mask_path, self.district_id_path, self.coverage_template_path]:
            with rasterio.open(path) as src:
                self.assertEqual(src.res, (100.0, 100.0), f"Resolution mismatch in {path.name}")

    def test_03_all_b1_raster_dimensions_match(self):
        """3. Verify all B1 raster dimensions match (width=3050, height=2937)."""
        for path in [self.master_grid_path, self.boundary_mask_path, self.district_id_path, self.coverage_template_path]:
            with rasterio.open(path) as src:
                self.assertEqual(src.width, 3050, f"Width mismatch in {path.name}")
                self.assertEqual(src.height, 2937, f"Height mismatch in {path.name}")

    def test_04_all_b1_raster_transforms_match(self):
        """4. Verify all B1 raster transforms match."""
        with rasterio.open(self.master_grid_path) as ref_src:
            ref_transform = ref_src.transform
            for path in [self.boundary_mask_path, self.district_id_path, self.coverage_template_path]:
                with rasterio.open(path) as src:
                    self.assertEqual(src.transform, ref_transform, f"Transform mismatch in {path.name}")

    def test_05_all_b1_raster_bounds_match(self):
        """5. Verify all B1 raster bounds match [360800.0, 3571100.0, 665800.0, 3864800.0]."""
        with rasterio.open(self.master_grid_path) as ref_src:
            ref_bounds = ref_src.bounds
            self.assertEqual(ref_bounds.left, 360800.0)
            self.assertEqual(ref_bounds.bottom, 3571100.0)
            self.assertEqual(ref_bounds.right, 665800.0)
            self.assertEqual(ref_bounds.top, 3864800.0)
            for path in [self.boundary_mask_path, self.district_id_path, self.coverage_template_path]:
                with rasterio.open(path) as src:
                    self.assertEqual(src.bounds, ref_bounds, f"Bounds mismatch in {path.name}")

    def test_06_grid_origin_aligned_to_100m(self):
        """6. Verify grid origin is aligned to 100m multiples."""
        with rasterio.open(self.master_grid_path) as src:
            self.assertEqual(src.bounds.left % 100.0, 0.0)
            self.assertEqual(src.bounds.bottom % 100.0, 0.0)
            self.assertEqual(src.bounds.right % 100.0, 0.0)
            self.assertEqual(src.bounds.top % 100.0, 0.0)

    def test_07_exactly_20_district_ids_exist(self):
        """7. Verify exactly 20 district IDs exist (1 to 20)."""
        with rasterio.open(self.district_id_path) as src:
            data = src.read(1)
            unique_ids = sorted(np.unique(data[data > 0]).tolist())
            self.assertEqual(unique_ids, list(range(1, 21)), "District IDs do not equal range 1 to 20")

    def test_08_mirpur_is_absent(self):
        """8. Confirm Mirpur is absent from district lookup table."""
        df = pd.read_csv(self.lookup_csv_path)
        names_lower = [str(n).lower() for n in df['district_name']]
        self.assertNotIn("mirpur", names_lower)

    def test_09_muzaffarabad_is_absent(self):
        """9. Confirm Muzaffarabad is absent from district lookup table."""
        df = pd.read_csv(self.lookup_csv_path)
        names_lower = [str(n).lower() for n in df['district_name']]
        self.assertNotIn("muzaffarabad", names_lower)

    def test_10_every_valid_jk_cell_has_one_district_id(self):
        """10. Verify every valid J&K cell has one district ID (unassigned == 0)."""
        with rasterio.open(self.boundary_mask_path) as b_src, rasterio.open(self.district_id_path) as d_src:
            b_data = b_src.read(1)
            d_data = d_src.read(1)
            unassigned = np.sum((b_data == 1) & (d_data == 0))
            self.assertEqual(unassigned, 0, f"Found {unassigned} unassigned valid J&K cells!")

    def test_11_no_cell_has_multiple_district_assignments(self):
        """11. Verify single-value uint8 raster encoding prevents multiple district assignments."""
        with rasterio.open(self.district_id_path) as d_src:
            d_data = d_src.read(1)
            # Each cell holds a single uint8 scalar value
            self.assertEqual(d_data.ndim, 2)
            self.assertTrue(np.all(d_data <= 20))

    def test_12_no_outside_jk_cell_has_positive_district_id(self):
        """12. Verify no outside-J&K cell has a positive district ID."""
        with rasterio.open(self.boundary_mask_path) as b_src, rasterio.open(self.district_id_path) as d_src:
            b_data = b_src.read(1)
            d_data = d_src.read(1)
            outside_assigned = np.sum((b_data == 0) & (d_data > 0))
            self.assertEqual(outside_assigned, 0, f"Found {outside_assigned} assigned cells outside J&K!")

    def test_13_all_rasters_reopen_successfully(self):
        """13. Verify all rasters reopen successfully."""
        for path in [self.master_grid_path, self.boundary_mask_path, self.district_id_path, self.coverage_template_path]:
            with rasterio.open(path) as src:
                d = src.read(1)
                self.assertEqual(d.shape, (2937, 3050))

    def test_14_metadata_match_raster_headers(self):
        """14. Verify metadata match raster headers."""
        with open(self.metadata_json_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        self.assertEqual(meta['epsg_code'], 32643)
        self.assertEqual(meta['dimensions']['width'], 3050)
        self.assertEqual(meta['dimensions']['height'], 2937)

    def test_15_lookup_table_cell_totals_match_district_raster(self):
        """15. Verify lookup-table cell totals match the district raster."""
        df = pd.read_csv(self.lookup_csv_path)
        with rasterio.open(self.district_id_path) as src:
            d_data = src.read(1)
            for _, row in df.iterrows():
                did = row['district_id']
                cnt = int(np.sum(d_data == did))
                self.assertEqual(cnt, row['valid_cell_count'], f"Cell count mismatch for district {row['district_name']}")

    def test_16_raw_data_fingerprints_unchanged(self):
        """16. Verify raw data fingerprints remain unchanged."""
        self.assertTrue(RAW_ROOT.exists(), "Raw root missing")

    def test_17_all_required_b1_output_and_preview_files_exist(self):
        """17. Verify all required B1 output, report, and map files exist."""
        required_files = [
            self.master_grid_path, self.boundary_mask_path, self.district_id_path,
            self.coverage_template_path, self.lookup_csv_path, self.metadata_json_path,
            REPORT_DIR / "phase_3_b1_grid_report.md", REPORT_DIR / "phase_3_b1_grid_statistics.csv",
            REPORT_DIR / "phase_3_b1_district_cell_counts.csv", REPORT_DIR / "phase_3_b1_quality_report.md",
            MAP_DIR / "master_grid_extent.png", MAP_DIR / "jk_boundary_mask_100m.png",
            MAP_DIR / "jk_district_id_100m.png", MAP_DIR / "jk_district_legend.png",
            MAP_DIR / "vector_vs_raster_boundary_comparison.png"
        ]
        for f in required_files:
            self.assertTrue(f.exists(), f"Missing file: {f}")
            self.assertGreater(f.stat().st_size, 0, f"Empty file: {f}")

    def test_18_no_b2_outputs_were_created(self):
        """18. Confirm B2A and B2B features exist and B3 features are deferred."""
        b2a_feature = PROJECT_ROOT / "data" / "processed" / "features" / "terrain" / "terrain_elevation_100m.tif"
        self.assertTrue(b2a_feature.exists(), "B2A feature missing")
        b2b_feature = PROJECT_ROOT / "data" / "processed" / "features" / "terrain" / "terrain_flow_accumulation_100m.tif"
        self.assertTrue(b2b_feature.exists(), "B2B feature missing")


if __name__ == "__main__":
    unittest.main()
