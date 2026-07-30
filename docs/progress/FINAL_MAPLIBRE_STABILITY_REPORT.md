# FINAL MAPLIBRE RUNTIME STABILITY & LIFECYCLE AUDIT REPORT

**Project**: GeoSlide-JK v1.0.0 — Himalayan Landslide Susceptibility & Dynamic Hazard System  
**Branch**: `final-application-functional-recovery`  
**Commit**: Pending Final Commit  
**Date**: 2026-07-30  

---

## 1. Issue Diagnosis & Root Cause Analysis

### Diagnosed Symptoms
During rapid interactive map navigation (e.g. repeated clicks, fast pan/zoom, layer toggling), Next.js development mode occasionally emitted:
`AbortError: signal is aborted without reason`
originating from MapLibre GL JS tile cancellation (`Vi.abortTile` → `_cleanUpRasterTiles` → `update`). A red runtime error overlay or toast appeared in the UI.

### Verified Root Causes
1. **Unstable Map Initialization Hook**:
   `MapContainer.tsx` contained `onSelectLocation` and `onSelectDistrict` callbacks in the `useEffect` dependency array. Whenever parent components re-rendered or updated callbacks during map clicks or district selection, the `useEffect` unmounted and called `mapRef.current.remove()`, then recreated the MapLibre instance. Calling `map.remove()` while raster tiles were loading aborted in-flight tile HTTP requests, throwing unhandled `AbortError` promises.
2. **Missing Global Rejection Prevention**:
   MapLibre GL JS uses native `fetch` with `AbortController` signals to cancel obsolete tile requests when zooming or panning out of tile bounds. These aborted tile promises bubble up to window `unhandledrejection` events, which Next.js interprets as runtime application failures unless caught and prevented.

---

## 2. Implemented MapLibre Lifecycle Fixes

1. **Stable Single-Mount Lifecycle**:
   - `MapContainer.tsx` map initialization `useEffect` now uses an empty dependency array `[]`.
   - `onSelectLocation` and `onSelectDistrict` callbacks are wrapped in stable React refs (`onSelectLocationRef`, `onSelectDistrictRef`) so map event handlers always access the latest callbacks without causing map recreation.
   - Added `if (mapRef.current) return;` to prevent double-initialization in React StrictMode.
   - Cleaned up unmount logic so `mapRef.current.remove()` executes idempotently only when the component actually unmounts.

2. **Scoped Window `unhandledrejection` Handler**:
   - Added a scoped event listener for window `unhandledrejection` events.
   - Calls `event.preventDefault()` exclusively when `event.reason` is an expected MapLibre tile `AbortError`.
   - Leaves all genuine application errors, network failures, and API exceptions untouched.

3. **Scoped Map & Fetch Error Handling**:
   - Added `map.on("error", ...)` filtering to ignore tile cancellation `AbortError`.
   - Wrapped point-query inspection `fetch` requests in safe `try/catch` blocks that return silently when `err.name === "AbortError"`.

4. **Raster Source & Layer Stabilization**:
   - Raster and vector layers are added once using `if (!map.getSource(id))` and `if (!map.getLayer(id))` guards.
   - Visibility changes triggered by `activeLayers` or `toggleLayer` use `map.setLayoutProperty(id, "visibility", ...)` without adding, removing, or recreating map sources.

5. **Updated Green Status Banner Wording**:
   Updated `app/page.tsx` and `app/explorer/page.tsx` to exact specification:
   `"GeoSlide-JK v1.0.0 Live: The static XGBoost susceptibility model and 100 m scenario-based dynamic hazard layers are available across all 20 J&K UT districts. Dynamic rainfall outputs are research proxy products and not operational observations."`

6. **Updated Production Startup Script (`scripts/start_demo.bat`)**:
   - Verifies if `apps/web/.next` exists, compiling Next.js production bundle via `npm run build` if missing.
   - Launches FastAPI backend on `127.0.0.1:8000` and Next.js production server on `127.0.0.1:3000`.
   - Performs automated PowerShell health check validation on both ports before reporting success.

---

## 3. Verification & Stress Regression Matrix

| Requirement | Verification Action | Result |
|:---|:---|:---:|
| **Development Mode Stability** | Tested rapid clicks & layer switches in dev mode | **PASS** (No uncaught AbortError) |
| **Production Mode Stability** | Tested against `npm run start` production server | **PASS** (No uncaught AbortError) |
| **Next.js Error Overlay** | Audited DOM for `#nextjs-portal` & `.nextjs-container-errors` | **PASS** (0 overlays triggered) |
| **Red Error Toast** | Checked for AbortError toast during stress clicks | **PASS** (0 error toasts triggered) |
| **25 Repeated Map Clicks** | Clicked 25 distinct geographic locations across J&K | **PASS** (Popup & Inspector updated cleanly) |
| **Pan & Zoom Stress** | Dragged viewport and scrolled mouse wheel 10+ times | **PASS** (Map remained smooth & visible) |
| **Layer Toggling** | Toggled 8+ raster & vector layers in rapid succession | **PASS** (Tiles rendered without rebuilds) |
| **District Changes** | Switched district dropdowns across Ramban, Doda, etc. | **PASS** (State updated without map recreation) |
| **Tile Endpoint Health** | Verified `/api/v1/tiles/{layer_id}/{z}/{x}/{y}.png` | **PASS** (`HTTP 200 OK`) |
| **Location Check Endpoint** | Verified `/api/v1/location-check?lat=33.245&lon=75.241` | **PASS** (`HTTP 200 OK`) |
| **Next.js Production Build** | Executed `npm run build` in `apps/web` | **PASS** (10/10 static pages compiled) |
| **Master Test Suite** | Executed `python tests/run_all_tests.py` | **PASS** (139/139 unit tests passed) |
