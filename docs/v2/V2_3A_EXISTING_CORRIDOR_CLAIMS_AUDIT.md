# GeoSlide-JK 2.0 — Checkpoint V2-3A Existing Corridor Claims Audit

> **Document Version:** 2.3A.0  
> **Status:** Completed Geometry Reconciliation  
> **Target Branch:** `geoslide-jk-v2-product-redesign`

---

## 1. Executive Summary & Reconciliation Objective

During Checkpoint V2-2 and V2-2.6, presentation UI shells displayed static corridor figures for NH-44:
- **Claimed Total Length:** 295 km
- **Claimed 500m Segment Count:** 590 segments

This audit evaluates the geometric provenance of these figures against authoritative project vector sources (`jk_nh44.parquet`, `jk_major_roads.parquet`, and `GeoSlide_JK_Roads_Settlements_Exposure.gpkg`).

---

## 2. Classification of Existing Claims

| Claimed Metric | UI / Doc Location | Claimed Value | Provenance Classification | Reconciled Verified Value | Reason & Correction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Corridor Length** | `apps/web/app/corridor/page.tsx` | 295.0 km | **C. Hard-Coded Presentation Value / D. Placeholder** | **74.88 km** (Pilot) / **301.31 km** (Full UT Extent) | The 295 km figure was an unverified macro estimate for the entire Jammu-to-Srinagar highway. The verified continuous mountain pilot corridor (Udhampur–Ramban–Banihal) is **74.88 km**. |
| **500m Segment Count** | `apps/web/app/corridor/page.tsx` | 590 Segments | **C. Hard-Coded Presentation Value / D. Placeholder** | **150 Segments** (Pilot) / **602 Segments** (Full UT Extent) | Derived directly from $295 \text{ km} / 0.5 \text{ km} = 590$. For the verified 74.88 km pilot corridor, linear referencing produces **150** 500m segments (`NH44-JK-0001` to `NH44-JK-0150`). |
| **Landslide Exposure Screening** | Highway Operations Dashboard | UI Preview Only | **B. Reproducibly Calculated (Geometry Ready)** | **Verified Continuous Geometry** | Geometry foundation is now 100% reproducible and backed by GeoParquet and GeoJSON files; exposure scoring ($LHS$) begins in Checkpoint V2-3B. |

---

## 3. Scientific Verification Decision

1. **REJECT** 295 km / 590 segments as unverified marketing placeholders for the mountain pilot corridor.
2. **ADOPT** **74.88 km** and **150 segments** as the authoritative, geometrically verified metrics for the **Udhampur – Ramban – Banihal NH-44 Mountain Pilot Corridor**.
