import streamlit as st
import requests
import os

st.set_page_config(page_title="Weather App", page_icon="🌤️")

API_KEY = os.getenv("WEATHER_API_KEY")

st.title("🌦️ Weather App")
city = st.text_input("Enter city name")

if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name")
    else:
        url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": API_KEY,
            "q": city
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            st.error(data["error"]["message"])
        else:
            st.success(f"Weather in {data['location']['name']}")
            st.write(f"🌡️ Temperature: {data['current']['temp_c']} °C")
            st.write(f"☁️ Condition: {data['current']['condition']['text']}")
            st.write(f"💨 Wind Speed: {data['current']['wind_kph']} kph")
