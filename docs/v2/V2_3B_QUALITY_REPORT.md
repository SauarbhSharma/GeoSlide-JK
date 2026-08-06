# GeoSlide-JK 2.0 — V2-3B Data Quality Report

> **Quality Gate Status:** PASSED (100% QUALITY VALIDATED)

---

## 1. Quality Control Rules & Assertions

1. **Segment Count Integrity:** Exactly 158 records in primary feature table.
2. **Unique Segment IDs:** 158 unique IDs matching authoritative V2-3A baseline.
3. **Chainage Monotonicity:** Zero chainage inversions; start/end chainages strictly increasing.
4. **Class Fraction Sums:** Susceptibility, land-cover, and structure fractions sum to `1.0` within `1e-4` tolerance.
5. **Structure Length Reconciliation:** Open road + tunnel + bridge length equals total segment length within `0.01 m`.
6. **Landslide Isolation:** Landslide counts excluded from primary feature table and restricted to validation context.
7. **No Dynamic Hazard / Alert Columns:** Zero dynamic rainfall or alert columns present.
