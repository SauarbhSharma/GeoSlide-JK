import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import rasterio
from rasterio.warp import transform as warp_transform
import geopandas as gpd
from shapely.geometry import Point

app = FastAPI(
    title="GeoSlide-JK API",
    description="Full-J&K Geospatial & Terrain Inspection Intelligence Engine",
    version="0.2.0-phase2-final"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_BOUNDARIES = PROJECT_ROOT / "data" / "processed" / "boundaries"
PROCESSED_TERRAIN = PROJECT_ROOT / "data" / "processed" / "terrain"
PROCESSED_VECTORS = PROJECT_ROOT / "data" / "processed" / "vectors"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

ELEV_COG = PROCESSED_TERRAIN / "jk_elevation_glo30_cog.tif"
SLOPE_COG = PROCESSED_TERRAIN / "jk_slope_degrees_cog.tif"
ASPECT_COG = PROCESSED_TERRAIN / "jk_aspect_degrees_cog.tif"
HILLSHADE_COG = PROCESSED_TERRAIN / "jk_hillshade_cog.tif"

DISTRICTS_GEOJSON = PROCESSED_BOUNDARIES / "jk_districts.geojson"
UT_GEOJSON = PROCESSED_BOUNDARIES / "jk_ut_boundary.geojson"

# Cache loaded boundaries
districts_cache = None

def get_districts_geojson():
    global districts_cache
    if districts_cache is None and DISTRICTS_GEOJSON.exists():
        with open(DISTRICTS_GEOJSON, 'r', encoding='utf-8') as f:
            districts_cache = json.load(f)
    return districts_cache

def sample_cog_value(cog_path: Path, lat: float, lon: float) -> Optional[float]:
    """Sample exact cell value from projected COG at lat/lon with strict NoData filtering."""
    if not cog_path.exists():
        return None
    try:
        with rasterio.open(cog_path) as src:
            xs, ys = warp_transform('EPSG:4326', src.crs, [lon], [lat])
            x, y = xs[0], ys[0]
            row, col = src.index(x, y)
            if 0 <= row < src.height and 0 <= col < src.width:
                val = float(src.read(1, window=((row, row+1), (col, col+1)))[0, 0])
                if (
                    src.nodata is not None and abs(val - float(src.nodata)) < 1e-4
                ) or val == -9999.0 or abs(val - (-9999.0)) < 1e-4:
                    return None
                if val < -1000.0 or val > 10000.0:
                    return None
                return val
    except Exception:
        pass
    return None

@app.get("/")
def read_root():
    return {
        "name": "GeoSlide-JK Phase 2 Static Geospatial Engine",
        "status": "online",
        "phase": "Phase 2 — Static Geospatial Products",
        "version": "v0.2.0",
        "model_status": "Not Trained",
        "truthfulness_notice": "Phase 2 delivers factual Copernicus DEM terrain derivatives and cleaned historical GIS layers. No susceptibility or risk predictions are generated."
    }

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "0.2.0"
    }

@app.get("/api/v1/status")
def system_status():
    return {
        "app_stage": "Phase 2 — Static Geospatial Products",
        "app_version": "v0.2.0",
        "data_freshness": "2026-07-29 (Copernicus DEM & GSI NGDR Data)",
        "dem_rules": "Use exactly four full-J&K DEM tiles. Do not use the pilot DEM.",
        "nlsm_status": "NLSM raster: Excluded",
        "model_pipeline_status": "Not Trained",
        "active_districts": 20,
        "summary_categories": [
            "Core datasets ready",
            "Ready after cleaning",
            "Partial coverage",
            "Optional/unconfirmed",
            "Excluded/problematic"
        ],
        "completed_phase_2_items": [
            "Four full-J&K Copernicus DEM tiles verified & mosaicked",
            "Pilot DEM explicitly excluded",
            "Elevation COG ready (30m, EPSG:32643)",
            "Slope COG ready (degrees)",
            "Aspect COG ready (degrees)",
            "Hillshade COG ready (8-bit)",
            "10 static vector layers processed to GeoPackage & GeoParquet",
            "FastAPI terrain sampling API hardened",
            "MapLibre terrain inspector hardened against null/out-of-bounds/rapid clicks",
            "Frontend CSS Tailwind UI styling repaired and verified",
            "Playwright browser computed-style tests verified"
        ],
        "truthful_limitations": [
            "Machine learning model: Not Trained",
            "Rainfall dataset: Not processed (Demo placeholder)",
            "Geomorphology: Unconfirmed",
            "Population coverage: Requires validation",
            "Dated landslide events: Insufficient",
            "NLSM susceptibility benchmark: Excluded"
        ]
    }

