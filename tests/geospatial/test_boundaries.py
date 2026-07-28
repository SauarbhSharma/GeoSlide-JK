import os
import json
import unittest
from pathlib import Path
from shapely.geometry import shape

class TestBoundaryProcessing(unittest.TestCase):
    def setUp(self):
        self.project_root = Path("D:/Projects/GeoSlide_JK").resolve()
        self.districts_path = self.project_root / "data" / "processed" / "boundaries" / "jk_districts.geojson"
        self.ut_path = self.project_root / "data" / "processed" / "boundaries" / "jk_ut_boundary.geojson"

    def test_districts_file_exists(self):
        self.assertTrue(self.districts_path.exists(), f"Missing {self.districts_path}")
        self.assertTrue(self.ut_path.exists(), f"Missing {self.ut_path}")

    def test_district_count_and_whitelist(self):
        with open(self.districts_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        features = data.get("features", [])
        self.assertEqual(len(features), 20, f"Expected 20 districts, found {len(features)}")

        source_names = [f["properties"]["source_name"] for f in features]
        display_names = [f["properties"]["display_name"] for f in features]
        district_ids = [f["properties"]["district_id"] for f in features]

        # Confirm MIRPUR and MUZAFFARABAD are strictly absent
        self.assertNotIn("MIRPUR", source_names)
        self.assertNotIn("MUZAFFARABAD", source_names)

        # Confirm uniqueness of district IDs
        self.assertEqual(len(district_ids), len(set(district_ids)), "District IDs are not unique!")

        # Confirm display name normalization for target districts
        name_map = dict(zip(source_names, display_names))
        self.assertEqual(name_map.get("BADGAM"), "Budgam")
        self.assertEqual(name_map.get("BANDIPURA"), "Bandipora")
        self.assertEqual(name_map.get("BARAMULA"), "Baramulla")
        self.assertEqual(name_map.get("PUNCH"), "Poonch")
        self.assertEqual(name_map.get("RAJAURI"), "Rajouri")
        self.assertEqual(name_map.get("RIASI"), "Reasi")
        self.assertEqual(name_map.get("SHUPIYAN"), "Shopian")

    def test_geometry_validity(self):
        with open(self.districts_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for feature in data.get("features", []):
            geom = shape(feature["geometry"])
            self.assertTrue(geom.is_valid, f"Invalid geometry for district {feature['properties']['district_id']}")
            self.assertFalse(geom.is_empty, f"Empty geometry for district {feature['properties']['district_id']}")

    def test_dissolved_ut_boundary(self):
        with open(self.ut_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        features = data.get("features", [])
        self.assertEqual(len(features), 1)
        ut_geom = shape(features[0]["geometry"])
        self.assertTrue(ut_geom.is_valid, "Dissolved UT geometry is invalid")
        self.assertFalse(ut_geom.is_empty, "Dissolved UT geometry is empty")

if __name__ == "__main__":
    unittest.main()
