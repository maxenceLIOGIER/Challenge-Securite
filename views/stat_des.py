import psycopg2
import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


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

    # Se connecter à la base de données SQLite
    MAX_RETRIES = 10  # Nombre maximum de tentatives
    WAIT_SECONDS = 2  # Temps d'attente entre chaque tentative

    for i in range(MAX_RETRIES):
        try:
            conn = psycopg2.connect(
                host="postgres",
                database="challenge_secu",
                user="admin",
                password="admin",
                port=5432,
            )
            print("Connexion réussie à PostgreSQL !")
            break  # Sort de la boucle dès que la connexion est établie
        except psycopg2.OperationalError:
            st.write(
                f"🔄 Tentative {i+1}/{MAX_RETRIES} : PostgreSQL n'est pas encore prêt..."
            )
            time.sleep(WAIT_SECONDS)
    else:
        st.write("Impossible de se connecter à PostgreSQL après plusieurs tentatives.")
        exit(1)

    query = "SELECT * FROM logs ORDER BY RANDOM() LIMIT 100000;"
    # on échantillonne pour des raisons de performance
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Créer un piechart pour 'proto'
    proto_counts = df["proto"].value_counts()
    fig_proto = go.Figure(
        data=[go.Pie(labels=proto_counts.index, values=proto_counts.values)],
        layout=go.Layout(title="Répartition des protocoles", width=600, height=400),
    )

    # Créer un graphique en secteurs pour 'action'
    action_counts = df["action"].value_counts()
    fig_action = go.Figure(
        data=[go.Pie(labels=action_counts.index, values=action_counts.values)],
        layout=go.Layout(title="Répartition des actions", width=600, height=400),
    )

    # Afficher les graphiques dans Streamlit côte à côte
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_proto)
    with col2:
        st.plotly_chart(fig_action)
