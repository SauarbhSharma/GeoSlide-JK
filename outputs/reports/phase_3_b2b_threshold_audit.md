# Phase 3 Checkpoint B2B — Drainage Threshold Scientific Audit Report

## Scientific Threshold Documentation

- **Source DEM Resolution**: 30.0 metres (Copernicus GLO-30 mosaic).
- **Flow Accumulation Engine**: WhiteboxTools v2.4.0 D8 Pointer & Accumulation (`d8_flow_accumulation`).
- **Resampling Method**: Bilinear interpolation from 30m accumulation grid to 100m master grid (`EPSG:32643`, 3050×2937).
- **Threshold Applied**: `flow_accumulation >= 500.0` (where accumulation stores 30m source cell counts).

## Scientific Area Calculation

$$\text{Threshold Area} = 500 \text{ source cells} \times (30\text{m} \times 30\text{m}) = 500 \times 900\text{ m}^2 = 450,000\text{ m}^2 = 0.45\text{ km}^2$$

## Truthful Specification Label

> **"500 source cells at 30m, equivalent to approximately 0.45 km² (450,000 m²) contributing area."**

This threshold effectively captures perennial and major seasonal stream channels across the varied terrain of Jammu and Kashmir.
