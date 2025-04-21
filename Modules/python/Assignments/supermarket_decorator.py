# supermarket_decorator.py
import pandas as pd
import matplotlib.pyplot as plt
import time
import functools # For wraps
import os

# --- Timing Decorator ---
def timing_decorator(func):
    """Prints the execution time of the decorated function."""
    @functools.wraps(func) # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter() # More precise than time.time()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        # Print info about which function was timed
        # args[0] is typically 'self' for instance methods
        if args and hasattr(args[0], '__class__'):
            print(f"'{args[0].__class__.__name__}.{func.__name__}' executed in {elapsed_time:.4f} seconds")
        else:
            print(f"'{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper

# --- Data Processing Class ---
class SalesDataProcessor:
    """Processes and visualizes supermarket sales data."""
    def __init__(self, csv_path="supermarket_sales - Sheet1.csv"):
        """Loads and preprocesses the sales data."""
        try:
            self.df = pd.read_csv(csv_path)
            # Convert 'Date' to datetime objects and 'Time' if needed
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            # Optional: Combine Date and Time if specific timestamp analysis is needed
            # self.df['Timestamp'] = pd.to_datetime(self.df['Date'].astype(str) + ' ' + self.df['Time'])
            print(f"Sales data loaded successfully from {csv_path}")
        except FileNotFoundError:
            print(f"Error: File not found at {csv_path}")
            self.df = None
        except KeyError as e:
             print(f"Error: Column {e} not found. Check CSV column names.")
             self.df = None
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = None

    @timing_decorator
    def summarize_total_sales(self):
        """Calculates and prints the total sales."""
        if self.df is None:
            print("DataFrame not loaded.")
            return None
        try:
            total_sales = self.df['Total'].sum()
            print(f"\n--- Total Sales Summary ---")
            print(f"Total Sales Revenue: ${total_sales:,.2f}")
            return total_sales
        except KeyError:
             print("Error: 'Total' column not found.")
             return None
        except Exception as e:
            print(f"Error calculating total sales: {e}")
            return None

    @timing_decorator
    def plot_sales_over_time(self, save_dir="plots"):
        """Plots total daily sales over time."""
        if self.df is None:
            print("DataFrame not loaded.")
            return

        try:
            daily_sales = self.df.groupby(self.df['Date'].dt.date)['Total'].sum() # Group by date part only

            plt.figure(figsize=(12, 6)) # Create new figure
            daily_sales.plot(kind='line', marker='o', linestyle='-')
            plt.title('Total Daily Sales Over Time')
            plt.xlabel('Date')
            plt.ylabel('Total Sales')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()

             # --- Saving Logic ---
            if save_dir:
                try:
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    save_path = os.path.join(save_dir, "daily_sales_over_time.png")
                    plt.savefig(save_path)
                    print(f"\nPlot saved to {save_path}")
                except Exception as e:
                    print(f"Error saving plot: {e}")

            plt.show()
        except KeyError:
             print("Error: 'Date' or 'Total' column not found for plotting.")
        except Exception as e:
            print(f"Error plotting sales over time: {e}")
        finally:
            plt.close() # Ensure plot is closed

# --- How to Use ---
if __name__ == "__main__":
    # Ensure 'supermarket_sales - Sheet1.csv' (or renamed version) is available
    processor = SalesDataProcessor(csv_path="supermarket_sales - Sheet1.csv")

    if processor.df is not None:
        processor.summarize_total_sales()
        processor.plot_sales_over_time(save_dir="supermarket_plots")