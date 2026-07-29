# GeoSlide-JK: Landslide Risk Prediction & Decision Support System

> **Terrain Intelligence and Rainfall-Triggered Landslide Risk Decision-Support Platform for the Union Territory of Jammu & Kashmir**

---

## Overview

**GeoSlide-JK** is a full-state geospatial decision-support application for Jammu and Kashmir (J&K). It integrates multi-source geospatial data—including digital elevation models (DEM), geological lithology, tectonic fault/thrust structures, land cover (LULC), historical landslide inventories, population distribution, and near-real-time satellite/gridded rainfall (NASA IMERG & IMD)—to deliver explainable landslide susceptibility and rainfall-triggered hazard advisories.

The system is designed as an explainable research platform providing statewide coverage across all **20 J&K UT Districts**.

---

## Current Status: Phase 2 — Static Geospatial Products (Complete)

- **App Version**: `v0.2.0` / `Phase 2 — Static Geospatial Products`
- **Global Status**: `Static Geospatial Layers: Live` | `Risk & Rainfall Modules: Demo`
- **DEM Source Lock**: Exactly four full-J&K Copernicus GLO-30 DEM tiles mosaicked & reprojected to `EPSG:32643` (30m resolution, 51,322,278 valid land pixels). Pilot DEM tile explicitly excluded.
- **Static Vector Layers**: 10 static vector layers processed to GeoPackage & GeoParquet clipped to 20 J&K UT districts (2,370 landslide points, 7,436 landslide polygons, 4,076 lithology units, tectonic faults/thrusts, NH-44, major roads, settlements, health facilities).
- **Active Fault Resolution**: Option B implemented (Active faults merged into `jk_faults.parquet` with attribute `fault_type = 'active'`).
- **Feature Reconciliation**: Produced `outputs/reports/phase_2_feature_count_reconciliation.csv` and `.md`.
- **Map Inspector**: MapLibre terrain cell inspector hardened against null, out-of-bounds, and rapid clicks.
- **UI & CSS Styling**: Full dark GeoSlide-JK theme repaired and verified across all 7 frontend routes.
- **Automated Test Suite**: 52 / 52 tests passing (100% clean execution).

---

## Key Architecture & Components

1. **Static Susceptibility Engine**: Machine learning model (XGBoost / Random Forest) trained on spatial terrain, geological, structural, and land-cover features using spatial block cross-validation (Model status: *Not Trained*).
2. **Rainfall Trigger Engine**: Antecedent and short-term rainfall accumulator utilizing IMD historical climatology and GPM IMERG near-real-time data (Status: *Demo placeholder*).
3. **Hazard & Response Priority Fusion**: Matrix-based fusion combining static susceptibility with dynamic rainfall triggers, overlaid against exposed population, settlements, critical facilities, and major transportation corridors (including NH-44).
4. **Interactive Map-First UI**: Modern web interface (Next.js, Tailwind CSS, MapLibre GL JS) offering statewide views, district intelligence cards, map-click explanations, and downloadable advisories.

---

## Directory Structure

```text
GeoSlide_JK/
├── AGENTS.md                          # Execution & safety guidelines for AI agents
├── README.md                          # Project overview & documentation index
├── CHANGELOG.md                       # Project version history
├── PROJECT_SPEC.md                    # Comprehensive system specifications
├── DATA_DICTIONARY.md                 # Data schema & source catalog
├── SECURITY_AND_DATA_RULES.md         # Read-only data isolation rules
├── .env.example                       # Environment configuration template
├── .gitignore                         # Version control exclusions
├── pyproject.toml                     # Python package metadata & tool configuration
├── requirements.txt                   # Python dependencies specification
│
├── apps/
│   ├── web/                           # Next.js map-first frontend application
│   └── api/                           # FastAPI backend REST & tile services
│
├── src/
│   └── geoslide/                      # Core Geoslide Python package
│       ├── audit/                     # Data discovery & quality validation
│       ├── boundaries/                # District & UT boundary processing
│       ├── terrain/                   # DEM processing & morphometric derivation
│       ├── geology/                   # Lithology & tectonic feature engineering
│       ├── landcover/                 # LULC feature processing
│       ├── landslides/                # Inventory sampling & pseudo-absence generation
│       ├── rainfall/                  # IMD & IMERG rainfall pipelines
│       ├── exposure/                  # Infrastructure & population exposure scoring
│       ├── features/                  # Wall-to-wall grid feature rasterization
│       ├── modelling/                 # Susceptibility ML pipeline & spatial CV
│       ├── risk/                      # Hazard fusion & matrix scoring
│       ├── tiling/                    # Map vector & raster tile generation
│       └── reporting/                 # Automated summary & advisory generators
│
├── configs/                           # Modular YAML system configuration
│   ├── project.yaml
│   ├── data_paths.yaml
│   ├── analysis_grid.yaml
│   ├── feature_config.yaml
│   ├── rainfall_thresholds.yaml
│   ├── risk_matrix.yaml
│   └── ui_config.yaml
│
├── data/                              # Data storage (Git-ignored)
│   ├── raw/                           # Linked or local raw sources
│   ├── interim/                       # Staged uncompressed files
│   ├── processed/                     # COGs, GeoPackages, GeoParquet
│   ├── tiles/                         # PMTiles & vector tile caches
│   └── samples/                       # Demo inspection slices
│
├── models/                            # Model persistence & SHAP artifacts
│   ├── registered/
│   └── metadata/
│
├── outputs/                           # Generated system deliverables
│   ├── maps/
│   ├── reports/                       # Reconciled feature count CSV/MD reports
│   ├── figures/
│   ├── logs/
│   └── demo/
│
├── tests/                             # Automated test suite (52 tests)
│   ├── data/
│   ├── geospatial/
│   ├── modelling/
│   ├── api/
│   └── frontend/
│
└── docs/                              # Comprehensive documentation
    ├── architecture/
    ├── methodology/
    ├── api/
    └── progress/                      # Phase reports & phase_2_final_screenshots archive
```

---

## Data Workspace Isolation Notice

- **Writable Workspace**: `D:\Projects\GeoSlide_JK`
- **Read-Only Source Folder**: `C:\Users\Saurabh Sharma\Downloads\J&K`

*Strict Rule*: Source raw data in the Downloads workspace is immutable. All script operations MUST treat the raw folder as read-only.
