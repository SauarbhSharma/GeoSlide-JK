# Phase 3 Gate A — Master Analysis Grid Design Proposal

## 1. Final Grid Specifications
- **Processing CRS**: EPSG:32643 (UTM Zone 43N)
- **Target Resolution**: **100 metres**
- **Bounds**: [360800.0, 3571100.0, 665800.0, 3864800.0] (UTM 43N)
- **Grid Dimensions**: **3,050 columns × 2,937 rows**
- **Total Cell Count**: **8,957,850 cells**
- **Valid J&K UT Land Cells**: **4,619,191 cells** (51.6% valid land area)
- **Outside Boundary Cells**: **4,338,659 cells** (48.4% NoData mask)
- **Raster File Size**: ~34.2 MB per Float32 feature, ~8.5 MB per UInt8 feature

## 2. Resolution Recommendation
- **Selected**: **100m Resolution**
- **Scientific Justification**:
  - DEM is 30m (3.3:1 aggregation ratio preserves morphometric detail).
  - WorldCover is 10m (exact 10×10 pixel block for clean land cover proportions).
  - J&K land area (~46,192 km²) yields ~4.6M valid cells — optimal scale for XGBoost ML modeling with ~10K–15K positive landslide cells.
  - 250m fallback rejected as it over-smooths slope curvature and TPI.

## 3. Unambiguous Feature Output Count
- **42 Unique Predictor Features** (16 Terrain + 10 Geology/Structure + 10 Land Cover + 6 Human Intervention)
- **10 Data Quality & Availability Features**
- **TOTAL FEATURE OUTPUTS**: **52 Unique Generated Feature Files** (Zero duplicate columns)
