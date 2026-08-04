# GeoSlide-JK 2.0 — Checkpoint V2-3A Reset: Corridor Identity Decision

> **Document Version:** 2.3A-RESET.1  
> **Status:** Corridor Identity Decision Established  
> **Target Branch:** `geoslide-jk-v2-nh44-corrected`  
> **Base Commit:** `222c03264627d057774ff025bca0a33e38708c35`

---

## 1. Authoritative Highway Identity Specification

- **Authoritative Highway Name:** **NH-44 Jammu–Srinagar National Highway**
- **Target Pilot Sector:** **Udhampur → Chenani/Nashri → Ramban → Ramsoo → Banihal**
- **Explicit Exclusions:** Kishtwar, Chatroo, Sinthan Pass, Vailoo, Donipawa, and the Sinthan Pass–Anantnag (NH-244) corridor are **STRICTLY EXCLUDED** from the NH-44 pilot workflow.

---

## 2. Selected Candidate Source

- **Selected Candidate Source:** `data/processed/vectors/jk_major_roads.parquet` (Trunk/Primary features filtered by Udhampur–Ramban–Banihal spatial bounding box: lat `32.85°N` to `33.50°N`, lon `74.85°E` to `75.40°E`).
- **Source Acceptance Gates:**
  1. Follows Udhampur–Ramban–Banihal sequence: **PASS**
  2. Intersects Udhampur and Ramban districts: **PASS**
  3. Excludes Sinthan Pass / Kishtwar / NH-244: **PASS**
  4. Verified spatial alignment with OpenStreetMap trunk highway relations: **PASS**
