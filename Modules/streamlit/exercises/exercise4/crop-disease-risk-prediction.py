import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="Crop Disease Risk Prediction",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Title and Description ---
st.title("🌿 Crop Disease Risk Prediction Dashboard")
st.markdown("""
This application predicts the risk of crop diseases based on location and environmental factors.
Use the sidebar to input parameters and view the prediction and visualizations.
*(This is a demo based on sample data)*
""")

# --- Data Loading ---
@st.cache_data # Cache the data loading for performance
def load_data(filepath="disease_risk_data.csv"):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        st.error(f"Error: The file {filepath} was not found.")
        st.warning("Please ensure 'disease_risk_data.csv' is in the same directory as the script.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return None

df = load_data()

if df is None:
    st.stop() # Stop execution if data loading failed

# --- Sidebar Inputs ---
st.sidebar.header("Input Parameters")

# Location Selection
locations = df['Location'].unique()
selected_location = st.sidebar.selectbox(
    "Select Location:",
    options=locations,
    index=0 # Default to the first location
)

# Environmental Factors (using average from data as defaults for sliders)
location_data_avg = df[df['Location'] == selected_location].mean(numeric_only=True)

temp_default = int(location_data_avg.get('Avg_Temperature_C', 25))
humidity_default = int(location_data_avg.get('Avg_Humidity_Percent', 75))
rainfall_default = int(location_data_avg.get('Avg_Rainfall_mm', 5))

st.sidebar.subheader("Current Environmental Conditions")
current_temp = st.sidebar.slider(
    "Temperature (°C):",
    min_value=10,
    max_value=40,
    value=temp_default,
    step=1
)

current_humidity = st.sidebar.slider(
    "Humidity (%):",
    min_value=40,
    max_value=100,
    value=humidity_default,
    step=1
)

current_rainfall = st.sidebar.slider(
    "Recent Rainfall (mm in last 24h):",
    min_value=0,
    max_value=50,
    value=rainfall_default,
    step=1
)

# --- Prediction Logic (Simplified) ---
# For this demo, we'll primarily use the *historical* data for the selected location.
# A more complex model would use the *current* inputs to adjust the prediction.

# Find the record(s) for the selected location
location_data = df[df['Location'] == selected_location].copy() # Use .copy() to avoid SettingWithCopyWarning

if not location_data.empty:
    # For simplicity, take the average risk score and most common disease for that location
    avg_risk_score = location_data['Disease_Risk_Score'].mean()
    predicted_disease = location_data['Predicted_Disease'].mode()[0] # Get the most frequent disease

    # Simulate adjustment based on current conditions (Simple Rule Example)
    risk_adjustment_factor = 1.0
    if current_temp > 28 and current_humidity > 80:
        risk_adjustment_factor = 1.1 # Increase risk slightly in hot & humid conditions
    elif current_temp < 18 and current_rainfall == 0:
        risk_adjustment_factor = 0.9 # Decrease risk slightly in cool & dry conditions

    # Apply adjustment (capped at 100)
    adjusted_risk_score = min(round(avg_risk_score * risk_adjustment_factor), 100)

else:
    predicted_disease = "N/A"
    adjusted_risk_score = 0
    avg_risk_score = 0

# --- Display Prediction ---
st.header(f"Prediction for: {selected_location}")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Predicted Disease", value=predicted_disease)

with col2:
    st.metric(
        label="Adjusted Risk Score (0-100)",
        value=f"{adjusted_risk_score}%",
        delta=f"{round(adjusted_risk_score - avg_risk_score, 1)}% vs Avg", # Show change from average
        delta_color="inverse" # Red delta = higher risk (worse)
    )

st.markdown("---") # Separator

# --- Visualizations using Plotly ---
st.header("Data Visualizations")

# 1. Bar Chart: Average Risk Score by Location
st.subheader("Average Disease Risk Score by Location")
avg_risk_by_loc = df.groupby('Location')['Disease_Risk_Score'].mean().reset_index()
fig_bar = px.bar(
    avg_risk_by_loc,
    x='Location',
    y='Disease_Risk_Score',
    title="Average Risk Score Comparison",
    labels={'Disease_Risk_Score': 'Average Risk Score (0-100)'},
    color='Disease_Risk_Score',
    color_continuous_scale=px.colors.sequential.Reds
)
fig_bar.update_layout(xaxis_title="Farm Location", yaxis_title="Avg. Risk Score")
st.plotly_chart(fig_bar, use_container_width=True)


# 2. Scatter Plot: Temperature vs Humidity for Selected Location (or all)
st.subheader(f"Environmental Factors vs. Risk for {selected_location}")
if not location_data.empty:
    fig_scatter = px.scatter(
        location_data,
        x='Avg_Temperature_C',
        y='Avg_Humidity_Percent',
        size='Disease_Risk_Score', # Size of bubble represents risk
        color='Predicted_Disease', # Color represents disease type
        hover_name='Location',
        hover_data=['Avg_Rainfall_mm', 'Disease_Risk_Score'],
        title=f"Temperature vs. Humidity Analysis for {selected_location}",
        labels={
            'Avg_Temperature_C': 'Average Temperature (°C)',
            'Avg_Humidity_Percent': 'Average Humidity (%)'
        }
    )
    # Add marker for current input conditions
    fig_scatter.add_trace(go.Scatter(
        x=[current_temp],
        y=[current_humidity],
        mode='markers',
        marker=dict(color='lime', size=15, symbol='star'),
        name='Current Conditions Input'
    ))
    fig_scatter.update_layout(legend_title_text='Predicted Disease')
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning(f"No detailed environmental data available to plot for {selected_location}.")


# 3. Optional: Show Raw Data Table
if st.checkbox("Show Raw Data Table"):
    st.subheader("Raw Data")
    st.dataframe(df)

st.sidebar.markdown("---")
st.sidebar.info("Created based on the Crop Disease Prediction Case Study.")