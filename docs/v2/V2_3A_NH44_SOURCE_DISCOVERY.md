# GeoSlide-JK 2.0 — Checkpoint V2-3A NH-44 Source Discovery Report

> **Document Version:** 2.3A.0  
> **Status:** Completed Discovery  
> **Target Branch:** `geoslide-jk-v2-product-redesign`

---

## 1. Candidate Source Inventory

| Candidate ID | File Path | File Size | CRS | Feature Count | Total Length | Selection Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Candidate 1** | `data/processed/vectors/jk_nh44.parquet` | 47,215 bytes | EPSG:4326 | 82 rows (81 LineString, 1 Point) | 67.85 km | **Primary Authoritative Source** — Filtered high-precision corridor line dataset. |
| **Candidate 2** | `data/processed/vectors/jk_major_roads.parquet` | 3.49 MB | EPSG:4326 | 4,762 rows (2,902 trunk/primary) | 3,140.11 km | **Secondary Reference** — Used to bridge minor network gaps near junctions. |
| **Candidate 3** | `raw_downloads/GeoSlide_JK_Roads_Settlements_Exposure.gpkg` | 179.66 MB | EPSG:4326 | 280,589 rows | 9,663.47 km | **Read-Only Raw Archive** — Base database. |

---

## 2. Selection Decision

Candidate 1 (`jk_nh44.parquet`) supplemented by topological linemerge with Candidate 2 (`jk_major_roads.parquet`) was selected to build the continuous **Udhampur – Ramban – Banihal NH-44 Mountain Pilot Corridor**.
