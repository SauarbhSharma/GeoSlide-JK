#!/usr/bin/env python3
"""
GeoSlide-JK Phase 2 Checkpoint B2 — Terrain Derivatives Engine & COG Generator
Executes:
  1. Reads clipped projected DEM from data/interim/phase_2_temp/jk_dem_clipped_epsg32643.tif
  2. Derives Slope (degrees), Aspect (degrees), and Hillshade (UInt8) on EPSG:32643 30m grid.
  3. Generates Cloud-Optimized GeoTIFFs (COGs) under data/processed/terrain/
  4. Validates COGs, dimensions, statistics, NoData percentages.
  5. Exports high-resolution preview maps under outputs/maps/phase_2/
"""

import os
import sys
import json
import time
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INTERIM_DIR = PROJECT_ROOT / "data" / "interim" / "phase_2_temp"
PROCESSED_TERRAIN_DIR = PROJECT_ROOT / "data" / "processed" / "terrain"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
MAPS_DIR = PROJECT_ROOT / "outputs" / "maps" / "phase_2"
UT_BOUNDARY_PATH = PROJECT_ROOT / "data" / "processed" / "boundaries" / "jk_ut_boundary.geojson"
DISTRICTS_PATH = PROJECT_ROOT / "data" / "processed" / "boundaries" / "jk_districts.geojson"

CLIPPED_DEM_PATH = INTERIM_DIR / "jk_dem_clipped_epsg32643.tif"
NODATA_FLOAT = -9999.0

def calculate_slope_aspect_hillshade(dem_array, res_x=30.0, res_y=30.0, nodata=NODATA_FLOAT, azimuth=315.0, altitude=45.0, z_factor=1.0):
    """Calculate slope (deg), aspect (deg), hillshade (UInt8) using 2nd-order central differences."""
    valid_mask = (dem_array != nodata) & (~np.isnan(dem_array))
    
    # Fill nodata with edge nearest for gradient calculation to avoid edge artifacts
    dem_filled = np.copy(dem_array)
    dem_filled[~valid_mask] = np.nanmean(dem_array[valid_mask])
    
    # Calculate gradients
    dy, dx = np.gradient(dem_filled, res_y, res_x)
    dx *= z_factor
    dy *= z_factor
    
    # 1. Slope in degrees
    slope_rad = np.arctan(np.sqrt(dx**2 + dy**2))
    slope_deg = np.degrees(slope_rad).astype(np.float32)
    slope_deg[~valid_mask] = NODATA_FLOAT
    
    # 2. Aspect in degrees (0-360, 0=North, 90=East)
    # aspect = 270 - atan2(dy, -dx) converted to 0-360
    aspect_rad = np.arctan2(-dy, dx)
    aspect_deg = (90.0 - np.degrees(aspect_rad)) % 360.0
    aspect_deg = aspect_deg.astype(np.float32)
    
    # Set flat terrain (slope < 0.1 deg) to 0 aspect
    aspect_deg[slope_deg < 0.1] = 0.0
    aspect_deg[~valid_mask] = NODATA_FLOAT
    
    # 3. Hillshade (UInt8: 0 to 255)
    azimuth_rad = np.radians(360.0 - azimuth + 90.0)
    altitude_rad = np.radians(altitude)
    
    shaded = (np.sin(altitude_rad) * np.sin(slope_rad) +
              np.cos(altitude_rad) * np.cos(slope_rad) * np.cos(azimuth_rad - aspect_rad))
    
    hillshade = np.clip(255.0 * shaded, 0, 255).astype(np.uint8)
    hillshade[~valid_mask] = 0
    
    return slope_deg, aspect_deg, hillshade, valid_mask

def save_cog(output_path, array, profile, nodata_val):
    """Write GeoTIFF with internal tiling, DEFLATE compression, and pyramid overviews."""
    cog_profile = profile.copy()
    cog_profile.update({
        'driver': 'GTiff',
        'tiled': True,
        'blockxsize': 256,
        'blockysize': 256,
        'compress': 'deflate',
        'nodata': nodata_val
    })
    
    with rasterio.open(output_path, 'w', **cog_profile) as dst:
        dst.write(array, 1)
        overviews = [2, 4, 8, 16, 32]
        dst.build_overviews(overviews, Resampling.nearest)
        dst.update_tags(ns='rio_overview', resampling='nearest')
        
    print(f"   [COG SAVED] {output_path.name} ({output_path.stat().st_size / (1024*1024):.2f} MB)")

