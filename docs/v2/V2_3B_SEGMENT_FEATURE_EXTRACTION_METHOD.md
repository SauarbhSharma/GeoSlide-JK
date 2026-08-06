# GeoSlide-JK 2.0 — V2-3B Segment Feature Extraction Methodology

> **Document Version:** 2.3B.1  
> **Status:** APPROVED & COMPLETE  
> **Target Branch:** `geoslide-jk-v2-nh44-segment-feature-extraction`  
> **Immutable Baseline Tag:** `v2.3a-nh44-authoritative-baseline`

---

## 1. Objective and Scope

This document specifies the scientific methodology used to extract segment-level static geospatial features for all 158 authoritative NH-44 corridor segments (78,619.370 m total route length).

## 2. Immutable Baseline & Geometry Rules

- **CRS Standard:** Metric calculations, buffers, and distances executed in `EPSG:32643` (UTM Zone 43N). Web-display copies in `EPSG:4326` (WGS 84).
- **Corridor Analysis Units:** 100 m bilateral buffer used as the primary static corridor profile unit; 50 m and 250 m buffers stored for sensitivity analysis.
- **Segment Immutability:** Baseline route geometry, segment IDs, sequence order, and chainages (`0.000 km` to `78.619 km`) accessed strictly read-only.

## 3. Landslide Inventory Leakage Prevention

To prevent data leakage during ML susceptibility modeling:
- Landslide occurrences are stored exclusively in `data/processed/corridor/nh44_segment_landslide_validation_context.parquet` and `outputs/reports/v2_3b_landslide_validation_context.csv`.
- Tagged with `usage_restriction = "VALIDATION_CONTEXT_ONLY_NOT_MODEL_INPUT"`.
