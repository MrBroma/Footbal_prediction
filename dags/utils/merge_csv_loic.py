import os
import pandas as pd

def merge():
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")

    # find the common columns in all csv files from data folder and put it in a list to preserve the column order
    common_columns = []
    for filename in os.listdir(data_folder):
        filepath = os.path.join(data_folder, filename)
        df = pd.read_csv(filepath)
        if not common_columns:
            common_columns = list(df.columns)
        else:
            common_columns = [col for col in common_columns if col in df.columns]

    # Merge file
    dfs = []
    for filename in os.listdir(data_folder):
        filepath = os.path.join(data_folder, filename)
        df = pd.read_csv(filepath)
        dfs.append(df)

    # save dfs into a merge csv file in data folder
    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df = merged_df[common_columns]
    merged_filepath = os.path.join(data_folder, "merge.csv")
    merged_df.to_csv(merged_filepath, index=False)
    print(f"Merged file saved as merge.csv in data folder")

