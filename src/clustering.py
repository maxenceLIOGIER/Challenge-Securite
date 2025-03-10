from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import pandas as pd

class AnomalyClustering:
    def __init__(self, n_estimators=500, eps=10, min_samples=20):
        """
        Initialise les modèles avec les paramètres spécifiés.
        """
        self.model_IF = IsolationForest(n_estimators=n_estimators, random_state=42)
        self.model_DB = DBSCAN(eps=eps, min_samples=min_samples)

    def fit(self, data):
        """
        Entraîne IsolationForest et DBSCAN sur les données et retourne les labels.
        
        :param data: DataFrame contenant les données prétraitées
        :return: DataFrame contenant les labels des clusters DBSCAN et les prédictions de l'Isolation Forest
        """
        # Entraînement Isolation Forest
        data['IF_pred'] = self.model_IF.fit_predict(data)

        # Entraînement DBSCAN
        data['DBSCAN_cluster'] = self.model_DB.fit_predict(data)

        return data[['IF_pred', 'DBSCAN_cluster']]
