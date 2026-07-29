# Phase 3 Checkpoint B3 — Data Leakage & Feature Isolation Audit Report

## Strict Feature Isolation Mandate

- **NLSM Susceptibility Raster**: Tagged `validation_only=true`. Reserved strictly for comparative benchmarking; excluded from training feature stack.
- **Latitude & Longitude Coordinates**: Tagged `excluded=true`. Excluded from model features to prevent spatial memorization.
- **Landslide Inventory Polygons & Points**: Tagged `label_data=true`. Reserved strictly for target label preparation in Phase 4.
- **Hospitals, Healthcare Facilities & Settlement Proximity**: Tagged `exposure_only=true`. Excluded from static landslide susceptibility predictors; strictly reserved for consequence and risk prioritisation.
- **Raw D8 Flow Direction**: Tagged `diagnostic_only=true`. Excluded from direct continuous numeric model input.
