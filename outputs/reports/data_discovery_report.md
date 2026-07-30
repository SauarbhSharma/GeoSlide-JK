# GeoSlide-JK Data Discovery & Audit Report

**Project Root**: `D:\Projects\GeoSlide_JK`
**Raw Data Root (Read-Only)**: `C:\Users\Saurabh Sharma\Downloads\J&K`

## Audit Summary
- Total Categories Configured: 18
- Categories Verified (Single Match): 7
- Categories with Multiple Matches / Tiles: 11
- Missing Categories: 0

## Category Details

| Category | Status | Match Count | Configured Patterns |
| :--- | :--- | :--- | :--- |
| `boundaries.district_search` | **MULTIPLE_MATCHES** | 4 | `Administrative Boundary Database For State Upto Distt level with HQ OVSF_1M_9/**/*.shp`, `Administrative Boundary Database For State Upto Distt level with HQ OVSF_1M_9/**/*.geojson` |
| `boundaries.tehsil_search` | **MULTIPLE_MATCHES** | 6 | `Administrative Boundary Database For State Upto Taluk level with HQ OVSF_1M_8/**/*.shp`, `Administrative Boundary Database For State Upto Taluk level with HQ OVSF_1M_8/**/*.geojson` |
| `dem.copernicus_glo30_search` | **MULTIPLE_MATCHES** | 5 | `copernicus_glo30/**/*.tif` |
| `landcover.worldcover_search` | **MULTIPLE_MATCHES** | 4 | `esa_worldcover_2021/**/*.tif` |
| `geology.lithology_geojson` | **VERIFIED** | 1 | `geology_50klithology_jammu_kashmir_geoJSON file/**/*.geojson` |
| `geology.lithology_shapefile` | **VERIFIED** | 1 | `geology_50klithology_jammu_kashmir_shape file/**/*.shp` |
| `tectonics.fault_search` | **MULTIPLE_MATCHES** | 2 | `FAULT and THRUST Tectonic J&K/**/*.shp` |
| `tectonics.active_fault_search` | **MULTIPLE_MATCHES** | 2 | `Active Fault, Earthquake J&K/**/*.shp` |
| `tectonics.lineament_search` | **VERIFIED** | 1 | `LINEAMENT and FOLD Tectonic J&K/**/*.shp` |
| `tectonics.geomorphology_lineament_search` | **VERIFIED** | 1 | `Geomorphology Lineatment J&K/**/*.shp` |
| `landslides.ngdr_geojson_search` | **MULTIPLE_MATCHES** | 2 | `NGDR GeoJSON File/**/*.geojson` |
| `landslides.ngdr_shapefile_search` | **MULTIPLE_MATCHES** | 2 | `NGDR Shape File J&K/**/*.shp` |
| `landslides.nlsm_reference_tif` | **VERIFIED** | 1 | `JammuandKashmir_Susceptibility.tif_NLSM_20260725210220.036_11842.tif` |
| `population.ghs_pop_search` | **VERIFIED** | 1 | `GHS_POP_E2025_GLOBE_R2023A_54009_100_V1_0_R6_C26/**/*.tif` |
| `rainfall.imd_search` | **MULTIPLE_MATCHES** | 6 | `IMD Yearly Gridded Rainfall Data/**/*.nc` |
| `rainfall.imerg_search` | **MULTIPLE_MATCHES** | 144 | `IMERG_Download_Helper_Windows/**/*.nc4` |
| `rainfall.wris_search` | **MULTIPLE_MATCHES** | 34 | `WRIS Rainfall Data/**/*.xlsx` |
| `reference_metadata.data_source_reference` | **VERIFIED** | 1 | `GeoSlide_JK_Data_Source_Reference.xlsx` |

---
*Report generated automatically by `geoslide.audit.discovery`. Source datasets verified read-only.*