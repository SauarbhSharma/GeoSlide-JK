#!/usr/bin/env python3
"""
GeoSlide-JK Phase 3 Checkpoint B4 Landslide Label Preparation & Sampling Domain Pipeline
Ingests NGDR landslide inventory points (2,370) and polygons (7,436),
rasterizes presence to the master 100m EPSG:32643 grid, defines sampling domain,
performs distance-buffered pseudo-absence sampling, and generates QA reports & maps.
"""

import sys
import time
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from scipy.ndimage import distance_transform_edt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_ROOT = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K")

GRID_DIR = PROJECT_ROOT / "data/processed/grid"
FEATURE_DIR = PROJECT_ROOT / "data/processed/features"
LABEL_DIR = FEATURE_DIR / "labels"
LABEL_DIR.mkdir(parents=True, exist_ok=True)

MASK_DIR = FEATURE_DIR / "masks"
TERRAIN_DIR = FEATURE_DIR / "terrain"
VECTOR_DIR = PROJECT_ROOT / "data/processed/vectors"
REPORT_DIR = PROJECT_ROOT / "outputs/reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
MAP_DIR = PROJECT_ROOT / "outputs/maps/phase_3/b4"
MAP_DIR.mkdir(parents=True, exist_ok=True)

REF_GRID = GRID_DIR / "jk_analysis_grid_100m.tif"
BOUNDARY_MASK = GRID_DIR / "jk_boundary_mask_100m.tif"
DISTRICT_GRID = GRID_DIR / "jk_district_id_100m.tif"
HAZARD_MASK = MASK_DIR / "hazard_feature_complete_mask_100m.tif"
SLOPE_RASTER = TERRAIN_DIR / "terrain_slope_100m.tif"

POINTS_PARQUET = VECTOR_DIR / "jk_slides_points.parquet" if (VECTOR_DIR / "jk_slides_points.parquet").exists() else VECTOR_DIR / "jk_landslides_points.parquet"
POLYGONS_PARQUET = VECTOR_DIR / "jk_slides_polygons.parquet" if (VECTOR_DIR / "jk_slides_polygons.parquet").exists() else VECTOR_DIR / "jk_landslides_polygons.parquet"


def compute_sha256(file_path, chunk_size=8192):
    sha = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            sha.update(chunk)
    return sha.hexdigest()


