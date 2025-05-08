import streamlit as st
import pandas as pd
import plotly.express as px
from utils.anomaly_detection import detect_anomalies
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="VNR Patients Records", layout="wide")

st.markdown("""
# 🩺 **VNR Patients Records**
""", unsafe_allow_html=True)

# Load data
df = pd.read_csv("data/patient_vitals.csv", parse_dates=["Timestamp"])

# Sidebar selections
selected_patient = st.sidebar.selectbox("Select Patient ID", df["PatientID"].unique())
time_filter = st.sidebar.selectbox("Select Time Filter", ["Last 24 Hours", "Last 3 Days", "Last 7 Days"])

# Filter patient data
patient_data = df[df["PatientID"] == selected_patient]
now = datetime.now()
if time_filter == "Last 24 Hours":
    patient_data = patient_data[patient_data["Timestamp"] >= now - timedelta(days=1)]
elif time_filter == "Last 3 Days":
    patient_data = patient_data[patient_data["Timestamp"] >= now - timedelta(days=3)]
elif time_filter == "Last 7 Days":
    patient_data = patient_data[patient_data["Timestamp"] >= now - timedelta(days=7)]

# Safety check
if patient_data.empty:
    st.warning("⚠️ No data available for the selected patient and time filter.")
    st.stop()  # ✅ Prevents IndexError

# Latest Vitals
st.subheader("🔍 Latest Vitals")
latest = patient_data.sort_values("Timestamp").iloc[-1]
col1, col2, col3 = st.columns(3)
col1.metric("❤️ Heart Rate", f"{latest.HeartRate} bpm")
col2.metric("🩸 Blood Pressure", f"{latest.BP_Systolic}/{latest.BP_Diastolic} mmHg")
col3.metric("🌬️ SpO2", f"{latest.SpO2} %")

# Health Score
st.subheader("🧠 Health Score")
score = 100
if latest.HeartRate < 60 or latest.HeartRate > 100:
    score -= 20
if latest.BP_Systolic < 90 or latest.BP_Systolic > 140 or latest.BP_Diastolic < 60 or latest.BP_Diastolic > 90:
    score -= 20
if latest.SpO2 < 95:
    score -= 20
st.progress(score / 100)
st.write(f"Health Score: {score}/100")

# Trend Chart
st.subheader("📈 Vitals Trend Over Time")
selected_vitals = st.multiselect("Select Vitals", ["HeartRate", "BP_Systolic", "BP_Diastolic", "SpO2"],
                                 default=["HeartRate", "SpO2"])
fig = px.line(patient_data, x="Timestamp", y=selected_vitals, labels={"value": "Reading", "Timestamp": "Time"})
st.plotly_chart(fig, use_container_width=True)

# Anomaly Alerts
st.subheader("🚨 Anomaly Alerts")
anomalies = detect_anomalies(patient_data)
st.dataframe(anomalies)

# Downloads
st.subheader("📄 Download Reports")
st.download_button("Download Patient Data (CSV)", patient_data.to_csv(index=False), "patient_data.csv", "text/csv")
st.download_button("Download Anomalies Report (CSV)", anomalies.to_csv(index=False), "anomalies.csv", "text/csv")

# Live Update Simulation
if st.checkbox("🔄 Simulate Live Update", value=False):
    st.info("New data will be appended every 5 seconds (simulation only)")
    for _ in range(3):
        with st.spinner("Simulating data..."):
            time.sleep(5)
        st.rerun()
