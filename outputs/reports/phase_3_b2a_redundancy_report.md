# Phase 3 Checkpoint B2A Correlation & Redundancy Report

## Correlation Summary
Sample correlation evaluation computed across 50,000 valid J&K UT grid cells:

- **Highly Correlated Feature Pairs (|r| > 0.85)**:
  - `elevation` & `tpi`: Strong macro-topographic relationship
  - `slope` & `tri`: High correlation (r = +0.89) — both measure local steepness/roughness.
  - `slope` & `local_relief`: Moderate-to-high correlation (r = +0.76).
- **Trigonometric Orientation Features**:
  - `northness` & `eastness`: Orthogonal (r = +0.02) — zero redundancy.
- **Curvature Measures**:
  - `profile_curvature` & `plan_curvature`: Low correlation (r = +0.14) — complementary flow accelerations.

## Model-Stage Recommendations
- Do NOT auto-remove correlated features at this stage. Preserve both `slope` and `tri` in the static feature stack.
- Evaluate feature importance via VIF and XGBoost gain metrics during Phase 4 model training.
