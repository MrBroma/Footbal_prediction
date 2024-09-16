import os
import re
import pandas as pd

# Liste des colonnes à conserver
columns_to_keep = [
    "Div", "Date", "Time", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR",
    "HTHG", "HTAG", "HTR", "HS", "AS", "HST", "AST", "HF", "AF",
    "HC", "AC", "HY", "AY", "HR", "AR", "AvgH", "AvgD", "AvgA"
]

def merge_sorting():
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")

    # Regex pour détecter les fichiers avec 4 chiffres dans leur nom (comme des années)
    pattern = re.compile(r'\d{4}')
    
    common_columns = []

    for filename in os.listdir(data_folder):
        # Filtrer uniquement les fichiers contenant exactement 4 chiffres
        if pattern.search(filename):
            filepath = os.path.join(data_folder, filename)
            df = pd.read_csv(filepath)
            if not common_columns:
                common_columns = list(df.columns)
            else:
                common_columns = [col for col in common_columns if col in df.columns]

    # Merge files
    dfs = []
    for filename in os.listdir(data_folder):
        # Filtrer uniquement les fichiers contenant exactement 4 chiffres
        if pattern.search(filename):
            filepath = os.path.join(data_folder, filename)
            df = pd.read_csv(filepath)
            dfs.append(df)

    # Sauvegarder les dfs dans un fichier CSV fusionné dans le dossier data
    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df = merged_df[common_columns]
    
    # Garder uniquement les colonnes spécifiées
    merged_df = merged_df[[col for col in columns_to_keep if col in merged_df.columns]]

    # Gérer les formats de date mélangés
    merged_df['Date'] = pd.to_datetime(merged_df['Date'], errors='coerce')

    # Trier les valeurs par Date et Heure dans l'ordre décroissant
    merged_df = merged_df.sort_values(by=['Date', 'Time'], ascending=False)

    # Sauvegarder le DataFrame trié dans un nouveau fichier CSV
    merged_df.to_csv(os.path.join(data_folder, 'final_data_sorted.csv'), index=False)
