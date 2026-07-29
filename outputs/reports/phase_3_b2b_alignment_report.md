# Phase 3 Checkpoint B2B Alignment Report

## Master Grid Alignment Matrix

All 6 generated hydrological terrain rasters plus updated quality mask rasters share **100% exact alignment** with the B1 Master Reference Grid (`data/processed/grid/jk_analysis_grid_100m.tif`):

| Property | B1 Master Reference Grid | B2B Hydrological Rasters | Status / Match |
|:---|:---:|:---:|:---:|
| **CRS** | `EPSG:32643` | `EPSG:32643` | **EXACT MATCH** |
| **Grid Dimensions (W x H)** | 3,050 x 2,937 | **3,050 x 2,937** | **EXACT MATCH** |
| **Pixel Resolution** | 100.0 m x 100.0 m | **100.0 m x 100.0 m** | **EXACT MATCH** |
| **Grid Bounds [MinX, MinY, MaxX, MaxY]** | `[360800.0, 3571100.0, 665800.0, 3864800.0]` | `[360800.0, 3571100.0, 665800.0, 3864800.0]` | **EXACT MATCH** |
| **Affine Transform** | `Affine(100.0, 0.0, 360800.0, 0.0, -100.0, 3864800.0)` | `Affine(100.0, 0.0, 360800.0, 0.0, -100.0, 3864800.0)` | **EXACT MATCH** |

---

## Output File Inventory

| Feature Name | Format | Path | File Size | SHA256 Checksum (Prefix) |
|:---|:---:|:---|:---:|:---|
| `flow_direction` | COG | `data/processed/features/terrain/terrain_flow_direction_100m.tif` | 1,697,286 bytes | `49865fac48c77551` |
| `flow_accumulation` | COG | `data/processed/features/terrain/terrain_flow_accumulation_100m.tif` | 17,068,111 bytes | `91a2d30ccb1cd2fc` |
| `drainage_network` | COG | `data/processed/features/terrain/terrain_drainage_network_100m.tif` | 283,008 bytes | `a0d8a56942c6b50b` |
| `distance_to_drainage` | COG | `data/processed/features/terrain/terrain_distance_to_drainage_100m.tif` | 1,941,616 bytes | `8bccc78327e02971` |
| `drainage_density` | COG | `data/processed/features/terrain/terrain_drainage_density_100m.tif` | 1,346,510 bytes | `8f924bb2469d8fd3` |
| `twi` | COG | `data/processed/features/terrain/terrain_twi_100m.tif` | 16,235,901 bytes | `818d42a07e14e79a` |
| `availability_count` | COG UInt8 | `data/processed/features/terrain/terrain_feature_availability_count_100m.tif` | 35,098 bytes | `5908686dbd073f83` |
| `complete_mask` | COG UInt8 | `data/processed/features/terrain/terrain_feature_complete_mask_100m.tif` | 33,253 bytes | `6abf04418206dbd4` |
