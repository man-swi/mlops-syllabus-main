# iris_filter_api.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import io
import base64
import os
from sklearn.datasets import load_iris

# --- Data Filtering and Plotting Class ---
class IrisDataFilter:
    def __init__(self):
        """Loads the Iris dataset from scikit-learn."""
        try:
            iris = load_iris()
            self.df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
            self.df['Species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
            self.species_list = list(iris.target_names)
            print("Iris data loaded successfully from scikit-learn.")
            print(f"Available species: {self.species_list}")
        except Exception as e:
            print(f"Error loading Iris data: {e}")
            self.df = None
            self.species_list = []

    def filter_by_species(self, species_name: str):
        """Filters the DataFrame by species name."""
        if self.df is None:
            return None
        if species_name not in self.species_list:
            print(f"Error: Species '{species_name}' not valid. Choose from {self.species_list}")
            return None # Indicate invalid species
        try:
            filtered_df = self.df[self.df['Species'] == species_name].copy()
            return filtered_df
        except Exception as e:
             print(f"Error filtering data: {e}")
             return None

    def plot_feature_distribution(self, data: pd.DataFrame, feature1: str, feature2: str):
        """Generates a scatter plot for two features of the filtered data."""
        if data is None or data.empty:
            print("No data to plot.")
            return None
        if feature1 not in data.columns or feature2 not in data.columns:
            print(f"Error: One or both features ('{feature1}', '{feature2}') not found.")
            return None

        try:
            plt.figure(figsize=(8, 6)) # Create new figure
            sns.scatterplot(data=data, x=feature1, y=feature2, hue='Species', palette='viridis', s=100) # s for size
            plt.title(f'{feature1} vs {feature2} (Species: {data["Species"].iloc[0]})')
            plt.xlabel(feature1)
            plt.ylabel(feature2)
            plt.grid(True)
            plt.tight_layout()

            # Save plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close() # Close the plot
            return buf
        except Exception as e:
            print(f"Error generating plot: {e}")
            plt.close() # Ensure plot is closed
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
app = FastAPI(title="Iris Data API")

# Load the filter
iris_filter = IrisDataFilter()

@app.get("/iris/filter/", tags=["Iris Data"])
async def get_filtered_iris_data(species: str,
                                feature1: str = 'sepal length (cm)',
                                feature2: str = 'petal length (cm)'):
    """
    Filters iris data by species and returns count and a
    scatter plot of two specified features.
    Valid species: setosa, versicolor, virginica
    Example features: 'sepal length (cm)', 'sepal width (cm)',
                      'petal length (cm)', 'petal width (cm)'
    """
    if iris_filter.df is None:
        raise HTTPException(status_code=500, detail="Iris dataset not loaded.")

    filtered_data = iris_filter.filter_by_species(species)

    if filtered_data is None:
         raise HTTPException(status_code=400, detail=f"Invalid species '{species}'. Choose from {iris_filter.species_list}")
    if filtered_data.empty:
         # This case shouldn't happen if species is valid, but good practice
         return {"message": f"No data found for species '{species}'", "filtered_data_count": 0, "plot_base64": None}

    # Generate plot using specified or default features
    plot_buffer = iris_filter.plot_feature_distribution(filtered_data, feature1, feature2)
    plot_base64 = iris_filter.plot_to_base64(plot_buffer)

    if plot_base64 is None:
         # Handle case where plotting failed
         raise HTTPException(status_code=500, detail=f"Plot generation failed for features '{feature1}' vs '{feature2}'. Check if features exist.")

    return JSONResponse(content={
        "message": f"Data filtered for species '{species}'",
        "filtered_data_count": len(filtered_data),
        "features_plotted": (feature1, feature2),
        "plot_base64": plot_base64 # Base64 string of the plot PNG
    })

@app.get("/", tags=["Info"])
async def read_root_iris():
    return {"message": "Welcome to the Iris Data API. Use /iris/filter/ endpoint. Go to /docs for details."}


# --- To Run ---
# Save as iris_filter_api.py
# Run in terminal: uvicorn iris_filter_api:app --reload
# Access endpoint e.g., http://127.0.0.1:8000/iris/filter/?species=versicolor
# Or: http://127.0.0.1:8000/iris/filter/?species=setosa&feature1=sepal%20width%20(cm)&feature2=petal%20width%20(cm)