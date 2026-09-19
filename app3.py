import streamlit as st
import time

# Page configuration for a wide horizontal split layout
st.set_page_config(page_title="AI Risk Monitor - NER", layout="wide")

# Main Dashboard Title
st.title("🌐 AI-Based Earthquaking and Landslide Risk Monitoring System in NER")
st.caption("Environment Focus: Northeast India Regional Safety Dashboard")
st.divider()

# Splitting layout into two parallel columns (Left and Right sides)
col1, col2 = st.columns(2)

# =========================================================================
# LEFT COLUMN (Sections 1, 2, and 3)
# =========================================================================
with col1:
    # 1. SENSORS SECTION
    st.header("🛠️ 1. Sensors")
    with st.container(border=True):
        st.write("Configure active tracking sensors:")
        sensor_seismo = st.checkbox("Seismometers (Earthquake tracking)", value=True)
        sensor_gps = st.checkbox("GPS / GNSS (Ground movement)", value=True)
        sensor_tilt = st.checkbox("Tilt sensors (Slope instability)", value=False)
        sensor_rain = st.checkbox("Rainfall sensors (Precipitation)", value=True)
        sensor_table = st.checkbox("Table data feeds", value=False)

    # 2. PRIMARY DATA SECTION
    st.header("📊 2. Primary Data")
    with st.container(border=True):
        ner_locations = [
            "Gangtok, Sikkim", "Guwahati, Assam", "Shillong, Meghalaya", 
            "Imphal, Manipur", "Aizawl, Mizoram", "Kohima, Nagaland"
        ]
        selected_loc = st.selectbox("Target NER Location:", options=ner_locations, index=0)
        sub_surface = st.slider("Sub-surface Data Level (meters)", min_value=100, max_value=3000, value=1600)
        rainfall_volume = st.slider("Rainfall Data (mm)", min_value=0, max_value=5000, value=3500)
        data_mode = st.radio("Data Mode Selection:", options=["Regional statistics", "Historical data"])

    # 3. RISK FACTORS SECTION
    st.header("⚠️ 3. Risk Factors")
    with st.container(border=True):
        emergency_focus = st.selectbox(
            "Emergency Services Readiness:", 
            options=["Police fire", "Medical emergencies", "Natural disaster management"]
        )
        infrastructure_risk = st.select_slider(
            "Infrastructure Vulnerability Level:", 
            options=["Low Risk", "Medium Risk", "High Risk"], 
            value="High Risk"
        )
        preparedness = st.checkbox("Disaster preparedness protocols deployed?", value=True)


# =========================================================================
# RIGHT COLUMN (Sections 4 and 5)
# =========================================================================
with col2:
    # 4. RISK ASSESSMENT SECTION
    st.header("📈 4. Risk Assessment")
    with st.container(border=True):
        st.write("**Continuous Monitoring System Active**")
        
        # Simple evaluation logic updating state based on active telemetry inputs
        calculated_risk = 50
        if rainfall_volume > 3000 or infrastructure_risk == "High Risk":
            calculated_risk = 85
        if sensor_seismo and rainfall_volume > 4000:
            calculated_risk = 92
            
        st.metric(label="Calculated Risk Level (%)", value=f"{calculated_risk}%")
        
        if calculated_risk >= 70:
            st.error(f"🚨 ALERT GENERATED: High Risk detected at {calculated_risk}%! Threshold exceeded for {selected_loc}.")
        else:
            st.success(f"✅ System Stable: Risk Level is at {calculated_risk}% (Within safe bounds).")

    # 5. SAFETY MAP SYSTEM SECTION
    st.header("🗺️ 5. Safety Map System")
    with st.container(border=True):
        st.info(f"📍 Mapped across North East India for: {selected_loc}")
        st.markdown("### 🌐 Map of NER Placeholder")
        st.caption("Visualizing telemetry from active sensors.")
        safety_check = st.checkbox("Safety and Security Verified for NER", value=True)

    # FINAL SYSTEM OBJECTIVE INTERACTIVE TRIGGERS
    st.write("")
    if st.button("🚀 Process System Integrity"):
        with st.spinner("Analyzing telemetry..."):
            time.sleep(1)
        st.success("🎯 **Better safety and disaster management achieved!**")
