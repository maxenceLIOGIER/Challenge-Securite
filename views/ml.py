import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from sqlalchemy import create_engine


def ml_page():
    """
    Renders the Machine Learning page
    """

    # Connexion à la base de données PostgreSQL
    # def get_db_connection():
    #     engine = create_engine("postgresql://user:password@host:port/database")  # Remplace par tes identifiants
    #     return engine

    def load_data():
        data=pd.read_csv("/Users/pierrebourbon/Documents/GitHub/Challenge-Securite/data_test.csv")
        data = data.drop(columns=['Interface_out', 'divers'])
        return data

    data = load_data()
    st.title("Analyse des Logs avec Machine Learning")

    def display_isolation_forest_results():
        st.subheader("1 - Détection des comportements normaux et anormaux (Isolation Forest)")
        
        data["Anomalie_IF"] = data["isolation"].map({1: "Normal", -1: "Anormal"})
        
        fig = px.histogram(data, x="Anomalie_IF", title="Répartition des anomalies", color="Anomalie_IF")
        st.plotly_chart(fig)

    def display_dbscan_results():
        st.subheader("2 - Clustering des comportements (DBSCAN)")
        
        fig = px.histogram(data, x="cluster", title="Distribution des clusters", color="cluster")
        st.plotly_chart(fig)

    def cross_analysis():
        st.subheader("3 - Analyse croisée des résultats")
        
        cross_tab = pd.crosstab(data["Anomalie_IF"], data["cluster"])
        st.write("Tableau croisé des anomalies et clusters")
        st.dataframe(cross_tab)
        
        fig = px.imshow(cross_tab, text_auto=True, color_continuous_scale="Blues", title="Carte de chaleur des anomalies et clusters")
        st.plotly_chart(fig)

    def time_series_visualization():
        st.subheader("4 - Évolution des anomalies au fil du temps")
        data_sorted = data.sort_values(by="date")
        
        fig = px.line(data_sorted, x="date", y="isolation", markers=True, title="Série temporelle des anomalies")
        st.plotly_chart(fig)

    def cluster_exploration():
        st.subheader("Exploration des clusters")
        selected_cluster = st.selectbox("Sélectionner un cluster", sorted(data["cluster"].unique()))
        selected_action = st.selectbox("Sélectionner une action", sorted(data["action"].unique()))
        filtered_data = data[(data["cluster"] == selected_cluster) & (data["action"] == selected_action)]
        
        st.write("Détails des observations dans le cluster sélectionné")
        st.dataframe(filtered_data)
    
    display_isolation_forest_results()
    display_dbscan_results()
    cross_analysis()
    time_series_visualization()
    cluster_exploration()

    st.write("Cette analyse permet de comparer les résultats des deux méthodes et d'identifier les corrélations entre anomalies et clusters de comportement.")
