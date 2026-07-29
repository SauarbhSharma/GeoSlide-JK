import unittest
import csv
from pathlib import Path
import geopandas as gpd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_VECTORS = PROJECT_ROOT / "data" / "processed" / "vectors"
VECTOR_COUNTS_CSV = PROJECT_ROOT / "outputs" / "reports" / "phase_2_vector_counts.csv"

class TestStaticVectorLayers(unittest.TestCase):
    def test_vector_parquet_files_exist(self):
        parquet_files = [
            "jk_landslides_points.parquet",
            "jk_landslides_polygons.parquet",
            "jk_faults.parquet",
            "jk_thrusts.parquet",
            "jk_lineaments.parquet",
            "jk_lithology.parquet",
            "jk_nh44.parquet",
            "jk_major_roads.parquet",
            "jk_settlements.parquet",
            "jk_health_facilities.parquet"
        ]
        for f in parquet_files:
            p = PROCESSED_VECTORS / f
            self.assertTrue(p.exists(), f"Vector Parquet file missing: {p}")
            gdf = gpd.read_parquet(p)
            self.assertGreater(len(gdf), 0, f"Vector Parquet file is empty: {f}")
            self.assertTrue(gdf.geometry.is_valid.all(), f"Invalid geometries found in {f}")

    def test_master_geopackage(self):
        gpkg = PROCESSED_VECTORS / "jk_static_layers.gpkg"
        self.assertTrue(gpkg.exists(), "Master GeoPackage missing")

    def test_vector_counts_csv(self):
        self.assertTrue(VECTOR_COUNTS_CSV.exists(), "Vector counts CSV missing")
        with open(VECTOR_COUNTS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 10, "Must record counts for 10 vector layers")

if __name__ == "__main__":
    unittest.main()
