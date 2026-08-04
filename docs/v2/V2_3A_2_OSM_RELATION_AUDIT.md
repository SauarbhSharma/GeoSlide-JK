# GeoSlide-JK 2.0 — Checkpoint V2-3A.2: OSM Relation Audit Report

> **Document Version:** 2.3A.2-RELATION.1  
> **Status:** Relation Audit Complete  
> **Target Branch:** `geoslide-jk-v2-nh44-mainline`  
> **Base Commit:** `cee05441a1eeeb1e7e436ff326305a415ffef8b5`

---

## 1. Executive Relation Verdict

> **VERDICT:** **NH-44 relation not independently established.**
> 
> While individual OSM way features retain `ref=NH 44` / `ref=NH-44` / `ref=NH 1A` and `highway=trunk` tags, the complete ordered OSM relation container was not preserved as a single sequential sequence in the local vector parquet files. Path extraction relies on metric graph-topology extraction over accepted source edges.

---

## 2. Relation Attributes

- **OSM Relation ID:** `OSM_REL_NH44_JK`
- **Relation Name:** NH 44 Jammu-Srinagar Highway
- **Relation Ref:** NH 44
- **Network Tag:** `IN:NH`
- **Route Tag:** `road`
- **Operator Tag:** `National Highways Authority of India (NHAI)`
- **Member Order Preservation:** Unordered in local vector layers
- **Audit Findings:** Constrained graph path extraction (Method B) is used to establish the single ordered mainline topology.
