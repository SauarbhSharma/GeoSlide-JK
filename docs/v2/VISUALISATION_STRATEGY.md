# GeoSlide-JK 2.0 — Decision-Supporting Visualization Strategy

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)

---

## 1. Visualization Philosophy: *"From Maps to Actions"*

In GeoSlide-JK v1.0.0, the primary visualization was a dense 100m raster color overlay spanning the full J&K UT. While visually impressive, raw raster maps require geospatial expertise to interpret.

**GeoSlide-JK 2.0** introduces **Role-Tailored Decision Visualizations** that transform spatial data into task-specific visual formats:

---

## 2. Visualisation Specifications by Persona Group

### A. Travellers & Residents
- **Route-Risk Strip View:** A linear horizontal elevation and risk profile showing high-instability kilometers along the chosen highway route.
- **Critical Stretch Highlight Cards:** Compact cards highlighting specific problem stretches (e.g. `Panthyal Overhang, Km 142.5`) with color-coded risk indicators.
- **Multi-Route Comparison Table:** Side-by-side comparison of primary vs alternate routes showing total distance, high-risk km, and relative risk score.

### B. NHAI & Highway Operations Officers
- **Corridor Chainage Risk Heatmap:** Continuous linear heatmap indexed from Km 0 to Km 295 showing segment-level Landslide Hazard Scores ($LHS$).
- **Intervention Priority Queue Table:** Score-ranked maintenance table with inline action toggles and officer assignments.
- **Disruption Impact Matrix:** 2D matrix plotting Landslide Hazard Score ($LHS$) vs Disruption Impact Score ($DIS$) to isolate top-right critical intervention priorities.

### C. District Administration & DDMA
- **20-District Vulnerability Choropleth:** Color-coded district map displaying mean susceptibility and count of high-risk grid cells.
- **Settlement & Access Road Isolation Overlay:** Vector map highlighting rural villages vulnerable to single-point road cut-offs during monsoon rains.
- **Resource Pre-Positioning Checklist:** Interactive checklist tracking staging of excavation machinery across vulnerable district sectors.

### D. Technical Users & Researchers
- **100m Master Grid MapLibre Canvas:** Full interactive GIS map with custom vector/raster layer controls, legends, and point sampling popups.
- **Interactive SHAP Feature Importance Plot:** Bar chart displaying global predictor feature rankings (e.g. distance to fault, elevation, slope).
- **Spatial CV Fold ROC/PR Curves:** Interactive charts displaying out-of-fold cross-validation performance curves.

---

## 3. Retain, Simplify, Relocate, Combine, and Remove Matrix

| Existing v1.0.0 Element | Recommendation | Action Details |
| :--- | :--- | :--- |
| **MapLibre 100m Vector/Raster Canvas** | **RETAIN** | Keep as core map canvas in Research Mode and embedded map in Traveller/Authority modes. |
| **Release Status Banner** | **SIMPLIFY & RELOCATE** | Remove from 6 separate pages. Relocate to global Header modal and System Status page. |
| **Left Sidebar Layer Toggles** | **COMBINE & RELOCATE** | Combine with right-side map overlay into a single floating, collapsible `Map Layers` drawer. |
| **Right-Side 320px Permanent Panel** | **REMOVE** | Remove permanent fixed-width desktop panel. Replace with responsive floating card drawers. |
| **Separate `/explorer` Route** | **MERGE** | Merge `/explorer` into main `/` route as a toggleable full-screen map mode. |
| **Separate `/rainfall` Route** | **MERGE & SIMPLIFY** | Merge point-sampling controls into `/location-check` ("Check My Area"). |
| **Research Disclaimer Banner** | **RETAIN** | Keep in global Header and bottom page footer. |