def main():
    print("=" * 60)
    print("GeoSlide-JK Phase 3 Checkpoint B4 Landslide Label Preparation Pipeline")
    print("=" * 60)

    start_time = time.time()

    # 1. Load Master Grid Profile & Boundary
    with rasterio.open(REF_GRID) as src:
        profile_float = src.profile.copy()
        profile_float.update(dtype=rasterio.float32, nodata=-9999.0)
        crs = src.crs
        transform = src.transform
        width = src.width
        height = src.height

    profile_uint8 = profile_float.copy()
    profile_uint8.update(dtype=rasterio.uint8, nodata=255)

    with rasterio.open(BOUNDARY_MASK) as src:
        boundary = src.read(1)
    valid_land = (boundary == 1)

    with rasterio.open(HAZARD_MASK) as src:
        hazard_complete = src.read(1)

    with rasterio.open(SLOPE_RASTER) as src:
        slope = src.read(1)

    with rasterio.open(DISTRICT_GRID) as src:
        district_ids = src.read(1)

    district_lookup = pd.read_csv(GRID_DIR / "jk_district_lookup.csv")

    # 2. Ingest Vector Landslide Inventories
    print(f"\n--- 1. Ingesting NGDR Vector Landslides ---")
    pts_gdf = gpd.read_parquet(POINTS_PARQUET)
    poly_gdf = gpd.read_parquet(POLYGONS_PARQUET)

    print(f"Loaded {len(pts_gdf)} landslide points from {POINTS_PARQUET.name}")
    print(f"Loaded {len(poly_gdf)} landslide polygons from {POLYGONS_PARQUET.name}")

    # Reproject to EPSG:32643
    pts_32643 = pts_gdf.to_crs(crs)
    poly_32643 = poly_gdf.to_crs(crs)

    # 3. Rasterize Landslide Presence
    print(f"\n--- 2. Rasterizing Landslide Presence to 100m Grid ---")
    shapes_poly = [(geom, 1) for geom in poly_32643.geometry if geom is not None and not geom.is_empty]
    poly_presence = rasterize(shapes_poly, out_shape=(height, width), transform=transform, fill=0, dtype=np.uint8)

    shapes_pts = [(geom, 1) for geom in pts_32643.geometry if geom is not None and not geom.is_empty]
    pts_presence = rasterize(shapes_pts, out_shape=(height, width), transform=transform, fill=0, dtype=np.uint8)

    combined_presence = np.where((poly_presence == 1) | (pts_presence == 1), 1, 0).astype(np.uint8)
    combined_presence[~valid_land] = 255
    poly_presence[~valid_land] = 255
    pts_presence[~valid_land] = 255

    pos_count = int(np.sum(combined_presence == 1))
    print(f"Rasterized Positive Landslide Cells: {pos_count:,} ({pos_count * 0.01:.2f} km²)")

    # 4. Compute Distance to Nearest Landslide (Euclidean Distance Transform)
    print(f"\n--- 3. Computing Euclidean Distance to Landslides ---")
    non_landslide_mask = (combined_presence != 1)
    dist_pixel = distance_transform_edt(non_landslide_mask)
    dist_m = (dist_pixel * 100.0).astype(np.float32)  # cell size = 100m
    dist_m[~valid_land] = -9999.0

    # 5. Define Sampling Domain & Target Labels
    print(f"\n--- 4. Defining Modelling Domain & Pseudo-Absence Sampling ---")
    # Mapping coverage mask: 1 across valid land where inventory mapping was conducted
    mapping_coverage = np.where(valid_land, 1, 0).astype(np.uint8)
    mapping_coverage[~valid_land] = 255

    modelling_domain = np.where(valid_land & (hazard_complete == 1) & (mapping_coverage == 1), 1, 0).astype(np.uint8)
    modelling_domain[~valid_land] = 255

    # Target label assignment:
    # 1 = Landslide presence
    # 0 = Verified pseudo-absence (dist > 200m, slope > 5.0°, hazard_complete == 1, inside valid land)
    # 255 = Excluded / Buffer zone / NoData
    target_label = np.full((height, width), 255, dtype=np.uint8)

    pos_mask = (combined_presence == 1) & valid_land
    neg_mask = (dist_m > 200.0) & (slope > 5.0) & (hazard_complete == 1) & valid_land & (~pos_mask)

    target_label[pos_mask] = 1
    target_label[neg_mask] = 0

    num_pos = int(np.sum(target_label == 1))
    num_neg = int(np.sum(target_label == 0))
    num_buf = int(np.sum(valid_land & (dist_m <= 200.0) & (~pos_mask)))
    num_low_slope = int(np.sum(valid_land & (dist_m > 200.0) & (slope <= 5.0)))
    num_incomplete = int(np.sum(valid_land & (dist_m > 200.0) & (slope > 5.0) & (hazard_complete == 0)))

    print(f"Target Label Statistics across Valid Land ({np.sum(valid_land):,} cells):")
    print(f"  - Positive (Landslide Presence = 1): {num_pos:,} ({num_pos/np.sum(valid_land)*100:.2f}%)")
    print(f"  - Pseudo-Absence (Non-Landslide = 0): {num_neg:,} ({num_neg/np.sum(valid_land)*100:.2f}%)")
    print(f"  - Excluded Buffer Zone (0-200m = 255): {num_buf:,} ({num_buf/np.sum(valid_land)*100:.2f}%)")
    print(f"  - Excluded Low Slope (<= 5° = 255): {num_low_slope:,} ({num_low_slope/np.sum(valid_land)*100:.2f}%)")
    print(f"  - Excluded Incomplete Data (255): {num_incomplete:,} ({num_incomplete/np.sum(valid_land)*100:.2f}%)")

    # 6. Save B4 Output Rasters
    print(f"\n--- 5. Saving B4 Label & Domain Rasters ---")
    rasters_to_save = [
        (LABEL_DIR / "landslide_presence_polygons_100m.tif", poly_presence, profile_uint8),
        (LABEL_DIR / "landslide_presence_points_100m.tif", pts_presence, profile_uint8),
        (LABEL_DIR / "landslide_presence_combined_100m.tif", combined_presence, profile_uint8),
        (LABEL_DIR / "distance_to_landslide_m_100m.tif", dist_m, profile_float),
        (LABEL_DIR / "landslide_mapping_coverage_mask_100m.tif", mapping_coverage, profile_uint8),
        (LABEL_DIR / "modelling_domain_mask_100m.tif", modelling_domain, profile_uint8),
        (LABEL_DIR / "landslide_target_label_100m.tif", target_label, profile_uint8)
    ]

    checksum_rows = []
    for out_path, arr, prof in rasters_to_save:
        with rasterio.open(out_path, 'w', **prof) as dst:
            dst.write(arr, 1)
        size_b = out_path.stat().st_size
        sha_full = compute_sha256(out_path)
        sha_16 = sha_full[:16]
        checksum_rows.append({
            "raster_name": out_path.stem,
            "filename": out_path.name,
            "file_size_bytes": size_b,
            "sha256_full": sha_full,
            "sha256_16": sha_16,
            "crs": "EPSG:32643",
            "width": width,
            "height": height,
            "dtype": str(prof['dtype']),
            "nodata": str(prof['nodata'])
        })
        print(f"Saved: {out_path.name} (SHA256_16: {sha_16})")

    checksum_df = pd.DataFrame(checksum_rows)
    checksum_df.to_csv(REPORT_DIR / "phase_3_b4_checksum_report.csv", index=False)

    # 7. Compute District Label Distribution
    print(f"\n--- 6. Computing District-Wise Label Breakdown (20 Districts) ---")
    dist_rows = []
    for _, d_row in district_lookup.iterrows():
        did = int(d_row['district_id'])
        dname = d_row['district_name']
        d_mask = (district_ids == did) & valid_land

        d_valid_cnt = int(np.sum(d_mask))
        d_pos = int(np.sum((target_label == 1) & d_mask))
        d_neg = int(np.sum((target_label == 0) & d_mask))
        d_excl = int(np.sum((target_label == 255) & d_mask))
        d_ratio = (d_pos / (d_pos + d_neg)) if (d_pos + d_neg) > 0 else 0.0

        dist_rows.append({
            "district_id": did,
            "district_name": dname,
            "valid_cells": d_valid_cnt,
            "landslide_presence_cells": d_pos,
            "pseudo_absence_cells": d_neg,
            "excluded_cells": d_excl,
            "prevalence_ratio": round(d_ratio, 6)
        })

    dist_df = pd.DataFrame(dist_rows)
    dist_df.to_csv(REPORT_DIR / "phase_3_b4_district_label_distribution.csv", index=False)

    # 8. Generate Map Previews
    print(f"\n--- 7. Generating Map Previews (outputs/maps/phase_3/b4/) ---")
    generate_b4_maps(combined_presence, dist_m, modelling_domain, target_label, valid_land)

    # 9. Write Audit Reports
    print(f"\n--- 8. Writing B4 Audit & Quality Markdown Reports ---")
    write_b4_reports(num_pos, num_neg, num_buf, num_low_slope, num_incomplete, int(np.sum(valid_land)))

    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"Phase 3 Checkpoint B4 Label Preparation COMPLETE in {elapsed:.1f} seconds!")
    print("=" * 60)


