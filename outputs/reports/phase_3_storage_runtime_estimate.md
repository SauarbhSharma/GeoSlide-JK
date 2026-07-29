# Phase 3 Gate A — Storage & Runtime Estimate (Revised Benchmark)

## 1. Storage & Disk Space Audit
- **Drive D: Free Space**: **92.22 GB**
- **Estimated Total Storage Needed**: **~4.3 GB**
- **Minimum Required**: **~8.0 GB**
- **Status**: **SUFFICIENT (PASS)**

## 2. Revised Runtime Estimates (Based on Empirical Benchmarks)
- Master 100m grid: 3,050 cols × 2,937 rows = 8,957,850 total cells (~4.6M valid J&K land cells)
- Benchmark sample (1M px): TRI/TPI = 0.07s, Whitebox Hydrology = 0.27s

| Processing Step | Estimated Runtime | Notes / Method |
|:---|:---|:---|
| Grid & Mask Generation | ~2 min | Rasterization of J&K UT & 20 districts |
| Terrain Resampling (30m→100m) | ~3 min | Bilinear resampling of elevation, slope, aspect |
| Morphometric Derivatives | ~5 min | Curvature, TPI, TRI, Local Relief via NumPy/SciPy |
| Full-DEM Hydrology (Whitebox) | ~5 min | 30m Full DEM pit filling, flow direction, accumulation |
| Geological & Tectonic Distances | ~5 min | Euclidean distance transforms (6 layers) |
| Moving-Window Densities | ~5 min | Radius kernels (faults, lineaments, roads, settlements) |
| Lithology Rasterization | ~3 min | 4,076 polygons mapped via 130-lookup table |
| WorldCover Mosaic & Proportions | ~8 min | 4 tiles (10m) aggregated to 100m proportions |
| Labels & Support Mask | ~2 min | Rasterization & 5km centroid buffer |
| **TOTAL ESTIMATED RUNTIME** | **~35–45 minutes** | Efficient parallel raster operations |

## 3. Memory & Storage Allocation
- **Peak RAM Usage**: **~1.5 GB** (during WorldCover block processing)
- **Temporary Disk Space**: **~350 MB** (intermediate 30m filled DEM and flow pointer)
