# GeoSlide-JK 2.0 — V2-3F Methodology and Limitations Report

> **Status:** COMPLETE  
> **Milestone:** V2-3F NH-44 DHI Robustness, Consensus and Uncertainty Audit

---

## 1. Independent & Redundant Formulations
- **Independent Formulations (3):** `DHI_A` (Linear product), `DHI_B` (Percentile modulation), `DHI_C` (Upper-tail P90 modulation).
- **Redundant Formulation (1):** `DHI_D` (sqrt modulation = `DHI_B^0.5`), verified strictly monotonic power transformation (Spearman rho = 1.000). Excluded from consensus.

## 2. Dry Control S0 Handling
- S0 (0 mm rainfall control) is mathematically unranked (`DRY_CONTROL_NO_DYNAMIC_DISCRIMINATION`). All 158 segments under S0 are unranked to prevent misleading false quintile assignment.

## 3. Native Rainfall Cell Limitation
- Rainfall forcing is extracted from **8 distinct native 0.1-degree (~11 km) GPM IMERG grid cells** (median 19.5 segments/cell). Segment-level outputs inherit 0.1° support and do not represent independent 500m rainfall measurements.
