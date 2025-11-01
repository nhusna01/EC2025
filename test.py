import streamlit as st

st.set_page_config(
    page_title="Student Survey"
)
visualise = st.Page('studentSurvey.py', title='Pencapaian Akademik Pelajar', icon=":material/school:")


st.set_page_config(
    page_title="Study of AV Accident Survey Data"
)
visualise = st.Page('StudentCoursework.py', title='Student Academic', icon=":material/book:")

home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [home, visualise]
        }
    )

pg.run()
