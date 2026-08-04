# GeoSlide-JK 2.0 — Checkpoint V2-3A Reset: Road Candidate Source Audit

> **Document Version:** 2.3A-RESET.1  
> **Status:** Candidate Audit Completed  
> **Target Branch:** `geoslide-jk-v2-nh44-corrected`  
> **Base Commit:** `222c03264627d057774ff025bca0a33e38708c35`

---

## 1. Executive Summary

A full audit of 2,984 candidate road features across local vector layers (`data/processed/vectors/jk_nh44.parquet` and `data/processed/vectors/jk_major_roads.parquet`) was conducted to evaluate highway identity against geographic anchor points:

- **NH-44 Anchor Towns:** Udhampur (`32.930°N, 75.000°E`), Ramban (`33.244°N, 75.247°E`), Banihal (`33.438°N, 75.204°E`).
- **NH-244 Exclusion Towns:** Sinthan Pass (`33.578°N, 75.518°E`), Kishtwar (`33.315°N, 75.766°E`).

---

## 2. Source Audit Results

| Source Layer | Audited Candidates | Accepted NH-44 Features | Rejected NH-244 Features | Primary Highway Identity |
| :--- | :--- | :--- | :--- | :--- |
| `jk_nh44.parquet` | 82 | 4 | 1 (Component 1) | Mixed: Contains NH-244 Sinthan Pass stretch (Component 1) alongside NH-44 fragments |
| `jk_major_roads.parquet` | 2,902 (Trunk/Primary) | 434 | 43 | Primary network for NH-44 Jammu–Srinagar trunk highway |

---

## 3. Cause of Initial Identity Mismatch

The initial Checkpoint V2-3A script performed an unconstrained topological `linemerge` on all features in `jk_nh44.parquet`. Component 1 of `jk_nh44.parquet` (length 74.88 km) covers lat `33.578°N` to `33.717°N` across Sinthan Pass and Donipawa/Anantnag. Because `jk_nh44.parquet` contained mislabeled features from the NH-244 Sinthan Pass feeder road, selecting the longest component produced the NH-244 route instead of the true NH-44 Udhampur–Ramban–Banihal corridor.
