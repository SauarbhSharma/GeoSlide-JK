import unittest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add project root and apps/api to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "apps" / "api"))

from main import app

class TestFastApiEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["service"], "GeoSlide-JK API")

    def test_status_endpoint(self):
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["active_districts"], 20)
        self.assertEqual(data["data_freshness"]["rainfall_mode"], "Demo Playback")
        self.assertIn("not an official warning system", data["disclaimer"])

    def test_districts_endpoint_whitelist_and_count(self):
        response = self.client.get("/api/v1/districts")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify exact 20 count requirement
        self.assertEqual(data["count"], 20, f"Expected exactly 20 districts, found {data['count']}")
        
        districts = data["districts"]
        self.assertEqual(len(districts), 20)
        
        source_names = [d["source_name"] for d in districts]
        display_names = [d["display_name"] for d in districts]
        
        # Mandatory exclusion verification
        self.assertNotIn("MIRPUR", source_names)
        self.assertNotIn("MUZAFFARABAD", source_names)
        
        # Display name check
        self.assertIn("Budgam", display_names)
        self.assertIn("Poonch", display_names)
        self.assertIn("Shopian", display_names)

    def test_layers_endpoint(self):
        response = self.client.get("/api/v1/layers")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("layers", data)
        self.assertTrue(len(data["layers"]) > 0)

    def test_coverage_endpoint(self):
        response = self.client.get("/api/v1/data/coverage")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
