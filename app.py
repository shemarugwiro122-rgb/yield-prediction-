# -*- coding: utf-8 -*-
"""
Created on October, 2025

@author: Alain Bonheur Rugwiro Shema
"""

import pandas as pd
import streamlit as st
import joblib

# -----------------------------
# Load the compressed yield prediction model
# -----------------------------
loaded_model = joblib.load('yield_model_small_compressed.joblib')

# -----------------------------
# Encoding mappings
# -----------------------------
region_map = {'East': 0, 'North': 1, 'South': 2, 'West': 3}
soil_map = {'Chalky': 0, 'Clay': 1, 'Loam': 2, 'Peaty': 3, 'Sandy': 4, 'Silt': 5}
crop_map = {'Barley': 0, 'Cotton': 1, 'Maize': 2, 'Rice': 3, 'Soybean': 4, 'Wheat': 5}
fertilizer_map = {False: 0, True: 1}
irrigation_map = {False: 0, True: 1}
weather_map = {'Cloudy': 0, 'Rainy': 1, 'Sunny': 2}

# -----------------------------
# Streamlit App
# -----------------------------
def main():
    # Display author name at the top
    st.markdown("## 👨‍💻 Created by: Alain Bonheur Rugwiro Shema")
    st.title('🌾 Crop Yield Prediction Portal')
    st.write("Predict crop yield based on environmental and agricultural factors.")

    # --- Dropdowns for categorical inputs ---
    region = st.selectbox('Region:', list(region_map.keys()))
    soil_type = st.selectbox('Soil Type:', list(soil_map.keys()))
    crop_type = st.selectbox('Crop Type:', list(crop_map.keys()))
    fertilizer_used = st.selectbox('Fertilizer Used:', ['No', 'Yes'])
    irrigation_used = st.selectbox('Irrigation Used:', ['No', 'Yes'])
    weather_condition = st.selectbox('Weather Condition:', list(weather_map.keys()))

    # --- Numeric inputs ---
    rainfall = st.number_input('Rainfall (mm):', min_value=0.0, step=0.1, value=100.0)
    temperature = st.number_input('Temperature (°C):', min_value=-10.0, max_value=50.0, step=0.1, value=25.0)
    days_to_harvest = st.number_input('Days to Harvest:', min_value=1, step=1, value=60)

    # --- Predict button ---
    if st.button('Predict Yield'):
        # Encode categorical inputs
        region_encoded = region_map[region]
        soil_encoded = soil_map[soil_type]
        crop_encoded = crop_map[crop_type]
        fertilizer_encoded = fertilizer_map[True if fertilizer_used=='Yes' else False]
        irrigation_encoded = irrigation_map[True if irrigation_used=='Yes' else False]
        weather_encoded = weather_map[weather_condition]

        # Prepare input dataframe
        input_data = pd.DataFrame([{
            'Region': region_encoded,
            'Soil_Type': soil_encoded,
            'Crop': crop_encoded,
            'Rainfall_mm': rainfall,
            'Temperature_Celsius': temperature,
            'Fertilizer_Used': fertilizer_encoded,
            'Irrigation_Used': irrigation_encoded,
            'Weather_Condition': weather_encoded,
            'Days_to_Harvest': days_to_harvest
        }])

        # Make prediction
        predicted_yield = loaded_model.predict(input_data)

        # Display result
        st.success(f'🌱 The predicted crop yield is: {predicted_yield[0]:.2f} tons/ha')

# -----------------------------
if __name__ == '__main__':
    main()
