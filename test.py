
import streamlit as st
from st_pages import Page, show_pages

# Only call this ONCE
st.set_page_config(
    page_title="Student Survey",
    page_icon=":material/school:"
)

# Define your pages correctly
show_pages([
    Page("studentSurvey.py", title="Pencapaian Akademik Pelajar", icon=":material/school:"),
    Page("StudentCoursework.py", title="Student Academic", icon=":material/book:")
])


home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [home, visualise]
        }
    )

pg.run()
