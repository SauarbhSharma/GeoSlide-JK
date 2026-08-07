# GeoSlide-JK 2.0 — V2-3F-R3 Scientific Integrity & Reproducibility Report

> **Status:** PASSED  
> **Corrective Release Milestone:** V2-3F-R3 NH-44 DHI Scientific Integrity, Native-Grid and Reproducibility Correction

---

## Key Scientific Corrections
1. **Native GPM Resolution Disambiguation:** 2 native 0.1° GPM cells (`GPM_NATIVE_33.25N_75.15E` with 98 segments, `GPM_NATIVE_33.25N_75.25E` with 60 segments). The 8 locations are 0.02° corridor-support interpolation nodes.
2. **Zero-Variance Correlation Semantics:** Constant DHI vectors return null/blank spearman_rho and status `UNDEFINED_ZERO_VARIANCE`.
3. **Scenario Provenance:** All scenario definitions reference existing tracked configuration `configs/rainfall_thresholds.yaml`.
4. **Reproducibility Path Independence:** `scripts/run_v2_3f_r3_reproducibility.py` uses 100% repository-relative paths.
