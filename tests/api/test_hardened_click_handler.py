import unittest
import json
from fastapi.testclient import TestClient
from main import app

class TestHardenedTerrainAPIContract(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_01_valid_jammu_click(self):
        res = self.client.get("/api/v1/terrain/value?lat=32.7266&lon=74.8570")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["code"], "OK")
        self.assertEqual(data["district"], "Jammu")
        self.assertIsNotNone(data["terrain"]["elevation_m"])
        self.assertIsNotNone(data["terrain"]["slope_deg"])

    def test_02_valid_ramban_click(self):
        res = self.client.get("/api/v1/terrain/value?lat=33.2450&lon=75.2410")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["district"], "Ramban")

    def test_03_valid_srinagar_click(self):
        res = self.client.get("/api/v1/terrain/value?lat=34.0833&lon=74.7973")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["district"], "Srinagar")

    def test_04_valid_kupwara_click(self):
        res = self.client.get("/api/v1/terrain/value?lat=34.5262&lon=74.2542")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["district"], "Kupwara")

    def test_05_valid_kishtwar_click(self):
        res = self.client.get("/api/v1/terrain/value?lat=33.3156&lon=75.7664")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["district"], "Kishtwar")

    def test_06_click_outside_jk_boundary(self):
        res = self.client.get("/api/v1/terrain/value?lat=31.5&lon=74.0")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["code"], "OUTSIDE_STUDY_AREA")
        self.assertFalse(data["inside_study_area"])

    def test_07_click_outside_map_bounds(self):
        res = self.client.get("/api/v1/terrain/value?lat=10.0&lon=10.0")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["code"], "OUTSIDE_STUDY_AREA")

    def test_08_nodata_pixel(self):
        # Click on edge/outer water cell where DEM is NoData
        res = self.client.get("/api/v1/terrain/value?lat=35.8&lon=76.8")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertFalse(data["success"])
        self.assertFalse(data["data_available"])

    def test_15_empty_nearby_feature_response(self):
        res = self.client.get("/api/v1/features/nearby?lat=32.0&lon=73.0&radius=1.0")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("nearby_counts", data)

if __name__ == "__main__":
    unittest.main()
