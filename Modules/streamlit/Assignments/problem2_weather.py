# Modules/streamlit/Assignments/problem2_weather.py

import streamlit as st
import requests
import datetime as dt

# --- Page Configuration ---
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

# --- API Key Handling ---
# IMPORTANT: Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
# For local testing, you can paste your key here directly.
# For deployment on Streamlit Cloud, use Secrets Management:
# 1. Create a file .streamlit/secrets.toml in your repo (add .streamlit/ to .gitignore!)
# 2. Add your key like this: openweathermap_api_key = "YOUR_ACTUAL_API_KEY"
# 3. Access it in the deployed app using st.secrets["openweathermap_api_key"]

# Attempt to load API key from Streamlit Secrets first (for deployed app)
try:
    api_key = st.secrets["openweathermap_api_key"]
    st.info("Using API Key from Streamlit Secrets.", icon="☁️")
except (FileNotFoundError, KeyError):
    # Fallback for local testing (replace with your key)
    # WARNING: Avoid committing your actual key to GitHub if your repo is public!
    api_key = "YOUR_API_KEY" # <<<--- PASTE YOUR KEY HERE FOR LOCAL RUN
    if api_key == "YOUR_API_KEY":
        st.warning("API Key not found in Streamlit Secrets. Using placeholder key. Please replace 'YOUR_API_KEY' in the code with your actual OpenWeatherMap API key for local testing.", icon="⚠️")


# --- API Endpoint ---
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# --- Helper Function to Fetch Weather Data ---
def get_weather_data(city, api_key):
    """Fetches weather data for a given city using OpenWeatherMap API."""
    url = BASE_URL + "appid=" + api_key + "&q=" + city + "&units=metric" # Using metric units (Celsius)
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            st.error(f"City not found: {city}. Please check the spelling.", icon="❓")
        elif response.status_code == 401:
             st.error("Authentication Error: Invalid API Key. Please check your API key in the code or Streamlit Secrets.", icon="🔑")
        else:
             st.error(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}", icon="❌")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"Connection Error: Could not connect to OpenWeatherMap. {conn_err}", icon="🌐")
        return None
    except requests.exceptions.Timeout as timeout_err:
        st.error(f"Timeout Error: The request timed out. {timeout_err}", icon="⏱️")
        return None
    except requests.exceptions.RequestException as req_err:
        st.error(f"An unexpected error occurred during the API request: {req_err}", icon="💥")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}", icon="🤯")
        return None


# --- Streamlit App Layout ---
st.title("🌤️ Problem 2: Weather Information App")
st.markdown("Enter a city name to get the current weather conditions.")

city_name = st.text_input("City Name:", placeholder="e.g., London, Tokyo, New York")

if st.button("Get Weather", key="weather_button"):
    if city_name and api_key != "YOUR_API_KEY":
        with st.spinner(f"Fetching weather for {city_name}..."):
            weather_data = get_weather_data(city_name, api_key)

        if weather_data:
            try:
                # Extract relevant data (refer to OpenWeatherMap API docs for structure)
                main_weather = weather_data['weather'][0]['main']
                description = weather_data['weather'][0]['description'].capitalize()
                icon_code = weather_data['weather'][0]['icon']
                temp_celsius = weather_data['main']['temp']
                feels_like_celsius = weather_data['main']['feels_like']
                humidity = weather_data['main']['humidity']
                wind_speed_mps = weather_data['main']['temp'] # meters per second
                country = weather_data['sys']['country']
                city_display_name = weather_data['name']
                timestamp = weather_data['dt']
                timezone_offset = weather_data['timezone'] # Offset in seconds from UTC

                # Convert timestamp to local time
                local_time = dt.datetime.utcfromtimestamp(timestamp + timezone_offset).strftime('%Y-%m-%d %H:%M:%S')

                # Display Weather Info
                st.subheader(f"Current Weather in {city_display_name}, {country}")
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                st.image(icon_url, caption=f"{main_weather}", width=80)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="Temperature", value=f"{temp_celsius:.1f} °C")
                with col2:
                    st.metric(label="Feels Like", value=f"{feels_like_celsius:.1f} °C")
                with col3:
                    st.metric(label="Humidity", value=f"{humidity}%")


                st.write(f"**Condition:** {description}")
                # Convert m/s to km/h for more common display
                wind_speed_kmh = wind_speed_mps * 3.6
                st.write(f"**Wind Speed:** {wind_speed_kmh:.1f} km/h")
                st.write(f"**Local Time:** {local_time} (approx.)")
                # st.write(f"(Data fetched at: {dt.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')})")

                # Optionally display raw data
                # if st.checkbox("Show Raw API Response"):
                #    st.json(weather_data)

            except KeyError as ke:
                 st.error(f"Could not parse expected data from the API response. Key not found: {ke}", icon=" L ")
                 # st.json(weather_data) # Show response for debugging
            except Exception as e:
                 st.error(f"An error occurred while processing the weather data: {e}", icon="⚙️")
                 # st.json(weather_data) # Show response for debugging


    elif not city_name:
        st.warning("Please enter a city name.", icon="🏙️")
    elif api_key == "YOUR_API_KEY":
         st.error("API Key is missing. Please add your OpenWeatherMap API key to the code or Streamlit Secrets.", icon="🔑")


# --- Optional: Add Footer ---
st.markdown("---")
st.text("Assignment 2 - Data provided by OpenWeatherMap.")