# GeoSlide-JK v1.0.0 — Standalone Demonstration Runbook

This document provides a concise 10-step procedure for starting, running, inspecting, and stopping the complete GeoSlide-JK v1.0.0 decision-support application.

---

## Startup

### 1. Launch All Microservices
Run the automated startup script in a terminal:
```cmd
scripts\start_demo.bat
```
This script automatically:
- Starts the FastAPI backend engine on `http://127.0.0.1:8000`
- Verifies health check (`/api/v1/health` → HTTP 200)
- Starts the Next.js web application on `http://127.0.0.1:3000`

---

## Live Demonstration Steps

### 2. Statewide Command Centre (`/`)
- Open `http://127.0.0.1:3000` in your web browser.
- Verify the OpenStreetMap dark basemap and 20 J&K UT district boundaries are visible.
- Observe the static XGBoost susceptibility probability raster overlay rendered by default across J&K.

### 3. Interactive Risk Explorer (`/explorer`)
- Navigate to **Risk Explorer** via top navigation bar.
- Toggle layer visibility using either the **Sidebar eye icons** or the **Map Layers checkboxes**.
- Toggle between **Static Susceptibility Probability**, **Static Susceptibility Class**, and **Dynamic Hazard Index**.

### 4. Map Cell Inspector
- Click any point on the interactive map surface (e.g., near Ramban / NH-44).
- Verify the **Inspector tab** and **Map Popup** automatically display sampled 100m cell values:
  - Elevation (meters ASL)
  - Slope Angle (degrees)
  - Aspect Azimuth
  - Static Susceptibility Probability & Rating Class
  - 24-Hour Rainfall Proxy & Dynamic Hazard Rating

### 5. Location Risk Check (`/location-check`)
- Navigate to **Location Check**.
- Select a preset location (e.g. `Panthyal NH-44, Ramban` or `Srinagar Aerodrome`) or enter coordinates manually (`33.2450°N, 75.2410°E`).
- Click **Query**.
- Verify HTTP 200 response returning district name, susceptibility rating, 24h rainfall proxy, P90 baseline, anomaly ratio, dynamic hazard rating, and precautionary advisories.

### 6. Rainfall Monitor (`/rainfall`)
- Navigate to **Rainfall Monitor**.
- Enter coordinates or select a preset and click **Sample Values**.
- Observe 24-hour rainfall proxy, P90 baseline proxy, anomaly ratio, and dynamic hazard index.

### 7. District Intelligence (`/districts`)
- Navigate to **District Intelligence**.
- Select different districts from the dropdown menu (e.g. `Ramban`, `Doda`, `Kishtwar`, `Jammu`, `Srinagar`).
- Verify the profile updates dynamically with verified boundary state and calculated zonal risk metrics.

### 8. Model & Methodology Transparency (`/transparency`)
- Navigate to **Model Transparency**.
- Review audited XGBoost metrics: ROC-AUC `0.8694`, PR-AUC `0.2760`, Brier `0.1788`.
- Review 5-fold spatial cross-validation scores and predictor isolation safeguards.

### 9. Data & System Status (`/status`)
- Navigate to **System Status**.
- Review live health status for all 9 core FastAPI endpoints (all showing `HTTP 200`).
- Review audit status (`Conditional Pass — Rainfall & P90 layers derived proxy products`).

---

## Shutdown

### 10. Stop All Services
Run the automated shutdown script:
```cmd
scripts\stop_demo.bat
```
