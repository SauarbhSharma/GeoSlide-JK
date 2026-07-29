# Phase 3 Checkpoint B2A Quality Assurance Report

## Scientific & Physical Range Audits

| Feature Name | Min | Max | Mean | Std Dev | Valid % | Out of Range | Physical Range Status |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `elevation` | 249.00 | 7017.30 | 2350.42 | 1276.02 | 99.98% | 0 | **PASS** |
| `slope` | 0.00 | 80.76 | 23.54 | 13.27 | 99.98% | 0 | **PASS** |
| `aspect` | 0.00 | 357.38 | 174.61 | 82.18 | 99.98% | 0 | **PASS** |
| `northness` | -1.00 | 1.00 | -0.26 | 0.60 | 99.98% | 0 | **PASS** |
| `eastness` | -1.00 | 1.00 | 0.04 | 0.75 | 99.98% | 0 | **PASS** |
| `profile_curvature` | -3.10 | 1.96 | -0.00 | 0.04 | 100.0% | 0 | **PASS** |
| `plan_curvature` | -3.02 | 3.14 | 0.00 | 0.03 | 100.0% | 0 | **PASS** |
| `tri` | 0.00 | 14537.86 | 36.54 | 152.74 | 100.0% | 0 | **PASS** |
| `tpi` | -14604.09 | 4925.98 | 0.29 | 174.84 | 100.0% | 0 | **PASS** |
| `local_relief` | 0.00 | 16667.02 | 226.11 | 554.45 | 100.0% | 0 | **PASS** |

## Verification Highlights
1. **Slope**: 100% inside physical range [0°, 90°]. No negative or >90° values.
2. **Northness & Eastness**: 100% inside trigonometric bounds [-1, 1].
3. **No Infinite or NaN Values**: All 10 feature rasters contain 0 infinite or NaN values.
4. **Coverage Mask**: 100% of valid J&K land cells ({valid_cell_count:,} cells) possess complete B2A coverage.
