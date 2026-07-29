# Phase 3 Checkpoint B2B — Resampling & Derivation Audit Report

## 30m-to-100m Resampling Rules

| Feature Name | 30m-to-100m Method | Rationale & Safeguards | Model Tag |
|:---|:---|:---|:---|
| **Flow Direction** | **Nearest-Neighbour** | Categorical D8 codes (1,2,4,8,16,32,64,128). Bilinear/cubic forbidden to prevent false codes. | `diagnostic_only=true`, `exclude_from_direct_numeric_model_input=true` |
| **Flow Accumulation** | **Bilinear Interpolation** | Continuous catchment cell count field. | Model Predictor Candidate |
| **Drainage Network** | **Binary Thresholding** | Derived on 100m grid (`fac_100m >= 500.0`). Binary UInt8 (1=stream, 0=non-stream). | Intermediate / Model Input |
| **Distance to Drainage** | **Euclidean Distance Transform** | Measured directly in metres at 100m resolution from 100m stream network. | Model Predictor Candidate |
| **Drainage Density** | **Square Moving Window** | Stream length per unit area (km/km²) in 5x5 window (500m width / 0.25 km² area). Underflow clipped to 0.0. | Model Predictor Candidate |
| **TWI** | **Physical Formula** | $\ln(a / \tan \beta)$ evaluated element-wise from 100m specific catchment area and 100m slope. | Model Predictor Candidate |
