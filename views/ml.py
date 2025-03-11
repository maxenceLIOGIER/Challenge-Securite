import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from sqlalchemy import create_engine
from src.preprocessing import PreProcessing
from src.clustering import AnomalyClustering

#Initialisation 
prepro = PreProcessing()
models = AnomalyClustering()

def ml_page():
    """
    Renders the Machine Learning page
    """

    # Connexion à la base de données PostgreSQL
    # def get_db_connection():
    #     engine = create_engine("postgresql://user:password@host:port/database")  # Remplace par tes identifiants
    #     return engine

    def load_data():
        data=pd.read_csv("donnees_finales/data_final.csv")
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        return data

    #Chargement des données 
    data_brut = load_data()

    #Prétraitement des données 
    data_encode = prepro.preprocess(data_brut)

    #Prédiction des modèles 
    preds = models.fit(data_encode)

    #Concat data et preds 
    data = pd.concat([data_brut, preds], axis=1)

    st.title("Analyse des Logs avec Machine Learning")

    def display_isolation_forest_results():
        st.subheader("1 - Détection des comportements normaux et anormaux (Isolation Forest)")
        
        data["Anomalie_IF"] = data["isolation"].map({1: "Normal", -1: "Anormal"})
        
        fig = px.histogram(data, x="Anomalie_IF", title="Répartition des anomalies", color="Anomalie_IF")
        st.plotly_chart(fig)
        st.markdown("<br><br>", unsafe_allow_html=True)

    def display_dbscan_results():
        st.subheader("2 - Clustering des comportements (DBSCAN)")
        
        fig = px.histogram(data, x="cluster", title="Distribution des clusters", color="cluster")
        st.plotly_chart(fig)
        st.markdown("<br><br>", unsafe_allow_html=True)

    def cross_analysis():
        st.subheader("3 - Analyse croisée des résultats")
        
        cross_tab = pd.crosstab(data["Anomalie_IF"], data["cluster"])
        st.write("Tableau croisé des anomalies et clusters")
        st.dataframe(cross_tab)
        
        fig = px.imshow(cross_tab, text_auto=True, color_continuous_scale="Blues", title="Carte de chaleur des anomalies et clusters")
        st.plotly_chart(fig)
        st.markdown("<br><br>", unsafe_allow_html=True)

    def time_series_visualization():
        st.subheader("4 - Évolution des anomalies au fil du temps")
        data_sorted = data.sort_values(by="date")
        
        fig = px.line(data_sorted, x="date", y="isolation", markers=True, title="Série temporelle des anomalies")
        st.plotly_chart(fig)
        st.markdown("<br><br>", unsafe_allow_html=True)

    def cluster_exploration():
        st.subheader("5 - Exploration des clusters")
        st.write("Cette analyse permet de comparer les résultats des deux méthodes et d'identifier les corrélations entre anomalies et clusters de comportement.")
        selected_cluster = st.selectbox("Sélectionner un cluster", sorted(data["cluster"].unique()))
        filtered_data = data[data["cluster"] == selected_cluster]

        # Ajout de filtres interactifs avec option "Tout sélectionner"
        all_ipsrc = ["Tout sélectionner"] + sorted(filtered_data["ipsrc"].unique())
        selected_ipsrc = st.multiselect("Filtrer par IP Source", all_ipsrc, default="Tout sélectionner")
        if "Tout sélectionner" in selected_ipsrc:
            selected_ipsrc = filtered_data["ipsrc"].unique()

        all_proto = ["Tout sélectionner"] + sorted(filtered_data["proto"].unique())
        selected_proto = st.multiselect("Filtrer par Protocole", all_proto, default="Tout sélectionner")
        if "Tout sélectionner" in selected_proto:
            selected_proto = filtered_data["proto"].unique()

        all_action = ["Tout sélectionner"] + sorted(filtered_data["action"].unique())
        selected_action = st.multiselect("Filtrer par Action", all_action, default="Tout sélectionner")
        if "Tout sélectionner" in selected_action:
            selected_action = filtered_data["action"].unique()
        
        # Appliquer les filtres
        filtered_data = filtered_data[
            (filtered_data["ipsrc"].isin(selected_ipsrc)) &
            (filtered_data["proto"].isin(selected_proto)) &
            (filtered_data["action"].isin(selected_action))
        ]
        
        # Compteur d'observations
        st.write(f"Nombre d'observations : {filtered_data.shape[0]}")

        st.write("Détails des observations dans le cluster sélectionné")
        st.dataframe(filtered_data)

        # Carte de chaleur des IPs sources et destinations suspectes
        st.subheader("Carte de chaleur des IPs suspectes")
        heatmap_data = filtered_data.groupby(["ipsrc", "ipdst"]).size().reset_index(name="count")
        fig = px.density_heatmap(heatmap_data, x="ipsrc", y="ipdst", z="count", color_continuous_scale="Inferno")
        st.plotly_chart(fig)

        # Diagramme en cordes pour visualiser les connexions
        st.subheader("Visualisation des connexions entre IPs et ports")
        fig = px.sunburst(filtered_data, path=["ipsrc", "ipdst", "portdst"], values=None, title="Flux réseau suspect")
        st.plotly_chart(fig)

    display_isolation_forest_results()
    display_dbscan_results()
    cross_analysis()
    time_series_visualization()
    cluster_exploration()
