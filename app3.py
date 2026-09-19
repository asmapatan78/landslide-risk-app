"""
AI-Based Landslide Risk Monitoring — Streamlit Web App
--------------------------------------------------------
Loads the model trained in NER_Landslide_Risk_Model.ipynb and lets a user
enter terrain/climate values (or pick a preset location) to get a
landslide risk percentage.

Run locally:   streamlit run app.py
Deploy free:   Streamlit Community Cloud (see README.md)
"""

import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="NER Landslide Risk Monitor", page_icon="🏔️", layout="centered")

MODEL_PATH = "landslide_model.pkl"
FEATURES_PATH = "landslide_model_features.pkl"

st.title("🏔️ AI Landslide Risk Monitor — Northeast India")
st.caption(
    "Susceptibility model trained on terrain, rainfall and vegetation data. "
    "Output is a static risk score, not a live weather-triggered alert."
)

# ---------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------
if not (os.path.exists(MODEL_PATH) and os.path.exists(FEATURES_PATH)):
    st.error(
        "Model files not found. Place `landslide_model.pkl` and "
        "`landslide_model_features.pkl` (exported from the Colab notebook) "
        "in the same folder as this app."
    )
    st.stop()

model = joblib.load(MODEL_PATH)
FEATURES = joblib.load(FEATURES_PATH)

# ---------------------------------------------------------------------
# Preset NER hotspots for quick testing
# ---------------------------------------------------------------------
PRESETS = {
    "-- Manual entry --": None,
    "Cherrapunji, Meghalaya": {"elevation": 1300, "slope": 42, "aspect": 180, "rainfall_mm": 11000, "ndvi": 0.35, "landcover": 20},
    "Shillong-Guwahati Highway": {"elevation": 900, "slope": 38, "aspect": 210, "rainfall_mm": 3200, "ndvi": 0.30, "landcover": 20},
    "Aizawl, Mizoram": {"elevation": 1100, "slope": 35, "aspect": 160, "rainfall_mm": 2500, "ndvi": 0.40, "landcover": 20},
    "Gangtok, Sikkim": {"elevation": 1600, "slope": 45, "aspect": 200, "rainfall_mm": 3500, "ndvi": 0.45, "landcover": 20},
    "Flat stable area (control)": {"elevation": 100, "slope": 3, "aspect": 90, "rainfall_mm": 1400, "ndvi": 0.65, "landcover": 40},
}

st.subheader("1. Choose a location preset or enter values manually")
preset_name = st.selectbox("Preset location", list(PRESETS.keys()))
preset = PRESETS[preset_name]

col1, col2 = st.columns(2)
with col1:
    elevation = st.number_input("Elevation (m)", 0, 6000, value=preset["elevation"] if preset else 800)
    slope = st.slider("Slope (degrees)", 0, 70, value=preset["slope"] if preset else 20)
    aspect = st.slider("Aspect / slope direction (degrees, 0=N)", 0, 360, value=preset["aspect"] if preset else 180)
with col2:
    rainfall_mm = st.number_input("Annual rainfall (mm)", 200, 12000, value=preset["rainfall_mm"] if preset else 2000)
    ndvi = st.slider("NDVI — vegetation greenness (-0.1 bare, 0.9 dense forest)", -0.1, 0.9, value=preset["ndvi"] if preset else 0.5, step=0.01)
    landcover = st.selectbox(
        "Land cover class",
        options=[10, 20, 30, 40, 50],
        format_func=lambda x: {10: "Tree cover", 20: "Shrubland", 30: "Grassland", 40: "Cropland", 50: "Built-up"}[x],
        index=[10, 20, 30, 40, 50].index(preset["landcover"]) if preset else 1,
    )

input_row = pd.DataFrame([{
    "elevation": elevation, "slope": slope, "aspect": aspect,
    "rainfall_mm": rainfall_mm, "ndvi": ndvi, "landcover": landcover,
}])[FEATURES]

st.subheader("2. Predicted risk")
if st.button("Calculate landslide risk", type="primary"):
    risk_pct = model.predict_proba(input_row)[0][1] * 100

    if risk_pct < 25:
        level, color = "LOW", "green"
    elif risk_pct < 50:
        level, color = "MODERATE", "orange"
    elif risk_pct < 75:
        level, color = "HIGH", "red"
    else:
        level, color = "VERY HIGH", "red"

    st.metric("Landslide risk", f"{risk_pct:.1f}%")
    st.markdown(f"**Risk level:** :{color}[{level}]")
    st.progress(min(int(risk_pct), 100))

    if risk_pct >= 50:
        st.warning(
            "High susceptibility score. This is a static model output, not a live alert — "
            "combine with real-time rainfall data and local authority guidance before acting on it."
        )

