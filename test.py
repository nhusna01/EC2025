import streamlit as st
import plotly.express as px
import pandas as pd

# Define the URL
url = "https://raw.githubusercontent.com/nhusna01/EC2025/refs/heads/main/arts_faculty_data.csv"

# Set the title for the Streamlit app
st.title("Arts Faculty Data Viewer")

@st.cache_data
def load_data(data_url):
    """
    Loads the data from the URL, handles the encoding, and caches the result.
    """
    try:
        # Read the CSV from the URL with specified encoding
        arts_df = pd.read_csv(data_url, encoding='latin1')
        return arts_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

# Load the data
arts_df = load_data(url)

# Check if the DataFrame is not empty before displaying
if not arts_df.empty:
    # Display the head of the DataFrame using Streamlit's st.dataframe
    st.subheader("Head of Arts Faculty Data")
    st.dataframe(arts_df.head()) # Use st.dataframe or st.table for display
    
    # Optional: Display the shape (rows, columns)
    st.write(f"Data successfully loaded. Shape: {arts_df.shape}")



# Define the URL for the data source
url = "https://raw.githubusercontent.com/nhusna01/EC2025/refs/heads/main/arts_faculty_data.csv"

# --- Data Loading (Best practice in Streamlit) ---
@st.cache_data
def load_data(data_url):
    """Loads and caches the arts faculty data."""
    try:
        arts_df = pd.read_csv(data_url, encoding='latin1')
        return arts_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

arts_df = load_data(url)
# ----------------------------------------------------

# Streamlit App Logic
st.title("Gender Distribution in Arts Faculty (Plotly)")

if not arts_df.empty:
    def plot_gender_distribution(df):
        # 1. Calculate gender counts and convert to DataFrame for Plotly
        gender_counts = df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count'] # Rename columns for clarity

        # 2. Create the Plotly Pie Chart using Plotly Express
        fig = px.pie(
            gender_counts,
            values='Count',
            names='Gender',
            title='Distribution of Gender in Arts Faculty',
            hole=0.3, # Optional: Creates a donut chart
            color_discrete_sequence=px.colors.qualitative.Pastel # Use a qualitative color scheme
        )

        # 3. Update layout for better appearance
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            title_x=0.5, # Center the title
            uniformtext_minsize=12,
            uniformtext_mode='hide'
        )

        # 4. Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Execute the plotting function
    plot_gender_distribution(arts_df)
else:
    st.warning("Data could not be loaded or is empty. Cannot generate the chart.")
