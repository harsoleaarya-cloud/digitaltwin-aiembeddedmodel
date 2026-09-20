import streamlit as st
import pandas as pd
import time
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Embedded Digital Twin",
    page_icon="🤖",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ai_live_data.csv"

# ============================================================
# TITLE
# ============================================================

st.title("🤖 AI Embedded Digital Twin")
st.subheader("Real-Time Device Monitoring & AI Fault Prediction")

st.caption("AI-powered virtual representation of an embedded device")

# ============================================================
# CHECK DATA FILE
# ============================================================

if not DATA_FILE.exists():
    st.error("❌ ai_live_data.csv not found!")
    st.info("Run device.py first to generate the live device data.")
    st.stop()

# ============================================================
# LOAD DATA
# ============================================================

try:
    df = pd.read_csv(DATA_FILE)
except Exception as e:
    st.error(f"Unable to read dataset: {e}")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# Convert numeric columns
numeric_columns = [
    "cpu_load",
    "memory_usage",
    "temperature",
    "battery",
    "network_latency"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

# Convert timestamp
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

# Remove invalid rows
df = df.dropna(subset=["timestamp"])

# Sort by time
df = df.sort_values("timestamp")

if len(df) == 0:
    st.warning("No device data available yet.")
    st.stop()

# ============================================================
# LATEST DATA
# ============================================================

latest = df.iloc[-1]

# ============================================================
# CURRENT DEVICE STATUS
# ============================================================

st.divider()

st.subheader("📡 Current Device Status")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "CPU Usage",
        f"{latest['cpu_load']:.2f}%"
    )

with col2:
    st.metric(
        "Memory",
        f"{latest['memory_usage']:.2f}%"
    )

with col3:
    st.metric(
        "Temperature",
        f"{latest['temperature']:.2f} °C"
    )

with col4:
    st.metric(
        "Battery",
        f"{latest['battery']:.2f}%"
    )

with col5:
    st.metric(
        "Network",
        f"{latest['network_latency']:.2f} ms"
    )

# ============================================================
# DEVICE HEALTH
# ============================================================

st.divider()

st.subheader("💚 Device Health")

health_col1, health_col2, health_col3 = st.columns(3)

with health_col1:

    cpu = float(latest["cpu_load"])

    if cpu >= 85:
        st.error("🔴 HIGH CPU LOAD")
    elif cpu >= 70:
        st.warning("🟡 ELEVATED CPU LOAD")
    else:
        st.success("🟢 CPU NORMAL")

with health_col2:

    temperature = float(latest["temperature"])

    if temperature >= 80:
        st.error("🔴 HIGH TEMPERATURE")
    elif temperature >= 60:
        st.warning("🟡 ELEVATED TEMPERATURE")
    else:
        st.success("🟢 TEMPERATURE NORMAL")

with health_col3:

    battery = float(latest["battery"])

    if battery <= 20:
        st.error("🔴 LOW BATTERY")
    elif battery <= 40:
        st.warning("🟡 BATTERY LOW")
    else:
        st.success("🟢 BATTERY HEALTHY")

# ============================================================
# AI FAULT PREDICTION
# ============================================================

st.divider()

st.subheader("🧠 AI Fault Prediction")

fault_column = None

possible_columns = [
    "ai_fault_probability",
    "fault_probability",
    "AI_Fault",
    "ai_fault",
    "fault_probability_percent"
]

for column in possible_columns:
    if column in df.columns:
        fault_column = column
        break

if fault_column:

    df[fault_column] = pd.to_numeric(
        df[fault_column],
        errors="coerce"
    )

    fault_probability = float(
        latest[fault_column]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "AI Fault Probability",
            f"{fault_probability:.2f}%"
        )

    with col2:

        if fault_probability >= 70:
            st.error("🚨 HIGH FAULT RISK")

        elif fault_probability >= 40:
            st.warning("⚠️ MEDIUM FAULT RISK")

        else:
            st.success("✅ DEVICE NORMAL")

    with col3:

        st.progress(
            min(max(fault_probability / 100, 0.0), 1.0)
        )

        st.caption("AI Risk Level")

else:

    st.info(
        "AI fault probability column not found in dataset."
    )

# ============================================================
# LIVE DEVICE GRAPHS
# ============================================================

st.divider()

st.subheader("📈 Live Device Parameters")

# Use recent records for cleaner graphs
graph_df = df.tail(100).copy()

graph_df = graph_df.set_index("timestamp")

# ------------------------------------------------------------
# CPU + MEMORY
# ------------------------------------------------------------

st.markdown("### ⚙️ CPU & Memory")

available_1 = [
    column
    for column in ["cpu_load", "memory_usage"]
    if column in graph_df.columns
]

if available_1:
    st.line_chart(
        graph_df[available_1],
        height=300
    )

# ------------------------------------------------------------
# TEMPERATURE
# ------------------------------------------------------------

st.markdown("### 🌡️ Temperature")

if "temperature" in graph_df.columns:

    st.line_chart(
        graph_df[["temperature"]],
        height=300
    )

# ------------------------------------------------------------
# BATTERY
# ------------------------------------------------------------

st.markdown("### 🔋 Battery")

if "battery" in graph_df.columns:

    st.line_chart(
        graph_df[["battery"]],
        height=300
    )

# ------------------------------------------------------------
# NETWORK
# ------------------------------------------------------------

st.markdown("### 🌐 Network Latency")

if "network_latency" in graph_df.columns:

    st.line_chart(
        graph_df[["network_latency"]],
        height=300
    )

# ------------------------------------------------------------
# AI FAULT PROBABILITY
# ------------------------------------------------------------

if fault_column:

    st.markdown("### 🤖 AI Fault Probability")

    st.line_chart(
        graph_df[[fault_column]],
        height=300
    )

# ============================================================
# DEVICE DATA TABLE
# ============================================================

st.divider()

st.subheader("📋 Latest Device Data")

display_df = df.tail(10).copy()

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# SYSTEM INFORMATION
# ============================================================

st.divider()

st.subheader("ℹ️ Digital Twin Information")

info1, info2, info3 = st.columns(3)

with info1:
    st.metric(
        "Total Records",
        len(df)
    )

with info2:
    st.metric(
        "Device ID",
        latest.get("device_id", "DT-001")
    )

with info3:
    st.metric(
        "Device State",
        latest.get("state", "NORMAL")
    )

# ============================================================
# LAST UPDATE
# ============================================================

st.caption(
    f"Last data received: {latest['timestamp']}"
)

st.caption(
    "🔄 Dashboard automatically refreshes every 2 seconds."
)

# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(2)
st.rerun()