@app.get("/api/v1/districts")
def get_districts():
    geojson = get_districts_geojson()
    if not geojson:
        raise HTTPException(status_code=404, detail="Districts boundary not found")
        
    districts_list = []
    for feat in geojson.get("features", []):
        props = feat.get("properties", {})
        districts_list.append({
            "district_id": props.get("district_id"),
            "display_name": props.get("display_name"),
            "source_name": props.get("source_name"),
            "state_ut": props.get("state_ut", "Jammu and Kashmir")
        })
    return {
        "count": len(districts_list),
        "districts": districts_list
    }

@app.get("/api/v1/districts/boundary")
def get_districts_boundary():
    geojson = get_districts_geojson()
    if not geojson:
        raise HTTPException(status_code=404, detail="Districts boundary file missing")
    return geojson

@app.get("/api/v1/terrain/metadata")
def get_terrain_metadata():
    stats_file = REPORTS_DIR / "phase_2_b1_elevation_stats.json"
    deriv_file = REPORTS_DIR / "phase_2_b2_derivatives_stats.json"
    
    b1_stats = {}
    b2_stats = {}
    if stats_file.exists():
        with open(stats_file, 'r', encoding='utf-8') as f:
            b1_stats = json.load(f)
    if deriv_file.exists():
        with open(deriv_file, 'r', encoding='utf-8') as f:
            b2_stats = json.load(f)
            
    return {
        "crs_web": "EPSG:4326 / Web Mercator",
        "crs_processing": "EPSG:32643",
        "crs_delivery": "EPSG:4326",
        "resolution_meters": 30.0,
        "elevation_stats": b1_stats,
        "derivatives_stats": b2_stats,
        "source": "Copernicus GLO-30 DEM 30m Mosaic"
    }

@app.get("/api/v1/terrain/value")
def get_terrain_value(
    lat: float = Query(..., description="Latitude in WGS84"),
    lon: float = Query(..., description="Longitude in WGS84")
):
    inside_bbox = (32.0 <= lat <= 36.0) and (73.0 <= lon <= 78.0)
    
    if not inside_bbox:
        return {
            "success": False,
            "code": "OUTSIDE_STUDY_AREA",
            "message": "The selected point is outside the current J&K study area.",
            "location": {"lat": round(lat, 5), "lon": round(lon, 5)},
            "inside_study_area": False,
            "data_available": False,
            "district": "Outside J&K UT Boundary",
            "terrain": {
                "elevation_m": None,
                "slope_deg": None,
                "aspect_deg": None,
                "hillshade": None
            },
            "source": {
                "dem": "Copernicus GLO-30 30m DEM",
                "resolution_m": 30.0,
                "processing_crs": "EPSG:32643",
                "web_crs": "EPSG:4326"
            }
        }
        
    district_name = "Outside J&K UT Boundary"
    inside_ut = False
    if DISTRICTS_GEOJSON.exists():
        gdf_dist = gpd.read_file(DISTRICTS_GEOJSON)
        pt = Point(lon, lat)
        matched = gdf_dist[gdf_dist.contains(pt)]
        if len(matched) > 0:
            district_name = matched.iloc[0]['display_name']
            inside_ut = True

    if not inside_ut:
        return {
            "success": False,
            "code": "OUTSIDE_STUDY_AREA",
            "message": "The selected point is outside the 20-district J&K UT boundary.",
            "location": {"lat": round(lat, 5), "lon": round(lon, 5)},
            "inside_study_area": False,
            "data_available": False,
            "district": district_name,
            "terrain": {
                "elevation_m": None,
                "slope_deg": None,
                "aspect_deg": None,
                "hillshade": None
            },
            "source": {
                "dem": "Copernicus GLO-30 30m DEM",
                "resolution_m": 30.0,
                "processing_crs": "EPSG:32643",
                "web_crs": "EPSG:4326"
            }
        }

    elev = sample_cog_value(ELEV_COG, lat, lon)
    slope = sample_cog_value(SLOPE_COG, lat, lon)
    aspect = sample_cog_value(ASPECT_COG, lat, lon)
    hillshade = sample_cog_value(HILLSHADE_COG, lat, lon)
    
    data_avail = elev is not None and slope is not None

    if not data_avail:
        return {
            "success": False,
            "code": "NO_TERRAIN_DATA",
            "message": "No valid terrain data are available at this location.",
            "location": {"lat": round(lat, 5), "lon": round(lon, 5)},
            "inside_study_area": True,
            "data_available": False,
            "district": district_name,
            "terrain": {
                "elevation_m": None,
                "slope_deg": None,
                "aspect_deg": None,
                "hillshade": None
            },
            "source": {
                "dem": "Copernicus GLO-30 30m DEM",
                "resolution_m": 30.0,
                "processing_crs": "EPSG:32643",
                "web_crs": "EPSG:4326"
            }
        }

    return {
        "success": True,
        "code": "OK",
        "message": "Terrain cell values sampled successfully.",
        "location": {"lat": round(lat, 5), "lon": round(lon, 5)},
        "inside_study_area": True,
        "data_available": True,
        "district": district_name,
        "terrain": {
            "elevation_m": round(elev, 2) if elev is not None else None,
            "slope_deg": round(slope, 2) if slope is not None else None,
            "aspect_deg": round(aspect, 2) if aspect is not None else None,
            "hillshade": int(hillshade) if hillshade is not None else None
        },
        "source": {
            "dem": "Copernicus GLO-30 30m DEM",
            "resolution_m": 30.0,
            "processing_crs": "EPSG:32643",
            "web_crs": "EPSG:4326"
        }
    }

