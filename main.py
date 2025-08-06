import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Load the API key from "weatherapi.com"
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

    st.subheader(f"Weather in {location['name']}, {location['country']}")
    st.image(icon_url, width=200, caption=current['condition']['text'])
    st.write(f"**Local Time:** {location['localtime']}")
    st.write(f"**Temperature:** {current['temp_c']} °C")
    st.write(f"**Condition:** {current['condition']['text']}")
    st.write(f"**Humidity:** {current['humidity']}%")
    st.write(f"**Wind Speed:** {current['wind_kph']} km/h")
    st.write(f"**Visibility:** {current['vis_km']} km")

    # Show the location pinpoint on a map
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

def display_forecast_chart(data):
    forecast_days = data['forecast']['forecastday']
    df = pd.DataFrame({
        "Date": [day['date'] for day in forecast_days],
        "Average Temp (°C)": [day['day']['avgtemp_c'] for day in forecast_days]
    })

    st.subheader("📈 Temperature Trend")
    fig = px.line(df, x="Date", y="Average Temp (°C)",
                  title='5-day Temperature',
                  markers=True,
                  line_shape='spline')  # Smooth curve

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        title_x=0.5,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

def set_background():
    st.markdown("""
        <style>
        .stApp {
            background-color: #f7f9fc;;
            background-image: linear-gradient(to bottom, #ffecd2, #fcb69f);
            background-image: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
            color: #333;
        }
        </style>
    """, unsafe_allow_html=True)


# Streamlit UI
st.title("🌍TheWeatherApp")
st.markdown("#### Get real-time weather updates and a 5-day forecast!")
set_background()

city = st.text_input("🔍 Enter a city name:")

if city:
    weather_data = get_weather(city)
    if weather_data:
        tab1, tab2 = st.tabs(["📍 Current", "📆 Forecast"])
        with tab1:
            display_weather(weather_data)
        with tab2:
            display_forecast(weather_data)
            display_forecast_chart(weather_data)
    else:
        st.error("❌ City not found or failed to fetch data.")

