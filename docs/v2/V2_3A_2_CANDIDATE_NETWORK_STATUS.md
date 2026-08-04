# GeoSlide-JK 2.0 — Checkpoint V2-3A.2: Candidate Network Status Report

> **Document Version:** 2.3A.2-STATUS.1  
> **Status:** Candidate Network Reclassified  
> **Target Branch:** `geoslide-jk-v2-nh44-mainline`  
> **Base Commit:** `cee05441a1eeeb1e7e436ff326305a415ffef8b5`

---

## 1. Output Reclassification

The pre-existing 372-edge vector dataset (`data/audit/nh44_candidate_source_edges.parquet`) is officially reclassified as:

> **`"Candidate NH-44 Source-Edge Network"`**

It is **NOT** and must **NEVER** be referred to as:
- final NH-44 alignment;
- corridor centreline;
- approved pilot route;
- authoritative alignment.

---

## 2. Rationale for Reclassification

1. **Connected Component != Single Route:** A single connected component in graph theory represents a network of interconnected edges. It can contain parallel carriageways, roundabouts, interchange loops, and feeder branches while remaining a single graph component.
2. **Visible Branches & Loops Remaining:** Human visual inspection and graph topology analysis confirm that the candidate network contains alternate bypasses, dual-carriageway loops, and minor feeder spurs across Udhampur and Ramban.
3. **112.52 km Total Length:** The total 112.52 km length represents the cumulative sum of all candidate network edges, including parallel carriageways and bypasses. The actual single-pass pilot mainline length between Udhampur and Banihal terminals will be extracted during this checkpoint.
