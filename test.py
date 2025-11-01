import streamlit as st
from st_pages import Page, show_pages

# Page Setup
st.set_page_config(page_title="Dashboard", page_icon=":material/home:")

# Sidebar Navigation Pages
show_pages([
    Page("home.py", title="Homepage", icon=":material/home:"),
    Page("studentSurvey.py", title="Student Survey", icon=":material/school:"),
    Page("StudentCoursework.py", title="Student Coursework", icon=":material/book:"),
    Page("AV_Accident.py", title="AV Accident Survey", icon=":material/car:")
])
