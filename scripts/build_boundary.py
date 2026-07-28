#!/usr/bin/env python3
"""
GeoSlide-JK District Boundary Builder & Whitelist Processor
Reads raw shapefile, applies strict 20-district whitelist, normalizes display names,
repairs invalid geometries, dissolves full J&K UT boundary, and writes outputs to data/processed/boundaries/
"""

import sys
import os
import json
from pathlib import Path
import shapefile
from shapely.geometry import shape, mapping, MultiPolygon, Polygon
from shapely.ops import unary_union

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from geoslide.audit.discovery import PathConfig

# Explicit 20-district whitelist for Jammu & Kashmir Union Territory
JK_DISTRICT_WHITELIST = {
    "ANANTNAG", "BADGAM", "BANDIPURA", "BARAMULA", "DODA", "GANDERBAL",
    "JAMMU", "KATHUA", "KISHTWAR", "KULGAM", "KUPWARA", "PULWAMA",
    "PUNCH", "RAJAURI", "RAMBAN", "RIASI", "SAMBA", "SHUPIYAN",
    "SRINAGAR", "UDHAMPUR"
}

# User-facing display name normalization
DISPLAY_NAME_MAP = {
    "ANANTNAG": "Anantnag",
    "BADGAM": "Budgam",
    "BANDIPURA": "Bandipora",
    "BARAMULA": "Baramulla",
    "DODA": "Doda",
    "GANDERBAL": "Ganderbal",
    "JAMMU": "Jammu",
    "KATHUA": "Kathua",
    "KISHTWAR": "Kishtwar",
    "KULGAM": "Kulgam",
    "KUPWARA": "Kupwara",
    "PULWAMA": "Pulwama",
    "PUNCH": "Poonch",
    "RAJAURI": "Rajouri",
    "RAMBAN": "Ramban",
    "RIASI": "Reasi",
    "SAMBA": "Samba",
    "SHUPIYAN": "Shopian",
    "SRINAGAR": "Srinagar",
    "UDHAMPUR": "Udhampur"
}

def slugify(text: str) -> str:
    return text.lower().replace(" ", "_").replace("-", "_")

def build_boundaries():
    path_cfg = PathConfig()
    
    # Path to source district shapefile inside read-only raw directory
    shp_path = path_cfg.raw_root / "Administrative Boundary Database For State Upto Distt level with HQ OVSF_1M_9" / "01" / "JAMMU_&_KASHMIR_DISTRICT_BDY.shp"
    
    if not shp_path.exists():
        raise FileNotFoundError(f"District shapefile not found at {shp_path}")

    print(f"Reading raw district shapefile from: {shp_path}")
    
    sf = shapefile.Reader(str(shp_path))
    records = sf.records()
    shapes = sf.shapes()
    
    features = []
    district_geoms = []
    
    ignored_districts = []

    for rec, shp_obj in zip(records, shapes):
        # Record dict
        rec_dict = rec.as_dict()
        source_name = str(rec_dict.get("DISTRICT", "")).strip()

        # Strict Whitelist Check
        if source_name not in JK_DISTRICT_WHITELIST:
            ignored_districts.append(source_name)
            print(f"  [EXCLUDED] District: {source_name} (Not in 20-district whitelist)")
            continue

        # Convert geometry to Shapely shape
        geom = shape(shp_obj.__geo_interface__)
        if not geom.is_valid:
            print(f"  [REPAIR] Fixing invalid geometry for {source_name}")
            geom = geom.buffer(0)

        display_name = DISPLAY_NAME_MAP.get(source_name, source_name.title())
        district_id = slugify(display_name)

        properties = {
            "source_name": source_name,
            "display_name": display_name,
            "district_id": district_id,
            "included_in_jk_ut": True,
            "state_ut": "Jammu & Kashmir",
            "lgd_code": rec_dict.get("DIST_LGD", "")
        }

        feature = {
            "type": "Feature",
            "properties": properties,
            "geometry": mapping(geom)
        }

        features.append(feature)
        district_geoms.append(geom)
        print(f"  [INCLUDED] {source_name} -> Display: '{display_name}' (ID: {district_id})")

    # Verify exact count
    print(f"\nTotal included districts: {len(features)}")
    if len(features) != 20:
        raise ValueError(f"CRITICAL ERROR: Expected exactly 20 districts, got {len(features)}!")

    # Dissolve to create full J&K UT Boundary
    print("Dissolving district geometries into unified J&K UT boundary...")
    dissolved_geom = unary_union(district_geoms)
    if not dissolved_geom.is_valid:
        dissolved_geom = dissolved_geom.buffer(0)

    ut_feature = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {
                "name": "Jammu & Kashmir",
                "type": "Union Territory",
                "district_count": 20
            },
            "geometry": mapping(dissolved_geom)
        }]
    }

    district_fc = {
        "type": "FeatureCollection",
        "features": features
    }

    # Output paths inside D:\Projects\GeoSlide_JK\data\processed\boundaries
    out_dir = path_cfg.project_root / "data" / "processed" / "boundaries"
    out_dir.mkdir(parents=True, exist_ok=True)

    districts_geojson_path = out_dir / "jk_districts.geojson"
    ut_geojson_path = out_dir / "jk_ut_boundary.geojson"

    with open(districts_geojson_path, "w", encoding="utf-8") as f:
        json.dump(district_fc, f, indent=2)
    print(f"Saved processed district boundary layer: {districts_geojson_path}")

    with open(ut_geojson_path, "w", encoding="utf-8") as f:
        json.dump(ut_feature, f, indent=2)
    print(f"Saved processed dissolved J&K UT boundary: {ut_geojson_path}")

    return districts_geojson_path, ut_geojson_path

if __name__ == "__main__":
    build_boundaries()
