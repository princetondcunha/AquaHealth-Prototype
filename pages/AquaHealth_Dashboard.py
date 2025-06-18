import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard",
    page_icon="🌊",
)

@st.cache_data
def load_data():
    return pd.read_csv("mock_logbook_data_6months.csv")

df = load_data()

st.title("🌊 AquaHealth Logbook Dashboard")

total_entries = len(df)
total_alerts = (df["alert_status"] != "Normal").sum()
critical_alerts = (df["alert_status"] == "Critical Alert").sum()
avg_risk = round(df["risk_score"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("📄 Total Entries", total_entries)
col2.metric("🚨 Alerts", total_alerts)
col3.metric("🔥 Critical Alerts", critical_alerts)
col4.metric("⚠️ Avg. Risk Score", avg_risk)

st.subheader("📊 Alert Status Over Time")
df['timestamp'] = pd.to_datetime(df['timestamp'])
fig_alerts = px.scatter(df, x="timestamp", y="risk_score", color="alert_status", symbol="alert_status",
                        color_discrete_map={
                            "Normal": "green",
                            "Early Warning": "orange",
                            "Anomaly Detected": "red",
                            "Critical Alert": "black"
                        },
                        title="Alert Trends")
st.plotly_chart(fig_alerts, use_container_width=True)

st.subheader("📈 Parameter Trends")
parameter = st.selectbox("Select parameter", ["temperature", "salinity", "oxygen", "risk_score"])
fig_param = px.line(df, x="timestamp", y=parameter, title=f"{parameter.title()} over Time")
st.plotly_chart(fig_param, use_container_width=True)

st.subheader("🧾 Detailed Logbook Entries")
alert_filter = st.selectbox("Filter by Alert Status", ["All"] + df["alert_status"].unique().tolist())
if alert_filter != "All":
    filtered_df = df[df["alert_status"] == alert_filter]
else:
    filtered_df = df

st.dataframe(filtered_df, use_container_width=True)
