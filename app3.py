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
        st.subheader("📉 4. Risk Assessment")
        with st.container(border=True):
            st.write("**Continuous Monitoring System Active**")
            
            import joblib
            import numpy as np
            import pandas as pd
            
            MODEL_PATH = "landslide_model.pkl"
            FEATURES_PATH = "landslide_model_features.pkl"
            
            model = None
            FEATURES = None
            
            try:
                if os.path.exists(MODEL_PATH) and os.path.exists(FEATURES_PATH):
                    model = joblib.load(MODEL_PATH)
                    FEATURES = joblib.load(FEATURES_PATH)
            except Exception as e:
                pass
                
            c4_live_placeholder = st.empty()

# =====================================
# COLUMN 5: SAFETY MAP SYSTEM
# =====================================
with c5:
        st.subheader("🗺️ 5. Safety Map")
        with st.container(border=True):
            st.caption(f"Mapped for: {selected_loc}")
            
            coords_dict = {
                "Gangtok, Sikkim": {"lat": 27.3314, "lon": 88.6138},
                "Guwahati, Assam": {"lat": 26.1445, "lon": 91.7362},
                "Shillong, Meghalaya": {"lat": 25.5788, "lon": 91.8933},
                "Imphal, Manipur": {"lat": 24.8170, "lon": 93.9368},
                "Aizawl, Mizoram": {"lat": 23.7271, "lon": 92.7176},
                "Kohima, Nagaland": {"lat": 25.6586, "lon": 94.1027}
            }
            
            loc_coords = coords_dict.get(selected_loc, {"lat": 27.3314, "lon": 88.6138})
            map_df = pd.DataFrame([loc_coords])
            st.map(map_df, zoom=11, use_container_width=True)
st.divider()

if "rainfall_history" not in st.session_state:
    st.session_state.rainfall_history = []

# ---------------------------------------------------------------------
# LIVE DATA & MODE CONTROL LOOP
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# SMS & EMAIL ALERT CONFIGURATION
# ---------------------------------------------------------------------
import smtplib
from email.mime.text import MIMEText

def send_automated_alerts(risk_val, location, rainfall_val):
    # 1. REAL SMS ALERT (Twilio)
    try:
        from twilio.rest import Client
        account_sid = 'AC6344c392e383b1951a8941920a1ef0af'
        auth_token = '43553a1d8124c880ee7aa1630132df9e'
        client = Client(account_sid, auth_token)
        
        message_sms = client.messages.create(
            from_='+17372508034',
            body=f"🚨 SMS ALERT: High Landslide Risk ({risk_val}%) detected in {location} due to {rainfall_val}mm rainfall!",
            to='+919491850877'
        )
    except Exception as e:
        pass

    # 2. REAL WHATSAPP ALERT (Twilio WhatsApp Sandbox)
    try:
        message_wa = client.messages.create(
            from_='whatsapp:+17372508034',
            body=f"🚨 *LANDSLIDE ALERT* 🚨\n\n*Location:* {location}\n*Risk Level:* {risk_val}%\n*Rainfall:* {rainfall_val} mm\n\nStatus: Critical condition active! Take immediate safety measures.",
            to='whatsapp:+919491850877'
        )
    except Exception as e:
        pass

    try:
        from twilio.rest import Client
        account_sid = 'AC6344c392e383b1951a8941920a1ef0af'
        auth_token = '4353a1d8124c880ee7a4f0cee65db26a'
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            from_='+17372508034',
            body=f"🚨 ALERT: High Landslide Risk ({risk_val}%) detected in {location} due to {rainfall_val}mm rainfall.",
            to='+919491850877'
        )
    except:
        pass

# ---------------------------------------------------------------------
# LIVE DATA, MODE CONTROL & AUTOMATED ALERT LOOP
# ---------------------------------------------------------------------
alert_sent = False

# ---------------------------------------------------------------------
# LIVE DATA, MODE CONTROL & AUTOMATED ALERT LOOP
# ---------------------------------------------------------------------
alert_sent = False

while True:
    import random
    
    if data_mode == "Regional":
        live_elevation = 1600 if "Gangtok" in selected_loc else 1100
        live_slope = 45 if "Gangtok" in selected_loc else 35
        live_aspect = 200
        live_rainfall = random.randint(1500, 4500)
        live_ndvi = round(random.uniform(0.3, 0.6), 2)
        live_landcover = 20
        
        st.session_state.rainfall_history.append(live_rainfall)
        if len(st.session_state.rainfall_history) > 15:
            st.session_state.rainfall_history.pop(0)
            
        with c2_live_placeholder.container():
            st.metric(label="Sub-surface (m)", value=f"{1577} m")
            st.metric(label="Rainfall (mm)", value=f"{live_rainfall} mm")
            
            st.caption("📈 Live Rainfall Trend (mm)")
            st.line_chart(st.session_state.rainfall_history, height=130)
            
        with c4_live_placeholder.container():
            calculated_risk = 45
            
            if model is not None and FEATURES is not None:
                try:
                    input_row = pd.DataFrame([{
                        "elevation": live_elevation, "slope": live_slope, "aspect": live_aspect,
                        "rainfall_mm": live_rainfall, "ndvi": live_ndvi, "landcover": live_landcover
                    }])[FEATURES]
                    
                    risk_pct = model.predict_proba(input_row) * 100
                    calculated_risk = int(risk_pct)
                except:
                    calculated_risk = 80 if live_rainfall > 3500 else 45
            else:
                calculated_risk = 80 if live_rainfall > 3500 else 45
                
            st.metric(label="Risk Level", value=f"{calculated_risk}%")
            
            if calculated_risk >= 70:
                st.error("🚨 CRITICAL ALERT: High Landslide Susceptibility!")
                if not alert_sent:
                    st.toast("⚡ Triggering SMS & Email Alerts to Disaster Management Team...")
                    send_automated_alerts(calculated_risk, selected_loc, live_rainfall)
                    alert_sent = True
            else:
                st.success("✅ Stable Condition")
                alert_sent = False
                
        time.sleep(3)  # ఇది ఇప్పుడు కరెక్ట్‌గా Regional ఇఫ్ బ్లాక్ లోపల ఉంది

    elif data_mode == "Historical":
        with c2_live_placeholder.container():
            st.info("📅 Historical Mode Active")
            selected_date = st.date_input("Select Past Date:", value=None)
            
            st.caption("📊 Historical Monthly Average Risk")
            hist_data = pd.DataFrame({"Risk %": [20, 25, 45, 60, 85, 70, 40]}, 
                                     index=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"])
            st.bar_chart(hist_data, height=130)
            
        with c4_live_placeholder.container():
            st.metric(label="Selected Date Risk", value="N/A")
            st.warning("Please choose a date from Column 2 to load offline records.")
            
        st.stop()
