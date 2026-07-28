#!/usr/bin/env python3
"""
GeoSlide-JK Page Screenshot Capture Tool
Automates headless browser navigation across all 7 UI pages and saves full-page PNG screenshots to outputs/figures/page_screenshots/
"""

import sys
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures" / "page_screenshots"

PAGES = [
    {"name": "01_statewide_command_centre", "url": "http://localhost:3000/"},
    {"name": "02_interactive_risk_explorer", "url": "http://localhost:3000/explorer"},
    {"name": "03_district_intelligence", "url": "http://localhost:3000/districts"},
    {"name": "04_rainfall_monitor", "url": "http://localhost:3000/rainfall"},
    {"name": "05_location_risk_check", "url": "http://localhost:3000/location-check"},
    {"name": "06_model_transparency", "url": "http://localhost:3000/transparency"},
    {"name": "07_data_system_status", "url": "http://localhost:3000/status"},
]

def capture():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"=== Capturing Browser Screenshots for All 7 GeoSlide-JK Pages ===")
    print(f"Output directory: {OUTPUT_DIR}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        for item in PAGES:
            name = item["name"]
            url = item["url"]
            out_file = OUTPUT_DIR / f"{name}.png"
            print(f"Navigating to {url}...")
            
            page.goto(url, wait_until="networkidle")
            time.sleep(1) # Allow SVG/renders to settle
            
            page.screenshot(path=str(out_file), full_page=True)
            print(f"  [SAVED] {out_file.name} ({out_file.stat().st_size} bytes)")

        browser.close()
    print("\nAll 7 page screenshots captured successfully!")

if __name__ == "__main__":
    capture()
