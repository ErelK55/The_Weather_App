import streamlit as st
import requests
#import os
import pandas as pd
#from dotenv import load_dotenv

# Load the API key from "weatherapi.com"
#load_dotenv()
API_KEY = st.secrets["api"]["WEATHER_API_KEY"]
BASE_URL = "https://api.weatherapi.com/v1/forecast.json"


def get_weather(city_name):
    params = {
        "key": API_KEY,
        "q": city_name,
        "days": 5, #gives a 5-day forecast
        "aqi": "no",
        "alerts": "no"
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)  # Debug info
        return None

    # Show the current weather at the location
def display_weather(data):
    location = data['location']
    current = data['current']
    icon_url = "https:" + current['condition']['icon']
    st.image(icon_url, width=100)

    st.subheader(f"Weather in {location['name']}, {location['country']}")
    st.write(f"**Local Time:** {location['localtime']}")
    st.write(f"**Temperature:** {current['temp_c']} °C")
    st.write(f"**Condition:** {current['condition']['text']}")
    st.write(f"**Humidity:** {current['humidity']}%")
    st.write(f"**Wind Speed:** {current['wind_kph']} km/h")
    st.write(f"**Visibility:** {current['vis_km']} km")

    # Show the location pinpoint on a map
    st.subheader("Location on Map 🗺️")
    lat = location['lat']
    lon = location['lon']
    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_data)

def display_forecast(data):
    forecast_days = data['forecast']['forecastday']
    st.subheader("5-Day Forecast 🌤️")
    cols = st.columns(5)

    for i, day in enumerate(forecast_days):
        date = day['date']
        avg_temp = day['day']['avgtemp_c']
        condition = day['day']['condition']['text']
        icon = "https:" + day['day']['condition']['icon']

        with cols[i]:
            st.markdown(f"**{date}**")
            st.image(icon, width=60)
            st.write(f"{condition}, {avg_temp} °C")


# Streamlit UI
st.title("The Weather App ☀️")
city = st.text_input("Please enter a city name:")

if city:
    weather_data = get_weather(city)
    if weather_data:
        display_weather(weather_data)
        display_forecast(weather_data)
    else:
        st.error("City not found or unable to fetch weather data.")
