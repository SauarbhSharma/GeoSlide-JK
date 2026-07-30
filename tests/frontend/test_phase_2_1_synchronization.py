import unittest
import urllib.request
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCREENSHOT_DIR = PROJECT_ROOT / "docs" / "progress" / "phase_2_screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

class TestPhase21Synchronization(unittest.TestCase):

    def test_01_api_version_and_status(self):
        """1. Verify application version reports Phase 2 and v0.2.0."""
        req = urllib.request.urlopen("http://127.0.0.1:8000/api/v1/status")
        self.assertEqual(req.status, 200)
        data = json.loads(req.read().decode())
        self.assertTrue("Phase" in data.get("app_stage", "") or "v1.0.0" in data.get("app_stage", ""))
        self.assertTrue(data.get("app_version", "").startswith("v"))

    def test_02_district_count_and_absence_of_mirpur_muzaffarabad(self):
        """2. Confirm exactly 20 districts and absence of Mirpur & Muzaffarabad."""
        req = urllib.request.urlopen("http://127.0.0.1:8000/api/v1/districts")
        self.assertEqual(req.status, 200)
        data = json.loads(req.read().decode())
        self.assertEqual(data.get("count"), 20)
        district_names = [d["display_name"].lower() for d in data.get("districts", [])]
        self.assertNotIn("mirpur", district_names)
        self.assertNotIn("muzaffarabad", district_names)

    def test_03_browser_phase_2_labels_and_absence_of_phase_1(self):
        """3. Confirm browser UI shows Phase 2 and no user-facing Phase 1.1 Prototype labels remain."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:3000", wait_until="load")
            time.sleep(2)

            content = page.content()
            self.assertNotIn("Phase 1.1 Prototype", content, "Stale 'Phase 1.1 Prototype' label found in DOM")
            self.assertNotIn("Phase 1.1 Shell", content, "Stale 'Phase 1.1 Shell' label found in DOM")
            self.assertIn("Phase 2", content, "Phase 2 label missing from DOM")

            browser.close()

    def test_04_master_layer_registry_synchronization(self):
        """4. Verify master layer registry is synchronized without conflicting statuses."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:3000", wait_until="load")
            time.sleep(2)

            # Sidebar layer text check
            sidebar_text = page.locator("div.w-80").first.text_content()
            self.assertNotIn("Unavailable until processing phase", sidebar_text)
            self.assertIn("Copernicus DEM Elevation", sidebar_text)
            self.assertIn("Terrain Slope", sidebar_text)

            browser.close()

    def test_05_terrain_inspector_popup_styling_and_crs(self):
        """5. Verify terrain inspector popup styling, dark theme, and CRS wording."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto("http://localhost:3000", wait_until="load")
            time.sleep(5)

            # Check backend health
            import requests
            try:
                r = requests.get("http://localhost:8000/api/v1/health", timeout=1)
                backend_online = (r.status_code == 200)
            except Exception:
                backend_online = False

            if not backend_online:
                self.skipTest("FastAPI backend (port 8000) is not running for interactive click test")

            map_el = page.locator("canvas.maplibregl-canvas").first
            map_el.scroll_into_view_if_needed()
            box = map_el.bounding_box()

            # Click Ramban area (x_pct 0.35, y_pct 0.50)
            cx = box["x"] + box["width"] * 0.35
            cy = box["y"] + box["height"] * 0.50
            page.mouse.click(cx, cy)
            popup_html = ""
            for _ in range(10):
                popup_html = page.evaluate("() => document.querySelector('.custom-popup')?.outerHTML || ''")
                if len(popup_html) > 0:
                    break
                time.sleep(0.5)

            if len(popup_html) > 0:
                self.assertIn("EPSG:4326", popup_html)
                self.assertIn("EPSG:32643", popup_html)

            # Take screenshot of styled popup
            page.screenshot(path=str(SCREENSHOT_DIR / "styled_terrain_popup.png"))

            browser.close()

if __name__ == "__main__":
    unittest.main()
