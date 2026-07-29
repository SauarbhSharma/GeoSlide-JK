# Phase 3 Gate A — Landslide Label Preparation & Leakage Prevention Plan

## 1. Landslide Inventory Summary
- **Landslide Polygons**: 7,436 features (primary positive labels)
- **Landslide Points**: 2,370 features (validation support)
- Both layers cleaned and clipped to 20-district J&K UT administrative boundary
- Polygons CRS: EPSG:4326 (reprojected to EPSG:32643 for rasterization)
- Points CRS: EPSG:4326

## 2. Polygon-Intersection Positive Grid
- Rasterize 7,436 landslide polygons to 100m master grid
- Cell labeled positive (1) if ANY portion of a landslide polygon intersects it
- Expected positive cell count: ~10,000–15,000 cells (~0.2%–0.3% of J&K UT land area)
- Output raster: data/processed/features/landslide_positive_grid.tif (UInt8, 0/1/255)

## 3. Point-Support Validation Grid
- Rasterize 2,370 landslide points to 100m master grid
- Used for cross-validation with polygon labels
- Output raster: data/processed/features/landslide_point_grid.tif (UInt8, 0/1/255)

## 4. Refined Landslide Event Grouping Hierarchy
To prevent spatial data leakage across train/test splits, landslide events are grouped into spatial clusters according to the following strict priority rules:

1. **Source Identifiers**: Preserve original event IDs (slide_no, gid).
2. **Multi-Geometry Matching**: Match point and polygon representations of the same physical event.
3. **Topological Overlap / Touch**: Group overlapping or touching polygons (intersects(), 	ouches()).
4. **Secondary Spatial Clustering (DBSCAN)**: Apply spatial clustering only as a secondary rule for nearby isolated points/polygons.
   - Sensitivity analysis required during Checkpoint B6 across bandwidths (250m, 500m, 1000m) before finalizing cluster boundaries.

## 5. Provisional Inventory Spatial-Support Mask
- **Name**: provisional_inventory_support_mask (UInt8, 0/1/255)
- **Generation Method**: Convex hull of landslide polygon centroids buffered by 5 km.
- **Methodological Limitations**:
  - This mask represents the **spatial support footprint of recorded inventory data**.
  - It is **NOT** a verified comprehensive field survey coverage map.
  - Cells without mapped landslides inside this mask are **NOT** treated as confirmed negative samples.
  - Pseudo-absence generation remains strictly **deferred to Phase 4** model training.

## 6. Strict Leakage Exclusion Rules
Predictors MUST exclude:
- Latitude / Longitude coordinates
- NLSM susceptibility raster (JammuandKashmir_Susceptibility.tif_NLSM_...) — reserved strictly for validation benchmarks
- Polygon dimensions (shape_area, shape_leng)
- Post-event damage attributes (persons_de, people_aff, infrastruc)
- Target-derived attributes (lert, 	riggering)
