# UI Static Map Layers Documentation — GeoSlide-JK Phase 2

## 1. Overview
This document outlines the UI layer hierarchy, MapLibre GL JS styling specifications, legend rules, and interactive inspection features integrated in Phase 2.

---

## 2. Layer Hierarchy & Styling

| Layer ID | Map Type | Symbology & Color Code | Visibility Default |
| :--- | :--- | :--- | :--- |
| `jk-districts-fill` | Vector Fill | Sky Blue `#0ea5e9` (Opacity: 0.12) | Visible |
| `jk-districts-line` | Vector Line | Light Sky `#38bdf8` (Width: 1.4px) | Visible |
| `jk-districts-labels` | Symbol Label | Upper Case `#e2e8f0` with Dark Halo | Visible |
| `jk-landslides-points` | Circle Marker | Red `#ef4444` (Radius: 4px) | Visible |
| `jk-landslides-polygons` | Vector Polygon | Dark Red `#b91c1c` (Opacity: 0.4) | Visible |
| `jk-faults` | Dashed Line | Pink `#ec4899` (Width: 2.2px, Dashed) | Visible |
| `jk-thrusts` | Solid Line | Purple `#a855f7` (Width: 2.5px) | Visible |
| `jk-nh44` | Highlight Line | Amber Gold `#eab308` (Width: 3.5px) | Visible |
| `jk-health` | Circle Marker | Emerald `#10b981` (Radius: 3.5px) | Hidden (Toggle) |
| `jk-settlements` | Circle Marker | Slate Blue `#64748b` (Radius: 2.5px) | Hidden (Toggle) |

---

## 3. Interactive Terrain Inspector
- **Map-Click Sampling**: Clicking any geographic location on the map triggers an HTTP request to `/api/v1/terrain/value?lat={lat}&lon={lon}`.
- **Inspector Popup**: Displays latitude, longitude, district name, sampled elevation (m ASL), slope angle (°), aspect (°), and data provenance.
- **Controlled Error Handling**: Clicking outside the J&K UT boundary gracefully indicates "Outside J&K UT Boundary" with null terrain values.
