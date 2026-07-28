# GeoSlide-JK
## Professional Full-Project Implementation Plan for Google Antigravity

### Project title
**Landslide Risk Prediction (J&K)**

### Objective
Use geospatial, geological, land-cover, landslide-inventory and rainfall data to identify landslide-prone zones across the Union Territory of Jammu and Kashmir, estimate changing rainfall-triggered hazard, assess exposed settlements and infrastructure, and present location-based research advisories through a professional map-first web application.

---

# 1. Product Definition

GeoSlide-JK must be implemented as a **full J&K geospatial decision-support platform**, not as a single prediction notebook.

The product must contain four linked analytical components:

1. **Static susceptibility**
   - Answers: Where are landslides more likely based on terrain, geology, land cover, structures and human disturbance?
2. **Rainfall trigger**
   - Answers: Are recent rainfall conditions unusually high?
3. **Current hazard and response priority**
   - Combines susceptibility and rainfall trigger.
   - Adds settlements, roads, population and health facilities for impact prioritisation.
4. **User-facing advisory interface**
   - Shows risk class, confidence, reasons, rainfall, exposed assets and safety guidance for a selected location.

The first operational version must be described as:

> An explainable landslide susceptibility and rainfall-triggered risk-nowcasting research prototype for Jammu and Kashmir.

It must not claim to be an official government warning system or a guaranteed landslide forecast.

---

# 2. Full J&K Coverage Requirement

The web interface must open with the complete current Union Territory of Jammu and Kashmir visible.

The processing workflow must:

1. Read all available district polygons.
2. print and review district names.
3. exclude Ladakh districts such as Leh and Kargil when they are present in an older 22-district boundary.
4. create:
   - current J&K UT boundary;
   - district boundary layer;
   - tehsil/subdistrict layer;
   - full analysis grid;
   - data-availability/confidence mask.
5. show all supported J&K areas in the UI.
6. label unsupported or incomplete areas as **Insufficient Data**, not Low Risk.

The NH-44 corridor may be highlighted as a focus corridor, but the main map must remain statewide.

---

# 3. Design Direction

## 3.1 Design inspiration

The interface should combine these proven patterns without copying logos or proprietary designs:

- **NASA LHASA:** separation of static susceptibility and current rainfall-triggered hazard.
- **USGS Landslide Inventory and Susceptibility Map:** clear map legend, inventory overlay and location-focused interpretation.
- **Copernicus Emergency Management Service:** map-first situational awareness, summary statistics and downloadable map products.
- **GDACS:** recency, severity colour coding, active-alert feed and concise event cards.
- **Windy-style interaction:** timeline playback, weather-layer switching and strong map focus.

## 3.2 Visual identity

Suggested product name:

**GeoSlide J&K**

Suggested tagline:

**Terrain Intelligence and Rainfall-Triggered Landslide Risk**

Visual style:

- professional geospatial command-centre aesthetic;
- dark navy/charcoal header;
- light map canvas by default;
- optional dark mode;
- compact cards;
- rounded but not playful components;
- subtle elevation/topographic background;
- clear hierarchy and generous spacing;
- accessible typography.

Suggested typography:

- UI: Inter or Source Sans 3
- numeric/KPI display: Inter
- maps: system sans-serif

Risk palette:

| Class | Colour guidance |
|---|---|
| Low | green |
| Moderate | yellow/amber |
| High | orange |
| Very High | red |
| Critical | dark magenta/deep red |
| Insufficient Data | grey hatch |

Do not rely only on colour. Show labels, icons and patterns.

---

# 4. User Roles and Main Experiences

## 4.1 Resident mode

Optimised for simple location checking.

Functions:

- search village, town, district or coordinates;
- use current location when permission is granted;
- see current risk, confidence and data freshness;
- see recent rainfall;
- see nearby high-risk slopes, roads and facilities;
- read short safety precautions;
- share or print a location advisory.

## 4.2 Analyst/administrator mode

Optimised for map exploration and decision support.

Functions:

- turn layers on/off;
- inspect district and tehsil summaries;
- compare static susceptibility with current hazard;
- analyse rainfall windows;
- view exposed population and road length;
- download map images, CSV summaries and GeoJSON;
- inspect model performance and feature importance;
- filter by risk class, district and data confidence.

---

# 5. Required Application Pages

## Page 1 — Statewide Command Centre

