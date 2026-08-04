# GeoSlide-JK 2.0 — Role-Specific Map Configuration Specifications

> **Document Version:** 2.2.6  
> **Status:** Completed Map Configuration  
> **Target Branch:** `geoslide-jk-v2-product-redesign`

---

## 1. Role-Based Map Configuration Matrix

To prevent cognitive overload and present relevant decision spatial layers, GeoSlide-JK 2.0 configures the map canvas specifically per role:

| Role Experience | Default Visible Spatial Layers | Default Hidden Spatial Layers | Default Zoom & Bounding Extent | Primary Actions Available |
| :--- | :--- | :--- | :--- | :--- |
| **1. Traveller / Resident** | • 5-Class Susceptibility Raster (`susceptibility_class`) <br> • 20-District Boundaries (`jk_districts`) <br> • NH-44 Corridor Polyline (`nh44`) | • Feature importance lists <br> • Tectonic faults & thrusts <br> • Raw float32 geotiff probability <br> • Full geospatial layer catalogue | Full J&K UT extent (`[73.2, 32.2] to [77.8, 35.2]`) or User Location | • Check My Area <br> • Plan Journey Preview <br> • View Technical Details |
| **2. Highway Operations** | • 5-Class Susceptibility Raster (`susceptibility_class`) <br> • NH-44 Corridor Polyline (`nh44`) <br> • Candidate 500m Analysis Segments <br> • Important Corridor Towns | • Raw model hyperparameters <br> • District admin summary cards <br> • Citizen precaution popups | Zoomed to NH-44 Corridor (Udhampur–Banihal stretch, `Zoom 9.5`) | • Open Corridor Screening <br> • Select Segment <br> • View Exposure Basis |
| **3. District Administration** | • 5-Class Susceptibility Raster (`susceptibility_class`) <br> • Selected District Boundary <br> • Mapped Major Roads <br> • Settlement & Health Facility Vectors | • Nationwide research benchmarks <br> • Model feature importance lists <br> • Microservice tile logs | Zoomed to Selected District Boundary (e.g. Ramban, `Zoom 9.0`) | • Review High-Susceptibility Zones <br> • View Access Constraints <br> • Review DDMA Suggestions |
| **4. Research / Technical** | • Full Layer Catalogue (Toggleable) <br> • Continuous Susceptibility Probability (`susceptibility_prob`) <br> • Dynamic 24h Rainfall Proxy <br> • Tectonic Faults, Thrusts, Lineaments <br> • NGDR Landslide Inventory | None (Unrestricted access to all 12 spatial vector & raster layers) | Full J&K UT extent with custom zoom controls | • Toggle Any Raster/Vector Layer <br> • Sample 100m Grid Cell Values <br> • Inspect Model Provenance |

---

## 2. Cartographic Contrast & 5-Class Color Palette

To ensure clear visibility against the CartoDB dark basemap, GeoSlide-JK 2.0 uses a high-contrast, colorblind-tested 5-class color palette:

- **Class 1 (Very Low, 0.00 – 0.15):** `#10b981` (Emerald Green)
- **Class 2 (Low, 0.15 – 0.35):** `#84cc16` (Lime Green)
- **Class 3 (Moderate, 0.35 – 0.55):** `#f59e0b` (Amber Yellow)
- **Class 4 (High, 0.55 – 0.75):** `#f97316` (Orange)
- **Class 5 (Very High, 0.75 – 1.00):** `#f43f5e` (Rose Red)
- **No Data / Outside Study Area:** Explicitly rendered as transparent / missing grid mask, never colored green or labeled "Low Risk".
