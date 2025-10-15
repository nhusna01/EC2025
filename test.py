import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go


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





# Example: arts_df is your dataset
# arts_df = pd.read_csv("your_dataset.csv")

st.title("Distribution of Bachelor Academic Year by Gender")

# Group by Gender and Academic Year and count occurrences
gender_year_counts = (
    arts_df.groupby(['Gender', 'Bachelor  Academic Year in EU'])
    .size()
    .reset_index(name='Count')
)

# Create grouped bar chart using Plotly Express
fig = px.bar(
    gender_year_counts,
    x='Gender',
    y='Count',
    color='Bachelor  Academic Year in EU',
    barmode='group',
    title='Distribution of Bachelor Academic Year by Gender',
    labels={'Gender': 'Gender', 'Count': 'Count', 'Bachelor  Academic Year in EU': 'Academic Year'},
    template='plotly_white'
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)





# Example: arts_df = pd.read_csv("your_dataset.csv")

st.title("Distribution of SSC and HSC GPA in Arts Faculty (Bright Colors)")

# Convert GPA columns to numeric
arts_df['S.S.C (GPA)'] = pd.to_numeric(arts_df['S.S.C (GPA)'], errors='coerce')
arts_df['H.S.C (GPA)'] = pd.to_numeric(arts_df['H.S.C (GPA)'], errors='coerce')

# Drop rows with missing GPA values
gpa_df = arts_df.dropna(subset=['S.S.C (GPA)', 'H.S.C (GPA)'])

# Define bright color palette
bright_colors = ['#FF5733', '#00BFFF']  # Bright orange & electric blue

# Create histogram for SSC GPA
fig_ssc = px.histogram(
    gpa_df,
    x='S.S.C (GPA)',
    nbins=20,
    title='Distribution of SSC GPA in Arts Faculty',
    color_discrete_sequence=[bright_colors[0]],
    marginal='box',  # Adds a boxplot on top
    template='plotly_white'
)

# Create histogram for HSC GPA
fig_hsc = px.histogram(
    gpa_df,
    x='H.S.C (GPA)',
    nbins=20,
    title='Distribution of HSC GPA in Arts Faculty',
    color_discrete_sequence=[bright_colors[1]],
    marginal='box',
    template='plotly_white'
)

# Customize layout style for both charts
for fig in [fig_ssc, fig_hsc]:
    fig.update_layout(
        title_font_size=20,
        font=dict(size=14, color='#222'),
        bargap=0.1,
        plot_bgcolor='rgba(240,240,240,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        showlegend=False
    )

# Display both histograms side-by-side in Streamlit
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_ssc, use_container_width=True)
with col2:
    st.plotly_chart(fig_hsc, use_container_width=True)






file_name = "arts_faculty_data.csv"
arts_df = pd.read_csv(file_name)

st.title("Average Student Expectations & Satisfaction by Gender (Interactive Radar Chart)")

# Clean column names (remove leading/trailing spaces)
arts_df.columns = arts_df.columns.str.strip()


spider_cols_full = [
    'Q3 [What was your expectation about the University as related to quality of resources?]',
    'Q4 [What was your expectation about the University as related to quality of learning environment?]',
    'Q5 [To what extent your expectation was met?]',
    'Q6 [What are the best aspects of the program?]'
]

# Check if all columns exist
missing_cols = [col for col in spider_cols_full if col not in arts_df.columns]
if missing_cols:
    st.error(f"Missing columns in your dataset: {missing_cols}")
    st.stop()

# Convert to numeric safely
for col in spider_cols_full:
    arts_df[col] = pd.to_numeric(arts_df[col], errors='coerce')

# Handle Gender column
if 'Gender' not in arts_df.columns:
    st.error("Column 'Gender' not found in dataset. Please check the exact column name.")
    st.stop()

# Drop rows with missing Gender or numeric responses
arts_df = arts_df.dropna(subset=['Gender'] + spider_cols_full)

# Group by Gender and compute mean values
spider_data = arts_df.groupby('Gender')[spider_cols_full].mean().reset_index()


categories_abbr = [
    'Q3: Resources (Expectation)',
    'Q4: Learning Env. (Expectation)',
    'Q5: Expectation Met',
    'Q6: Best Aspects'
]


fig = go.Figure()

# Bright colors
colors = {'Female': '#00BFFF', 'Male': '#FF5733'}

# Add trace per gender
for i in range(len(spider_data)):
    gender = spider_data.loc[i, 'Gender']
    values = spider_data.loc[i, spider_cols_full].values.flatten().tolist()
    values += values[:1]  # Close the loop

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories_abbr + [categories_abbr[0]],
        fill='toself',
        name=str(gender),
        line=dict(color=colors.get(gender, '#888'), width=3),
        fillcolor=colors.get(gender, '#888'),
        opacity=0.4
    ))


fig.update_layout(
    polar=dict(
        bgcolor='white',
        radialaxis=dict(
            visible=True,
            range=[0, 5],
            tickvals=[1, 2, 3, 4, 5],
            tickfont=dict(size=11, color='grey')
        ),
        angularaxis=dict(
            tickfont=dict(size=12, color='black')
        )
    ),
    showlegend=True,
    legend=dict(
        title="Gender",
        font=dict(size=12),
        bgcolor='rgba(255,255,255,0.7)'
    ),
    title=dict(
        text='Average Student Expectations & Satisfaction by Gender',
        x=0.5,
        font=dict(size=18)
    ),
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)
