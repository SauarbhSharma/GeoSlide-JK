import unittest
import json
from pathlib import Path
import rasterio

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_TERRAIN = PROJECT_ROOT / "data" / "processed" / "terrain"
B1_STATS_JSON = PROJECT_ROOT / "outputs" / "reports" / "phase_2_b1_elevation_stats.json"
B2_STATS_JSON = PROJECT_ROOT / "outputs" / "reports" / "phase_2_b2_derivatives_stats.json"

class TestTerrainDerivatives(unittest.TestCase):
    def test_cog_files_exist(self):
        cogs = [
            "jk_elevation_glo30_cog.tif",
            "jk_slope_degrees_cog.tif",
            "jk_aspect_degrees_cog.tif",
            "jk_hillshade_cog.tif"
        ]
        for cog in cogs:
            p = PROCESSED_TERRAIN / cog
            self.assertTrue(p.exists(), f"COG missing: {p}")
            with rasterio.open(p) as src:
                self.assertEqual(str(src.crs), "EPSG:32643")
                self.assertTrue(src.is_tiled)

    def test_elevation_statistics(self):
        self.assertTrue(B1_STATS_JSON.exists(), "B1 elevation stats JSON missing")
        with open(B1_STATS_JSON, 'r', encoding='utf-8') as f:
            stats = json.load(f)
            self.assertEqual(stats["checkpoint"], "CHECKPOINT_B1_PASSED")
            self.assertGreater(stats["min_elevation_m"], 100)
            self.assertLess(stats["max_elevation_m"], 8850)
            self.assertEqual(stats["suspicious_extreme_values"], 0)

    def test_slope_aspect_statistics(self):
        self.assertTrue(B2_STATS_JSON.exists(), "B2 derivatives stats JSON missing")
        with open(B2_STATS_JSON, 'r', encoding='utf-8') as f:
            stats = json.load(f)
            self.assertEqual(stats["checkpoint"], "CHECKPOINT_B2_PASSED")
            self.assertGreaterEqual(stats["slope_stats"]["min_deg"], 0.0)
            self.assertLessEqual(stats["slope_stats"]["max_deg"], 90.0)

if __name__ == "__main__":
    unittest.main()
