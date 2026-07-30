"""
GeoSlide-JK — Create Deployment-Optimized 100m Terrain COGs
Resamples 30m full-J&K terrain rasters to the 100m Master Analysis Grid (EPSG:32643)
producing COGs < 20 MB each for GitHub & Render public deployment.
"""

import sys
from pathlib import Path
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MASTER_GRID_PATH = PROJECT_ROOT / "data" / "processed" / "susceptibility" / "jk_susceptibility_probability_100m.tif"
TERRAIN_DIR = PROJECT_ROOT / "data" / "processed" / "terrain"

# 30m Source paths
ELEV_30M = TERRAIN_DIR / "jk_elevation_glo30_cog.tif"
SLOPE_30M = TERRAIN_DIR / "jk_slope_degrees_cog.tif"
ASPECT_30M = TERRAIN_DIR / "jk_aspect_degrees_cog.tif"
HILLSHADE_30M = TERRAIN_DIR / "jk_hillshade_cog.tif"

# 100m Target deployment paths
ELEV_100M = TERRAIN_DIR / "jk_elevation_100m_cog.tif"
SLOPE_100M = TERRAIN_DIR / "jk_slope_degrees_100m_cog.tif"
ASPECT_100M = TERRAIN_DIR / "jk_aspect_degrees_100m_cog.tif"
HILLSHADE_100M = TERRAIN_DIR / "jk_hillshade_100m_cog.tif"

def main():
    print("=== GeoSlide-JK Deployment Terrain COG Generator ===")
    
    # 1. Load Master Analysis Grid Reference
    with rasterio.open(MASTER_GRID_PATH) as ref:
        dst_crs = ref.crs
        dst_transform = ref.transform
        dst_width = ref.width
        dst_height = ref.height
        master_data = ref.read(1)
        valid_mask = (master_data != ref.nodata) & (~np.isnan(master_data)) & (master_data >= 0)
        
    print(f"Master Grid Reference: {dst_width}x{dst_height}, CRS={dst_crs}, Valid Pixels={np.sum(valid_mask):,}")
    
    out_profile = {
        'driver': 'GTiff',
        'dtype': 'float32',
        'nodata': -9999.0,
        'width': dst_width,
        'height': dst_height,
        'count': 1,
        'crs': dst_crs,
        'transform': dst_transform,
        'tiled': True,
        'blockxsize': 256,
        'blockysize': 256,
        'compress': 'deflate',
        'predictor': 3
    }

    # 2. Resample Elevation (Bilinear)
    print("\nProcessing Elevation (30m -> 100m Bilinear)...")
    with rasterio.open(ELEV_30M) as src:
        dst_elev = np.full((dst_height, dst_width), -9999.0, dtype=np.float32)
        reproject(
            source=rasterio.band(src, 1),
            destination=dst_elev,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear,
            src_nodata=src.nodata,
            dst_nodata=-9999.0
        )
    dst_elev[~valid_mask] = -9999.0
    write_cog(ELEV_100M, dst_elev, out_profile)

    # 3. Resample Slope (Bilinear)
    print("\nProcessing Slope (30m -> 100m Bilinear)...")
    with rasterio.open(SLOPE_30M) as src:
        dst_slope = np.full((dst_height, dst_width), -9999.0, dtype=np.float32)
        reproject(
            source=rasterio.band(src, 1),
            destination=dst_slope,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear,
            src_nodata=src.nodata,
            dst_nodata=-9999.0
        )
    dst_slope[valid_mask] = np.clip(dst_slope[valid_mask], 0.0, 90.0)
    dst_slope[~valid_mask] = -9999.0
    write_cog(SLOPE_100M, dst_slope, out_profile)

    # 4. Resample Aspect (Circular Sin/Cos Decomposition)
    print("\nProcessing Aspect (30m -> 100m Circular Sin/Cos Decomposition)...")
    with rasterio.open(ASPECT_30M) as src:
        src_aspect = src.read(1).astype(np.float32)
        src_nodata = src.nodata if src.nodata is not None else -9999.0
        
        valid_src = (src_aspect != src_nodata) & (src_aspect >= 0.0) & (src_aspect <= 360.0)
        src_sin = np.full_like(src_aspect, -9999.0, dtype=np.float32)
        src_cos = np.full_like(src_aspect, -9999.0, dtype=np.float32)
        
        src_aspect_rad = np.radians(src_aspect[valid_src])
        src_sin[valid_src] = np.sin(src_aspect_rad)
        src_cos[valid_src] = np.cos(src_aspect_rad)
        
        dst_sin = np.full((dst_height, dst_width), -9999.0, dtype=np.float32)
        dst_cos = np.full((dst_height, dst_width), -9999.0, dtype=np.float32)
        
        reproject(
            source=src_sin,
            destination=dst_sin,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear,
            src_nodata=-9999.0,
            dst_nodata=-9999.0
        )
        reproject(
            source=src_cos,
            destination=dst_cos,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear,
            src_nodata=-9999.0,
            dst_nodata=-9999.0
        )
        
    dst_aspect = np.full((dst_height, dst_width), -9999.0, dtype=np.float32)
    valid_reconstructed = (
        valid_mask & 
        (dst_sin != -9999.0) & 
        (dst_cos != -9999.0) & 
        (~np.isnan(dst_sin)) & 
        (~np.isnan(dst_cos))
    )
    
    aspect_rad = np.arctan2(dst_sin[valid_reconstructed], dst_cos[valid_reconstructed])
    aspect_deg = np.degrees(aspect_rad) % 360.0
    aspect_deg[aspect_deg >= 360.0] = 0.0
    aspect_deg[aspect_deg < 0.0] = 0.0
    
    dst_aspect[valid_reconstructed] = aspect_deg
    dst_aspect[~valid_mask] = -9999.0
    write_cog(ASPECT_100M, dst_aspect, out_profile)

    # 5. Resample Hillshade (Bilinear)
    print("\nProcessing Hillshade (30m -> 100m Bilinear)...")
    with rasterio.open(HILLSHADE_30M) as src:
        dst_hill = np.full((dst_height, dst_width), -9999.0, dtype=np.float32)
        reproject(
            source=rasterio.band(src, 1),
            destination=dst_hill,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear,
            src_nodata=src.nodata,
            dst_nodata=-9999.0
        )
    dst_hill[valid_mask] = np.clip(dst_hill[valid_mask], 0.0, 255.0)
    dst_hill[~valid_mask] = -9999.0
    write_cog(HILLSHADE_100M, dst_hill, out_profile)
    
    print("\n=== Generation Complete ===")


def write_cog(out_path: Path, data: np.ndarray, profile: dict):
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(data, 1)
        overviews = [2, 4, 8, 16]
        dst.build_overviews(overviews, Resampling.nearest)
        dst.update_tags(ns='rio_overview', resampling='nearest')
        
    file_size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"Created {out_path.name}: {file_size_mb:.2f} MB")


if __name__ == "__main__":
    main()
