# GeoSlide-JK Public UI Verification Matrix

## Route & Interface Verification

| # | Route / Element | Target Behavior | Local Verification | Production Requirement |
|:---|:---|:---|:---|:---|
| 1 | `/` (Home) | Statewide command-centre dashboard, MapLibre map, top nav | PASS | Render Web Service |
| 2 | `/explorer` | Fullscreen MapLibre spatial explorer | PASS | Render Web Service |
| 3 | `/districts` | 20-district intelligence dashboard & selector | PASS | Render Web Service |
| 4 | `/rainfall` | Dynamic rainfall scenario monitor & sampler | PASS | Render Web Service |
| 5 | `/location-check` | Point-specific location risk query & advisory | PASS | Render Web Service |
| 6 | `/transparency` | Phase 4 XGBoost metrics (ROC-AUC 0.8694, 5 folds) | PASS | Render Web Service |
| 7 | `/status` | Data system endpoint status monitor | PASS | Render Web Service |
| 8 | CARTO Basemap | CartoDB dark matter tile overlay | PASS | Same-origin |
| 9 | Boundary Layers | J&K UT and 20 district GeoJSON polygons | PASS | Same-origin |
| 10 | Susceptibility Probability | 100m raster tile overlay (`/api/v1/tiles/...`) | PASS | Same-origin |
| 11 | Susceptibility Class | 5-class color-coded raster tile overlay | PASS | Same-origin |
| 12 | Dynamic Hazard Index | Combined susceptibility × rainfall anomaly | PASS | Same-origin |
| 13 | Dynamic Hazard Class | 5-class dynamic hazard raster tile overlay | PASS | Same-origin |
| 14 | Map Click Inspector | Point-sampling popup with elevation/slope/susc/hazard | PASS | Same-origin |
| 15 | Streamlit Wrapper | Embedded iframe rendering authoritative Next.js app | PASS | Streamlit Community Cloud |
