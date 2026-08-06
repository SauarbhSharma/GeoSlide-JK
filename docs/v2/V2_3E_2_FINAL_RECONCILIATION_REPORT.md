# GeoSlide-JK 2.0 — V2-3E.2 Final Rainfall Accounting and Formula Reconciliation Report

> **Reconciliation Status:** PASSED WITH RAINFALL DATA LIMITATIONS  
> **Source Branch:** `geoslide-jk-v2-nh44-rainfall-dynamic-hazard-scientific-review`  
> **Target Branch:** `geoslide-jk-v2-nh44-rainfall-dynamic-hazard-final-reconciliation`  
> **Source Commit:** `f3bd3bc26350455c119a33056c6640bb3910bfdc`

---

## Final Reconciliation Highlights
1. **Reconciled Source Entities:** 6 source entities (4 logical observational archives, 1 climatology product, 1 scenario set) yield 3 dataset-level quality records (HIGH: 2/3, SCENARIO_ONLY: 1/3).
2. **Explicit S0-S5 Definitions:** S0 (Dry Control), S1-S4 (Climatology-Derived Reference), S5 (Synthetic Stress Test).
3. **Corrected DHI Correlation Matrix:**
   - All-Formulation Minimum Spearman: **0.965** (DHI_A vs DHI_C)
   - All-Formulation Maximum Spearman: **1.000** (DHI_B vs DHI_D)
   - Independent-Formulation Minimum Spearman: **0.965** (DHI_A vs DHI_C)
   - Independent-Formulation Maximum Spearman: **0.982** (DHI_A vs DHI_B)
4. **Proof of DHI_D Redundancy:** DHI_D = sqrt(DHI_B) = (DHI_B)^0.5 is a strictly monotonic power transformation. Spearman rho(DHI_B, DHI_D) = 1.000. DHI_D is classified as **MONOTONICALLY_REDUNDANT**. Independent formulation count = **3**.
5. **Corrected Spatial-Support Wording:** Refers to **"8 distinct native 0.1-degree rainfall grid cells intersecting the authoritative corridor"** rather than claiming statistical independence.
6. **Static-Dynamic Collapse Finding:** When rainfall is spatially uniform across the corridor, DHI ranking collapses to static susceptibility ranking (Spearman rho = 1.000).
7. **Validation Statement:** "NO TEMPORAL EVENT VALIDATION WAS POSSIBLE. The dynamic indicators are scenario-based research profiles and are not calibrated event-prediction outputs."