Default landing screen.

Required content:

- full J&K map;
- current hazard layer;
- current data time and age;
- statewide status;
- number of High/Very High/Critical grid cells or zones;
- districts with elevated hazard;
- exposed settlements;
- road kilometres under elevated priority;
- alert/advisory feed;
- quick search;
- layer switcher;
- current-vs-static toggle.

Layout:

- top application bar;
- left collapsible navigation;
- centre map;
- right situational summary panel;
- bottom timeline/rainfall playback control.

## Page 2 — Interactive Risk Explorer

Required map layers:

- current hazard;
- static susceptibility;
- rainfall trigger;
- data confidence;
- elevation;
- slope;
- aspect/hillshade;
- land cover;
- lithology;
- faults;
- thrusts;
- lineaments;
- historical landslides;
- district and tehsil boundaries;
- major roads and NH-44;
- settlements;
- hospitals;
- population.

Map interaction:

- zoom, pan and reset;
- location search;
- layer opacity;
- legend;
- map click;
- coordinate display;
- measurement;
- basemap selection;
- fullscreen;
- export map as PNG/PDF.

Map-click response:

- latitude and longitude;
- district and tehsil;
- static susceptibility probability/class;
- current rainfall trigger;
- current hazard;
- response priority;
- confidence;
- 1 h, 6 h, 24 h, 72 h rainfall;
- dominant factors;
- nearest road, settlement and hospital;
- data timestamp;
- research disclaimer.

## Page 3 — District Intelligence

For each of the 20 J&K districts, display:

- district map;
- current risk distribution;
- static susceptibility distribution;
- number of exposed settlements;
- estimated exposed population when coverage is valid;
- major road length under elevated risk;
- current rainfall statistics;
- top contributing factors;
- data confidence;
- downloadable district report.

## Page 4 — Rainfall Monitor

Required components:

- IMERG rainfall map;
- time slider;
- 30-minute, 1 h, 3 h, 6 h, 12 h, 24 h, 48 h and 72 h accumulation;
- IMD historical percentiles;
- station-vs-satellite comparison;
- stale/missing interval indicators;
- demo playback mode for the available July 2026 sample;
- latest-data mode when automated ingestion is implemented.

## Page 5 — Location Risk Check

Input:

- place search;
- latitude/longitude;
- click on map;
- browser geolocation.

Output:

- large risk badge;
- confidence badge;
- simple explanation;
- rainfall summary;
- static terrain summary;
- nearby exposed features;
- safety guidance;
- printable/shareable advisory.

## Page 6 — Model and Data Transparency

Display:

- datasets used;
- data coverage;
- preprocessing steps;
- model version;
- spatial cross-validation results;
- precision-recall and calibration;
- SHAP global importance;
- local reason codes;
- uncertainty;
- limitations;
- research-only disclaimer.

## Page 7 — Data and System Status

Display:

- source file status;
- ingestion status;
- last successful run;
- missing files;
- rainfall freshness;
- raster/vector product versions;
- model version;
- API status;
- log summary.

---

# 6. Recommended Technical Architecture

## 6.1 Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- MapLibre GL JS
- Recharts or Apache ECharts
- TanStack Query
- Zustand for map/UI state
- responsive desktop/tablet/mobile layout

## 6.2 Backend/API

- Python 3.11
- FastAPI
- Pydantic
- Uvicorn
- SQLAlchemy
- PostgreSQL/PostGIS for production
- SQLite/GeoPackage/GeoParquet for early local development
- Redis only when background jobs or caching are needed

## 6.3 Geospatial processing

- GeoPandas
- Shapely
- Pyogrio
- Rasterio
- Rioxarray
- Xarray
- NetCDF4
- GDAL
- WhiteboxTools or GRASS GIS for hydrological terrain features

## 6.4 Machine learning

- Scikit-learn
- XGBoost
- LightGBM optional
- SHAP
- MLflow for experiments
- Joblib for local model persistence

## 6.5 Web map delivery

Do not send raw 2–3 GB data to the browser.

Use:

- Cloud-Optimized GeoTIFFs for raster layers;
- TiTiler for raster tiles;
- PMTiles/vector tiles for roads, boundaries and landslides;
- simplified GeoJSON only for small layers;
- GeoParquet for processed analytical tables;
- cached district summaries in JSON.

