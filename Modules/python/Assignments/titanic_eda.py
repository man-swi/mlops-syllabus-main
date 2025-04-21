# titanic_eda.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class TitanicEDA:
    """Performs basic Exploratory Data Analysis on the Titanic dataset."""

    def __init__(self, csv_path="titanic.csv"):
        """Loads the Titanic dataset."""
        try:
            self.df = pd.read_csv(csv_path)
            print(f"Data loaded successfully from {csv_path}")
            # Basic preprocessing: Fill missing Age with median for visualization
            self.df['Age'].fillna(self.df['Age'].median(), inplace=True)
            # Fill missing Embarked with mode
            self.df['Embarked'].fillna(self.df['Embarked'].mode()[0], inplace=True)
        except FileNotFoundError:
            print(f"Error: File not found at {csv_path}")
            self.df = None
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = None

    def summary_stats(self):
        """Prints summary statistics of the dataset."""
        if self.df is not None:
            print("\n--- Dataset Info ---")
            self.df.info()
            print("\n--- Descriptive Statistics (Numeric) ---")
            print(self.df.describe())
            print("\n--- Descriptive Statistics (Object) ---")
            print(self.df.describe(include=['object']))
        else:
            print("DataFrame not loaded. Cannot generate stats.")

    def plot_survival_distribution(self, feature, save_dir="plots"):
        """
        Visualizes the distribution of survival rates based on a given feature.

        Args:
            feature (str): The column name to analyze (e.g., 'Pclass', 'Sex', 'Age', 'Embarked').
            save_dir (str): Directory to save the plot image. Creates if not exists.
        """
        if self.df is None:
            print("DataFrame not loaded. Cannot generate plot.")
            return
        if feature not in self.df.columns:
            print(f"Error: Feature '{feature}' not found in the dataset.")
            return

        plt.figure(figsize=(10, 6)) # Create a new figure for each plot

        # --- Plotting Logic ---
        if self.df[feature].dtype == 'object' or self.df[feature].nunique() < 10:
            # Categorical feature: Use countplot
            sns.countplot(data=self.df, x=feature, hue='Survived', palette='viridis')
            plt.title(f'Survival Distribution by {feature}')
            plt.ylabel('Count')
        else:
            # Numerical feature: Use histogram or KDE plot
            sns.histplot(data=self.df, x=feature, hue='Survived', kde=True, palette='viridis', bins=30)
            plt.title(f'Survival Distribution by {feature}')
            plt.ylabel('Frequency')

        plt.xlabel(feature)
        plt.xticks(rotation=45, ha='right') # Improve readability for categorical labels
        plt.tight_layout() # Adjust layout

        # --- Saving Logic ---
        if save_dir:
            try:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                save_path = os.path.join(save_dir, f"survival_by_{feature}.png")
                plt.savefig(save_path)
                print(f"Plot saved to {save_path}")
            except Exception as e:
                print(f"Error saving plot: {e}")

        plt.show() # Display the plot

# --- How to Use ---
if __name__ == "__main__":
    # Ensure you have 'titanic.csv' (or the correct filename like 'train.csv')
    # in the same directory or provide the full path.
    # Often the Kaggle file is named 'train.csv' for the training set.
    eda = TitanicEDA(csv_path="train.csv") # Use 'train.csv' if that's the file

    if eda.df is not None:
        eda.summary_stats()

        # Create and save plots
        plot_directory = "titanic_plots"
        eda.plot_survival_distribution('Pclass', save_dir=plot_directory)
        eda.plot_survival_distribution('Sex', save_dir=plot_directory)
        eda.plot_survival_distribution('Age', save_dir=plot_directory)
        eda.plot_survival_distribution('Embarked', save_dir=plot_directory)
        eda.plot_survival_distribution('SibSp', save_dir=plot_directory) # Siblings/Spouses
        eda.plot_survival_distribution('Parch', save_dir=plot_directory) # Parents/Children