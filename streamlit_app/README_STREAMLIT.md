# GeoSlide-JK — Streamlit Submission Companion Application

This standalone Streamlit application is designed for institutional submission and deployment on Streamlit Community Cloud.

## Deployment Details

- **GitHub Repository**: `SauarbhSharma/GeoSlide-JK`
- **Branch**: `main`
- **Main File Path**: `streamlit_app/streamlit_app.py`
- **Requirements File Path**: `streamlit_app/requirements.txt`

## Local Execution Instructions

To launch the application locally:

```bash
cd D:\Projects\GeoSlide_JK
streamlit run streamlit_app/streamlit_app.py
```

The application will open in your default browser at `http://localhost:8501`.

## Application Features

1. **Project Overview**: High-level abstract, grid details, and research disclaimer.
2. **Statewide Risk Explorer**: Interactive map of J&K with district boundaries, static susceptibility ratings, and dynamic hazard scenario overlays using Plotly & PyDeck.
3. **District Intelligence**: Detailed breakdown across all 20 UT districts.
4. **Location Risk Check**: Preset locations along critical corridors (e.g. Panthyal, NH-44) with sampled terrain, susceptibility, and rainfall proxy parameters.
5. **Model Transparency**: Phase 4 XGBoost 5-fold spatial cross-validation metrics and feature importances.
6. **Data Sources & Limitations**: Transparent description of inputs and proxy limitations.
