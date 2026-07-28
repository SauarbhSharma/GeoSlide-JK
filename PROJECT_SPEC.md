# GeoSlide-JK System Specification

## 1. System Vision & Objective

GeoSlide-JK provides an end-to-end geospatial decision-support pipeline for assessing landslide susceptibility and dynamic rainfall-triggered hazard across the Union Territory of Jammu and Kashmir.

### Core Objectives
1. Maintain statewide spatial analytics across all 20 current J&K districts.
2. Separate static slope susceptibility (terrain, geology, land cover, structures) from dynamic trigger state (recent cumulative rainfall).
3. Compute exposure metrics for population, settlements, and major highway corridors (NH-44).
4. Provide transparent, explainable location-level risk advisories backed by SHAP factor importance.

---

## 2. Technical Stack

| Layer | Technology |
| :--- | :--- |
| **Language & Runtime** | Python 3.11+ |
| **Geospatial Engine** | GeoPandas, Shapely, Pyogrio, Rasterio, Rioxarray, Xarray, NetCDF4, GDAL |
| **Machine Learning** | Scikit-learn, XGBoost, SHAP, Joblib |
| **Backend API** | FastAPI, Pydantic, Uvicorn, SQLAlchemy |
| **Data Formats** | Cloud-Optimized GeoTIFF (COG), GeoPackage (GPKG), GeoParquet, PMTiles |
| **Frontend Framework** | Next.js, React, TypeScript, Tailwind CSS, MapLibre GL JS, TanStack Query |
| **Processing Grid** | EPSG:32643 (UTM Zone 43N), 100m cell size (250m fallback) |
| **Web Delivery CRS** | EPSG:4326 (WGS 84) |

---

## 3. Data Processing Architecture

```
                               ┌────────────────────────────────┐
                               │  Read-Only Raw Data Workspace  │
                               │ C:\Users\...\Downloads\J&K     │
                               └───────────────┬────────────────┘
                                               │
                                               ▼
                              ┌──────────────────────────────────┐
                              │ Safe Data Discovery & Validation │
                              │   (src/geoslide/audit/)          │
                              └────────────────┬─────────────────┘
                                               │
               ┌───────────────────────────────┼───────────────────────────────┐
               ▼                               ▼                               ▼
  ┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
  │  Phase C: Terrain Pipeline│     │Phase D: Geological & LULC│     │  Phase G: Rainfall Engine│
  │ DEM, Slope, Aspect, TWI │     │ Lithology, Faults, LULC │     │  IMD Climatology, IMERG │
  └────────────┬────────────┘     └────────────┬────────────┘     └────────────┬────────────┘
               │                               │                               │
               └───────────────────────┬───────┘                               │
                                       ▼                                       │
                         ┌───────────────────────────┐                         │
                         │  Phase F: Static Model    │                         │
                         │ XGBoost Susceptibility    │                         │
                         └─────────────┬─────────────┘                         │
                                       │                                       │
                                       └───────────────────┬───────────────────┘
                                                           ▼
                                             ┌───────────────────────────┐
                                             │ Phase H: Hazard Matrix    │
                                             │ Dynamic Risk & Exposure   │
                                             └─────────────┬─────────────┘
                                                           │
                                                           ▼
                                             ┌───────────────────────────┐
                                             │  Phase 1-7: FastAPI & UI  │
                                             │   MapLibre Command Center │
                                             └───────────────────────────┘
```

---

## 4. Operational Requirements & Boundaries

- **Statewide J&K Scope**: Explicit boundary processing filtering Leh & Kargil from historical 22-district boundary files to yield the modern 20 J&K districts.
- **Data Confidence Masking**: Any grid cell lacking required predictor coverage MUST be assigned `Insufficient Data` (Confidence: Low/Insufficient), preventing false "Low Risk" classifications.
- **Reproducibility**: All feature thresholds, matrix definitions, and spatial block cross-validation split seeds are governed by external YAML configurations.
