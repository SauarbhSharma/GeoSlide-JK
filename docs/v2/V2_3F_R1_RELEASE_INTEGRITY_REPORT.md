# GeoSlide-JK 2.0 — V2-3F-R1 Post-Release Integrity Reconciliation Report

> **Status:** PASSED  
> **Corrective Release Milestone:** V2-3F-R1 NH-44 DHI Post-Release Integrity Reconciliation

---

## Key Integrity Reconciliations
1. **Native Cell Distribution:** Reconciled native-cell count vector: `[18, 20, 20, 20, 20, 20, 20, 20]` (Sum = 158 segments, Min = 18, Median = 20.0, Max = 20).
2. **Complete 6-Pair Spearman Matrices:** Published complete formulation correlation matrices for S1, S2, S3, S4, S5 individually and pooled (36 total pairs).
3. **S4 Scenario Provenance:** Documented S4 `SATURATED_ANTECEDENT` as a compound reference scenario combining P95 antecedent moisture (95 mm API7) with 120 mm 24h rainfall.
4. **IQR Quantile Specification:** Documented exact `numpy.percentile` 3-value IQR calculation formula (`IQR = 0.5 * Range`).
