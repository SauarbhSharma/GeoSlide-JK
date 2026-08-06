# GeoSlide-JK 2.0 — V2-3D.1 Scientific Review Report

> **Review Status:** PASSED WITH DOCUMENTED LIMITATIONS  
> **Source Branch:** `geoslide-jk-v2-nh44-static-prioritization-analysis`  
> **Source Commit:** `f1baf6dec0ad96257e154c776083e444626ec20c`  
> **Release Tag Target:** `v2.3c-nh44-static-component-profiles` (`3ee356e76d875a026cf7d8a5ec11aad0c8ae7193`)

---

## Executive Summary

Phase V2-3D.1 has conducted a rigorous scientific review of the static segment prioritization baseline, weight sensitivity analysis, and rank uncertainty decomposition across all 158 authoritative NH-44 corridor segments:

1. **Release Tag & Commit Reconciliation:**
   - Reconciled V2-3C release tag target (`3ee356e`) vs PR merge commit (`cd15dba`). Both are validated ancestors of V2-3D HEAD (`f1baf6d`).
   - 100% immutability confirmed for V2-3A route/segments, V2-3B features, and V2-3C component profiles.

2. **Method Count & Consensus Construction:**
   - Separated **11 numerical score-producing methods** (Methods A-F, H1-H5) from **1 non-numerical analytical flag** (Method G: Epsilon-Dominance Membership).
   - Primary consensus median rank strictly aggregates only the 11 numerical methods. Zero non-numerical flags enter numerical consensus.

3. **Weight Sensitivity & Rank Uncertainty:**
   - All 2,000 weight vectors are 100% unique, bounded within [0.05, 0.60], and sum to 1.000000.
   - 90% consensus rank interval median width is **8.5 positions** (max width = 32.0 positions).
   - Exactly 14 segments achieve top-10% membership probability >= 0.80 under weight perturbation.

4. **Moran's I & Permutation Resolution:**
   - Corrected consensus Moran's I empirical p-value reporting from `p < 0.001` to `p = 0.001` (matching exact 999 permutation resolution: `(0 + 1) / 1000 = 0.001`).

5. **Post-Hoc Landslide Validation:**
   - Consensus percentile rank achieves Spearman rho = 0.412 [95% CI: 0.272, 0.533], p = 0.001 against 648 corridor-intersecting landslide polygons.
   - Landslide data remains 100% validation-only. Zero operational alerts created.
