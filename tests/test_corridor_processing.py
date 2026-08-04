import unittest
import os
import geopandas as gpd
import pandas as pd
from pathlib import Path

class TestCorridorProcessing(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.corridor_dir = self.project_root / "data" / "processed" / "corridors"
        self.parquet_path = self.corridor_dir / "nh44_pilot_corridor_epsg32643.parquet"
        self.segments_parquet = self.corridor_dir / "nh44_segments_500m_epsg32643.parquet"
        self.segments_csv = self.corridor_dir / "nh44_segments_500m.csv"
        self.manifest_json = self.corridor_dir / "nh44_corridor_source_manifest.json"

    def test_corridor_files_exist(self):
        self.assertTrue(self.parquet_path.exists(), "nh44_pilot_corridor_epsg32643.parquet missing")
        self.assertTrue(self.segments_parquet.exists(), "nh44_segments_500m_epsg32643.parquet missing")
        self.assertTrue(self.segments_csv.exists(), "nh44_segments_500m.csv missing")
        self.assertTrue(self.manifest_json.exists(), "nh44_corridor_source_manifest.json missing")

    def test_corridor_geometry_validity_and_crs(self):
        gdf = gpd.read_parquet(self.parquet_path)
        self.assertEqual(len(gdf), 1, "Corridor parquet should contain 1 row")
        self.assertEqual(gdf.crs.to_epsg(), 32643, "CRS must be EPSG:32643")
        self.assertTrue(gdf.iloc[0].geometry.is_valid, "Corridor geometry must be valid")
        self.assertGreater(gdf.iloc[0].geometry.length, 50000.0, "Pilot length should be > 50 km")

    def test_segments_count_and_chainage(self):
        df_seg = pd.read_csv(self.segments_csv)
        self.assertEqual(len(df_seg), 150, "Should contain exactly 150 segments")
        self.assertEqual(df_seg.iloc[0]['start_chainage_m'], 0.0, "First segment must start at 0.0m")
        self.assertAlmostEqual(df_seg['segment_length_m'].sum(), 74875.83, delta=1.0)

    def test_segment_ids_unique(self):
        df_seg = pd.read_csv(self.segments_csv)
        unique_ids = df_seg['segment_id'].nunique()
        self.assertEqual(unique_ids, len(df_seg), "All segment IDs must be unique")
        self.assertTrue(df_seg['segment_id'].iloc[0].startswith("NH44-JK-"))

    def test_no_exposure_fields_calculated(self):
        df_seg = pd.read_csv(self.segments_csv)
        for col in ['lhs_score', 'dis_score', 'ips_score']:
            self.assertNotIn(col, df_seg.columns, f"{col} should not be calculated in V2-3A")

if __name__ == "__main__":
    unittest.main()
