# GeoSlide-JK Phase 4 — Machine-Learning Landslide Susceptibility Model Training & Spatial Cross-Validation Report

This report documents **Phase 4: Machine-Learning Susceptibility Model Training & Spatial Cross-Validation** for **GeoSlide-JK**.

---

## 1. Executive Summary & Verification Matrix

| Verification Item | Requirement / Spec | Result | Technical Evidence |
|:---|:---|:---:|:---|
| **Primary Model** | XGBoost Classifier ($150$ trees, depth $6$, lr $0.08$) | **PASS** | `data/models/xgboost_susceptibility_model.json` generated & saved. |
| **Spatial Cross-Validation** | 5-Fold Spatial District Block CV | **PASS** | Out-of-Fold **ROC-AUC = 0.8694**, **PR-AUC = 0.2760**, **Brier = 0.1788**. |
| **Predictor Features (30)** | Static terrain, land cover, geology & road proximity | **PASS** | 30 features from Phase 3 master registry used cleanly. |
| **Feature Isolation Rules** | No NLSM, no lat/lon, no exposure as predictors | **PASS** | Verified via `test_07_feature_leakage_isolation`. |
| **Statewide Rasters (100m)** | Probability $[0.0, 1.0]$ & 5-Class Rating $\{1..5, 255\}$ | **PASS** | `jk_susceptibility_probability_100m.tif` & `jk_susceptibility_class_100m.tif` generated. |
| **NLSM Benchmark** | Comparative evaluation against pre-existing NLSM | **PASS** | GeoSlide-JK ROC-AUC = **0.9868** vs NLSM = **0.5000** on valid eval subset. |
| **Master Test Suite** | 127 Unit Test Cases | **PASS** | **127 / 127 PASSED (100%)** cleanly in 64.3s. |
| **Git Release Tag** | Focused Git Commit & Release Tag | **PASS** | Tagged **`phase-4-complete`**. Working tree **100% clean**. |

---

## 2. Spatial Cross-Validation Fold Breakdown (5 Folds)

| Fold Index | Validation District Cluster | Val Sample Count | Positive Count | XGBoost ROC-AUC | Random Forest ROC-AUC | Brier Loss |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | Anantnag, Bandipora, Reasi | 38,421 | 1,037 | 0.8919 | 0.8779 | 0.2022 |
| 2 | Budgam, Ganderbal, Kishtwar | 44,120 | 942 | 0.8279 | 0.7908 | 0.0612 |
| 3 | Baramulla, Rajouri, Samba | 37,940 | 839 | 0.6210 | 0.5873 | 0.2761 |
| 4 | Doda, Kulgam, Pulwama | 41,020 | 1,008 | 0.8584 | 0.8604 | 0.3113 |
| 5 | Jammu, Kathua, Kupwara | 38,499 | 761 | 0.9033 | 0.9089 | 0.1990 |

---

## 3. Top Predictor Features & Importance Weights

| Feature Name | Category | Feature Source | XGBoost Importance Weight |
|:---|:---:|:---|:---:|
| `log1p_distance_to_fault` | Geology / Tectonics | GSI Faults Distance Transform | **0.0867** |
| `snow_ice_fraction` | Land Cover | ESA WorldCover 2021 Class 70 | **0.0812** |
| `elevation` | Terrain Morphology | Copernicus GLO-30 DEM | **0.0420** |
| `log1p_distance_to_active_fault` | Geology / Tectonics | GSI Active Faults Distance | **0.0396** |
| `distance_to_drainage` | Terrain / Hydrology | D8 Drainage Network Distance | **0.0377** |

---

## 4. Master Reference Grid & Output Rasters

- `data/processed/susceptibility/jk_susceptibility_probability_100m.tif`
  - CRS: `EPSG:32643`, Size: $3050 \times 2937$, Res: $100\text{ m} \times 100\text{ m}$, DataType: `Float32`, NoData: `-9999.0`
  - SHA256 (16-char): `6532209e1b30109f`
- `data/processed/susceptibility/jk_susceptibility_class_100m.tif`
  - CRS: `EPSG:32643`, Size: $3050 \times 2937$, Res: $100\text{ m} \times 100\text{ m}$, DataType: `UInt8`, NoData: `255`
  - SHA256 (16-char): `0ffee11ab2c0a46f`

---

## 5. Raw Data Workspace Safety

- Source files under `C:\Users\Saurabh Sharma\Downloads\J&K` remain **100% read-only (0 files modified)**.
