# GeoSlide-JK 2.0 — Final NH-44 Authoritative Baseline Freeze and 500 m Segmentation Report

> **Document Version:** 2.3A-FINAL.2  
> **Gate Status:** APPROVED & COMPLETED (Decision A)  
> **Target Branch:** `geoslide-jk-v2-nh44-final-baseline-segmentation`  
> **Source Commit:** `6fc7ee50e5a67c2d7d40d034ae0e6802e6bf7c21`

---

## 1. Executive Gate Summary

The **NH-44 Udhampur–Banihal Pilot Corridor** has achieved final baseline freeze and 500 m spatial segmentation:

- **Baseline Gate Decision:** `A. AUTHORITATIVE NH-44 BASELINE VERIFIED`
- **Authoritative Route Length:** **78.619 km** (**78,619.370 m**)
- **Southern Terminal:** Udhampur North NH-44 Pilot Start (`32.991498°N, 75.191949°E`) — Km 0.000
- **Northern Terminal:** Banihal NH-44 Pilot End (`33.436961°N, 75.194231°E`) — Km 78.619
- **500 m Segments Created:** **158 segments** (157 x 500.0 m + 1 x 119.37 m residual)
- **Geodesic Invariants:** 100% PASSED across all consecutive anchor pairs.
- **OSM Provenance Wording:** **100% internal member-way match against the locally preserved relation snapshot; external OSM provenance not independently verified.**

---

## 2. Terminal Reference Objects & Keyed Anchors

| Object Key | Role | Lon / Lat | Route Chainage | Status / Verification |
| :--- | :--- | :--- | :--- | :--- |
| `udhampur_place_reference` | Town Centroid Reference | `75.000000°E, 32.930000°N` | Out of Scope | Verified Separate Object |
| `udhampur_pilot_start` | Pilot Highway Start | `75.191949°E, 32.991498°N` | **0.000 km** | Verified Exact Start |
| `chenani_route_projection` | Highway Anchor | `75.140000°E, 33.045000°N` | **15.437 km** | Passed Geodesic Margin (+7.766 km) |
| `ramban_route_projection` | Highway Anchor | `75.247000°E, 33.244000°N` | **43.054 km** | Passed Geodesic Margin (+3.350 km) |
| `ramsoo_route_projection` | Highway Anchor | `75.195000°E, 33.340000°N` | **63.505 km** | Passed Geodesic Margin (+8.733 km) |
| `banihal_place_reference` | Town Centroid Reference | `75.204000°E, 33.438000°N` | Out of Scope | 918.42 m from Highway |
| `banihal_highway_projection` | Highway Anchor | `75.194231°E, 33.436961°N` | **78.619 km** | Matches Endpoint <= 0.01 m |
| `banihal_pilot_end` | Pilot Highway Endpoint | `75.194231°E, 33.436961°N` | **78.619 km** | Verified Exact End |
| `qazigund_place_reference` | Geographic Reference | `75.161000°E, 33.593000°N` | Out of Scope | Out-of-Scope (No Pilot Chainage) |
| `verinag_place_reference` | Geographic Reference | `75.250000°E, 33.543000°N` | Out of Scope | Out-of-Scope (No Pilot Chainage) |

---

## 3. Canonical Manifest & Single-Source Artifacts

All subsequent modeling, raster extraction, risk scoring, and web visualizations MUST consume exclusively from these canonical files:

- **Canonical Route GeoJSON:** [`data/audit/nh44_authoritative_pilot_final.geojson`](file:///D:/Projects/GeoSlide_JK/data/audit/nh44_authoritative_pilot_final.geojson)
- **Canonical Route Parquet:** [`data/audit/nh44_authoritative_pilot_final.parquet`](file:///D:/Projects/GeoSlide_JK/data/audit/nh44_authoritative_pilot_final.parquet)
- **Canonical 500 m Segments GeoJSON:** [`data/processed/corridor/nh44_segments_500m_final.geojson`](file:///D:/Projects/GeoSlide_JK/data/processed/corridor/nh44_segments_500m_final.geojson)
- **Canonical 500 m Segments Parquet:** [`data/processed/corridor/nh44_segments_500m_final.parquet`](file:///D:/Projects/GeoSlide_JK/data/processed/corridor/nh44_segments_500m_final.parquet)
- **Canonical Manifest:** [`data/audit/nh44_authoritative_manifest_final.json`](file:///D:/Projects/GeoSlide_JK/data/audit/nh44_authoritative_manifest_final.json)

---

## 4. 500 m Spatial Segmentation Results

- **Total Segment Count:** 158
- **Nominal Segment Length:** 500.0 metres (Segments `NH44_SEG_001` through `NH44_SEG_157`)
- **Terminal Segment Length:** 119.37 metres (`NH44_SEG_158`)
- **Continuity & Topology:** Zero gaps, zero overlaps, strictly monotonic chainage sequence.
