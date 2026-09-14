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
