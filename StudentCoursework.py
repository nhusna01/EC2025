import streamlit as st
import pandas as pd

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="AV Accident Survey Data", layout="wide")

# --- CSV File Path (from GitHub Raw Link) ---
csv_url = "https://raw.githubusercontent.com/nhusna01/EC2025/refs/heads/main/processed_av_accident_data.csv"

st.title("AV Accident Data Viewer")

try:
    # Load the CSV file from GitHub URL
    df = pd.read_csv(csv_url)
    st.success("CSV file loaded successfully from GitHub!")
    
    # Display dataset preview
    st.dataframe(df, use_container_width=True)

    # Optional: Show dataset info
    st.write("### Dataset Summary")
    st.write(df.describe(include='all'))

except Exception as e:
    st.error(f" An error occurred while loading the data: {e}")

