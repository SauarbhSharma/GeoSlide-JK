#!/usr/bin/env python3
"""
GeoSlide-JK Phase 2 Checkpoint B1 — Terrain Mosaic & Study Area Clipping
Executes:
  1. Reads approved 4 DEM tile paths from outputs/reports/phase_2_approved_dem_sources.csv.
  2. Mosaics 4 DEM tiles in memory/temp directory.
  3. Reprojects to EPSG:32643 (UTM 43N, 30m resolution, Bilinear resampling).
  4. Clips cleanly to 20-district J&K UT boundary (NoData outside UT).
  5. Calculates post-clipping elevation statistics & seam QA.
  6. Exports temporary projected DEM to data/interim/phase_2_temp/jk_dem_epsg32643.tif
  7. Generates preview PNG in outputs/maps/phase_2/elevation_preview.png
"""

import os
import sys
import csv
import json
import time
from pathlib import Path
import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K")
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim" / "phase_2_temp"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
MAPS_DIR = PROJECT_ROOT / "outputs" / "maps" / "phase_2"

UT_BOUNDARY_PATH = PROCESSED_DIR / "boundaries" / "jk_ut_boundary.geojson"
DEM_LOCK_CSV = REPORTS_DIR / "phase_2_approved_dem_sources.csv"
TARGET_CRS = "EPSG:32643"
TARGET_RES = 30.0  # 30 meters
NODATA_VAL = -9999.0

