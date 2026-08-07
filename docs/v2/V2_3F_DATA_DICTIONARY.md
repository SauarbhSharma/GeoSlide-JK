# GeoSlide-JK 2.0 — V2-3F-R4 Data Dictionary

## 1. Dynamic Hazard & Robustness Fields (`outputs/reports/v2_3f_scenario_segment_robustness.csv`)

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

## 2. V2-3F-R4 Canonical Evidence Tables

| Table File Path | Description | Key Fields |
|---|---|---|
| `outputs/reports/v2_3f_r4_native_gpm_cell_evidence.csv` | 2 Native 0.1° GPM cells metadata | `native_cell_id`, `raster_crs`, `raster_row_index`, `raster_column_index`, `center_latitude_deg`, `center_longitude_deg`, `west_bound_deg`, `east_bound_deg`, `south_bound_deg`, `north_bound_deg`, `longitude_spacing_deg`, `latitude_spacing_deg`, `coordinate_convention`, `segment_count`, `assigned_segment_range`, `segment_ids_sha256` (64-char), `mapping_source`, `computation_path`, `verification_status` |
| `outputs/reports/v2_3f_r4_derived_support_location_evidence.csv` | 8 Derived 0.02° support nodes metadata | `support_node_id`, `latitude_deg`, `longitude_deg`, `assigned_segments_count`, `assigned_segment_range`, `segment_ids_sha256` (64-char), `node_type`, `mapping_source`, `computation_path`, `verification_status` |
| `outputs/reports/v2_3f_r4_segment_native_cell_mapping.csv` | Segment to native cell 1-to-1 mapping | `segment_id`, `native_gpm_cell_id`, `assignment_method`, `verification_status` |
| `outputs/reports/v2_3f_r4_segment_support_location_mapping.csv` | Segment to support node 1-to-1 mapping | `segment_id`, `support_node_id`, `assignment_method`, `verification_status` |
| `outputs/reports/v2_3f_r4_scenario_pairwise_spearman.csv` | 30 Scenario rank correlation rows | `scenario_id`, `pair`, `raw_column_x`, `raw_column_y`, `sample_size`, `spearman_rho`, `spearman_p_value`, `kendall_tau`, `status`, `reason`, `var_x`, `var_y`, `unique_count_x`, `unique_count_y`, `missing_value_handling`, `tie_handling`, `verification_status` |
| `outputs/reports/v2_3f_r4_uncertainty_reconciliation.csv` | Uncertainty & Degeneracy results | `scenario_id`, `valid_rows`, `unique_dhi_a`..`unique_dhi_d`, `var_dhi_a`..`var_dhi_d`, `mean_percentile_range`, `median_percentile_range`, `max_percentile_range`, `mean_iqr`, `median_iqr`, `max_iqr`, `threshold_stable_count`, `moderate_count`, `sensitive_count`, `informative_row_count`, `degenerate_tied_row_count`, `informative_for_segment_discrimination`, `degeneracy_status`, `scientifically_informative_stability`, `percentile_method`, `rounding_stage`, `verification_status` |
| `outputs/reports/v2_3f_r4_dhi_d_redundancy_audit.csv` | DHI_D exact redundancy audit | `audit_item`, `formula_dhi_b`, `formula_dhi_d`, `sample_size`, `max_absolute_residual`, `relationship_status`, `consensus_exclusion_action`, `verification_status` |
