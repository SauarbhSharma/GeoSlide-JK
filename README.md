# GeoSlide-JK: Landslide Risk Prediction & Decision Support System

> **Terrain Intelligence and Rainfall-Triggered Landslide Risk Decision-Support Platform for the Union Territory of Jammu & Kashmir**

---

## Overview

**GeoSlide-JK** is a full-state geospatial decision-support application for Jammu and Kashmir (J&K). It integrates multi-source geospatial data—including digital elevation models (DEM), geological lithology, tectonic fault/thrust structures, land cover (LULC), historical landslide inventories, population distribution, and near-real-time satellite/gridded rainfall (NASA IMERG & IMD)—to deliver explainable landslide susceptibility and rainfall-triggered hazard advisories.

The system is designed as an explainable research prototype providing statewide coverage across all 20 districts of Jammu & Kashmir.

---

## Key Architecture & Components

1. **Static Susceptibility Engine**: Machine learning model (XGBoost / Random Forest) trained on spatial terrain, geological, structural, and land-cover features using spatial block cross-validation.
2. **Rainfall Trigger Engine**: Antecedent and short-term rainfall accumulator utilizing IMD historical climatology and GPM IMERG near-real-time data.
3. **Hazard & Response Priority Fusion**: Matrix-based fusion combining static susceptibility with dynamic rainfall triggers, overlaid against exposed population, settlements, critical facilities, and major transportation corridors (including NH-44).
4. **Interactive Map-First UI**: Modern web interface (Next.js, Tailwind CSS, MapLibre GL JS) offering statewide views, district intelligence cards, map-click explanations, and downloadable advisories.

---

## Directory Structure

```text
GeoSlide_JK/
├── AGENTS.md                          # Execution & safety guidelines for AI agents
├── README.md                          # Project overview & documentation index
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
│   ├── reports/
│   ├── figures/
│   ├── logs/
│   └── demo/
│
├── tests/                             # Automated test suite
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
    └── progress/
```

---

## Data Workspace Isolation Notice

- **Writable Workspace**: `D:\Projects\GeoSlide_JK`
- **Read-Only Source Folder**: `C:\Users\Saurabh Sharma\Downloads\J&K`

*Strict Rule*: Source raw data in the Downloads workspace is immutable. All script operations MUST treat the raw folder as read-only.

---

## Phase 0 Status

Phase 0 foundation complete:
- Repository layout established.
- Core specifications & safety rules documented.
- Modular YAML configuration templates deployed.
- Safe read-only data-discovery engine created (`src/geoslide/audit/discovery.py`).
- Safety & path validation automated unit tests implemented (`tests/`).
