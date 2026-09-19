import streamlit as st
import time

# పేజీ సెట్టింగ్స్
st.set_page_config(page_title="AI Risk Monitor - NER", layout="centered")

# ప్రధాన టైటిల్ (Main Title)
st.title("🌐 AI-Based Earthquaking and Landslide Risk Monitoring System in NER")
st.caption("Environment Focus: Northeast India Regional Safety Dashboard")
st.divider()

# =========================================================================
# 1. SENSORS SECTION
# =========================================================================
st.header("🛠️ 1. Sensors")
with st.container(border=True):
    st.write("Configure active tracking sensors in the NER region:")
    
    # ఇంటరాక్టివ్ చెక్‌బాక్స్‌లు
    sensor_seismo = st.checkbox("Seismometers (Earthquake tracking)", value=True)
    sensor_gps = st.checkbox("GPS / GNSS (Ground movement)", value=True)
    sensor_tilt = st.checkbox("Tilt sensors (Slope instability)", value=False)
    sensor_rain = st.checkbox("Rainfall sensors (Precipitation)", value=True)
    sensor_table = st.checkbox("Table data feeds (Historical records)", value=False)

# =========================================================================
# 2. PRIMARY DATA SECTION
# =========================================================================
st.header("📊 2. Primary Data")
with st.container(border=True):
    # లొకేషన్ డ్రాప్‌డౌన్ (NER ఊర్ల పేర్లు ఎప్పుడూ ఉండేలా)
    ner_locations = [
        "Gangtok, Sikkim", "Guwahati, Assam", "Shillong, Meghalaya", 
        "Imphal, Manipur", "Aizawl, Mizoram", "Kohima, Nagaland"
    ]
    selected_loc = st.selectbox("Target NER Location Location:", options=ner_locations, index=0)
    
    # ప్రైమరీ డేటా ఇన్‌పుట్స్
    sub_surface = st.slider("Sub-surface Data Level (meters)", min_value=100, max_value=3000, value=1600)
    rainfall_volume = st.slider("Rainfall Data (mm)", min_value=0, max_value=5000, value=3500)
    
    data_mode = st.radio("Data Mode Selection:", options=["Regional statistics", "Historical data"])

# =========================================================================
# 3. RISK FACTORS SECTION
# =========================================================================
st.header("⚠️ 3. Risk Factors")
with st.container(border=True):
    emergency_focus = st.selectbox(
        "Emergency Services Readiness:", 
        options=["Police fire", "Medical emergencies", "Natural disaster management"]
    )
    infrastructure_risk = st.select_slider(
        "Infrastructure Vulnerability Data Level:", 
        options=["Low Risk", "Medium Risk", "High Risk"], 
        value="High Risk"
    )
    preparedness = st.checkbox("Disaster preparedness protocols deployed?", value=True)

# =========================================================================
# 4. RISK ASSESSMENT SECTION
# =========================================================================
st.header("📈 4. Risk Assessment")
with st.container(border=True):
    st.write("**Continuous Monitoring System Active**")
    
    # మీ పాత లాజిక్ ప్రకారం వాల్యూస్ ఆధారంగా రిస్క్ శాతాన్ని లెక్కించడం
    # ఇక్కడ ఒక బేసిక్ AI డెమో లాజిక్ రాశాను
    calculated_risk = 50
    if rainfall_volume > 3000 or infrastructure_risk == "High Risk":
        calculated_risk = 85
    if sensor_seismo and rainfall_volume > 4000:
        calculated_risk = 92
        
    st.metric(label="Calculated Risk Level (%)", value=f"{calculated_risk}%")
    
    # Threshold generation & Alert generation
    if calculated_risk >= 70:
        st.error(f"🚨 ALERT GENERATED: High Risk detected at {calculated_risk}%! Threshold exceeded for {selected_loc}.")
    else:
        st.success(f"✅ System Stable: Risk Level is at {calculated_risk}% (Within safe bounds).")

# =========================================================================
# 5. SAFETY MAP SYSTEM SECTION
# =========================================================================
st.header("🗺️ 5. Safety Map System")
with st.container(border=True):
    st.info(f"📍 Displaying location-wise risk on the map for: {selected_loc}")
    
    # మ్యాప్ ప్లేస్‌హోల్డర్ (భవిష్యత్తులో ఇక్కడ నిజమైన మ్యాప్ లింక్ చేయవచ్చు)
    st.markdown("### 🌐 Map of NER")
    st.caption(f"Visualizing telemetry from active sensors for {selected_loc} coordinates.")
    
    safety_check = st.checkbox("Safety and Security Verified for NER", value=True)

# =========================================================================
# FINAL OBJECTIVE OUTPUT
# =========================================================================
st.divider()
if st.button("🚀 Process System Integrity Click to Verify"):
    with st.spinner("Analyzing telemetry..."):
        time.sleep(1)
    st.success("🎯 **Better safety and disaster management successfully achieved!**")
