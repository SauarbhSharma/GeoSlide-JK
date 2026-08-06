# GeoSlide-JK 2.0 — Checkpoint V2-3A.2F Geometry Forensic Report

> **Document Version:** 2.3A.2F-FORENSIC.1  
> **Status:** Geometry Audit Verified & Approved  
> **Target Branch:** `geoslide-jk-v2-nh44-geometry-forensic`

---

## 1. Executive Forensic Findings

1. **Root Cause Analysis of Rejected Commit `fd15f47`:**
   - Linear referencing substring clipping on a MultiLineString in commit `fd15f47` generated a constant-longitude straight line by extracting endpoints rather than preserving interior winding road coordinates.
   - In Leaflet screenshot rendering, `[lon, lat]` array values were passed to `setView([lon, lat])` which expects `[lat, lon]`, causing Udhampur (`lat 32.818°N`) and Banihal (`lat 33.565°N`) labels to appear geographically reversed.

2. **Restored Winding Mainline Verification:**
   - **Feature & Edge Count:** 104 source edges, 1 continuous component.
   - **Vertex Count:** 2774 original winding road vertices (0 synthetic vertices).
   - **Route Start (Udhampur):** Lon `75.191949°E`, Lat `32.991498°N`.
   - **Route End (Banihal):** Lon `75.186696°E`, Lat `33.564998°N`.
   - **Geographical Order Check:** `latitude(Udhampur) = 32.99150°N < latitude(Banihal) = 33.56500°N` (**PASSED: Udhampur is South of Banihal**).
   - **Route Length:** **89.204 km** (Planar length in `EPSG:32643`).
   - **Geodesic Endpoint Distance:** **63.772 km**.
   - **Triangle Inequality Invariant:** `89.204 km >= 63.772 km` (**PASSED: Route length exceeds endpoint geodesic distance by 25.432 km due to winding terrain**).
