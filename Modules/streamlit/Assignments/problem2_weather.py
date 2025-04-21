# Modules/streamlit/Assignments/problem2_weather.py

import streamlit as st
import requests
import datetime as dt

# --- Page Configuration ---
st.set_page_config(
    page_title="Weather App (Local Debug)", # Indicate debugging mode
    page_icon="🌤️",
    layout="centered"
)

# --- API Key Handling (Simplified for Local Debugging) ---
# This section forces the use of the key below when running locally.
# The try/except for st.secrets has been REMOVED for this test.
st.info("Forcing hardcoded API key for local testing.", icon="🔧")

# <<<--- PASTE YOUR KEY HERE AGAIN, VERY CAREFULLY ---<<<
# WARNING: Avoid committing your actual key to GitHub if your repo is public!
api_key = "76532aa31d466b787da612e89acd87fd"

# Check if the key was pasted correctly
if not api_key or api_key == "YOUR_API_KEY":
     st.error("API Key is missing or still set to placeholder in the simplified section. Please paste your key above.", icon="🔑")
     st.stop() # Stop execution if key is missing

# --- API Endpoint ---
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# --- Helper Function to Fetch Weather Data ---
# (This function remains the same)
def get_weather_data(city, api_key):
    """Fetches weather data for a given city using OpenWeatherMap API."""
    url = BASE_URL + "appid=" + api_key + "&q=" + city + "&units=metric" # Using metric units (Celsius)
    st.write(f"DEBUG: Requesting URL: {url.replace(api_key, '***API_KEY***')}") # Debug: Show URL without key
    try:
        response = requests.get(url, timeout=10) # Added timeout
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: Status Code {response.status_code}") # Simplified message
        if response.status_code == 404:
            st.error(f"--> City not found: {city}. Please check the spelling.", icon="❓")
        elif response.status_code == 401:
             # Show last 4 digits for easier debugging confirmation
             st.error(f"--> Authentication Error: Invalid API Key (Key ending in: ...{api_key[-4:]}). Please double-check the key in the code.", icon="🔑")
        else:
             st.error(f"--> Details: {http_err}", icon="❌")
        # Log the response text for detailed debugging if available
        try:
            st.error(f"API Response Text: {response.text}")
        except Exception:
             pass # Ignore if text cannot be read
        return None
    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"Connection Error: Could not connect to OpenWeatherMap. {conn_err}", icon="🌐")
        return None
    except requests.exceptions.Timeout as timeout_err:
        st.error(f"Timeout Error: The request timed out after 10 seconds. {timeout_err}", icon="⏱️")
        return None
    except requests.exceptions.RequestException as req_err:
        st.error(f"An unexpected error occurred during the API request: {req_err}", icon="💥")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}", icon="🤯")
        return None


# --- Streamlit App Layout ---
# (This section remains the same)
st.title("🌤️ Problem 2: Weather Information App")
st.markdown("Enter a city name to get the current weather conditions.")

city_name = st.text_input("City Name:", placeholder="e.g., London, Tokyo, New York")

if st.button("Get Weather", key="weather_button"):
    if city_name:
        with st.spinner(f"Fetching weather for {city_name}..."):
            weather_data = get_weather_data(city_name, api_key) # Pass the determined api_key

        if weather_data:
            try:
                # Extract relevant data (refer to OpenWeatherMap API docs for structure)
                main_weather = weather_data['weather'][0]['main']
                description = weather_data['weather'][0]['description'].capitalize()
                icon_code = weather_data['weather'][0]['icon']
                temp_celsius = weather_data['main']['temp']
                feels_like_celsius = weather_data['main']['feels_like']
                humidity = weather_data['main']['humidity']
                # Corrected: Wind speed is in weather_data['wind']['speed']
                try:
                    wind_speed_mps = weather_data['wind']['speed'] # meters per second
                except KeyError:
                    wind_speed_mps = 0 # Handle cases where wind data might be missing
                    st.warning("Wind speed data not available.")

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

            except KeyError as ke:
                 st.error(f"Could not parse expected data from the API response. Key not found: {ke}", icon=" L ")
                 st.json(weather_data) # Show response for debugging
            except Exception as e:
                 st.error(f"An error occurred while processing the weather data: {e}", icon="⚙️")
                 st.json(weather_data) # Show response for debugging

    elif not city_name:
        st.warning("Please enter a city name.", icon="🏙️")

# --- Optional: Add Footer ---
st.markdown("---")
st.text("Assignment 2 - Data provided by OpenWeatherMap.")