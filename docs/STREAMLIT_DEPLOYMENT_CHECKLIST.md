# GeoSlide-JK — Streamlit Community Cloud Deployment Checklist

This document provides a step-by-step checklist to deploy the **GeoSlide-JK Streamlit Submission Companion Application** to Streamlit Community Cloud.

---

## 📋 Deployment Parameters

- **GitHub Repository**: `SauarbhSharma/GeoSlide-JK`
- **Branch**: `main`
- **Main Entrypoint Path**: `streamlit_app/streamlit_app.py`
- **Requirements File Path**: `streamlit_app/requirements.txt`
- **Theme Configuration**: `.streamlit/config.toml`

---

## 🛠️ Step-by-Step Deployment Guide

### Step 1: Push Repository to GitHub
Ensure the latest code and release tags are pushed to public GitHub:
```bash
git push -u origin main
git push origin --tags
```

### Step 2: Access Streamlit Community Cloud
1. Open your browser and navigate to [https://share.streamlit.io](https://share.streamlit.io).
2. Log in using your GitHub account (`SauarbhSharma`).

### Step 3: Configure New App
1. Click **"Create app"** or **"New app"**.
2. Select **"I already have an app"**.
3. Fill in the deployment form exactly as follows:
   - **Repository**: `SauarbhSharma/GeoSlide-JK`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app/streamlit_app.py`
   - **App URL** (Optional): Choose a custom slug (e.g. `geoslide-jk.streamlit.app`).

### Step 4: Advanced Settings Verification
1. Click **"Advanced settings..."**.
2. Verify Python version is set to **Python 3.11** or **3.10**.
3. Confirm no secret keys or environment variables are required (all compact assets are self-contained under `streamlit_app/assets/`).

### Step 5: Deploy & Verify
1. Click **"Deploy!"**.
2. Streamlit Cloud will build the container using `streamlit_app/requirements.txt`.
3. Upon completion, verify that all 6 sections navigate smoothly:
   - ✅ Section 1: Overview & Research Disclaimer
   - ✅ Section 2: Statewide Risk Explorer (Interactive Plotly Map)
   - ✅ Section 3: District Intelligence (All 20 Districts Dropdown)
   - ✅ Section 4: Location Risk Check (8 Corridors)
   - ✅ Section 5: Model Transparency (XGBoost Metrics)
   - ✅ Section 6: Data Sources & Limitations

---

## 🔍 Pre-Flight Verification Checklist

| Verification Item | Requirement | Status |
| :--- | :--- | :--- |
| **Path Compatibility** | Uses `pathlib.Path(__file__).resolve().parent` | **PASSED** |
| **No Drive Letters** | Zero absolute `D:\...` Windows paths | **PASSED** |
| **No Localhost Calls** | Self-contained asset reading, zero `http://127.0.0.1` API calls | **PASSED** |
| **Dependency File** | `streamlit_app/requirements.txt` beside entrypoint | **PASSED** |
| **Data Integrity** | All metrics derived from verified Phase 4 & 5 outputs | **PASSED** |
| **Disclaimer Present** | *"GeoSlide-JK is a research decision-support prototype..."* | **PASSED** |
