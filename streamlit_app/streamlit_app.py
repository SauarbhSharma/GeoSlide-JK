import json
import csv
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="GeoSlide-JK v1.0.0 — Landslide Intelligence",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# PATH DEFINITIONS & DATA LOADERS (ST.CACHE_DATA)
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

@st.cache_data
def load_district_geojson():
    path = ASSETS_DIR / "jk_districts_simplified.geojson"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@st.cache_data
def load_district_summary():
    path = ASSETS_DIR / "district_summary.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data
def load_preset_locations():
    path = ASSETS_DIR / "preset_locations.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data
def load_model_metrics():
    path = ASSETS_DIR / "model_metrics.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@st.cache_data
def load_feature_importance():
    path = ASSETS_DIR / "feature_importance.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Load cached data
district_geojson = load_district_geojson()
df_districts = load_district_summary()
df_presets = load_preset_locations()
metrics = load_model_metrics()
features = load_feature_importance()

# -----------------------------------------------------------------------------
# NAVIGATION SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.title("🏔️ GeoSlide-JK")
st.sidebar.caption("Full-J&K Landslide Intelligence Engine")
st.sidebar.markdown("---")

navigation = st.sidebar.radio(
    "Navigation Menu",
    [
        "1. Project Overview",
        "2. Statewide Risk Explorer",
        "3. District Intelligence",
        "4. Location Risk Check",
        "5. Model Transparency",
        "6. Data Sources & Limitations"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**GeoSlide-JK v1.0.0**\n\n"
    "Master Analysis Grid: 100m EPSG:32643\n"
    "Spatial CV ROC-AUC: **0.8694**\n"
    "Active UT Districts: **20**"
)

# -----------------------------------------------------------------------------
# SECTION 1: PROJECT OVERVIEW
# -----------------------------------------------------------------------------
if navigation == "1. Project Overview":
    st.title("🏔️ GeoSlide-JK v1.0.0 — Project Overview")
    st.subheader("Research Decision-Support Prototype for Jammu & Kashmir")
    
    st.warning(
        "⚠️ **Research Disclaimer**: GeoSlide-JK is a research decision-support prototype "
        "and is not an official government warning system."
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Abstract & System Purpose
        **GeoSlide-JK** is a state-of-the-art geospatial intelligence system designed to model, quantify, and visualize 
        landslide susceptibility and dynamic trigger risks across all **20 districts** of the Union Territory of Jammu and Kashmir.
        
        The platform unifies multi-source satellite Earth observation, high-resolution topography (**Copernicus GLO-30 DEM**), 
        geological structures (**GSI 50K Lithology & Tectonic Faults**), land cover (**ESA WorldCover 2021**), and historical 
        landslide occurrences (**NGDR Inventory**) into a standardized **100m EPSG:32643 UTM Zone 43N Master Analysis Grid**.
        """)
        
        st.markdown("""
        #### Core System Pillars
        1. **Static Susceptibility Intelligence**: Powered by an engineered **30-Predictor XGBoost Machine Learning Model** evaluated via 5-fold spatial district-block cross-validation (**ROC-AUC: 0.8694**).
        2. **Dynamic Hazard Scenario Modeling**: Combines static susceptibility with 24-hour rainfall accumulation and climatological IMD 90th percentile (P90) anomaly ratios ($R_{anomaly} = P_{24h} / P_{90}$).
        3. **Multi-Scale Decision Support**: Provides statewide grid exploration, district-level summaries, and point-specific location risk checks along vulnerable transportation corridors like **NH-44**.
        """)

    with col2:
        st.metric(label="Coverage Domain", value="20 UT Districts")
        st.metric(label="Analysis Grid", value="100m EPSG:32643")
        st.metric(label="Valid Land Cells", value="4,619,191 cells")
        st.metric(label="XGBoost Spatial ROC-AUC", value="0.8694")
        st.metric(label="Model Status", value="Verified (Phase 4)")
        st.metric(label="Dynamic Rainfall Status", value="Scenario / Proxy Mode")

# -----------------------------------------------------------------------------
# SECTION 2: STATEWIDE RISK EXPLORER
# -----------------------------------------------------------------------------
elif navigation == "2. Statewide Risk Explorer":
    st.title("🗺️ Statewide Risk Explorer")
    st.caption("Interactive 20-District Spatial Visualization of Susceptibility & Dynamic Hazard Scenarios")
    
    col_ctrl, col_map = st.columns([1, 3])
    
    with col_ctrl:
        st.markdown("#### Layer Controls")
        selected_layer = st.radio(
            "Select Active Map Layer",
            ["District Susceptibility Rating", "Dynamic Hazard Scenario Class", "Landslide Risk Hotspots"]
        )
        
        st.markdown("---")
        st.markdown("#### Legend")
        if selected_layer == "District Susceptibility Rating":
            st.markdown("""
            - 🟢 **Very Low / Low**: Jammu, Samba, Srinagar, Pulwama
            - 🟡 **Low to Moderate**: Udhampur, Anantnag, Baramulla
            - 🟠 **Moderate to High**: Ramban, Doda, Kishtwar, Reasi, Poonch, Kupwara
            """)
        elif selected_layer == "Dynamic Hazard Scenario Class":
            st.markdown("""
            - 🔵 **Low Scenario**: Normal precipitation baseline
            - 🟡 **Moderate Scenario**: Moderate rainfall accumulation ($R_{anomaly} \ge 1.0$)
            - 🔴 **High Scenario**: Intense rainfall ($R_{anomaly} \ge 1.5$) along steep slopes
            """)
        else:
            st.markdown("""
            - 🔴 **Critical Corridors**: NH-44 Ramban-Banihal stretch, Chenab Valley
            - 🟠 **Secondary Risk**: Pir Panjal Range, Kupwara Border Slopes
            """)
            
        st.info("💡 **Interactive Guide**: Hover over district polygons to inspect mean susceptibility probability and high-risk coverage.")

    with col_map:
        if not df_districts.empty:
            # Create Plotly Mapbox choropleth
            fig = px.choropleth_mapbox(
                df_districts,
                geojson=district_geojson,
                locations="display_name",
                featureidkey="properties.display_name",
                color="mean_susceptibility" if selected_layer != "Dynamic Hazard Scenario Class" else "high_risk_area_pct",
                color_continuous_scale="YlOrRd" if selected_layer != "Dynamic Hazard Scenario Class" else "Viridis",
                range_color=[0.1, 0.7] if selected_layer != "Dynamic Hazard Scenario Class" else [0, 50],
                mapbox_style="carto-darkmatter",
                zoom=6.8,
                center={"lat": 33.7, "lon": 75.0},
                opacity=0.65,
                hover_name="display_name",
                hover_data={
                    "display_name": False,
                    "susceptibility_rating": True,
                    "mean_susceptibility": ":.4f",
                    "high_risk_area_pct": ":.1f%",
                    "dynamic_hazard_class": True
                },
                labels={
                    "mean_susceptibility": "Mean Susceptibility",
                    "high_risk_area_pct": "High Risk Area %",
                    "susceptibility_rating": "Rating",
                    "dynamic_hazard_class": "Hazard Class"
                }
            )
            fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                height=600,
                paper_bgcolor="#0f172a",
                plot_bgcolor="#0f172a",
                font={"color": "#f8fafc"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("District boundary layers are loading or unavailable.")

# -----------------------------------------------------------------------------
# SECTION 3: DISTRICT INTELLIGENCE
# -----------------------------------------------------------------------------
elif navigation == "3. District Intelligence":
    st.title("📊 District Intelligence Summary")
    st.caption("Detailed Susceptibility & Dynamic Hazard Breakdown across 20 J&K UT Districts")
    
    if not df_districts.empty:
        district_names = sorted(df_districts["display_name"].tolist())
        selected_district = st.selectbox("Select District for Deep-Dive Analysis", district_names, index=district_names.index("Ramban") if "Ramban" in district_names else 0)
        
        dist_row = df_districts[df_districts["display_name"] == selected_district].iloc[0]
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        
        with m_col1:
            st.metric(
                label="Mean Susceptibility Prob",
                value=f"{dist_row['mean_susceptibility']:.4f}"
            )
        with m_col2:
            st.metric(
                label="Susceptibility Rating",
                value=dist_row['susceptibility_rating']
            )
        with m_col3:
            st.metric(
                label="High-Risk Slope Area %",
                value=f"{dist_row['high_risk_area_pct']:.1f}%"
            )
        with m_col4:
            st.metric(
                label="Dynamic Hazard Class",
                value=dist_row['dynamic_hazard_class']
            )
            
        st.markdown("---")
        
        st.subheader("All 20 District Comparative Table")
        
        # Display formatted table for all districts
        st.dataframe(
            df_districts.style.highlight_max(subset=["high_risk_area_pct"], color="#991b1b")
                              .highlight_min(subset=["high_risk_area_pct"], color="#166534"),
            use_container_width=True,
            height=400
        )
    else:
        st.error("District summary data file is unavailable.")

# -----------------------------------------------------------------------------
# SECTION 4: LOCATION RISK CHECK
# -----------------------------------------------------------------------------
elif navigation == "4. Location Risk Check":
    st.title("📍 Location Risk Check & Corridor Analysis")
    st.caption("Point-Specific Susceptibility & Dynamic Trigger Sampling along Critical Corridors")
    
    st.info(
        "ℹ️ **Notice**: Dynamic rainfall-related metrics displayed here represent **Scenario/Proxy — not live operational rainfall.**"
    )
    
    if not df_presets.empty:
        preset_names = df_presets["name"].tolist()
        selected_preset_name = st.selectbox("Select Preset High-Vulnerability Location", preset_names)
        
        p_row = df_presets[df_presets["name"] == selected_preset_name].iloc[0]
        
        r_col1, r_col2 = st.columns([1, 1])
        
        with r_col1:
            st.markdown("### 🏞️ Terrain & Location Parameters")
            st.write(f"**Location Name**: {p_row['name']}")
            st.write(f"**District**: {p_row['district']}")
            st.write(f"**Coordinates**: Latitude {p_row['latitude']:.4f}°N, Longitude {p_row['longitude']:.4f}°E")
            st.write(f"**Elevation**: {p_row['elevation_m']} m ASL")
            st.write(f"**Slope Gradient**: {p_row['slope_deg']}°")
            
            st.markdown("---")
            st.markdown("### 🎯 Static Susceptibility Rating")
            st.metric(label="Susceptibility Probability", value=f"{p_row['susc_prob']:.4f}")
            st.metric(label="Susceptibility Class", value=p_row['susc_class'])

        with r_col2:
            st.markdown("### 🌧️ Dynamic Rainfall Scenario Parameters")
            st.write(f"**24h Rainfall Accumulation Proxy**: {p_row['rainfall_24h_mm']} mm")
            st.write(f"**IMD P90 Baseline Proxy**: {p_row['p90_baseline_mm']} mm")
            st.write(f"**Precipitation Anomaly Ratio ($R_{{anomaly}}$)**: {p_row['anomaly_ratio']:.2f}")
            
            st.markdown("---")
            st.markdown("### ⚡ Combined Dynamic Hazard Rating")
            st.metric(label="Dynamic Hazard Index ($H_{{dyn}}$)", value=f"{p_row['hazard_index']:.4f}")
            st.metric(label="Dynamic Hazard Class", value=p_row['hazard_class'])
            
        st.markdown("---")
        st.markdown("### 🛡️ Research Precautionary Guidance")
        if p_row['hazard_class'] in ["High", "Critical"]:
            st.error(
                "🚨 **High Vulnerability Advisory**: Steep un-engineered slope cuts along this corridor exhibit "
                "elevated instability potential under intense precipitation scenarios. Avoid non-essential travel during heavy rainfall."
            )
        else:
            st.success(
                "✅ **Moderate/Low Vulnerability Advisory**: Standard slope monitoring applies. Continue verifying local weather reports."
            )
    else:
        st.error("Preset location data file unavailable.")

# -----------------------------------------------------------------------------
# SECTION 5: MODEL TRANSPARENCY
# -----------------------------------------------------------------------------
elif navigation == "5. Model Transparency":
    st.title("🔬 Model Transparency & Performance Metrics")
    st.caption("Phase 4 XGBoost Spatial Cross-Validation & Predictor Isolation Audit")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric(label="Spatial CV ROC-AUC", value=f"{metrics.get('spatial_cv_roc_auc', 0.8694):.4f}")
    with col_m2:
        st.metric(label="Spatial CV PR-AUC", value=f"{metrics.get('spatial_cv_pr_auc', 0.2760):.4f}")
    with col_m3:
        st.metric(label="Brier Reliability Score", value=f"{metrics.get('brier_score', 0.1788):.4f}")
    with col_m4:
        st.metric(label="Total Predictor Features", value=metrics.get('predictors', 30))

    st.markdown("---")
    
    col_folds, col_imp = st.columns([1, 1])
    
    with col_folds:
        st.subheader("5-Fold Spatial District Block Cross-Validation")
        st.markdown("Out-of-fold evaluations across spatially disjoint district blocks:")
        
        fold_data = metrics.get("fold_roc_auc", {})
        df_folds = pd.DataFrame(list(fold_data.items()), columns=["Spatial District Block Fold", "ROC-AUC"])
        
        fig_fold = px.bar(
            df_folds,
            x="Spatial District Block Fold",
            y="ROC-AUC",
            text="ROC-AUC",
            color="ROC-AUC",
            color_continuous_scale="Blues",
            range_y=[0.0, 1.0]
        )
        fig_fold.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font={"color": "#f8fafc"},
            height=380
        )
        st.plotly_chart(fig_fold, use_container_width=True)

    with col_imp:
        st.subheader("Top Predictor Feature Importance")
        st.markdown("Engineered morphometric, geological, and land-cover features:")
        
        if features:
            df_imp = pd.DataFrame(features)
            fig_imp = px.bar(
                df_imp,
                x="importance",
                y="feature",
                orientation="h",
                color="category",
                labels={"importance": "XGBoost Importance", "feature": "Predictor Feature"}
            )
            fig_imp.update_layout(
                paper_bgcolor="#0f172a",
                plot_bgcolor="#0f172a",
                font={"color": "#f8fafc"},
                yaxis={"categoryorder": "total ascending"},
                height=380
            )
            st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("---")
    st.subheader("🔒 Feature Leakage & Isolation Safeguards")
    st.markdown("""
    - **NLSM Benchmark Isolation**: The pre-existing NLSM susceptibility raster was excluded from the predictor feature stack.
    - **Geographic Coordinate Exclusion**: Latitude and Longitude were strictly excluded as predictors to prevent spatial overfitting.
    - **Exposure Feature Isolation**: Population density, settlements, and health facilities were excluded from the susceptibility model stack.
    - **Spatial Block Cross-Validation**: Spatial district block partitioning prevented geographic leakage between training and evaluation sets.
    """)

# -----------------------------------------------------------------------------
# SECTION 6: DATA SOURCES AND LIMITATIONS
# -----------------------------------------------------------------------------
elif navigation == "6. Data Sources & Limitations":
    st.title("📚 Data Sources & System Limitations")
    
    st.markdown("""
    ### Primary Geospatial Data Sources
    - **Copernicus GLO-30 DEM**: 30m Global Digital Elevation Model (mosaicked and resampled to 100m EPSG:32643).
    - **ESA WorldCover 2021**: 10m global land cover product providing land cover fraction predictors.
    - **GSI Lithology & Tectonic Database**: Geological Survey of India 50K lithology units, fault lines, thrusts, and lineaments.
    - **NGDR Landslide Inventory**: National Geo-hazard Data Repository historical landslide point and polygon occurrences.
    - **Exposure Datasets**: Major roads (NH-44), settlements, and critical health infrastructure.
    
    ---
    
    ### Key Methodological Limitations
    1. **Static Model Scope**: The machine learning model strictly predicts **static spatial susceptibility**. It does not forecast time-of-occurrence.
    2. **Scenario / Proxy Rainfall Mode**: Dynamic 24-hour rainfall accumulation and IMD P90 baseline percentiles represent **research proxy products** designed for scenario demonstration. Operational GPM/IMD satellite stream integration is planned for future releases.
    3. **Resolution Constraint**: The 100m analysis grid is optimized for regional UT decision support. Site-specific geotechnical engineering slope stability requires fine-scale ground survey.
    4. **Non-Warning Disclaimer**: **GeoSlide-JK is a research decision-support prototype and is not an official government warning system.**
    """)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption("GeoSlide-JK v1.0.0 — Public Release & Submission Companion Application | Jammu & Kashmir UT")
