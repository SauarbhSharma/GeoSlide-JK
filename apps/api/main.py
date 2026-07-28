from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
import os
import sys

# Add project root and src to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

app = FastAPI(
    title="GeoSlide-JK Decision Support API",
    description="Explainable Landslide Susceptibility and Rainfall-Triggered Risk Research Prototype API",
    version="0.1.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
def get_health():
    return {
        "status": "ok",
        "service": "GeoSlide-JK API",
        "version": "0.1.0",
        "environment": "development"
    }

@app.get("/api/v1/status")
def get_system_status():
    return {
        "pipeline_phase": "Phase 1 - Shell & Status Demo",
        "active_districts": 20,
        "data_freshness": {
            "boundaries": "Verified (20 J&K Districts)",
            "rainfall_mode": "Demo Playback",
            "sample_rainfall_period": "July 2026 Sample Granules",
            "model_version": "v0.1.0-prototype"
        },
        "disclaimer": "GeoSlide-JK is an explainable landslide susceptibility research prototype. It is not an official warning system."
    }

@app.get("/api/v1/districts")
def get_districts():
    geojson_path = PROJECT_ROOT / "data" / "processed" / "boundaries" / "jk_districts.geojson"
    if not geojson_path.exists():
        raise HTTPException(status_code=404, detail="Processed district boundaries not found.")

    with open(geojson_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    districts = []
    for feat in data.get("features", []):
        props = feat.get("properties", {})
        # Filter strictly
        if props.get("source_name") in ["MIRPUR", "MUZAFFARABAD"]:
            continue
        districts.append({
            "district_id": props.get("district_id"),
            "display_name": props.get("display_name"),
            "source_name": props.get("source_name"),
            "included_in_jk_ut": props.get("included_in_jk_ut", True),
            "state_ut": props.get("state_ut", "Jammu & Kashmir"),
            "lgd_code": props.get("lgd_code")
        })

    return {
        "count": len(districts),
        "districts": districts
    }

@app.get("/api/v1/layers")
def get_layers():
    return {
        "layers": [
            {
                "id": "jk_ut_boundary",
                "name": "J&K UT Boundary",
                "category": "Boundaries",
                "type": "vector",
                "status": "Verified (20 Districts)",
                "default_visible": True
            },
            {
                "id": "jk_districts",
                "name": "District Boundaries (20)",
                "category": "Boundaries",
                "type": "vector",
                "status": "Verified",
                "default_visible": True
            },
            {
                "id": "dem_elevation",
                "name": "Copernicus GLO-30 DEM Elevation",
                "category": "Terrain",
                "type": "raster",
                "status": "Raw Tiles Audited (5 Tiles)",
                "default_visible": False
            },
            {
                "id": "slope",
                "name": "Terrain Slope",
                "category": "Terrain",
                "type": "raster",
                "status": "Phase 2 Pipeline Target",
                "default_visible": False
            },
            {
                "id": "lithology",
                "name": "Geological Lithology (1:50k)",
                "category": "Geology",
                "type": "vector",
                "status": "Audited Single Match",
                "default_visible": False
            },
            {
                "id": "landslides",
                "name": "NGDR Landslide Inventory",
                "category": "Landslides",
                "type": "vector",
                "status": "Audited Single Match",
                "default_visible": True
            },
            {
                "id": "rainfall_imerg",
                "name": "IMERG Satellite Rainfall (Demo Playback)",
                "category": "Rainfall",
                "type": "raster",
                "status": "Demo Playback (July 2026 Sample)",
                "default_visible": True
            }
        ]
    }

@app.get("/api/v1/data/coverage")
def get_data_coverage():
    manifest_path = PROJECT_ROOT / "outputs" / "reports" / "data_discovery_manifest.json"
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        return manifest
    return {
        "status": "audit_pending",
        "total_categories_scanned": 18,
        "summary": {"verified": 7, "multiple_matches": 11, "missing": 0}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
