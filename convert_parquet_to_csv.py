import os
import pandas as pd

# Charger le fichier Parquet
df = pd.read_parquet("donnees_finales/logs_processed.parquet")

# Remplacer les NaN par NULL pour compatibilité avec PostgreSQL
df = df.where(pd.notna(df), None)

# Conversion des colonnes
df["year"] = df["date"].dt.year.astype(str)
df["month"] = df["date"].dt.month.astype(str)
df["day"] = df["date"].dt.day.astype(str)
df["timestamp"] = df["date"].dt.time
df["rule"] = df["rule"].astype(str)


# Fonction de catégorisation des ports
def categorize_port(port):
    """
    catégorise les ports en fonction de leur plage selon la RFC 6056
    """
    if port < 1024:
        return "well-known"
    elif port < 49152:
        return "Registered"
    else:
        return "Dynamic"


df["portsrc_range"] = df["portsrc"].apply(categorize_port)
df["portdst_range"] = df["portdst"].apply(categorize_port)

# Sauvegarder en CSV
df.to_csv("donnees_finales/logs_processed.csv", index=False)

# # desinstaller le fichier parquet
# os.remove("donnees_finales/logs_processed.parquet")
