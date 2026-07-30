# FINAL FUNCTIONAL ACCEPTANCE REPORT

**Project**: GeoSlide-JK v1.0.0 — Himalayan Landslide Susceptibility & Dynamic Hazard System  
**Branch**: `final-application-functional-recovery`  
**Commit**: Pending Final Commit  
**Date**: 2026-07-30  

---

## 1. Application Runtime Configuration

- **Frontend URL**: `http://127.0.0.1:3000` (Next.js 14.2)
- **Backend URL**: `http://127.0.0.1:8000` (FastAPI 1.0.0)
- **Central API Config**: `apps/web/lib/api.ts` + `apps/web/.env.local` + `next.config.js` proxy rewrites (`/api/*` → `http://127.0.0.1:8000/api/*`)
- **Backend Startup Command**: `scripts/start_demo.bat` (`C:\Program Files\Python311\python.exe -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000`)
- **Frontend Startup Command**: `npm run dev -- -p 3000 -H 127.0.0.1`
- **Shutdown Command**: `scripts/stop_demo.bat`

---

## 2. Executive Verification Summary

| Verification Category | Status | Details |
|:---|:---:|:---|
| **Backend Health** | **PASS** | `GET /api/v1/health` returns `HTTP 200` (`status: healthy`) |
| **Location Risk Check** | **PASS** | `GET /api/v1/location-check` returns `HTTP 200` with full advisory |
| **Raster Tile Server** | **PASS** | PNG tile service rendering 256x256 Web Mercator tiles for 8 rasters |
| **Map Basemap & Fallback** | **PASS** | CARTO Dark OpenStreetMap basemap active with local boundary fallback |
| **Susceptibility Raster Display**| **PASS** | Static susceptibility probability overlay visible by default |
| **Dynamic Hazard Display** | **PASS** | Dynamic hazard index & class PNG raster tiles fully functional |
| **Map Cell Inspector** | **PASS** | Map click samples 100m cells returning real elevation, slope, ML & hazard |
| **Synchronized Layer Controls** | **PASS** | Sidebar eye icons, Map Layers checkboxes, and map visibility 100% synced |
| **Rainfall Monitor Query** | **PASS** | Point query samples 24h proxy, P90 baseline, anomaly ratio & hazard index |
| **District Intelligence** | **PASS** | Dynamic zonal statistics loaded for all 20 districts via API |
| **Live Status Page** | **PASS** | Dynamic health check querying all 9 FastAPI endpoints (all HTTP 200) |
| **Model Transparency** | **PASS** | XGBoost ROC-AUC 0.8694, 30 features, 5-fold spatial CV results |
| **Next.js Production Build** | **PASS** | `npm run build` completed with 0 errors across 10 static pages |
| **Playwright E2E Tests** | **PASS** | 100% pass rate across 11 test flows and screenshots |

---

## 3. Live API Endpoint Matrix (22 Endpoints Tested)

| Path | Method | Status | Format | Functionality |
|:---|:---:|:---:|:---:|:---|
| `/api/v1/health` | GET | `200 OK` | JSON | Health status & endpoint readiness |
| `/api/v1/status` | GET | `200 OK` | JSON | Pipeline lifecycle execution status |
| `/api/v1/districts` | GET | `200 OK` | JSON | List 20 J&K UT districts |
| `/api/v1/districts/boundary` | GET | `200 OK` | GeoJSON | District polygons (EPSG:4326) |
| `/api/v1/terrain/click` | GET | `200 OK` | JSON | Point query (elevation, slope, ML, hazard) |
| `/api/v1/terrain/value` | GET | `200 OK` | JSON | Point query alias |
| `/api/v1/location-check` | GET | `200 OK` | JSON | Point risk check with advisory & precautions |
| `/api/v1/tiles/susceptibility_prob/{z}/{x}/{y}.png` | GET | `200 OK` | PNG | Static susceptibility probability tile |
| `/api/v1/tiles/susceptibility_class/{z}/{x}/{y}.png` | GET | `200 OK` | PNG | Static susceptibility class tile |
| `/api/v1/tiles/dynamic_hazard_index/{z}/{x}/{y}.png` | GET | `200 OK` | PNG | Dynamic hazard index tile |
| `/api/v1/tiles/dynamic_hazard_class/{z}/{x}/{y}.png` | GET | `200 OK` | PNG | Dynamic hazard class tile |
| `/api/v1/tiles/elevation/{z}/{x}/{y}.png` | GET | `200 OK` | PNG | Copernicus DEM elevation tile |
| `/api/v1/tiles/slope/{z}/{x}/{y}.png` | GET | `200 OK` | PNG | Terrain slope angle tile |
| `/api/v1/tiles/aspect/{z}/{x}/{y}.png` | GET | `200 OK` | PNG | Terrain aspect orientation tile |
| `/api/v1/tiles/hillshade/{z}/{x}/{y}.png` | GET | `200 OK` | PNG | Analytical hillshade tile |
| `/api/v1/layers` | GET | `200 OK` | JSON | Master layer registry manifest |
| `/api/v1/static-layers` | GET | `200 OK` | JSON | Vector layers list |
| `/api/v1/static-layers/{layer}` | GET | `200 OK` | GeoJSON | Vector feature layer GeoJSON |
| `/api/v1/summary/statewide` | GET | `200 OK` | JSON | Statewide zonal statistics & ML metrics |
| `/api/v1/summary/district/{id}` | GET | `200 OK` | JSON | District zonal summary statistics |
| `/api/v1/transparency` | GET | `200 OK` | JSON | Model metrics & leakage safeguards |
| `/api/v1/map/config` | GET | `200 OK` | JSON | Map center, zoom & CRS config |

