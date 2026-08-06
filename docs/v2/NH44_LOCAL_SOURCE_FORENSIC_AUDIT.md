# GeoSlide-JK 2.0 — NH-44 Local Source Forensic Audit Report

> **Document Version:** 2.3A-FORENSIC.1  
> **Status:** Local Attribute Schema Audit Complete  
> **Target Branch:** `geoslide-jk-v2-nh44-source-audit`  
> **Base Commit:** `222c03264627d057774ff025bca0a33e38708c35`

---

## 1. Executive Summary

A forensic attribute-level schema audit was conducted on local vector datasets:
- `data/processed/vectors/jk_nh44.parquet`
- `data/processed/vectors/jk_major_roads.parquet`

---

## 2. Dataset Schema & Tag Findings

1. **`jk_nh44.parquet` Findings:**
   - Total Rows: 82 features
   - Primary Columns: `name`, `highway`, `operator`, `tunnel`, `bridge`, `surface`
   - **Missing Explicit Reference Attribute:** Neither dataset retains an explicit `ref` column (e.g. `ref=NH 44` or `ref=NH-44`).
   - Feature `name` Values: Contains generic OSM road names (`"Jammu-Srinagar Highway"`, `"NH44"`, etc.) alongside Sinthan Pass feeder segments.

2. **`jk_major_roads.parquet` Findings:**
   - Total Rows: 4,762 features
   - Primary Columns: `highway`, `name`, `operator`, `surface`, `tunnel`
   - `highway` Value Counts: `trunk` (245), `primary` (482), `secondary` (1,230), `tertiary` (2,805)
   - Explicit `ref` column is absent in the processed parquet schema.
