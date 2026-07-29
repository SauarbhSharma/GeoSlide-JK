#!/usr/bin/env python3
"""
Reprocesses raw district shapefile into geographically accurate WGS84 GeoJSON boundaries:
  - data/processed/boundaries/jk_districts.geojson (20 Whitelisted Districts)
  - data/processed/boundaries/jk_ut_boundary.geojson (Dissolved Statewide UT Envelope)
"""

import json
from pathlib import Path
import geopandas as gpd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_SHP = Path(r"C:\Users\Saurabh Sharma\Downloads\J&K\Administrative Boundary Database For State Upto Distt level with HQ OVSF_1M_9\01\JAMMU_&_KASHMIR_DISTRICT_BDY.shp")
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "boundaries"

WHITELIST_20 = [
    'ANANTNAG', 'BADGAM', 'BANDIPURA', 'BARAMULA', 'DODA', 'GANDERBAL',
    'JAMMU', 'KATHUA', 'KISHTWAR', 'KULGAM', 'KUPWARA', 'PULWAMA', 'PUNCH',
    'RAJAURI', 'RAMBAN', 'RIASI', 'SAMBA', 'SHUPIYAN', 'SRINAGAR', 'UDHAMPUR'
]

DISPLAY_NAME_MAP = {
    "BADGAM": "Budgam",
    "BANDIPURA": "Bandipora",
    "BARAMULA": "Baramulla",
    "PUNCH": "Poonch",
    "RAJAURI": "Rajouri",
    "RIASI": "Reasi",
    "SHUPIYAN": "Shopian"
}

def reprocess_boundaries():
    print("=== Reprocessing J&K Vector Boundaries ===")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    gdf_raw = gpd.read_file(RAW_SHP)
    print(f"Raw shapefile loaded: {len(gdf_raw)} polygons, Source CRS: {gdf_raw.crs}")
    
    # Filter 20 whitelisted districts
    gdf_20 = gdf_raw[gdf_raw['DISTRICT'].str.upper().isin(WHITELIST_20)].copy()
    if len(gdf_20) != 20:
        raise ValueError(f"Expected 20 whitelisted districts, got {len(gdf_20)}")
        
    # Check Mirpur / Muzaffarabad absence
    names_upper = gdf_20['DISTRICT'].str.upper().tolist()
    assert "MIRPUR" not in names_upper and "MUZAFFARABAD" not in names_upper
    
    # Reproject to EPSG:4326 (WGS84)
    gdf_wgs84 = gdf_20.to_crs("EPSG:4326")
    
    # Add normalized district attributes
    features = []
    for idx, row in gdf_wgs84.iterrows():
        source_name = row['DISTRICT'].strip()
        disp_name = DISPLAY_NAME_MAP.get(source_name.upper(), source_name.title())
        dist_id = disp_name.lower().replace(" ", "_")
        
        # Build feature dict
        feat = {
            "type": "Feature",
            "properties": {
                "district_id": dist_id,
                "display_name": disp_name,
                "source_name": source_name,
                "state_ut": "Jammu and Kashmir",
                "objectid": row.get('OBJECTID_1', idx + 1),
                "dist_lgd": row.get('DIST_LGD', None)
            },
            "geometry": json.loads(gpd.GeoSeries([row.geometry]).to_json())['features'][0]['geometry']
        }
        features.append(feat)
        
    dist_geojson = {
        "type": "FeatureCollection",
        "name": "jk_districts_20",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": features
    }
    
    dist_out_path = PROCESSED_DIR / "jk_districts.geojson"
    with open(dist_out_path, 'w', encoding='utf-8') as f:
        json.dump(dist_geojson, f)
    print(f"Saved {dist_out_path} (20 Whitelisted Districts, WGS84)")
    
    # Dissolve to Outer UT Boundary
    gdf_dissolved = gdf_wgs84.dissolve()
    ut_feature = {
        "type": "FeatureCollection",
        "name": "jk_ut_boundary",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": [{
            "type": "Feature",
            "properties": {
                "state_ut": "Jammu and Kashmir",
                "district_count": 20
            },
            "geometry": json.loads(gdf_dissolved.to_json())['features'][0]['geometry']
        }]
    }
    
    ut_out_path = PROCESSED_DIR / "jk_ut_boundary.geojson"
    with open(ut_out_path, 'w', encoding='utf-8') as f:
        json.dump(ut_feature, f)
    print(f"Saved {ut_out_path} (Dissolved UT Boundary, WGS84)")

if __name__ == "__main__":
    reprocess_boundaries()
