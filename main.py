import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load the API key
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.weatherapi.com/v1/current.json"


def get_weather(city_name):
    params = {
        "key": API_KEY,
        "q": city_name
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)  # Debug info
        return None


def display_weather(data):
    location = data['location']
    current = data['current']

    st.subheader(f"Weather in {location['name']}, {location['country']}")
    st.write(f"**Temperature:** {current['temp_c']} °C")
    st.write(f"**Condition:** {current['condition']['text']}")
    st.write(f"**Humidity:** {current['humidity']}%")
    st.write(f"**Wind Speed:** {current['wind_kph']} km/h")


# Streamlit UI
st.title("The Weather App 🌦️")
city = st.text_input("Please enter a city name:")

if city:
    weather_data = get_weather(city)
    if weather_data:
        display_weather(weather_data)
    else:
        st.error("City not found or unable to fetch weather data.")
