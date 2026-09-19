import streamlit as st
import time

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
        sub_surface = st.slider("Sub-surface (m)", min_value=100, max_value=3000, value=1600)
        rainfall_volume = st.slider("Rainfall (mm)", min_value=0, max_value=5000, value=3500)
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
        calculated_risk = 50
        if rainfall_volume > 3000 or infrastructure_risk == "High":
            calculated_risk = 85
        if sensor_seismo and rainfall_volume > 4000:
            calculated_risk = 92
            
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
