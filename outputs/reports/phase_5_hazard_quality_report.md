# Phase 5 — Dynamic Rainfall Ingestion, Climatological Percentiles & Dynamic Hazard Report

---

## 1. Executive Summary

This report documents **Phase 5: Dynamic Rainfall Ingestion, Climatological Percentiles & Dynamic Hazard Thresholds** for **GeoSlide-JK**.

- **24h Precipitation Accumulation Range**: **5.0 mm - 160.0 mm**
- **IMD 90th Percentile Baseline P90 Range**: **30.0 mm - 95.0 mm**
- **Dynamic Landslide Hazard Index Formula**: $H_{dyn} = S \times \left(\frac{\text{Rainfall}_{24h}}{\text{P90}}\right)$
- **India-WRIS Station Cross-Validation MAE**: **1.94 mm**

---

## 2. 5-Class Dynamic Hazard Rating Breakdown

| Rating Class Code | Hazard Level | Cell Count | Area ($	ext{km}^2$) | Percentage of Valid Land |
|:---:|:---|:---:|:---:|:---:|
| **1** | Very Low | 3,120,791 | 31207.91 | 67.56% |
| **2** | Low | 437,521 | 4375.21 | 9.47% |
| **3** | Moderate | 371,692 | 3716.92 | 8.05% |
| **4** | High | 382,017 | 3820.17 | 8.27% |
| **5** | Critical / Very High | 307,190 | 3071.90 | 6.65% |

---

## 3. Master Reference Grid Verification

- All 5 Phase 5 rasters align to `EPSG:32643`, $3050 \times 2937$, 100m grid.
- **Raw Data Safety**: `C:\Users\Saurabh Sharma\Downloads\J&K` **100% Read-Only**.
- **Status**: **PASS**.
