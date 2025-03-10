import streamlit as st
from streamlit_option_menu import option_menu

from views.home import home_page
from views.dashboard import dashboard_page
from views.stat_des import stat_des_page
from views.ml import ml_page

APP_TITLE = "Challenge Sécurité"

st.set_page_config(
    page_title=APP_TITLE,
    # page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    # st.image("")

    selected = option_menu(
        menu_title="",
        options=[
            "Accueil",
            "Dashboard",
            "Statistiques Descriptives",
            "Machine Learning",
        ],
        icons=["house", "chart-line", "table", "robot"],
        default_index=0,
        # orientation="horizontal",
    )

if selected == "Accueil":
    home_page()
elif selected == "Dashboard":
    dashboard_page()
elif selected == "Statistiques Descriptives":
    stat_des_page()
elif selected == "Machine Learning":
    ml_page()
