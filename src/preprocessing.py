import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

class PreProcessing:
    def __init__(self):
        self.le = LabelEncoder()
        self.ohe = OneHotEncoder(sparse_output=False)
        self.scaler = StandardScaler()

    def parse_dates(self, data):
        """Parse la colonne 'date' en format datetime et extraire les composants"""
        data['date'] = pd.to_datetime(data['date'])
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month
        data['day'] = data['date'].dt.day
        data['hour'] = data['date'].dt.hour
        data['minute'] = data['date'].dt.minute
        data['second'] = data['date'].dt.second
        return data

    def drop_columns(self, data, columns_to_drop):
        """Supprime les colonnes spécifiées"""
        return data.drop(columns=columns_to_drop)

    def drop_na(self, data):
        """Supprime les lignes avec des valeurs manquantes"""
        return data.dropna(axis=0)

    def encode_label(self, data, columns):
        """Encode les colonnes spécifiées avec LabelEncoder"""
        for col in columns:
            data[col] = self.le.fit_transform(data[col])
        return data

    def encode_one_hot(self, data, column):
        """Applique One Hot Encoding sur la colonne spécifiée"""
        encoded_cols = self.ohe.fit_transform(data[[column]])
        encoded_col_names = self.ohe.get_feature_names_out([column])
        encoded_df = pd.DataFrame(encoded_cols, columns=encoded_col_names)
        encoded_df.index = data.index
        data = pd.concat([data, encoded_df], axis=1)
        data = data.drop(columns=column)
        return data

    def standardize(self, data, columns):
        """Applique la standardisation sur les colonnes spécifiées"""
        for col in columns:
            data[col] = self.scaler.fit_transform(data[[col]])
        return data

    def preprocess(self, data):
        """Méthode complète pour le prétraitement des données"""
        # Parsing de la date
        data = self.parse_dates(data)
        data["year"] = data["year"].replace(2024, 2025)

        # Suppression des colonnes inutiles
        data = self.drop_columns(data, ['interface_out', 'divers'])

        # Suppression des lignes avec des valeurs manquantes
        data = self.drop_na(data)

        # Suppression de la colonne 'date'
        data = self.drop_columns(data, ['date'])

        # Encodage des colonnes avec LabelEncoder
        ip_proto_cols = ["ipsrc", "ipdst", "proto", "interface_in"]
        data = self.encode_label(data, ip_proto_cols)

        # Encodage One Hot sur la colonne 'action'
        data = self.encode_one_hot(data, 'action')

        # Standardisation des colonnes spécifiées
        list_std = ["portsrc", "portdst"]
        data = self.standardize(data, list_std)

        return data
