import os
import sys
import shutil
import csv
import json
import hashlib
from pathlib import Path
import rasterio

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K")
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
TEMP_DIR = PROJECT_ROOT / "data" / "interim" / "phase_2_temp"

# Approved 4 DEM Tile Paths (Exact Absolute Paths)
APPROVED_TILES = [
    {
        "quadrant": "Southwest (73.5-75.5°E, 32.0-34.0°N)",
        "path": r"C:\Users\Saurabh Sharma\Downloads\J&K\copernicus_glo30\full_jk\Southwest\output_hh.tif",
        "expected_bounds": [73.5, 32.0, 75.5, 34.0]
    },
    {
        "quadrant": "Southeast (75.5-77.5°E, 32.0-34.0°N)",
        "path": r"C:\Users\Saurabh Sharma\Downloads\J&K\copernicus_glo30\full_jk\Southeast\output_hh.tif",
        "expected_bounds": [75.5, 32.0, 77.5, 34.0]
    },
    {
        "quadrant": "Northwest (73.5-75.5°E, 34.0-36.0°N)",
        "path": r"C:\Users\Saurabh Sharma\Downloads\J&K\copernicus_glo30\full_jk\Northwest\output_hh.tif",
        "expected_bounds": [73.5, 34.0, 75.5, 36.0]
    },
    {
        "quadrant": "Northeast (75.5-77.5°E, 34.0-36.0°N)",
        "path": r"C:\Users\Saurabh Sharma\Downloads\J&K\copernicus_glo30\full_jk\Northeast\output_hh.tif",
        "expected_bounds": [75.5, 34.0, 77.5, 36.0]
    }
]

EXCLUDED_PILOT_PATH = r"C:\Users\Saurabh Sharma\Downloads\J&K\copernicus_glo30\Pilot\output_hh.tif"

def check_disk_space():
    total, used, free = shutil.disk_usage("D:\\")
    free_gb = free / (1024 ** 3)
    print(f"Drive D: Free Storage: {free_gb:.2f} GB (Required: min 15 GB, recommended 20 GB)")
    if free_gb < 15.0:
        raise RuntimeError(f"HARD FAILURE: Insufficient disk space on D:. Free: {free_gb:.2f} GB < 15.0 GB minimum required.")
    return free_gb

def compute_checksum(filepath, max_bytes=10*1024*1024):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(max_bytes)
        hasher.update(buf)
    return hasher.hexdigest()

def lock_dem_sources():
    print("=== Safeguard 1 & 2: DEM Path Lock & Checksum Verification ===")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    free_gb = check_disk_space()

    # Verify count is exactly 4
    if len(APPROVED_TILES) != 4:
        raise ValueError(f"HARD FAILURE: Approved tile count must be exactly 4, got {len(APPROVED_TILES)}")

    checksums = set()
    tile_records = []

    for tile in APPROVED_TILES:
        path_obj = Path(tile["path"])
        if not path_obj.exists():
            raise FileNotFoundError(f"HARD FAILURE: Approved DEM file missing: {tile['path']}")
        
        if "pilot" in str(path_obj).lower():
            raise ValueError(f"HARD FAILURE: Pilot DEM detected in approved tiles: {tile['path']}")

        checksum = compute_checksum(path_obj)
        if checksum in checksums:
            raise ValueError(f"HARD FAILURE: Duplicate checksum detected: {checksum}")
        checksums.add(checksum)

        with rasterio.open(path_obj) as src:
            b = [round(x, 4) for x in [src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top]]
            rec = {
                "quadrant": tile["quadrant"],
                "absolute_path": str(path_obj),
                "parent_folder": path_obj.parent.name,
                "filename": path_obj.name,
                "bounds": json.dumps(b),
                "dimensions": f"{src.width}x{src.height}",
                "resolution": f"{src.res[0]:.6f}°",
                "full_checksum": checksum,
                "selection_status": "APPROVED_LOCKED"
            }
            tile_records.append(rec)
            print(f"  [LOCKED] {tile['quadrant']}: {path_obj.name} ({src.width}x{src.height}, {rec['resolution']})")

    # Save phase_2_approved_dem_sources.csv
    csv_path = REPORTS_DIR / "phase_2_approved_dem_sources.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "quadrant", "absolute_path", "parent_folder", "filename", "bounds",
            "dimensions", "resolution", "full_checksum", "selection_status"
        ])
        writer.writeheader()
        writer.writerows(tile_records)

    print(f"\nAPPROVED DEM PATH LOCK FILE CREATED: {csv_path}")
    print(f"Pilot DEM at '{EXCLUDED_PILOT_PATH}' remains EXCLUDED.\n")

if __name__ == "__main__":
    lock_dem_sources()
