#!/usr/bin/env python3
"""
Captures Playwright browser screenshots of all 7 public web application routes for GeoSlide-JK v1.0.0 Final Submission Hotfix.
Saves screenshots to docs/progress/final_submission_screenshots/
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = PROJECT_ROOT / "docs/progress/final_submission_screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

ROUTES = [
    ("01_command_centre.png", "http://localhost:3000/"),
    ("02_risk_explorer.png", "http://localhost:3000/explorer"),
    ("03_district_intelligence.png", "http://localhost:3000/districts"),
    ("04_rainfall_monitor.png", "http://localhost:3000/rainfall"),
    ("05_location_risk_check.png", "http://localhost:3000/location-check"),
    ("06_model_transparency.png", "http://localhost:3000/transparency"),
    ("07_data_system_status.png", "http://localhost:3000/status")
]

def main():
    print("=" * 60)
    print("Capturing Playwright Browser Screenshots for Final Submission Hotfix")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        for filename, url in ROUTES:
            print(f"Navigating to {url} ...")
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            out_path = SCREENSHOT_DIR / filename
            page.screenshot(path=str(out_path))
            print(f"Saved: {out_path.name}")

        browser.close()

    print("\nAll 7 final submission browser screenshots captured successfully!")

if __name__ == "__main__":
    main()
