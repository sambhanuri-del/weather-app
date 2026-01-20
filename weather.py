import streamlit as st
import requests
import os

API_KEY =os.getenv("6bf1ddc0bdceba120034f06f6cd74454")  # OpenWeatherMap key

st.set_page_config(page_title="Weather App", page_icon="🌦️")

st.title("🌦️ Weather App")

city = st.text_input("Enter city name")

if st.button("Get Weather"):
    if city.strip() == "":
        st.warning("Please enter a city name")
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            st.success(f"Weather in {data['name']}, {data['sys']['country']}")
            st.write(f"🌡️ Temperature: {data['main']['temp']} °C")
            st.write(f"☁️ Condition: {data['weather'][0]['description'].title()}")
            st.write(f"💧 Humidity: {data['main']['humidity']}%")

        except:
            st.error("City not found or API error")
