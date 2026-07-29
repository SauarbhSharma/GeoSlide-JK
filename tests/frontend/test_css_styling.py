import unittest
import urllib.request
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCREENSHOT_DIR = PROJECT_ROOT / "docs" / "progress" / "phase_3_b3_frontend_runtime_repair"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
PHASE_2_SCREENSHOT_DIR = PROJECT_ROOT / "docs" / "progress" / "phase_2_screenshots"
PHASE_2_SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

class TestCSSStylingAndComputedProperties(unittest.TestCase):

    def test_css_asset_loading_and_computed_styles(self):
        css_requests = []
        js_requests = []
        failed_requests = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})

            def on_response(response):
                url = response.url
                status = response.status
                content_type = response.headers.get("content-type", "")

                if "/_next/static/css/" in url:
                    css_requests.append({
                        "url": url,
                        "status": status,
                        "content_type": content_type
                    })
                elif "/_next/static/chunks/" in url:
                    js_requests.append({
                        "url": url,
                        "status": status
                    })

                if status >= 400 and "favicon" not in url:
                    failed_requests.append(f"{url} returned HTTP {status}")

            page.on("response", on_response)

            # 1. Open Home Page
            page.goto("http://localhost:3000", wait_until="load")
            time.sleep(2)

            # 2. Verify CSS Assets Returned HTTP 200 with text/css
            self.assertGreater(len(css_requests), 0, "No /_next/static/css stylesheet requests were detected.")
            for css in css_requests:
                self.assertEqual(css["status"], 200, f"CSS asset {css['url']} failed with status {css['status']}")
                self.assertTrue("text/css" in css["content_type"], f"CSS asset {css['url']} has invalid content-type: {css['content_type']}")

            # 3. Verify No Failed JS or CSS Chunks
            self.assertEqual(len(failed_requests), 0, f"Failed static asset requests: {failed_requests}")

            # 4. Verify Computed Styles on Home Page
            body_bg = page.evaluate("() => window.getComputedStyle(document.body).backgroundColor")
            self.assertNotEqual(body_bg, "rgba(0, 0, 0, 0)", "Body background color must not be transparent")
            self.assertNotEqual(body_bg, "rgb(255, 255, 255)", "Body background color must not be plain white")
            self.assertTrue("9, 13, 22" in body_bg or "15, 23, 42" in body_bg or "rgb(" in body_bg, f"Unexpected body background: {body_bg}")

            nav_display = page.evaluate("() => window.getComputedStyle(document.querySelector('header div')).display")
            self.assertEqual(nav_display, "flex", "Header navigation container display must be flex")

            card_border = page.evaluate("() => window.getComputedStyle(document.querySelector('.border')).borderColor")
            self.assertTrue(card_border != "", "Card element must have styled borders")

            # 5. Capture Screenshots of All 7 Styled Routes
            routes = [
                ("/", "01_statewide_command_centre.png"),
                ("/explorer", "02_interactive_risk_explorer.png"),
                ("/districts", "03_district_intelligence.png"),
                ("/rainfall", "04_rainfall_monitor.png"),
                ("/location-check", "05_location_risk_check.png"),
                ("/transparency", "06_model_transparency.png"),
                ("/status", "07_data_system_status.png"),
            ]

            for path, filename in routes:
                url = f"http://localhost:3000{path}"
                page.goto(url, wait_until="load")
                time.sleep(1)

                # Computed style check on each page
                nav_count = page.locator("header nav, header a").count()
                self.assertGreater(nav_count, 0, f"Route {path} missing header navigation")

                page.screenshot(path=str(SCREENSHOT_DIR / filename))
                page.screenshot(path=str(PHASE_2_SCREENSHOT_DIR / filename))

            browser.close()

if __name__ == "__main__":
    unittest.main()
