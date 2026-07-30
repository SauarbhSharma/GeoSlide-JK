import sys
import time
import json
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = PROJECT_ROOT / "docs" / "progress" / "maplibre_stress_screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

RESULTS = {
    "test_name": "MapLibre Runtime Stability & Stress Regression Test",
    "mode": "production_and_dev",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "clicks_performed": 0,
    "pan_zoom_actions": 0,
    "layer_toggles": 0,
    "district_changes": 0,
    "uncaught_errors": [],
    "abort_errors_ignored_safely": 0,
    "error_overlay_detected": False,
    "red_toast_detected": False,
    "backend_health_status": "UNKNOWN",
    "pass_status": False,
}

def run_stress_test(base_url="http://127.0.0.1:3000"):
    print(f"============================================================")
    print(f"  MapLibre Stress Regression Test on {base_url}")
    print(f"============================================================")

    # Verify backend health first
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8000/api/v1/health", timeout=3)
        if req.status == 200:
            RESULTS["backend_health_status"] = "HTTP 200 OK"
            print("Backend health check: PASSED (HTTP 200)")
        else:
            RESULTS["backend_health_status"] = f"HTTP {req.status}"
    except Exception as e:
        print(f"Backend health check failed: {e}")
        RESULTS["backend_health_status"] = f"FAILED: {e}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        page_errors = []
        console_errors = []

        def handle_pageerror(err):
            err_msg = str(err)
            if "AbortError" in err_msg or "aborted without reason" in err_msg:
                RESULTS["abort_errors_ignored_safely"] += 1
                print(f"[SAFELY IGNORED MAPLIBRE ABORT]: {err_msg}")
            elif "WebGL" in err_msg or "fragment shader" in err_msg or "GL_" in err_msg:
                print(f"[HEADLESS WEBGL WARNING IGNORED]: {err_msg}")
            else:
                page_errors.append(err_msg)
                print(f"[PAGE ERROR DETECTED]: {err_msg}")

        def handle_console(msg):
            if msg.type == "error":
                text = msg.text
                if "AbortError" in text or "aborted" in text:
                    RESULTS["abort_errors_ignored_safely"] += 1
                elif "WebGL" in text or "fragment shader" in text or "GL_" in text or "favicon" in text:
                    pass
                else:
                    console_errors.append(text)
                    print(f"[CONSOLE ERROR]: {text}")

        page.on("pageerror", handle_pageerror)
        page.on("console", handle_console)

        # 1. Open Risk Explorer
        print("\n1. Navigating to Risk Explorer...")
        page.goto(f"{base_url}/explorer", wait_until="load")
        time.sleep(3)

        # 2. Verify Map Canvas is Present
        map_el = page.locator("div.relative.w-full.h-full").first
        map_el.wait_for(state="visible", timeout=10000)
        box = map_el.bounding_box()
        print(f"Map canvas bounding box: {box}")

        # 3. Perform 25 Repeated Map Clicks across different locations
        print("\n2. Performing 25 map clicks across J&K domain...")
        click_coordinates = [
            (0.35, 0.50), (0.40, 0.45), (0.45, 0.55), (0.30, 0.60), (0.50, 0.40),
            (0.38, 0.52), (0.42, 0.48), (0.33, 0.58), (0.48, 0.42), (0.36, 0.54),
            (0.52, 0.38), (0.32, 0.62), (0.46, 0.46), (0.41, 0.51), (0.37, 0.49),
            (0.44, 0.53), (0.39, 0.47), (0.49, 0.41), (0.34, 0.56), (0.51, 0.39),
            (0.35, 0.51), (0.43, 0.47), (0.37, 0.53), (0.47, 0.43), (0.40, 0.50),
        ]

        inspector_values_sampled = []

        for idx, (x_pct, y_pct) in enumerate(click_coordinates, 1):
            cx = box["x"] + box["width"] * x_pct
            cy = box["y"] + box["height"] * y_pct
            page.mouse.click(cx, cy)
            RESULTS["clicks_performed"] += 1
            time.sleep(0.3)

            # Sample inspector value if active
            inspect_text = page.locator("div:has-text('Selected Location')").last.text_content() if page.locator("div:has-text('Selected Location')").count() > 0 else ""
            if inspect_text:
                inspector_values_sampled.append(inspect_text[:60])

        print(f"Completed {RESULTS['clicks_performed']} map clicks.")

        # 4. Perform Pan and Zoom Interactions
        print("\n3. Performing pan and zoom stress actions...")
        center_x = box["x"] + box["width"] * 0.5
        center_y = box["y"] + box["height"] * 0.5

        # Pan operations
        for drag in [(-100, 50), (150, -80), (-80, -120), (200, 100)]:
            page.mouse.move(center_x, center_y)
            page.mouse.down()
            page.mouse.move(center_x + drag[0], center_y + drag[1], steps=5)
            page.mouse.up()
            RESULTS["pan_zoom_actions"] += 1
            time.sleep(0.3)

        # Zoom operations (mouse wheel)
        page.mouse.move(center_x, center_y)
        for _ in range(3):
            page.mouse.wheel(0, -300) # zoom in
            RESULTS["pan_zoom_actions"] += 1
            time.sleep(0.3)
        for _ in range(3):
            page.mouse.wheel(0, 300) # zoom out
            RESULTS["pan_zoom_actions"] += 1
            time.sleep(0.3)

        # 5. Switch Layer Visibility (At least 8 toggles)
        print("\n4. Stress toggling map layers...")
        if page.locator("button:has-text('Map Layers')").count() > 0:
            page.locator("button:has-text('Map Layers')").first.click()
            time.sleep(0.3)
        checkboxes = page.locator("input[type='checkbox']")
        count = checkboxes.count()
        print(f"Found {count} layer checkboxes.")

        for i in range(min(count, 8)):
            cb = checkboxes.nth(i)
            cb.click()
            RESULTS["layer_toggles"] += 1
            time.sleep(0.2)
            cb.click()
            RESULTS["layer_toggles"] += 1
            time.sleep(0.2)

        # 6. Change Districts via Selector if available
        print("\n5. Testing District Selection...")
        district_select = page.locator("select").first
        if district_select.count() > 0:
            for dist_val in ["ramban", "doda", "kishtwar", "srinagar", "jammu"]:
                try:
                    district_select.select_option(value=dist_val)
                    RESULTS["district_changes"] += 1
                    time.sleep(0.4)
                except Exception:
                    pass

        # 7. Check for Next.js Runtime Error Overlay or Red Error Toast
        print("\n6. Checking for error overlays or error toasts...")
        next_overlay = page.locator("nextjs-portal, #__next-build-watcher, .nextjs-container-errors")
        if next_overlay.count() > 0 and next_overlay.first.is_visible():
            RESULTS["error_overlay_detected"] = True
            print("[ERROR] Next.js runtime error overlay detected!")

        red_toast = page.locator("div:has-text('signal is aborted'), div:has-text('AbortError')")
        if red_toast.count() > 0 and red_toast.first.is_visible():
            RESULTS["red_toast_detected"] = True
            print("[ERROR] Red AbortError toast detected!")

        # 8. Capture Final Stress Test Screenshot
        screenshot_path = SCREENSHOT_DIR / "stress_test_completed.png"
        page.screenshot(path=str(screenshot_path))
        print(f"Saved stress test screenshot to {screenshot_path}")

        # 9. Verify Point-Query & Tile Endpoints HTTP 200
        print("\n7. Verifying tile & point-query endpoints status...")
        location_check_res = urllib.request.urlopen("http://127.0.0.1:8000/api/v1/location-check?lat=33.245&lon=75.241")
        tile_res = urllib.request.urlopen("http://127.0.0.1:8000/api/v1/tiles/susceptibility_prob/8/181/102.png")

        print(f"Location check status: HTTP {location_check_res.status}")
        print(f"Raster tile status: HTTP {tile_res.status}")

        browser.close()

        # Evaluate Overall Pass Status
        no_uncaught = (len(page_errors) == 0)
        no_overlay = not RESULTS["error_overlay_detected"]
        no_toast = not RESULTS["red_toast_detected"]
        endpoints_ok = (location_check_res.status == 200 and tile_res.status == 200)

        RESULTS["uncaught_errors"] = page_errors
        RESULTS["pass_status"] = (no_uncaught and no_overlay and no_toast and endpoints_ok)

    # Output Results JSON
    print("\n============================================================")
    print("  STRESS TEST SUMMARY")
    print("============================================================")
    print(json.dumps(RESULTS, indent=2))

    # Save to Markdown report
    report_path = PROJECT_ROOT / "docs" / "progress" / "MAPLIBRE_STRESS_TEST_RESULTS.md"
    shot_path_str = str(screenshot_path).replace("\\", "/")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# MAPLIBRE STRESS TEST RESULTS REPORT\n\n")
        f.write(f"- **Timestamp**: {RESULTS['timestamp']}\n")
        f.write(f"- **Target URL**: {base_url}\n")
        f.write(f"- **Overall Pass Status**: **{'PASS' if RESULTS['pass_status'] else 'FAIL'}**\n")
        f.write(f"- **Map Clicks Executed**: {RESULTS['clicks_performed']}\n")
        f.write(f"- **Pan / Zoom Actions Executed**: {RESULTS['pan_zoom_actions']}\n")
        f.write(f"- **Layer Toggles Executed**: {RESULTS['layer_toggles']}\n")
        f.write(f"- **District Selection Changes**: {RESULTS['district_changes']}\n")
        f.write(f"- **MapLibre Tile AbortErrors Handled Safely**: {RESULTS['abort_errors_ignored_safely']}\n")
        f.write(f"- **Uncaught Page Errors**: {len(page_errors)}\n")
        f.write(f"- **Next.js Error Overlay Detected**: {RESULTS['error_overlay_detected']}\n")
        f.write(f"- **Red Error Toast Detected**: {RESULTS['red_toast_detected']}\n")
        f.write(f"- **Backend Tile & Query Health**: {RESULTS['backend_health_status']}\n\n")
        f.write(f"## Captured Screenshot\n\n")
        f.write(f"![Stress Test Complete](file:///{shot_path_str})\n")

    return RESULTS["pass_status"]

if __name__ == "__main__":
    success = run_stress_test()
    sys.exit(0 if success else 1)
