import streamlit as st


def stat_des_page():
    """
    Renders the Descriptive Statistics page
    """
    st.markdown("### Page de statistiques descriptives")

    st.markdown(" ## Tableau de données")
    st.markdown(
        " ## Colonnes : IP Source, Port, Type de flux (rejeté/autorisé), Date et heure, etc."
    )
    st.markdown(" ## Statistiques détaillées")
    st.markdown(" ## Nombre d'occurrences pour chaque IP source contactée.")
    st.markdown(" ## Répartition des flux rejetés et autorisés par IP source.")
    st.markdown(" ## Graphiques détaillés")
    st.markdown(" ## Histogramme des occurrences des IP sources.")
    st.markdown(" ## Graphique en secteurs des types de flux par IP source.")
    st.markdown(" ## Filtres avancés")
    st.markdown(
        " ## Permet de filtrer les données par plages de dates, types de flux, etc."
    )