st.divider()
st.caption(
    "Model: trained in NER_Landslide_Risk_Model.ipynb on Random Forest / XGBoost using terrain "
    "(SRTM DEM), rainfall (CHIRPS) and vegetation (Sentinel-2 NDVI) features. "
    "This is a susceptibility (static risk) tool, not a real-time early warning system."
)
st.markdown("---")
st.info("ℹ️ **Project Information:** This AI-based system is designed to predict landslide susceptibility in Northeast India using environmental parameters. The model is trained and validated using the `ner_landslide_dataset.csv` dataset.")
st.subheader("🛡️ Landslide Mitigation & Safety Guidelines")
col_tip1, col_tip2 = st.columns(2)
with col_tip1:
    st.warning("🚨 **Early Warning Signs:**\n- New cracks appearing on buildings, roads, or retaining walls.\n- Tilting of trees, utility poles, or fences on slopes.\n- Sudden changes in creek water levels or muddy water flow.")
with col_tip2:
    st.error("🏃 **Emergency Actions:**\n1. Evacuate immediately if you hear rumbling sounds or suspect imminent danger.\n2. Stay informed via local authority alerts and weather updates.\n3. Avoid low-lying areas and steep slopes during heavy rainfall.")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# =========================================================
# STEP 1: Input Logic with Clear/Delete Functionality
# =========================================================
st.title("🏔️ AI Landslide Risk Monitor – Northeast India")
st.subheader("1. Choose a location preset or enter values manually")

preset = st.selectbox("Preset location", ["Custom Values", "Gangtok, Sikkim", "Guwahati, Assam", "Shillong, Meghalaya"])

if preset == "Gangtok, Sikkim":
    default_elevation = 1600
    default_slope = 22
    default_aspect = 120
    default_rainfall = 3500
    default_ndvi = 0.50
    default_land_cover = "Grassland"
    is_disabled = True

elif preset == "Guwahati, Assam":
    default_elevation = 55
    default_slope = 5
    default_aspect = 45
    default_rainfall = 1700
    default_ndvi = 0.40
    default_land_cover = "Shrubland"
    is_disabled = True

elif preset == "Shillong, Meghalaya":
    default_elevation = 1525
    default_slope = 18
    default_aspect = 90
    default_rainfall = 2400
    default_ndvi = 0.60
    default_land_cover = "Forest"
    is_disabled = True

else:
    default_elevation = 0
    default_slope = 0
    default_aspect = 0
    default_rainfall = 0
    default_ndvi = 0.0
    default_land_cover = "Shrubland"
    is_disabled = False
col1, col2 = st.columns(2)

with col1:
    elevation = st.number_input(
        "Elevation (m)",
        value=None if default_elevation == 0 else default_elevation,
        placeholder="Enter elevation...",
        disabled=is_disabled,
    )
    slope = st.slider(
        "Slope (degrees)",
        min_value=0,
        max_value=90,
        value=default_slope,
        disabled=is_disabled,
    )
    aspect = st.slider(
        "Aspect / slope direction (degrees, 0=N)",
        min_value=0,
        max_value=360,
        value=default_aspect,
        disabled=is_disabled,
    )

with col2:
    rainfall = st.number_input(
        "Annual rainfall (mm)",
        value=None if default_rainfall == 0 else default_rainfall,
        placeholder="Enter rainfall...",
        disabled=is_disabled,
    )
    ndvi = st.slider(
        "NDVI – vegetation greenness",
        min_value=-0.1,
        max_value=0.9,
        value=default_ndvi,
        step=0.01,
        disabled=is_disabled,
    )
    land_cover = st.selectbox(
        "Land cover class",
        ["Shrubland", "Forest", "Barren", "Grassland"],
        index=["Shrubland", "Forest", "Barren", "Grassland"].index(
            default_land_cover
        ),
        disabled=is_disabled,
    )

if not is_disabled:
    if st.button("🗑️ Clear All Custom Values"):
        st.rerun()

graph_elevation = elevation if elevation is not None else 0
graph_rainfall = rainfall if rainfall is not None else 0

# =========================================================
# STEP 2: Visualizations Section
# =========================================================
st.markdown("---")
st.subheader("📊 Current Location Feature Breakdown")

col_graph1, col_graph2, col_graph3 = st.columns(3)

with col_graph1:
    fig1, ax1 = plt.subplots(figsize=(4, 5))
    sns.barplot(
        x=["Elevation", "Rainfall"],
        y=[graph_elevation, graph_rainfall],
        palette="Reds_r",
        ax=ax1,
    )
    ax1.set_title("Elevation & Rainfall Scale", fontsize=10)
    st.pyplot(fig1)

with col_graph2:
    fig2, ax2 = plt.subplots(figsize=(4, 5))
    sns.barplot(
        x=["Slope", "Aspect"],
        y=[slope, aspect],
        palette="Oranges_r",
        ax=ax2,
    )
    ax2.set_title("Angles & Slopes (Degrees)", fontsize=10)
    st.pyplot(fig2)

with col_graph3:
    fig3, ax3 = plt.subplots(figsize=(4, 5))
    sns.barplot(x=["NDVI (Greenness)"], y=[ndvi], palette="Greens_r", ax=ax3)
    ax3.set_title("Vegetation Index", fontsize=10)
    ax3.set_ylim(-0.1, 1.0)
    st.pyplot(fig3)
