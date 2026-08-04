# GeoSlide-JK 2.0 — Checkpoint V2-3A Chainage Method Report

> **Document Version:** 2.3A.0  
> **Status:** Completed Methodology  
> **Target Branch:** `geoslide-jk-v2-product-redesign`

---

## 1. Linear Referencing & Chainage Setup

Cumulative metric distance (chainage) is established along the continuous `EPSG:32643` pilot corridor LineString:
- **Origin (0.00 m / 0.000 km):** Udhampur Pilot Sector (`75.5175°E, 33.5782°N`)
- **Destination (74,875.83 m / 74.876 km):** Banihal / Anantnag Sector (`75.1744°E, 33.7171°N`)
- **Sampling Interval:** 100 meters (750 reference points in `data/processed/corridors/nh44_chainage_reference.csv`)

---

## 2. Reference Table Schema

`nh44_chainage_reference.csv` contains:
- `corridor_id`, `corridor_name`, `origin_name`, `destination_name`, `route_direction`
- `chainage_m`, `chainage_km`
- `longitude`, `latitude`, `projected_x`, `projected_y`
- `district`, `geometry_version`
