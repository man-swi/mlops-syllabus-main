# wine_filter_api.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import io
import base64
import os

# --- Data Filtering and Plotting Class ---
class WineDataFilter:
    def __init__(self, csv_path="winequality-red.csv"):
        """Loads the Wine Quality dataset."""
        try:
            self.df = pd.read_csv(csv_path)
            # Handle potential separator issues if needed (sometimes it's ';')
            if self.df.shape[1] == 1: # Check if only one column was loaded
                 print("Attempting to reload with ';' separator.")
                 self.df = pd.read_csv(csv_path, sep=';')
            print(f"Wine data loaded successfully from {csv_path}")
        except FileNotFoundError:
            print(f"Error: File not found at {csv_path}")
            self.df = None
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = None

    def filter_by_quality(self, min_quality: int = 7):
        """Filters the DataFrame for wines with quality >= min_quality."""
        if self.df is None:
            return None
        try:
            filtered_df = self.df[self.df['quality'] >= min_quality].copy()
            return filtered_df
        except KeyError:
             print("Error: 'quality' column not found.")
             return None
        except Exception as e:
             print(f"Error filtering data: {e}")
             return None

    def plot_feature_distribution(self, data: pd.DataFrame, feature: str):
        """Generates a histogram for a specific feature."""
        if data is None or data.empty:
            print("No data to plot.")
            return None
        if feature not in data.columns:
            print(f"Feature '{feature}' not found.")
            return None

        try:
            plt.figure(figsize=(8, 5)) # Create a new figure
            sns.histplot(data[feature], kde=True, bins=15)
            plt.title(f'Distribution of {feature} (Quality >= {data["quality"].min()})')
            plt.xlabel(feature)
            plt.ylabel('Frequency')
            plt.tight_layout()

            # Save plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close() # Close the plot to free memory
            return buf
        except Exception as e:
            print(f"Error generating plot: {e}")
            plt.close() # Ensure plot is closed on error
            return None

    def plot_to_base64(self, plot_buffer: io.BytesIO):
        """Converts a plot buffer to a base64 encoded string."""
        if plot_buffer is None:
            return None
        try:
            img_base64 = base64.b64encode(plot_buffer.read()).decode('utf-8')
            return f"data:image/png;base64,{img_base64}"
        except Exception as e:
            print(f"Error encoding plot: {e}")
            return None

# --- FastAPI Application ---
app = FastAPI(title="Wine Data API")

# Load the filter (ensure 'winequality-red.csv' is available)
wine_filter = WineDataFilter(csv_path="winequality-red.csv")

@app.get("/wine/filter/", tags=["Wine Data"])
async def get_filtered_wine_data(min_quality: int = 7, feature: str = 'alcohol'):
    """
    Filters red wine data by minimum quality and returns count
    and a distribution plot of a specified feature (default: alcohol).
    """
    if wine_filter.df is None:
        raise HTTPException(status_code=500, detail="Wine dataset not loaded.")

    filtered_data = wine_filter.filter_by_quality(min_quality)

    if filtered_data is None:
         raise HTTPException(status_code=404, detail=f"'quality' column not found or error filtering.")
    if filtered_data.empty:
         return {"message": f"No wines found with quality >= {min_quality}", "filtered_data_count": 0, "plot_base64": None}


    plot_buffer = wine_filter.plot_feature_distribution(filtered_data, feature)
    plot_base64 = wine_filter.plot_to_base64(plot_buffer)

    if plot_base64 is None:
        # Handle case where plotting failed but data exists
         return {"message": f"Filtered data available, but plot generation failed for feature '{feature}'.",
                 "filtered_data_count": len(filtered_data),
                 "plot_base64": None}


    return JSONResponse(content={
        "message": f"Data filtered for quality >= {min_quality}",
        "filtered_data_count": len(filtered_data),
        "feature_plotted": feature,
        "plot_base64": plot_base64 # Base64 string of the plot PNG
    })

@app.get("/", tags=["Info"])
async def read_root_wine():
    return {"message": "Welcome to the Wine Data API. Use /wine/filter/ endpoint. Go to /docs for details."}


# --- To Run ---
# Save as wine_filter_api.py
# Ensure winequality-red.csv from Kaggle is in the same directory
# Run in terminal: uvicorn wine_filter_api:app --reload
# Access endpoint e.g., http://127.0.0.1:8000/wine/filter/?min_quality=6&feature=volatile%20acidity