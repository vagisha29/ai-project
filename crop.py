import streamlit as st
import pandas as pd
import pickle

model = pickle.load(open("model.pkl", "rb"))
le_soil = pickle.load(open("le_soil.pkl", "rb"))
le_crop = pickle.load(open("le_crop.pkl", "rb"))


st.set_page_config(page_title="Crop AI", page_icon="🌱")
st.title("🌱 Smart Crop Recommendation System")

st.write("Enter details below to get crop suggestion.")


col1, col2 = st.columns(2)

with col1:
    temperature = st.number_input("Temperature (°C)")
    humidity = st.number_input("Humidity (%)")
    rainfall = st.number_input("Rainfall (mm)")
    ph = st.number_input("pH (0–14)", min_value=0.0, max_value=14.0)

with col2:
    nitrogen = st.number_input("Nitrogen (kg/ha)", min_value=0.0)
    phosphorous = st.number_input("Phosphorous (kg/ha)", min_value=0.0)
    potassium = st.number_input("Potassium (kg/ha)", min_value=0.0)
    carbon = st.number_input("Carbon (%)", min_value=0.0)


soil_options = list(le_soil.classes_)
soil = st.selectbox("Soil Type", soil_options)
soil_value = le_soil.transform([soil])[0]


if st.button("Predict Crop 🌾"):

    new_data = pd.DataFrame([[
        temperature, humidity, rainfall, ph,
        nitrogen, phosphorous, potassium, carbon, soil_value
    ]], columns=[
        "Temperature", "Humidity", "Rainfall", "PH",
        "Nitrogen", "Phosphorous", "Potassium", "Carbon", "Soil"
    ])

    prediction = model.predict(new_data)[0]
    crop_name = le_crop.inverse_transform([prediction])[0]

    st.success(f"🌾 Recommended Crop: {crop_name}")