## 6.6 Development and deployment

- Docker Compose
- `.env` configuration
- Pytest
- Ruff
- Black
- ESLint
- Prettier
- Git with raw data excluded
- local deployment first;
- cloud deployment only after data/licence review.

---

# 7. Professional Repository Structure

```text
GeoSlide_JK/
├── AGENTS.md
├── README.md
├── PROJECT_SPEC.md
├── DATA_DICTIONARY.md
├── SECURITY_AND_DATA_RULES.md
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── apps/
│   ├── web/                         # Next.js frontend
│   └── api/                         # FastAPI application
│
├── src/
│   └── geoslide/
│       ├── audit/
│       ├── boundaries/
│       ├── terrain/
│       ├── geology/
│       ├── landcover/
│       ├── landslides/
│       ├── rainfall/
│       ├── exposure/
│       ├── features/
│       ├── modelling/
│       ├── risk/
│       ├── tiling/
│       └── reporting/
│
├── configs/
│   ├── project.yaml
│   ├── data_paths.yaml
│   ├── analysis_grid.yaml
│   ├── feature_config.yaml
│   ├── rainfall_thresholds.yaml
│   ├── risk_matrix.yaml
│   └── ui_config.yaml
│
├── data/
│   ├── raw/                         # Immutable or linked raw data
│   ├── interim/
│   ├── processed/
│   ├── tiles/
│   └── samples/
│
├── models/
│   ├── experiments/
│   ├── registered/
│   └── metadata/
│
├── outputs/
│   ├── maps/
│   ├── reports/
│   ├── figures/
│   ├── logs/
│   └── demo/
│
├── notebooks/
│   ├── 01_data_validation.ipynb
│   ├── 02_inventory_analysis.ipynb
│   ├── 03_feature_analysis.ipynb
│   └── 04_model_evaluation.ipynb
│
├── scripts/
│   ├── audit_data.py
│   ├── build_boundary.py
│   ├── build_static_features.py
│   ├── train_susceptibility.py
│   ├── process_rainfall.py
│   ├── build_current_risk.py
│   ├── build_tiles.py
│   └── run_demo_pipeline.py
│
├── tests/
│   ├── data/
│   ├── geospatial/
│   ├── modelling/
│   ├── api/
│   └── frontend/
│
└── docs/
    ├── architecture/
    ├── methodology/
    ├── api/
    ├── ui/
    └── progress/
```

---

# 8. How to Give the Data Folder to Antigravity

## Recommended setup: two local folders in one Antigravity Project

Do not upload the 2.98 GB raw dataset to Antigravity or GitHub.

Create:

```text
D:\Projects\GeoSlide_JK\
```

for code and generated outputs.

Keep the existing audited dataset folder, for example:

```text
C:\Users\<YOUR_USER_NAME>\Downloads\J&K\
```

as the raw-data source.

In Antigravity:

1. Select **Project**.
2. Choose **New Project**.
3. Add folder:
   ```text
   D:\Projects\GeoSlide_JK\
   ```
4. Add a second folder:
   ```text
   C:\Users\<YOUR_USER_NAME>\Downloads\J&K\
   ```
5. Name the project:
   ```text
   GeoSlide-JK
   ```
6. use project-specific permissions.
7. require review/confirmation before terminal commands.
8. do not enable unrestricted destructive actions.
9. tell Antigravity that the dataset folder is strictly read-only.
10. allow writes only inside the project folder.

## Backup rule

Before allowing an agent to work:

- keep a complete backup of the raw-data folder;
- do not select the whole Downloads drive as a workspace;
- do not grant the agent access to unrelated personal folders;
- do not permit deletion, moving or renaming in the raw-data workspace.

## Path configuration

Create `.env`:

```env
GEOSLIDE_PROJECT_ROOT=D:/Projects/GeoSlide_JK
GEOSLIDE_RAW_DATA_ROOT=C:/Users/<YOUR_USER_NAME>/Downloads/J&K
GEOSLIDE_INTERIM_ROOT=D:/Projects/GeoSlide_JK/data/interim
GEOSLIDE_PROCESSED_ROOT=D:/Projects/GeoSlide_JK/data/processed
GEOSLIDE_OUTPUT_ROOT=D:/Projects/GeoSlide_JK/outputs
```

Create `configs/data_paths.yaml`:

