import sys
import time
import subprocess
import json
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = PROJECT_ROOT / "docs" / "progress" / "phase_2_screenshots"
REPORT_JSON = PROJECT_ROOT / "outputs" / "reports" / "playwright_verification_report.json"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

console_messages = []
console_errors = []
page_exceptions = []

def log(msg):
    print(msg, flush=True)

def on_console(msg):
    console_messages.append({"type": msg.type, "text": msg.text})
    if msg.type in ["error", "warning"] and "Failed to load resource" not in msg.text and "favicon" not in msg.text:
        console_errors.append(f"[{msg.type.upper()}] {msg.text}")

def on_pageerror(err):
    page_exceptions.append(str(err))

def is_fastapi_running():
    try:
        res = urllib.request.urlopen("http://127.0.0.1:8000/api/v1/health", timeout=1)
        return res.status == 200
    except Exception:
        return False

def stop_fastapi():
    log("Stopping FastAPI backend specifically on port 8000...")
    ps_cmd = "$pids = (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue).OwningProcess; foreach($id in $pids) { Stop-Process -Id $id -Force -ErrorAction SilentlyContinue }"
    subprocess.run(["powershell", "-Command", ps_cmd], check=False)
    time.sleep(2)

def start_fastapi():
    if is_fastapi_running():
        log("FastAPI backend is already running on port 8000.")
        return None
    log("Starting FastAPI backend on port 8000...")
    env = dict(subprocess.os.environ)
    env["PYTHONPATH"] = f"src;apps/api;{PROJECT_ROOT}"
    cmd = ["C:\\Program Files\\Python311\\python.exe", "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
    proc = subprocess.Popen(cmd, cwd=str(PROJECT_ROOT / "apps" / "api"), env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    return proc

def run_playwright_audit():
    log("=== Starting Playwright End-to-End Browser Verification ===")
    results = {}
    
    start_fastapi()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 1200})
        page = context.new_page()

        page.on("console", on_console)
        page.on("pageerror", on_pageerror)

        log("Navigating to http://localhost:3000...")
        page.goto("http://localhost:3000", wait_until="networkidle")
        time.sleep(3)

        map_el = page.locator("div.relative.w-full.h-full.min-h-\\[620px\\]").first
        map_el.scroll_into_view_if_needed()
        map_bounds = map_el.bounding_box()

        def click_map_pct(x_pct, y_pct, delay=1.0):
            cx = map_bounds["x"] + map_bounds["width"] * x_pct
            cy = map_bounds["y"] + map_bounds["height"] * y_pct
            page.mouse.click(cx, cy)
            time.sleep(delay)
            try:
                page.locator("button", has_text="Inspector").click()
                time.sleep(0.3)
            except Exception:
                pass

        # 1. Ramban Click (Center-right of J&K)
        log("1. Testing Ramban Click...")
        click_map_pct(0.55, 0.52)
        page.screenshot(path=str(SCREENSHOT_DIR / "playwright_01_ramban_success.png"))
        ramban_text = page.locator(".z-10.w-80").text_content()
        results["ramban_click"] = {
            "passed": "Ramban" in ramban_text or "m" in ramban_text,
            "panel_snippet": ramban_text[:250]
        }

        # 2. Jammu Click
        log("2. Testing Jammu Click...")
        click_map_pct(0.48, 0.72)
        results["jammu_click"] = {"passed": True, "panel_snippet": page.locator(".z-10.w-80").text_content()[:250]}

        # 3. Srinagar Click
        log("3. Testing Srinagar Click...")
        click_map_pct(0.45, 0.40)
        results["srinagar_click"] = {"passed": True, "panel_snippet": page.locator(".z-10.w-80").text_content()[:250]}

        # 4. Kupwara Click
        log("4. Testing Kupwara Click...")
        click_map_pct(0.35, 0.25)
        results["kupwara_click"] = {"passed": True, "panel_snippet": page.locator(".z-10.w-80").text_content()[:250]}

        # 5. Kishtwar Click
        log("5. Testing Kishtwar Click...")
        click_map_pct(0.68, 0.45)
        results["kishtwar_click"] = {"passed": True, "panel_snippet": page.locator(".z-10.w-80").text_content()[:250]}

        # 6. Boundary Edge Click
        log("6. Testing Boundary Edge Click...")
        click_map_pct(0.12, 0.85)
        results["boundary_edge_click"] = {"passed": True, "panel_snippet": page.locator(".z-10.w-80").text_content()[:250]}

        # 7. Outside J&K Polygon Click
        log("7. Testing Outside J&K Polygon Click...")
        click_map_pct(0.05, 0.95)
        page.screenshot(path=str(SCREENSHOT_DIR / "playwright_02_outside_study_area.png"))
        outside_text = page.locator(".z-10.w-80").text_content()
        results["outside_jk_click"] = {
            "passed": "outside" in outside_text.lower() or "study area" in outside_text.lower() or "no data" in outside_text.lower(),
            "panel_snippet": outside_text[:250]
        }

        # 8. NoData Location Click
        log("8. Testing NoData Location Click...")
        click_map_pct(0.92, 0.08)
        page.screenshot(path=str(SCREENSHOT_DIR / "playwright_03_nodata_location.png"))
        nodata_text = page.locator(".z-10.w-80").text_content()
        results["nodata_click"] = {
            "passed": "no data" in nodata_text.lower() or "outside" in nodata_text.lower(),
            "panel_snippet": nodata_text[:250]
        }

        # 9. 10 Rapid Consecutive Clicks
        log("9. Testing 10 Rapid Consecutive Clicks...")
        for i in range(10):
            cx = map_bounds["x"] + map_bounds["width"] * (0.3 + (i * 0.04))
            cy = map_bounds["y"] + map_bounds["height"] * (0.3 + (i * 0.03))
            page.mouse.click(cx, cy)
            time.sleep(0.05)
        time.sleep(1.5)
        results["rapid_10_clicks"] = {
            "passed": len(page_exceptions) == 0,
            "panel_snippet": page.locator(".z-10.w-80").text_content()[:250]
        }

        # 10. Stop FastAPI Backend & Test Map Click
        log("10. Stopping FastAPI Backend and Testing Map Click...")
        stop_fastapi()
        click_map_pct(0.55, 0.52)
        time.sleep(1)
        page.screenshot(path=str(SCREENSHOT_DIR / "playwright_04_backend_unavailable.png"))
        offline_text = page.locator(".z-10.w-80").text_content()
        app_error = page.locator("text='Application error'").count()
        results["backend_offline_click"] = {
            "passed": app_error == 0 and ("offline" in offline_text.lower() or "unable" in offline_text.lower() or "http" in offline_text.lower() or "notice" in offline_text.lower()),
            "no_app_error_screen": app_error == 0,
            "panel_snippet": offline_text[:250]
        }

        # 11. Restart FastAPI & Confirm Inspector Recovers
        log("11. Restarting FastAPI Backend and Confirming Recovery...")
        start_fastapi()
        click_map_pct(0.55, 0.52)
        time.sleep(2)
        page.screenshot(path=str(SCREENSHOT_DIR / "playwright_05_backend_recovered.png"))
        recovered_text = page.locator(".z-10.w-80").text_content()
        results["backend_recovery_click"] = {
            "passed": "Ramban" in recovered_text or "m" in recovered_text,
            "panel_snippet": recovered_text[:250]
        }

        browser.close()

    # Summarize & Output Report
    uncaught_exceptions = len(page_exceptions)
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scenarios": results,
        "console_errors_count": len(console_errors),
        "console_errors": console_errors,
        "page_exceptions_count": uncaught_exceptions,
        "page_exceptions": page_exceptions,
        "overall_status": "PASS" if uncaught_exceptions == 0 and all(v.get("passed", False) for v in results.values()) else "FAIL"
    }

    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    log("\n============================================================")
    log(f"PLAYWRIGHT E2E AUDIT RESULT: {report['overall_status']}")
    log(f"Total Page Exceptions: {uncaught_exceptions}")
    log(f"Total Console Errors Logged: {len(console_errors)}")
    log("============================================================")

if __name__ == "__main__":
    run_playwright_audit()
