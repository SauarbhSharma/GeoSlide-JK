# GeoSlide-JK Changelog

All notable changes to the **GeoSlide-JK** project will be documented in this file.

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
