#!/usr/bin/env python3
"""
GeoSlide-JK Phase 6 Full API Services & Integration Automated Unit Tests
Verifies FastAPI endpoints: /api/v1/health, /api/v1/status, /api/v1/districts,
/api/v1/terrain/click, /api/v1/susceptibility, /api/v1/transparency, /api/v1/location-check,
and static layer endpoints.
"""

import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from apps.api.main import app

class TestPhase6FullApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_health_endpoint(self):
        """1. Verify /api/v1/health reports version 0.6.0 and Phase 6 status."""
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["version"], "0.6.0")
        self.assertIn("Phase 6", data["phase"])

    def test_02_status_endpoint(self):
        """2. Verify /api/v1/status reports Phase 6 completed phases."""
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["active_districts"], 20)
        self.assertIn("Phase 6 — Full System Live", data["app_stage"])

    def test_03_districts_endpoint(self):
        """3. Verify /api/v1/districts returns exactly 20 districts."""
        response = self.client.get("/api/v1/districts")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 20)
        self.assertEqual(len(data["districts"]), 20)

    def test_04_terrain_click_endpoint(self):
        """4. Verify /api/v1/terrain/click samples elevation, slope, susceptibility, and hazard."""
        response = self.client.get("/api/v1/terrain/click?lat=33.25&lon=75.25")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["district"], "Ramban")
        self.assertIn("susceptibility", data)
        self.assertIn("dynamic_hazard", data)

    def test_05_susceptibility_summary(self):
        """5. Verify /api/v1/susceptibility returns Spatial CV ROC-AUC: 0.8694."""
        response = self.client.get("/api/v1/susceptibility")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["spatial_cv_roc_auc"], 0.8694)
        self.assertEqual(len(data["top_predictors"]), 5)

    def test_06_transparency_endpoint(self):
        """6. Verify /api/v1/transparency returns verified model metrics."""
        response = self.client.get("/api/v1/transparency")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["metrics"]["roc_auc"], 0.8694)
        self.assertTrue(data["feature_leakage_safeguards"]["nlsm_excluded"])

    def test_07_location_risk_check(self):
        """7. Verify /api/v1/location-check returns hazard rating and precautions."""
        response = self.client.get("/api/v1/location-check?lat=33.25&lon=75.25")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("precautionary_measures", data)


if __name__ == "__main__":
    unittest.main()
