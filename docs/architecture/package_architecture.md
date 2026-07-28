# GeoSlide-JK Package Architecture & Modular Design

---

## Package Layout (`src/geoslide`)

```text
src/geoslide/
├── __init__.py                # Package initialization & version metadata
├── audit/                     # Non-destructive data discovery & quality checks
│   ├── __init__.py
│   └── discovery.py
├── boundaries/                # Boundary extraction & 20-district J&K filtering
├── terrain/                   # DEM processing & terrain attribute calculation
├── geology/                   # Lithology & structural distance engineering
├── landcover/                 # LULC raster feature generation
├── landslides/                # Landslide inventory sampling & pseudo-absence
├── rainfall/                  # IMD & IMERG rainfall parsing & accumulators
├── exposure/                  # Settlement & road exposure scoring
├── features/                  # Wall-to-wall grid feature stack rasterization
├── modelling/                 # ML susceptibility training & spatial CV
├── risk/                      # Hazard matrix fusion & priority calculation
├── tiling/                    # Vector/raster tile creation & map delivery
└── reporting/                 # Automated summary report & advisory generators
```

---

## Configuration Architecture (`configs/`)

All system parameters, thresholds, paths, and matrices are externalized into YAML configurations:

- `project.yaml`: Global metadata, target CRS (`EPSG:32643`), district definitions.
- `data_paths.yaml`: Configurable glob search expressions for raw source discovery.
- `analysis_grid.yaml`: Target processing resolution (100m / 250m fallback), bounding box, nodata value.
- `feature_config.yaml`: Active feature list, scaling methods, and encoding rules.
- `rainfall_thresholds.yaml`: Cumulative rainfall duration windows and percentile trigger boundaries.
- `risk_matrix.yaml`: Susceptibility x Rainfall matrix rules for physical hazard calculation.
- `ui_config.yaml`: UI palette, risk colors, default map viewports, branding parameters.