```yaml
raw_root: "${GEOSLIDE_RAW_DATA_ROOT}"

boundaries:
  district_search: "**/*DISTRICT_BDY*.shp"
  tehsil_search: "**/*TALUK*BDY*.shp"

dem:
  full_jk_search: "**/copernicus_glo30/full_jk/**/*.tif"

landslides:
  points_search:
    - "**/landslide_point_STATE_JK.shp"
    - "**/landslide_point_STATE_JK.geojson"
  polygons_search:
    - "**/landslide_polygon_STATE_JK.shp"
    - "**/landslide_polygon_STATE_JK.geojson"

geology:
  lithology_search:
    - "**/lithology*gcs*JK.shp"
    - "**/lithology*gcs*JK.geojson"

tectonics:
  fault_search: "**/fault*JK.shp"
  thrust_search: "**/thrust*JK.shp"
  lineament_search: "**/lineament*JK.shp"
  active_fault_search: "**/active_fault*JK.shp"
  earthquake_search: "**/earthquake*JK.shp"

lulc:
  worldcover_search: "**/ESA_WorldCover_10m_2021*.tif"

rainfall:
  imd_search: "**/RF25_ind*_rfp25.nc"
  imerg_search: "**/*.nc4"
  wris_search: "**/Rainfall_*.xlsx"

exposure:
  osm_gpkg_search: "**/*Roads_Settlements_Exposure*.gpkg"
  population_search: "**/GHS_POP*.tif"
```

The code must resolve glob patterns and produce a clear error when zero or multiple ambiguous matches are found.

---

# 9. Data Processing Workflow

## Phase A — Audit and boundary correction

Tasks:

1. scan all files;
2. detect duplicates;
3. validate CRS and geometry;
4. create a data catalogue;
5. list district names;
6. remove/exclude Leh and Kargil from the current J&K UT boundary if present;
7. repair invalid geometry;
8. create district, tehsil and dissolved J&K boundaries;
9. generate a coverage mask for every major dataset.

Deliverables:

```text
data/processed/boundaries/jk_ut_boundary.gpkg
data/processed/boundaries/jk_districts.gpkg
data/processed/boundaries/jk_tehsils.gpkg
data/processed/quality/data_coverage_mask.tif
outputs/reports/data_quality_report.md
```

Acceptance criteria:

- current J&K boundary contains 20 districts;
- no invalid district geometry;
- all source layers have documented coverage;
- missing coverage is not interpreted as low risk.

## Phase B — Analysis grid

Recommended statewide display grid:

- 100 m where computationally practical;
- configurable 100–250 m fallback;
- projected processing CRS: EPSG:32643;
- web/output CRS: EPSG:4326.

Create one master grid with:

- identical resolution;
- origin;
- extent;
- width/height;
- NoData;
- CRS.

## Phase C — Terrain pipeline

1. mosaic all four full-J&K DEM tiles;
2. clip to current J&K;
3. remove obvious voids;
4. create:
   - elevation;
   - slope;
   - aspect;
   - northness;
   - eastness;
   - curvature;
   - TRI;
   - TPI;
   - local relief;
   - flow accumulation;
   - drainage;
   - distance to drainage;
   - drainage density;
   - TWI;
   - hillshade.
4. save outputs as COGs.

Never calculate flow products separately on individual DEM tiles.

## Phase D — Geological and land-cover pipeline

Create:

- lithology class;
- broad engineering-geology class;
- distance to fault;
- distance to thrust;
- distance to active fault;
- distance to lineament;
- lineament density;
- fault density;
- earthquake density;
- ESA WorldCover dominant class;
- proportional tree, cropland, built-up, bare, grassland and snow coverage;
- distance to roads;
- road density;
- distance to NH-44;
- distance to settlements.

## Phase E — Landslide labels

1. use polygons as the primary landslide-area labels;
2. use points for catalogue validation and additional coverage;
3. identify exact and near duplicates;
4. create stable group IDs;
5. retain audit logs;
6. create positive grid samples;
7. generate multiple pseudo-absence sets inside a reasonable inventory-coverage footprint;
8. prevent samples from the same landslide being split across train and test;
9. do not use raw coordinates as predictors;
10. do not use post-event attributes or the existing NLSM map as training predictors.

## Phase F — Static susceptibility models

Implement:

1. Frequency Ratio or Information Value baseline;
2. Logistic Regression;
3. Random Forest;
4. XGBoost.

