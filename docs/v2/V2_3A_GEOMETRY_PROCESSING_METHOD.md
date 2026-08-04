# GeoSlide-JK 2.0 — Checkpoint V2-3A Geometry Processing Method

> **Document Version:** 2.3A.0  
> **Status:** Completed Methodology  
> **Target Branch:** `geoslide-jk-v2-product-redesign`

---

## 1. Reprojection & Distance CRS

All geometric calculations, line merges, and linear referencing operations are performed strictly in the project metric projected coordinate system:
- **Processing CRS:** `EPSG:32643` (UTM Zone 43N / WGS 84)
- **Web Delivery CRS:** `EPSG:4326` (WGS 84 Ellipsoidal)

---

## 2. Geometry Cleaning Pipeline

1. **Filtering & Deduplication:** Filter out non-line geometries (Points, Polygons, empty geometries) and line fragments $<10$ m.
2. **Topological Merge:** Apply `shapely.ops.unary_union` followed by `shapely.ops.linemerge` to assemble individual highway way lines into continuous LineStrings.
3. **Direction Standardization:** Orient the LineString to flow deterministically from South (Udhampur, start chainage 0.0 m) to North (Banihal, end chainage 74,875.83 m).
4. **Export Artifacts:**
   - `data/processed/corridors/nh44_pilot_corridor_epsg32643.parquet`
   - `data/processed/corridors/nh44_pilot_corridor_web.geojson`
   - `data/processed/corridors/nh44_corridor_source_manifest.json`
