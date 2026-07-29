import unittest
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MAP_CONTAINER_TSX = PROJECT_ROOT / "apps" / "web" / "components" / "map" / "MapContainer.tsx"
ERROR_BOUNDARY_TSX = PROJECT_ROOT / "apps" / "web" / "components" / "map" / "MapErrorBoundary.tsx"

class TestMapClickSafetyAndHardening(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MAP_CONTAINER_TSX.exists(), "MapContainer.tsx file missing")
        self.assertTrue(ERROR_BOUNDARY_TSX.exists(), "MapErrorBoundary.tsx file missing")
        with open(MAP_CONTAINER_TSX, "r", encoding="utf-8") as f:
            self.container_code = f.read()
        with open(ERROR_BOUNDARY_TSX, "r", encoding="utf-8") as f:
            self.boundary_code = f.read()

    def test_09_http_400_detail_handling(self):
        self.assertIn("res.ok", self.container_code, "Must check res.ok status before parsing JSON")
        self.assertIn("errJson.detail", self.container_code, "Must handle FastAPI detail error responses")

    def test_10_http_500_handling(self):
        self.assertIn("try", self.container_code, "Must wrap map click requests in try/catch/finally")
        self.assertIn("catch", self.container_code)

    def test_11_backend_unavailable_handling(self):
        self.assertIn("NETWORK_ERROR", self.container_code, "Must handle network errors gracefully without crashing")

    def test_12_network_timeout_and_abort(self):
        self.assertIn("AbortController", self.container_code, "Must use AbortController to cancel stale requests")
        self.assertIn("controller.signal.aborted", self.container_code, "Must verify request was not aborted")

    def test_13_null_terrain_values_safety(self):
        self.assertIn("formatFiniteNumber", self.container_code, "Must use safe number formatting function")
        self.assertIn("Number.isFinite", self.container_code, "Must check Number.isFinite before toFixed calls")

    def test_17_rapid_sequence_clicking_safety(self):
        self.assertIn("abortControllerRef.current.abort()", self.container_code, "Must abort previous requests on rapid clicking")

    def test_19_inspector_error_boundary_wrapping(self):
        self.assertIn("<MapErrorBoundary", self.container_code, "Must wrap inspector in React Error Boundary")
        self.assertIn("componentDidCatch", self.boundary_code, "Error Boundary must implement componentDidCatch")

if __name__ == "__main__":
    unittest.main()
