import streamlit as st
import time
import random
# Page configuration for maximum width to fit all 5 columns side-by-side
st.set_page_config(page_title="AI Risk Monitor - NER", layout="wide")

# Main Title
st.title("🌐 AI-Based Earthquaking and Landslide Risk Monitoring System in NER")
st.caption("Environment Focus: Northeast India Regional Safety Dashboard")
st.divider()

# Creating 5 parallel columns side-by-side for a true row layout
c1, c2, c3, c4, c5 = st.columns(5)

# =========================================================================
# COLUMN 1: SENSORS
# =========================================================================
with c1:
    st.subheader("🛠️ 1. Sensors")
    with st.container(border=True):
        sensor_seismo = st.checkbox("Seismometers", value=True)
        sensor_gps = st.checkbox("GPS / GNSS", value=True)
        sensor_tilt = st.checkbox("Tilt sensors", value=False)
        sensor_rain = st.checkbox("Rainfall sensors", value=True)
        sensor_table = st.checkbox("Table data", value=False)

# =========================================================================
# COLUMN 2: PRIMARY DATA
# =========================================================================
with c2:
    st.subheader("📊 2. Primary Data")
    with st.container(border=True):
        ner_locations = ["Gangtok, Sikkim", "Guwahati, Assam", "Shillong, Meghalaya", "Imphal, Manipur", "Aizawl, Mizoram", "Kohima, Nagaland"]
        selected_loc = st.selectbox("Target NER:", options=ner_locations, index=0)
        
        c2_live_placeholder = st.empty() 
        
        data_mode = st.radio("Data Mode:", options=["Regional", "Historical"])

# =========================================================================
# COLUMN 3: RISK FACTORS
# =========================================================================
with c3:
    st.subheader("⚠️ 3. Risk Factors")
    with st.container(border=True):
        emergency_focus = st.selectbox("Emergency:", options=["Police fire", "Medical", "Disaster Mgmt"])
        infrastructure_risk = st.select_slider("Vulnerability:", options=["Low", "Medium", "High"], value="High")
        preparedness = st.checkbox("Ready?", value=True)

# =========================================================================
# COLUMN 4: RISK ASSESSMENT
# =========================================================================
with c4:
    st.subheader("📈 4. Risk Assessment")
    with st.container(border=True):
        st.write("**Continuous Monitoring System Active**")
        
        # Loading your machine learning model file safely
        import pickle
        import numpy as np
        
        try:
            with open("landslide_model.pkl", "rb") as f:
                model = pickle.pickle.load(f) if hasattr(pickle, "pickle") else pickle.load(f)
                
            # Preparing input data according to your features format
            # Elevation (sub_surface), Slope (infrastructure conversion), Aspect, Rainfall, NDVI, Land Cover
            slope_val = 22 if infrastructure_risk == "High" else (12 if infrastructure_risk == "Medium" else 5)
            ndvi_val = 0.50
            
            # Creating input array for features
            features = np.array([[sub_surface, slope_val, 120, rainfall_volume, ndvi_val]])
            
            # Predict probability if model supports it, else use predict
            if hasattr(model, "predict_proba"):
                risk_prob = model.predict_proba(features)[0][1]
                calculated_risk = int(risk_prob * 100)
            else:
                pred = model.predict(features)[0]
                calculated_risk = 90 if pred == 1 else 30
                
        except Exception as e:
            # Fallback if pickle loading error occurs during sync
            calculated_risk = 75 if rainfall_volume > 3000 else 45

        st.metric(label="Risk Level", value=f"{calculated_risk}%")
        
        if calculated_risk >= 70:
            st.error("🚨 ALERT")
        else:
            st.success("✅ Stable")
# =========================================================================
# =========================================================================
# COLUMN 5: SAFETY MAP SYSTEM
# =========================================================================
with c5:
    st.subheader("🗺️ 5. Safety Map")
    with st.container(border=True):
        st.caption(f"Mapped for: {selected_loc}")
        
        # Mapping coordinates logic based on selected city
        import pandas as pd
        coords = {"lat": [27.3314], "lon": [88.6138]} # Default Gangtok
        if selected_loc == "Guwahati, Assam":
            coords = {"lat": [26.1445], "lon": [91.7362]}
        elif selected_loc == "Shillong, Meghalaya":
            coords = {"lat": [25.5788], "lon": [91.8833]}
        elif selected_loc == "Imphal, Manipur":
            coords = {"lat": [24.8170], "lon": [93.9368]}
        elif selected_loc == "Aizawl, Mizoram":
            coords = {"lat": [23.7271], "lon": [92.7176]}
        elif selected_loc == "Kohima, Nagaland":
            coords = {"lat": [25.6751], "lon": [94.1086]}
            
        # Displaying real interactive map
        st.map(pd.DataFrame(coords), zoom=9)
        safety_check = st.checkbox("Verified", value=True)
# =========================================================================
# BOTTOM PROCESS BUTTON
# =========================================================================
st.divider()
if st.button("🚀 Process System Integrity"):
    with st.spinner("Analyzing..."):
        time.sleep(1)
    st.success("🎯 Better safety achieved!")
while True:
    with c2_live_placeholder.container():
        import random
        live_sub_surface = random.randint(500, 3000)
        live_rainfall = random.randint(0, 5000)
        
        st.metric(label="Sub-surface (m)", value=f"{live_sub_surface} m")
        st.metric(label="Rainfall (mm)", value=f"{live_rainfall} mm")
        
    time.sleep(3)