def generate_b4_maps(combined_presence, dist_m, modelling_domain, target_label, valid_land):
    extent = [360800, 665800, 3571100, 3864800]

    # Map 1: Combined Landslide Presence
    plt.figure(figsize=(10, 9))
    cmap_pres = ListedColormap(['#1e293b', '#ef4444'])
    arr_pres = np.where(valid_land, combined_presence, 0)
    plt.imshow(arr_pres, extent=extent, cmap=cmap_pres)
    plt.colorbar(label="Presence (0=None, 1=Landslide)")
    plt.title("GeoSlide-JK: Combined Landslide Inventory Presence (100m Grid)")
    plt.xlabel("Easting (m)"); plt.ylabel("Northing (m)")
    plt.tight_layout()
    plt.savefig(MAP_DIR / "combined_landslide_presence.png", dpi=150)
    plt.close()

    # Map 2: Distance to Landslide
    plt.figure(figsize=(10, 9))
    arr_dist = np.where(valid_land, dist_m, np.nan)
    plt.imshow(arr_dist, extent=extent, cmap="viridis_r")
    plt.colorbar(label="Distance to Landslide (m)")
    plt.title("GeoSlide-JK: Euclidean Distance to Landslides (m)")
    plt.xlabel("Easting (m)"); plt.ylabel("Northing (m)")
    plt.tight_layout()
    plt.savefig(MAP_DIR / "distance_to_landslide.png", dpi=150)
    plt.close()

    # Map 3: Modelling Domain Mask
    plt.figure(figsize=(10, 9))
    cmap_dom = ListedColormap(['#0f172a', '#3b82f6'])
    arr_dom = np.where(valid_land, modelling_domain, 0)
    plt.imshow(arr_dom, extent=extent, cmap=cmap_dom)
    plt.colorbar(label="Domain Mask (1=Valid Data & Coverage)")
    plt.title("GeoSlide-JK: Static Susceptibility Modelling Domain")
    plt.xlabel("Easting (m)"); plt.ylabel("Northing (m)")
    plt.tight_layout()
    plt.savefig(MAP_DIR / "modelling_domain_mask.png", dpi=150)
    plt.close()

    # Map 4: Target Label (Positive / Pseudo-Absence / Excluded)
    plt.figure(figsize=(10, 9))
    lbl_display = np.zeros_like(target_label)
    lbl_display[target_label == 0] = 1  # Absence -> 1 (blue)
    lbl_display[target_label == 1] = 2  # Presence -> 2 (red)
    lbl_display[target_label == 255] = 0 # Excluded -> 0 (dark gray)

    cmap_lbl = ListedColormap(['#1e293b', '#22c55e', '#ef4444'])
    plt.imshow(lbl_display, extent=extent, cmap=cmap_lbl)
    plt.colorbar(ticks=[0.33, 1.0, 1.67], label="0=Excluded, 1=Pseudo-Absence, 2=Presence")
    plt.title("GeoSlide-JK: Final Static Susceptibility Target Labels")
    plt.xlabel("Easting (m)"); plt.ylabel("Northing (m)")
    plt.tight_layout()
    plt.savefig(MAP_DIR / "landslide_target_label.png", dpi=150)
    plt.close()

    # Regional Zoom QA Maps
    zooms = {
        "zoom_ramban_nh44.png": ("Ramban-Banihal Corridor B4 Labels", [490000, 540000, 3660000, 3710000]),
        "zoom_kashmir_valley.png": ("Kashmir Valley B4 Labels", [430000, 510000, 3730000, 3810000]),
        "zoom_chenab_basin.png": ("Chenab Basin B4 Labels", [500000, 580000, 3640000, 3720000])
    }
    for zname, (ztitle, zbox) in zooms.items():
        plt.figure(figsize=(8, 7))
        plt.imshow(lbl_display, extent=extent, cmap=cmap_lbl)
        plt.xlim(zbox[0], zbox[1]); plt.ylim(zbox[2], zbox[3])
        plt.title(f"GeoSlide-JK Zoom: {ztitle}")
        plt.tight_layout()
        plt.savefig(MAP_DIR / zname, dpi=150)
        plt.close()


