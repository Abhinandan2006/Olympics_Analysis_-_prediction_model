import os
import sys
import streamlit as st
import joblib
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from modules import preprocessor
from modules import  helper

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "pipeline.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "model", "label_encoder.pkl")

pipeline = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

athlete_data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'athlete_events.csv'))
region_data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'noc_regions.csv'))

st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        [data-testid="stSidebarUserContent"] {
            padding-top: 0rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.sidebar.page_link("app.py", label="Back to Home", icon="🏠")
st.markdown("<h1 style='text-align: center;'>Athlete Performance Model 🏅</h1>", unsafe_allow_html=True)

EXPECTED_COLUMNS = ['Age', 'Sex', 'Height', 'Weight', 'Sport', 'region']

df = preprocessor.preprocess_overall(athlete_data, region_data)
country, sport = helper.get_country_sport(df)
def predict_medal(input_dict):
    df = pd.DataFrame([input_dict])[EXPECTED_COLUMNS]
    pred = pipeline.predict(df)
    return label_encoder.inverse_transform(pred)[0]


age = st.number_input("Age", 10, 60)
sex = st.selectbox("Sex", ["M", "F"])
height = st.number_input("Height (cm)", 100, 220)
weight = st.number_input("Weight (kg)", 30, 150)
sport = st.selectbox("Sport", sport)
region = st.selectbox("Region", country)

if st.button("Predict"):
    res = predict_medal({
        "Age": age,
        "Sex": sex,
        "Height": height,
        "Weight": weight,
        "Sport": sport,
        "region": region
    })

    st.success(f"Predicted Medal: **{res}** 🏅")
