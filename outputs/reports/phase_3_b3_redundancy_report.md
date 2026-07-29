# Phase 3 Checkpoint B3 — Redundancy & Correlation Report

## Compositional & Spatial Correlation Analysis

- **WorldCover Class Fractions**: Fractional land cover sum equals 1.0 across valid land. For linear models, drop one fraction (e.g. `moss_lichen_fraction`) to prevent exact compositional multicollinearity.
- **Distance & Log-Distance Pairings**: `distance_to_X_m` and `log1p_distance_to_X` exhibit expected strong non-linear monotone correlation. Both retained in raw feature stack; model-stage VIF selection deferred to Phase 4.
