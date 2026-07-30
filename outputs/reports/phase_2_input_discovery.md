# GeoSlide-JK Phase 2 Input Discovery Report

**Date**: 2026-07-29 02:15:35
**Status**: **INPUT DISCOVERY COMPLETE — AWAITING APPROVAL A**

---

## 1. Selected Four Full-J&K DEM Tiles

| Quadrant | Relative Subfolder | Filename | Size (MB) | Dimensions (WxH) | Res | Bounds (Lon, Lat) | Elevation Range | Checksum |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Northeast (75.5-77.5°E, 34.0-36.0°N) | `copernicus_glo30\full_jk\Northeast` | `output_hh.tif` | 200.62 | 7200x7200 | 0.000278° | `[75.50, 34.00, 77.50, 36.00]` | 2144.79m to 8570.56m | `3d2e2b628f...` |
| Northwest (73.5-75.5°E, 34.0-36.0°N) | `copernicus_glo30\full_jk\Northwest` | `output_hh.tif` | 202.76 | 7200x7200 | 0.000278° | `[73.50, 34.00, 75.50, 36.00]` | 535.0m to 8104.31m | `30fe057f62...` |
| Southeast (75.5-77.5°E, 32.0-34.0°N) | `copernicus_glo30\full_jk\Southeast` | `output_hh.tif` | 202.94 | 7200x7200 | 0.000278° | `[75.50, 32.00, 77.50, 34.00]` | 244.0m to 7072.66m | `7560a7bc43...` |
| Southwest (73.5-75.5°E, 32.0-34.0°N) | `copernicus_glo30\full_jk\Southwest` | `output_hh.tif` | 191.76 | 7200x7200 | 0.000278° | `[73.50, 32.00, 75.50, 34.00]` | 198.12m to 4879.31m | `dfdeac97db...` |
| Southwest (73.5-75.5°E, 32.0-34.0°N) | `esa_worldcover_2021` | `ESA_WorldCover_10m_2021_v200_N30E072_Map (1).tif` | 117.15 | 36000x36000 | 0.000083° | `[72.00, 30.00, 75.00, 33.00]` | 10.0m to 90.0m | `08ccc86880...` |
| Southeast (75.5-77.5°E, 32.0-34.0°N) | `esa_worldcover_2021` | `ESA_WorldCover_10m_2021_v200_N30E075_Map.tif` | 97.79 | 36000x36000 | 0.000083° | `[75.00, 30.00, 78.00, 33.00]` | 10.0m to 100.0m | `1ebf66aff1...` |
| Northwest (73.5-75.5°E, 34.0-36.0°N) | `esa_worldcover_2021` | `ESA_WorldCover_10m_2021_v200_N33E072_Map.tif` | 146.1 | 36000x36000 | 0.000083° | `[72.00, 33.00, 75.00, 36.00]` | 10.0m to 100.0m | `3aab21ba29...` |
| Northeast (75.5-77.5°E, 34.0-36.0°N) | `esa_worldcover_2021` | `ESA_WorldCover_10m_2021_v200_N33E075_Map.tif` | 93.02 | 36000x36000 | 0.000083° | `[75.00, 33.00, 78.00, 36.00]` | 10.0m to 100.0m | `bbfdbf60bf...` |
| Northeast (75.5-77.5°E, 34.0-36.0°N) | `GHS_POP_E2025_GLOBE_R2023A_54009_100_V1_0_R6_C26` | `GHS_POP_E2025_GLOBE_R2023A_54009_100_V1_0_R6_C26.tif` | 69.45 | 10000x10000 | 100.000000° | `[6959000.00, 3000000.00, 7959000.00, 4000000.00]` | 0.0m to 14738.48m | `c819a318b4...` |

## 2. Excluded Pilot DEM Tile

| Filename | Relative Subfolder | Size (MB) | Reason for Exclusion | Absolute Path |
| :--- | :--- | :---: | :--- | :--- |
| `output_hh.tif` | `copernicus_glo30\Pilot` | 46.31 | Excluded from Phase 2 processing (Pilot Candidate - partial extent 46 MB) | `C:\Users\Saurabh Sharma\Downloads\J&K\copernicus_glo30\Pilot\output_hh.tif` |
| `JammuandKashmir_Susceptibility.tif_NLSM_20260725210220.036_11842.tif` | `.` | 0.53 | Excluded from Phase 2 processing (Pilot Candidate - partial extent 46 MB) | `C:\Users\Saurabh Sharma\Downloads\J&K\JammuandKashmir_Susceptibility.tif_NLSM_20260725210220.036_11842.tif` |

---

## 3. Boundary Inputs

- **District Boundary Path**: `D:\Projects\GeoSlide_JK\data\processed\boundaries\jk_districts.geojson`
- **UT Boundary Path**: `D:\Projects\GeoSlide_JK\data\processed\boundaries\jk_ut_boundary.geojson`
- **District Count**: **20 / 20 Whitelisted Districts**
- **CRS**: `EPSG:4326` | Bounds: `[3401978.6481, 4909133.8048, 3701754.4165, 5204221.29]`
- **Mirpur & Muzaffarabad Excluded**: `True`

## 4. Vector Inputs Manifest

### A. Landslide Inventory

### B. Tectonics & Lithology

### C. OSM Infrastructure & Exposure
