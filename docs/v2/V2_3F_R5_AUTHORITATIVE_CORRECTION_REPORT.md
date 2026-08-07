# GeoSlide-JK 2.0 — V2-3F-R5 Authoritative Grid & Provenance Correction Report

> **Status:** PASSED  
> **Corrective Release Milestone:** V2-3F-R5 NH-44 DHI Authoritative Grid, Provenance and Reproducibility Correction

---

## Key Scientific & Evidence Corrections
1. **Authoritative 2D Spatial GPM Grid Intersection:** 11 native 2D 0.1° GPM cells across 5 latitude rows (33.0°N to 33.5°N) mapped to all 158 segments with 100% Path A/B agreement.
2. **Unproven 8 Support Locations:** Marked `ROLE_UNPROVEN` and excluded from scientific calculations.
3. **Scenario Derivation Provenance:** Corrected S4 and S5 to repository-defined hypothetical stress test classifications.
4. **Zero-Variance Correlation Semantics:** Constant DHI vectors return null/blank spearman_rho and status `UNDEFINED_ZERO_VARIANCE` (`VERIFIED_UNDEFINED_ZERO_VARIANCE`).
5. **DHI_D Redundancy Exclusion:** `DHI_D = sqrt(DHI_B)` proved with 0.0 machine-precision residual in full precision and 4.29e-5 on 4-decimal rounded values (`ROUNDED_SERIALIZATION_CONSISTENT`).
6. **Documentation and UI Alignment:** `README.md`, `CHANGELOG.md`, `V2_3F_METHODOLOGY_AND_LIMITATIONS.md`, `V2_3F_DATA_DICTIONARY.md`, `V2_3F_COMPLETION_REPORT.md`, and Next.js UI (`apps/web/app/corridor/page.tsx`) updated.
