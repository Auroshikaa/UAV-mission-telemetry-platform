import sqlite3

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

DATABASE_NAME = "uav_mission.db"


def load_data() -> pd.DataFrame:
    connection = sqlite3.connect(DATABASE_NAME)

    query = """
    SELECT *
    FROM telemetry
    ORDER BY timestamp DESC
    """

    df = pd.read_sql_query(query, connection)
    connection.close()

    return df


st.set_page_config(
    page_title="UAV Ground Control Dashboard",
    layout="wide"
)

st_autorefresh(interval=3000, key="uav_refresh")

st.title("UAV Fleet Mission Telemetry Dashboard")

df = load_data()

if df.empty:
    st.warning("No UAV telemetry found. Start the backend and simulator first.")

else:
    uav_options = sorted(df["uav_id"].unique())

    selected_uav = st.selectbox(
        "Select UAV",
        uav_options
    )

    filtered_df = df[df["uav_id"] == selected_uav].copy()

    latest = filtered_df.iloc[0]

    st.subheader("Current Mission Status")
    st.write(f"**Mission Type:** {latest['mission_type']}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Mission Phase", latest["mission_phase"])
    col2.metric("Health Status", latest["health_status"])
    col3.metric("Battery (%)", latest["battery_percent"])
    col4.metric("Fault", latest["fault"])

    if latest["health_status"] == "CRITICAL":
        st.error("CRITICAL ALERT: Mission risk detected.")
    elif latest["health_status"] == "WARNING":
        st.warning("WARNING: Monitor UAV closely.")
    else:
        st.success("UAV operating normally.")

    st.subheader("Live Flight Telemetry")

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Altitude (m)", latest["altitude_m"])
    col6.metric("Speed (km/h)", latest["speed_kmh"])
    col7.metric("Motor Temp (°C)", latest["motor_temp_c"])
    col8.metric("Signal Strength", latest["signal_strength"])

    st.subheader("Telemetry Trends")

    chart_df = filtered_df.sort_values("timestamp")

    st.write("Altitude Over Time")
    st.line_chart(
        chart_df.set_index("timestamp")["altitude_m"]
    )

    st.write("Battery Over Time")
    st.line_chart(
        chart_df.set_index("timestamp")["battery_percent"]
    )

    st.write("Motor Temperature Over Time")
    st.line_chart(
        chart_df.set_index("timestamp")["motor_temp_c"]
    )

    st.write("Signal Strength Over Time")
    st.line_chart(
        chart_df.set_index("timestamp")["signal_strength"]
    )

    st.subheader("Recent Mission Log")

    display_df = filtered_df.drop(columns=["id"])

    st.dataframe(
        display_df.head(25),
        use_container_width=True
    )