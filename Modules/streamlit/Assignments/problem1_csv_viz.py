# Modules/streamlit/Assignments/problem1_csv_viz.py

import streamlit as st
import pandas as pd
import plotly.express as px
import io # Needed for handling byte stream from file uploader

# --- Page Configuration ---
st.set_page_config(
    page_title="CSV Data Visualizer",
    page_icon="📊",
    layout="wide"
)

# --- Title and Description ---
st.title("📊 Problem 1: CSV Data Visualizer")
st.markdown("""
This application allows users to upload a CSV file and visualize its data using
basic charts like Line Charts, Bar Charts, and Histograms.
""")
st.markdown("---")

# --- Use session state to keep track of the dataframe across reruns ---
# Initialize session state variables if they don't exist
if 'dataframe_problem1' not in st.session_state:
    st.session_state.dataframe_problem1 = None
if 'uploaded_filename_problem1' not in st.session_state:
    st.session_state.uploaded_filename_problem1 = None

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="problem1_uploader") # Unique key is good practice

if uploaded_file is not None:
    # Check if it's a new file or the same one to avoid reprocessing
    if uploaded_file.name != st.session_state.uploaded_filename_problem1:
        try:
            # Read the CSV data into a pandas DataFrame
            # Use io.StringIO to decode bytes (handles different encodings better)
            stringio = io.StringIO(uploaded_file.getvalue().decode('utf-8', errors='replace')) # Added error handling for decoding
            df = pd.read_csv(stringio)
            st.session_state.dataframe_problem1 = df # Store df in session state
            st.session_state.uploaded_filename_problem1 = uploaded_file.name # Store filename
            st.success(f"Successfully loaded '{uploaded_file.name}'")
        except pd.errors.ParserError as pe:
             st.error(f"Parsing Error: Could not parse the CSV file. Please ensure it's well-formatted. Details: {pe}")
             st.session_state.dataframe_problem1 = None
             st.session_state.uploaded_filename_problem1 = None
        except UnicodeDecodeError as ude:
            st.error(f"Encoding Error: Could not decode the file using UTF-8. Try saving your CSV with UTF-8 encoding. Details: {ude}")
            st.session_state.dataframe_problem1 = None
            st.session_state.uploaded_filename_problem1 = None
        except Exception as e:
            st.error(f"An unexpected error occurred while reading the CSV file: {e}")
            st.session_state.dataframe_problem1 = None # Reset dataframe on error
            st.session_state.uploaded_filename_problem1 = None
    # If it's the same file, df will be loaded from session state below

    # Assign dataframe from session state for use in the rest of the script
    df = st.session_state.dataframe_problem1

    # --- Display Dataframe and Visualization Options ---
    if df is not None:
        st.markdown("---")
        st.subheader("Data Preview")
        st.dataframe(df.head()) # Display the first few rows

        st.markdown("---")
        st.subheader("Configure Visualization")

        # Get column names safely
        try:
            df_columns = df.columns.tolist()
            numeric_columns = df.select_dtypes(include='number').columns.tolist()
            non_numeric_columns = df.select_dtypes(exclude='number').columns.tolist()
        except AttributeError:
            st.warning("Could not extract columns from the DataFrame. Please check the CSV format.")
            df_columns = []
            numeric_columns = []
            non_numeric_columns = []

        # --- Chart Type Selection ---
        chart_type = st.selectbox("Select Chart Type:", ["Line Chart", "Bar Chart", "Histogram"], key="problem1_chart_type")

        # --- Column Selectors based on Chart Type ---
        col1, col2 = st.columns(2) # Create columns for selectors

        x_axis = None
        y_axis = None
        hist_col = None
        plot_ready = False # Flag to check if columns are selected

        with col1:
            if chart_type == "Line Chart":
                x_axis_options = ["(Use Index)"] + df_columns
                x_axis = st.selectbox("Select X-axis (Optional):", x_axis_options, index=0, key="problem1_line_x")
                with col2:
                    y_axis = st.multiselect("Select Y-axis (Numeric):", numeric_columns, default=numeric_columns[0] if numeric_columns else None, key="problem1_line_y")
                if y_axis: # Need at least one Y-axis column
                    plot_ready = True
                # Map "(Use Index)" back to None for plotting
                if x_axis == "(Use Index)":
                    x_axis = None

            elif chart_type == "Bar Chart":
                if non_numeric_columns:
                     x_axis = st.selectbox("Select Categorical Axis (X-axis):", non_numeric_columns, index=0, key="problem1_bar_x")
                else:
                     st.warning("No non-numeric columns found for the categorical axis.")
                     x_axis = None

                with col2:
                     if numeric_columns:
                          y_axis = st.selectbox("Select Numerical Axis (Y-axis):", numeric_columns, index=0, key="problem1_bar_y")
                     else:
                          st.warning("No numeric columns found for the numerical axis.")
                          y_axis = None
                if x_axis and y_axis:
                    plot_ready = True

            elif chart_type == "Histogram":
                if numeric_columns:
                    hist_col = st.selectbox("Select Column (Numeric):", numeric_columns, index=0, key="problem1_hist_col")
                    plot_ready = True
                else:
                    st.warning("No numeric columns found to create a histogram.")
                    hist_col = None

        # --- Generate Plot ---
        st.markdown("---")
        st.subheader(f"{chart_type} Visualization")

        if plot_ready:
            try:
                fig = None # Initialize fig
                if chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, title=f"Line Chart")
                    if x_axis:
                        fig.update_layout(xaxis_title=x_axis)

                elif chart_type == "Bar Chart":
                    # Simple bar chart - assumes data is already aggregated or suitable
                    # For large datasets, aggregation might be needed before plotting
                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"Bar Chart: {y_axis} by {x_axis}")

                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=hist_col, title=f"Histogram of {hist_col}", nbins=st.slider("Number of bins:", 5, 100, 20, key="problem1_hist_bins")) # Added bins slider


                if fig:
                     st.plotly_chart(fig, use_container_width=True)
                else:
                     # This case should ideally not be reached if plot_ready is True and columns selected
                     st.warning("Plot could not be generated. Please check column selections.")

            except Exception as e:
                st.error(f"An error occurred during plot generation: {e}")
                st.exception(e) # Shows the full traceback for debugging

        else:
            # If plot_ready is False
             if df_columns: # Only show this warning if columns were actually found
                st.warning("Please select appropriate column(s) for the chosen chart type.")

else:
    # If no file is uploaded or cleared, reset session state
    if uploaded_file is None and st.session_state.uploaded_filename_problem1 is not None:
        # This block executes if a file was previously uploaded but now the uploader is empty
        st.session_state.dataframe_problem1 = None
        st.session_state.uploaded_filename_problem1 = None

    st.info("⬆️ Upload a CSV file to get started.")


# --- Optional: Add Footer ---
st.markdown("---")
st.text("Assignment 1 - Built with Streamlit and Plotly.")