Validation:

- spatial block cross-validation;
- district-group holdout;
- group all cells from one landslide together;
- no random split as the primary reported result.

Metrics:

- ROC-AUC;
- PR-AUC;
- recall;
- precision;
- F1;
- balanced accuracy;
- false-negative rate;
- Brier score;
- calibration;
- landslides captured in top 10% and 20% susceptibility area.

Outputs:

- calibrated susceptibility probability;
- five susceptibility classes;
- model uncertainty;
- data confidence;
- SHAP explanations;
- model metadata.

## Phase G — Rainfall pipeline

Historical IMD:

- daily rainfall;
- 3-day, 7-day, 15-day and 30-day accumulation;
- monthly/seasonal means;
- 90th/95th/99th percentiles;
- anomalies;
- consecutive wet days;
- antecedent rainfall index.

IMERG:

- parse all half-hourly files;
- validate time continuity;
- convert rate to half-hour amount when required;
- create 1 h, 3 h, 6 h, 12 h, 24 h, 48 h, 72 h and 7-day rainfall;
- create data freshness;
- create quality flags;
- support demo playback.

WRIS:

- parse station metadata and rainfall workbooks separately;
- compare daily totals with IMERG;
- calculate bias, RMSE and correlation.

Because event dates are unavailable or not sufficiently complete, use a transparent provisional rainfall-trigger classification based on local percentiles. Label it as a research trigger index.

## Phase H — Hazard and response-priority fusion

Keep physical hazard and exposure priority separate.

Recommended logic:

1. classify static susceptibility:
   - Very Low;
   - Low;
   - Moderate;
   - High;
   - Very High.
2. classify rainfall trigger:
   - Normal;
   - Elevated;
   - High;
   - Extreme.
3. combine them through a configurable risk matrix.
4. calculate exposure separately.
5. generate response priority from:
   - current hazard;
   - population;
   - settlement;
   - roads;
   - critical facilities.
6. calculate confidence from:
   - model uncertainty;
   - data coverage;
   - rainfall quality;
   - rainfall freshness.

Store all rules in YAML. Do not hide weights in source code.

Output fields:

```text
hazard_score
hazard_class
response_priority
confidence_class
static_susceptibility
rainfall_trigger
rainfall_data_age
dominant_factors
valid_from
valid_until
model_version
data_version
```

---

# 10. API Specification

Required endpoints:

```text
GET  /api/v1/health
GET  /api/v1/status
GET  /api/v1/layers
GET  /api/v1/districts
GET  /api/v1/districts/{district_id}
GET  /api/v1/risk/current
GET  /api/v1/risk/point?lat=&lon=
GET  /api/v1/risk/district/{district_id}
GET  /api/v1/rainfall/current
GET  /api/v1/rainfall/timeseries?lat=&lon=
GET  /api/v1/alerts
GET  /api/v1/model/metrics
GET  /api/v1/model/features
GET  /api/v1/data/coverage
GET  /api/v1/reports/district/{district_id}
```

Tile endpoints:

```text
GET /tiles/raster/{layer}/{z}/{x}/{y}.png
GET /tiles/vector/{layer}/{z}/{x}/{y}.pbf
```

Point-risk response must include values, class, confidence, dominant factors, nearby exposure and timestamps.

---

# 11. Testing and Quality Requirements

## Data tests

- source exists;
- CRS exists;
- bounds overlap current J&K;
- valid coordinate range;
- valid geometry;
- expected fields;
- valid raster classes;
- rainfall units detected;
- timestamps continuous;
- missing intervals logged;
- duplicate records logged.

## Model tests

- no target leakage;
- no spatial leakage;
- group IDs respected;
- all features wall-to-wall;
- model calibrated;
- reproducible random seeds;
- metrics stable across pseudo-absence samples;
- uncertainty generated.

## UI tests

- full J&K loads;
- all 20 districts selectable;
- map layer opacity works;
- location search works;
- click response is correct;
- mobile/tablet layout works;
- keyboard navigation;
- accessible contrast;
- colour-independent risk labels;
- stale rainfall clearly shown;
- no-data clearly different from low risk.

## Performance targets

- initial shell visible quickly;
- statewide map uses tiles, not large raw GeoJSON;
- heavy computation never runs in the browser;
- expensive statistics cached;
- map remains responsive while layers change;
- district cards load independently.

