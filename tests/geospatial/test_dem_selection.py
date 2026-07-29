import unittest
import csv
from pathlib import Path
import rasterio

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEM_LOCK_CSV = PROJECT_ROOT / "outputs" / "reports" / "phase_2_approved_dem_sources.csv"
PILOT_DEM_PATH = r"C:\Users\Saurabh Sharma\Downloads\J&K\copernicus_glo30\Pilot\output_hh.tif"

class TestDEMSelection(unittest.TestCase):
    def test_approved_dem_sources(self):
        self.assertTrue(DEM_LOCK_CSV.exists(), "Approved DEM sources lock CSV missing")
        paths = []
        checksums = set()
        with open(DEM_LOCK_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = row["absolute_path"]
                self.assertNotIn("pilot", p.lower(), "Pilot DEM detected in approved DEM sources lock")
                paths.append(p)
                checksums.add(row["full_checksum"])
                
        self.assertEqual(len(paths), 4, "Must select exactly 4 approved full-J&K DEM tiles")
        self.assertEqual(len(checksums), 4, "All 4 selected DEM tiles must have unique checksums")
        
        for p in paths:
            self.assertTrue(Path(p).exists(), f"Approved DEM file missing: {p}")
            with rasterio.open(p) as src:
                self.assertEqual(src.width, 7200)
                self.assertEqual(src.height, 7200)

if __name__ == "__main__":
    unittest.main()
