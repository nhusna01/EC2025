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


# Define the URL for the data source (from previous steps)
url = "https://raw.githubusercontent.com/nhusna01/EC2025/refs/heads/main/arts_faculty_data.csv"

# --- Data Loading Function with Caching ---
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
# ------------------------------------------

# Streamlit App Execution
st.title("Gender Distribution in Arts Faculty")

if not arts_df.empty:
    # 1. Calculate gender counts and convert to DataFrame format for Plotly
    gender_counts_df = arts_df['Gender'].value_counts().reset_index()
    gender_counts_df.columns = ['Gender', 'Count'] # Rename columns

    # 2. Create the Plotly Pie/Donut Chart
    fig = px.pie(
        gender_counts_df,
        values='Count',
        names='Gender',
        title='Distribution of Gender in Arts Faculty',
        color_discrete_sequence=px.colors.qualitative.D3
    )

    # 3. Update the figure layout for presentation
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label', # Shows both percentage and category label
        marker=dict(line=dict(color='#000000', width=1)) # Adds a black border to slices
    )
    
    fig.update_layout(
        title_x=0.5, # Center the title
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )

    # 4. Display the interactive chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw Data Counts")
    st.dataframe(gender_counts_df)

else:
    st.warning("Data could not be loaded or the 'Gender' column is missing/empty. Cannot generate the chart.")





# --- Data Preparation ---
medium_col = 'H.S.C or Equivalent study medium'
gpa_col = '1st Year Semester 1' # Best available GPA column

# Assuming arts_df is loaded and GPAs are converted to numeric

# Drop rows where the GPA is NaN and clean the medium column
plot_df = arts_df.dropna(subset=[gpa_col])
plot_df[medium_col] = plot_df[medium_col].fillna('Unknown').str.strip()

# Filter out categories with less than 2 observations
medium_counts = plot_df[medium_col].value_counts()
min_observations = 2
valid_mediums = medium_counts[medium_counts >= min_observations].index.tolist()
plot_df = plot_df[plot_df[medium_col].isin(valid_mediums)]


# --- Plotly Histogram Code ---

fig = px.histogram(
    plot_df,
    x=gpa_col,
    color=medium_col,
    marginal="box", # Adds a box plot on top for a concise summary (median/quartiles)
    histnorm='probability density', # Normalises the area to 1, showing the shape of the distribution
    barmode='overlay', # Stacks the bars on top of each other
    opacity=0.6,
    title=f'Distribution of Student Performance ({gpa_col}) by Prior Study Medium'
)

# Customise axes and layout
fig.update_xaxes(
    title_text='GPA (First Year, First Semester)',
    range=[2.5, 4.0] 
)
fig.update_yaxes(
    title_text='Density / Probability'
)
fig.update_layout(
    height=600,
    width=900,
    legend_title_text='Study Medium'
)

# --- Streamlit Integration ---
# In your Streamlit app (e.g., app.py), you would call:
# st.plotly_chart(fig, use_container_width=True) 

# (The output HTML file is 'gpa_medium_histogram.html')
