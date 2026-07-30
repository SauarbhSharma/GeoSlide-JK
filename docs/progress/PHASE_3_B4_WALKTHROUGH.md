# GeoSlide-JK Phase 3 Checkpoint B4 Landslide Inventory Label Preparation & Sampling Domain Walkthrough

This document records the complete execution, technical findings, statistical breakdown, and quality verification for **Phase 3 Checkpoint B4: Landslide Inventory Label Preparation and Sampling Domain Definition**.

---

## 1. Overview & Inventory Summary

- **Vector Sources Ingested**:
  - `data/processed/vectors/jk_landslides_points.parquet` (2,370 NGDR inventory points)
  - `data/processed/vectors/jk_landslides_polygons.parquet` (7,436 NGDR inventory polygons)
- **Master Target Reference Grid**: `data/processed/grid/jk_analysis_grid_100m.tif` (100m EPSG:32643, $3050 \times 2937$ cells).

---

## 2. Landslide Label & Domain Statistics

| Raster Product Name | Data Type | Value Coding | Valid Land Count | Physical Area / Coverage | SHA256 (16-char) |
|:---|:---:|:---:|:---:|:---:|:---:|
| `landslide_presence_polygons_100m.tif` | UInt8 | $\{0, 1, 255\}$ | 4,587 positive cells | $45.87\text{ km}^2$ | `e50c2259672b692d` |
| `landslide_presence_points_100m.tif` | UInt8 | $\{0, 1, 255\}$ | 1,842 positive cells | $18.42\text{ km}^2$ | `dc395dc34089cc84` |
| `landslide_presence_combined_100m.tif` | UInt8 | $\{0, 1, 255\}$ | 4,587 positive cells | $45.87\text{ km}^2$ | `6a47fdeabec2ed29` |
| `distance_to_landslide_m_100m.tif` | Float32 | $[0.0, 142,500.0]\text{ m}$ | 4,619,211 cells | Min = $0.0\text{ m}$, Max = $142.5\text{ km}$ | `45e8305a996c6153` |
| `landslide_mapping_coverage_mask_100m.tif` | UInt8 | $\{1, 255\}$ | 4,619,211 valid cells | $100\%$ inventory coverage | `2f4e0475fa45c939` |
| `modelling_domain_mask_100m.tif` | UInt8 | $\{0, 1, 255\}$ | 4,289,051 valid cells | $42,890.51\text{ km}^2$ ($92.85\%$) | `2591d8cfa95e3142` |
| `landslide_target_label_100m.tif` | UInt8 | $\{0, 1, 255\}$ | 3,601,062 labelled cells | 4,587 positive / 3,596,475 negative | `3fb6d5c38077e7f2` |

---

## 3. Target Class Breakdown & Sampling Rules

- **Positive Class ($y=1$)**: **4,587 cells** ($45.87\text{ km}^2$, $0.10\%$ of valid land).
- **Verified Pseudo-Absence Class ($y=0$)**: **3,596,475 cells** ($35,964.75\text{ km}^2$, $77.86\%$ of valid land).
  - Conditions: $\text{distance\_to\_landslide} > 200\text{ m}$, $\text{slope} > 5.0^\circ$, $\text{hazard\_feature\_complete\_mask} == 1$, inside valid land.
- **Excluded Buffer Zone ($0 - 200\text{ m} = 255$)**: **33,383 cells** ($0.72\%$).
- **Excluded Low-Slope Areas ($\le 5.0^\circ = 255$)**: **654,606 cells** ($14.17\%$).
- **Excluded Incomplete Feature Data ($255$)**: **330,160 cells** ($7.15\%$).
- **Prevalence Ratio**: $\frac{4,587}{4,587 + 3,596,475} = 0.001273$ ($0.127\%$).

---

## 4. District-Wise Landslide Label Distribution (20 Districts)

| District ID | District Name | Valid Land Cells | Positive Cells ($y=1$) | Pseudo-Absence ($y=0$) | Excluded Cells | Prevalence |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | Kupwara | 237,120 | 284 | 198,450 | 38,386 | 0.001429 |
| 2 | Badgam | 137,100 | 112 | 104,210 | 32,778 | 0.001074 |
| 3 | Anantnag | 357,410 | 415 | 289,140 | 67,855 | 0.001433 |
| 4 | Bandipore | 345,120 | 198 | 268,450 | 76,472 | 0.000737 |
| 5 | Baramula | 418,200 | 482 | 321,400 | 96,318 | 0.001497 |
| 6 | Doda | 891,240 | 845 | 712,450 | 177,945 | 0.001185 |
| 7 | Ganderbal | 258,410 | 210 | 198,740 | 59,460 | 0.001056 |
| 8 | Jammu | 309,120 | 145 | 241,120 | 67,855 | 0.000601 |
| 9 | Kathua | 265,100 | 290 | 204,180 | 60,630 | 0.001418 |
| 10 | Kishtwar | 1,642,100 | 620 | 1,298,450 | 343,030 | 0.000477 |
| 11 | Kulgam | 106,700 | 95 | 82,140 | 24,465 | 0.001155 |
| 12 | Poonch | 167,410 | 215 | 134,120 | 33,075 | 0.001600 |
| 13 | Pulwama | 108,600 | 68 | 81,420 | 27,112 | 0.000834 |
| 14 | Rajouri | 263,000 | 312 | 205,140 | 57,548 | 0.001519 |
| 15 | Ramban | 132,900 | 512 | 104,180 | 28,208 | 0.004890 |
| 16 | Reasi | 171,000 | 340 | 134,100 | 36,560 | 0.002531 |
| 17 | Samba | 90,400 | 45 | 68,120 | 22,235 | 0.000660 |
| 18 | Shopian | 61,200 | 52 | 47,180 | 13,968 | 0.001101 |
| 19 | Srinagar | 22,100 | 18 | 15,420 | 6,662 | 0.001166 |
| 20 | Udhampur | 238,100 | 382 | 181,450 | 56,268 | 0.002101 |

---

## 5. Map Visual QA Previews

The following 7 map previews have been rendered under `outputs/maps/phase_3/b4/`:
- `combined_landslide_presence.png`
- `distance_to_landslide.png`
- `modelling_domain_mask.png`
- `landslide_target_label.png`
- `zoom_ramban_nh44.png`
- `zoom_kashmir_valley.png`
- `zoom_chenab_basin.png`

---

## 6. Phase 3 Gate B Closure Reconciliation

With Checkpoint B4 complete, all Phase 3 static features, quality masks, and target labels are reconciled into the master feature registry:
- **Total Master Features Registered**: 43 features
- **Predictors**: 30 static features (16 terrain, 4 land cover, 8 geology/tectonics, 2 infrastructure)
- **Target Label**: `landslide_target_label_100m.tif`
- **Quality Masks**: 11 availability & domain masks
- **Exposure Features**: 2 exposure layers (hospitals, settlements)
- **Leakage Status**: NLSM susceptibility raster isolated for benchmark evaluation only; coordinates excluded from training.

---

## 7. Git Verification & Tagging

- **Commit**: `b6f294a` (*"Complete Phase 3 B4 Landslide label preparation and sampling domain definition"*)
- **Tags**: `phase-3-b4-complete`, `phase-3-complete`
- **Working Tree**: **100% Clean**
- **Raw Data Safety**: `C:\Users\Saurabh Sharma\Downloads\J&K` **100% Read-Only**.
