# GeoSlide-JK 2.0 — Data & Integration Readiness Audit

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)  
> **Audit Focus:** Dataset Availability, Integration Feasibility, and Governance Constraints

---

## 1. Readiness Classification Scheme

To prevent unverified claims and scientific misrepresentation, all data features, models, and outputs in GeoSlide-JK 2.0 are classified into three strict operational tiers:

- **Category A: Build Now with Existing Verified Data** — Features supported 100% by local, verified datasets already processed and validated in GeoSlide-JK v1.0.0.
- **Category B: Build as Clearly Labeled Research Scenario** — Features using validated spatial proxy models or scenario inputs (e.g., elevation-dependent rainfall accumulation scenarios, synthetic P90 baselines).
- **Category C: Do Not Build Until Authoritative Data/Validation Obtained** — Features requiring live external agency integrations, official engineering validations, or confidential government datasets.

---

## 2. Category A: Existing Verified Data (Ready for Immediate v2.0 UI Integration)

| Dataset / Asset | Source & Format | Coverage | Status in v1.0.0 | Operational Use in v2.0 |
| :--- | :--- | :--- | :--- | :--- |
| **Master Reference Grid** | 100m EPSG:32643 GeoTIFF | 4.62M valid cells (All 20 J&K Districts) | Processed & Verified | Spatial foundation for all grid & road-segment calculations |
| **Static Susceptibility Raster** | `jk_susceptibility_probability_100m.tif` | Full J&K UT (100m) | XGBoost Model (ROC 0.8694) | Basis for Landslide Hazard Score & Road Segment Risk |
| **Static Susceptibility Classes** | `jk_susceptibility_class_100m.tif` | Full J&K UT (100m) | 5-Class Categorical (1-5) | Basis for 5-level risk ratings (Very Low to Critical) |
| **UT & District Boundaries** | `jk_districts.geojson`, `jk_ut_boundary.geojson` | 20 Districts (EPSG:4326/32643) | Processed & Verified | District aggregation & administrative clipping |
| **Highway Corridors (NH-44)** | `jk_nh44.parquet` | Jammu–Udhampur–Ramban–Banihal–Srinagar | Processed & Verified | Highway corridor segmentation & "Manage My Corridor" |
| **Major Transport Network** | `jk_major_roads.parquet` | 4,762 road segments across J&K | Processed & Verified | Route exposure scoring & "Plan My Journey" |
| **Landslide Inventory** | `jk_landslides_points.parquet`, `jk_landslides_polygons.parquet` | 2,370 Points / 7,436 Polygons (NGDR) | Processed & Verified | Benchmark validation & historical hotspot density |
| **Structural Tectonics** | `jk_faults.parquet`, `jk_thrusts.parquet`, `jk_lineaments.parquet` | Statewide GSI 50K Structural Features | Processed & Verified | Slope instability driver identification |
| **Land Cover (LULC)** | `ESA WorldCover 2021 10m Mosaic` | Full J&K UT | Processed & Verified | Land cover vulnerability & tree/bare land proportions |
| **Exposure Infrastructure** | `jk_settlements.parquet`, `jk_health_facilities.parquet` | Statewide exposure layers | Processed & Verified | Vulnerable community & isolation risk mapping |

---

## 3. Category B: Build as Clearly Labeled Research Scenarios

| Feature / Output | Data Source / Method | Labelling Requirement | Operational Use in v2.0 |
| :--- | :--- | :--- | :--- |
| **24-Hour Rainfall Accumulation** | Orographic elevation-dependent proxy model (`jk_rainfall_accum_24h_100m.tif`, 5.0–160.0 mm) | *"Research Proxy Scenario — Not Live IMD Telemetry"* | Dynamic Hazard Index ($H_{dyn} = S \times R_{ratio}$) |
| **IMD P90 Baseline Climatology** | Synthetic 90th percentile proxy raster (`jk_imd_p90_baseline_100m.tif`, 30.0–95.0 mm) | *"Historical Baseline Proxy"* | Anomaly Ratio calculation ($R_{anomaly} = P_{24h} / P_{90}$) |
| **Pre-Monsoon Preparedness Outlook** | Static susceptibility + historical June–Sept monsoon rainfall proxy overlay | *"Seasonal Preparedness Outlook Scenario"* | Pre-monsoon staging & resource allocation planning |
| **Alternative Route Relative Risk** | Polyline intersection with 100m susceptibility raster across secondary roads | *"Lower Relative Risk Route (Research Estimate)"* | Route comparison in "Plan My Journey" |

---

## 4. Category C: Do Not Build Until Authoritative Data Obtained

The following features MUST NOT be implemented or claimed publicly in GeoSlide-JK 2.0 until formal integration agreements or authoritative data feeds are established:

| Requested Feature | Missing Data / Dependency Required | Reason for Exclusion in Immediate Build |
| :--- | :--- | :--- |
| **Live Operational Road Closures** | J&K Traffic Police / NHAI live API feed | Fake or outdated road closure advice creates severe public safety hazards and legal liability. |
| **Real-Time Automated Citizen SMS Alerts** | State Disaster Management Authority (SDMA) formal authorization | Automated mass public alerts without human-in-the-loop official approval violate state disaster protocols. |
| **Pavement Structural Condition** | NHAI Pavement Maintenance System (RAMS) internal data | Landslide susceptibility measures slope instability exposure, not structural pavement or asphalt quality. |
| **Live GPM / IMD Radar Telemetry** | IMD / ISRO real-time NetCDF data pipeline | Live satellite/radar ingestion requires dedicated backend ingestion microservices not yet active on Render Free tier. |
| **Exact Landslide Event Time Prediction** | High-frequency soil moisture sensor networks + slope displacement telemetry | Deterministic time-of-failure prediction is scientifically unfeasible without real-time geotechnical sensor grids. |