---

# 12. Development Phases and Deliverables

## Phase 0 — Safety and scaffold

Deliver:

- repository structure;
- AGENTS.md;
- environment files;
- read-only data rules;
- data path discovery;
- dependency setup;
- Docker configuration;
- basic tests.

Do not process or train yet.

## Phase 1 — Full J&K UI shell and data-status demo

Deliver:

- polished statewide map interface;
- navigation and design system;
- full J&K boundary;
- district selector;
- mock/current KPI cards;
- layer controls;
- empty risk legend;
- data status page;
- responsive layout;
- basic FastAPI health/status endpoints.

This is the first demonstration milestone.

## Phase 2 — Static map products

Deliver:

- DEM mosaic;
- elevation;
- slope;
- hillshade;
- landslide inventory;
- faults;
- roads;
- settlements;
- tile services;
- map-click metadata.

## Phase 3 — Feature engineering

Deliver all static feature rasters and the model-ready feature table.

## Phase 4 — Susceptibility model

Deliver calibrated model, spatial validation, uncertainty, SHAP and statewide susceptibility COG.

## Phase 5 — Rainfall engine

Deliver historical climatology, IMERG playback, accumulation products and rainfall trigger.

## Phase 6 — Current hazard and exposure

Deliver hazard matrix, exposure calculations, response priority and district summaries.

## Phase 7 — Production UI

Replace mock values with API data, complete all pages, downloadable reports and location advisories.

## Phase 8 — QA, documentation and deployment

Deliver:

- automated tests;
- model card;
- data card;
- user manual;
- API documentation;
- methodology report;
- Docker deployment;
- demo video;
- final presentation assets.

---

# 13. Antigravity Execution Rules

Antigravity must follow these rules:

1. Never modify, rename, move or delete anything in the raw-data folder.
2. Never write generated files to the raw-data folder.
3. Never run recursive delete commands.
4. Never process all files without first showing the discovery result.
5. Never assume the first matching file is correct when multiple candidates exist.
6. Never use the incomplete NLSM raster as a model feature or target.
7. Never claim live data when using the July 2026 demo sample.
8. Never call missing data Low Risk.
9. Never use a random train/test split as the primary model validation.
10. Never claim official warnings.
11. Create logs and manifests for every generated output.
12. Stop at the end of each phase and provide:
    - files created;
    - commands run;
    - tests passed/failed;
    - screenshots;
    - risks;
    - next-step plan.

---

# 14. Master Prompt to Give Antigravity

