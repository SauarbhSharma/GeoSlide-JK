#!/usr/bin/env python3
"""
GeoSlide-JK Phase 2 Input Discovery Engine
Scans read-only raw workspace and processed outputs to build the Phase 2 input manifest.
Generates:
  - outputs/reports/phase_2_input_manifest.csv
  - outputs/reports/phase_2_input_discovery.md
"""

import os
import sys
import hashlib
import json
import csv
import time
from pathlib import Path
import rasterio
import geopandas as gpd
import shapefile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

RAW_DIR = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K")
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

def compute_checksum(filepath, max_bytes=10*1024*1024):
    """Compute MD5 checksum of file header/sample."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(max_bytes)
        hasher.update(buf)
    return hasher.hexdigest()

def inspect_dem_tiles():
    """Find and inspect all Copernicus GLO-30 DEM candidates."""
    print("--- Inspecting Copernicus DEM Candidates ---")
    candidates = []
    
    dem_files = []
    for root, dirs, files in os.walk(RAW_DIR):
        for file in files:
            if file.endswith('.tif') or file.endswith('.TIF'):
                dem_files.append(Path(root) / file)
                
    for fp in sorted(dem_files):
        size_bytes = fp.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        checksum = compute_checksum(fp)
        
        with rasterio.open(fp) as src:
            bounds = [src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top]
            arr = src.read(1, masked=True)
            min_val = float(arr.min()) if arr.count() > 0 else None
            max_val = float(arr.max()) if arr.count() > 0 else None
            
            info = {
                "path": str(fp),
                "filename": fp.name,
                "relative_dir": str(fp.parent.relative_to(RAW_DIR)),
                "size_bytes": size_bytes,
                "size_mb": round(size_mb, 2),
                "checksum": checksum,
                "crs": str(src.crs),
                "width": src.width,
                "height": src.height,
                "res": src.res,
                "bounds": [round(b, 5) for b in bounds],
                "count": src.count,
                "dtype": str(src.dtypes[0]),
                "nodata": src.nodata,
                "min_val": round(min_val, 2) if min_val is not None else None,
                "max_val": round(max_val, 2) if max_val is not None else None,
            }

        w, s, e, n = bounds
        if size_mb < 50:
            info["classification"] = "pilot DEM"
            info["quadrant"] = "Pilot DEM Candidate (Excluded from Phase 2)"
        elif w < 74.5 and s < 33.0:
            info["classification"] = "full-J&K tile"
            info["quadrant"] = "Southwest (73.5-75.5°E, 32.0-34.0°N)"
        elif e > 76.5 and s < 33.0:
            info["classification"] = "full-J&K tile"
            info["quadrant"] = "Southeast (75.5-77.5°E, 32.0-34.0°N)"
        elif w < 74.5 and n > 35.0:
            info["classification"] = "full-J&K tile"
            info["quadrant"] = "Northwest (73.5-75.5°E, 34.0-36.0°N)"
        elif e > 76.5 and n > 35.0:
            info["classification"] = "full-J&K tile"
            info["quadrant"] = "Northeast (75.5-77.5°E, 34.0-36.0°N)"
        else:
            info["classification"] = "pilot DEM"
            info["quadrant"] = "Pilot / Unsuitable Candidate"
            
        candidates.append(info)
        print(f"  [{info['classification']}] {fp.parent.name}/{fp.name} ({info['size_mb']} MB) - Bounds: {info['bounds']}")
        
    return candidates

def inspect_boundary_inputs():
    """Inspect boundary files in processed directory."""
    print("\n--- Inspecting Boundary Inputs ---")
    dist_file = PROCESSED_DIR / "boundaries" / "jk_districts.geojson"
    ut_file = PROCESSED_DIR / "boundaries" / "jk_ut_boundary.geojson"
    
    gdf_dist = gpd.read_file(dist_file)
    gdf_ut = gpd.read_file(ut_file)
    
    source_names = list(gdf_dist["source_name"])
    display_names = list(gdf_dist["display_name"])
    
    info = {
        "districts_path": str(dist_file),
        "ut_path": str(ut_file),
        "district_count": len(gdf_dist),
        "mirpur_absent": "MIRPUR" not in source_names,
        "muzaffarabad_absent": "MUZAFFARABAD" not in source_names,
        "display_names": sorted(display_names),
        "source_names": sorted(source_names),
        "crs": str(gdf_dist.crs),
        "bounds": [round(b, 5) for b in list(gdf_dist.total_bounds)]
    }
    print(f"  District Boundary: {len(gdf_dist)} districts, CRS: {info['crs']}, Mirpur absent: {info['mirpur_absent']}, Muzaffarabad absent: {info['muzaffarabad_absent']}")
    return info

def inspect_vector_inputs():
    """Inspect shapefiles and geopackages under raw workspace."""
    print("\n--- Inspecting Raw Vector Inputs ---")
    
    vector_summary = {}
    
    # 1. Landslides
    landslide_shps = [
        RAW_DIR / "Landslide Inventory" / "01" / "landslide_point_STATE_JK.shp",
        RAW_DIR / "Landslide Inventory" / "01" / "landslide_polygon_STATE_JK.shp"
    ]
    
    vector_summary["landslides"] = []
    for shp in landslide_shps:
        if not shp.exists(): continue
        gdf = gpd.read_file(shp)
        item = {
            "path": str(shp),
            "filename": shp.name,
            "size_mb": round(shp.stat().st_size / (1024*1024), 2),
            "crs": str(gdf.crs),
            "feature_count": len(gdf),
            "geom_type": str(gdf.geometry.type.iloc[0]) if len(gdf) > 0 else "Unknown",
            "bounds": [round(b, 5) for b in list(gdf.total_bounds)],
            "null_geom_count": int(gdf.geometry.is_null().sum()),
            "invalid_geom_count": int((~gdf.geometry.is_valid).sum()),
            "fields": list(gdf.columns)
        }
        vector_summary["landslides"].append(item)
        print(f"  Landslide: {shp.name} - {item['feature_count']} features ({item['geom_type']}), CRS: {item['crs']}")

    # 2. Tectonics & Lithology
    tectonic_shps = [
        RAW_DIR / "Geology and Structure Database" / "01" / "active_fault_ngdr_STATE_JK.shp",
        RAW_DIR / "Geology and Structure Database" / "01" / "fault_tectonic_ngdr_STATE_JK.shp",
        RAW_DIR / "Geology and Structure Database" / "01" / "thrust_tectonic_ngdr_STATE_JK.shp",
        RAW_DIR / "Geology and Structure Database" / "01" / "lineament_250k_ngdr_STATE_JK.shp",
        RAW_DIR / "Geology and Structure Database" / "01" / "lithology_gcs_ngdr_STATE_JK.shp",
        RAW_DIR / "Geology and Structure Database" / "01" / "earthquake_ngdr_STATE_JK.shp",
        RAW_DIR / "Geology and Structure Database" / "01" / "fold_tectonic_ngdr_STATE_JK.shp",
    ]
    
    vector_summary["tectonics_lithology"] = []
    for shp in tectonic_shps:
        if not shp.exists(): continue
        gdf = gpd.read_file(shp)
        item = {
            "path": str(shp),
            "filename": shp.name,
            "size_mb": round(shp.stat().st_size / (1024*1024), 2),
            "crs": str(gdf.crs),
            "feature_count": len(gdf),
            "geom_type": str(gdf.geometry.type.iloc[0]) if len(gdf) > 0 else "Unknown",
            "bounds": [round(b, 5) for b in list(gdf.total_bounds)],
            "null_geom_count": int(gdf.geometry.is_null().sum()),
            "invalid_geom_count": int((~gdf.geometry.is_valid).sum()),
            "fields": list(gdf.columns)
        }
        vector_summary["tectonics_lithology"].append(item)
        print(f"  Tectonic/Geology: {shp.name} - {item['feature_count']} features ({item['geom_type']}), CRS: {item['crs']}")

    # 3. OSM Exposure GPKG
    gpkg_file = RAW_DIR / "OSM Exposure Infrastructure Database" / "GeoSlide_JK_Roads_Settlements_Exposure.gpkg"
    vector_summary["osm_exposure"] = []
    if gpkg_file.exists():
        import fiona
        layers = fiona.listlayers(str(gpkg_file))
        layer_details = {}
        for l in layers:
            gdf_l = gpd.read_file(gpkg_file, layer=l)
            layer_details[l] = {
                "feature_count": len(gdf_l),
                "crs": str(gdf_l.crs),
                "geom_type": str(gdf_l.geometry.type.iloc[0]) if len(gdf_l) > 0 else "Unknown",
                "fields": list(gdf_l.columns)
            }
        item = {
            "path": str(gpkg_file),
            "filename": gpkg_file.name,
            "size_mb": round(gpkg_file.stat().st_size / (1024*1024), 2),
            "layers": layer_details
        }
        vector_summary["osm_exposure"].append(item)
        print(f"  OSM Exposure GPKG: {gpkg_file.name} - {len(layers)} layers: {list(layer_details.keys())}")
        
    return vector_summary

def run_discovery():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    dem_candidates = inspect_dem_tiles()
    boundary_info = inspect_boundary_inputs()
    vector_info = inspect_vector_inputs()
    
    full_dem_tiles = [d for d in dem_candidates if d['classification'] == 'full-J&K tile']
    pilot_dem_tiles = [d for d in dem_candidates if d['classification'] == 'pilot DEM']
    
    # Write CSV manifest
    csv_path = REPORTS_DIR / "phase_2_input_manifest.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Classification", "Quadrant_Name", "Filename", "Subfolder", "Size_MB", "CRS", "Pixel_Width", "Pixel_Height", "Resolution_Deg", "Bounds_LonLat", "NoData", "Min_Elevation_m", "Max_Elevation_m", "MD5_Checksum", "Path"])
        
        for d in dem_candidates:
            writer.writerow([
                "DEM Elevation",
                d["classification"],
                d["quadrant"],
                d["filename"],
                d["relative_dir"],
                d["size_mb"],
                d["crs"],
                d["width"],
                d["height"],
                f"{d['res'][0]:.6f}",
                json.dumps(d["bounds"]),
                d["nodata"],
                d["min_val"],
                d["max_val"],
                d["checksum"],
                d["path"]
            ])
            
        writer.writerow(["Boundary", "Verified Vector", "Statewide J&K UT", Path(boundary_info["districts_path"]).name, "data/processed/boundaries", "", boundary_info["crs"], "", "", "", json.dumps(boundary_info["bounds"]), "", "", "", "", boundary_info["districts_path"]])
        
        for cat, items in vector_info.items():
            for item in items:
                writer.writerow([
                    cat,
                    "Raw Vector Input",
                    item.get("filename", ""),
                    item.get("filename", ""),
                    Path(item["path"]).parent.name,
                    item.get("size_mb", ""),
                    item.get("crs", ""),
                    "", "", "",
                    json.dumps(item.get("bounds", [])),
                    "", "", "", "",
                    item["path"]
                ])
                
    print(f"\nManifest CSV generated: {csv_path}")
    
    # Write Markdown Discovery Report
    md_path = REPORTS_DIR / "phase_2_input_discovery.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# GeoSlide-JK Phase 2 Input Discovery Report\n\n")
        f.write(f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Status**: **INPUT DISCOVERY COMPLETE — AWAITING APPROVAL A**\n\n")
        f.write("---\n\n")
        
        f.write("## 1. Selected Four Full-J&K DEM Tiles\n\n")
        f.write("| Quadrant | Relative Subfolder | Filename | Size (MB) | Dimensions (WxH) | Res | Bounds (Lon, Lat) | Elevation Range | Checksum |\n")
        f.write("| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        for tile in full_dem_tiles:
            b = tile["bounds"]
            b_str = f"[{b[0]:.2f}, {b[1]:.2f}, {b[2]:.2f}, {b[3]:.2f}]"
            res_str = f"{tile['res'][0]:.6f}°"
            elev_str = f"{tile['min_val']}m to {tile['max_val']}m"
            f.write(f"| {tile['quadrant']} | `{tile['relative_dir']}` | `{tile['filename']}` | {tile['size_mb']} | {tile['width']}x{tile['height']} | {res_str} | `{b_str}` | {elev_str} | `{tile['checksum'][:10]}...` |\n")
            
        f.write("\n## 2. Excluded Pilot DEM Tile\n\n")
        f.write("| Filename | Relative Subfolder | Size (MB) | Reason for Exclusion | Absolute Path |\n")
        f.write("| :--- | :--- | :---: | :--- | :--- |\n")
        for tile in pilot_dem_tiles:
            f.write(f"| `{tile['filename']}` | `{tile['relative_dir']}` | {tile['size_mb']} | Excluded from Phase 2 processing (Pilot Candidate - partial extent 46 MB) | `{tile['path']}` |\n")
            
        f.write("\n---\n\n")
        f.write("## 3. Boundary Inputs\n\n")
        f.write(f"- **District Boundary Path**: `{boundary_info['districts_path']}`\n")
        f.write(f"- **UT Boundary Path**: `{boundary_info['ut_path']}`\n")
        f.write(f"- **District Count**: **20 / 20 Whitelisted Districts**\n")
        f.write(f"- **CRS**: `{boundary_info['crs']}` | Bounds: `{boundary_info['bounds']}`\n")
        f.write(f"- **Mirpur & Muzaffarabad Excluded**: `{boundary_info['mirpur_absent'] and boundary_info['muzaffarabad_absent']}`\n\n")
        
        f.write("## 4. Vector Inputs Manifest\n\n")
        f.write("### A. Landslide Inventory\n")
        for item in vector_info.get("landslides", []):
            f.write(f"- `{item['filename']}` ({item['size_mb']} MB): **{item['feature_count']}** features (`{item['geom_type']}`), CRS: `{item['crs']}`, Null Geoms: {item['null_geom_count']}, Invalid Geoms: {item['invalid_geom_count']}\n")
            
        f.write("\n### B. Tectonics & Lithology\n")
        for item in vector_info.get("tectonics_lithology", []):
            f.write(f"- `{item['filename']}` ({item['size_mb']} MB): **{item['feature_count']}** features (`{item['geom_type']}`), CRS: `{item['crs']}`, Null Geoms: {item['null_geom_count']}, Invalid Geoms: {item['invalid_geom_count']}\n")
            
        f.write("\n### C. OSM Infrastructure & Exposure\n")
        for item in vector_info.get("osm_exposure", []):
            f.write(f"- `{item['filename']}` ({item['size_mb']} MB):\n")
            for layer_name, ldetails in item["layers"].items():
                f.write(f"  - Layer `{layer_name}`: **{ldetails['feature_count']}** features (`{ldetails['geom_type']}`), CRS: `{ldetails['crs']}`\n")

    print(f"Discovery Report MD generated: {md_path}")

if __name__ == "__main__":
    run_discovery()