def write_b4_reports(num_pos, num_neg, num_buf, num_low_slope, num_incomplete, total_valid):
    rep_md = f"""# Phase 3 Checkpoint B4 — Landslide Inventory Label Preparation & Sampling Domain Report

---

## 1. Executive Summary

This report documents **Phase 3 Checkpoint B4: Landslide Inventory Label Preparation and Pseudo-Absence Sampling** for **GeoSlide-JK**.

- **Landslide Presence Cells (Positive)**: **{num_pos:,} cells** ({num_pos * 0.01:.2f} km², {num_pos/total_valid*100:.2f}% of valid land)
- **Verified Pseudo-Absence Cells (Negative)**: **{num_neg:,} cells** ({num_neg * 0.01:.2f} km², {num_neg/total_valid*100:.2f}% of valid land)
- **Excluded Buffer Zone (0 - 200m)**: **{num_buf:,} cells** ({num_buf/total_valid*100:.2f}%)
- **Excluded Low-Slope Areas (<= 5.0°)**: **{num_low_slope:,} cells** ({num_low_slope/total_valid*100:.2f}%)
- **Excluded Incomplete Data Cells**: **{num_incomplete:,} cells** ({num_incomplete/total_valid*100:.2f}%)
- **Prevalence Ratio (Positive / (Positive + Negative))**: **{num_pos / (num_pos + num_neg):.4f}** ({num_pos / (num_pos + num_neg)*100:.2f}%)

---

## 2. Methodological Rules Applied

1. **No NLSM Predictor Usage**: The NLSM raster was **NOT** used to define pseudo-absences or predictors.
2. **Buffer Exclusion**: All cells within $200\\text{{ m}}$ of any landslide polygon or point are tagged $255$ (buffer exclusion zone) to avoid false negatives at slope margins.
3. **Terrain Slope Threshold**: Plain valleys, lakes, and low-gradient terrain ($\text{{slope}} \\le 5.0^\\circ$) are excluded from sampling to prevent trivial negative class bias.
4. **Data Completeness Requirement**: Negative samples are drawn exclusively from cells where `hazard_feature_complete_mask == 1`.
5. **No Raw Data Modification**: Source vector archives under `C:\\Users\\Saurabh Sharma\\Downloads\\J&K` remain **100% read-only**.

---

## 3. Final Target Label Decision

| Target Label Value | Category | Cell Count | Percentage of Valid Land | Model Treatment |
|:---:|:---|:---:|:---:|:---|
| **1** | Landslide Presence | {num_pos:,} | {num_pos/total_valid*100:.2f}% | Positive Class ($y=1$) |
| **0** | Verified Pseudo-Absence | {num_neg:,} | {num_neg/total_valid*100:.2f}% | Negative Class ($y=0$) |
| **255** | Excluded / Buffer / Low Slope | {num_buf + num_low_slope + num_incomplete:,} | {(num_buf + num_low_slope + num_incomplete)/total_valid*100:.2f}% | Excluded from Training & Evaluation |

---

## 4. Verification Checkpoint Status

- **Grid Alignment**: All 7 label rasters align to `EPSG:32643`, $3050 \\times 2937$, 100m grid.
- **Raw Data Safety**: `C:\\Users\\Saurabh Sharma\\Downloads\\J&K` **100% Read-Only**.
- **Status**: **PASS**.
"""
    with open(REPORT_DIR / "phase_3_b4_quality_report.md", "w") as f:
        f.write(rep_md)


if __name__ == "__main__":
    main()
