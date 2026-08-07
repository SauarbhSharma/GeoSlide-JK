# GeoSlide-JK 2.0 — V2-3F Data Dictionary

| Field Name | Type | Description |
|---|---|---|
| segment_id | string | Authoritative NH-44 segment identifier (e.g. NH44_SEG_001) |
| scenario_id | string | Research scenario code (S0-S5) |
| native_cell_id | string | Intersecting 0.1-degree native GPM grid cell ID |
| rank_dhi_a | float | Tie-aware relative rank for DHI_A (1-158) |
| rank_dhi_b | float | Tie-aware relative rank for DHI_B (1-158) |
| rank_dhi_c | float | Tie-aware relative rank for DHI_C (1-158) |
| rank_dhi_d_audit | float | Audit-only rank for redundant DHI_D |
| consensus_median_percentile | float | Equal-formulation median percentile across DHI_A, DHI_B, DHI_C |
| percentile_range | float | Spread between max and min independent percentile |
| stability_category | string | STABLE_CONSENSUS, MODERATE_AGREEMENT, FORMULATION_SENSITIVE, or DRY_CONTROL_UNRANKED |
