# Phase 2 Feature Count Reconciliation Report

This report provides complete, transparent reconciliation between raw input GIS datasets and final processed vector outputs.

## Reconciliation Summary Table

| Layer Name | Raw Count | Null Geom | Invalid Geom | Outside J&K | Duplicate Cand | Repair Count | Clipped Count | Final Count | Reconciliation Reason |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **landslide points** | 2379 | 0 | 0 | 9 | 0 | 0 | 9 | **2370** | 9 points located outside 20-district J&K UT administrative boundary clipped. |
| **landslide polygons** | 7456 | 0 | 12 | 20 | 0 | 12 | 20 | **7436** | 20 polygons outside J&K UT clipped; 12 self-intersecting geometries repaired via buffer(0). |
| **lineaments** | 855 | 0 | 0 | 81 | 0 | 0 | 81 | **774** | 81 lineaments extending beyond 20-district J&K UT boundary trimmed/clipped. |
| **lithology units** | 4229 | 0 | 45 | 153 | 0 | 45 | 153 | **4076** | 153 outer units clipped to J&K UT boundary; 45 invalid topology geometries repaired via buffer(0). |
| **faults** | 3 | 0 | 0 | 0 | 0 | 0 | 0 | **3** | 3 major tectonic fault traces inside J&K fully retained. |
| **active faults** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** | Option B Selected: Active faults preserved and merged into processed faults dataset with fault_type = 'active'. |
| **thrusts** | 14 | 0 | 0 | 0 | 0 | 0 | 0 | **14** | 14 tectonic thrust lines inside J&K fully retained. |
| **major roads** | 4762 | 0 | 0 | 0 | 0 | 0 | 0 | **4762** | 4,762 major road segments retained within J&K UT boundary. |
| **settlements** | 5060 | 0 | 0 | 0 | 0 | 0 | 0 | **5060** | 5,060 settlement point locations retained within J&K UT boundary. |
| **health facilities** | 1079 | 0 | 0 | 202 | 0 | 0 | 202 | **877** | 877 medical facilities filtered & retained; 202 outside 20-district J&K UT boundary removed. |


## Layer Reconciliation Notes & Active Fault Decision

### Active Fault Resolution (Option B Selected)
- **Decision**: Option B — Active faults are merged into the processed fault layer with `fault_type = 'active'`.
- **Rationale**: Preserves all active fault line geometries as a distinct attribute for Phase 3 distance-to-active-fault feature extraction without cluttering layer selection.

### Lithology Readiness (Non-Blocking UI Limitation)
- **File**: `data/processed/vectors/jk_lithology.parquet`
- **Status**: Fully processed (4,076 units, EPSG:32643 / WGS84, clipped to J&K UT, source identifiers retained).
- **Phase 3 Readiness**: 100% ready for spatial rasterization. UI connection remains pending as a non-blocking limitation.
