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




# Load the data
file_name = "arts_faculty_data.csv"
arts_df = pd.read_csv(file_name)

# 1. Identify GPA columns (indices 12 to 23 inclusive, based on previous inspection)
gpa_cols_full = arts_df.columns[12:24].tolist()

# 2. Convert GPA columns to numeric
for col in gpa_cols_full:
    arts_df[col] = pd.to_numeric(arts_df[col], errors='coerce')

# Select only the relevant columns and drop rows with missing Arts Program
plot_df = arts_df[['Arts Program'] + gpa_cols_full].dropna(subset=['Arts Program'])

# 3. Melt the DataFrame to long format
# 'id_vars' are columns to keep, 'value_vars' are columns to unpivot (GPA semesters)
melted_df = plot_df.melt(
    id_vars='Arts Program',
    value_vars=gpa_cols_full,
    var_name='Semester Name',
    value_name='GPA'
).dropna(subset=['GPA'])

# 4. Create a numerical semester order column for correct plotting
semester_order_map = {name: i + 1 for i, name in enumerate(gpa_cols_full)}
melted_df['Semester Order'] = melted_df['Semester Name'].map(semester_order_map)

# 5. Calculate the mean GPA for each Arts Program at each Semester
gpa_trend_df = melted_df.groupby(['Arts Program', 'Semester Order', 'Semester Name'])['GPA'].mean().reset_index()

# 6. Create the Plotly Line Chart
fig = px.line(
    gpa_trend_df,
    x='Semester Name',
    y='GPA',
    color='Arts Program',
    markers=True,
    title='Average GPA Trend by Arts Program Over Academic Semesters'
)

# Customise axes and layout for better readability
fig.update_xaxes(
    tickangle=45,
    title_text='Academic Semester',
    categoryorder='array',
    categoryarray=gpa_cols_full # Ensure semesters are in the correct chronological order
)
fig.update_yaxes(
    title_text='Average GPA',
    range=[2.5, 4.0] # Set a relevant range for GPA
)
fig.update_layout(
    height=600,
    width=1000,
    hovermode="x unified",
    legend_title_text='Arts Program'
)

# Save the plot as an HTML file for easy viewing and Streamlit integration
fig.write_html("gpa_trend_line_chart.html")