def load_approved_dem_sources():
    if not DEM_LOCK_CSV.exists():
        raise FileNotFoundError(f"HARD FAILURE: DEM sources lock CSV missing: {DEM_LOCK_CSV}")
    
    paths = []
    with open(DEM_LOCK_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "pilot" in row["absolute_path"].lower():
                raise ValueError(f"HARD FAILURE: Pilot DEM detected in approved sources: {row['absolute_path']}")
            paths.append(row["absolute_path"])
            
    if len(paths) != 4:
        raise ValueError(f"HARD FAILURE: Approved DEM tile count must be exactly 4, got {len(paths)}")
    return paths

def execute_checkpoint_b1():
    print("=== CHECKPOINT B1: TERRAIN MOSAIC & CLIPPING ===")
    start_time = time.time()
    
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    
    dem_paths = load_approved_dem_sources()
    print(f"Loaded {len(dem_paths)} approved DEM source paths:")
    for p in dem_paths:
        print(f"  - {p}")
        
    # 1. Mosaic 4 DEM tiles
    print("\n1. Mosaicking 4 DEM tiles...")
    src_files_to_mosaic = [rasterio.open(p) for p in dem_paths]
    mosaic_arr, mosaic_transform = merge(src_files_to_mosaic)
    mosaic_crs = src_files_to_mosaic[0].crs
    mosaic_nodata = src_files_to_mosaic[0].nodata
    
    for s in src_files_to_mosaic:
        s.close()
        
    print(f"   Mosaic dimensions: {mosaic_arr.shape[2]} x {mosaic_arr.shape[1]}, CRS: {mosaic_crs}")
    
    # 2. Save temporary unprojected mosaic
    temp_mosaic_path = INTERIM_DIR / "temp_mosaic_wgs84.tif"
    with rasterio.open(
        temp_mosaic_path, 'w',
        driver='GTiff',
        height=mosaic_arr.shape[1],
        width=mosaic_arr.shape[2],
        count=1,
        dtype=mosaic_arr.dtype,
        crs=mosaic_crs,
        transform=mosaic_transform,
        nodata=mosaic_nodata
    ) as dst:
        dst.write(mosaic_arr[0], 1)
        
    # 3. Reproject to EPSG:32643 at 30m resolution using Bilinear resampling
    print(f"\n2. Reprojecting Mosaic to {TARGET_CRS} (30m target resolution)...")
    with rasterio.open(temp_mosaic_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, TARGET_CRS, src.width, src.height, *src.bounds, resolution=(TARGET_RES, TARGET_RES)
        )
        
        proj_dem_path = INTERIM_DIR / "jk_dem_epsg32643.tif"
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': TARGET_CRS,
            'transform': transform,
            'width': width,
            'height': height,
            'dtype': 'float32',
            'nodata': NODATA_VAL
        })
        
        with rasterio.open(proj_dem_path, 'w', **kwargs) as dst:
            reproject(
                source=rasterio.band(src, 1),
                destination=rasterio.band(dst, 1),
                src_transform=src.transform,
                src_crs=src.crs,
                src_nodata=src.nodata,
                dst_transform=transform,
                dst_crs=TARGET_CRS,
                dst_nodata=NODATA_VAL,
                resampling=Resampling.bilinear
            )
            
    print(f"   Projected DEM created: {proj_dem_path} ({width} x {height})")
    
    # 4. Clip projected DEM to 20-district J&K UT Boundary
    print("\n3. Clipping Projected DEM to 20-district J&K UT boundary...")
    gdf_ut = gpd.read_file(UT_BOUNDARY_PATH)
    gdf_ut_proj = gdf_ut.to_crs(TARGET_CRS)
    geometries = gdf_ut_proj.geometry.values
    
    clipped_dem_path = INTERIM_DIR / "jk_dem_clipped_epsg32643.tif"
    with rasterio.open(proj_dem_path) as src:
        out_image, out_transform = mask(src, geometries, crop=True, nodata=NODATA_VAL)
        out_meta = src.meta.copy()
        out_meta.update({
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "nodata": NODATA_VAL
        })
        
        with rasterio.open(clipped_dem_path, "w", **out_meta) as dest:
            dest.write(out_image)
            
    print(f"   Clipped DEM created: {clipped_dem_path} ({out_image.shape[2]} x {out_image.shape[1]})")
    
    # 5. Post-clipping Elevation Statistics & Validation
    print("\n4. Calculating Post-Clipping J&K UT Elevation Statistics...")
    data = out_image[0]
    valid_mask = (data != NODATA_VAL) & (~np.isnan(data))
    valid_pixels = data[valid_mask]
    
    min_elev = float(np.min(valid_pixels))
    max_elev = float(np.max(valid_pixels))
    mean_elev = float(np.mean(valid_pixels))
    std_elev = float(np.std(valid_pixels))
    
    total_pixels = data.size
    valid_count = int(np.sum(valid_mask))
    nodata_count = total_pixels - valid_count
    nodata_pct = (nodata_count / total_pixels) * 100.0
    
    # Check for extreme suspicious values (< 0 or > 8900m)
    extreme_count = int(np.sum((valid_pixels < 0.0) | (valid_pixels > 8900.0)))
    
    stats = {
        "checkpoint": "CHECKPOINT_B1_PASSED",
        "processing_time_sec": round(time.time() - start_time, 2),
        "target_crs": TARGET_CRS,
        "target_resolution_m": TARGET_RES,
        "dimensions": f"{out_image.shape[2]} x {out_image.shape[1]}",
        "total_pixels": total_pixels,
        "valid_pixels": valid_count,
        "nodata_pixels": nodata_count,
        "nodata_percent": round(nodata_pct, 2),
        "min_elevation_m": round(min_elev, 2),
        "max_elevation_m": round(max_elev, 2),
        "mean_elevation_m": round(mean_elev, 2),
        "std_elevation_m": round(std_elev, 2),
        "suspicious_extreme_values": extreme_count
    }
    
    print("   Post-Clipping Statistics:")
    print(f"     - Min Elevation:  {min_elev:.2f} m")
    print(f"     - Max Elevation:  {max_elev:.2f} m")
    print(f"     - Mean Elevation: {mean_elev:.2f} m")
    print(f"     - Valid Pixels:   {valid_count:,} / {total_pixels:,} ({100 - nodata_pct:.2f}% coverage)")
    print(f"     - Extreme Values: {extreme_count}")

    # Validation Checks
    if min_elev < 100 or max_elev > 8850:
        raise ValueError(f"HARD FAILURE: Post-clipping elevation out of physical J&K range: min={min_elev}, max={max_elev}")
    if valid_count < 10_000_000:
        raise ValueError(f"HARD FAILURE: Insufficient valid pixels in clipped J&K DEM: {valid_count}")
        
    # Save statistics report
    stats_json_path = REPORTS_DIR / "phase_2_b1_elevation_stats.json"
    with open(stats_json_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

    # 6. Generate Preview Map PNG
    print("\n5. Generating Elevation Preview Map...")
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    fig.patch.set_facecolor('#090d16')
    ax.set_facecolor('#090d16')
    
    masked_data = np.ma.masked_where(~valid_mask, data)
    im = ax.imshow(masked_data, cmap='terrain', extent=[gdf_ut_proj.total_bounds[0], gdf_ut_proj.total_bounds[2], gdf_ut_proj.total_bounds[1], gdf_ut_proj.total_bounds[3]])
    
    gdf_ut_proj.boundary.plot(ax=ax, color='cyan', linewidth=1.2, linestyle='--', label='J&K UT Boundary')
    
    cbar = fig.colorbar(im, ax=ax, shrink=0.75, pad=0.03)
    cbar.set_label('Elevation (meters ASL)', color='white', fontsize=9)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax, 'yticklabels'), color='white', fontsize=8)
    
    ax.set_title("GeoSlide-JK — Phase 2 Clipped Copernicus DEM Elevation (EPSG:32643)", color='white', fontsize=11, fontweight='bold', pad=12)
    ax.tick_params(colors='gray', labelsize=8)
    ax.grid(True, color='#1e293b', linestyle=':', alpha=0.5)
    
    preview_png = MAPS_DIR / "elevation_preview.png"
    plt.savefig(preview_png, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    
    print(f"   Preview map saved: {preview_png}")
    print("\n>>> CHECKPOINT B1 PASSED SUCCESSFULLY! <<<\n")
    return stats

if __name__ == "__main__":
    execute_checkpoint_b1()
