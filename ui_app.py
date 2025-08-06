import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/predict"

st.title("💓 Heart Disease Prediction App")

# Input fields
age = st.number_input("Age", min_value=1, max_value=120, value=40)
sex = st.selectbox("Sex", ["M", "F"])  # M = 1, F = 0
chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "ASY", "TA"])  # ATA=1, NAP=2, ASY=0, TA=3
resting_bp = st.number_input("Resting BP", value=120)
cholesterol = st.number_input("Cholesterol", value=200)
fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1])
resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])  # Normal=1, ST=2, LVH=0
max_hr = st.number_input("Max HR", value=150)
exercise_angina = st.selectbox("Exercise-Induced Angina", ["Y", "N"])  # Y=1, N=0
oldpeak = st.number_input("Oldpeak", step=0.1)
st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])  # Up=2, Flat=1, Down=0

# Mapping categorical to numeric
sex = 1 if sex == "M" else 0
chest_pain_map = {"ASY": 0, "ATA": 1, "NAP": 2, "TA": 3}
resting_ecg_map = {"LVH": 0, "Normal": 1, "ST": 2}
exercise_angina = 1 if exercise_angina == "Y" else 0
st_slope_map = {"Down": 0, "Flat": 1, "Up": 2}

# Submit button
if st.button("🔍 Predict"):
    data = {
        "Age": age,
        "Sex": sex,
        "ChestPainType": chest_pain_map[chest_pain],
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "RestingECG": resting_ecg_map[resting_ecg],
        "MaxHR": max_hr,
        "ExerciseAngina": exercise_angina,
        "Oldpeak": oldpeak,
        "ST_Slope": st_slope_map[st_slope]
    }

    try:
        response = requests.post(API_URL, json=data)
        result = response.json()
        prob = result.get("probability")
        msg = result.get("message")

        if result.get("prediction") == 1:
            st.error(f"💔 {msg} (Risk: {prob})")
        else:
            st.success(f"💖 {msg} (Risk: {prob})")

    except Exception as e:
        st.warning(f"API Error: {e}")
