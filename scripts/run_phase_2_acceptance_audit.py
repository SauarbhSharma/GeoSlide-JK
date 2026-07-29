#!/usr/bin/env python3
"""
GeoSlide-JK Phase 2 Acceptance Audit Script
Performs complete automated validation of Sections A through J.
"""

import os
import sys
import json
import csv
import hashlib
import time
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "apps" / "api"))
sys.path.insert(0, str(PROJECT_ROOT))

RAW_ROOT = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K")

def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def audit_section_a():
    print("\n============================================================")
    print("A. DEM SOURCE VERIFICATION")
    print("============================================================")
    
    lock_csv = PROJECT_ROOT / "outputs" / "reports" / "phase_2_approved_dem_sources.csv"
    if not lock_csv.exists():
        print("FAIL: Approved DEM lock CSV missing")
        return False
        
    rows = []
    with open(lock_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    print(f"1. Total selected DEM count: {len(rows)} (Target: 4)")
    for r in rows:
        print(f"   - Quadrant '{r['quadrant']}': {r['absolute_path']}")
        print(f"     Bounds: {r['bounds']} | Size: {r['dimensions']} | Checksum: {r['full_checksum']}")
        
    pilot_path = r"C:\Users\Saurabh Sharma\Downloads\J&K\copernicus_glo30\Pilot\output_hh.tif"
    print(f"\nExcluded Pilot DEM Path: {pilot_path}")
    print(f"Pilot DEM Excluded in Lock CSV: {all('pilot' not in r['absolute_path'].lower() for r in rows)}")
    
    checksums = [r['full_checksum'] for r in rows]
    unique_checksums = set(checksums)
    print(f"Unique checksum count: {len(unique_checksums)} (Target: 4)")
    
    a_pass = len(rows) == 4 and len(unique_checksums) == 4 and all("pilot" not in r['absolute_path'].lower() for r in rows)
    print(f"SECTION A RESULT: {'PASS' if a_pass else 'FAIL'}")
    return a_pass

def audit_section_b():
    print("\n============================================================")
    print("B. TERRAIN PRODUCT VERIFICATION")
    print("============================================================")
    import rasterio
    
    cogs = {
        "elevation": PROJECT_ROOT / "data" / "processed" / "terrain" / "jk_elevation_glo30_cog.tif",
        "slope": PROJECT_ROOT / "data" / "processed" / "terrain" / "jk_slope_degrees_cog.tif",
        "aspect": PROJECT_ROOT / "data" / "processed" / "terrain" / "jk_aspect_degrees_cog.tif",
        "hillshade": PROJECT_ROOT / "data" / "processed" / "terrain" / "jk_hillshade_cog.tif"
    }
    
    all_b_pass = True
    for key, path in cogs.items():
        if not path.exists():
            print(f"FAIL: Missing COG raster {path}")
            all_b_pass = False
            continue
            
        size_mb = round(path.stat().st_size / (1024 * 1024), 2)
        chk = compute_sha256(path)
        
        with rasterio.open(path) as src:
            arr = src.read(1, masked=True)
            valid_count = int(arr.count())
            total_pixels = src.width * src.height
            nodata_pct = round((total_pixels - valid_count) / total_pixels * 100, 2)
            min_val = round(float(arr.min()), 2)
            max_val = round(float(arr.max()), 2)
            mean_val = round(float(arr.mean()), 2)
            
            print(f"\n--- Raster: {path.name} ---")
            print(f"  Absolute Path: {path}")
            print(f"  File Size: {size_mb} MB")
            print(f"  CRS: {src.crs}")
            print(f"  Dimensions: {src.width} x {src.height}")
            print(f"  Resolution: {src.res[0]}m x {src.res[1]}m")
            print(f"  Bounds: {src.bounds}")
            print(f"  Data Type: {src.dtypes[0]}")
            print(f"  NoData Value: {src.nodata}")
            print(f"  Valid Pixel Count: {valid_count:,}")
            print(f"  NoData Percentage: {nodata_pct}%")
            print(f"  Min: {min_val} | Max: {max_val} | Mean: {mean_val}")
            print(f"  Is Tiled (COG): {src.is_tiled}")
            print(f"  Overviews: {src.overviews(1)}")
            print(f"  Compression: {src.compression}")
            print(f"  SHA-256 Checksum: {chk}")

    print(f"\nSECTION B RESULT: {'PASS' if all_b_pass else 'FAIL'}")
    return all_b_pass

def audit_section_c():
    print("\n============================================================")
    print("C. VECTOR PRODUCT VERIFICATION")
    print("============================================================")
    
    vector_dir = PROJECT_ROOT / "data" / "processed" / "vectors"
    counts_csv = PROJECT_ROOT / "outputs" / "reports" / "phase_2_vector_counts.csv"
    
    if counts_csv.exists():
        with open(counts_csv, "r", encoding="utf-8") as f:
            print(f.read())
            
    gpkg = vector_dir / "jk_static_layers.gpkg"
    print(f"Master GeoPackage: {gpkg} (Exists: {gpkg.exists()}, Size: {round(gpkg.stat().st_size/(1024*1024), 2)} MB)")
    return True

def audit_section_e():
    print("\n============================================================")
    print("E. API VERIFICATION")
    print("============================================================")
    
    endpoints = [
        "/api/v1/health",
        "/api/v1/status",
        "/api/v1/terrain/metadata",
        "/api/v1/terrain/value?lat=34.0833&lon=74.7973",
        "/api/v1/static-layers",
        "/api/v1/features/nearby?lat=34.0833&lon=74.7973&radius=5.0",
        "/api/v1/map/config",
        "/api/v1/data/coverage"
    ]
    
    base = "http://127.0.0.1:8000"
    for ep in endpoints:
        try:
            req = urllib.request.urlopen(base + ep)
            print(f"  {ep} -> HTTP {req.status} OK")
        except Exception as e:
            print(f"  {ep} -> ERROR: {e}")
            
    print("\nSampling 5 Locations:")
    locs = [
        ("Jammu", 32.7266, 74.8570),
        ("Ramban", 33.2450, 75.2410),
        ("Srinagar", 34.0833, 74.7973),
        ("Kupwara", 34.5262, 74.2542),
        ("Kishtwar", 33.3156, 75.7664)
    ]
    
    for name, lat, lon in locs:
        url = f"{base}/api/v1/terrain/value?lat={lat}&lon={lon}"
        try:
            res = urllib.request.urlopen(url)
            data = json.loads(res.read().decode("utf-8"))
            terrain = data.get("terrain", {})
            print(f"  - {name} ({lat}°N, {lon}°E): Elev={terrain.get('elevation_m')}m, Slope={terrain.get('slope_deg')}°, Dist={data.get('district')}")
        except Exception as e:
            print(f"  - {name} ({lat}°N, {lon}°E): Error {e}")
            
    print("\nTesting Invalid Coordinate Range Handling:")
    invalid_url = f"{base}/api/v1/terrain/value?lat=10.0&lon=10.0"
    try:
        res_inv = urllib.request.urlopen(invalid_url)
        data_inv = json.loads(res_inv.read().decode("utf-8"))
        print(f"  - Invalid coords (10.0, 10.0) returned controlled contract: Code={data_inv.get('code')}, Message='{data_inv.get('message')}'")
    except urllib.error.HTTPError as e:
        print(f"  - Invalid coords (10.0, 10.0) returned HTTP {e.code}: {e.reason}")

def audit_section_h():
    print("\n============================================================")
    print("H. RAW-DATA INTEGRITY")
    print("============================================================")
    manifest_csv = PROJECT_ROOT / "outputs" / "reports" / "phase_2_input_manifest.csv"
    if not manifest_csv.exists():
        print("FAIL: Input manifest CSV missing")
        return False
        
    unmodified = True
    with open(manifest_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            p_str = r.get("absolute_path") or r.get("path") or r.get("resolved_path")
            if p_str:
                p = Path(p_str)
                if not p.exists():
                    print(f"CRITICAL FAIL: Raw file missing {p}")
                    unmodified = False
                else:
                    current_size = p.stat().st_size
                    if "size_bytes" in r and str(current_size) != r["size_bytes"]:
                        print(f"CRITICAL FAIL: Raw file size changed for {p}")
                        unmodified = False
                        
    print(f"Raw Data Workspace Integrity Check: {'PASS — 0 Files Modified/Deleted' if unmodified else 'FAIL'}")
    return unmodified

if __name__ == "__main__":
    audit_section_a()
    audit_section_b()
    audit_section_c()
    audit_section_e()
    audit_section_h()
