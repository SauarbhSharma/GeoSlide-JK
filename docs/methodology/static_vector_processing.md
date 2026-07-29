# Static Vector Layer Processing Methodology — GeoSlide-JK Phase 2

## 1. Overview
This document describes the vector processing pipeline used to extract, clean, standardize, and format 10 static GIS vector layers for Jammu and Kashmir UT.

---

## 2. Geometry Cleaning & Standardization
- **Coordinate Reference Systems**:
  - Processing CRS: `EPSG:32643` (UTM 43N meters) for distance/buffer calculations.
  - Delivery CRS: `EPSG:4326` (WGS84 lat/lon) for web GeoJSON/GeoParquet export.
- **3D POLYGONZ Handling**:
  Raw landslide polygon shapefiles containing 3D `POLYGONZ` geometries are converted to 2D `Polygon` geometries for browser map rendering while preserving raw elevation Z attributes in source feature properties.
- **Duplicate Identification**:
  Duplicate feature candidates are logged to audit files (`outputs/reports/phase_2_vector_counts.csv`). No records are silently deleted.

---

## 3. Layer Specifications

| Layer Key | Feature Type | Primary Attributes | Target Output |
| :--- | :--- | :--- | :--- |
| `landslides_points` | Point | Event ID, location name, district | `jk_landslides_points.parquet` |
| `landslides_polygons` | Polygon | Area, perimeter, elevation Z | `jk_landslides_polygons.parquet` |
| `faults` | LineString | Fault name, type, GSI source | `jk_faults.parquet` |
| `thrusts` | LineString | Thrust name, type, GSI source | `jk_thrusts.parquet` |
| `lineaments` | LineString | Length, orientation, structural type | `jk_lineaments.parquet` |
| `lithology` | Polygon | Rock unit, litho-type, formation | `jk_lithology.parquet` |
| `nh44` | LineString | Highway designation, segment ID | `jk_nh44.parquet` |
| `major_roads` | LineString | Road classification, length | `jk_major_roads.parquet` |
| `settlements` | Point | Name, settlement_type (City/Town/Village) | `jk_settlements.parquet` |
| `health_facilities` | Point | Facility name, facility_type (Hospital/Clinic) | `jk_health_facilities.parquet` |

---

## 4. Master GeoPackage Export
All 10 cleaned vector layers are packaged into a single SQLite-backed Master GeoPackage at `data/processed/vectors/jk_static_layers.gpkg` for spatial querying and desktop GIS software integration.
