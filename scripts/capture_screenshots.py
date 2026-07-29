import asyncio
import os
from playwright.async_api import async_playwright

PAGES = [
    ("http://localhost:3000/", "01_statewide_command_centre.png"),
    ("http://localhost:3000/explorer", "02_interactive_risk_explorer.png"),
    ("http://localhost:3000/districts", "03_district_intelligence.png"),
    ("http://localhost:3000/rainfall", "04_rainfall_monitor.png"),
    ("http://localhost:3000/location-check", "05_location_risk_check.png"),
    ("http://localhost:3000/transparency", "06_model_transparency.png"),
    ("http://localhost:3000/status", "07_data_system_status.png"),
]

OUTPUT_DIR = r"D:\Projects\GeoSlide_JK\outputs\figures\page_screenshots"

async def capture_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=== Capturing Browser Screenshots for All 7 GeoSlide-JK Pages ===")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu", "--ignore-certificate-errors"]
        )
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        for url, filename in PAGES:
            print(f"Navigating to {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(1.5)
            filepath = os.path.join(OUTPUT_DIR, filename)
            await page.screenshot(path=filepath, full_page=True)
            size = os.path.getsize(filepath)
            print(f"  [SAVED] {filename} ({size} bytes)")

        await browser.close()
    print("\nAll 7 page screenshots captured successfully!")

if __name__ == "__main__":
    asyncio.run(capture_all())
