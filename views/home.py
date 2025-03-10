""" This module contains the "Home" page. """

import streamlit as st


def home_page():
    """
    Renders the Home page.
    """
    st.markdown("### 🏠 Accueil")

    st.markdown(
        """
        Bienvenue sur l'application de visualisation et d'analyse de flux réseau. 
        Cette application permet de visualiser les données de flux réseau, de générer des statistiques descriptives et de réaliser des analyses de Machine Learning.
        """
    )
