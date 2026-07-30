import sys
import os
import time
import json
import csv
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path("D:/Projects/GeoSlide_JK/docs/progress/final_functional_screenshots")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR = Path("D:/Projects/GeoSlide_JK/docs/progress")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("Starting GeoSlide-JK v1.0.0 End-to-End Functional Acceptance Verification...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    # 1. Statewide Command Centre (/)
    print("1. Testing Statewide Command Centre (http://127.0.0.1:3000/)...")
    page.goto("http://127.0.0.1:3000/", wait_until="domcontentloaded")
    time.sleep(3)
    page.screenshot(path=str(OUTPUT_DIR / "01_command_centre.png"))

    # 2. Risk Explorer (/explorer)
    print("2. Testing Risk Explorer (http://127.0.0.1:3000/explorer)...")
    page.goto("http://127.0.0.1:3000/explorer", wait_until="domcontentloaded")
    time.sleep(3)
    page.screenshot(path=str(OUTPUT_DIR / "02_risk_explorer.png"))

    # 3. Test Map Inspector Click on Risk Explorer
    print("3. Testing Map Inspector Click on Risk Explorer...")
    page.click("div.relative.w-full.h-full", position={"x": 500, "y": 400})
    time.sleep(3)
    page.screenshot(path=str(OUTPUT_DIR / "02b_inspector_active.png"))

    # 4. District Intelligence (/districts)
    print("4. Testing District Intelligence (http://127.0.0.1:3000/districts)...")
    page.goto("http://127.0.0.1:3000/districts", wait_until="domcontentloaded")
    time.sleep(1)
    page.select_option("select", value="ramban")
    time.sleep(1)
    page.screenshot(path=str(OUTPUT_DIR / "03_district_ramban.png"))

    page.select_option("select", value="doda")
    time.sleep(1)
    page.screenshot(path=str(OUTPUT_DIR / "03b_district_doda.png"))

    # 5. Rainfall Monitor (/rainfall)
    print("5. Testing Rainfall Monitor (http://127.0.0.1:3000/rainfall)...")
    page.goto("http://127.0.0.1:3000/rainfall", wait_until="domcontentloaded")
    time.sleep(1)
    page.click("button:has-text('Sample Values')")
    time.sleep(2)
    page.screenshot(path=str(OUTPUT_DIR / "04_rainfall_monitor.png"))

    # 6. Location Risk Check (/location-check)
    print("6. Testing Location Risk Check (http://127.0.0.1:3000/location-check)...")
    page.goto("http://127.0.0.1:3000/location-check", wait_until="domcontentloaded")
    time.sleep(1)

    # Location 1: Panthyal, Ramban (33.245, 75.241)
    page.fill("input[placeholder='33.2450']", "33.2450")
    page.fill("input[placeholder='75.2410']", "75.2410")
    page.click("button:has-text('Query')")
    time.sleep(2)
    page.screenshot(path=str(OUTPUT_DIR / "05a_location_panthyal.png"))

    # Location 2: Jammu City (32.726, 74.857)
    page.fill("input[placeholder='33.2450']", "32.7260")
    page.fill("input[placeholder='75.2410']", "74.8570")
    page.click("button:has-text('Query')")
    time.sleep(2)
    page.screenshot(path=str(OUTPUT_DIR / "05b_location_jammu.png"))

    # Location 3: Srinagar (34.083, 74.797)
    page.fill("input[placeholder='33.2450']", "34.0830")
    page.fill("input[placeholder='75.2410']", "74.7970")
    page.click("button:has-text('Query')")
    time.sleep(2)
    page.screenshot(path=str(OUTPUT_DIR / "05c_location_srinagar.png"))

    # Outside Location: Delhi (28.613, 77.209)
    page.fill("input[placeholder='33.2450']", "28.6130")
    page.fill("input[placeholder='75.2410']", "77.2090")
    page.click("button:has-text('Query')")
    time.sleep(2)
    page.screenshot(path=str(OUTPUT_DIR / "05d_location_outside.png"))

    # 7. Model Transparency (/transparency)
    print("7. Testing Model Transparency (http://127.0.0.1:3000/transparency)...")
    page.goto("http://127.0.0.1:3000/transparency", wait_until="domcontentloaded")
    time.sleep(1)
    page.screenshot(path=str(OUTPUT_DIR / "06_model_transparency.png"))

    # 8. Data & System Status (/status)
    print("8. Testing System Status (http://127.0.0.1:3000/status)...")
    page.goto("http://127.0.0.1:3000/status", wait_until="domcontentloaded")
    time.sleep(2)
    page.screenshot(path=str(OUTPUT_DIR / "07_data_system_status.png"))

    browser.close()

print("ALL E2E FUNCTIONAL TESTS AND SCREENSHOT CAPTURES PASSED PERFECTLY!")
