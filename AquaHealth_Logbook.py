import streamlit as st
import datetime
import joblib
import numpy as np

st.set_page_config(
    page_title="Logbook Entry",
    page_icon="📝",
)

st.title("📝 AquaHealth Logbook Entry")


model = joblib.load("aquahealth_anomalydetection_model.pkl")
scaler = joblib.load("aquahealth_feature_scaler.pkl")

def render_circular_score(score, color):
    score = int(score)
    return f"""
    <div style="display: flex; justify-content: center; margin-top: 10px;">
        <svg width="140" height="140" viewBox="0 0 36 36">
            <path
              stroke="{color}"
              stroke-dasharray="{score}, 100"
              d="M18 2.0845
                 a 15.9155 15.9155 0 0 1 0 31.831
                 a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke-width="3.5"
            />
            <text x="18" y="20.35" fill="{color}" font-size="6" text-anchor="middle" alignment-baseline="middle">
              {score}%
            </text>
        </svg>
    </div>
    """

def generate_suggestions(temp, oxy, sal, foam):
    suggestions = []

    if temp > 28 and oxy < 4 and sal > 36:
        suggestions.append("🔥 High temperature, low DO, and high salinity suggest severe evaporation or eutrophication. Immediate water exchange and aeration are recommended.")
    elif temp > 27 and oxy < 4 and foam != "No":
        suggestions.append("🫧 Elevated temp, low DO, and foam may indicate algal bloom. Apply algaecide cautiously and increase aeration.")
    elif sal < 27 and oxy < 4 and temp > 25:
        suggestions.append("🌧️ Low salinity, high temp, and low DO hint at freshwater flooding or runoff. Verify recent rainfall and adjust pond management accordingly.")
    elif sal > 35 and oxy < 5 and foam != "No":
        suggestions.append("⚠️ High salinity with low DO and surface foam could mean chemical contamination. Test water quality and isolate affected ponds.")
    elif temp > 29 and oxy < 3.5 and sal < 27:
        suggestions.append("🌡️ Unstable pond conditions due to high heat, oxygen stress, and low salinity. Initiate emergency oxygenation and monitor closely.")

    elif temp > 28 and oxy < 4:
        suggestions.append("⚠️ High temperature and low DO suggest thermal stratification. Increase aeration and consider mixing layers.")
    elif temp > 26 and sal > 36:
        suggestions.append("🔥 Warm, saline water may indicate high evaporation. Check for concentration of pollutants and consider water exchange.")
    elif sal < 28 and oxy < 5:
        suggestions.append("🧪 Low salinity and low DO might result from freshwater runoff. Check rainfall data and assess runoff impact.")
    elif temp > 25 and sal < 28:
        suggestions.append("🌧️ Warm, fresh water could stress fish. Watch for rainfall events and monitor feeding response.")
    elif oxy < 4 and foam != "No":
        suggestions.append("🫧 Low DO with surface foam may indicate organic pollution or algal bloom. Test ammonia levels.")

    if temp > 20:
        suggestions.append("🌡️ Consider shading ponds or increasing water exchange to reduce temperature.")
    if oxy < 5:
        suggestions.append("💨 Increase aeration or reduce stocking density to improve dissolved oxygen levels.")
    if sal < 28:
        suggestions.append("🚰 Check freshwater inflow or dilution sources. Adjust salinity via controlled salting.")
    elif sal > 35:
        suggestions.append("🌊 Dilute pond water or monitor evaporation rates; consider controlled flushing.")

    if not suggestions:
        suggestions.append("✅ All values are within acceptable limits. Continue routine monitoring.")

    return " ".join(suggestions)

with st.form("logbook_form"):
    st.subheader("Observation Details")

    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date of Observation", value=datetime.date.today())
    
    with col2:
        time = st.time_input("Time of Observation")

    col3, col4 = st.columns(2)

    with col3:
        feeding = st.selectbox("Feeding Behavior", ["Normal", "Reduced", "Refused"])
        dead_fish = st.number_input("Number of Dead Fish", min_value=0)

    with col4:
        behavior = st.text_area("Fish Behavior Notes")

    col5, col6, col7 = st.columns(3)

    with col5:
        water_color = st.selectbox("Water Color", ["Clear", "Green", "Brown", "Murky", "Other"])

    with col6:
        odor = st.selectbox("Water Odor", ["None", "Mild", "Rotten/Eggy", "Chemical"])

    with col7:
        foam = st.radio("Surface Foam", ["No", "Yes - Light", "Yes - Heavy"])

    col8, col9, col10 = st.columns(3)

    with col8:
        temperature = st.number_input("Temperature Reading(°C)", min_value=0.0, max_value=40.0, step=0.1,format="%.6f")

    with col9:
        oxygen = st.number_input("DO Reading (ml/L)", min_value=0.0, max_value=20.0, step=0.1,format="%.6f")

    with col10:
        salinity = st.number_input("Salinity Reading (PSU)", min_value=0.0, max_value=50.0, step=0.1,format="%.6f")

    aeration = st.selectbox("Aeration Status", ["Working Normally", "Not Functional", "Not Present"])

    col11, col12 = st.columns(2)

    with col11:
        sensor_issue = st.text_area("Sensor/Equipment Issues")

    with col12:
        intervention = st.text_area("Actions Taken")

    photo = st.file_uploader("Upload Photo (optional)", type=["jpg", "png"])

    technician_name = st.text_input("Technician Name")
    notes = st.text_area("Additional Comments")

    submitted = st.form_submit_button("Submit Log Entry")

if submitted:
    features = np.array([[temperature, salinity, oxygen]])
    scaled = scaler.transform(features)

    prediction = model.predict(scaled)[0]
    score = model.decision_function(scaled)[0]

    score_min = -0.1
    score_max = 0.1

    score_range = score_max - score_min
    if score_range == 0:
        risk_score = 50
    else:
        risk_score = round(100 * (1 - (score - score_min) / score_range), 2)

    risk_score = max(0, min(100, risk_score))

    if risk_score <= 40:
        color = "green"
    elif risk_score <= 70:
        color = "orange"
    else:
        color = "red"

    reasons = []
    if temperature > 20:
        reasons.append("High temperature")
    if oxygen < 5:
        reasons.append("Low dissolved oxygen")
    if salinity < 28 or salinity > 35:
        reasons.append("Salinity out of range")
    reason_msg = "; ".join(reasons) if reasons else "Unusual pattern detected (no single variable outside safe range)"
    suggestion_msg = generate_suggestions(temperature, oxygen, salinity, foam)

    # Display result
    st.subheader("🧠 Risk Assessment")

    if prediction == -1:
        st.markdown(
            f"<h2 style='text-align: center; color: {color};'>⚠️ Risk Score: {risk_score}</h2>",
            unsafe_allow_html=True
        )
        st.markdown(render_circular_score(risk_score, color), unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'><strong>Reason:</strong> {reason_msg}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'><strong>Suggested Action:</strong> {suggestion_msg}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: green;'>✅ Normal</h2>", unsafe_allow_html=True)


