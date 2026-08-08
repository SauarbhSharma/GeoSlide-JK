<p align="center">
  <img src="apps/web/public/branding/geoslide-jk-logo-horizontal.png" alt="GeoSlide-JK — Landslide Risk Intelligence" width="560">
</p>

<p align="center">
  <b>Machine-Learning Landslide Susceptibility and Rainfall-Triggered Hazard Decision Support for Jammu & Kashmir</b>
</p>

# 🏔️ GeoSlide-JK v1.0.0 — Full-J&K Landslide Susceptibility & Dynamic Hazard Intelligence Engine

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14.2.35-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)
[![Spatial CV ROC-AUC](https://img.shields.io/badge/Spatial_CV_ROC--AUC-0.8694-success.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **⚠️ Research Disclaimer**: GeoSlide-JK is a research decision-support prototype and is not an official government warning system.

---

## 📌 Executive Summary

**GeoSlide-JK** is an end-to-end geospatial artificial intelligence engine and interactive decision-support application built for the Union Territory of Jammu and Kashmir (J&K), India. The system integrates multi-source Earth observation satellites, high-resolution topographic data (**Copernicus GLO-30 DEM**), geological structures (**GSI 50K Lithology & Tectonics**), land cover (**ESA WorldCover 2021**), exposure layers, and historical landslide events (**NGDR Inventory**) into a standardized **100m EPSG:32643 Master Analysis Grid** covering **4.62 million valid land cells** across all **20 UT districts**.

The platform provides dual deployment interfaces:
1. **Full-Featured Next.js + FastAPI Research Prototype**: High-performance MapLibre GL vector/raster web application with custom FastAPI microservices.
2. **Streamlit Submission Companion Application**: Standalone lightweight dashboard optimized for institutional review and Streamlit Community Cloud hosting.

---

## 🎯 Main Objectives

- **Standardized Multi-Domain Raster Stack**: Harmonize disparate vector/raster datasets onto a single UTM Zone 43N (EPSG:32643) 100m spatial grid.
- **Leakage-Isolated Machine Learning**: Train an engineered **30-predictor XGBoost Classifier** evaluated via 5-fold spatial district-block cross-validation, strictly isolating pre-existing susceptibility benchmarks (NLSM), geographic coordinates, and exposure layers.
- **Dynamic Scenario Triggering**: Combine static ML susceptibility ratings with 24-hour rainfall accumulation scenarios and climatological IMD 90th percentile (P90) anomaly ratios ($R_{anomaly} = P_{24h} / P_{90}$).
- **Corridor & District Intelligence**: Enable multi-scale location risk checks along critical transportation corridors (e.g. NH-44 Jammu-Srinagar Highway at Panthyal).

---

## 🗺️ System Architecture

```
                               ┌──────────────────────────────────────────────┐
                               │       Multi-Source Raw Input Discovery       │
                               │  Copernicus DEM | ESA WorldCover | GSI | NGDR │
                               └──────────────────────┬───────────────────────┘
                                                      │
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │  Phase 2 Master Analysis Grid (EPSG:32643)   │
                               │     100m Resolution | 4.62M Land Cells      │
                               └──────────────────────┬───────────────────────┘
                                                      │
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │ Phase 3 Multi-Domain Feature Engineering     │
                               │  Terrain (16) | Geology (10) | Landcover(10) │
                               └──────────────────────┬───────────────────────┘
                                                      │
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │   Phase 4 Machine-Learning Susceptibility    │
                               │  XGBoost Classifier | Spatial Block 5-CV     │
                               │           Spatial ROC-AUC: 0.8694            │
                               └──────────────────────┬───────────────────────┘
                                                      │
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │  Phase 5 Dynamic Rainfall Hazard Scenarios   │
                               │    24h Accumulation & IMD P90 Baseline       │
                               └──────────────┬────────────────┬──────────────┘
                                              │                │
                      ┌───────────────────────┘                └───────────────────────┐
                      ▼                                                                ▼
   ┌─────────────────────────────────────┐                          ┌─────────────────────────────────────┐
   │ Next.js 14 + FastAPI Microservices  │                          │ Streamlit Submission Companion App  │
   │  MapLibre GL JS | Tile Server REST  │                          │ Independent Streamlit Deployment   │
   └─────────────────────────────────────┘                          └─────────────────────────────────────┘
```

---

## 📊 Phase 4 Model Performance & Validation

The susceptibility model was trained using an **XGBoost Gradient Boosted Classifier** (150 trees, max depth 6, learning rate 0.08) and evaluated using **5-Fold Out-of-Fold Spatial District-Block Cross-Validation** to eliminate spatial autocorrelation leakage.

### Quantitative Metrics Summary

| Validation Metric | Score | Validation Standard |
| :--- | :--- | :--- |
| **Spatial CV ROC-AUC** | **0.8694** | Exceeds target threshold ($\ge 0.8000$) |
| **Spatial CV PR-AUC** | **0.2760** | Baseline positive prevalence: $0.0051$ |
| **Brier Reliability Score** | **0.1788** | Well-calibrated probabilistic outputs |
| **Active UT Districts** | **20** | 100% UT district coverage |

### 5-Fold Spatial District Block Breakdown

- **Fold 1 (Jammu Region)**: ROC-AUC **0.8919**
- **Fold 2 (Chenab Valley)**: ROC-AUC **0.8279**
- **Fold 3 (Kashmir Valley)**: ROC-AUC **0.6210**
- **Fold 4 (Pir Panjal Range)**: ROC-AUC **0.8584**
- **Fold 5 (Northern Border)**: ROC-AUC **0.9033**

### Top Predictor Features
1. `log1p_distance_to_fault`: Proximity to tectonic fault structures ($8.67\%$ importance)
2. `snow_ice_fraction`: Cryospheric land cover fraction ($8.12\%$ importance)
3. `elevation`: Terrain altitude above sea level ($4.20\%$ importance)
4. `log1p_distance_to_active_fault`: Distance to neotectonic faults ($3.96\%$ importance)
5. `distance_to_drainage`: Proximity to fluvial erosion channels ($3.77\%$ importance)

---

## ⚠️ Phase 5 Dynamic Rainfall Scenario & Proxy Limitations

- **Scenario / Proxy Mode**: Dynamic 24-hour rainfall accumulation and IMD P90 baseline percentiles represent **research proxy products** designed for scenario demonstration.
- **Operational Integration Notice**: Live real-time IMD/GPM satellite stream ingestion remains future work.
- **Non-Warning Disclaimer**: Output dynamic hazard maps ($H_{dyn}$) must not be treated as real-time operational weather warnings.

---

## 🚀 Execution Instructions

### Option A: Launch Streamlit Submission Companion Application (Recommended for Cloud)

```bash
# 1. Navigate to project root
cd D:\Projects\GeoSlide_JK

# 2. Launch Streamlit companion app
streamlit run streamlit_app/streamlit_app.py
```
*Access in browser at `http://localhost:8501`.*

---

### Option B: Launch Full Next.js + FastAPI Local Stack

```bash
# 1. Run automated startup batch script
scripts\start_demo.bat

# 2. Or manually start backend & frontend:
# Backend (FastAPI):
python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000

# Frontend (Next.js):
cd apps/web
npm run start -- -p 3000 -H 127.0.0.1
```
*Access Next.js UI at `http://localhost:3000` and API docs at `http://localhost:8000/docs`.*

To stop background services cleanly:
```bash
scripts\stop_demo.bat
```

---

## ☁️ Streamlit Community Cloud Deployment

To deploy this application to **Streamlit Community Cloud**:

1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **"New app"**.
3. Fill in the exact repository parameters:
   - **Repository**: `SauarbhSharma/GeoSlide-JK`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app/streamlit_app.py`
4. The dependency configuration file is located at `streamlit_app/requirements.txt`.
5. Click **"Deploy!"**.

---

## 📁 Repository Structure

```
GeoSlide-JK/
├── apps/
│   ├── api/                   # FastAPI backend microservices
│   └── web/                   # Next.js 14 MapLibre web frontend
├── configs/                   # System YAML configurations (grid, features, paths)
├── data/
│   ├── models/                # Trained XGBoost susceptibility model JSON/PKL
│   └── processed/boundaries/  # 20-District J&K boundary GeoJSON
├── docs/                      # Comprehensive Phase 0–6 reports & verification
│   ├── PUBLIC_RELEASE_AUDIT.md
│   ├── STREAMLIT_DEPLOYMENT_CHECKLIST.md
│   └── FINAL_GITHUB_AND_STREAMLIT_VERIFICATION.md
├── outputs/reports/           # Verified CSV and Markdown audit logs
├── scripts/                   # Automated startup/shutdown & stress test scripts
├── streamlit_app/             # Standalone Streamlit Submission Companion App
│   ├── assets/                # Compact derived deployment assets (GeoJSON, CSV, JSON)
│   ├── requirements.txt       # Lightweight Streamlit dependencies
│   ├── README_STREAMLIT.md    # Streamlit app documentation
│   └── streamlit_app.py       # Streamlit main entrypoint
├── .streamlit/                # Streamlit dark theme config
├── tests/                     # 286 passing Python master unit tests
├── .gitignore                 # Strengthened security & data exclusion rules
└── README.md                  # Main repository README
```

---

## 📜 Citation & Acknowledgements

If you use GeoSlide-JK software, datasets, or methodology in your research, please cite:

```bibtex
@misc{geoslide_jk_2026,
  author = {Sharma, Saurabh and GeoSlide-JK Team},
  title = {GeoSlide-JK: Full-J&K Landslide Susceptibility & Dynamic Hazard Intelligence Engine},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/SauarbhSharma/GeoSlide-JK}}
}
```

*Data Sources Acknowledgment: Copernicus GLO-30 DEM (ESA/Copernicus), ESA WorldCover 2021 (ESA), Geological Survey of India (GSI 50K Lithology/Tectonics), National Geo-hazard Data Repository (NGDR Landslide Inventory).*

---

## 🔬 V2-3F-R7 Scientific Evidence & Release Integrity

### GeoSlide-JK Release Baseline & Current Stable Version: `2.3.13`
- **Current Milestone Tag:** `v2.3f-r7-nh44-dhi-cryptographic-evidence-correction`
- **Release Date:** August 8, 2026
- **Status:** PASSED (V2-3F-R7 NH-44 DHI Cryptographic Evidence, Authoritative Provenance and Reproducibility Correction)
- **Authoritative 2D GPM Spatial Grid Intersection:** 11 native 2D 0.1° GPM cells across 5 latitude bands (33.0°N to 33.5°N) mapped to all 158 corridor segments with 100% Path A/B agreement.
- **Unproven 8 Support Locations:** Marked `ROLE_UNPROVEN` and excluded from scientific calculations.
- **Scenario Provenance:** Corrected S4 and S5 to repository-defined hypothetical stress test classifications.
- **DHI_D Redundancy:** `DHI_D = sqrt(DHI_B)` proved with 0.0 machine-precision residual in full precision and 4.29e-5 on 4-decimal rounded values (`ROUNDED_SERIALIZATION_CONSISTENT`).
- **Reproducibility:** 100% path-independent, isolated, fresh-clone reproducible pipeline with complete POSIX manifest coverage.
