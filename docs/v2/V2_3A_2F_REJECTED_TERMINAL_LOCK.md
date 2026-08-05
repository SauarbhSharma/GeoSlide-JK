# GeoSlide-JK 2.0 — Checkpoint V2-3A.2F Rejected Terminal-Lock Audit

> **Document Version:** 2.3A.2F-REJECTED.1  
> **Status:** Rejection Logged & Isolated  
> **Rejected Commit:** `fd15f47953284bc5c4b1a4369e900aaef93514a3`  
> **Target Branch:** `geoslide-jk-v2-nh44-geometry-forensic`

---

## 1. Reason for Rejection

1. **Straight-Line Artifact:** The previous linear-referencing substring clipping operation produced a constant-longitude straight vertical LineString instead of retaining original winding road coordinates.
2. **Reversed Terminal Labels:** Udhampur and Banihal terminal labels were geographically reversed in screenshot generation scripts due to latitude/longitude axis ordering inversion.
3. **Impossible Route Length:** Reported clipped length (54.978 km) was mathematically smaller than the geodesic endpoint distance (~59.6 km), violating the fundamental triangle inequality.
4. **Data Isolation:** All files generated in commit `fd15f47` (`nh44_locked_pilot_*`, `v2-3a-2t` screenshots) are formally marked as **REJECTED** and isolated. They will NOT be used for API, frontend delivery, or downstream 500m corridor chainage segmentation.

---

## 2. Restored Baseline

Checkpoints are resumed strictly from **Commit `0759d6e151cde7e0ee6cfe569e297910fd8864de`**, which contains the verified 104-edge, 89.204 km continuous winding NH-44 mainline.
