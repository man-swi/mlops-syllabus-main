# house_predictor_api.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import numpy as np # For handling potential NaN in prediction

# --- Pydantic Model for Input Features ---
# Based on common influential features (simplified)
class HouseFeatures(BaseModel):
    GrLivArea: float  # Above grade (ground) living area square feet
    BedroomAbvGr: int  # Bedrooms above grade (does NOT include basement bedrooms)
    FullBath: int      # Full bathrooms above grade
    YearBuilt: int     # Original construction date
    TotalBsmtSF: float # Total square feet of basement area (handle potential missing)

# --- Prediction Class ---
class HousePricePredictor:
    def __init__(self, train_csv_path="house.csv"):
        self.model = None
        self.imputer = None
        self.features = ['GrLivArea', 'BedroomAbvGr', 'FullBath', 'YearBuilt', 'TotalBsmtSF']
        self._train_model(train_csv_path)

    def _train_model(self, train_csv_path):
        try:
            df = pd.read_csv(train_csv_path)
            print(f"Training data loaded from {train_csv_path}")

            # Select features and target
            X = df[self.features]
            y = df['SalePrice']

            # Handle missing values (simple imputation)
            # Impute missing TotalBsmtSF with the mean
            self.imputer = SimpleImputer(strategy='mean')
            X_imputed = self.imputer.fit_transform(X)
            X_imputed_df = pd.DataFrame(X_imputed, columns=self.features) # Convert back for train/test split

            # Check for NaNs in target and remove corresponding rows in X and y
            nan_price_indices = y.isnull()
            if nan_price_indices.any():
                print(f"Warning: Removing {nan_price_indices.sum()} rows due to missing SalePrice.")
                y = y[~nan_price_indices]
                X_imputed_df = X_imputed_df[~nan_price_indices]


            # Basic check if data remains after cleaning
            if X_imputed_df.empty or y.empty:
                 print("Error: No valid data remaining after cleaning missing values.")
                 return


            # Split data (optional for this simple example, could train on all)
            X_train, X_test, y_train, y_test = train_test_split(
                X_imputed_df, y, test_size=0.2, random_state=42
            )

            # Train a simple Linear Regression model
            self.model = LinearRegression()
            self.model.fit(X_train, y_train)

            # Evaluate (optional)
            y_pred = self.model.predict(X_test)
            rmse = mean_squared_error(y_test, y_pred, squared=False)
            print(f"Model trained. RMSE on test set: {rmse:.2f}")

        except FileNotFoundError:
            print(f"Error: Training file not found at {train_csv_path}")
            self.model = None
        except KeyError as e:
            print(f"Error: Column {e} not found in training data. Check feature names.")
            self.model = None
        except Exception as e:
            print(f"Error during model training: {e}")
            self.model = None

    def preprocess_input(self, features_dict: dict):
        """Converts input dictionary to DataFrame suitable for prediction."""
        try:
            # Create DataFrame with columns in the correct order
            input_df = pd.DataFrame([features_dict], columns=self.features)
            # Impute potential missing values using the trained imputer
            input_imputed = self.imputer.transform(input_df)
            return input_imputed
        except Exception as e:
            print(f"Error preprocessing input: {e}")
            return None

    def predict(self, input_data):
        """Predicts house price for the given input data."""
        if self.model is None:
            return {"error": "Model not trained or loaded."}
        if input_data is None:
            return {"error": "Input preprocessing failed."}

        try:
            prediction = self.model.predict(input_data)
             # Handle potential NaN or infinite values in prediction
            if np.isnan(prediction[0]) or not np.isfinite(prediction[0]):
                return {"error": "Prediction resulted in invalid number."}

            return {"predicted_sale_price": round(prediction[0], 2)}
        except Exception as e:
            print(f"Error during prediction: {e}")
            return {"error": "Prediction failed."}


# --- FastAPI Application ---
app = FastAPI(title="House Price Predictor API")

# Load the predictor (ensure 'train.csv' is available)
predictor = HousePricePredictor(train_csv_path="train.csv")

@app.post("/predict/", tags=["Prediction"])
async def predict_house_price(features: HouseFeatures):
    """
    Predicts the house sale price based on input features.
    Provide features like GrLivArea, BedroomAbvGr, FullBath, YearBuilt, TotalBsmtSF.
    """
    if predictor.model is None:
        return {"error": "Model is not available."}

    features_dict = features.dict()
    preprocessed_data = predictor.preprocess_input(features_dict)
    prediction_result = predictor.predict(preprocessed_data)
    return prediction_result

@app.get("/", tags=["Info"])
async def read_root():
    return {"message": "Welcome to the House Price Prediction API. Go to /docs for details."}

# --- To Run ---
# Save as house_predictor_api.py
# Ensure train.csv from Kaggle is in the same directory
# Run in terminal: uvicorn house_predictor_api:app --reload
# Access docs at http://127.0.0.1:8000/docs