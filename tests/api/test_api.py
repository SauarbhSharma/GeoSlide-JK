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
        self.assertIn("Trained", data["model_status"])

    def test_health_endpoint(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    def test_status_endpoint(self):
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("NLSM", data["nlsm_status"])
        self.assertIn("Trained", data["model_pipeline_status"])

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
        self.assertGreaterEqual(len(data["raster_layers"]), 4)
        self.assertEqual(len(data["vector_layers"]), 11)

if __name__ == "__main__":
    unittest.main()
