# GeoSlide-JK Changelog

All notable changes to the **GeoSlide-JK** project will be documented in this file.

---

## [2.3.11] - 2026-08-08

### Added
- **V2-3F-R5 Corrective Release:** `v2.3f-r5-nh44-dhi-authoritative-correction`.
- **Authoritative 2D Spatial GPM Grid Intersection:** 11 native 2D 0.1° GPM cells across 5 latitude bands (33.0°N to 33.5°N) mapped to all 158 corridor segments with 100% Path A/B agreement (`outputs/reports/v2_3f_r5_native_cell_evidence.csv`).
- **Unproven Support Locations:** Marked 8 historical 0.02° locations as `ROLE_UNPROVEN` and excluded them from scientific calculations (`v2_3f_r5_derived_support_location_evidence.csv`).
- **Scenario Provenance Alignment:** Corrected S4 and S5 provenance to repository-defined hypothetical stress tests (`v2_3f_r5_authoritative_scenario_definitions.csv`).
- **DHI_D Redundancy Audit:** `DHI_D = sqrt(DHI_B)` proved with 0.0 machine-precision residual in full precision and 4.29e-5 on 4-decimal rounded values (`v2_3f_r5_dhi_d_redundancy_audit.csv`).
- **Full POSIX Manifest Coverage:** Complete manifest covering outputs, docs, UI, scripts, tests, and build logs (`v2_3f_r5_output_hashes.csv`).

---

## [2.3.10] - 2026-08-07

### Added - V2-3F-R4 NH-44 DHI Scientific Evidence and Release-Integrity Completion
- **Native GPM Resolution Disambiguation:** Proven 2 native 0.1-degree (~11 km) GPM IMERG grid cells (`GPM_NATIVE_33.25N_75.15E` with 98 segments and `GPM_NATIVE_33.25N_75.25E` with 60 segments). The 8 locations are derived 0.02-degree corridor-support interpolation nodes.
- **Zero-Variance Correlation Semantics:** Standardized within-scenario constant vector rank correlations to null/blank numeric fields with `status = UNDEFINED_ZERO_VARIANCE` and `verification_status = VERIFIED_UNDEFINED_ZERO_VARIANCE`.
- **DHI_D Exact Redundancy:** Proved `DHI_D = sqrt(DHI_B)` with 0.0 max absolute residual, strictly excluding DHI_D from all consensus and stability calculations.
- **Scenario Derivation Provenance:** Documented explicit YAML keys in `configs/rainfall_thresholds.yaml` and Parquet columns in `data/processed/rainfall/nh44_rainfall_climatology_percentiles.parquet`.
- **UI & Documentation Sync:** Updated Next.js corridor page (`apps/web/app/corridor/page.tsx`), README, CHANGELOG, methodology, data dictionary, and completion report.

---

## [2.3.6] - 2026-08-07

### Added - V2-3F NH-44 DHI Robustness, Consensus and Uncertainty Audit Complete
- **Independent & Redundant Formulations:** Evaluated `DHI_A`, `DHI_B`, `DHI_C` as independent formulations. Proved `DHI_D = sqrt(DHI_B)` is a strictly monotonic power transformation (Spearman rho = 1.000) and excluded it from consensus.
- **Dry Control S0 Handling:** Unranked zero-rainfall control under `DRY_CONTROL_NO_DYNAMIC_DISCRIMINATION` status to prevent false quintile assignments.
- **Native Grid Cell Limitation:** Exposed 8 distinct native 0.1-degree (~11 km) GPM IMERG grid cells (median 19.5 segments/cell) with mandatory coarse spatial support disclaimers.
- **UI Integration:** Updated Next.js NH-44 Corridor page with consensus selector, formulation spread, native cell support details, and research truthfulness disclaimers.
- **Automated Test Suite:** Expanded Python test suite to 286 automated tests with 100% pass rate.

---

## [2.3.5] - 2026-08-06

### Added - V2-3E Scenario-Based Rainfall Dynamic Hazard Profiles
- **Scenarios S0-S5:** Integrated 6 research scenarios across 158 NH-44 corridor segments (948 records).
- **Antecedent Rainfall Indices:** Calculated 24h, 72h, and API7 antecedent moisture indices across 10-year GPM IMERG baseline.

---

## [0.2.0] - 2026-07-29

### Added - Phase 2 & Phase 2.1 Complete
- **Copernicus DEM 30m Mosaic**: Mosaicked 4 approved Copernicus GLO-30 DEM tiles covering all 20 J&K districts (`EPSG:32643`, 51,322,278 valid land pixels).
- **Raster COGs**: Generated Cloud-Optimized GeoTIFFs for Elevation (`jk_elevation_glo30_cog.tif`), Slope (`jk_slope_degrees_cog.tif`), Aspect (`jk_aspect_degrees_cog.tif`), and Hillshade (`jk_hillshade_cog.tif`).
- **Static Vector Layers**: Processed 10 static vector layers to GeoPackage and GeoParquet format clipped to J&K UT boundary (2,370 landslide points, 7,436 landslide polygons, 774 lineaments, 4,076 lithology units, tectonic thrusts, NH-44, major roads, settlements, health facilities).
- **Active Fault Resolution**: Option B implemented — merged active faults into `jk_faults.parquet` with attribute `fault_type = 'active'`.
- **Feature Count Reconciliation**: Generated `outputs/reports/phase_2_feature_count_reconciliation.csv` and `.md` documenting exact raw vs processed count differences across all 10 layers.
- **Master Layer Registry**: Built `apps/web/lib/layerRegistry.ts` defining single source of truth for 17 layers used across UI and API.
- **Public UI Wording**: Standardized public UI wording to `"20 J&K UT Districts"`, `"FULL J&K UT GEOGRAPHIC MAP"`, and dual status badges (`Static Geospatial Layers: Live` | `Risk & Rainfall Modules: Demo`).
- **Map Inspector Hardening**: Hardened MapLibre map inspector against null values, out-of-bounds clicks, NoData cells, and rapid consecutive clicks.
- **CSS & Tailwind Repair**: Fixed Next.js build compilation and stylesheet loading issue (`_next/static/css/f42b54daaa2f47d9.css` HTTP 200 OK), verified via automated Playwright computed style tests.
- **Screenshot Archive**: Permanently archived all 14 final UI screenshots in `docs/progress/phase_2_final_screenshots/`.
- **Automated Test Suite**: Expanded test coverage to 52 automated test cases with 100% pass rate.

---

## [0.1.1] - 2026-07-28

### Added - Phase 1.1 Correction Pass
- Truthfulness disclosures across all 7 frontend pages (`Model Pipeline Status: Not Trained`, `Interface Demonstration Only`, `Example Location — Illustrative Advisory`).
- Removed synthetic metrics (XGBoost prototype versions, ROC-AUC, PR-AUC, SHAP percentages).
- Enforced 20 whitelisted districts and excluded Mirpur & Muzaffarabad from administrative boundary endpoints.

---

## [0.1.0] - 2026-07-27

### Added - Phase 0 Foundation
- Established workspace architecture and read-only raw data rules (`C:\Users\Saurabh Sharma\Downloads\J&K`).
- Deployed modular YAML system configuration (`configs/`).
- Implemented read-only data discovery engine (`src/geoslide/audit/discovery.py`).
