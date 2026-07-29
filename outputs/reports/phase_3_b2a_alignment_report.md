# Phase 3 Checkpoint B2A Alignment Report

## Master Grid Alignment Matrix

All 10 generated non-hydrological terrain rasters plus 2 quality mask rasters share **100% exact alignment** with the B1 Master Reference Grid (`data/processed/grid/jk_analysis_grid_100m.tif`):

| Property | B1 Master Reference Grid | B2A Terrain Rasters | Status / Match |
|:---|:---:|:---:|:---:|
| **CRS** | `EPSG:32643` | `EPSG:32643` | **EXACT MATCH** |
| **Grid Dimensions (W x H)** | 3,050 x 2,937 | **3,050 x 2,937** | **EXACT MATCH** |
| **Pixel Resolution** | 100.0 m x 100.0 m | **100.0 m x 100.0 m** | **EXACT MATCH** |
| **Grid Bounds [MinX, MinY, MaxX, MaxY]** | `[360800.0, 3571100.0, 665800.0, 3864800.0]` | `[360800.0, 3571100.0, 665800.0, 3864800.0]` | **EXACT MATCH** |
| **Affine Transform** | `Affine(100.0, 0.0, 360800.0, 0.0, -100.0, 3864800.0)` | `Affine(100.0, 0.0, 360800.0, 0.0, -100.0, 3864800.0)` | **EXACT MATCH** |
| **NoData Value** | `-9999.0` (Float32) / `255` (UInt8) | `-9999.0` (Float32) / `255` (UInt8) | **EXACT MATCH** |

---

## Output File Inventory

| Feature Name | Format | Path | File Size | SHA256 Checksum (Prefix) |
|:---|:---:|:---|:---:|:---|
| `elevation` | COG Float32 | `data/processed/features/terrain/terrain_elevation_100m.tif` | 15,701,194 bytes | `ff24b08b55a32c77` |
| `slope` | COG Float32 | `data/processed/features/terrain/terrain_slope_100m.tif` | 16,401,546 bytes | `21c8b6b878bae455` |
| `aspect` | COG Float32 | `data/processed/features/terrain/terrain_aspect_100m.tif` | 16,348,555 bytes | `05740a3aee0b7cac` |
| `northness` | COG Float32 | `data/processed/features/terrain/terrain_northness_100m.tif` | 16,924,564 bytes | `f9a33bd1161fa1e1` |
| `eastness` | COG Float32 | `data/processed/features/terrain/terrain_eastness_100m.tif` | 16,731,847 bytes | `ccf95042ce752bba` |
| `profile_curvature` | COG Float32 | `data/processed/features/terrain/terrain_profile_curvature_100m.tif` | 17,311,662 bytes | `35673a222fd712ba` |
| `plan_curvature` | COG Float32 | `data/processed/features/terrain/terrain_plan_curvature_100m.tif` | 17,302,385 bytes | `e90a12a3b11bb823` |
| `tri` | COG Float32 | `data/processed/features/terrain/terrain_tri_100m.tif` | 15,610,610 bytes | `d54429fb2ccbe904` |
| `tpi` | COG Float32 | `data/processed/features/terrain/terrain_tpi_100m.tif` | 15,335,326 bytes | `504b35f83fd4b9a9` |
| `local_relief` | COG Float32 | `data/processed/features/terrain/terrain_local_relief_100m.tif` | 13,701,659 bytes | `12827bba9c336335` |
| `availability_count` | COG UInt8 | `data/processed/features/terrain/terrain_feature_availability_count_100m.tif` | 35,097 bytes | `4de850b793dca9d1` |
| `complete_mask` | COG UInt8 | `data/processed/features/terrain/terrain_feature_complete_mask_100m.tif` | 33,253 bytes | `6abf04418206dbd4` |
