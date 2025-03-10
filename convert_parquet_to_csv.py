import os
import pandas as pd

# Charger le fichier Parquet
df = pd.read_parquet("donnees_exemple/log_export.parquet")

# Remplacer les NaN par NULL pour compatibilité avec PostgreSQL
df = df.where(pd.notna(df), None)

# Sauvegarder en CSV
df.to_csv("donnees_exemple/log_export.csv", index=False)

# desinstaller le fichier parquet
os.remove("donnees_exemple/log_export.parquet")
