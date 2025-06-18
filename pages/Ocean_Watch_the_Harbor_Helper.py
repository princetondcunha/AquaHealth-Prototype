import streamlit as st
import pandas as pd

st.set_page_config(page_title="Harbor Helper", layout="wide")

st.title("📰 Harbor Helper – Explaining the Ocean Watch")
st.markdown("Insights explaining the *why* behind community-reported ocean anomalies.")

# Load dataset
df = pd.read_csv("oceanwatchfeed_with_insights.csv")
df = df[df["harbor_helper_insight"].notnull()].reset_index(drop=True)

# Sidebar Filters
st.sidebar.header("🔍 Filter Insights")

# Location filter
locations = sorted(df["location"].unique())
selected_location = st.sidebar.selectbox("Filter by Location", ["All"] + locations)

# Search input
search_term = st.sidebar.text_input("Search by keyword (tag, message, insight)", "")

# Apply filters
filtered_df = df.copy()

if selected_location != "All":
    filtered_df = filtered_df[filtered_df["location"] == selected_location]

if search_term:
    mask = (
        filtered_df["tag"].str.contains(search_term, case=False, na=False) |
        filtered_df["message"].str.contains(search_term, case=False, na=False) |
        filtered_df["harbor_helper_insight"].str.contains(search_term, case=False, na=False)
    )
    filtered_df = filtered_df[mask]

# Show results
if filtered_df.empty:
    st.info("No insights match your filter/search. Try different options.")
else:
    cols = st.columns(3)
    for idx, row in filtered_df.iterrows():
        col = cols[idx % 3]
        with col:
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 20px; background-color: #f9f9f9;">
                    <div style="font-size: 14px; color: #666;"><b>{row['tag']}</b> · 📍 {row['location']}</div>
                    <div style="margin-top: 10px; font-size: 15px;">{row['harbor_helper_insight']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
