import streamlit as st
from streamlit_option_menu import option_menu

from views.home import home_page
from views.exploration import exploration_page
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
            "Exploration des Données",
            "Statistiques Descriptives",
            "Machine Learning",
        ],
        icons=["house", "search", "bar-chart", "robot"],
        default_index=0,
    )

if selected == "Accueil":
    home_page()
if selected == "Exploration des Données":
    exploration_page()
elif selected == "Statistiques Descriptives":
    stat_des_page()
elif selected == "Machine Learning":
    ml_page()
