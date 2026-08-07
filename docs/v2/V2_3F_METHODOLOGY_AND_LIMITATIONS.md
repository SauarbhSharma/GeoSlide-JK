# GeoSlide-JK 2.0 — V2-3F Methodology and Limitations Report

> **Status:** COMPLETE (V2-3F-R4 RELEASE INTEGRITY COMPLETED)  
> **Milestone:** V2-3F NH-44 DHI Robustness, Consensus and Uncertainty Audit (R4 Scientific Evidence Completion)

---

## 1. Independent & Redundant Formulations
- **Independent Formulations (3):** `DHI_A` (Linear product), `DHI_B` (Percentile modulation), `DHI_C` (Upper-tail P90 modulation).
- **Redundant Formulation (1):** `DHI_D` (`DHI_D = sqrt(DHI_B)`), verified strictly monotonic power transformation with 0.0 max absolute residual. Excluded from consensus.

## 2. Dry Control S0 Handling
- S0 (0 mm rainfall control) is mathematically unranked (`DRY_CONTROL_NO_DYNAMIC_DISCRIMINATION`). All 158 segments under S0 are unranked to prevent misleading false quintile assignment.

## 3. Native GPM Grid Cell & Support Location Resolution
- **2 Native 0.1° GPM Grid Cells:** Authoritative spatial intersection proves the NH-44 corridor intersects exactly 2 native 0.1-degree (~11 km) GPM IMERG grid cells: `GPM_NATIVE_33.25N_75.15E` (98 segments) and `GPM_NATIVE_33.25N_75.25E` (60 segments).
- **8 Derived 0.02° Support Nodes:** The 8 locations spaced at 0.02° (~1.8 km) are derived corridor-support interpolation nodes. Segment ranges are strictly non-overlapping and sum to 158 segments.

## 4. Zero-Variance Correlation Semantics
- Uniform corridor-wide scenario screening produces constant DHI vectors within each scenario S1–S5.
- Spearman and Kendall rank correlations across constant vectors are mathematically undefined (`status = UNDEFINED_ZERO_VARIANCE`, `verification_status = VERIFIED_UNDEFINED_ZERO_VARIANCE`).
- Zero spread across constant DHI vectors represents complete within-scenario ties (`NON_DISCRIMINATING_COMPLETE_TIE`), not 100% segment-level discrimination robustness.

## 5. Research Disclaimer
- Results are research scenario screening only. No real-time weather forecasts, operational warning claims, road-closure recommendations, or safe/unsafe route decisions are created.
