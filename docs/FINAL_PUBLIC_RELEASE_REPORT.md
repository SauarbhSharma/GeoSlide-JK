# GeoSlide-JK v1.0.0 — Final Public Release & Deployment Report

## 1. Repository & System Information

- **GitHub Repository URL**: `https://github.com/SauarbhSharma/GeoSlide-JK.git`
- **Target Branch**: `main`
- **Deployment Target**: Render Free Web Service (Docker-based single container)
- **Streamlit Wrapper**: Streamlit Community Cloud (Minimal iframe embed)

---

## 2. System Architecture & Container Design

The production web service packages both authoritative components into a single Docker container running on Render's free tier:

1. **FastAPI Backend**: Runs internally on `127.0.0.1:8000` via `uvicorn`.
2. **Next.js Frontend**: Runs standalone on `0.0.0.0:$PORT` via `node server.js`.
3. **Same-Origin Proxying**: Next.js rewrites proxy `/api/*` requests internally to `http://127.0.0.1:8000/api/*`, eliminating CORS issues and localhost dependencies in browser requests.

---

## 3. Streamlit Companion App Replacement

The separately recreated Streamlit dashboard has been **replaced with a minimal iframe wrapper**:

- **No duplicate metrics, maps, or hardcoded calculations.**
- **Embeds the authoritative Render URL** full-screen via `st.components.v1.iframe`.
- **Configured via secret**: `GEOSLIDE_PUBLIC_APP_URL`.
- Includes fallback direct link: *"Open GeoSlide-JK in full screen ↗"*.

---

## 4. Asset Strategy & Limitations

| Asset Category | Strategy | Size / Status |
|:---|:---|:---|
| **Susceptibility Rasters** | Included in Git & Docker build | ~16.7 MB total (Probability + Class) |
| **Dynamic Hazard Rasters** | Included in Git & Docker build | ~16.7 MB total (Index + Class) |
| **Rainfall Proxy Rasters** | Included in Git & Docker build | ~43.0 MB total (24h, P90, Anomaly) |
| **Boundary GeoJSON** | Included in Git & Docker build | ~0.2 MB total (UT + 20 Districts) |
| **Vector Layers** | Included in Git & Docker build | ~11.5 MB total (Parquet) |
| **Terrain COGs** | Excluded from Git (>100MB limit) | Elevation (216MB), Slope (231MB), Aspect (231MB) |

*Note: The application degrades gracefully when terrain COGs are unavailable — analytical layers (susceptibility, hazard, rainfall, vectors, boundaries) remain 100% operational.*

---

## 5. Model Transparency & Truthfulness Summary

- **Primary Model**: XGBoost Classifier (30 predictor features)
- **Spatial CV ROC-AUC**: `0.8694`
- **Spatial CV PR-AUC**: `0.2760`
- **Brier Reliability Score**: `0.1788`
- **Spatial Folds**:
  - Fold 1 (Anantnag, Bandipora, Reasi, Shopian): `0.8919`
  - Fold 2 (Budgam, Ganderbal, Kishtwar, Poonch): `0.8279`
  - Fold 3 (Baramulla, Rajouri, Samba, Srinagar): `0.6210`
  - Fold 4 (Doda, Kulgam, Pulwama, Udhampur): `0.8584`
  - Fold 5 (Jammu, Kathua, Kupwara, Ramban): `0.9033`
- **Rainfall Wording**: Scenario/proxy rainfall products (not live operational IMD/GPM observations).
- **Disclaimer**: *"GeoSlide-JK is a research decision-support prototype and is not an official government warning system."*
