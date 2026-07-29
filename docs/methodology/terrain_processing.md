# Terrain Processing Methodology — GeoSlide-JK Phase 2

## 1. Overview
This document specifies the end-to-end processing workflow used to transform raw Copernicus GLO-30 Digital Elevation Model (DEM) tiles into Cloud-Optimized GeoTIFFs (COGs) and terrain derivative products for Jammu and Kashmir UT.

---

## 2. Input DEM Selection & Safeguards
- **Source Dataset**: Copernicus GLO-30 30m Global DEM (`output_hh.tif` granules).
- **Approved Tiles**: Four tiles covering SW, SE, NW, NE quadrants locked in `outputs/reports/phase_2_approved_dem_sources.csv`.
- **Exclusions**: The Pilot DEM tile (`copernicus_glo30/Pilot/output_hh.tif`) is explicitly excluded.

---

## 3. Reprojection & Mosaicking
1. **Source CRS**: `EPSG:4326` (WGS84 lat/lon coordinates).
2. **Target Planar CRS**: `EPSG:32643` (UTM Zone 43N, 30m cell resolution).
3. **Mosaicking**: The four approved tiles are mosaicked into a unified float32 elevation raster using Bilinear resampling prior to terrain derivative derivation.
4. **Boundary Clipping**: Clipped to the 20-district J&K UT boundary. Pixels outside the UT boundary are assigned NoData value `-9999.0`.

---

## 4. Terrain Derivative Algorithms
- **Slope (Degrees)**:
  $$\text{Slope} = \arctan\left(\sqrt{\left(\frac{\partial z}{\partial x}\right)^2 + \left(\frac{\partial z}{\partial y}\right)^2}\right) \times \frac{180}{\pi}$$
  Calculated using 3x3 Horn Sobel gradient operators in projected meter coordinates (`EPSG:32643`).
- **Aspect (Degrees)**:
  $$\text{Aspect} = \text{mod}\left(450 - \arctan2\left(\frac{\partial z}{\partial y}, -\frac{\partial z}{\partial x}\right) \times \frac{180}{\pi}, 360\right)$$
  Aspect represents downhill compass orientation (0° = North, 90° = East, 180° = South, 270° = West).
- **Hillshade (UInt8)**:
  Shaded relief calculated with solar azimuth 315° (NW illumination) and altitude 45°, scaled to 8-bit unsigned integer range `[0–255]`.

---

## 5. Cloud-Optimized GeoTIFF (COG) Architecture
All four output rasters (`jk_elevation_glo30_cog.tif`, `jk_slope_degrees_cog.tif`, `jk_aspect_degrees_cog.tif`, `jk_hillshade_cog.tif`) are formatted as COGs with:
- Internal tile size: 256 x 256 pixels
- Compression: DEFLATE
- Overview pyramid levels: 2, 4, 8, 16, 32
- Fast cell sampling via GDAL/Rasterio windowed reads.
