import streamlit as st


def stat_des_page():
    """
    Renders the Descriptive Statistics page
    """
    st.markdown("# Page de statistiques descriptives")

    st.write("Tableau de données")
    st.write(
        "Colonnes : IP Source, Port, Type de flux (rejeté/autorisé), Date et heure, etc."
    )
    st.write("Statistiques détaillées")
    st.write("Nombre d'occurrences pour chaque IP source contactée.")
    st.write("Répartition des flux rejetés et autorisés par IP source.")
    st.write("Graphiques détaillés")
    st.write("Histogramme des occurrences des IP sources.")
    st.write("Graphique en secteurs des types de flux par IP source.")
    st.write("Filtres avancés")
    st.write("Permet de filtrer les données par plages de dates, types de flux, etc.")