@app.get("/api/v1/static-layers")
def list_static_layers():
    return {
        "raster_layers": [
            {"id": "elevation", "name": "Elevation (meters ASL)", "file": "jk_elevation_glo30_cog.tif", "type": "COG", "availability": "Available"},
            {"id": "slope", "name": "Slope (degrees)", "file": "jk_slope_degrees_cog.tif", "type": "COG", "availability": "Available"},
            {"id": "aspect", "name": "Aspect (orientation)", "file": "jk_aspect_degrees_cog.tif", "type": "COG", "availability": "Available"},
            {"id": "hillshade", "name": "Hillshade (shaded relief)", "file": "jk_hillshade_cog.tif", "type": "COG", "availability": "Available"}
        ],
        "vector_layers": [
            {"id": "districts", "name": "20-District Boundaries", "count": 20, "availability": "Available"},
            {"id": "landslides_points", "name": "Historical Landslide Locations", "count": 2370, "availability": "Available"},
            {"id": "landslides_polygons", "name": "Historical Landslide Polygons", "count": 7436, "availability": "Available"},
            {"id": "faults", "name": "Tectonic Fault Lines", "count": 3, "availability": "Available"},
            {"id": "thrusts", "name": "Tectonic Thrust Lines", "count": 14, "availability": "Available"},
            {"id": "lineaments", "name": "Geomorphological Lineaments", "count": 774, "availability": "Available"},
            {"id": "lithology", "name": "Geological Lithology Units", "count": 4076, "availability": "Processed but UI connection pending"},
            {"id": "nh44", "name": "NH-44 Highway Corridor", "count": 7, "availability": "Available"},
            {"id": "major_roads", "name": "Statewide Major Roads", "count": 4762, "availability": "Available"},
            {"id": "settlements", "name": "Cities, Towns & Villages", "count": 5060, "availability": "Available"},
            {"id": "health_facilities", "name": "Hospitals & Clinics", "count": 877, "availability": "Available"}
        ]
    }

@app.get("/api/v1/static-layers/{layer_name}")
def get_static_vector_layer(layer_name: str):
    parquet_path = PROCESSED_VECTORS / f"jk_{layer_name}.parquet"
    if not parquet_path.exists():
        if layer_name == "districts":
            return get_districts_boundary()
        raise HTTPException(status_code=404, detail=f"Vector layer '{layer_name}' not found")
        
    gdf = gpd.read_parquet(parquet_path)
    return json.loads(gdf.to_json())

@app.get("/api/v1/features/nearby")
def get_nearby_features(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    radius: float = Query(5.0, description="Radius in kilometers", ge=0.1, le=50.0)
):
    pt = Point(lon, lat)
    deg_radius = radius / 111.0
    buffer_geom = pt.buffer(deg_radius)
    
    nearby_summary = {}
    vector_files = {
        "landslide_points": "jk_landslides_points.parquet",
        "health_facilities": "jk_health_facilities.parquet",
        "settlements": "jk_settlements.parquet",
        "nh44": "jk_nh44.parquet"
    }

    for key, f in vector_files.items():
        p = PROCESSED_VECTORS / f
        if p.exists():
            gdf = gpd.read_parquet(p)
            intersected = gdf[gdf.intersects(buffer_geom)]
            nearby_summary[key] = len(intersected)

    return {
        "success": True,
        "query": {"latitude": round(lat, 5), "longitude": round(lon, 5), "radius_km": radius},
        "nearby_counts": nearby_summary
    }

@app.get("/api/v1/map/config")
def get_map_config():
    return {
        "center": [75.0, 33.7],
        "zoom": 7.2,
        "min_zoom": 6.5,
        "max_zoom": 15.0,
        "crs_web": "EPSG:4326 / Web Mercator",
        "crs_processing": "EPSG:32643",
        "bounds": [73.2, 32.2, 77.8, 35.2],
        "basemaps": ["carto-dark", "carto-light", "satellite"],
        "default_active_layers": ["districts", "hillshade", "landslides_points", "nh44"]
    }