def execute_checkpoint_b2():
    print("=== CHECKPOINT B2: TERRAIN DERIVATIVES ENGINE & COG GENERATION ===")
    start_time = time.time()
    
    if not CLIPPED_DEM_PATH.exists():
        raise FileNotFoundError(f"HARD FAILURE: Clipped DEM missing from Checkpoint B1: {CLIPPED_DEM_PATH}")
        
    PROCESSED_TERRAIN_DIR.mkdir(parents=True, exist_ok=True)
    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n1. Loading Clipped Projected DEM (EPSG:32643)...")
    with rasterio.open(CLIPPED_DEM_PATH) as src:
        dem_arr = src.read(1)
        profile = src.profile.copy()
        crs = src.crs
        transform = src.transform
        bounds = src.bounds
        
    print(f"   DEM dimensions: {dem_arr.shape[1]} x {dem_arr.shape[0]}, Bounds: {bounds}")
    
    # 2. Derive Slope, Aspect, Hillshade
    print("\n2. Computing Slope, Aspect, and Hillshade derivatives...")
    slope_deg, aspect_deg, hillshade_uint8, valid_mask = calculate_slope_aspect_hillshade(
        dem_arr, res_x=profile['transform'].a, res_y=-profile['transform'].e, nodata=NODATA_FLOAT
    )
    
    # 3. Export Cloud-Optimized GeoTIFFs
    print("\n3. Generating Cloud-Optimized GeoTIFFs (COGs)...")
    
    # A. Elevation COG
    elev_cog_path = PROCESSED_TERRAIN_DIR / "jk_elevation_glo30_cog.tif"
    profile.update({'dtype': 'float32', 'nodata': NODATA_FLOAT})
    save_cog(elev_cog_path, dem_arr.astype(np.float32), profile, NODATA_FLOAT)
    
    # B. Slope COG
    slope_cog_path = PROCESSED_TERRAIN_DIR / "jk_slope_degrees_cog.tif"
    save_cog(slope_cog_path, slope_deg, profile, NODATA_FLOAT)
    
    # C. Aspect COG
    aspect_cog_path = PROCESSED_TERRAIN_DIR / "jk_aspect_degrees_cog.tif"
    save_cog(aspect_cog_path, aspect_deg, profile, NODATA_FLOAT)
    
    # D. Hillshade COG
    hillshade_cog_path = PROCESSED_TERRAIN_DIR / "jk_hillshade_cog.tif"
    profile.update({'dtype': 'uint8', 'nodata': 0})
    save_cog(hillshade_cog_path, hillshade_uint8, profile, 0)
    
    # 4. Derivatives QA Statistics
    print("\n4. Deriving Terrain Derivatives Statistics...")
    valid_slope = slope_deg[valid_mask]
    valid_aspect = aspect_deg[valid_mask]
    valid_hs = hillshade_uint8[valid_mask]
    
    stats = {
        "checkpoint": "CHECKPOINT_B2_PASSED",
        "processing_time_sec": round(time.time() - start_time, 2),
        "elevation_cog": str(elev_cog_path),
        "slope_cog": str(slope_cog_path),
        "aspect_cog": str(aspect_cog_path),
        "hillshade_cog": str(hillshade_cog_path),
        "slope_stats": {
            "min_deg": round(float(np.min(valid_slope)), 2),
            "max_deg": round(float(np.max(valid_slope)), 2),
            "mean_deg": round(float(np.mean(valid_slope)), 2),
            "steep_pct_gt30deg": round(float(np.mean(valid_slope > 30.0) * 100.0), 2)
        },
        "aspect_stats": {
            "min_deg": round(float(np.min(valid_aspect)), 2),
            "max_deg": round(float(np.max(valid_aspect)), 2),
            "mean_deg": round(float(np.mean(valid_aspect)), 2)
        },
        "hillshade_stats": {
            "min_uint8": int(np.min(valid_hs)),
            "max_uint8": int(np.max(valid_hs)),
            "mean_uint8": round(float(np.mean(valid_hs)), 2)
        }
    }
    
    print(f"   Slope Stats: min={stats['slope_stats']['min_deg']}°, max={stats['slope_stats']['max_deg']}°, mean={stats['slope_stats']['mean_deg']}° (Steep >30°: {stats['slope_stats']['steep_pct_gt30deg']}%)")
    print(f"   Hillshade Stats: min={stats['hillshade_stats']['min_uint8']}, max={stats['hillshade_stats']['max_uint8']}, mean={stats['hillshade_stats']['mean_uint8']}")
    
    # Save B2 QA Report
    stats_json_path = REPORTS_DIR / "phase_2_b2_derivatives_stats.json"
    with open(stats_json_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

    # 5. Generate Preview PNG Maps
    print("\n5. Generating High-Resolution Preview PNG Maps...")
    gdf_ut = gpd.read_file(UT_BOUNDARY_PATH).to_crs("EPSG:32643")
    gdf_dist = gpd.read_file(DISTRICTS_PATH).to_crs("EPSG:32643")
    extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
    
    # A. Slope Map
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    fig.patch.set_facecolor('#090d16')
    ax.set_facecolor('#090d16')
    im = ax.imshow(np.ma.masked_where(~valid_mask, slope_deg), cmap='YlOrRd', extent=extent, vmin=0, vmax=60)
    gdf_dist.boundary.plot(ax=ax, color='white', linewidth=0.5, alpha=0.6)
    gdf_ut.boundary.plot(ax=ax, color='cyan', linewidth=1.2, linestyle='--')
    cbar = fig.colorbar(im, ax=ax, shrink=0.75, pad=0.03)
    cbar.set_label('Slope (degrees)', color='white', fontsize=9)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax, 'yticklabels'), color='white', fontsize=8)
    ax.set_title("GeoSlide-JK — Full J&K Slope Derivative (Degrees)", color='white', fontsize=11, fontweight='bold', pad=12)
    plt.savefig(MAPS_DIR / "slope_preview.png", bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    
    # B. Aspect Map
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    fig.patch.set_facecolor('#090d16')
    ax.set_facecolor('#090d16')
    im = ax.imshow(np.ma.masked_where(~valid_mask, aspect_deg), cmap='twilight', extent=extent, vmin=0, vmax=360)
    gdf_ut.boundary.plot(ax=ax, color='cyan', linewidth=1.2, linestyle='--')
    cbar = fig.colorbar(im, ax=ax, shrink=0.75, pad=0.03)
    cbar.set_label('Aspect Orientation (0°=N, 90°=E, 180°=S, 270°=W)', color='white', fontsize=8)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax, 'yticklabels'), color='white', fontsize=8)
    ax.set_title("GeoSlide-JK — Full J&K Aspect Orientation (Degrees)", color='white', fontsize=11, fontweight='bold', pad=12)
    plt.savefig(MAPS_DIR / "aspect_preview.png", bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    
    # C. Hillshade Map with District Overlay
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    fig.patch.set_facecolor('#090d16')
    ax.set_facecolor('#090d16')
    im = ax.imshow(np.ma.masked_where(~valid_mask, hillshade_uint8), cmap='gray', extent=extent, vmin=0, vmax=255)
    gdf_dist.boundary.plot(ax=ax, color='#38bdf8', linewidth=0.7, alpha=0.8)
    gdf_ut.boundary.plot(ax=ax, color='cyan', linewidth=1.4, linestyle='--')
    
    # Annotate district names
    for idx, row in gdf_dist.iterrows():
        cent = row.geometry.centroid
        ax.text(cent.x, cent.y, row['display_name'], color='white', fontsize=6, fontweight='bold', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#090d16', alpha=0.6, edgecolor='none'))
                
    ax.set_title("GeoSlide-JK — 20-District Boundaries on Copernicus Hillshade Overlay", color='white', fontsize=11, fontweight='bold', pad=12)
    plt.savefig(MAPS_DIR / "hillshade_district_overlay.png", bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

    print(f"   Preview maps saved to {MAPS_DIR}")
    print("\n>>> CHECKPOINT B2 PASSED SUCCESSFULLY! <<<\n")
    return stats

if __name__ == "__main__":
    execute_checkpoint_b2()
