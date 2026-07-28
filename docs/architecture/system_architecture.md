# GeoSlide-JK System Architecture & Design Document

---

## 1. Executive Architecture Summary

GeoSlide-JK is structured as a decoupled, multi-tier geospatial system. High-performance raster/vector processing and ML inference are performed in Python backends, served via Fast-API tile and REST endpoints, and visualized through a modern React/Next.js map-first frontend.

```mermaid
graph TD
    subgraph Storage & Ingestion Layer
        RAW["Read-Only Raw Data Workspace<br/>(C:\...\Downloads\J&K)"]
        INTERIM["Interim Staging / Extracted Data<br/>(data/interim/)"]
        PROCESSED["Processed Datasets<br/>(COGs, GeoParquet, GPKG)"]
    end

    subgraph Core Analytical Engines
        AUDIT["Audit & Discovery Engine<br/>(geoslide.audit)"]
        STATIC_ENGINE["Static Feature & Susceptibility Engine<br/>(geoslide.features / modelling)"]
        RAINFALL_ENGINE["Dynamic Rainfall Engine<br/>(geoslide.rainfall)"]
        HAZARD_FUSION["Hazard & Response Priority Fusion<br/>(geoslide.risk)"]
    end

    subgraph Service & API Layer
        FASTAPI["FastAPI REST Application<br/>(apps/api)"]
        TILE_SERVER["Vector/Raster Tile Services<br/>(PMTiles / COG Tiles)"]
    end

    subgraph Presentation & UI Layer
        WEB_APP["Next.js Statewide Command Centre<br/>(apps/web)"]
    end

    RAW --> AUDIT
    RAW --> INTERIM
    INTERIM --> STATIC_ENGINE
    INTERIM --> RAINFALL_ENGINE
    STATIC_ENGINE --> PROCESSED
    RAINFALL_ENGINE --> PROCESSED
    PROCESSED --> HAZARD_FUSION
    HAZARD_FUSION --> FASTAPI
    PROCESSED --> TILE_SERVER
    FASTAPI --> WEB_APP
    TILE_SERVER --> WEB_APP
```

---

## 2. Key Component Specifications

### 2.1 Static Susceptibility Module (`geoslide.modelling`)
- **Algorithms**: XGBoost Classifier with spatial block cross-validation.
- **Predictors**: 20+ terrain, geological, structural, and land-cover rasters aligned to 100m UTM grid (`EPSG:32643`).
- **Explainability**: SHAP (SHapley Additive exPlanations) values per location prediction.

### 2.2 Dynamic Rainfall Engine (`geoslide.rainfall`)
- **Climatology**: Historical daily gridded IMD rainfall percentiles (90th, 95th, 99th).
- **Near-Real-Time Trigger**: GPM IMERG 30-minute to 72-hour cumulative accumulation.
- **Fallback**: India-WRIS station network data validation.

### 2.3 Web Delivery & Tile Strategy (`geoslide.tiling`)
- Raw heavy rasters (2+ GB) are NEVER transferred directly to the frontend.
- Rasters are served via Cloud-Optimized GeoTIFFs (COG) / TiTiler.
- Vectors (roads, boundaries, landslide inventories) are served via PMTiles / MapLibre vector tiles.
