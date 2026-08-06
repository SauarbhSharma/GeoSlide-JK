# GeoSlide-JK 2.0 — V2-3B Baseline Verification Report

> **Gate Status:** PASSED (100% IMMUTABLE MATCH)  
> **Source Commit:** `67329a212f2fe02c88ae82f27333917f9ba79395`  
> **Release Tag:** `v2.3a-nh44-authoritative-baseline`

---

## 1. Baseline Invariant Audit

| Metric | Expected Value | Observed Value | Status |
| :--- | :--- | :--- | :--- |
| **Route GeoJSON SHA256** | `7141c209c578f8e8f19bc13b85409eeb220b709703c62691fac732594b2e3564` | `7141c209c578f8e8f19bc13b85409eeb220b709703c62691fac732594b2e3564` | **PASS** |
| **Geometry WKB SHA256** | `49edeba25fad803f6be27cb66d75867848662276811e5b85c66e2765bbeb6e40` | `49edeba25fad803f6be27cb66d75867848662276811e5b85c66e2765bbeb6e40` | **PASS** |
| **Segment Raw SHA256** | `775998e07bbb332d352093961ce2d47b7ca3488179885abceca1df843a50f172` | `775998e07bbb332d352093961ce2d47b7ca3488179885abceca1df843a50f172` | **PASS** |
| **Normalized Segment Semantic SHA256** | `de25ecf1f4f80450df0f1179e7c18ed26f7dbee6688bbe6c5a4448168105c5bf` | `de25ecf1f4f80450df0f1179e7c18ed26f7dbee6688bbe6c5a4448168105c5bf` | **PASS** |
| **Authoritative Route Length** | `78,619.370 m` | `78619.370 m` | **PASS** |
| **Total Segments** | `158` | `158` | **PASS** |
| **Nominal 500 m Segments** | `157` | `157` | **PASS** |
| **Residual Segment Length** | `119.370 m` | `119.370 m` | **PASS** |
| **Maximum Gap / Overlap** | `0.000 m` | `0.000 m / 0.000 m` | **PASS** |
| **Unique Segment IDs** | `158` | `158` | **PASS** |
| **Monotonic Chainage Order** | `True` | `True` | **PASS** |

---

## 2. Verification Conclusion

The checked-out V2-3A authoritative baseline has been verified 100% continuous, valid, and immutable. Proceeding to Phase 3 Data-Source Readiness Audit.