```text
You are the lead product architect, geospatial engineer, machine-learning
engineer and senior frontend developer for the project described below.

PROJECT
GeoSlide-JK: Landslide Risk Prediction and Rainfall-Triggered Risk
Decision-Support Platform for the Union Territory of Jammu and Kashmir.

OBJECTIVE
Build a professional, full-J&K, map-first web application that combines
static landslide susceptibility, recent rainfall trigger conditions,
settlement/road/population exposure and explainable risk advisories.

WORKSPACES
1. Writable project workspace:
   D:\Projects\GeoSlide_JK
2. Read-only source-data workspace:
   <INSERT THE EXACT PATH OF THE AUDITED J&K DATA FOLDER>

NON-NEGOTIABLE DATA RULES
- Treat the complete source-data workspace as immutable.
- Never delete, rename, move, overwrite or edit source files.
- Write only inside the writable project workspace.
- Do not copy all raw files unnecessarily.
- Do not upload raw IMD or restricted data to external services.
- Resolve source files through configurable glob patterns.
- Before using a source, record path, CRS, bounds, schema, size and checksum.
- Stop and report ambiguity when multiple conflicting source files match.

PRODUCT REQUIREMENTS
- The primary interface must display full current J&K UT coverage.
- Review the district list and exclude Leh and Kargil if the boundary is the
  former 22-district J&K structure.
- Support all 20 current J&K districts.
- Highlight NH-44 as a focus corridor without limiting statewide coverage.
- Label missing/incomplete data as Insufficient Data, never Low Risk.
- Present the system as a research prototype, not an official warning system.

DESIGN REQUIREMENTS
Build a world-class geospatial interface inspired by the interaction patterns
of NASA LHASA, USGS landslide maps, Copernicus EMS, GDACS and Windy:
- full-screen interactive map;
- strong layer controls and legends;
- district and state KPI cards;
- current status and data freshness;
- timeline/rainfall playback;
- alert/advisory feed;
- location search and coordinate lookup;
- map-click risk explanation;
- light and dark mode;
- responsive desktop/tablet/mobile design;
- accessible risk colours plus text/icons/patterns.

TECH STACK
Frontend:
- Next.js, React, TypeScript
- Tailwind CSS and shadcn/ui
- MapLibre GL JS
- Recharts or Apache ECharts
- TanStack Query

Backend:
- Python 3.11 and FastAPI
- Pydantic
- GeoPandas, Shapely, Pyogrio
- Rasterio, Rioxarray, Xarray, NetCDF4
- Scikit-learn, XGBoost and SHAP
- PostgreSQL/PostGIS for production
- GeoPackage/GeoParquet/COG for local development
- TiTiler for raster tiles
- PMTiles or vector tiles for vector data

IMPLEMENTATION PRINCIPLES
- Use EPSG:4326 for web delivery.
- Use EPSG:32643 for distance, area and terrain processing.
- Build a configurable 100 m analysis grid, with a 250 m fallback.
- Use Cloud-Optimized GeoTIFFs for raster products.
- Do not send large raw rasters or GeoJSON files to the browser.
- Use tiled map delivery and cached JSON summaries.
- Keep hazard separate from exposure/response priority.
- Keep all thresholds and risk matrices in YAML.
- Produce uncertainty and data-confidence outputs.
- Use spatial block cross-validation for susceptibility modelling.
- Use landslide polygons as primary labels and points as catalogue support.
- Use transparent rainfall-percentile trigger rules until dated events exist.
- Make every result reproducible and versioned.

REQUIRED PAGES
1. Statewide Command Centre
2. Interactive Risk Explorer
3. District Intelligence
4. Rainfall Monitor
5. Location Risk Check
6. Model and Data Transparency
7. Data and System Status

PHASED EXECUTION
Do not attempt the entire project in one unreviewed run.

PHASE 0
- Create the repository structure.
- Create AGENTS.md, README.md, PROJECT_SPEC.md,
  SECURITY_AND_DATA_RULES.md, .env.example, configs and tests.
- Create a data-discovery script that only reads metadata.
- Create a project plan and architecture diagram.
- Do not process data.

PHASE 1
- Discover the source data.
- Prepare the current 20-district J&K boundary.
- Create the polished full-J&K UI shell.
- Add district navigation, layer controls, design system, KPI placeholders,
  risk legend, status page and responsive layout.
- Implement FastAPI health, status, district and layer endpoints.
- Use clearly labelled mock values only where processed outputs do not exist.

PHASE 2
- Mosaic and clip DEM.
- generate elevation, slope, aspect and hillshade.
- clean and tile landslide, fault, road, settlement and boundary layers.
- connect these layers to the UI.

PHASE 3
- Build the static feature stack.

PHASE 4
- Train and validate the static susceptibility models using spatial CV.
- Create susceptibility, uncertainty and explanation products.

PHASE 5
- Build IMD historical climatology and IMERG demo-playback trigger products.

PHASE 6
- Fuse susceptibility and rainfall through a configurable matrix.
- calculate exposure and response priority.
- generate district summaries and location advisories.

PHASE 7
- Complete all live API integrations, reports and final UI.

PHASE 8
- Complete tests, documentation, Docker deployment and final demo.

REPORTING RULE
At the end of every phase:
1. stop;
2. show the task plan;
3. list every file created or changed;
4. show test results;
5. provide screenshots;
6. describe unresolved issues;
7. request approval before proceeding.

START NOW WITH PHASE 0 AND PHASE 1 ONLY.
Do not train a model and do not modify raw data.
```

---

# 15. First Demonstration Acceptance Criteria

The first UI milestone is complete only when:

- the full current J&K UT boundary is visible;
- all 20 districts can be selected;
- the interface has a professional map-first layout;
- navigation works;
- layer controls work;
- the risk legend is visible;
- map-click produces a structured placeholder/details panel;
- the data-status page lists collected datasets;
- DEM, landslide and rainfall status are shown;
- data freshness is visible;
- mock values are labelled Demo;
- no official-warning language is used;
- the frontend and API start through documented commands;
- screenshots and a progress report are produced.
