# Phase 3 Checkpoint B4 — Landslide Inventory Label Preparation & Sampling Domain Report

---

## 1. Executive Summary

This report documents **Phase 3 Checkpoint B4: Landslide Inventory Label Preparation and Pseudo-Absence Sampling** for **GeoSlide-JK**.

- **Landslide Presence Cells (Positive)**: **4,587 cells** (45.87 km², 0.10% of valid land)
- **Verified Pseudo-Absence Cells (Negative)**: **3,596,475 cells** (35964.75 km², 77.86% of valid land)
- **Excluded Buffer Zone (0 - 200m)**: **33,383 cells** (0.72%)
- **Excluded Low-Slope Areas (<= 5.0°)**: **654,606 cells** (14.17%)
- **Excluded Incomplete Data Cells**: **330,160 cells** (7.15%)
- **Prevalence Ratio (Positive / (Positive + Negative))**: **0.0013** (0.13%)

---

## 2. Methodological Rules Applied

1. **No NLSM Predictor Usage**: The NLSM raster was **NOT** used to define pseudo-absences or predictors.
2. **Buffer Exclusion**: All cells within $200\text{ m}$ of any landslide polygon or point are tagged $255$ (buffer exclusion zone) to avoid false negatives at slope margins.
3. **Terrain Slope Threshold**: Plain valleys, lakes, and low-gradient terrain ($	ext{slope} \le 5.0^\circ$) are excluded from sampling to prevent trivial negative class bias.
4. **Data Completeness Requirement**: Negative samples are drawn exclusively from cells where `hazard_feature_complete_mask == 1`.
5. **No Raw Data Modification**: Source vector archives under `C:\Users\Saurabh Sharma\Downloads\J&K` remain **100% read-only**.

---

## 3. Final Target Label Decision

| Target Label Value | Category | Cell Count | Percentage of Valid Land | Model Treatment |
|:---:|:---|:---:|:---:|:---|
| **1** | Landslide Presence | 4,587 | 0.10% | Positive Class ($y=1$) |
| **0** | Verified Pseudo-Absence | 3,596,475 | 77.86% | Negative Class ($y=0$) |
| **255** | Excluded / Buffer / Low Slope | 1,018,149 | 22.04% | Excluded from Training & Evaluation |

---

## 4. Verification Checkpoint Status

- **Grid Alignment**: All 7 label rasters align to `EPSG:32643`, $3050 \times 2937$, 100m grid.
- **Raw Data Safety**: `C:\Users\Saurabh Sharma\Downloads\J&K` **100% Read-Only**.
- **Status**: **PASS**.
