import requests
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# ---------------- CONFIG ---------------- #
API_KEY = "YOUR_API_KEY"   # put your key here
CITY = "London"

# ---------------- STREAMLIT UI ---------------- #
st.set_page_config(page_title="Weather ML System", layout="centered")
st.title("🌦️ Intelligent Weather Classification & Alert System")

# ---------------- FETCH WEATHER DATA ---------------- #
def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    
    data = {
        "temp": response["main"]["temp"],
        "humidity": response["main"]["humidity"],
        "pressure": response["main"]["pressure"],
        "wind_speed": response["wind"]["speed"],
        "clouds": response["clouds"]["all"],
        "rain": response.get("rain", {}).get("1h", 0)
    }
    return data

weather = fetch_weather(CITY)
df = pd.DataFrame([weather])

st.subheader("📊 Current Weather Data")
st.write(df)

# ---------------- WEATHER CLASSIFICATION ---------------- #
def label_weather(row):
    if row["rain"] > 5 or row["wind_speed"] > 15:
        return "Stormy"
    elif row["clouds"] > 60:
        return "Cloudy"
    elif row["temp"] > 35:
        return "Extreme Heat"
    else:
        return "Clear"

df["weather_type"] = df.apply(label_weather, axis=1)

X_class = df[["temp", "humidity", "pressure", "wind_speed", "clouds", "rain"]]
y_class = df["weather_type"]

classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_class, y_class)

predicted_weather = classifier.predict(X_class)[0]

st.subheader("🧠 Weather Classification Result")
st.success(f"Predicted Weather Type: **{predicted_weather}**")

# ---------------- WEATHER PREDICTION ---------------- #
df["future_temp"] = df["temp"] + 1  # dummy target for demo

X_reg = df[["humidity", "pressure", "wind_speed", "clouds", "rain"]]
y_reg = df["future_temp"]

regressor = RandomForestRegressor(n_estimators=100, random_state=42)
regressor.fit(X_reg, y_reg)

predicted_temp = regressor.predict(X_reg)[0]

st.subheader("📈 Weather Prediction")
st.info(f"Predicted Next-Day Temperature: **{predicted_temp:.2f} °C**")

# ---------------- EXTREME WEATHER ALERTS ---------------- #
st.subheader("⚠️ Weather Alerts")

alerts = []

if weather["temp"] > 40:
    alerts.append("🔥 Heatwave Warning")
if weather["wind_speed"] > 20:
    alerts.append("🌪️ Strong Wind Alert")
if weather["rain"] > 10:
    alerts.append("🌧️ Heavy Rain Alert")
if weather["pressure"] < 1000:
    alerts.append("⛈️ Storm Risk Alert")

if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("No extreme weather alerts today.")

st.caption("Built using Machine Learning + Real-Time Weather API")
