# FINAL FUNCTIONAL DIAGNOSTIC REPORT

**Date**: 2026-07-30  
**Branch**: `final-submission-hotfix`  
**Commit**: `130b2ae`  

---

## 1. Backend

- **Runtime**: FastAPI + Uvicorn
- **Default URL**: `http://localhost:8000`
- **Health**: `GET /api/v1/health` → `{"status":"healthy",...}`

### Discovered Endpoints (from FastAPI source)

| Route | Method | Description |
|:---|:---|:---|
| `/` | GET | Root info |
| `/api/v1/health` | GET | Health check |
| `/api/v1/status` | GET | System status |
| `/api/v1/districts` | GET | District list |
| `/api/v1/districts/boundary` | GET | Districts GeoJSON |
| `/api/v1/terrain/click` | GET | Full point query (terrain+susc+hazard) |
| `/api/v1/terrain/value` | GET | Alias for terrain/click |
| `/api/v1/features/nearby` | GET | Nearby features |
| `/api/v1/susceptibility` | GET | Susceptibility summary |
| `/api/v1/transparency` | GET | Model transparency info |
| `/api/v1/location-check` | GET | Location risk check (delegates to terrain/click) |
| `/api/v1/static-layers` | GET | List static layers |
| `/api/v1/static-layers/{name}` | GET | Individual vector layer GeoJSON |
| `/api/v1/map/config` | GET | Map configuration |

**Total unique routes**: 14 (not 9 as claimed by Status page)

---

## 2. Frontend-to-Backend Integration Failures

### 2.1 Location-Check 404
- **Cause**: Frontend `location-check/page.tsx` line 58 calls `fetch('/api/v1/location-check?...')` — a **relative URL** which resolves to `http://localhost:3000/api/v1/location-check` (Next.js dev server). No proxy/rewrite configured in `next.config.js`.
- **Fix**: Use `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000` and centralized API config.

### 2.2 Map API calls hardcoded
- **Cause**: `MapContainer.tsx` hardcodes `http://localhost:8000` for district boundaries (line 166), vector layers (line 238), and terrain inspection (line 340).
- **Fix**: Use same centralized API config.

### 2.3 Status page hardcodes health URL
- **Cause**: `status/page.tsx` line 12 uses `http://127.0.0.1:8000` (inconsistent with other pages).
- **Fix**: Use centralized config.

---

## 3. Map Rendering Issues

### 3.1 Basemap
- CARTO dark tiles (`https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png`) are valid.
- `maplibre-gl/dist/maplibre-gl.css` IS imported on line 5 of MapContainer.tsx.
- Map container has `min-h-[620px]` and `w-full h-full`.
- **Likely Issue**: No error — the basemap should work when loaded. However, if CARTO CDN is blocked, no fallback exists. Add basemap error handling.

### 3.2 Raster Layers Not Rendering
- **Cause**: These are server-side sampled rasters — there is NO raster tile endpoint. The `/api/v1/terrain/click` endpoint returns pixel values at a point, not tiles. The map can display GeoJSON vectors but cannot render rasters as map layers because no tile server exists.
- **Reality**: The layer registry references `/api/v1/terrain/click` and `/api/v1/susceptibility` as `tileOrSourceUrl`, but these return JSON, not raster tiles.
- **Fix**: The map must load vector data and use click-inspect for raster values. Susceptibility/hazard display would require a COG tile server (e.g., titiler) which doesn't exist. Register these layers as "Inspector-Only (Point Query)" rather than visual map layers.

### 3.3 Dynamic Hazard Layers Disabled
- **Cause**: `MapContainer.tsx` line 517: `isAvailable = layer.availability === "Available"` — Scenario/Proxy Mode layers are excluded from checkboxes.
- **Fix**: Allow "Scenario / Proxy Mode" layers in the map panel too.

---

## 4. Outdated Labels

| Location | Issue |
|:---|:---|
| MapContainer.tsx line 511 | "Phase 2 Master Layer Registry" |
| MapContainer.tsx line 385 | Popup badge "Phase 2" |
| Sidebar.tsx line 125 | "Risk Scale & Legend (Demo)" |
| Sidebar.tsx lines 132-160 | Five "Demo Priority" labels |
| Status.tsx line 78 | "9 Live Endpoints" hardcoded |
| Status.tsx line 58 | "Operational" shown without checking |

---

## 5. Transparency Page Provenance

- **LR ROC-AUC 0.7420**: NOT found in any auditable output file.
- **RF ROC-AUC 0.8410**: NOT found in any auditable output file.
- **Fix**: Remove numeric values, label as "Evaluated" only.
