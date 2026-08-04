# GeoSlide-JK 2.0 — Checkpoint V2-3A Reset: Rejected Corridor Outputs Audit

> **Document Version:** 2.3A-RESET.1  
> **Status:** Outputs Quarantined & Rejected  
> **Target Branch:** `geoslide-jk-v2-nh44-corrected`  
> **Base Commit:** `222c03264627d057774ff025bca0a33e38708c35`

---

## 1. Executive Summary of Rejection

During Checkpoint V2-3A, a 74.88 km LineString component was extracted and designated as the "NH-44 Pilot Corridor". Independent spatial and topological verification revealed a critical identity mismatch:

> **Rejection Finding:** The extracted 74.88 km line traverses between **Sinthan Pass Sector (`33.57816°N, 75.51750°E`)** in Kishtwar/Anantnag and **Donipawa (`33.71707°N, 75.17438°E`)** in Anantnag. This geographic alignment corresponds to **National Highway 244 (NH-244)**, NOT the Jammu–Srinagar arterial corridor **NH-44** (which connects Udhampur → Ramban → Banihal).

---

## 2. Inventory of Quarantined & Rejected Artifacts

| Artifact Category | File Path | Status | Rejection Reason |
| :--- | :--- | :--- | :--- |
| **Corridor Vector Parquet** | `data/processed/corridors/nh44_pilot_corridor_epsg32643.parquet` | REJECTED | Represents NH-244 Sinthan Pass route |
| **Corridor Web GeoJSON** | `data/processed/corridors/nh44_pilot_corridor_web.geojson` | REJECTED | Represents NH-244 Sinthan Pass route |
| **Segments Parquet (500m)** | `data/processed/corridors/nh44_segments_500m_epsg32643.parquet` | REJECTED | 150 segments generated along NH-244 |
| **Segments Web GeoJSON** | `data/processed/corridors/nh44_segments_500m_web.geojson` | REJECTED | 150 segments generated along NH-244 |
| **Segments Metadata CSV** | `data/processed/corridors/nh44_segments_500m.csv` | REJECTED | 150 segments metadata for NH-244 |
| **Chainage Reference CSV** | `data/processed/corridors/nh44_chainage_reference.csv` | REJECTED | 100m chainage reference along NH-244 |
| **Corridor Source Manifest** | `data/processed/corridors/nh44_corridor_source_manifest.json` | REJECTED | Mislabeled manifest pointing to NH-244 |

---

## 3. Preservation of Raw Data

Original raw vector files (`C:\Users\Saurabh Sharma\Downloads\J&K` and local vector files `data/processed/vectors/jk_nh44.parquet`, `data/processed/vectors/jk_major_roads.parquet`) remain **UNTOUCHED** in read-only / raw storage. No raw source files have been deleted.
