import streamlit as st


def dashboard_page():
    """
    Renders the Dashboard page
    """
    st.markdown("# Page Dashboard résumant les stats principales")
    st.write("Nb de flux rejetés et autorisés, filtre par plage de ports")
