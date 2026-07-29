import unittest
from fastapi.testclient import TestClient
from main import app

class TestFastApiEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("GeoSlide-JK", data["name"])
        self.assertEqual(data["model_status"], "Not Trained")

    def test_health_endpoint(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    def test_status_endpoint(self):
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["nlsm_status"], "NLSM raster: Excluded")
        self.assertEqual(data["model_pipeline_status"], "Not Trained")
        self.assertIn("Core datasets ready", data["summary_categories"])

    def test_districts_endpoint(self):
        response = self.client.get("/api/v1/districts")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 20)

    def test_districts_boundary_endpoint(self):
        response = self.client.get("/api/v1/districts/boundary")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["features"]), 20)

    def test_static_layers_endpoint(self):
        response = self.client.get("/api/v1/static-layers")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["raster_layers"]), 4)
        self.assertEqual(len(data["vector_layers"]), 11)

if __name__ == "__main__":
    unittest.main()
