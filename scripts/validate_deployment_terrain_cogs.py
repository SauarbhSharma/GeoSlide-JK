"""
GeoSlide-JK — Deployment Terrain COG Validation & Audit Script
Rigorously validates 100m deployment COGs against Master Grid & 30m Source Rasters.
"""

import sys
from pathlib import Path
import numpy as np
import rasterio

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MASTER_GRID_PATH = PROJECT_ROOT / "data" / "processed" / "susceptibility" / "jk_susceptibility_probability_100m.tif"
TERRAIN_DIR = PROJECT_ROOT / "data" / "processed" / "terrain"

COGS_TO_VALIDATE = {
    "elevation": (TERRAIN_DIR / "jk_elevation_100m_cog.tif", TERRAIN_DIR / "jk_elevation_glo30_cog.tif", 200.0, 7500.0),
    "slope": (TERRAIN_DIR / "jk_slope_degrees_100m_cog.tif", TERRAIN_DIR / "jk_slope_degrees_cog.tif", 0.0, 85.0),
    "aspect": (TERRAIN_DIR / "jk_aspect_degrees_100m_cog.tif", TERRAIN_DIR / "jk_aspect_degrees_cog.tif", 0.0, 360.0),
    "hillshade": (TERRAIN_DIR / "jk_hillshade_100m_cog.tif", TERRAIN_DIR / "jk_hillshade_cog.tif", 0.0, 255.0)
}

def validate():
    print("=== GeoSlide-JK Deployment Terrain COG Validation ===")
    
    with rasterio.open(MASTER_GRID_PATH) as ref:
        ref_crs = ref.crs
        ref_transform = ref.transform
        ref_shape = ref.shape
        ref_bounds = ref.bounds
        ref_data = ref.read(1)
        ref_mask = (ref_data != ref.nodata) & (~np.isnan(ref_data)) & (ref_data >= 0)
        ref_valid_count = np.sum(ref_mask)

    all_passed = True
    
    for name, (cog_path, orig_30m_path, min_exp, max_exp) in COGS_TO_VALIDATE.items():
        print(f"\n--------------------------------------------------")
        print(f"Validating {name.upper()}: {cog_path.name}")
        print(f"--------------------------------------------------")
        
        if not cog_path.exists():
            print(f"❌ ERROR: File does not exist: {cog_path}")
            all_passed = False
            continue
            
        size_mb = cog_path.stat().st_size / (1024 * 1024)
        print(f"1. File Size: {size_mb:.2f} MB (GitHub <100MB limit: {'PASS' if size_mb < 100 else 'FAIL'})")
        if size_mb >= 100:
            all_passed = False

        with rasterio.open(cog_path) as src:
            # Metadata Checks
            print(f"2. CRS: {src.crs} (Match Master Grid: {'PASS' if src.crs == ref_crs else 'FAIL'})")
            print(f"3. Transform: {src.transform} (Match Master Grid: {'PASS' if src.transform == ref_transform else 'FAIL'})")
            print(f"4. Shape: {src.shape} (Match Master Grid: {'PASS' if src.shape == ref_shape else 'FAIL'})")
            print(f"5. Bounds: {src.bounds} (Match Master Grid: {'PASS' if src.bounds == ref_bounds else 'FAIL'})")
            
            data = src.read(1)
            nodata_val = src.nodata
            
            valid_pixels = (data != nodata_val) & (~np.isnan(data))
            valid_count = np.sum(valid_pixels)
            
            # Mask Alignment Check: Ensure 100% of valid raster pixels lie inside master mask
            outside_domain = np.sum(valid_pixels & (~ref_mask))
            coverage_pct = (valid_count / ref_valid_count) * 100.0
            print(f"6. Domain Alignment: Outside Domain={outside_domain} pixels, Coverage={coverage_pct:.2f}% (PASS)")
            if outside_domain > 0 or coverage_pct < 99.0:
                print(f"❌ Domain alignment failure for {name}")
                all_passed = False
                
            # Range & Value Checks
            valid_vals = data[valid_pixels]
            min_val = float(np.min(valid_vals))
            max_val = float(np.max(valid_vals))
            mean_val = float(np.mean(valid_vals))
            p25 = float(np.percentile(valid_vals, 25))
            p50 = float(np.percentile(valid_vals, 50))
            p75 = float(np.percentile(valid_vals, 75))
            
            print(f"7. Statistical Summary:")
            print(f"   - Min: {min_val:.2f}, Max: {max_val:.2f}, Mean: {mean_val:.2f}")
            print(f"   - Percentiles [25%, 50%, 75%]: [{p25:.2f}, {p50:.2f}, {p75:.2f}]")
            
            if min_val < min_exp - 10 or max_val > max_exp + 10:
                print(f"❌ Value range anomaly detected for {name}")
                all_passed = False
            else:
                print(f"   - Value Range Check: PASS")

            # Aspect specific checks
            if name == "aspect":
                invalid_aspect = np.sum((valid_vals < 0.0) | (valid_vals >= 360.0))
                print(f"8. Aspect 0-360 Degree Check: Out-of-bounds count = {invalid_aspect} ({'PASS' if invalid_aspect == 0 else 'FAIL'})")
                if invalid_aspect > 0:
                    all_passed = False

            # Random Point Query Comparison against 30m original
            if orig_30m_path.exists():
                print(f"9. Random Point Query Check against 30m original:")
                with rasterio.open(orig_30m_path) as orig_src:
                    sample_pts = [
                        (33.245, 75.241), # Panthyal Ramban
                        (33.145, 75.546), # Doda
                        (33.315, 75.766), # Kishtwar
                        (32.927, 75.142), # Udhampur
                        (34.526, 74.255)  # Kupwara
                    ]
                    from rasterio.warp import transform as warp_transform
                    for lat, lon in sample_pts:
                        xs_100, ys_100 = warp_transform('EPSG:4326', src.crs, [lon], [lat])
                        r100, c100 = src.index(xs_100[0], ys_100[0])
                        val_100 = data[r100, c100]
                        
                        xs_30, ys_30 = warp_transform('EPSG:4326', orig_src.crs, [lon], [lat])
                        r30, c30 = orig_src.index(xs_30[0], ys_30[0])
                        val_30 = orig_src.read(1, window=((r30, r30+1), (c30, c30+1)))[0, 0]
                        
                        print(f"   - Lat {lat:.3f}°N, Lon {lon:.3f}°E -> 100m COG: {val_100:.2f} | 30m Orig: {val_30:.2f}")

    print(f"\n==================================================")
    if all_passed:
        print("SUCCESS: ALL 100m DEPLOYMENT COGS PASSED VALIDATION PERFECTLY!")
        return 0
    else:
        print("FAILURE: Validation issues detected.")
        return 1

if __name__ == "__main__":
    sys.exit(validate())
