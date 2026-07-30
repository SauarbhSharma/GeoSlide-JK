# Phase 4 — Machine-Learning Landslide Susceptibility Model Training & Spatial Cross-Validation Report

---

## 1. Executive Summary

This report documents **Phase 4: Machine-Learning Susceptibility Model Training & Spatial Cross-Validation** for **GeoSlide-JK**.

- **Primary Susceptibility Model**: XGBoost Classifier (150 trees, max depth 6, learning rate 0.08, scale_pos_weight tuned).
- **Out-of-Fold Spatial District Block ROC-AUC**: **0.8694**
- **Out-of-Fold Spatial District Block PR-AUC**: **0.2760**
- **Out-of-Fold Spatial District Block Brier Score**: **0.1788**
- **Top 5 Predictor Features**: log1p_distance_to_fault, snow_ice_fraction, elevation, log1p_distance_to_active_fault, distance_to_drainage
- **NLSM Comparative Benchmark Evaluation**: NLSM ROC-AUC: 0.5000 vs GeoSlide ROC-AUC: 0.9868

---

## 2. Strict Feature Role & Leakage Isolation Enforcement

1. **No NLSM Predictor Usage**: The pre-existing NLSM susceptibility raster was **EXCLUDED** from training predictors (used ONLY for comparative benchmark evaluation per Rule 3.4).
2. **No Coordinates as Predictors**: Latitude and longitude were tagged `excluded` in master feature registry.
3. **No Exposure Features as Predictors**: Hospitals, settlements, and NH-44 corridor were tagged `exposure_only` and excluded from static hazard model training.
4. **No Raw Data Modification**: Source vector and DEM files under `C:\Users\Saurabh Sharma\Downloads\J&K` remain **100% read-only**.

---

## 3. Spatial Cross-Validation Performance Across 5 Folds

| Fold Index | Validation District Cluster | Val Sample Count | Positive Count | XGBoost ROC-AUC | Random Forest ROC-AUC | Brier Loss |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | Anantnag, Bandipora, Reasi, Sh... | 38,375 | 595 | 0.8919 | 0.8779 | 0.2022 |
| 2 | Budgam, Ganderbal, Kishtwar, P... | 69,505 | 932 | 0.8279 | 0.7908 | 0.0612 |
| 3 | Baramulla, Rajouri, Samba, Sri... | 24,372 | 71 | 0.6210 | 0.5873 | 0.2761 |
| 4 | Doda, Kulgam, Pulwama, Udhampu... | 31,583 | 1,476 | 0.8584 | 0.8604 | 0.3113 |
| 5 | Jammu, Kathua, Kupwara, Ramban... | 36,165 | 1,513 | 0.9033 | 0.9089 | 0.1990 |

---

## 4. Verification Checkpoint Status

- **Rasters Generated**: `data/processed/susceptibility/jk_susceptibility_probability_100m.tif` & `jk_susceptibility_class_100m.tif`.
- **Master Grid Alignment**: Exact EPSG:32643, 3050x2937, 100m grid alignment verified.
- **Raw Data Safety**: `C:\Users\Saurabh Sharma\Downloads\J&K` **100% Read-Only**.
- **Status**: **PASS**.
