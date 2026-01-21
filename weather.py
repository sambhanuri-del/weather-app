import streamlit as st
import requests
import os

st.set_page_config(page_title="Weather App", page_icon="🌤️")

API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.title("🌦️ Weather App")
city = st.text_input("Enter city name")

if st.button("Get Weather"):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city.strip(),
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    st.write("STATUS CODE:", response.status_code)
    st.write("RAW RESPONSE:")
    st.json(response.json())
