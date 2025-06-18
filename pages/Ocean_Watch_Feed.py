from socket import has_dualstack_ipv6
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import os
from PIL import Image

st.set_page_config(page_title="Ocean Watch Feed", layout="wide",page_icon="🌊",)
st.title("🌊 Ocean Watch Feed")

tags = [
    "#AlgalBloom",
    "#FishDieOff",
    "#PlasticPollution",
    "#OilSpill",
    "#JellyfishBloom",
    "#TurbiditySpike",
    "#LowOxygen",
    "#SeafloorAnomaly",
    "#WaterDiscoloration",
    "#FoamSlick",
    "#MarineDebris",
    "#RedTide",
    "#CoralBleaching",
    "#SensorAlert",
    "#OilSheen",
    "#StrangeSmell",
    "#FishKill",
    "#StormRunoff",
    "#KelpCollapse",
    "#Microplastics",
    "#HighSalinity",
    "#OxygenDrop",
    "#DeadZone",
    "#ThermalSpike",
    "#NoMarineLife",
    "#SlickSurface",
    "#FloatingGarbage",
    "#ToxicWaters",
    "#ScumLayer",
    "#BrownTide",
    "#FishDistress",
    "#ShellfishMortality",
    "#WaterHazard",
    "#UnusualBioluminescence",
    "#ClarityDrop",
    "#ContaminatedWaters",
    "#CoastalErosion",
    "#SensorMismatch",
    "#UnnaturalColor",
    "#BleachedSeaweed",
    "#BiofilmSpread",
    "#CrabDieOff",
    "#CrudeLeak",
    "#JellySwarm",
    "#SalinitySpike",
    "#BeachClosure",
    "#MarineSlick",
    "#EcosystemShift",
    "#AnoxicWaters",
    "#MassBeachings",
    "#TideFoam",
    "#BacterialBloom",
    "#ChemicalSpill",
    "#UnknownBloom",
    "#DeadMarineLife",
    "#NoisePollution",
    "#HighTurbidity",
    "#GasRelease",
    "#SeagrassDieOff",
    "#PlasticWave",
    "#WarmWaterAlert",
    "#FreakTide",
    "#SedimentPlume",
    "#FloatingFilm",
    "#CoastalDistress",
    "#ToxicFoam",
    "#EnvironmentalRisk",
    "#AquacultureAlert",
    "#WildlifeAnomaly",
    "#ToxicAlgae",
    "#HypoxicZone",
    "#OceanWarning",
    "#HabitatStress",
    "#BioindicatorAlert"
]

post_df = pd.read_csv("oceanwatchfeed_mock.csv")

os.makedirs("images", exist_ok=True)

st.subheader("📝 Report an Ocean Anomaly")
with st.form("new_post_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        user = st.text_input("Username", placeholder="Your name or alias")
    with col2:
        tag = st.selectbox("Category", options=tags)
        
    message = st.text_area("What did you observe?", placeholder="Describe the anomaly...")

    col3, col4, col5 = st.columns(3)
    with col3:
        location = st.text_input("Location name")
    with col4:
        lat = st.number_input("Latitude", format="%.6f")
    with col5:
        lon = st.number_input("Longitude", format="%.6f")
    image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Submit Observation")

if submitted:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    image_filename = ""

    if image:
        safe_name = f"{user or 'anonymous'}_{timestamp.replace(':', '').replace(' ', '_')}.png"
        image_path = os.path.join("images", safe_name)
        with open(image_path, "wb") as f:
            f.write(image.read())
        image_filename = image_path

    new_post = {
        "user": user or "Anonymous",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "location": location or "Unknown",
        "lat": lat,
        "lon": lon,
        "message": message,
        "tag": tag,
        "image_path": image_filename
    }

    post_df = pd.concat([pd.DataFrame([new_post]), post_df], ignore_index=True)
    post_df.to_csv("oceanwatchfeed_mock.csv", index=False)
    st.success("Observation submitted successfully!")

st.subheader("🌐 Community Ocean Anomaly Posts")

for i, row in post_df.iterrows():
    
    with st.container():

        image_path = row.get("image_path", "")
        has_image =  isinstance(image_path, str) and image_path.strip() and os.path.exists(image_path)

        if has_image:
            col1, col2, col3 = st.columns([2,1,1])

            with col1:
                st.markdown(f"**@{row['user']}** · *{row['timestamp']}*  ")
                st.markdown(f"{row['message']} <span style='color: #0066cc'>{row['tag']}</span>", unsafe_allow_html=True)
                st.markdown(f"📍 {row['location']}")

            with col2:
                st.image(image_path, use_container_width="always")

            with col3:
                m = folium.Map(location=[row['lat'], row['lon']], zoom_start=9)
                folium.Marker([row['lat'], row['lon']], tooltip=row['message']).add_to(m)
                st_folium(m, width=300, height=250, key=f"map_{i}")
        else:
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**@{row['user']}** · *{row['timestamp']}*  ")
                st.markdown(f"{row['message']} <span style='color: #0066cc'>{row['tag']}</span>", unsafe_allow_html=True)
                st.markdown(f"📍 {row['location']}")

            with col2:
                m = folium.Map(location=[row['lat'], row['lon']], zoom_start=9)
                folium.Marker([row['lat'], row['lon']], tooltip=row['message']).add_to(m)
                st_folium(m, width=300, height=250, key=f"map_{i}")

        st.markdown("---")
