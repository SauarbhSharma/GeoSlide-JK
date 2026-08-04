# GeoSlide-JK 2.0 — Checkpoint V2-3A Corridor API Specification

> **Document Version:** 2.3A.0  
> **Status:** Implemented FastAPI Specification  
> **Target Branch:** `geoslide-jk-v2-product-redesign`

---

## Endpoint Definitions

### 1. GET `/api/v1/corridors`
Returns a list of all available highway corridors.
- **Response:** JSON list of corridor metadata summaries.

### 2. GET `/api/v1/corridors/nh44`
Returns metadata and GeoJSON geometry for the NH-44 pilot corridor.
- **Response Fields:** `corridor_id`, `corridor_name`, `origin_name`, `destination_name`, `total_length_km`, `segment_count`, `geometry_version`, `data_quality_status`, `geojson`.

### 3. GET `/api/v1/corridors/nh44/segments`
Returns all 150 500m segments for the NH-44 corridor.
- **Query Parameters:** `district` (optional filter), `limit` (default 200), `offset` (default 0).
- **Response Fields:** List of segment metadata (`segment_id`, `sequence_number`, `start_chainage_km`, `end_chainage_km`, `segment_length_m`, `district_primary`, `data_quality_status`).

### 4. GET `/api/v1/corridors/nh44/segments/{segment_id}`
Returns details and geometry for a specific 500m segment.
- **Response Fields:** Full segment metadata, GeoJSON line geometry, and future scoring fields marked as `"Not yet calculated (Checkpoint V2-3B)"`.
