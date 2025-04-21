# mall_iterator.py
import pandas as pd

class ChunkIterator:
    """
    Custom iterator to process a CSV dataset in chunks.
    """
    def __init__(self, csv_path="Mall_Customers.csv", chunk_size=10):
        """
        Initializes the iterator.

        Args:
            csv_path (str): Path to the CSV file.
            chunk_size (int): Number of rows per chunk.
        """
        self.csv_path = csv_path
        self.chunk_size = chunk_size
        self.file_iterator = None
        print(f"ChunkIterator initialized for '{csv_path}' with chunk size {chunk_size}.")

    def __iter__(self):
        """Returns the iterator object (self) and initializes the pandas iterator."""
        try:
            # Create the TextFileReader object which yields DataFrames
            self.file_iterator = pd.read_csv(self.csv_path, chunksize=self.chunk_size)
            print("Starting iteration...")
            return self
        except FileNotFoundError:
            print(f"Error: File not found at {self.csv_path}")
            # Return an empty iterator to prevent errors downstream
            return iter([])
        except Exception as e:
            print(f"Error initializing pandas chunk reader: {e}")
            return iter([])


    def __next__(self):
        """Returns the next chunk from the dataset."""
        if self.file_iterator is None:
            raise StopIteration # Ensure __iter__ was called or handled initialization error

        try:
            # Get the next DataFrame chunk from the pandas iterator
            chunk = next(self.file_iterator)
            return chunk
        except StopIteration:
            # Pandas iterator is exhausted, signal the end
            print("Iteration finished.")
            raise StopIteration
        except Exception as e:
            print(f"Error reading next chunk: {e}")
            raise StopIteration # Stop iteration on error

    def get_chunk_stats(self, chunk_df: pd.DataFrame):
        """Calculates and returns basic statistics for a given chunk."""
        if not isinstance(chunk_df, pd.DataFrame) or chunk_df.empty:
            return {"error": "Invalid or empty chunk provided."}
        try:
            # Calculate basic stats only for numeric columns
            numeric_stats = chunk_df.describe(include='number')
            return numeric_stats
        except Exception as e:
            print(f"Error calculating stats for chunk: {e}")
            return {"error": "Could not calculate statistics."}

# --- How to Use ---
if __name__ == "__main__":
    # Ensure Mall_Customers.csv is in the same directory or provide full path
    chunk_iterator = ChunkIterator(csv_path="Mall_Customers.csv", chunk_size=50)
    chunk_number = 1

    # Iterate through the chunks
    try:
        for data_chunk in chunk_iterator:
            print(f"\n--- Processing Chunk {chunk_number} ---")
            print(f"Chunk shape: {data_chunk.shape}")
            # print("Chunk Head:")
            # print(data_chunk.head()) # Optional: print head of chunk

            # Get and print stats for the chunk
            stats = chunk_iterator.get_chunk_stats(data_chunk)
            print("\nChunk Statistics (Numeric Columns):")
            print(stats)

            chunk_number += 1
    except Exception as e:
        print(f"\nAn error occurred during iteration: {e}")