---

## 4. Location Risk Check Point-Query Verification

Verified three geographically distinct J&K locations and one outside-area boundary point:

### Location 1: Panthyal, Ramban (33.2450°N, 75.2410°E)
- **HTTP Status**: `200 OK`
- **District**: Ramban District
- **Elevation / Slope**: 1,425.6m ASL / 34.2°
- **Susceptibility Class**: Moderate (Probability: `0.2045`)
- **24h Rainfall Proxy / P90**: 25.0 mm / 45.0 mm (Anomaly Ratio: `0.56x`)
- **Dynamic Hazard Class**: Low (Index: `0.1145`)
- **Advisory**: Dynamic hazard rating for location in Ramban is currently Low. Monitor local weather and road advisories.

### Location 2: Jammu City (32.7260°N, 74.8570°E)
- **HTTP Status**: `200 OK`
- **District**: Jammu District
- **Elevation / Slope**: 312.4m ASL / 4.1°
- **Susceptibility Class**: Very Low (Probability: `0.0210`)
- **24h Rainfall Proxy / P90**: 12.0 mm / 55.0 mm (Anomaly Ratio: `0.22x`)
- **Dynamic Hazard Class**: Very Low (Index: `0.0046`)
- **Advisory**: Dynamic hazard rating for location in Jammu is currently Very Low.

### Location 3: Srinagar Aerodrome (34.0830°N, 74.7970°E)
- **HTTP Status**: `200 OK`
- **District**: Srinagar District
- **Elevation / Slope**: 1,582.1m ASL / 2.8°
- **Susceptibility Class**: Low (Probability: `0.0845`)
- **24h Rainfall Proxy / P90**: 18.0 mm / 40.0 mm (Anomaly Ratio: `0.45x`)
- **Dynamic Hazard Class**: Low (Index: `0.0380`)
- **Advisory**: Dynamic hazard rating for location in Srinagar is currently Low.

### Location 4: Outside Study Domain (Delhi: 28.6130°N, 77.2090°E)
- **HTTP Status**: `200 OK` (Controlled Validation Response)
- **inside_study_area**: `false`
- **data_available**: `false`
- **message**: "The selected point is outside the 20-district J&K UT boundary."

---

## 5. UI Control Audit Matrix

| Route | Control | Expected Action | Actual Behavior | Status |
|:---|:---|:---|:---|:---:|
| `/` | District Selector | Zoom map to district | Viewport fits district bounds | **PASS** |
| `/` | Sidebar Eye Toggle | Toggle map layer visibility | Toggles MapLibre layer | **PASS** |
| `/` | Map Layers Checkbox | Toggle map layer from panel | Synchronized with sidebar & map | **PASS** |
| `/` | Map Click Inspector | Sample 100m raster cell | Displays real elevation, slope, ML & hazard | **PASS** |
| `/` | Reset to J&K | Reset map bounds | Viewport fits [73.2 32.2 77.8 35.2] | **PASS** |
| `/explorer` | Layer Checkbox | Toggle raster layers | Renders PNG tiles dynamically | **PASS** |
| `/districts` | District Dropdown | Change district profile | Loads zonal summary from API | **PASS** |
| `/rainfall` | Sample Values Button | Query 24h rain proxy | Displays 24h proxy & P90 baseline | **PASS** |
| `/location-check` | Query Button | Execute point-risk check | Returns HTTP 200 with full advisory | **PASS** |
| `/location-check` | Preset Selector | Load preset coordinates | Populates Ramban, Jammu, Srinagar | **PASS** |
| `/location-check` | GPS Geolocation | Request browser location | Prompts location permission cleanly | **PASS** |
| `/status` | Page Load Check | Poll 9 FastAPI endpoints | Displays live HTTP 200 badges | **PASS** |

---

## 6. Captured Screenshot Evidence

Saved to `docs/progress/final_functional_screenshots/`:

1. `01_command_centre.png` — Command Centre map with visible basemap, boundaries & susceptibility raster
2. `02_risk_explorer.png` — Risk Explorer with active layer controls
3. `02b_inspector_active.png` — Active Map Inspector displaying real 100m sampled raster values
4. `03_district_ramban.png` — District Intelligence profile for Ramban
5. `03b_district_doda.png` — District Intelligence profile for Doda
6. `04_rainfall_monitor.png` — Rainfall Monitor with sampled 24h proxy values
7. `05a_location_panthyal.png` — Location Risk Check for Panthyal, Ramban (HTTP 200)
8. `05b_location_jammu.png` — Location Risk Check for Jammu City (HTTP 200)
9. `05c_location_srinagar.png` — Location Risk Check for Srinagar Aerodrome (HTTP 200)
10. `05d_location_outside.png` — Location Risk Check for outside-area coordinate (Controlled response)
11. `06_model_transparency.png` — Model Transparency with audited XGBoost metrics
12. `07_data_system_status.png` — Data & System Status showing 9 live endpoints connected

---

## 7. Standalone Runbook

Refer to `docs/progress/DEMO_RUNBOOK.md` for the quick 10-step startup and demonstration runbook.
