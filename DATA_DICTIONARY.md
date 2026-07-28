# GeoSlide-JK Data Dictionary & Source Reference

---

## 1. Raw Dataset Catalog

Below is the summary catalog of raw datasets identified in `C:\Users\Saurabh Sharma\Downloads\J&K`:

| Category | Primary Directory / Pattern | Format | Target Features / Usage |
| :--- | :--- | :--- | :--- |
| **Elevation & Morphometry** | `copernicus_glo30/` | GeoTIFF (.tif) | DEM, Slope, Aspect, Curvature, TWI, Local Relief, TRI |
| **Land Cover (LULC)** | `esa_worldcover_2021/` | GeoTIFF (.tif) | Dominant land cover classes (Tree, Cropland, Bare, Built-up) |
| **Geology & Lithology** | `geology_50klithology_jammu_kashmir_*` | GeoJSON & Shapefile | Lithology classes, Engineering geology categories |
| **Faults & Thrusts** | `FAULT and THRUST Tectonic J&K` | Shapefile / Zip | Fault lines, Thrust lines, Distance to fault/thrust |
| **Lineaments & Folds** | `LINEAMENT and FOLD Tectonic J&K`, `Geomorphology Lineatment J&K` | Shapefile / Zip | Lineament density, Structural orientation |
| **Active Faults & Earthquakes** | `Active Fault, Earthquake J&K` | Shapefile / Zip | Active fault proximity, Historical epicenters density |
| **Landslide Inventory** | `NGDR Shape File J&K`, `NGDR GeoJSON File` | GeoJSON & Shapefile | Landslide points & polygons (Training targets & validation) |
| **Population & Exposure** | `GHS_POP_E2025_GLOBE_...` | GeoTIFF (.tif) | Exposed population count (2025 projection) |
| **Administrative Boundaries** | `Administrative Boundary Database...` | Shapefile / Zip | 20 J&K District & Tehsil boundaries |
| **Historical Rainfall** | `IMD Yearly Gridded Rainfall Data` | NetCDF (.nc) | Historical rainfall climatology, percentiles (90th, 95th, 99th) |
| **Satellite Rainfall** | `IMERG_Download_Helper_Windows` | NetCDF4 (.nc4) | Dynamic 30-min to 72-hr rainfall accumulation |
| **Station Rainfall** | `WRIS Rainfall Data` | Excel (.xlsx) | Station rainfall comparison and validation |
| **Susceptibility Reference** | `JammuandKashmir_Susceptibility.tif_NLSM_...` | GeoTIFF (.tif) | GSI NLSM Reference Map (Validation & benchmark comparison ONLY) |

---

## 2. Derived Feature Schema (Target Analysis Grid: EPSG:32643)

| Feature Name | Type | Unit / Range | Description |
| :--- | :--- | :--- | :--- |
| `elevation` | Continuous | meters (m) | Terrain height above sea level |
| `slope_deg` | Continuous | degrees (0–90°) | Slope steepness derived from DEM |
| `aspect_rad` | Continuous | radians (0–2π) | Terrain orientation direction |
| `twi` | Continuous | index | Topographic Wetness Index |
| `tri` | Continuous | index | Terrain Roughness Index |
| `dist_fault_m` | Continuous | meters (m) | Euclidean distance to nearest tectonic fault |
| `dist_thrust_m` | Continuous | meters (m) | Euclidean distance to nearest thrust line |
| `lineament_density` | Continuous | km/km² | Spatial density of lineaments |
| `lithology_class` | Categorical | ID (1–N) | Dominant rock/sediment lithological unit |
| `lulc_class` | Categorical | ID (10–100) | ESA WorldCover land cover class |
| `dist_road_m` | Continuous | meters (m) | Proximity to road network (including NH-44) |
| `dist_stream_m` | Continuous | meters (m) | Proximity to drainage channels |
